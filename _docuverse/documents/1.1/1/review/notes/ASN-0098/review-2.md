# Review of ASN-0098

## REVISE

### Issue 1: K.δ reference inconsistent with the state model in use
**ASN-0098, "The Projection Operation"**: "Entity registration (K.σ, K.δ) that only updates `dom(Σ.M)` and initialises arrangements to empty cannot retroactively affect existing projections through existing documents."
**ASN-0098, LP8**: "K.σ (document registration) extends `dom(Σ.M)` by adding a fresh document `d_new`..."
**Problem**: The ASN's State Components section commits to ASN-0093 (which has K.σ for document registration; no K.δ). LP8 itself addresses only K.σ. The informal mention of K.δ is from ASN-0047's vocabulary and is not consistent with the cited model.
**Required**: Either remove the K.δ reference and commit purely to the ASN-0093 K family, or commit to the ASN-0047 model and add formal coverage for K.δ in all three of its sub-cases (node, account, document).

### Issue 2: K.ρ from ASN-0047 not addressed
**ASN-0098, "Operation Effects on Projection"**: LP6–LP11 cover K.α, K.λ, K.σ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~.
**Problem**: The ASN cites K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L from ASN-0047 but never addresses K.ρ (ProvenanceRecording), also in ASN-0047's K family. K.ρ's frame preserves M, so by LP4 it preserves all projections — but this must be stated, not assumed.
**Required**: Add a one-line lemma covering K.ρ (analogous to LP6/LP7), or explicitly note that K.ρ is out of scope and justify why.

### Issue 3: Multi-step composition left implicit in LP18 and LP19
**ASN-0098, LP18 proof**: "Because LP3 keeps the link's coverage fixed across the entire sequence..."
**ASN-0098, LP19 proof**: "By the monotonicity of both stores (S1 of ASN-0036 for content, L12a of ASN-0043 for links, both subsumed by P0 and L12 of ASN-0093), `dom(Σ.C) ⊇ dom(Σ_e.C)` and `dom(Σ.L) ⊇ dom(Σ_e.L)`."
**Problem**: LP3 is per-transition (`Σ → Σ'`), not multi-step (`Σ →* Σ'`). Same for the cited store monotonicity. These proofs use the multi-step form without deriving it. Compare to ASN-0040's pattern of introducing B0★ as a corollary of B0.
**Required**: Introduce LP3★ (multi-step coverage invariance) and a multi-step store-monotonicity corollary, each derived inductively from the per-step versions. Then cite the multi-step forms in LP18 and LP19.

### Issue 4: LP11 reverse inclusion not made explicit
**ASN-0098, LP11 proof**: The biconditional chain establishes `v ∈ project(e, d, Σ) ⟺ π(v) ∈ project(e, d, Σ')` for `v ∈ dom(Σ.M(d))`.
**Problem**: This chain gives `π(project(e, d, Σ)) ⊆ project(e, d, Σ')` directly. The reverse inclusion `project(e, d, Σ') ⊆ π(project(e, d, Σ))` requires that every `v' ∈ project(e, d, Σ')` has a preimage under π — invoking π's bijectivity on `dom(Σ.M(d)) = dom(Σ'.M(d))`. The proof states bijectivity but doesn't use it in the chain.
**Required**: After the biconditional, add an explicit step: "For the reverse inclusion: any `v' ∈ project(e, d, Σ') ⊆ dom(Σ'.M(d)) = dom(Σ.M(d))` has a unique preimage `v = π⁻¹(v')`; by the biconditional applied to `v`, `v ∈ project(e, d, Σ)`, so `v' = π(v) ∈ π(project(e, d, Σ))`."

### Issue 5: `discoverable_from` definition presupposes `a ∈ dom(Σ.L)` implicitly
**ASN-0098, Definition — Discoverability**: "`discoverable_from(a, d, Σ) ≡ (E i : 1 ≤ i ≤ |Σ.L(a)| : project(a, i, d, Σ) ≠ ∅)`"
**Problem**: `|Σ.L(a)|` and `Σ.L(a).eᵢ` are undefined when `a ∉ dom(Σ.L)`. The definition needs to either condition on `a ∈ dom(Σ.L)` explicitly or specify behaviour when it does not hold.
**Required**: Add `a ∈ dom(Σ.L)` to the definition's preconditions, matching how `project(e, d, Σ)` explicitly requires `d ∈ dom(Σ.M)`.

### Issue 6: Worked trace's K.μ~ example does not illustrate projection motion
**ASN-0098, "A Worked Trace"**: After K.μ~ with π permuting `{v₁, v₂, v₃}`, the trace states `project(a, 1, d₁, Σ_3) = {v₃, v₂, v₁} = π(project(a, 1, d₁, Σ_1))`.
**Problem**: All three V-positions are in the projection in Σ_1 (since `i₁, i₂, i₃ ∈ coverage`), so any permutation of `dom(Σ_1.M(d₁))` leaves the projection set identical. The example does not exhibit movement — it exhibits trivial set preservation under permutation.
**Required**: Modify the example so only a strict subset of V-positions is in the projection (e.g., coverage = `{i₁}` only). Then π moves `{v₁}` to `{π(v₁)} = {v₃}` — actual motion. Alternatively, add a second tracing line showing per-V-position rebinding (`v₁` carries `i₁` to position `v₃`).

### Issue 7: "Tight at state Σ_e" prose conflicts with formal definition
**ASN-0098, LP19**: "An endset `e` is *tight at state `Σ_e`* (the state of the system at the time `e` was incorporated into a link) when its coverage is entirely populated"
**Problem**: The parenthetical pins `Σ_e` to a link-incorporation state, but the formal definition `coverage(e) ⊆ dom(Σ_e.C) ∪ dom(Σ_e.L)` is general for any state. The lemma's quantification "for any endset `e` tight at `Σ_e`" then admits any `Σ_e`, not just link-incorporation states. This creates ambiguity about what `Σ_e` denotes.
**Required**: Either drop the parenthetical (formal definition is general) or tighten the formal definition (introduce a link-creation event predicate). Recommend the former for generality.

### Issue 8: Numbering gaps unexplained
**ASN-0098, "Claims Introduced" table**: Lemmas LP2 through LP21 listed, with LP14 and LP15 absent. There is no LP1.
**Problem**: The commit message mentions collapsing LP14/LP15 but the ASN itself does not. Readers cannot tell whether the gap is intentional or whether content is missing.
**Required**: Either renumber to close the gaps (LP2→LP1, LP16→LP14, etc.) or add a footnote to the table noting the deliberate absence of LP1, LP14, LP15 from this revision.

### Issue 9: "Claims Introduced" table omits `discoverable_from`
**ASN-0098, "Claims Introduced"**: Lists `project` and `tight` as definitions but omits `discoverable_from`.
**Problem**: `discoverable_from` is defined in the prose ("Definition — Discoverability") and used by LP12, LP13, LP16, LP17. Table should be complete.
**Required**: Add a row for `discoverable_from`.

### Issue 10: Informal text about K.α boundary insertion uses "typically" without anchoring
**ASN-0098, "Frame Conditions" (LP6 discussion)**: "Since K.α allocates fresh I-addresses outside any existing range... the new V-position's I-address typically lies outside `coverage(e)`, and the projection does not grow."
**Problem**: "Typically" is correct only under the tightness construction discipline of LP19. Without tightness, the new I-address could land inside coverage. As written, the prose appears to claim a universal property.
**Required**: Replace "typically" with a forward reference: "...the new V-position's I-address lies outside `coverage(e)` whenever `e` was tightly constructed (LP19 formalises this), and the projection does not grow."

## OUT_OF_SCOPE

### Topic 1: Reverse-discovery primitive
**Why out of scope**: The ASN explicitly lists this in Open Questions. Forward projection is well-formed in isolation; reverse discovery (given a V-position, find all links projecting to it) is a separate operation requiring its own treatment.

### Topic 2: V-order structure of projections (contiguity, fragmentation under K.μ~)
**Why out of scope**: Already in the ASN's Open Questions. The current ASN establishes set-level guarantees; ordering structure of projections is a separable question.

### Topic 3: Coverage spanning beyond dom(Σ.C) at link-creation time
**Why out of scope**: This is the "non-tight" case that LP19 deliberately excludes. The ASN flags it as Open Question 5.

### Topic 4: Link-of-link discovery semantics
**Why out of scope**: Endsets may reference link addresses (L4 of ASN-0043 permits this), but the induction of link discoverability from one link to another is a separate question. Listed in Open Questions.

META: The ASN remains focused on abstract state guarantees about a derived computation (projection), not on implementation mechanics.

VERDICT: REVISE
