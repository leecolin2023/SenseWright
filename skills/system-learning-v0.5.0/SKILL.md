---
name: system-learning
description: Turn a concept, system, person, event, method, question, or source material into a reusable knowledge model, identify the few gaps that block real understanding or use, and adaptively probe for missing user- or expert-specific information when needed. Use when the user wants to truly understand something for future reasoning, meetings, implementation, or decisions rather than merely summarize, critique, or be tested on it.
---

# System Learning V0.5.0 — Model → Gap → Probe → Update → Use

## Suite 集成边界

本 Skill 在 SenseWright 中承担 **L — Learning**。

目标是：

> **形成用户自己的知识模型，并把真正阻塞理解或使用的未知继续补齐。**

- “原文讲了什么” → Deep Read。
- “材料哪里有问题” → Review。
- “我应该怎样理解、为什么会这样、还缺什么” → Learning。
- “不要再讲，用场景测试我是不是真的会” → Practice。

Questioning 不再作为独立 Skill。原来的知识型追问能力并入 Learning。

---

## Optional Reference Context

Learning 的主要依据仍是 Raw Source / 用户事实 / 当前任务。

可以选择性参考：

- **Deep Read**：作者结构、关键概念、机制、案例等 source reconstruction；
- **Review**：关键分歧、证据薄弱处、风险、替代解释等 judgment；
- **Practice**：暴露出的误解、Application Gap、Boundary Gap、Trade-off Gap 等 performance findings。

三个规则：

1. **Reference ≠ Evidence**：涉及“原文到底说了什么”仍回 Raw Source；涉及外部事实仍需要相应证据。
2. **Transform, don't copy**：Reference 应改变 Learning 的模型、注意力或 Gap，而不是被原样复制。
3. **Selective, not mandatory**：只有 reference 能明显改善当前学习任务时才使用。

当用户指定以附件/材料为学习基础时，材料未支持的外部知识不得静默写成材料结论。

---

## 目标

Learning 保留三层主体：

`Build Model → Find Gaps → Project to Use`

但 Find Gaps 内部允许出现一个轻量循环：

`Gap → Probe / Research → Update Model`

这不是为了把 Learning 变成不停提问，而是为了：

> **当一个缺口真的阻塞当前 Knowledge Model 时，用最小动作减少不确定性。**

---

# 一、Build Model

## 1. 先验证命题，再解释命题

输入是问题、观点或反常识命题时，不默认前提已经成立。

先区分：
- 用户真正观察到的现象；
- 夹带的未经验证前提；
- 可以靠结构推理澄清的部分；
- 必须依赖数据、史料、案例、专家或外部证据确认的部分。

> 先确认“发生了什么”，再解释“为什么”。

如果命题被改写，后续知识结构必须跟着重建。

---

## 2. 不要孤立解释概念

把知识放回系统、关系、事件和状态变化中。

优先回答：

> 它为什么出现？如果没有它会发生什么？它在整个系统哪里？一件真实事情发生时它做了什么？

对于动态知识，优先使用事件链：

`触发 → 判断 → 动作 → 状态变化 → 反馈 → 下一步`

---

## 3. 追到底层机制

流程说明“发生了什么”，机制说明“为什么这样工作”。

不要停留在名词替换。

优先找真正决定行为的机制，例如：
- 表示与计算；
- 控制权；
- 状态拥有；
- 信息验真；
- 风险计量；
- 资源占用；
- 反馈；
- 失败恢复；
- 激励与约束。

---

## 4. 不服从原材料结构

材料只是输入，不是最终 Knowledge Model。

允许重新分层、抽象、连接和纠偏。

但：

> **重构不等于新增事实。**

区分：
- Source-supported；
- Derived synthesis；
- External extension。

简单判断：

> **假设模型除了当前材料什么都不知道，这个结论还能推出吗？**

不能推出的，就不能包装成“基于材料得到”。

---

## 5. 最终形成自己的分析框架

Knowledge Model 应该帮助用户以后处理相邻问题，而不是只回答这一次。

完整学习单元尽量留下 Knowledge Note：
- 核心判断；
- 对象模型；
- 上位结构；
- 关键机制或事件；
- 重要边界与纠偏；
- 可迁移分析框架。

---

# 二、Find Gaps

Knowledge Model 建立后，只保留真正阻塞下一步的 Gap。

### Knowledge Gap

> 概念、机制或关系仍不清楚。

### Validation Gap

> 当前判断仍只是合理假设，缺数据、案例、实验、反例或基线。

### Context Gap

> 缺的是用户自身情况、业务现场、专家事实或当前环境信息。

### Decision Gap

> 不存在唯一知识答案，需要业务、专家、技术或管理选择。

### Application Gap

> 我会解释，但一到真实操作就不会。

Application Gap 如果需要通过“让用户做一次”来验证，应交给 Practice，而不是继续讲更多知识。

---

# 三、Adaptive Learning Probe

只有当 Gap 阻塞当前模型，而且最合适的信息源是用户、专家或后续交流时，才提问。

## 目的

> **减少 knowledge uncertainty，而不是测试用户。**

### 可按需使用的 Probe Lens

- **Clarify**：这里的 X 到底指什么？
- **Reason**：为什么会得出这个判断？
- **Evidence**：依据来自数据、案例、经验还是推断？
- **Assumption**：哪些前提还没有验证？
- **Alternative**：还有什么可以解释同一现象？
- **Mechanism**：A 到 B 中间到底怎么发生？
- **Boundary**：什么时候不成立？
- **Missing**：哪条缺失信息最影响当前模型？
- **Action**：最小验证动作是什么？

这些 Lens 不是固定 Checklist。

## 提问规则

1. 默认一次只推进一个最有信息价值的问题；
2. 下一问根据新回答重新选择，不预设整棵问题树；
3. 先澄清事实和概念，再挑战原因；
4. 问用户只能知道的信息，不把本可以自己解释的问题全部反问给用户；
5. 不把自己的答案藏进诱导性问题；
6. 如果外部公开资料才是合适信息源，应研究或核实，而不是把检索任务甩给用户。

### 状态更新

每次 Probe 后区分：

- **Confirmed**
- **Assumed**
- **Unknown**
- **Contradiction**
- **Next Gap**

然后更新 Knowledge Model。

### 停止条件

当：
- Knowledge Model 已足够回答当前目标；
- 关键 Gap 已转成可验证动作；
- 下一步必须依赖新的数据/专家/实验；
- 继续语言追问的信息增益很低；

停止追问并继续 Project to Use。

---

# 四、Project to Use

把知识投影到用户下一步。

### 继续学习
进入当前最值得补的一层，而不是生成课程目录。

### 会议 / 专家交流
把 Context / Validation / Decision Gap 转成少量高信息价值问题。

这属于 Learning 的知识获取动作，不需要单独 Questioning Skill。

### 开始实施
形成：

`第一批输入 → 第一步动作 → 初版产物 → 如何验证 → 下一轮`

### 方案 / 决策
形成：

`选择 + 支撑证据 + 权衡 + 尚未确定的信息`

### 转入 Practice

当用户需要验证：

> “我是不是只会解释，实际不会用？”

则把当前 Knowledge Model 和关键边界交给 Practice。

---

# 五、输出原则

Learning 默认仍然以“形成理解”为主，不要因为吸收了 probing 就退化成苏格拉底问答机器人。

如果当前信息已经足以建立高质量模型：

> **直接教清楚。**

只有真正需要用户/专家新信息时才问。

如果用户明确要求“通过追问和我一起想清楚”，可以提高 Probe 比例，但仍以 Knowledge Model 的形成与更新为终点。

---

# 六、验收标准

一次高质量 Learning 结束后，用户应得到：

1. 一套稳定且可迁移的 Knowledge Model；
2. 对 source / derived / external 边界有正确认识；
3. 关键 Gap 被识别，而不是列出所有没学过的知识；
4. 必要的追问确实减少了 knowledge uncertainty；
5. 当真正问题是“会不会用”时，能够及时交给 Practice。

> **Learning 的终点是“我真正懂了”，不是“我回答了很多问题”。**
