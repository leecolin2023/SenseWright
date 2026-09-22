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
