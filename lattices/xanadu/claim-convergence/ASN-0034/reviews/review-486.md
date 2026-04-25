# Regional Review — ASN-0034/NAT-sub (cycle 1)

*2026-04-24 03:54*

### Use-site inventories in NAT-sub Depends slot
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: NAT-sub — Depends list for each of NAT-order, NAT-closure, NAT-addbound, NAT-addcompat, NAT-zero, NAT-discrete. Example: "NAT-order ... used in the signature's domain condition ... and in the antecedents ... of the conditional-closure and inverse-characterisation clauses; supplies the at-least-one trichotomy axiom and irreflexivity axiom, together with two conjuncts of the exactly-one-trichotomy Consequence — `¬(x < y ∧ y < x)`, against which the strict-monotonicity derivation dispatches the `a = b`, `b < a`-and-`<`, and `b < a`-and-`=` subcases, and `¬(m < n ∧ m = n)` at `(m, n) := (n, m)`..."
**Issue**: The Depends bullets catalog every use site of each import — the pattern explicitly flagged as degrading in the review discipline. The structural slot "which foundation is relied on" has been inflated with proof-body bookkeeping that the derivations themselves already carry.

### Meta-prose justifying Consequence-vs-Axiom placement
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: NAT-sub — "Retaining it as an axiom clause would launder that derivation through a non-minimal clause, the same concern that kept NAT-order's disjointness form `m < n ⟹ m ≠ n` from being separately exported and left it as a derivable contrapositive..." and, for strict-positivity, "recorded as a Consequence rather than an axiom clause because its content is not purely subtractive — lifting `m − n ≠ 0` to `m − n ≥ 1` leans on NAT-discrete's structural commitment to discreteness of ℕ."
**Issue**: These are defensive rationales about where to place a claim, not content of the claim. A consumer reading the Consequence does not need the placement argument; the derivation itself carries its own weight.

### Meta-prose defending Depends declarations in NAT-addcompat
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: NAT-addcompat — "Both foundations are declared in the Depends slot so that the axiom body can be read without silently importing them."
**Issue**: New prose around an axiom explaining why imports are declared rather than what the axiom says. The previous sentence already enumerates what each foundation supplies; the closing sentence adds nothing but justification of the bookkeeping.

### Inconsistent "this ASN" qualifier
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: NAT-discrete — Depends list: "NAT-closure (NatArithmeticClosureAndIdentity, this ASN)".
**Issue**: Only NAT-discrete uses the "this ASN" parenthetical on its NAT-closure dependency; NAT-addcompat, NAT-addbound, and NAT-sub reference NAT-closure without it. Minor surface inconsistency.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 211s*
