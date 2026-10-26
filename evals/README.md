# SenseWright 评测指南 — Eval V0.2

> **活跃合同（2026-10）**：Learning V0.7.0 使用**规则失败模式 → 任务 Rubric → 独立证据评分 → 匿名成对比较**。保留原有 80 个测试 ID、原始任务和 fixture；其中 57 个 Learning 案例是在 `evals.json` 原位改写，未删除、归档或重新编号。D、R、P 的既有断言继续保留。历史设计见 [HISTORY.md](HISTORY.md)。

## 为什么这样评测？

Learning 的每条 R00–R15 规则都针对一类具体认知失败：例如把术语堆砌当机制解释、把教学例子冒充实测、让小误差掩盖正确主干、把简短定义强制升级为研究项目。

**评测的是这些失败有没有发生，以及新规则是否实际减少失败，而不是模型有没有输出固定章节或背诵规则名。** 任务 Rubric 应评估用户想学懂的对象、必要的机制过程及关键边界；不能因教材采用自然的「定义→原理→步骤」顺序而机械扣分。用户在题目中**明确要求**先解释某个场景时，仍应尊重该题特定要求。

## 文件与测试集

| 路径 | 功能 |
|---|---|
| [evals.json](evals.json) | 80 个既有测试：57 个 Learning 使用 `learning_eval`，其余 Skill 使用既有 `assertions` |
| [fixtures/](fixtures/) | 现有原材料，生成阶段只传入任务对应文件 |
| [triggering.json](triggering.json) | 67 条触发/近邻负例，独立于文章质量评分 |
| [baselines.json](baselines.json) | 冻结 Git 对照版本；选择合适邻近版本而非默认比较最早版本 |
| [../scripts/validate_evals.py](../scripts/validate_evals.py) | 静态验证字段、fixture、Learning R00–R15 主规则覆盖 |
| [../scripts/init_eval_workspace.py](../scripts/init_eval_workspace.py) | 生成任务目录、独立评分空模板、匿名 A/B 分配 |
| [../scripts/prepare_pairwise.py](../scripts/prepare_pairwise.py) | 将实际输出复制为匿名 A/B 文件 |
| [../scripts/aggregate_benchmark.py](../scripts/aggregate_benchmark.py) | 汇总已完成的独立评分、独立运行记录及成对偏好；无评分保持未评测 |

## 一、单案例合同

每个 Learning 测试保留已有 `id`、`name`、`prompt`、`files`、`expected_route` 和 D/R→L 前置合同，改为：

- `primary_rule`：本例重点验证 R00–R15 的哪条规则；`related_rules` 仅说明相关维度，**不产生重复扣分**。
- `failure_mode`：本规则需要避免的具体失败；不是强迫输出展示的文字。
- `rubric`：三个独立任务检查：`goal`（权重 4）、`mechanism`（权重 4）、`boundary`（权重 2）。
- `critical_failures`：会推翻核心学习结论的错误；独立报告，不用细枝末节抵消。
- `not_required`：本例不得强制的形式或额外步骤；**不是禁止用户明确要求的内容**。

评级为每项 `0`（缺失/错误）、`1`（部分成立）、`2`（充分成立），加权得分 `Σ(weight × rating/2)`，范围 0–10。评分须引用实际回答证据，不能仅复制 Rubric 或无依据标注通过。关键失败单独记录，不能因为总分不错就略过。

R00 是**运行约束**：需要宿主 Trace 证明 D、R 独立处理同一 Raw Input，D/R 全部结束后才启动 L，且 L 收到双方结果。文章分三节或自述执行成功都不足以证明。缺少 Trace 标为 `unverified`，不能误报成功，也不应擅自当作已确认失败。

## 二、运行：同输入、同条件、不同 Skill

```bash
python scripts/validate_skills.py
python scripts/validate_evals.py
python scripts/init_eval_workspace.py --iteration 1 --baseline learning_v0_6_2_pre_general_refactor
```

可按实际研究问题更换基线；若要识别**新版规则自身**的增益，优先比较最接近改动前的版本，再加 `without_skill` 对照。冻结 Git 基线不能被随意改写。

初始化**不调用任何模型、不生成文章、不评分**。同一案例的两份实际结果分别保存：

```text
.eval-workspace/iteration-1/<case-name>/
  eval_metadata.json
  with_skill/outputs/response.md
  with_skill/grading.template.json
  with_skill/grading.json             # 由独立评审另行生成
  with_skill/preflight.json           # 真正有 Trace 后再标 verified/failed
  <baseline>/outputs/response.md
  <baseline>/grading.json
  <baseline>/preflight.json
  pairwise/assignment.json           # 不能交给盲评者
  pairwise/A.md                      # 由 prepare_pairwise.py 准备
  pairwise/B.md
  pairwise/vote.template.json
  pairwise/vote.json                  # 由盲评者另行填写
```

生成两份回答时**仅提供 prompt、对应原始 fixture 和被测的 Skill/宿主条件**。不能把 `expected_output`、Rubric、`critical_failures` 或盲评答案反馈给被测模型，否则答案将被污染。记录运行模型、版本、温度、工具权限和成本口径，尽量让两组条件一致。不要把数天后不同模型版本的结果硬当 A/B。

## 三、独立评审与成对比较

独立评分的评审者应看到同一份原题、允许使用的材料、回答和 Rubric，但**不能把回答模型的自评当独立证据**。可以是另一模型或人工评审，记录 `reviewer.id`、`kind: human|model`、`independent: true`、`blind_to_variant: true`。将填好的 `grading.template.json` 保存为 `grading.json`，每条 criterion 填 `rating` 及可核查的 `evidence`，关键失败填 `occurred` 及证据。未填完整不会被统计为 0 分，而是 **ungraded**。

```bash
python scripts/prepare_pairwise.py .eval-workspace/iteration-1
```

该命令仅在两份实际输出都存在时复制 A.md/B.md。盲评者只应接收 A、B、同一问题/材料及 Rubric，**不可接收 assignment.json，也不能看到模型/版本标签**。按读者目标比较哪个回答更有助理解、是否出现重大机制错误、是否过度教学或无据宣称；允许 `tie`。在 `vote.json` 填 `reviewer`（独立、盲评）、`winner: A|B|tie` 及 `evidence`，再由统计程序读取隐藏的答案分配映射。评分标签是过程声明，不等于已技术证明评分者独立；重大差异应人工复核。

## 四、聚合与解释

```bash
python scripts/aggregate_benchmark.py .eval-workspace/iteration-1
```

生成 `benchmark.json` 与 `benchmark.md`。对 Learning 分别展示：

1. **评分覆盖率**（graded/total）：缺少评分、证据或评审者身份的案例标为 ungraded。
2. **质量分数**（0–10）与关键失败案例数：不得在覆盖率不同的情况下只比较平均分。
3. **R00 运行验证数**（verified/failed/unverified）：它是独立执行证据，不是文章文风评分。
4. **成对偏好**（新版胜/基线胜/平局/未评）：盲评应保留具体理由。
5. **按 primary_rule 汇总**：有助于发现哪些规则有效、哪些规则没有实际增益。

这套工具仅聚合**外部真实执行与独立评分**，不会自动调用 LLM、自动进行主观判分，也不能从文章质量推断用户真的已学会。若要测量真实学习效果，应另做读者前后测/闭卷复述，而不是强制每篇教学文章附题。

## 五、结果质量与失败处理

- 发现错误先对照对应 `failure_mode`；若仅是轻微措辞、教学近似或格式差别，局部扣分或不扣分，而非重写整篇。
- 如两个版本都高分，但盲评有一致明确偏好，检查 Rubric 是否漏掉了理解主干；反过来，如果两版都轻松全分，也需要检查案例是否缺乏判别力。
- 不把触发测试、静态文件验证、真实模型输出、独立评分或用户学习效果混为同一种证据。
- 增加规则前应先证实一个**重复发生、会影响学习**的失败，而不是从个别评分意见直接制造新硬步骤。

**评测目标：验证规则是否减少实际学习失败，而不是验证输出是否像一份规则清单。**
