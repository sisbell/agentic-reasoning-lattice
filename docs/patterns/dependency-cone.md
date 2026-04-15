# Dependency Cone

## Pattern

Per-property iterative refinement decomposes a system into independent units and converges each one separately. This works when properties are loosely coupled — fix one, move on. But some properties form tightly coupled constraint systems where each unit's correctness depends on precise alignment with its neighbors. Fixing one seam shifts another. The decomposition that enables convergence for most properties creates a bottleneck for the coupled ones.

A dependency cone is the specific shape this bottleneck takes: one property (the apex) depends on many others that are individually correct and stable. The apex keeps getting revised because no single fix can reconcile all its inputs at once.

## Structure

```
        S8          ← apex (thrashing)
       / | \
  S8-fin S8a D-CTG  ← stable foundations
    |     |    |
   ...   T4  S8-depth
```

The dependencies form a DAG, not a cycle. The foundations converged early — they're simple, loosely coupled properties that per-property refinement handles well. The apex is a complex property that must reconcile all of them simultaneously. Each per-finding fix adjusts one seam with one neighbor, which shifts another seam, which the next review flags.

## Cause

The per-property constraint that drives convergence for loosely coupled properties prevents it for tightly coupled ones. When a property has N stable dependencies and its proof must reference all of them consistently — correct dependency lists, accurate contracts, precise cross-references — fixing one inconsistency at a time can't reach a global solution. The reviser sees one finding but never the full picture.

This is analogous to iterative methods for solving systems of equations. Gauss-Seidel iteration (one variable at a time) converges when the system is diagonally dominant (loose coupling). For tightly coupled systems, direct solution (simultaneous treatment) is needed.

## Detection

The pattern is detectable mechanically from revision history:

1. One property has significantly more touches than its dependencies in recent review commits
2. Its dependencies have low or zero touch counts in the same window
3. The pattern persists across multiple review cycles

The asymmetry — apex thrashing, dependencies stable — distinguishes a cone from general non-convergence where multiple properties are all changing.

## Resolution

Narrow the scope to the coupled set and resolve it as a unit:

1. Assemble the apex and its same-ASN dependencies as a single context
2. Load only the cross-ASN foundation labels the cone references
3. Review the cone as a constraint system — "are these jointly consistent" rather than "find any issue in the full ASN"
4. Revise with all cone properties visible, enabling coordinated fixes
5. Once the cone converges, resume full-ASN review to verify nothing broke

The narrower context focuses the reviewer on the constraint system instead of scattering attention across unrelated properties. For ASN-0036, this reduced review context from ~90K to ~37K characters.

## Resolution stages

When a cone is resolved through focused review, the findings progress through distinct stages. Each stage only becomes visible after the previous one is resolved — you can't see mathematical precision issues until the citations are correct, and you can't see structural organization until the proofs are complete. The cone peels layers.

**Stage 1: Citation accuracy.** Wrong foundation properties cited. Missing preconditions in contracts. Different names used for the same operation. These are surface issues — the proof is right but the references are wrong.

*Observed: TumblerAdd→OrdinalShift, missing T3/GlobalUniqueness/S7c in contracts, shift/inc equivocation.*

**Stage 2: Completeness.** Missing axioms that proofs assume without stating. Undeclared dependencies. Missing guards on postconditions that fail at boundary values. The proof has gaps.

*Observed: AX-1 (initial state), S7d (document allocation), D-CTG missing from S8 depends, D-MIN guard at m≥2.*

**Stage 3: Structural coherence.** Axioms scoped too narrowly. Proof structures that don't match what they're trying to show. Narrative and formal content inconsistent.

*Observed: AX-1 expanded to cover content store, S5 rewritten from isolated-state to execution-trace model, S3 pre-state/post-state formula inconsistency.*

**Stage 4: Mathematical precision.** Unstated assumptions about the domain. Properties that are derivable but asserted as axioms. Proofs that claim a specific scope when the argument is more general.

*Observed: natural-number discreteness unstated, S8-vdepth promoted from design requirement to theorem, subspace-universal scope in VIP narrowed to "text-subspace."*

**Stage 5: Structural organization.** Phantom dependencies. Redundant properties whose postconditions duplicate other properties. Mathematical insights about edge cases.

*Observed: phantom dependencies (referenced but not stated), D-CTG postcondition duplicating D-CTG-depth, VIP empty-case insight (infinitely many mutually exclusive valid positions).*

## Leads to

[Scope narrowing](scope-narrowing.md) — the cone is resolved by narrowing to the cluster and applying [review/revise iteration](review-revise-iteration.md) with focused context. The stages above are what the review/revise cycle finds at each layer.

[Verification V-Cycle](../design-notes/verification-v-cycle.md) — the multi-scale architecture that emerged from the cone problem. Property, cluster, and system scales composed into an upward-downward pass, each handling the error class it is efficient at.

## Origin

Discovered during ASN-0036 formalization, reviews 60-65. S8 (FiniteCorrespondenceRunDecomposition) was touched in 4 of 6 consecutive cross-review commits while its 7 dependencies were touched 0-1 times. The cross-review had already converged the loosely coupled properties (S7, ValidInsertionPosition, S3) in earlier rounds — what remained was the tightly coupled S8 core.
