# Regional Review — ASN-0034/T10 (cycle 1)

*2026-04-23 00:20*

### NAT-order axiom-slot meta-prose
**Class**: OBSERVE
**Foundation**: n/a (internal)
**ASN**: NAT-order axiom paragraph: "The axiom slot introduces `<` before constraining it: the first clause `< ⊆ ℕ × ℕ` posits `<` as a binary relation on ℕ, and the three strict-total-order clauses that follow then constrain that relation. NAT-closure follows the same register for the arithmetic primitive, opening its axiom slot with the signature `+ : ℕ × ℕ → ℕ` before the unit-membership and left-identity clauses."
**Issue**: The paragraph explains the structural pattern used in axiom slots (how the slot is organized, what register NAT-closure uses) rather than what the NAT-order axiom says. It is reviser drift of the "new prose around an axiom explains why the axiom is needed rather than what it says" form. The content of the axiom is fully carried by the formal contract.

### NAT-wellorder declaration-defence meta-prose
**Class**: OBSERVE
**Foundation**: n/a (internal)
**ASN**: NAT-wellorder prose: "NAT-order is therefore declared in the Depends slot so that the axiom body can be read without silently importing the definition" and "The set-theoretic primitives `⊆`, `∈`, and `≠ ∅` carry their standard first-order meaning ... they are not axiomatized by any NAT dependency and no NAT axiom is cited to ground them."
**Issue**: Both paragraphs are defensive justifications for the Depends declaration and for what is *not* axiomatized. They explain the declaration choices rather than the axiom content. The dependency on NAT-order is already carried by the Depends slot itself.

### T3 prose statement uses unquantified ellipsis
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: T3 statement: "`(A a, b ∈ T : a₁ = b₁ ∧ ... ∧ aₙ = bₙ ∧ #a = #b ≡ a = b)`"
**Issue**: The index bound `n` is not bound in the quantifier and the ellipsis is ambiguous when `#a ≠ #b`. The formal contract's `(A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)` form disambiguates; the headline statement does not. A precise reader must cross-reference the contract to resolve the range.

### T3 use-site inventory and motivation essay
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: T3 prose: "Gregory's implementation achieves T3 through a normalization routine ...", the `tumblercmp` misclassification walkthrough, and "T3 matters because address identity is load-bearing. If two representations could denote the same tumbler ..."
**Issue**: The Gregory paragraphs are a use-site inventory describing how an external implementation relies on T3 and what breaks when it fails; "T3 matters because ..." is a motivation essay. Neither advances the extensional-equality argument that T3 actually makes. They sit between the claim and its proof and must be skipped to follow the reasoning.

### T10 Depends mislabels the NAT-order properties invoked
**Class**: OBSERVE
**Foundation**: NAT-order (axiomatizes irreflexivity, transitivity, totality of `<`; defines `≤` via `m < n ∨ m = n`)
**ASN**: T10 Depends: "NAT-order (NatStrictTotalOrder) — trichotomy and transitivity of `≤` on ℕ."
**Issue**: Trichotomy is a property of `<`, not `≤`; NAT-order axiomatizes totality for `<` and defines `≤`. What T10's proof uses is (a) totality of `<` (via its `≤` companion) to split `m ≤ n` vs `m > n`, and (b) transitivity (of `<`/`≤`) for `k ≤ ℓ ≤ m ⟹ k ≤ m`. The cite compresses these into non-standard phrasing.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 133s*
