# Review of ASN-0115

## REVISE

### Issue 1: R8's link sub-case describes a configuration the substrate forbids

**ASN-0115, R8 (TransclusionRevelation)**: "In the **link sub-case** (`subspace(v) = s_L`, `a ∈ dom(Σ.L)`): the two delivered items are the identical reference `⟨ref, a⟩` (R10), again resolved through the one shared address, with common provenance `home(a)` ... no deduplication, by the same exactness argument as (iii)."

**Problem**: R8 contemplates two active positions `v, v'` (within one spec or across specs) with `Σ.M(d)(v) = Σ.M(d')(v') = a` and `a ∈ dom(Σ.L)`. Under the transition model this ASN builds on, this configuration is unreachable:
- CL-OWN (ASN-0047) forces `origin(M(d)(v)) = d` for every link-subspace position, so a link address `a` can appear only in the arrangement of `origin(a) = home(a)`. Two documents `d, d'` both binding `a` in their link subspaces force `d = d'`.
- CL-UNIQ (ASN-0047) makes `M(d)` injective on the link subspace, so within that one document two distinct positions cannot both map to `a`, forcing `v = v'`.

Both are per-state invariants of every reachable state (ASN-0047, ExtendedReachableStateInvariants). Hence two **distinct** active link positions can never share a link address — genuine link transclusion does not occur. The link sub-case is therefore vacuous, yet it is presented as a substantive co-delivery guarantee (identical references, shared `home(a)`, no deduplication), exactly parallel to the content sub-case which *is* realizable (S5 UnrestrictedSharing permits content multiplicity within and across documents). The synthesis inherits the over-statement ("positions sharing an address deliver identical, shared-origin material ... (R8)").

**Required**: Either (a) remove the link sub-case and confine R8 to content (where S5 makes sharing real), or (b) explicitly acknowledge that CL-OWN + CL-UNIQ make distinct link positions sharing an address impossible, so the link sub-case is vacuous and the only multiplicity available for links is one V-position named by two overlapping specs (which is not transclusion). The ASN must not present a guarantee over an unreachable configuration as if it were on equal footing with the content sub-case.

### Issue 2: empty spec-set (`p = 0`) delivery left implicit

**ASN-0115, "What a spec-set is"**: "A *spec-set* is a finite **ordered** sequence `R = ⟨ρ₁, …, ρₚ⟩` of V-specs, `p ≥ 0`."

**Problem**: The ASN admits `p = 0` but never states what `deliver(⟨⟩, Σ)` is or whether it is a successful (empty) delivery. R6 addresses the *empty-`act`* boundary within a spec, but not the empty-request boundary. While R0's concatenation definitionally yields `⟨⟩`, the empty-structure boundary is one the standards require to be made explicit, and "delivery succeeds and returns nothing" is the natural companion to R6's partial-success discipline.

**Required**: State that `deliver(⟨⟩, Σ) = ⟨⟩` and that the empty spec-set is a valid, successful (empty) delivery — one sentence, parallel to R6.

## OUT_OF_SCOPE

### Topic 1: link transclusion as a future capability
**Why out of scope**: A model in which a link entity may be arranged at multiple V-positions (relaxing CL-UNIQ/CL-OWN) would make R8's link sub-case meaningful, but that is a change to the transition model, not a defect to repair here. The current ASN should simply not claim it.

VERDICT: REVISE
