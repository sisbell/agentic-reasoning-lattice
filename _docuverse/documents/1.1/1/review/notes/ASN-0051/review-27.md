# Review of ASN-0051

## REVISE

### Issue 1: SV10 witness violates S7c (foundation invariant)
**ASN-0051, SV10 worked example**: "Take origin O = 1.0.1.0.1 and three element-level sibling addresses i₁ = O.0.1, i₂ = O.0.2, i₃ = O.0.3"
**Problem**: With O = [1,0,1,0,1] (length 5), each i_k = O.0.k = [1,0,1,0,1,0,k] has element field E(i_k) = [k] of length 1. S7c (ASN-0036, foundation) requires #E(a) ≥ 2 for every a ∈ dom(Σ.C). The witness violates a foundation axiom.
**Required**: Use addresses with #E ≥ 2, e.g., i₁ = O.0.1.1, i₂ = O.0.1.2, i₃ = O.0.1.3 with ℓ_span = [0,0,0,0,0,0,0,3] (action point 8). Verify the reach computation and that each address satisfies S7c.

### Issue 2: SV6 — T4-validity of generic t in span not explicitly established
**ASN-0051, SV6 proof, "Restricting to element-level t"**: "since b is element-level (S7b — `zeros(b) = 3`), and every element-level t ∈ ⟦(s, ℓ)⟧ has origin(t) = origin(s)"
**Problem**: The proof requires origin(t) to be well-defined for every element-level t in the span, which requires T4-validity of t. Element-level (zeros(t) = 3) alone does not guarantee T4-validity — the no-adjacent-zeros, t₁ ≠ 0, and t_#t ≠ 0 conjuncts must also hold. The proof should explicitly verify these from agreement with s on positions 1..k−1 (inheriting s's T4 properties on the prefix) and from positions k..#t being all non-zero (since the three zeros are at p₁, p₂, p₃ < k).
**Required**: Add explicit T4-validity argument for t in the span before invoking origin(t).

### Issue 3: SV6 sub-lemma — implicit #t ≥ j assumption
**ASN-0051, SV6 sub-lemma proof**: "Since t ≥ s and t agrees with s on positions 1 through j−1, T1(i) gives tⱼ > sⱼ"
**Problem**: T1 case (i) requires both t and s to have a component at position j. The proof doesn't establish #t ≥ j. The argument: if #t < j, then t is a proper prefix of s (since t agrees with s on positions 1..#t < j ≤ #s), so by T1(ii) t < s, contradicting s ≤ t. This argument is needed before T1(i) can fire.
**Required**: Insert the prefix-exclusion argument to establish #t ≥ j before invoking T1(i).

### Issue 4: wp(K.μ⁺) assumes single mapping
**ASN-0051, Weakest Precondition Analysis**: "**wp(K.μ⁺ adding v_new ↦ i_new, π(e, d) ≠ ∅) = `π(e, d) ≠ ∅ ∨ i_new ∈ coverage(e)`**"
**Problem**: K.μ⁺ Effect (ASN-0047) allows adding any extension `dom(M'(d)) ⊃ dom(M(d))` — not a single mapping. The wp expression handles only the single-mapping case. For multiple new mappings adding I-addresses I_new, the wp should be `π(e, d) ≠ ∅ ∨ coverage(e) ∩ I_new ≠ ∅`.
**Required**: Generalize the wp to a set of new mappings (or restrict the K.μ⁺ characterization to single-mapping extensions and justify the restriction).

### Issue 5: wp(K.μ⁻) doesn't constrain V_rm to D-SEQ tail
**ASN-0051, Weakest Precondition Analysis**: "**wp(K.μ⁻ removing V_rm ⊆ dom(Σ.M(d)), π(e, d) ≠ ∅) = `(E v : v ∈ dom(Σ.M(d)) \ V_rm : Σ.M(d)(v) ∈ coverage(e))`**"
**Problem**: K.μ⁻ (ASN-0047) requires V_rm to be removed from the maximum end of V_S(d) per D-SEQ. The wp treats V_rm as arbitrary, but only D-SEQ-admissible V_rm sets are valid preconditions. An editor reading this wp could falsely conclude an arbitrary V_rm is permissible.
**Required**: State that V_rm must be a tail of V_S(d) (or all of V_S(d)) per D-SEQ as part of the wp's domain of applicability.

### Issue 6: SV0 — L-equality precondition extraneous, framing misleading
**ASN-0051, SV0**: "`Σ₁.L = Σ₂.L ∧ Σ₁.M(d) = Σ₂.M(d) ⇒ locate_{Σ₁}(e, d) = locate_{Σ₂}(e, d)`"
**Problem**: locate is defined as `{v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}` — taking the endset e directly as input, not derived from a link address. So locate doesn't depend on Σ.L at all; the L-equality precondition is vacuous. The "architectural, not definitional" framing is then misleading: by the definitions given, the claim is definitional, not architectural. The substantive claim ("no operation records or returns historical V-positions, so caching of stale V-positions is structurally precluded") is a meta-property of the *state-space schema*, not of the locate function.
**Required**: Either reformulate SV0 to make a substantive non-trivial claim (e.g., "Σ contains no historical-M field; the schema admits no resolution function R that takes more inputs than (e, current M(d))"), or acknowledge that SV0 restates the definition and explain what additional architectural commitment it expresses.

### Issue 7: SV2 proof attributes ran growth to "frame" instead of "effect"
**ASN-0051, SV2 proof**: "ran(M'(d)) ⊇ ran(M(d)) (K.μ⁺/K.μ⁺_L frame)"
**Problem**: The growth of ran(M(d)) comes from the K.μ⁺/K.μ⁺_L *Effect* (which extends dom while preserving existing V↦I mappings), not the Frame (which describes what's untouched in *other* documents and other state components). The frame for K.μ⁺ would say `(A d' : d' ≠ d : M'(d') = M(d'))` — irrelevant to the d under consideration.
**Required**: Replace "frame" with "effect" in the citation.

### Issue 8: SV11 distributivity step implicit
**ASN-0051, SV11**: "`π_text(e, d) = (∪ j, k : 1 ≤ j ≤ m ∧ 1 ≤ k ≤ p : ⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k))`"
**Problem**: The decomposition relies on set-distributivity of ∩ over ∪: π_text = coverage(e) ∩ (⋃_k I(β_k)) = ⋃_k (coverage(e) ∩ I(β_k)) = ⋃_k ⋃_j (⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k)) = ⋃_{j,k}(...). This algebraic step is left implicit. Combined with coverage(e) = ⋃_j ⟦(sⱼ, ℓⱼ)⟧ (the endset's span union), the formula is reachable but unstated.
**Required**: Insert the explicit distributive derivation (one or two lines) showing how the formula is obtained.

### Issue 9: Title doesn't match content
**ASN-0051, title**: "Link Projection Displacement"
**Problem**: The body never formalizes a "displacement" concept for links. The content is about *survivability* — projection π, location locate, discovery discover_s, and their behavior under arrangement transitions. The term "displacement" appears nowhere in the body in any technical sense.
**Required**: Either retitle (e.g., "Link Survivability" or "Link Projection and Discovery Survivability"), or introduce a formal "displacement" concept that ties to the body content.

## OUT_OF_SCOPE

### Topic 1: Link-subspace contribution to projection
**Why out of scope**: SV11 explicitly defers projection contributions through link-subspace V-positions (where endsets reference link addresses, per L13 ReflexiveAddressing) to "the Link Subspace ASN". The text-subspace partial result given here is well-formed; the link-subspace extension is a separate piece of work.

### Topic 2: Formal SV claims for same-origin coverage growth
**Why out of scope**: The "Content Allocation and Coverage Stability" section discusses same-origin growth mechanisms (sequential overshoot, child-depth entry via inc(t, k')) descriptively but defers formal SV claims to the allocator-discipline treatment in ASN-0034. The descriptive content motivates SV6's restriction to cross-origin without overcommitting.

### Topic 3: Higher-arity links (N > 3)
**Why out of scope**: The Scoping note defers treatment of N > 3 endset slots to ASN-0043, which already permits |L(a)| ≥ 3. The standard-triple framing here is a reasonable scope restriction.

### Topic 4: Empty document, multi-link interaction, and version-fork-link interactions
**Why out of scope**: Several Open Questions (overlap of independent links, fork-arrangement-link interaction, link discovery latency) belong in subsequent ASNs. The acknowledged deferral is appropriate.

VERDICT: REVISE
