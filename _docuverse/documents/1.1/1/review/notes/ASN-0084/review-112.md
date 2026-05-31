# Review of ASN-0084

## REVISE

### Issue 1: I-start preservation justified by a non-sequitur in R-BLK Phase 3
**ASN-0084, R-BLK, "*I-start, width, and contiguity of reassembled runs*"**: "its I-start is preserved because the rearrangement modifies no I-addresses (M'(d) and M(d) share the same value set, only repositioned)."
**Problem**: "No I-addresses are modified / same value set" does not establish that the reassembled run (π(vⱼ), aⱼ, nⱼ) has I-start aⱼ. What is required is M'(d)(π(vⱼ)) = aⱼ. Preserving the *set* of I-address values says nothing about which V-position now carries aⱼ — if π(vⱼ) mapped to a different value, the I-start would change despite no value being modified. The actual reason is the permutation defining property M'(d)(π(vⱼ)) = M(d)(vⱼ) = aⱼ, which is in fact supplied in the very next paragraph ("The second equality uses the permutation defining property"). So the stated reason is insufficient and is superseded a sentence later.
**Required**: Drop the "same value set, only repositioned" justification and ground the I-start on the permutation property M'(d)(π(vⱼ)) = M(d)(vⱼ) = aⱼ (i.e., cite the S8-cons derivation that immediately follows), or merge the two paragraphs so the I-start claim and its only valid justification sit together.

### Issue 2: Commutation/same-region discharge restated three times in R-BLK Phase 3
**ASN-0084, R-BLK, Phase 3**: the identity π(vⱼ + k) = π(vⱼ) + k and its same-region-precondition discharge appear in three consecutive sub-paragraphs — first the "*The commutation π(vₖ + k) = π(vₖ) + k holds trivially on non-S and exterior runs … supplied by R-COMM*" paragraph, then "*the same-region precondition of the identity π(vⱼ + k) = π(vⱼ) + k (established above) is discharged for each run*," then again under S8-cons ("*the first uses R-COMM*").
**Problem**: Per the anti-bloat mandate this is the same fact (with the same precondition discharge) re-stated across adjacent slots. A reader must verify the same R-COMM application three times to follow what is one lemma invocation feeding three conclusions (contiguity, width, S8-cons).
**Required**: Discharge the same-region precondition once for each post-split run (the runs lie in a single region by Phase 1/SUBCONF), then consume the resulting π(vⱼ + k) = π(vⱼ) + k identity without re-justifying its applicability in each downstream conclusion.

## OUT_OF_SCOPE

### Topic 1: Link-endset validity under rearrangement
The ASN scopes REARRANGE to the text subspace and passes subspace-2 (link) positions through untouched (Worked Example 6). Whether a link's endsets remain well-formed/discoverable after a text-subspace rearrangement is not addressed. Since C' = C and ran(M'(d)) = ran(M(d)), the I-addresses links reference are preserved, so nothing here is broken — but the explicit link-integrity guarantee belongs to the link model (a future/separate ASN), not this one.
**Why out of scope**: This is new territory (link semantics under arrangement mutation), not a defect in the cut-point rearrangement claims, which are self-contained over M(d) and C.

VERDICT: REVISE
