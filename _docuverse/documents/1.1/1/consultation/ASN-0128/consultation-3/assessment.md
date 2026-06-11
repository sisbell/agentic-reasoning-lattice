# Channel Assignment — ASN-0128 review-3

**Date:** 2026-06-10 18:12

## Issue 1: I0's justification for coverage-sameness is falsified by this note's own enumeration predicates, and the resulting information loss is never stated
Reason: The review demands the sameness criterion be argued against the alternative, not just patched — which requires knowing whether endset identity was meant to track covered content or presented decomposition (design intent) and whether the implementation's matching machinery actually normalizes span sets to coverage or preserves decomposition (evidence). Both channels are needed.
Nelson question: When two links reference the same content through different span decompositions (one span versus that span plus a sub-span it already contains), does the design regard them as the same assertion — i.e., is computed equivalence among links meant to compare what the endsets cover, or is the particular decomposition itself meaningful content of the link?
Gregory question: When udanax-green stores and matches link endsets (e.g., in retrieval queries like FINDLINKSFROMTO), does it compare span sets by the region they cover — normalizing containment or abutment — or does it preserve and distinguish the exact span decomposition supplied at link creation?

## Issue 2: `retract_stale` has an unbound retracting document
Reason: This is a free-variable bug and a wording ambiguity; the fix (bind `d_retr` in the signature, discharge P0 with the constant-across-batch argument, reword "initial state") follows directly from the note's own P0, S3 from-fill semantics, and batch-sequencing text. No external evidence or intent is needed.

## Issue 3: Behavior labels B1–B4 collide with ASN-0126's bridge lemmas B1–B3, which this note cites throughout
Reason: This is a notation-hygiene rename the review already scopes (e.g., BH1–BH4 or the descriptive names the note uses in parallel), purely editorial and derivable from the ASN's own content. Neither design intent nor implementation evidence bears on label choice.
