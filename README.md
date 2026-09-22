# SenseWright V2.4.0

**Agent skills for making sense of complex information.**

SenseWright is a modular agent skill system that chooses the right cognitive approach for understanding, reviewing, learning from, and questioning complex information.

SenseWright 用一个统一入口管理四种彼此独立、可以组合的认知任务：

- **D — Deep Read V6.1**：source-centered，忠实理解与压缩原材料。
- **R — Vibe Review V0.9**：judgment-centered，独立审阅材料是否成立、是否足以支持决策。
- **L — System Learning V0.4.3**：learner-centered，建立可复用知识模型并投影到下一步使用。
- **Q — Questioning V0.1**：inquiry-centered，找到高信息价值的下一问，并根据回答持续更新。

核心原则：

> **统一管理，不融合认知任务。Router 只判断“当前需要哪种认知能力”，具体复杂度与专项逻辑交给子 Skill。**

## 四种模式为什么独立

四个模式的完成标准不同：

- Deep Read 的终点是“我理解原材料了”；
- Review 的终点是“我知道哪些判断值得信到什么程度”；
- Learning 的终点是“我形成了以后还能复用的知识模型”；
- Questioning 的终点是“我知道当前最值得问什么，并通过回答减少了关键不确定性”。

Questioning 不是“生成更多问题”。它运行一个轻量闭环：

~~~text
Current Model
    ↓
Critical Uncertainty
    ↓
Probe
    ↓
Answer
    ↓
Update State
    ↓
Next Probe / Stop
~~~

内部参考 critical questioning 与访谈式 probing 的思想，但不把任何问题分类当成固定 Checklist。

## Router

根 `SKILL.md` 是唯一入口：

~~~text
User Intent
   ↓
SenseWright Router
   ├── D — Deep Read
   ├── R — Review
   ├── L — Learning
   └── Q — Questioning
~~~

Q 可以单独使用，也可以叠加在其他模式之后：

- D + Q：先读懂，再围绕材料继续追问；
- R + Q：先审阅，再把关键不确定性转成访谈问题；
- L + Q：先形成知识模型，再围绕 Knowledge Gap 连续追问。

不新增 `DQ / RQ / LQ / DRLQ` 等新的 Skill 文件，避免组合爆炸。

## Skills

~~~text
skills/
├── article-deep-read-v6.1/
│   └── SKILL.md
├── vibe-review-v0.9/
│   └── SKILL.md
├── system-learning-v0.4.3/
│   └── SKILL.md
└── questioning-v0.1/
    └── SKILL.md
~~~

## Agent Skills 标准兼容

所有 `SKILL.md` 的 YAML frontmatter 使用跨工具最小公共集：

~~~yaml
---
name: skill-name
description: What the skill does and when it should be used.
---
~~~

- `name`：稳定的 Skill 标识；
- `description`：同时描述能力与触发场景，用于 Skill discovery / triggering；
- 版本信息放在标题、目录与 `CHANGELOG.md`，不放入自定义 frontmatter 字段。

本地静态校验：

~~~bash
python scripts/validate_skills.py
~~~

## Evaluation Workflow V0.1

评测遵循：

~~~text
test cases
   ↓
with-skill  ───────┐
                   ├─> assertions + human review
baseline / old-skill┘
   ↓
grading + timing
   ↓
benchmark
   ↓
failure analysis
   ↓
next iteration
~~~

当前 Eval 已覆盖 D / R / L / Q 及部分组合路由。Q 的 V0.1 首先测试“第一问质量”：

- 是否默认只推进一个关键问题；
- 是否优先澄清真正的歧义；
- 是否避免诱导性问题；
- 是否避免在提问之前先替用户回答。

多轮适应性、停止条件和访谈长链路将在后续迭代增加。

首个长期 old-skill baseline 仍固定为：

`ffdb60e1f27ae99011d18c29c683dc747cec64f1`

详细评测约定见 `evals/README.md`。

## 使用

以根目录 `SKILL.md` 作为唯一入口。普通用户不需要单独管理四个子 Skill。
