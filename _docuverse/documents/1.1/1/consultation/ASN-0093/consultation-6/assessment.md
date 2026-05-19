# Channel Assignment — ASN-0093 review-6

**Date:** 2026-05-18 18:17

## Issue 1: L3 invariant statement not reverted
Reason: Pure mechanical revert per the patch's explicit instruction; the substitute form is given in the review itself and aligns with ASN-0043's already-cited general form. No external input needed.

## Issue 2: K.λ operation signature still locks to three-arity
Reason: Structural consequence of Issue 1's L3 revert — if L3 admits N ≥ 3 links, the operation that constructs them must accept N-arity sequences. K.λ's atomicity and overall shape are unchanged; only the value-shape parameter generalizes. Derivable from the ASN plus the patch.

## Issue 3: Parameter semantics paragraph not updated for K.λ
Reason: Pure citation update — the paragraph just references K.λ's signature and must match whatever Issue 2 produces. Internal.

## Issue 4: Registry entry for L3 not updated
Reason: Pure registry consistency update reflecting Issues 1 and 2. The new name and source text follow mechanically from ASN-0043's L3 and the revised K.λ precondition. Internal.

## Issue 5: Discharge matrix entry for L3 cites fixed-three-arity precondition
Reason: Pure consistency update — the discharge cell must cite the revised K.λ precondition produced by Issue 2. Internal.

## Issue 6: Open Questions item contradicts patch
Reason: Pure consistency cleanup — the item is invalidated by the L3 revert and either deletes or rewrites as a forward-looking note. Internal.

## Issue 7: Worked example consistency check
Reason: Mechanical reconciliation between the example's three-tuple invocations and the revised K.λ signature; the arity-3 default is already preserved by the patch as the StandardTriple convention. Internal.
