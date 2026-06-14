# Review of ASN-0131

The core proofs are sound. RE-NCD's prefix-relation/separator-zero argument, RE-ADDR's antichain-plus-unit-depth reasoning, RE-RET's sole-bearer biconditional (including the correct identification that the forward direction needs the `coverage(Θ) ∩ dom(Σ.C) = ∅` hypothesis precisely to handle a retracted type-Θ link's `(3, Θ)` pair being re-supplied by the fresh emitter `b`), RE-UDIST-∩'s twin counterexamples, and RE-CWP's weakest precondition all check out. The findings below are one underived consequence and two anti-bloat items (per the `review-mode.anti-bloat` classifier).

## REVISE

### Issue 1: RE-UDIST's decisive bearing on Open Question 1 is proved-but-underived

**ASN-0131, §Extent / §Composing regions / RE-UDIST**: The note proves `RE(W₁ ∪ W₂, d, Σ) = RE(W₁, d, Σ) ∪ RE(W₂, d, Σ)` (RE-UDIST) for the adopted whole-endset reading, and separately debates whole-endset (RE-WHOLE) vs. touching-spans-only (`RE_clip`) as Open Question 1. §Extent lists what survives the reading choice — "RE-CLIP and the shared selection (RE-OVL, soundness, completeness) stand firm under either answer" — but is silent on union-distributivity.

**Problem**: Union-distributivity is a property that *decisively distinguishes the two readings*, and the distinction is fully derivable from claims already in the ASN. Under the whole reading the returned value `e = Σ.L(a).eᵢ` is region-independent, so RE-UDIST holds (the proof factors `touch_W` over the disjunction). Under `RE_clip` the returned value `clip_W(Σ.L(a).eᵢ)` *is* region-dependent, and union-distributivity **fails**. The ASN's own RE-UDIST-∩ counterexample already supplies the witness: take the injective `Σ.M(d) = {[1,1] ↦ a, [1,2] ↦ b}` and endset `e = {(a, δ(1,#a)), (b, δ(1,#b))}`, with `W₁ = {[1,1]}`, `W₂ = {[1,2]}`. Then

- `RE_clip(W₁) = {(1, {(a,δ(1,#a))})}`, `RE_clip(W₂) = {(1, {(b,δ(1,#b))})}`,
- `RE_clip(W₁ ∪ W₂) = {(1, {(a,δ(1,#a)), (b,δ(1,#b))})}` (since `image(W₁∪W₂) = {a,b}` and both spans meet it),

so `RE_clip(W₁ ∪ W₂) ≠ RE_clip(W₁) ∪ RE_clip(W₂)`. The same construction shows even the `⊆` half of RE-UDIST-∩ fails for `RE_clip`. So the whole-endset reading uniquely yields the clean composition laws (RE-UDIST and the unconditional RE-UDIST-∩ `⊆` direction), and this is a stronger, fully algebraic argument for the adopted reading than the "where else this anchoring lives" faithfulness argument the ASN offers — yet the connection is never made, and a reader weighing OQ1 is left to rediscover it.

**Required**: Either derive the consequence explicitly — note that RE-UDIST (and RE-UDIST-∩'s `⊆` half) hold for whole-endset surfacing and fail for `RE_clip`, and surface it as a consideration bearing on OQ1 — or, at minimum, state plainly that RE-UDIST and RE-UDIST-∩ are *reading-dependent* (unlike the reading-invariant RE-CLIP/RE-OVL/RE-SND/RE-CMP that §Extent already enumerates), so the existing "stands under either answer" list is not misread as exhaustive of the proved properties.

### Issue 2: RE-NCD introduction enumerates its downstream consumers

**ASN-0131, §"When does an endset touch the region?"**: "One structural fact about *non-content* anchoring recurs below — in the worked instance (for a type endset) and in the retraction analysis (for a withdrawal's to-set) — so we record it once, in general form rather than inside either use."

**Problem**: This is the flagged "definition's introduction enumerates downstream consumers... rather than advancing the definition's meaning" pattern, compounded with placement justification ("record it once... rather than inside either use"). The lemma RE-NCD is load-bearing and well-stated; the framing sentence advances none of its content and is exactly the meta-prose a precise reader skips.

**Required**: Drop the consumer-inventory/placement sentence; state RE-NCD directly.

### Issue 3: prefix-antichain re-derived inline, then equated to a foundation lemma, behind scaffolding prose

**ASN-0131, §"Fresh emissions and the addressable population"**: A full paragraph re-derives that `dom(Σ.L)` is a prefix-antichain from ASN-0093 primitives (ChainMembershipForOrigin, T10a.1/T10a.2, CrossDocumentDisjointness, ChainPrefixExtension), closing with "This is the content of ASN-0086's R0a/FlatLinkDomain." The section is introduced with "Two consequences are all we use. First... Second..." and "Two further facts feed the addressability argument. The first is an *inventory*... The second is **structural**..."

**Problem**: The antichain is a foundation result (R0a, ASN-0086; equivalently ASN-0093's sub-allocator discipline). The re-grounding in ASN-0093 has a defensible purpose (R0a's stated scope is ASN-0086's `→`, narrower than ASN-0047's vocabulary), so the substantive step may stay — but spelling out the two-chain incomparability case-by-case when the cited ASN-0093 lemmas already deliver it, the trailing "This is the content of ASN-0086's R0a/FlatLinkDomain" cross-reference, and the "Two consequences are all we use" / "Two further facts feed the addressability argument / The first is an inventory... The second is structural" signposting are scaffolding the argument does not need. These are exactly the use-site-inventory / exhaustiveness-claim patterns the classifier targets.

**Required**: Compress the antichain establishment to a citation of ASN-0093's sub-allocator antichain (or R0a), drop the redundant trailing equivalence note, and cut the "Two consequences / Two further facts / inventory / structural" framing.

## OUT_OF_SCOPE

### Topic 1: Resolving OQ1 (committing to whole-endset vs. touching-spans-only)

**Why out of scope**: Issue 1 asks only that the *existing* RE-UDIST consequence and its reading-dependence be surfaced; it does not require the ASN to close OQ1. Choosing and proving one reading as canonical (against all of OQ1's faithfulness, rendering, and composition considerations) is legitimate future work.

### Topic 2: The deferred questions OQ2–OQ7

**Why out of scope**: Multiplicity preservation (OQ2), V-rendered answers (OQ3), the weakest structurally-restricted sufficient condition for intersection-equality (OQ4 — the necessary-and-sufficient touch-implication is already settled in-note), cross-store completeness (OQ5), type-slot matches against content (OQ6), and link-subspace regions (OQ7) are correctly posed as open questions, not as claims this ASN must discharge. No out-of-scope topic from the Scope list is defined as a claim.

VERDICT: REVISE
