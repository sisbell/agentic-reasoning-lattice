# Cone Review — ASN-0034/D1 (cycle 1)

*2026-04-16 22:45*

### Stale forward reference to Tumbler subtraction
**Foundation**: N/A — internal document ordering
**ASN**: "## Tumbler arithmetic" introductory prose: *"tumbler addition (⊕, constructed in TumblerAdd) and subtraction (⊖, constructed in TumblerSub — forward reference, § Tumbler subtraction below)"*
**Issue**: The "§ Tumbler subtraction below" description is inverted. In the document as presented, the `## Tumbler subtraction` section (defining TumblerSub) and TA0 both appear *above* `## Tumbler arithmetic`, not below it. The "forward reference" phrasing is stale with respect to the current section order, which presents subtraction before addition's arithmetic section. A reader following the cue will look downward for the TumblerSub definition and not find it there.
**What needs resolving**: Either relabel TumblerSub as already-defined and adjust the prose (since TumblerSub and TA0 both precede this section), or reorder the sections so the forward-reference phrasing matches actual document flow. Whichever fix is chosen, the direction of the reference should be made consistent with the physical ordering.

---

### Unresolved reference to "D0" in TumblerSub prose
**Foundation**: N/A — internal property cross-reference
**ASN**: `## Tumbler subtraction` intro prose: *"D0 takes the first as a precondition and proves the necessity of the second via its negative postcondition (`#a > #b → a ⊕ (b ⊖ a) ≠ b`); the positive round-trip identity under the full conjunction is established by D1."*
**Issue**: "D0" is named as the property that carries the negative postcondition about `#a > #b` and motivates splitting the roundtrip necessity across two properties. The ASN content shown contains D1 but no D0 property; D0 is not listed in TumblerSub's *Depends*, not defined alongside D1, and not present among the sister properties called out elsewhere (TA-Pos, ActionPoint, TA1 are named explicitly; D0 is not). If D0 is intended as a sister property, it is absent from this ASN; if it was superseded or renamed, the prose reference is stale.
**What needs resolving**: Confirm whether D0 exists as a property of this ASN. If it does, make it explicit (as TA-Pos and ActionPoint are made explicit as sister properties). If it does not, rewrite the prose so the motivation for the two preconditions of D1 does not depend on citing a nonexistent property.

---

### TumblerSub precondition consequence: scope of the "vacuous" clause
**Foundation**: N/A — internal precondition chain
**ASN**: TumblerSub precondition block: *"Preconditions: a ∈ T, w ∈ T, a ≥ w (T1). Consequence: when zpd(a, w) is defined, aₖ > wₖ at k = zpd(a, w)."* and, in the proof, *"When zpd is undefined, no subtraction at the divergence point occurs — the constructive definition produces the zero tumbler — and the precondition holds vacuously."*
**Issue**: The closing sentence of the precondition-consequence proof says "the precondition holds vacuously," but the *precondition* (`a ≥ w`) is not vacuous — it is an unconditional hypothesis that must hold independently of whether zpd is defined. The sentence likely means that the *consequence* (`aₖ > wₖ`) is vacuously true when zpd is undefined (there is no `k` to evaluate). As stated, the prose conflates precondition with consequence at exactly the point where the reader is being shown that the formal contract is watertight. A precise reader (which the review asks us to be) will notice the loose use of "precondition" and lose confidence that the case split has been argued correctly.
**What needs resolving**: Rewrite the zpd-undefined branch so that it distinguishes the precondition `a ≥ w` (which still holds, by hypothesis) from the consequence `aₖ > wₖ` (which is vacuous because `k = zpd(a, w)` does not exist). The argument is sound; only the phrasing misattributes vacuity.
