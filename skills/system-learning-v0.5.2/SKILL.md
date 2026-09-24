---
name: system-learning
description: Turn a concept, system, person, event, method, question, or source material into grounded understanding first and a reusable knowledge model second; for mechanism-heavy technical knowledge, make the mechanism executable enough to trace and predict, identify the few gaps that block real understanding or use, and adaptively probe for missing user- or expert-specific information when needed.
---

# System Learning V0.5.2 — Ground → Run → Explain → Vary → Model → Use

## Suite 集成边界

本 Skill 在 SenseWright 中承担 **L — Learning**。

目标是：

> **先让当前对象真正变得可理解；对机制型知识，再让它“跑起来”，直到用户不仅知道它是什么，还能解释它为什么这样工作、条件变化后会发生什么；最后再压缩成可复用知识模型。**

- “原文讲了什么” → Deep Read。
- “材料哪里有问题” → Review。
- “我应该怎样理解、为什么会这样、它在现实中到底改变了什么 / 怎么运行” → Learning。
- “不要再讲，用场景测试我是不是真的会” → Practice。

Questioning 不再作为独立 Skill。用于减少 knowledge uncertainty 的追问继续留在 Learning。

---

## Optional Reference Context

Learning 的主要依据仍是 Raw Source / 用户事实 / 当前任务。

可以选择性参考：

- **Deep Read**：作者结构、关键概念、机制、案例、比喻和认知桥梁等 source reconstruction；
- **Review**：关键分歧、证据薄弱处、风险、替代解释等 judgment；
- **Practice**：暴露出的误解、Application Gap、Boundary Gap、Trade-off Gap 等 performance findings。

三个规则：

1. **Reference ≠ Evidence**：涉及“原文到底说了什么”仍回 Raw Source；涉及外部事实仍需要相应证据。
2. **Transform, don't copy**：Reference 应改变 Learning 的模型、注意力或 Gap，而不是被原样复制。
3. **Selective, not mandatory**：只有 reference 能明显改善当前学习任务时才使用。

当 Deep Read 提供了作者有价值的故事、比喻或例子时，Learning 可以把它们当作认知脚手架，但最终需要回到真实对象和机制；**比喻帮助进入机制，不替代机制本身。**

---

## 目标

Learning 的通用主体仍然是：

`Ground Object → Build Model → Find Gaps → Project to Use`

对于 **mechanism-heavy technical knowledge**，Build Model 内部优先启用：

`Ground → Run Once → Explain Mechanism → Vary One Condition → Compress Model`

必要时在 Find Gaps 内部使用：

`Gap → Probe / Research → Update Model`

这不是要求所有主题都套技术模板。只有当“知道定义”仍不足以形成理解，且对象本身存在可追踪的计算、状态、控制流、数据流、资源变化或反馈机制时，才提高 Mechanism Depth。

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

如果找不到能拉开差异的真实情境，应允许结论是：

> 当前区分对这个任务没有实质价值，或者现有产品已经覆盖了大部分差异。

不要为了维护术语而制造差异。

---

## 3. Teaching Example 属于 Learning，不属于 Practice

### Teaching Example
目的是让用户听懂。可以直接给过程、答案、变量变化和对比。

### Performance Task
目的是测试用户会不会。这时不提前给答案，而要求用户判断、设计或排错；这才进入 Practice。

> **场景化解释 ≠ 场景化测试。**

Learning 可以主动展示完整机制；Practice 才要求用户自己完成。

---

## 4. Grounding Recovery

把“我还是没理解 / 太抽象 / 像生造的 / 实际有什么用 / 不就是 X 吗”等反馈视为当前解释没有建立认知的强信号。

出现这些信号时：

1. 停止继续上提抽象层级；
2. 不增加新的 taxonomy / runtime / framework 来解释旧术语；
3. 回到用户熟悉的对象、工作、事件或系统；
4. 选择最能拉开差异的具体情境；
5. 一步一步跑过程，直到能够回答“到底哪一步变了”；
6. 只有解释成功后，才重新命名或抽象。

成功判据：

> **用户可以把概念映射回一个具体对象，并指出它改变了什么。**

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

## 2. 对机制型技术知识：能运行，就不要只描述

如果对象涉及算法、系统、Agent、RAG、数据库、网络、运行时、缓存、调度、状态管理等机制，优先选一个最小具体实例，让它真实“跑一遍”。

根据知识本身选择需要追踪的维度，例如：

- 输入；
- 中间表示；
- 状态；
- 控制流；
- 数据流；
- 资源占用；
- 动作；
- 输出；
- 反馈。

不是每项都必须有。只追踪真正决定当前机制的部分。

目标是从：

> “它由 A / B / C 三个组件组成”

推进到：

> “一个真实输入进入后，A 做了什么，改变了什么；为什么接下来必须到 B；最终输出为何会这样。”

### 最小运行单元

优先选择能把机制看清的最小案例，而不是一上来解释完整生产系统。

例如：

- Agent State：一次动作完成后 State 怎样变化，重启后怎样影响下一步；
- Rerank：几个召回 chunk 如何重新打分并改变排序；
- Attention：一个 token 如何形成 query，并从其他 token 聚合信息；
- Transaction：两步写入中途失败时，无事务与有事务分别留下什么状态；
- KV Cache：一个新 token 解码时哪些历史计算被复用。

如果一个技术概念无法通过“跑一次”直接理解，可以改用结构变化、资源流、因果链或最小实验，不强行模拟。

---

## 3. 解释为什么每一步存在

跑完一次之后，不停在“流程记忆”。

逐步追问：

> 为什么必须做这一步？它解决了上一步留下的什么问题？如果跳过它会怎样？

优先寻找真正决定行为的机制，例如：

- 表示与计算；
- 信息交互；
- 控制权；
- 状态拥有；
- 信息验真；
- 风险计量；
- 资源占用；
- 反馈；
- 失败恢复；
- 激励与约束。

流程告诉用户发生了什么；机制解释为什么结果会如此。

如果某个机制词本身又变成新的抽象负担，重新落回具体行为。

---

## 4. 改变一个关键条件，看模型还能否解释

对于已经跑通的机制，选择一个真正会影响行为的变量做 **Teaching Variation**。

一次优先改变一个主要条件，例如：

- 输入规模增大；
- 某个组件移除；
- 状态丢失；
- 缓存关闭；
- 候选集合扩大；
- 上下文变长；
- 资源预算降低；
- 一个前提失效；
- 换一种实现方式。

然后直接展示：

`条件变化 → 哪一步首先受影响 → 状态/成本/结果怎样变化 → 为什么`

这仍然属于 Learning，因为答案可以直接给出。

Practice 与它的区别在于：Practice 会把变化条件交给用户自己判断，不提前解释。

---

## 5. Prediction as Understanding Check

对 mechanism-heavy knowledge，内部增加一个理解检查：

> **当前模型是否足以预测至少一个相邻条件变化后的结果？**

如果用户只能复述定义和标准流程，却无法从机制推出“条件变化后为什么不同”，说明可能只有描述性知识，还没有形成机制模型。

这个检查主要用于决定 Learning 是否需要继续解释；默认不把它变成考试。

如果需要让用户独立预测，转 Practice。

---

## 6. 比喻是脚手架，不是建筑本身

当 Raw Source 或 Deep Read 中存在高价值比喻时：

1. 保留它帮助理解的那一层对应关系；
2. 明确比喻映射到真实系统中的哪些对象或关系；
3. 一旦真实机制已经能理解，逐渐减少对比喻的依赖；
4. 检查比喻在哪些地方会失真，避免把类比当机制。

> **Deep Read 负责忠实保留作者的认知桥梁；Learning 负责利用桥梁走到真实机制。**

---

## 7. 不服从原材料结构

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

## 8. 最终形成自己的分析框架

Knowledge Model 应该帮助用户以后处理相邻问题，而不是只回答这一次。

完整学习单元尽量留下 Knowledge Note：
- 核心判断；
- 当前对象到底怎么运行；
- 一个能解释关键差异的具体例子；
- 对机制型知识：一次最小运行、关键状态/变量和至少一个条件变化；
- 上位结构；
- 重要边界与纠偏；
- 可迁移分析框架。

Knowledge Note 不是固定模板。对象已经简单清楚时，不为了完整把所有项目都打印出来。

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

注意区分：
- **还没听懂现实含义** → Grounding；
- **知道有什么用，但看不懂怎么工作** → Mechanism Depth；
- **已经理解，需要验证自己能不能独立做** → Practice。

---

# 四、Adaptive Learning Probe

只有当 Gap 阻塞当前模型，而且最合适的信息源是用户、专家或后续交流时，才提问。

目的：

> **减少 knowledge uncertainty，而不是测试用户。**

可按需使用 Clarify / Reason / Evidence / Assumption / Alternative / Mechanism / Boundary / Missing / Action 等 Lens。

规则：

1. 默认一次只推进一个最有信息价值的问题；
2. 下一问根据新回答重新选择，不预设整棵问题树；
3. 先澄清事实和概念，再挑战原因；
4. 问用户只能知道的信息，不把本可以自己解释的问题全部反问给用户；
5. 不把自己的答案藏进诱导性问题；
6. 如果外部公开资料才是合适信息源，应研究或核实，而不是把检索任务甩给用户；
7. 如果困难只是解释太抽象，优先 Grounding；
8. 如果困难是机制看不见，优先 Run Once / Teaching Variation，而不是继续定义术语。

每次 Probe 后可区分 Confirmed / Assumed / Unknown / Contradiction / Next Gap，并更新 Knowledge Model。

---

# 五、Project to Use

把知识投影到用户下一步。

### 继续学习
进入当前最值得补的一层，而不是生成课程目录。

### 最小实验
对于技术知识，如果语言解释已经不足，形成：

`最小输入 → 可观察变量 → 执行动作 → 预期变化 → 如何判断模型是否正确`

实验服务于理解，不为了练技术强行搭系统。

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

普通主题优先：

`具体理解 → 关键机制 → 必要抽象 → 边界 → 可迁移模型`

机制型技术主题可以自然展开为：

`为什么需要 → 跑一次 → 为什么这样跑 → 改一个条件 → 最后抽象`

但这只是认知顺序，不是固定标题模板。

避免：

`定义 → 组件清单 → taxonomy → framework → 公式 → 最后补一个例子`

如果当前信息已经足够：

> **直接教清楚。**

如果用户已经明确表示上一轮没听懂：

> **不要把同一个解释换一组更高级的术语再说一遍。**

如果用户已经看懂“为什么需要”，但仍看不懂“怎么工作”：

> **不要重复 Grounding；让机制真正运行一次。**

---

# 七、验收标准

一次高质量 Learning 结束后，至少检查：

1. 用户是否能把核心概念映射回一个具体对象、事件或任务；
2. 用户是否能说清“引入这个概念/机制前后，哪一步真的发生了变化”；
3. 对于“为什么需要 X / X 与 Y 有何区别”，是否给出了能拉开差异的情境并说明边界；
4. 对机制型技术知识，是否至少有一个具体实例真正运行起来，而不是停在组件说明；
5. 用户是否能看见关键输入、状态/表示/资源变化、动作和输出之间的因果连接；
6. 是否解释了关键步骤为什么存在，而不是只复述标准流程；
7. 当前机制模型是否足以解释至少一个相邻条件变化后的结果；
8. 比喻若被使用，是否最终映射回真实机制，并说明其失真边界；
9. 抽象模型是否是对已经理解事实的压缩，而不是替代解释；
10. source / derived / external 边界是否正确；
11. 关键 Gap 是否真正阻塞下一步；
12. 当用户需要测试“会不会”时，是否正确转入 Practice。

如果知识很多、术语正确，但用户仍然不知道：

> **“一个真实输入进去以后，到底发生了什么；为什么；条件变了又会怎样？”**

则 mechanism-heavy Learning 没有完成任务。

> **Learning 的终点不是记住说明，而是形成一个能运行、能解释、能预测的 mental model。**
