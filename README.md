# SenseWright V2.6.0

**Agent skills for making sense of complex information — and proving you can use what you learned.**

SenseWright 现在收敛为四种一级认知模式：

- **D — Deep Read V6.1**：理解材料。
- **R — Vibe Review V0.10**：审阅材料。
- **L — System Learning V0.5.0**：形成知识模型。
- **P — Practice V0.1**：检验知识迁移。

核心边界可以压缩成四个问题：

~~~text
D — 我理解材料了吗？
R — 这份材料可靠吗、够用吗？
L — 我真正懂了吗？
P — 我真正会了吗？
~~~

## 为什么删除 Questioning 一级路由

V2.4 曾把 Questioning 建模为独立 Skill。实际迭代后发现，“提问”更像一种跨任务控制策略，而不是稳定的最终用户目标。

同一句“问我一个问题”，可能有两种完全不同的目的：

~~~text
为了获得缺失知识
→ Learning Probe

为了暴露学习者能力
→ Practice Probe
~~~

因此 V2.6.0 将 `questioning-v0.1.1` 从 active tree 移除，并把它最有价值的机制拆入 L / P：

### Learning 吸收
- Clarify / Reason / Evidence / Assumption；
- Alternative / Mechanism / Boundary / Missing；
- 一次一个高信息价值问题；
- 根据回答更新 Confirmed / Assumed / Unknown / Contradiction / Next Gap；
- 访谈 / 专家交流作为 Project to Use。

### Practice 吸收
- 一次一个主要任务；
- 下一问随用户表现变化；
- 追真实情境；
- 不使用诱导性问题泄漏答案；
- What-if / Why-not-alternative 压力测试；
- 停止条件与动态难度。

Questioning 的历史没有删除，仍保留在 Git 历史和 CHANGELOG。

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
        │ Knowledge Model
        ▼
     Practice
        P
        │
        │ Performance Gap
        └──────────────► Learning
~~~

### Source-facing

D / R 继续严格隔离：
- 都直接读取 Raw Source；
- 不读取 sibling outputs；
- D 与 R 互不消费结果。

### Knowledge-facing

L / P 可以选择性参考已有结果：

- Learning 可参考 D / R，以及 Practice 暴露出的 Gap；
- Practice 可参考 D / R / L，其中 Learning Knowledge Model 通常是主要输入。

统一规则：

> **Reference ≠ Evidence. Transform, don't copy. Selective, not mandatory.**

## Learning V0.5.0

主体仍然是：

~~~text
Build Model
→ Find Gaps
→ Project to Use
~~~

但在真正阻塞模型时允许：

~~~text
Gap
→ Adaptive Probe / Research
→ Update Model
~~~

Learning Probe 的目标是减少 **knowledge uncertainty**。

如果问题变成“你到底会不会”，转入 Practice。

## Practice V0.1

核心循环：

~~~text
Diagnose
→ Situate
→ Perform
→ Stress
→ Debrief
~~~

Practice 不把工作和面试当作目标本身。

它们只是两种常用情境：

- 工作场景：测试能否真实决策、操作、排错；
- 面试场景：用连续追问检验模型是否稳定、能否解释 trade-off 和反例。

Practice Probe 的目标是减少对用户 **capability uncertainty**。

## Skills

~~~text
skills/
├── article-deep-read-v6.1/
│   └── SKILL.md
├── vibe-review-v0.10/
│   └── SKILL.md
├── system-learning-v0.5.0/
│   └── SKILL.md
└── practice-v0.1/
    └── SKILL.md
~~~

## Evaluation Workflow V0.1

Eval 路由同步收敛为：

`D / R / L / P`

原 Q case 已重新归属：
- “把问题问清楚 / 专家访谈求证” → Learning；
- “用场景或面试追问检验是否会用” → Practice。

新增 Practice transfer cases，重点验证：
- 是否把 Knowledge Model 转成真实判断任务；
- 是否避免重新讲答案；
- 是否一次只推进一个主要任务；
- 是否根据上一轮表现改变 stress condition；
- 是否能把表现失败回流成明确 Knowledge Gap。

V2.5.1 commit `9bbc0360616b60c4d960e412979b841853a10369` 固定为本次架构收敛前 baseline。

本地校验：

~~~bash
python scripts/validate_skills.py
python scripts/validate_evals.py
~~~

## 使用

以根目录 `SKILL.md` 作为唯一入口。
