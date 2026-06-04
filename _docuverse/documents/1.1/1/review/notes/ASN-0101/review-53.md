# Review of ASN-0101

I checked the operation specification (D0), the gap-closure algebra (D1), the preservation theorems (D2–D8), the projection characterisation (D9), the ValidComposite★ extension (D10), and the wp computations (D11), including the three worked examples and the boundary-case enumeration. The mathematics is sound: the shift-inverse `σ_d` is correctly grounded in TS1/TS2, the containment-precondition reduction is rigorous, the D8 source-correspondence argument correctly handles the `Q ∩ X ≠ ∅` re-mapping, and the P4★ "neutral-to-helpful" framing is properly scoped to a composite-boundary obligation rather than a false per-state assumption. I found no correctness defect. The findings below are anti-bloat (the note carries the `review-mode.anti-bloat` classifier).

## REVISE

### Issue 1: D11's cross-document wp bullets are trivial inventory
**ASN-0101, D11**: "wp(DEL[d, σ], discoverable_from(ℓ, d'', ·)) ≡ enabled(DEL[d, σ]) ∧ discoverable_from(ℓ, d'', Σ)" and the parallel "wp(DEL[d, σ], |project(L(ℓ).eᵢ, d'', ·)| = k) ≡ enabled(DEL[d, σ]) ∧ |project(L(ℓ).eᵢ, d'', Σ)| = k".

**Problem**: Both cross-document (`d'' ≠ d`) bullets compute a wp whose pullback is identical to the pre-state predicate — they merely restate D9's first-clause invariance in wp form. This is the "wp only computed where the answer is trivially true" pattern. The two non-trivial wps (from `d`) already carry the analytic content; rounding the presentation out to a 2×2 matrix adds two full bullets, each with its own justification paragraph, plus a paired re-verification in the third worked example, all establishing nothing beyond "DEL on `d` is transparent to `d''`."

**Required**: Collapse the two cross-document bullets into a single one-line remark ("by D9's first clause, both wps from any `d'' ≠ d` reduce to the pre-state predicate"), and remove the corresponding duplicate cross-document wp verification from the transclusion example.

### Issue 2: Empty-arrangement "Consequence" over-enumerates states the precondition already excludes
**ASN-0101, "The operation" (Consequence — non-applicability to empty arrangements)**: "This excludes, in particular, every freshly-registered document immediately after K.σ ... or after K.δ in the IsDocument case ... — both establish `M'(d_new) = ∅` ... until at least one V-position has been placed by a subsequent K.μ⁺ ... Symmetrically, after DEL itself empties a subspace ..."

**Problem**: The span-well-formedness precondition `s ∈ V_S(d)` already excludes empty arrangements outright. The paragraph then spends ~150 words enumerating every mechanism that produces an empty arrangement (K.σ, K.δ-IsDocument, post-DEL clearance). This is the "paragraph imagines/enumerates cases the precondition already excludes" pattern — the enumeration adds no constraint and advances no claim.

**Required**: Reduce to a single sentence: DEL is inapplicable when `V_S(d) = ∅`, an immediate consequence of `s ∈ V_S(d)`.

### Issue 3: Defensive "what the proof does not use" sentence in the D0 reduction
**ASN-0101, "Justification of the reduction"**: "The argument uses only T1's lex order against the structural forms of `s` and `r`, together with T0's grounding of components in ℕ — S8a is not invoked, since `v` is an arbitrary candidate tumbler not yet known to inhabit `V_S(d)`."

**Problem**: This sentence narrates which lemma the proof avoids rather than advancing the argument. The non-circularity point (a candidate `v` cannot be assumed well-formed) is real, but it can be conveyed at the one step where `v`'s components are reasoned about, not as a retrospective inventory of unused premises.

**Required**: Either inline the non-circularity caveat at the relevant step or delete the standalone defensive sentence.

## OUT_OF_SCOPE

None. The ASN correctly defers version creation and full historical reconstruction (the recoverability note explicitly scopes versioning out and confines DEL's contribution to its non-destruction guarantees).

VERDICT: REVISE
