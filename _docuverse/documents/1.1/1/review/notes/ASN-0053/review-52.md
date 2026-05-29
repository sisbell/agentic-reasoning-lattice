# Review of ASN-0053

This is a mature, carefully-argued ASN. The core algebra (classification, intersection, merge, split, normalization, difference) is sound, every claim carries a concrete worked instance, and inverse/composition consequences are derived rather than asserted. The findings below are localized rigor gaps and one anti-bloat note — none threaten the architecture.

## REVISE

### Issue 1: S3 collapses two adjacency disjuncts without showing one is vacuous
**ASN-0053, S3 (MergeEquivalence) proof**: "Without loss of generality, assume start(α) ≤ start(β). The overlap-or-adjacency condition means reach(α) ≥ start(β)."
**Problem**: `adjacent(α, β)` has two disjuncts: `reach(α) = start(β)` and `reach(β) = start(α)`. Under the WLOG assumption `start(α) ≤ start(β)`, the second disjunct is impossible (`reach(β) = start(α) ≤ start(β) < reach(β)` gives `reach(β) < reach(β)`), so it must be excluded before "means reach(α) ≥ start(β)" follows. The proof glosses this collapse — "means" hides a step that, per the standards, should be explicit.
**Required**: One sentence noting that `reach(β) = start(α)` is vacuous under `start(α) ≤ start(β)`, leaving only `reach(α) = start(β)` (adjacency) or `reach(α) > start(β)` (overlap), whence `reach(α) ≥ start(β)`.

### Issue 2: S1 asserts the empty branch instead of deriving it
**ASN-0053, S1 (IntersectionClosure) proof**: "If r' ≤ s', the intersection is empty — this covers the separated and adjacent cases. Otherwise r' > s', and: ⟦α⟧ ∩ ⟦β⟧ = {t : s' ≤ t < r'}. We verify this equality by membership."
**Problem**: Emptiness in the `r' ≤ s'` case is asserted, and the membership argument that would justify it is presented only inside the `r' > s'` branch. The forward inclusion (`t ∈ ⟦α⟧ ∩ ⟦β⟧ ⟹ s' ≤ t < r'`) in fact holds unconditionally, so emptiness follows directly — but the proof's structure does not make that available to the `r' ≤ s'` case.
**Required**: State the forward inclusion before the case split (it is order-only), then observe that `{t : s' ≤ t < r'} = ∅` when `r' ≤ s'`. This closes the empty branch by derivation rather than assertion.

### Issue 3 (anti-bloat): use-site inventory in the reach section
**ASN-0053, reach-function section**: "Every use in this ASN is level-uniform (#a = #b), so all three conditions hold throughout."
**Problem**: This is the use-site-inventory pattern — a definition/setup paragraph pre-certifying that all downstream consumers satisfy the conditions, rather than advancing the local argument. Each claim that needs `#a ≤ #b` (S4, S5, WF, WR) already discharges level-uniformity at its own site, so this global pre-emption is redundant prose the reader must reconcile against the per-claim discharges. The preceding D0/D1/D2 distinction (round-trip can fail) is genuine reasoning and should stay; only the closing inventory sentence is noise.
**Required**: Delete the closing sentence; the per-claim level-uniformity discharges carry the burden.

## OUT_OF_SCOPE

### Topic 1: span-set difference bound (last Open Question)
**Why out of scope**: The tight bound on `|normalize(⟦Σ₁⟧ \ ⟦Σ₂⟧)|` for normalized span-sets is genuinely new territory built on S11d, not a gap in the single-span difference results stated here. Correctly left as an Open Question.

### Topic 2: cross-level intersection and allocation-stability of normalized forms
**Why out of scope**: Intersection of spans at different hierarchical levels, and preservation of normalized form under new address allocation, are dynamic/cross-level concerns. They belong to later ASNs and are properly listed under Open Questions.

VERDICT: REVISE
