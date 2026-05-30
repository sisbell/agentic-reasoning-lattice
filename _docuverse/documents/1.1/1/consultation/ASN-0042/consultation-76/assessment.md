# Channel Assignment — ASN-0042 review-76

**Date:** 2026-05-29 22:53

## Issue 1: The delegation predicate is claimed complete but O18 imposes an unlisted seventh condition
Reason: Internal. The fix is a bookkeeping reconciliation between O15's "six conditions" claim and O18's freshness axiom — either relabel the predicate as "six conditions plus the O18 baptism discipline," add freshness as condition (vii), or note that freshness is supplied by O18 rather than the predicate. All three options are decidable from the ASN's own definitions; the baptism mechanism itself is already out of scope (ASN-0040), so no external channel is needed.

## Issue 2: "Why the axiom is needed" prose attached to O14
Reason: Internal. Pure deletion of justification prose; the clauses' necessity already lives in the consuming proofs (O8, PrefixBaptismCoupling). No design-intent or implementation evidence is required to remove explanatory text.

## Issue 3: Multiple sections defer to the Delegation section for the same content
Reason: Internal. Removing forward-reference pointers and the duplicate (ii)/(vi) restatement is a reorganization of content already present in the ASN; no external evidence informs where a definition is stated.

## Issue 4: Worked-example fork analysis duplicated for π_B
Reason: Internal. The π_A non-coverage argument and the field-opening branch are both already in the ASN; keeping the new case and dropping the transposed restatement is an editorial cut.

## Issue 5: Excluded-case parentheticals (reviser drift)
Reason: Internal. The corollary precondition `a ∈ Σ.B` already forecloses the excluded case; removing the redundant parenthetical and trimming the OwnershipDomainPermanence tail is derivable from the ASN's own preconditions.

## Issue 6: Essay content in the O10 Postconditions slot
Reason: Internal. The depth/sovereignty commentary is already established in the O10 proof body; reducing the Postconditions slot to the formula and `zeros(a')` clause is a placement fix needing no external input.

## Issue 7: `allocated_by_Σ` introduction enumerates downstream consumers
Reason: Internal. The relation's signature and semantics are already stated; dropping the O5/O16 consumer inventory from the introduction is an editorial trim, and both properties reference the relation at their own sites.
