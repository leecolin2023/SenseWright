# Document Intelligence Suite V2.3.1

Document Intelligence Suite 用一个统一入口管理三种彼此独立的认知任务：

- **D — Deep Read V6.1**：source-centered，忠实理解与压缩原材料。
- **R — Vibe Review V0.9**：judgment-centered，独立审阅材料是否成立、是否足以支持决策。
- **L — System Learning V0.4.3**：learner-centered，建立可复用知识模型并投影到下一步使用。

核心原则：

> **统一管理，不融合认知任务。Router 只判断“走哪条路”，具体认知工作由子 Skill 完成。**

## 为什么不把三个 Skill 合成一个大文件

Deep Read 要忠实作者；Review 要能离开作者框架独立判断；Learning 则允许重组材料形成自己的知识模型。三种目标存在天然张力，强行揉成一个 Prompt 容易相互污染。

因此项目采用：

> **一个 Suite / 一个根入口 / 三个内部 Skill。**

复合任务不新增 Skill 类型，而是组合已有能力：D + R、D + L、L + R、D + L + R。多路执行默认直接读取 Raw Source，不把上一路的压缩输出作为下一路的唯一输入。

## Agent Skills 标准兼容

V2.3.1 将所有 `SKILL.md` 的 YAML frontmatter 收敛到跨工具最小公共集：

~~~yaml
---
name: skill-name
description: What the skill does and when it should be used.
---
~~~

- `name` 是稳定的 Skill 标识。
- `description` 同时描述能力与触发场景，用于 Skill discovery / triggering。
- 版本号不再放进 frontmatter，而由标题、目录与 `CHANGELOG.md` 管理。
- 不再使用自定义 `summary` 字段，减少不同 Agent Runtime 对 metadata 处理不一致的风险。

本地校验：

~~~bash
python scripts/validate_skills.py
~~~

## Evaluation Workflow V0.1

从 V2.3.1 开始，评测成为 Skill 演进的一等公民：

~~~text
test cases
   ↓
with-skill  ───────┐
                   ├─> assertions + human review
baseline / old-skill┘
   ↓
grading + timing
   ↓
benchmark
   ↓
failure analysis
   ↓
next iteration
~~~

V0.1 遵循五个原则：

1. 同一批 case 同时跑 with-skill 与 baseline。
2. 对既有 Skill 的改进，优先使用“改动前版本”作为 baseline。
3. 客观可验证结果使用 assertions；主观质量保留 human review。
4. 保存 token 与 duration，避免只看质量不看成本。
5. 新版本回放历史 case，形成 regression。

首个 old-skill baseline 固定为 `ffdb60e1f27ae99011d18c29c683dc747cec64f1`。

### 评测资产

~~~text
evals/
├── README.md
├── evals.json
├── triggering.json
├── baselines.json
└── fixtures/

scripts/
├── validate_skills.py
├── validate_evals.py
├── init_eval_workspace.py
└── aggregate_benchmark.py
~~~

### 开始一次迭代

~~~bash
python scripts/validate_skills.py
python scripts/validate_evals.py
python scripts/init_eval_workspace.py --iteration 1 --baseline old_skill
~~~

完成两组运行并保存输出、transcript、grading 与 timing 后：

~~~bash
python scripts/aggregate_benchmark.py .eval-workspace/iteration-1
~~~

详细约定见 `evals/README.md`。

## 使用

以根目录 `SKILL.md` 作为唯一入口。子 Skill 位于 `skills/`，普通用户无需单独维护三个入口。
