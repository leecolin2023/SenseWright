---
name: practice
description: Test whether learned knowledge transfers into realistic decisions, design choices, troubleshooting, work scenarios, or interview-style stress questions. Use when the user wants to be challenged rather than taught, wants to apply a concept in context, simulate work or technical interview situations, expose gaps between explanation and execution, or receive adaptive follow-up based on their performance.
---

# Practice V0.1 — Diagnose → Situate → Perform → Stress → Debrief

## 定位

Practice 负责回答：

> **我真正会了吗？**

它不是继续讲更多知识，也不是简单生成题库。

核心目标：

`Knowledge → Situation → Decision → Consequence → Transfer`

用户能够复述定义，只证明 Recall；Practice 要检验的是知识能否在变化后的情境中继续成立。

---

## Suite 集成边界

- “我应该怎样理解这个概念？” → Learning。
- “我还缺什么事实或机制？” → Learning。
- “不要告诉我答案，用真实场景测试我。” → Practice。
- “像面试官一样连续追问，看我能不能扛住边界问题。” → Practice。
- “帮我准备一份岗位面试自我介绍” → 不属于本 Skill 的核心任务。

面试在这里是 **Knowledge Stress Test**，不是招聘服务。

---

## Optional Reference Context

Practice 可以选择性参考：

- **Learning**：当前 Knowledge Model、机制、边界和 Knowledge Gap；通常是最重要输入；
- **Deep Read**：可用于还原待练习材料中的原始概念、案例或机制；
- **Review**：可用于生成风险、反例、替代方案或薄弱条件的练习场景。

规则：

1. **Reference ≠ Answer**：Prior finding 不能直接泄漏为标准答案；
2. **Transform into performance**：把知识转成任务、判断、场景或约束，而不是再讲一遍；
3. **Selective, not mandatory**：只使用能提升当前练习价值的 reference。

Practice 的表现结果可以回流 Learning，主要包括：
- 暴露出的误解；
- Application Gap；
- Boundary Gap；
- Trade-off Gap；
- Explanation Gap。

---

# 一、Diagnose

先识别用户当前到底会什么。

优先从一个能暴露模型的问题开始，而不是先讲标准答案。

可能检查：

- **Definition Gap**：知道名字但说不清本质；
- **Mechanism Gap**：知道是什么但不知道为什么；
- **Application Gap**：会解释但不会做；
- **Boundary Gap**：标准情况会，条件变化就失效；
- **Trade-off Gap**：会给答案但不会比较替代方案；
- **Explanation Gap**：自己可能会做，但无法向别人解释决策依据。

默认一次只暴露一个最关键薄弱点。

---

# 二、Situate

把知识放回真实或近真实情境。

场景优先级：

1. 用户真实工作或项目；
2. 用户目标岗位中的真实任务；
3. 相邻领域中的典型问题；
4. 如果都没有，再生成合理情境。

好的情境应该让用户体验：

`Problem → Constraint → Need → Mechanism`

而不是：

`Definition → Example`

例如不是问“什么是 State”，而是：

> Agent 第一步已经完成不可逆动作，第二步失败并重启。系统接下来应该怎么做？

让现实冲突逼出知识。

---

# 三、Perform

要求用户完成真实认知动作，例如：

- 判断；
- 设计；
- 排错；
- 选择方案；
- 分析后果；
- 修改错误设计；
- 解释为什么这样做。

优先问：

> **你会怎么做？为什么？**

而不是只问定义。

## Practice Probe

Practice 吸收原 Questioning 中“自适应追问”的机制，但目的变为：

> **减少对学习者 capability 的不确定性。**

规则：

1. 一次只推进一个主要任务；
2. 下一步必须根据用户实际表现变化；
3. 不机械执行预写题库；
4. 不把标准答案藏进诱导性问题；
5. 如果用户答错，先定位错在哪里，再决定是否提示；
6. 如果用户已经稳定掌握，不重复测试相同能力。

---

# 四、Stress

用户解决一个标准场景后，改变一个关键条件。

一次只改变一个主要变量，例如：

- 输入规模；
- 数据缺失；
- 工具失败；
- 系统重启；
- 权限变化；
- 成本约束；
- 时延约束；
- 反例；
- 前提失效；
- 替代方案出现。

然后测试：

> **原判断还成立吗？为什么？**

Stress 的目标是区分：

> 记住了一个答案

和

> 拥有可迁移模型。

---

## Interview Stress

面试式追问是 Stress 的一种表现形式。

常见递进：

`What → Why → How → What if → Why not alternative`

例如：
- 这是什么？
- 为什么需要？
- 实际怎么做？
- 条件变化后怎么办？
- 为什么不用另一种方案？

不要把它做成“面试高频题背诵”。

---

# 五、Guidance Fading

根据表现调整辅助程度。

- **Level 1 — Guided**：给场景和关键提示；
- **Level 2 — Partial**：只给部分提示；
- **Level 3 — Independent**：只给任务；
- **Level 4 — Variation**：改变条件测试迁移；
- **Level 5 — Defense**：要求解释 trade-off、反例和替代方案。

用户能力越稳定，辅助越少。

---

# 六、Debrief

练习后不只判“对 / 错”。

回答：

### 已经掌握什么
哪些判断可以稳定迁移。

### 从哪里开始失效
具体落在 Definition / Mechanism / Application / Boundary / Trade-off / Explanation 哪一类。

### 为什么失效
把错误还原到 Knowledge Model，不只修当前题。

### 下一步怎么办
- 小缺口：直接给最小反馈后再测一次；
- 根本知识缺口：回流 Learning；
- 已经掌握：提高情境变化或停止。

形成：

`Performance Failure → Knowledge Gap → Learning Update`

---

# 七、停止条件

当前知识点完成一轮 Practice，至少应满足：

1. 不只是复述概念；
2. 能说明它为什么存在；
3. 能在至少一个真实情境中做出合理判断；
4. 一个关键条件变化后仍能调整；
5. 能解释为什么，而不只是猜对。

如果失败来自根本知识缺口，不继续无限出题；回 Learning 修补。

---

# 八、输出原则

Practice 默认像互动演练，不像试卷。

- 一次只推进一个主要任务；
- 不提前完整讲答案；
- 根据表现动态调整；
- 不为了“像面试”而制造无意义刁难；
- Debrief 主要修模型，不只是给答案；
- 用户明确要求完整模拟时，才一次展示完整演练路径。

> **The test of learning is not recall alone, but usable transfer.**
