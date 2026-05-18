# Channel Assignment — ASN-0093 review-4

**Date:** 2026-05-18 14:38

## Issue 1: T10a chain-lemma applicability remark mis-attributes T4-validity dependency to T10a.1 and T10a.7
Reason: Fix is internal — verifiable directly against ASN-0034's stated dependency lists for T10a.1, T10a.7, T10a.8. No design intent or implementation evidence is at stake; the remark either correctly cites ASN-0034 or it doesn't.

## Issue 2: K.α and K.λ subsequent-emit freshness derivations skip the max-comparison step
Reason: Fix is internal — spelling out the max-comparison step uses only T10a.7 (cited), ChainMembershipForOrigin (proved in-ASN), and the max-property of `a_prev` (definitional). No external channels needed.

## Issue 3: ChainMembershipForOrigin lemma's "partition" wording oversells the proved subset claim
Reason: Fix is internal — either restate as subset inclusion (with partition as corollary from C2 + Cross-document disjointness, both already in-ASN) or extend the proof body using substrate machinery already present. No external channels needed.

## Issue 4: L1c invariant statement uses `a` for the link address, breaking convention with K.λ
Reason: Pure notational consistency fix — rename `a` to `ℓ` in L1c's statement to match K.λ and the chain exhibition. No design or evidence question involved.

## Issue 5: T7 alias "SubspaceDisjointness" diverges from ASN-0034's canonical name
Reason: Fix is internal — ASN-0034 establishes the canonical name "FirstElementFieldDistinction"; either use it or add an alias note. Pure citation hygiene.

## Issue 6: Subsequent emissions implicitly form a contiguous initial segment of the sub-allocator chain, but the substrate never states or proves this
Reason: Fix is internal — the author must choose between stating contiguity as an explicit inductive invariant or noting that the max-property alone (with T10a.7's strict monotonicity) suffices for freshness without contiguity. Both routes use machinery already in the ASN.
