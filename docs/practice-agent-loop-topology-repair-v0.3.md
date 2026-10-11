# Agent Loop Practice V0.3 — Decision Topology Audit & Branch Drill, corrected pass (2026-10-11)

> **Method:** source inspection + model-self-drill (not user interview) + illustrative case variations. No actual DeepSeek Harness model/tool-choice test was run. The prior [round-one write-up](practice-agent-loop-drill-v0.3.md) captured one real downstream issue but **FAILED topology coverage**; its former overall PASS is withdrawn. This second pass corrects the discovery method rather than adding another random interview question.

## 1. The true failure was upstream of the selected branch

The old main chain, `Model Request → Tool Call → Execution → Observation → Next Request`, describes the **execution transport**, not the entire causal decision process. Its first arrow hides *why* a tool call is warranted and *which* tool is chosen. That omission invalidates a "comprehensive Agent Loop drill" even if a retry failure investigation is useful.

**Distinction:** a missing reason for an essential action is an unfinished **main-chain mechanism**, not a low-ranked optional side branch. First map those gaps, then select branches for deeper rehearsal.

## 2. Causal topology — main decisions and current evidence

| Decision / transition | Essential question and possible branch | Evidence / status |
|---|---|---|
| User goal → operational task | What does the user want, what counts as success, and are object/time/scope resolved? | General model reasoning; **not previously investigated** |
| Task → need for action | Can I answer from context or must I read/write/ask? What counts as justified tool use? | Model behavior, **behavior not tested** |
| Need → available capabilities | Where do discoverable tools come from? Which names/descriptions/schemas are visible? | **Source-inspected** ToolRuntime and SystemPrompt |
| Available capabilities → tool choice | Why pick tool A rather than similar B or none? Is there an explicit classifier? | **Source-inspected interface; actual model choice not tested** |
| Selected tool → grounded arguments | Where do IDs, paths, date range and object references come from? What if missing? | Tool Schema and argument validation **source-inspected**; model grounding not tested |
| Single action → multi-step plan | Which call precedes the next? Can parallel calls alter business outcomes? | AgentLoop and tool-calls scheduling **source-inspected** |
| Intent → permission / approval | Visible does not equal authorized; what blocks a forbidden action? | **Source-inspected** registry restriction and policy pipeline |
| Dispatch → external effect | When is a call logged, and when is actual external state changed? | Source-inspected; real external integration **unverified** |
| Tool result → next decision | Which result is model-visible, how does it influence the next action? | **Source-inspected** session/deriveMessages and event flow |
| Continue / terminate → task success | No tool-call means step completed, but does that mean user goal achieved? | **Source-inspected** loop condition; task-quality result untested |
| Crash / retry / continuation | Can logs reconstruct model history yet lack external effect evidence? | Source-inspected; isolated lost-ack probe is separate, **not DSH E2E** |

**Structural review result:** the previous Practice started with dispatch and failure; it omitted the first *five* decisions, including the essential "why this tool?" bridge. A single downstream retry probe cannot compensate.

## 3. Deep branch A — intent understanding vs tool selection

### Interview challenge 1: Who recognizes intent and selects a tool?

**Model demonstration (not a measured model answer):** Do not presuppose a separate classifier. In DSH **native** mode, tool plugins register `name`, `description` and `parameters` in ToolRuntime. SystemPrompt assembles the permitted ToolSchemas for the current agent step; AgentLoop constructs a model request with history and those schemas. The model can emit a structured `tool-call`; the Harness **interprets, validates and dispatches** it. The last part is deterministic execution of the emitted intention, not independent proof that it was the right choice.

**Verified implementation anchors:**
- [tools/README.md#register-a-tool](https://github.com/leecolin2023/dsh-intramate/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/core/tools/README.md): model-facing name/description/parameters; registration, masks and validation.
- [system-prompt/README.md](https://github.com/leecolin2023/dsh-intramate/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/core/system-prompt/README.md): schemas assembled with prompt, scoped contributors.
- [agent.ts#L266-L289](https://github.com/leecolin2023/dsh-intramate/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/core/agent-loop/src/agent.ts#L266-L289): `preStep` assembles the context.
- [agent.ts#L650-L688](https://github.com/leecolin2023/dsh-intramate/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/core/agent-loop/src/agent.ts#L650-L688): `buildRequest` passes `messages`, `tools` and tool history into the model request.
- [agent.ts#L530-L544](https://github.com/leecolin2023/dsh-intramate/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/core/agent-loop/src/agent.ts#L530-L544): extract `tool-call` from model output; invoke `executeToolCalls`; without a tool call normal step ends.
- [tools/README.md#configure-the-presentation-mode](https://github.com/leecolin2023/dsh-intramate/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/core/tools/README.md): `native`, `ptc`, `both` choices; in `ptc` model sees `run_code` and generated SDK rather than every end-tool as direct callable schema.

**Important qualification:** this shows the model-facing surface and observed code path, **not** the internal features or classification process in model weights; neither does it prove there are no plugins or upstream routers in arbitrary compositions.

### Interview challenge 2: Same user request, different available tools — what changes?

**Synthetic case:** User says “请核对某客户最新授信批复是否与已签合同一致，给出差异报告。” Hypothetical permitted tool set:

- `search_approval(customer_id, as_of)` — find signed-off approval/version.
- `read_contract(contract_id)` — retrieve contract content.
- `compare_documents(approval, contract)` — produce differences.
- `write_business_result(...)` — mutates production business record, **not implied by this request**.

**Reasoned action chain:** resolve customer and contract identifiers / date context (or request missing disambiguation); search authoritative latest approval; retrieve appropriate contract; compare conditions with traceable clauses; present differences with uncertainty and references. Do **not** write production records without an authorized user goal. Selection must be explained by task goal, visible affordance, argument requirements and permission, not simply matching the verb “核对” to a named tool.

This scenario is a **thought experiment**. No model selection trace, model scores or real bank record is claimed.

### Interview challenge 3: What if the tools overlap or the best tool is absent?

Change **one** condition at a time:
1. `compare_documents` absent but two read tools remain. The model may be able to perform bounded comparison from retrieved inputs, ask for specialized execution, or refuse a reliable comparison depending on context and constraints. Do not fabricate nonexistent tool calls.
2. A second `search_approval_archive` advertises only historical versions. "最新" and approval status must disambiguate selection; not just similar name matching.
3. `search_approval` registered but masked from this agent. It is not a permitted tool to choose. A prompt cannot override an actual registry/policy gate.
4. Request is "你知道授信批复是什么吗？" There need not be any tool call; overusing tools is also a selection failure.
5. `ptc` mode active: direct tool-name call changes to `run_code` plus generated SDK; the user's goal is unchanged but tool presentation and dispatch path change.

**What is NOT yet known:** which prompt/schema choices actually raise tool-selection accuracy or reduce hallucination in this specific model/Harness combination. That requires controlled model runs; source inspection alone cannot answer.

## 4. Remaining high-value branch research queue (not synonyms)

| Branch line | Fundamental question | What could change | Current disposition |
|---|---|---|---|
| Goal/task disambiguation | When should the Agent clarify rather than assume an entity, date, or permission? | Wrong task entirely | **High** |
| Tool-need decision | Why call any tool instead of answering directly? | Unnecessary cost vs unverifiable output | **High** |
| Tool selection & discovery | How do descriptions, visible set, semantic overlap, tool-count and PTC change selection? | Wrong or missing action | **High; illustrated above** |
| Argument grounding | How to bind exact ID, file, scope and date without inventing them? | Correct tool, wrong customer | **High** |
| Planning and dependencies | How to know which tool is needed first, and whether results support the next step? | Incomplete/incorrect chain | **High** |
| Permission & trust | Is a visible tool actually authorized; can retrieved text instruct the Agent to misuse it? | Security boundary breach | **High** |
| Model/tool interface | What does the model emit, what does the adapter parse, what does Harness validate? | Invalid-call diagnosis | **Source-inspected, more tests possible** |
| Feedback & stopping | Is `completed` a model step status or proof the user's goal was met? | False-success report | **High** |
| State and compaction | What survives a turn/session/restart, and what is model-visible? | Lost context/repeated work | **Medium** |
| Parallel scheduling | When are parallel calls safe and what order are results committed? | Dependence/race effects | **Medium** |
| External uncertain side effect | What if a write succeeded but response vanished? | Duplicate action, incorrect retry | **Already rehearsed as one downstream branch** |

**No global 1–3 topic limit:** that shortcut in Practice V0.3 was wrong for a requested full drill. Breadth-first discovery and prerequisite coverage precede deep dives.

## 5. Evidence-oriented practice / acceptance

We can inspect the **source** to establish tool projection, model request construction, emission extraction, schema validation and execution hooks. To verify **selection quality**, run a matched suite using the actual DSH model adapter:

- Construct a small controlled set of tasks: answer-only, single-tool, overlapping tools, multi-step, missing tool, unauthorized tool, ambiguous customer/date.
- Freeze model, temperature, system instruction, task inputs; vary **only one** of description, schema detail, candidate count, permission mask, or `native` vs `ptc` per comparison (mode change may affect more than one dimension; report that confounding explicitly).
- Save tool schema list **actually visible** at each step, model output `tool-call` names and arguments, guard decisions, result sequence, and final correctness as judged against an independently authored reference.
- Grade **need-to-call decision**, **tool choice**, **argument accuracy**, **permission compliance**, **plan completeness**, **final task correctness**, plus unnecessary-call rate and cost. Do not use apparent success or self-reported confidence as the only metric.
- Report evidence and failures before changing prompts/rules. Tool choice cannot be proven by a standalone SQLite retry test.

This model-selection suite is **specified but not executed**. The earlier lost-ack SQLite study validates only the separate retry side-effect mechanism, not any tool decision quality.

## 6. Practice → Learning diagnosis

1. **Primary mechanism gap / Learning candidate:** "Absent a dedicated intent classifier, by what mechanism does an LLM translate user goals and a changing schema-defined capability set into a tool-call or no-call decision, and how can we discriminate alternative explanations with controlled evidence?"
2. **Evidence gap / run experiment:** On DSH with a specified model, measure tool-choice changes under controlled schema descriptions, visible-set restrictions, and ambiguous tasks.
3. **Application gap / continue Practice:** Given actual results, design tool descriptions, candidate disclosure, permission routing and clarifying behavior for the bank workflow.
4. **Previously selected failure branch:** Lost response after external write is still valuable, but **downstream**, not a sufficient first or sole branch.

A new formal Learning on the primary gap requires new independent D/R on the chosen raw input; this Practice does not claim to have performed that new L.

## 7. Honest stabilization verdict

- **Round 1 (original write-up): FAIL — Topology Coverage**: omitted tool-need/choice/argument formation before dispatch.
- **Round 2 (this corrected source-grounded drill): PASS — structural discovery and explicit evidence boundaries**, with detailed exemplary branch and a non-duplicative queue.
- **Real tool-selection model evaluation: NOT TESTED.**
- **User interview capability: NOT TESTED.**
- **Controlled prior/new Practice behavioral A/B: NOT TESTED.**
- **True dsh E2E: NOT TESTED.**

**Takeaway:** the root correction is **causal topology audit before branch prioritization**, not “add another intent-recognition interview question.”