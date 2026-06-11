# Channel Assignment — ASN-0120 review-17

**Date:** 2026-06-11 04:27

## Issue 1: The stated endset-record postcondition does not pin coverage — ML2 is false as written
Reason: The formal repair options are given by the review, but choosing among them forecloses a behavior — coverage reaching the unallocated chain frontier would make the link discoverable from content allocated *after* creation. Whether that is a leak or an intended behavior is a design-intent question, and which admissibility (tight-at-Σ vs. extensional) matches reality is an implementation-evidence question.
Nelson question: Did Nelson intend a link's endsets to attach only to the content that existed at creation time, or was a link meant to also capture content later inserted or appended within the spanned region?
Gregory question: Do the sporgls emitted by `vspanset2sporglset` during CREATELINK always have I-widths tracing exactly the currently-allocated istream content, or can a stored sporgl's width extend past the allocation frontier into not-yet-allocated I-addresses?

## Issue 2: ML1's claims-table formula is malformed — unbound index, missing union
Reason: Purely mechanical — the body already states the correct union over `j`, and the fix is copying that binder into the claims table. No design intent or implementation evidence is involved.

## Issue 3: The span-merge induction uses TS3 without citing it
Reason: A missing citation in an otherwise sound induction; TS3 (ShiftComposition, ASN-0034) is already in the substrate the ASN cites, and the review specifies exactly where the clause goes. Derivable from the ASN's own content.
