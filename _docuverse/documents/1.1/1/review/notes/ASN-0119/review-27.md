# Review of ASN-0119

This is a strong, careful note. The transposition is specified by its target arrangement (not by a displacement formula), the bijection `π` is imported cleanly from ASN-0084, the worked pivot and swap check the key postconditions against explicit ordinals, the boundary cases (empty text subspace, single position, empty exterior, whole-run interval, equal-width middle) are correctly dispositioned, and the full ASN-0047 invariant package — including the genuinely value-dependent S8★ and the trace-quantified P4a — is discharged with the right level of argument rather than by frame-waving. I verified the four RA7c worked footprints, the two-pivot atomicity decomposition (RA8a/b), and the middle-region displacement `w_β − w_α` numerically; all hold. The substance is sound. The findings below are precision and pruning items.

## REVISE

### Issue 1: RA1 attributes the bijection equation to the wrong source
**ASN-0119, "What is preserved: I-address correspondence" / Claims table (RA1)**: "`M'(d)(π(v)) = M(d)(v)`, hence `ran(M'(d)) = ran(M(d))` | imported (ASN-0084 R-RI)", with the body stating "This is ASN-0084's range invariance R-RI restated."

**Problem**: RA1 bundles two facts of different provenance under one citation. The range equality `ran(M'(d)) = ran(M(d))` is indeed R-RI's key intermediate — correctly sourced. But the pointwise equation `M'(d)(π(v)) = M(d)(v)` is a *precondition* of R-RI, not a result of it: R-RI's stated preconditions assume "there exists a bijection `π` with `M'(d)(π(v)) = M(d)(v)`" and use it to derive `ran(M'(d)) ⊆ dom(C')`. The equation is *established* by ArrangementRearrangement (DEF) and the correctness clauses of R-PPERM (pivot) / R-SPERM (swap) — which the note itself already cites one row down under RA2. Attributing the equation to R-RI inverts the dependency. This matters because RA1's equation is load-bearing in the RA7a chain ("`M'(d)(π(v)) ∈ coverage(a, i)`" justified "by RA1"), so the equation must be sourced correctly at RA1, not borrowed from R-RI's hypothesis.

**Required**: Split RA1's attribution — cite ArrangementRearrangement / R-PPERM / R-SPERM (= RA2's source) for the pointwise equation `M'(d)(π(v)) = M(d)(v)`, and R-RI only for the range equality `ran(M'(d)) = ran(M(d))`.

### Issue 2: discoverability biconditional derived twice
**ASN-0119, "Links" / "Discoverability under fragmentation"**: "Because `π` is a bijection, the footprint is nonempty after exactly when it was nonempty before (immediate from RA7a) … **A link discoverable from `d` before the rearrangement is discoverable from `d` after it.** Discovery answers by address: ASN-0098's LP12 … reduces discoverability from `d` to `coverage(a, i) ∩ ran(M(d)) ≠ ∅`, and by RA1 that intersection is invariant …"

**Problem**: The biconditional "discoverable from `d` before ⟺ after" is established twice in adjacent sentences — once as the existential-over-slots consequence of RA7b, and again via LP12 + RA1. The LP12 route subsumes the RA7b-aggregate conclusion and additionally supplies the address-characterization (`coverage ∩ ran` invariant), which is the deeper "why." The intermediate sentence asserting the same biconditional from RA7b is redundant given the derivation that immediately follows it.

**Required**: Let RA7b stand as the per-slot fact and let the LP12 address-view carry the discoverability conclusion (it explains *why* — discovery is address-keyed and addresses are invariant); drop the intervening sentence that re-derives the same biconditional from RA7b.

## OUT_OF_SCOPE

No scope violations to flag. The note's Open Questions already defer the genuinely future topics — cross-document boundary-hood under transclusion, serialization-free concurrent rearrangement, the content-discovery-index invariant under footprint fragmentation, prior-arrangement recoverability, and the boundary-preservation guard for any formula-based displacement refinement. These are correctly identified as future ASNs, not gaps in this one. (I checked: the inline re-derivation of LP3/LP11 for REARRANGE is *not* a standard-7 violation — LP11 is stated specifically for `K.μ~` transitions, REARRANGE is emphatically not `K.μ~`, and the note's justification for re-proving rather than citing is sound.)

VERDICT: REVISE
