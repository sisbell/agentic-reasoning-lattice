# Cone Review — ASN-0034/PositiveTumbler (cycle 3)

*2026-04-16 21:57*

### T1 forward-references T3 in document order
**Foundation**: n/a (internal ordering)
**ASN**: T1 (LexicographicOrder) appears in § *The total order*; T3 (CanonicalRepresentation) appears in § *Canonical form*, which follows. T1's *Depends* clause explicitly annotates: "T3 (CanonicalRepresentation) [forward reference — T3 is stated in § Canonical form, after this section]".
**Issue**: T1's proof of trichotomy (part (b), Cases 1–3) load-bears on T3 to bridge component-level agreement/disagreement with tumbler equality/inequality. T3 depends only on T0, so a topological ordering is available — T3 could precede T1. The current layout forces the reader to accept a forward reference to resolve Case 1's conclusion `a = b` and Cases 2/3's conclusions `a ≠ b`. Previous finding #3 called out TA0's forward references; the T1 → T3 forward reference is a separate, independently fixable occurrence.
**What needs resolving**: Reorder so that T3 is stated before T1, and remove the "forward reference" annotation from T1's *Depends* clause.

### TA0 uses `Pos(w)` without citing a defining property
**Foundation**: n/a (foundation ASN)
**ASN**: TA0 (WellDefinedAddition), *Preconditions:* "a ∈ T, w ∈ T, Pos(w), actionPoint(w) ≤ #a (ActionPoint, this ASN)"; proof: "By ActionPoint (this ASN), `Pos(w)` yields a well-defined action point…".
**Issue**: `actionPoint(·)` is tagged with the citation "(ActionPoint, this ASN)", but `Pos(·)` has no citation tag and no corresponding entry in TA0's *Depends* clause. ActionPoint (as named in *Depends*) is about the action-point function, not the positivity predicate. Previous finding #1 addressed TumblerAdd and ActionPoint as undefined in-this-ASN citations; the predicate `Pos` is a distinct third name that is used but neither defined in the visible text nor listed in TA0's *Depends*.
**What needs resolving**: Either introduce a property (e.g., PositiveTumbler) that defines `Pos(·)` within the ASN and add it to TA0's *Depends*, declare a defining property as an external dependency in the ASN metadata, or inline the condition that `Pos(w)` abbreviates (e.g., `(E i : 1 ≤ i ≤ #w : wᵢ ≥ 1)`) so TA0's preconditions are self-contained.
