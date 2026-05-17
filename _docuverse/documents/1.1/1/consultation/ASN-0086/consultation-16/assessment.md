# Channel Assignment — ASN-0086 review-16

**Date:** 2026-05-16 22:04

## Issue 1: Worked Sketch Step 2 omits concrete L-invariant verification at a₂
Reason: The required fix is a mechanical replay of Step 1's L-invariant verification at a different concrete tumbler, using only definitions and lemmas (L0-L14a, R0 Step 4) already established in the ASN. Fully derivable from the ASN's own content.

## Issue 2: Emit_K's Definition does not specify when fresh emissions enter A_K
Reason: The clarification follows directly from definitions already present in the ASN — R0a's antichain property, the Nullify operation's unit-depth-span shape, and the "Crafted-span retractions" remark already acknowledge both regimes. Composing these into a postcondition note about A_K-membership requires no new design intent or implementation evidence.

## Issue 3: R0a's relationship to the substrate emission primitive could be more cohesively stated
Reason: This is a presentation issue — the required summary paragraph gathers and restates material already distributed across five sections of the ASN. No external information is needed; the dependency chain is fully present in the existing text.
