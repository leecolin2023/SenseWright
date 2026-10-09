# Mandatory Deep Read + Review Preflight for Learning V0.6.1

## Normative pipeline

~~~text
Current Raw Input
     ├─ D: independent, faithful source reconstruction
     └─ R: independent, source-facing Review
              [both complete]
                    |
                    v
            L: grounded problem chain
               + mechanism + stabilization
~~~

D and R must run on the **same current raw user input/source independently**. D never reads R, R never reads D. Both must complete before L begins, and both artifacts must be made available to L. Previously cached output never substitutes for this run.

## Mandatory execution, selective incorporation

- D exposes the source's actual claims, cognitive topology, necessary examples, and analogies, with original provenance.
- R checks the raw material atomically then selectively reports substantive defects, alternative interpretations, unsupported assumptions, and evidence limits.
- L consumes both, but treats these as **scaffolds, not evidence**: Return to Raw Input, build a fresh object-oriented problem chain, test the smallest necessary mechanism, and mark derived claims and unknowns.
- R's independent source audit is **not the same** as L's internal Boundary & Evidence Stabilization Gate.
- Default delivery is one coherent L response; separate D/R reports are for explicit user requests.

## No-document case

Input may be just a conceptual question, without a source document. D faithfully frames the supplied question and context; R examines material premises and ambiguities, and may find no issue. D/R can be brief but never skipped. Do not fabricate a missing source, author, citation, or criticism.

## Boundary with P

P-only implementation tasks keep their existing direct route; however a task routed to L (including P→L gap repair) must use a **fresh D/R** before L. Optional historical P references do not count as a D/R pass.

## Verification requirements

Static Eval metadata uses the prefix ["D","R","L"] for each L task and a mandatory preflight contract. This **does not ensure** independent model invocations, source isolation, or barrier enforcement; such guarantees require the execution host to log separate stage IDs, raw-input identity, context boundaries, completion times, and read dependencies. Without inspectable execution records, label independence/barrier checks **unverified**, not PASS.

## Anti-patterns

1. Performing only D, or only R, because the other seems unneeded.
2. Reading R through D's summary instead of directly auditing the source.
3. Treating D or R statements as evidence rather than source-facing scaffolds.
4. Concatenating D and R as a final L result.
5. Calling preflight complete merely because the final answer has three headings.
6. Fabricating a document or flaws when the user supplied only a short question.
