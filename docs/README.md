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

## Agentic Protocols and Modules

The system is built from two kinds of specifications, both written in the modular formalism of Cachin (*Reliable and Secure Distributed Programming*) but adapted for LLM-agent coordination rather than distributed nodes. **Protocols** govern ongoing interaction between participants — convergence-shaped ones iterate until a graph predicate holds; consultation has coordination structure between participants under a vocabulary firewall. **Modules** provide transformations or services that protocols compose with. See [protocols overview](protocols/README.md) and [modules overview](modules/README.md) for layering and reading order.

### Protocols

- [Consultation Protocol](protocols/consultation-protocol.md) — *production*. Produces an initial note from a campaign-bound inquiry. Two channels (theory and evidence) consult under enforced vocabulary separation; a synthesizer integrates their outputs.
- [Note Convergence Protocol](protocols/note-convergence-protocol.md) — *convergence*. Drives notes to stability during discovery. Specializes the convergence protocol for notes; `comment.out-of-scope` is the off-ramp that feeds lattice operations.
- [Claim Convergence Protocol](protocols/claim-convergence-protocol.md) — *convergence*. Drives claims to formal precision after claim derivation. Specializes the convergence protocol for claims; adds structural validation, the algorithm, and correctness arguments.
- [Convergence Protocol](protocols/convergence-protocol.md) — the document-type-neutral foundation. Convergence predicate, comment/resolution link types, safety/liveness properties shared by both convergence-shaped specializations.
- [Maturation Protocol](protocols/maturation-protocol.md) — the meta-protocol governing transitions between stage protocols and executing lattice operations (extract, absorb, scope promotion). Reaches quiescence rather than convergence.

### Modules

- [Substrate Module](modules/substrate-module.md) — persistent, append-only link graph every protocol reads from and writes to. Defines retraction as a substrate operation (link-to-link nullification) and the `ActiveLinks` query that subtracts retracted links from results. Properties: SUB1 permanence, SUB2 query soundness, SUB3 count consistency, SUB4–SUB5 retraction nullify-and-shadow, SUB6 retraction idempotence.
- [Agent Module](modules/agent-module.md) — agent identity and operation attribution above the substrate. Defines `agent` (classifies a doc as an agent — its address is the agent's identity) and `manages` (declares an agent is currently responsible for an operation).
- [Claim Derivation Module](modules/claim-derivation-module.md) — transforms a converged note into per-claim files conforming to the Claim Document Contract. The boundary between note convergence and claim convergence; a representation change.

## How the system works, fails, and is disciplined

- [Patterns](patterns/README.md) — observed structural regularities. The primary cycle (Narrow → Refine → Verify), patterns that adjust or feed it, patterns that seed hypothesis space, and the structure that accumulates output.
- [Principles](principles/README.md) — design commitments the system enforces. Coupling (prose:formal ratio as health signal), Validation (structural contract as review precondition), and Voice (positive style structure constraining LLM output) live here.
- [Equilibrium (failure modes)](equilibrium/README.md) — specific ways the system fails to converge. Gravitational (continuous pressure requiring permanent discipline), transitional (acts at representation boundaries, fixable once per boundary), and oscillatory (acts at sites of undecidability, fixable by establishing an arbitrating criterion).

## Design notes

- [Design notes](design-notes/README.md) — architectural choices and aggregate observations that aren't patterns. Domain Language Emergence, Self-Healing, Production Drive.

## Domain-specific

- [Software](software/README.md) — grounded domain: reverse-engineering legacy software systems. Demonstrated on the Xanadu hypertext system.
- [Science](science/README.md) — applying the architecture to scientific discovery. Discovery stage landed on a materials lattice (Maxwell 1867 + Dulong–Petit 1819); downstream stages still to run.

## Guides and runbooks

- [Discovery guide](guides/discovery.md) — note manifest schema, campaign binding, channel artifacts
- [Claim derivation guide](guides/claim-derivation.md) — phases, output structure (body markdown + sidecars)
- [Claim convergence guide](guides/claim-convergence.md) — review steps, caching, dependency management, convergence
- [Claim derivation runbook](runbooks/claim-derivation.md) — step-by-step execution
- [Claim convergence runbook](runbooks/claim-convergence.md) — step-by-step execution
