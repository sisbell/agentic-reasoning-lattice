# Review of ASN-0112

The mathematics of this note is sound. I checked V1–V18, the two-case coverage proof (V2), the same-depth tightness argument (V3), the cross-subspace bounding-box claims (V5/V6), the empty-case typing of the wp predicates, and the worked examples (including the `m_C = 3 > m_L = 2` divergent variant). The D0/D1 round-trip case split holds, the reach biconditional is correctly proved in both directions, and the half-open coverage `max O(d) < r⋆` holds in both depth regimes. No correctness defects.

The findings below are prose accretion, which this review mode (`review-mode.anti-bloat`) directs me to surface.

## REVISE

### Issue 1: V8 parenthetical defends against a case its own hypothesis excludes
**ASN-0112, "The origin is permanent" / V8**: "(The depth `m_C` of this canonical value is itself fixed throughout — re-pinning is confined to full subspace clearance, which V18 accounts for; under V8's 'content present' hypothesis no clearance occurs.)"
**Problem**: V8's carrier hypothesis is "the content subspace is non-empty." The parenthetical raises full subspace clearance — a transition the hypothesis already excludes — only to say it does not occur here, and forward-references V18 for it. This matches two flagged accretion patterns at once: imagining a case the precondition rules out, and deferring to a downstream location. The load-bearing content (the depth is fixed within a content-present regime) survives without the clearance excursion.
**Required**: Reduce to the depth-fixed point alone, e.g. "(the depth `m_C` is fixed throughout any content-present regime, by S8-depth)"; drop the clearance/V18 deferral, which V18 already owns.

### Issue 2: Precondition section carries a defensive completeness justification
**ASN-0112, "Preconditions and well-definedness"**: "This single precondition is all the value semantics require; authorization is a deployment-level access gate outside the value semantics this ASN specifies."
**Problem**: The first clause asserts the precondition's own sufficiency (a defensive justification in a structural slot); the scope-fencing of authorization is the only part that informs the reader. The completeness assertion does not advance the argument.
**Required**: Keep the scope statement ("authorization is outside this note's value semantics"); drop "This single precondition is all the value semantics require."

### Issue 3: "⟨⟩ is not a T12 span" restated across V0, V11, and both table rows
**ASN-0112, V0 prose / V11 prose / table rows V0, V11**: V0 proves the summand distinctness via S2 ("no T12 span can denote ∅"); V11 re-asserts "the empty span-set ⟨⟩ ... which is *not* a T12 span"; both table rows repeat the parenthetical "(not a T12 span)".
**Problem**: The non-degeneracy of `⟨⟩` is established once in V0 by S2. V11's restatement of the same fact (its genuinely new content is the sentinel/TA6 point) and the duplicate table parentheticals are redundant carriers of one proved fact.
**Required**: State the distinctness once (V0). In V11 keep only the sentinel/TA6 material; in the V11 table row, cite V0 rather than re-asserting "not a T12 span."

## OUT_OF_SCOPE

### Topic 1: Per-subspace extent and the extent/count relation in the multi-subspace case
**Why out of scope**: Open Question 1 and per-subspace reporting belong to ASN-0113; the note correctly defers them rather than claiming an invariant it cannot supply with one span.

### Topic 2: Origin-as-document-identity vs. minimum-occupied-position
**Why out of scope**: Open Question 2 is genuinely new territory (relating the locator tumbler to the V-origin), not a gap in this boundary-query specification.

VERDICT: REVISE
