#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import re

ROOT = Path(__file__).resolve().parents[1]

def slug(value):
    return re.sub(r"[^a-z0-9-]+", "-", value.lower()).strip("-")

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

    iteration = ROOT / args.workspace / f"iteration-{args.iteration}"
    iteration.mkdir(parents=True, exist_ok=True)
    manifest = {
        "iteration": args.iteration,
        "skill_name": "document-intelligence-suite",
        "baseline": args.baseline,
        "cases": []
    }

    for case in cases:
        name = slug(case["name"])
        case_dir = iteration / name
        for config in ("with_skill", args.baseline):
            (case_dir / config / "outputs").mkdir(parents=True, exist_ok=True)
        metadata = {
            "eval_id": case["id"],
            "eval_name": name,
            "prompt": case["prompt"],
            "files": case["files"],
            "expected_route": case["expected_route"],
            "expected_output": case["expected_output"],
            "assertions": case["assertions"]
        }
        (case_dir / "eval_metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8"
        )
        manifest["cases"].append(name)

    (iteration / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
    print(f"Created {iteration.relative_to(ROOT)} with {len(cases)} paired eval cases")

if __name__ == "__main__":
    main()
