---
name: sensewright
description: Route Deep Read, independent Review, Learning and engineering Practice. For every Learning request require both Deep Read and Review independently executed on the current original input before Learning starts; Learning then transforms both non-authoritative scaffolds into a grounded mental model. D and R never read each other, and P remains focused on engineering.
---

# SenseWright V2.8.1

## 核心设计

> **统一入口，独立职责；提问是策略，不再是一级任务。**

SenseWright 维护四种一级认知模式：

- **D — Deep Read**：先忠实恢复原材料的认知结构，再按交付意图选择完整覆盖型或认知提炼型压缩。
- **R — Review**：完整覆盖原材料后独立评价。
- **L — Learning**：**必须先完成独立 D + R**，再读取当轮两份认知脚手架，回到真实对象、问题链与必要机制；经过内置稳定化审阅形成 Knowledge Model。
- **P — Practice**：把已经理解的知识放进真实工程场景，完整走通设计、实现、运行、验证、排错和工程化，把 Knowledge Model 转成 Executable Engineering Model。

Questioning 不再作为独立路由。

- **Learning Probe** 继续用于减少 knowledge uncertainty；
- **Practice 不再以提问测试用户能力为核心**。只有关键工程约束缺失且会实质改变实施路径时，才提出最少量澄清问题。

---

## Router — Mandatory Prerequisite Scheduling

1. **Route Selection**：先判断用户目标是否包含 L；任何包含 L 的请求自动展开为 D + R → L。D 和 R **都必需**，不能只挑其中一个。D-only / R-only / D+R / P-only 不强制追加 L。
2. **Independent Execution**：D、R 各自从当前 Raw Input 开始，输入中不能包含对方的输出；可并行，但 L 必须等待二者均完成。宿主需为严格隔离提供独立执行上下文与 barrier。
3. **Mandatory Handoff**：L 必须消费两份当轮结果，但将其当作认知脚手架，不当作证据；只选择性吸收真正有用的具体发现，最后回到原始对象重新构建机制。
4. **Query-only**：没有独立材料仍要对用户原始问题分别进行轻量 D（问题与含义重建）和 R（前提/歧义核查），不造假来源、不过度审稿。默认最终只展示整合后 L 输出。

Router 负责编排规则；纯文字 Skill 无法证明运行时硬隔离，需执行记录验证。Practice 的历史上下文引用仍可选。

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

→ 使用 `skills/system-learning-v0.6.1/SKILL.md`

**中心问题：我真正懂了吗？**

用户觉得概念“太抽象、像生造的、实际没区别”时，先降层回到真实对象：原有行为是什么、哪里失败、最小新增机制改变了哪一步。复杂学习任务优先按 `Current Explanation → Failure → Necessary Mechanism → Next Problem (if useful)` 推进，术语和具体 Framework 后置。技术知识保留 Run Once / Boundary Variation，并区分 **Problem Knowledge / Implementation Evidence / Architecture Decision**。不要从 UNKNOWN 推出 ABSENT，更不能从 ABSENT 直接推出“应自研”。

**D 与 R 必须分别从本轮原始输入执行，并且在 L 开始前完成。** L 读取双方结果，保留 D 的认知桥梁、审视 R 的事实与证据疑点，但不能直接复制或把 Review 观点认作事实。Learning 自身的 `Problem-chain Review → Concept First-Appearance Audit → Boundary & Evidence Review → Repair` 是另外一组内置成稿 Gate，不能替代独立 R Skill。P 历史发现仍可选择性参考。

### Learning Probe

当真正阻塞 Knowledge Model 的缺口来自：
- 用户自己的观察或上下文；
- 概念含义仍然模糊；
- 一个未验证前提；
- 必须由专家或业务方确认的事实；

Learning 可以一次提出一个高信息价值问题，并根据回答更新 Knowledge Model。

用户明确要求短自测，可将其作为 Learning 的教学反馈；单纯出题、面试或测试“会不会”不自动路由 Practice。只有完整工程实施、验证与排障才进入 P。

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

## 强制上游与非对称隔离

~~~text
       Raw Input
       /       \
      v         v
   D [raw]    R [raw]
      \         /
       \       /
      [both complete]
             |
             v
         L Learning
    (return to real object)
             |
             v
        P Practice
             |
      implementation gap
             |
             +----> L (new D/R preflight)
~~~

D 和 R 互相独立，禁止对方输出进入自己的上下文。任何新 L 都要求本轮 D/R 重新运行；已有 D/R 结果不满足 fresh preflight。D、R 只直接消费 Raw Input 和原始用户上下文。

## Learning 上游三原则

- **Mandatory execution, selective incorporation**：必须执行两个上游 Skill，但不要求把全部结果照搬进最终答案。
- **Reference ≠ Evidence**：D/R 产物是脚手架，事实仍要回源验证。
- **Transform, don't copy**：Learning 重新构建真实对象、因果机制与适用边界，不输出拼贴报告。

D/R 独立执行与 barrier 要由宿主保证。静态规则和测试定义不能替代实际隔离 trace。P-only 仍可选择性使用既有 D/R/L 成果。

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
