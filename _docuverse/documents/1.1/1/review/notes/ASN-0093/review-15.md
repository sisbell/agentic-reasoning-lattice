# Review of ASN-0093

## REVISE

### Issue 1: FirstEmissionFreshness's link case left as "symmetric"
**ASN-0093, FirstEmissionFreshness proof**: "Take the content case; the link case is symmetric."
**Problem**: The lemma is consumed at both K.α and K.λ first-emit precondition discharge. The content case proof has two distinct sub-proofs (against dom(C) using ChainPrefixExtension + ChainMembershipForOrigin + Cross-document disjointness + T10; against dom(L) using L0 + SC-NEQ + StoreT4Validity + T7). The link case requires the *symmetric* but not identical substitution — and "symmetric" leaves the substitution rule implicit. Downstream ASNs citing this lemma for K.λ need to perform the C↔L substitution mentally.
**Required**: Explicitly state the link case proof, even if compactly. At minimum, give the substitution rule: "Against dom(L), use Cross-document disjointness lifted to (ℓ, ℓ' ∈ dom(L)); against dom(C), use SC-NEQ in the reverse direction."

### Issue 2: ChainPrefixExtension's inductive step for link case
**ASN-0093, ChainPrefixExtension proof step**: "The link case is symmetric, with b_L(d) in place of b_C(d) and A_L(d) in place of A_C(d)."
**Problem**: For an induction step that downstream proofs rely on heavily (cited in cross-document freshness derivations and FirstEmissionFreshness), having both content and link cases as explicit symmetric proofs improves auditability. The substitution rule is simple, but writing it out costs little and forecloses ambiguity.
**Required**: Carry out the link case's step explicitly or strengthen the substitution rule with named lemma swaps.

### Issue 3: DisjointSubAllocatorChains' implicit induction
**ASN-0093, DisjointSubAllocatorChains proof**: "Hence every element of A_C(d) inherits E_1 = s_C from t_1^C(d)..."
**Problem**: The proof states the conclusion of an induction over chain index without explicit base/step structure. The mechanism — TA5(b)/(c) preserving position #d + 2 at every step since sig = #d + 3 ≠ #d + 2 — is given, but the lift from per-step preservation to chain-wide preservation is not exhibited.
**Required**: Structure as: *Base*: t_1 has E_1 = s_C by FirstEmission's structural form. *Step*: Assume t_n has E_1 = s_C at position #d + 2. By ChainElementT4Validity, t_n is T4-valid, so TA5-SigValid gives sig(t_n) = #d + 3. By TA5(b) at k = 0, position #d + 2 (≠ sig(t_n)) is preserved across inc(t_n, 0); hence t_{n+1}'s value at #d + 2 equals t_n's. By IH, t_{n+1} has E_1 = s_C.

### Issue 4: Sub-case B.i with strict inequality not exercised in worked example
**ASN-0093, Worked Example**: Step 9 verifies Cross-document disjointness Case B at sub-case B.i with `#d = #d_alt = 5` (equality) and sub-case B.ii with `#d_alt < #d'` (strict). Sub-case B.i with strict `#d_1 < #d_2` is not exercised.
**Problem**: While the lemma's proof handles this sub-case generally, the worked example's role is to verify against concrete instances. Sub-case B.i with strict inequality is structurally distinct from the equality case (the witness extraction works through `d_1 ⋠ d_2` alone, not symmetrically). A reader cannot verify this sub-case fires correctly against a concrete document pair.
**Required**: Add a brief verification — either a fourth registered document with prefix-incomparable structure and strict shorter length, or an explicit walk-through of how `(d, d_alt')` with `d_alt' = [3, 0, 7]` would resolve under sub-case B.i strict.

### Issue 5: Frame quantifier range underspecified
**ASN-0093, K.α frame / K.λ frame**: "L' = L; dom(M') = dom(M); (A d' :: M'(d') = M(d'))"
**Problem**: The universal `(A d' :: M'(d') = M(d'))` has no explicit range. The intended reading (over `dom(M)` under partial-function semantics, or over T with the convention that undefined equals undefined) is clarified parenthetically below ("Under partial-function semantics the two together force M' = M"), but the frame clause itself should be self-contained.
**Required**: Either explicitly state `M' = M` (after asserting `dom(M') = dom(M)`) or quantify over `d' ∈ dom(M)` directly.

### Issue 6: SubAllocatorAxiom.Exists's "permanence" argument relies on circular-feeling discharge
**ASN-0093, SubAllocatorAxiom.Exists explanation**: "The axiom commits *activation at every Σ in which d ∈ dom(M)* — it does not directly assert 'once active, always active.' The permanence reading... follows as a *consequence*, not as additional axiom content: it is the composition of this axiom with M1."
**Problem**: The justification reads that M1 supplies the permanence, but M1 itself is one of the transition-indexed invariants established by simultaneous induction. At the inductive base (Σ_0 = (∅, ∅, ∅)), dom(M) is empty so no chain is active; the first activation happens at the first K.σ event. M1 governs subsequent transitions. This is sound but the prose could clarify that the "permanence reading" is established inductively along with all other transition-indexed invariants — not as a separate corollary fact.
**Required**: Clarify that the permanence reading is part of what the simultaneous induction establishes, not an after-the-fact corollary requiring M1 to already be in scope.

VERDICT: REVISE
