# Document Intelligence Suite V2.3

V2.3 在 V2.2 的精简架构上增加 **L — Learning**，实现一个入口统一管理三种认知任务。

## 三种模式

- **D — Deep Read V6.1**：原材料中心，忠实理解与压缩。
- **R — Vibe Review V0.9**：判断中心，独立审阅与实质差异。
- **L — System Learning V0.4.3**：学习者中心，`Build Model → Find Gaps → Project to Use`。

## 为什么不把三个 Skill 合成一个大文件

统一管理 ≠ 混合认知任务。

Deep Read 要忠实作者；Review 要能离开作者框架独立判断；Learning 则允许重组材料，形成自己的知识模型。三种目标存在天然张力，强行揉成一个 Prompt 会互相污染。

因此 V2.3 的做法是：

> **一个 Suite / 一个根入口 / 三个内部模块。**

用户只需要保存、安装或维护整个 `document-intelligence-suite-v2.3`，不需要分别管理三个独立 Skill。

## 复合任务

不为每种组合继续新增 Skill：

- D + R：总结并审阅
- D + L：先忠实读懂，再形成自己的理解
- L + R：学习主题，同时评价输入材料
- D + L + R：三路直接读原材料，最后合并

## 使用

以根目录 `SKILL.md` 作为唯一入口。
