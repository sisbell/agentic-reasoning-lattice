# Review of ASN-0042

I checked the foundation usage (ASN-0034, ASN-0040 — both permitted foundations), the eleven O-series proofs, the derived invariants, and the worked example. The mathematics is sound: the longest-match argument for O2, the refinement chain in O3, the irrevocability argument in O8, and the fork construction in O10 all close, and the worked-example witnesses are arithmetically consistent (e.g. `next(Σ.B,[1],2)=[1,0,3]`, `zeros=1=zeros(pfx(π_N))+1`). My findings are the forward-reference accretion patterns this pass is asked to surface.

## REVISE

### Issue 1: Duplicated document-ordering justification for the shared induction
**ASN-0042, O1a paragraph & State Axioms / Shared invariant induction**:
- O1a: "They share one induction, proved together in *State Axioms* under *Shared invariant induction* — sited after the axioms O12–O15, O14, and Freshness-(v) it consumes."
- Shared invariant induction: "...reachable-state invariants, established here — after the axioms O12–O15, O14 and the derived fact Freshness-(v) on which the base and step cases depend — by a single induction..."

**Problem**: Both passages assert the identical fact (O1a/O1b/T4-validity are joint invariants proved by one induction) and both justify *where* the induction sits relative to O12–O15/O14/Freshness-(v). The "— sited after ... it consumes" / "— after ... on which the base and step cases depend —" clauses are document-ordering justification, and the content is said twice. A reader following O1a must skip the placement essay to reach the claim.
**Required**: Keep one statement of the joint induction (at the proof site). Reduce the O1a mention to a bare forward pointer ("proved in *State Axioms*") and delete the ordering justification in both places.

### Issue 2: "supplied by O17b, not by (v)" role-disclaimer restated in ≥3 slots
**ASN-0042, O17b / Delegation definition / O7(c) / Properties table**:
- O17b: "O17b is the sole carrier of this form; delegation condition (v) gives only validity and freshness of `pfx(π')`."
- Delegation (introduced) and its table row: "the next-reachable baptism form `pfx(π') = next(Σ.B, p, d)` is supplied by O17b, not by (v)."
- O7(c) postcondition and proof: "(the form imposed by O17b)" … "O17b further fixes the form … not an arbitrary strict descendant of `pfx(π')`."

**Problem**: The same division-of-labor disclaimer (form comes from O17b, freshness/validity from condition (v)) is repeated across four locations. It is informative once; thereafter it is a use-site inventory that does not advance the local argument.
**Required**: State the O17b/condition-(v) split once (at O17b) and replace the other occurrences with a plain reference, or drop them.

### Issue 3: Role disclaimers and downstream-consumer inventories in the Properties table
**ASN-0042, Properties Introduced**:
- `pfx(π)` row: "(injectivity O1b and `zeros ≤ 1` O1a are derived invariants, not part of this axiom)."
- O14 row: "...bootstrap with finiteness/O1a/O1b/T4/non-nesting/O18 base cases."

**Problem**: The `pfx` parenthetical re-litigates what belongs to the axiom versus what is derived — a distinction already made at the axiom site. The O14 row enumerates which downstream invariants the axiom seeds (a downstream-consumer inventory) rather than stating O14's content. Both are noise in a summary slot.
**Required**: The table should state each property's claim. Remove the "derived, not part of this axiom" disclaimer and the seed-list inventory; if the axiom/derived split needs recording, it belongs once at the definition, not in the index.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer invariants
The Open Questions correctly defer transfer (O3 describes only the refinement regime; Nelson's "bought the document rights" is noted as having no implementation mechanism). This is future territory, not a defect here.

VERDICT: REVISE
