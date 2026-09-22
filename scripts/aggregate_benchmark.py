#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import statistics

def read_json(path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))

def mean_std(values):
    if not values:
        return None, None
    if len(values) == 1:
        return float(values[0]), 0.0
    return statistics.mean(values), statistics.pstdev(values)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("iteration_dir")
    args = p.parse_args()
    root = Path(args.iteration_dir)
    manifest = read_json(root / "manifest.json")
    if not manifest:
        raise SystemExit("manifest.json not found; initialize workspace first")

    configs = ["with_skill", manifest["baseline"]]
    summary = {}

    for config in configs:
        passed = total = 0
        tokens, durations, per_eval = [], [], []
        for case_name in manifest["cases"]:
            run = root / case_name / config
            grading = read_json(run / "grading.json") or {}
            timing = read_json(run / "timing.json") or {}
            expectations = grading.get("expectations", [])
            case_pass = sum(e.get("passed") is True for e in expectations)
            case_total = len(expectations)
            passed += case_pass
            total += case_total
            if isinstance(timing.get("total_tokens"), (int, float)):
                tokens.append(timing["total_tokens"])
            if isinstance(timing.get("duration_ms"), (int, float)):
                durations.append(timing["duration_ms"])
            per_eval.append({
                "eval_name": case_name,
                "passed": case_pass,
                "total": case_total,
                "pass_rate": case_pass / case_total if case_total else None,
                "total_tokens": timing.get("total_tokens"),
                "duration_ms": timing.get("duration_ms")
            })

        token_mean, token_sd = mean_std(tokens)
        duration_mean, duration_sd = mean_std(durations)
        summary[config] = {
            "assertions_passed": passed,
            "assertions_total": total,
            "pass_rate": passed / total if total else None,
            "token_mean": token_mean,
            "token_stddev": token_sd,
            "duration_ms_mean": duration_mean,
            "duration_ms_stddev": duration_sd,
            "evals": per_eval
        }

    benchmark = {
        "schema_version": "0.1",
        "iteration": manifest["iteration"],
        "skill_name": manifest["skill_name"],
        "baseline": manifest["baseline"],
        "configs": summary
    }
    (root / "benchmark.json").write_text(
        json.dumps(benchmark, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )

    def fmt(value, pct=False):
        if value is None:
            return "n/a"
        return f"{value:.1%}" if pct else f"{value:.1f}"

    lines = [
        f"# Benchmark — iteration {manifest['iteration']}",
        "",
        "| Config | Assertion pass rate | Tokens mean ± sd | Duration ms mean ± sd |",
        "|---|---:|---:|---:|"
    ]
    for config in configs:
        s = summary[config]
        lines.append(
            f"| {config} | {fmt(s['pass_rate'], True)} | "
            f"{fmt(s['token_mean'])} ± {fmt(s['token_stddev'])} | "
            f"{fmt(s['duration_ms_mean'])} ± {fmt(s['duration_ms_stddev'])} |"
        )

    lines.extend(["", "## Per-eval", ""])
    for config in configs:
        lines.extend([f"### {config}", "", "| Eval | Pass rate | Tokens | Duration ms |", "|---|---:|---:|---:|"])
        for item in summary[config]["evals"]:
            lines.append(
                f"| {item['eval_name']} | {fmt(item['pass_rate'], True)} | "
                f"{item['total_tokens'] if item['total_tokens'] is not None else 'n/a'} | "
                f"{item['duration_ms'] if item['duration_ms'] is not None else 'n/a'} |"
            )
        lines.append("")

    (root / "benchmark.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {root / 'benchmark.json'}")
    print(f"Wrote {root / 'benchmark.md'}")

if __name__ == "__main__":
    main()
