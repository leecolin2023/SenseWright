# Changelog

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
