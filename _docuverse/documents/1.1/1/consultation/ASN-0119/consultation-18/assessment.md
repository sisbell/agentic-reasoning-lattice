# Channel Assignment — ASN-0119 review-18

**Date:** 2026-06-09 18:28

## Issue 1: Open question rests on a premise the model excludes
Reason: Internal. The note's own Document Isolation section and P9 already establish that transclusion shares I-addresses, not V-positions ("each document is its own V→I mapping over the common, immutable content") — which is precisely the model fact that makes the question's premise incoherent. Reframing the question around a shared I-address (a content boundary that is a cut in one arrangement but interior to another) follows directly from material already present; no design intent or implementation evidence is required.

## Issue 2: Introduced claim labels P0–P9 collide systematically with ASN-0047's P-scheme
Reason: Internal. Mechanical relabeling to a distinctive prefix (e.g. `RA-*`) plus a table-ordering fix; the colliding ASN-0047 labels are already enumerated in the review. No semantic question for either channel.

## Issue 3: REARRANGE's status in ASN-0047's *transition* model is left unresolved, and the atomicity claim depends on it
Reason: Internal. This is a formal reconciliation across foundations the note already imports — ASN-0084's atomic REARRANGE_K and ASN-0047's K.μ~ with its J0/J1★/J1'★ obligations. The design intent that REARRANGE is a single atomic motion is already settled in the note from Nelson's "two cuts at once" (4/67) and the imported ASN-0084 definition, and the reviewer has supplied the positive K.μ~ characterization to verify against ASN-0047. Neither fresh design intent nor implementation evidence is needed.

## Issue 4: Minor meta-prose (anti-bloat)
Reason: Internal. Prose trimming — drop the citation-choice justification and the hardest/easiest editorializing while keeping the substantive clause (key set unchanged ⟹ key-only invariants inherited), which the surrounding prose already carries.
