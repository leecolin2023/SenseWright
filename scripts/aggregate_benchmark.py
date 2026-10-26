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
    return {"score": score, "critical_count": observed}, None


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
    per_case = []
    learning_total = 0
    pairwise = {"with_skill": 0, baseline: 0, "tie": 0, "graded": 0}

    for variant in configs:
        summary[variant] = {
            "learning_graded": 0, "learning_total": 0, "learning_scores": [],
            "learning_critical_cases": 0, "learning_ungraded": [],
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
        if learning:
            learning_total += 1
            winner = pair_result(case_dir, baseline)
            if winner is not None:
                pairwise[winner] += 1
                pairwise["graded"] += 1
        else:
            winner = None
        case_item = {"case": name, "learning": learning, "primary_rule": metadata.get("learning_eval", {}).get("primary_rule"), "pairwise_winner": winner, "variants": {}}
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
                    case_item["variants"][variant] = {"graded": True, **result, "preflight": status}
                    rule = metadata["learning_eval"]["primary_rule"]
                    bucket = rule_results.setdefault(rule, {}).setdefault(variant, [])
                    bucket.append(result["score"])
            else:
                result = grade_legacy(grade, metadata["assertions"]) if grade else None
                if result:
                    s["legacy_graded_cases"] += 1
                    s["legacy_passed"] += result["passed"]
                    s["legacy_total"] += result["total"]
                case_item["variants"][variant] = {"graded": result is not None, **(result or {})}
        per_case.append(case_item)
    for variant, s in summary.items():
        s["learning_score_mean_10"] = mean(s.pop("learning_scores"))
        s["tokens_mean"] = mean(s.pop("tokens"))
        s["duration_ms_mean"] = mean(s.pop("duration_ms"))
        s["legacy_assertion_pass_rate"] = s["legacy_passed"] / s["legacy_total"] if s["legacy_total"] else None
    by_rule = {rule: {variant: {"graded": len(rule_results.get(rule, {}).get(variant, [])), "mean_score_10": mean(rule_results.get(rule, {}).get(variant, []))} for variant in configs} for rule in sorted(rule_results)}
    benchmark = {
        "schema_version": "0.2", "iteration": manifest["iteration"],
        "baseline": baseline, "learning_case_count": learning_total,
        "configs": summary, "learning_by_primary_rule": by_rule,
        "pairwise": {**pairwise, "ungraded": learning_total - pairwise["graded"]},
        "cases": per_case,
        "interpretation": "Scores require independent blind evidence; absent data are ungraded. Preflight unverified is not proof of failure. No automatic LLM calls or grading occurred.",
    }
    (root / "benchmark.json").write_text(json.dumps(benchmark, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        f"# Evaluation iteration {manifest['iteration']} — rubric + blind pairwise",
        "",
        "This report only aggregates **supplied actual results**. Missing/unverified entries are not failures.",
        "",
        "| Variant | Learning graded/total | Mean rubric score /10 | Critical cases | D/R→L verified |",
        "|---|---:|---:|---:|---:|",
    ]
    for variant, s in summary.items():
        score = f"{s['learning_score_mean_10']:.2f}" if s["learning_score_mean_10"] is not None else "n/a"
        lines.append(f"| {variant} | {s['learning_graded']}/{s['learning_total']} | {score} | {s['learning_critical_cases']} | {s['preflight']['verified']} |")
    lines += [
        "",
        "## Blind pairwise preference",
        "",
        f"Validated pairs: {pairwise['graded']}/{learning_total}; with_skill wins: {pairwise['with_skill']}; "
        f"{baseline} wins: {pairwise[baseline]}; ties: {pairwise['tie']}; missing: {learning_total-pairwise['graded']}.",
        "",
        "## Scores by primary Learning rule",
        "",
        "| Rule | with_skill graded / mean | baseline graded / mean |",
        "|---|---:|---:|",
    ]
    for rule, values in by_rule.items():
        def shown(variant):
            item = values[variant]
            return str(item["graded"]) + " / " + (f"{item['mean_score_10']:.2f}" if item["mean_score_10"] is not None else "n/a")
        lines.append(f"| {rule} | {shown('with_skill')} | {shown(baseline)} |")
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
    print(f"Wrote {root / 'benchmark.json'} and benchmark.md; paired reviews: {pairwise['graded']}/{learning_total}")


if __name__ == "__main__":
    main()
