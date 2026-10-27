#!/usr/bin/env python3
"""Resolve independent blind A/B grades to variants after judges submit their ratings."""
import argparse
import json
import shutil
from pathlib import Path
from aggregate_benchmark import grade_learning


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("iteration_dir")
    args = parser.parse_args()
    root = Path(args.iteration_dir)
    manifest = read(root / "manifest.json")
    imported, skipped = 0, 0
    for name in manifest["cases"]:
        case = root / name
        metadata = read(case / "eval_metadata.json")
        learning = "L" in metadata["expected_route"]
        if not (learning or "deep_read_eval" in metadata):
            continue
        contract = metadata["learning_eval"] if learning else metadata["deep_read_eval"]
        mapping = read(case / "pairwise" / "assignment.json")
        if set(mapping) != {"A", "B"} or set(mapping.values()) != {"with_skill", manifest["baseline"]}:
            raise SystemExit(f"{name}: invalid A/B assignment")
        for side, variant in mapping.items():
            source = case / "pairwise" / f"{side}.grading.json"
            dest = case / variant / "grading.json"
            if not source.is_file():
                skipped += 1
                continue
            result, error = grade_learning(read(source), contract)
            if error:
                raise SystemExit(f"{name} {side}: invalid independent grade: {error}")
            if dest.exists():
                raise SystemExit(f"{name}: existing {dest}; refusing to overwrite")
            shutil.copyfile(source, dest)
            imported += 1
    print(f"Imported {imported} independently scored answers; {skipped} ungraded answers remain")
    print("A/B mappings are disclosed only during this post-judging resolution step")


if __name__ == "__main__":
    main()
