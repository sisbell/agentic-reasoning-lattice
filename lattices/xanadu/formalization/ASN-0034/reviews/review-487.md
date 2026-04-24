# Regional Review — ASN-0034/T4 (cycle 1)

*2026-04-24 04:17*

### Mis-attributed "disjointness axiom" of NAT-order
**Class**: REVISE
**Foundation**: NAT-order (axioms: irreflexivity, transitivity, at-least-one trichotomy; Consequence: exactly-one trichotomy, whose four conjuncts include `¬(m < n ∧ m = n)`)
**ASN**: T4, Exhaustion prose — "trichotomy's exactly-one clause — exported by NAT-order as a Consequence of the at-least-one axiom, **the disjointness axiom `m < n ⟹ m ≠ n`**, and irreflexivity+transitivity — then forbids the third."
**Issue**: NAT-order has no disjointness axiom. The statement `m < n ⟹ m ≠ n` is the contrapositive of the exactly-one Consequence's `¬(m < n ∧ m = n)` conjunct — it is part of exactly-one, not an input to its derivation. Attributing an axiom slot to it both mis-describes NAT-order and makes the derivation it sketches circular (exactly-one derived from disjointness, where disjointness is a conjunct of exactly-one). NAT-order's own body shows the derivation runs from at-least-one, irreflexivity, transitivity, plus indiscernibility of `=`.
**What needs resolving**: T4's account of how exactly-one is exported must either cite the three actual NAT-order axioms (and whatever logical principle it uses internally) or simply cite exactly-one as a NAT-order Consequence without re-deriving it inline with an imagined axiom.

### Defensive claim about "substitution of equals under `<`" being unavailable
**Class**: REVISE
**Foundation**: NAT-order (its Consequence's four-conjunct exactly-one trichotomy is derived in NAT-order's own body using indiscernibility of `=` — substituting `m = n` into `m < n` to rewrite as `m < m` against irreflexivity)
**ASN**: T4c, Exhaustion prose — "This uses trichotomy alone — neither transitivity, irreflexivity, nor substitution of equals under `<` is invoked, which matters because substitution of equals under `<` is not among NAT-order's stated properties." And again in Injectivity's closing clause "without appeal to substitution of equals under `<` (which Exhaustion already flagged as unavailable)."
**Issue**: Reviser drift. Two problems compounded: (i) the conjunct `¬(m < n ∧ m = n)` is part of NAT-order's exactly-one Consequence, so the substitution fact ("m = n ⟹ ¬(m < n)") is in NAT-order's stated properties — the parenthetical "not among NAT-order's stated properties" is false; (ii) NAT-order's own derivation of exactly-one relies on indiscernibility of `=` applied to `<`, so any consumer citing exactly-one (as T4c does) has already inherited that principle. The defensive clauses in Exhaustion and Injectivity explain what the claim does *not* use rather than what it uses, and mis-describe the foundation to justify a restriction that is not binding. They do not advance reasoning; they work around a non-existent hazard.
**What needs resolving**: T4c should either drop the defensive "not invoked / not among NAT-order's stated properties" remarks or replace them with a positive statement of the exactly-one conjunct actually being used. The Injectivity back-reference to the Exhaustion "flag" should go with it.

VERDICT: REVISE
