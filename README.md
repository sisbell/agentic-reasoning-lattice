# Agentic Reasoning Lattice

An autonomous multi-agent framework for mathematical discovery. Agents discover, formalize, and verify mathematical structure through structured disagreement between independent evidence channels — then use that mathematics to build the coordination protocols that let them scale.

Theory says X, data shows Y, agents reason about the gap. The gap is where discovery happens.

Two agent channels — one consulting established theory, one analyzing raw evidence — are separated by a vocabulary firewall. A synthesis agent integrates both into structured reasoning documents with dependency-mapped claims. Where the channels agree, principles are validated. Where they disagree, new principles emerge.

The Xanadu hypertext system (Nelson's *Literary Machines*, Gregory's udanax-green) provides the target coordination architecture: permanent addresses, bidirectional links, transclusion, immutable content, traceable provenance. These protocols enable multi-agent collaboration at scale — every reasoning step permanent, every claim traceable through its dependency chain. The agents formalize these protocols as part of their own operation, building the infrastructure they need to operate autonomously.

The framework has produced a verified, domain-independent mathematical foundation through its own operation: sequence arithmetic, interval algebra, correspondence decomposition, and displacement theory — with machine-checked proofs at the foundation and bounded model checking across the lattice.

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

```
vault/
  1-reasoning-docs/      — ASN reasoning documents (discovery output)
  2-blueprints/          — per-property decomposition (blueprinting output)
  3-formalization/       — formalized properties with contracts
  3-modeling/            — Dafny proofs and Alloy models
  project-model/         — per-ASN manifests, exports, dependency graphs

scripts/                 — pipeline automation
docs/                    — methodology, guides, runbooks
```

## Pipelines

### Blueprinting

```bash
python scripts/blueprint.py <ASN>           # full pipeline: decompose → enrich → disassemble → validate
python scripts/promote-blueprint.py <ASN>    # copy to formalization
```

### Formalization

```bash
python scripts/formalize.py <ASN>            # produce contracts, Dijkstra rewrite
python scripts/formalization-review.py <ASN>  # convergence loop
python scripts/formalization-assembly.py <ASN> # export to project-model
```

### Modeling

```bash
python scripts/dafny.py <ASN>                # translate to Dafny
python scripts/alloy.py <ASN>                # bounded model checking
```
