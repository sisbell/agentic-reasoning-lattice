# Review of ASN-0043

## REVISE

### Issue 1: L11 non-injectivity formal statement is universally quantified but should be existential

**ASN-0043, IdentityByAddress — Non-injectivity**: "`¬(A a₁, a₂ ∈ dom(Σ.L) :: Σ.L(a₁) = Σ.L(a₂) ⟹ a₁ = a₂)` for any state with `|dom(Σ.L)| ≥ 2`"

**Problem**: This asserts that in every state with ≥ 2 links, there exist distinct addresses mapping to the same triple. False: a state with two links having different endsets is injective. Consider `dom(Σ.L) = {a₁, a₂}` with `Σ.L(a₁) = (F₁, G₁, Θ₁)` and `Σ.L(a₂) = (F₂, G₂, Θ₂)` where the triples differ — injectivity holds, contradicting the universal claim.

The "More precisely" paragraph and the witness construction give the correct existential formulation (any conforming state with a link can be extended to a non-injective conforming state), but the formal statement preceding them makes a different — and false — universal claim.

**Required**: Replace the formal statement with the existential formulation that the proof actually establishes:

`(A Σ satisfying L0–L14, a ∈ dom(Σ.L) :: (E Σ' extending Σ, a' ∈ dom(Σ'.L) :: a' ≠ a ∧ Σ'.L(a') = Σ.L(a) ∧ Σ' satisfies L0–L14))`

This says the invariants *permit* non-injectivity (every state with a link can be extended to a non-injective state), not that every multi-link state *is* non-injective.

### Issue 2: L9 proof cites wrong finiteness property

**ASN-0043, TypeGhostPermission — witness construction**: "such an address exists: by T0(b), `T` is unbounded, and `dom(Σ.C)` is finite by S8-fin"

**Problem**: S8-fin states "For each document `d`, `dom(Σ.M(d))` is finite" — it constrains arrangement domains, not the content store domain. No existing invariant in ASN-0034 or ASN-0036 establishes finiteness of `dom(Σ.C)`. The conclusion (a fresh ghost address exists) is almost certainly correct in any reachable state, but the cited property does not support it.

**Required**: Replace the S8-fin citation with a correct argument for the existence of `g ∈ T` with `fields(g).E₁ = s_C` and `g ∉ dom(Σ.C)`. One repair: by S7a (DocumentScopedAllocation), every address in `dom(Σ.C)` is allocated under some document's prefix. By T9 (ForwardAllocation), allocation within any document's content subspace is strictly increasing. By T0(a) (UnboundedComponents), components are unbounded, so addresses beyond any document's current allocation frontier always exist. A content-subspace address beyond the frontier of any document satisfies the requirements.

### Issue 3: L9 proof omits verification of six properties

**ASN-0043, TypeGhostPermission — verification**: The proof explicitly checks L0, L1, L1a, L3–L5, L11, L12, L14, and S0–S3 for the extended state `Σ'`. It does not address L2, L6, L8, L10, L12a, or L13.

**Problem**: All six are trivially preserved — L2 is structural (home is field extraction), L6 is vacuous (F = G = ∅ makes the antecedent false), L8/L10/L13 are lemmas that do not constrain states, L12a follows from L12. But a proof that explicitly checks 10 of 16 properties and silently omits 6 leaves the reader to close each gap independently. This is inconsistent with the worked example, which verifies every property (including vacuous cases) with explicit justification.

**Required**: Add a single line acknowledging the omitted properties. E.g.: "L2 holds structurally; L6 vacuously (F = G = ∅); L8, L10, L13 are lemmas not constraining states; L12a follows from L12."

## OUT_OF_SCOPE

### Topic 1: Finiteness of dom(Σ.C) and dom(Σ.L)

Neither the content store domain nor the link store domain has a formal finiteness constraint. The L9 proof exposed this gap when it needed — and incorrectly cited — a finiteness property for `dom(Σ.C)`. In reachable states (finitely many operations from an initial state), both domains should be finite, but the current invariants do not capture this. A finiteness invariant paralleling S8-fin (but for the content and link stores rather than arrangements) would close the gap.

**Why out of scope**: Foundation-level constraint belonging in ASN-0034/ASN-0036 or a future foundation ASN, not in the link ontology.

VERDICT: REVISE
