# Channel Assignment — ASN-0042 review-119

**Date:** 2026-05-30 04:53

## Issue 1: O7(c) restates the same condition-classification three times with an intra-claim deferral
Reason: Pure expository consolidation. The (iii)/(v)-binding vs (ii)/(iv)-auto-discharged classification is already argued in the ASN's own O7(c) proof; the fix moves it to one location. No design intent or implementation evidence is involved.

## Issue 2: Condition (v) prose defers its content instead of stating it
Reason: Internal. Condition (v)'s content (next-reachability, `pfx(π') = next(Σ.B, p, d)`) is already fully stated in the Delegation definition and Formal Contract; the fix either inlines that content or deletes the pointer. Derivable from the ASN alone.

## Issue 3: Fresh-baptism of a delegate prefix is encoded redundantly and near-circularly
Reason: Internal logical hygiene. All four facts (O18, O17b, condition (v), Freshness-(v)) are present in the ASN; the fix is designating one primitive and deriving the rest to break the circular triple-statement. This is a deduplication of the formal model's own axioms, requiring no design intent or code evidence.

## Issue 4: A load-bearing invariant is buried as an inline one-line induction
Reason: Internal. The base case (O14 bootstrap-registry clause) and inductive step (O17b) are already cited in the ASN; the fix promotes them to a named derived invariant with base/step shown once. No external channel needed.
