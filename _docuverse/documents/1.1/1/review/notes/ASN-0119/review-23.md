# Review of ASN-0119

I checked the imported REARRANGE_K postconditions against ASN-0084 (R-PIV/R-SWP, R-RI, R-PPERM/R-SPERM, R-COMM, R-BLK, R-CANON), verified the worked pivot and swap arithmetic, the two-move composite's `π₂ ∘ π₁ = π` identity, the four contiguity sub-cases, and the invariant-preservation triage (key-only invariants inherited verbatim; S2/S3★/S8★ separately derived; C/E/R/L frames). The core reasoning is sound and deep — the S3★ derivation through `π⁻¹`, the J0/J1★/J1'★ vacuity, P4★ via content-subspace range invariance, and the RA8a/RA8b atomicity witness all hold. Two issues remain.

## REVISE

### Issue 1: LP3 cited for coverage invariance, but LP3 is a transition lemma that did not consider REARRANGE
**ASN-0119, "Links" (RA7a derivation)**: "Coverage is a property of the endset's spans alone (ASN-0098, LP3 — coverage invariance), and the operation freezes the link store (RA6: Σ'.L = Σ.L), so coverage(a, i) is one fixed address set across the transition."

**Problem**: ASN-0098's LP3 is established (via LP2, SlotInvariance) by case analysis over ASN-0098's transition vocabulary — K.α, K.λ, the K.μ family, K.ρ, K.δ. REARRANGE_K is a primitive introduced in *this* ASN and post-dates ASN-0098, so it is not among the transitions LP3's proof ranged over; LP3 cannot be invoked to establish coverage invariance *under REARRANGE*. This is exactly the objection the note itself raises one sentence later to decline LP11: "REARRANGE_K is not K.μ~, and LP11 is a lemma about K.μ~ transitions." LP3 is equally a lemma over transitions that did not include REARRANGE — the note applies the correct principle to LP11 and violates it for LP3 in the same paragraph. Separately, the premise actually needed ("coverage is a property of the endset's spans alone") is ASN-0098's *Definition — Coverage*, not LP3, which is a downstream *consequence* of that definitional property combined with link-store invariance.

**Required**: Attribute the premise to the coverage Definition (coverage is a function of the endset alone) and carry invariance through RA6 directly: `Σ'.L = Σ.L ⟹ Σ'.L(a).eᵢ = Σ.L(a).eᵢ ⟹ coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)`. This is self-sufficient and consistent with the note's own re-derivation of RA7a in place of LP11. Drop or correct the LP3 citation.

### Issue 2: "the contiguity outcomes are therefore four" — count does not follow, and overstates exhaustiveness
**ASN-0119, "Links" (contiguity analysis)**: "Run structure is preserved *within* a region; *across* regions a seam can heal contiguity ... or break it ... The contiguity outcomes are therefore four, and we exhibit one of each..."

**Problem**: The stated within/across analysis yields three categories (within-preserved, across-heal-preserved, across-break), and the contiguity *outcomes* themselves are two (preserved, broken). "Therefore four" does not follow from the preceding reasoning; the fourth arises only by splitting "break" into two illustrative configurations (fixed-exterior + relocated block; partially-covered block) — a distinction the within/across logic never introduces. Nor are the four an exhaustive taxonomy: a footprint spanning three or more regions (e.g. exterior + α + β) falls under none of them. The exhaustiveness phrasing claims more than the examples establish.

**Required**: Drop "therefore four"; present the cases as representative illustrations of the two outcomes (preserved / broken), not as a closed enumeration. The concrete worked examples are valuable and should stay — only the counted-outcome framing is the defect.

## OUT_OF_SCOPE

None. The five Open Questions correctly route cross-document transclusion boundary-hood, concurrent rearrangement serialization, the discovery-index/fragmentation relation, prior-arrangement recoverability (versioning), and the closed-form displacement guard to future ASNs. The RETRIEVE mention in the atomicity section is a thought-experiment about observability, not a claim defined on RETRIEVEV, so it is not a scope violation.

VERDICT: REVISE
