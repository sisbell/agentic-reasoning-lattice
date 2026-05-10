# Review of ASN-0061

## REVISE

### Issue 1: D-PRE(v) is unsatisfiable as stated
**ASN-0061, Precondition**: "⟦(p, w)⟧ ⊆ V_S(d) where ⟦·⟧ is span denotation (ASN-0053)"
**Problem**: Span denotation (ASN-0053) is defined as `⟦σ⟧ = {t ∈ T : start(σ) ≤ t < reach(σ)}` — all tumblers in the range, at every depth. For p = [1, 2] and reach = [1, 4], the denotation includes [1, 2, 1], [1, 3, 5, 7], and infinitely many other tumblers of depth > 2 (by T0(b) and T5). Since V_S(d) contains only tumblers of fixed depth #p (by S8-depth), these deeper tumblers are not in V_S(d). The subset condition is unsatisfiable for any non-trivial span.
**Required**: Replace with a depth-restricted predicate, e.g.: `(A v : subspace(v) = S ∧ #v = #p ∧ p ≤ v < p ⊕ w : v ∈ V_S(d))`. The rest of the ASN (three-region partition, D-LEFT, D-DEL, D-SHIFT) correctly works with V_S(d) directly, so only this precondition needs repair.

### Issue 2: The displacement w is used at two incompatible depths
**ASN-0061, Precondition / D-SHIFT / D-SEP**: w is defined as "a positive ordinal displacement (an element-local displacement of the same depth as the V-positions, per TA7a)"
**Problem**: For span arithmetic (p ⊕ w = r), w must be at V-position depth. The worked example confirms: p = [1, 2], w = [0, 2], r = [1, 4]. But for the shift σ(v) = (S, ord(v) ⊖ w), w must be at ordinal depth. The worked example silently switches: "ordinal [4] ⊖ [2] = [2]" — using [2] (depth 1), not [0, 2] (depth 2). At ordinal depth 1, [4] ⊖ [0, 2] would give [4, 0] ⊖ [0, 2] = [4, 0] (divergence at position 1, a₁ = 4 ≠ 0 = w₁, so r₁ = 4, r₂ = 0). The subtraction does nothing. D-SEP's proof has the same gap: "(ord(p) ⊕ w) ⊖ w = ord(p)" requires w at ordinal depth for TA4 to apply (action point k = #a = 1, #w = 1). The block decomposition section introduces a third usage: "c₁ = p − v" treating the offset as a natural number, conflating tumbler subtraction with the integer offset in M4.
**Required**: Define an explicit projection w_ord from the V-depth displacement to the ordinal-depth displacement (e.g., w_ord = [w₂, ..., w_{#w}] stripping the leading zero). State D-SHIFT using w_ord. Show that ord(r) = ord(p) ⊕ w_ord and that the shift σ uses w_ord. Clarify the relationship between the natural-number block offset c and the tumbler displacement.

### Issue 3: ord(v) is used throughout but never defined
**ASN-0061, D-SHIFT**: "let σ(v) be the V-position in subspace S with ordinal ord(v) ⊖ w"
**Problem**: The function ord(v) appears in D-SHIFT, D-SEP, D-BJ, D-DP, and the block decomposition section, but is never defined. TA7a (ASN-0034) establishes the concept — "a position in subspace S with identifier N and ordinal o" — but the extraction function from V-position to ordinal and the reconstruction from (S, ordinal) back to V-position are not stated. The reader can infer ord([S, k₁, ..., kₘ]) = [k₁, ..., kₘ], but a specification should define its terms.
**Required**: Add a definition: for a V-position v with #v = m and subspace(v) = v₁, define ord(v) = [v₂, ..., vₘ] (the ordinal portion per TA7a). Define the reconstruction: vpos(S, o) = [S, o₁, ..., oₘ] for subspace S and ordinal o of depth m.

### Issue 4: Proofs restricted to depth 2 but claims unrestricted
**ASN-0061, D-PRE(iv)**: "#p ≥ 2 (same depth constraint as insertion)"
**Problem**: The precondition allows V-positions of any depth ≥ 2 (ordinal depth ≥ 1). But every non-trivial proof is restricted to depth 2 / ordinal depth 1:

- **D-SEP**: TA4 requires "∀i : 1 ≤ i < k : aᵢ = 0" — vacuously true at ordinal depth 1 (k = 1) but fails at depth > 1 where ordinal components are positive (S8a). The round-trip (ord(p) ⊕ w) ⊖ w = ord(p) is not established for deeper ordinals. The ASN itself acknowledges this in Open Questions.

- **D-BLK B3 consistency**: "σ(v) + j = σ(v + j)" is proven only "At depth 1 (standard case): [(vₘ − w_c) + j] = [(vₘ + j) − w_c] by commutativity and associativity of ℕ arithmetic." At ordinal depth 2, subtraction does not commute with increment through TumblerSub because TumblerSub's tail-copy rule interacts with the multi-component structure.

- **D-DP Case 2/3**: contiguity preservation by σ relies on the shift commuting with ordinal increment, which is only shown at depth 1.

**Required**: Either restrict D-PRE(iv) to #p = 2 and note depth > 2 as future work, or provide depth-general proofs. The former is sufficient — the ASN already flags the generalization as an open question.

### Issue 5: D-DP Case 2 contiguity argument is circular
**ASN-0061, Contiguity Preservation, Case 2**: "σ maps the contiguous set R to positions from σ(r) onward contiguously, so every intermediate position is covered"
**Problem**: The claim that σ maps a contiguous set to a contiguous set is exactly what's being proved. The argument says "the preimage σ⁻¹ is also order-preserving ... so σ⁻¹(v) exists in the range [u, w] — provided v is in the range of σ." The clause "provided v is in the range of σ" is the hypothesis under proof. The argument never discharges it. At depth 1 the proof is trivial: consecutive integers shifted by a constant remain consecutive. But the ASN avoids this direct argument in favor of a general-sounding but circular one.
**Required**: State the depth-1 argument directly: if R occupies ordinals {a, a+1, ..., b}, then σ maps them to {a − w_c, a − w_c + 1, ..., b − w_c}, which are consecutive. Contiguity follows from integer subtraction preserving the unit gap between consecutive ordinals. Case 3 (L ∪ Q₃ contiguous) then follows from D-SEP establishing that max ordinal of L is ord(p) − 1 and min ordinal of Q₃ is ord(p).

### Issue 6: D-CTG's status as a system invariant is unresolved
**ASN-0061, Arrangement Contiguity**: "We take D-CTG as an invariant of every reachable state."
**Problem**: The ASN claims invariant status but (a) does not verify D-CTG at Σ₀ (trivially holds — V_S(d) = ∅ for all d — but should be stated), and more importantly (b) does not reconcile D-CTG with ASN-0047's transition framework. A bare K.μ⁻ removing a single interior V-position is a valid composite transition under ASN-0047 (J2 is satisfied, J0/J1/J1' are vacuous), yet it violates D-CTG. So D-CTG is not preserved by all valid composite transitions as ASN-0047 defines them. The ASN's own Open Questions ask whether D-CTG is a system-wide invariant or a per-operation precondition, showing the question is unresolved — yet the ASN simultaneously asserts invariant status.
**Required**: Either (a) classify D-CTG as a design constraint that further restricts which composites constitute well-formed operations (beyond ASN-0047's validity predicate), making this explicit, or (b) demote D-CTG to a precondition that DELETE assumes and preserves, deferring the system-wide question. Verify D-CTG at Σ₀ in either case.

## OUT_OF_SCOPE

### Topic 1: D-CTG preservation by INSERT, COPY, REARRANGE
**Why out of scope**: The ASN's scope explicitly excludes these operations. Each operation's ASN must prove D-CTG preservation independently.

### Topic 2: Link endset behavior when DELETE orphans I-addresses
**Why out of scope**: Link semantics are explicitly excluded from scope. The interaction between orphaned I-addresses and link endsets (which reference I-addresses, not V-positions) is a link-operations concern.

### Topic 3: Version reconstruction and historical backtrack
**Why out of scope**: Version creation is excluded from scope. The ASN correctly identifies that the pre-deletion state is recoverable in principle (content persists, provenance records survive), but the mechanism belongs in a version-management ASN.

VERDICT: REVISE
