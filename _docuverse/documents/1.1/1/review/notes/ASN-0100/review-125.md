# Review of ASN-0100

I checked the substrate decomposition, every invariant discharge, the closed-interval reduction, the I3 coincidence, the projection-shift derivation, the wp computations, and all six worked examples. The correctness argument is sound: edge cases (empty, append, prepend, interior, deep-subspace `m_C=3`, re-insertion into a cleared subspace) are covered, the K.μ⁻ omission/strict-contraction logic is correct, foundation citations are foundation-only (rule 7 satisfied), and I found no hand-waves or skipped invariant conjuncts. The findings below are bloat/clarity only.

## REVISE

### Issue 1: I3-coincidence setup restated four times
**ASN-0100, §Effect Three through §Post-state V-position well-formedness**: the clause "`M'(d) ↾ (Left ∪ Shifted-right)` is pointwise [identical to] the I3-specified arrangement" is established once in §Effect Three (INS.I3-coincide) and then re-stated verbatim-in-substance at each of: §S2 ("so its internal functionality is exactly I3-S2"), §S3★ ("whose referential integrity is I3-S3"), §S8a ("inherit both: I3-VP… and I3-VD"), and §S8-fin ("applicable… via INS.I3-coincide").
**Problem**: four lead-ins re-erect the same coincidence scaffolding before each property discharge — the "say the same thing in different words" pattern. A reader re-parses the identical premise four times.
**Required**: state once (e.g., at INS.I3-coincide) that on Left ∪ Shifted-right `M'(d)` coincides with the I3 arrangement and therefore inherits I3-S2, I3-S3, I3-VP, I3-VD, I3-fin on those regions; then each verification section cites the inherited lemma directly without rebuilding the premise.

### Issue 2: Claims-table cells carry essay-length proof content
**ASN-0100, Claims Introduced**: the cells for INS.pre, INS.alloc, INS.proj, and INS.atomicity are multi-clause paragraphs that reproduce material already proved in §The Operation's Inputs, §Effect One, and §Verifying the Invariants (INS.pre's cell, for instance, re-unpacks both ValidInsertionPosition and ValidFirstInsertionPosition in full).
**Problem**: a claims index is a structural slot for terse statements; reproducing the precondition/derivation prose duplicates the body and inflates the table past its summarizing function.
**Required**: reduce these cells to the claim statement plus its label; leave the unpacking in the body where it is already given.

## OUT_OF_SCOPE

(none — the note's §Bounding the Scope correctly defers DELETE/COPY/REARRANGE, link-subspace insertion, versioning, and replication.)

VERDICT: REVISE
