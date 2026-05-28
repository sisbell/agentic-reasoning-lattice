# Channel Assignment — ASN-0100 review-16

**Date:** 2026-05-28 12:25

## Issue 1: L0's content-subspace clause is treated as "a property of L alone" — but INSERT mutates dom(C)
Reason: The correct justification (`subspace_I(a_k) = s_C` by SubAllocatorAxiom.Subspace / DisjointSubAllocatorChains) is already established in the ASN's own §Effect One when discharging the `a_k ∉ dom(Σ_k.L)` clause; the fix just relocates that reasoning into the L0 discussion.

## Issue 2: INS.inv.func cites a lemma the proof does not use
Reason: The body proof already states which facts it uses (TumblerAdd component arithmetic + TS2); correcting the table to match is purely internal bookkeeping.

## Issue 3: Case (i.b) decomposition analysis introduces a non-load-bearing, environment-dependent alternative that obscures the contract
Reason: Trimming to the load-bearing fact (K.μ⁻ omitted because no admissible firing shrinks `s_C` while preserving `s_L`) is an editorial reduction; that fact is already present and the parallel treatment of case (i.a) is already in the ASN.
