# Documentation

Complete index of the documentation. The root [README](../README.md) is the project overview and points into this tree; this file is the documentation map organized by type.

## Core reference

- [Vision](vision.md) — hypothesis space navigation, semantic communication substrate, building the engine
- [Methodology](methodology.md) — inquiry decomposition, two-channel discovery, claim convergence
- [Discovery](discovery.md) — finding formal structure through structured consultation
- [Blueprinting](blueprinting.md) — meet operation: document → atomic claims
- [Claim Convergence](claim-convergence.md) — precision as a discovery tool
- [Architecture](architecture.md) — structural hierarchy (domain / lattice / campaign / inquiry / note / claim) and the lattice lifecycle
- [Principles](principles/README.md) — three disciplines that keep the review cycle focused on its real job: [Coupling](principles/coupling.md) (prose and formal content authored as a pair), [Validation](principles/validation.md) (structural contract as a precondition for review), and [Voice](principles/voice.md) (positive style structure constrains LLM output by construction). Coupling and validation monitor and check; voice prevents problems from being generated. All three are needed.
- [Glossary](glossary.md) — system-specific terms and their definitions

## Agentic Protocols

The system is a stack of protocols sharing a substrate. The convergence protocol defines the shared predicate and link types; note convergence and claim convergence specialize it for different scales; the maturation protocol orchestrates transitions between stages and executes lattice operations. Following the modular formalism of Cachin (*Reliable and Secure Distributed Programming*), but for LLM-agent coordination rather than distributed nodes.

- [Convergence Protocol](protocols/convergence-protocol.md) — the document-type-neutral module. Convergence predicate, comment/resolution link types, safety/liveness properties shared by all review/revise processes.
- [Note Convergence Protocol](protocols/note-convergence-protocol.md) — drives notes to stability during discovery. Specializes the convergence protocol for notes; adds `comment.out-of-scope` as the off-ramp that feeds lattice operations.
- [Claim Convergence Protocol](protocols/claim-convergence-protocol.md) — drives claims to formal precision after blueprinting. Specializes the convergence protocol for claims; adds structural validation, the algorithm, and correctness arguments.
- [Maturation Protocol](protocols/maturation-protocol.md) — the meta-protocol governing transitions between stage protocols and executing lattice operations (extract, absorb, scope promotion). Reaches quiescence rather than convergence.

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
- [Blueprinting guide](guides/blueprinting.md) — pipeline stages, YAML format, output structure
- [Claim convergence guide](guides/claim-convergence.md) — review steps, caching, dependency management, convergence
- [Blueprinting runbook](runbooks/blueprinting.md) — step-by-step execution
- [Claim convergence runbook](runbooks/claim-convergence.md) — step-by-step execution
