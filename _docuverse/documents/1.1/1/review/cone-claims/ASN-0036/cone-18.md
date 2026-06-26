The foundation statements are well-formed and internally consistent. The proof of S7 (StructuralAttribution) is the principal subject; I trace it in full before flagging.

**Well-definedness.** The sequence T4-validity via S7a → T10a.4, then T4b projections, then T0 comprehension for `origin(a) ∈ T`, is correctly assembled. The component map `r` is well-typed, the length bound `p ≥ 2 ≥ 1` is adequate, and the zero-count argument (`zeros(origin(a)) = 2` from the two separator positions) is correctly chained through NAT-addassoc's re-association and NAT-sub's left-telescoping. The four-conjunct T4-validity discharge for `origin(a)` (zero-count bound, non-adjacency, first-component, last-component) is structurally sound.

**No-two-zeros-adjacent case analysis.** The four-case elimination (matching the adjacent pair `(i, i+1)` to the two zero positions `{#N(a)+1, X}`) is complete and correctly ordered: the two equal-assignment cases close by irreflexivity `¬(i < i)` against NAT-addcompat's `i < i+1`; the order-reversed case closes by NAT-order's exactly-one trichotomy `¬(i < i+1 ∧ i+1 < i)`. The surviving case `i = #N(a)+1`, `i+1 = X` leads to the adjacency contradiction. One grounding step in that contradiction is wrong — see finding below.

**Identification, Uniqueness, Permanence.** All three sub-proofs are sound: Identification is tautological (S7a's axiom matches `origin`'s definition); Uniqueness correctly chains S7d (event-distinctness) through GlobalUniqueness (event-distinctness → address-distinctness) to tumbler-distinctness; Permanence is immediate from S0 and the fact that tumblers are immutable mathematical objects.

---

### `2 > 1` attributed to NAT-order + NAT-closure; NAT-addcompat required

**Class**: REVISE
**Foundation**: NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor clause `(A n ∈ ℕ :: n < n + 1)`
**ASN**: S7 (StructuralAttribution) — two locations: (1) the no-two-zeros-adjacent contradiction step in the Well-definedness section ("with `2 > 1` (NAT-order, the constant `2 := 1 + 1 ∈ ℕ` by NAT-closure) we now hold both..."); (2) the same phrase in the Postconditions ("against `2 > 1` (NAT-order, the constant `2 := 1 + 1 ∈ ℕ` by NAT-closure)")
**Issue**: The fact `2 > 1` (equivalently `1 < 2 = 1 + 1`) is attributed in both locations to "(NAT-order, the constant `2 := 1 + 1 ∈ ℕ` by NAT-closure)." Neither cited source establishes the claim. NAT-order axiomatizes the strict-order relation and defines `>` as `m > n ⟺ n < m`; it produces no specific ordering instance. NAT-closure's successor-positivity clause `(A n ∈ ℕ :: 0 < n + 1)` at `n := 1` establishes `0 < 2` (i.e., `2 > 0`), which is a different fact. Establishing `1 < 2 = 1 + 1` requires NAT-addcompat's strict successor `(A n ∈ ℕ :: n < n + 1)` instantiated at `n := 1`. The Depends entry for NAT-addcompat currently records only the `i < i + 1` use in the four-case walk, not the `1 < 2` use in the adjacency contradiction — so the gap is also in the declared dependencies, not only in the in-prose attribution. The contradiction turns on this: from `1 = #U(a) + 1 ≥ 2` the proof derives `1 ≥ 2` and then requires `1 < 2` to reach `1 < 1`; if `1 < 2` is ungrounded the contradiction is unestablished.
**What needs resolving**: Correct the attribution "(NAT-order, the constant `2 := 1 + 1 ∈ ℕ` by NAT-closure)" to "(NAT-addcompat's strict successor at `n := 1`, giving `1 < 1 + 1 = 2`; NAT-order's `>`-definition converts this to `2 > 1`)" at both sites. Update the Depends entry for NAT-addcompat to record this instantiation alongside the existing `i < i + 1` use.

---

### Postconditions section re-derives the adjacency contradiction in full

**Class**: OBSERVE
**Foundation**: N/A
**ASN**: S7 (StructuralAttribution) — Postconditions section, the parenthetical block beginning "were they adjacent at `i`, `i + 1`, both indices would lie among the two zero positions…" through "against NAT-order's irreflexivity `¬(1 < 1)` — the named contradicted fact"
**Issue**: The Postconditions section of S7's Formal Contract contains a near-complete re-derivation of the no-two-zeros-adjacent contradiction — four-case elimination, NAT-addassoc re-association, NAT-sub telescoping, `1 = #U(a) + 1 ≥ 2`, and the two-branch `1 < 1` argument — that duplicates the Well-definedness proof body. Postconditions should state what holds as consequences of the proof, not re-argue the steps. This also means the `2 > 1` attribution error (the REVISE above) appears twice and must be repaired in both locations.
**What needs resolving**: Condense the T4-validity postcondition for `origin(a)` into a statement of what was established ("the two separators are non-adjacent (difference `#U(a)+1 ≥ 2`)") without re-deriving it; cross-reference the Well-definedness section for the argument.

VERDICT: REVISE