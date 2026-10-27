#!/usr/bin/env python3
"""Static checks for frozen-draft selective Deep Read recall evals; never calls a model."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    data = json.loads((ROOT / "evals/recall/cases.json").read_text(encoding="utf-8"))
    baseline = json.loads((ROOT / "evals/evals.json").read_text(encoding="utf-8"))
    originals = {case["id"]: case for case in baseline["evals"]}
    errors, seen = [], set()
    gates, modes, rules = set(), set(), set()
    if data.get("suite_version") != "0.1" or data.get("design") != "frozen_first_draft_selective_repair":
        errors.append("Unsupported recall suite schema")
    for item in data.get("cases", []):
        cid = item.get("id")
        if not isinstance(cid, str) or not cid or cid in seen:
            errors.append(f"Duplicate/invalid recall ID: {cid}")
        seen.add(cid)
        parent = originals.get(item.get("parent_eval_id"))
        rule = item.get("rule")
        mode = item.get("mode")
        gate = item.get("expected_gate")
        gates.add(gate)
        modes.add(mode)
        rules.add(rule)
        if not parent or parent.get("deep_read_eval", {}).get("primary_rule") != rule:
            errors.append(f"{cid}: parent_eval_id must match original D02/D03 case")
        if not parent or parent.get("deep_read_eval", {}).get("compression_mode") != mode:
            errors.append(f"{cid}: compression mode differs from original test")
        if gate not in {"repair", "skip"} or rule not in {"D02", "D03"}:
            errors.append(f"{cid}: invalid gate or rule")
        if mode not in {"coverage_preserving", "cognitive_synthesis"}:
            errors.append(f"{cid}: invalid compression mode")
        if not isinstance(item.get("reading_goal"), str) or not item["reading_goal"].strip():
            errors.append(f"{cid}: missing reading_goal")
        source_path = ROOT / str(item.get("source_file", ""))
        draft_path = ROOT / str(item.get("draft_file", ""))
        if not source_path.is_file() or not draft_path.is_file():
            errors.append(f"{cid}: source/draft fixture missing")
            continue
        if item["source_file"] not in parent.get("files", []):
            errors.append(f"{cid}: source must match original case fixture")
        source = source_path.read_text(encoding="utf-8")
        draft = draft_path.read_text(encoding="utf-8")
        if not draft.strip():
            errors.append(f"{cid}: frozen first draft empty")
        anchors = item.get("source_anchors")
        if not isinstance(anchors, list) or not anchors or any(
            not isinstance(anchor, str) or anchor not in source for anchor in anchors
        ):
            errors.append(f"{cid}: anchors must be literal substrings of Raw Source")
        probes = item.get("probes")
        if not isinstance(probes, list) or not probes:
            errors.append(f"{cid}: missing blind reader probes")
            continue
        for probe in probes:
            if not isinstance(probe.get("question"), str) or not probe["question"].strip():
                errors.append(f"{cid}: blank reader question")
            points = probe.get("key_points")
            if not isinstance(points, list) or not points or any(
                not isinstance(point, str) or not point.strip() for point in points
            ):
                errors.append(f"{cid}: empty judge-only key points")
    if gates != {"repair", "skip"} or rules != {"D02", "D03"}:
        errors.append("Both positive/negative and D02/D03 cases are required")
    if modes != {"coverage_preserving", "cognitive_synthesis"}:
        errors.append("Both Deep Read compression modes must be exercised")
    if errors:
        print("Targeted recall eval validation failed:")
        for err in errors:
            print(" -", err)
        return 1
    print(f"OK: {len(seen)} frozen-draft targeted recall cases; rules D02/D03, both modes and both gates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
