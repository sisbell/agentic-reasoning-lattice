# Guide: Claim convergence

*Updated 2026-04-25.*

## Overview

Claim convergence transforms per-claim file pairs from blueprinting into rigorously proven specifications with formal contracts. Each claim is reviewed and revised independently — its dependencies are immutable context. See [why per-claim review converges](#why-per-claim-review-converges).

Review operates at two scales:

- **Cone scale** — cone-sweep. A tightly coupled group of claims reviewed together (the [dependency cone](../patterns/dependency-cone.md): apex + its direct dependencies, with lazy expansion when the reviewer needs more context).
- **Full scale** — full-review. The entire note reviewed at once with eager 1-hop foundation context.

The [claim convergence protocol](../protocols/claim-convergence-protocol.md) defines convergence as a predicate on the link graph: every `comment.revise` targeting a claim has a matching `resolution`. Cone sweep and full-review alternate until both produce zero outstanding revise comments.

## Stages

### Converge

Rewrites every non-definition, non-axiom claim's proof to Dijkstra standard and produces formal contracts (preconditions, postconditions, invariants, frame conditions).

- Reads each claim's contract kind (axiom, theorem, lemma, corollary, definition, design-requirement) from the substrate to filter candidates (skips axioms, design-requirements, definitions)
- Processes claims in dependency order (topological sort over the `Depends:` lists in each claim's Formal Contract section)
- Processes each dependency level in parallel
- Auto-commits after each dependency level

### Cone-Scale Review: Cone Sweep

**Cone sweep** — Walks the dependency graph bottom-up. For each claim with enough same-note dependencies, assembles the full dependency cone (apex + all direct dependents) and runs a focused review/revise loop with the entire cone as context.

Per-claim review stalls on tightly coupled claims — one claim keeps getting revised while its dependencies sit stable. This is a [dependency cone](../patterns/dependency-cone.md). The cone sweep detects these clusters and reviews them as a unit. The loop runs until the predicate is satisfied for the cone or max cycles is reached.

### Full-Scale Review: Full-Review

**Full-review** — Reads the entire assembled note (all claims) + foundation statements. Finds issues that narrower scales can't catch: carrier-set conflation, precondition chain gaps, circular reasoning across claims. Reviser agent can edit multiple `.md` files; new dependencies discovered during revision are added to the claim's `Depends:` list in the Formal Contract section (add-only).

### Outer Loop

Cone sweep and full-review alternate until both produce zero outstanding revise comments. Each scale handles the errors it is efficient at; the alternation ensures cross-cone issues uncovered by full-review get resolved at the cone scale, and any new cross-cone issues introduced by cone-scale revisions get caught by the next full-review.

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

Dependencies live in each claim's markdown body under the `Depends:` bullet of the `*Formal Contract:*` section. The substrate (link store) materializes them as `citation` links; the convergence predicate and orchestrators consult the link store, not the YAML.

- **Add-only**: when a proof revision introduces a new dependency, the reviser adds it to the `Depends:` list. Existing dependencies are never removed by automation.
- **Why add-only**: extra dependencies are cosmetic noise (unnecessary import). Missing dependencies are dangerous (build failures, hidden gaps). The asymmetry is intentional.
- **Manual removal**: if a dependency is genuinely wrong, remove it manually from the markdown body.
- **Cross-note deps**: resolved mechanically by scanning upstream note claim-convergence directories for matching labels.

## YAML Metadata Format

```yaml
label: T8
name: AllocationPermanence
summary: Every address, once allocated, persists in all future states.
```

- **label** — stable key, never changes
- **name** — PascalCase, can be refined
- **summary** — 1-3 sentence summary, generated by summarize.py

The contract kind (axiom, definition, design-requirement, lemma, theorem, corollary) is recorded by the substrate as the claim's contract classifier link, not in YAML. Dependencies are recorded in the markdown body's Formal Contract section.

## File Structure

```
lattices/xanadu/claim-convergence/ASN-NNNN/
  S0.yaml          ← metadata: label, name, summary
  S0.md            ← body: statement + justification + proof + formal contract (incl. Depends)
  S1.yaml
  S1.md
  _preamble.md     ← structural (no YAML pair)
  _cache.json      ← hash cache (not git-tracked, delete to force re-run)
  _summary-cache.json ← summarize hash cache
  reviews/         ← review artifacts (timestamped)
```

The `.yaml` carries the durable identity (label, name) and the operator-readable summary. The `.md` carries the reasoning, proof, and Formal Contract — including the `Depends:` list which the substrate reads to materialize citation links. Scripts pull the body as markdown; structured queries (predicate evaluation, dependency walks) go through the link store.

## Why Per-Claim Review Converges

The per-claim constraint is architectural. Each claim is reviewed and revised independently — its dependencies are immutable context. This is like solving a system of equations one variable at a time with the others fixed. It converges. Multi-claim review would be like solving them all simultaneously — it can oscillate.

When tightly coupled claims stall narrow-scope review, a [dependency cone](../patterns/dependency-cone.md) is the signal — one apex claim thrashing against stable dependencies. The cone sweep widens context to the cluster (lazily, expanding only as the reviewer asks) and resolves it with focused attention. Full-review catches what cone-scope can't — gaps between distant claims that only show up at full-note scope.

The two scales compose: cone scale handles tightly coupled clusters with lazy expansion; full scale handles cross-cone issues with eager foundation loading. The outer loop alternates cone sweep and full-review until both find nothing to revise.

See the [Claim Convergence Protocol](../protocols/claim-convergence-protocol.md) for the formal predicate and the algorithm in pseudocode.
