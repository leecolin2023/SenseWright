# SenseWright Eval V0.1

V0.1 不建立某一家模型供应商专用 benchmark 平台，而是先固定 **Skill 迭代的最小证据链**。

## 1. 两类评测

### Triggering

`triggering.json` 检查根 Skill 的 `description` 是否覆盖真正应该触发的场景，同时避开相邻但不属于本 Suite 的任务。

V0.1 当前使用 22 个 query：12 个应触发、10 个不应触发。负样本优先使用 near-miss，而不是完全无关问题。

触发行为依赖具体 Agent Runtime，因此仓库保存 test set 与结果，但不假设不同 Runtime 的 discovery 机制完全一致。

### Task Quality

`evals.json` 覆盖 D / R / L / Q 与主要复合路由。每个 case 包含 prompt、files、expected_route、expected_output、assertions。

assertions 只写尽量客观、可复核的要求；文风、洞察力等主观质量继续交给 human review。

### Reference Context

V2.5.0 在 Eval metadata 中增加可选 `reference_context`，用于验证非对称协作：

~~~json
"reference_context": [
  {
    "source_skill": "R",
    "file": "evals/fixtures/reference-review-agent-workflow.md",
    "purpose": "optional_reference"
  }
]
~~~

规则：
- 只有 expected route 包含 **L 或 Q** 的 case 才允许声明 `reference_context`；
- 纯 D / R case 若配置 reference context，静态校验直接失败；
- reference 的目标是测试“选择性吸收”，不是把 sibling output 当 source。

Eval 当前重点验证：
- **Source isolation**：D / R 不消费 sibling result；
- **Selective reference**：L / Q 能利用真正有价值的 prior finding，同时不继承为事实或结论。

### Questioning V0.1

Q 的首个 Eval 暂时只测试 **第一问质量**，不假装已经覆盖完整多轮 Agent Loop：

- 默认是否只推进一个关键问题；
- 是否优先澄清问题定义或追真实案例；
- 是否避免把答案藏进诱导性问题；
- 是否在获得新信息前避免提前回答。

多轮 `Answer → State Update → Next Probe`、停止条件和长访谈稳定性留给后续版本。

## 2. Baseline 策略

这是一个已存在的 Skill Suite，所以第一次评测优先比较：

- `with_skill`：当前版本
- `old_skill`：改造前版本 `ffdb60e1f27ae99011d18c29c683dc747cec64f1`

`without_skill` 作为可选控制组，用于回答“整个 Suite 相比无 Skill 到底提供多少价值”。

同一 iteration 尽量在相同模型、参数和相近时间窗口内完成 with-skill 与 baseline，避免先跑一组、过几天再补另一组。

## 3. 初始化 workspace

~~~bash
python scripts/init_eval_workspace.py --iteration 1 --baseline old_skill
~~~

默认生成：

~~~text
.eval-workspace/
└── iteration-1/
    ├── deep-read-faithful/
    │   ├── eval_metadata.json
    │   ├── with_skill/
    │   │   └── outputs/
    │   └── old_skill/
    │       └── outputs/
    └── ...
~~~

`.eval-workspace/` 是运行产物，不提交 Git。

## 4. 每个 run 保存什么

建议至少保存：

~~~text
with_skill/
├── outputs/
│   └── response.md
├── transcript.md
├── grading.json
└── timing.json
~~~

`old_skill/` 使用同样结构。

### grading.json

~~~json
{
  "expectations": [
    {
      "text": "输出忠实解释材料主线，没有把独立批评混入 Deep Read。",
      "passed": true,
      "evidence": "response.md 中的具体证据"
    }
  ]
}
~~~

如果 assertion 能由程序确定，优先脚本检查；不能客观判断的内容交给独立 grader 或 human review。

### timing.json

~~~json
{
  "total_tokens": 12480,
  "duration_ms": 8120,
  "total_duration_seconds": 8.12
}
~~~

Runtime 不提供的数据可以省略，不要估算。

## 5. 聚合 benchmark

~~~bash
python scripts/aggregate_benchmark.py .eval-workspace/iteration-1
~~~

输出 `benchmark.json` 和 `benchmark.md`。V0.1 聚合 assertion pass rate、token mean/stddev、duration mean/stddev。

不要只看总 pass rate，还要检查：

- assertion 是否两个版本都总能通过，导致没有区分度；
- 某个 case 是否波动特别大；
- 质量提升是否以明显 token / latency 增长为代价；
- 新版本是否修复目标问题却破坏其他路由。

## 6. Human Review

量化不是最终裁决。对每个 case 同时看 with-skill 与 baseline：

- 哪个更忠实、更有判断价值或更能形成知识模型；
- 哪些差异真正改变理解或行动；
- 哪些改善只是“写得更长”；
- 哪些 failure 应该修改 Skill，而不是修改测试去迎合 Skill。

建议把人工反馈保存为 iteration 下的 `feedback.json`，下一轮修改前先读它。

## 7. 下一轮

~~~bash
python scripts/init_eval_workspace.py --iteration 2 --baseline old_skill
~~~

V0.1 默认保持最初 old-skill baseline 稳定，便于观察累计改进。以后如果需要相邻版本比较，可以新增 baseline，而不是覆盖历史记录。
