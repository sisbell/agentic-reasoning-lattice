# Review of ASN-0051

## REVISE

### Issue 1: SV6 proof's citation of S7b is misleading

**ASN-0051, SV6 (CrossOriginExclusion) proof, final paragraph**: "Since b is element-level (S7b — zeros(b) = 3), and every element-level t ∈ ⟦(s, ℓ)⟧ has origin(t) = origin(s), the contrapositive gives..."

**Problem**: S7b (ASN-0036) is `(A a ∈ dom(Σ.C) :: zeros(a) = 3)` — a property of content-store entries, not all element-level tumblers. The SV6 precondition already supplies `zeros(b) = 3` directly for any `b ∈ T`. Citing S7b here suggests the conclusion requires `b ∈ dom(Σ.C)`, but the proof works for any element-level `b`. The Worked Example later relies on SV6 applied to `j` *before* fully detailing its dom(C) status, so the appearance of an S7b dependency is potentially load-bearing-looking even though it isn't.

**Required**: Either drop the S7b parenthetical (the precondition stands alone), or rephrase as "Since `b` is element-level (zeros(b) = 3 from the precondition; consistent with S7b if `b ∈ dom(C)`)".

### Issue 2: SV5 proof's subspace preservation of ψ is implicit

**ASN-0051, SV5 (ReorderingProjectionInvariance)**: "Let ψ be the reordering bijection from K.μ~ (so that M'(d)(ψ(v)) = M(d)(v) for all v ∈ dom(M(d)))."

**Problem**: The proof of `locate_{Σ'}(e, d) = {ψ(v) : v ∈ locate_Σ(e, d)}` relies only on ψ being a bijection on `dom(M(d))` (K.μ~-FIX). But for an endset whose coverage spans multiple subspaces, the locate-image transformation is well-defined only if ψ preserves subspace membership. K.μ~-FIX itself states "subspace preservation (link-subspace fixity)" as one of its derivation premises (D-SEQ + bijection cardinality + subspace preservation), but SV5's proof does not surface this. A reader checking the proof against an arbitrary `ψ` could ask whether subspace-crossing permutations are admitted.

**Required**: Add a sentence stating that ψ preserves subspace (citing K.μ~-FIX's subspace-preservation clause), or note that the transformation formula holds even without subspace preservation because locate is defined pointwise on `dom(M(d))` — whichever is the intended reading.

### Issue 3: SV10 witness omits G and Θ specification

**ASN-0051, SV10 worked witness**: "Let a ∈ dom(Σ.L) be the link carrying F = {(i₁, ℓ_span)} so coverage(F) ⊇ {i₁, i₂, i₃} ∋ i₂."

**Problem**: L3 (ASN-0043) requires `|Σ.L(a)| ≥ 3` and `Σ.L(a).e₃ ≠ ∅`. The witness specifies only F (slot 1) and says nothing about G (slot 2) or Θ (slot 3). For the link's K.λ allocation to be valid in the constructed Σ, both G and Θ must be specified (with Θ non-empty). The witness chain enumerates K.δ, K.α, K.λ, K.μ⁺, K.ρ steps but the K.λ step's `(F, G, Θ) ∈ Link` precondition cannot be discharged without saying what G and Θ are. Additionally, K.λ also requires the link's *address* `ℓ` (with `zeros(ℓ) = 3` and `fields(ℓ).E₁ = s_L`) — but no candidate link address is supplied either.

**Required**: Specify the link's address (e.g., `a = 1.0.1.0.1.0.s_L.1` with `s_L ≥ 2` from SC-NEQ), and specify G and Θ explicitly (e.g., `G = ∅`, `Θ = {(τ, δ(1, #τ))}` for some chosen type-hierarchy tumbler τ), or note that G and Θ are arbitrary subject to L3 and that the witness is independent of their specific values. The same applies to the CrossDocumentDecoupling corollary which inherits `a` from this witness.

### Issue 4: Cross-document decoupling chain depends on SV10 ground-state allocations not enumerated

**ASN-0051, Cross-Document Decoupling corollary, "Setup precondition (inherited from SV10)"**: "We assume these K.δ allocations have taken place prior to Σ..."

**Problem**: The SV10 base-state Σ is asserted reachable from Σ₀, but the reachability chain itself is described only as "a standard composite chain" with "K.δ allocates the node entity at 1, the account entity at 1.0.1, and the document d itself". Per ASN-0047's `InitialState`, `E₀ = {n₀}` for a designated bootstrap node — the address of `n₀` is not fixed, and could be anything satisfying `IsNode(n₀)`. If `n₀ ≠ 1`, then "K.δ allocates the node entity at 1" is itself a step requiring its own preconditions (K.δ for root nodes requires no parent, but the node-1 address must be `ValidAddress` and `¬IsElement` — satisfied for a single-component tumbler `1`, but worth noting). The witness assumes `n₀` is either `1` or that allocating node `1` is admissible — but doesn't say which.

**Required**: Either fix `n₀ = 1` explicitly (it satisfies IsNode), or note that node 1 is allocated via K.δ if not already present. This is small but matters because both SV10 and CrossDocumentDecoupling are existence witnesses whose reachability claims should be airtight.

### Issue 5: SV11's iff-attainment direction stated but not proved

**ASN-0051, SV11 statement**: "The bound m · p is attained iff every (j, k) pair yields a non-empty decomposition term *and* these terms are pairwise non-adjacent within each block."

**Problem**: The proof body derives the strict-inequality criterion ("count < m·p whenever (a) some term is empty or (b) two non-empty terms within a single block are adjacent or overlap") — which is the reverse direction of the iff. The forward direction (both conditions ⇒ count = m·p) is implicit but not stated. A reader checking the iff has to invert the strict-inequality criterion themselves. Given that SV11 is the most structurally novel claim in this ASN, the iff deserves explicit two-direction support.

**Required**: Either state "the count inequality is strict iff (a) or (b) holds" with both directions, or split the iff into two named consequences (Forward: both conditions imply attainment; Reverse: attainment implies both conditions).

### Issue 6: SV6 element-level proof argues for arbitrary b, but precondition's k > p₃ scope-restriction not mirrored in SV13(f)

**ASN-0051, SV13 part (f)**: "*Cross-origin coverage exclusion:* new allocations from a different origin cannot enter existing endset spans when the span start is element-level and the action point is within the element field. [SV6]"

**Problem**: SV6's precondition is `k > p₃` (action point strictly past the third zero), not merely "within the element field". The element field starts at position `p₃ + 1`, so `k > p₃ ⟺ k ≥ p₃ + 1`, which is "at or beyond the first position of the element field". This matches "within the element field" if "within" is read inclusively from the field's start. But the body's careful k > p₃ formulation is conditioned in part on `k ≤ p₃` being a *broader-level span* (admitting cross-document coverage growth by design) — the synthesis should preserve this distinction. As written, "action point is within the element field" is correct but loses the structural reason.

**Required**: Tighten part (f) to: "action point lies strictly past the document field-separator (k > p₃)", or add a parenthetical "(equivalently, within the element field, but not at its first separator)".

## OUT_OF_SCOPE

### Topic 1: Reflexive/recursive endset chains

The ASN defers detailed treatment of link-subspace endsets to "the Link Subspace ASN" — this is appropriate. Questions about chains of links referencing other links (where SV-style discovery and projection compose recursively) are not in scope here.

### Topic 2: Same-origin coverage growth conditions

The ASN explicitly defers same-origin growth (sequential overshoot, child-depth entry mechanisms) to ASN-0034's allocator-discipline treatment. The "no formal SV claim" stance with descriptive prose is appropriate scope.

### Topic 3: Broader-level span survivability

Spans with `k ≤ p₃` (action point in document/account/node prefix) are explicitly out of scope per the ASN's own statement. The architectural reasoning for this deferral is sound.

VERDICT: REVISE
