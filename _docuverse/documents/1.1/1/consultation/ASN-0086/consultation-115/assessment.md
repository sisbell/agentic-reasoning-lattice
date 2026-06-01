# Channel Assignment — ASN-0086 review-115

**Date:** 2026-05-31 22:04

## Issue 1: R0/Emit_K/wp domain declared as the full `↝*` state space, but the proofs rely on state-local invariants the full space explicitly need not preserve
Reason: The contradiction and its fix are internal — the note's own definitions (Categorical reachability, the L-catalog membership of L1c/L-fin) and its own proofs establish the over-reach; restricting the domain to the L1c/L-fin-satisfying sub-space is derivable from the ASN's existing content without design intent or implementation evidence.

## Issue 2: WP Case 1 conflates per-conjunct load-bearingness with weakest-precondition; P2c (full conformance) is strictly stronger than weakest
Reason: This is a pure proof-logic defect — the reviewer's own counterexample and the local-condition fix (mirroring Case 2's `NoCraftedSpanReachesD` treatment) are fully derivable from the ASN's definitions of wp, `nullified`, and R0a.

## Issue 3: Duplicated justification prose around forward references (anti-bloat)
Reason: Purely editorial deduplication; deciding where the non-circularity claim and conformance-free rationale belong requires only the ASN's own text.
