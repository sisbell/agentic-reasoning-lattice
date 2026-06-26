I will read the foundation statements, then trace S7's proof carefully for system-level gaps.

---

**Dependency structure.** ASN-0036 declares one claim cluster: S7 (StructuralAttribution) proved from axioms S0, S7a, S7b, S7d plus the imported foundation (T0, T4, T4a, T4b, T10a.4, GlobalUniqueness, and the NAT tower). The axioms are unchallenged; I concentrate on S7's proof.

**S7 Well-definedness — T4-validity of `a`.** The chain S7a → T10a.4 is correctly invoked: S7a delivers `A_element ∈ 𝒯` and `a ∈ dom(A_element)`; T10a.4 is instantiated at `A := A_element, t := a`; T4-validity of `a` follows. S7b supplies `zeros(a) = 3`. Both preconditions for the T4b projection calls are met. ✓

**Construction of `origin(a)` ∈ T.** T0 comprehension is instantiated at length `p = ((((#N(a)+1)+#U(a))+1)+#D(a))` and the block-wise component map `r`. The bound `p ≥ 1` follows from T4a's `#N(a) ≥ 1` lifted through `+1` by NAT-addcompat, plus non-negativity of the trailing summands; the `p ≥ 2` claim is correct. The map `r` sends each field position to a component of N(a), U(a), or D(a) (all in ℕ⁺ by T4b) and each separator position to `0 ∈ ℕ` (NAT-zero). T0's comprehension delivers `origin(a) ∈ T`. ✓

**Zero count `zeros(origin(a)) = 2`.** T4's definition is applied to `r`. The zero-index set is `{#N(a)+1, ((#N(a)+1)+#U(a))+1}`. NAT-addassoc re-associates the second position to `(#N(a)+1)+(#U(a)+1)`. NAT-sub left-telescoping at `n := #N(a)+1, m := #U(a)+1` gives the difference `#U(a)+1`. T4a's `#U(a) ≥ 1` lifts this to `#U(a)+1 ≥ 2 > 0`, so the two indices are distinct. NAT-card counts a two-element set with a strictly increasing enumeration: cardinality 2. ✓

**T4-validity of `origin(a)` — four conjuncts.**

- *Zero count* `2 ≤ 3`: immediate. ✓
- *First component non-zero*: position 1 is in the node block (since `1 < #N(a)+1 ≥ 2`); T4b gives `N(a)₁ ∈ ℕ⁺`. ✓
- *Last component non-zero*: position `p` is in the document block (since `#D(a) ≥ 1` places `p ≥ s₂+1`); T4b gives `D(a)_{#D(a)} ∈ ℕ⁺`. ✓
- *No two adjacent zeros*: see finding below.

**Identification and Uniqueness steps.** Identification cites S7a (axiom). Uniqueness routes S7d's event-distinctness through GlobalUniqueness to get tumbler-distinctness; T3 gives component-wise decidability. Both steps are sound. ✓

**Permanence.** S0 supplies address persistence; `origin(a)` is a deterministic function of `a`'s components, so it is unchanged across states. ✓

---

### No-two-adjacent-zeros contradiction step is unjustified
**Class**: REVISE
**Foundation**: NAT-sub (NatPartialSubtraction) — left-telescoping `(n + m) − n = m`; NAT-order (NatStrictTotalOrder) — irreflexivity; NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality
**ASN**: S7 (StructuralAttribution), Well-definedness, no-adjacent-zeros paragraph — "so the two separators differ by exactly `1`. But they differ by `#U(a) + 1`…`2 > 1` — a contradiction."
**Issue**: After identifying `i = #N(a)+1` and `i+1 = (#N(a)+1)+(#U(a)+1)`, the proof claims these two facts yield a contradiction via `#U(a)+1 ≥ 2 > 1`. The contradiction is never pinned. The proof does not state the key equating inference: applying NAT-sub's left-telescoping at `n := i, m := 1` gives `(i+1)−i = 1`; applying it at `n := #N(a)+1, m := #U(a)+1` gives `((#N(a)+1)+(#U(a)+1))−(#N(a)+1) = #U(a)+1`; since both compute the same difference (`i = #N(a)+1`), uniqueness of NAT-sub's output (it is a function) forces `1 = #U(a)+1`. Only then does `#U(a)+1 ≥ 2` give `1 ≥ 2`, contradicting irreflexivity (`¬(1 < 1)` via NAT-order). As written, the phrase "a contradiction" asserts the outcome without identifying what equals what, leaving the chain `1 = #U(a)+1 ≥ 2 > 1` entirely implicit.
**What needs resolving**: The proof must state the intermediate step: from `i = #N(a)+1` and `i+1 = (#N(a)+1)+(#U(a)+1)`, both applications of NAT-sub left-telescoping produce the difference of the same two positions, so `1 = #U(a)+1`; then `#U(a)+1 ≥ 2` gives `1 ≥ 2`, which NAT-order's strict order (and `2 > 1 > 0` established from NAT-closure's `2 := 1+1` and NAT-addcompat) contradicts. The word "contradiction" must name the contradicted fact.

---

### Unparenthesized five-way sum in a non-commutative context
**Class**: OBSERVE
**Foundation**: NAT-addassoc (NatAdditionAssociative)
**ASN**: S7 (StructuralAttribution), Well-definedness — "`p = #N(a) + 1 + #U(a) + 1 + #D(a)`"
**Issue**: Addition is not posited commutative at this stratum; the unparenthesized five-way sum is formally ambiguous. The proof implies left-to-right grouping — evident from the second-separator position written as `((#N(a)+1)+#U(a))+1` — but this parenthesization is never declared. NAT-addassoc bridges any two groupings, but the specific grouping used should be fixed once so that downstream references to sub-expressions (second separator, total length `p`) are unambiguous.
**What needs resolving**: Declare the parenthesization of `p` explicitly, e.g., `p = (((#N(a)+1)+#U(a))+1)+#D(a)`, matching the left-to-right grouping implied by the rest of the proof.

---

VERDICT: REVISE