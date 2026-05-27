# Channel Assignment — ASN-0099 review-14

**Date:** 2026-05-26 20:12

## Issue 1: F4's "any further refinement" general clause is informally stated
Reason: The fix is internal — either tightening the abstract minimality argument or restricting realizability claims to the three enumerated cases. The structural minimality of F1 follows from the definition itself; the canonical-span realizability question is internal to the spec's existing machinery (PrefixSpanCoverage, L4).

## Issue 2: `result(I, Σ)`, `result_filtered(C, Σ)`, `result_scoped(I, S, Σ)` introduced informally
Reason: Pure notational/definitional issue. The fix is to either add type signatures matching the style used for `image`, `matches`, `findlinks`, or rephrase conformance claims without naming the symbols. Internal.

## Issue 3: F9 inductive composition is gestured at but not stated
Reason: A binary internal choice — either promote to a labeled claim (one-line transitivity-of-equality derivation chaining into F8 over endpoints) or delete the dangling paragraph. No external evidence required.

## Issue 4: F10's chronological-order derivation rests on an unstated assumption
Reason: Citation work — the K.λ "subsequent emission" precondition exists in ASN-0093 (the reviewer already cites it), and the fix is to surface that citation in F10's derivation. Derivable from existing spec text.

## Issue 5: F10's cross-document T1 case (ii) sub-argument has a subtle gap on length comparison
Reason: Pure formal-verification gap-filling. The length values are computable from existing ASN content (`#b_L(d) = #d + 2` from the anchor construction in ASN-0093). Internal.

## Issue 6: Worked example doesn't exercise type-endset filtering
Reason: Example construction using existing formal machinery. L3 (ASN-0043) mandates slot 3 non-empty; L4 permits any address in T. The author picks any tumbler addresses for the type-endsets and verifies F2-filt/F3-filt fire correctly. No external input needed.

## Issue 7: Worked example doesn't exercise link-subspace V-positions or address-of-address links
Reason: Example construction. K.μ⁺_L is defined in ASN-0047, S3★ (ASN-0047) establishes the cross-subspace property, and L4 permits endsets to reference link addresses. All formal machinery is in place; the author constructs a witness. Internal.

## Issue 8: F10 prose has minor informalities
Reason: Terminology fix using vocabulary already established in ASN-0093 (SequentialTransitionAxiom, transition order). No external input needed.
