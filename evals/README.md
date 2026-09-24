# SenseWright Eval V0.1

V0.1 不建立某一家模型供应商专用 benchmark 平台，而是先固定 **Skill 迭代的最小证据链**。

## 1. 两类评测

### Triggering

`triggering.json` 检查根 Skill 的 `description` 是否覆盖真正应该触发的场景，同时避开相邻但不属于本 Suite 的任务。

V0.1 当前使用 24 个 query：14 个应触发、10 个不应触发。负样本优先使用 near-miss，而不是完全无关问题。

触发行为依赖具体 Agent Runtime，因此仓库保存 test set 与结果，但不假设不同 Runtime 的 discovery 机制完全一致。

### Task Quality

`evals.json` 覆盖 D / R / L / P 与主要复合路由。每个 case 包含 prompt、files、expected_route、expected_output、assertions。

assertions 只写尽量客观、可复核的要求；文风、洞察力等主观质量继续交给 human review。

### Review Coverage / Atomic Review Units

Vibe Review V0.10 增加 coverage-oriented eval。

Review case 可以声明可选的 `gold_review_units`：

~~~json
"gold_review_units": [
  {"id": "U01", "description": "一个可独立审阅的语义单元"}
]
~~~

它的作用不是要求最终答案逐条打印，而是让 grader / human review 有一个 coverage 基准。

Review coverage 重点看三件事：
- **Unit Recall**：原材料中的 Gold Atomic Review Units 是否进入审阅；
- **Relation Preservation**：条件、例外、冲突、依赖等是否在拆解后仍被保留；
- **Selective Reporting**：内部完整 coverage 是否仍能收敛为面向用户的重点发现。

当前 `review-atomic-coverage` fixture 故意把问题分散在数字、控制流程、例外和结论中，用来捕捉“先挑重点、后审阅”导致的漏审。

升级前 Review V0.9 baseline：
`46ec079238fd58e6771ebbb1234d170ed7f68087`

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
- 只有 expected route 包含 **L 或 P** 的 case 才允许声明 `reference_context`；
- 纯 D / R case 若配置 reference context，静态校验直接失败；
- reference 的目标是测试“选择性吸收”，不是把 sibling output 当 source。

Eval 当前重点验证：
- **Source isolation**：D / R 不消费 sibling result；
- **Selective reference**：L / P 能利用真正有价值的 prior finding，同时不继承为事实或结论。

### Learning Adaptive Probe

原 Questioning 中用于“补知识”的能力已迁入 Learning。

相关 Eval 验证：
- 当用户自身语境是关键缺口时，Learning 会先澄清，而不是凭常识补原因；
- 默认一次只问一个高信息价值问题；
- 专家访谈问题服务于 Knowledge Model 更新；
- 提问不是独立终点。

### Learning Grounding

System Learning V0.5.1 增加 grounding-oriented regression，用来捕捉“知识模型结构完整，但用户仍然不知道现实里到底改变了什么”的失败。

相关 Eval 验证：
- **Ground before abstract**：先用具体对象和任务解释，再形成上位模型；
- **Contrastive grounding**：对概念差异同时找低差异与高差异场景，避免强行制造价值；
- **Grounding recovery**：用户明确反馈“没理解 / 太抽象”后，必须降低抽象层级而不是继续增加术语；
- **Cross-domain transfer**：同一规则应能解释数据库事务等非 Agent 概念，而不是只针对某个案例特判。

当前相邻版本 baseline：`learning_v0_5_0`。

### Learning Mechanism Depth

System Learning V0.5.2 在 V0.5.1 grounding 基础上增加技术机制深度回归。

相关 Eval 验证：
- **Run once**：机制型技术不能只停在组件说明，至少让一个最小实例真实运行；
- **Mechanism causality**：不仅说明发生了什么，还解释关键步骤为什么存在；
- **Teaching variation**：改变一个主要条件并解释结果变化，答案可直接展示，仍属于 Learning；
- **Prediction check**：当前模型应足以解释至少一个相邻条件变化，而不是只复述定义；
- **Analogy scaffolding**：Deep Read 保留下来的比喻/故事可以帮助进入机制，但 Learning 最终应映射回真实系统并说明类比边界。

当前相邻版本 baseline：`learning_v0_5_1`。

### Practice Transfer

Practice Eval 重点验证：
- 不重新讲已经学过的答案；
- 能把 Knowledge Model 转成真实 decision / design / troubleshooting 场景；
- 一次只推进一个主要任务；
- 下一轮根据上一轮表现改变 stress condition；
- 面试式追问用于检验 transfer，而不是背题。

当前首个 transfer 主题使用“为什么 LLM 基于 token”，并分别测试初始场景化与 adaptive stress。


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

- 哪个更忠实、更有判断价值，或更能让用户先形成具体理解再形成知识模型；
- 哪些差异真正改变理解或行动；
- 哪些改善只是“写得更长”；
- 哪些 failure 应该修改 Skill，而不是修改测试去迎合 Skill。

建议把人工反馈保存为 iteration 下的 `feedback.json`，下一轮修改前先读它。

## 7. 下一轮

~~~bash
python scripts/init_eval_workspace.py --iteration 2 --baseline old_skill
~~~

V0.1 默认保持最初 old-skill baseline 稳定，便于观察累计改进。以后如果需要相邻版本比较，可以新增 baseline，而不是覆盖历史记录。
