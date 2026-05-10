# Review of ASN-0051

## REVISE

### Issue 1: Worked example performs an invalid contraction

**ASN-0051, Worked Example**: "A K.μ⁻ step removes the mapping at v₃, producing M'(d) with dom(M'(d)) = {v₁, v₂, v₄, v₅}"

**Problem**: K.μ⁻'s postcondition requires D-CTG and D-MIN. By D-SEQ (ASN-0036), valid V-position sets must be `{[S, 1, ..., 1, k] : 1 ≤ k ≤ n}` — a contiguous ordinal range. The set `{v₁, v₂, v₄, v₅}` has a gap at v₃, violating D-CTG. The ASN-0047 definition of K.μ⁻ explicitly notes: "valid contractions are constrained to removal from the maximum end of V_S(d) or removal of all positions in V_S(d)." Removing from the interior is not a valid elementary contraction.

This invalidity propagates through the rest of the worked example: the post-contraction block decomposition "β₁ = (v₁, a₁, 2) covering {v₁, v₂} ... β₂ = (v₄, a₄, 2) covering {v₄, v₅}" is built on an unreachable state, and the subsequent reordering step also operates on this invalid state.

**Required**: Replace the single K.μ⁻ with a valid composite. For example: K.μ~ reordering M(d) to place a₃ at v₅ (yielding `{v₁↦a₁, v₂↦a₂, v₃↦a₄, v₄↦a₅, v₅↦a₃}`), followed by K.μ⁻ removing v₅ (yielding `dom = {v₁, v₂, v₃, v₄}`, contiguous). This achieves `ran = {a₁, a₂, a₄, a₅}` with block decomposition β₁ = (v₁, a₁, 2) and β₂ = (v₃, a₄, 2). The SV11 fragment computation gives the same result `{a₂} ∪ {a₄}`, but the block structure and subsequent reordering step need corresponding adjustment.

### Issue 2: K.μ⁺\_L and K.λ omitted from survivability analysis

**ASN-0051, SV13(e)**: "All other elementary transitions (K.α, K.δ, K.ρ) preserve M in their frame, so resolve(e, d) is unchanged."

**Problem**: The enumeration of elementary transitions is incomplete. Two foundation operations from ASN-0047 are missing:

- **K.λ** (LinkAllocation) has frame `(A d' :: M'(d') = M(d'))` — all arrangements preserved. It belongs in the frame-preserving list alongside K.α, K.δ, K.ρ.

- **K.μ⁺\_L** (LinkSubspaceExtension) modifies M(d) by adding a link-subspace mapping `v_ℓ ↦ ℓ`. It does *not* preserve M in frame. Its effect on projection is analogous to SV2: `ran(M'(d)) ⊇ ran(M(d))` (one new link address added), so `π_{Σ'}(e, d) ⊇ π_Σ(e, d)`. But this analysis is nowhere in the ASN.

Consequently, SV2 should mention K.μ⁺\_L alongside K.μ⁺ (same proof structure), and SV4 should list K.μ⁺\_L alongside K.μ⁺/K.μ⁻/K.μ~ (same frame for d' ≠ d).

**Required**: Add K.λ to the frame-preserving list. Either extend SV2 and SV4 to cover K.μ⁺\_L explicitly, or state that K.μ⁺\_L's effect on projection is deferred to the Link Subspace ASN — but in that case, the "all other" claim in SV13(e) must be qualified rather than stated as exhaustive.

### Issue 3: False claim about non-text V-positions

**ASN-0051, SV11**: "In the current foundation model, no defined operation creates non-text V-positions, so π\_text(e, d) = π(e, d) for all reachable states."

**Problem**: K.μ⁺\_L (LinkSubspaceExtension, ASN-0047) creates link-subspace V-positions — mappings `v_ℓ ↦ ℓ` where `subspace(v_ℓ) = s_L`. After K.μ⁺\_L, `ran(M(d))` includes link addresses, so `π(e, d) = coverage(e) ∩ ran(M(d))` can include link addresses that `π_text(e, d)` excludes. The equality `π_text = π` does not hold for reachable states where K.μ⁺\_L has been applied.

**Required**: Replace the parenthetical with an accurate statement. Either: "K.μ⁺\_L creates link-subspace V-positions, so π\_text(e, d) ⊆ π(e, d) in general; the link-subspace contribution is deferred to the Link Subspace ASN." Or extend the analysis.

### Issue 4: Name collision with foundation definition of resolve

**ASN-0051, Endset Resolution definition**: "resolve(e, d) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}"

**Problem**: ASN-0058 (foundation) defines `resolve(d_s, σ)` — a function from content references to I-address sequences (Definition — Resolution). ASN-0051 defines `resolve(e, d)` — a function from endsets × documents to V-position sets. These have different signatures, different return types, and answer different questions. Reusing the name in a formal specification creates ambiguity: a reader encountering "resolve" must determine from context which function is meant.

**Required**: Rename the ASN-0051 function to avoid collision. Candidates: `vresolve(e, d)`, `locate(e, d)`, `positions(e, d)`.

### Issue 5: Fragment splitting mechanism incorrectly attributed to single contraction

**ASN-0051, Partial Survival**: "a single contraction that removes I-addresses from the interior of a contiguous endset region splits one fragment into two"

**Problem**: K.μ⁻ removes V-positions exclusively from the maximum end of V\_S(d) (D-CTG/D-SEQ postcondition, ASN-0047). This can shrink or remove the last block(s) in the block decomposition, but interior blocks are unaffected — their V-positions remain in dom(M'(d)) and their I-addresses are unchanged. A fragment within an interior block is therefore unchanged by K.μ⁻. A fragment within the last block can only be shrunk from its right end (never split), because contiguous removal from the right of a contiguous ordinal range produces a contiguous range. Splitting a fragment requires a K.μ~ reordering (which changes the block decomposition) followed by K.μ⁻ — a composite, not "a single contraction."

**Required**: Correct the mechanism description. The growth in fragment count across arrangement operations comes from reordering (which restructures blocks) combined with contraction, not from contraction alone.

## OUT_OF_SCOPE

### Topic 1: Link subspace interaction with endset projection
**Why out of scope**: Full treatment of how link-subspace V-positions (created by K.μ⁺\_L) affect endset projection, including links whose endsets reference other link addresses (L13, ReflexiveAddressing), belongs in the Link Subspace ASN. The REVISE items above address only the factual errors in the current ASN's claims about these operations, not the missing analysis itself.

### Topic 2: Within-document sharing resolution semantics
**Why out of scope**: When multiple V-positions in a document map to the same I-address (S5, UnrestrictedSharing), the resolution set |resolve(e, d)| > |π(e, d)|. The ASN correctly notes this and defers the question of what ordering or presentation guarantees the system must provide. This is new territory — a resolution policy ASN.

VERDICT: REVISE
