# Channel Assignment — ASN-0043 review-83

**Date:** 2026-05-30 09:57

## Issue 1: CPP closing sentence duplicates the `s = h(a)` postcondition it precedes
Reason: Pure editorial deduplication — delete the preview, keep the postcondition. Both the duplicated fact and the redundancy with L1c's chain clause are internal to the ASN.

## Issue 2: Forward-pointing meta-prose justifying lemma ordering in L1c
Reason: Delete a forward-pointer sentence that advances no reasoning; CPP's own precondition already states its requirement. Fully internal.

## Issue 3: Non-load-bearing AllocatedSet apparatus in L11b freshness argument
Reason: Replace the AllocatedSet initial-segment device with the simpler L-fin + T10a.7 finiteness argument; the freshness fact and the cited invariants are all present in the ASN.

## Issue 4: Duplicated "remaining items" inventory
Reason: Consolidate two identical use-site inventories into one statement at FSP with a citation from L11b/L9. Purely structural, internal.

## Issue 5: Downstream-consumer meta-prose embedded in FSP statement
Reason: Trim a consumer-naming clause from the lemma statement, keeping the factual half. Internal editorial fix.

## Issue 6: Redundant "Consequence — identification within a state" subsection
Reason: The trivial half follows from the `Σ.L : T ⇀ Link` typing and L11a's real claim is already stated above; deletion/reduction is derivable from the ASN's own definitions.
