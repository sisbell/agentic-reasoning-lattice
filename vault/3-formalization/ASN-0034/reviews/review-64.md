# Cone Review — ASN-0034/D0 (cycle 3)

*2026-04-16 01:59*

### ActionPoint is a phantom external dependency, not an internal definition
**Foundation**: TumblerAdd (TumblerAdd), formal contract: "Depends: … ActionPoint (ActionPoint) — supplies `k = actionPoint(w)` with bounds `1 ≤ k ≤ n` and `wₖ ≥ 1`"
**ASN**: No section defines a property named ActionPoint. TA0's formal contract references `actionPoint(w) ≤ #a (ActionPoint)`. TumblerAdd's body text says "By ActionPoint, the precondition `Pos(w)` yields a well-defined action point."
**Issue**: TumblerAdd's Depends clause lists ActionPoint as something it *consumes* — an external property that must exist independently. Yet ActionPoint has no definition, formal contract, or axiom statement anywhere in the document. This is structurally identical to the T0 phantom: the function `actionPoint`, its domain restriction to positive tumblers, its codomain `{1, …, #w}`, and its defining equation `min{i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}` are scattered across prose in TumblerAdd's body but never formalized as a standalone property. The issue is not merely one of document ordering — TumblerAdd explicitly does not define actionPoint; it depends on a property that does not exist.
**What needs resolving**: ActionPoint must appear as a stated definition with a formal contract exporting: the function `actionPoint(w)` for `Pos(w)`, the defining equation, and the bounds `1 ≤ actionPoint(w) ≤ #w` with `w_{actionPoint(w)} ≥ 1`. Every property that currently references ActionPoint in Depends or preconditions (TA0, TumblerAdd, D0 implicitly) must be traceable to this definition.

---

### T3 claims axiom status but derives its justification from T0
**Foundation**: T3 (CanonicalRepresentation), formal contract: "Axiom: Tumbler equality is sequence equality…" — no Depends line
**ASN**: T3 proof text: "T3 is not derived from other properties; it holds by the definition of the carrier set. By T0, T is the set of all finite sequences over ℕ."
**Issue**: T3's formal contract labels it "Axiom" and includes no Depends line, asserting independence. But the proof's first substantive sentence invokes T0 to establish what T is — the justification that T3 "holds by the definition of the carrier set" is precisely the claim that T3 is a consequence of T0's characterization of T. If T3 is an axiom, it stands independently and should not reference T0; if it is a definitional consequence of T0, it needs a Depends line and should not be labeled "Axiom." The current presentation is self-inconsistent: the contract says "assumed," the proof says "derived." A formalizer cannot determine whether T3 is an independent axiom that could be changed without affecting T0, or a forced consequence of T0 that would change if T0's carrier-set definition changed.
**What needs resolving**: T3 must be classified consistently. Either (a) label it Axiom and remove the T0 reference from the justification (the proof should appeal to sequence equality directly, not through T0), or (b) label it a theorem/corollary of T0 and add a Depends line on T0, following the pattern of other derived properties.

---

### Divergence and ZPD symmetry consumed by D0 but never stated
**Foundation**: D0 (DisplacementWellDefined), proof: "zpd(b, a) = divergence(a, b) = k (ZPD, Relationship to Divergence, case (i))"
**ASN**: ZPD's Relationship to Divergence (body text): "In Divergence case (i) … `zpd(a, w) = divergence(a, w) = k`." Divergence (Definition): "`divergence(a, b)` is defined by two cases…"
**Issue**: ZPD's relationship is stated with matching argument order: `zpd(a, w) = divergence(a, w)`. D0 invokes it with reversed order: `zpd(b, a) = divergence(a, b)`. The identification requires `divergence(b, a) = divergence(a, b)` — the symmetry of the divergence function. This symmetry holds because the first-disagreement position is the same regardless of which operand is named first, but it is never stated as a property of Divergence, never exported in Divergence's formal contract, and never proved. The same applies to `zpd(b, a) = zpd(a, b)`. D0's proof silently consumes symmetry of both functions. A formalizer tracing D0's argument through formal contracts alone would find no justification for the argument-order swap.
**What needs resolving**: Either Divergence's formal contract must export symmetry (`divergence(a, b) = divergence(b, a)` for all `a ≠ b`) and ZPD's contract must export the analogous symmetry, or D0's proof must apply ZPD's relationship with the correct argument order `(b, a)` and state the symmetry step explicitly.

---

### TumblerSub derives positivity of result but does not export it
**Foundation**: TumblerSub (TumblerSub), formal contract: "Postconditions: `a ⊖ w ∈ T`, `#(a ⊖ w) = max(#a, #w)`"
**ASN**: TumblerSub precondition proof: "aₖ > wₖ at `k = zpd(a, w)`" (the "Consequence" attached to preconditions). TumblerSub construction: "`rₖ = aₖ − wₖ`" — therefore `rₖ ≥ 1` when zpd is defined. D0 proof: independently derives `Pos(b ⊖ a)` from `wₖ = bₖ − aₖ ≥ 1`.
**Issue**: When `zpd(a, w)` is defined (the operands are not zero-padded-equal), TumblerSub's own precondition consequence guarantees `aₖ − wₖ ≥ 1`, making the result component at position `k` nonzero. This means the result is positive: `Pos(a ⊖ w)`. But TumblerSub's postconditions export only membership and length — not positivity. The positivity is a direct consequence of a fact TumblerSub already proves (the "Consequence" in its preconditions section), yet it is placed as an input characterization rather than reflected as an output guarantee. D0 must re-derive `Pos(b ⊖ a)` from scratch. By contrast, TumblerAdd exports the ordering postcondition `a ⊕ w > a`, which is analogously derived from its construction. The asymmetry means a consumer of TumblerSub who knows `a > w` (hence zpd is defined) cannot conclude `Pos(a ⊖ w)` from TumblerSub's contract alone.
**What needs resolving**: TumblerSub's formal contract should export a conditional postcondition: when `zpd(a, w)` is defined, `Pos(a ⊖ w)` and `actionPoint(a ⊖ w) = zpd(a, w)`. This would parallel TumblerAdd's ordering postconditions and allow D0 (and future consumers) to cite TumblerSub directly rather than re-deriving positivity.
