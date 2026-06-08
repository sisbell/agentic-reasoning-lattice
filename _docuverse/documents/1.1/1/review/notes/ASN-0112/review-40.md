# Review of ASN-0112

## REVISE

### Issue 1: Type confusion — span equated with span-set in V12

**ASN-0112, "What the caller learns beyond the name" and V12 table row**: "decides emptiness (`σ_d = ⟨⟩ ⟺ O(d) = ∅`, V11)" and "emptiness (`σ_d = ⟨⟩ ⟺ O(d) = ∅`)".

**Problem**: `σ_d` is defined throughout as the *span* `(origin_d, extent_d)` (V0, V2), while `⟨⟩` is the empty *span-set*. Writing `σ_d = ⟨⟩` equates a span with a span-set — a type error. It also contradicts the ASN's own careful statement elsewhere that on the empty result "there is no `σ_d`" (wp section, both `Exact` and `Tight` parentheticals). The query's result is `RETRIEVEDOCVSPAN(d) ∈ SpanSet`, not `σ_d`.

**Required**: Replace `σ_d = ⟨⟩` with `RETRIEVEDOCVSPAN(d) = ⟨⟩` in both occurrences, matching V0/V11 and the worked example's `RETRIEVEDOCVSPAN(d) = ⟨([1,1],[1,2])⟩` usage.

### Issue 2: Forward-referencing restatement in the Vstream section

**ASN-0112, "The Vstream is what we measure, not the Istream", closing paragraph**: "The relationship the extent must bear to the arrangement is therefore one of *current correspondence*: by V2 the span covers every occupied position, and by V4 it draws its endpoints from no other source. For a document whose occupied positions lie in a single subspace, this correspondence is *exact*."

**Problem**: The paragraph restates V2 and V4 (just established) and then teases V5's exact-cover result, which is the subject of the very next section. Per the anti-bloat checks this is a section deferring forward to a downstream claim plus a restatement that advances no new reasoning.

**Required**: Drop the closing sentence (the V5 teaser) and the V2/V4 restatement; V4 already stands on its own. If a bridge to V5 is wanted, a single clause is enough.

## OUT_OF_SCOPE

(none — the ASN reports a single whole-document bounding span and does not encroach on per-subspace reporting, content delivery, or version comparison)

VERDICT: REVISE
