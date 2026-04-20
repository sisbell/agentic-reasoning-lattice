# Cone Review — ASN-0034/OrdinalShift (cycle 1)

*2026-04-13 22:18*

### Undefined properties T1, T3 used in proofs without definition or dependency declaration

**Foundation**: N/A — this is a foundation ASN
**ASN**: PositiveTumbler proof: "By T1 case (i) with witness k, z < t" and "by T1 case (ii) with witness #z + 1, z < t"; zero tumbler section: "Under T3, the tumblers [0], [0, 0], [0, 0, 0], etc., are distinct elements of T"
**Issue**: The PositiveTumbler proof rests on two case-dispatch rules of T1 (the ordering), and the zero-tumbler discussion invokes T3 — but neither T1 nor T3 appears in this document. The ASN declares no dependencies. Every proof step in a foundation ASN must trace to something defined within that ASN. As written, the PositiveTumbler result — which is load-bearing for TA0 and OrdinalShift — has an ungrounded proof chain.
**What needs resolving**: Either T1 and T3 must be defined within this ASN (with their case structure explicit enough to verify the two applications in the PositiveTumbler proof), or they must be declared as external dependencies with their exported statements listed.

---

### TA4 referenced but absent

**Foundation**: N/A
**ASN**: PositiveTumbler section: "The condition w > 0 in TA0 and TA4 excludes all all-zero displacements regardless of length"
**Issue**: TA4 is cited as sharing PositiveTumbler's w > 0 precondition, but TA4 is not defined anywhere in this document. This is a dangling forward reference. A reviewer or formalizer cannot verify that PositiveTumbler's result actually satisfies what TA4 needs, because TA4's statement is unknown.
**What needs resolving**: Either TA4 must appear in this ASN (making the forward reference a presentation-order issue to fix), or the reference to TA4 must be removed from PositiveTumbler's scope and placed wherever TA4 is defined.

---

### TA0 and TumblerAdd duplicate the same construction; definitional status unclear

**Foundation**: N/A
**ASN**: TA0 proof: "The constructive definition (TumblerAdd) builds r = a ⊕ w = [r₁, ..., rₙ] by three rules: rᵢ = aᵢ for 1 ≤ i < k (copy from start), rₖ = aₖ + wₖ (single-component advance), and rᵢ = wᵢ for k < i ≤ n (copy from displacement)." Then TumblerAdd restates the identical three-rule piecewise definition.
**Issue**: TA0 is labeled an "axiomatic property" yet its proof gives the full construction. TumblerAdd is labeled the "constructive definition" yet it appears after the construction has already been stated and used. The section introducing TumblerAdd says "the axiomatic properties above state what ⊕ and ⊖ must satisfy; we now give a constructive definition" — framing TumblerAdd as implementation and TA0 as specification. But TA0's proof *is* the implementation. For TLA+ formalization, ⊕ needs exactly one definition; TA0 is then either an axiom (no proof, the definition is the axiom) or a theorem (proved from TumblerAdd as the definition). The current structure is neither.
**What needs resolving**: Establish which is the definition of ⊕ and which is the derived property. If TumblerAdd is the definition, TA0 should cite it rather than re-derive the construction. If TA0 is axiomatic, TumblerAdd is redundant and its formal contract should merge with TA0's.

---

### Section heading promises ⊖ but only ⊕ is defined

**Foundation**: N/A
**ASN**: Section heading: "Constructive definition of ⊕ and ⊖"
**Issue**: The section defines TumblerAdd (⊕) but contains no definition or construction for ⊖. Combined with the TA4 reference in PositiveTumbler, this suggests ⊖ and its properties were intended to appear here but are missing. Any downstream property that depends on ⊖ (the displacement-recovery operation mentioned in the introduction: "recover the displacement between two positions") has no foundation to cite.
**What needs resolving**: Either the ⊖ construction must be provided (with its own well-definedness property analogous to TA0), or the section heading must be corrected and ⊖'s location documented.

---

### Definition order inverts the dependency chain

**Foundation**: T0 (CarrierSetDefinition)
**ASN**: TA0 proof: "Since w ∈ T requires n ≥ 1" (uses T0); TumblerAdd body: "a ⊕ w ∈ T by T0" (uses T0); TumblerAdd body: "By PositiveTumbler, the precondition w > 0 means..." (uses PositiveTumbler). Both appear before T0 and PositiveTumbler are stated.
**Issue**: TA0 and TumblerAdd are stated and proved using T0 and PositiveTumbler, which appear later in the document. While mathematical texts sometimes use forward references, TLA+ modules require definitions before use — a spec cannot reference an ASSUME or operator not yet declared. The current ordering means the logical dependency chain reads bottom-up: OrdinalShift → TA0/TumblerAdd → T0/PositiveTumbler, but the document presents it top-down. This is not merely cosmetic; a formalizer following the document order will hit undefined references.
**What needs resolving**: The presentation order must be reconciled with the dependency order so that every property is stated after the properties it references. The natural order is: T0 → T1 → PositiveTumbler → TumblerAdd → TA0 → OrdinalDisplacement → OrdinalShift.
