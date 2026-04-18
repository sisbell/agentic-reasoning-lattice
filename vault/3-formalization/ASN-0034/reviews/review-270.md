# Cone Review — ASN-0034/TumblerSub (cycle 3)

*2026-04-18 10:18*

Reading through the ASN with attention to cross-property consistency.

### TumblerAdd's dominance proof invokes a "symmetric form" of summand absorption that may not be among NAT-cancel's stated clauses
**Foundation**: T0's exhaustive NAT-* enumeration describes NAT-cancel (NatAdditionCancellation) as bundling "additive cancellation (left, right, and summand absorption)". T0 further stipulates the enumeration is exhaustive and that commutativity of addition on ℕ is *not* included — a point TumblerAdd explicitly relies on when it routes its strict-advancement chain through right order-compatibility + left-identity `0 + wₖ = wₖ` precisely to avoid needing `1 + wₖ > wₖ`. The standard summand-absorption statement in ℕ is `(A m, n ∈ ℕ : m + n = m : n = 0)` — "appending a summand on the *right* and getting back the original forces that summand to be 0".
**ASN**: TumblerAdd's dominance proof, inner sub-case `aₖ > 0`: "NAT-cancel's summand absorption **in its symmetric form** `n + m = m ⟹ n = 0` (instantiated at `n = aₖ, m = wₖ`) rules out the equality `aₖ + wₖ = wₖ`." The Depends reiterates: "NAT-cancel's summand absorption in its symmetric form (`(A m, n ∈ ℕ : n + m = m : n = 0)`, instantiated at `n = aₖ, m = wₖ`) to rule out the equality disjunct `aₖ + wₖ = wₖ`". The phrase "symmetric form" is used precisely because this is *not* the standard `m + n = m ⟹ n = 0` form — it places the candidate-zero summand on the *left*, which under ℕ (without commutativity) is a distinct statement from the standard form.
**Issue**: T0's three-item summary of NAT-cancel — "left, right, and summand absorption" — is most naturally read as three clauses: left cancellation, right cancellation, and one form of summand absorption. For NAT-addcompat, T0 is explicit that the "two compatibility clauses cover [both directions]"; for NAT-cancel it is not explicit that summand absorption comes in both left-summand and right-summand forms. If only the standard `m + n = m ⟹ n = 0` form is stated, the "symmetric form" `n + m = m ⟹ n = 0` is not derivable without commutativity, which T0 excludes — and TumblerAdd's inner sub-case `aₖ > 0` depends on it. A route that uses only stated axioms is available (rewrite `aₖ + wₖ = wₖ` as `aₖ + wₖ = 0 + wₖ` via NAT-closure's left-identity, then apply NAT-cancel's right cancellation to cancel `wₖ` on the right and obtain `aₖ = 0`), but the present proof does not take it.
**What needs resolving**: Either (a) NAT-cancel's formal contract must explicitly state both forms of summand absorption as axioms (and T0's enumeration updated so that "summand absorption" is understood to bundle both, matching the precedent of NAT-addcompat bundling left and right order compatibility), or (b) the TumblerAdd dominance proof and its Depends must reroute the equality-rule-out through only those NAT-cancel clauses T0 actually states — most naturally via NAT-closure's left-identity rewrite followed by right cancellation — with the narrative and Depends updated to reflect the new citation chain.

## Result

Cone converged after 4 cycles.

*Elapsed: 2860s*
