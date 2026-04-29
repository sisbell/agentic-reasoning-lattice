# Regional Review — ASN-0034/TA-Pos (cycle 2)

*2026-04-22 23:09*

### NAT-zero's "minimum" reading is walked in prose but never stated as an exported consequence
**Class**: REVISE
**Foundation**: NAT-zero (NatZeroMinimum)
**ASN**: NAT-zero formal contract: "*Axiom:* `0 ∈ ℕ` …; `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` …". NAT-zero prose: "Combined with NAT-order's irreflexivity `¬(n < n)` and transitivity …, these clauses identify `0` as the minimum — that no `n ∈ ℕ` satisfies `n < 0`. Suppose some `n ∈ ℕ` did satisfy `n < 0`; … the minimum reading of NAT-zero rests on NAT-order's irreflexivity and transitivity …". NAT-zero Depends: "… are what lift the disjunction `0 < n ∨ 0 = n` to the minimum reading `¬(n < 0)`."
**Issue**: The ASN name is `NatZeroMinimum` and the prose derives `(A n ∈ ℕ :: ¬(n < 0))` in full, citing it as "the minimum reading of NAT-zero." But the formal contract carries only the disjunction `0 < n ∨ 0 = n`; the minimum statement `(A n ∈ ℕ :: ¬(n < 0))` never appears as an exported clause in any slot (Axiom, Definition, or otherwise). A downstream ASN citing "NAT-zero's minimum claim" finds no formal statement to cite — only a prose walk or the strictly-weaker disjunction axiom. Sibling TA-Pos exports the derived equivalence explicitly in a dedicated *Complementarity:* bullet (`(A t ∈ T :: Pos(t) ⟺ ¬Zero(t))`) alongside a prose proof of the same shape; NAT-zero does the same derivation in prose but omits the parallel exported statement.
**What needs resolving**: Either add the minimum statement to the formal contract as a *Consequence:*/*Theorem:* bullet parallel to TA-Pos's *Complementarity:* (so the ASN's advertised content is citable), or rename/rescope the ASN so its formal contract matches what it exports. The prose derivation without a corresponding contract bullet is a gap between name and content.

---

### NAT-zero's *Depends:* entry carries an inline proof sketch
**Class**: OBSERVE
**Foundation**: NAT-zero (NatZeroMinimum)
**ASN**: NAT-zero Depends: "NAT-order (NatStrictTotalOrder) — supplies the strict-order primitive `<` used in the second clause; **its irreflexivity `¬(n < n)` and transitivity `m < n ∧ n < p ⟹ m < p` are what lift the disjunction `0 < n ∨ 0 = n` to the minimum reading `¬(n < 0)`.**"
**Issue**: The second half of the dependency entry is not a pointer — it is an inline proof sketch naming exactly which sibling axioms are invoked and what consequence they lift to. This is the same slot-discipline pattern cycle-3 OBSERVE'd for NAT-closure's *Depends:* ("meta-commentary … belongs in prose"), now appearing in NAT-zero's *Depends:* in a proof-sketch form. A mechanical reader extracting DAG edges has to parse past the sketch to find the dependency edge. (OBSERVE only — logged for register.)

---

### NAT-order prose carries a cross-reference to NAT-closure's structural register
**Class**: OBSERVE
**Foundation**: NAT-order (NatStrictTotalOrder)
**ASN**: NAT-order prose: "The axiom slot introduces `<` before constraining it: the first clause `< ⊆ ℕ × ℕ` posits `<` as a binary relation on ℕ, and the three strict-total-order clauses that follow then constrain that relation. **NAT-closure follows the same register for the arithmetic primitive, opening its axiom slot with the signature `+ : ℕ × ℕ → ℕ` before the unit-membership and left-identity clauses.**"
**Issue**: The bolded sentence describes NAT-closure's axiom-slot structure from inside NAT-order — a cross-reference advertising that a sibling follows "the same register." This is reviser narration: after the cycle-7 finding required NAT-closure to introduce `+` before constraining it, NAT-order's prose was updated to advertise the parity. The axiom content of NAT-order is unchanged by what shape NAT-closure takes; a precise reader can open NAT-closure directly and see its shape. (OBSERVE only — logged for register.)

VERDICT: REVISE
