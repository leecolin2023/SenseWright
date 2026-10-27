#!/usr/bin/env python3
"""Offline smoke test for Learning + Deep Read rubric, blind pairwise, and aggregation; no LLM."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def invoke(script, *args):
    subprocess.run([sys.executable, str(ROOT / "scripts" / script), *map(str, args)],
                   cwd=ROOT, check=True, capture_output=True, text=True)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    with tempfile.TemporaryDirectory(prefix="sensewright-eval-") as temp:
        invoke("init_eval_workspace.py", "--iteration", 1,
               "--baseline", "learning_v0_6_2_pre_general_refactor", "--workspace", temp)
        run = Path(temp) / "iteration-1"
        manifest = load(run / "manifest.json")
        assert len(manifest["cases"]) == 80
        # Missing grade data must NOT become zero scores.
        invoke("aggregate_benchmark.py", run)
        empty = load(run / "benchmark.json")
        assert empty["configs"]["with_skill"]["learning_graded"] == 0
        assert empty["pairwise"]["graded"] == 0
        assert empty["deep_read_case_count"] == 4
        assert empty["configs"]["with_skill"]["deep_read_graded"] == 0
        assert empty["deep_read_pairwise"]["ungraded"] == 4
        mixed = run / "deep-read-plus-review"
        assert (mixed / "with_skill" / "review.grading.template.json").is_file()
        name = "learning-v07-short-concept-no-forced-16-step-output"
        case = run / name
        assert case.is_dir()
        for variant in ("with_skill", manifest["baseline"]):
            answer = case / variant / "outputs" / "response.md"
            answer.write_text("事务原子性：相关操作整体提交或整体回滚，例如转账两步必须一同生效。\n", encoding="utf-8")
        deep_cases = ["deep-read-faithful", "deep-read-coverage-preserving", "deep-read-cognitive-synthesis"]
        for deep_name in deep_cases:
            deep_case = run / deep_name
            for variant in ("with_skill", manifest["baseline"]):
                (deep_case / variant / "outputs" / "response.md").write_text(
                    "Synthetic Deep Read output for offline pipeline test, not a real assessed answer.\n",
                    encoding="utf-8",
                )
        invoke("prepare_pairwise.py", run)
        assignment = load(case / "pairwise" / "assignment.json")
        assert set(assignment) == {"A", "B"}
        assert (case / "pairwise" / "A.md").exists()
        for side in ("A", "B"):
            file = case / "pairwise" / f"{side}.grading.template.json"
            grade = load(file)
            grade["reviewer"] = {"id": "synthetic-test-reviewer", "kind": "human",
                                 "independent": True, "blind_to_variant": True}
            for criterion in grade["criteria"]:
                criterion["rating"] = 2
                criterion["evidence"] = "测试桩：仅用于验证数据管道，不代表真实文章已获此评分"
            grade["failure_mode_assessment"]["occurred"] = False
            grade["failure_mode_assessment"]["severity"] = "none"
            grade["failure_mode_assessment"]["evidence"] = "测试桩"
            for item in grade["critical_failures"]:
                item["occurred"] = False
                item["evidence"] = "测试桩"
            save(case / "pairwise" / f"{side}.grading.json", grade)
        vote = load(case / "pairwise" / "vote.template.json")
        vote["reviewer"] = {"id": "synthetic-test-pair-judge", "kind": "human",
                            "independent": True, "blind_to_variant": True}
        vote["winner"] = "tie"
        vote["evidence"] = "两份测试桩内容相同；此投票用于验证A/B解盲逻辑"
        save(case / "pairwise" / "vote.json", vote)
        for deep_name in deep_cases:
            dcase = run / deep_name
            mapping = load(dcase / "pairwise" / "assignment.json")
            packet = load(dcase / "pairwise" / "judge_packet.json")
            assert packet["skill"] == "Deep Read"
            assert packet["compression_mode"] in ("coverage_preserving", "cognitive_synthesis")
            for side, variant in mapping.items():
                grade = load(dcase / "pairwise" / f"{side}.grading.template.json")
                grade["reviewer"] = {"id": "synthetic-test-reviewer", "kind": "human",
                                     "independent": True, "blind_to_variant": True}
                is_baseline = variant != "with_skill"
                for criterion in grade["criteria"]:
                    criterion["rating"] = 1 if is_baseline else 2
                    criterion["evidence"] = "Synthetic comparison-only evidence"
                assessment = grade["failure_mode_assessment"]
                assessment["occurred"] = is_baseline
                assessment["severity"] = "major" if is_baseline else "none"
                assessment["evidence"] = "Synthetic failure flag, not observed model behavior"
                for item in grade["critical_failures"]:
                    item["occurred"] = False
                    item["evidence"] = "Synthetic absence"
                save(dcase / "pairwise" / f"{side}.grading.json", grade)
            vote = load(dcase / "pairwise" / "vote.template.json")
            vote["reviewer"] = {"id": "synthetic-test-pair-judge", "kind": "human",
                                "independent": True, "blind_to_variant": True}
            vote["winner"] = next(side for side, variant in mapping.items() if variant == "with_skill")
            vote["evidence"] = "Synthetic win tests A/B mapping and Deep Read aggregation"
            save(dcase / "pairwise" / "vote.json", vote)
        invoke("resolve_blind_grades.py", run)
        invoke("aggregate_benchmark.py", run)
        result = load(run / "benchmark.json")
        assert result["configs"]["with_skill"]["learning_graded"] == 1
        assert result["configs"][manifest["baseline"]]["learning_graded"] == 1
        assert result["configs"]["with_skill"]["learning_score_mean_10"] == 10
        assert result["configs"]["with_skill"]["preflight"]["verified"] == 0
        assert result["pairwise"]["graded"] == 1
        assert result["pairwise"]["tie"] == 1
        assert result["pairwise"]["ungraded"] == 56
        assert result["configs"]["with_skill"]["deep_read_graded"] == 3
        assert result["configs"][manifest["baseline"]]["deep_read_graded"] == 3
        assert result["configs"]["with_skill"]["deep_read_score_mean_10"] == 10
        assert result["configs"][manifest["baseline"]]["deep_read_score_mean_10"] == 5
        assert result["deep_read_pairwise"]["graded"] == 3
        assert result["deep_read_pairwise"]["with_skill"] == 3
        assert result["deep_read_pairwise"]["ungraded"] == 1
        assert result["deep_read_by_primary_rule"]["D02"]["paired_failure_changes"]["reduced"] == 1
        assert result["deep_read_by_primary_rule"]["D03"]["paired_failure_changes"]["reduced"] == 2
    print("OK: Learning + Deep Read offline pipeline smoke test (synthetic only)")


if __name__ == "__main__":
    main()
