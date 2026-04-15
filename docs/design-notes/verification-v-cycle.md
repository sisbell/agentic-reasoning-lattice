# Verification V-Cycle

*Design note. See [Formalization Guide](../guides/formalization.md) for the practical pipeline reference.*

## Overview

Iterative formal verification at a single scale stalls when properties are tightly coupled. Local review (one property at a time) converges fast on independent properties but can't resolve cross-property consistency. Global review (full system scan) can find cross-property issues but wastes attention on noise and converges slowly. Neither scale alone is efficient across the full range of verification problems.

The Verification V-Cycle addresses this by cycling through three scales of review, each handling the error class it's efficient at. The architecture is inspired by multigrid methods in numerical analysis (Brandt 1977), where multi-scale cycling converges faster than single-scale iteration by matching the solver to the error structure.

## Scales

**Local** — formalize, proof-review, contract-review. One property at a time, dependencies as fixed context. Fast convergence on property-level issues: logical gaps, missing cases, contract mismatches. Cannot see cross-property consistency problems.

**Regional** — cone-sweep. Reviews dependency cones: properties with many same-ASN dependencies, processed bottom-up in topological order. Narrowed context (apex + dependencies + relevant foundation only) focuses attention on the constraint system. Catches issues that span tightly coupled clusters — the [dependency cone](../patterns/dependency-cone.md) pattern.

**Global** — cross-review. Full ASN scan with complete foundation context. Finds issues invisible at narrower scales: carrier-set conflation, precondition chain gaps across unrelated properties, scope mismatches between proof and narrative. Broadest view, noisiest context, slowest convergence.

## Cycle Structure

Each pass follows an upward-then-downward path:

```
── Upward ──
  1. formalize         local     produce formal contracts
  2. proof-review      local     fix proofs
  3. contract-review   local     fix contracts
  4. cone-sweep        regional  fix clusters (bottom-up DAG walk)
  5. cross-review      global    broad scan

── Downward ──
  6. cone-review       regional  re-check cones affected by upward changes
  7. proof-review      local     re-check properties affected by steps 5-6
  8. contract-review   local     re-check contracts affected by steps 5-7
```

The upward pass builds confidence — each scale inherits a cleaner state from the one below it. The downward pass verifies — corrections from wider scales are checked at narrower scales with higher precision.

**Convergence**: when no scale changes anything in a full pass — local, regional, and global all agree that the ASN is clean.

## Why Multi-Scale Works

Each scale is efficient at a different class of verification problem:

- A missing case in a proof is caught instantly by local review but is invisible to global (buried in noise).
- A dependency cone where one property can't reconcile its many dependencies is invisible to local (each property looks correct in isolation) but caught by regional.
- A scope mismatch between a proof and its narrative claim is invisible to regional (not in any cone) but caught by global.

Single-scale iteration wastes cycles: local grinds on issues it can't resolve, global scans dozens of properties to find one issue. Multi-scale cycling routes each problem to the scale that can handle it efficiently.

## Relationship to Multigrid Methods

The Verification V-Cycle adapts the multigrid V-cycle from numerical analysis. In multigrid, iterative relaxation on a fine grid eliminates high-frequency errors quickly but stalls on low-frequency (smooth) errors. Projecting the residual to a coarser grid makes the smooth error oscillatory and therefore easy to fix. Cycling between grid levels converges in O(N) operations — optimal.

The analogy:

| Multigrid | Verification V-Cycle |
|-----------|------|
| Fine grid relaxation | Local review (proof, contract) |
| Medium grid | Regional review (cone-sweep) |
| Coarse grid | Global review (cross-review) |
| High-frequency error | Property-level issues (local inconsistencies) |
| Low-frequency error | Cross-property patterns (dependency cones) |
| Restriction | Assembling wider context |
| Prolongation | Propagating corrections to affected properties |

The V-cycle differs from classical multigrid in two ways. First, each scale runs to internal convergence before passing to the next (cascadic behavior), rather than doing a few sweeps and restricting the residual. Second, the restriction is implicit — wider context reveals what narrower context can't see, rather than an explicit residual projection. The downward verification pass is this cycle's addition — classical cascadic multigrid has no downward pass.

## Detection of Scale-Appropriate Problems

The cycle includes a mechanical detection mechanism for regional-scale problems. The [dependency cone](../patterns/dependency-cone.md) pattern identifies properties that keep getting revised while their dependencies are stable — a signal that local review is stalling on a tightly coupled cluster. Cone detection uses git revision frequency and YAML dependency metadata, with no LLM involvement.

## Origin

Developed during formalization of ASN-0036 on the Xanadu project (Strand Model, 31 properties). The flat review cycle (proof → contract → cross, repeat) ran 65+ reviews without converging on tightly coupled properties around S8 (FiniteCorrespondenceRunDecomposition). Analysis of git revision history revealed the [dependency cone](../patterns/dependency-cone.md) pattern. The cone mechanism reduced review context by 58% and produced higher-quality findings. Generalizing from reactive cone detection to proactive multi-scale cycling produced the Verification V-Cycle architecture.
