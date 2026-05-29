# Channel Assignment — ASN-0040 review-113

**Date:** 2026-05-29 05:28

## Issue 1: B8's formal contract makes the whole claim conditional, contradicting its own "unconditional" cross-namespace clause
Reason: Internal. The proof already separates Case 1 (same-namespace, uses B-Seq) from Case 2 (cross-namespace, uses only B7); the fix is editorial — split the formal contract to mirror the two cases and confine the single-authority precondition to Case 1. No design-intent or implementation evidence is required.

## Issue 2: B8 cites a "no-fork clause" that B-Seq's formal axiom does not contain
Reason: Internal. The review's determinism route is self-contained: a baptism is a transition edge (B4) and `baptize(p,d)` is a partial function (NoDeallocation), so two distinct commits with equal source state + same namespace would be the identical edge — contradiction yields s₁ ≠ s₂. This needs only properties already present in the ASN, no external channel.

## Issue 3: B7 re-derives a guarantee the foundation already proves, using a notation that duplicates the foundation allocator stream
Reason: Internal. Whether B7 reduces to T10a.6/GlobalUniqueness, or instead requires the stated generality over arbitrary B6-valid p ∈ T (versus allocators in a conforming tree), is settled by comparing B7's quantification against the foundation theorems in ASN-0034 — both within the spec corpus. No design intent or implementation behavior is in question.

## Issue 4: Repeated frame-dispatch boilerplate across three invariant proofs
Reason: Internal. Pure refactoring — lift the frame-case preservation into a single statement under B0a and cite it from B1, B10, B_fin. Nothing about design intent or implementation is involved.
