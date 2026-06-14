# Channel Assignment — ASN-0131 review-72

**Date:** 2026-06-14 11:39

## Issue 1: Redundant second justification + forward reference for link-only K.μ⁻ stability
Reason: Internal. The paragraph's direct argument (retained-position agreement ⟹ `image(W, d, Σ') = image(W, d, Σ)`) is already complete and present in the note, and RE-CWP is the note's own later result; deleting the redundant `Δ = ∅` sentence or relocating the cross-link is a mechanical editorial edit requiring no design intent or implementation evidence.

## Issue 2: Editorial defense of a result's status in RE-UDIST-∩
Reason: Internal. The necessary-and-sufficient characterization is already fully earned by the preceding paragraphs (⊆ unconditional, ⊇ refuted under both non-injective and injective arrangements); excising the defensive "settled, not for want of a sharper condition…" clause removes meta-prose without touching any claim, so no channel is needed.

## Issue 3: Notation reconciliation produces a mismatch it claims to resolve
Reason: Internal. The relationship among `L_R`, `Emit_R`, `Emit_Θ`, and the retraction type `Θ` is fully laid out in the note itself, so standardizing the subscript one way and dropping the gloss is a mechanical notation choice — a matter of this note's internal consistency, not of design intent or implementation behavior.

## Issue 4: Shift-based insert/delete paragraph — assumption-justification and non-monotonicity exposition around a one-line conclusion
Reason: Internal. The trim retains material already established in the note (the M-only principle, the named conservative-lift modelling assumption, the delete-`#p=2`/insert-`#p≥2` depth scoping) and cuts rationale and non-monotonicity exposition that merely restate RE-EDIT's already-stated global non-monotonicity; reducing these to a clause requires no design intent or implementation evidence.
