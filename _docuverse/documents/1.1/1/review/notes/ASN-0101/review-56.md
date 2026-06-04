# Review of ASN-0101

I read the operation specification (D0), the gap-closure proof (D1), the preservation claims (D2–D9), the ValidComposite★ extension (D10), and the wp analysis (D11), and verified the three worked examples and the boundary-case enumeration. The mathematics is sound: the critical tiling check — that `Λ` (last component `1..p−1`) and `Q = σ_d(Π)` (last component `p..n_S−n`) abut at exactly position `p` with no gap and no overlap — holds, and D8 addresses every conjunct of ExtendedReachableStateInvariants. I found no correctness or completeness defect.

The findings below are prose accretion of the kind the `review-mode.anti-bloat` classifier flags.

## REVISE

### Issue 1: Implementation-theory essay generalizing beyond the abstract claim
**ASN-0101, "What shifts: closing the gap"**: "Any implementation that represents the arrangement compactly (as runs, or as B-tree nodes) must arrange for the deletion boundaries `s` and `r` to coincide with representation boundaries before the per-region action can be applied uniformly. Without such alignment, individual cells of the representation would span the boundary and require special-case handling. The two-knife pattern ... generalises beyond tree representations to any compact arrangement."

**Problem**: The Gregory two-phase-protocol paragraph immediately above is legitimate implementation evidence. But this "Boundary alignment is necessary, not incidental" observation is not evidence about Gregory's code nor a statement about what DELETE does — it is a general claim about how *any* compact representation must behave. It does not advance D0–D11 (which characterise `M'(d)` as a partial function with no notion of "cell" or "boundary"), and the ASN itself states two paragraphs later that "The specification has no notion of 'tree'." The reader must skip past it to reach the next claim.

**Required**: Remove the generalized implementation-theory observation, or fold any load-bearing content into the Gregory evidence paragraph as evidence rather than as a claim about all implementations. (The companion bullet, "No reconciliation across the gap," states what DELETE does *not* do and should stay.)

### Issue 2: The link-immutability ⇒ coverage-invariance fact is stated three times
**ASN-0101, D3 section**: "Under D3, `L'(ℓ).eᵢ = L(ℓ).eᵢ`, so `coverage(L'(ℓ).eᵢ) = coverage(L(ℓ).eᵢ)`. Whatever I-addresses the link referenced before DELETE, it references after."

**ASN-0101, "Link discoverability: the projection picture" intro**: "DELETE is, from the link store's viewpoint, an arrangement-only operation: link values are unchanged, coverage is unchanged, only the projection into the affected document's affected subspace is altered."

**Problem**: The same fact (link store untouched ⇒ coverage unchanged ⇒ only projection moves) is asserted in D3's "sharper" coverage analysis, restated in the projection-picture intro, and re-derived a third time inside D9's justification ("`coverage(L'(ℓ).eᵢ) = coverage(L(ℓ).eᵢ)` by D3"). Two of the three are scene-setting restatements in different words; only the D9 justification use is load-bearing.

**Required**: Keep the derivation where it is used (D9's justification) and the formal corollary in D3; drop the projection-picture intro's restatement so the section opens directly on D9's characterisation.

### Issue 3: "Boundaries the abstract specification does not cross" is defensive scope prose
**ASN-0101, final section**: three bullets ("Auxiliary indices," "Representation," "Enumeration of orphaned I-addresses") each stating that a concern is "a downstream concern," "out of scope," or "treated as a feature ... not a defect."

**Problem**: Each bullet restates that something is not in scope and points back to D2/D5 as the underlying truth — material already established. The bullets do not advance any claim; they are disclaimers occupying a structural slot. The closing paragraph ("These observations clarify scope ...") then re-summarises the same disclaimer.

**Required**: Collapse to a single sentence noting that DELETE's guarantees concern only the state components named in D0's frame, and that auxiliary indices, representation, and orphan-enumeration are downstream. Drop the closing re-summary.

## OUT_OF_SCOPE

None. The ASN correctly confines itself to DELETE and defers INSERT/COPY/REARRANGE/versioning to the Open Questions.

VERDICT: REVISE
