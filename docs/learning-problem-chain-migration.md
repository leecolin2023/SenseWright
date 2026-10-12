# Learning V0.6.0：IntraMate 问题链方法迁移记录

> **历史设计记录（非现行固定流程）**：本文保留 V0.6.0 当时如何吸收问题驱动学习方法，以及后来 V0.6.1 的编排修订。当前 Learning 已重构为自适应认知责任，不再强制完整问题链或固定三道 Gate；详见 [活跃 Learning Skill](../skills/system-learning-v0.6.2/SKILL.md) 与 [核心方法重构审计](learning-core-refactor-20261011.md)。文中对 Practice 的旧工程定位也不是当前默认规范。

来源：[IntraMate 学习方法](https://github.com/leecolin2023/IntraMate/blob/main/Architecture/method/00-learning-method.md)。当时的案例：[Agent Runtime](https://github.com/leecolin2023/IntraMate/blob/main/Architecture/learning/01-agent-runtime/D-deep-read.md)、[Work Agent](https://github.com/leecolin2023/IntraMate/blob/main/Architecture/learning/02-work-agent/D-deep-read.md)。

## 一、为什么把问题链迁移到 Learning，而不是改造 Deep Read？

当时 IntraMate 的部分文档虽然叫 Deep Read，实际关键动作是：从当前解释中的失败出发，一步步寻找解决失败所必需的新概念。

这属于**学习者中心的知识建构**。SenseWright 的 D 则必须**原材料中心**：恢复作者真实的认知推进与结构，而不能强迫所有原文按外部预设的问题链重写。因此此方法主要被吸收进 L，而不是替代 D 的源材料忠实性。

## 二、当时吸收了什么？

| IntraMate 的线索 | V0.6.0 在 Learning 中的对应做法 |
| --- | --- |
| Problem First | 从有现实依据、可观察的困难出发 |
| Mechanism Before Framework | 先推出必要行为，再给概念和框架命名 |
| 旧机制失效 → 新机制出现 | 让问题链解释机制如何一步步产生 |
| Knowledge Stable ≠ Implementation Ready | 区分理解完成与工程可执行 |
| Problem Knowledge / Native Framework Evidence | 分离问题知识、实现证据和架构决策 |
| Problem-chain Review | 用内置检查避免因果推进缺失 |
| Concept First-Appearance Audit | 确认概念首次出现时有足够解释 |
| Boundary Review | 检查证据、适用范围和越界主张 |
| 三框架比较与 Agent 分类 | 只在具体研究对象需要时使用，不跨领域硬套 |

## 三、当时的典型示例

```text
模型说“我要查询记录” → 实际还没有操作发生
→ 需要受控执行工具调用
→ 工具执行完成，模型却不知道结果
→ 需要将工具结果回写到下一次观察
→ Agent 才能继续判断、行动与观察
```

原设计希望在这段因果链清楚后再引入 Execution、Observation、AgentLoop 等术语，并要求具体产品实现仍另行以源码或实验核验。

但后续 Practice 发现：**这条链仍省略了“模型为何决定使用工具、为何选择某个工具”这些上游关键机制。** 这也是为什么历史问题链不能被视为无缺口的最终解释。

## 四、当时试图防止的错误

- 直接从 Runtime / Framework / API 分类开始讲，却没有真实问题；
- 为了延长问题链而创造并不存在的困难；
- 要求非技术主题也必须运行程序 Probe；
- 混淆 **未知（UNKNOWN）不等于不存在（ABSENT）**，以及 **框架没有不等于必须自建（BUILD）**；
- 未执行实验却声称有运行证据；
- 把某个必要行为差异直接推导成必须新建一个软件模块。

其中“纯面试问题不进入 Practice”的旧判断**已经失效**。当前 Practice 可以围绕已学知识进行有深度的问题发现和追问，但不等于机械出题。

## 五、当时的写作稳定化设计

```text
草稿 → 问题链检查 → 修复
     → 概念首次出现检查 → 修复
     → 边界与证据检查 → 修复
     → 复核 → 稳定或明确阻断性未知
```

这些原本意在要求作者在交付前完成实质修正，而不是把 Gate 留给下一轮用户触发。后来 [Learning 通用核心重构](learning-core-refactor-20261011.md) 指出：如果不断把特定案例的修复方式加为通用必经阶段，反而会增加刚性与过拟合。因此 **V0.6.2 当前只保留自适应的认知责任与必要的内部质量判断**，不必逐项输出上述旧流程。

## 六、历史回归与后续演进

- 旧 V0.5.3 的冻结基线在 `evals/baselines.json` 中保留；当时 #22–27 用于验证因果链、证据分离、概念首次出现、非技术迁移和不过度工程化。
- 静态测试能验证 Skill 打包和评测 JSON 的部分结构，**不能证明模型行为提升**。
- 在 V0.6.1 中新增本轮 D/R 独立前置：D、R 各自读取相同 Raw Input，L 在二者完成后读取其结果。详细的历史决策见 [D/R 前置记录](learning-mandatory-dr-preflight.md)。
- 当前问题链只是有用的解释方式之一；是否需要延长、改变或终止问题链，应由用户真实问题与证据决定。

这篇记录的价值是保留方法迁移的**缘起、当时的机制和后来已知的局限**，而不是要求新版本逐行复现旧流程。