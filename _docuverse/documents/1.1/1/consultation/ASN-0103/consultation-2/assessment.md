# Channel Assignment — ASN-0103 review-2

**Date:** 2026-06-05 00:06

## Issue 1: Dangling reference to undefined claim label "Q10"
Reason: Internal fix. The claims table already restates this fact as CND.E; replacing the stale label requires no design intent or implementation evidence.

## Issue 2: Ownership derivation invokes `ω_Σ(A)` without establishing `A ∈ Σ.B`
Reason: Internal fix. Whether `A ∈ Σ.B` is added as a precondition or discharged via an E↔Σ.B coupling invariant is a formal-bookkeeping choice within the existing foundation vocabulary (ASN-0042/0047); no design intent or implementation behavior is in question — the entity/registry coupling is a spec-internal definitional matter.

## Issue 3: Superseded invariant cited in the extended-state context
Reason: Internal fix. The ASN already establishes S3★ (ASN-0047) supersedes S3 (ASN-0036) and discharges S3★ in Invariants Maintained; aligning Effect Two's citation is purely internal consistency.
