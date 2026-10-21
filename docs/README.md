# SenseWright 文档导航

本目录分为**现行使用说明**和**历史研究档案**。请不要按照文件日期或标题中的“Core / Gate / Pipeline”推测其当前有效性。

## 现行使用说明

| 文档 | 内容 | 读者 |
| --- | --- | --- |
| [仓库中文首页](../README.md) | 项目定位、四条 Skill 总览与快速入口 | 所有人 |
| [整体架构与边界](architecture.md) | D/R/L/P 如何分工，何时组合，执行隔离与证据边界 | 使用者、集成者 |
| [使用指南](usage.md) | 不同目的的自然语言示例与结果判断 | 使用者 |
| [评测指南](../evals/README.md) | 测试集、运行方式、评分与行为验证边界 | 维护者 |
| [文档维护约定](documentation-guide.md) | 如何避免说明过时、案例侵入通用规则 | 贡献者 |
| [版本更新记录](../CHANGELOG.md) | 真实修订过程与版本沿革 | 全体贡献者 |

**现行执行规范**始终是 [根入口](../SKILL.md) 与：

- [D — Deep Read V6.4](../skills/article-deep-read-v6.4/SKILL.md)
- [R — Vibe Review V0.10](../skills/vibe-review-v0.10/SKILL.md)
- [L — System Learning V0.6.2](../skills/system-learning-v0.6.2/SKILL.md)
- [P — Practice V0.3](../skills/practice-v0.3/SKILL.md)

旧版 [Practice V0.2](../archive/skills/practice-v0.2/SKILL.md) 已移入[历史归档](../archive/README.md)，只供演变研究，不属于现行 Skill。

## 历史设计与审计记录

以下文档保留**当时的问题、推演和复盘结果**，可用于解释版本演变或构造评测用例，**不可反向解释为当前所有任务都必须执行的额外步骤**。

| 主题 | 历史材料 | 当前如何理解 |
| --- | --- | --- |
| Learning 的通用化 | [核心方法重构审计（2026-10-11）](learning-core-refactor-20261011.md) | 为什么不再把领域案例不断追加为固定认知阶段 |
| 问题与证据对齐 | [例子能否检验主问题](learning-question-evidence-alignment.md) | 说明、机制演示和真正区分关键判断的证据不能混同 |
| Learning 前置编排 | [D/R 独立前置的设计记录](learning-mandatory-dr-preflight.md) | 记录 V0.6.1 的决策；现行规则以根入口和 L 为准 |
| 问题驱动演变 | [问题链方法迁移](learning-problem-chain-migration.md) | 从 IntraMate 得来的历史启发，不是每次强制问题链 |
| 发现主问题 | [Problem Discovery](learning-problem-discovery.md) | 记录当年特定案例的纠偏，不是额外必经阶段 |
| 领域理论 | [Domain Anchor](learning-domain-anchor.md) | 需要时调取成熟理论，不硬编码某个行业知识 |
| 现实证据 | [Reality Calibration](learning-reality-calibration.md) | 需要时校准数量、状态、可比性，不必每个主题都量化 |
| Practice 错误案例 | [Agent Loop 第一轮](practice-agent-loop-drill-v0.3.md) | 只研究了下游超时重试；整体主干覆盖不足 |
| Practice 修复案例 | [Agent Loop 第二轮](practice-agent-loop-topology-repair-v0.3.md) | 发现上游工具选择等遗漏，仍不是实际模型性能测试 |

## 文件性质与使用边界

- `docs/` 下的历史文章是**研究记录**，其旧流程图、验收表、测试样例有时间语境。
- `evals/fixtures/` 的文章、业务、Agent 和金融示例是**测试素材**，不是运行时通用指令。
- `scripts/` 是脚本工具：其存在不代表 CI 已运行，也不代表模型行为通过验证。
- `SKILL.md` 是面向执行的活跃约束，说明文档只能**解释**这些约束，不能擅自添加或覆盖。

维护文档时遵照 [文档维护约定](documentation-guide.md)，优先修复错误导航与过时定位，尽量保留可审计的历史研究。