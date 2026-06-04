# Channel Assignment — ASN-0091 review-64

**Date:** 2026-06-04 01:27

## Issue 1: RA-adm is a single-state preservation property but is discharged with a reachability-closure theorem
Reason: The fix turns on what ASN-0047 actually supplies — whether ExtendedReachableStateInvariants is genuinely reachability-keyed, whether any single-step preservation theorem exists for the arrangement-dependent package (S3★, CL-OWN, etc.), and whether the reachability relation is closed under K.μ⁻/K.μ⁺ steps so a "Σ reachable" premise discharges Σ' trivially. These are foundation/knowledge-base facts, not design intent.
Gregory question: Does ASN-0047 supply any single-step (per-transition) preservation theorem for the arrangement-dependent invariants S3★, S3★-aux, CL-OWN, CL-UNIQ, S8★, or is ExtendedReachableStateInvariants — keyed to reachability from Σ₀ — the only available handle, and is that reachability relation closed under valid K.μ⁻/K.μ⁺ transitions?

## Issue 2: "State-Component-Only Invariants" conflates per-transition invariants with single-state predicates
Reason: Correctly partitioning the listed foundation invariants into single-state predicates versus binary transition invariants `(A Σ→Σ' :: …)` requires the exact formal statement of each in its home foundation ASN; the reviewer classified only a sample, and ASN-0091 does not restate their forms. This is knowledge-base evidence.
Gregory question: For each foundation invariant listed under "State-Component-Only Invariants" (S0, S1, S4, S7, S7a, S7b, S7d, M0, M1, P0–P8, NodeLineage, ActivatedEmission, L0, L1, L1a–c, L3, L12, L14, L-fin, C0, C1, C1b, C1c, C2, C-fin), which are stated as single-state predicates over one state and which are stated as binary transition invariants over `Σ → Σ'`?
