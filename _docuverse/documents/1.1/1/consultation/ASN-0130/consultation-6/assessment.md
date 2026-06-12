# Channel Assignment — ASN-0130 review-6

**Date:** 2026-06-12 10:30

## Issue 1: Free-variable set of a referent overclaimed as "exactly" its parameters
Reason: The fix is internal — PR-SIG's own statement ("free variables are among its parameters") supplies the correct inclusion, and the review already traces that every downstream proof step (WT-α totality, Weaken provisos, Substitute non-interference) consumes only the inclusion. No design-intent or implementation question bears on a set-equality-vs-inclusion wording fix in the note's own lemma chain.
