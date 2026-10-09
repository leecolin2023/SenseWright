# Learning V0.6.0 — IntraMate Problem-chain Method Transfer

Source: [IntraMate learning method](https://github.com/leecolin2023/IntraMate/blob/main/Architecture/method/00-learning-method.md). Worked examples: [Agent Runtime](https://github.com/leecolin2023/IntraMate/blob/main/Architecture/learning/01-agent-runtime/D-deep-read.md), [Work Agent](https://github.com/leecolin2023/IntraMate/blob/main/Architecture/learning/02-work-agent/D-deep-read.md).

## Why transfer to L instead of rewriting D

IntraMate's method was developed while writing documents labeled Deep Read. But its defining operation — discovering one necessary concept after another from failures in the current explanation — is **learner-centered knowledge construction**, which belongs to SenseWright's L. SenseWright D must remain source-centered: it preserves the author's actual cognitive topology, not force-rewrite source materials into an externally preferred learning chain.

## What is reused

| IntraMate | SenseWright L V0.6.0 |
|---|---|
| Problem First | Start from a grounded, observable problem |
| Mechanism Before Framework | Derive necessary behavior, then name concepts |
| Existing mechanism → failure → new mechanism | Problem Chain within Build Model |
| Knowledge Stable ≠ Implementation Ready | Maintain L→P boundary |
| Problem Knowledge / Native Framework Evidence | Generalize to knowledge / implementation evidence / decision |
| Problem-chain Review | Built-in causal progression Gate |
| Concept First-Appearance Audit | Built-in nomenclature Gate |
| Boundary Review | Built-in evidence, generalization and scope Gate |
| Three native frameworks and Agent taxonomy | Not generalized: apply only when relevant to learning topic |

## Positive example

```text
Model says it will query a record; nothing has actually executed
→ action intent needs controlled execution
→ action finished but model has no result
→ tool result must become the next observation
→ agent can now continue to decide, act and observe
```

Only after this causal chain name Execution, Observation and AgentLoop. Product/framework-specific implementations require separate actual evidence.

## Anti-patterns

- Starting with a Runtime/Framework/API taxonomy rather than an unresolved problem.
- Fabricating extra problems to force a long chain when current explanation is sufficient.
- Requiring technical Probe for nontechnical subjects.
- Confusing **UNKNOWN ≠ ABSENT**, or **ABSENT ≠ BUILD**.
- Claiming executable evidence without executing a probe.
- Inferring a mandatory software module from a necessary behavioral distinction.
- Routing pure self-testing and interview questions to P; P is for full engineering transfer.

## Built-in stabilization contract

```text
Draft
 → Problem-chain Review → Repair
 → Concept First-Appearance Audit → Repair
 → Boundary & Evidence Review → Repair
 → Re-check → Stable Knowledge or explicit blocking unknown
```

Gates are authoring actions, not TODOs for the next user turn. If substantive issues remain, mark knowledge Not Stable and the blocking Gap. No invented completion claim.

## Regression strategy and release conditions

- V0.5.3 can be recovered from frozen Git baseline `learning_v0_5_3`.
- Cases 22–27 test causal chain, evidence separation, concept-first appearance, nontechnical transfer, non-overengineering, and integrated repair.
- D / R source isolation and P V0.2 engineering transfer remain unchanged.
- Static tests only validate skill packaging and eval file structure; **model behavior improvements require controlled old/new runs** with human review and output/transcript evidence.
