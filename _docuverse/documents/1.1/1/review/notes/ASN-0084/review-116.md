# Review of ASN-0084

I traced all five worked examples, checked the displacement arithmetic in every μ sub-case, verified the π formulas against the R-P*/R-S* clauses, and audited the well-definedness, permutation, R-BLK, and R-CANON proofs. The mathematics is sound and the case coverage (forward/fixed/backward μ, empty exteriors, non-S pass-through, minimum widths) is genuinely thorough. The findings below are about accreted meta-prose and one precision mismatch — not about correctness.

## REVISE

### Issue 1: Single-region containment is asserted twice with the same justification

**ASN-0084, R-BLK, Phase 2 (Classify) and "Same-region discharge of the commutation identity"**:

Phase 2: "Each run in the post-split partition lies entirely within one region ... because no run crosses a cut boundary (subspace-S runs are split at S-subspace cuts, and non-S runs are entirely contained in their subspace, shown above)."

Same-region discharge: "After Phase 1, every post-split run lies entirely within a single region — subspace-S runs by the split-at-cuts construction, non-S runs by the subspace confinement shown above — so each run ... satisfies the same-region precondition..."

**Problem**: Both paragraphs establish the identical claim ("every post-split run lies in one region") with the identical justification ("split at cuts; non-S by subspace confinement"). The second paragraph's only new content is the discharge of R-COMM's precondition and the trivial/non-trivial split. A reader following the S8-cons derivation must re-read a conclusion already proven one phase earlier. This is the flagged "two paragraphs say the same thing in different words" pattern.

**Required**: In the Same-region discharge paragraph, cite Phase 2's containment conclusion rather than re-deriving it; keep only the new step (each run meets R-COMM's same-region precondition; trivial on non-S/exterior, R-COMM on α/μ/β).

### Issue 2: R-COMM's region list is inconsistent with the partition used to invoke it

**ASN-0084, R-COMM statement vs. R-BLK Phase 2 / displacement formulas**: R-COMM enumerates the regions as "the non-S subspace ..., the subspace-S exterior, α, μ, or β" — treating the subspace-S exterior as one region. R-BLK Phase 2 and the permutation formulas instead distinguish "exterior left" (`v < c₀`) and "exterior right" (`v ≥ c_{n−1}`), two disconnected intervals.

**Problem**: When the Same-region discharge invokes R-COMM on an exterior-left or exterior-right run, the run's region (per Phase 2) is not literally one of R-COMM's named regions; the reader must silently identify "exterior left/right" with R-COMM's combined "subspace-S exterior." The identity holds (π is the identity on both pieces), so this is a precision gap, not a soundness gap — but the two taxonomies should match verbatim so the discharge cites a region R-COMM actually names.

**Required**: Reconcile the two region lists — either have R-COMM enumerate exterior-left and exterior-right separately, or have Phase 2 and the discharge refer to a single "subspace-S exterior" region consistently.

## OUT_OF_SCOPE

### Topic 1: Weakest-precondition analysis for the post-state invariant suite Q
The ASN proves invariant preservation in the forward direction (each ASN-0036 invariant maintained) and defers wp to the final open question. Computing the weakest precondition for REARRANGE_K to establish Q is a natural next step but is legitimately separable from introducing the operation and its bijection.

### Topic 2: Generalization to k-cut rearrangements (k > 4) and composition of rearrangements
The first two open questions (k > 4 cut classes; whether a composition of rearrangements is itself a single rearrangement) are new territory, not gaps in the pivot/swap treatment.

VERDICT: REVISE
