# Review of ASN-0112

## REVISE

### Issue 1: Design-rationale paragraph that does not advance the claim

**ASN-0112, "What the caller must be handed"**: "We *considered* the alternative of typing the result uniformly as a span-set throughout — wrapping the non-empty answer as the singleton `⟨σ_d⟩` … We reject it because Nelson fixes the result as …"

**Problem**: V0 already fixes the type as `Span + {⟨⟩}` with full justification from 4/68. The "considered the alternative … we reject it" paragraph is defensive design-rationale explaining *why a choice was made* rather than stating what the result is. This is the "essay content in a structural slot" / reviser-drift pattern flagged by the anti-bloat classifier.

**Required**: Delete the paragraph; the rejection of a singleton-wrapper type adds no expressive content beyond V0's statement.

### Issue 2: The level-uniform / endpoint-level-compatible distinction restated in five places

**ASN-0112, substrate / V2 / V6 / V17 / worked example**: substrate — "We must keep this notion sharply distinct … the two inequalities point opposite ways and coincide only at equality"; V2 — "This is an endpoint condition, *not* span level-uniformity — indeed the span is level-uniform iff `#origin_d ≥ #reach_d`"; V17 — "V17's `Pos` and `actionPoint` claims hold *without* any endpoint depth relation"; worked example — "This must not be confused with the span being non-level-uniform — it is not."

**Problem**: The same distinction (span level-uniformity `#s = #ℓ` vs endpoint compatibility `#start = #reach`) is re-derived and re-stated at least five times in different words. Two or more paragraphs saying the same thing is the precise anti-bloat target. The reader must re-absorb the identical caveat at each claim.

**Required**: State the distinction once (in the substrate section, where it is introduced) and reference it; strip the re-derivations from V2, V6, V17, and the worked example.

### Issue 3: Repeated "implementation never exercises `m_C ≠ m_L`" framing

**ASN-0112, V6 / worked example / preconditions**: V6 — "We treat the `m_C ≠ m_L` divergence as an abstract possibility S8-depth admits but the implementation never exercises"; worked example — an entire "endpoint-depth-divergent variant" prefaced and followed by the same hedge; the wp section restates the reach-equality factoring again.

**Problem**: The abstract `m_C ≠ m_L` case is legitimately covered (S8-depth admits it, and the divergent worked example correctly demonstrates V2 survives it). But the surrounding "the implementation never exercises this" disclaimer is repeated across three sections — meta-prose around the same forward concern. The concrete divergent example is fine; the recurring defensive framing is noise.

**Required**: Keep the divergent worked example (it earns its place demonstrating V2 without level-uniformity); collapse the "implementation never realizes this" commentary to a single statement.

### Issue 4: V10 over-hedges a coincidence that always holds in its own regime

**ASN-0112, V10**: "when the content subspace is maximal (link subspace empty) … with the count-coincidence (extent's final component `= |O(d)|`) holding only in the dense, depth-uniform single-subspace regime."

**Problem**: V10's antecedent — content subspace maximal, link subspace empty, content present — *is* the single-subspace content regime, which is always dense (D-SEQ★) and depth-uniform (S8-depth). So the count-coincidence holds in *every* instance of V10's case; the qualifier "holding only in the dense, depth-uniform single-subspace regime" wrongly suggests V10's regime sometimes lacks it. The intended contrast is with the cross-subspace case (V6), not with sub-cases of V10.

**Required**: State that the coincidence holds throughout V10's case, and move the contrast (where it fails) to a reference to V6, rather than hedging within V10's own scope.

### Issue 5: `Exact` predicate undefined on the empty result

**ASN-0112, "Preconditions and well-definedness"**: "`Exact ≡ "⟦σ_d⟧ contains no occupied-depth position outside O(d)"` … If `O(d)` lies in a single subspace `s` (or is empty, vacuously) …"

**Problem**: For an empty document the operation returns `⟨⟩` and there is no `σ_d`, so `⟦σ_d⟧` is undefined and `Exact` has no truth value. The parenthetical "(or is empty, vacuously)" asserts vacuity without defining how `Exact` reads when no span is returned. The wp equation folds the empty case under "at most one subspace," but the postcondition it ranges over is ill-defined there.

**Required**: Define `Exact` to hold (vacuously) when the result is `⟨⟩` — i.e., predicate it on "no span is returned, or `⟦σ_d⟧` contains no occupied-depth position outside `O(d)`" — so the wp statement is well-typed over the tagged-union codomain.

## OUT_OF_SCOPE

(none — the ASN correctly defers per-subspace extent reporting, content delivery, and version comparison without introducing claims for them.)

VERDICT: REVISE
