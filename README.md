# SenseWright V2.8.2

**Four cognitive skills, one entrypoint:** [SKILL.md](SKILL.md).

| Skill | Primary job |
|---|---|
| [Deep Read V6.4](skills/article-deep-read-v6.4/SKILL.md) | Faithfully reconstruct a source and preserve the reasoning that matters |
| [Review V0.10](skills/vibe-review-v0.10/SKILL.md) | Independently review the original source, covering all units before prioritizing issues |
| [Learning V0.6.2](skills/system-learning-v0.6.2/SKILL.md) | Rebuild grounded understanding and necessary mechanisms from a real problem |
| [Practice V0.2](skills/practice-v0.2/SKILL.md) | Transfer understood knowledge into executable, verifiable engineering work |

## How Learning works

~~~text
                   Raw Input
                  /         \
      Deep Read (D)        Review (R)
       [isolated]          [isolated]
                  \         /
                 both complete
                       |
                       v
                  Learning (L)
          Ground → Mechanism → Boundary
                       |
                       v
                Practice (P)
               [only if needed]
~~~

Every Learning run requires **fresh D and R** on the same raw input, independently executed. Learning reads both results as cognitive scaffolds, not extra evidence; it must return to the real object and mechanism rather than copy or concatenate the upstream reports.

For a question without an attached document, D/R operate briefly on the actual user question and its premises. This is still required; no source or critique should be invented. D-only, R-only, D+R, and P-only requests keep their independent paths.

The host Runtime must enforce actual isolation and a completion barrier. This repository's skill instructions and static checks **do not by themselves prove** that two isolated calls occurred.

## Learning behavior

1. Ground the question in an observable example; check unsupported premises.
2. When necessary, advance through a real failure → minimal required mechanism → next meaningful problem.
3. Trace technical mechanisms with a minimal run; use a single high-information condition change when it clarifies boundaries.
4. Distinguish source facts, derived knowledge, external evidence, and unknowns.
5. Repair broken explanation chains and unsupported claims before delivery. Output one coherent answer instead of internal audit logs.

Learning **does not imply an implementation decision**. Practice is for design and real engineering execution, not merely testing whether the user can answer questions.

## Mechanism-to-Implementation Mapping

**Universal principle:** Understand the real problem, derive the necessary mechanism, then anchor the explanation in concrete reality. This applies to technical books, algorithms, source code, CLI operations, SQL examples, protocols, experiments, architecture and business workflows—not only coding.

**Research order** and **teaching order** are distinct:
- **Research:** inspect original materials and verifiable behavior first, then determine which mechanism the evidence supports. Do not turn unexecuted examples into measured results.
- **Teaching:** real problem → necessary mechanism → concrete realization or operation → minimal verifiable evidence → next meaningful problem (only if useful).

**Two internal checks:** (1) After removing framework/API/command names, can the learner explain why the mechanism exists and how it works? (2) After reintroducing the concrete realization, does each important claim map to actual materials, observed input/output or source? If evidence contradicts the expected mechanism, revise the model, not the implementation.

**Precise coding intent:** Learning requests such as "why is this function designed this way?", "understand the agent loop from source", "trace tool calls" still route **D + R → L**. L should map the mechanism to actual control/data flow and relevant, verifiable file/line anchors, without an API inventory. A request to debug or implement code without a learning goal remains Practice (P); a source-faithful file inventory can be D alone. This teaching rule does not force a large implementation section onto short conceptual questions.

D and R remain independent and source-facing; the explanation reorder is owned by L.


## Validation

~~~bash
python scripts/validate_skills.py
python scripts/validate_evals.py
~~~

[Evaluation guidelines](evals/README.md) cover route tests, regression cases, and baseline comparisons. Passing the static validators does **not** establish behavioral superiority or actual Runtime isolation.

The detailed evolution and rationale are retained in [CHANGELOG.md](CHANGELOG.md), [method migration notes](docs/learning-problem-chain-migration.md), and [D/R preflight specification](docs/learning-mandatory-dr-preflight.md). They are not required reading for ordinary Skill execution.
