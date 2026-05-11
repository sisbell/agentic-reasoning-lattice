# Channel Assignment — ASN-0036 review-101

**Date:** 2026-05-11 14:29

## Issue 1: Auxiliary lemma in S8 — strict inequality `#aⱼ − δⱼ + 1 < #aⱼ` stated, not derived
Reason: Pure derivation work using NAT-sub, NAT-order, and NAT-addcompat from ASN-0034 (all already cited elsewhere in this ASN). Internal fix.

## Issue 2: Auxiliary lemma in S8 — conclusion (iii) silently assumes T4-validity of `shift(aⱼ, k)`
Reason: Internal expository fix — add a sentence verifying the no-adjacent-zeros and `t₁ ≠ 0` T4 conjuncts using TumblerAdd's prefix rule and T4 on `aⱼ`, both already in scope.

## Issue 3: S7c postconditions stated without derivation
Reason: Restructuring/derivation work using T4b, T4 positivity, and the same NAT-* chain as Issue 1. All foundations are internal to this ASN and ASN-0034.

## Issue 4: subspace_I's postcondition (c) circularity with S8's auxiliary lemma
Reason: Internal structural fix — either inline the two-line derivation under subspace_I (TumblerAdd prefix rule plus the S7c position arithmetic) or rewrite the dependency phrasing. No external evidence needed.

## Issue 5: "observable state" undefined in S3
Reason: Choice between committing to "every state" versus defining a quiescent-state notion is a design-intent question — what did Nelson intend the referential-integrity invariant to guarantee, and at what granularity?
Nelson question: Did the two-stream architecture intend referential integrity (every V-reference resolves) to hold universally at every state, or only at quiescent boundaries between operations — and is mid-operation violation a permitted intermediate condition?

## Issue 6: S5 cross-document construction's `dᵢ` not certified T4-valid where T4-validity is consumed
Reason: Internal citation fix — correct "T0" to "NAT-closure" and explicitly tie `i ≥ 1` to T4's positive-component requirement on `D(dᵢ)`. All references are to ASN-0034 axioms already cited elsewhere.
