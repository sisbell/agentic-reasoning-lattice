# Channel Assignment — ASN-0087 review-71

**Date:** 2026-06-04 03:28

## Issue 1: The "state-determined" conclusion about `v_ℓ` is asserted repeatedly across sections
Reason: Pure prose-dedup edit — delete a redundant rationale clause and let the lead-in carry the state-determinacy point. No design intent or implementation evidence bears on which sentence to keep; fully derivable from the ASN's own text.

## Issue 2: `v_ℓ`'s derivation rule is spelled out in four places
Reason: Internal consolidation — collapse four restatements of one mechanical positioning rule to a single home in *Effect* with pointers elsewhere. The rule's content is already fixed by K.μ⁺_L and M-DepthConv within the ASN; no external channel is needed.
