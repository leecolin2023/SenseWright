---
name: sensewright
description: Route complex information and knowledge-work tasks among faithful deep reading, independent review, systematic learning, and adaptive questioning. Use when the user wants to understand source material, judge whether a document or argument is sound, build a reusable knowledge model, discover what to ask next, or combine those goals. Deep Read and Review remain source-isolated; Learning and Questioning may selectively use prior skill outputs as attributed reference context rather than inherited truth.
---

# SenseWright V2.5.1

## 核心设计

> **统一入口，独立职责，非对称协作。**

SenseWright 维护四种认知模式：

- **D — Deep Read**：忠实理解原材料。
- **R — Review**：完整覆盖原材料后独立评价，重要性只控制报告，不控制是否审阅。
- **L — Learning**：把材料、问题或主题转化为自己的知识模型。
- **Q — Questioning**：找到当前最值得知道的下一件事，通过追问减少关键不确定性。

四个 Skill 不处在同一种协作关系中：

- **D / R 是 source-facing**：严格面向原始材料，彼此隔离，也不消费 L / Q 的结果。
- **L / Q 是 knowledge-facing**：仍以原始材料、用户事实和当前任务为主要依据，但可以选择性参考已经产生的其他 Skill 结果。

---

## Router 只做两件事

### 1. Route Selection

判断当前任务需要 D / R / L / Q 中的哪一种或哪几种认知能力。

### 2. Reference Selection

只有当目标包含 **L 或 Q** 时，才判断已有 sibling result 是否值得作为可选参考。

Router 不解释材料、不生成结论，也不建立共享黑板。

---

## D — Deep Read / 忠实深读

当用户主要想知道：
- 这篇文章/这份文档到底讲了什么；
- 帮我总结、梳理、提炼、解读；
- 保留作者的故事、比喻、术语和推理过程；
- 做忠实的深读笔记。

→ 使用 `skills/article-deep-read-v6.1/SKILL.md`

**判断标准：用户的中心对象是“原材料本身”。**

### Context Policy

Deep Read 只读取 Raw Source、用户对当前任务的直接要求和必要的原始用户上下文。

**不得读取或消费 Review / Learning / Questioning 的输出。**

---

## R — Review / 独立审阅

当用户主要想知道：
- 这份材料写得对不对、够不够、有没有遗漏或冲突；
- 有什么逻辑、证据、数字、流程、责任、边界或方案问题；
- 如果独立重想一次，会不会得出不同结论；
- 哪些地方真正值得修改。

→ 使用 `skills/vibe-review-v0.10/SKILL.md`

**判断标准：用户的中心任务是“判断这份材料的质量或决策价值”。**

### Context Policy

Review 只读取 Raw Source、用户对当前 Review 任务的直接要求和必要的原始用户上下文。

即使 Deep Read 已经运行过，**Review 也不得读取 Deep Read 输出**。同样不读取 Learning / Questioning 的结果。

### Coverage Policy

Review V0.10 不再先挑“重点内容”再审。

内部顺序是：

`Atomize Source → Reconcile Coverage → Review Every Unit → Assess Materiality → Report Selectively`

原文先被拆成 Atomic Review Units；所有有信息内容都必须有去处。分析深度可以不同，但 Materiality 只能影响最终报告，不能提前决定哪些内容值得检查。

---

## L — Learning / 系统学习

当用户主要想真正学会一个概念、系统、人物、事件或方法，形成自己的理解框架，并继续进入会议、实施或决策：

→ 使用 `skills/system-learning-v0.4.4/SKILL.md`

Learning 的主要依据仍是 Raw Source / 用户事实 / 当前任务，但可以选择性参考已有 D / R / Q 结果。这些内容是 **Reference Context**，不是自动继承的事实或结论。

---

## Q — Questioning / 连续追问

当用户主要想不要马上给答案，而是通过连续追问把问题想清楚、设计访谈或决定下一问：

→ 使用 `skills/questioning-v0.1.1/SKILL.md`

Questioning 可以选择性参考 D / R / L 的已有发现，但 Reference 只用于选择下一问，不自动成为已确认事实。

---

## 非对称协作规则

~~~text
Raw Source / User Context
        │
   ┌────┴────┐
   ▼         ▼
Deep Read   Review
   D         R
[isolated] [isolated]
   │         │
   └────┬────┘
        │ optional references
        ▼
     Learning
        L
        │
        ▼
   Questioning
        Q
        │
        └──────────────► Learning
~~~

允许：
- D → L
- R → L
- D → Q
- R → Q
- L → Q
- Q → L

禁止：
- 任何 Skill → D
- 任何 Skill → R
- D ↔ R 之间直接传递结果

---

## Reference Context 的三条规则

- **Reference ≠ Evidence**
- **Transform, don't copy**
- **Selective, not mandatory**

这些规则只适用于 L / Q；D / R 不消费 sibling results。

---

## 四条认知边界

- **D 是 source-centered**：为了理解可以按认知价值压缩。
- **R 是 judgment-centered**：为了判断先保证 substantive coverage，再按 materiality 收敛输出。
- **L 是 learner-centered**：形成用户以后还能继续使用的知识模型。
- **Q 是 inquiry-centered**：选择最有信息价值的下一问并根据回答持续更新。

---

## 最终原则

> **D / R 独立面对 Source；R 先覆盖再筛选；L / Q 可以从已有认知成果中学习，但 Reference 永远不是 inherited truth。**
