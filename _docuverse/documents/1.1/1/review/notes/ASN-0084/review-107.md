# Review of ASN-0084

I checked the arithmetic of all six worked examples, the well-definedness proofs (R-PIV, R-SWP), the permutation bijections (R-PPERM, R-SPERM), the commutation lemma (R-COMM), the run-transformation (R-BLK), and the canonicality argument (R-CANON). The core mathematics is sound: width positivity, tiling/exhaustiveness, displacement formulas, and the merge/canonical reasoning all hold, and the EXT-VAC boundary case is handled correctly. My findings are confined to accumulated meta-prose that the precise reader must work around.

## REVISE

### Issue 1: R-CANON states the "work at depth m, not depth 2" point three times
**ASN-0084, R-CANON**: The lemma makes the same framing remark in three places:
1. Preamble: "We first record facts used in both directions, stated at the actual depth of each run rather than only at the text subspace's depth 2 — B′ covers all of dom(M'(d)), so its runs may lie in subspaces other than S, which S8-depth (ASN-0036) permits to carry depths greater than 2."
2. Mid-paragraph: "within that subspace all V-positions share one depth m (S8-depth, ASN-0036) — for a non-text subspace m may exceed 2 — ..."
3. After the fact list: "Each determination below compares positions that share a common V-position and therefore a common subspace and depth, so these facts apply at that run's actual depth m, not only at depth 2."

**Problem**: Three sentences in one lemma carry the identical message ("the facts hold at the run's true depth m, which may exceed 2"). This is the "two paragraphs say the same thing in different words" pattern. The reader must reconcile three restatements of a single framing decision before reaching the actual forward/backward-extension arguments.

**Required**: State the depth-m framing once (the mid-paragraph form, where the facts are actually introduced, suffices) and delete the preamble sentence and the post-list restatement. The fact list itself carries the content.

### Issue 2: Run-decomposition preamble justifies *why* a foundation result applies rather than using it
**ASN-0084, "Correspondence-Run Decomposition Transformation," opening**: "Extended Associativity and its underlying TS3 (ShiftComposition, ASN-0034) hold for any tumbler in T irrespective of depth, so shift acts on I-addresses identically to V-positions."

**Problem**: This is an "explains why X applies" justification rather than object-level content. The preceding clause already establishes that `+` on an I-address `a_s` denotes `shift(a_s, k)`; that, plus the fact that TS3/Extended Associativity are stated over all of T, is all the Split/Merge proofs invoke. The added sentence re-licenses foundation results that are already foundation results, which is the kind of defensive meta-prose that compounds across cycles.

**Required**: Drop the sentence. If a pointer is wanted, fold it into the prior clause as a parenthetical ("`shift(a_s, k)` per S8's run convention, valid at any depth"), without the standalone re-justification.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4 and composition of rearrangements
**Why out of scope**: The ASN deliberately restricts to n ∈ {3, 4} (CS1) and to a single REARRANGE_K transition. Generalization to k > 4 and the algebra of composed rearrangements is genuinely new territory, correctly parked in Open Questions rather than left as a gap in this ASN.

### Topic 2: Weakest-precondition characterization of REARRANGE_K
**Why out of scope**: The ASN establishes invariant *preservation* (R-RI plus the invariant-preservation audit) thoroughly; a full wp analysis of the post-state invariant suite Q is posed as an Open Question and does not undermine the operation definition or its proofs here.

VERDICT: REVISE
