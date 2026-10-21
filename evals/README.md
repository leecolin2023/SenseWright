# SenseWright 评测指南

> **现行评测入口 · Eval V0.1**。本文介绍目前如何检查与评估四条 Skill；各阶段历史设计、旧版技术细节和案例变化保留于 [评测历史记录](HISTORY.md)。**评测数据不是运行时规则**。

## 一、为什么要评测

四条 Skill 很容易出现“输出写得更长，却没有变得更好”的问题。真正关心的是：

- **D：** 是否完整而忠实地恢复材料的认知结构；压缩是否符合用户意图？
- **R：** 是否审过全部重要语义单元，而非提前只挑重点？判断是否独立且合理？
- **L：** 是否解释真实机制，案例能否支撑它声称解释的主问题？是否保持证据边界？
- **P：** 是否找到了已有知识主干遗漏的必要前提和独立研究枝干？是否对重点问题真正深入，而非凑题数或固定工程流程？

评测既要发现真实改进，也要防止为个别案例不断向通用 Skill 加特殊规则。

## 二、评测文件和当前范围

| 文件或目录 | 用途 |
| --- | --- |
| [evals.json](evals.json) | 任务案例，包含 `prompt`、`files`、`expected_route`、`expected_output` 与 `assertions` |
| [triggering.json](triggering.json) | 正例及相邻负例，用于检查是否错误触发 Skill |
| [fixtures/](fixtures/) | 原材料和情景输入；不是对所有任务生效的指令 |
| [baselines.json](baselines.json) | 经过冻结的旧版本对照基线 |
| [HISTORY.md](HISTORY.md) | 旧版方法、案例来源和评测方案演变 |
| [../scripts/](../scripts/) | 基础验证、初始化工作区、汇总统计 |

当前 `main` 数据含 **75 个任务案例和 63 个触发样例**。其中 **#59–63** 对应 Learning 问题—证据对齐回归，**#64–70** 对应 Practice 的分支发现等回归，**#71–75** 对应故障问题定义、诊断分流与非故障场景的防回归。精确数量以 JSON 和脚本结果为准，避免手工维护多个数字来源。

### 评价时不要混淆输入与答案

- `files` 只提供待阅读材料，不应直接泄露预期问题清单；
- `expected_output` / `assertions` 是评测合同，不应回填成模型生成时的提示词；
- `gold_review_units` 可记录 Review 的覆盖目标（字段 `id` 与 `description`），不能误读成只需检查这些单元；
- `reference_context` 可以模拟已有学习记录，但不能冒充本轮 D/R 已独立执行。

## 三、结构检查

在项目根目录执行：

```bash
python scripts/validate_skills.py
python scripts/validate_evals.py
```

对应 GitHub Actions 的 [CI 定义](../.github/workflows/skill-ci.yml) 在推送和 PR 时执行上述两条脚本。

**通过只表示：** Skill 元数据、任务字段、部分路由约束、测试素材引用和正负触发样例结构符合检查规则。

**不代表：** 模型真正遵守了这些方法、Learning 的 D/R 在独立上下文运行、案例质量提升，或任何实际工具/业务系统的端到端执行成功。

## 四、怎样开展行为对照

选择待评版本与 [冻结基线](baselines.json)，尽量固定模型、参数、原始输入、宿主能力、环境和评审标准；不要把数天后不同模型的输出硬当作有效 A/B。

### 1. 生成本地工作区

```bash
python scripts/init_eval_workspace.py --iteration 1 --baseline old_skill
```

脚本将根据全部任务案例建立 `.eval-workspace/iteration-1/`、`manifest.json`、每项 `eval_metadata.json`，以及 `with_skill/` 和基线对应的输出目录。

**注意：该脚本只生成评测目录与清单，不会自动调用模型、生成回答或评分。** 所有案例初始化和逐例运行是两个不同动作。

### 2. 实际运行并留下证据

对同一案例分别在新旧 Skill 条件下运行，并保存至少：

```text
iteration-1/
  <案例名称>/
    eval_metadata.json
    with_skill/
      outputs/response.md
      transcript.md       # 有记录才保存
      grading.json        # 对照断言给出证据
      timing.json         # Runtime 能提供才记录
    old_skill/
      outputs/response.md
      grading.json
      timing.json
```

`grading.json` 中 `expectations` 是包含 `text`、`passed`、`evidence` 等信息的数组。没有充分证据就不应填 `passed: true`。耗时和 Token 用量不能靠估算补齐。

### 3. 汇总结果

```bash
python scripts/aggregate_benchmark.py .eval-workspace/iteration-1
```

当逐项评分与测量文件已经存在时，脚本生成 `benchmark.json` 和 `benchmark.md`，汇总断言通过率、Token/耗时统计（有数据时）及逐案例表现。

**不要在空工作区运行后把缺失的评分误读成“全部失败”，也不要把自动汇总误认为脚本已经检查过语义正确性。**

### 4. 独立人工复核

至少抽查改变判断的案例、失败案例和成本显著变化案例：

- 哪个版本更忠实、更全面、更能支持用户当前目标？
- 哪些差异只是篇幅增长、术语增加或格式美化？
- 是否新增了隐含的硬步骤和领域过拟合？
- 模型“解释自己做了什么”能否被运行记录证实？
- 是否存在两版都通过、但断言本身太浅而没有判别力的情况？

只有在**可比环境 + 真实输出 + 评分证据 + 独立复核**具备时，才适合讨论实际行为改进。

## 五、四条 Skill 的专项回归关注点

| Skill | 必须防止的回归 |
| --- | --- |
| D · Deep Read V6.4 | 将 Coverage-Preserving 做成逐字复述；或 Cognitive-Synthesis 压掉必要解释；混入 R 的独立评判 |
| R · Vibe Review V0.10 | 在原子覆盖前先筛重要性；遗漏表格、例外、数字、责任转换；把所有小问题都堆成最终报告 |
| L · System Learning V0.6.2 | 没有本轮 D/R 前置；把解释例子当作主问题的因果验证；不必要地固化领域模型或阶段 |
| P · Practice V0.3 | 只挑一个下游异常，漏掉上游必需机制；将含糊反馈直接认定为某个根因；只有排查清单而没有可区分的证据；默认工程施工或给未答题用户评分 |

Learning 的回归还需要核实 `expected_route` 使用 **D、R、L** 顺序和 `learning_preflight` 的合同；但这只验证元数据，不能代替宿主调用 Trace。

## 六、结果说明方式

每份评测报告应当明确写清：

1. **评测对象与基线**：具体 Git 提交、Skill 版本和模型配置；
2. **样本与任务**：真实材料、合成材料、样本量及限制；
3. **证据类型**：静态验证 / 模型对照 / 人工审阅 / 实际执行；
4. **发现与失败**：指出具体案例，不只报总分；
5. **结论边界**：哪些结果尚不能推广或仍未验证。

历史详解和旧案例映射见 [评测历史记录](HISTORY.md)，方法总体边界见 [整体架构与边界](../docs/architecture.md)。