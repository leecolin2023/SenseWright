# SenseWright Eval V0.1

V0.1 不建立某一家模型供应商专用 benchmark 平台，而是先固定 **Skill 迭代的最小证据链**。

## 1. 两类评测

### Triggering

`triggering.json` 检查根 Skill 的 `description` 是否覆盖真正应该触发的场景，同时避开相邻但不属于本 Suite 的任务。

样本数量以 `triggering.json` 与验证器输出为准。负样本优先使用 near-miss，而不是完全无关问题。

触发行为依赖具体 Agent Runtime，因此仓库保存 test set 与结果，但不假设不同 Runtime 的 discovery 机制完全一致。

### Task Quality

`evals.json` 覆盖 D / R / L / P 与主要复合路由。每个 case 包含 prompt、files、expected_route、expected_output、assertions。

assertions 只写尽量客观、可复核的要求；文风、洞察力等主观质量继续交给 human review。

### Deep Read Dual Compression

Deep Read V6.4 增加同源双契约回归，用同一份多议题材料验证“交付意图而不是材料类型”决定压缩方式：

- **Coverage-Preserving**：检查所有独立认知单元是否仍可追踪，同时确认重复案例和语言冗余被压缩；
- **Cognitive-Synthesis**：检查是否真正跨单元形成更高密度理解，而不是逐项换写原文；同时确认压缩没有改变核心认知模型；
- 两条路线都继续验证 Source Boundary、认知发动机和必要解释冗余。

当前相邻版本 baseline：`deep_read_v6_1`。

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

### Learning V0.6.0 — Problem Chain & Built-in Stabilization

Cases **22–27** cover: a causal Agent action loop; Framework Evidence vs stable Knowledge and architecture selection; transaction concepts appearing only after failure; business/usage-rate cross-domain transfer; simple tasks where long chains harm clarity; and repairing a deliberately flawed outline rather than leaving Gates pending.

Three internal gates: **Problem-chain Review → Concept First-Appearance Audit → Boundary & Evidence Review**, with repair and re-check *before* delivery. Verify that these checks change actual explanations, not just append a checklist. The old `learning_v0_5_3` baseline is pinned to `6bfc5519e089d8a1b08d254d500e947388400e78`.

The fixture `learning-premature-framework-outline.md` contains intentionally incorrect claims and should never be treated as verified product evidence. A static validator pass does not imply behavioral success. Run each case on old and new Skill under matched model, configuration and time, save outputs/grading and perform human review.

### Learning V0.6.1 — Mandatory D + R Preflight

Every L eval now includes the route prefix ["D","R","L"] and the following contract:

~~~json
{
  "required_before_L": ["D", "R"],
  "source_policy": "same_raw_input_independent_contexts",
  "completion_barrier": "both_complete_before_L",
  "handoff": "mandatory_read_selective_use_scaffold_not_evidence",
  "output_policy": "integrated_learning_unless_explicit"
}
~~~

D/R independently consume current Raw Input. Both are mandatory and must finish before L; L reads both as cognitive scaffolds, while returning to the real object and mechanism. Historical optional reference_context cannot replace current D/R. Query-only prompts still receive two concise preflight stages without fabricating sources. Cases 28–30 cover source preflight, no-document preflight, and non-authoritative scaffold handling. **Static validation cannot prove actual runtime isolation**: check execution traces or mark isolation and barrier UNVERIFIED.

### Learning V0.6.2 — Mechanism-to-Implementation Mapping

Cases **31–35** test one general Learning contract, not a code-only special case: **research original materials / behavior before forming conclusions; teach real problem → necessary mechanism → concrete realization → minimal verifiable evidence → next meaningful problem**. Fresh independent D/R preflight is unchanged.

- **31–33, code-specific:** toy Agent loop must derive Tool Execution from the problem *before* citing code; a counterexample must shrink unsupported claims; types-only input cannot be treated as executed capability. Exact function/data-flow and source anchors remain essential where source code exists.
- **34, technical textbook / SQL:** use a two-update inconsistency to derive transaction atomicity before listing BEGIN/COMMIT/ROLLBACK; anchor in the teaching SQL and clearly label hypothetical outcomes, not executed database evidence.
- **35, operational technical textbook / Linux:** derive why external process control and subsequent state observation matter, then map to sample terminal commands/signals; do not treat the mock terminal transcript as actually run.

Two quality gates: **Mechanism Independence** (remove function/product/command names, and why/how must still make sense) and **Implementation Grounding** (map every important behavior back to the real artifact and its evidence). The optional `mechanism_mapping` metadata applies across evidence media, with controlled specificity for source-code/line-number tasks. No forced five-section templates or invented external facts.

New fixtures are explicitly synthetic. Static validators ensure structure/metadata, not model quality, actual experiment execution or D/R runtime separation. Use frozen `learning_v0_6_1` for matched A/B evaluation.

### Learning V0.6.2 follow-up — Conditional Reality Calibration

Cases **36–41** 在不新增 Skill/版本号和固定输出模板的前提下，测试 Learning 是否会根据**真实结论依赖的变量**选择最小现实校准，而不是把金融计算推广到所有问题：

- **36：财务/经营**：从一张GPU的收入形成过程出发，最少计算70%→50%计费使用率的差异；保底付款情景不能把使用率当作实收金额，未知合同应明确。
- **37：技术性能**：基于合成trace识别API延迟关键路径，改变一个阶段；区分个别请求与总体p95，不能把p95阶段值直接相加。
- **38：银行流程**：用一笔审批—签约—生效业务的状态、交接与返回结果做现实锚定，不强行计算ROI/完成率。
- **39：健康证据**：区分评论体验与群体因果证据，不捏造有效率、不代替诊断。
- **40：消费价格**：不同频率的内存+挂牌价/成交价，正确的算术比值不能直接升级为同款市场涨幅。
- **41：必要时跳过**：简明解释“服务期≠不可撤销付款义务”，不能无增益地强制量化或生成表格。

每个 case 使用可选 `reality_calibration` 一致性契约和 `expected_calibration_kind` 类型。类型为 `minimal_quantitative`、`execution_trace`、`workflow_state`、`evidence_quality`、`comparability`、`skip`。静态验证检查元数据、fixture和路由，并不判定回答实际达到理解效果。

**验收先后**：校验比较对象/来源 → 机制和现实锚定是否一致 → 最小数量或状态变化能否改变/界定结论 → 是否明确事实/假设/推导/未知 → 是否停止在对学习真正有用的深度。注意“高技术含量”不等于“高理解价值”。

冻结 `learning_v0_6_2_pre_reality_calibration` 为相邻A/B基线。人工比较除正确性以外，还要关注简洁度、没有不必要的数字与输出负担。对缺乏执行 Trace 的 D/R 隔离，仍必须标为 **UNVERIFIED**。

### Practice Engineering Transfer

Practice V0.2 不再以 capability test 为核心，而是验证 **Knowledge → Executable Engineering Model**：

- **Scenario grounding**：不是给定义套故事，而是进入真实工程目标与约束；
- **System placement**：明确概念在系统里的位置、责任边界、输入输出与依赖；
- **Implementation specificity**：具体到组件、Schema、接口、状态、配置或工程产物；
- **Run one path**：至少让一个具体输入真实跑完整链路；
- **Verification**：提供可以判断“做对没有”的反馈机制；
- **Troubleshooting**：展示高信息价值的 failure symptom → diagnosis → fix；
- **Artifact readiness**：用户知道真正动手时要创建、运行和验收哪些东西；
- **Generalization**：区分概念本身的不变量与当前项目的实现选择。

当前回归主题使用 **RAG 文档切分** 与 **Agent State**，用于验证 Practice 是否真正填平“知道 → 知道怎么做”的鸿沟。

当前相邻版本 baseline：`practice_v0_1`.


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
