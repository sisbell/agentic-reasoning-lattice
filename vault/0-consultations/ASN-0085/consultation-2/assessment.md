# Revision Categorization — ASN-0085 review-2

**Date:** 2026-04-11 01:21

## Issue 1: Inverse claims stated in prose, not in formal contracts
Category: INTERNAL
Reason: The inverse properties follow mechanically from the definitions of ord and vpos already present in the ASN. Promoting them to formal postconditions with explicit preconditions requires only the definitions and S8a conditions already stated in the document.

## Issue 2: w_ord actionPoint postcondition not conditioned on w > 0
Category: INTERNAL
Reason: The fix is adding a `w > 0` guard to the actionPoint postcondition. The ASN already correctly conditions the positivity postcondition on `w > 0` and references TA0's requirement — this is an internal consistency fix matching the pattern already used in the same contract.

## Issue 3: No concrete example
Category: INTERNAL
Reason: The review supplies the exact examples. Computing them requires only plugging values into TumblerAdd and the extraction functions defined in this ASN — no external design intent or implementation evidence needed.

## Issue 4: TA7a connection claimed but not derived
Category: INTERNAL
Reason: The corollary chains OrdAddHom (proved in this ASN) with TA7a's S-membership postconditions (established in ASN-0034). Both sides are already formally stated; the missing piece is one sentence of derivation connecting them, which the review spells out explicitly.
