# Channel Assignment — ASN-0100 review-61

**Date:** 2026-06-05 02:21

## Issue 1: Per-intermediate invariant verification duplicates the post-state proofs and defers to them
Reason: Purely an expository restructuring — collapsing trivially-framed inheritances and arguing the non-trivial intermediates once. No design intent or implementation evidence is needed; the frame reasoning and invariant list are already present in the ASN.

## Issue 2: The projection-shift correspondence is narrated at full length in four places
Reason: A deduplication of the same derivation across four sections, with the §Coverage Steps 0–4 proof as the single home. All material is internal to the ASN; no theory or evidence input required.

## Issue 3: Notational-convention prose justifies consistency rather than stating the convention
Reason: Removing a defensive justification clause for a self-contained convention. Entirely internal — the convention `shift(t,0) := t` stands on its own.

## Issue 4: "Caller-chosen depth m" is presented as an operation input but is derivable from p
Reason: The signature `INSERT(d, p, …)` and `#p = m_C` precondition already establish that `m = #p`; correcting the framing is derivable from the ASN's own content without external channels.
