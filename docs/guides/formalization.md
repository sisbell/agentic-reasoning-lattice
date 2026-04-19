# Guide: Formalization V-Cycle

*Updated 2026-04-14.*

## Overview

Formalization transforms per-property file pairs from blueprinting into rigorously proven specifications with formal contracts. Each property is formalized independently — its dependencies are immutable context. See [why this converges](#why-per-property-formalization-converges).

The V-cycle operates at three scales, inspired by multigrid methods (Brandt 1977):

- **Property scale** — proof review, contract review. One property at a time, dependencies fixed.
- **Cluster scale** — cone sweep. A tightly coupled group of properties reviewed together.
- **System scale** — full-review. The entire ASN reviewed at once.

These compose into a V-cycle: upward through scales (property → cluster → system), then downward to re-verify anything that changed.

## Stages

### Formalize

Rewrites every non-definition, non-axiom property's proof to Dijkstra standard and produces formal contracts (preconditions, postconditions, invariants, frame conditions).

- Reads `type` from each property's `.yaml` to filter candidates (skips axioms, design-requirements, definitions)
- Processes properties in dependency order (topological sort from `depends` fields)
- Processes each dependency level in parallel
- Auto-commits after each dependency level

### Property-Scale Review

**Proof review** — For each property, sends the body + dependency context to the LLM. Checks logical gaps, unjustified steps, missing cases, dependency correctness, formal contract completeness. On FOUND, a reviser agent edits the `.md` file. If new dependencies are discovered, the reviser adds them to the `.yaml` depends list (add-only).

**Contract review** — Validates that each formal contract matches the proof. On MISMATCH, rewrites the contract. Vocabulary context is aggregated from all property YAMLs automatically.

### Cluster-Scale Review: Cone Sweep

**Cone sweep** — Walks the dependency graph bottom-up. For each property with enough same-ASN dependencies, assembles the full dependency cone (apex + all direct dependents) and runs a focused review/revise loop with the entire cone as context.

Per-property review stalls on tightly coupled claims — one property keeps getting revised while its dependencies sit stable. This is a [dependency cone](../patterns/dependency-cone.md). The cone sweep detects these clusters and reviews them as a unit. The loop runs until the reviewer finds no issues or max cycles is reached.

### System-Scale Review: Full-Review

**Full-review** — Reads the entire assembled ASN (all properties) + foundation statements. Finds issues that narrower scales can't catch: carrier-set conflation, precondition chain gaps, circular reasoning across properties. Reviser agent can edit multiple `.md` files and update `.yaml` depends (add-only).

### V-Cycle Orchestrator

Composes all three scales into a single upward-downward pass:

1. **Upward pass:** proof review → contract review → cone sweep → full-review
2. **Dirty set detection:** after full-review, check which properties changed via git diff
3. **Downward pass:** for any changed properties, run cone review on affected cones, then re-run proof and contract review on the changed properties

The downward pass fires on ANY change during the upward pass. Each scale handles the errors it is efficient at.

### Summarize

Generates 1-3 sentence summaries for property YAML files. These summaries populate the `summary` field in each `.yaml` and are used by assembly and foundation loading. Run this before assembly. Hash caching skips unchanged properties.

### Assembly

Mechanical, no LLM. Reads YAML summaries + .md formal contracts and writes two export files in `vault/project-model/ASN-NNNN/`:

- `formal-statements.md` — summary + formal contract per property, in dependency order
- `dependency-graph.yaml` — structured dependency data for discovery and rebase

Requires summaries to exist (run summarize first). Milliseconds, not minutes.

### Foundation Loading

Downstream ASNs load foundation dependencies directly from per-property YAML (summary) + .md (formal contract) files. No export gate — if the per-property files exist and have summaries, they can be loaded.

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
summary: Every address, once allocated, persists in all future states.
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
- **summary** — 1-3 sentence summary, generated by summarize.py
- **depends** — direct dependencies, add-only during formalization

## File Structure

```
vault/3-formalization/ASN-NNNN/
  S0.yaml          ← metadata: label, name, type, summary, depends
  S0.md            ← body: statement + justification + proof + formal contract
  S1.yaml
  S1.md
  _preamble.md     ← structural (no YAML pair)
  _cache.json      ← hash cache (not git-tracked, delete to force re-run)
  _summary-cache.json ← summarize hash cache
  reviews/         ← review artifacts (timestamped)
```

The `.yaml` is the metadata source of truth. The `.md` is what the LLM reads and writes. Scripts read metadata from YAML, pass body as markdown to the LLM.

## Why Per-Property Formalization Converges

The per-property constraint is architectural. Each property is formalized independently — its dependencies are immutable context. This is like solving a system of equations one variable at a time with the others fixed. It converges. Multi-property formalization would be like solving them all simultaneously — it can oscillate.

Per-property handles independent claims fast. When tightly coupled claims stall single-property review, a [dependency cone](../patterns/dependency-cone.md) is the signal — one apex property thrashing against stable dependencies. The cone sweep widens context to the cluster and resolves it with focused attention. Full-review catches what both narrower scales miss — gaps between distant properties that only show up at full-ASN scope.

The three scales compose: property scale handles 80% fast, cluster scale handles 15% that needs coupling context, system scale handles 5% that needs the full picture. The V-cycle iterates until all three scales converge.

See [Verification V-Cycle](../design-notes/verification-v-cycle.md) for the theoretical grounding and multigrid analogy.
