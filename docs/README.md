# Documentation

Complete index of the documentation. The root [README](../README.md) is the project overview and points into this tree; this file is the documentation map organized by type.

## Core reference

- [Vision](vision.md) — hypothesis space navigation, semantic communication substrate, building the engine
- [Methodology](methodology.md) — inquiry decomposition, two-channel discovery, claim derivation, claim convergence
- [Two-Channel Architecture](two-channel-architecture.md) — independent theory and evidence channels, vocabulary firewall, channel asymmetry, synthesis. The mechanism that produces new knowledge for the lattice.
- [Discovery](discovery.md) — finding formal structure through structured consultation
- [Claim Derivation](claim-derivation.md) — meet operation: document → atomic claims
- [Claim Convergence](claim-convergence.md) — precision as a discovery tool
- [Architecture](architecture.md) — structural hierarchy (domain / lattice / campaign / inquiry / note / claim) and the lattice lifecycle
- [Principles](principles/README.md) — three disciplines that keep the review cycle focused on its real job: [Coupling](principles/coupling.md) (prose and formal content authored as a pair), [Validation](principles/validation.md) (structural contract as a precondition for review), and [Voice](principles/voice.md) (positive style structure constrains LLM output by construction). Coupling and validation monitor and check; voice prevents problems from being generated. All three are needed.
- [Glossary](glossary.md) — system-specific terms and their definitions

## Protocol stack

The system runs on a substrate-mediated *stigmergic* protocol stack — agents read substrate state and emit, with no direct message passing. See [Protocol Stack overview](protocols/README.md) for the taxonomy, the Cachin-mapping (system model / communication primitive / message format / termination / scheduling discipline → where each lives), and reading order. Three architectural layers:

### Substrate spec — [overview](protocols/substrate/README.md)

The medium, message format, and execution model on which all protocols compose:

- [Typed Relations on Address Sets](protocols/substrate/types.md) — typed-relation primitive, three operations, R0–R7
- [Relation Shapes](protocols/substrate/shapes.md) — shape restrictions, Sh-conf + Sh0–Sh5
- [Predicate Composition](protocols/substrate/predicate-composition.md) — predicate language `PL`, PC0–PC6
- [Agents](protocols/substrate/agents.md) — agent semantics, AG0–AG7
- [Quiescence](protocols/substrate/quiescence.md) — termination condition, Q0–Q10
- [Runner](protocols/substrate/runner.md) — scheduling discipline, Run0–Run5

### Agent registry — [overview](protocols/agents/README.md)

The 26 agents in `scripts/lib/agents/` documented by *caste*. Two hand-off mechanisms (stigmergic, sequential) and the Stigmergic Protocol primitives (Correction, Marker, Self-Review, Cycle):

- [Producers](protocols/agents/producers.md) — agents that grant new substrate identity
- [Refiners](protocols/agents/refiners.md) — agents that close findings
- [Scouts](protocols/agents/scouts.md) — agents that detect and report

### Maturation Stigmergic Protocols

Compositions of Stigmergic Protocol primitives terminating at scope quiescence at a designated tier:

- [Note-to-Claim Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md) — first instance; inquiry → confirmed-note → quiescent-claim arc

## How the system works, fails, and is disciplined

- [Patterns](patterns/README.md) — observed structural regularities. The primary cycle (Narrow → Refine → Verify), patterns that adjust or feed it, patterns that seed hypothesis space, and the structure that accumulates output.
- [Principles](principles/README.md) — design commitments the system enforces. Coupling (prose:formal ratio as health signal), Validation (structural contract as review precondition), and Voice (positive style structure constraining LLM output) live here.
- [Equilibrium (failure modes)](equilibrium/README.md) — specific ways the system fails to converge. Gravitational (continuous pressure requiring permanent discipline), transitional (acts at representation boundaries, fixable once per boundary), and oscillatory (acts at sites of undecidability, fixable by establishing an arbitrating criterion).

## Design notes

- [Design notes](design-notes/README.md) — architectural choices and aggregate observations that aren't patterns. Domain Language Emergence, Self-Healing, Production Drive.

## Domain-specific

- [Software](software/README.md) — grounded domain: reverse-engineering legacy software systems. Demonstrated on the Xanadu hypertext system.
- [Science](science/README.md) — applying the architecture to scientific discovery. Discovery stage landed on a materials lattice (Maxwell 1867 + Dulong–Petit 1819); downstream stages still to run.

