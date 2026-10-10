---
name: sensewright
description: Route knowledge work among independent source-faithful Deep Read, source-critical Review, grounded Learning, and executable engineering Practice. Every Learning task must first run fresh Deep Read and Review independently on the same original input and use both as non-authoritative scaffolds.
---

# SenseWright V2.8.2

Choose the task by **user goal**, not by the existence of an attachment:

| Mode | Goal | Skill |
|---|---|---|
| **D — Deep Read** | 原材料实际说了什么、怎样推导 | `skills/article-deep-read-v6.4/SKILL.md` |
| **R — Review** | 原材料的事实、论证和决策依据是否成立 | `skills/vibe-review-v0.10/SKILL.md` |
| **L — Learning** | 用户怎样从真实问题理解机制，并将机制映射到具体实现与证据 | `skills/system-learning-v0.6.2/SKILL.md` |
| **P — Practice** | 怎样把已理解知识落成可执行、可验证、可排错的真实工程 | `skills/practice-v0.2/SKILL.md` |

## 执行编排

- **只要任务包含 L，必须先运行本轮 D 和 R**：二者分别只读相同 Raw Input（原始文件/用户问题/直接提供的上下文），互不读取对方或 L/P 产物；可并行，**均完成后 L 才启动**。不得用历史 D/R 结果替代。
- **L 必须读取本轮 D/R 结果及 Raw Input**，选择性利用认知结构、例子、疑点与边界，但 D/R **只是认知脚手架，不是新增证据**。L 重新解释真实对象和因果机制，不能把 D/R 直接拼接成答案。
- 用户只有一个概念问题、没有独立文件时，D 先简要澄清问题含义，R 独立核对其中的事实前提与歧义；没有问题可如实说明。**D/R 必须执行，但不强制展开长篇报告或捏造材料。**
- 仅要求 D、R、D+R 或 P 的任务按各自 Skill 独立执行，**不因其他模式存在就自动追加 L**。P-only 可以按需引用已有知识模型；P→L 的新学习请求仍须重新完成本轮 D/R。
- D/R 的独立上下文和完成屏障需要宿主执行层保证。**仅有 Skill 文字约束或最终答案三个标题，不能证明实际发生了隔离调用**；没有执行 Trace 时不能声称已验证运行时隔离。

## 边界与交付

- **D** 忠实还原材料的认知拓扑，并按交付目的选择 Coverage-Preserving 或 Cognitive-Synthesis；不插入独立批评。
- **R** 对原材料完整覆盖后再判断重要性，独立审阅；不消费 D 的总结。
- **L** 不服从原文结构，不接受 R 意见为天然事实；对于探索型或多材料任务，先检查用户给出的表层问题是否为值得研究的主问题，从异常、竞争解释和关键约束中按需做 **Problem Discovery**，再建立问题链；通过真实场景、必要机制、证据和边界形成自己的知识模型。**对有实现或操作的知识，先核实材料和行为，再按问题→机制→具体实现→证据讲解；源码学习精确对应调用链与可核验位置**。当结论受现实规模、状态、行为或来源可比性影响时，**按需采用最小 Reality Calibration**（数量/操作轨迹/对照证据/反例），不强制所有主题量化。内部自检不是独立 R Skill 的替代品。
- **P** 专注设计、端到端实施、运行、验证、排障及工程交付；纯提问、自测或模拟面试不因形式自动路由 P。知识补缺可由 L 使用简短、非诱导的追问完成。

默认**只输出满足当前用户目标的结果**。包含 L 的任务默认交付整合后的学习解释；用户明确要求时才展示 D/R 各自完整结果。不要打印内部路由、前置检查表或质量 Gate。
