# Channel Assignment — ASN-0132 review-14

**Date:** 2026-06-13 10:23

## Issue 1: CN-ENUM elaborates a one-line identity three times over
Reason: Pure deletion of rhetorical restatement — the substantive proof (first sentence) and the "at one state" qualifier are already in the ASN and are what remains. No design intent or implementation evidence is needed to identify the three sentences as redundant.

## Issue 2: The "Σ.M is not read" justification is repeated near-verbatim across sections
Reason: The fix consolidates a repeated justification into a back-reference to CN-LOC, which is already stated and proved within the ASN; identifying the duplicate clauses and replacing them with "by CN-LOC" is a purely internal editorial operation.

## Issue 3: The "That same realisation" implementation-note refrain restates two claims at code level
Reason: The fix trims the CN-ENUM and CN-SNAP notes down to their already-stated implementation facts (shared routine; recompute-not-cache) and deletes the sentences that restate CN-ENUM/CN-SNAP; the kept facts are retained verbatim and the dropped ones are identifiable as restatement from the ASN itself, so no new implementation evidence is required.
