# Channel Assignment — ASN-0040 review-71

**Date:** 2026-05-29 00:18

## Issue 1: Defensive "what is not needed" clause in S0
Reason: Purely editorial deletion of a defensive clause; the surviving claim (operands lie in T) is already established by the cited TA5 axioms in the proof. No design intent or implementation evidence bears on the wording.

## Issue 2: Redundant meta-prose about condition (iii) being subsumed by (i)
Reason: Relocating a single observation to B6's definition and deleting its repetitions is internal bookkeeping; the mathematical content (when (iii) binds) is fully settled within the ASN's own proof.

## Issue 3: Forward use-site pointer in B5a follow-up
Reason: Dropping a downstream-consumer pointer while keeping the self-standing uniformity result is a prose edit; the derived equation is proved from TA5/B5/B5a already present.

## Issue 4: B8 single-path scoping stated three times
Reason: Consolidating three restatements of the co-reachability scope into the headline is editorial; the scope's correctness is internal to B8's own statement and proof.

## Issue 5: Redundant unboundedness restatement in B9 proof
Reason: Trimming essayistic re-argument down to the load-bearing NAT-closure + TA5(c) fact is internal; the induction and its conclusion already live in the ASN.

## Issue 6: Defensive "what it is not" clause in B4 prose
Reason: Deleting a contrast against a misreading is editorial; the read-against-precondition-state semantics and Σ-placement are already stated in B4.

## Issue 7: Defensive parenthetical in S2 statement
Reason: Both the drop and the tightening ("among trailing-zero parents the only length-1 case is [0]") follow from the ASN's own length arithmetic (#p ≥ 2, T0, T4); no external channel needed.
