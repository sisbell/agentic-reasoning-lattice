# Equilibrium

Patterns of disequilibrium — specific ways the reasoning system fails to converge. Each describes a recognizable failure mode, its cause, how to detect it, and how to resolve it.

Convergence is the goal: all scales of review (claim, cluster, system) agree that the note is clean. Equilibrium patterns describe what breaks that.

Each was observed through operation. Resolution is not "try harder" — it is a specific structural fix.

## Three classes of failure

**Gravitational failures** act continuously. Every review cycle produces the pressure: the reviser is tempted to extend rather than restructure; exhaustiveness obligations create defense-of-completeness loops; citation accounting creeps into prose. These cannot be fixed once. They require permanent discipline — prompt framing, coupling monitoring, and the authoring habits that resist the pull.

**Transitional failures** act at representation boundaries. A stage introduces a new unit of structure; its output has rules that must hold for the structure to mean anything; if the transition doesn't specify the rules, downstream stages silently operate on malformed state. The force does not recur once the boundary's contract is sound — but every new representation change introduced anywhere in the system carries the same risk.

**Oscillatory failures** act at sites of undecidability. Two resolutions both look locally valid and nothing in the cycle picks between them, so consecutive cycles pick opposite ones. The force is neither continuous nor boundary-bound — it fires wherever a review/revise pair lacks a shared criterion to defer to. Resolution is to establish the criterion: a missing contract, a missing convention, or an explicit scope ruling.

The distinction matters for intervention. Gravitational failures are prompt and monitoring problems. Transitional failures are contract and validation problems. Oscillatory failures are arbitration problems. A pattern in the wrong class gets the wrong fix.

## Gravitational patterns

- [Surface Expansion](surface-expansion.md) — textual surface grows monotonically across review cycles without reasoning growth. The shared mechanism underneath Contract/Prose/Index Sprawl. Directly measurable via word delta, prose:structure ratio, and cycles-since-contraction — enables cycle-health monitoring independent of which Sprawl variant forms.
- [Contract Sprawl](contract-sprawl.md) — a claim's formal contract keeps growing across cycles. Two modes: by-item (more clauses) and by-entry (Depends entries become essays). Driven by Genesis Attractor, exhaustiveness obligations, and citation accounting inlined into prose. Contract-surface manifestation of Surface Expansion.
- [Prose Sprawl](prose-sprawl.md) — narrative prose grows across cycles with meta-commentary that does not advance the reasoning. Driven by defensive justification, exhaustiveness obligations, and reviser verbosity defaults. Narrative-surface manifestation of Surface Expansion.
- [Index Sprawl](index-sprawl.md) — a file accumulates an enumeration of named entities that have their own homes elsewhere. Propagates sibling-to-sibling via exhaustiveness obligations. Enumeration-surface manifestation of Surface Expansion.
- [Citation Drift](citation-drift.md) — citations reference facts whose home has moved, been renamed, or never had a declared home. Distributed across many claims. Internally driven by proof evolution, passively driven by upstream foundation changes.

## Transitional patterns

- [Uncontracted Representation Change](uncontracted-representation-change.md) — a stage introduces a new unit of structure without specifying what well-formed output means. Downstream agents inherit the structure without the rules and spend review cycles on symptoms of violations that have no names. The most visible manifestation is a non-converging cone whose findings are structural (duplicated definitions, dangling references, metadata disagreement) rather than semantic.

## Oscillatory patterns

- [Reverse-Course Oscillation](reverse-course-oscillation.md) — a reviser's change in cycle N is undone in cycle N+1 because two locally-valid resolutions exist and the cycle has no shared criterion to pick between them. Subtypes by source of undecidability: contract-absent (same cause as Uncontracted Representation Change), judgment-call, and exhaustiveness-vs-restraint. Detectable from symmetric cross-cycle diffs at the same file region.
