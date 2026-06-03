# Channel Assignment — ASN-0071 review-34

**Date:** 2026-06-03 08:23

## Issue 1: Orthogonal axiom invocation in the finiteness proof
Reason: Pure deletion of a non-load-bearing sentence the prose itself labels "orthogonal"; the count closes on finite ancestry + finite composites already present in the ASN. No design intent or implementation evidence needed.

## Issue 2: K.μ~ enumeration clause addresses a case the framing already excludes
Reason: The induction is explicitly over elementary steps and K.μ~ is non-elementary by definition; dropping the clause is internal to the ASN's own framing. Neither channel is required.

## Issue 3: "no appeal to well-formedness" repeated across three slots
Reason: Removing duplicate assertions and retaining the single statement at the PC proof is an editorial deduplication wholly derivable from the ASN's own structure. No channel needed.

## Issue 4: Unmodeled formation-state/evaluation-state distinction
Reason: The vspec is just the pair `(d_s, σ)` with no modeled formation state; reducing to the precondition (optionally one clause citing P1, already in the ASN) is internal. No design intent or implementation evidence required.
