#!/usr/bin/env python3
"""Prepare task cases and EMPTY grading artifacts; does not call a model or judge."""
from pathlib import Path
import argparse
import json
import random
import re

ROOT = Path(__file__).resolve().parents[1]


def slug(value):
    return re.sub(r"[^a-z0-9-]+", "-", value.lower()).strip("-")


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--iteration", type=int, required=True)
    p.add_argument("--baseline", default="old_skill")
    p.add_argument("--workspace", default=".eval-workspace")
    args = p.parse_args()

    cases = json.loads((ROOT / "evals/evals.json").read_text(encoding="utf-8"))["evals"]
    baselines = json.loads((ROOT / "evals/baselines.json").read_text(encoding="utf-8"))["baselines"]
    if args.baseline not in {b["name"] for b in baselines}:
        raise SystemExit(f"Unknown baseline: {args.baseline}")
    if args.baseline == "with_skill":
        raise SystemExit("Baseline cannot be with_skill")

    iteration = ROOT / args.workspace / f"iteration-{args.iteration}"
    if (iteration / "manifest.json").exists():
        raise SystemExit("Existing iteration: choose a NEW iteration; never overwrite blind assignment")
    iteration.mkdir(parents=True, exist_ok=True)
    manifest = {
        "iteration": args.iteration,
        "eval_version": "0.2",
        "skill_name": "sensewright",
        "baseline": args.baseline,
        "cases": [],
    }
    for case in cases:
        name = slug(case["name"])
        case_dir = iteration / name
        metadata = {k: v for k, v in case.items() if k not in ("assertions",)}
        if "L" not in case["expected_route"]:
            metadata["assertions"] = case["assertions"]
        case_dir.mkdir(parents=True, exist_ok=True)
        dump(case_dir / "eval_metadata.json", metadata)

        for variant in ("with_skill", args.baseline):
            run_dir = case_dir / variant
            (run_dir / "outputs").mkdir(parents=True, exist_ok=True)
            if "L" in case["expected_route"]:
                contract = case["learning_eval"]
                grading = {
                    "reviewer": {"id": None, "kind": None, "independent": None, "blind_to_variant": None},
                    "criteria": [
                        {"id": criterion["id"], "rating": None, "evidence": None}
                        for criterion in contract["rubric"]
                    ],
                    "critical_failures": [
                        {"description": failure, "occurred": None, "evidence": None}
                        for failure in contract["critical_failures"]
                    ],
                    "notes": None,
                }
                dump(run_dir / "grading.template.json", grading)
                dump(run_dir / "preflight.template.json", {
                    "status": "unverified",
                    "trace_reference": None,
                    "notes": "Only actual D/R isolation & L handoff trace supports verified status",
                })
            else:
                dump(run_dir / "grading.template.json", {
                    "reviewer": {"id": None, "kind": None, "independent": None},
                    "expectations": [{"text": item, "passed": None, "evidence": None} for item in case["assertions"]],
                })
        if "L" in case["expected_route"]:
            pair = case_dir / "pairwise"
            pair.mkdir(exist_ok=True)
            variants = ["with_skill", args.baseline]
            random.Random(f"{args.iteration}:{case['id']}:sensewright").shuffle(variants)
            # Assignment is for evaluator orchestration, never provide it to the blind judge.
            dump(pair / "assignment.json", {"A": variants[0], "B": variants[1]})
            dump(pair / "vote.template.json", {
                "reviewer": {"id": None, "kind": None, "independent": None, "blind_to_variant": None},
                "winner": None,
                "evidence": None,
            })
        manifest["cases"].append(name)
    dump(iteration / "manifest.json", manifest)
    print(f"Prepared {iteration}: {len(cases)} cases; no outputs or scores generated")


if __name__ == "__main__":
    main()
