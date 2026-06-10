# Channel Assignment — ASN-0116 review-59

**Date:** 2026-06-09 21:49

## Issue 1: The reachability-licensing step is established twice across a section boundary
Reason: Purely structural deduplication — the fix deletes a re-derivation already concluded one section above and opens directly with its use. No design intent or implementation evidence is at stake; the licensing chain (valid composite + Σ reachable ⟹ post-state reachable) is internal to the ASN and stated verbatim in the prior section.
