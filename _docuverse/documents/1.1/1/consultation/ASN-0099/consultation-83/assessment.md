# Channel Assignment — ASN-0099 review-83

**Date:** 2026-06-04 15:32

## Issue 1: Retired-labels paragraph is pure numbering meta-prose
Reason: Pure deletion of document-bookkeeping prose; no design intent or implementation evidence is involved. Derivable from the ASN alone.

## Issue 2: Use-site back-pointers in the match-predicate prose
Reason: Mechanical removal of location pointers, retaining the already-stated relation to `discoverable_from`. No external channel needed.

## Issue 3: "Primary obligation" framing is protocol rationale
Reason: Drops editorializing while keeping the factoring equation and its premise chain already present in the ASN. Internal.

## Issue 4: F10 finiteness cites the implementation result where the definition suffices
Reason: The substitution (use `findlinks ⊆ dom(Σ.L)` by definition instead of routing through F3) follows directly from the comprehension's own definition. Internal.
