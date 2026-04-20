# Pattern Language for Agentic Reasoning Systems

Patterns for how agents discover, verify, and organize knowledge. These patterns were observed during operation on the Xanadu demonstration domain. They generalize to any system where agents produce structured knowledge under dependency constraints.

The scientific method is the lineage: narrow scope, refine through iteration, verify coherence. These patterns describe what happens when agents operationalize that rhythm — the specific structures, failure modes, and growth mechanisms that emerge.

Each pattern was observed before it was named. They emerge from running the system, not from upfront design.

## The primary pattern

- [Narrow → Refine → Verify](narrow-refine-verify.md) — the three-phase cycle that every process follows. Narrow scope to make the problem tractable, refine within that scope, verify that the pieces cohere. One rhythm, everywhere.

## Patterns

The primary cycle's three phases, each a pattern in its own right:

- [Scope narrowing](scope-narrowing.md) — narrow scope to harden each piece. Widen when coupling stalls convergence.
- [Review/revise iteration](review-revise-iteration.md) — find issues, fix them, re-check. The refinement loop within the narrowed scope.
- [Verify the whole](verify-the-whole.md) — step back and check that the refined pieces cohere.

Patterns that adjust or feed the cycle:

- [Dependency cone](dependency-cone.md) — tight coupling defeats narrow-scope refinement. A signal to widen.
- [Scoped inquiry](scoped-inquiry.md) — narrowing applied to questions. Each authority investigates what it's qualified to evaluate.
- [Two data authorities](two-data-authorities.md) — independent channels with enforced separation. Agreement validates, disagreement discovers new hypotheses.
  - [Legacy software discovery](two-data-authorities-legacy-software.md) — grounded instantiation: reverse-engineering legacy systems with designer material × implementation code.
  - [Channel asymmetry](channel-asymmetry.md) — shape-mismatch between the two channels is what forces genuine coinage rather than symbol-matching. Serves Two Data Authorities.
- [Consult authority](consult-authority.md) — during refinement, go back to the source when uncertain. Keeps the review/revise loop grounded in evidence.
- [Representation change](representation-change.md) — same content, different form. A tool that scope narrowing uses when the current form can't support finer granularity.
- [Prose compression](prose-compression.md) — a concept already named in prose gets a symbol for formal manipulation. Same concept, compressed form.
- [Vocabulary bridge](vocabulary-bridge.md) — map domain language to structural language once, share across the lattice. Sits between foundation algebra and higher layers.
- [Extract/absorb](extract-absorb.md) — shared concepts extracted into new foundation layers, duplicates absorbed. How the lattice grows inward.
- [Accretion](accretion.md) — claims grow the lattice by adding new claims, not by mutating existing ones. The discipline that prevents Contract Sprawl.

Patterns that seed the hypothesis space — how the system proposes new territory to explore:

- [Prose coinage](prose-coinage.md) — at the concept level. Synthesis coins a new prose word proposing a concept that didn't exist in either channel's source. Each coinage is a structural claim.
- [Scope promotion](scope-promotion.md) — at the topic level. An out-of-scope finding is promoted to a first-class investigation, proposing a whole area worth its own note. How the lattice grows outward.

Patterns of convergence — when iteration stops, relative to the downstream verifier:

Convergence is always relative to what consumes the output next. Different verifiers imply different stopping criteria; the underlying iterative machinery is the same. Candidates observed in this system, with pattern documentation status noted:

- **Ground State** — V-cycle convergence across all scales (claim, cluster, system review all agree). Defined in [glossary](../glossary.md#g); discussed in [Review V-Cycle](../design-notes/review-v-cycle.md). Not yet a standalone pattern doc.
- **Saturation** — probe-archive convergence: new questions become answerable from the existing archive rather than requiring new probes (Gregory's 80-test finding). Discussed in [Self-Healing](../design-notes/self-healing.md). Not yet a standalone pattern doc.
- **Hypothesis articulation** — science-domain convergence: claim stated precisely enough that another lab could reproduce the test. Not yet documented; conjectured from the reproducibility / falsifiability framing.

The structure that accumulates the output:

- [Lattice](lattice.md) — nodes with explicit dependencies at two granularities: notes and claims. Grows outward via scope promotion, inward via extract/absorb. Produced by repeated narrow → refine → verify cycles.

## How they connect

```
narrow → refine → verify (the primary cycle, applied everywhere)
  │         │         │
  │         │         └─ verify the whole
  │         └─ review/revise iteration
  └─ scope narrowing
       └─ overshoots ─→ dependency cone (widen and retry)

scoped inquiry ─── narrows questions for ──→ two data authorities

repeated cycles ─── accumulate into ──→ lattice
  ├─ grows outward via ─→ scope promotion
  └─ grows inward via ──→ extract/absorb
```

## How patterns are documented

Each pattern stands on its own. Connections to other patterns appear in "leads to" and "motivated by" sections within each document. Applications — concrete uses in this system — are a separate section within each pattern. The pattern is general; the applications are specific.