# Channel Assignment — ASN-0047 review-175

**Date:** 2026-05-31 21:51

## Issue 1: K.σ subsumption enumerates only two routes into E_doc, omitting the k = 0 sibling-document route
Reason: Internal consistency fix — the ASN's own S7d verification already enumerates all three routes (k=2, k=1, k=0) and the entity-hierarchy worked example Step 4 demonstrates the k=0 sibling-document registration. The correction is purely a matter of aligning the subsumption paragraph with content already present in the ASN.

## Issue 2: K.δ "Effect on M" and frame contradict the total-M typing override — M is unchanged for IsDocument(e)
Reason: Internal fix derivable from the ASN's own total-M typing note (`M(d) = ∅` for `d ∉ E_doc`, freshness precondition `e ∉ E`). The conclusion that `M' = M` and registration is carried solely by E follows directly from the ASN's stated definitions.

## Issue 3: SubAllocatorAxiom is declared "inherited without modification" yet its Disjointness clause is re-derived in full
Reason: Editorial/organizational fix. Whether to cite ASN-0093's Disjointness clause or relabel the discharge as a local lemma is internal to this ASN's structure and the cross-ASN reference to ASN-0093; neither design intent nor implementation evidence bears on it.

## Issue 4: P4a is proved twice — the four-component derivation is subsumed by the extended-state derivation
Reason: Internal redundancy fix. The ASN establishes that the link-free fragment is the special case where J1'★ reduces to J1', so dropping the vestigial four-component derivation is derivable from the ASN's own structure.
