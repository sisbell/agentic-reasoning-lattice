# Channel Assignment — ASN-0116 review-47

**Date:** 2026-06-09 16:31

## Issue 1: IP4's "incomparable" claim is false
Reason: Neither channel is needed — this is a set-theoretic error fully internal to the formal reasoning. The corrected relationship follows from the ASN's own I-SHIFT/I-NEW clauses and the already-cited L4/L9 ghost-reference permission (a vacated slot `v` can be re-populated with new content also in `coverage(e)`); the review supplies both the counterexample and the corrected statement, so no design intent or implementation evidence is at stake.

## Issue 2: PROV mischaracterizes provenance timing as "atomic with allocation"
Reason: Internal consistency fix — the contradiction is between PROV's prose and the valid-composite section's own K-atomic sequence (`K.ρ` sequenced strictly after every `K.α`), both already in the ASN. Aligning the wording to the model the note itself builds needs no external input; the implementation's DOCISPAN detail does not change the abstract composite's step ordering.

## Issue 3: Methodology meta-prose around the citation style
Reason: Pure anti-bloat deletion of defensive citation-methodology asides; the per-clause status tags already record derivation provenance. No claim content changes and nothing external is consulted.
