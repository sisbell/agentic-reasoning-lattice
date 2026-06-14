# Review of ASN-0131

I checked all 18 introduced claims (RE-DEF through RE-CWP) for correctness, the worked example, the boundary cases (RE-BND), the soundness/completeness biconditional, the union/intersection algebra, and the full stability analysis. The mathematics is sound: the `Avail(Σ)` factoring underwriting RE-UDIST is correct, the two-counterexample argument in RE-UDIST-∩ (non-injective and injective) genuinely forecloses an arrangement-restriction fix, the RE-CWP weakest precondition correctly reduces to "nothing dropped" with the right `R = ∅` boundary, RE-RET's sole-bearer iff is discharged both directions via R6a and R-Scope, and the `Σ.L`-evolution bridge legitimately carries the ASN-0086 lemmas into the ASN-0047 state space. The conditional results (RE-ADDR, RE-RET) have their hypotheses flagged, the foundation citations are accurate, and no non-foundation ASN is cited in a load-bearing way. The scope is respected — image/discovery machinery is cited from ASN-0127, not rebuilt.

The findings below are confined to the anti-bloat patterns the `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: Use-site inventory and placement justification in the RE-ADDR section opener
**ASN-0131, "Fresh emissions and the addressable population"**: "One structural fact about the addressable population is needed repeatedly below — in composing regions (RE-UDIST-∩) and again under emission and retraction (RE-RET) — so we record it here, with that population freshly in view."
**Problem**: This single sentence carries two of the named accretion patterns at once. It is a *use-site inventory* — it enumerates downstream consumers (RE-UDIST-∩, RE-RET) rather than advancing RE-ADDR's content — and a *document-ordering justification* ("so we record it here, with that population freshly in view"). The reader must skip past both before reaching the actual structural fact, which begins only at "A `K.λ` step emits a *fresh* link…".
**Required**: Open the section with the substance (the `K.λ` freshness argument leading to RE-ADDR). The fact that RE-ADDR is reused at RE-UDIST-∩ and RE-RET is already established by those claims citing it at their own sites; it does not need to be pre-announced here.

### Issue 2: Opener/closer restate the same "two motions" framing
**ASN-0131, "Stability" section opener**: "…its stability is entirely determined by how state changes move the two things it reads: the region's image and the addressable population."
**ASN-0131, "Under retraction" closer**: "The answer's stability thus reduces to two tracked motions: the region's image under editing (RE-EDIT, with RE-CWP the exact contraction sub-case) and the active population under emission and retraction (RE-RET)."
**Problem**: The two sentences state the same decomposition — stability = image-motion + population-motion — in different words, bracketing the section. The closer's only added content over the opener is the mapping to claim labels.
**Required**: Drop the redundant "two things/motions" restatement. If the claim-label mapping in the closer is wanted, keep only that mapping and let the opener carry the "image + population" framing once.

## OUT_OF_SCOPE

None. The note correctly cites ASN-0127's image and existence/discovery machinery rather than re-deriving it, withholds link identities (RE-UNIT) rather than enumerating them, and routes genuinely new territory (whole-vs-touching-span extent, multiplicity, rendered answers, the structural intersection-equality condition, cross-store completeness, type-slot/content matches, link-subspace regions) into its Open Questions rather than into claims.

VERDICT: REVISE
