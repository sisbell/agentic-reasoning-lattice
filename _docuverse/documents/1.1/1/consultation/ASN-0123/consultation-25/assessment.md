# Channel Assignment — ASN-0123 review-25

**Date:** 2026-06-13 09:07

## Issue 1: The cross-owner branch's freshness precondition is asserted, not derived
Reason: Internal fix — the reviewer has already named the exact foundation lemmas needed (ASN-0047's ChildSpawnFreshness and FrontierEquivalence, TA5(a), namespace disjointness, K.δ-ID.parent-2), all of which the ASN already builds on (FrontierEquivalence is cited in VN-B1). Discharging the freshness precondition is a structural proof obligation parallel to the owned branch's existing VN-B1 argument; it raises no design-intent question (Nelson) and no implementation-evidence question (Gregory), since the fix concerns the abstract spec's internal completeness, not what the code does.
