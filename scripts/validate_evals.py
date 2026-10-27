#!/usr/bin/env python3
"""Validate evaluation assets only; does not run an LLM or grade its answers."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals"
RULES = {f"R{i:02d}" for i in range(16)}
DEEP_RULES = {"D02", "D03"}
PREFLIGHT = {
    "required_before_L": ["D", "R"],
    "source_policy": "same_raw_input_independent_contexts",
    "completion_barrier": "both_complete_before_L",
    "handoff": "mandatory_read_selective_use_scaffold_not_evidence",
    "output_policy": "integrated_learning_unless_explicit",
}
LEGACY_L_CONTRACTS = {
    "mechanism_mapping", "reality_calibration", "expected_calibration_kind",
    "problem_discovery", "domain_anchor",
}


def load(name):
    return json.loads((EVALS / name).read_text(encoding="utf-8"))


def present_text(value):
    return isinstance(value, str) and bool(value.strip())


def validate_learning(case, prefix, errors):
    contract = case.get("learning_eval")
    if not isinstance(contract, dict):
        errors.append(f"{prefix}: missing learning_eval")
        return None
    rule = contract.get("primary_rule")
    if rule not in RULES:
        errors.append(f"{prefix}: primary_rule must be R00–R15")
    related = contract.get("related_rules")
    if not isinstance(related, list) or any(r not in RULES or r == rule for r in related) or len(related) != len(set(related)):
        errors.append(f"{prefix}: invalid related_rules")
    if not present_text(contract.get("failure_mode")):
        errors.append(f"{prefix}: failure_mode must explain the concrete failure")
    if contract.get("grading_policy") != "independent_evidence_based_0_1_2_per_criterion":
        errors.append(f"{prefix}: unsupported grading_policy")
    if contract.get("pairwise_policy") != "blind_A_B_same_prompt_fixture_runtime":
        errors.append(f"{prefix}: unsupported pairwise_policy")
    if "assertions" in case:
        errors.append(f"{prefix}: Learning must use task rubric, not legacy assertions")
    if any(key in case for key in LEGACY_L_CONTRACTS):
        errors.append(f"{prefix}: obsolete Learning contract still present")
    for field in ("critical_failures", "not_required"):
        value = contract.get(field)
        if not isinstance(value, list) or not value or not all(map(present_text, value)):
            errors.append(f"{prefix}: {field} must contain concrete nonempty text")
    rubric = contract.get("rubric")
    if not isinstance(rubric, list) or len(rubric) != 3:
        errors.append(f"{prefix}: rubric must contain 3 concrete criteria")
    else:
        expected_weights = {"goal": 4, "mechanism": 4, "boundary": 2}
        ids = [item.get("id") for item in rubric if isinstance(item, dict)]
        for item in rubric:
            if not isinstance(item, dict) or item.get("id") not in expected_weights or item.get("weight") != expected_weights[item["id"]] or not present_text(item.get("criterion")):
                errors.append(f"{prefix}: invalid rubric criterion/weight")
        if set(ids) != set(expected_weights) or len(ids) != len(set(ids)):
            errors.append(f"{prefix}: rubric IDs must be goal/mechanism/boundary")
    if case.get("learning_preflight") != PREFLIGHT:
        errors.append(f"{prefix}: D/R→L runtime preflight contract absent or changed")
    return rule



def validate_deep_read(case, prefix, errors):
    contract = case.get("deep_read_eval")
    if not isinstance(contract, dict):
        errors.append(f"{prefix}: missing deep_read_eval")
        return None
    rule = contract.get("primary_rule")
    if rule not in DEEP_RULES:
        errors.append(f"{prefix}: deep_read primary_rule must be D02 or D03")
    related = contract.get("related_rules")
    if not isinstance(related, list) or any(r not in DEEP_RULES or r == rule for r in related) or len(related) != len(set(related)):
        errors.append(f"{prefix}: invalid deep_read related_rules")
    if contract.get("compression_mode") not in ("coverage_preserving", "cognitive_synthesis"):
        errors.append(f"{prefix}: missing/invalid Deep Read compression_mode")
    if not present_text(contract.get("failure_mode")):
        errors.append(f"{prefix}: Deep Read failure_mode must name a concrete observable failure")
    if contract.get("grading_policy") != "independent_evidence_based_0_1_2_per_criterion":
        errors.append(f"{prefix}: unsupported Deep Read grading_policy")
    if contract.get("pairwise_policy") != "blind_A_B_same_prompt_fixture_runtime":
        errors.append(f"{prefix}: unsupported Deep Read pairwise_policy")
    for field in ("critical_failures", "not_required"):
        value = contract.get(field)
        if not isinstance(value, list) or not value or not all(map(present_text, value)):
            errors.append(f"{prefix}: invalid deep_read {field}")
    rubric = contract.get("rubric")
    weights = {"task_fit": 3, "cognitive_value": 5, "integrity": 2}
    if not isinstance(rubric, list) or len(rubric) != len(weights):
        errors.append(f"{prefix}: deep_read rubric must contain 3 criteria")
    else:
        ids = [entry.get("id") for entry in rubric if isinstance(entry, dict)]
        if set(ids) != set(weights) or len(ids) != len(set(ids)):
            errors.append(f"{prefix}: deep_read rubric IDs invalid")
        for entry in rubric:
            if not isinstance(entry, dict) or entry.get("id") not in weights or entry.get("weight") != weights.get(entry.get("id")) or not present_text(entry.get("criterion")):
                errors.append(f"{prefix}: invalid deep_read rubric criterion/weight")
    if "L" in case.get("expected_route", []):
        errors.append(f"{prefix}: Deep Read standalone grading cannot be attached to D/R->L cases")
    if "assertions" in case and "R" not in case.get("expected_route", []):
        errors.append(f"{prefix}: pure Deep Read must use rubric, not legacy assertions")
    return rule


def main():
    errors = []
    data = load("evals.json")
    cases = data.get("evals", [])
    if data.get("eval_version") != "0.2":
        errors.append("evals.json: expected Eval V0.2")
    ids, names, covered, deep_covered, deep_modes = set(), set(), set(), set(), set()
    for case in cases:
        ident = case.get("id")
        prefix = f"eval {ident}"
        for field in ("id", "name", "prompt", "expected_route", "expected_output", "files"):
            if field not in case:
                errors.append(f"{prefix}: missing {field}")
        if ident in ids:
            errors.append(f"{prefix}: duplicate id")
        ids.add(ident)
        name = case.get("name")
        if name in names:
            errors.append(f"{prefix}: duplicate name")
        names.add(name)
        for field in ("name", "prompt", "expected_output"):
            if not present_text(case.get(field)):
                errors.append(f"{prefix}: missing/empty {field}")
        route = case.get("expected_route", [])
        if not isinstance(route, list) or not route or any(r not in {"D", "R", "L", "P"} for r in route):
            errors.append(f"{prefix}: invalid route")
            route = []
        if "L" in route:
            if route[:3] != ["D", "R", "L"]:
                errors.append(f"{prefix}: Learning requires D/R before L")
            rule = validate_learning(case, prefix, errors)
            if rule in RULES:
                covered.add(rule)
        else:
            if "learning_eval" in case or "learning_preflight" in case:
                errors.append(f"{prefix}: non-L case contains Learning contract")
            if "D" in route:
                rule = validate_deep_read(case, prefix, errors)
                if rule in DEEP_RULES:
                    deep_covered.add(rule)
                    if rule == "D03":
                        deep_modes.add(case["deep_read_eval"]["compression_mode"])
                # A combined D+R case retains legacy Review/cross-skill assertions.
                if "R" in route:
                    assertions = case.get("assertions")
                    if not isinstance(assertions, list) or not assertions or not all(map(present_text, assertions)):
                        errors.append(f"{prefix}: combined D+R case still needs Review assertions")
            else:
                if "deep_read_eval" in case:
                    errors.append(f"{prefix}: non-D case contains Deep Read contract")
                assertions = case.get("assertions")
                if not isinstance(assertions, list) or not assertions or not all(map(present_text, assertions)):
                    errors.append(f"{prefix}: non-D case needs assertions")
        for rel in case.get("files", []):
            if not (ROOT / rel).is_file():
                errors.append(f"{prefix}: missing fixture {rel}")
        refs = case.get("reference_context", [])
        if refs and not any(s in route for s in ("L", "P")):
            errors.append(f"{prefix}: reference_context only allowed for L or P")
        for ref in refs:
            if ref.get("source_skill") not in {"D", "R", "L", "P"} or not present_text(ref.get("purpose")) or not (ROOT / ref.get("file", "__missing__")).is_file():
                errors.append(f"{prefix}: invalid reference_context")
        gold = case.get("gold_review_units", [])
        if gold and "R" not in route:
            errors.append(f"{prefix}: gold_review_units requires R")
        seen = set()
        for unit in gold:
            if not present_text(unit.get("id")) or not present_text(unit.get("description")) or unit.get("id") in seen:
                errors.append(f"{prefix}: invalid/duplicate gold unit")
            seen.add(unit.get("id"))
    if covered != RULES:
        errors.append("Learning R00–R15 primary-rule coverage incomplete: " + str(sorted(RULES - covered)))
    if deep_covered != DEEP_RULES:
        errors.append("Deep Read D02/D03 primary-rule coverage incomplete: " + str(sorted(DEEP_RULES - deep_covered)))
    if deep_modes != {"coverage_preserving", "cognitive_synthesis"}:
        errors.append("Deep Read D03 must test both compression contracts")
    trigger = load("triggering.json").get("queries", [])
    positive = sum(q.get("should_trigger") is True for q in trigger)
    negative = sum(q.get("should_trigger") is False for q in trigger)
    if len(trigger) < 10 or not positive or not negative:
        errors.append("triggering.json: must include positive and negative cases")
    baseline = load("baselines.json").get("baselines", [])
    if not any(b.get("name") == "old_skill" and b.get("ref") for b in baseline):
        errors.append("baselines.json: old_skill baseline missing")
    if errors:
        print("Eval validation failed:")
        for error in errors:
            print("- " + error)
        return 1
    n_learning = sum("L" in c["expected_route"] for c in cases)
    n_deep = sum("deep_read_eval" in c for c in cases)
    print(f"OK: {len(cases)} task evals ({n_learning} Learning, {n_deep} Deep Read); "
          f"{len(trigger)} triggers ({positive} positive / {negative} negative); "
          f"{len(covered)} primary Learning and {len(deep_covered)} Deep Read rules covered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
