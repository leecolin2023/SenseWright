# Practice V0.3 — Agent Loop branch-stress fixture

## Known knowledge model (from prior D/R/L)
Agent can take action only if model tool-call intent is mapped to registered tools, passed through execution, and the observation is made available on a subsequent model request. Distinguish model vs Harness action, step vs turn vs session, and run-state vs durable history.

## Anchored implementation under examination
Fork: leecolin2023/dsh-intramate at commit 5badb15009ae1756c3afe0ae0cef1faafc290ccc.
- packages/core/agent-loop/src/agent.ts lines 398–545: prepare, request, model stream, assistant/message commit, extract tool-call, call executeToolCalls.
- packages/core/agent-loop/src/tool-calls.ts lines 60–103, 134–171, 254–290: parse arguments, schedule, append tool/call and tool/result, preserve ordered results.
- packages/core/agent-loop/src/agent.ts lines 323–355: failed-step tool-result recovery.
- docs/architecture.md and packages/core/agent-loop/README.md: session append-only event log, deriveMessages; tool-result recovery code distinction (including TOOL_OUTCOME_UNKNOWN for a recorded call with missing outcome, and TOOL_NOT_STARTED where no call was recorded). Docs are source evidence, not executed probes.

## Scenario
An enterprise Agent calls a tool to write a bank post-loan inspection report. The external system commits the write, but the response is lost. The Agent or operator sees a timeout and considers retrying the call.

This is a deliberately **synthetic scenario**. It does not claim actual banking-system integration, access to production, or an observed DeepSeek Harness failure.

## Required competing hypotheses
H1. Response timed out before dispatch; write did not happen.
H2. Dispatch happened and external side-effect committed, but acknowledgement was lost.
H3. Write failed after dispatch, no commit.

A timeout/error alone does not decide among these. A stable operation identity plus authoritative external reconciliation evidence can.

## Branches worth exploring
1. Execution outcome ambiguous: Harness durable tool history vs actual external effect.
2. Compaction and resume: reconstruction of model-visible history vs transactional recovery.
3. Cross-tool overlap: multiple parallel-safe tool calls and exclusive barriers.

## Low-value distractor
Ask ten definitions of AgentLoop, tool, AgentSession, and schema without any changed outcome. Pure recall doesn't verify situated transfer.

## Evaluation scope
Assess whether the answer differentiates source inspection from a real runtime test; does not infer exactly-once from session replay; prioritizes one consequential branch; and routes unresolved new knowledge to L only when genuinely needed.
