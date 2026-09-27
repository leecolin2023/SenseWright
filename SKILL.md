---
name: sensewright
description: Route complex information and knowledge-work tasks among faithful deep reading, independent review, systematic learning, and engineering practice. Use when the user wants to understand source material, judge whether a document or argument is sound, build a reusable knowledge model, or turn an understood concept into executable engineering know-how in a realistic project. Deep Read and Review remain source-isolated; Learning and Practice may selectively use prior outputs as attributed reference context rather than inherited truth.
---

# SenseWright V2.7.0

## 核心设计

> **统一入口，独立职责；提问是策略，不再是一级任务。**

SenseWright 维护四种一级认知模式：

- **D — Deep Read**：先忠实恢复原材料的认知结构，再按交付意图选择完整覆盖型或认知提炼型压缩。
- **R — Review**：完整覆盖原材料后独立评价。
- **L — Learning**：先把当前对象落到真实情境中讲清楚；模型建立后，在有明显认知增量时改变一个关键前提、观察角度、变量或边界，暴露适用范围；对机制型技术知识进一步让机制跑起来，再形成可复用知识模型。
- **P — Practice**：把已经理解的知识放进真实工程场景，完整走通设计、实现、运行、验证、排错和工程化，把 Knowledge Model 转成 Executable Engineering Model。

Questioning 不再作为独立路由。

- **Learning Probe** 继续用于减少 knowledge uncertainty；
- **Practice 不再以提问测试用户能力为核心**。只有关键工程约束缺失且会实质改变实施路径时，才提出最少量澄清问题。

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

→ 使用 `skills/article-deep-read-v6.4/SKILL.md`

**中心问题：我理解原材料了吗？**

### Context Policy

Deep Read 只读取 Raw Source、用户对当前任务的直接要求和必要的原始用户上下文。

**不得读取或消费 Review / Learning / Practice 的输出。**


### Compression Contract

Deep Read 在完成材料理解后，再根据用户的交付意图选择压缩契约：

- **Coverage-Preserving**：完整保留所有具有独立意义的认知单元，只压缩单元内部冗余；
- **Cognitive-Synthesis**：允许跨单元归并与抽象，但继续压缩不能改变陌生读者最终形成的核心认知模型。

不要按“文章 / 会议 / 制度”等材料类型固定路由。Compression Contract 决定的是**哪些信息允许消失**，不是输出应该有多长。


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

→ 使用 `skills/system-learning-v0.5.3/SKILL.md`

**中心问题：我真正懂了吗？**

当用户觉得概念“太抽象、像生造的、实际没区别”，Learning 必须先降回具体对象，用能拉开差异的真实情境解释“到底哪一步变了”。模型建立后，如果改变一个关键前提、观察角度、变量或边界能够显著改变理解，应按需做一次 Boundary Variation，观察哪些结论仍成立、哪些消失、哪些问题已经变得不可回答；这不是强制 checklist，也不是科学论证流程。对于算法、系统、Agent、RAG、数据库等 mechanism-heavy knowledge，仅知道“为什么需要”还不够：应尽量让一个最小实例真实跑一遍，并用条件变化检验当前机制模型能否解释结果。抽象应该压缩已经理解的事实，而不是成为解释的起点。

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

## P — Practice / 工程实践

当用户主要想：
- 已经理解一个概念，但不知道真正打开 IDE / 系统后第一步做什么；
- 把 RAG、Agent、数据库、工作流等技术放进真实项目完整实现一遍；
- 看清组件、接口、数据、状态、配置和工程产物如何连接；
- 让一个具体输入真正跑完整链路，而不是只看架构图；
- 知道如何测试、验收、排错、观测和处理边界问题；
- 从“知道原理”跨到“知道怎么做”。

→ 使用 `skills/practice-v0.2/SKILL.md`

**中心问题：如果现在真的要把它做出来，我该怎么做？**

Practice 可以选择性参考 D / R / L 的结果，其中 Learning Knowledge Model 通常是最重要输入。

默认：

`Ground Scenario → Engineering Model → Implement End-to-End → Run One Path → Verify → Troubleshoot → Operationalize → Generalize`

Practice 的主产物是一份 **End-to-End Engineering Walkthrough**，并应明确真正需要创建、运行和验收的工程产物。

它不是默认的知识测验、题库或模拟面试工具。

---

## “提问”如何路由

不要因为用户要求“问我问题”就建立 Questioning 路由。

判断提问目的：

- “这个问题我还没想清楚，先问我最关键的一件事，帮助我建立理解。” → **L**
- “我要访谈专家，把当前知识缺口转成最值得确认的问题。” → **L**
- “我已经理解 RAG 文档切分，现在用真实制度库把实现、检索、评测和排错完整走一遍。” → **P**
- “我知道 Agent State 是什么，现在告诉我真实工程里状态怎么建模、持久化、重启恢复和测试。” → **P**

单纯“出题考我 / 模拟面试 / 连续追问”不再因为测试形式自动路由 Practice；Practice 的核心目标已经从 **Knowledge Assessment** 转为 **Engineering Transfer**。

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
        │ implementation-discovered gaps
        └──────────────► Learning
~~~

允许：
- D → L
- R → L
- D → P
- R → P
- L → P
- P → L（主要回流实施过程中暴露出的 Knowledge Gap、未验证前提和机制边界）

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
- **P — engineering-centered**：如果现在真的要把它做出来，我该怎么做？

---

## 最终原则

> **Read what it says. Review whether it holds. Learn how it works. Practice how it gets built and run.**

Questioning 不再作为独立产品级 Skill；Learning 可用 Probe 补知识，Practice 只在工程约束真正阻塞实施时做最少量澄清。
