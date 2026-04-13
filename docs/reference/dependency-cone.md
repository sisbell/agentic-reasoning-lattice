# Dependency Cone

A dependency cone is a convergence bottleneck in cross-review where one property (the apex) keeps getting revised while its dependencies are stable.

## Shape

The apex sits atop a set of dependencies in the DAG. The dependencies are correct and stable — they stopped changing. The apex keeps getting patched because each per-finding fix adjusts one seam with its neighbors, which shifts another seam, which the next review flags.

```
        S8          ← apex (thrashing)
       / | \
  S8-fin S8a D-CTG  ← stable foundations
    |     |    |
   ...   T4  S8-depth
```

## Detection

Mechanical, from git history:

1. Count property file touches in the last N cross-review commits for this ASN
2. The most-touched property is the candidate apex
3. If the apex has >= 3 touches and its dependencies have < half that, it's a cone

```bash
# Auto-detection happens within cross-review
python scripts/cross-review.py 36 --max-cycles 5

# Force a specific apex
python scripts/cross-review.py 36 --cone S8
```

## Why per-finding revision fails

Cross-review finds: "S8 is missing D-CTG in its dependency list." The reviser fixes S8.md but not S8.yaml. Next review finds: "S8's contract cites S8-depth but doesn't list it as a precondition." The reviser adjusts the contract. Next review finds another seam.

Each fix is correct in isolation. But the reviser only sees one finding at a time — it never sees the full picture of what the apex needs to reconcile across all its inputs.

## Resolution

When a cone is detected, cross-review switches to a focused loop:

1. Assemble just the cone (apex + same-ASN dependencies)
2. Load only the cross-ASN foundation labels the cone references
3. Run the same cross-review prompt with this narrower context
4. Revise findings — the reviser can now make coordinated fixes
5. Loop until the cone converges, then return to full cross-review

The narrower context means the reviewer focuses entirely on the constraint system instead of scanning 29 properties and finding scattered issues. For ASN-0036, this reduced the review context from ~90K to ~37K characters.

## When it fires

The cone pattern appears after cross-review has converged the loosely-coupled properties. What remains is the tightly-coupled core — typically a complex theorem that depends on many stable foundations. The per-property convergence approach (solving one equation at a time) works for loose coupling but stalls on tight coupling.

## Discovered

ASN-0036 cross-review, reviews 60-65. S8 (FiniteCorrespondenceRunDecomposition) was touched in 4 of 6 consecutive cross-review commits while its 7 dependencies were touched 0-1 times.
