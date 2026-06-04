# Review of ASN-0087

## REVISE

### Issue 1: Atomicity section restates "allocated but unplaced" three times
**ASN-0087, Atomicity**: The bullet "`ℓ ∉ ran(Σ_mid.M(d))` — the link is not yet visible in any V-arrangement", then the prose "the link exists in `dom(L)` with its endsets recorded but is unplaced in `M(d)`", then "The substrate-observable fact specific to atomicity is the intermediate state itself: at `Σ_mid` the link satisfies `ℓ ∈ dom(L)` yet `ℓ ∉ ran(M(d))` — allocated but unplaced."
**Problem**: The same fact (link in `dom(L)`, absent from `ran(M(d))` at `Σ_mid`) is asserted three times across consecutive paragraphs — the duplicate-paragraph anti-bloat pattern. The reader must confirm each restatement carries nothing new.
**Required**: State the intermediate-state fact once (the bullet list suffices), then proceed directly to the consequence (the protocol-layer obligation). Delete the two restatements.

### Issue 2: M-DepthConv introduced with why-needed justification rather than content
**ASN-0087, Inputs**: "We make the convention explicit precisely because the depth is *not* recoverable from `Σ` in the boundary case where the link subspace is empty." and the parenthetical "(`m_L(d)`, ASN-0047, is well-defined only while `V_{s_L}(d) ≠ ∅`)".
**Problem**: This is prose explaining *why* the convention is needed, not what it commits to — the "explains why needed rather than what it says" pattern. The normative content ("MAKELINK commits to `m = 2` for every first link it places; S8-depth then pins `m_L(d) = 2`") is sufficient on its own; the necessity rationale is meta-prose a precise reader must skip.
**Required**: Reduce to the commitment itself. The non-recoverability of `m` is implicit in the fact that the convention exists at all.

### Issue 3: "Discoverability Is Symmetric" restates the close of "What Is Indexed?"
**ASN-0087, Discoverability Is Symmetric**: "the home document has no privileged position in discovery. By LP12, any document whose arrangement reaches `coverage(eᵢ)` for any `i` becomes a source from which `ℓ` is discoverable".
**Problem**: "What Is Indexed?" already concluded "this biconditional holds at the post-state for every `d ∈ dom(Σ'.M)`. The link is discoverable from every document whose arrangement reaches into any of its endset coverages." The symmetry section reuses the identical LP12 substance with only an emphasis change ("no privileged position"). Two sections in different slots delivering the same claim.
**Required**: Fold the "no privileged home document" emphasis into the closing line of "What Is Indexed?" (or into M-DiscSymmetry's statement) and delete the standalone section.

## OUT_OF_SCOPE

### Topic 1: Whether normatively fixing link-subspace depth at `m = 2` over-constrains alternative implementations
**Why out of scope**: M-DepthConv makes a defensible scoped commitment given that `Σ` underdetermines `m`. Whether the abstract spec should instead admit nondeterministic `m ≥ 2` for first links is a design-policy question about the operation vocabulary, not a defect in this ASN's reasoning.

### Topic 2: Concrete verification of the subsequent-emission positioning (`v_ℓ = shift(max(V_{s_L}(d)), 1)`)
**Why out of scope**: The worked example exercises only the first-emission (empty link subspace) case. The standards require *at least one* concrete scenario, which is met; a second example for the subsequent case is a nice-to-have, not a required revision.

VERDICT: REVISE
