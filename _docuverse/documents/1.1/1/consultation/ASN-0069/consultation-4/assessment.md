# Channel Assignment — ASN-0069 review-4

**Date:** 2026-05-25 12:58

## Issue 1: V11's inductive step double-counts V5 invocations
Reason: Pure proof-structure correction. V4, V5, and V8 are all properties defined within this ASN, so the choice between (a) using V4 + IH directly or (b) substituting V8 for V4 is derivable from the existing statements alone.

## Issue 2: V10's notation conflates parallel and sequential forks
Reason: The fix is a notational clarification consistent with V1's already-stated dispatch on `A_v(d_src)`'s emission state. Sequential semantics is the only admissible reading given V1; no external input is needed.

## Issue 3: Undefined reference "P.2" in K.μ⁺ verification
Reason: Internal labeling cleanup. V0's stated precondition and the non-empty-case dispatch supply the correct citation directly.

## Issue 4: V6's subspace-identifier justification cites the wrong property
Reason: The body of the ASN already defines `V_{s_C}(d) = {v ∈ dom(M(d)) : subspace(v) = s_C}` and attributes it to ASN-0047. The citation correction is internal.

## Issue 5: V_{s_C}(d_new) = V_{s_C}(d_src) exact equality not stated
Reason: The verification in "The Fork Composite" already establishes the exact equality step-by-step (K.δ → ∅, K.μ⁺ adds exactly `V_{s_C}(d_src)`, K.ρ frames M). Promoting it to a named property is a pure restatement.

## Issue 6: V8b's "preserve or shrink this inclusion but never violate it" is unclear
Reason: Mechanical restatement of the monotonicity claim using a clearly time-indexed set. The mathematical content is already in V8b's derivation; only the framing changes.

## Issue 7: K.μ⁺ verification cites S3 instead of S3★
Reason: The reviewer supplies the correct citation directly (S3★ at `d_src` restricted to subspace = `s_C`, ASN-0047). Since ASN-0069 operates explicitly on the ASN-0047 extended state, the substitution is internal.

## Issue 8: Worked example covers only first-fork case
Reason: V1's subsequent-fork rule (`d_new = inc(d_prev, 0)`), V2's prefix-ancestry chain, and the TA5(c) reasoning already established in the inductive step of the prefix proof supply everything needed to extend the worked example. No external input required.
