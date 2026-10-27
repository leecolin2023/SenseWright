#!/usr/bin/env python3
"""Prepare a frozen-first-draft targeted-recall experiment; no model execution or grading."""
import argparse
import json
import random
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "evals/recall/cases.json"


def put_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def init(root):
    if (root / "manifest.json").exists():
        raise SystemExit("Existing recall iteration; do not overwrite blind assignments")
    root.mkdir(parents=True, exist_ok=True)
    cases = read_json(SUITE)["cases"]
    put_json(root / "manifest.json", {
        "suite": "deep_read_targeted_recall", "cases": [c["id"] for c in cases],
        "control": "frozen_first_draft", "candidate": "targeted_recall",
    })
    for case in cases:
        here = root / case["id"]
        inp = here / "input"
        inp.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / case["source_file"], inp / "source.md")
        shutil.copyfile(ROOT / case["draft_file"], inp / "first_draft.md")
        # Do not leak gates, answer keys or source anchors to the candidate generator.
        put_json(inp / "generator_packet.json", {
            "reading_goal": case["reading_goal"],
            "compression_mode": case["mode"],
            "source_file": "source.md",
            "frozen_first_draft": "first_draft.md",
            "instruction": (
                "以现有 Deep Read 初稿为基础，按 D02/D03 判断有无重大且可定位的"
                "理解缺口；仅在确有必要时定向回查原文并局部修复。"
                "已有充分解释时保持初稿不变；交付自然阅读正文，不输出检查报告。"
            ),
        })
        (here / "control").mkdir(exist_ok=True)
        shutil.copyfile(inp / "first_draft.md", here / "control" / "response.md")
        (here / "targeted_recall").mkdir(exist_ok=True)
        put_json(here / "targeted_recall" / "trace.template.json", {
            "decision": None,  # repair / skip; do not grade missing traces as success
            "reason": None,
            "source_spans_checked": [],  # original source text/paragraph references
            "edited_sections": [],  # target draft sections only
            "token_cost": None,
            "duration_ms": None,
        })
        put_json(here / "judge_only" / "reference.json", {
            "expected_gate": case["expected_gate"],
            "failure_type": case["failure_type"],
            "source_anchors": case["source_anchors"],
            "probes": case["probes"],
        })
        assigned = ["control", "targeted_recall"]
        random.Random(f"recall:{root.name}:{case['id']}").shuffle(assigned)
        put_json(here / "pairwise" / "assignment.json", {
            "A": assigned[0], "B": assigned[1]
        })
        put_json(here / "pairwise" / "vote.template.json", {
            "reviewer": {"id": None, "kind": None, "independent": None,
                         "blind_to_variant": None},
            "winner": None, "evidence": None,
        })
    print(f"Prepared {len(cases)} recall cases at {root} without generating or scoring answers")
    print("Candidate writer sees input/ ONLY; judge_only and assignment.json are hidden")


def pairwise(root):
    manifest = read_json(root / "manifest.json")
    prepared, missing = 0, 0
    for name in manifest["cases"]:
        here = root / name
        candidate = here / "targeted_recall" / "response.md"
        if not candidate.is_file() or not candidate.read_text(encoding="utf-8").strip():
            missing += 1
            continue
        assignment = read_json(here / "pairwise" / "assignment.json")
        for side, variant in assignment.items():
            shutil.copyfile(here / variant / "response.md", here / "pairwise" / f"{side}.md")
        reference = read_json(here / "judge_only" / "reference.json")
        put_json(here / "pairwise" / "reader_questions.json", {
            "questions": [x["question"] for x in reference["probes"]]
        })
        for side in ("A", "B"):
            put_json(here / "pairwise" / f"{side}.reader_answers.template.json", {
                "reader": {"id": None, "kind": None, "blind_to_variant": None,
                           "source_blind": None},
                "answers": [{"question": p["question"], "answer": None}
                            for p in reference["probes"]],
            })
        put_json(here / "pairwise" / "grading.template.json", {
            "reviewer": {"id": None, "kind": None, "independent": None,
                         "blind_to_variant": None},
            "per_answer": {
                side: [{"question": p["question"], "rating": None, "evidence": None}
                       for p in reference["probes"]]
                for side in ("A", "B")
            },
        })
        prepared += 1
    print(f"Prepared {prepared} anonymous pairs; {missing} missing candidate responses")
    print("Blind readers see A.md/B.md and reader_questions.json, NOT judge_only or assignment.json")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iteration", type=int, required=True)
    parser.add_argument("--workspace", default=".eval-recall-workspace")
    parser.add_argument("--prepare-pairwise", action="store_true")
    args = parser.parse_args()
    root = ROOT / args.workspace / f"iteration-{args.iteration}"
    if args.prepare_pairwise:
        pairwise(root)
    else:
        init(root)


if __name__ == "__main__":
    main()
