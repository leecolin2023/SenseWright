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

## Source-grounded code learning

The **research order** is source/tests/observable behavior first, then infer a mechanism. The **teaching order** is the reverse of a file walkthrough: **real problem → necessary mechanism → implementation logic → a few exact source anchors → next useful question**. Source citations must actually support the adjacent claim. If code contradicts the assumed mechanism, revise the explanation rather than inventing implementation. Type declarations and documentation alone do not prove runtime behavior; reading source is not the same as running a probe.

This rule applies only when learning from source code; it does not add source-code overhead to simple conceptual learning. D and R remain faithful/independent source-facing stages; the presentation reorder happens only in L.

## Validation

~~~bash
python scripts/validate_skills.py
python scripts/validate_evals.py
~~~

[Evaluation guidelines](evals/README.md) cover route tests, regression cases, and baseline comparisons. Passing the static validators does **not** establish behavioral superiority or actual Runtime isolation.

The detailed evolution and rationale are retained in [CHANGELOG.md](CHANGELOG.md), [method migration notes](docs/learning-problem-chain-migration.md), and [D/R preflight specification](docs/learning-mandatory-dr-preflight.md). They are not required reading for ordinary Skill execution.
