The foundation statements are internally consistent and their exported contracts are clean. Dependent claims S7b, S7d, Σ.C, and S0 are axioms and pose no internal proof obligations. S7a and S7 carry substantive proof structure; I read both in full.

**S7a** establishes the existential `(A a ∈ dom(Σ.C) :: (E A_element ∈ 𝒯 :: a ∈ dom(A_element)))` and uses it with T10a.4 + S7b to place `a ∈ dom(U)` and `a ∈ dom(D)`, making the prefix projection well-formed. The two-membership discharge of T10a.4 is correct; the quantifier-order note (∀∃, not ∃∀) is correctly stated and necessary.

**S7** — I traced the Well-definedness section step by step: T0 comprehension (length `p` and component map `r`), the zero-count computation via T4 + NAT-card, the four-conjunct T4-validity discharge, Identification via S7a, Uniqueness via S7d + GlobalUniqueness, and Permanence via S0. Most of this proof is sound. One precondition for NAT-card's invocation is silently asserted rather than discharged.

---

### NAT-card invocation: upper-bound precondition for second zero position not discharged

**Class**: REVISE
**Foundation**: NAT-card (NatFiniteSetCardinality) — Axiom: `(A n ∈ ℕ, S : S ⊆ {j ∈ ℕ : 1 ≤ j ≤ n} :: |S|` is the unique `k ∈ ℕ` such that a strictly increasing enumeration `f : {1,...,k} → ℕ` with image exactly `S` exists)
**ASN**: S7 (StructuralAttribution), Well-definedness section — "the index set `{#N(a) + 1, ((#N(a) + 1) + #U(a)) + 1}` is a subset of `{1, …, p} ⊆ ℕ` — both members are positions in `r`'s domain `{j ∈ ℕ : 1 ≤ j ≤ p}`"
**Issue**: NAT-card's axiom requires `S ⊆ {j ∈ ℕ : 1 ≤ j ≤ n}` before `|S|` is assigned a value. The proof invokes NAT-card at `n = p` with `S = {#N(a)+1,\ X}` where `X = ((#N(a)+1)+#U(a))+1`. It establishes `#N(a)+1 ≤ p` (carried over from the length-bound argument `p ≥ #N(a)+1 ≥ 2`) but does not establish `X ≤ p`. The needed bound `X ≤ p` follows from `p = X + #D(a)` combined with `0 ≤ #D(a)` (NAT-zero), NAT-addcompat's left order-compatibility, and NAT-closure's right identity — all of which are in S7's Depends list — but none of this derivation appears in the proof. Similarly, the lower bounds `1 ≤ #N(a)+1` and `1 ≤ X` (each following from NAT-closure's `0 < n+1` and NAT-discrete's forward direction) are not traced. The assertion "both members are positions in `r`'s domain" is unproved, so NAT-card's formal precondition is not discharged.
**What needs resolving**: The proof must discharge `{#N(a)+1, X} ⊆ {j ∈ ℕ : 1 ≤ j ≤ p}` before invoking NAT-card. Specifically: `1 ≤ #N(a)+1` (NAT-closure `0 < n+1` at `n := #N(a)`, then NAT-discrete); `#N(a)+1 ≤ p` (already established); `1 ≤ X` (NAT-closure `0 < n+1` at `n := (#N(a)+1)+#U(a)`, then NAT-discrete); and `X ≤ p` (from `p = X + #D(a)`, NAT-zero `0 ≤ #D(a)`, NAT-addcompat left compatibility at `m := X, p_ineq := 0, n_ineq := #D(a)`, and NAT-closure right identity). Alternatively, the cardinality step may invoke NAT-card at `n = X` rather than `n = p` (both elements are trivially ≤ X), eliminating the `X ≤ p` obligation entirely.

---

### S7 Formal Contract Preconditions conflate caller obligations with proof-internal consequences

**Class**: OBSERVE
**Foundation**: N/A
**ASN**: S7 (StructuralAttribution), Preconditions — "`A_element ∈ 𝒯 ∧ a ∈ dom(A_element)` for the document owner's T10a-conforming element allocator (S7a)" and "`zeros(a) = 3` (S7b, element-level I-address)"
**Issue**: The second and third listed preconditions are not independent caller obligations — they are consequences of the sole genuine precondition `a ∈ dom(Σ.C)`, derived within S7's proof via the axioms S7a and S7b respectively. S7a holds for all `a ∈ dom(Σ.C)` and S7b holds for all `a ∈ dom(Σ.C)`; neither requires anything from the caller beyond that membership. Listing them as Preconditions presents the proof's internal discharge steps as external proof burdens, which a downstream formalization tool would read as requiring the caller to independently supply witnesses for `A_element` and establish `zeros(a) = 3` before invoking S7.
**What needs resolving**: The Preconditions section should list only the genuine caller obligation: `a ∈ dom(Σ.C)`. The derivation of `A_element ∈ 𝒯 ∧ a ∈ dom(A_element)` from S7a and `zeros(a) = 3` from S7b belongs in the proof body (where it already appears) or in a "Derived from precondition via S7a/S7b" annotation, not in the Preconditions slot.

---

VERDICT: REVISE