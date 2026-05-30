# Channel Assignment — ASN-0084 review-54

**Date:** 2026-05-30 12:47

## Issue 1: Post-state S8 derivation stated four times
Reason: Pure deduplication of an internal claim; the ASN already establishes that foundation S8 supplies the maximal partition once dom, S2, S3 are preserved. No design intent or implementation evidence required.

## Issue 2: Identical sentence duplicated across R-PPERM and R-SPERM
Reason: Removing a redundant explanatory sentence whose content is already shown by the piecewise formulas' non-S row and cited via R-NS(NS-π). Entirely internal.

## Issue 3: Same future-ASN deferral repeated in multiple sections
Reason: Editorial consolidation of a repeated deferral statement into one location (Open Questions); derivable from the ASN's own structure.

## Issue 4: w_μ ≥ 1 attributed to CS2, contradicting the ASN's own derivation
Reason: The Width-positivity consequence already derives w_μ ≥ 1 from R-PRE(iv) plus CS2–CS4; the fix is to align the parenthetical with that internal derivation.

## Issue 5: R-NS (NS-inv) is a downstream-consumer inventory
Reason: Reducing a catalogue that duplicates R-SP's per-clause audit to (NS-inv)'s actual content; the trimmed statement is self-contained within the ASN.

## Issue 6: REARRANGE_K *Partiality* paragraph is defensive non-content
Reason: Deleting defensive meta-prose; the retained sentence ("partial, defined exactly where R-PRE(K) holds") fully captures the content. Internal.

## Issue 7: "S7 ≡ S7a ∧ S7b ∧ S7d" mischaracterizes a theorem
Reason: The correct characterization — S7 is a theorem about origin(a) derived from S7a/S7b/S7d plus T4, preserved because origin depends only on Σ.C and C' = C — is already supplied by the review and consistent with the ASN's C-transport reasoning; the fix is a wording correction.
