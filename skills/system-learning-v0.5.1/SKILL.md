---
name: system-learning
description: Turn a concept, system, person, event, method, question, or source material into grounded understanding first and a reusable knowledge model second, identify the few gaps that block real understanding or use, and adaptively probe for missing user- or expert-specific information when needed. Use when the user wants to truly understand something for future reasoning, meetings, implementation, or decisions rather than merely summarize, critique, or be tested on it.
---

# System Learning V0.5.1 — Ground → Model → Gap → Probe → Use

## Suite 集成边界

本 Skill 在 SenseWright 中承担 **L — Learning**。

目标是：

> **先让当前对象真正变得可理解，再把已经理解的东西压缩成可复用知识模型，并补齐真正阻塞理解或使用的未知。**

- “原文讲了什么” → Deep Read。
- “材料哪里有问题” → Review。
- “我应该怎样理解、为什么会这样、它在现实中到底改变了什么” → Learning。
- “不要再讲，用场景测试我是不是真的会” → Practice。

Questioning 不再作为独立 Skill。用于减少 knowledge uncertainty 的追问继续留在 Learning。

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

Learning 的主体调整为：

`Ground Object → Build Model → Find Gaps → Project to Use`

必要时在 Find Gaps 内部使用：

`Gap → Probe / Research → Update Model`

这里新增的 Ground Object 不是“每次都必须举例”，而是修复一个关键失败模式：

> **不要用更高一层抽象解释用户尚未理解的抽象。**

当对象本身已经具体、用户已经掌握现实含义时，可以快速进入 Build Model；当用户明确说“没理解”“太抽象”“像生造的”“实际有什么用”“不就是 X 吗”，必须优先降层，而不是继续增加术语。

---

# 一、Ground Object

## 1. 先解释对象，再抽象方法

抽象不能替代对象知识。

优先回答：

> 这件事在现实里到底发生了什么？如果没有 X，现在怎么做？引入 X 后，哪一步真的发生变化？

只有当前对象已经能够运行起来，才继续形成上位模型。

> **抽象应该压缩已经理解的事实，而不应该成为解释的起点。**

对于人物、事件、业务、系统和工程概念，默认先保留对象本身的知识密度；只有当材料自然暴露出更通用的方法时，再继续上提。

---

## 2. 对“X 和 Y 有什么区别 / 为什么需要 X”优先做 Contrastive Grounding

当用户质疑两个概念差异是否真实，或觉得某个设计是“生造出来的”，不要先给分类表。

优先寻找两个情境：

- **低差异 / 无价值情境**：引入 X 后几乎没有改善；
- **高差异 / 有价值情境**：引入 X 后某个真实负担、失败模式或工作步骤明显改变。

然后沿同一条任务链比较：

`原来怎么做 → 引入 X 后怎么做 → 哪一步变化 → 谁少承担了什么 / 系统多承担了什么 → 什么情况下仍然没区别`

这样做的目的不是“证明 X 更高级”，而是找到它真正成立的边界。

如果找不到能拉开差异的真实情境，应允许结论是：

> 当前区分对这个任务没有实质价值，或者现有产品已经覆盖了大部分差异。

不要为了维护术语而制造差异。

---

## 3. Teaching Example 属于 Learning，不属于 Practice

真实场景有两种用途，必须区分：

### Teaching Example

目的是让用户听懂。

可以直接给出过程、答案和对比，例如：

> “改一句话时 X 几乎没价值；维护一个反复修改八轮的项目时，X 接走了版本和上下文协调。”

这仍然是 Learning。

### Performance Task

目的是测试用户会不会。

这时不提前给答案，而要求用户判断、设计或排错。

这才进入 Practice。

> **场景化解释 ≠ 场景化测试。**

不要因为 Practice 存在，就把 Learning 退化成抽象讲解。

---

## 4. Grounding Recovery

把用户的以下反馈视为“当前解释没有建立认知”的强信号：

- “我还是没理解”；
- “太抽象了”；
- “感觉是生造出来的”；
- “这对实际工作有什么帮助”；
- “不就是 X 吗”；
- 用户连续追问同一个概念，却仍无法指出现实差异。

出现这些信号时：

1. **停止继续上提抽象层级**；
2. 不增加新的 taxonomy、runtime、ownership、framework 等术语来解释旧术语；
3. 回到用户熟悉的对象、工作、事件或系统；
4. 选择最能拉开差异的具体情境；
5. 一步一步跑过程，直到能够回答“到底哪一步变了”；
6. 只有解释成功后，才重新命名或抽象。

Grounding Recovery 的成功判据不是“换了一个更漂亮的比喻”，而是：

> **用户现在可以把概念映射回一个具体对象，并指出它改变了什么。**

---

# 二、Build Model

Grounding 之后再形成可迁移模型。

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

## 2. 把知识放回系统、关系和状态变化中

对象已经具体后，再恢复它在系统里的位置。

对于动态知识，优先使用事件链：

`触发 → 判断 → 动作 → 状态变化 → 反馈 → 下一步`

事件链的作用是让机制可观察，不是为了展示框架。

---

## 3. 追到底层机制

流程说明“发生了什么”，机制说明“为什么这样工作”。

优先寻找真正决定行为的机制，例如：
- 表示与计算；
- 控制权；
- 状态拥有；
- 信息验真；
- 风险计量；
- 资源占用；
- 反馈；
- 失败恢复；
- 激励与约束。

如果某个机制词本身又变成新的抽象负担，必须重新落回具体行为解释。

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
- 当前对象到底怎么运行；
- 一个能解释关键差异的具体例子；
- 上位结构；
- 关键机制或事件；
- 重要边界与纠偏；
- 可迁移分析框架。

Knowledge Note 不是必须把所有层都写出来。对象还没讲清时，不允许用“可迁移框架”掩盖理解失败。

---

# 三、Find Gaps

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

注意区分两种情况：

- **用户只是还没听懂现实含义** → 继续 Learning，用 Teaching Example / Grounding Recovery；
- **用户已经理解，但需要验证自己能不能独立做** → 转 Practice。

不要把“没听懂”误判成“需要考试”。

---

# 四、Adaptive Learning Probe

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
6. 如果外部公开资料才是合适信息源，应研究或核实，而不是把检索任务甩给用户；
7. 如果当前困难只是“解释太抽象”，优先 Grounding，而不是把本应由自己解释的问题反问给用户。

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
- 当前对象已经可以被具体解释；
- Knowledge Model 已足够回答当前目标；
- 关键 Gap 已转成可验证动作；
- 下一步必须依赖新的数据/专家/实验；
- 继续语言追问的信息增益很低；

停止追问并继续 Project to Use。

---

# 五、Project to Use

把知识投影到用户下一步。

### 继续学习
进入当前最值得补的一层，而不是生成课程目录。

### 会议 / 专家交流
把 Context / Validation / Decision Gap 转成少量高信息价值问题。

### 开始实施
形成：

`第一批输入 → 第一步动作 → 初版产物 → 如何验证 → 下一轮`

### 方案 / 决策
形成：

`选择 + 支撑证据 + 权衡 + 尚未确定的信息`

### 转入 Practice

只有当用户需要验证：

> “我已经理解了，但我是不是只会解释，实际不会用？”

才把当前 Knowledge Model 和关键边界交给 Practice。

---

# 六、输出原则

Learning 默认以“让用户真正形成理解”为主，而不是展示一个完整知识体系。

优先顺序：

`具体理解 → 关键机制 → 必要抽象 → 边界 → 可迁移模型`

而不是：

`定义 → taxonomy → framework → runtime → 最后补一个例子`

如果当前信息已经足够：

> **直接教清楚。**

如果用户已经明确表示上一轮没听懂：

> **不要把同一个解释换一组更高级的术语再说一遍。**

内部可以有复杂框架，外部只输出当前理解真正需要的层级。

---

# 七、验收标准

一次高质量 Learning 结束后，至少检查：

1. 用户是否能把核心概念映射回一个具体对象、事件或任务；
2. 用户是否能说清“引入这个概念/机制前后，哪一步真的发生了变化”；
3. 对于“为什么需要 X / X 与 Y 有何区别”，是否给出了能拉开差异的情境，并同时说明 X 价值很小或不成立的边界；
4. 抽象模型是否是对已经理解事实的压缩，而不是替代解释；
5. 是否形成了必要且可迁移的 Knowledge Model，而没有为了泛化牺牲当前对象；
6. source / derived / external 边界是否正确；
7. 关键 Gap 是否真正阻塞下一步，而不是“还可以继续学什么”的清单；
8. 必要的 Probe 是否确实减少 knowledge uncertainty；
9. 当用户需要测试“会不会”时，是否正确转入 Practice。

如果知识很多、框架很完整，但用户仍然不知道：

> **“这在现实里到底改变了什么？”**

则 Learning 没有完成任务。

> **Learning 的终点不是拥有更多术语，而是对象能跑起来、机制能解释、抽象能迁移。**
