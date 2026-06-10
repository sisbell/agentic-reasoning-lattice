# Review of ASN-0119

The mathematics is sound. I checked every introduced claim against its imported support and against the two worked examples, and found no correctness error: P0–P2 import cleanly from ASN-0084 (R-FRAME-P/S, R-RI, R-PIV/R-SWP); S3★ is correctly derived through `π⁻¹` (each subspace mapped onto itself); P7a's inline biconditional is valid and its avoidance of LP11 is well-justified (a symmetric-content REARRANGE yields `M'(d) = M(d)`, failing K.μ~'s non-triviality clause); the pivot/swap arithmetic, the four R-COMM region constants, the middle-displacement `w_β − w_α`, and the P8a/P8b two-move composite all check out numerically. Edge cases (empty subspace, single position, `c₀ = min`, whole-run interval, zero-width region) are handled as domain or vacuous-branch cases. This is a strong, deep note.

The findings below are the accreted meta-prose and structural duplication the `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: Redundant framing and a tautological "characterization" in the footprint-contiguity discussion
**ASN-0119, Links section**: The paragraph "*Fragmentation requires straddling, but straddling does not force it.*" — "This is all the structure entitles us to claim, and it is exactly P7c read contrapositively ... We claim nothing stronger about the kind of straddle — in particular not that the run must cover a partial block. ... so does any sharper necessity condition."

**Problem**: This paragraph carries no content beyond what two neighbours already establish. "Straddling does not force it" is the same proposition as the earlier paragraph "*Confinement is not necessary (a straddling footprint can stay contiguous).*" "Fragmentation requires straddling" is P7c's contrapositive, already in hand. What remains is meta-commentary about claim scope ("all the structure entitles us to claim," "nothing stronger," "any sharper necessity condition") — the reader must skip past it to reach the geometric account. Worse, its disclaimer "not that the run must cover a partial block" is then re-made by Example B's own framing ("covering complete blocks ... yet it fragments"), so the paragraph pre-empts a point its own examples carry.

Separately, the sentence "The exact characterization is therefore geometric: a contiguous footprint survives as contiguous precisely when its image under π is again an interval" is tautological: by P7a the post-footprint *is* `π(F)`, so "is contiguous precisely when its image is an interval" reads "is contiguous precisely when it is contiguous." The genuine content is the configuration analysis that follows (within-region holds; exterior-meets-region fails); the framing sentence is empty.

**Required**: Delete the "Fragmentation requires straddling" paragraph; its mathematical content is P7c plus the preceding "not necessary" paragraph. Replace the tautological lead-in with the real criterion directly — the post-footprint is an interval exactly when `π` lays the footprint's region-pieces down adjacently, which holds within one region and across relocated regions that re-abut but fails when a fixed-exterior position sits beside a relocated one — and let the three examples (gain, exterior-break, partial-block) stand as the demonstration.

### Issue 2: The worked pivot is forward-referenced and partially recomputed before it is established
**ASN-0119, S7/S3★ section and Links section**: S3★ — "in the worked pivot below `M'([s_C,2]) = a₃` while `M([s_C,2]) = a₂`"; Links — "In the worked pivot below (`A B C D E ↦ A C D E B`) ... `π` sends `ord 2 ↦ ord 5` and `ord 5 ↦ ord 4`"; then the dedicated section **A worked transposition** sets the same pivot up from scratch ("Transpose the single-byte region `α = {B}` ... cuts `c₀ = [s_C, 2]`, `c₁ = [s_C, 3]`, `c₂ = [s_C, 6]`").

**Problem**: Two earlier sections defer to "the worked pivot below" and consume its specific ordinals and `π`-values inline, before the worked-transposition section establishes them. The reader either jumps ahead or trusts the values on faith, and the pivot's setup ends up scattered across three locations with the `π`-table effectively computed twice (once in Links, once in section 10). This is the forward-reference-to-a-single-downstream-location pattern.

**Required**: Move the worked transposition (at least the pivot setup and its `π` table) before the sections that depend on it, so S3★ and the Links examples cite an already-established example rather than forward-referencing it; or merge the Links footprint examples into the worked-transposition section. Either removes both forward references and the duplicated computation.

### Issue 3: The third "ordering invariant" in Atomicity is interpretation, not reasoning
**ASN-0119, Atomicity section**: "Third, the operation treats both regions as moving relative to each other. There is no privileged stationary block; position is relational, defined by neighbours rather than by an absolute index, and what survives the swap is connectivity (P6), not any region's claim to have stayed put."

**Problem**: The first two atomicity points yield formal content (P8a/P8b; the single-frame cut resolution). The third yields none — it restates P6 in interpretive language and philosophizes about position semantics. It is essay content occupying a structural slot that the section otherwise reserves for the three invariants the atomic form exposes.

**Required**: Cut the third point, or reduce it to the one operational fact it actually states (no region is privileged; both displacements are computed against the same pre-state frame), which the second point already covers.

## OUT_OF_SCOPE

### Topic 1: Rearrangement outside the imported scope
**Why out of scope**: Reordering link-subspace V-positions, positions at depth `> 2`, and cut counts `n > 4` are all beyond ASN-0084's REARRANGE_K (CS1/CS3/CS4 fix `n ∈ {3,4}`, `S = 1`, depth 2). The note correctly confines itself; these are future territory, not gaps here.

### Topic 2: The note's own Open Questions
**Why out of scope**: Transclusion-shared cuts, unserialized concurrent rearrangement, the content-index/fragmentation invariant, prior-arrangement recoverability, and subspace-boundary preservation are appropriately deferred — each is a new operation or cross-operation guarantee, not a defect in this ASN.

VERDICT: REVISE
