# Review of ASN-0103

I read the operation, traced the two-branch K.δ decomposition, and checked the load-bearing proofs — freshness, the cross-allocator version-dominance argument in CND.monotone, the `D_A = E ∩ S(A,2)` identity, and the full invariant discharge against `ExtendedReachableStateInvariants` + P3.

The proofs hold up under scrutiny:

- **Version-dominance (CND.monotone, subsequent case)** correctly avoids T9 (which is same-allocator only) and resolves `d > v` by direct T1 case (i) at position `#A+2`, with `i ≤ p−1 < p` established via the length-filtered `D_A` and entity permanence (P1). The first-fork operand is pinned to a root document `[A,0,i]` through a clean length argument (`#t < #A` contradicts `zeros(t)=2`; the single `k=2` descent must be off `A` itself, else `A ≼ t` breaks). No hand-wave.
- **The length filter** (`#e = #A+2`) is genuinely load-bearing and is motivated by the worked example's collision (`inc(v1,0) = [1,0,1,0,1,2]` would re-baptise the next version). `D_A ⊆ S(A,2)` is proved via the unique parse, not asserted.
- **Freshness** routes version distinctness through B7 namespace disjointness and cross-account through GlobalUniqueness/B8 — and the ASN correctly declines to use T10, observing that `Account(A')` alone does not discharge T10's non-nesting premise. That is a precise catch.
- **Edge cases covered**: `D_A = ∅` (first document, vacuous version-dominance), gaps in the stream (explicitly not relying on contiguous-prefix), boundary `zeros(A)+1 = 2 ≤ 3`.
- **Invariant discharge** is exhaustive: all 32 per-state conjuncts of `ExtendedReachableStateInvariants` plus the 3 composite-boundary properties and P3 are each assigned to direct/vacuous/frame, and the count is complete.
- **Ownership scoping** is handled with care: CND.own derives only the structural `pfx(π) ≼ d` (pure prefix transitivity from the precondition, no registry needed) and explicitly defers the effective-owner statement `ω_{Σ'}(d) = ω_Σ(A)`, correctly noting that `ω` is defined over a registry component absent from ASN-0047's state and that no foundation couples `E` to `B` on the document chain. The deferral is recorded as an open question rather than papered over.

All cross-ASN references are to foundation ASNs (0034, 0036, 0040, 0042, 0045, 0047, 0093); CREATENEWVERSION and other deferred operations are flagged out of scope, not cited as numbered dependencies.

## REVISE

(none)

## OUT_OF_SCOPE

The `E`↔`B` coupling invariant needed to derive the effective-owner reading of ownership is correctly identified by the ASN itself as belonging to a registry-carrying ASN; this is appropriate deferral, not an error here.

VERDICT: CONVERGED
