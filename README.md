# SenseWright V2.9.0

**Four independent cognitive skills, one entrypoint:** [SKILL.md](SKILL.md).

| Skill | Primary job |
|---|---|
| [Deep Read V6.4](skills/article-deep-read-v6.4/SKILL.md) | Faithfully reconstruct source reasoning |
| [Review V0.10](skills/vibe-review-v0.10/SKILL.md) | Independently evaluate sources and claims |
| [Learning V0.6.2](skills/system-learning-v0.6.2/SKILL.md) | Build transferable, evidence-grounded understanding |
| [Practice V0.2](skills/practice-v0.2/SKILL.md) | Implement, operate, and verify an engineering result |

## Learning: orchestration vs cognitive method

```text
             Current Raw Input
              /           \
      Deep Read (D)     Review (R)
       [isolated]        [isolated]
              \           /
             both complete
                   |
             Learning (L)
       Adaptive understanding loop
                   |
          Practice (P) only if
         execution is requested
```

**Orchestration contract:** Learning still requires fresh D/R from the same input with independent contexts and a completion barrier. Both outputs inform L but are not independent new evidence. For query-only prompts, preflight is brief and source-honest. The runtime, not Skill prose, must prove actual execution isolation with a Trace.

**General cognitive loop (not a mandatory sequence):**

- **Orient** — understand the user's learning intent and the real object. Distinguish a selected sample, a convenient metric and the actual purpose.
- **Frame** — activate *relevant and appropriately scoped* prior knowledge, then keep, revise or discover the research question. Neither the deepest-sounding question nor a single universal terminal criterion is automatically right.
- **Explain** — derive the smallest necessary causal, procedural, conceptual or formal mechanism, using a real example where useful.
- **Anchor** — connect the mechanism to original source, code, observed behavior, comparable evidence or proportionate quantitative reasoning. Distinguish verified facts, inferences, assumptions and unknowns.
- **Challenge & rebuild** — try a competing explanation or consequential changed condition, revise as needed, and give a coherent explanation at the user's requested depth. Stop when more work adds no real understanding.

These are **responsibilities that can recur**. They are not six headings that every answer must print; simple definitions may need only a short answer, while complex source analysis may require multiple evidence loops.

**Research order differs from teaching order:** check materials and observations before deciding what mechanism they support; teach the problem and mechanism first, then show the evidence. Source code learning should cite exact control/data/state links and line anchors when available; claims of actual execution require an actual run. Subject-specific theories must come from the task context or trustworthy subject sources, **not from hardcoded finance, banking, health or product examples in the generic Learning Skill**.

**Boundaries:** D restores source faithfully; R critiques source independently; L builds understanding; P builds and tests real artifacts. Learning does not automatically authorize market forecasts, clinical decisions or implementing systems.

## Evaluation and historical context

```bash
python scripts/validate_skills.py
python scripts/validate_evals.py
```

The [learning refactor review](docs/learning-core-refactor-20261011.md) audits the October 9–11 iteration history, identifies which capabilities to retain or externalize, and defines regression goals. [Evaluation guidelines](evals/README.md) retain old and new domain-specific cases as **test data**, not runtime instructions.

Historical design notes: [Mechanism / Problem Chain](docs/learning-problem-chain-migration.md), [Reality Calibration](docs/learning-reality-calibration.md), [Problem Discovery](docs/learning-problem-discovery.md), [Domain Anchor](docs/learning-domain-anchor.md), and [D/R orchestration](docs/learning-mandatory-dr-preflight.md). They document earlier reasoning and concrete examples, **not separate mandatory Learning stages**.

Passing static CI verifies assets and metadata, **not** teaching quality, domain generalization or independent D/R runtime execution. Behavioral claims require paired model runs under matched inputs and settings plus human review.
