# Practice V0.3 — Agent Loop 第一轮演练（已发现结构性缺口，2026-10-11）

> **历史失败案例，非完整现行 Practice 范本。** 本轮只处理一个下游超时重试问题，后来发现其整体知识主干覆盖不足。请结合 [第二轮中文复盘](practice-agent-loop-topology-repair-v0.3.md) 阅读；当前 Practice 的简化方法以 [V0.3 Skill](../skills/practice-v0.3/SKILL.md) 为准。

> **后续审计结论：第一轮不是完整的 Agent Loop Practice；它漏掉最基本的任务理解、是否需要工具、可见工具选择、参数构造等上游因果节点。此前的总体通过判断撤回。修订后的完整决策拓扑见 [第二轮修复报告](practice-agent-loop-topology-repair-v0.3.md)。**

> 类型：**model-self-drill + source inspection + isolated executable probe**。本次没有用户现场作答，不能评估用户的面试能力；没有运行 dsh 真实 API / 应用链，不能宣布真实 Harness E2E 通过。
>
> 旧主干：用户此前学习 Agent Loop，关键关系为 Model Request → tool-call → Harness 受控执行 → tool/result 成为下一步 observation → 新 Model Request。现以 DeepSeek Harness Fork 固定 commit `5badb15009ae1756c3afe0ae0cef1faafc290ccc` 的源码为可核实实现证据。

## 1. 任务与成功标准

情境：一个企业办公 Agent 经用户授权，调用工具将一份贷后检查结论写回银行内部业务系统。操作请求发出后工具层超时，Agent 收不到成功响应。

**本次 Practice 的成功标准不是“能定义 Agent Loop”，而是：在不知道外部操作是否完成时，不误将重试视为安全；能说清各组件知道什么、缺什么证据、如何核验与恢复。**

约束：业务记录不允许重复创建，工具结果日志与业务系统实际记录可能不一致；写入不是简单只读查询。这里的贷后数据和外部系统均为**合成案例**。

## 2. 候选分支排序

| 分支 | 关键问题 | 为什么重要 | 处理 |
|---|---|---|---|
| A. 失去响应后是否可重试 | 外部副作用是否已经完成 | 直接改变重复写入风险、恢复操作与成功判断 | **立即深入** |
| B. Session / Compaction / Resume | 恢复模型上下文是否等于业务步骤恢复 | 影响跨进程、崩溃后的继续执行假设 | 反事实校验 |
| C. 并行 Tool Calls | 并发完成顺序如何映射到结果 | 影响依赖/副作用排序 | 保留为候选 |
| D. “AgentLoop” 名词解释十连问 | 大部分不改变场景中的决定 | 低分辨率记忆测试 | **剔除** |

## 3. 核心质询与示范应答

### Q1：模型发出了 Tool Call，是否说明业务操作已经发生？

**示范应答：否。** Model 输出是结构化调用意图；Harness 需要先承认调用、解析参数、走受控执行流水线，最后才能把结果写入会话。模型有 tool-call 输出、系统持有 tool/call 事件、外部副作用真实发生，是三个不同事实。

**源码核查**：
- [agent.ts#L513-L544](https://github.com/leecolin2023/dsh-intramate/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/core/agent-loop/src/agent.ts#L513-L544)：提交 assistant/message，过滤 tool-call，再交给 executeToolCalls；无 tool-call 则返回 completed。
- [tool-calls.ts#L60-L103](https://github.com/leecolin2023/dsh-intramate/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/core/agent-loop/src/tool-calls.ts#L60-L103)：参数解析与运行组调度。
- [tool-calls.ts#L263-L290](https://github.com/leecolin2023/dsh-intramate/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/core/agent-loop/src/tool-calls.ts#L263-L290)：tool/call、tool/result 记录。

### Q2：既然 Session 中有 Tool Result，为什么还不能确认业务完成？

**示范应答：** 工具日志是 Harness 在其可观察范围内收到/写入的事实。外部银行系统的持久化副作用属于另一边界。即便 Harness 可记录 tool/call 和 tool/result，也不等于它能事务性地同时提交业务系统记录和本地 Session；跨系统消息丢失会产生“真实成功、调用者看到失败”的歧义。

**源码核查**：
- [agent.ts#L320-L355](https://github.com/leecolin2023/dsh-intramate/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/core/agent-loop/src/agent.ts#L320-L355)：执行异常时补记录未回答的 tool result。
- [agent-loop README 的 Failure and cancellation](https://github.com/leecolin2023/dsh-intramate/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/core/agent-loop/README.md)：tool/call 已记录而结果未知可写入 TOOL_OUTCOME_UNKNOWN；未记录调用的恢复路径用 TOOL_NOT_STARTED；这些标记不是对外部副作用的反证。

### Q3（关键条件变化）：写入成功但响应丢失，模型决定自动重试。对吗？

**示范应答：不能直接重试非幂等写入。** 同一超时可以对应：
- H1：调用尚未派发，外部无写入；
- H2：调用执行并已提交，回包丢失；
- H3：调用执行但未提交。

三者观察到的表层错误可能相同，却需要不同动作。应携带稳定业务 `operation_id`，向外部**权威状态源**查询执行结果；无法确证时暂停自动重试或走人工/补偿。若由外部系统支持同一 `operation_id` 的**原子去重+结果回放**，才可以在该明确保证范围内做安全重试。只在 Agent Prompt 中写“不要重复”不是幂等保证。

### Q4（再次挑战）：如果 Session 可恢复，为什么不能从上一步自动续跑？

**示范应答：** 恢复日志、重建模型可见历史，与恢复未完成的外部事务是两种不同保证。session.deriveMessages() 从事件日志构造后续模型请求；它不拥有外部写入的提交事实。流程需要外部幂等协议、对账或补偿才能跨越这个边界。

**源码核查**：[agent.ts#L650-L688](https://github.com/leecolin2023/dsh-intramate/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/core/agent-loop/src/agent.ts#L650-L688) 使用 session.deriveMessages() 构造请求；[architecture.md](https://github.com/leecolin2023/dsh-intramate/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/docs/architecture.md) 说明事件持久化与模型可见历史的边界。

## 4. 已执行的最小对照实验

以 **Python sqlite3 内存数据库**模拟业务写入，不使用真实银行系统，也**不运行 dsh**。实验输入固定为 `op-17`，先提交写入、再模拟确认响应丢失；尝试第二次相同操作。

| 实验阶段 | 存在的业务记录行数 | 观察 |
|---|---:|---|
| 非幂等首次调用，写入成功但 ack 丢失 | 1 | 调用者看到超时，业务已生效 |
| 非幂等重试 | 2 | **实际发生重复写入** |
| 同一操作使用 `op_id` 原子去重，首次 ack 丢失 | 1 | 业务记录只有一条 |
| 相同 `op_id` 再次调用 | 1 | 返回已有结果，不再次插入 |

可复现实验代码：[agent_loop_lost_ack_probe.py](../scripts/probes/agent_loop_lost_ack_probe.py)。在仓库根目录运行：

```bash
python scripts/probes/agent_loop_lost_ack_probe.py
```

输出带有断言校验（对应 1→2 与 1→1），无需额外第三方依赖。

**实际运行结果：** 非幂等 1→2；数据库事务内去重 1→1。该结果支持“ack 丢失 + 非幂等重试可能重复副作用”，但不证明 DSH 现成的工具默认支持业务幂等，也不证明所有数据库/网络时序条件。

最小实现契约：外部写入工具必须携带跨重试保持不变的 `operation_id`；业务提交和去重记录应处于同一原子边界（或目标系统提供等效保证），并提供按 `operation_id` 查询结果的接口。调用方应先校验授权和同一操作参数一致性，避免不同请求误用相同 id。

## 5. 分支诊断与回流

| 发现 | 缺口类型 | 下一动作 |
|---|---|---|
| 不能仅从 tool/result 缺失判断外部是否执行 | 明确了关键边界 | P 已产生可迁移判断 |
| DSH 实际崩溃点是否均按源码注释落成配对错误结果 | **Evidence Gap** | 加入断点 / 崩溃注入，采集 Session log |
| 外部系统有没有 operation_id 去重与按 ID 对账 | **Environment/Contract Gap** | 先审接口、事务、错误码和一致性契约 |
| 若学习者不理解原子事务/幂等产生机制 | **Knowledge Gap** | 新 L 主问题：“回包丢失后如何在不同故障点确保同一业务操作至多提交一次？”启动新 L 时先独立 D/R |
| 多工具并行对结果序的影响 | 暂时非阻塞分支 | 进入下轮场景，不抢占当前主问题 |

## 6. 质量检查（修订后判断）

- **Topology Coverage — FAIL**：只深入下游超时重试，漏掉理解目标、行动必要性、工具可见性、工具选择与参数构造；不能声称完成 Agent Loop 全链路练习。
- Task Fidelity — PARTIAL：单一异常情境的自演练有效，但不满足完整实践范围。
- Branch Value — PASS：副作用是否提交直接改变重试策略；剔除了低价值定义题。
- Challenge Discrimination — PASS：只改变“确认响应是否丢失/有无外部去重”，出现可观察不同结果。
- Evidence Honesty — PASS：源码证据、SQLite 实测、合成银行场景和未测的 dsh 运行严格分开。
- Transfer — PASS（模型示范层面）：给出操作标识、外部核验、稳定幂等契约等跨系统原则。
- Repair Routing — PASS：区分 Evidence Gap、Knowledge Gap、Contract Gap。
- **Real User Interview Performance — NOT TESTED**：用户没有亲自作答。
- **DeepSeek Harness end-to-end failure injection — NOT VERIFIED**：当前未运行 dsh 模型与外部 Tool。
- **Controlled old/new Skill behavioral A/B — NOT RUN**：本次增加了回归用例和真实问题检验，但不能声称 Skill 行为统计改进。

## 7. 下一步可验证实验

在独立测试环境准备一个最小 Tool：先对外部 sqlite/服务完成写入，再主动丢弃响应；运行真实 dsh agent 一次，采集 Session 的 `assistant/message`、`tool/call`、`tool/result`、`step/end`、后续模型请求快照和外部表计数。分别测试 **超时前未派发 / 已提交未回包 / 工具正常结果**，比较错误标记、模型推断和外部事实是否一致；随后接入稳定 `operation_id` 的外部幂等实现再测。只有这一步运行并保存记录，才可将 Harness E2E 标记为 verified。

**修正结论：** 本轮仅验证一个下游异常分支，**没有证明 Practice 能系统发现重要分支**；从目标到工具选择的基础机制遗漏必须优先补齐。见 [拓扑覆盖修复](practice-agent-loop-topology-repair-v0.3.md)。