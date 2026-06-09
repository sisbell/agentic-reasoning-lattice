# Review of ASN-0119

## REVISE

### Issue 1: P7c (ContiguityWP) is not the weakest precondition — it is wrong in both directions

**ASN-0119, "Links" section / Claims table P7c**: "wp(REARRANGE_K, "footprint of (a,i) resolves to a contiguous span") ≡ project(a, i, d, Σ) ⊆ one region (exterior, α, μ, or β)" and "a footprint stays contiguous iff confined to a single region and fragments iff it straddles a cut."

**Problem**: The biconditional fails in both directions.

*Too strong (⟸ fails).* Within each region π is a rigid ordinal shift, but REARRANGE also creates a **new seam**: in the pivot, the last byte of β (now at ord c₀+w_β−1) becomes adjacent to the first byte of α (now at ord c₀+w_β). A footprint `{c₂−1, c₀}` — one position in β, one in α — *straddles* the cut, yet lands at the two adjacent post-positions `{c₀+w_β−1, c₀+w_β}`, a single contiguous span. Concretely, take a pivot with w_α = w_β = 1 (swap of two adjacent single positions) and footprint `{c₀, c₁}`: π(c₀)=c₀+1, π(c₁)=c₀, post-footprint `{c₀, c₀+1}` is contiguous. Here `project ⊄ one region` (the formula evaluates false) but the postcondition holds — so the stated formula excludes a pre-state that satisfies the postcondition. The claim "fragments iff it straddles a cut" is simply false: a footprint straddling exactly at the relocated seam stays contiguous.

*Too weak (⟹ fails).* coverage(e) is an arbitrary address set (L4, EndsetGenerality), so a footprint can be **discontiguous within a single region** in the pre-state (e.g. ord 3 and ord 5 inside β=[3,6)). A rigid shift preserves that gap, so the post-footprint is discontiguous, yet `project ⊆ one region` is true — the formula admits a pre-state whose post fails the postcondition.

**Required**: Either relativize the postcondition to "the footprint's contiguity (run count) is preserved" rather than "resolves to a contiguous span," or correct the wp to account for (a) the requirement that the relevant pre-footprint already be a single contiguous run, and (b) the new seams the permutation introduces (β-end abutting α-start in the pivot; the three seams of the swap), under which a straddling footprint can remain contiguous. Then exhibit a concrete fragmentation example (the worked section checks P1/P2/P3/P7a but never the one "non-trivial" claim), which would have surfaced the seam counterexample. The downstream remark "every other postcondition here has wp = true" should be re-stated once P7c is corrected.

## OUT_OF_SCOPE

### Topic 1: Cut falling on a transclusion-shared V-position
**Why out of scope**: Correctly deferred to the Open Questions; cross-document cut semantics is new territory, not an error here. P9 already establishes isolation for the rearranged document.

### Topic 2: Recoverability of a prior arrangement / version history
**Why out of scope**: Belongs to version creation (CREATENEWVERSION), explicitly excluded by scope; the Open Question records it appropriately.

VERDICT: REVISE
