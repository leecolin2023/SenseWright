---
name: practice
description: Turn an understood concept or knowledge model into executable engineering know-how by placing it in a realistic scenario and walking through the complete implementation path: system position, components, interfaces, data, state, configuration, execution, verification, failure handling, and operational constraints. Use when the user understands what something is but still needs to know exactly how it is built, run, tested, debugged, and transferred into a real project.
---

# Practice V0.2 — Knowledge to Execution

## 定位

Practice 不再以“测试用户会不会”为中心。

它负责弥补：

> **“我知道它是什么”**

到：

> **“如果现在让我真正做，我知道从哪里开始、一步一步怎么做、怎么证明做对了。”**

之间的鸿沟。

中心问题：

> **如果现在真的要把它做出来，我该怎么做？**

核心转化：

> **Knowledge Model → Executable Engineering Model**

最终产物不是题库、面试追问或再次解释概念，
而是一条可以沿着真实场景执行的工程实践路径。

---

## 1. Context Contract

Practice 可以使用：

- 用户当前要实践的概念、技术或方法；
- Learning 已形成的 Knowledge Model；
- 用户真实项目、代码、系统、数据和约束；
- 必要时 Deep Read 中的原始机制或案例；
- 必要时 Review 暴露出的风险、薄弱条件或待验证点。

Learning 通常是最重要的上游输入。

统一遵守：

- **Reference ≠ Evidence**
- **Transform, don't copy**
- **Selective, not mandatory**

Practice 可以为了完成工程落地补充实现知识，但应区分：

- 来源中已经建立的原理；
- 当前场景中的工程推导；
- 为完成实现而增加的工程选择。

如果关键工程约束未知但不阻塞演示，优先给出合理假设并明确说明；
只有当缺失信息会实质改变实现路径时，才提出最少量澄清问题。

> **不要把 Practice 重新变成连续提问。**

---

## 2. Ground a Real Scenario

不要继续从抽象概念向下解释。

先建立一个：

> **这个概念真正有必要存在的工程场景。**

优先级：

1. 用户真实项目；
2. 用户目标岗位中的真实工程任务；
3. 相邻领域的代表性工程问题；
4. 如果都没有，再构造足够真实的场景。

场景应尽量明确：

- 目标；
- 输入；
- 输出；
- 系统边界；
- 关键依赖；
- 数据；
- 约束；
- 成功条件。

不要使用只为了说明定义而存在的玩具示例。

> **Scenario 应该逼出机制，而不是装饰机制。**

---

## 3. Build the Engineering Model

在写代码或操作步骤前，先回答：

> **这个概念在整个系统里到底处于什么位置？**

明确：

- 谁调用它；
- 它依赖什么；
- 输入是什么；
- 输出是什么；
- 状态在哪里；
- 与哪些组件交互；
- 哪些责任属于它；
- 哪些责任不属于它。

必要时建立：

`Component → Interface → Data → State → Dependency`

关系。

目标是避免：

> 概念已经理解，
> 但不知道它应该放进真实系统的哪一层。

---

## 4. Walk the Implementation End to End

真正开始工程实施。

不要停在：

- “需要建立数据库”；
- “需要做向量检索”；
- “需要增加状态管理”；
- “需要配置监控”。

继续回答：

> **具体怎么做？**

根据场景，展开到实际执行所需的粒度，例如：

- 项目 / 模块怎样组织；
- 需要哪些组件；
- 数据结构与 Schema 是什么；
- API / 接口如何连接；
- 配置放在哪里；
- 状态怎样流转；
- 哪一步先做、哪一步后做；
- 最小可运行版本是什么；
- 每一步会留下什么工程产物。

代码、配置、命令、SQL、目录结构、API、Prompt、测试数据或伪代码是否需要出现，
由当前实践路径决定，不作为固定模板。

> **不要为了“工程感”堆技术细节；但任何阻碍实际执行的关键空白，都不能用概念性语言跳过。**

---

## 5. Run One Concrete Path

仅描述架构不算完成 Practice。

至少选择一个具体输入，让它真实沿系统走一遍：

`Input → Processing → State Change → Intermediate Artifact → Output`

明确展示：

- 每一步收到什么；
- 做了什么；
- 产生什么；
- 下一步为什么能够继续。

对于 Agent、RAG、工作流、数据库、消息系统等机制型对象，
应尽量展示一次真实的数据、状态、控制流或资源变化。

> **概念必须在一个具体实例里跑起来。**

---

## 6. Verify the Result

必须回答：

> **我怎么知道刚才真的做对了？**

根据场景建立真实 Feedback Loop，例如：

- 单元测试；
- 集成测试；
- 输入输出断言；
- 数据校验；
- 日志 / Trace；
- 指标；
- 人工验收；
- Golden Dataset；
- 回归测试。

不要只展示 Happy Path，却不给判断正确性的办法。

> **没有 Feedback Loop 的工程实践是不完整的。**

---

## 7. Walk Through Failure and Troubleshooting

真实工程一定会失败。

选择对当前概念最有信息价值的失败点，说明：

> **它会怎么坏？**
>
> **你会看到什么现象？**
>
> **先检查哪里？**
>
> **怎样定位到真正原因？**
>
> **应该怎样修？**

重点建立工程直觉，不穷举所有异常。

原 Practice 的 Stress 思想仅保留为这里的条件变化与失败分析：

> **不是为了考试用户，而是为了暴露工程模型的真实边界。**

---

## 8. Operationalize

如果当前场景会持续运行，补齐真正影响落地的工程约束，例如：

- 配置管理；
- 权限与安全；
- 数据 / Schema / Prompt 版本；
- 并发；
- 性能；
- 成本；
- 可观测性；
- 重试；
- 幂等；
- 回滚；
- 部署；
- 增量更新；
- 版本升级。

不是每次都展开全部项目。

判断标准：

> **如果忽略它，这个案例还能不能在目标环境中可靠工作？**

如果不能，就必须处理。

---

## 9. Make the Engineering Artifacts Explicit

完成 Walkthrough 后，明确当前 Case 真正需要产生什么工程产物。

根据场景列出实际需要的内容，例如：

- 模块 / 文件；
- 数据结构 / Schema；
- 配置；
- API；
- 测试 fixture；
- Golden Eval Set；
- 运行命令；
- 监控指标；
- 验收结果；
- 文档或决策记录。

不要强制所有 Case 使用同一份清单。

目标是让用户知道：

> **明天真正打开 IDE、终端或系统以后，要创建和交付哪些东西。**

---

## 10. Generalize the Practice

当前 Case 跑通后，区分：

> **哪些做法来自概念本身？**

和：

> **哪些只是这个项目的实现选择？**

再说明：

- 换一个工程场景时什么保持不变；
- 哪些参数、组件或结构需要重新设计；
- 哪些边界决定方案是否还能复用。

Practice 不是让用户背住当前 Case。

最终应形成：

> **一个已经在真实场景中跑通的、可迁移的实施模型。**

---

## 11. Deliverable Contract

一个合格的 Practice 输出，应让一个已经理解概念、
但没有真正实施过的人：

> **能够沿着当前案例开始实际动手。**

他应该知道：

- 为什么在这里需要这个概念；
- 它放在系统什么位置；
- 要创建哪些工程对象；
- 按什么顺序完成；
- 每一步输入输出是什么；
- 一条真实数据怎样跑完整链路；
- 怎样验证做对；
- 出问题时从哪里查；
- 哪些工程约束不能忽略；
- 最终需要留下哪些工程产物。

Practice 不要求每次都提供生产级完整代码。

但不能留下这样的空白：

> **“原理我懂了，可真正打开 IDE / 系统以后，我还是不知道第一步干什么。”**

如果仍然存在这个空白，Practice 就没有完成任务。

---

## 12. Acceptance Gate

交付前检查：

### Scenario Reality
这个 Case 是否足够真实，还是只给定义套了一个故事？

### System Placement
用户是否知道这个概念在整个工程中的位置和责任边界？

### End-to-End Completeness
从目标到最终验证之间，是否还有需要用户自己脑补的关键步骤？

### Implementation Specificity
是否已经具体到组件、数据、接口、状态、配置或工程产物，而不是停留在“建设 / 优化 / 接入 / 实现”？

### Execution Trace
是否真的让至少一个具体实例跑完完整路径？

### Verification
是否说明怎么判断它做对了？

### Failure Readiness
是否覆盖最有信息价值的失败现象与排查方法？

### Artifact Readiness
用户是否知道真正实施时要创建、运行和验收哪些工程产物？

### Concept Traceability
工程设计是否来自当前 Knowledge Model 和真实约束，而不是无目的堆“最佳实践”？

### Scope Control
是否为了显得专业加入了与当前目标无关的复杂度？

---

## 13. Repair Loop

如果仍然太抽象：

> 回到 Implementation Walkthrough，补工程对象、步骤、接口、数据和产物。

如果步骤看似完整但无法实际执行：

> 找出隐藏跳步并展开。

如果只有代码没有工程理解：

> 回到 Engineering Model，补设计依据和组件职责。

如果只有 Happy Path：

> 补 Verification 与 Troubleshooting。

如果用户仍不知道真正要创建什么：

> 补 Engineering Artifacts。

如果复杂度明显超过当前场景：

> 删除非必要组件，恢复最小完整实现。

如果场景没有真正使用当前概念：

> 更换场景，而不是继续补解释。

如果实践过程中暴露的是根本知识缺口：

> 回流 Learning，修正 Knowledge Model 后再继续 Practice。

修复后重新执行 Acceptance Gate。

---

## 最终原则

> **Practice 不是证明“我会不会”，而是把已经理解的知识编译成一条真正能够执行、验证、排错和迁移的工程路径。**
