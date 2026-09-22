#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals"

def load(name):
    return json.loads((EVALS / name).read_text(encoding="utf-8"))

def main():
    errors = []
    data = load("evals.json")
    cases = data.get("evals", [])
    ids, names = set(), set()

    for case in cases:
        prefix = f"eval {case.get('id')}"
        for key in ("id", "name", "prompt", "expected_route", "expected_output", "files", "assertions"):
            if key not in case:
                errors.append(f"{prefix}: missing {key}")
        if case.get("id") in ids:
            errors.append(f"{prefix}: duplicate id")
        ids.add(case.get("id"))
        if case.get("name") in names:
            errors.append(f"{prefix}: duplicate name")
        names.add(case.get("name"))
        if any(x not in {"D", "R", "L", "Q"} for x in case.get("expected_route", [])):
            errors.append(f"{prefix}: invalid expected_route")
        if not case.get("assertions"):
            errors.append(f"{prefix}: assertions must not be empty")
        for rel in case.get("files", []):
            if not (ROOT / rel).exists():
                errors.append(f"{prefix}: fixture does not exist: {rel}")

        references = case.get("reference_context", [])
        if references and not any(x in {"L", "Q"} for x in case.get("expected_route", [])):
            errors.append(f"{prefix}: reference_context is only allowed when expected_route includes L or Q")
        for ref in references:
            if ref.get("source_skill") not in {"D", "R", "L", "Q"}:
                errors.append(f"{prefix}: invalid reference source_skill")
            rel = ref.get("file")
            if not rel or not (ROOT / rel).exists():
                errors.append(f"{prefix}: reference fixture does not exist: {rel}")
            if not ref.get("purpose"):
                errors.append(f"{prefix}: reference purpose is required")

        gold_units = case.get("gold_review_units", [])
        if gold_units and "R" not in case.get("expected_route", []):
            errors.append(f"{prefix}: gold_review_units is only allowed for Review evals")
        seen_units = set()
        for unit in gold_units:
            unit_id = unit.get("id")
            if not unit_id or not unit.get("description"):
                errors.append(f"{prefix}: each gold review unit needs id and description")
            if unit_id in seen_units:
                errors.append(f"{prefix}: duplicate gold review unit id: {unit_id}")
            seen_units.add(unit_id)

    trigger = load("triggering.json").get("queries", [])
    positives = sum(q.get("should_trigger") is True for q in trigger)
    negatives = sum(q.get("should_trigger") is False for q in trigger)
    if len(trigger) < 10 or positives == 0 or negatives == 0:
        errors.append("triggering.json: need positive and negative near-miss cases")

    baseline = load("baselines.json").get("baselines", [])
    if not any(b.get("name") == "old_skill" and b.get("ref") for b in baseline):
        errors.append("baselines.json: old_skill git baseline is required")

    if errors:
        print("Eval validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"OK: {len(cases)} task evals; {len(trigger)} trigger evals ({positives} positive / {negatives} negative)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
