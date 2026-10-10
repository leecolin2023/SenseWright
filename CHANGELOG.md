# Changelog

## Unreleased — Learning problem discovery and question validity (V0.6.2 refinement)
- 修复 Learning “默认已有问题是正确问题”的深层缺陷。在 Ground 之后、Problem Chain 之前新增**按需触发的 Problem Discovery / Framing**，把用户任务/选样规则、主研究问题、机制子问题和证据核验问题分开；不新增独立 Skill。
- 在真实矛盾、异常、竞争机制和关键现实约束中筛选问题；用**解释力、区分力、可验证性及用户价值**替代“抽象得更高就是更深刻”；不得从选出的上涨股票倒推涨价因果。
- 加入修题回路与停止条件：后续证据推翻起点时先改问题；单纯定义/精确问题不强制升级成宏观研究；不自行改写用户使命，不预写结论。
- 补充股价强势样本、两家业务逆差、代码执行、银行流程、明确短问题等跨领域回归；更新 README/Router 和设计说明。静态检查不能证明输出行为与 D/R 隔离真实有效。

## Unreleased — Learning reality calibration (V0.6.2 in-place refinement)
- 不新增第五条 Skill，不更改 D/R/L/P 编排；在 Learning V0.6.2 中新增按需触发的 **Reality Calibration / 现实校准**，延续既有 Mechanism-to-Implementation Mapping 与 Contrast & Vary。
- 不将“财务量化”升格为通用硬门槛：数量敏感用最小临界值/数量级；流程用状态与交接；程序用执行证据；医学/历史/社会观察用证据层级、可比性和反例；简单概念允许跳过。
- 明确同口径比较、事实/假设/推导/未知、单变量变化、结论修正和停止条件。真实证据缺失时只说明最小需核验的证据，不捏造测量数据。
- 增加覆盖金融、性能、业务流程、健康证据、硬件价格可比性、短概念的回归测试；静态验证结构与元数据，行为优劣仍需匹配 Runtime 评测与人工审查。

## V2.8.2 — Mechanism-to-Implementation Mapping in Learning V0.6.2
- 新增 `skills/system-learning-v0.6.2/SKILL.md` 并替换活跃 `V0.6.1` 路由；保留本轮独立 **D + R → L**，其他 D/R/P Skill 版本不变。
- 将原源码专项规则**泛化为通用“机制到实现映射”**：技术书、算法、源码、配置、命令、实验、协议及工程/业务流程皆适用；区分研究顺序（先核实材料/行为，再判断机制）与教学顺序（问题→必要机制→具体实现→可核验证据→有意义的新问题）。
- 保留源码学习精准性：从真实问题触发 Learning，结合关键调用/数据链与可核验位置，而非代码/API 清单；实现与预想冲突时纠正机制，不捏造代码或实测。
- 增加“机制独立性 + 实现锚定”两道内置自检，简单概念不强迫跑完整实现链或长文章。
- 新增源码回归 #31–33 和跨领域技术教材回归 #34–35（SQL 事务、Linux 进程信号），更新触发用例和静态校验；冻结 V0.6.1 Git baseline。静态通过不证明模型行为优越或真实 D/R 隔离 Trace。


## V2.8.1 — Mandatory D/R before Learning
- 收敛活跃 Learning Skill 为精简执行契约，合并重复的 Ground / Problem Chain / Boundary Variation / Gate / Acceptance 说明；保留回归用例，版本演变解释仅存于非运行文档。
- System Learning V0.6.0 → **V0.6.1**，D V6.4、R V0.10、P V0.2 的独立职责保持不变。
- 所有含 L 的路线强制展开为 **D + R → L**：D、R 只从本轮原始输入独立执行，可以并行，但必须全部完成后才启动 L，不能用历史结果代替。
- L 必须读取 D/R 当轮结果，但不照搬它们。**Mandatory execution, selective incorporation**；D 恢复认知结构与案例，R 独立检查逻辑与证据，L 再回到真实对象和机制。
- 无独立文档时仍基于问题原文进行轻量 D/R，不杜撰原文、批评；D/R 分别运行的硬隔离需真实宿主编排和 trace，静态 Skill 不能保证。
- 更新 Router、README、L Skill、评测路由/验证脚本、新增案例和架构文档；冻结前版 V0.6.0 基线。


## V2.8.0 — Learning: transfer IntraMate's problem-driven method

- System Learning **V0.5.3 → V0.6.0**。Deep Read V6.4、Review V0.10、Practice V0.2 核心不变。
- 从 IntraMate `Architecture/method/00-learning-method.md` 吸收 **Problem First、Mechanism Before Framework、知识与原生证据分离、三道内置 Stabilization Gate**；不复制其三框架比较和 Agent 领域架构结论。
- Learning 新增可追溯的问题链：`Real Problem → Current Mechanism Fails → Minimal Necessary Behavior → Next Problem (if useful) → Stable Model`。保留 V0.5.3 具体化、机制可运行、单变量变化、适应式补缺能力；不强制非技术主题跑长技术流程。
- 区分 **Problem Knowledge / Implementation Evidence / Architecture Decision**。规定 UNKNOWN ≠ ABSENT、ABSENT ≠ BUILD、Knowledge Stable ≠ Implementation Ready；无真实 Probe 不声称 executable evidence。
- 将 **Problem-chain Review、Concept First-Appearance Audit、Boundary & Evidence Review** 作为生成过程中的 Draft → Gate → Repair → Re-check，而非交付后的“待审阅”阶段。
- 修复旧的“知识测验自动路由 Practice”描述；Practice 聚焦知识到实际工程实现的转化。
- 新增六个 Learning 回归用例与负面提纲 fixture，更新触发测试，冻结升级前 `learning_v0_5_3` baseline 为 `6bfc5519e089d8a1b08d254d500e947388400e78`。
- 此版本只增加评测定义和静态契约，不宣称已经完成新旧 Skill 在相同模型/参数下的实测对比。


## V2.7.0 — Practice engineering transfer
- Practice 从 **V0.1 升级到 V0.2**；Deep Read V6.4、Review V0.10、Learning V0.5.3 保持不变。
- Practice 的 Mission 从 **Knowledge Assessment / capability stress test** 正式调整为 **Knowledge-to-Execution / Engineering Transfer**。
- 中心问题从“我真正会了吗？”改为“**如果现在真的要把它做出来，我该怎么做？**”。
- 新核心路径：`Ground Scenario → Engineering Model → Implement End-to-End → Run One Path → Verify → Troubleshoot → Operationalize → Generalize`。
- 新增 Engineering Artifacts：Practice 不只讲步骤，还应明确真实实施需要创建、运行和验收的模块、Schema、配置、测试、Eval、监控或其他工程产物。
- 保留 Learning Knowledge Model 作为最重要上游 Reference Context；Practice 实施中暴露的知识缺口、未验证前提和机制边界允许回流 Learning。
- 旧版 Diagnose / Practice Probe / Interview Stress / Guidance Fading 退出 Practice Core；Stress 的有效部分仅保留为 Failure & Troubleshooting，用于暴露工程边界而不是考试用户。
- Router 同步更新：P 只在用户需要把已理解知识放进真实工程、完整走通实施与验证路径时触发；单纯出题、模拟面试或连续追问不再因为测试形式自动路由 P。
- Eval 将旧 token capability-test case 替换为 **RAG 文档切分** 与 **Agent State** 两个工程迁移回归，并冻结升级前 commit `1aa694d00e896f7c7896b07c5439c252e4344d82` 为 `practice_v0_1` baseline。

## V2.6.4 — Deep Read dual compression contract
- Deep Read 从 **V6.1 升级到 V6.4**；Review、Learning、Practice 与 D / R / L / P 总体架构保持不变。
- Deep Read 明确为完整认知任务契约：`Input / Context → Deep Read Core → Compression Contract → Deliverable → Acceptance Gate → Repair`。
- 保留“删除语言冗余，不删除理解过程”，并把核心阅读逻辑收敛为：恢复材料自己的认知拓扑、忠实认知推进、识别认知发动机、保留必要解释冗余、按功能而不是形式取舍内容。
- 新增 **Dual Compression Contract**：`Coverage-Preserving` 与 `Cognitive-Synthesis` 共用同一阅读核心，分叉只发生在读懂以后“哪些信息允许消失”。
- Coverage-Preserving 以 **100% 独立认知单元可追踪** 为底线，只压缩单元内部重复、同功能案例和语言冗余；避免把“完整覆盖”误解为原文复述。
- Cognitive-Synthesis 允许跨单元归并与抽象，并使用边际认知收益继续压缩；压缩上限定义为 **Model-Preserving Compression Boundary**，不能让陌生读者形成不同的核心认知模型。
- 明确两条 Contract 不是“长版 / 短版”，也不按文章、会议、制度等材料类型固定路由，而按用户的交付意图选择。
- 将自检升级为真正的 **Acceptance Gate → Repair Loop**：Coverage 路线重点检查 Unit Coverage / Over-Merging，Synthesis 路线重点检查 Cognitive Density / Model Preservation。
- Eval 新增同源双契约回归 fixture，并冻结升级前 commit `4692f7f332059cdf9681e046dd60d5c592d850f4` 为 `deep_read_v6_1` baseline。

## V2.6.3 — Learning boundary variation
- System Learning 从 **V0.5.2 升级到 V0.5.3**；D / R / L / P 总体架构、Router、Deep Read、Review 与 Practice 均保持不变。
- 将原本主要用于 mechanism-heavy technical knowledge 的 **Vary One Condition** 向通用 Learning 提升半级，新增按需启用的 **Boundary Variation**。
- Knowledge Model 初步建立后，如果改变一个关键前提、观察角度、变量、范围或边界会带来明显认知增量，优先只改变一个条件，观察结论是继续成立、变弱、消失/反转，还是问题已经变得无法由当前材料回答。
- 明确 Boundary Variation **不是强制 checklist，也不是科学论证流程**；只有它能暴露适用边界、阻止过度外推或重构问题时才执行，避免 Learning 因追求严谨而退化成 Review / Research。
- 对技术机制继续保留 Teaching Variation：`条件变化 → 哪一步首先受影响 → 状态/成本/结果怎样变化 → 为什么`；通用 Boundary Variation 与技术机制深挖共用“改一个条件”的思想，但不要求所有主题都跑技术模板。
- Learning 输出与验收同步增加：当模型容易被外推时，应能说明“什么还成立、什么不再成立、什么已经变成新问题”。
- 本次为小步约束升级，不新增一级 Skill、不修改非对称协作架构，也不增加新的 mandatory pipeline。

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
