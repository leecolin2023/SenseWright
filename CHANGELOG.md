# Changelog

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
