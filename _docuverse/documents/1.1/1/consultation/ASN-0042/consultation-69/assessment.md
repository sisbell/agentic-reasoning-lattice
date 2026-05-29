# Channel Assignment — ASN-0042 review-69

**Date:** 2026-05-29 06:31

## Issue 1: O1a and O1b are simultaneously labeled axioms and proved by induction
Reason: The fix is a logical-consistency decision internal to the ASN. The review itself supplies the deciding argument — Π grows by O15, which does not force `zeros ≤ 1` or injectivity, so these must be derived invariants with O14(iii)/(iv) as base cases. Relabeling and removing the contradictory framing is derivable from the ASN's own proof structure.

## Issue 2: The T8-vs-B0 parenthetical is repeated verbatim across the document
Reason: Pure editorial deduplication; the T8/B0 distinction is already correct and just needs to be stated once and cited thereafter. No external evidence required.

## Issue 3: DelegatorAllocatesPrefix duplicates O18's "two views of one act" prose
Reason: Editorial deduplication — the coupling claim is already carried by O18, so DelegatorAllocatesPrefix can cite it. Internal.

## Issue 4: Use-site inventories around axioms and definitions (forward-reference accretion)
Reason: Removing downstream-consumer enumerations is editorial; consumers already cite the properties they use. No design or implementation input needed.

## Issue 5: O10's "longer Form B sub-delegates" sub-paragraph re-treats a case already excluded
Reason: The length argument already discharges these sub-delegates, so the redundant sub-paragraph can be cut using the proof's own existing reasoning. Internal.

## Issue 6: The worked example's B6/B1/hwm bookkeeping drifts into baptism-mechanism territory
Reason: The ASN itself declares baptism mechanism and allocation invariants OUT OF SCOPE and assigns B6/B1 to ASN-0040; reducing the trajectory to ownership-relevant facts and citing ASN-0040 is derivable from the ASN's own scope boundaries.
