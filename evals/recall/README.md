# Deep Read · 定向回查实验（Eval Recall V0.1）

## 定位

此处不是第三条 Deep Read 规则，也不是把每次阅读都变成多次工具调用。**D02** 仍负责保留理解桥梁，**D03** 仍负责按目标选择压缩边界；回查是一项按需使用的修复操作。

与现有 `evals/evals.json` 的 80 个任务案例分开，保留原有测试 ID、Skill 路由、Learning Eval V0.3 与盲评脚本不变。这里新增的是**固定初稿的增量修复实验**，用于回答：什么时候值得回查？回查是否改善阅读后的理解？是否会损害原本已足够好的文章？

## 实验对象

`cases.json` 中有 6 组可追踪的合成案例，均复用现有 Raw Source，而不修改既有 fixture：

| 场景 | 规则 | 压缩模式 | 候选是否应回查 |
|---|---|---|---|
| 公告概括/核验对照只剩抽象标签 | D02 | 认知提炼 | repair |
| 公告两任务及其行动差异已经解释充分 | D02 | 认知提炼 | skip |
| 试点会议纪要完整覆盖型漏掉预算采购 | D03 | 完整覆盖 | repair |
| 五项试点议题及行动已能追踪 | D03 | 完整覆盖 | skip |
| 认知提炼稿虽保留结论，却没有解释场景 | D03 | 认知提炼 | repair |
| 认知提炼稿已保留关键具体场景与约束 | D03 | 认知提炼 | skip |

两类失败分别测：**不该省的被省了**，以及**不该加的被加了**。尤其是后者，防止模型为了“完成回查流程”而重复原文、稀释已有理解。

这些案例由测试者设计，`expected_gate` 不是模型运行结果。真实《宋徽宗联金灭辽》的上轮测试发现 6 处解释偏薄，但由同一分析者完成修复和自查，不能将其视为独立盲测成功，也不直接向公开仓库上传用户提供的视频全文。

## 三个互相独立的评价对象

**一、回查决策（是否必要）。** 候选可以报告 `decision=repair|skip`。若 `repair`，在 `trace.json` 中记录实际查看的**原文子串**、要修复的段落和理由；如果 `skip`，候选正文应与初稿相同。没有 Trace 是 **unverified**，不是默认成功或失败。自报查阅过原文并不证明执行工具回查，真实运行可另保留日志。

**二、读者理解（是否真的更好）。** 盲读者只能阅读匿名 A/B 成品及事先固定的理解问题，不看 Raw Source、期望答案、修复标记或来源片段。独立评审再依据 Raw Source、事先固定的参考点和盲读者实际回答逐题给 0/1/2 分：

- 0：理解错误或未能回答；
- 1：知道结论，但缺乏能解释它的主要桥梁；
- 2：能重建主要因果、比较关系及必要场景。

分别报告控制版与修复版的平均分，**按 case 配对计算增益**。盲读的回答不能由修复者自己生成并自己给分。

**三、成本与副作用。** 记录修复是否增加无用文字、改坏原有正确段落，额外 token 与时间（若运行环境能提供）。比较 repair/skip 的实际决定和预置的必要性分类，分开观察**有效修复、漏回查、无谓回查、原稿退化**。没有成本日志就标未知，不推算虚假成本。

## 运行方法

**1. 静态检查和初始化：**

```bash
python scripts/validate_recall_evals.py
python scripts/prepare_recall_eval.py --iteration 1
```

每个案例会产生：

```text
.eval-recall-workspace/iteration-1/<case-id>/
  input/
    source.md
    first_draft.md
    generator_packet.json       # 生成方只能获取 input/
  control/response.md           # 固定初稿，作为无修复对照
  targeted_recall/
    trace.template.json
    response.md                 # 生成方实际提交；初始化时不存在
    trace.json                  # 如有实际执行记录，另行提交
  judge_only/reference.json    # 禁止交给生成方/盲读者
  pairwise/
    assignment.json             # 禁止交给盲读者
    vote.template.json
```

**2. 同一冻结初稿的定向修复：** 向被测模型提供 `input/source.md`、`input/first_draft.md`、`input/generator_packet.json` 和当前 D02/D03 Skill；不得提供 `judge_only/`。将产物保存为 `targeted_recall/response.md`，真实回查信息写入 `trace.json`。若判定无需回查，正文保持初稿不变。

**3. 准备匿名阅读：**

```bash
python scripts/prepare_recall_eval.py --iteration 1 --prepare-pairwise
```

在候选回答存在时才生成 `pairwise/A.md`、`B.md`、`reader_questions.json`、`A.reader_answers.template.json`、`B.reader_answers.template.json` 和 `grading.template.json`。盲读者分别读 A/B 并提交 `A.reader_answers.json`、`B.reader_answers.json`；`reader` 填 `id`、`kind=human|model`、`blind_to_variant=true`、`source_blind=true`。

**4. 独立评分：** 给另一个评审者 Raw Source、`judge_only/reference.json`、匿名的阅读回答及评分模板；评审者根据来源支持的解释而非机械关键词命中给每题 0/1/2 分，提交 `pairwise/grading.json`。其中 `reviewer` 记录 `id`、`kind`、`independent=true`、`blind_to_variant=true`；必须与两位盲读者的 ID 不同。每个评分附真实回答依据。

**5. 汇总：**

```bash
python scripts/aggregate_recall_eval.py .eval-recall-workspace/iteration-1
```

输出 `recall-benchmark.json` 和 `recall-benchmark.md`。未生成、未盲读或没有合法独立评分的案例，一律标 **ungraded**。自报回查来源不等于真实工具 Trace，聚合结果明确区分 `declared_...` 和真实理解得分。

## 与常规 Deep Read Eval 的关系

- 原有 Deep Read Eval V0.3：测试从 Raw Source **初次生成**的质量，比较 Skill 和冻结基线。
- 本套 Recall Eval V0.1：**固定同一份已生成初稿**，把“是否进行定向回查并局部修复”作为唯一主要变量，与保留初稿的控制版本对比。
- 以后可增加一个完整端到端实验：同条件多次生成初稿→随机分配是否允许回查→独立盲读；切勿把一次修复结果当成模型的稳定增益。
- 如果原稿完整可读，允许模型依常规方式查看它；本机制重点不是强制 `retrieve` 工具，而是**仅针对真实缺口、定位真实原文、进行局部修复**。

### 不应从本实验得出的结论

静态用例通过不证明 Skill 有效，合成缺口被修复不证明它会在真实长文中自动发现，单个模型自查不等于独立盲读。尤其不要把“更多原文片段被复制”“文章变长”“所有初稿都触发回查”当作成功指标。
