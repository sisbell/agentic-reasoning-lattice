# Review of ASN-0099

## REVISE

### Issue 1: Silent-projection "uniqueness" is overclaimed
**ASN-0099, "A Two-Phase Factoring" (Phase 1)**: "silent projection is the only treatment that is total over R ⊆ T for a fixed allocated document without fabricating I-addresses absent from the arrangement... silent projection is the unique total treatment whose every image is an actual arrangement image."

**Problem**: As stated, "unique" is false. The two properties cited — totality over R and "every image is an actual arrangement image" — are also satisfied by treatments that *drop* present V-positions (e.g., the constant `∅` treatment is total and vacuously emits only actual images, yet is not silent projection). The property that actually pins down silent projection is missing: it must additionally agree with `Σ.M(d)` on *every* present V-position (faithfulness/completeness on `R ∩ dom(Σ.M(d))`). Without that conjunct the uniqueness assertion does not hold.

**Required**: Either weaken the prose to "silent projection is *a* design-justified total treatment that fabricates no I-addresses," or restore the missing requirement (faithful on present V-positions) and state uniqueness against the full predicate.

### Issue 2: F13 proof stops at the per-slot condition
**ASN-0099, F13 (SetAdditive)**: "By distributivity of intersection over union, `coverage(e) ∩ (I₁ ∪ I₂) = (coverage(e) ∩ I₁) ∪ (coverage(e) ∩ I₂)`, non-empty iff at least one disjunct is non-empty."

**Problem**: The claim is a set equality on `findlinks`, whose membership predicate is an *existential over slots* `(E i : coverage(eᵢ) ∩ I ≠ ∅)`. The proof establishes only the per-slot fact; it omits the load-bearing lift `(E i : Pᵢ ∨ Qᵢ) ⟺ (E i : Pᵢ) ∨ (E i : Qᵢ)` that carries the per-slot result up to `findlinks(I₁∪I₂) = findlinks(I₁) ∪ findlinks(I₂)`. Given the explicit per-step standard the rest of this ASN holds itself to (e.g., F10a's four-step zero-count unfolding, F9-λ's full derivation), the terseness here is below the ASN's own bar.

**Required**: Add the existential-over-disjunction step that lifts the per-slot biconditional to the comprehension-level set equality.

### Issue 3: V-side additivity asserted "directly" with no derivation
**ASN-0099, F20 (ImageSetAdditive)**: "V-side additivity for `findlinks_V` then follows from F12 + F20 + F13 directly."

**Problem**: This is an unnamed derived guarantee stated as "X follows from Y + Z directly" with no steps shown — exactly the pattern the standards forbid ("'X follows from Y + Z' is not a proof, it's a claim. Show the steps."). The chain (F12 unfold → F20 image-union → F13 set-additive → F12 refold) is short but is the substance of the claim and is left to the reader.

**Required**: Either show the four-step chain explicitly, or label the consequence and give the derivation as is done for the other F-claims.

## OUT_OF_SCOPE

### Topic 1: Semantics for query I-addresses outside `dom(Σ.C) ∪ dom(Σ.L)`
**Why out of scope**: The ASN correctly lists this under "What We Have Not Specified" and "Open Questions"; it is genuinely new territory (coverage is purely combinatorial over `T`, so the operation is already total over arbitrary `I`), not an error in the present operation.

### Topic 2: Partition/replication consistency and the FOLLOWLINK inverse direction
**Why out of scope**: Inter-server propagation, consistency models, and the inverse (endset→V-position) resolution belong to future ASNs (BEBE / FOLLOWLINK), which are explicitly excluded.

VERDICT: REVISE
