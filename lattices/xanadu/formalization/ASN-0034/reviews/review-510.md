# Regional Review — ASN-0034/TA6 (cycle 1)

*2026-04-24 09:10*

### TA6 Conjunct 2 duplicates TA-PosDom's postcondition
**Class**: REVISE
**Foundation**: TA6 (ZeroTumblers); TA-PosDom (PositiveDominatesZero)
**ASN**: TA6 Postcondition (b): `(A s, t ∈ T : Zero(s) ∧ (E j : 1 ≤ j ≤ #t : tⱼ > 0) ⟹ s < t)`. TA-PosDom Postcondition: `(A t ∈ T, z ∈ T : Pos(t) ∧ Zero(z) :: z < t)`.
**Issue**: TA6's proof of Conjunct 2 reduces the hypothesis `(E j : 1 ≤ j ≤ #t : tⱼ > 0)` to `Pos(t)` via `tⱼ > 0 ⟺ tⱼ ≠ 0`, then invokes TA-PosDom directly. The resulting postcondition is the same tumbler-ordering fact with the positivity witness re-expressed. Two claim sites now export the same ordering fact — downstream consumers must choose, and any future revision to one must mirror the other. TA6 Conjunct 1 (zero tumblers are not valid addresses) is genuinely new content; Conjunct 2 is a re-statement packaged next to it.
**What needs resolving**: Decide whether TA6's scope is (a) only the invalidity claim, with the ordering fact referred back to TA-PosDom, or (b) a consolidated zero-tumbler summary that subsumes TA-PosDom. If (b), TA-PosDom's standalone postcondition becomes redundant in turn. Either way, remove the duplicate export so there is exactly one site stating "every zero tumbler is below every positive tumbler under T1."

### TA-Pos notation note references an undefined alternative ordering
**Class**: OBSERVE
**Foundation**: TA-Pos (PositiveTumbler)
**ASN**: "Note on notation (outside the formal contract). The predicate `Pos(t)` is written with a dedicated symbol rather than as `t > 0`: `>` is reserved for a separate tumbler ordering under which zero tumblers need not all be minimal..."
**Issue**: The note explains the notational choice by appealing to a "separate tumbler ordering" which is not defined in this ASN and is not cited as a forward reference to any named downstream claim. TA-PosDom establishes that under T1 zero tumblers are in fact all dominated by positive tumblers, so the reader cannot reconcile the stated reservation of `>` against any ordering present in the ASN. As it is explicitly flagged "outside the formal contract," soundness is unaffected, but the motivation is ungrounded prose.

VERDICT: REVISE
