# Review of ASN-0117

## REVISE

### Issue 1: LP3★ is mischaracterized and redundant in the link-survival argument

**ASN-0117, §"Invariants...Link survival" (P4 body)**: "the endset stored at each link slot has unchanged coverage across the (possibly two-step) transition: `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)` (**LP3★ ...**). Coverage is a state-independent property of an endset value (ASN-0098); the content of LP3★ is that the *stored* endset `Σ.L(a).eᵢ` itself does not change, which L12 forbids."

**Problem**: Two faults.
(a) *Mischaracterization of a foundation lemma.* LP3★ (ASN-0098) states coverage invariance, `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)` — nothing more. It does **not** assert "the stored endset itself does not change"; coverage is explicitly lossy (two distinct endsets can share coverage). The claim that "the content of LP3★ is that the stored endset itself does not change" is L12's content (value immutability), not LP3★'s. The ASN attributes L12's guarantee to LP3★.
(b) *Redundancy.* DELETE's own contract clause DEL-LIMM establishes `Σ'.L = Σ.L` in both domain and value, and this is derivable directly from the component frames (`L' = L` in both K.μ⁻ and K.μ⁺, ASN-0047). Once `Σ'.L = Σ.L`, then `Σ'.L(a) = Σ.L(a)` and coverage invariance is immediate in one line. Invoking LP3★ (and the single-step LP3 for the `R = ∅` case, and contrasting with L12) is wholly subsumed by DEL-LIMM. These foundation lemmas exist for settings where the link store *can* grow; DELETE forbids that, so the apparatus is accreted citation around a fact DEL-LIMM already delivers.

**Required**: State coverage invariance as a one-line corollary of DEL-LIMM (`Σ'.L = Σ.L ⟹ Σ'.L(a) = Σ.L(a) ⟹ coverage unchanged`). Drop the LP3★/LP3/L12 chain, or if LP3★ is retained, describe it correctly (coverage invariance) rather than as value invariance. Collapse the duplicated "stronger than L12" comparison (it appears in both the Frame section and P4).

### Issue 2: LP16 cited where LP12 is the operative lemma

**ASN-0117, §"Invariants...Link survival" (P4) and §"A worked deletion" (cross-document transclusion)**: "remains discoverable from every other document that still arranges its coverage (foundation LP16 (TransclusionDiscoverability), ASN-0098)"; and "stays discoverable from `d'` ... since `coverage(eᵢ) ∩ ran(M'(d')) = coverage(eᵢ) ∩ ran(M(d')) ≠ ∅` is untouched (LP16, TransclusionDiscoverability)".

**Problem**: LP16's implication has premise `coverage ∩ ran(M(d_src)) ∩ ran(M(d_new)) ≠ ∅` — a *two-document, shared-address* condition. The fact actually used — "discoverability from `d'` turns solely on `coverage ∩ ran(M(d'))`" — is LP12 (DiscoverabilityCharacterisation), a single-document characterisation. In the cross-document example the deleted addresses `a_3, a_4` are no longer in `ran(M'(d))`, so LP16's triple-intersection premise *fails* at the post-state; the conclusion holds purely by LP12 applied to `d'` together with P5 (`ran(M'(d')) = ran(M(d'))`). LP16 does not apply post-deletion.

**Required**: Cite LP12 for single-document discoverability of `d'`; reserve LP16 for a genuine two-document shared-address claim if one is intended.

## OUT_OF_SCOPE

### Topic 1: Deletion from text subspaces of depth m > 2
**Why out of scope**: The operation fixes `m = #p = 2` in its precondition, inheriting the depth-2 limit of the contraction foundation (ASN-0082). S8a permits `m ≥ 2`, so documents with deeper text arrangements cannot be deleted from under this contract. Generalizing requires first extending ASN-0082's contraction beyond depth 2 — new foundation territory, not an error in this ASN.

VERDICT: REVISE
