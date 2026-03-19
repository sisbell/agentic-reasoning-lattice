# Revision Categorization — ASN-0029 review-6

**Date:** 2026-03-11 12:14

## Issue 1: D7 — `home(a) ∈ Σ.D` not established
Category: GREGORY
Reason: The missing link is whether INSERT on document `d` allocates I-addresses under `d`'s tumbler prefix. This is an I-space allocation discipline question answerable from the udanax-green implementation.
Gregory question: When INSERT allocates fresh I-addresses for document `d`, are those addresses always allocated under `d`'s tumbler prefix (i.e., `d ≼ fresh`), or can they fall elsewhere in the I-space?

## Issue 2: Privashed state — prose claims unsupported by formal model
Category: INTERNAL
Reason: The inconsistency is between the ASN's own prose and its formal model — no operation transitions out of `privashed`, yet the prose claims it can revert. The fix is to align the prose with the model's current state, which requires no external evidence.

## Issue 3: ASN-0026 frame extension for Σ.pub is unnamed
Category: INTERNAL
Reason: This is a labeling issue — a load-bearing property embedded in prose needs a name. The content and justification are already present in the ASN; it just needs to be elevated to a named property.
