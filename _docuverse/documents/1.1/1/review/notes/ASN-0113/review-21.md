# Review of ASN-0113

The mathematics is sound. I checked W4's exact-coverage derivation (T5 confinement plus half-open last-component bound), W5's contiguity iff (forward construction at the run's *actual* minimum via T0(a)+S8-fin+T5, converse via order-convexity with a concrete counterexample), W10/W11's first-component disjointness, and the boundary cases (allocated-empty → `⟨⟩`, unallocated → failure, single-occupied subspace, n_S = 1, depth-3 prefix-confinement). The worked instances genuinely exercise the non-trivial step (the depth-3 case excludes `[S,2,1]` with an admissible last component). No technical gap found.

The findings below are the anti-bloat patterns the `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: Defensive meta-prose commenting on a proof's adequacy
**ASN-0113, "Why text and links must be reported apart" (W11 derivation)**: "The SC-NEQ contradiction on the first component, under T1, suffices on its own."
**Problem**: This sentence does not advance the derivation — the two-line argument it follows (any `t` in the intersection needs `t₁ = s_C` and `t₁ = s_L` at once, impossible by SC-NEQ) already closes the claim. The trailing line only asserts that the just-given proof is sufficient. It is exactly the "defensive justification" the classifier names; a reader must skip it to reach the next claim.
**Required**: Delete the sentence. The preceding two lines stand alone.

### Issue 2: Cross-member independence claim restated several ways
**ASN-0113, W15 (Independence)**: "Independence is therefore a property of the *counts* — each read off its own subspace's positions — and the single-subspace edit is the conditional it yields: an edit confined to one subspace leaves the other's count untouched, since a content edit cannot alter `V_{s_L}(d)` and a link edit cannot alter `V_{s_C}(d)`. The link count can grow without altering the character count, and text can be inserted or deleted without altering the link count — the two members move independently."
**Problem**: The same proposition is stated three times in immediate succession — once as "a property of the counts," once as "the single-subspace edit ... leaves the other's count untouched," and once as "the link count can grow without altering the character count." This is the "two paragraphs say the same thing in different words" pattern. The formal claim plus the one-clause disjointness justification (`s_C ≠ s_L` makes the position sets disjoint, so the counts read non-overlapping data) carries the entire content.
**Required**: Collapse to the formal statement plus the disjoint-position-set justification; drop the two restatements.

### Issue 3: Precondition paragraph explains why-needed at length rather than stating the boundary
**ASN-0113, "The substrate we measure" (after W-pre)**: "This is necessary because only `Document(e)` events extend `dom(M)` ... for `d ∉ dom(M)`, `M(d)` is undefined, so `O(d)`, `V_S(d)`, `occupied(d)`, and every derived quantity below are *undefined* — not empty."
**Problem**: The operative object-level content is a single distinction — allocated-empty yields the defined `⟨⟩` (W0), unallocated is outside the domain and signals failure. The surrounding prose is a why-the-precondition-is-needed justification (the "explains why the axiom/precondition is needed rather than what it says" pattern), enumerating which derived quantities go undefined. The Gregory back-end sentence is legitimate implementation confirmation and should stay; the undefined-quantity enumeration is the part that does not advance the argument.
**Required**: State the allocated-empty/unallocated distinction directly (one sentence), retain the back-end confirmation, and drop the enumeration of derived quantities that "go undefined."

## OUT_OF_SCOPE

### Topic 1: Version-fork permanence, transclusion consistency, overall-extent agreement
The Open Questions defer per-subspace extent behavior across version forks, transclusion from an edited source, and consistency with any single overall extent the document exposes. These are correctly held out — they belong to future operations (version comparison, transclusion, RETRIEVEDOCVSPAN reconciliation), not to this query's contract. No action needed; they are already framed as questions, not claims.

VERDICT: REVISE
