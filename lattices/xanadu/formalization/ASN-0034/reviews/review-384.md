# Regional Review — ASN-0034/TA-Pos (cycle 3)

*2026-04-22 22:27*

### NAT-order's Axiom slot contains the definition of `≤` alongside the axioms for `<`
**Class**: REVISE
**Foundation**: NAT-order (NatStrictTotalOrder)
**ASN**: NAT-order formal contract: "*Axiom:* `< ⊆ ℕ × ℕ` …; `(A n ∈ ℕ :: ¬(n < n))` (irreflexivity); `(A m, n, p ∈ ℕ : m < n ∧ n < p : m < p)` (transitivity); `(A m, n ∈ ℕ :: m < n ∨ m = n ∨ n < m)` (totality). **The non-strict relation `≤` on ℕ is defined by `m ≤ n ⟺ m < n ∨ m = n`.**"
**Issue**: The final sentence inside the *Axiom:* bullet is not an axiom — it is a definitional equivalence introducing the derived symbol `≤` from the primitive `<`. Sibling ASNs separate these roles explicitly: TA-Pos's formal contract carries a dedicated *Definition:* slot for `Pos`, `Zero`, `Z`, kept apart from its *Complementarity:* bullet. NAT-order folds the defined relation into its axiom slot, so a mechanical reader extracting "the axioms of NAT-order" sees four clauses where three would suffice, and a reader extracting "the definitions of NAT-order" finds nothing. The cycle-7 finding that carved Complementarity apart from Nonvacuity applied the same slot-discipline principle; it has not been applied here.
**What needs resolving**: Move the `≤` definition out of the *Axiom:* bullet — either into a separate *Definition:* slot parallel to TA-Pos's structure, or into prose — so the Axiom slot contains only clauses that posit or constrain the primitive `<`.

### T0 prose duplicates the *Depends:* slot's content as a use-site inventory
**Class**: OBSERVE
**Foundation**: T0 (CarrierSetDefinition)
**ASN**: T0 prose: "The numeral `1` bounding the length from below is the `1 ∈ ℕ` posited by NAT-closure; the relation `≤` is the non-strict order on ℕ defined by NAT-order. The inequality `1 ≤ #a` is thus well-typed within ℕ…". *Depends:* "NAT-closure … supplies `1 ∈ ℕ` for the lower bound of the nonemptiness clause `1 ≤ #a`. NAT-order … supplies the non-strict relation `≤` on ℕ appearing in the nonemptiness clause `1 ≤ #a`."
**Issue**: The prose sentence catalogues which dependency supplies which symbol in the clause `1 ≤ #a`, and the *Depends:* slot then says the same thing in structured form. This is the use-site-inventory pattern the review guidance names as noise — the prose explains provenance a precise reader can read off the Depends slot directly. Cycle-7 OBSERVE'd the analogous paragraph in TA-Pos ("typing-rationale"); T0 carries the same pattern and was not flagged there. (OBSERVE only — logged for register.)

VERDICT: REVISE
