# Channel Assignment — ASN-0118 review-28

**Date:** 2026-06-10 19:18

## Issue 1: K.μ⁺'s image-membership conjunct is asserted "uniformly discharged" but never shown for the displaced trailing bindings
Reason: The finding itself supplies the complete discharge chain (S3★ at `Σ` places the trailing images in `dom(Σ.C)`, K.μ⁻'s content frame carries this to `Σ₁`), and every cited fact is already in the ASN's substrate section. The fix is purely a matter of writing out an instantiation that was elided; no design intent or implementation evidence is involved.

## Issue 2: the closure-bounding rationale is stated three times in three sections
Reason: This is a prose-deduplication edit — keep the clauses, state the rationale once at CP3c, delete the echoes at CP6 and CP12. The content of all four clauses is unchanged, so nothing needs external grounding.

## Issue 3: the redundant-K.ρ/J1'★-indifference argument is duplicated verbatim in the worked example
Reason: The fix replaces a restated general argument with a concrete instantiation (`x₁ ∈ ran(Σ.M(d))|_{s_C}`, P4★, P2), all of which already appears in the composite section and the example's own setup. Internal rewrite only.

## Issue 4: the partial-binding decision is stated twice in adjacent paragraphs
Reason: The fix is to delete the anticipatory clause from the spec-set paragraph and let the `act` paragraph carry the occupancy decision, which is already properly grounded there with its Nelson quote. No new semantic content is introduced, so no channel is needed.
