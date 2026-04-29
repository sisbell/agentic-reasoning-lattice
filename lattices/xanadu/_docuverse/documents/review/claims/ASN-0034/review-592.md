# Cone Review — ASN-0034/TA4 (cycle 4)

*2026-04-26 02:50*

### TumblerSub: "by T3 (contrapositive)" cites the wrong implication
**Class**: REVISE
**ASN**: TumblerSub. In the proof of `âₖ > ŵₖ`: "Since zpd is defined, `a` and `w` are not zero-padded-equal (ZPD), so by T3 (contrapositive) `a ≠ w`; combined with `a ≥ w`, this yields `w < a` (T1)."
**Issue**: T3 is the biconditional `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)` — its contrapositive is `a ≠ b ⟺ #a ≠ #b ∨ (∃ i : 1 ≤ i ≤ #a : aᵢ ≠ bᵢ)`, a statement about *native* components and lengths. "Not zero-padded-equal" is a statement about *padded* components on `{1, ..., L}`. The implication used here is "not-zero-padded-equal ⟹ a ≠ w", which is the contrapositive of "a = w ⟹ a, w are zero-padded-equal" — a fact that requires T3 *together with* ZPD's padded-projection definition, with a case split on whether the disagreement position lies in the shared native domain (`i ≤ #a ∧ i ≤ #w`, giving native component disagreement) or beyond it (giving `#a ≠ #w`). Citing "T3 (contrapositive)" alone elides this case split. The conclusion holds, but the citation chain does not ground it without the auxiliary derivation.
**What needs resolving**: Either expand the citation to record both ingredients (T3 contrapositive plus ZPD's padded-projection definition, with the case split on shared vs. padding-zone disagreement), or introduce a named lemma "a = w ⟹ zero-padded-equal" (with its derivation from T3 and ZPD) that this proof can cite directly.

### TumblerSub Definition: zero-tumbler branch lacks Postcondition
**Class**: REVISE
**ASN**: TumblerSub. The Formal Contract's *Postconditions:* slot states `a ⊖ w ∈ T`, `#(a ⊖ w) = L`, and the conditional Pos/actionPoint clauses "when zpd(a, w) is defined". When zpd is undefined, only the Definition slot's "a ⊖ w = [0, …, 0]" records the zero-tumbler shape.
**Issue**: TA4 case 2 (and any future caller hitting the no-divergence branch) relies on the fact "when zpd(a, w) is undefined, Zero(a ⊖ w)" — i.e., the result lies in **Z**. The TA4 proof says "the no-divergence branch yields the zero tumbler of length k" and concludes `(a ⊕ w) ⊖ w = a` from this together with the precondition that `a` is the zero tumbler of length k. The fact being consumed is that the result satisfies Zero in the no-divergence case, but this is not exported as a postcondition — only as a clause inside the Definition. A downstream consumer reading only the Postconditions slot cannot see this commitment. Either the Postconditions slot should record "when zpd(a, w) is undefined: Zero(a ⊖ w)" as an explicit conditional postcondition, or the Definition's role as a contract should be made explicit.
**What needs resolving**: Lift the no-divergence shape to the *Postconditions:* slot as a conditional postcondition `when zpd(a, w) is undefined: Zero(a ⊖ w)` (citing TA-Pos for the predicate), so that callers like TA4 can cite a postcondition rather than reading the Definition body.

VERDICT: REVISE
