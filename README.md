# Agentic Reasoning Lattice

A multi-agent framework that accelerates verified hypothesis discovery through structured disagreement between independent evidence channels. Agents grow a lattice of permanently addressed, dependency-tracked, verified claims — replacing ad-hoc knowledge with verified principles traceable to their foundations.

## Two-channel architecture

### What it produces

The framework has produced a verified, domain-independent mathematical foundation through its own operation: sequence arithmetic, interval algebra, correspondence decomposition, and displacement theory — with machine-checked proofs at the foundation and bounded model checking across the lattice.

A reasoning lattice is a set of reasoning documents with explicit dependencies between them. Each document covers one topic, declares what it depends on, and builds on verified foundations below it. The lattice grows through discovery as shared concepts are extracted into new layers. Foundation documents are converged and verified first. Everything above builds on what's been proven.

Agents grow the lattice by creating permanent links and reasoning trails — the communication substrate builds itself through operation. Each verified node is a compact, generalizable principle — permanently addressed, dependency-tracked, and machine-verified. The lattice IS the protocol: permanent addresses, bidirectional dependencies, traceable provenance. Agents coordinate through it, not around it.

- Permanent knowledge trails — every reasoning step is addressable and retrievable
- Traceable provenance — any conclusion can be traced back through its dependency chain
- Shared reasoning — agents work from the same verified claims, not copies that drift

### How it works

A human-posed question is decomposed into channel-appropriate sub-questions. Two independent agent channels — one consulting established theory, one analyzing raw evidence — are separated by a vocabulary firewall that forces hypothesis space exploration. The theory channel cannot use evidence-specific terms. The evidence channel cannot retrieve known solutions from theoretical vocabulary. A synthesis agent integrates both into a structured reasoning document with dependency-mapped claims. Where the channels agree, principles are validated. Where they disagree, new hypotheses emerge.

Each synthesized document is driven to stability by the [note convergence protocol](docs/protocols/note-convergence-protocol.md), then decomposed into atomic claims by the [claim derivation module](docs/modules/claim-derivation-module.md) (a meet operation), then driven toward formal precision by the [claim convergence protocol](docs/protocols/claim-convergence-protocol.md). Convergence is a predicate on the link graph: every active `comment.revise` has a matching active `resolution`. Both protocols specialize the document-type-neutral [convergence protocol](docs/protocols/convergence-protocol.md). The protocol defines when convergence is reached; how to get there — scope strategy, review order, context assembly — is choreography. Mechanical verification (Dafny proofs, Alloy bounded model checking) confirms logical consistency. Every verified node is a testable prediction — the oracle traces failures back to the specific claim and evidence channel that diverged.

Out-of-scope findings flagged during review become [new inquiries](docs/patterns/scope-promotion.md), attaching to the lattice as new nodes. The system discovers the questions it should be asking, not just answers to questions posed.

The system is demonstrated on the Xanadu hypertext system — deriving formal claims from Ted Nelson's design intent (*Literary Machines*) and Roger Gregory's 1988 implementation (udanax-green) under enforced vocabulary separation. Xanadu's protocol primitives — permanent addresses, bidirectional links, traceable provenance — are what the system discovered. The methodology bootstrapped the mathematics of the protocol through its own operation.

## Applying to science

The architecture is deployment-general. The machinery — two-channel discovery, claim derivation, claim convergence, verification — operates on abstract inputs with domain-specific verifiers. The Xanadu case uses Dafny as the verifier for proof soundness; a scientific deployment would use experimental reproducibility.

In a science deployment, the system produces hypotheses, not discoveries. Verification happens externally — in a lab, through replication, or by matching against known answers for rediscovery tests. The AI's job ends at articulating claims precisely enough to be tested; reality confirms or refutes them.

See [Science Approach](docs/science/README.md) for the convergence framing, cone-as-hypothesis-cluster structure, and the Judger evaluation model.

## Agentic Protocols and Modules

The system is built from two kinds of specifications, both written in the modular formalism of Cachin (*Reliable and Secure Distributed Programming*) but adapted for LLM-agent coordination rather than distributed nodes. **Protocols** govern ongoing interaction — convergence-shaped protocols iterate until a graph predicate holds; consultation has coordination structure between participants under a vocabulary firewall. **Modules** provide transformations or services that protocols compose with — they have a precondition, a transformation or service, and a postcondition. Both share the specification surface; they differ in whether the underlying shape is interaction or transformation.

See [protocols overview](docs/protocols/README.md) and [modules overview](docs/modules/README.md) for layering and reading order.

### Protocols

- [Consultation Protocol](docs/protocols/consultation-protocol.md) — *production*. Produces an initial note from a campaign-bound inquiry. Two channels (theory and evidence) consult under enforced vocabulary separation; a synthesizer integrates their outputs.
- [Note Convergence Protocol](docs/protocols/note-convergence-protocol.md) — *convergence*. Drives notes to stability during discovery. Specializes the convergence protocol for notes; `comment.out-of-scope` is the off-ramp that feeds lattice operations.
- [Claim Convergence Protocol](docs/protocols/claim-convergence-protocol.md) — *convergence*. Drives claims to formal precision after claim derivation. Specializes the convergence protocol for claims; adds structural validation, the algorithm, and correctness arguments.
- [Convergence Protocol](docs/protocols/convergence-protocol.md) — the document-type-neutral foundation. Convergence predicate, comment/resolution link types, safety/liveness properties shared by both convergence-shaped specializations.
- [Maturation Protocol](docs/protocols/maturation-protocol.md) — the meta-protocol governing transitions between stage protocols and executing lattice operations (extract, absorb, scope promotion). Reaches quiescence rather than convergence.

### Modules

- [Substrate Module](docs/modules/substrate-module.md) — persistent, append-only link graph every protocol reads from and writes to. Defines retraction as a substrate operation (link-to-link nullification) and the `ActiveLinks` query that subtracts retracted links from results. Properties: SUB1 permanence, SUB2 query soundness, SUB3 count consistency, SUB4–SUB5 retraction nullify-and-shadow, SUB6 retraction idempotence.
- [Agent Module](docs/modules/agent-module.md) — agent identity and operation attribution above the substrate. Defines `agent` (classifies a doc as an agent — its address is the agent's identity) and `manages` (declares an agent is currently responsible for an operation). Lets convergence protocols attribute their work to specific agents without protocol identity leaking into the substrate's type system.
- [Claim Derivation Module](docs/modules/claim-derivation-module.md) — transforms a converged note into per-claim files conforming to the Claim Document Contract. The boundary between note convergence and claim convergence; a representation change.

## Documentation

- [Vision](docs/vision.md) — hypothesis space navigation, semantic communication substrate, Lamarckian evolution, building the engine
- [Methodology](docs/methodology.md) — inquiry decomposition, two-channel discovery, claim convergence, pattern language
- [Principles](docs/principles/README.md) — three disciplines that keep the review cycle on its real job: [Coupling](docs/principles/coupling.md) (prose and formal content authored as a pair), [Validation](docs/principles/validation.md) (structural contract as a precondition for review), and [Voice](docs/principles/voice.md) (positive style structure constrains LLM output by construction). Why the system can make new discoveries rather than stalling or drifting.
- [Two-Channel Architecture](docs/two-channel-architecture.md) — independent theory and evidence channels, vocabulary firewall, channel asymmetry, synthesis. The mechanism that produces new knowledge for the lattice.
- [Discovery](docs/discovery.md) — finding formal structure through structured consultation
- [Claim Derivation](docs/claim-derivation.md) — meet operation: document → atomic claims
- [Claim Convergence](docs/claim-convergence.md) — precision as a discovery tool, reasoning that improves itself
- [Pattern Language](docs/patterns/README.md) — operationally discovered patterns for agentic reasoning systems
- [Glossary](docs/glossary.md) — system-specific terms and their definitions

### Domains

- [Software](docs/software/README.md) — grounded domain on legacy software reverse-engineering (Xanadu)
- [Science](docs/science/README.md) — domain for scientific discovery (discovery stage landed on a materials lattice; downstream stages still to run)

### Guides

- [Claim derivation guide](docs/guides/claim-derivation.md) — stages, output structure
- [Claim convergence guide](docs/guides/claim-convergence.md) — review steps, caching, dependency management, convergence

### Runbooks

- [Claim derivation runbook](docs/runbooks/claim-derivation.md) — step-by-step execution
- [Claim convergence runbook](docs/runbooks/claim-convergence.md) — step-by-step execution

## Structure

```
lattices/xanadu/      — xanadu (software) domain lattice: substrate
                        documents (notes, claims, inquiries, campaigns)
                        plus workspace artifacts and verification output
lattices/materials/   — materials (science) domain lattice
                        (Maxwell 1867 + Dulong–Petit 1819)
channels/             — channel plugins per domain (theory and evidence
                        sources: Nelson/Gregory for xanadu,
                        Maxwell/Dulong-Petit for materials)
prompts/              — protocol prompts organized by lattice
                        (shared, xanadu, materials)
scripts/              — protocol automation (consultation, note convergence,
                        claim derivation, claim convergence, verification,
                        validation)
run/                  — shell entry points for common protocol invocations
docs/                 — methodology, patterns, principles, protocols,
                        design notes, guides, runbooks
```