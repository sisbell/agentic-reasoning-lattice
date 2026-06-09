# Channel Assignment — ASN-0117 review-3

**Date:** 2026-06-08 22:16

## Issue 1: The "weakest precondition" formula is strictly stronger than the weakest precondition
Reason: Internal fix — the error is a quantifier-structure mismatch between the per-slot universal formula and the existential discoverability semantics (LP12) already stated in the ASN; the correction is purely logical and derivable from the ASN's own definitions and prose.

## Issue 2: DEL-REMOVE's first conjunct is false under within-document sharing
Reason: Internal fix — within-document sharing (S5/M13) and the worked example `M(d)(q_2)=a_5` are already present in the ASN, and the corrected statement follows directly from the gap-closure clauses already derived; no design intent or implementation evidence is required.
