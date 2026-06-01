# Channel Assignment — ASN-0086 review-163

**Date:** 2026-06-01 06:03

## Issue 1: "P1 does not gate emission" is announced, then re-shown, inside the same definition
Reason: This is an internal prose-deduplication task — removing a forward-deferring announcement that restates the composition paragraph's proven conclusion. The semantics (P0 gates emission, P1 gates only the postcondition) are already fully derived within the ASN, so no design-intent or implementation evidence is needed.

## Issue 2: wp section intro mislabels Case 1 as a weakest-precondition use
Reason: This is an internal consistency fix — the intro's "both cases compute the weakest predicate" framing contradicts Case 1's own self-description ("a *sufficient* precondition … not the weakest"). The correct wording is fully determined by the section's existing content, requiring no external channel.
