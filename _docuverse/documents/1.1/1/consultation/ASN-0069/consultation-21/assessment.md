# Channel Assignment — ASN-0069 review-21

**Date:** 2026-05-25 18:47

## Issue 1: Σ^k notation overloaded between sections
Reason: Pure notational disambiguation internal to the ASN — no design intent or implementation evidence is required to choose disjoint notation between the verification sub-states and the post-composite states.

## Issue 2: V11 inductive-step parenthetical claims a V4b equality chain that the formal premise cannot support
Reason: The fix is derivable from the ASN's own machinery — the induction hypothesis already supplies `v ∈ dom(M^{k-1}(d^{k-1}_new))` and `subspace(v) = s_C` follows from `v ∈ V_{s_C}(d_src)`, giving the inclusion `V_{s_C}(d_src) ⊆ V_{s_C}(d^{k-1}_new)` that V4 at step k needs. No external input required.

## Issue 3: V11 prose / formal premise mismatch
Reason: Alignment between prose and formal premise is an internal editorial choice within the ASN; the necessary scope is determined by what the revised Issue 2 proof actually consumes, which is fixed by the ASN's own logic.

## Issue 4: V0 Effects table — "V_{s_C}(d_src)" used without state subscript where ambiguity matters
Reason: V5 (already established in this ASN) supplies the pre/post-state invariance of `M(d_src)`; the fix is to surface that invariance in the Effects table via annotation. Purely internal disambiguation.
