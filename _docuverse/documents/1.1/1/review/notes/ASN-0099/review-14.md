# Review of ASN-0099

## REVISE

### Issue 1: F4's "any further refinement" general clause is informally stated
**ASN-0099, F4 (MatchFormulaUniqueness)**: "any further refinement is governed by the same witness pattern, realized through the canonical-span construction used in the three cases above."
**Problem**: The general clause asserts the canonical-span witness pattern extends to any strengthening, but doesn't prove this. The three enumerated witnesses (containment in either direction, threshold k > 1) each receive a concrete witness pair construction; the general clause is hand-waved. The argument is not closed: canonical-span coverages under PrefixSpanCoverage are infinite prefix subtrees, so a hypothetical strengthening like "P fires only for endsets with finite coverage" rejects every canonical-span instance whether F1 fires or not, and the canonical-span construction alone does not exhibit a witness. The text never establishes that every strict strengthening admits a witness within the realizable construction.
**Required**: Either prove the general claim — showing the canonical-span construction yields a witness for any P strictly stronger than F1 — or trim the clause to the abstract principle alone: "any predicate P strictly stronger than F1 admits some F1-admitted (a, I) pair as witness; the realization through canonical spans is verified for the three enumerated classes." Don't conflate "F1 is uniquely minimal" (an abstract truth from definition) with "canonical spans suffice as witnesses" (which requires per-class verification).

### Issue 2: `result(I, Σ)`, `result_filtered(C, Σ)`, `result_scoped(I, S, Σ)` introduced informally
**ASN-0099, F2/F3/F2-filt/F3-filt/F2-sco/F3-sco**: "We let `result(I, Σ)` denote the implementation's actual output..." (and similar for the variants).
**Problem**: Each conformance symbol is introduced as a placeholder without a formal type signature or definition. F2/F3 use the symbols as if they were defined functions. The rest of the spec carefully defines every introduced symbol (image, matches, findlinks, etc.) with preconditions and signatures; the conformance symbols stand out as informal exceptions. A reader cannot determine, for example, whether `result(I, Σ)` is required to be functional in (I, Σ) or could be non-deterministic.
**Required**: Either define each as an explicit function (e.g., "result : 𝒫(T) × State → 𝒫(T)") or rephrase the conformance claims without naming the symbols, e.g., "every conforming implementation produces output O(I, Σ) for the query (I, Σ) with O(I, Σ) = findlinks(I, Σ)."

### Issue 3: F9 inductive composition is gestured at but not stated
**ASN-0099, F9 discussion**: "The pure-K.μ inductive composition of F9 across edit-only sequences (each step's Σᵢ.L = Σᵢ₊₁.L chaining by transitivity into F8 over the endpoints) is a structural completeness observation rather than an operationally needed claim; we note it here but do not develop it further."
**Problem**: The ASN mentions but does not formalize multi-step F9 across edit-only sequences. F11 covers the general inclusion case (which is monotone, not equality), so the equality-across-edit-only-sequences claim is genuinely separate. Either it deserves a labeled claim (F9★, perhaps) or the discussion should be deleted rather than left as a dangling observation. Half-stated claims rot.
**Required**: Either promote to a labeled claim with a one-line derivation (transitivity of `Σᵢ.L = Σᵢ₊₁.L` chained into F8 between endpoints), or remove the paragraph entirely. The current "we note it here but do not develop it further" leaves an unresolved theorem in the middle of an otherwise rigorous derivation chain.

### Issue 4: F10's chronological-order derivation rests on an unstated assumption
**ASN-0099, F10 discussion**: "Within a home document, T1 = K.λ order."
**Problem**: The argument cites ChainEnumerationInjectivity (ASN-0093) to lift per-step `inc(·, 0)` strict increase to chain-index ordering. But the claim "chain index = K.λ order within the chain" requires that consecutive K.λ events for the same home document use successive chain elements. The K.λ precondition in ASN-0093 enforces this: subsequent emission is `inc(prev, 0)` where `prev := max{ℓ' ∈ dom(L) : origin(ℓ') = d}`. So chain index = K.λ event count for this document. But the ASN doesn't cite this premise explicitly — it just asserts "T1 = K.λ order" within a document.
**Required**: Either cite ASN-0093's K.λ "subsequent emission" precondition explicitly (the `max{...}` clause that pins the next emission to the chain successor) so the chain-index-equals-K.λ-event-count step is grounded, or extract this as a one-sentence corollary with the citation. Otherwise the derivation chain has an unstated step.

### Issue 5: F10's cross-document T1 case (ii) sub-argument has a subtle gap on length comparison
**ASN-0099, F10 discussion**: "at position `#d₁+1`, `b_L(d₁)` has the appended `0` separator while `b_L(d₂)` has `d₂_{#d₁+1} ≥ 1`, yielding `b_L(d₁) < b_L(d₂)` by T1 case (i)."
**Problem**: This identifies the divergence at position `#d₁ + 1` and applies T1 case (i). T1 case (i) requires the divergence position `k ≤ min(#a, #b)`. Here `b_L(d₁)` has length `#d₁ + 2` and `b_L(d₂)` has length `#d₂ + 2 ≥ #d₁ + 3`, so `min(#b_L(d₁), #b_L(d₂)) = #d₁ + 2 ≥ #d₁ + 1`. The divergence position `#d₁ + 1` satisfies `#d₁ + 1 ≤ #d₁ + 2`, so T1 case (i) applies. Good — but the ASN doesn't verify this length condition.
**Required**: Add the explicit length-bound verification: "the divergence position `#d₁ + 1` satisfies `#d₁ + 1 ≤ min(#b_L(d₁), #b_L(d₂)) = #d₁ + 2`, so T1 case (i) applies."

### Issue 6: Worked example doesn't exercise type-endset filtering
**ASN-0099, Worked Example**: Queries 1–7 exercise from/to endset matching but not type-endset (slot 3) filtering.
**Problem**: F7(b) (filter conjunction) and L3 (slot 3 mandatory non-empty type endset) are central. The "Implementation Notes" promise that filtered queries against the type-endset are first-class operations. But no worked-example query exercises a `(3, J)` constraint. A reader cannot verify by concrete example that the filtered form correctly handles type-based queries — and the type-endset is the very thing that distinguishes Xanadu-style links from generic spans.
**Required**: Add at least one query exercising a slot-3 constraint, e.g., `findlinks_filtered({(3, I_type)}, Σ)` for some I_type subset of T. Pair it with an evaluation against ℓ and ℓ' that turns the empty-by-assumption type-endset coverage into a concrete witness — for instance, place ℓ's type endset at a specific link-type address and verify the filter fires on ℓ, fails on ℓ'.

### Issue 7: Worked example doesn't exercise link-subspace V-positions or address-of-address links
**ASN-0099, Worked Example**: The example uses only s_C V-positions; no s_L positions are arranged in d_a or d_b.
**Problem**: The ASN explicitly admits cross-subspace queries (V-positions in s_L mapping to dom(L) per S3★) and the address-agnostic match predicate, and frames "annotation on an annotation, a comment about a typed connection" as a natural use case. But the abstract handling is asserted without a concrete instance. The reader has to take on faith that the spec works uniformly across subspaces.
**Required**: Add at least one query against an s_L V-position, e.g., extend d_b's arrangement via K.μ⁺_L with `v_b^L ↦ ℓ`, then evaluate `findlinks_V({v_b^L}, d_b, Σ)`. Show the image is `{ℓ}`, the match predicate tests each link's endset coverage against `{ℓ}`, and the result is the set of links whose endsets reference ℓ (introduce a third link ℓ'' to demonstrate a non-trivial result). This exercises the cross-subspace path end-to-end.

### Issue 8: F10 prose has minor informalities
**ASN-0099, F10 discussion**: "two documents may interleave their K.λ commitments arbitrarily in time"
**Problem**: "In time" is informal; the substrate's transition semantics are about transition order (atomic, totally ordered per SequentialTransitionAxiom, ASN-0093), not chronological time. Minor but inconsistent with the spec's transition-vocabulary terminology elsewhere.
**Required**: Replace with "interleave across the operation history in any order" or similar transition-vocabulary phrasing.

## OUT_OF_SCOPE

The ASN's Open Questions section already correctly identifies topics belonging in future ASNs: addresses outside `dom(C) ∪ dom(L)`, multi-instance partition tolerance, access-control composition, audit witnesses, K.λ-to-FINDLINKS latency bounds, the inverse direction (FOLLOWLINK/RETRIEVEENDSETS), and the ASN-0047 frame-clause revision that would eliminate A1. No additional out-of-scope items.

VERDICT: REVISE
