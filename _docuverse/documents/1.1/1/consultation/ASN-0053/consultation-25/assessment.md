# Channel Assignment — ASN-0053 review-25

**Date:** 2026-05-13 15:13

## Issue 1: S11 tightness claim asserted without derivation
Reason: The required derivation uses S0 (convexity) and N2 (strict inequality), both already present in the ASN. The argument is purely structural — a single convex span cannot denote a set with a gap. No external evidence needed.

## Issue 2: S11c Case 1 lacks explicit element-chase
Reason: The element-chase uses only the case hypothesis (start(α) < start(β) < reach(α) < reach(β)) and the definitions of ⟦α⟧ and ⟦β⟧ already in the ASN. Mechanical derivation, internal to the proof.

## Issue 3: S7 claim is trivially achievable; proof's content unstated
Reason: This is a claim-vs-proof alignment decision internal to the author. Either tighten the claim to match the construction (|Σ| ≤ |P|) or weaken it to sufficiency-only — both options are derivable from the ASN's own content and S7's downstream usage (none in this ASN).

## Issue 4: Symmetry-by-relabeling in S3b Case B is left implicit
Reason: This is a proof formulation choice — whether S3b recovers an ordered or unordered pair. Since S3 (merge) is commutative (S3a) and the input pair {α, β} is unordered under merge, the natural resolution is internal: state the conclusion as recovery of the unordered pair or pin down λ/ρ assignment per case using only definitions already present.
