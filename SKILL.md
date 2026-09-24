---
name: sensewright
description: Route complex information and knowledge-work tasks among faithful deep reading, independent review, systematic learning, and applied practice. Use when the user wants to understand source material, judge whether a document or argument is sound, build a reusable knowledge model, or test whether that knowledge can transfer into realistic decisions, scenarios, or interview-style stress questions. Deep Read and Review remain source-isolated; Learning and Practice may selectively use prior outputs as attributed reference context rather than inherited truth.
---

# SenseWright V2.6.1

## 核心设计

> **统一入口，独立职责；提问是策略，不再是一级任务。**

SenseWright 维护四种一级认知模式：

- **D — Deep Read**：忠实理解原材料。
- **R — Review**：完整覆盖原材料后独立评价。
- **L — Learning**：先把当前对象落到真实情境中讲清楚，再形成可复用知识模型，并在必要时通过自适应追问补齐关键知识缺口。
- **P — Practice**：把知识放进真实或仿真情境，检验是否能够迁移、判断、操作和解释。

Questioning 不再作为独立路由。原 Questioning 的能力拆分为两种内部策略：

- **Learning Probe**：为了减少 knowledge uncertainty 而提问；
- **Practice Probe**：为了暴露 capability gap 而提问。

---

## Router 只做两件事

### 1. Route Selection

判断当前任务需要 D / R / L / P 中的哪一种或哪几种能力。

### 2. Reference Selection

只有当目标包含 **L 或 P** 时，才判断已有结果是否值得作为可选 Reference Context。

Router 不解释材料、不生成结论，也不建立共享黑板。

---

## D — Deep Read / 忠实深读

当用户主要想知道：
- 这篇文章或文档到底讲了什么；
- 作者如何一步步推出结论；
- 保留故事、比喻、术语和推理过程；
- 做忠实的深读、总结或解读。

→ 使用 `skills/article-deep-read-v6.1/SKILL.md`

**中心问题：我理解原材料了吗？**

### Context Policy

Deep Read 只读取 Raw Source、用户对当前任务的直接要求和必要的原始用户上下文。

**不得读取或消费 Review / Learning / Practice 的输出。**

---

## R — Review / 独立审阅

当用户主要想知道：
- 这份材料写得对不对、够不够、有没有遗漏或冲突；
- 数字、逻辑、流程、责任、边界或方案是否成立；
- 哪些地方会改变结论、风险或行动；
- 是否值得修改。

→ 使用 `skills/vibe-review-v0.10/SKILL.md`

**中心问题：这份材料可靠吗、够用吗？**

### Context Policy

Review 只读取 Raw Source、用户对当前 Review 任务的直接要求和必要的原始用户上下文。

即使 Deep Read 已经运行过，**Review 也不得读取 Deep Read 输出**；同样不读取 Learning / Practice 的结果。

### Coverage Policy

Review 先完整覆盖，再判断重要性：

`Atomize Source → Reconcile Coverage → Review Every Unit → Assess Materiality → Report Selectively`

---

## L — Learning / 系统学习

当用户主要想：
- 真正理解一个概念、系统、人物、事件或方法；
- 从问题或材料中形成自己的知识模型；
- 追到底层机制、边界和可迁移关系；
- 发现还缺什么，并通过必要的追问、研究或专家交流继续补齐；
- 把知识投影到会议、实施或决策。

→ 使用 `skills/system-learning-v0.5.1/SKILL.md`

**中心问题：我真正懂了吗？**

当用户觉得概念“太抽象、像生造的、实际没区别”，Learning 必须先降回具体对象，用能拉开差异的真实情境解释“到底哪一步变了”，而不是继续增加新的上位术语。抽象应该压缩已经理解的事实，而不是成为解释的起点。

Learning 可以选择性参考已有 D / R / P 结果，但它们只是 Reference Context。

### Learning Probe

当真正阻塞 Knowledge Model 的缺口来自：
- 用户自己的观察或上下文；
- 概念含义仍然模糊；
- 一个未验证前提；
- 必须由专家或业务方确认的事实；

Learning 可以一次提出一个高信息价值问题，并根据回答更新 Knowledge Model。

如果问题是为了“测试用户会不会”，则不是 Learning Probe，而应路由 Practice。

---

## P — Practice / 应用演练

当用户主要想：
- 检验自己是不是真的学会；
- 把知识放进工作、工程、业务或其他真实情境；
- 不要继续讲答案，而是让我做判断、设计、排错或选择；
- 通过条件变化、反例、连续追问或模拟面试检验知识迁移；
- 找出“会解释但不会用”的 Application Gap。

→ 使用 `skills/practice-v0.1/SKILL.md`

**中心问题：我真正会了吗？**

Practice 可以选择性参考 D / R / L 的结果，其中 Learning Knowledge Model 通常是最重要输入。

### Practice Probe

Practice 的问题不是为了获得未知事实，而是为了暴露用户当前能力。

默认：

`Diagnose → Situate → Perform → Stress → Debrief`

面试只是 Practice 的一种 stress surface，不是独立任务类型。

---

## “提问”如何路由

不要因为用户要求“问我问题”就建立 Questioning 路由。

判断提问目的：

- “这个问题我还没想清楚，先问我最关键的一件事，帮助我建立理解。” → **L**
- “我要访谈专家，把当前知识缺口转成最值得确认的问题。” → **L**
- “不要再讲，出场景测试我是否真正理解。” → **P**
- “像面试官一样连续追问，看我能不能解释和应对变化。” → **P**

> **L 的问题为了获得知识；P 的问题为了暴露能力。**

---

## 非对称协作

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
        │ knowledge model
        ▼
     Practice
        P
        │
        │ performance gaps
        └──────────────► Learning
~~~

允许：
- D → L
- R → L
- D → P
- R → P
- L → P
- P → L（主要回流 Performance Gap、暴露出的误解和新的 Knowledge Gap）

禁止：
- 任何 Skill → D
- 任何 Skill → R
- D ↔ R 之间直接传递结果

---

## Reference Context 的三条规则

- **Reference ≠ Evidence**
- **Transform, don't copy**
- **Selective, not mandatory**

这些规则只适用于 L / P；D / R 不消费 sibling results。

---

## 四条认知边界

- **D — source-centered**：我理解材料了吗？
- **R — judgment-centered**：材料可靠吗、够用吗？
- **L — learner-centered**：我真正懂了吗？
- **P — performance-centered**：我真正会了吗？

---

## 最终原则

> **Read what it says. Review whether it holds. Learn how it works. Practice whether you can use it.**

Questioning 作为内部控制策略服务于 Learning 和 Practice，不再作为独立产品级 Skill。
