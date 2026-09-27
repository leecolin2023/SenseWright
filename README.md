# SenseWright V2.7.0

**Agent skills for making sense of complex information — and turning understanding into executable engineering practice.**

SenseWright 现在收敛为四种一级认知模式：

- **D — Deep Read V6.4**：先恢复认知结构，再按交付目标选择完整覆盖或认知提炼。
- **R — Vibe Review V0.10**：审阅材料。
- **L — System Learning V0.5.3**：先落地理解；必要时改变一个高信息量条件暴露边界；技术机制再跑起来，最后形成知识模型。
- **P — Practice V0.2**：把已理解的知识编译成可执行、可验证、可排错的真实工程路径。

核心边界可以压缩成四个问题：

~~~text
D — 我理解材料了吗？
R — 这份材料可靠吗、够用吗？
L — 我真正懂了吗？
P — 如果现在真的要把它做出来，我该怎么做？
~~~

## 为什么 Questioning 不再是一级路由

Questioning 仍然不是稳定的最终用户目标。

Learning 可以在真正的知识缺口阻塞理解时使用 **Learning Probe**；但 Practice V0.2 不再继承原 Questioning 的“能力测验 / 自适应追问”定位。

Practice 的目标已经从：

`Knowledge Assessment`

调整为：

`Knowledge Model → Executable Engineering Model`

因此“出题考我、模拟面试、连续压力追问”不再是进入 P 的充分条件。P 只有在用户需要把已理解知识落进真实工程、走通实施与验证路径时触发。

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
        │ Implementation Gap
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

## Deep Read V6.4

Deep Read 从 V6.1 的“忠实深读 + 长文分层”升级为一个更明确的认知任务契约：

~~~text
Raw Source
→ Restore Cognitive Topology
→ Identify Cognitive Units / Engines
→ Choose Compression Contract
   ├─ Coverage-Preserving
   └─ Cognitive-Synthesis
→ Deliverable
→ Acceptance Gate
→ Repair if needed
~~~

两条 Contract 共用同一个理解核心，分叉发生在“读懂以后哪些信息允许消失”：

- **Coverage-Preserving**：Coverage first, compression second。所有具有独立意义的认知单元必须可追踪，只压缩单元内部重复、同功能案例和语言冗余。
- **Cognitive-Synthesis**：Understanding first, coverage second。允许跨单元归并、抽象和省略低价值信息，但压缩上限是 **Model-Preserving Compression Boundary**：不能让未读原文的人形成不同的核心认知模型。

这不是“长版 / 短版”的区别。篇幅由材料复杂度和认知价值决定；Contract 决定的是信息保留规则。

V6.4 同时把自检升级为真正的 **Acceptance Gate → Repair Loop**：Coverage 路线重点防漏项和过度合并，Synthesis 路线重点防忠实改写和过度压缩。

> **Deep Read 可以替代理解性重读，不能替代证据性回查。**

## Learning V0.5.3

主体调整为：

~~~text
Ground Object
→ Build Model
→ Find Gaps
→ Project to Use
~~~

当用户对一个概念仍觉得抽象时，Learning 优先用具体任务和对照情境解释“引入它前后到底哪一步发生了变化”。如果找不到真实差异，允许结论是“这个区分对当前任务没有实质价值”。

> **抽象应该压缩已经理解的事实，而不应该成为解释的起点。**

Teaching Example 仍属于 Learning；只有当用户已经理解、需要检验自己能否独立判断或操作时，才进入 Practice。

V0.5.3 在不改变 Learning 主体架构的前提下，把 **Vary One Condition** 从技术机制中的局部能力推广为按需启用的 **Boundary Variation**：模型初步建立后，如果改变一个关键前提、观察角度、变量、范围或边界会带来明显认知增量，就只改变一个，观察哪些结论仍成立、哪些削弱或消失、哪些问题已经超出当前材料的回答能力。它不是强制步骤，也不是科学论证 checklist。

对 mechanism-heavy technical knowledge，Learning 继续保留按需启用的深度路径：

~~~text
Ground
→ Run Once
→ Explain Mechanism
→ Vary One Condition
→ Compress Model
~~~

目标不是固定输出“定义 / 原理 / 示例 / 优缺点”，而是让一个真实输入经过系统时的关键状态、表示、资源或控制流变得可观察。随后改变一个关键条件，看当前模型是否能够解释结果为什么变化。

> **技术理解的更强判据：模型不只能够描述系统，还应该能够解释并预测相邻条件变化。**

但在真正阻塞模型时允许：

~~~text
Gap
→ Adaptive Probe / Research
→ Update Model
~~~

Learning Probe 的目标是减少 **knowledge uncertainty**。

如果问题变成“你到底会不会”，转入 Practice。

## Practice V0.2

Practice 的产品定位从“检验是否会用”改为“把已经理解的知识落进真实工程”。

核心路径：

~~~text
Knowledge Model
→ Ground Real Scenario
→ Build Engineering Model
→ Implement End-to-End
→ Run One Concrete Path
→ Verify
→ Troubleshoot
→ Operationalize
→ Generalize
~~~

Practice 的完成标准不是“用户答对了”，而是：

> **一个已经理解概念、但没有真正实施过的人，拿到输出后能够开始实际动手，并知道怎样判断做对、怎样排错、最终要留下哪些工程产物。**

RAG 文档切分回归案例验证了这一点：输出不能停在 chunk size / overlap 定义，而需要把 Parser Block Schema、结构恢复、Chunk Policy、Metadata、Parent-Child Retrieval、具体 Query 链路、Golden Eval、故障排查和工程目录真正串成一条可执行路径。

旧版 Diagnose / Practice Probe / Interview Stress / Guidance Fading 不再属于 Practice Core。原 Stress 的有效部分仅保留为 Failure & Troubleshooting，用来暴露工程模型边界，而不是考试用户。

## Skills

~~~text
skills/
├── article-deep-read-v6.4/
│   └── SKILL.md
├── vibe-review-v0.10/
│   └── SKILL.md
├── system-learning-v0.5.3/
│   └── SKILL.md
└── practice-v0.2/
    └── SKILL.md
~~~

## Evaluation Workflow V0.1

Eval 路由同步收敛为：

`D / R / L / P`

原 Q case 已重新归属：
- “把问题问清楚 / 专家访谈求证” → Learning；
- “用场景或面试追问检验是否会用” → Practice。

Learning V0.5.1 的 grounding regression 继续保留，重点验证：
- 概念差异先回到真实任务，而不是继续堆 taxonomy；
- 能同时给出低差异场景与高差异场景，明确价值边界；
- 用户明确说“还是没懂”后会降层恢复，不再增加上位术语；
- 抽象出现在具体差异之后，而不是之前。

Learning V0.5.2 的 mechanism-depth regression 继续保留，重点验证：
- 技术概念是否通过最小具体实例真正“运行一遍”；
- 是否从流程进一步解释每一步为什么存在；
- 是否通过移除组件 / 改变规模 / 关闭缓存等单变量变化解释结果变化；
- 是否把 prediction 当作理解检查，而不是把 Learning 变成考试；
- 是否能利用 Deep Read 的比喻和案例作为脚手架，最终回到真实机制。

Practice engineering-transfer cases 验证：
- 是否从 Knowledge Model 进入真实工程场景，而不是再次解释概念；
- 是否明确系统位置、组件边界、数据/状态/接口与工程产物；
- 是否至少让一个具体输入跑完整链路；
- 是否提供可执行的验证、故障定位和修复路径；
- 是否区分概念本身的不变量与当前项目的实现选择。

V2.5.1 commit `9bbc0360616b60c4d960e412979b841853a10369` 固定为本次架构收敛前 baseline。

本地校验：

~~~bash
python scripts/validate_skills.py
python scripts/validate_evals.py
~~~

## 使用

以根目录 `SKILL.md` 作为唯一入口。
