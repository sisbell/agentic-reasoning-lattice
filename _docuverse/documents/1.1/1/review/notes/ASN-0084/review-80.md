# Review of ASN-0084

I checked the cut-point arithmetic, the pivot/swap postconditions, the bijection lemmas (R-PPERM, R-SPERM), the well-definedness proofs (R-PIV, R-SWP), the invariant-preservation audit, and traced all six worked examples against the explicit formulas. The mathematics is sound: the region tiling closes, the displacement arithmetic is correct, S8 is properly re-derived for the post-state, and the boundary cases (empty exteriors, w_α=w_β=1, the three μ sub-cases, non-S pass-through) are each exercised concretely. The issues below are structural — a forward-reference dependency the anti-bloat classifier asks me to surface.

## REVISE

### Issue 1: R-PIV / R-SWP cite R-NS for a fact that needs only the frame condition, importing an unnecessary forward reference

**ASN-0084, "Postcondition Well-Definedness" (R-PIV and R-SWP proofs)**: "For v ∈ dom(M(d)) with subspace(v) ≠ S: R-NS(NS-π) (equivalently R-FRAME-P(a)) assigns M'(d)(v) = M(d)(v)…"

**Problem**: R-PIV and R-SWP only need the value fact `M'(d)(v) = M(d)(v)` on non-S positions — which is exactly R-FRAME-P(a) / R-FRAME-S(a), as the parenthetical "(equivalently …)" concedes. But they cite R-NS instead. R-NS additionally asserts `π(v) = v`, and its *statement* opens "Let π be the cut-point-induced bijection (R-PPERM for n = 3, R-SPERM for n = 4)" — definitions that appear two sections *later* and that themselves cite R-NS in their proofs. So R-PIV/R-SWP (which establish that M'(d) is a function, a fact logically prior to π even existing) are made to depend, via R-NS, on the permutation lemmas downstream. The well-definedness of the post-state arrangement should not reach forward to the bijection that is built on top of it. This is the forward-reference tangle the note is being watched for: the indirection layer (every non-S step routes through `R-NS(NS-π)`) is what carries the forward dependency.

**Required**: In R-PIV and R-SWP cite R-FRAME-P(a) / R-FRAME-S(a) directly for the non-S value fact; drop the R-NS citation there. Reserve R-NS (which legitimately bundles `π(v) = v`) for the lemmas where π actually exists and the identity-on-π claim is used — R-PPERM, R-SPERM, R-COMM, R-BLK.

### Issue 2: R-COMM proves a non-S (and subspace-S exterior) case that no consumer uses

**ASN-0084, "Correspondence-Run Decomposition Transformation" (R-COMM)**: the lemma's region list includes "the non-S subspace … the subspace-S exterior," and the proof discharges both ("*Non-S subspace (both forms):* … π(v + k) = v + k = π(v) + k"; "*Subspace-S exterior (both forms):* …").

**Problem**: R-COMM's only consumer is R-BLK Phase 3, and there the non-S and exterior runs are handled directly by the identity ("For non-S runs π is the identity (R-NS(NS-π)) and the run passes through unchanged"; "Exterior runs: π(vₖ) = vₖ by the subspace-S exterior clause"). The contiguity/`S8-cons` argument that actually invokes R-COMM is needed only for the α/μ/β runs, where π applies a non-trivial uniform displacement. The non-S and exterior branches of R-COMM are proven but never consumed — decorative completeness that widens the lemma without serving a downstream claim.

**Required**: Either restrict R-COMM's statement to the displaced regions (α, μ, β) that consume it, or add one sentence at the consumption site (R-BLK Phase 3) noting that R-COMM is what licenses identity-commutation on the fixed regions, so the proven cases are not orphaned.

## OUT_OF_SCOPE

### Topic 1: Generalization beyond the depth-2 (m₁ = 2) text subspace
**Why out of scope**: The note scopes itself to m₁ = 2 so that ord(v) is a singleton identifiable with ℕ⁺, on which the width/displacement arithmetic is built. Lifting to m₁ > 2 requires the ordinal arithmetic to be redone over multi-component ordinals — genuinely new machinery, correctly deferred. (The Open Questions already flag the k > 4 and composition generalizations.)

### Topic 2: Weakest-precondition characterization of REARRANGE_K
**Why out of scope**: The note verifies the forward direction thoroughly (R-PRE ⟹ postcondition ⟹ invariant suite, via the preservation audit). The wp question — what R-PRE(iv) adds beyond D-SEQ — is explicitly listed as open and is a refinement, not a gap in the present claims.

VERDICT: REVISE
