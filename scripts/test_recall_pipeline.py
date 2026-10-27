#!/usr/bin/env python3
"""Offline synthetic smoke test for selective recall; not an actual model/reader evaluation."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def invoke(script, *args):
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script), *map(str, args)],
        cwd=ROOT, check=True, capture_output=True, text=True,
    )


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    invoke("validate_recall_evals.py")
    with tempfile.TemporaryDirectory(prefix="sensewright-recall-test-") as temp:
        invoke("prepare_recall_eval.py", "--iteration", 1, "--workspace", temp)
        root = Path(temp) / "iteration-1"
        manifest = load(root / "manifest.json")
        assert len(manifest["cases"]) == 6
        assert set(manifest["cases"]) == {
            "recall-01", "recall-02",
            "recall-03", "recall-04",
            "recall-05", "recall-06",
        }
        # No generated outputs or grades must be mistaken for real results.
        invoke("aggregate_recall_eval.py", root)
        blank = load(root / "recall-benchmark.json")
        assert blank["scored"] == 0 and blank["total"] == 6
        positive = "recall-01"
        negative = "recall-04"
        for name in (positive, negative):
            case = root / name
            packet = load(case / "input" / "generator_packet.json")
            assert "expected_gate" not in packet and "probes" not in packet
            source = (case / "input" / "source.md").read_text(encoding="utf-8")
            draft = (case / "input" / "first_draft.md").read_text(encoding="utf-8")
            candidate = case / "targeted_recall" / "response.md"
            if name == positive:
                candidate.write_text(draft + "\n补充测试桩：不同公告任务需要不同检索动作。\n", encoding="utf-8")
                anchor = "概括这份公告"
                assert anchor in source
                trace = {
                    "decision": "repair", "reason": "Synthetic missing bridge",
                    "source_spans_checked": [anchor], "edited_sections": ["final paragraph"],
                }
            else:
                candidate.write_text(draft, encoding="utf-8")
                trace = {"decision": "skip", "reason": "Synthetic sufficient draft",
                         "source_spans_checked": [], "edited_sections": []}
            save(case / "targeted_recall" / "trace.json", trace)
        invoke("prepare_recall_eval.py", "--iteration", 1,
               "--workspace", temp, "--prepare-pairwise")
        for name in (positive, negative):
            case = root / name
            questions = load(case / "pairwise" / "reader_questions.json")["questions"]
            mapping = load(case / "pairwise" / "assignment.json")
            for side in ("A", "B"):
                assert (case / "pairwise" / f"{side}.md").is_file()
                record = load(case / "pairwise" / f"{side}.reader_answers.template.json")
                record["reader"] = {
                    "id": f"synthetic-reader-{side}", "kind": "human",
                    "blind_to_variant": True, "source_blind": True,
                }
                for answer in record["answers"]:
                    answer["answer"] = "Synthetic answer; not an actual blind reconstruction"
                save(case / "pairwise" / f"{side}.reader_answers.json", record)
            grade = load(case / "pairwise" / "grading.template.json")
            grade["reviewer"] = {
                "id": "synthetic-independent-judge", "kind": "human",
                "independent": True, "blind_to_variant": True,
            }
            for side in ("A", "B"):
                for entry in grade["per_answer"][side]:
                    entry["rating"] = 2 if (name == negative or mapping[side] == "targeted_recall") else 1
                    entry["evidence"] = "Synthetic grading evidence, no model has been evaluated"
            save(case / "pairwise" / "grading.json", grade)
        invoke("aggregate_recall_eval.py", root)
        result = load(root / "recall-benchmark.json")
        assert result["scored"] == 2 and result["total"] == 6
        summary = {x["case"]: x for x in result["cases"]}
        assert summary[positive]["gain_0_2"] == 1
        assert summary[negative]["gain_0_2"] == 0
        assert summary[positive]["trace_status"] == "declared_repair_with_source_spans"
        assert summary[negative]["trace_status"] == "declared_skip_unchanged"
        assert result["declared_unnecessary_repairs"] == 0
        assert result["declared_missed_repairs"] == 0
    print("OK: targeted recall fixtures, frozen-draft preparation, independent grading shape and aggregation (synthetic only)")


if __name__ == "__main__":
    main()
