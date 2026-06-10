# Review of ASN-0119

The mathematics is sound. I checked both worked instances by hand (pivot `A B C D E ↦ A C D E B` with `π = (1↦1, 2↦5, 3↦2, 4↦3, 5↦4)`; swap `A B C D E F ↦ A E F C D B` with the middle's `+1 = w_β − w_α` displacement), verified the destination ordinals tile disjointly in every case, traced the region constant-displacements off R-PPERM/R-SPERM (`β: −w_α`, `α: +w_β` for the pivot; `−(w_α+w_μ), w_β−w_α, w_β+w_μ, 0` for the swap), confirmed the RA7a biconditional chain and the S3★ inverse-permutation argument, and re-checked the two-move atomicity composite reaches `A C D E B` through the divergent intermediate `A C D B E`. All correct. The invariant discharge is genuinely complete — every conjunct of ExtendedReachableStateInvariants is accounted for, and the one value-dependent invariant (S8★) gets a positive R-BLK + R-CANON argument rather than a key-set inheritance hand-wave.

The findings below are organizational (the note carries `review-mode.anti-bloat`) plus one precision nit.

## REVISE

### Issue 1: General invariant-discharge paragraph buried in the Links section
**ASN-0119, "Links"**: "As a transition in ASN-0047's model REARRANGE allocates no content and records no provenance... The remaining ExtendedReachableStateInvariants conjuncts (P6, P7, P8, P7a, P4a, the E-family NodeLineage/ActivatedEmission, the L-family, the C-family) are preserved by the C/E/R/L frame. ASN-0047's second transition theorem, ExtendedTransitionInvariants (its sole conjunct P3...)..."

**Problem**: This is a complete general transition-invariant discharge (J0, J1★, J1'★, P4★, P3, P6, P7, P8, P7a, P4a, the E/C-families) sitting between the Question-4 footprint derivation and the Question-5 contiguity discussion. Almost none of it is link-specific — J0/J1★ are allocation–provenance couplings, P4★ is content containment, P3/P6/P7/P8 and the E/C-families are general — yet it interrupts the link narrative and duplicates the *role* of the "What is preserved" section, which already discharges S2, S3★, S8★, and the inherited text-subspace invariants. A reader tracking link guarantees must read past a wall of unrelated invariant bookkeeping; a reader auditing invariant preservation must hunt for half of it inside "Links."

**Required**: Move the J/P/E/C discharge into "What is preserved" alongside S2/S3★/S8★, so the invariant accounting lives in one place. Leave "Links" to carry only link-specific guarantees (RA6, RA7a/b/c) plus, at most, the discoverability-coupling sentence that genuinely connects to links.

### Issue 2: The same non-citation justification, stated twice with a forward cross-reference
**ASN-0119, "Links"**: "We carry this through RA6 rather than cite ASN-0098's LP3 (coverage invariance): LP3 is established by case analysis over a transition vocabulary that does not include REARRANGE_K — **the same reason we decline LP11 just below**." ... and later: "We derive RA7a inline from RA1 rather than cite ASN-0098's LP11 (ReorderingBijection): REARRANGE_K is not K.μ~, and LP11 is a lemma about K.μ~ transitions."

**Problem**: One methodological point — *ASN-0098's projection lemmas are proved over a transition vocabulary that excludes REARRANGE_K, so we re-derive their conclusions rather than cite them* — is made twice, in two places, with an explicit forward pointer ("the same reason we decline LP11 just below") whose only reason to exist is that the content recurs. This is exactly the forward-reference accretion the review mode targets: the cross-reference is the symptom, the duplicated rationale is the cause. The substantive arguments (coverage invariant via RA6; RA7a via the RA1 biconditional) each stand on their own without the "why we didn't cite X" gloss.

**Required**: State the principle once — naturally where REARRANGE is first distinguished from K.μ~ in "The two streams" — then let each inline derivation stand. Drop the cross-reference.

### Issue 3 (minor): "wp = true" is imprecise for a partial operation
**ASN-0119, "Well-definedness" / "Links"**: "Every other postcondition of this note holds unconditionally (wp = true); the footprint's contiguity is the single property REARRANGE does not preserve in general..."

**Problem**: The note itself stresses that "REARRANGE is therefore a *partial* operation: it is defined exactly where its preconditions R-PRE hold." For a partial operation the weakest precondition of any postcondition includes enabledness, so for these postconditions `wp = R-PRE`, not `true` — `wp = true` would assert the postcondition is established from *every* initial state, including those on which the operation does not apply. The shorthand contradicts the note's own careful partiality treatment one section earlier.

**Required**: Replace "wp = true" with "wp = R-PRE" (or "holds wherever the operation is defined"). The companion framing — contiguity as the one property needing a precondition, RA7c sufficient-not-necessary — is fine and should stay: the `{B,C,D,E}`-preserved vs `{B,C}`-broken pair (both crossing the same `α/β` cut, opposite outcomes) confirms the contiguity outcome is position-dependent with no simpler closed-form precondition, so settling for a sufficient condition is the right ceiling here, not a gap.

## OUT_OF_SCOPE

### Topic 1: REARRANGE at depths > 2 and in subspaces other than s_C
**Why out of scope**: The note inherits ASN-0084's REARRANGE_K scope (text subspace `s_C`, depth 2 via CS3/CS4) and explicitly disclaims the rest ("We make no claim about other subspaces or other depths"). Lifting the closed-form permutations to higher depth or other subspaces is new territory for a future note, not a defect here. The honest scoping is correct.

### Topic 2: The five Open Questions
**Why out of scope**: Cross-document boundary-hood of a cut resolving into another document's region, unserialized concurrent rearrangements, the discovery-index invariant under footprint fragmentation, prior-arrangement recoverability from the content store, and the displacement-arithmetic boundary guard are all genuine future-ASN territory and are correctly parked in "Open Questions" rather than half-answered in the body.

VERDICT: REVISE
