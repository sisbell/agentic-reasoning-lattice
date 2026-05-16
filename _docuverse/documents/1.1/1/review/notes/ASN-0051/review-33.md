# Review of ASN-0051

Reading the ASN end-to-end and checking each SV claim's proof and worked-example verification.

## REVISE

### Issue 1: Notation inconsistency in worked example
**ASN-0051, "Two-span, non-injective scenario"**: "V-adjacency: v₆ = shift(v₁, 5)? Yes. ✓ I-adjacency: a₂ = a₁ ⊕ 5 = a₆?"

**Problem**: The expression `a₁ ⊕ 5` mixes the tumbler-addition operator ⊕ (defined on T × T via TumblerAdd, ASN-0034) with the numeric operand `5`. The OrdinalShiftBase convention in ASN-0058 specifies `t + k` (denoting `shift(t, k)` for k ≥ 1), which is the proper notation; `a₁ ⊕ 5` is informal and would parse formally as `a₁ ⊕ [5]` (a length-1 tumbler), which is *not* the same as `shift(a₁, 5)` when `#a₁ > 1`. The same paragraph also writes "a₅ + 1" (using the convention) and "v₆ = shift(v₁, 5)" (using shift). Three notations are mixed in one paragraph.

**Required**: Pick one notation. Either replace all numeric-operand uses of ⊕ with `+` (per OrdinalShiftBase), or replace them with `shift(·, n)`. The same fix applies wherever ⊕ appears with a numeric right operand (search for similar uses throughout the worked example and M7 merge-condition checks).

### Issue 2: CrossDocumentDecoupling witness omits referential-integrity discharge
**ASN-0051, Corollary (CrossDocumentDecoupling)**: "Introduce a second document d₂ ≠ d₁ with Σ.M(d₂) = {v₁ ↦ j} where j is any element-level T4-valid I-address satisfying origin(j) ≠ O"

**Problem**: For `M(d₂)(v₁) = j` to be part of a valid state, S3 (ReferentialIntegrity, ASN-0036) — and S3★ in the ASN-0047 extension — requires `j ∈ dom(Σ.C)` when `subspace(v₁) = s_C`. The witness must therefore *also* state that j has been allocated by some K.α step under a document whose origin differs from O, so that j ∈ dom(C) and origin(j) ≠ O simultaneously. The text says "admissible by SV6" but SV6 only forbids different-origin j from entering the span — it does not by itself construct j ∈ dom(C).

**Required**: Make the construction explicit: "Reach a state in which d₂ is allocated (K.δ) under a node/account prefix yielding `origin(d₂) ≠ O`; K.α allocates j with `fields(j).E₁ = s_C` under d₂'s prefix, so `origin(j) = origin(d₂) ≠ O` and `j ∈ dom(Σ.C)`; K.μ⁺ places `v₁ ↦ j` in `M(d₂)`. Then SV6 gives j ∉ coverage(F)."

### Issue 3: SV11 strictness analysis omits the empty-term mechanism
**ASN-0051, SV11**: "totalling *at most* m · p of them across all blocks; the inequality is strict whenever adjacent or overlapping decomposition terms within a single block coalesce into a single maximal fragment."

**Problem**: Two distinct mechanisms make the bound `m · p` strict, not one. The proof names *coalescence within a block* (non-empty adjacent terms merging into one fragment), but it omits the orthogonal mechanism: *empty decomposition terms* — pairs (j, k) where `⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k) = ∅` contribute zero fragments to the count. A trivial case: two non-adjacent spans, each intersecting only one of two blocks, gives 4 decomposition terms but 2 empty and 2 non-empty, so the fragment count is 2, well below m · p = 4 without any coalescence. The parenthetical "The 'at most' bound is reached when every non-empty decomposition term is itself a maximal fragment" implicitly requires *all* terms to be non-empty, but the proof text doesn't surface this requirement.

**Required**: Amend the strictness clause to read along the lines of: "the inequality is strict whenever (a) some decomposition term `⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k)` is empty, or (b) two non-empty terms in a single block are ordinally adjacent or overlap, coalescing into one fragment. The bound m · p is attained iff every (j, k) pair yields a non-empty term and these terms are pairwise non-adjacent within each block."

### Issue 4: SV11 cites M11/M12 for a restriction; the correct foundation lemma is C1a
**ASN-0051, SV11 statement**: "Let B = {β₁, ..., β_p} be the maximally merged block decomposition (M11, M12, ASN-0058) of the restriction M(d)|_{V_{s_C}(d)}."

**Problem**: ASN-0058 M11 and M12 are stated for `M(d)` directly, not for restrictions. The lemma that extends M11/M12 to arbitrary finite partial functions satisfying functionality, finite domain, and common depth ≥ 2 is C1a (RestrictionDecomposition, ASN-0058). The proof body correctly invokes C1a's conditions ("This restriction satisfies C1a's conditions: functionality from S2, finiteness from S8-fin, and fixed depth from S8-depth within subspace s_C"), but the statement above cites only M11/M12, which on their face do not cover restrictions.

**Required**: Replace the citation in the SV11 statement with `(C1a, ASN-0058)` — or write `(M11, M12 extended via C1a, ASN-0058)` — so the citation matches the lemma actually being applied.

## OUT_OF_SCOPE

### Topic 1: Survivability under composite/multi-step transitions
The SV claims are stated per elementary transition. Survivability across a chain Σ₀ → Σ₁ → … → Σₙ follows by induction, and the ASN's "open questions" section flags fork survivability explicitly. Formal multi-step survivability theorems (especially for J4 ForkComposite) are appropriate for a successor ASN.

### Topic 2: Link-subspace contribution to projection
SV11 deliberately scopes to the text-subspace projection π_text(e, d), explicitly deferring the link-subspace contribution to "the Link Subspace ASN." This includes the reflexive-addressing case (L13) and links-referencing-links. Acceptable deferral, not an error in this ASN.

### Topic 3: Broader-level spans (k ≤ p₃)
SV6 is explicitly restricted to action points strictly within the element field (k > p₃). The ASN gives three substantive reasons for deferring broader-level span survivability: SV2–SV5/SV11 carry through unchanged, SV6's exclusion is by design absent at broader levels, and udanax-green does not implement broader spans. Proper subject of ASN-0034's address-hierarchy treatment.

### Topic 4: Same-origin coverage-growth allocator discipline
The "Content Allocation and Coverage Stability" section is explicitly descriptive about TA5/T10a mechanisms (sequential overshoot, child-depth entry) and explicitly defers formal characterisation: "the precise allocator-discipline conditions that determine *which* same-origin allocations enter *which* spans are deferred to the allocator-discipline treatment in ASN-0034." Appropriate scope.

VERDICT: REVISE
