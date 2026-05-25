# Channel Assignment — ASN-0051 review-25

**Date:** 2026-05-15 21:13

## Issue 1: SV1 and SV12 numbering gaps
Reason: Purely editorial bookkeeping — whether to renumber consecutively or annotate the gaps is an internal documentation choice derivable from the ASN's own revision history and label usage. Neither design intent nor implementation evidence bears on the fix.

## Issue 2: Confused empty-endset and empty-query collapse
Reason: A notational disambiguation issue — the definitions of π, locate, and discover_s already present in the ASN make clear which argument is an endset versus an I-address set. The corrected statement follows mechanically from those definitions; no external channel is needed.

## Issue 3: Loose biconditional on locate–π relation
Reason: A formal quantifier fix derivable entirely from the definitions of locate and π already stated in the ASN. The restriction v ∈ dom(M(d)) is built into locate's defining set comprehension; no external channel is needed.
