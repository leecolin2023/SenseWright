# SenseWright V2.5.0

**Agent skills for making sense of complex information.**

SenseWright is a modular agent skill system for understanding, reviewing, learning from, and questioning complex information.

V2.5.0 引入 **Asymmetric Collaboration / 非对称协作**：

- **D — Deep Read V6.1**：source-facing，严格从原始材料忠实理解。
- **R — Vibe Review V0.9**：source-facing，严格从原始材料独立审阅。
- **L — System Learning V0.4.4**：knowledge-facing，可选择性参考已有认知结果来构建用户自己的知识模型。
- **Q — Questioning V0.1.1**：knowledge-facing，可选择性利用已有发现和 Knowledge Gap 来决定下一问。

核心原则：

> **D and R reason in isolation; L and Q learn from context.**

## Architecture

~~~text
Raw Source / User Context
        │
   ┌────┴────┐
   ▼         ▼
Deep Read   Review
   D         R
[isolated] [isolated]
   │         │
   └────┬────┘
        │ optional references
        ▼
     Learning
        L
        │
        │ knowledge model / gaps
        ▼
   Questioning
        Q
        │
        │ newly confirmed answers
        └──────────────► Learning
~~~

### Source-facing Skills

Deep Read 和 Review 保持严格隔离：

- 都直接读取 Raw Source；
- D 不读取 R/L/Q 的结果；
- R 不读取 D/L/Q 的结果；
- 即使 D 已经做完，R 也不能基于 D 的摘要审阅。

这样避免把“另一个 Skill 对 Source 的表示”误当成 Source 本身。

### Knowledge-facing Skills

Learning 和 Questioning 可以选择性吸收已有结果。

Learning 可参考：
- D 的 source reconstruction；
- R 的 material differences / uncertainty / risks；
- Q 中用户新确认的事实和未解决 Gap。

Questioning 可参考：
- D 暴露出的关键结构或概念；
- R 暴露出的关键不确定性；
- L 形成的 Knowledge Gap。

但所有 sibling output 都属于 **Reference Context**：

> **Reference ≠ Evidence. Transform, don't copy. Selective, not mandatory.**

## Router

根 `SKILL.md` 是唯一入口。Router 只做两层轻量决策：

1. **Route Selection**：当前任务需要 D / R / L / Q 哪些能力；
2. **Reference Selection**：仅当目标包含 L / Q 时，从已经存在的 sibling results 中选择真正有帮助的参考。

当前项目不引入 Shared Blackboard、Artifact Registry 或额外协作 runtime。V2.5.0 先把 Context Policy 固定在 Skill 契约和 Eval 中。

## L ↔ Q：唯一允许形成反馈环的区域

~~~text
Learning
   ↓
Knowledge Gap
   ↓
Questioning
   ↓
New Answer / New Evidence
   ↓
Learning
   ↓
Updated Knowledge Model
~~~

Q 回流给 L 的重点应是：
- 用户或专家新确认的信息；
- 新证据；
- 仍未解决的 Gap。

不是把 Questioning 的整段内部推理原样回灌。

## Skills

~~~text
skills/
├── article-deep-read-v6.1/
│   └── SKILL.md
├── vibe-review-v0.9/
│   └── SKILL.md
├── system-learning-v0.4.4/
│   └── SKILL.md
└── questioning-v0.1.1/
    └── SKILL.md
~~~

## Evaluation Workflow V0.1

Eval 继续验证原有任务质量，并增加两类架构回归：

- **Source isolation**：D / R 不消费 sibling results；
- **Selective reference**：L / Q 可以利用有价值的 prior finding，但不能复制或把 sibling judgment 当成原材料事实。

`evals.json` 允许为 L / Q case 提供可选的 `reference_context`。D / R case 不允许配置该字段，静态校验会直接失败。

当前 Eval 仍是 runner-neutral 的实验协议，不自动执行模型调用。

## Agent Skills 标准兼容

所有 `SKILL.md` frontmatter 使用跨工具最小公共集：

~~~yaml
---
name: skill-name
description: What the skill does and when it should be used.
---
~~~

本地校验：

~~~bash
python scripts/validate_skills.py
python scripts/validate_evals.py
~~~

## 使用

以根目录 `SKILL.md` 作为唯一入口。普通用户无需单独管理四个子 Skill。
