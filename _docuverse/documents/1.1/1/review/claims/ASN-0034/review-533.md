# Regional Review — ASN-0034/TA-PosDom (cycle 1)

*2026-04-24 13:55*

### Case 1 closing uses `>` before it is introduced
**Class**: OBSERVE
**Foundation**: n/a (internal)
**ASN**: T1 trichotomy, Case 1: "Part (a) gives `¬(a < a)` and `¬(a > a)`."
**Issue**: The reverse abbreviation `a > b` is introduced only at the end of T1's block ("`a > b` abbreviates `b < a`"), after the proof. The Case 1 closing invokes `¬(a > a)` before that abbreviation has been declared in the document's forward reading order. The content is also telegraphic: the mutual-exclusion conjuncts of the trichotomy postcondition (`¬(a < b ∧ a = b)`, `¬(a < b ∧ b < a)`, `¬(a = b ∧ b < a)`) are discharged by substituting `a = b` and invoking irreflexivity, but the step "`¬(a < a)` and `¬(a > a)` ⟹ the three mutual-exclusion clauses hold under `a = b`" is left implicit.

### T3 sits between T0 and T1 structurally but is placed after T1
**Class**: OBSERVE
**Foundation**: n/a (internal)
**ASN**: T1 Depends cites "T3 (CanonicalRepresentation, this ASN)"; T3 is declared later in the section ordering (after the NAT-axiom cluster).
**Issue**: T1's proof cites T3 at three points (Case 1 concludes `a = b`, Cases 2 and 3 conclude `a ≠ b`), but T3 is stated after T1 in the document's linear order. T3's content is effectively T0's extensionality clause re-expressed as a biconditional plus Leibniz — its forward direction *is* T0's axiom. A reader encounters "by T3" before T3 is on the page, and once they reach T3 they find it is a near-restatement of a T0 axiom. The dependency DAG is sound; the presentation order invites a forward reference that could be avoided by citing T0's extensionality directly, or by declaring T3 before T1.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 497s*
