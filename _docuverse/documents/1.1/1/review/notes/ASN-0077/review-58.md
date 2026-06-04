# Review of ASN-0077

## REVISE

### Issue 1: Claims table over-attributes reliance on O11.1
**ASN-0077, Claims Introduced table (O11.1 row)**: "(corollary discharging the post-state admissibility that O11/O11'/O11★★ rely on)"
**Problem**: O11 and O11' do **not** rely on post-state admissibility. Both are single-step equality claims whose proofs only invoke precondition (vi) *at Σ* (see O11 (⊇) Case (ii) sub-case (a): "precondition (vi) at Σ gives v ∈ dom(M(d))"). The conclusion `origins_V(Σ) = origins_V(Σ')` is a comparison of two sets, each well-defined via S3★ regardless of whether σ is admissible at Σ'. O11.1's own body scopes itself correctly — "To chain these single-step claims into multi-step lemmas, we extract the post-state preservation..." — i.e., only O11★★ consumes it. The table contradicts the body.
**Required**: Replace "that O11/O11'/O11★★ rely on" with "that O11★★ relies on," matching O11.1's body.

### Issue 2: Forward-reference deferrals (anti-bloat)
**ASN-0077, "Lifting origin to a V-span" / "Direct resolution"**:
- "(The link-subspace case `u₁ = s_L`, where the result reduces to `{d}`, is treated as an edge case below.)"
- "(Reporting link origins from an I-span is left as Open Question 1; the V-span case is uniformly handled — see below.)"

**Problem**: Both are bare forward pointers ("treated below," "see below," "left as Open Question 1") inserted mid-derivation. They defer rather than advance — the reader must carry the pointer and look ahead. This is the forward-reference accretion the review mode flags.
**Required**: Drop the parentheticals; the edge-case section and Open Questions already carry the content. The deferrals add no reasoning.

### Issue 3: Unused arrange-vs-allocate clarification (anti-bloat)
**ASN-0077, end of "Where origin already lives"**: "CL-OWN (ASN-0047) records a related consequence at the arrangement level... This is downstream of (b) — CL-OWN governs *which document arranges* a link, while K.λ governs *which document allocates* it. The two coincide for the home-document case..."
**Problem**: No subsequent claim consumes this distinction as a proof step — the V-span link edge case invokes CL-OWN directly without needing the "arrange vs allocate" gloss. The paragraph is reader-orientation prose ("a related consequence") sitting in a derivation slot.
**Required**: Remove, or relocate to a non-load-bearing remark. If retained, it should not interrupt the O0 derivation chain.

## OUT_OF_SCOPE

### Topic 1: Reporting link origins from a cross-subspace I-span
**Why out of scope**: The I-span lift is defined content-only by construction (`∩ dom(C)`); whether to surface link origins from an I-span is explicitly Open Question 1 and is new territory, not an error in this ASN.

### Topic 2: Historical-containment operation over Σ.R
**Why out of scope**: The "not historical containment" exclusion correctly defers the complementary `Σ.R`-based operation to a future ASN; coupling invariants between origin and provenance are new content.

VERDICT: REVISE
