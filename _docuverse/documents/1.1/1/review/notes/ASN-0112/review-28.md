# Review of ASN-0112

The mathematics is sound. I checked V2's covering argument in both depth regimes (D1 closes the round-trip when `#origin_d ≤ #reach_d`; D0 forces `reach_d < r⋆` via a proper-prefix overshoot when `#origin_d > #reach_d`), verified the worked example and the depth-divergent variant compute as stated, and confirmed V3's tightness rests correctly on `sig(w) = #w` (S8a) so `shift(w,1) = inc(w,0)`. The note has a concrete example, a non-trivial wp analysis, and derived consequences — the depth requirements are met.

The findings below are all anti-bloat (the note carries `review-mode.anti-bloat`): accreted meta-prose and duplicated justification.

## REVISE

### Issue 1: Duplicated empty-case well-typedness justification in the wp section
**ASN-0112, Preconditions and well-definedness**: For `Exact`: "so `Exact` holds vacuously on the empty result `⟨⟩`, where there is no `σ_d` and `⟦σ_d⟧` would be ill-typed, and the predicate is well-typed over the whole `Span + {⟨⟩}` codomain." For `ReachTight`: "vacuous on the empty result `⟨⟩` (where `reach(σ_d)` and `#origin_d` are undefined, so the bare equality would be ill-typed) and hence well-typed over the whole `Span + {⟨⟩}` codomain."
**Problem**: The same well-typedness move (empty result → vacuous → well-typed over `Span + {⟨⟩}`) is spelled out twice in near-identical words. This is the "two paragraphs say the same thing in different words" pattern. The reader has already absorbed the vacuity convention from the first instance.
**Required**: State the empty-result vacuity convention once for both distinguished predicates, then define `Exact` and `ReachTight` without re-litigating well-typedness.

### Issue 2: Self-restating sentence in V4
**ASN-0112, "The Vstream is what we measure"**: "The extent measures *what the arrangement currently contains*, not *what the store has ever held*: it accounts only for the content presently belonging to the document, not for all content it ever held."
**Problem**: The clause after the colon restates the clause before it ("currently contains, not ever held" = "presently belonging, not ever held"). Both halves carry the identical contrast.
**Required**: Drop one half.

### Issue 3: Forward-reference / out-of-scope inventory embedded in a structural slot
**ASN-0112, "The substrate we measure"**: "We measure the whole document as one span; per-subspace reporting, content delivery, and region reads are out of scope, as is the reach-arithmetic of how each edit moves `max O(d)` — that belongs to INSERT and DELETE, not this query."
**Problem**: This is a use-site/scope inventory deferring to downstream operations, planted inside the foundation-facts list that should be advancing the substrate definition. It also duplicates the note's own Scope section. The deferral ("belongs to INSERT and DELETE") adds no reasoning the claims need.
**Required**: Remove the inventory; the Scope section already carries the exclusions.

### Issue 4: Result type fixed in prose, then immediately re-fixed in V0
**ASN-0112, "What the caller must be handed"**: "We therefore fix the result type *once and explicitly* as the tagged union `RETRIEVEDOCVSPAN : dom(M) → Span + {⟨⟩}` ... We record this as **V0** (span-or-empty result): for a non-empty document `RETRIEVEDOCVSPAN(d)` returns one well-formed span ..."
**Problem**: The signature and its meaning are stated in the prose sentence, then restated in full as V0 in the same paragraph — "once and explicitly" is followed by a second explicit statement. The two-summand-distinctness remark and the V0 record cover the same ground.
**Required**: Let the prose introduce the intent and V0 carry the formal statement, without restating the full signature in both.

## OUT_OF_SCOPE

The five Open Questions (multi-subspace extent/count invariant, origin-as-identity coincidence, historical-version faithfulness, run-composition of the global span, out-of-range addressing arithmetic) are correctly deferred — each is genuine future territory, not a gap in this query's value semantics. No action needed.

VERDICT: REVISE
