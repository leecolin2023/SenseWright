#!/usr/bin/env python3
"""Offline smoke test for V0.2 workspace, blind grading and aggregation; no LLM calls."""
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
        name = "learning-v07-short-concept-no-forced-16-step-output"
        case = run / name
        assert case.is_dir()
        for variant in ("with_skill", manifest["baseline"]):
            answer = case / variant / "outputs" / "response.md"
            answer.write_text("事务原子性：相关操作整体提交或整体回滚，例如转账两步必须一同生效。\n", encoding="utf-8")
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
    print("OK: Eval V0.2 offline smoke test (synthetic grading artifacts only)")


if __name__ == "__main__":
    main()
