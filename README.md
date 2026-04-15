# Agentic Reasoning Lattice

A multi-agent system that discovers formal properties and constraints through structured disagreement between independent evidence channels. Local agents run structured pipelines — discovery, blueprinting, formalization, verification — producing a dependency lattice of reasoning documents with machine-checked proofs.

## What it produces

The framework has produced a verified, domain-independent mathematical foundation through its own operation: sequence arithmetic, interval algebra, correspondence decomposition, and displacement theory — with machine-checked proofs at the foundation and bounded model checking across the lattice.

A reasoning lattice is a set of reasoning documents with explicit dependencies between them. Each document covers one topic, declares what it depends on, and builds on verified foundations below it. The lattice grows through discovery as shared concepts are extracted into new layers. Foundation documents are formalized and verified first. Everything above builds on what's been proven.

The agents discover formal properties and constraints. Those properties specify a protocol for agentic memory and communication:

- Permanent knowledge trails — every reasoning step is addressable and retrievable
- Traceable provenance — any conclusion can be traced back through its dependency chain
- Shared reasoning — agents work from the same claims, not copies that drift

## How it works

Two agent channels — one consulting established theory, one analyzing raw evidence — are separated by a vocabulary firewall. The theory channel cannot reference specific data. The data channel cannot use theoretical terms. A synthesis agent integrates both into structured reasoning documents with dependency-mapped claims. Where the channels agree, principles are validated. Where they disagree, new principles emerge.

The system is demonstrated on the Xanadu hypertext system — deriving formal properties from Ted Nelson's design intent (*Literary Machines*) and Roger Gregory's 1988 implementation (udanax-green) under enforced vocabulary separation. Xanadu's protocol primitives — permanent addresses, bidirectional links, traceable provenance — are what the system discovered. The methodology bootstrapped the mathematics of the protocol through its own operation.

## Documentation

### Methodology

- [Methodology](docs/methodology.md) — overall approach: discovery → blueprinting → formalization → modeling
- [Discovery](docs/discovery.md) — finding the formal structure through structured consultation
- [Blueprinting](docs/blueprinting.md) — constructing the intermediate representation for formalization
- [Formalization](docs/formalization.md) — precision as a discovery tool, reasoning that improves itself

### Guides

- [Blueprinting guide](docs/guides/blueprinting.md) — pipeline stages, YAML format, output structure
- [Formalization guide](docs/guides/formalization.md) — review steps, caching, dependency management, convergence

### Runbooks

- [Blueprinting runbook](docs/runbooks/blueprinting.md) — step-by-step execution
- [Formalization runbook](docs/runbooks/formalization.md) — step-by-step execution

## Structure

- [vault/1-reasoning-docs/](vault/1-reasoning-docs/) — ASN reasoning documents (discovery output)
- [vault/2-blueprints/](vault/2-blueprints/) — per-property decomposition (blueprinting output)
- [vault/3-formalization/](vault/3-formalization/) — formalized properties with contracts
- [vault/3-modeling/](vault/3-modeling/) — Dafny proofs and Alloy models
- [vault/project-model/](vault/project-model/) — per-ASN manifests, exports, dependency graphs
- [scripts/](scripts/) — pipeline automation
- [docs/](docs/) — methodology, guides, runbooks

## Vision

What exists today is local agents running rigorous pipelines with a systematic methodology — convergence criteria, dependency ordering, formal verification. The next step scales something that works locally into something that works distributedly. Permanent addressable knowledge trails let distributed agents trace how any conclusion was reached, share reasoning without copying, and propagate changes through dependency links.

1. Local agents discover formal properties and constraints (today, working, demonstrated)
2. Those properties specify a remote communication protocol
3. That protocol enables distributed collaboration
4. Distributed agents discover more, better, faster