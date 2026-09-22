---
name: sensewright
description: Route complex information and knowledge-work tasks among faithful deep reading, independent review, systematic learning, and adaptive questioning. Use when the user wants to understand what source material says, evaluate whether a document or argument is sound or decision-useful, build a reusable mental model, discover what to ask next, conduct an interview with follow-up probes, or combine those goals. Keep routing separate from content production and preserve source boundaries across modes.
---

# SenseWright V2.4.0

## 核心设计

> **统一管理，不融合认知任务。**

只维护一个 Suite、一个入口 `SKILL.md`。内部保留四种彼此独立的认知模式：

- **D — Deep Read**：忠实理解原材料。
- **R — Review**：独立评价原材料。
- **L — Learning**：把材料、问题或主题转化为自己的知识模型，并继续进入使用。
- **Q — Questioning**：找到当前最值得知道的下一件事，通过连续追问减少关键不确定性。

Router 只判断“当前需要哪种认知能力”，不提前替子 Skill 做内容生成。

---

## D — Deep Read / 忠实深读

当用户主要想知道：
- 这篇文章/这份文档到底讲了什么；
- 帮我总结、梳理、提炼、解读；
- 保留作者的故事、比喻、术语和推理过程；
- 做忠实的深读笔记。

→ 使用 `skills/article-deep-read-v6.1/SKILL.md`

**判断标准：用户的中心对象是“原材料本身”。**

---

## R — Review / 独立审阅

当用户主要想知道：
- 这份材料写得对不对、够不够；
- 有什么逻辑、证据、架构、方案或表达问题；
- 如果独立重想一次，会不会得出不同结论；
- 哪些地方真正值得修改。

→ 使用 `skills/vibe-review-v0.9/SKILL.md`

**判断标准：用户的中心任务是“判断这份材料的质量或决策价值”。**

---

## L — Learning / 系统学习

当用户主要想：
- 真正学会一个概念、系统、人物、事件或方法；
- 不只是复述材料，而是形成自己的理解框架；
- 找出还卡在哪里、下一步应该学什么或验证什么；
- 把知识进一步转成会议问题、实施步骤或决策输入。

→ 使用 `skills/system-learning-v0.4.3/SKILL.md`

**判断标准：用户的中心对象是“自己的知识模型”，原材料只是输入。**

如果用户提供了文章/文件来学习：
- 可以重组材料，不必服从原目录；
- 但不得把材料未支持的外部知识偷偷写成材料结论；
- 只有用户要求研究、核实、扩展时，才引入外部信息，并区分来源、推断和原材料内容。

---

## Q — Questioning / 连续追问

当用户主要想：
- 不要马上给答案，而是通过连续追问把问题想清楚；
- 判断“下一步最值得问什么”；
- 为访谈、专家交流或需求调研设计主问题与追问；
- 根据上一轮回答动态决定下一问，而不是拿固定问题清单机械执行；
- 把模糊判断逐步推进到事实、证据、机制、边界或可验证行动。

→ 使用 `skills/questioning-v0.1/SKILL.md`

**判断标准：用户的中心任务是“通过提问减少关键不确定性”。**

默认一次只推进一个最重要的问题；只有用户明确要求访谈提纲或问题清单时，才一次输出多个主问题及必要 Probe。

---

## “读懂、学会、继续问”的边界

按用户当前目标判断：

- “这篇文章到底说了什么？” → **D**
- “作者为什么这样推到这个结论？” → **D**
- “这份材料哪里站不住？” → **R**
- “这个概念我到底应该怎么理解？” → **L**
- “基于这篇文章，帮我建立一套自己的知识框架。” → **L**
- “我还缺什么知识？” → 通常 **L**
- “不要回答，先问我最重要的一个问题，和我一起想清楚。” → **Q**
- “我要访谈研发负责人，帮我准备主问题和追问。” → **Q**
- “先帮我建立理解，再通过追问把剩余不确定性问清楚。” → **L + Q**

只有当不同路由会明显改变交付方式、而上下文又无法判断时才询问。

---

## 复合意图：组合，不制造 Skill 组合爆炸

D / R / L 仍按用户目标自由组合。

Q 不为每个组合新增新 Skill 名称，而是作为“继续询问和获取新信息”的能力叠加到已有任务上。例如：

- 读懂后继续追问 → **D + Q**
- 学习后围绕 Knowledge Gap 连续追问 → **L + Q**
- 审阅后把关键不确定性转成专家访谈 → **R + Q**
- 单独把一个模糊问题问清楚 → **Q**

执行原则：
1. D / R / L 各路尽量直接读取原始材料，不让某一路的压缩结果成为另一路唯一输入；
2. Q 维护当前对话中的认知状态，根据新回答更新下一问；
3. 有原材料时，Q 应保持原材料可访问，不把其他分支的解释误当成原文事实；
4. Q 可以使用 D / R / L 的阶段性结果作为工作状态，但需要继续区分“原材料”“已有判断”“用户新回答”；
5. 最后按用户目标自然合并，不强制打印内部路由过程。

---

## 四条认知边界

- **D 是 source-centered**：忠实还原作者。
- **R 是 judgment-centered**：独立判断材料是否成立、是否完成任务。
- **L 是 learner-centered**：建立用户以后还能继续使用的知识模型。
- **Q 是 inquiry-centered**：选择最有信息价值的下一问，并根据回答持续更新。

不要因为四者放在同一个 Suite 里，就把它们融合成一个大 Prompt。

---

## 长文与复杂任务

Router 不自建 Document Map、不跑 Claim Coverage、不重复实现 Learning 或 Questioning 的内部框架。

把原材料、对话状态和用户目标交给对应子 Skill，由子 Skill 自己决定：
- 是否启用长文结构处理；
- 是否检查命题前提；
- 是否重构知识模型；
- 是否触发专项审阅；
- 是否澄清概念、追事实、查证据、追机制或停止继续提问。

---

## 最终原则

> **用户只管理一个 Skill；SenseWright 内部根据认知目标切换模式。**

统一的是入口、路由和管理方式，不是不同任务的思维过程。
