#!/usr/bin/env python3
"""Export blind A/B answers and grading templates. Do not expose assignment.json to judges."""
import argparse
import json
from pathlib import Path


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("iteration_dir")
    args = p.parse_args()
    root = Path(args.iteration_dir)
    manifest = read_json(root / "manifest.json")
    prepared, missing = 0, 0
    for name in manifest["cases"]:
        case = root / name
        metadata = read_json(case / "eval_metadata.json")
        learning = "L" in metadata["expected_route"]
        deep_read = "deep_read_eval" in metadata
        if not (learning or deep_read):
            continue
        pair_dir = case / "pairwise"
        assignment = read_json(pair_dir / "assignment.json")
        if set(assignment) != {"A", "B"} or set(assignment.values()) != {"with_skill", manifest["baseline"]}:
            raise SystemExit(f"{name}: invalid blind assignment")
        paths = {side: case / variant / "outputs" / "response.md" for side, variant in assignment.items()}
        if not all(path.is_file() for path in paths.values()):
            missing += 1
            continue
        # Both answers are assessed against the exact same Rubric, unseen by the generator.
        template = read_json(case / "with_skill" / "grading.template.json")
        for side, source in paths.items():
            (pair_dir / f"{side}.md").write_bytes(source.read_bytes())
            (pair_dir / f"{side}.grading.template.json").write_text(
                json.dumps(template, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
        contract = metadata["learning_eval"] if learning else metadata["deep_read_eval"]
        judge_packet = {
            "skill": "Learning" if learning else "Deep Read",
            "prompt": metadata["prompt"],
            "files": metadata["files"],
            "failure_mode": contract["failure_mode"],
            "rubric": contract["rubric"],
            "critical_failures": contract["critical_failures"],
            "not_required": contract["not_required"],
        }
        if deep_read:
            judge_packet["compression_mode"] = contract["compression_mode"]
            if "R" in metadata["expected_route"]:
                judge_packet["grading_scope"] = "Only grade the Deep Read part; Review is checked separately."
        (pair_dir / "judge_packet.json").write_text(
            json.dumps(judge_packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        prepared += 1
    print(f"Prepared {prepared} blind rubric pairs (Learning / Deep Read); {missing} pairs missing a response")
    print("Disclose only A.md, B.md, judge_packet.json, required fixtures and grading templates.")
    print("DO NOT disclose assignment.json, model identity, filenames indicating variants, or prior scores.")


if __name__ == "__main__":
    main()
