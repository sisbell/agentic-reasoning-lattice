# Review of ASN-0102

The core argument is sound. I checked the displacement tiling (X16), the wp-reduction of S3★ to the copied region, the run-fragmentation/merge reasoning (X8, X11, X12), the self-transclusion pre-state pinning, and the coupling discharge (X14) against the worked examples. The boundary cases — append (`p = n_S+1`), empty subspace (`n_S = 0`), self-transclusion overlapping the displaced region, and the coalescing copy — are each instantiated concretely and the postconditions check out. No correctness defect found.

The findings below are accretion of meta-prose around forward references, which this note's `review-mode.anti-bloat` classifier asks me to surface at source.

## REVISE

### Issue 1: Downstream-consumer enumeration in the resolution section
**ASN-0102, "The source designation and its resolution"**: "The downstream claims X10(b) and X15 invoke this fact rather than re-establish it."
**Problem**: This sentence is a use-site inventory — it names which downstream claims consume the pre-state pinning without advancing the pinning's meaning. It is exactly the "definition's introduction enumerates downstream consumers" pattern. A reader following the resolution argument must skip past it.
**Required**: Delete the sentence. The pinning stands on its own; consumers cite it where they need it.

### Issue 2: Pre-state pinning re-stated across three sections
**ASN-0102, resolution section / X10(b) / worked example**:
- resolution: "This single pre-state pinning is what makes self-transclusion (`d_s = d`) well-defined"
- X10(b): "established once in the resolution section ... The atomicity of COPY (X15) is what makes that pinning a single indivisible read."
- worked example: "**Why X10(b)/X15 are load-bearing here.**"

**Problem**: The same load-bearing fact (resolution reads `Σ.M(d)` before displacement) is asserted in the resolution section, restated and back-pointed in X10(b), and framed a third time in the self-transclusion example. This is the "multiple paragraphs in different sections defer to the same location" plus "two paragraphs say the same thing in different words" pattern. The *concrete counterfactual computation* in the worked example (`[1,3]` would hold `x_2`, yielding a circular result) is legitimate and should stay; the surrounding framing prose and the X10(b) back-pointer are the redundancy.
**Required**: State the pinning once in the resolution section. In X10(b) state only the property ("for `d_s = d`, the target-as-source is read at the pre-state and is itself displaced") without "established once in" / "what makes that pinning indivisible." Keep the worked example's computation, drop its motivational framing.

### Issue 3: X15 consequence-inventory and excluded-case reasoning
**ASN-0102, X15**: "COPY either applies in full — establishing X1, X3, X7, S2, S3★, and the subspace's density discipline D-SEQ (X16) together — or not at all" and "A partial application would leave `Σ'.M(d)` either non-dense (a V-gap, contradicting X16) or double-bound ..."
**Problem**: The first clause is a consequence inventory inside the claim statement — atomicity does not establish those claims, it applies whichever transition establishes them. The "A partial application would leave ..." sentence reasons about an intermediate state that the claim's carrier (a single elementary transition under SequentialTransitionAxiom) already forecloses — the "paragraph imagines a case the precondition already excludes" pattern.
**Required**: State X15 as: COPY is a single elementary transition (SequentialTransitionAxiom), so precondition-read and effect-commit are one indivisible step with no observable intermediate. Drop the X1/X3/X7/... inventory and the hypothetical partial-state paragraph.

## OUT_OF_SCOPE

The four Open Questions (re-displacement and discoverability, transitive containment, time-varying views, identity under unreachable allocators) are correctly posed as future work, not gaps in this ASN.

VERDICT: REVISE
