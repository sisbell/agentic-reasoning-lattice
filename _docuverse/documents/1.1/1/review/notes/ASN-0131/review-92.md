# Review of ASN-0131

## REVISE

### Issue 1: "Three further transition kinds" claims three, elaborates one

**ASN-0131, §"Stability…", paragraph beginning "Editing of *other* documents…"**: "Three further transition kinds leave the answer fixed for the same root reason — each leaves the queried fiber `Σ.M(d)` and the link store `Σ.L` fixed (LP8 supplying the K.δ document-registration case). Entity creation `K.δ` — registering a new node, account, or document `e ≠ d` — leaves `Σ.M(d)` untouched … and leaves `Σ.L` fixed (frame)…"

**Problem**: The sentence promises three transition kinds and then discharges exactly one (K.δ). The intended three are presumably K.α, K.δ, K.ρ — but K.α and K.ρ are never named here, and their frame behavior on `Σ.M(d)` is never stated, only collapsed into "the same root reason." This is precisely the "no proof by similarly" gap: the three kinds differ in frame structure (K.δ's document-registration case is non-trivial and needs LP8; K.α and K.ρ have trivial `M' = M` / `M'(d) = M(d)` frames), and the note shows the hard one while leaving the other two for the reader to reconstruct. RE-EDIT's summary claim "left fixed by every other transition" rests on this paragraph, so the gap propagates upward: as written, RE-EDIT is unsupported for K.α and K.ρ. (If instead "three transition kinds" was meant as K.δ's three sub-cases, then K.α and K.ρ are not covered at all in the stability analysis, which is a worse gap.)

**Required**: Name K.α and K.ρ explicitly and discharge each: K.α frames `M' = M ∧ L' = L` (ASN-0093/ASN-0047), so both the image and `Avail(Σ)` are fixed; K.ρ frames `M'(d) = M(d) ∧ L' = L` (ASN-0047) — or cite LP14 (ASN-0098) directly for K.ρ projection-invariance. Either spell out all three or rewrite the count to match what is actually shown.

### Issue 2: Worked-example mischaracterizes a unit-depth span's coverage

**ASN-0131, §"A worked instance," RE-CLIP bullet**: "A clipping implementation would have returned the width-1 span `(a₂, δ(1, #a₂))` covering `a₂` alone, falsely shrinking the link's grip to fit the query."

**Problem**: By PrefixSpanCoverage (ASN-0043) — which the note invokes throughout this very example — `coverage({(a₂, δ(1, #a₂))}) = {t : a₂ ≼ t}`, i.e., `a₂` *and its descendants*, not `a₂` alone. Two paragraphs earlier the note describes the structurally identical span `(a₄, δ(1, #a₄))` as "reaching only `a₄` and its descendants." So the mandated concrete verification gives two contradictory readings of identical span shapes. (The half-open interval `[a₂, a₃)` contains no exact-singleton characterization at all; no span covers exactly `{a₂}`.)

**Required**: State what the unit-depth span actually covers — `a₂` and its descendants, or "only `a₂` among the four arranged pieces" if that is the intended contrast — to match the note's own coverage semantics. Minor, but it sits in the example the rigor of the note rests on.

## OUT_OF_SCOPE

The note correctly defers its forward-looking territory to Open Questions rather than over-reaching: the touching-spans vs. whole-endset return value (OQ1), rendered/V-position answers (OQ3), a structural sufficient condition for intersection-equality (OQ4), multiplicity preservation (OQ2), cross-store completeness (OQ5), type-slot-against-content semantics (OQ6), and link-subspace regions (OQ7). These belong in future notes and are not gaps in this one. The existence/discovery taxonomy and the content-region image machinery are cited (RE-SEL, image, `findlinks_V`) rather than rebuilt, consistent with the stated scope.

VERDICT: REVISE
