# Review of ASN-0087

## REVISE

### Issue 1: StandardAuthoring necessity-argument is duplicated and carries meta-prose into a structural slot
**ASN-0087, Inputs (Standard authoring) and Claims Introduced (StandardAuthoring row)**: The Inputs prose states "The restriction to substrate-emittable addresses is essential, not a convenience: `coverage(e)` is a union of half-open T1-intervals ... each infinite by T0(a)/T0(b) ... whereas the stores are finite ... An unrestricted ... would hold for *no* endset containing a span, making the predicate vacuous." The Claims table then repeats the same argument: "The intersection with `F` is essential: unrestricted coverage is infinite (T0(a)/T0(b)), hence never contained in the finite stores."
**Problem**: The same necessity argument appears twice (the "two paragraphs say the same thing" pattern), and both instances explain *why the definition has its shape* rather than stating what it is — the "new prose around a definition explains why it's needed" pattern. The Claims table is a structural slot for the claim statement, not its motivation. The phrase "the discipline still delivers the inference it exists for" is likewise meta-commentary on the predicate's purpose.
**Required**: State `StandardAuthoring(e, Σ) ≡ coverage(e) ∩ F ⊆ dom(Σ.C) ∪ dom(Σ.L)` once, with at most a single clause naming `F` (ASN-0098). Remove the duplicated necessity essay from the Claims table; if the infinitude motivation is kept at all, keep it in exactly one place.

### Issue 2: S8a verification references `m_L(d)`, which is undefined in the first-link (empty) case
**ASN-0087, Invariant Preservation (Per-State Invariants, S8a row)**: "S8a: zeros(v_ℓ) = 0, #v_ℓ = m_L(d) ≥ 2, components all > 0".
**Problem**: When `V_{s_L}(d) = ∅` at `Σ` — the first-link case the note explicitly handles — `m_L(d)` is undefined (ASN-0047: "`m_S(d)` is well-defined only while `V_S(d) ≠ ∅`"). The note's own M-DepthConv establishes the depth *at the post-state* by committing `m = 2`. Writing `#v_ℓ = m_L(d)` against the pre-state operand is therefore ill-typed in precisely the boundary case the discharge must cover.
**Required**: State the S8a check at the post-state: `#v_ℓ = m_L(d')` where `m_L(d') = 2` in the empty case (pinned by M-DepthConv) and `m_L(d') = m_L(d)` (the existing depth) in the non-empty case.

### Issue 3: Redundant restatement of LP12 as a post-MAKELINK property
**ASN-0087, What Is Indexed?**: "By LP12 (ASN-0098): discoverable_from(ℓ, d, Σ') ⟺ (E i : coverage(Σ'.L(ℓ).eᵢ) ∩ ran(Σ'.M(d)) ≠ ∅). After MAKELINK, this biconditional holds at the post-state for every `d ∈ dom(Σ'.M)` (M-DiscSymmetry)."
**Problem**: LP12 is a foundation lemma that holds at *every* reachable state for every (link, document) pair; "After MAKELINK, this biconditional holds at the post-state" adds nothing and dresses an unconditional foundation result as a MAKELINK-specific guarantee. This is meta-prose around a citation.
**Required**: Drop the "After MAKELINK, this biconditional holds..." sentence. State the symmetric-discoverability content (M-DiscSymmetry) directly: `ℓ` is discoverable from every document whose arrangement range meets some endset coverage, since LP12 treats all documents uniformly.

## OUT_OF_SCOPE

### Topic 1: Permission/ownership semantics for endset-referenced content
The "No Permission Check" section correctly observes the substrate exposes no permission state. Any actual authorization model belongs to a future protocol-layer ASN, not here.

### Topic 2: Deferred-consistency discoverability model
Open Question "Must MAKELINK's discoverability guarantee hold at the precise post-state ... or is a deferred-consistency model admissible?" is correctly left open; it concerns a consistency-model ASN, not this operation.

VERDICT: REVISE
