# Channel Assignment — ASN-0047 review-305

**Date:** 2026-06-02 00:19

## Issue 1: K.μ⁻ "equivalence" of constructive precondition and post-state characterization is overstated — strictness is dropped on one side
Reason: This is a purely logical mismatch between the stated biconditional, the strict-contraction conjunct, and the `⊆` reverse-direction proof — all the relevant definitions (constructive precondition, effect clause, reverse proof) are present in the ASN, so the fix (align strictness or recast as a shape equivalence) is derivable internally.

## Issue 2: Document-ordering justification in body prose (forward-reference accretion)
Reason: This is an editorial self-containment fix — the justifying content (K.δ Document-case effect growing both sets by `{e}`; the off-`E_doc` default-value convention) already appears in the ASN, so inlining it to remove the "stated immediately below" pointer requires no external input.
