# Regional Review — ASN-0034/TA-Pos (cycle 1)

*2026-04-22 16:09*

### NAT-zero "self-containment" claim contradicts its own semantics
**Foundation**: NAT-zero (NatZeroMinimum)
**ASN**: "The second clause is phrased with the primitives `<` and `=` rather than the defined `≤`, so NAT-zero is self-contained and does not presuppose NAT-order. … the disjunction ensures no element sits strictly below it under `<`."
**Issue**: The axiom `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` alone does not ensure "no element sits strictly below 0". To rule out `n < 0`, one must exclude: (a) `0 < n ∧ n < 0` (requires transitivity + irreflexivity from NAT-order), and (b) `0 = n ∧ n < 0` (requires irreflexivity from NAT-order). So the "minimum" reading of NAT-zero genuinely presupposes NAT-order, directly contradicting the "self-contained" prose.
**What needs resolving**: Either drop the self-containment claim and acknowledge the minimum-interpretation depends on NAT-order's irreflexivity/transitivity, or strengthen NAT-zero's formal axiom to directly forbid `n < 0`.

### "Nonempty" in T0 is never formalized as `#a ≥ 1`
**Foundation**: T0 (CarrierSetDefinition)
**ASN**: T0 formal contract: "T is the set of all nonempty finite sequences over ℕ, equipped with length `#· : T → ℕ`…" TA-Pos uses quantifier range `1 ≤ i ≤ #t`.
**Issue**: The word "nonempty" is prose; the formal contract never states `#a ≥ 1` for `a ∈ T`. Without that, `#t = 0` is not formally excluded, in which case the quantifier range `1 ≤ i ≤ #t` is empty, making `Pos(t)` vacuously false *and* `Zero(t)` vacuously true for the same `t` — i.e., the Pos/Zero dichotomy implicit in "Zero tumblers and positivity" fails at the empty-index case.
**What needs resolving**: T0's formal contract must carry `(A a ∈ T :: #a ≥ 1)` (or equivalent) so downstream dichotomy claims about Pos/Zero have a nonempty index domain to stand on.

### NAT-closure asserts "additive identity" but only states left identity
**Foundation**: NAT-closure (NatArithmeticClosureAndIdentity)
**ASN**: Prose: "with `0` as the additive identity." Formal contract: `(A n ∈ ℕ :: 0 + n = n)`.
**Issue**: "Additive identity" is a two-sided notion (`0 + n = n = n + 0`). Only the left identity is axiomatized. Without commutativity of `+` elsewhere, `n + 0 = n` is not derivable. The prose name overstates what is formally guaranteed.
**What needs resolving**: Either add `n + 0 = n` (or commutativity) to the formal contract, or downgrade the prose to "left additive identity".

### Pos/Zero relationship is not stated
**Foundation**: TA-Pos (PositiveTumbler)
**ASN**: "A tumbler `t ∈ T` is *positive*, written `Pos(t)`, iff … A tumbler `t ∈ T` is a *zero tumbler*, written `Zero(t)`, iff …"
**Issue**: The section is titled "Zero tumblers and positivity" and the note contrasts `Pos` against `Zero`, strongly implying dichotomy. But TA-Pos never asserts `Pos(t) ⟺ ¬Zero(t)`, nor exhaustiveness `Pos(t) ∨ Zero(t)`. Downstream claims that treat positivity as the negation of being a zero tumbler will have no anchor here — each would re-derive it, or silently assume it.
**What needs resolving**: Either add the dichotomy/exhaustiveness as part of TA-Pos's formal contract (grounded on `#t ≥ 1`), or explicitly state that Pos and Zero are independent predicates whose joint behavior is established elsewhere.

### `≠` is used without being introduced
**Foundation**: TA-Pos (PositiveTumbler)
**ASN**: `Pos(t)` iff `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`.
**Issue**: The symbol `≠` appears in the formal contract, but none of the cited dependencies introduces it. NAT-order supplies `<` and `=` and defines `≤`; `≠` is nowhere defined. TA-Pos's careful depends paragraph lists `≠` alongside `=` as "equalities and inequalities … well-typed within ℕ" without grounding.
**What needs resolving**: Either introduce `≠` as the negation of `=` (most naturally in NAT-order, alongside `≤`), or rephrase TA-Pos using `¬(tᵢ = 0)`.
