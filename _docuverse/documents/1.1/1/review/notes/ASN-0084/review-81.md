# Review of ASN-0084

The mathematics here is careful and the worked examples are thorough — coverage/exhaustiveness in R-PIV, R-SWP, R-PPERM, R-SPERM, and the width-positivity alignment all hold up, and the four μ-displacement sub-cases (forward, fixed, backward) plus the empty-exterior boundary are each exercised against concrete values. My findings are confined to the meta-prose accretion the `review-mode.anti-bloat` classifier asks me to surface; the proofs themselves do not have a correctness gap I can identify.

## REVISE

### Issue 1: Duplicated citation-rationale meta-prose in R-PIV and R-SWP
**ASN-0084, R-PIV and R-SWP proofs**: "Only the value fact M'(d)(v) = M(d)(v) is needed here — well-definedness of M'(d) is logically prior to the cut-point-induced bijection π, so we cite the frame condition directly rather than R-NS."
**Problem**: This sentence justifies *why one citation is used instead of another* rather than advancing the proof, and it appears verbatim in both lemmas. It is exactly the "defensive justification" / duplicated-prose pattern. A reader following the well-definedness argument must skip past it.
**Required**: Delete the clause in both proofs. Cite R-FRAME-P(a) / R-FRAME-S(a) for the non-S value and move on; no explanation of the R-NS non-choice is needed.

### Issue 2: Use-site inventory in R-BLK Phase 3
**ASN-0084, R-BLK Phase 3 (Reassemble)**: "...the same identity-commutation π(vₖ + k) = vₖ + k = π(vₖ) + k there that its α/μ/β cases supply on the displaced regions; this is where those two fixed-region cases of R-COMM are consumed."
**Problem**: The trailing clause "this is where those two fixed-region cases of R-COMM are consumed" is a use-site inventory (consumption-tracking), not reasoning. Worse, the citation is over-engineered: on non-S and exterior runs π is the identity (already established by R-NS(NS-π) one bullet earlier), so width preservation is immediate — invoking R-COMM's fixed cases adds nothing.
**Required**: Remove the consumption clause. For non-S/exterior runs, state width preservation directly from "π is the identity" and reserve R-COMM for the displaced (α/μ/β) runs where it does work.

### Issue 3: Meta-labeling in the invariant-preservation audit
**ASN-0084, Invariant preservation**: "S3 (referential integrity) is precisely the postcondition of R-RI above — ran(M'(d)) ⊆ dom(C') — so R-RI is the S3-preservation step of this invariant audit."
**Problem**: The final clause restates, in audit-bookkeeping terms, what the first half of the sentence already says. It is a label on a step rather than a step.
**Required**: End the sentence at "ran(M'(d)) ⊆ dom(C')."

### Issue 4: Triplicated empty-right-exterior reasoning
**ASN-0084, "Consequences of R-PRE / Empty-exterior boundary cases"** and **R-BLK Phase 1 step (3)**: both derive that when `ord(c_{n−1}) = N+1` (resp. `c_{n−1} > max(V_S(d))`) the right-exterior subset `{v ∈ V_S(d) : v ≥ c_{n−1}}` is empty, in nearly identical words; the dedicated boundary worked example then demonstrates it a third time.
**Problem**: The same fact is established abstractly in two separate sections. The R-PRE consequence and the R-BLK Phase 1 derivation say the same thing differently.
**Required**: Establish empty-exterior vacuity once (the R-PRE consequences paragraph is the natural home) and have R-BLK Phase 1 cite it rather than re-deriving `> N`. The worked example may keep its concrete trace.

## OUT_OF_SCOPE

### Topic 1: Generalization beyond depth m₁ = 2
The note restricts the text subspace to the minimum depth m₁ = 2, which underwrites the singleton-tumbler/ℕ identification carrying all width arithmetic. Lifting REARRANGE_K to m₁ > 2 (where ordinals are multi-component tumblers) is genuinely new territory, not a defect here.
**Why out of scope**: The depth-2 restriction is declared scope, and the arithmetic is sound within it; generalization needs its own ordinal-difference machinery.

### Topic 2: k-cut rearrangements and composition closure
The Open Questions already name these (k > 4 cuts; whether composition of two rearrangements is a single rearrangement).
**Why out of scope**: These are forward directions, correctly parked.

VERDICT: REVISE
