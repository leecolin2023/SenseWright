#!/usr/bin/env python3
"""Summarize actual graded runs. Missing grades are NOT scored as failures."""
import argparse
import json
import statistics
from pathlib import Path


def read_json(path):
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def mean(values):
    return statistics.mean(values) if values else None


def reviewer_valid(grade, require_blind=True):
    reviewer = grade.get("reviewer", {}) if isinstance(grade, dict) else {}
    return (
        isinstance(reviewer, dict)
        and isinstance(reviewer.get("id"), str)
        and bool(reviewer["id"].strip())
        and reviewer.get("kind") in ("human", "model")
        and reviewer.get("independent") is True
        and (reviewer.get("blind_to_variant") is True if require_blind else True)
    )


def grade_learning(grade, contract):
    if not reviewer_valid(grade):
        return None, "missing independent blind reviewer attribution"
    checks = grade.get("criteria")
    rubric = contract["rubric"]
    if not isinstance(checks, list) or len(checks) != len(rubric):
        return None, "incomplete rubric criteria"
    by_id = {item.get("id"): item for item in checks if isinstance(item, dict)}
    if set(by_id) != {entry["id"] for entry in rubric} or len(by_id) != len(checks):
        return None, "mismatched/duplicate rubric criterion IDs"
    score = 0.0
    for criterion in rubric:
        check = by_id[criterion["id"]]
        rating = check.get("rating")
        if type(rating) is not int or rating not in (0, 1, 2):
            return None, "criterion rating must be 0, 1, or 2"
        if not isinstance(check.get("evidence"), str) or not check["evidence"].strip():
            return None, "each criterion needs independent evidence"
        score += criterion["weight"] * rating / 2
    failure_check = grade.get("failure_mode_assessment")
    if not isinstance(failure_check, dict) or failure_check.get("description") != contract["failure_mode"]:
        return None, "missing rule failure-mode assessment"
    failure_occurred = failure_check.get("occurred")
    severity = failure_check.get("severity")
    if type(failure_occurred) is not bool:
        return None, "rule failure-mode occurrence must be true or false"
    if severity not in (("minor", "major", "critical") if failure_occurred else ("none",)):
        return None, "rule failure-mode severity inconsistent with occurrence"
    if failure_occurred and not isinstance(failure_check.get("evidence"), str):
        return None, "rule failure-mode needs evidence"
    if failure_occurred and not failure_check["evidence"].strip():
        return None, "rule failure-mode evidence cannot be empty"
    failures = grade.get("critical_failures")
    expected = contract["critical_failures"]
    if not isinstance(failures, list) or len(failures) != len(expected):
        return None, "critical failure review missing"
    observed = 0
    for item, name in zip(failures, expected):
        if not isinstance(item, dict) or item.get("description") != name or type(item.get("occurred")) is not bool:
            return None, "critical failure review malformed"
        if item["occurred"]:
            observed += 1
            if not isinstance(item.get("evidence"), str) or not item["evidence"].strip():
                return None, "critical failure requires concrete evidence"
    return {"score": score, "critical_count": observed, "failure_occurred": failure_occurred,
            "failure_severity": severity}, None


def grade_legacy(grade, assertions):
    if not isinstance(grade, dict) or not isinstance(grade.get("expectations"), list):
        return None
    items = grade["expectations"]
    if len(items) != len(assertions):
        return None
    if any(item.get("text") != expected or type(item.get("passed")) is not bool or not isinstance(item.get("evidence"), str) or not item["evidence"].strip()
           for item, expected in zip(items, assertions)):
        return None
    return {"passed": sum(item["passed"] for item in items), "total": len(items)}


def preflight_status(path):
    record = read_json(path)
    if record is None:
        return "unverified"
    status = record.get("status")
    if status in ("verified", "failed") and isinstance(record.get("trace_reference"), str) and record["trace_reference"].strip():
        return status
    return "unverified"


def pair_result(case_dir, baseline):
    pair_dir = case_dir / "pairwise"
    vote = read_json(pair_dir / "vote.json")
    assignment = read_json(pair_dir / "assignment.json")
    if not vote or not assignment:
        return None
    if set(assignment) != {"A", "B"} or set(assignment.values()) != {"with_skill", baseline}:
        return None
    if not reviewer_valid(vote) or vote.get("winner") not in ("A", "B", "tie"):
        return None
    if not isinstance(vote.get("evidence"), str) or not vote["evidence"].strip():
        return None
    if not (pair_dir / "A.md").is_file() or not (pair_dir / "B.md").is_file():
        return None
    return "tie" if vote["winner"] == "tie" else assignment[vote["winner"]]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("iteration_dir")
    args = p.parse_args()
    root = Path(args.iteration_dir)
    manifest = read_json(root / "manifest.json")
    if not manifest:
        raise SystemExit("manifest.json not found")
    baseline = manifest["baseline"]
    configs = ("with_skill", baseline)
    summary = {}
    rule_results = {}
    rule_pairs = {}
    paired_deltas = {}
    paired_failure_changes = {}
    rule_failure_counts = {}
    per_case = []
    learning_total = 0
    deep_read_total = 0
    deep_rule_results, deep_rule_pairs, deep_paired_deltas = {}, {}, {}
    deep_paired_failure_changes, deep_rule_failure_counts = {}, {}
    pairwise = {"with_skill": 0, baseline: 0, "tie": 0, "graded": 0}
    deep_pairwise = {"with_skill": 0, baseline: 0, "tie": 0, "graded": 0}

    for variant in configs:
        summary[variant] = {
            "learning_graded": 0, "learning_total": 0, "learning_scores": [],
            "learning_critical_cases": 0, "learning_failure_cases": 0, "learning_ungraded": [],
            "deep_read_graded": 0, "deep_read_total": 0, "deep_read_scores": [],
            "deep_read_critical_cases": 0, "deep_read_failure_cases": 0, "deep_read_ungraded": [],
            "preflight": {"verified": 0, "failed": 0, "unverified": 0},
            "legacy_passed": 0, "legacy_total": 0, "legacy_graded_cases": 0,
            "tokens": [], "duration_ms": [],
        }
    for name in manifest["cases"]:
        case_dir = root / name
        metadata = read_json(case_dir / "eval_metadata.json")
        if metadata is None:
            raise SystemExit(f"Missing metadata: {name}")
        learning = "L" in metadata["expected_route"]
        deep_read = "deep_read_eval" in metadata and not learning
        if learning:
            learning_total += 1
            winner = pair_result(case_dir, baseline)
            rule = metadata["learning_eval"]["primary_rule"]
            bucket = rule_pairs.setdefault(rule, {"with_skill": 0, baseline: 0, "tie": 0, "graded": 0})
            if winner is not None:
                pairwise[winner] += 1
                pairwise["graded"] += 1
                bucket[winner] += 1
                bucket["graded"] += 1
        elif deep_read:
            deep_read_total += 1
            winner = pair_result(case_dir, baseline)
            rule = metadata["deep_read_eval"]["primary_rule"]
            bucket = deep_rule_pairs.setdefault(rule, {"with_skill": 0, baseline: 0, "tie": 0, "graded": 0})
            if winner is not None:
                deep_pairwise[winner] += 1
                deep_pairwise["graded"] += 1
                bucket[winner] += 1
                bucket["graded"] += 1
        else:
            winner = None
        case_item = {
            "case": name, "learning": learning, "deep_read": deep_read,
            "primary_rule": (metadata.get("learning_eval") or metadata.get("deep_read_eval") or {}).get("primary_rule"),
            "pairwise_winner": winner, "variants": {},
        }
        for variant in configs:
            run = case_dir / variant
            s = summary[variant]
            grade = read_json(run / "grading.json")
            timing = read_json(run / "timing.json") or {}
            for field, target in (("total_tokens", "tokens"), ("duration_ms", "duration_ms")):
                val = timing.get(field)
                if isinstance(val, (int, float)) and not isinstance(val, bool) and val >= 0:
                    s[target].append(val)
            if learning:
                s["learning_total"] += 1
                status = preflight_status(run / "preflight.json")
                s["preflight"][status] += 1
                result, reason = grade_learning(grade, metadata["learning_eval"]) if grade else (None, "not graded")
                if result is None:
                    s["learning_ungraded"].append({"case": name, "reason": reason})
                    case_item["variants"][variant] = {"graded": False, "reason": reason, "preflight": status}
                else:
                    s["learning_graded"] += 1
                    s["learning_scores"].append(result["score"])
                    s["learning_critical_cases"] += int(result["critical_count"] > 0)
                    s["learning_failure_cases"] += int(result["failure_occurred"])
                    case_item["variants"][variant] = {"graded": True, **result, "preflight": status}
                    rule = metadata["learning_eval"]["primary_rule"]
                    bucket = rule_results.setdefault(rule, {}).setdefault(variant, [])
                    bucket.append(result["score"])
                    rule_failure_counts.setdefault(rule, {}).setdefault(variant, []).append(int(result["failure_occurred"]))
            elif deep_read:
                s["deep_read_total"] += 1
                result, reason = grade_learning(grade, metadata["deep_read_eval"]) if grade else (None, "not graded")
                if result is None:
                    s["deep_read_ungraded"].append({"case": name, "reason": reason})
                    case_item["variants"][variant] = {"graded": False, "reason": reason}
                else:
                    s["deep_read_graded"] += 1
                    s["deep_read_scores"].append(result["score"])
                    s["deep_read_critical_cases"] += int(result["critical_count"] > 0)
                    s["deep_read_failure_cases"] += int(result["failure_occurred"])
                    case_item["variants"][variant] = {"graded": True, **result}
                    rule = metadata["deep_read_eval"]["primary_rule"]
                    deep_rule_results.setdefault(rule, {}).setdefault(variant, []).append(result["score"])
                    deep_rule_failure_counts.setdefault(rule, {}).setdefault(variant, []).append(int(result["failure_occurred"]))
                if metadata.get("assertions"):
                    # D+R Review assertions require their own separate grading record.
                    review_grade = read_json(run / "review.grading.json")
                    review_result = grade_legacy(review_grade, metadata["assertions"]) if review_grade else None
                    if review_result:
                        s["legacy_graded_cases"] += 1
                        s["legacy_passed"] += review_result["passed"]
                        s["legacy_total"] += review_result["total"]
                    case_item["variants"][variant]["review_assertions_graded"] = review_result is not None
            else:
                result = grade_legacy(grade, metadata["assertions"]) if grade else None
                if result:
                    s["legacy_graded_cases"] += 1
                    s["legacy_passed"] += result["passed"]
                    s["legacy_total"] += result["total"]
                case_item["variants"][variant] = {"graded": result is not None, **(result or {})}
        if learning:
            a = case_item["variants"]["with_skill"]
            b = case_item["variants"][baseline]
            if a["graded"] and b["graded"]:
                rule = metadata["learning_eval"]["primary_rule"]
                paired_deltas.setdefault(rule, []).append(a["score"] - b["score"])
                change = "reduced" if b["failure_occurred"] and not a["failure_occurred"] else (
                    "regressed" if a["failure_occurred"] and not b["failure_occurred"] else "unchanged"
                )
                paired_failure_changes.setdefault(rule, {"reduced": 0, "regressed": 0, "unchanged": 0})[change] += 1
        elif deep_read:
            a = case_item["variants"]["with_skill"]
            b = case_item["variants"][baseline]
            if a["graded"] and b["graded"]:
                rule = metadata["deep_read_eval"]["primary_rule"]
                deep_paired_deltas.setdefault(rule, []).append(a["score"] - b["score"])
                change = "reduced" if b["failure_occurred"] and not a["failure_occurred"] else (
                    "regressed" if a["failure_occurred"] and not b["failure_occurred"] else "unchanged"
                )
                deep_paired_failure_changes.setdefault(rule, {"reduced": 0, "regressed": 0, "unchanged": 0})[change] += 1
        per_case.append(case_item)
    for variant, s in summary.items():
        s["learning_score_mean_10"] = mean(s.pop("learning_scores"))
        s["deep_read_score_mean_10"] = mean(s.pop("deep_read_scores"))
        s["tokens_mean"] = mean(s.pop("tokens"))
        s["duration_ms_mean"] = mean(s.pop("duration_ms"))
        s["legacy_assertion_pass_rate"] = s["legacy_passed"] / s["legacy_total"] if s["legacy_total"] else None
    by_rule = {
        rule: {
            "variants": {
                variant: {
                    "graded": len(rule_results.get(rule, {}).get(variant, [])),
                    "mean_score_10": mean(rule_results.get(rule, {}).get(variant, [])),
                    "failure_cases": sum(rule_failure_counts.get(rule, {}).get(variant, [])),
                }
                for variant in configs
            },
            "paired_comparisons": len(paired_deltas.get(rule, [])),
            "paired_mean_delta_10": mean(paired_deltas.get(rule, [])),
            "paired_failure_changes": paired_failure_changes.get(rule, {"reduced": 0, "regressed": 0, "unchanged": 0}),
            "pairwise": rule_pairs.get(rule, {"with_skill": 0, baseline: 0, "tie": 0, "graded": 0}),
        }
        for rule in sorted(set(rule_pairs) | set(rule_results))
    }
    deep_by_rule = {
        rule: {
            "variants": {
                variant: {
                    "graded": len(deep_rule_results.get(rule, {}).get(variant, [])),
                    "mean_score_10": mean(deep_rule_results.get(rule, {}).get(variant, [])),
                    "failure_cases": sum(deep_rule_failure_counts.get(rule, {}).get(variant, [])),
                }
                for variant in configs
            },
            "paired_comparisons": len(deep_paired_deltas.get(rule, [])),
            "paired_mean_delta_10": mean(deep_paired_deltas.get(rule, [])),
            "paired_failure_changes": deep_paired_failure_changes.get(
                rule, {"reduced": 0, "regressed": 0, "unchanged": 0}
            ),
            "pairwise": deep_rule_pairs.get(rule, {"with_skill": 0, baseline: 0, "tie": 0, "graded": 0}),
        }
        for rule in sorted(set(deep_rule_pairs) | set(deep_rule_results))
    }
    benchmark = {
        "schema_version": "0.3", "iteration": manifest["iteration"],
        "baseline": baseline, "learning_case_count": learning_total,
        "deep_read_case_count": deep_read_total,
        "configs": summary, "learning_by_primary_rule": by_rule,
        "deep_read_by_primary_rule": deep_by_rule,
        "pairwise": {**pairwise, "ungraded": learning_total - pairwise["graded"]},
        "deep_read_pairwise": {**deep_pairwise, "ungraded": deep_read_total - deep_pairwise["graded"]},
        "cases": per_case,
        "interpretation": "Scores require independent blind evidence; absent data are ungraded. Preflight unverified is not proof of failure. No automatic LLM calls or grading occurred.",
    }
    (root / "benchmark.json").write_text(json.dumps(benchmark, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        f"# Evaluation iteration {manifest['iteration']} — rubric + blind pairwise",
        "",
        "This report only aggregates **supplied actual results**. Missing/unverified entries are not failures.",
        "",
        "| Variant | Learning graded/total | Mean rubric score /10 | Rule failures | Critical cases | D/R→L verified |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for variant, s in summary.items():
        score = f"{s['learning_score_mean_10']:.2f}" if s["learning_score_mean_10"] is not None else "n/a"
        lines.append(f"| {variant} | {s['learning_graded']}/{s['learning_total']} | {score} | {s['learning_failure_cases']} | {s['learning_critical_cases']} | {s['preflight']['verified']} |")
    lines += [
        "",
        "## Blind pairwise preference",
        "",
        f"Validated pairs: {pairwise['graded']}/{learning_total}; with_skill wins: {pairwise['with_skill']}; "
        f"{baseline} wins: {pairwise[baseline]}; ties: {pairwise['tie']}; missing: {learning_total-pairwise['graded']}.",
        "",
        "## Scores by primary Learning rule",
        "",
        "| Rule | with_skill failure/graded | baseline failure/graded | Paired reduced/regressed | Rubric Δ /10 | Pairwise W/B/T |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for rule, values in by_rule.items():
        def shown(variant):
            item = values["variants"][variant]
            return str(item["graded"]) + " / " + (f"{item['mean_score_10']:.2f}" if item["mean_score_10"] is not None else "n/a")
        delta = values["paired_mean_delta_10"]
        delta_display = f"{delta:+.2f}" if delta is not None else "n/a"
        pairs = values["pairwise"]
        pair_display = f"{pairs['with_skill']} / {pairs[baseline]} / {pairs['tie']}"
        changes = values["paired_failure_changes"]
        change_display = f"{changes['reduced']} / {changes['regressed']}"
        a = values["variants"]["with_skill"]
        b = values["variants"][baseline]
        lines.append(
            f"| {rule} | {a['failure_cases']}/{a['graded']} | {b['failure_cases']}/{b['graded']} | "
            f"{change_display} | {delta_display} | {pair_display} |"
        )
    lines += [
        "",
        "## Deep Read D02 / D03 rubric and blind comparison",
        "",
        "| Variant | Deep Read graded/total | Mean rubric score /10 | Rule failures | Critical cases |",
        "|---|---:|---:|---:|---:|",
    ]
    for variant, s in summary.items():
        score = f"{s['deep_read_score_mean_10']:.2f}" if s["deep_read_score_mean_10"] is not None else "n/a"
        lines.append(
            f"| {variant} | {s['deep_read_graded']}/{s['deep_read_total']} | {score} | "
            f"{s['deep_read_failure_cases']} | {s['deep_read_critical_cases']} |"
        )
    lines += [
        "",
        f"Deep Read blind pairs: {deep_pairwise['graded']}/{deep_read_total}; "
        f"with_skill wins {deep_pairwise['with_skill']}, {baseline} wins {deep_pairwise[baseline]}, "
        f"ties {deep_pairwise['tie']}; missing {deep_read_total-deep_pairwise['graded']}.",
        "",
        "| Rule | with_skill failures/graded | baseline failures/graded | Paired reduced/regressed | Rubric delta /10 | Pairwise W/B/T |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for rule, values in deep_by_rule.items():
        a = values["variants"]["with_skill"]
        b = values["variants"][baseline]
        changes = values["paired_failure_changes"]
        pair = values["pairwise"]
        delta = values["paired_mean_delta_10"]
        delta_text = f"{delta:+.2f}" if delta is not None else "n/a"
        lines.append(
            f"| {rule} | {a['failure_cases']}/{a['graded']} | {b['failure_cases']}/{b['graded']} | "
            f"{changes['reduced']}/{changes['regressed']} | {delta_text} | "
            f"{pair['with_skill']}/{pair[baseline]}/{pair['tie']} |"
        )
    lines += [
        "",
        "## Limitations",
        "",
        "- No model generation or independent grading is performed by this aggregator.",
        "- A rubric score measures assessed article quality, **not demonstrated learner mastery**.",
        "- Blindness/independence fields are reviewer attestations, not cryptographic proof.",
        "- Compare cost and latency only when timing data are available under comparable runtime conditions.",
    ]
    (root / "benchmark.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"Wrote {root / 'benchmark.json'} and benchmark.md; "
        f"Learning pairs: {pairwise['graded']}/{learning_total}; "
        f"Deep Read pairs: {deep_pairwise['graded']}/{deep_read_total}"
    )


if __name__ == "__main__":
    main()
