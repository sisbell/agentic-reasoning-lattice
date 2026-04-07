# Review of ASN-0063

## REVISE

### Issue 1: CL0 statement overclaims exactness scope
**ASN-0063, Endset Resolution (CL0 statement)**: "it is contained in the denotation of a span whose element-level members are exactly the image"
**Problem**: The proof establishes that **depth-#a_β members** of ⟦ρ⟧ are exactly the image — not all element-level members. The span's denotation includes proper extensions of image addresses (tumblers t with a_β + k ≼ t, #t > #a_β) that are themselves element-level (zeros(t) = 3). For example, if a_β = `2.0.1.0.1.0.1.1` (depth 8), then `2.0.1.0.1.0.1.1.5` (depth 9) has zeros = 3, lies in ⟦ρ⟧ by T1(ii), and is element-level — but is not in the image.

The proof's own language is correct: "the depth-#a_β members of ⟦ρ⟧ are exactly {a_β + k : c ≤ k < c'}." The companion text after CL1 is also correct: "each CL0 I-span captures every I-address in the image **at depth #a_β**, with no spurious same-depth addresses." The lemma statement is the only place the overclaim appears.

No downstream result depends on the overclaim — CL1, CL2, resolve, and CL11 all use containment only. The fix is localized.

**Required**: In CL0's statement, replace "element-level members" with "depth-#a_β members" (or "members at the I-address depth"). Similarly, the label "Element-level tightness" after CL1 should read "Same-depth tightness" or "Depth-#a_β tightness."

## OUT_OF_SCOPE

### Topic 1: Depth ≥ 2 constraint for the text subspace
The ASN correctly identifies and enforces m_L ≥ 2 for link-subspace V-positions (ordinal shift at depth 1 would alter the subspace identifier). The same constraint applies to the text subspace — at depth 1, shift([s_C], 1) = [s_C + 1], changing the subspace — but is not enforced by S8a or S8-depth in ASN-0036. The constraint holds in practice (D-SEQ with n ≥ 2 at depth 1 is impossible), but an explicit depth ≥ 2 design requirement for all subspaces belongs in ASN-0036, not here.
**Why out of scope**: This is a gap in the foundation layer (ASN-0036), not an error in ASN-0063.

VERDICT: REVISE
