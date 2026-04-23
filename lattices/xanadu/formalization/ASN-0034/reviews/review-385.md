# Regional Review — ASN-0034/TA-Pos (cycle 1)

*2026-04-22 23:06*

### NAT-order prose references a "closure clause" that NAT-closure no longer carries
**Class**: REVISE
**Foundation**: NAT-order (NatStrictTotalOrder)
**ASN**: NAT-order prose (final sentence): "NAT-closure follows the same register for the arithmetic primitive, opening its axiom slot with the signature `+ : ℕ × ℕ → ℕ` before the **closure and identity clauses**."
**Issue**: NAT-order's prose describes NAT-closure's Axiom slot as containing "closure and identity clauses." After the cycle-1 revision, NAT-closure's Axiom slot no longer contains a closure clause — it now holds only the signature, `1 ∈ ℕ`, and the left-identity clause. The cross-reference in NAT-order is a stale descriptor of a sibling whose shape has moved. A precise reader following the cited register to NAT-closure finds the described "closure clause" missing, and cannot tell whether NAT-order's sentence is advertising a structural feature NAT-closure should have (but doesn't), or was never updated when NAT-closure was trimmed. This is reviser drift from the cycle-1 edit not propagated to the sibling's descriptive prose.
**What needs resolving**: Update NAT-order's prose to describe NAT-closure as it now stands (e.g., "before the identity clause" or equivalent), or drop the enumerative descriptor. The cross-reference should match the current NAT-closure contract.

---

### NAT-closure *Depends:* slot contains non-dependency meta-content
**Class**: OBSERVE
**Foundation**: NAT-closure (NatArithmeticClosureAndIdentity)
**ASN**: NAT-closure Depends: "NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` appearing in the left-identity clause `0 + n = n`. **The binary operation `+ : ℕ × ℕ → ℕ` is not supplied by a dependency: it is posited directly by this axiom's first clause, in the same register NAT-order uses to posit `<`.**"
**Issue**: The second sentence is not a dependency declaration — it is meta-commentary about what is *not* a dependency, including a register cross-reference. The Depends slot's role is to list upstream axioms a mechanical reader can extract as edges in the dependency DAG; explanatory narration about non-dependencies belongs in prose. This is the same slot-discipline concern cycle-7 raised for TA-Pos's formal contract (prose-with-embedded-justification mixed with symbolic claims), now appearing in NAT-closure's Depends slot. (OBSERVE only — logged for register.)

---

### TA-Pos typing-rationale paragraph extends into a use-site inventory
**Class**: OBSERVE
**Foundation**: TA-Pos (PositiveTumbler)
**ASN**: TA-Pos prose: "`tᵢ` itself is a natural number by T0's carrier, the literal `0` against which it is compared is the `0 ∈ ℕ` posited by NAT-zero, the numeral `1` bounding the quantifier range is the `1 ∈ ℕ` posited by NAT-closure, and the relation `≤` bounding that range is the non-strict companion of `<` defined on ℕ by NAT-order…"
**Issue**: This continues the typing-rationale paragraph cycle-2 OBSERVE'd, but extends into a four-item use-site inventory cataloguing which dependency supplies each symbol inside the Pos/Zero quantifier bodies. Cycle-3 OBSERVE'd the analogous pattern in T0's prose for the single clause `1 ≤ #a`; TA-Pos carries a longer version of the same pattern, and a precise reader can read the four provenances directly off the Depends slot. (OBSERVE only — logged for register.)

VERDICT: REVISE
