# Changelog

## V2.6.2 — Learning mechanism depth
- System Learning 从 **V0.5.1 升级到 V0.5.2**；D / R / L / P 总体架构和 Deep Read V6.1 均保持不变。
- 保留 V0.5.1 的 Grounding，并针对 **mechanism-heavy technical knowledge** 增加按需启用的 `Ground → Run Once → Explain Mechanism → Vary One Condition → Compress Model`。
- 新增 **Executable Mental Model**：算法、系统、Agent、RAG、数据库、缓存、运行时等主题优先选最小具体实例，追踪真正相关的输入、中间表示、状态、控制流、资源变化、输出或反馈。
- 新增 **Teaching Variation**：一次改变一个关键条件，直接展示哪一步首先受影响、结果/成本为何变化；该过程仍属于 Learning，而不是 Practice。
- 新增 **Prediction as Understanding Check**：机制模型至少应能够解释一个相邻条件变化；如果只能复述定义和标准流程，则认为理解深度仍不足。
- 明确 **比喻是脚手架，不是机制本身**：Deep Read 继续忠实保留作者的故事、比喻和认知桥梁；Learning 可利用它们进入真实机制，并在理解建立后说明类比边界。
- Project to Use 增加 **最小实验**：当语言解释不足时，用最小输入、可观察变量和预期变化验证机制模型，而不是为了练技术搭大工程。
- Eval 新增 3 个 mechanism-depth regression：RAG rerank 的运行与条件变化、Agent State 的状态演化、技术比喻从脚手架回到真实机制。
- 冻结 V2.6.1 commit `4b3e79a263ee90a992cf50a9eb5616fe198e35dc` 为 `learning_v0_5_1` baseline，便于 V0.5.1 vs V0.5.2 相邻版本比较。

## V2.6.1 — Learning grounding before abstraction
- System Learning 从 **V0.5.0 升级到 V0.5.1**；D / R / L / P 总体架构保持不变，本次仅修 Learning 的理解目标与回归标准。
- 恢复并强化“**先解释对象，再抽象方法**”：新增 `Ground Object → Build Model → Find Gaps → Project to Use`，避免用更高层术语解释尚未理解的抽象。
- 新增 **Contrastive Grounding**：对“X 和 Y 有何区别 / 为什么需要 X”优先比较一个低差异场景和一个高差异场景，再总结真实变化与适用边界。
- 明确 **Teaching Example 属于 Learning，Performance Task 才属于 Practice**，避免因为存在 Practice 就把 Learning 退化成抽象讲解。
- 新增 **Grounding Recovery**：当用户反馈“没理解 / 太抽象 / 像生造的 / 实际有什么用 / 不就是 X 吗”时，停止继续上提抽象，回到具体对象逐步跑过程。
- 新增原则：**抽象应该压缩已经理解的事实，而不应该成为解释的起点。**
- Learning 验收新增“能否映射回具体对象、能否指出前后哪一步真正变化”；若框架完整但用户仍不知道“现实里到底改变了什么”，判定 Learning 未完成。
- Eval 新增 3 个 grounding regression：Workspace Agent 概念差异、解释失败后的降层恢复、数据库事务的跨领域泛化。
- 冻结 V2.6.0 commit `5ab713149329685c3834bc97b65bf010c6d70c36` 为 `learning_v0_5_0` baseline，便于 V0.5.0 vs V0.5.1 相邻版本比较。

## V2.6.0 — Learning / Practice convergence
- 将 **Questioning 从一级 Skill 降级为内部控制策略**，active tree 删除 `questioning-v0.1.1`；其历史完整保留在 Git。
- 一级路由从 D / R / L / Q 收敛为 **D / R / L / P**。
- 新增 **P — Practice V0.1**：以 `Diagnose → Situate → Perform → Stress → Debrief` 检验知识能否迁移到真实或仿真情境。
- System Learning 从 **V0.4.4 升级到 V0.5.0**，吸收 Questioning 中用于减少 knowledge uncertainty 的 adaptive probing：Clarify / Evidence / Assumption / Mechanism / Boundary 等按需触发。
- 明确两种提问机制：Learning Probe 用于补知识，Practice Probe 用于暴露能力；不再因“用户要求提问”而建立独立 Q 路由。
- 非对称协作更新为 source-facing D/R + knowledge-facing L/P；D/R 继续严格隔离，L/P 可选择性使用 Reference Context。
- 建立 **L ↔ P 学习闭环**：Learning 输出 Knowledge Model，Practice 暴露 Performance Gap，再回流 Learning 更新模型。
- Eval 路由、trigger cases、reference_context 规则同步迁移到 D / R / L / P；原 Q eval 重新归属 Learning，并新增 Token transfer 的 Practice regression。
- 固定 V2.5.1 commit `9bbc0360616b60c4d960e412979b841853a10369` 为 `pre_practice_refactor` baseline。

## V2.5.1 — Review Coverage
- Vibe Review 从 **V0.9** 升级为 **V0.10**，SenseWright 总体非对称协作架构保持不变。
- Review 新增 **Coverage Before Materiality**：先把 Raw Source 拆成 Atomic Review Units，完成 source-span coverage reconciliation，再进入判断。
- Atomization 阶段禁止提前按“重点 / 重要性”筛选；分类只发生在原子单元形成之后，用于决定审阅方式和深度。
- 原子化必须保留条件、例外、因果、前后依赖、责任转移和范围限定，避免为了 coverage 把关系拆没。
- 所有 Unit 都进入 Review，但允许 adaptive depth；Materiality 从审阅选择器后移为 reporting filter。
- 取消“重复细节抽样”策略：重复内容先逐一进入 coverage，确认一致后才能聚类处理。
- Eval 新增 Review coverage fixture、Gold Atomic Review Units 和漏审回归；新增 `review_v0_9` baseline 指向升级前 V2.5.0 commit。

## V2.5.0 — Asymmetric Collaboration
- 将四种 Skill 的协作关系从“基本独立”收敛为 **非对称协作**。
- Deep Read V6.1 与 Vibe Review V0.9 保持严格 source isolation：两者只面向 Raw Source / 用户直接要求，不读取任何 sibling Skill 输出，D 与 R 之间也不传递结果。
- System Learning 升级至 **V0.4.4**：允许选择性参考 D / R / Q 结果，但明确 `Reference ≠ Evidence`、`Transform, don't copy`、`Selective, not mandatory`。
- Questioning 升级至 **V0.1.1**：允许把 D / R / L 结果作为 inquiry signal，并优先把新确认的信息与未解决 Gap 回流给 Learning。
- Router 增加轻量 Reference Selection：仅当目标包含 L / Q 时考虑 sibling reference；当前不引入 Shared Blackboard 或 Artifact Registry。
- Eval 增加 `reference_context` 元数据与静态边界检查，并增加 Learning / Questioning 的 selective-reference case；D / R case 若配置 reference context 将直接校验失败。

## V2.4.0 — Questioning
- 新增 **Q — Questioning V0.1**，形成 D / R / L / Q 四种认知模式。
- Questioning 采用 `Gap → Probe → Update` 循环：先识别当前最大不确定性，默认一次只问一个高信息价值问题，再根据回答更新认知状态与下一问。
- 引入 Clarify / Reason / Evidence / Assumption / Alternative / Mechanism / Boundary / Missing / Action 等 Question Lens，但明确仅按需触发，不执行固定 Checklist。
- 增加访谈式 Probe：优先把抽象观点追到 Situation / Reason / Action / Result / Reflection。
- Router 增加 Q 路由，并把 Q 设计为可叠加能力，不为 D+Q、R+Q、L+Q 等组合新增独立 Skill，避免组合爆炸。
- Eval V0.1 增加 Q 路由合法性与“第一问质量”case；当前先验证找准第一问，后续再扩展多轮适应性与停止条件。

## V2.3.2 — SenseWright brand migration
- 项目正式更名为 **SenseWright**。
- 根 Skill 标识统一迁移为 `sensewright`。
- README、Eval metadata、workspace manifest、CI 和当前主分支中的品牌引用统一迁移到 SenseWright。
- 三个内部 Skill 名称与版本保持不变，避免品牌迁移与认知逻辑变更混在一起。
- Eval V0.1 的 frozen baseline commit `ffdb60e1f27ae99011d18c29c683dc747cec64f1` 保持不变，品牌迁移不重写历史，也不破坏 old-skill 对照基线。

## V2.3.1
- 将根 Skill 与三个子 Skill 的 frontmatter 统一为 `name` + `description`，兼容当前 Agent Skills 核心 metadata 约定。
- 将版本信息从 YAML frontmatter 移回文档标题 / CHANGELOG，减少自定义 metadata 对跨 Runtime 可移植性的影响。
- 增加 `scripts/validate_skills.py`，静态检查 Skill frontmatter、命名规则与必需字段。
- 增加 **Evaluation Workflow V0.1**：任务 eval、trigger eval、baseline 记录、workspace 初始化、grading/timing 约定与 benchmark 聚合。
- 固定改造前 commit `ffdb60e1f27ae99011d18c29c683dc747cec64f1` 为首个 old-skill baseline。
- 增加 CI，在 push / pull request 时执行 Skill 与 Eval 静态校验。
- 本版本不改变 D / R / L 的核心认知逻辑，只补标准兼容与可回归验证基础设施。

## V2.3
- 在 V2.2 基础上新增 **L — Learning** 路由。
- 集成 System Learning V0.4.3，保留其 `Build Model → Find Gaps → Project to Use` 主体逻辑。
- 明确 D / R / L 三种中心：source-centered / judgment-centered / learner-centered。
- 新增“读懂 vs 学会”边界，避免 Deep Read 与 Learning 路由冲突。
- 复合任务采用已有模式组合，不新增 DRL 等新的 Skill 类型。
- 多路执行默认直接读取原始材料，避免“摘要污染审阅”或“审阅污染学习”。
- 保持 Deep Read V6.1 与 Vibe Review V0.9 核心逻辑不变，避免因新增 Learning 破坏 V2.2 回归基线。

## V2.2
- Router 收敛为轻量 D / R / DR 路由。
- Deep Read V6.1：忠实理解；长文自动分层。
- Vibe Review V0.9：四步独立审阅；专项检查按触发启用。
