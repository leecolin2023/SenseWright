# SenseWright 评测指南 — Eval V0.3

> 生成规则不等于评测规则。Skill 只保留真正可能改善模型行为的最小干预；Eval 可以观察更多质量问题，但不因发现问题就自动增加一条 Skill 规则。

## 目标与范围

评测使用 **规则要防止的失败 → 任务 Rubric → 独立证据评分 → 匿名成对比较**。核心判断是：**移除某条规则后，是否更容易出现重要、可观察的失败？保留它是否在相同条件下减少失败？**

所有 **80 个原有案例** 均保留 ID、任务、路由和 fixture，未删除、归档或重新编号：

- **Learning：57 例**，沿用 R00–R15 及 D/R→L 前置合同，评分字段为 `learning_eval`。
- **Deep Read：4 例**，直接在原有 1、4、20、21 号案例上改写，字段为 `deep_read_eval`；不把 57 个 Learning 案例里的前置 D 运行重复算成独立 Deep Read 测试。
- **其他 R/P：19 例**，仍使用原有 `assertions`；D+R 的第 4 例也额外保留原 Review/职责隔离断言。
- **Trigger：67 条**，独立评估路由触发，不能与生成质量得分混在一起。

Deep Read 现在只有两条活跃规则：

| 规则 | 要检验的实际失败 | 原有案例 |
|---|---|---|
| **D02：保留使读者理解的关键推导** | 明明提到了例子，却把情境、动作、差异和原因压成抽象标签；或者只留结论，丢失理解桥梁 | #1 公告概括/可靠性判断、#4 企业助手方案 |
| **D03：按目标决定压缩边界** | 完整覆盖型漏掉独立议题与行动，或认知提炼型逐项机械复述、错误归并、压成只有结论 | #20 完整覆盖、#21 认知提炼（同一 fixture） |

**重要限制：** 四个既有 D 案例可以验证数据管道和部分重要失败，但材料较短，尚不足以证明新规则对长篇、生动叙事材料的改善会稳定出现。特别是《宋徽宗联金灭辽》长稿所暴露的“故事被压成概念标签、解释厚度丢失、出现防御性插话”，当前短 fixture 只能覆盖其中一部分。下一阶段要通过真实多次执行以及更具判别力的长篇材料检验，不能把设计期案例直接当成模型效果证据。

## 定向回查：条件式修复的独立实验

Deep Read 的 **D02 可选定向回查**已引入 Skill：只有初稿丢失了重要且可从原文定位的理解桥梁，才定向读取原文并局部修复；初稿已足够时直接停止，不规定每篇必须回查。

为避免与“初次生成质量”混淆，另设 [Recall Eval V0.1](recall/README.md)。它复用已有 Raw Source，但**固定初稿**，用 6 个应修复/应停止的正负例考察两条规则 D02/D03，且不改变原有 80 个案例：

- 静态核验：`python scripts/validate_recall_evals.py`
- 初始化隔离实验：`python scripts/prepare_recall_eval.py --iteration 1`
- 候选修订提交后准备匿名阅读：`python scripts/prepare_recall_eval.py --iteration 1 --prepare-pairwise`
- 独立盲读与人工/模型评审提交后汇总：`python scripts/aggregate_recall_eval.py .eval-recall-workspace/iteration-1`

比较三项不同的结果：**是否该触发回查**、**匿名读者能否更准确地重建原文理解**、**有无不必要重写或额外成本**。参考答案与期待触发结果只给评审，不给生成方。没有实际回查输出与独立评分时一律显示 ungraded；合成 smoke test 不构成实际效果证明。

## 单案例评测合同

Learning 与 Deep Read 均使用以下字段：`primary_rule`、`related_rules`、`failure_mode`、`rubric`、`critical_failures`、`not_required`、`grading_policy`、`pairwise_policy`。Deep Read 额外具有 `compression_mode`，取 `coverage_preserving` 或 `cognitive_synthesis`。

`primary_rule` 只标记**该例重点验证的一个规则**，`related_rules` 不额外扣分。失败模式是评审要观察的现象，**不是要求被测模型在文章中打印的文字**。`not_required` 明确不因格式、篇幅、逐字复述、全部案例保留或没有机械免责声明而扣分。

Rubric 每项评分为 0（缺失/错误）、1（部分成立）、2（充分成立），合计 0–10：

| Skill | Criterion | 权重 | 关注什么 |
|---|---|---:|---|
| Learning | goal / mechanism / boundary | 4 / 4 / 2 | 学习目标、运行机制、重要条件 |
| Deep Read | task_fit / cognitive_value / integrity | 3 / 5 / 2 | 阅读目标、真正帮助理解的内容与压缩质量、核心关系与内容忠实度 |

Deep Read 刻意让 `cognitive_value` 权重最高，但**不能通过机械计数例子或篇幅评分**。要回看原始 fixture，找出作者的论证如何通过具体场景和例子建立理解：如果删除后读者难以理解机制，即便保留了术语与结论，也应扣分。关键内容逆转、遗漏独立行动、把不同限制硬归为单一原因等列在 `critical_failures`，独立报告，不能被普通高分抵消。

## 运行与盲评

建议按同一模型、同一问题、同一 fixture、同一上下文/工具权限、同等采样设置对比新版与合适的冻结版本。对于验证 D02/D03 最小规则是否有效，可优先使用 `deep_read_v6_4_dual_contract`，再补 `without_skill`；若只想看删掉 D01 之后有无退化，可使用 `deep_read_v6_4_pre_two_rules`。Learning 可选邻近 Learning 的冻结基线。基线在 `baselines.json` 中，不要覆盖已有冻结版本。

```bash
python scripts/validate_skills.py
python scripts/validate_evals.py
python scripts/test_eval_pipeline.py

# 每一轮评测使用一个新 workspace，避免污染匿名分组
python scripts/init_eval_workspace.py --iteration 1 --baseline deep_read_v6_4_dual_contract
```

初始化只创建元数据、空评分模板和隐藏的 A/B 分配，**不调用模型、不生成文章、不评分**。完整的工作流为：

1. 对同一个案例生成 `with_skill/outputs/response.md` 与 `<baseline>/outputs/response.md`；被测模型只看到任务、相应原始 fixture 和本组 Skill/运行条件，**不得看到 Rubric、期待结论和评审结果**。
2. 运行 `python scripts/prepare_pairwise.py .eval-workspace/iteration-1`，导出 `pairwise/A.md`、`B.md`、各自的 `*.grading.template.json` 和 `judge_packet.json`。
3. 独立评审者只能看到匿名 A/B、原材料和 Rubric，分别为 A/B 填 `*.grading.json`；必须提供 `reviewer.id`、`kind`、`independent: true`、`blind_to_variant: true`，各 criterion 的 0/1/2 分与具体回答证据，以及 `failure_mode_assessment.occurred`、严重程度与证据；关键失败逐条判定。再根据同一用户目标投独立 `vote.json`（A / B / tie，附依据）。**不要提供 `assignment.json` 给评审者**。
4. 运行 `python scripts/resolve_blind_grades.py .eval-workspace/iteration-1`，校验评分后解盲并导入，不覆盖已有正式评分。
5. 运行 `python scripts/aggregate_benchmark.py .eval-workspace/iteration-1`，输出 `benchmark.json` 与 `benchmark.md`。

D+R 第 4 例的 **Deep Read 部分**与其他 D 案例一样匿名评分；额外保留的 Review / 运行职责隔离断言使用 `review.grading.template.json` 单独填写 `review.grading.json`，汇总为 legacy 断言成绩，**不能用文章样式宣称真正做到了上下文隔离；隔离需运行 Trace**。

Learning R00 的独立 D/R 与交接也必须有真实执行 Trace。缺少 Trace 应标为 `unverified`，不得当成已确认失败或者已验证通过。

## 汇总口径与限制

`benchmark.json` 保留原有 Learning 统计 `learning_by_primary_rule` / `pairwise`，并新增独立的 `deep_read_by_primary_rule` / `deep_read_pairwise`。各 Skill 展示：

- 已评分数/应评分数、平均 Rubric 分数、发生失败模式的案例数、关键失败案例数。
- 相同案例**两份评分都齐全**时才统计分差和失败模式减少/恶化；仅单侧已评分不能比较。
- 只有合法独立、匿名、有实际输出与投票依据的 A/B 才计入成对偏好；缺失数据记 `ungraded` 而非 0 分。
- Review/Practice 的既有断言单独计数，不混入 Deep Read 的认知价值评分。

评审独立性声明不是技术证明；合成测试评分只用于证明流水线处理，不代表实际文章达到分数；没有读者测验也不能说已证明真实读者理解能力提高。

**原则：Eval 负责观察规则是否降低了用户实际感受到的阅读失败。不要为了让 Eval 好评分，而倒逼 Deep Read 增加固定模板、免责声明或多余阅读步骤。**
