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

## Tooling

```bash
# Auto-detection within cross-review (fires when pattern is found)
python scripts/cross-review.py 36 --max-cycles 5

# Force a specific apex (skip detection, go straight to cone review)
python scripts/cross-review.py 36 --cone S8
```

Detection parameters: window of 5 cross-review commits, threshold of 3+ apex touches with dependencies at less than half. The window uses only cross-review commits for the specific ASN (path-filtered git log).

## Origin

Discovered during ASN-0036 formalization, reviews 60-65. S8 (FiniteCorrespondenceRunDecomposition) was touched in 4 of 6 consecutive cross-review commits while its 7 dependencies were touched 0-1 times. The cross-review had already converged the loosely coupled properties (S7, ValidInsertionPosition, S3) in earlier rounds — what remained was the tightly coupled S8 core.
