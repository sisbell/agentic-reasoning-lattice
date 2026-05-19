# Channel Assignment — ASN-0086 review-72

**Date:** 2026-05-19 16:28

## Issue 1: R7a's proof relies on ChainMembershipForOrigin, which is not in the substrate-conforming catalog
Reason: The author must choose among (a), (b), (c) — a design choice about what substrate-conformance should mean. Nelson's intent on whether chain discipline is substrate-level (vs. K.λ-implementation policy) informs whether option (a)/(b) is faithful; Gregory's evidence on what udanax-green actually enforces grounds whether the categorical claim survives or option (c) is needed.
Nelson question: Was the per-document sibling-frontier chain discipline (single link chain enumeration per document) intended as a substrate-level invariant binding on all conforming link-emission paths, or as a K.λ-specific implementation policy that higher layers could legitimately sidestep with broader L1c-conforming emissions?
Gregory question: Does udanax-green's link allocator deposit link addresses exclusively on the per-document A_L sibling chain enumeration (matching ChainMembershipForOrigin), or does it expose any link-emission path that produces L1c-conforming but off-chain addresses (e.g., deeper element fields, alternative child-spawn patterns under d)?
