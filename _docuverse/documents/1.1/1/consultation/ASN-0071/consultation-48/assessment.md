# Channel Assignment — ASN-0071 review-48

**Date:** 2026-06-03 09:54

## Issue 1: "Prefix names subtree" is asserted as a specification guarantee but never stated as a claim, and the blanket form is false for width > 1
Reason: Internal. The precise cross-depth capture set is computable from ASN-0053's `⟦σ⟧` denotation and TumblerAdd's prefix-copy (both already used in the note); whether to add a derived claim or downgrade the prose is an editorial/derivational decision needing no external channel.

## Issue 2: The same Nelson "any portion" quote is made "the operative reading" of two distinct phenomena
Reason: Nelson is needed because the fix turns on what Nelson's "any portion ... regardless of where native copies are located" was *intended* to govern — result-document fragments (transclusion discovery) versus query-span subtree denotation. The math of the cross-depth justification is internal, but correctly attributing the quote requires the designer's intent.
Nelson question: Does "retrieve any portion of the material specified ... regardless of where the native copies are located" (LM 4/63) describe the *result* (each returned document may contain only a fragment of the queried material) or the *query reach* (naming a coarse coordinate pulls in its whole subtree)?

## Issue 3: Completeness/soundness/distinctness are definitional restatements presented as results
Reason: Internal. These are the two halves of `find`'s defining biconditional and the set codomain; folding them back into F-find and trimming the ceremony is a pure editorial change derivable from the ASN's own definitions.

## Issue 4: F-LOC is an orphan claim
Reason: Internal. Whether F-LOC is load-bearing for F-CUR or unused accretion is settled by reading the note's own derivations; no external evidence or intent is required.
