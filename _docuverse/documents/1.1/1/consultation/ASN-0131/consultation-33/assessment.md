# Channel Assignment — ASN-0131 review-33

**Date:** 2026-06-13 21:33

## Issue 1: the "insert/delete are shift primitives, not K.μ~" point is stated five-plus times in one paragraph
Reason: Pure prose-consolidation. The load-bearing content (insert/delete shift content per I3/D-SHIFT, so the image swings non-monotonically) is already present and correctly cited to ASN-0082; the fix only deletes the repeated "not-K.μ~" assertions and the disclaimed-decomposition parenthetical. No design intent or implementation evidence is in question — the framing is already settled in the note.

## Issue 2: key claims restated verbatim-ish across sections
Reason: Pure deduplication. The fix states the RE-UNIT epigram and RE-IDENT once at their first load-bearing point and references them thereafter (resolving the self-falsifying "we state it once"). Both claims already live in the ASN; nothing external is needed to decide where the single statement should sit.

## Issue 3: claims-table entries duplicate prose derivations
Reason: Pure structural trim. The fix reduces the RE-RET/RE-EDIT table entries to claim-plus-conditions, leaving the b-addressability and R-Scope reasoning in the body where it already resides. This is a table-vs-prose placement decision derivable entirely from the ASN's own content.
