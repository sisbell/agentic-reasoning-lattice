# Review of ASN-0043

## REVISE

### Issue 1: Meta-prose around the L1c chain condition explains why the guard is encoded rather than what it says
**ASN-0043, L1c — LinkAllocatorConformance (paragraph immediately after the chain formula)**: "Both child-spawn guards appear, mirroring TA5a's two cases ... so the chain condition literally states T10a-conformance rather than leaving one conjunct for the reader to reconstruct. The two guards are not symmetric in force, however: on a T4-valid input `zeros(tᵢ₋₁) ≤ 3` holds unconditionally, so the `k = 1` guard is discharged automatically and never excludes a step ... The `k = 2` guard is the only child-spawn constraint that can actually fail ... We encode both for fidelity to T10a while noting that only the latter is binding here."

**Problem**: This is a four-sentence justification of an authorial encoding choice ("We encode both for fidelity to T10a"), not reasoning that advances the claim. It explains *why* the redundant `k = 1` conjunct is present and *that* it is non-binding — exactly the "new prose around an axiom explains why the axiom is needed rather than what it says" pattern the anti-bloat classifier targets. The chain formula already states both guards; the reader does not need a paragraph defending their inclusion. The precise reader must skip past this to reach "The first step seats the field-separating zero...".

**Required**: Collapse to at most one clause stating the operative fact (e.g., that on T4-valid inputs the `k = 1` guard is automatically discharged by T10a.4, so only the `k = 2` guard at `zeros = 3` constrains a step), or delete it entirely. Drop the "for fidelity / we encode both" framing.

### Issue 2: The Coverage definition note states its single point twice
**ASN-0043, Definition — Coverage (closing note)**: "Note that coverage is a lossy projection: two endsets with different span decompositions may have identical coverage. Coverage tells us *which addresses* an endset references, abstracting away the particular decomposition into spans, but it does not determine endset identity."

**Problem**: Both sentences assert the same fact — coverage discards span-decomposition information and so does not fix endset identity. The second sentence re-says the first in different words. The point is also demonstrated non-vacuously in the worked example (Step 6, `Θ_split` vs `Θ_single`), so the duplicated prose carries no additional content.

**Required**: Keep one sentence (the lossy-projection statement) and delete the restatement.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
