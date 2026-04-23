# Regional Review — ASN-0034/TA5a (cycle 2)

*2026-04-23 01:56*

Reading the ASN end-to-end for new issues not covered by previous findings.

### T4a hedges T0's explicit length axiom as a "local unpacking"
**Class**: OBSERVE
**Foundation**: T4a (SyntacticEquivalence), preamble
**ASN**: "T0 declares every `t ∈ T` to be a nonempty finite sequence over ℕ; a nonempty sequence has at least one component, so by the definition of length `#t ≥ 1` — this is a local unpacking performed here, not a postcondition cited from T0."
**Issue**: T0's Formal Contract Axiom literally reads "T is the set of finite sequences `a` over ℕ satisfying `1 ≤ #a`" — `1 ≤ #a` is a named clause of T0's axiom, not something T4a must unpack locally. The hedge "not a postcondition cited from T0" contradicts T0 as stated in this same document and adds meta-prose without advancing the proof. T4a can cite T0 directly for `#t ≥ 1`.

### NAT-zero Consequence proof carries a parenthetical meta-remark on equality
**Class**: OBSERVE
**Foundation**: NAT-zero (NatZeroMinimum), Consequence derivation
**ASN**: "`0 = n` rewrites `n < 0` to `0 < 0` by indiscernibility of `=` — a logical property of equality available throughout, not a property of `<` — again contradicting irreflexivity."
**Issue**: The em-dashed aside explaining why indiscernibility of equality is not a `<`-property (and by implication why no separate dependency is declared for it) is defensive justification about dependency bookkeeping rather than substance of the derivation. Matches the "new prose around an axiom explains why the axiom is needed rather than what it says" pattern flagged in the review discipline. The derivation reads cleaner with the aside removed.

VERDICT: OBSERVE

## Result

Regional review converged after 2 cycles.

*Elapsed: 694s*
