# Agent Loop — Raw material for Practice regression

## Existing Learning trunk

A model can issue a structured tool call. Harness maps it to registered capabilities, performs guarded execution, records the result, and supplies the result when constructing a subsequent model request. The prior Learning focused on the action/observation loop; it did not separately settle every design choice.

## Source anchors

Implementation: `leecolin2023/dsh-intramate`, commit `5badb15009ae1756c3afe0ae0cef1faafc290ccc`.

- `packages/core/agent-loop/src/agent.ts`: `preStep` (around 268–289), `step` (398–545), `buildRequest` (around 598–689).
- `packages/core/tools/README.md`: registering tool schemas, scope-specific available tools, native/PTC tool presentation and policy.
- `packages/core/system-prompt/README.md`: prompt and permitted tool schemas assembled per step.
- `packages/core/agent-loop/src/tool-calls.ts`: execution scheduling and durable call/result recording.
- `packages/core/agent-loop/README.md`: failure recovery and Session history.

These are **source reference locations**, not evidence of a live model-selection experiment.

## Independent synthetic situations

**A — Task with potential tool choices.** A user asks: “核对这个客户最新的授信批复与已签合同是否一致，列出差异。” Fictional available tool definitions:
- `approval_search(customer_id, as_of)`: locate a currently approved decision/version;
- `approval_archive(customer_id)`: retrieve historical approval versions;
- `contract_read(contract_id)`: fetch identified contract content;
- `business_write(record_id, payload)`: update a business record.

The request gives no customer ID, contract ID or date context. These four functions are illustrative only, not claimed to be registered tools in the fork.

**B — External side effect uncertainty.** A different task asks the Agent to save a document. The external save might have committed before the tool response timed out; no actual production incident is supplied.

The task is to practice reasoning with these inputs, not to assume a particular tool choice, retry strategy or answer in advance.
