# Channel Assignment — ASN-0036 review-77

**Date:** 2026-05-11 00:49

## Issue 1: D-SEQ "Assembly" step skips a step
Reason: Pure proof-gap closure — the bridge from {finite, contiguous, contains 1} to {1, ..., n} is standard mathematical reasoning (define n = max, apply contiguity, conclude equality). Fully derivable from the ASN's own definitions.

## Issue 2: S8 uniqueness-within-subspace proof conflates generic t and specific w
Reason: Structural reorganization of an existing proof — extract a clean within-subspace incompatibility lemma, then apply it. No design intent or implementation evidence required; the mathematical content is already in the ASN.

## Issue 3: ValidInsertionPosition empty-case parameterization is implicit
Reason: Pure formalization choice — the ASN already establishes that m is an operational input not fixed by the strand model (citing LM 4/31). The fix is to make the predicate's signature match this commitment (relation on (v, m) or parameter m), not to learn new facts about design or implementation.

## Issue 4: OrdAddHom precondition contains redundancy
Reason: Internal consistency check against ASN-0034's ActionPoint contract — `#w = m` together with ActionPoint's `1 ≤ actionPoint(w) ≤ #w` makes `actionPoint(w) ≤ m` automatic. Derivable from cited dependencies alone.
