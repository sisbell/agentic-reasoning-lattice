# Review of ASN-0091

This is a rigorous, well-structured note. The abstract Vstream-only class is cleanly separated from the REARRANGE_K realisation, the RE-* derivations correctly cite abstract vs. concrete vs. structural provenance, the degenerate cases (empty, identity, net-effect collapse) are each handled, and the six worked examples each exercise a distinct mechanism with values that check out. I could not find a rigor gap in the core derivations. The remaining issues are anti-bloat prose, which the `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: Defensive closers in worked examples justify the example rather than advance it
**ASN-0091, Worked Example (basic) and Worked Example — Net-Effect Collapse**:
- "Every derived claim holds at the concrete level; **no two derived claims conflict at any point of the trace.**"
- "The collapse branch is thus a witnessed instance, **not an unexhibited appeal.**"

**Problem**: Both trailing clauses are defensive meta-prose. Once each RE-* claim is individually verified against concrete values, "no two derived claims conflict" asserts nothing checkable and adds no reasoning — claims that are each true cannot conflict. "not an unexhibited appeal" justifies the example's existence rather than stating a fact about the trace. These are exactly the skippable assurances the anti-bloat pass targets: a reader following the verification must step past them.
**Required**: Delete the defensive clauses; end each worked example on its last verified claim.

### Issue 2: Multi-step `RE-frag★/coal★/eq★` is double-presented in prose and the ★ table
**ASN-0091, "Composition Across Multi-Step REARRANGE Sequences" and the second Claims Introduced table**: The prose paragraph ("**RE-frag★ / RE-coal★ / RE-eq★** ... Construction by spatial partitioning: choose `n` pairwise-disjoint content-subspace sub-ranges ... at step `i` apply REARRANGE_K confined to the i-th sub-range. RE-ext preserves every other sub-range pointwise...") and the table row ("...the concatenation construction (spatial partitioning into disjoint sub-ranges with RE-ext bridging between steps) supplies the per-step realisability") state the same construction at the same level of detail.

**Problem**: The first Claims Introduced table earns its place as a terse one-line summary of claims derived at length in prose (different granularity). The ★ section breaks that discipline: the per-★ prose paragraphs (RE-other★, RE-ext★, RE-trans★, RE-frag★/coal★/eq★) and the table's "Composition Conditions" column carry the substantive conditions at comparable detail — two presentations of the same content.
**Required**: Keep the conditions in one place (the prose derivations) and reduce the ★ table's "Composition Conditions" column to a back-reference, or vice versa.

## OUT_OF_SCOPE

### Topic 1: Same-source span reconstitution after a splitting cut; link-subspace rearrangement semantics
**Why out of scope**: The note correctly marks both as open questions ("Whether the two fragments *jointly reconstitute* the original source span ... is not established here"; link-subspace rearrangement semantics). These are future-ASN territory, not defects here, and are appropriately confined to the Open Questions section rather than claimed.

VERDICT: REVISE
