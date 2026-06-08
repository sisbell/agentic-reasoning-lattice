# Review of ASN-0113

The mathematics is sound. I checked W4 (T5 confinement of the half-open interval to the canonical prefix, then last-component pinning), W5 (forward direction builds the span at the run's *actual* minimum, using T0(a)+S8-fin to force a shared prefix; converse via T12 order-convexity), W10/W11 (first-component confinement under T1 + SC-NEQ), and the three worked instances (depth-2 degenerate, one-member, depth-3 non-vacuous prefix-confinement). All hold. The precondition discipline (W-pre, allocated-empty vs. unallocated) is correctly maintained throughout. No correctness or missing-edge-case defects.

The findings below are anti-bloat / redundancy issues, which this note's `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: W18 and W19 state the same permanence fact twice
**ASN-0113, "Permanence of the report" (W18, W19)**: W18 — "any two queries against the *same* `Σ` return identical span-sets, and any query against a *changed* `Σ` may legitimately differ." W19 — "against an unchanged state `Σ`, repeated queries return identical span-sets; a later report contradicts an earlier one only if `M(d)` changed in between."
**Problem**: These are the same proposition in different words. "Same Σ → identical result" (W18) and "unchanged state → identical / changes only if M(d) changed" (W19) carry one content. W19's only genuine additions over W18 are the M(d)-granularity and the home-links remark; the core stability statement is duplicated across two adjacent claims.
**Required**: Merge into one claim. Keep the pure-function statement (W18 from W8) and fold W19's M(d)-granularity and home-links (CL-OWN) remarks into it; drop the duplicated "repeated queries return identical span-sets" sentence.

### Issue 2: W5's stated conclusion contradicts Open Question 1
**ASN-0113, W5 / Open Questions**: W5 concludes "Faithful reporting then requires a *span-set* within the single subspace, one member per contiguous cluster." Open Question 1 then asks "must the per-subspace report fragment into one span per contiguous cluster, or may it return a single bounding span that overshoots interior gaps?"
**Problem**: W5 already takes the position that faithful reporting *requires* fragmentation (citing Gregory's bounding-box behavior as the unfaithful alternative), yet Open Question 1 re-poses the identical question as undecided. A reader cannot tell whether the ASN has decided this or left it open. One of the two must yield.
**Required**: Either restate Open Question 1 to ask only what W5 leaves genuinely open (e.g., whether the *operation* should fragment or whether faithfulness is the caller's concern), or soften W5 from "requires" to a conditional statement and let the Open Question own the design decision. Do not assert and defer the same proposition.

### Issue 3: W-pre carries defensive meta-prose justifying the precondition
**ASN-0113, "The substrate we measure" (W-pre)**: "The distinction is sharp and must not be collapsed." … "All postconditions below are stated under W-pre; we make no claim about unallocated `d`."
**Problem**: "The distinction is sharp and must not be collapsed" is pure emphasis that advances no reasoning. "we make no claim about unallocated `d`" restates the scope already fixed by W-pre's "requires `d ∈ dom(M)`." This is the "prose around an axiom explains why it is needed rather than what it says" pattern: the empty-vs-unallocated point is already made once (empty yields ⟨⟩, unallocated is undefined); the surrounding emphasis is accretion.
**Required**: State the precondition and the empty-vs-unallocated distinction once. Drop the emphatic and the scope-restating sentences.

### Issue 4: W12 interpretive taxonomy is essay content
**ASN-0113, "What the pair reveals that neither member alone could"**: "high text with near-zero links is original prose; near-zero text with high link count is a purely connective document — a link-set, an annotation layer; both substantial is a compound collage."
**Problem**: This sentence classifies documents by profile but advances no part of the formal claim. W12's content — that neither projection is injective, with the reachability witness — is fully established without it. The taxonomy is color, not reasoning.
**Required**: Remove the taxonomy sentence; the witness construction is the substance of W12.

## OUT_OF_SCOPE

None. The Open Questions touch version forks, transclusion, and consistency with the single overall extent (ASN-0112), but they are posed as open questions, not claims, so no out-of-scope claim is asserted (see Issue 2 for the one Open Question that conflicts with a claim).

VERDICT: REVISE
