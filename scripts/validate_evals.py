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
        if any(x not in {"D", "R", "L", "P"} for x in case.get("expected_route", [])):
            errors.append(f"{prefix}: invalid expected_route")
        route = case.get("expected_route", [])
        if "L" in route:
            if route[:3] != ["D", "R", "L"]:
                errors.append(f"{prefix}: Learning must be preceded by D and R")
            expected_preflight = {
                "required_before_L": ["D", "R"],
                "source_policy": "same_raw_input_independent_contexts",
                "completion_barrier": "both_complete_before_L",
                "handoff": "mandatory_read_selective_use_scaffold_not_evidence",
                "output_policy": "integrated_learning_unless_explicit",
            }
            if case.get("learning_preflight") != expected_preflight:
                errors.append(f"{prefix}: missing or invalid Learning preflight contract")
        elif "learning_preflight" in case:
            errors.append(f"{prefix}: non-L case cannot set Learning preflight")
        if "source_learning" in case:
            errors.append(f"{prefix}: deprecated code-only source_learning contract")
        if "mechanism_mapping" in case:
            expected_mapping = {
                "research_order": "verify_original_material_and_behavior_before_modeling",
                "presentation_order": "problem_mechanism_realization_evidence_next_problem",
                "evidence": "minimal_verifiable_anchors_appropriate_to_medium",
                "contradictions": "revise_model_not_invent_implementation",
            }
            if "L" not in route or case.get("mechanism_mapping") != expected_mapping:
                errors.append(f"{prefix}: invalid Mechanism-to-Implementation Mapping contract")
            if not case.get("files"):
                errors.append(f"{prefix}: mechanism-mapping eval must have source fixtures")
        if "reality_calibration" in case or "expected_calibration_kind" in case:
            expected_calibration = {
                "mode": "conditional_domain_adaptive",
                "minimum_evidence": "decision_relevant",
                "source_boundary": "facts_assumptions_derivations_unknowns",
                "output": "plain_language_mechanism_first_no_forced_metrics",
            }
            supported_kinds = {
                "minimal_quantitative", "execution_trace", "workflow_state",
                "evidence_quality", "comparability", "skip",
            }
            if "L" not in route or case.get("reality_calibration") != expected_calibration:
                errors.append(f"{prefix}: invalid domain-adaptive Reality Calibration contract")
            kind = case.get("expected_calibration_kind")
            if kind not in supported_kinds:
                errors.append(f"{prefix}: invalid expected_calibration_kind")
            if kind != "skip" and not case.get("files"):
                errors.append(f"{prefix}: calibrated evidence case must have a fixture")
        if "problem_discovery" in case:
            expected_discovery = {
                "mode": "conditional",
                "question_test": "grounded_discriminating_user_aligned",
                "outcome": "select_revise_bound_or_preserve",
                "anti_pattern": "abstraction_is_not_depth",
            }
            discovery = case.get("problem_discovery", {})
            outcome = discovery.get("expected_outcome")
            if "L" not in route or {
                k: v for k, v in discovery.items() if k != "expected_outcome"
            } != expected_discovery or outcome not in {"reframe", "preserve"}:
                errors.append(f"{prefix}: invalid Problem Discovery contract")
            if outcome == "reframe" and not case.get("files"):
                errors.append(f"{prefix}: reframe eval must have raw evidence fixture")
        if not case.get("assertions"):
            errors.append(f"{prefix}: assertions must not be empty")
        for rel in case.get("files", []):
            if not (ROOT / rel).exists():
                errors.append(f"{prefix}: fixture does not exist: {rel}")

        references = case.get("reference_context", [])
        if references and not any(x in {"L", "P"} for x in case.get("expected_route", [])):
            errors.append(f"{prefix}: reference_context is only allowed when expected_route includes L or P")
        for ref in references:
            if ref.get("source_skill") not in {"D", "R", "L", "P"}:
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
