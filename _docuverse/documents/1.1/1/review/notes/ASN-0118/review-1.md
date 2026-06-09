# Review of ASN-0118

## REVISE

### Issue 1: Cross-ASN reference to non-foundation ASN-0115
**ASN-0118, "What a spec-set names"**: "a well-formed, level-uniform, ordinal-level span `σ` whose start is a well-formed V-position, exactly as ASN-0115 fixes for RETRIEVEV; we adopt that definition unchanged." and "`act(ρ, Σ) = dom(Σ.M(d_s)) ∩ ⟦σ⟧` (ASN-0115)."
**Problem**: ASN-0115 is not a foundation ASN. The V-spec definition is deferred wholesale ("adopt unchanged") rather than restated, and the active-positions notion is attributed to it. Standard 7 forbids cross-ASN references except to foundations; the ASN is not self-contained.
**Required**: Define the V-spec self-containedly using only foundation primitives (ASN-0034 span/T12, ASN-0053 level-uniform/ordinal-level, ASN-0036 V-position), and state `act` from those. Remove the ASN-0115 citations.

### Issue 2: No concrete worked example
**ASN-0118, throughout**: The ASN states CP0–CP11 abstractly and never instantiates them.
**Problem**: Standard 6 makes a concrete scenario mandatory. There is no worked case ("resolve spec-set ⟨(d_s,σ)⟩ over specific addresses, place at position p, then check CP1, CP2, CP3a, CP5, CP11 against the result").
**Required**: Add one concrete scenario with specific tumblers — ideally a non-contiguous two-source assembly — verifying CP1 (store unchanged), CP2 (placement), CP3a (shift), and CP11 (origin multiset preserved) numerically.

### Issue 3: CP4 multiplicity arithmetic is wrong
**ASN-0118, CP4 / Claims table**: "the number of `(document, V-position)` pairs mapping to a placed address `cᵢ` is strictly greater than before — by at least the `W` new placements".
**Problem**: For a fixed address `cᵢ`, the reference count increases by the number of times `cᵢ` occurs in `resolve(R,Σ)` (typically 1), not "by at least `W`". The aggregate over all placed addresses increases by `W`; the per-address claim conflates the two.
**Required**: State it correctly — total references increase by `W`; per-address `cᵢ`, the increase equals its occurrence count in the resolved sequence (≥ 1).

### Issue 4: CP7b cites a lemma whose precondition is not met
**ASN-0118, "Survival of links"**: "after COPY ... `a` is discoverable from `d` (ASN-0098, LP18 Resurrection; the symmetric form LP16 TransclusionDiscoverability)."
**Problem**: LP18 requires `a` to be *orphaned* at `Σ` (discoverable from no document). A link anchored to source content is generally discoverable from its source, so the orphan premise fails. LP16 requires a three-way intersection `coverage ∩ ran(M(d_src)) ∩ ran(M(d_new)) ≠ ∅`, also not what is established. The correct and sufficient tool is LP12 applied at the post-state, which the prose already uses inline.
**Required**: Drop the LP18/LP16 citations (or use them only where their preconditions hold) and ground CP7b on LP12 directly.

### Issue 5: Contiguity/sequentiality preservation asserted, not derived
**ASN-0118, "The destination's prior arrangement"**: "the placement fills exactly the vacated gap, so `V_{s_C}(d)` after COPY is `{p' : min ≤ p' ≤ max+W}` with no holes, and D-CTG, D-MIN, D-SEQ are preserved (inherited from ASN-0082's I3 preservation lemmas at width `W`)."
**Problem**: ASN-0082's I3 supplies only the *shift* of trailing content; it does not place new content, so it cannot establish gap-filling. The no-holes tiling depends on combining CP2 (W contiguous placements at `p..p+W-1`) with CP3a (shift of `v≥p` to `v+W`) and showing the placement region exactly equals the W-wide vacated ordinal gap — which requires `p`'s ordinal ≤ N+1 (valid insertion). This combined argument is not shown; the citation does not cover it.
**Required**: Give the explicit tiling argument: placement occupies ordinals `[p_ord, p_ord+W)`, shifted content occupies `[p_ord+W, max_ord+W]`, left content `[min_ord, p_ord)`, union contiguous with no overlap. Cite the disjointness from ordinal arithmetic, not from I3.

### Issue 6: Weakest-precondition analysis is trivial
**ASN-0118, "The transclusion frame"**: "`wp(COPY, "placed material refers to existing content") = (A i : 0 ≤ i < W : cᵢ ∈ dom(Σ.C))`".
**Problem**: This wp merely restates CP0(a), which holds by the source arrangements — the answer is trivially true. Standard 6 requires a non-trivial wp case.
**Required**: Compute a non-trivial wp — e.g., wp for "link `a` discoverable from `d` after COPY" (pulls back to `coverage(Σ.L(a).eⱼ) ∩ {c₀,…,c_{W−1}} ≠ ∅`), or wp for a self-transclusion postcondition.

### Issue 7: CP8 provenance justification incomplete for already-referenced addresses
**ASN-0118, CP8**: "the destination records fresh provenance for each reused address (J1★)."
**Problem**: J1★ fires only when `cᵢ` is *new to the content-subspace range* of `M'(d)`. In self-transclusion (CP9), or when `cᵢ` is already transcluded into `d`, `cᵢ` is not range-new, so no fresh recording occurs (and J1'★ forbids it); the membership `(cᵢ,d) ∈ Σ'.R` then holds via the pre-existing record (P2), not via J1★. The blanket "records fresh provenance for each" is wrong for these cases.
**Required**: State CP8 as a membership postcondition discharged by J1★ for range-new addresses and by provenance permanence (P2) for addresses already referenced by `d`.

## OUT_OF_SCOPE

### Topic 1: Open questions are correctly deferred
Partial binding semantics, overlapping/repeated source spans resolving one address to multiple positions, mixed element-field depth assembly, post-COPY link undiscoverability under later removal, the correspondence relation, and link-subspace transclusion are all genuinely new territory and are appropriately listed as Open Questions, not errors in this ASN.

VERDICT: REVISE
