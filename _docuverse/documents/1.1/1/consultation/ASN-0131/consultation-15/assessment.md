# Channel Assignment — ASN-0131 review-15

**Date:** 2026-06-13 15:09

## Issue 1: RE-RET's core stability result is overclaimed as unconditional — the type-slot re-witnessing case breaks it
Reason: Internal. The reviewer's counterexample is built entirely from facts the ASN already states or cites — RE-DEF ranges `i` over all slots, ASN-0086's R6b/R6c admit retraction-of-retraction, `Emit_R` always deposits `Θ` in slot 3, and the note itself grants a `Θ` can meet content. Both prescribed remedies (attach the `coverage(Θ) ∩ dom(Σ.C) = ∅` hypothesis to the core result, or scope the "sole bearer ⟹ drops" claim to slots `i ∈ {1,2}` and route `(3, Θ)` to Open Question 6) are logical corrections derivable from the ASN's own definitions; the deeper semantic question is explicitly deferred to OQ6, not resolved by the fix.

## Issue 2: RE-WHOLE's provisionality is deferred to Open Question 1 in three separate places
Reason: Internal. Pure prose-dedup — state the provisional status once at RE-WHOLE's definition, let the table tag carry it, and drop the worked-instance re-announcement; no design intent or implementation evidence bears on which sentences to cut.

## Issue 3: The Stability "full taxonomy" paragraph accretes forward-reference navigation and vocabulary asides
Reason: Internal. Editorial trim — remove the inline forward pointers to RE-CWP/RE-RET (the immediately following subsections) and the extension-splits-into-two vs. contraction-is-one vocabulary aside, leaving the transition classification itself; the classification content is unchanged and derivable from the ASN.

## Issue 4: The s_C-restriction justification enumerates its downstream consumers
Reason: Internal. Editorial trim — the substantive reason (`W ⊆ s_C` puts the image in `dom(Σ.C)` by S3★) is already in the prior sentence; deleting the use-site inventory of later passages requires nothing beyond the ASN's own text.
