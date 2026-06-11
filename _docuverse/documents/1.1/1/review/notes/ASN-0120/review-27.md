# Review of ASN-0120

## REVISE

### Issue 1: ML10's "sources unmodified" gloss fails when a source is the home document
**ASN-0120, "The invariants MAKELINK preserves" (Frame, ML10), and Claims table row ML10**: "The sources the endsets read are unmodified by the act of being linked into: a link *to* a region changes nothing about that region" / "the linked-into sources are unmodified by being linked into"
**Problem**: The operation admits a source document `d_j` that equals the home `d` — `wf` constrains only `d_j ∈ dom(Σ.M)`, ML4 expressly asserts independence of home and endset content, and the foundation (L4(b), ASN-0043) anticipates intra-document links. In that case the source *is* modified: `Σ'.M(d_j) ⊋ Σ.M(d_j)`, since `K.μ⁺_L` seats `v_a ↦ a` in `d_j = d`'s link subspace. The formal frame `(A d' ≠ d : Σ'.M(d') = Σ.M(d'))` is correct, but the prose gloss and the claims-table row state an unqualified claim that is false at exactly this boundary case — a boundary the ASN's own worked example (all-distinct documents) never exercises. What is true uniformly is narrower: the *content-subspace* restriction of every source's arrangement is unchanged, so the regions the endsets read are unaffected in every case.
**Required**: Scope the gloss to the coordinates the endsets read — e.g., "every source's content-subspace arrangement is unmodified; when a source coincides with the home, its arrangement gains only the link-subspace seating binding" — and correct the ML10 table row to match. One sentence acknowledging the home-as-source case suffices.

### Issue 2: Worked example applies V-position vocabulary to I-addresses
**ASN-0120, "A worked example", item (iii)**: "Had `e₁` been recorded as the single merged span `(a₁, δ(2, #a₁))`, that one span now covers one active position and one inactive — exactly the partial-span shape that motivated `ρ`'s active-position filter"
**Problem**: The merged span is an I-span; its coverage contains the I-addresses `a₁` and `a₂` (and their subtrees), not positions. "Active" is this ASN's vocabulary for V-positions (`v ∈ dom(Σ.M(d))`); the corresponding notion for an I-address is membership in `ran(Σ''.M(A))` (arranged / no longer arranged). The sentence also asserts identity ("exactly the partial-span shape") between two different things: the creation-time filter operates on V-coordinates (a V-span over a partially-deleted arrangement at `Σ`), whereas the post-edit situation is an I-span partially un-arranged at `Σ''`. The structural parallel is real, but stating it in collapsed vocabulary blurs the V/I distinction that the ASN itself declares to be the entire content of the operation ("Position is mutable; identity is permanent").
**Required**: Restate in I-vocabulary — "that one span now covers one I-address still arranged in `A` and one no longer arranged" — and present the parallel as the I-side counterpart of the partial V-span that motivated `ρ`'s filter, not as the same shape.

## OUT_OF_SCOPE

### Topic 1: Endset arguments supplied directly as I-addresses or I-spans
**Why out of scope**: The ASN correctly restricts MAKELINK-via-V-specs to content-backed endsets (`ρ(R_i, Σ) ⊆ dom(Σ.C)`) and notes that ghost types (L9) and foreign/ghost endsets (full L4 generality) require a distinct argument shape that bypasses V-span resolution. That argument shape — and with it link-subspace endset references, already logged as the second Open Question — is a future operation variant, not a defect here.

### Topic 2: Isolation of the K.λ → K.μ⁺_L intermediate state
**Why out of scope**: MAKELINK is a two-step ValidComposite★; between the steps the link exists in `Σ.L` but is not yet seated in its home's V-stream. Whether other composites can observe or interleave with that intermediate state is a property of the substrate's composite/transition model (ASN-0047's sequencing semantics), not of this operation; the ASN discharges the intermediate-state preconditions, which is all the composite definition requires of it.

VERDICT: REVISE
