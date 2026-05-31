# Channel Assignment — ASN-0086 review-85

**Date:** 2026-05-31 15:38

## Issue 1: Observe_K justifies match-decidability by a false finiteness claim
Reason: The corrected justification (F̂ finite + per-element decidability of `t ∈ coverage(F)` via T2 intrinsic comparison) is fully specified in the review and rests on lemmas the note already cites (T2, T12, PrefixSpanCoverage); no design intent or implementation evidence is required.

## Issue 2: Duplicated "catalog (a) alone is insufficient" with a deferral forward-reference
Reason: Pure prose-structure fix — remove the parenthetical rationale/forward pointer from the `↝` paragraph and leave the insufficiency argument at its single home in R7a; nothing about design intent or implementation is in question.

## Issue 3: substrate-conforming-layer Definition embeds use-site inventory and granularity rationale
Reason: Editorial restructuring — reduce clause (a) to the catalog contents and relocate the discharge-granularity observation into R7a; the catalog contents and discharge argument already exist in the note, so the fix is internal.

## Issue 4: "Unit-depth retraction discipline" Definition enumerates its downstream consumer
Reason: Pure deletion — remove the "Consumption" sub-paragraph (the relational-layer Definition already records the commitment) while retaining the "Scope" clause; no external channel needed.
