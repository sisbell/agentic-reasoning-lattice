# Channel Assignment — ASN-0071 review-18

**Date:** 2026-06-02 23:28

## Issue 1: Depth-mismatch over-collection is admitted but never analyzed
Reason: The choice between (a) reinstating a depth constraint and (b) declaring "prefix names subtree" benign is a semantic decision about what content-transclusion discovery is meant to do at coarse granularity — Nelson speaks to that intent; Gregory can say whether the implementation resolves coarse spans to whole subtrees or requires granularity match.
Nelson question: When a user names content at a coarser granularity than the source document's leaves (a depth-2 anchor over depth-3 content), is the transclusion query intended to discover everything in the named subtree, or must the query match the content's native granularity?
Gregory question: When FINDDOCSCONTAINING (or its content-resolution path) receives a span whose depth is shallower than the source arrangement's positions, does udanax-green resolve it to the entire subtree under that prefix, reject it, or normalize it to the native granularity?

## Issue 2: Subset claim `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` asserted "for every Q and Σ" without the well-definedness gate
Reason: Internal — the `wp-defined` precondition is already defined in the ASN for `find`; the fix is to gate the F-iaddrs subset claim and its prose on that same precondition, derivable entirely from the ASN's own content (M1, the existing precondition).

## Issue 3: Worked scenario does not delineate composite boundaries
Reason: Internal — grouping the steps into allocate–place–record composites and checking J0/J1★/J1'★ uses ValidCompositeAmended and the coupling constraints already imported from ASN-0047; no design intent or implementation evidence is required, only restructuring against the cited foundation.
