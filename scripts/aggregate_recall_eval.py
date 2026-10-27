#!/usr/bin/env python3
"""Aggregate source-blind reading probes and declared recall traces; no model calls or auto-grading."""
import argparse
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def reviewer_ok(value, *, reader=False):
    if not isinstance(value, dict) or not isinstance(value.get("id"), str) or not value["id"].strip():
        return False
    if value.get("kind") not in {"human", "model"} or value.get("blind_to_variant") is not True:
        return False
    return value.get("source_blind") is True if reader else value.get("independent") is True


def valid_reader(record, probes):
    if not isinstance(record, dict) or not reviewer_ok(record.get("reader"), reader=True):
        return False
    answers = record.get("answers")
    return (
        isinstance(answers, list) and len(answers) == len(probes)
        and all(isinstance(item, dict)
                and item.get("question") == probe["question"]
                and isinstance(item.get("answer"), str) and bool(item["answer"].strip())
                for item, probe in zip(answers, probes))
    )


def valid_grade(record, probes, readers):
    if not isinstance(record, dict) or not reviewer_ok(record.get("reviewer")):
        return False
    if record["reviewer"]["id"] in {x["reader"]["id"] for x in readers.values()}:
        return False  # Reader and source-aware judge must be independent.
    checks = record.get("per_answer")
    if not isinstance(checks, dict) or set(checks) != {"A", "B"}:
        return False
    for side in ("A", "B"):
        entries = checks[side]
        if not isinstance(entries, list) or len(entries) != len(probes):
            return False
        for entry, probe in zip(entries, probes):
            if (
                not isinstance(entry, dict) or entry.get("question") != probe["question"]
                or type(entry.get("rating")) is not int or entry["rating"] not in (0, 1, 2)
                or not isinstance(entry.get("evidence"), str) or not entry["evidence"].strip()
            ):
                return False
    return True


def trace_state(case, candidate, frozen, source):
    trace = read(case / "targeted_recall" / "trace.json")
    if trace is None:
        return "unverified", None
    decision = trace.get("decision")
    if decision not in {"skip", "repair"} or not isinstance(trace.get("reason"), str) or not trace["reason"].strip():
        return "invalid", decision
    if decision == "skip":
        return ("declared_skip_unchanged" if candidate == frozen else "invalid_skip_changed"), decision
    spans = trace.get("source_spans_checked")
    regions = trace.get("edited_sections")
    if candidate == frozen or not isinstance(spans, list) or not spans:
        return "invalid_repair", decision
    if not isinstance(regions, list) or not regions:
        return "invalid_repair", decision
    if any(not isinstance(s, str) or len(s) < 5 or s not in source for s in spans):
        return "invalid_source_spans", decision
    return "declared_repair_with_source_spans", decision


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("iteration_dir")
    args = parser.parse_args()
    root = Path(args.iteration_dir)
    manifest = read(root / "manifest.json")
    if not manifest or manifest.get("suite") != "deep_read_targeted_recall":
        raise SystemExit("Invalid recall workspace manifest")
    records = []
    for name in manifest["cases"]:
        case = root / name
        ref = read(case / "judge_only" / "reference.json")
        mapping = read(case / "pairwise" / "assignment.json")
        if ref is None or mapping is None or set(mapping.values()) != {"control", "targeted_recall"}:
            raise SystemExit(f"{name}: invalid judge-only reference or A/B mapping")
        target = case / "targeted_recall" / "response.md"
        frozen = (case / "input" / "first_draft.md").read_text(encoding="utf-8")
        source = (case / "input" / "source.md").read_text(encoding="utf-8")
        output = target.read_text(encoding="utf-8") if target.is_file() else None
        trace, decision = trace_state(case, output, frozen, source) if output else ("unverified", None)
        item = {"case": name, "expected_gate": ref["expected_gate"], "decision": decision,
                "trace_status": trace, "scored": False}
        probes = ref["probes"]
        readers = {side: read(case / "pairwise" / f"{side}.reader_answers.json") for side in ("A", "B")}
        grade = read(case / "pairwise" / "grading.json")
        if output and all(valid_reader(readers[side], probes) for side in ("A", "B")) and valid_grade(grade, probes, readers):
            side_scores = {
                side: sum(c["rating"] for c in grade["per_answer"][side]) / len(probes)
                for side in ("A", "B")
            }
            inverted = {variant: side for side, variant in mapping.items()}
            base, new = side_scores[inverted["control"]], side_scores[inverted["targeted_recall"]]
            item.update(scored=True, score_control_0_2=base, score_recall_0_2=new, gain_0_2=new-base,
                        improved=new>base, regressed=new<base)
        records.append(item)
    graded = [x for x in records if x["scored"]]
    by_gate = {}
    for gate in ("repair", "skip"):
        group = [x for x in graded if x["expected_gate"] == gate]
        by_gate[gate] = {
            "scored": len(group),
            "mean_gain_0_2": statistics.mean(x["gain_0_2"] for x in group) if group else None,
            "improved": sum(x["improved"] for x in group),
            "regressed": sum(x["regressed"] for x in group),
        }
    outcome = {
        "schema": "recall-eval-0.1", "total": len(records), "scored": len(graded),
        "cases": records, "by_expected_gate": by_gate,
        "declared_unnecessary_repairs": sum(
            x["expected_gate"] == "skip" and x["decision"] == "repair" for x in records
        ),
        "declared_missed_repairs": sum(
            x["expected_gate"] == "repair" and x["decision"] == "skip" for x in records
        ),
        "limitations": (
            "No model generation or automatic grading. Blind/source-free reader responses and "
            "source-aware independent judge assessments must be supplied separately. "
            "A self-reported source span is not verified retrieval/tool trace."
        ),
    }
    (root / "recall-benchmark.json").write_text(json.dumps(outcome, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    lines = [
        "# Targeted Recall experiment",
        "",
        f"Independently scored: {len(graded)}/{len(records)}; unscored are **not failures**.",
        "",
        "| Case | Expected trigger | Declared decision | Trace | Reader gain /2 |",
        "|---|---|---|---|---:|",
    ]
    for item in records:
        gain = f"{item['gain_0_2']:+.2f}" if item["scored"] else "ungraded"
        lines.append(f"| {item['case']} | {item['expected_gate']} | {item['decision'] or 'missing'} | {item['trace_status']} | {gain} |")
    lines += [
        "", "## Outcome", "",
        f"Unnecessary declared repairs: {outcome['declared_unnecessary_repairs']}; "
        f"missed declared repairs: {outcome['declared_missed_repairs']}.",
        "",
        "Scores must come from source-blind readers and an independent source-aware judge. "
        "Missing grades are ungraded; trace is only an attested record, not independently verified tool usage.",
    ]
    (root / "recall-benchmark.md").write_text("\n".join(lines)+"\n", encoding="utf-8")
    print(f"Wrote recall-benchmark.json/md; independent grades: {len(graded)}/{len(records)}")


if __name__ == "__main__":
    main()
