---
name: practice
description: Transfer an already established knowledge model into situated capability through realistic tasks, consequential branch discovery, adversarial condition changes, performance, evidence-based evaluation, and feedback to Learning. Trigger for substantive interview follow-ups, case defense, engineering execution, debugging, or decision rehearsal; not for generic quiz generation or simple conceptual explanation.
---

# Practice V0.3 — Situated Knowledge Transfer

## Mission

**Knowledge Model → Situated Capability, with evidence of transfer and a repair path.**

Learning 建立“真实问题 → 必要机制 → 具体实现/证据 → 边界”的因果知识模型；Practice 把已有模型放入具体情境，在关键分支与变化约束中要求**应对、判断或行动**，然后验证表现。Practice 不再等于工程落地，也不退化为记忆测试。

核心问题：**换一个真实条件，我能否使用这个模型做出可辩护的回答、选择或行动；不行的原因是什么？**

Practice 的四类主要场景：技术面试与交叉质询、工程执行与排障、架构/业务决策、研究假说与反事实检验。它们共用方法，产物随任务不同。保留 V0.2 Engineering Walkthrough 作为工程场景中的可选完整路径。

## 0. Routing & Boundary

- 用户目标是**学懂机制或从零建立知识模型**：L，遵循本轮独立 D + R → L。即使学习中包含一两个最小验证问题，也不因此触发 P。
- 用户已具备/已提供知识模型，要求**面试深挖、真实案例应对、失败注入、迁移检验、实际方案辩护或工程实施**：P。P-only 可以读取历史 L/D/R 或直接提供的模型，不自动重跑 D/R。
- **“出 10 道题”** 是一般题库请求，除非用户明确要求按真实知识模型做分支压力测试、观察应对并反馈；一般题库不必触发 SenseWright。
- 简单问答、背诵、格式变换、纯 artifact 制作不强制 P。纯执行/修 bug 可直接做事，只有用户要求建立可迁移实践能力时才按 P 方法交付。
- 发现根本机制缺口时，标注并转入 L；若实际发起新的 L，必须重新满足该轮 D/R 前置条件。**不能把 P 内的临时追问冒充已完成独立 D/R/L。**

## 1. Context Contract — Ground the Target

优先使用：用户已经建立的 Knowledge Model、原始源码/材料与可查证事实、用户真实项目/目标岗位、现有证据与未知。按优先级选择真实场景，不发明用户经历、运行日志或测量结果。

开始前在内部确定：
- 已知主干：一句话描述原有机制和成立条件，区分知识事实与框架实现；
- 当前任务：要回答/实施/判断什么，成功与安全底线是什么；
- 场景约束：人员、系统、数据、时序、权限、规模、可用执行环境；
- 证据级别：**已实际运行 / 直接查证源码 / 可复现推演 / 假设 / 未知**。

缺少数据不影响讨论时，采用明确假设；会实质改变实践路径时询问最少量问题。不要把“原理讲解”包装成场景。

## 2. Branch Discovery — Find Consequential Branches

从真实情境的**关键假设、状态转换、异常、竞争方案、信任边界、指标、证据缺口**探索分支，而不是给主干每个术语随意附 5 个“为什么”。

每个候选分支使用反事实测试：
> **若该分支答案或条件不同，是否改变机制解释、行动选择、预测结果或成败判断？**

仅保留能说明以下至少一项的分支：
1. 区分两个以上可信解释或设计；
2. 揭露原主干默认但未证明的关键假设；
3. 改变风险、权限、成本、结果或恢复策略；
4. 提供能将未知缩小的观察/最小实验。

按**决策影响 × 证据可获得性 × 当前任务相关性**挑选一到三个高价值分支，优先深入其中一个。数量不是目标；简单场景可以零分支。分支深度不是术语密度，也不是“为什么”追问次数。

## 3. Perform — Real Response Before Ideal Answer

根据目标选择 **one of**：
- 面试/方案辩护：提出一个有边界的真实追问；用户参与时先让用户回答，再诊断与追问；没有用户回答时明确采用 **model-self-drill / 示范应答 + 独立反驳**，绝不评分用户能力。
- 工程执行：从系统位置、接口/状态到最小完整流程，再实际运行与校验。V0.2 的 System Placement → End-to-End → Verification → Troubleshooting → Artifacts 作为本模式的深度合同，不强加给非工程任务。
- 研究/业务/决策：写出可检验的备选解释/方案，选择证据或决策动作，保留目标与不可牺牲的约束。

每轮应答要交代：判断、必要机制、具体实例/证据、成立条件、未知和下一步动作；不能只说“应该考虑幂等、监控、审计”。

## 4. Challenge — Change One Important Condition

优先采用**最有区分力**的一次变化：在执行前与执行后发生超时、同一请求重放、模型上下文改变、部分成功、权限改变、数据失真等。指出**哪一步首先变化，原答案哪部分仍成立，哪部分失效**。

避免一次改变多个变量造成混淆；确需多变量时显式分离。不能从“系统记录了错误”推导“外部副作用必定已取消”。

## 5. Verify — What Was Actually Demonstrated?

- 解释类：用反例、源码、事实证据或跨场景预测校验主张；
- 面试类：检验回答能否承受追问、反事实和必要证据，而非关键词命中数；
- 工程类：实测输入输出、状态变化、Trace、故障注入、回归断言，说明测试环境；
- 研究类：对比竞争机制的预测与可获得证据。

严格区分 **source-inspected**, **executed probe**, **illustrative trace**, **unverified**。检验无法执行就提出最小实验和预计区分结果，不得报告 PASS。静态文件检查不证明 Skill 的行为优越性。

## 6. Diagnose & Feedback

针对重要失败分流：
- **Knowledge Gap → Learning**：不会解释必要机制/关键前提，作为新的主问题登记；只有真的启动 L 才执行新的 D/R。
- **Evidence Gap → Investigation/Probe**：机制可能正确，但需要运行、阅读更精确源码或核对真实流程；不要自动再讲一遍概念。
- **Application/Decision Gap → Continue P**：原理充分，但无法在具体条件下做取舍、排序、应对或执行；
- **Execution Defect → Repair & Reverify**：实现已失败，修复并保留复现证据；
- **Out of Scope → Park**：不影响当前决定，标记，不扩大主干。

**New Branch → Qualified Research Question**：仅当新枝干的回答足以改变重要结论，并且目前缺少机制理解时，提升为新的 Learning 主问题。原主干不因每个边枝都改写。

## 7. Deliverable — Adaptive, Not a Fixed Worksheet

默认一份简洁但完整的实践记录：
1. 任务、已知主干、成功条件与证据级别；
2. 关键分支与它改变结果的理由；
3. 一次真实应对/执行的具体过程；
4. 一个能区分机制的条件变化或反例；
5. 实际验证证据（若无，明确未验证）；
6. 诊断、是否回流 L、最小下一步。

无需每次打印 6 个固定标题。多轮模拟面试以**一次一问 → 真实应答 → 必要追问**优先；如果用户要求一次完整示范，可提交完整自演练，但必须标明**这不是对用户的能力评分**。

## 8. Built-in Stabilization Gate

交付前内部完成并修复（不留“待 Review”占位）：

- **Task Fidelity**：实际任务是否是深挖迁移，而非只列题/写教材？
- **Branch Value**：关键分支的答案改变哪一个决策/判断？若无，删除。
- **Challenge Discrimination**：条件变化是否使不同机制给出不同预测？若无，调整。
- **Evidence Honesty**：是否把模拟、源码文档、假设和实际运行严格分开？
- **Transfer**：实践结论包含可迁移不变量和场景特有选择吗？
- **Repair Routing**：缺口应继续 P、做 Probe、回流 L，还是暂停？
- **Scope**：没有为炫技增加不必要的分支、产物、指标或工程重量。

不能满足就修订；不具备环境和证据就标注范围内的 Not Verified，而不是宣布通过。Practice 可以是“关键限制已定位、下一实验明确”的有效产物，但**不能伪装已具备能力**。

## 9. Anti-patterns

- 把 Practice 收缩成“如何打开 IDE 施工”，从而排除面试、反事实和决策；
- 为每个术语批量生成追问题库；
- 模型自己回答后宣称用户“已掌握”；
- 把 Review 的审稿批评当作对人的实操能力评分；
- 把演示输出当作生产验证，或把 Harness 的日志保证冒充外部事务 exactly-once；
- 发现全新核心概念时在 P 内偷偷再造完整 L，却绕过必要 D/R；
- 因出现一个技术术语就强迫展开全套工程架构。

**Final rule:** Practice is where understood knowledge meets consequential reality, not where we simply recite more knowledge.
