# Review of ASN-0116

This is a strong revision. The composite decomposition (K.α×n → K.μ⁻ → K.μ⁺ → K.ρ×n) is exhibited explicitly with per-step precondition discharge at the intermediate states; the gapped/filled bridge to ASN-0082's I3 family is handled honestly rather than by silent identification; the coupling constraints J0/J1★/J1'★ are traced through the range identity RAN, including the subtle range-old status of the shifted suffix; the forward-merge impossibility argument in IP1 is genuinely airtight (the chain-frontier argument via ChainMembershipForOrigin and CrossDocumentDisjointness holds for arbitrary-origin suffix content); and the boundary cases (append, empty subspace with both content-region sub-cases, front insertion exercising `n'_{s_C} = 0`) are each worked rather than waved at. I verified the IP4 four-part decomposition, the count formula, the incomparability argument via the greatest suffix witness, and the worked example's LP-Fin coverage reductions; all check out. Two issues remain — one missing premise in a derivation chain, one duplication of the kind the anti-bloat mode flags.

## REVISE

### Issue 1: IP6's set-level identity is asserted without the link-population premise

**ASN-0116, "A weakest precondition" section**: "Therefore `D(d, Σ') = D(d, Σ) ∪ Added`, where `Added = {a ∈ dom(Σ.L) : (E i : coverage(Σ.L(a).eᵢ) ∩ A_new ≠ ∅)}`…"

**Problem**: The displayed equivalence chain establishes a per-link biconditional — `discoverable_from(a, d, Σ') ⟺ discoverable_from(a, d, Σ) ∨ (E i : coverage(eᵢ) ∩ A_new ≠ ∅)` — quantified "for every prior link `a`". But `D(d, Σ')` is by definition a subset of `dom(Σ'.L)`, and the lift from the per-link biconditional to the set identity `D(d, Σ') = D(d, Σ) ∪ Added` requires `dom(Σ'.L) = dom(Σ.L)`, i.e., that the composite mints no new links. F-LINK supplies exactly this, but the derivation never invokes it — the only cited frame facts in this chain are RAN, LP12, LP13, and LP3★, which cover value preservation and coverage invariance for *prior* links and say nothing about the absence of *new* ones. Both directions of the wp claim ride on the set identity, so the gap sits under the headline result of the section.

**Required**: One clause at the lifting step: cite F-LINK (`Σ'.L = Σ.L`, hence `dom(Σ'.L) = dom(Σ.L)`) so the quantification over prior links is exhaustive of `D(d, Σ')`, then conclude the set identity.

### Issue 2: The paragraph preceding IP4 duplicates IP4

**ASN-0116, "Link anchoring across the displacement"**: "This is the precise sense of Nelson's survivability clause restricted to insertion (4/43)… The resolved witnesses are V-positions, and the suffix witnesses are *relabelled* by `v ↦ shift(v, n)` — so the post-insert V-position set is not in general a superset of the prior one (IP4's case split below makes the conditions precise). What is monotone is the *count* of witnesses and the *resolved content*: each prior witness maps injectively to a surviving one (left verbatim, suffix shifted, cross-subspace verbatim), and the new block can only add witnesses, never remove or redirect. We record it."

**Problem**: Apart from the Nelson anchor in its first sentence, this paragraph is a prose restatement of what IP4 says formally in the immediately following claim: the injective mapping with its three-part verbatim/shifted/verbatim structure, the non-superset caveat, the count monotonicity, and the content monotonicity all reappear word-for-word-in-different-words inside IP4. This is the adjacent-paragraphs-saying-the-same-thing pattern: the three derivation bullets above it are the proof, IP4 is the claim, and this paragraph is a third pass adding nothing the other two don't carry. The forward pointer "(IP4's case split below makes the conditions precise)" is the tell — the paragraph knows its content is restated one paragraph later.

**Required**: Cut the paragraph to the Nelson-anchor sentence ("This is the precise sense of Nelson's survivability clause restricted to insertion (4/43): because insertion removes nothing, every link survives with its designated content unchanged. We record it.") and let IP4 carry the injectivity/monotonicity content once.

## OUT_OF_SCOPE

### Topic 1: Concurrent insertions without a serializing authority
**Why out of scope**: The ASN correctly operates under SequentialTransitionAxiom and lists the concurrency question among its Open Questions; freshness under concurrent allocation is new territory, not an error here.

### Topic 2: Provenance and link behavior under transclusion-based placement
**Why out of scope**: IP5 covers the isolation of *existing* sharers under INSERT, which is in scope; placement *by* transclusion (COPY) and its provenance semantics are deferred to the reframed transclusion ASN, as the Open Questions acknowledge.

VERDICT: REVISE
