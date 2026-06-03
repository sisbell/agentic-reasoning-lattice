# Review of ASN-0071

## REVISE

### Issue 1: PC-RANGE assumes every arrangement position has depth ≥ #u
**ASN-0071, *Resolution* ("Which positions resolve — cross-depth capture in general") and the PC-RANGE claim row**: "We claim, for any `v ∈ dom(M(d_s))` (depth `#v ≥ #u`): `v ∈ ⟦σ⟧ ⟺ (A j : 1 ≤ j < #u : v_j = u_j) ∧ u_{#u} ≤ v_{#u} < r_{#u}`" and the set equality `⟦σ⟧ ∩ dom(M(d_s)) = { v ∈ dom(M(d_s)) : ... ∧ u_{#u} ≤ v_{#u} < r_{#u} }`.

**Problem**: The parenthetical "(depth `#v ≥ #u`)" is presented as a fact about every `v ∈ dom(M(d_s))`, but the vspec preconditions place no relation between `#u` and the source's content-subspace depth `m_C` (S8-depth). ASN-0058's ContentReference clause (iii) `#u = m` was deliberately dropped here, so a vspec with `#u > m_C` is admissible. When `#u > m_C`, *every* arrangement position has depth `m_C < #u`, the right-hand predicate references a non-existent component `v_{#u}`, and the set-builder — which ranges over all of `dom(M(d_s))` — is ill-typed for those positions. The proof never case-splits on `#v < #u`; it simply assumes the depth bound. The set equality still holds (such positions are excluded from `⟦σ⟧` by PC's totality, and excluded from the RHS because `v_{#u}` is undefined), but that argument is exactly what is missing.

**Required**: Either state `#u ≤ m_C` as an explicit precondition of PC-RANGE, or add the case `#v < #u` and show those positions contribute to neither side (vspec anchored deeper than the source arrangement → empty resolution). The `#u > m_C` boundary should also appear as a worked or stated case, since it is the dual of the cross-depth example already exhibited.

### Issue 2: The same "coarse-coordinate reach" motif is restated three times
**ASN-0071, introduction / *Resolution* / *A worked scenario***: intro — *"A digit of 'one' may be used to designate all of a given version ... or the entire docuverse"* and "so a coarse coordinate names everything beneath it"; *Resolution* — "a shallow vspec thereby reaches every deeper arrangement position beneath the named coarse coordinate — the coarse-coordinate reach Nelson's address convention promises"; worked scenario — "The coarse shallow anchor ... discovered the full transclusion community of the subtree's content" and "Cross-depth capture, in general."

**Problem**: The single point — a shallow prefix captures the whole subtree beneath it — is asserted as motivation (intro), proven (PC-RANGE in *Resolution*), and then re-narrated twice in the example. The repeated appeal to "the coarse-coordinate reach Nelson's address convention promises" is meta-prose that does not advance the argument after PC-RANGE is established. Likewise "promised in the introduction" recurs in *Source self-inclusion* (F-SELF) and *Partial overlap suffices* ("discharge the retrieval promise framed in the introduction") — multiple sections deferring back to the same intro promise.

**Required**: State the coarse-coordinate-reach consequence once (at PC-RANGE), let the example illustrate it numerically without re-deriving the general statement, and drop the recurring "promised in the introduction" back-references.

### Issue 3: "Partial overlap suffices" restates F-find/F-PART already in the claims table
**ASN-0071, *Partial overlap suffices***: "`d ∈ find(Q)(Σ) ⟺ d ∈ Σ.E_doc ∧ (E a : a ∈ ran(Σ.M(d)) : a ∈ iaddrs(Q)(Σ))`".

**Problem**: This biconditional is a verbatim unfolding of F-find's `≠ ∅`, and is already recorded as F-PART in the Claims table ("direct from F-find (unfolding `≠ ∅`)"). The section's only non-redundant content is the "no inherent extent measure" observation. The restated biconditional plus the surrounding "The asymmetry matters ..." prose is essay padding around a claim that is one line in the table.

**Required**: Keep the extent-measure observation (and the `|ran(Σ.M(d)) ∩ iaddrs(Q)(Σ)|` note); remove the re-derivation of the F-PART biconditional, which belongs only in the table.

## OUT_OF_SCOPE

### Topic 1: Relationship between current-containment result and provenance relation R
**Why out of scope**: The ASN correctly defers this to Open Questions; `find` reads only `E_doc` and `M`, and the ever-containing relation `R` is a separate guarantee belonging to a future ASN.

VERDICT: REVISE
