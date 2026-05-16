# Review of ASN-0084

## REVISE

### Issue 1: R-WP label is structurally misleading

**ASN-0084, R-WP**: "*Label convention.* The label R-WP is retained as a stable identifier. The lemma establishes sufficiency only (one direction, ⇐): the conjunction below is sufficient for the post-state predicate, not necessarily equivalent to the weakest precondition."

**Problem**: A label conventionally read as "weakest precondition" is admitted to denote only a sufficient precondition. Retaining a misleading label "for stability" is the inverse of what stable names should do — encode meaning, not preserve confusion. Downstream consumers will reasonably assume R-WP characterizes wp(REARRANGE_C, Q); the ASN's own prose has to disclaim this in a label-convention paragraph.

**Required**: Rename to R-SP (SufficientPrecondition) or similar, with an inline cross-reference noting the prior identifier. Alternatively, prove the converse (necessity) for at least the load-bearing conjuncts and earn the R-WP label. The current necessity sketches handle R-PRE(iv) and (gestures at) R-PRE(iii), but R-PRE(i), R-PRE(ii) are dismissed as "well-typedness guards" without counterexamples — that gap is exactly the work R-WP would need to complete.

### Issue 2: PermutationDisplacement Δ has decorative arithmetic in Phase 3

**ASN-0084, R-BLK Phase 3 and Definition — PermutationDisplacement**: "We do *not* define addition, multiplication, or an ordering on the signed-magnitude carrier in this ASN"; yet Phase 3 of R-BLK is described as "α runs: V-start shifts by the α displacement" and the worked examples write "(α, V-start shifted +3)".

**Problem**: Δ is a signed magnitude with explicitly no defined arithmetic. The "shift by Δ" language in Phase 3 and the worked examples uses arithmetic that doesn't formally exist in this ASN. The operational tool is π (with contiguity from R-COMM); Δ is decorative. A reader trying to verify Phase 3 mechanically against the formal definition of Δ has nothing to evaluate.

**Required**: Either (a) state Phase 3 purely in terms of π — "the V-start of each subspace-S run is replaced by π(v_j), the I-start and width are preserved" — and demote Δ to commentary; or (b) define ordinal addition with a signed-magnitude on V-positions (carrier extension, well-typing the operations, identity with π under proven correspondence). Option (a) is the smaller change; the proofs already use R-COMM operationally.

### Issue 3: No worked example at the boundary

**ASN-0084, "Worked Example" sections**: All three worked examples use V_S(d) of size 5, 7, or 8.

**Problem**: The minimum admissible cases — V_S(d) of size 2 for n = 3 (w_α = w_β = 1, c_0 = [S, 1], c_2 = [S, 3]) and V_S(d) of size 3 for n = 4 (w_α = w_β = w_μ = 1, c_0 = [S, 1], c_3 = [S, 4]) — are exactly where region formulas could collapse. Likewise the empty-left-exterior case (c_0 = [S, 1]) and the empty-right-exterior case (c_{n−1} = [S, N + 1]) are discussed in prose ("Empty-exterior boundary cases") but never traced. Dijkstra: "showing the common case works does not establish that the edge cases do." The general arguments cover these, but no concrete verification exists.

**Required**: One worked example for the minimum-size n = 3 case and one for c_{n−1} = [S, N + 1] (empty right exterior). The latter is the harder boundary because the "Outside ⋃_k V(b_k)" branch of Phase 1 fires; tracing it explicitly against R-BLK would confirm the bookkeeping.

### Issue 4: R-PRE(v) "non-independence" argument is incomplete

**ASN-0084, "R-PRE(v) is non-independent"**: "R-PRE(v) (region widths w_α, w_β, w_μ ≥ 1) is logically implied by R-PRE(iii)... CS2's strict ordering c_i < c_{i+1} forces ord(c_{i+1}) − ord(c_i) ≥ 1 — i.e., each region width is at least 1."

**Problem**: The argument derives the ordinal-difference ≥ 1 from CS2. But R-PRE(v) as originally stated ("Every region is non-empty: w_α ≥ 1...") uses w_α = |α|, the V-position cardinality. Bridging from "ord(c_1) − ord(c_0) ≥ 1" to "|α| ≥ 1" requires R-PRE(iv) (which lifts every ordinal in [c_0, c_1) at depth 2 in subspace S into V_S(d)) plus D-SEQ. The argument as stated claims implication from R-PRE(iii) alone, when in fact it implicitly uses R-PRE(iv) and D-SEQ. Since both are also in the precondition the conclusion is correct, but the chain is misstated.

**Required**: Either restate as "R-PRE(v) is implied by R-PRE(iii) ∧ R-PRE(iv) (via D-SEQ)" and show both steps, or remove R-PRE(v) from the precondition list entirely and derive it as a stated consequence in the "Width-ordinal identities" paragraph.

### Issue 5: R-NS forward reference muddles dependency direction

**ASN-0084, R-NS**: "This lemma is stated here, immediately after the operation definition and before the bijection lemmas R-PPERM (3-cut) and R-SPERM (4-cut)... The proof of R-NS below invokes two results whose formal statement appears later in the ASN: R-PPERM (PivotPermutation) and R-SPERM (SwapPermutation), specifically the non-S branches of their piecewise definitions."

**Problem**: R-NS proves "π is the identity on non-S positions" by citing R-PPERM/R-SPERM's non-S branches. R-PPERM/R-SPERM proofs then cite R-NS(NS-π) for their own non-S cases. This is not technically circular — the non-S branch is *defined* (not derived) and R-NS just collects what R-FRAME-P(a) / R-FRAME-S(a) already say. But the ASN structures this as "R-NS depends on R-PPERM/R-SPERM" when in fact R-NS depends on R-FRAME-P(a)/R-FRAME-S(a) (frame conditions) together with the bare piecewise *definitions* of π, neither of which requires the well-definedness proofs of R-PPERM/R-SPERM. The current presentation creates the appearance of a tighter dependency than exists.

**Required**: Reframe R-NS as depending on R-FRAME-P(a), R-FRAME-S(a), and the non-S branch of the bijection definitions (which can be quoted directly from the operation contract before R-PPERM/R-SPERM are proved). The bijection lemmas then cite R-NS without circularity because R-NS no longer needs them. Alternatively, fold R-NS into R-PPERM and R-SPERM as the non-S sub-case of each proof.

## OUT_OF_SCOPE

### Topic 1: Composition of REARRANGE_C operations
**Why out of scope**: REARRANGE_C ∘ REARRANGE_C' need not be expressible as a single REARRANGE_C''; characterizing composable rearrangements is a future-ASN question. The ASN lists this in open questions.

### Topic 2: Cross-subspace transposition (link subspace V_2(d))
**Why out of scope**: REARRANGE_C is confined to S = 1 (text) at depth 2. The link subspace is preserved pointwise by R-FRAME-P(a)/R-FRAME-S(a). Link-rearrangement semantics belongs in a separate ASN.

### Topic 3: Documents with m_1 > 2 (text subspace at depth > 2)
**Why out of scope**: ValidFirstInsertionPosition leaves m_1 operator-chosen subject to m_1 ≥ 2; this ASN restricts to m_1 = 2. Generalizing to higher depths requires re-deriving the singleton-tumbler identification at depth m_1 − 1 ≥ 2.

### Topic 4: Necessity (full weakest precondition for Q)
**Why out of scope**: The ASN proves sufficiency only and explicitly defers necessity. The R-PRE(iv) and R-PRE(iii)/CS3 sketches indicate the shape of what a necessity proof would require but stop short.

### Topic 5: Characterizing pre-state runs that produce post-state mergeability
**Why out of scope**: The 4-cut worked example exhibits B + 2 = H causing a post-rearrangement merge; characterizing when this happens (in terms of pre-state I-address structure relative to region assignment) is a separate analysis the ASN explicitly defers.

### Topic 6: Validity of arbitrary cut positions relative to run boundaries
**Why out of scope**: CS1–CS4 and R-PRE(iv) together constrain cut positions, but whether tighter constraints (e.g., cuts must coincide with run boundaries) are necessary or natural is an open question.

VERDICT: REVISE
