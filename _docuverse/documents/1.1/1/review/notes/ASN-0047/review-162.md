# Review of ASN-0047

The technical core — the elementary transition set, the K.μ~ decomposition, the per-subspace D-SEQ★ derivation, and the Class (a)/(b) reachable-state induction — is sound on the cases I checked (full-document clearance, fork from empty/non-empty source, interior replacement, orphan links, the four-step vs two-/three-step replacement partition). The findings below are the anti-bloat patterns this note's `review-mode.anti-bloat` classifier directs me to surface: rationale and excluded-case prose that the precise reader must read past to follow the actual claims.

## REVISE

### Issue 1: Axiom annotated with rationale for its own absence elsewhere
**ASN-0047, Link-subspace extension**: "**Asymmetry with content-subspace depth (intentional).** No content-side analog of LinkVPositionDepthAxiom is imposed: a document's content-subspace V-position depth is *not* fixed per-document and may legitimately differ across re-populations. After a full content-subspace clearance ... a subsequent K.μ⁺ re-insertion may pin the first content V-position at any depth `m ≥ 2` ..."
**Problem**: This is a paragraph explaining *why the axiom is scoped as it is* (and why no twin axiom exists), not what the axiom states. It is exactly the "new prose around an axiom explains why it's needed rather than what it says" pattern. The object-level fact — content depth is governed by `ValidFirstInsertionPosition` and may change after clearance — is already carried by K.μ⁺'s precondition citing `ValidFirstInsertionPosition`; this paragraph restates it as a defense of the asymmetry.
**Required**: Delete the asymmetry paragraph. If the per-clearance depth freedom needs stating, state it once at K.μ⁺'s first-content-insertion precondition, not as a justification appended to the link-side axiom.

### Issue 2: Reviser drift — discharging a case the operation excludes
**ASN-0047, Link-subspace extension**: "K.μ⁺_L adds exactly one mapping per firing, so the pairwise-distinctness clause that K.μ⁺ states for its newly added V-positions has no work to do here — the singleton `{v_ℓ ↦ ℓ}` is trivially in bijective correspondence with itself, and there are no 'two distinct new mappings' to disagree on a shared V-position."
**Problem**: K.μ⁺_L's effect adds a single mapping by construction; "two distinct new mappings" is a configuration the operation cannot produce. Spending a sentence establishing that an excluded case "has no work to do" is the flagged pattern "a paragraph imagines a case the claim's carrier or precondition already excludes." It reads as K.μ⁺'s multi-position prose relocated to the singleton operation rather than removed.
**Required**: Drop the sentence. The substantive obligation here is `v_ℓ ∉ dom(M(d))` (already verified in parts (a)/(b) immediately after), which is what preserves S2; no statement about absent multiple mappings is needed.

### Issue 3: Use-site inventory in a notation slot
**ASN-0047, Notation (Set-inclusion notation)**: "The non-strict relations are written `⊆` and `⊇`. The convention is load-bearing for K.μ⁺'s effect clause `dom(M'(d)) ⊃ dom(M(d))` (strict extension) and K.μ⁻'s effect clause `dom(M'(d)) ⊂ dom(M(d))` (strict contraction) — both require strict inequality on the domain to qualify as actual mutations."
**Problem**: A notation definition that enumerates its downstream consumers. The `⊂`/`⊃` = proper-subset convention is fully specified by the preceding clause; the "load-bearing for K.μ⁺ ... and K.μ⁻ ..." tail is a use-site inventory ("this is consumed by X, Y") that does not advance the definition's meaning. The strictness requirement belongs at the K.μ⁺/K.μ⁻ effect clauses (where it is in fact already restated).
**Required**: End the convention at "The non-strict relations are written `⊆` and `⊇`." Remove the consumer inventory.

### Issue 4: First-emission/subsequent-emission freshness discharge restated verbatim across five sites
**ASN-0047** — the same dichotomy ("first emission ⟹ SubAllocatorAxiom.FirstEmission; subsequent emission ⟹ T10a GlobalUniqueness on the inc chain; cross-subspace via SC-NEQ + T7 / L14") is spelled out in full at: (a) the K.α definition, (b) the K.λ definition, (c) the *Link distinctness* prose under Class (a), (d) the *S4* prose under Class (a), and (e) the worked-example Steps 1 and 4.
**Problem**: This is the "two paragraphs in the same document say the same thing in different words" pattern, multiplied. Each instance re-derives the identical first-vs-subsequent split with the identical premises. The repetition is not pedagogical scaffolding — the worked example, the matrix cells, and the definition prose each present it as the load-bearing argument afresh.
**Required**: State the first/subsequent freshness-discharge argument once (it is genuinely a single lemma over any sub-allocator chain: FirstEmission for the seed, GlobalUniqueness thereafter, L14 cross-subspace). Have K.α, K.λ, the distinctness rows, and the worked example cite it by name rather than re-derive it.

### Issue 5: Defensive premise-cataloguing and role-distinction prose
**ASN-0047, FrontierEquivalence**: "*Three load-bearing premises.* (i) ... T10a.7 (EnumerationInjectivity, ASN-0034) is cited only for well-definedness of 'frontier' ..."; and **K.δ case (ii) freshness**: "The per-`(t, k')` uniqueness axiom is reserved for T2 spawn admissibility ... it governs whether the spawn is permitted, not the pre-state freshness fact `e ∉ E`."
**Problem**: Both are "Scope"-style sub-paragraphs that pre-empt a misreading rather than advance the argument — "cited only for," "reserved for ... not the ..." defend the boundary of an axiom's role instead of using it. FrontierEquivalence's three-premise catalogue then re-cites the same premises inside the forward/reverse proof, so the catalogue is redundant with the proof body it precedes.
**Required**: Cite T10a.7, T10a chain-advancement uniqueness, P1, and the per-`(t,k')` axiom at the proof step that consumes each; remove the standalone premise catalogue and the "reserved for / not the" defensive gloss.

## OUT_OF_SCOPE

None beyond what the ASN already routes to its Open Questions (link-withdrawal/tombstoning mechanism, account-level depth-1 extension, node-registry protocol, concurrency). These are correctly deferred and need no action here.

VERDICT: REVISE
