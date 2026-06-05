# Channel Assignment — ASN-0100 review-63

**Date:** 2026-06-05 02:40

## Issue 1: A bullet labeled "not admissible" concludes the opposite
Reason: Pure editorial restructuring — relocating or relabeling a passage so the header matches its content. The correct content (the `n'_{s_C} = 0` decomposition is admissible) is already established within the ASN itself; no design intent or implementation evidence is at stake.

## Issue 2: Inter-step ordering constraints stated twice in the same section
Reason: De-duplication of two passages that argue the same ordering constraints from the same preconditions, both already present in the ASN. Consolidating them requires only the ASN's own content.

## Issue 3: Cross-document projection invariance derived twice
Reason: De-duplication — the same LP4-composed result with the same citation appears in two sections. Choosing one location and cross-referencing is internal editorial work needing no external channel.

## Issue 4: The `#p = m_C` precondition is self-referential in the empty case
Reason: The genuine constraint (`#p ≥ 2` for the empty case, `m_C` fixed by S8-depth for the non-empty case) is already stated in the ASN via the precondition list and `ValidFirstInsertionPosition`; splitting the precondition into its two cases is a clarity edit derivable from the ASN alone.
