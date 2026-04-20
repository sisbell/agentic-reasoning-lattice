# Guide: Formalization V-Cycle

*Updated 2026-04-14.*

## Overview

Formalization transforms per-claim file pairs from blueprinting into rigorously proven specifications with formal contracts. Each claim is formalized independently — its dependencies are immutable context. See [why this converges](#why-per-claim-formalization-converges).

The V-cycle operates at three scales, inspired by multigrid methods (Brandt 1977):

- **Local scale** — local-review, contract-review. One claim at a time, dependencies fixed.
- **Regional scale** — regional-sweep. A tightly coupled group of claims reviewed together.
- **Full scale** — full-review. The entire note reviewed at once.

These compose into a V-cycle: upward through scales (local → regional → full), then downward to re-verify anything that changed.

## Stages

### Formalize

Rewrites every non-definition, non-axiom claim's proof to Dijkstra standard and produces formal contracts (preconditions, postconditions, invariants, frame conditions).

- Reads `type` from each claim's `.yaml` to filter candidates (skips axioms, design-requirements, definitions)
- Processes claims in dependency order (topological sort from `depends` fields)
- Processes each dependency level in parallel
- Auto-commits after each dependency level

### Claim-Scale Review

**Local review** — For each claim, sends the body + dependency context to the LLM. Checks logical gaps, unjustified steps, missing cases, dependency correctness, formal contract completeness. On FOUND, a reviser agent edits the `.md` file. If new dependencies are discovered, the reviser adds them to the `.yaml` depends list (add-only).

**Contract review** — Validates that each formal contract matches the proof. On MISMATCH, rewrites the contract. Vocabulary context is aggregated from all claim YAMLs automatically.

### Cluster-Scale Review: Regional Sweep

**Regional sweep** — Walks the dependency graph bottom-up. For each claim with enough same-note dependencies, assembles the full dependency cone (apex + all direct dependents) and runs a focused review/revise loop with the entire cone as context.

Per-claim review stalls on tightly coupled claims — one claim keeps getting revised while its dependencies sit stable. This is a [dependency cone](../patterns/dependency-cone.md). The regional sweep detects these clusters and reviews them as a unit. The loop runs until the reviewer finds no issues or max cycles is reached.

### System-Scale Review: Full-Review

**Full-review** — Reads the entire assembled note (all claims) + foundation statements. Finds issues that narrower scales can't catch: carrier-set conflation, precondition chain gaps, circular reasoning across claims. Reviser agent can edit multiple `.md` files and update `.yaml` depends (add-only).

### V-Cycle Orchestrator

Composes all three scales into a single upward-downward pass:

1. **Upward pass:** local review → contract review → regional sweep → full-review
2. **Dirty set detection:** after full-review, check which claims changed via git diff
3. **Downward pass:** for any changed claims, run regional review on affected cones, then re-run proof and contract review on the changed claims

The downward pass fires on ANY change during the upward pass. Each scale handles the errors it is efficient at.

### Summarize

Generates 1-3 sentence summaries for claim YAML files. These summaries populate the `summary` field in each `.yaml` and are used by assembly and foundation loading. Run this before assembly. Hash caching skips unchanged claims.

### Assembly

Mechanical, no LLM. Reads YAML summaries + .md formal contracts and writes two export files in `lattices/xanadu/manifests/ASN-NNNN/`:

- `formal-statements.md` — summary + formal contract per claim, in dependency order
- `dependency-graph.yaml` — structured dependency data for discovery and rebase

Requires summaries to exist (run summarize first). Milliseconds, not minutes.

### Foundation Loading

Downstream notes load foundation dependencies directly from per-claim YAML (summary) + .md (formal contract) files. No export gate — if the per-claim files exist and have summaries, they can be loaded.

## Caching

Hashes are stored in `_cache.json` (not git-tracked). The hash covers both `.md` and `.yaml` content — changes to either invalidate the claim and its dependents.

- Delete `_cache.json` to force a full re-run
- Unchanged claims are skipped automatically
- When a claim changes, its downstream dependents are added to the dirty set

## Dependency Management

Dependencies are tracked in per-claim `.yaml` files under the `depends` field.

- **Add-only**: when a proof revision introduces a new dependency, the reviser adds it. Existing dependencies are never removed by automation.
- **Why add-only**: extra dependencies are cosmetic noise (unnecessary import). Missing dependencies are dangerous (build failures, hidden gaps). The asymmetry is intentional.
- **Manual removal**: if a dependency is genuinely wrong, remove it manually from the `.yaml` file.
- **Cross-note deps**: resolved mechanically by scanning upstream note formalization directories for matching labels.

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
lattices/xanadu/formalization/ASN-NNNN/
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

## Why Per-Claim Formalization Converges

The per-claim constraint is architectural. Each claim is formalized independently — its dependencies are immutable context. This is like solving a system of equations one variable at a time with the others fixed. It converges. Multi-claim formalization would be like solving them all simultaneously — it can oscillate.

Per-claim handles independent claims fast. When tightly coupled claims stall single-claim review, a [dependency cone](../patterns/dependency-cone.md) is the signal — one apex claim thrashing against stable dependencies. The regional sweep widens context to the cluster and resolves it with focused attention. Full-review catches what both narrower scales miss — gaps between distant claims that only show up at full-note scope.

The three scales compose: local scale handles 80% fast, regional scale handles 15% that needs coupling context, full scale handles 5% that needs the full picture. The V-cycle iterates until all three scales converge.

See [Review V-Cycle](../design-notes/review-v-cycle.md) for the theoretical grounding and multigrid analogy.
