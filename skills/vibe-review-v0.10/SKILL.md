---
name: vibe-review
description: Independently review a document, argument, plan, architecture, or proposal with full substantive coverage before prioritizing findings. Use when the user asks whether material is sound, sufficient, well-reasoned, decision-useful, complete, or worth changing. Atomize the source into reviewable units, preserve their relationships, review every unit with adaptive depth, and report selectively based on materiality.
---

# Vibe Review V0.10 — Coverage Before Materiality

## 目标

> **先完整覆盖，再独立审阅；审阅可以全，报告可以有重点。**

Review 不是为了制造更多问题，而是判断材料是否足以完成它该完成的任务。

两条核心原则：

> **Coverage before judgment.**  
> **Review comprehensively; report selectively.**

Materiality 只能决定“哪些发现值得重点输出”，不能提前决定“哪些原文值得被审”。

---

## Core 1 — Understand the assignment

先搞清楚这份材料为什么存在、当前负责做到哪一步。

- 如果有用户目标、任务书、招标/合同、上游要求，优先依据它们；
- 如果只有文章本身，就以作者明确提出的问题为准，不发明外部 Mission；
- 普通文章、随笔、观点文默认是自足文本，不强行做项目 Mission 分析。

用当前文档应承担的职责评价它，不因为未来还能做得更细，就把“当前没做”自动判成缺陷。

---

## Core 2 — Build the Review Map

Review 在判断重要性之前，先把 Raw Source 转成一组 **Atomic Review Units / 原子审阅单元**。

### 什么是 Atomic Review Unit

> **最小的、能够被独立理解，并接受某种审阅判断的语义单位。**

它不等于句子、段落或 bullet。

例如：

> “系统上线后，由客户经理发起申请，经团队长审批后提交总行，原则上 2 个工作日内完成。”

至少可以拆成：

- 客户经理负责发起申请；
- 申请需要团队长审批；
- 团队长审批后提交总行；
- 处理时限原则上为 2 个工作日。

### Atomization 阶段禁止提前筛选

这一阶段不问：

- 这重要吗？
- 这是不是重点？
- 这最终要不要输出？
- 这属于哪种典型问题？

只问：

> **这段原文究竟表达了几个可以独立成立的内容？**

先拆完整，再判断。

### Coverage Reconciliation

原子化后检查：

> **原文中每个有信息内容的 source span 是否都有去处？**

每一部分至少应：
- 被一个或多个 Review Unit 覆盖；或
- 明确归为纯结构/过渡/无新增语义的重复内容。

“没有输出”不能等于“没有看见”。

### Preserve Relations

原子化不能把关系拆没。

需要保留真正影响语义的关系，例如：
- 条件；
- 例外；
- 因果；
- 前后依赖；
- 责任转移；
- 范围限定；
- 同一概念在不同位置的引用。

如果一个 Unit 是另一个 Unit 的条件、例外或依赖，应在内部关系中保留。

### 长文、表格与重复内容

- 长文可以按语义区块处理，但每个区块仍要完成原子化和 coverage；
- 表格、流程图、附录只要承载事实、规则、数字、责任或边界，就进入 Review Map；
- 重复内容先全部进入 coverage，再允许聚类；
- 聚类前必须确认不同位置表达是否真的一致，不能用“看起来重复”代替检查。

---

## Core 3 — Review Every Unit

所有原子审阅单元都进入 Review。

但：

> **全覆盖 ≠ 等深度。**

不同 Unit 可以使用不同分析深度。

### 先分类，再选择审阅方式

分类发生在 atomization 之后，只用于决定怎么审，不用于决定审不审。

可能的 Unit 类型包括但不限于：
- 事实陈述；
- 数字或比例；
- 判断或预测；
- 因果关系；
- 定义；
- 假设；
- 流程步骤；
- 责任分配；
- 条件与例外；
- 方案设计；
- 依赖；
- 结论；
- 行动建议。

不要先拿固定分类表去全文“找问题”。

### Adaptive Depth

例如：
- 普通、低风险且自洽的事实 → 快速检查；
- 核心数字 → 深查口径、分母、时间范围和来源；
- 关键因果 → 深查证据强度、替代解释和边界；
- 流程 / 责任 → 检查主体、动作、状态、交接和空档；
- 条件 / 例外 → 检查与主规则及其他位置是否冲突。

审阅深度可以不同，但 Unit 不能因为“看起来次要”而被默认跳过。

---

## Core 4 — Think Independently

完成 coverage 后，再从材料自己要解决的问题出发独立思考：

- 真正的问题是什么？
- 证据能支持到什么强度？
- 有没有其他解释？
- 哪些判断是事实、哪些是预测或价值选择？
- 当前方案是否遗漏了会阻塞下游的条件？
- 如果必须行动，什么会真正改变选择或风险？

不跑固定 Checklist；Triggered Checks 只是对已识别 Unit 选择合适的审阅 Lens。

---

## Core 5 — Assess Materiality After Review

Materiality 发生在 Review 之后。

每个发现可以内部判断为：
- **Material**：会改变理解、结论可信度、优先级、行动方向、风险或关键边界；
- **Minor**：存在问题，但不改变当前核心判断或行动；
- **No issue**：已检查，没有需要报告的问题。

只有这一步之后，才决定最终输出篇幅。

> **Materiality 是 reporting filter，不是 coverage filter。**

---

## Triggered Checks — 用来决定怎么审，不决定审不审

### 数字 / 评分 / 覆盖率
检查分母、定义、口径、周期、算术、是否把代理指标当目标。

### 因果 / 预测
检查证据能否支持因果强度；区分趋势判断、时间点预测和价值判断。

### 方案 / 架构
检查边界、依赖、故障模式、替代方案和成本。

### 组织 / 流程 / 责任
检查控制目标、角色、动作、状态转换、交接和责任空档。

### 外部权威 / 监管 / 行业惯例
区分正式要求、公开证据、访谈、经验判断和作者推断。

### 投入较大的建议
检查价值、替代方案、优先级和投入回收逻辑。

这些 Lens 只有在相应 Unit 出现时启用，不构成预设问题清单。

---

## 写作方式

最终答案优先是自然分析，不打印内部 Review Map。

通常可以写：

1. **总体判断**：材料是否完成当前任务；
2. **关键发现**：重点展开 Material findings；
3. **必要的次要发现**：只有用户明确要“全部问题 / 逐项审阅”时再展开；
4. **边界 / 下一步**：只给真正改变判断或行动的内容。

必要时可以简短说明：

> 已覆盖正文、表格、流程、数字、条件和例外；以下只展开会影响判断或行动的差异。

用户同时要求“总结 + 审阅”时，Review 仍直接读取 Raw Source，不依赖 Deep Read 摘要。

---

## 五条禁止

- 不在 Atomization 前先判断“这部分不重要所以可以不看”；
- 不用抽样代替对重复或同类内容的 coverage；
- 不把原子化做成逐句机械切分，并因此破坏条件、例外或依赖关系；
- 不因为文档没写某事就默认应该补；
- 不把“证据不足”写成“结论一定错误”。

---

## 自检

- 原文每个有信息内容的部分是否都能对应到 Review Unit，或明确说明为何没有独立审阅语义？
- 我是否在 coverage 完成前就开始筛“重点”？
- 条件、例外、因果、责任转移等关系有没有在原子化时被拆坏？
- 重复内容是否真的逐一确认后才聚类？
- 每个 Unit 是否至少经过了与其性质相匹配的检查？
- Materiality 是否只影响最终报告，而没有反过来影响 coverage？
- 最终答案是否没有因为“全面审阅”而退化成冗长问题清单？
