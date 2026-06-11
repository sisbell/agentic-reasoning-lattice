# Channel Assignment — ASN-0111 review-38

**Date:** 2026-06-10 22:45

## Issue 1: Endsets called "span-sets" — a foundation term with different semantics
Reason: This is a terminology correction fully resolvable from the ASN and its cited foundations — the review itself supplies the correct term ("endsets", ASN-0043) and the replacement phrasing; no design intent or implementation evidence bears on which defined term names the carrier of `coverage`.

## Issue 2: "No address-computable predicate is sufficient" is false without the satisfiability qualifier
Reason: The fix is internal — the body proof already establishes exactly the qualified claim ("any *satisfiable* address-only predicate..."), and the revision is propagating that qualifier to the headline, the derivation sentence, and the claims-table entry. No external channel is needed to insert a qualifier the ASN's own proof already carries.
