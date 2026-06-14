# Review of ASN-0131

This is a careful, largely sound note. The defining biconditional (RE-DEF), the locality/soundness/completeness reads, the union law, the discovery-side placement (RE-SEL), the contraction weakest-precondition (RE-CWP), and the retraction iff (RE-RET) all check out against the foundation, and the worked instance correctly exercises RE-OVL/CLIP/WHOLE/UNIT (I verified `a₂ ⊕ δ(2,#a₂) = shift(a₂,2) = a₄`, the `e₂`/`e₃` misses, and the `s_type ≠ s_C` field-agreement argument). Two issues remain.

## REVISE

### Issue 1: The RE-UDIST-∩ counterexample omits two of its required witnesses

**ASN-0131, "Composing regions"**: "take a position `v₁ ∈ W₁ ∖ W₂` and a position `v₂ ∈ W₂ ∖ W₁` sharing one I-address `Σ.M(d)(v₁) = Σ.M(d)(v₂) = a` … and an endset `e` covering `a`. Then `e` meets `image(W₁, d, Σ)` (through `v₁`) and `image(W₂, d, Σ)` (through `v₂`), so `(i, e) ∈ RE(W₁, d, Σ) ∩ RE(W₂, d, Σ)`; yet `a ∉ image(W₁ ∩ W₂, d, Σ)` and `e` meets that image nowhere, so `(i, e) ∉ RE(W₁ ∩ W₂, d, Σ)`."

**Problem**: This is the freshly-revised content settling `⊇` negatively, and as written it does not exhibit a member of the right-hand side. Two witnesses are skipped:

1. **No bearing link.** By RE-DEF, `(i, e) ∈ RE(W₁, d, Σ)` requires `∃ a' ∈ addressable(Σ) : Σ.L(a').eᵢ = e`. The construction floats "an endset `e` covering `a`" without placing `e` in any addressable link's slot `i`. "`e` meets `image(W₁)`" establishes only `touch_{W₁}(e)`, not membership in `Avail(Σ)`; the step "so `(i, e) ∈ RE(W₁, d, Σ)`" is therefore unjustified.

2. **`a ∉ image(W₁∩W₂)` does not give "`e` meets that image nowhere."** Non-membership in the LHS needs `coverage(e) ∩ image(W₁ ∩ W₂, d, Σ) = ∅`. The construction guarantees only that the *single* address `a` is absent from `image(W₁∩W₂)`. If `e` covers any other address that `W₁∩W₂` happens to map to, then `(i,e) ∈ RE(W₁∩W₂)` and the refutation collapses. The note asserts the stronger condition ("meets that image nowhere") rather than securing it.

**Required**: Construct the counterexample completely: (a) posit an addressable link `ℓ_e` with `Σ.L(ℓ_e).eᵢ = e` (constructible by a K.λ emission, e.g. the unit endset `e = {(a, δ(1,#a))}`), and (b) pin the arrangement so that `coverage(e) ∩ image(W₁ ∩ W₂, d, Σ) = ∅`, not merely `a ∉ image(W₁∩W₂)`.

### Issue 2: RE-EDIT's shift-insert/delete coverage rests on an undischarged, foreign assumption — flagged in prose but not in the claim's status, and surrounded by meta-prose

**ASN-0131, "Stability" / Claims table RE-EDIT**: "We make that choice explicit and adopt it as an **assumption of this note**: the *natural lift* of ASN-0082's `(C, M)` insert/delete to the full `(C, L, E, M, R)` state writes only `Σ.M(d)` and frames the rest, `L' = L ∧ E' = E ∧ R' = R`." The table then states RE-EDIT "Over ASN-0047's atomic movers **and ASN-0082's shift-based insert/delete**, only the content-subspace movers on `d` … can move the answer."

**Problem**: Three distinct concerns at one site.

- *Vocabulary mismatch.* Shift-based mid-document insert/delete is **not** in this ASN's transition model (ASN-0047's K.μ⁺ appends only at the contiguous frontier; K.μ⁻ truncates the tail; K.μ~ reorders — none shifts). The note must reach into ASN-0082 to cover it.
- *Undischarged assumption doing headline work.* The bridge requires "M-only ⟹ frames `L`, `E`, `R`," which neither foundation establishes: ASN-0082 has no `L/E/R` to frame, and ASN-0047 has no shift transition. The note correctly labels it an assumption — but RE-EDIT is then listed as "introduced" (established), with no marker that part of its range is assumption-conditional. Contrast RE-WHOLE, which the same table honestly marks "provisional." The flagging is uneven: an equally-conditional claim is presented as settled.
- *Bloat.* The justification is heavy meta-commentary — "This is a cross-model lift, and its status must be labelled honestly," "those stores are absent from its model, so there is no write-set over the full state for them to 'lie outside' of — but a property of how the lift is performed" — essay about *why* the assumption is admissible rather than the assumption and its use. This is precisely the accretion the anti-bloat classifier targets.

**Required**: Pick one and align the prose: (a) excise the shift cases from RE-EDIT and defer them to an ASN that unifies ASN-0082's displacement with the full state (see OUT_OF_SCOPE below); or (b) keep them but mark RE-EDIT's shift coverage **conditional on the stated assumption** in the Claims table, as RE-WHOLE is marked. Either way, reduce the cross-model justification to the assumption statement plus its use; drop the "labelled honestly" / "property of how the lift is performed" commentary.

## OUT_OF_SCOPE

### Topic 1: Stability under shift-based mid-document insert/delete over the full `(C,L,E,M,R)` state

**Why out of scope**: ASN-0082 establishes I3/D-SHIFT only over a `(C,M)` state; the full-state lift's frame on `Σ.L`, `Σ.E`, `Σ.R` is not a theorem of any foundation here. The natural home is an ASN that lifts ASN-0082's displacement primitives into ASN-0047's transition vocabulary; once that exists, RE-EDIT's shift cases follow without a note-local assumption. (If retained, see Issue 2(b).) The remaining Open Questions (whole-vs-touching surfacing, multiplicity, V-rendered answers, intersection-equality-under-injectivity, non-co-resident link stores, type-slot/content matches, link-subspace regions) are all appropriately future territory, not gaps in this note.

VERDICT: REVISE
