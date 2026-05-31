# Review of ASN-0047

## REVISE

### Issue 1: K.μ~ existence condition `|dom_C(M(d))| ≥ 2` is not sufficient when content positions share an I-address

**ASN-0047, *Decomposition of K.μ~* (Preconditions / sufficiency construction) and *Decomposition* (necessity argument)**: "`|dom_C(M(d))| ≥ 2` — necessary and sufficient for clause (ii) `π ≠ id` to admit a witness," with sufficiency discharged by the transposition witness `π_swap(v₁) = v₂, π_swap(v₂) = v₁`.

**Problem**: S5 (UnrestrictedSharing, ASN-0036) permits two distinct content V-positions to map to the *same* I-address (transclusion) — the ASN itself relies on this in the partial-suffix "Relation to pointwise fixity" remark. Consider a reachable state with `dom_C(M(d)) = {[1,1], [1,2]}` and `M(d)([1,1]) = M(d)([1,2]) = a`. Then `|dom_C(M(d))| = 2 ≥ 2`, but the only non-identity permutation of `dom_C` is the swap, whose net effect is `M'(d) = M(d)` (since both positions carry `a`). Clause (ii) is glossed as "a permutation whose net effect is the identity is not a K.μ~ transition (the system simply does not change)," so this swap is *not* an admissible witness — yet the sufficiency proof admits it by checking only that the *map* differs from identity (`π_swap(v₁) = v₂ ≠ v₁`), not that the *net effect* differs. Either reading is defective:
- Literal `π ≠ id` (map): K.μ~ admits no-op "reorderings," contradicting clause (ii)'s stated purpose ("real reordering").
- Net-effect reading: sufficiency fails — `|dom_C(M(d))| ≥ 2` does **not** guarantee a non-trivial witness, so the "necessary and sufficient" claim (restated again in ValidComposite★ clause (1)) is false.

**Required**: Sharpen clause (ii) to a net-effect condition and replace the existence condition with the correct one — e.g., "`dom_C(M(d))` is not constant-valued under `M(d)` and `|dom_C(M(d))| ≥ 2`," or equivalently "`M(d)|_{dom_C}` takes at least two distinct values." Fix the transposition construction to select `v₁, v₂` with `M(d)(v₁) ≠ M(d)(v₂)` (and show such a pair exists under the corrected precondition). Update the necessity argument, ValidComposite★ clause (1), and the K.μ~ verification-matrix preamble accordingly.

### Issue 2: Non-circularity / document-ordering meta-prose and verbatim repetition (anti-bloat patterns)

**ASN-0047, *Decomposition of K.μ~*, *Allocator hierarchy*, FrontierEquivalence, K.δ discharge**: Per the `review-mode.anti-bloat` directive, the following accreted patterns degrade the argument and should be removed at source:

- **Non-circularity justification as prose.** "The chain is non-circular: CL-UNIQ at the pre-state is consumed only at Step (D), so Steps (A)–(C) are independent of it"; the entire "*Well-formedness of the precondition under the outer induction*" paragraph; "The reader who encounters the precondition's necessity derivation should read 'CL-UNIQ at the pre-state' as the inductive hypothesis on Σ, not as a property whose preservation is being established." These justify ordering/non-circularity rather than advancing the claim.
- **Verbatim repetition across cycles.** The qualifier "T10a chain-advancement uniqueness at `(t, 0)` (derived from TA5(c) + P1 + precondition; see FrontierEquivalence)" — together with its parenthetical contrast against the "direct per-`(t, k')` uniqueness axiom" — is restated near-identically in FrontierEquivalence, the K.δ k=0 *Rationale*, *Freshness discharge*, the *K.δ case (ii) discharge* k=0 bullet, SubAllocatorAxiom.T10aConformance, and the S4/Link-distinctness matrix prose (≥7 occurrences). State once; cite by name thereafter.
- **Downstream-deferral chains.** "Steps (C)–(E) follow in the same order in the prose below"; "Step (E) appears in the *Decomposition* paragraph below"; the dual-consequence paragraph re-deferring to "Steps 1–3." Multiple paragraphs deferring to the same locations.

**Required**: Collapse the non-circularity meta-prose into the lemma statements' premise lists; introduce the derived-uniqueness handle once and cite by name; remove the deferral chains.

## OUT_OF_SCOPE

### Topic 1: Link V-position depth fixed at 2 while content depth is left free
**Why out of scope**: LinkVPositionDepthAxiom pins `m_L = 2` for every document, whereas the D-SEQ★ derivation accommodates content-subspace depths `m_{s_C} ≥ 3`. Whether the link subspace should also admit variable depth (and what would drive it) is a structural design question for a future operations/link-arrangement ASN, not an error in this one.

META: (none — the ASN defines state, transitions, and invariants abstractly; it has not drifted into implementation mechanics.)

VERDICT: REVISE
