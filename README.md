# SenseWright V2.5.1

**Agent skills for making sense of complex information.**

SenseWright is a modular agent skill system for understanding, reviewing, learning from, and questioning complex information.

当前四种模式：

- **D — Deep Read V6.1**：source-facing，忠实理解；为了理解允许按认知价值压缩。
- **R — Vibe Review V0.10**：source-facing，先完整建立审阅覆盖，再独立判断；重要性只决定最终报告。
- **L — System Learning V0.4.4**：knowledge-facing，可选择性参考已有认知结果建立知识模型。
- **Q — Questioning V0.1.1**：knowledge-facing，可选择性利用已有发现和 Knowledge Gap 决定下一问。

核心协作原则仍然是：

> **D and R reason in isolation; L and Q learn from context.**

V2.5.1 不改变 V2.5.0 的非对称协作架构，只升级 Review 内部机制。

## Review V0.10：Coverage Before Materiality

旧版 Review 容易把“只输出真正重要的问题”前移成“只深入检查重要内容”。

V0.10 把顺序固定为：

~~~text
Raw Source
   ↓
Atomic Review Units
   ↓
Coverage Reconciliation
   ↓
Review Every Unit
   ↓
Adaptive Depth
   ↓
Materiality Assessment
   ↓
Selective Reporting
~~~

关键区别：

> **先完整拆解，再判断；不是先判断什么值得审，再拆解。**

### Atomic Review Unit

不是句子、段落或 bullet，而是：

> 最小的、能够被独立理解并接受审阅判断的语义单位。

Atomization 阶段不做重要性筛选。原文中每个有信息内容的 source span 都应被某个 Review Unit 覆盖，或明确归为纯结构 / 过渡 / 无新增语义的重复内容。

同时保留：
- 条件；
- 例外；
- 因果；
- 前后依赖；
- 责任转移；
- 范围限定。

原子化是为了 coverage，不是为了切碎 context。

### Review all, report what matters

所有 Unit 都进入 Review，但不同 Unit 可以使用不同分析深度。

Materiality 发生在 Review 之后，只控制最终报告：

- Material → 重点展开；
- Minor → 视用户需要简述；
- No issue → 默认不输出。

因此：

> **全面审阅 ≠ 全量输出。**

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
        ↓
   Questioning
        Q
        └──────────────► Learning
~~~

Deep Read 与 Review 仍严格隔离。Review V0.10 的覆盖机制不会读取 D / L / Q 的结果。

## Skills

~~~text
skills/
├── article-deep-read-v6.1/
│   └── SKILL.md
├── vibe-review-v0.10/
│   └── SKILL.md
├── system-learning-v0.4.4/
│   └── SKILL.md
└── questioning-v0.1.1/
    └── SKILL.md
~~~

## Evaluation Workflow V0.1

除原有任务质量、source isolation 和 selective reference 外，新增 Review coverage regression：

- 人工标注 Gold Atomic Review Units；
- 检查分散在不同位置的问题是否被遗漏；
- 检查条件 / 例外 / 前后依赖是否在 atomization 后仍被保留；
- 检查“全覆盖”有没有导致最终输出退化成逐条问题清单。

当前增加 `review_v0_9` baseline，指向升级前的 V2.5.0 commit，可直接用于 V0.9 vs V0.10 比较。

示例：

~~~bash
python scripts/init_eval_workspace.py --iteration 1 --baseline review_v0_9
~~~

当前 Eval 仍是 runner-neutral 的实验协议，不自动执行模型调用。

## Agent Skills 标准兼容

所有 `SKILL.md` frontmatter 使用 `name + description` 最小公共集。

本地校验：

~~~bash
python scripts/validate_skills.py
python scripts/validate_evals.py
~~~

## 使用

以根目录 `SKILL.md` 作为唯一入口。
