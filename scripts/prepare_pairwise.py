#!/usr/bin/env python3
"""Copy generated Learning answers into blind A/B files. Never expose assignment to judges."""
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
        if "L" not in metadata["expected_route"]:
            continue
        assignment = read_json(case / "pairwise" / "assignment.json")
        if set(assignment) != {"A", "B"} or set(assignment.values()) != {"with_skill", manifest["baseline"]}:
            raise SystemExit(f"{name}: invalid blind assignment")
        paths = {
            side: case / variant / "outputs" / "response.md"
            for side, variant in assignment.items()
        }
        if not all(path.is_file() for path in paths.values()):
            missing += 1
            continue
        for side, source in paths.items():
            # Blind judge receives only A.md, B.md, prompt/fixtures and rubric; never assignment.json.
            (case / "pairwise" / f"{side}.md").write_bytes(source.read_bytes())
        prepared += 1
    print(f"Prepared {prepared} blind Learning pairs; {missing} pairs missing a response")
    print("Give judges only pairwise/A.md, pairwise/B.md and the task rubric; hide assignment.json")


if __name__ == "__main__":
    main()
