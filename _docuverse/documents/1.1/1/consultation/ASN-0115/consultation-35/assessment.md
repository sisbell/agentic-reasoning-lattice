# Channel Assignment — ASN-0115 review-35

**Date:** 2026-06-10 00:52

## Issue 1: `V_S(d)=∅ ⟹ act=∅` is derived twice, the first time out of dependency order
Reason: Internal. The fix deletes an out-of-order forward-referencing clause whose consequence (`V_S(d)=∅ ⟹ act=∅`) is already established, in proper dependency order, inside R6 via `act` and Confinement. Nothing about design intent or the implementation is at stake — it is a pure dedup/ordering edit derivable from the ASN's own structure.

## Issue 2: R6's closing paragraph speculates about authorization/consultability the model does not have
Reason: Internal. The fix is reductive — strip the "open-document precondition," "authorization," and "consultability" prose (none of which name anything in the substrate) and replace it with a scope note grounded in the model's one precondition, `d ∈ dom(Σ.M)`. The design-intent question this prose gestured at is deliberately left unformalized as an existing open question, so we defer rather than resolve it; no channel is needed to remove speculation and point at a question already posed.

## Issue 3: Forward-reference and justification micro-accretions (batch sweep)
Reason: Internal. Three editorial deletions — a downstream-consumer enumeration, a deferral parenthetical, and a precedent aside appealing to ASN-0058's existence (not using its definition). Each underlying statement (`item`-totality, R9, the depth-compatibility constraint) stands unchanged once the pointer is removed; no design intent or implementation evidence is involved.
