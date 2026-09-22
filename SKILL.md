---
name: sensewright
description: Route complex information and knowledge-work tasks among faithful deep reading, independent review, systematic learning, and adaptive questioning. Use when the user wants to understand source material, judge whether a document or argument is sound, build a reusable knowledge model, discover what to ask next, or combine those goals. Deep Read and Review remain source-isolated; Learning and Questioning may selectively use prior skill outputs as attributed reference context rather than inherited truth.
---

# SenseWright V2.5.0

## 核心设计

> **统一入口，独立职责，非对称协作。**

SenseWright 维护四种认知模式：

- **D — Deep Read**：忠实理解原材料。
- **R — Review**：独立评价原材料。
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

Deep Read 只读取：
- Raw Source；
- 用户对当前 Deep Read 任务的直接要求；
- 必要的原始用户上下文。

**不得读取或消费 Review / Learning / Questioning 的输出。**

---

## R — Review / 独立审阅

当用户主要想知道：
- 这份材料写得对不对、够不够；
- 有什么逻辑、证据、架构、方案或表达问题；
- 如果独立重想一次，会不会得出不同结论；
- 哪些地方真正值得修改。

→ 使用 `skills/vibe-review-v0.9/SKILL.md`

**判断标准：用户的中心任务是“判断这份材料的质量或决策价值”。**

### Context Policy

Review 只读取：
- Raw Source；
- 用户对当前 Review 任务的直接要求；
- 必要的原始用户上下文。

即使 Deep Read 已经运行过，**Review 也不得读取 Deep Read 输出**。同样不读取 Learning / Questioning 的结果。

> Review 必须审原材料，不审别的 Skill 对原材料的表示。

---

## L — Learning / 系统学习

当用户主要想：
- 真正学会一个概念、系统、人物、事件或方法；
- 不只是复述材料，而是形成自己的理解框架；
- 找出还卡在哪里、下一步应该学什么或验证什么；
- 把知识进一步转成会议问题、实施步骤或决策输入。

→ 使用 `skills/system-learning-v0.4.4/SKILL.md`

**判断标准：用户的中心对象是“自己的知识模型”。**

Learning 的主要依据仍是 Raw Source / 用户事实 / 当前任务，但可以选择性参考已有：
- Deep Read：作者结构、概念、机制等 source reconstruction；
- Review：关键分歧、不确定性、风险等 judgment；
- Questioning：用户新确认的事实、尚未解决的 Gap。

这些内容是 **Reference Context**，不是自动继承的事实或结论。

---

## Q — Questioning / 连续追问

当用户主要想：
- 不要马上给答案，而是通过连续追问把问题想清楚；
- 判断“下一步最值得问什么”；
- 为访谈、专家交流或需求调研设计主问题与追问；
- 根据上一轮回答动态决定下一问；
- 把模糊判断逐步推进到事实、证据、机制、边界或可验证行动。

→ 使用 `skills/questioning-v0.1.1/SKILL.md`

**判断标准：用户的中心任务是“通过提问减少关键不确定性”。**

Questioning 可以选择性参考：
- D：哪些结构、概念或论证值得进一步澄清；
- R：哪些不确定性、风险或证据缺口值得求证；
- L：哪些 Knowledge Gap 最值得继续问。

Reference 只用于选择下一问，不自动成为 Q 已确认的事实。

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
        │ knowledge gaps / model
        ▼
   Questioning
        Q
        │
        │ newly confirmed answers
        └──────────────► Learning
~~~

允许：
- D → L
- R → L
- D → Q
- R → Q
- L → Q
- Q → L（主要传递用户新确认的信息、事实或仍未解决的 Gap）

禁止：
- 任何 Skill → D
- 任何 Skill → R
- D ↔ R 之间直接传递结果

---

## Reference Context 的三条规则

### 1. Reference ≠ Evidence

Sibling output 只能作为参考、线索、假设或 Gap。涉及原文事实时仍回到 Raw Source；涉及外部事实时仍需要相应证据。

### 2. Transform, don't copy

L / Q 必须按照自己的任务目标重新解释 reference，而不是复制 sibling output。

### 3. Selective, not mandatory

“存在某个 sibling result”不等于“必须注入当前 Context”。只有它能明显改善当前 Learning / Questioning 时才选择。

---

## 复合意图

不新增 DQ / RLQ / DRLQ 等组合 Skill。

例如：
- 总结 + 审阅 → D + R，但两路严格隔离；
- 总结 + 学习 → D + L，L 可选择性参考 D；
- 审阅 + 学习 → R + L，L 可选择性参考 R；
- 学习 + 追问 → L + Q；
- 审阅后准备专家访谈 → R + Q。

组合只表示任务中需要多种能力，不改变各 Skill 自己的 Context Policy。

---

## 四条认知边界

- **D 是 source-centered**：忠实还原作者。
- **R 是 judgment-centered**：独立判断材料是否成立、是否完成任务。
- **L 是 learner-centered**：建立用户以后还能继续使用的知识模型。
- **Q 是 inquiry-centered**：选择最有信息价值的下一问，并根据回答持续更新。

---

## 最终原则

> **D / R 独立面对 Source；L / Q 可以从已有认知成果中学习，但 Reference 永远不是 inherited truth。**

用户只管理一个 SenseWright；内部负责路由、边界和可选参考。
