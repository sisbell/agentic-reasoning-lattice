# Review of ASN-0075

## REVISE

### Issue 1: Supplementary lemma proves only one of two conjuncts per address group

**ASN-0075, "Vacuity of both report halves" — supplementary lemma (R-disjointness implies Q0)**: 

> "For any `a` with `(a, d_A) ∈ R` ... [conjunct 1 excluded]. The symmetric argument excludes `DELETED(a, d_B) ∧ CURRENT(a, d_A)` for any `a` with `(a, d_B) ∈ R`. Addresses with neither ... trivially satisfy both negations. So every `a ∈ dom(C)` falsifies both conjuncts, and `Q0` holds."

**Problem**: `Q0` requires every `a` to falsify *both* conjuncts. The proof partitions `dom(C)` into three groups (in `d_A`'s `R`-projection, in `d_B`'s, neither) but explicitly disposes of only *one* conjunct for each of the first two groups:
- For `a` with `(a, d_A) ∈ R`: conjunct 1 `[DELETED(a,d_A) ∧ CURRENT(a,d_B)]` is excluded, but conjunct 2 `[DELETED(a,d_B) ∧ CURRENT(a,d_A)]` is never addressed for this group.
- For `a` with `(a, d_B) ∈ R`: conjunct 2 is excluded, but conjunct 1 is left unshown.

The conclusion "every `a` falsifies both conjuncts" is therefore asserted, not shown. This is exactly the "you proved one case, claimed both" pattern.

**Required**: State the missing half explicitly. For `a` with `(a, d_A) ∈ R`, disjointness gives `(a, d_B) ∉ R`, so `DELETED(a, d_B)` is false (its first conjunct fails), falsifying conjunct 2 directly — no `P4★` chain needed. Symmetrically for the `(a, d_B) ∈ R` group. The conclusion holds, but each group must be shown to falsify both conjuncts.

### Issue 2: Output-half disjointness over-cites D-EXH

**ASN-0075, Definition (SHOWDELETIONS)**: "The two halves are necessarily disjoint: by D-EXH, no `a` can simultaneously satisfy `DELETED(a, d_A)` and `CURRENT(a, d_A)` ..."

**Problem**: The disjointness here is between `DeletedFromAWithB` (requires `CURRENT(a, d_B)`) and `DeletedFromBWithA` (requires `DELETED(a, d_B)`), i.e. the mutual exclusion of `CURRENT(a, d_B)` and `DELETED(a, d_B)`. That exclusion is immediate from the definitions (`a ∈ ran(M(d_B))` versus `a ∉ ran(M(d_B))`) and requires neither D-EXH nor the composite-boundary hypothesis that D-EXH carries. As written, the citation imports an unnecessary boundary dependency into a claim that is unconditionally true.

**Required**: Derive the disjointness directly from the contradictory range-membership conditions, or drop the D-EXH citation; do not route an unconditional fact through the boundary-dependent lemma.

## OUT_OF_SCOPE

### Topic 1: Multi-document and three-way deletion reporting
**Why out of scope**: The open questions about families of more than two documents and content "deleted from both but current in a third" introduce a generalized witness structure that is genuinely new territory, not a defect in the binary operation specified here.

### Topic 2: Restoration operation semantics
**Why out of scope**: D-ACT and the composability section correctly stop at showing the output is *consumable* by an address-based extension; the restoration operation itself belongs in a future ASN.

VERDICT: REVISE
