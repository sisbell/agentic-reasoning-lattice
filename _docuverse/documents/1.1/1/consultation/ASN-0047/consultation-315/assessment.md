# Channel Assignment — ASN-0047 review-315

**Date:** 2026-06-02 02:08

## Issue 1: K.δ characterizes case-(ii) freshness as caller-checked "not derived from a structural fact," but the worked examples and S7d derive it from GlobalUniqueness
Reason: The fix splits the freshness characterization by regime using machinery already present in the ASN (FrontierEquivalence for k=0; T10a at-most-once-per-(t,k') plus GlobalUniqueness for k∈{1,2}, as the worked examples and S7d already discharge). No design intent or implementation evidence is needed — the correction is purely aligning the prose with the ASN's own discharges.

## Issue 2: The Bridging lemma justifies (†) `dom(M) = E_doc` twice
Reason: Pure editorial deduplication — keep the rigorous lockstep + default-value justification and delete the informal restatement; entirely internal.

## Issue 3: P4a definition box carries a forward-deferral and a prose restatement that add no content
Reason: Pure editorial cleanup — delete the forward-pointer and the prose restatement, relying on the existing preamble for temporal-scope classification; entirely internal.
