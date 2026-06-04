# Channel Assignment — ASN-0101 review-52

**Date:** 2026-06-04 05:44

## Issue 1: Projection-picture preamble duplicates D9
Reason: Purely editorial deduplication — drop the three informal bullets that restate D9's three clauses verbatim. No design intent or implementation evidence is at stake; the fix is internal prose surgery.

## Issue 2: D3 closing paragraph restates the content/link parallel without new content
Reason: The substantive reasoning is already present in the two preceding paragraphs; removing the restatement paragraph is derivable from the ASN's own structure. No channel needed.

## Issue 3: `V_S(·)` overloaded onto arrangements without definition
Reason: A notational gap fixable from the ASN alone — either add the one-line definition `V_S(N) := {v ∈ dom(N) : subspace(v) = S}` or inline the explicit set. Internal.

## Issue 4: D2 "cardinality consequence" over-reaches past DELETE
Reason: Trimming the cross-vocabulary monotonicity claim to DELETE's own strict-equality consequence is derivable from D2 itself; the over-reaching assertion about K.α and other transitions is simply out of scope. Internal.
