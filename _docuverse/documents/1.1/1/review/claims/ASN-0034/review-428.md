# Regional Review — ASN-0034/TA-MTO (cycle 1)

*2026-04-23 03:47*

### Meta-prose in TA-Pos definition
**Class**: OBSERVE
**Foundation**: (foundation ASN)
**ASN**: TA-Pos (PositiveTumbler) — the paragraph beginning "The bound variable `i` is typed to ℕ because the projection `tᵢ` is defined by T0 only on the index domain..." and continuing through "...requiring no additional symbol on ℕ."
**Issue**: This paragraph is a use-site inventory of symbol origins (where `0`, `1`, `≤`, `tᵢ` each come from) and a justification for why `i ∈ ℕ` is typed rather than content of the definition. Readers following the definition must skip past a full paragraph of type-hygiene prose to reach the complementarity claim. Reviser-drift pattern: new prose around a definition explaining why it is well-typed rather than what it says.

### Meta-prose in NAT-cancel axiom
**Class**: OBSERVE
**Foundation**: (foundation ASN)
**ASN**: NAT-cancel (NatAdditionCancellation) — "Both summand-absorption forms are stated independently because the NAT-* axioms of this ASN do not include commutativity of addition on ℕ, so neither form is derivable from the other. The same reason governs the independent statement of left and right cancellation."
**Issue**: Defensive justification for the shape of the axiom — explains why two forms are listed rather than stating the axiom. An axiom either posits these clauses or it does not; the non-derivability argument belongs in commentary, not in the axiom body.

### "By minimality of j" skips a small NAT dichotomy
**Class**: OBSERVE
**Foundation**: (foundation ASN)
**ASN**: TumblerAdd, dominance proof, Case some `aⱼ > 0`: "For 1 ≤ i < j: `aᵢ = 0` by minimality of `j`..."
**Issue**: Minimality of `j` in `{j : 1 ≤ j < k ∧ aⱼ > 0}` gives `¬(aᵢ > 0)` for `i < j` in that index range; concluding `aᵢ = 0` additionally uses NAT-zero + NAT-order dichotomy on ℕ. The surrounding proof is pedantic about citing NAT-* axioms at every step, so this one-step compression is a slight stylistic inconsistency rather than a gap.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 174s*
