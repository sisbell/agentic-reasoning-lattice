# Cone Review — ASN-0034/NAT-sub (cycle 1)

*2026-04-25 17:26*

I'll review the NAT-* axioms for internal consistency.

### NAT-sub body contains use-site inventory paragraph duplicating Depends
**Class**: OBSERVE
**Foundation**: n/a (structural)
**ASN**: NAT-sub body, final paragraph: "The axiom body invokes symbols beyond ℕ's primitive membership. The strict order `<` together with its non-strict companion `≤` and reverse companions `≥`, `>` — all defined in NAT-order by … — appear in the signature's domain condition…. The binary addition `+` closed over ℕ by NAT-closure appears in the sums `(m − n) + n`, `n + (m − n)`, `m + n`, and `n + m`. NAT-addbound's right-dominance clause … discharges the conditional-closure precondition implicit in the unguarded equation `(m + n) − n = m`…"
**Issue**: This entire paragraph is a use-site inventory of which dependency supplies which symbol, which is already what the Depends slot encodes. The body restates the Depends content in prose without advancing reasoning. Same "use-site inventory" pattern previous cycles flagged — here it has migrated from the Depends slot into the body, but the meta-prose nature is unchanged.

---

### NAT-sub Consequence slot carries export-decision commentary
**Class**: OBSERVE
**Foundation**: n/a (structural slot prose)
**ASN**: NAT-sub Consequence slot: "(strict monotonicity) — derived from the right-inverse clause … as shown in the preceding strict-monotonicity prose; **recorded as a Consequence rather than an axiom clause so the derivation is not laundered through a non-minimal clause**." And similarly for strict positivity: "**recorded as a Consequence rather than an axiom clause because its content is not purely subtractive — lifting `m − n ≠ 0` to `m − n ≥ 1` leans on NAT-discrete's structural commitment to discreteness of ℕ.**"
**Issue**: The Consequence slot states what the Consequence is and from what it's derived. The trailing dash-clauses justify *why* the claim is exported as Consequence rather than Axiom — a meta-decision about authorial design, not what the Consequence supplies. Editorial reasoning about export choice belongs in review notes, not the formal contract.

---

### NAT-sub body justifies export choices with defensive cross-axiom reference
**Class**: OBSERVE
**Foundation**: n/a (presentation)
**ASN**: NAT-sub body before strict-monotonicity derivation: "Strict monotonicity — `m ≥ p ∧ n ≥ p ∧ m < n ⟹ m − p < n − p` — is exported as a *Consequence:* rather than an additional axiom clause, because its content derives from the right-inverse together with … Retaining it as an axiom clause would launder that derivation through a non-minimal clause, **the same concern that kept NAT-order's disjointness form `m < n ⟹ m ≠ n` from being separately exported and left it as a derivable contrapositive** of the exactly-one-trichotomy Consequence's `¬(m < n ∧ m = n)` conjunct."
**Issue**: A defensive paragraph explaining why this Consequence is not an Axiom, anchored to a comparison with what NAT-order chose *not* to export. The cross-reference invokes a non-claim of a sibling axiom — m ≠ n as a non-export — to rationalize the present export choice. Reviser-drift pattern: prose around a claim explaining authorial design decisions rather than advancing the claim.

---

### NAT-sub strict-positivity export commentary
**Class**: OBSERVE
**Foundation**: n/a (presentation)
**ASN**: NAT-sub body: "Strict positivity — `m > n ⟹ m − n ≥ 1` — is exported as a *Consequence:* rather than an additional axiom clause, because its content is not purely subtractive: lifting `m − n ≠ 0` to `m − n ≥ 1` requires the discreteness fact that no natural number lies strictly between `0` and `1`, which NAT-discrete names."
**Issue**: Same pattern as the strict-monotonicity export paragraph. The first sentence justifies the slot choice; the strict-positivity derivation that follows would stand alone without this preface. The justificatory framing is editorial commentary about the contract's structure.

---

### "Unfolds via ≤-definition" misnames a one-way introduction step
**Class**: OBSERVE
**Foundation**: NAT-order ≤-definition `m ≤ n ⟺ m < n ∨ m = n`
**ASN**: NAT-sub strict-monotonicity derivation, `b < a` case: "The `b < a` case unfolds via NAT-order's `≤`-definition to `b ≤ a`; NAT-addcompat's right order compatibility applied at antecedent `b ≤ a` then delivers `b + p ≤ a + p`…"
**Issue**: "Unfolds … to `b ≤ a`" misdescribes the step. The biconditional `b ≤ a ⟺ b < a ∨ b = a` unfolds `b ≤ a` into the disjunction, not the reverse direction. Going from `b < a` to `b ≤ a` is disjunction-introduction (`∨`-intro) on the unfolded form, not unfolding. The conclusion is correct but the mechanic is misnamed.

---

### NAT-zero Depends slot omits NAT-carrier despite using ℕ in axiom clauses
**Class**: OBSERVE
**Foundation**: NAT-carrier (NatCarrierSet)
**ASN**: NAT-zero Depends: lists only NAT-order. NAT-zero's Axiom clauses — `0 ∈ ℕ`, `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` — and Consequence clause `(A n ∈ ℕ :: ¬(n < 0))` all use ℕ as primitive.
**Issue**: NAT-order is declared (supplying `<`) but NAT-carrier (supplying `ℕ` itself) is not. NAT-order does declare NAT-carrier in its Depends with the rationale that `<` is posited on ℕ and bounded quantifiers range over ℕ. NAT-zero's Axiom clauses make analogous use of ℕ but rely on transitive supply through NAT-order. The convention is workable but inconsistent: the same justification that earned NAT-carrier a direct slot in NAT-order would earn it one here. NAT-closure has the same gap.

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 176s*
