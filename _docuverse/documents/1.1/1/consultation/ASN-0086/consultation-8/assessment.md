# Channel Assignment — ASN-0086 review-8

**Date:** 2026-05-16 18:39

## Issue 1: Nullify's single-tuple-scope is discipline-conditional but the proof header and Remark misrepresent the role of P3.
Reason: Both fix options are internal proof-restructuring decisions. The ASN already exposes the relevant dependencies (R0a's discipline-conditional tag, substrate-primitive permissiveness, R0 Step 2's construction); the choice between relabeling versus constraining Emit_R's composition is derivable from the ASN's own content without design intent or implementation evidence.

## Issue 2: R0 Step 4's invariant verification chain omits L12b.
Reason: Pure completeness gap. L12b is a named ASN-0043 lemma and its preservation follows trivially from R0's Frame (`Σ'.M = Σ.M`) plus Step 1's `d ∈ dom(Σ.M)`, both already in the ASN. Adding the bullet requires no external input.
