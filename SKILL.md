---
name: sensewright
description: Route knowledge work among independent source-faithful Deep Read, source-critical Review, grounded Learning, and branch-exploration Practice. Every Learning task must first run fresh Deep Read and Review independently on the same original input and use both as non-authoritative scaffolds.
---

# SenseWright V2.9.0

Choose the task by **user goal**, not by the existence of an attachment:

| Mode | Goal | Skill |
|---|---|---|
| **D — Deep Read** | 原材料实际说了什么、怎样推导 | `skills/article-deep-read-v6.4/SKILL.md` |
| **R — Review** | 原材料的事实、论证和决策依据是否成立 | `skills/vibe-review-v0.10/SKILL.md` |
| **L — Learning** | 用户怎样从真实问题理解机制，并将机制映射到具体实现与证据 | `skills/system-learning-v0.6.2/SKILL.md` |
| **P — Practice** | 沿已有知识主干发现并深入尚未解决的关键问题与独立枝干 | `skills/practice-v0.3/SKILL.md` |

## 执行编排

- **只要任务包含 L，必须先运行本轮 D 和 R**：二者分别只读相同 Raw Input（原始文件/用户问题/直接提供的上下文），互不读取对方或 L/P 产物；可并行，**均完成后 L 才启动**。不得用历史 D/R 结果替代。
- **L 必须读取本轮 D/R 结果及 Raw Input**，选择性利用认知结构、例子、疑点与边界，但 D/R **只是认知脚手架，不是新增证据**。L 重新解释真实对象和因果机制，不能把 D/R 直接拼接成答案。
- 用户只有一个概念问题、没有独立文件时，D 先简要澄清问题含义，R 独立核对其中的事实前提与歧义；没有问题可如实说明。**D/R 必须执行，但不强制展开长篇报告或捏造材料。**
- 仅要求 D、R、D+R 或 P 的任务按各自 Skill 独立执行，**不因其他模式存在就自动追加 L**。P-only 可以按需引用已有知识模型；P→L 的新学习请求仍须重新完成本轮 D/R。
- D/R 的独立上下文和完成屏障需要宿主执行层保证。**仅有 Skill 文字约束或最终答案三个标题，不能证明实际发生了隔离调用**；没有执行 Trace 时不能声称已验证运行时隔离。

## 边界与交付

- **D** 忠实还原材料的认知拓扑，并按交付目的选择 Coverage-Preserving 或 Cognitive-Synthesis；不插入独立批评。
- **R** 对原材料完整覆盖后再判断重要性，独立审阅；不消费 D 的总结。
- **L** 以用户的学习目的和真实对象为中心：按需使用相关领域知识校准问题、解释必要机制、用适合材料的实际证据检验，并在矛盾出现时修正理解。**这是可往返的自适应认知循环，不是 Domain Anchor / Problem Discovery / Reality Calibration 的强制流水线**。技术源码须对应可核验的调用/数据/状态链；非技术主题选相应的原始材料与证据形式。具体行业理论属于学习内容，不写死在通用 Skill 中。L 内部自检不能替代独立 R。
- **P** 从已有知识主干出发，检查被遗漏的因果前提，探索独立问题线，再深入有判断价值的枝干。可用于技术追问、案例判断与实际应用；不默认要求工程实施、固定题数或验收清单。若确需启动新的 L，仍须遵循本轮独立 D/R 前置；模型自演练不能评价用户掌握程度。

默认**只输出满足当前用户目标的结果**。包含 L 的任务默认交付整合后的学习解释；用户明确要求时才展示 D/R 各自完整结果。不要打印内部路由、前置检查表或质量 Gate。
