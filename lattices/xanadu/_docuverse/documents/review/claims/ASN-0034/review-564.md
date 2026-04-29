# Cone Review — ASN-0034/T4b (cycle 3)

*2026-04-25 20:21*

### NAT-card body references T0's `#·` without declaring T0 as a dependency
**Class**: REVISE
**Foundation**: n/a (internal)
**ASN**: NAT-card (NatFiniteSetCardinality), Axiom-slot prose: "The operator `|·|` is distinct from T0's tumbler-length `#· : T → ℕ`, which acts on sequences rather than sets." NAT-card's *Depends* slot lists only NAT-order, NAT-closure, NAT-zero — not T0.
**Issue**: NAT-card's body references `T0` and `T0`'s tumbler-length `#·` directly, but the *Depends* slot does not declare T0. T0 and NAT-card are sibling foundations (T0 depends on NAT-order/NAT-closure; NAT-card depends on NAT-order/NAT-closure/NAT-zero). A foundation should not name another claim's symbol in its body without declaring the dependency, since a precise reader walking dependency order encounters `T0`'s `#·` before T0 has been introduced. The disambiguation `|·| ≠ #·` is also restated in T4's body where both operators are actually used together (T4 declares both T0 and NAT-card), so the remark is redundant at NAT-card and cleaner at T4.
**What needs resolving**: Either remove the T0-referencing remark from NAT-card and let T4 carry the disambiguation (T4 already does), or add T0 to NAT-card's *Depends* with a justification for why the type comparison sits in NAT-card rather than the consumer.

### T4b's image-in-T claim implicitly relies on T0 comprehension without citation
**Class**: OBSERVE
**Foundation**: n/a (internal)
**ASN**: T4b (UniqueParse). Body claims for each present projection: "the components listed lie in `ℕ⁺`, so the resulting sub-sequence belongs to the all-positive subset of `T`". Postconditions then state each projection "returns a nonempty finite sequence over `ℕ⁺` — an element of `T`". T4b's *Depends* entry on T0 mentions only the carrier, the index domain, the nonemptiness clause `1 ≤ #a`, and the subscript projection `·ᵢ`.
**Issue**: Asserting that the extracted sub-sequence `(t_{s_i+1}, ..., t_{s_{i+1}-1})` is itself an element of `T` requires T0's comprehension axiom (which guarantees that every length-and-component-map presentation of a nonempty finite sequence over ℕ is realised in T) plus extensionality (for uniqueness). The derivation invokes neither comprehension nor extensionality by name. A precise reader has to reconstruct that the embedding step is exactly T0's comprehension applied to `p := s_{i+1} − s_i − 1` and `r(j) := t_{s_i + j}`.

### T4 Axiom's quantifier "used as an address" is undefined within T4
**Class**: REVISE
**Foundation**: n/a (internal)
**ASN**: T4 (HierarchicalParsing) Axiom slot: "Every tumbler `t ∈ T` used as an address is T4-valid."
**Issue**: The phrase "used as an address" delimits the scope of the constraint but `address` has no definition in T4 or any of T4's declared dependencies. T4c later assigns four kinds of address (node, user, document, element) but T4c depends on T4, not the reverse, so the term cannot be imported from T4c without circularity. As stated, the Axiom is a constraint conditioned on an undefined predicate; consumers cannot determine to which tumblers the Axiom applies. T4b in particular treats "T4-valid" as the carved-out domain of `N, U, D, E` — but T4b's domain claim is `dom(N)` = T4-valid subset, not "tumblers used as addresses".
**What needs resolving**: Either drop the "used as an address" qualifier and state the Axiom as a constraint on the subset of T being characterised (e.g., introduce a distinguished subset `T_addr ⊆ T` defined as the T4-valid tumblers, or recast T4 as a definition of T4-validity rather than an Axiom imposing it), or define what "used as an address" means before the Axiom invokes the term. The downstream consumers (T4a, T4b, T4c) all use "T4-valid" directly as their predicate of interest; the Axiom should match.

### NAT-card axiom phrasing packs existence and uniqueness into "the unique"
**Class**: OBSERVE
**Foundation**: n/a (internal)
**ASN**: NAT-card (NatFiniteSetCardinality) Axiom slot: "`|S|` is the unique `k ∈ ℕ` such that `(E f :: f : {j ∈ ℕ : 1 ≤ j ≤ k} → ℕ ∧ ... ∧ S = {f.j : 1 ≤ j ≤ k})` — strictly-increasing-function characterisation, existence-and-uniqueness of `k` carried by 'the unique'".
**Issue**: The axiom relies on the definite-description device "the unique `k`" to simultaneously assert existence (some such `k` exists) and uniqueness (exactly one). The trailing parenthetical "existence-and-uniqueness of `k` carried by 'the unique'" is meta-commentary explaining what the formula does rather than stating substantive content. A precise reader would prefer the existence and uniqueness to be split into two clauses (or for the meta-remark to be elided).

VERDICT: REVISE
