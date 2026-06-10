# Review of ASN-0119

This is a careful, largely sound note. The arithmetic in both worked examples checks out under inspection (I verified the pivot `A B C D E ↦ A C D E B` and the swap `A B C D E F ↦ A E F C D B` against R-P*/R-S*, the `π` table against the destination equations, and all four RA7c footprint outcomes). The S3★ derivation through `π⁻¹` is genuine work rather than a checkmark, the boundary analysis (empty subspace, single position, empty exterior as a vacuous branch) is real, and the non-trivial wp case (footprint contiguity) is correctly isolated and exhibited in four sub-cases. The findings below are a completeness gap and an anti-bloat trim, not correctness errors.

## REVISE

### Issue 1: Invariant-preservation ledger omits S8★, the one value-dependent invariant REARRANGE actually transforms

**ASN-0119, "What is preserved: I-address correspondence"** (the contiguity paragraph): "Every reachable-state invariant that constrains this set alone is therefore inherited verbatim from the pre-state, **none of them mentioning the values `M(d)(v)` that `π` reshuffles**. Concretely: ... D-CTG★ ... D-SEQ★ ... D-MIN★ ... S8a ... S8-depth ... and finiteness (S8-fin) ... We may now read off the remaining obligations."

**Problem**: The note discharges the two value-dependent invariants that need real argument — S2 (functionality) and S3★ (referential integrity) — and the six key-set invariants by verbatim inheritance. But S8★ (PerSubspaceSpanDecomposition), a per-state conjunct of ASN-0047's ExtendedReachableStateInvariants, is never discharged anywhere in the note. By the paragraph's own scoping ("none of them mentioning the values"), the inheritance argument *cannot* reach S8★, since S8★ constrains the run decomposition — a function of the values `M(d)(v)`, not the key set. And REARRANGE is precisely the operation that *changes* that decomposition: a content subspace that was one maximal run before a pivot (e.g. `[1..5]` mapping to sequential I-addresses) fragments into several runs afterward. Asserting that S8★ still *holds* (a unique maximal-run decomposition still exists) therefore requires a positive argument the note does not give, while its enumerate-and-discharge method ("read off the remaining obligations") implies a completeness it does not have. The link-subspace value-dependent invariants (CL-OWN, CL-UNIQ) are preserved trivially by the frozen frame, so they need no separate treatment — S8★ is the lone genuine omission.

**Required**: Add S8★ to the preserved-invariant ledger with an explicit discharge. The fix is one line: ASN-0084's R-BLK (RunDecompositionTransformation) and R-CANON (CanonicalityOfMergeNormalForm) already establish that the post-state `M'(d)` admits the unique maximal-run partition guaranteed by S8 — i.e. S8★ on the content subspace — so cite them.

### Issue 2: Defensive proof-method justification in the Links section (anti-bloat)

**ASN-0119, "Links"** (paragraph following the RA7a biconditional): "This inline derivation rests on the bijection equation RA1 and holds for *every* REARRANGE, which is why we give it rather than cite ASN-0098's LP11 (ReorderingBijection). The relationship is worth stating precisely. A *non-trivial* REARRANGE_K meets all five of K.μ~'s admissibility conditions ... A *trivial* REARRANGE_K ... lies outside LP11's hypothesis. REARRANGE itself is ASN-0084's atomic primitive ... the RA1-based derivation covers the non-trivial and trivial branches alike, including the no-op a bare LP11 citation cannot."

**Problem**: This ~130-word passage does not advance the RA7a derivation, which is the self-contained four-line biconditional immediately above it. It is meta-commentary defending a methodological choice — *why* the note derives RA7a from RA1 instead of citing LP11 — combined with a re-elaboration of the REARRANGE-vs-K.μ~ atomicity distinction already established in the intro ("distinct from and not reducible to ASN-0047's own non-atomic K.μ~ composite (a K.μ⁻ + K.μ⁺ pair that necessarily passes through a content-removed intermediate)..."). Under the active `review-mode.anti-bloat` classifier this is two flagged patterns at once: prose that "explains why [a choice was made] rather than what it says," and "two paragraphs in the same document say the same thing in different words." A reader following the RA7a argument must skip past it.

**Required**: Cut to a brief clause noting the derivation is via RA1 so it also covers the trivial no-op (which is no K.μ~), and let the intro carry the atomicity distinction. The K.μ~ relationship is genuinely *used* only at RA8b (the observable intermediate); it does not need a second full treatment here.

## OUT_OF_SCOPE

### Topic 1: Cross-document boundary-hood under transclusion (Open Question 1)
**Why out of scope**: The question of what REARRANGE must guarantee when a cut resolves to an I-address interior to *another* document's independent arrangement is correctly deferred. It concerns transclusion semantics (COPY territory) and the interaction of two documents' cut frames — new ground, not a defect in this single-document operation. The note's RA9 isolation guarantee already settles the only obligation in scope (other documents are inert). The remaining open questions (concurrent unserialized rearrangements, discovery-index invariants under fragmentation, prior-arrangement recoverability) are likewise appropriately future.

VERDICT: REVISE
