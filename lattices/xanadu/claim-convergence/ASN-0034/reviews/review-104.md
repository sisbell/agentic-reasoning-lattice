# Cone Review — ASN-0034/PositiveTumbler (cycle 1)

*2026-04-16 21:21*

### TA0 depends on undefined properties in a foundation ASN
**Foundation**: (none — this is marked as a foundation ASN)
**ASN**: TA0 (WellDefinedAddition): "TumblerAdd's piecewise construction yields a well-defined tumbler... By ActionPoint, `Pos(w)` yields a well-defined action point `k = actionPoint(w)`"; contract lists *Depends:* "TumblerAdd (TumblerAdd)" and "ActionPoint (ActionPoint)".
**Issue**: TA0's proof delegates entirely to TumblerAdd ("each component of the result lies in ℕ and `#(a ⊕ w) = #w ≥ 1`") and uses an `actionPoint` function from ActionPoint. Neither TumblerAdd nor ActionPoint is stated in this ASN, and the ASN metadata declares no external dependencies. A foundation ASN cannot cite non-existent properties; every cited name must be defined internally or in a declared dependency.
**What needs resolving**: Either state TumblerAdd and ActionPoint as properties of this ASN (with their own contracts), declare them as external dependencies in the ASN metadata, or move TA0 out of this ASN to wherever TumblerAdd/ActionPoint live.

### Numbering gap: T2 is missing
**Foundation**: n/a
**ASN**: Properties are labeled T0, T1, T3, TA0 — T2 is absent.
**Issue**: The jump T1 → T3 gives no indication of what happened to T2. A reader cannot tell whether T2 was deleted, renumbered, lives in another ASN and is cited by omission, or was never written. T3's proof references T0 and "the extensional characterisation," not T2, so no evidence suggests T2 would disrupt the chain — but the unexplained gap is itself a specification defect.
**What needs resolving**: Either renumber to close the gap or include a one-line note stating where T2 lives (and add it to declared depends if external).

### TA0 precedes its own prerequisites in document order
**ASN**: TA0 appears before the "Zero tumblers and positivity" section. TA0's precondition list uses `Pos(w)`, and its proof uses "ActionPoint" terminology. PositiveTumbler (which defines `Pos`) is stated after TA0, and its closing prose in turn cites TA0 as a "forward reference."
**Issue**: `Pos` is used in TA0 before it is defined. The dependency contract for PositiveTumbler explicitly tags TA0 as a forward reference, and TA0 implicitly forward-references PositiveTumbler. In a foundation ASN with no external citations, a strictly topological ordering should be possible: each property definable only in terms of properties stated earlier. The current layout forces the reader to read forward to resolve `Pos(w)` and then read back.
**What needs resolving**: Reorder so PositiveTumbler (and ActionPoint / TumblerAdd if they are to live here) are stated before TA0, eliminating the mutual forward references.

### PositiveTumbler has no property label
**ASN**: "**Definition (PositiveTumbler).** A tumbler `t ∈ T` is *positive*…"
**Issue**: Every other property is labeled with an identifier (T0, T1, T3, TA0) that other properties cite. PositiveTumbler is cited by TA0 (via `Pos(w)`) and by its own postcondition proof, but it carries no T-number. If a downstream ASN needs to cite it, there is no canonical handle; the ASN-internal citation pattern is inconsistent.
**What needs resolving**: Assign PositiveTumbler a property label consistent with the T/TA naming scheme, and update any internal citations to use that label.

### Section heading "Tumbler arithmetic" referenced but not present
**ASN**: PositiveTumbler's closing paragraph: "The condition `Pos(w)` in TA0 (WellDefinedAddition — forward reference, § Tumbler arithmetic below) excludes all all-zero displacements…"
**Issue**: The cross-reference points to "§ Tumbler arithmetic," but no such heading appears in the ASN content. TA0 is stated without a preceding section header. Either the heading was removed, or the cross-reference is aspirational.
**What needs resolving**: Add the section heading where TA0 lives, or correct the cross-reference to name the actual location.
