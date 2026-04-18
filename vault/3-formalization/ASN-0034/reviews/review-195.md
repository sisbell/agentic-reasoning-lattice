# Cone Review — ASN-0034/TumblerAdd (cycle 2)

*2026-04-17 19:54*

### Dominance proof's `aₖ > 0 ⟹ rₖ > wₖ` sub-case asserts strict advancement on the *left* summand without derivation or supporting axioms

**Foundation**: TumblerAdd (TumblerAdd) — dominance postcondition `a ⊕ w ≥ w`, inner case split at the action point inside the "aᵢ = 0 for all i < k" branch.

**ASN**: The proof establishes the strict-advancement postcondition `a ⊕ w > a` via an explicit chain *"`rₖ = aₖ + wₖ ≥ aₖ + 1 > aₖ`"* — NAT-addcompat's left order-compatibility lifts `wₖ ≥ 1` to `aₖ + wₖ ≥ aₖ + 1`, NAT-addcompat's strict successor inequality `aₖ < aₖ + 1` then supplies the strict step, and NAT-order composes. Inside the dominance proof, the symmetric conclusion is asserted in a single sentence: *"When `aₖ > 0`, `rₖ > wₖ` and T1 case (i) again gives `r > w`."*

**Issue**: The asserted step is `aₖ + wₖ > wₖ` under `aₖ > 0` — advancement on the *right* summand, not the left. The strict-advancement chain shown earlier cannot be reused symmetrically with the axioms as stated:

- Right order-compatibility lifts `aₖ ≥ 1` to `aₖ + wₖ ≥ 1 + wₖ`. To finish via strict successor, one would need `1 + wₖ > wₖ`, but NAT-addcompat states only `wₖ < wₖ + 1`, not `wₖ < 1 + wₖ`. The two forms coincide only under commutativity of addition on ℕ.
- Left order-compatibility with `aₖ ≥ 1` yields `wₖ + aₖ ≥ wₖ + 1 > wₖ`, but `wₖ + aₖ = aₖ + wₖ` again requires commutativity.
- A detour through NAT-sub's right telescoping (`(aₖ + wₖ) − wₖ = aₖ`) plus NAT-sub's strict positivity or NAT-order can discharge `aₖ + wₖ > wₖ` without commutativity, but this route is not taken and NAT-sub is cited in TumblerAdd's Depends only for the result-length identity.

T0's NAT-* enumeration is declared exhaustive and does not include a commutativity axiom (NAT-addassoc is listed, NAT-addcomm is not). The strict-advancement derivation is therefore *asymmetric*: it works when `wₖ ≥ 1` (the action-point's own guarantee) but not when the positivity sits on the start-position side `aₖ ≥ 1`, which is exactly the sub-case the dominance proof asserts without justification.

**What needs resolving**: Either (a) supply an explicit derivation of `aₖ > 0 ⟹ aₖ + wₖ > wₖ` using only the axioms in T0's exhaustive list (e.g., through NAT-sub right-telescoping + NAT-order, with the corresponding Depends additions), or (b) add commutativity of ℕ addition as a NAT-* axiom and update T0's exhaustive enumeration accordingly, or (c) restructure the dominance proof so the sub-case does not require strict advancement on the left summand. The current text asserts `rₖ > wₖ` at the same per-step granularity that every other strict inequality in this ASN is derived explicitly — leaving this one gap uniquely unjustified.
