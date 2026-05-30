# Review of ASN-0058

## REVISE

### Issue 1: Duplicate causal claim bracketing the Split-Merge Duality section

**ASN-0058, "The Split-Merge Duality" (section intro and post-M10 paragraph)**:
- Intro: "This is the algebraic core of the permutation model, and it holds because width coupling (M0) forces both dimensions to split and merge at the same count."
- After M10: "The algebra is clean — it works precisely because width coupling forces both dimensions to split and merge at the same ordinal count."

**Problem**: These two paragraphs in the same section state the same causal claim in slightly different words ("holds because width coupling forces both dimensions to split and merge at the same count" / "works precisely because width coupling forces both dimensions to split and merge at the same ordinal count"). This is the anti-bloat pattern "two paragraphs in the same document say the same thing in different words." The post-M10 editorializing ("The algebra is clean") adds nothing the section intro and M9/M10 proofs do not already establish.

**Required**: Keep the causal observation in one slot. The bijection statement after M10 is the substantive content; drop the redundant "it works precisely because…" clause (or drop the equivalent sentence from the intro).

### Issue 2: M7-cov forward-pointer stated twice within four lines

**ASN-0058, M7**:
- "Both conditions are necessary, and a fourth case — V-overlap — is impossible by M7-cov below."
- "*Overlap is impossible.* The remaining case `v₂ < v₁ + n₁` is ruled out by the following sub-lemma."

**Problem**: The same forward deferral to M7-cov is carried twice in close proximity — once in the lead summary sentence and again in the dedicated overlap paragraph. The reader receives the identical "overlap is handled by M7-cov" pointer twice before reaching the lemma. This matches the flagged pattern of multiple sentences deferring to the same downstream location.

**Required**: State the overlap-impossibility deferral once. The "*Overlap is impossible.*" paragraph carries it where the case is actually treated; drop the trailing clause from the lead sentence (leave it as "Both conditions are necessary; V-overlap is treated separately below," or fold it into the overlap paragraph alone).

## OUT_OF_SCOPE

None.

VERDICT: REVISE
