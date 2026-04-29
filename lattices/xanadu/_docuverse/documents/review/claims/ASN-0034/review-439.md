# Regional Review — ASN-0034/TumblerSub (cycle 2)

*2026-04-23 04:50*

### Missing NAT-* axiom statements for axioms cited throughout
**Class**: REVISE
**Foundation**: self (the "Foundation Statements (current)" block declares "(none — this is a foundation ASN; review internal consistency only)")
**ASN**: Depends slots across T0, T1, Divergence, ZPD, TA-Pos, ActionPoint, TumblerAdd, TumblerSub cite **NAT-closure (NatArithmeticClosureAndIdentity)**, **NAT-wellorder (NatWellOrdering)**, **NAT-cancel (NatAdditionCancellation)**, and **NAT-discrete (NatDiscreteness)**, e.g.:
> "NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` for the numeral bounding that range." (TA-Pos)
> "NAT-wellorder (NatWellOrdering) — least-element principle…" (Divergence, ZPD, ActionPoint, TumblerAdd)
> "NAT-cancel (NatAdditionCancellation) — summand absorption…" (TumblerAdd, T1)
> "NAT-discrete (NatDiscreteness) — forward direction m < n ⟹ m + 1 ≤ n." (T1 Case 1, ActionPoint)

**Issue**: The ASN body includes fully stated axiom blocks for NAT-order, NAT-addcompat, NAT-sub, and NAT-zero in the same register one would expect for any foundation-level axiom here, but the four axioms above — which are load-bearing in the proofs of T1's trichotomy (Case 1 relies on NAT-discrete's contraposition), ActionPoint's existence (NAT-wellorder), TumblerAdd's dominance (NAT-cancel's summand absorption `n + m = m ⟹ n = 0`, NAT-closure's additive identity `0 + n = n`), and Divergence's case (i) (NAT-wellorder) — are never stated. Under the self-contained reading the block imposes, every proof step that unfolds `0 + n = n`, invokes a least element, contraposes `m < n ⟹ m + 1 ≤ n`, or applies summand absorption is ungrounded. In particular, "NAT-cancel's symmetric summand absorption `n + m = m ⟹ n = 0`" (TumblerAdd dominance) and "NAT-closure's additive identity `(A n ∈ ℕ :: 0 + n = n)`" (ActionPoint, TumblerAdd) are cited as if they are direct axiom clauses — but no axiom slot here posits either.

**What needs resolving**: Either (a) add axiom blocks for NAT-closure, NAT-wellorder, NAT-cancel, NAT-discrete in the same Axiom/Depends style used for NAT-order/NAT-addcompat/NAT-sub/NAT-zero, explicitly enumerating the clauses callers cite (at minimum: `1 ∈ ℕ`, `0 + n = n` for NAT-closure; `n + m = m ⟹ n = 0` for NAT-cancel; least-element principle for nonempty ℕ-subsets for NAT-wellorder; `m < n ⟺ m + 1 ≤ n` or at least its forward direction for NAT-discrete); or (b) reclassify these as imports from another foundation ASN and update the Foundation Statements block to declare that import, removing the "review internal consistency only" framing that implies self-containment.

VERDICT: REVISE
