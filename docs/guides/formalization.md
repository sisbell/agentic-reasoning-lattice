# Guide: Formalization Pipeline

*Updated 2026-04-12.*

## Overview

Formalization transforms per-property file pairs from blueprinting into rigorously proven specifications with formal contracts. Each property is formalized independently — its dependencies are immutable context. See [why this converges](#why-per-property-formalization-converges). The pipeline runs: formalize → review cycle → assembly.

## Pipeline Stages

### Formalize

Rewrites every non-definition, non-axiom property's proof to Dijkstra standard and produces formal contracts (preconditions, postconditions, invariants, frame conditions).

- Reads `type` from each property's `.yaml` to filter candidates (skips axioms, design-requirements, definitions)
- Processes properties in dependency order (topological sort from `depends` fields)
- Processes each dependency level in parallel
- Auto-commits after each dependency level

### Review Cycle

Four review steps run in a convergence loop:

**Proof review** — For each property, sends the body + dependency context to the LLM. Checks 7 points: logical gaps, unjustified steps, missing cases, dependency correctness, formal contract completeness. On FOUND, a reviser agent edits the `.md` file. If new dependencies are discovered, the reviser adds them to the `.yaml` depends list (add-only).

**Contract review** — Validates that each formal contract matches the proof. On MISMATCH, rewrites the contract. Vocabulary context is aggregated from all property YAMLs automatically.

**Cross-review** — Reads the entire assembled ASN (all properties concatenated) + foundation statements. Finds issues that per-property review can't catch: carrier-set conflation, precondition chain gaps, circular reasoning across properties. Reviser agent can edit multiple `.md` files and update `.yaml` depends (add-only).

**Dependency review** — Scans property bodies for references to labels not declared in the `depends` field. Add-only — new deps found are added to the `.yaml`, never removed.

### Assembly

Produces two export files in `vault/project-model/ASN-NNNN/`:

- `formal-statements.md` — trimmed property sections for downstream consumers
- `dependency-graph.yaml` — structured dependency data for discovery and rebase

Generated from per-property files on demand — not maintained during formalization.

## Caching

Hashes are stored in `_cache.json` (not git-tracked). The hash covers both `.md` and `.yaml` content — changes to either invalidate the property and its dependents.

- Delete `_cache.json` to force a full re-run
- Unchanged properties are skipped automatically
- When a property changes, its downstream dependents are added to the dirty set

## Dependency Management

Dependencies are tracked in per-property `.yaml` files under the `depends` field.

- **Add-only**: when a proof revision introduces a new dependency, the reviser adds it. Existing dependencies are never removed by automation.
- **Why add-only**: extra dependencies are cosmetic noise (unnecessary import). Missing dependencies are dangerous (build failures, hidden gaps). The asymmetry is intentional.
- **Manual removal**: if a dependency is genuinely wrong, remove it manually from the `.yaml` file.
- **Cross-ASN deps**: resolved mechanically by scanning upstream ASN formalization directories for matching labels.

## YAML Metadata Format

```yaml
label: T8
name: AllocationPermanence
type: theorem
depends:
  - T1
  - T2
  - T4
  - T10a
  - TA5
  - TumblerAdd
  - TumblerSub
  - NoDeallocation
```

- **label** — stable key, never changes
- **name** — PascalCase, can be refined
- **type** — classification from blueprinting (axiom, definition, design-requirement, lemma, theorem, corollary)
- **depends** — direct dependencies, add-only during formalization

## File Structure

```
vault/3-formalization/ASN-NNNN/
  S0.yaml          ← metadata: label, name, type, depends
  S0.md            ← body: statement + justification + proof + formal contract
  S1.yaml
  S1.md
  _preamble.md     ← structural (no YAML pair)
  _cache.json      ← hash cache (not git-tracked, delete to force re-run)
  reviews/         ← review artifacts (timestamped)
```

The `.yaml` is the metadata source of truth. The `.md` is what the LLM reads and writes. Scripts read metadata from YAML, pass body as markdown to the LLM.

## Why Per-Property Formalization Converges

The per-property constraint is architectural. Each property is formalized independently — its dependencies are immutable context. This is like solving a system of equations one variable at a time with the others fixed. It converges. Multi-property formalization would be like solving them all simultaneously — it can oscillate.

In discovery, the whole ASN is the context and converges because the full picture constrains it. When you split into smaller pieces (per-property), each piece has room to improve independently, and those improvements can cascade — fix S7a, now S7 needs updating, now S8 references S7 differently. Without a fixed boundary (your dependencies are immutable), refinement never stops.

The per-property constraint prevents infinite refinement. Cross-review is the escape valve for the issues that per-property can't catch (carrier-set conflation, precondition chain gaps, circular reasoning across properties). Per-property handles 95% fast. Cross-review handles the 5% that needs a wider view.
