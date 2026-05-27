# Review of ASN-0099

## REVISE

### Issue 1: Excessive length and meta-commentary
**ASN-0099, throughout**: Phrases like "We surface this as a labeled claim", "We let these facts emerge naturally", "This is the structural basis of attribution", and "Let us recognize that the question splits cleanly" recur throughout, adding length without content. The substantive content (F1, F2/F3, F8/F9/F11/F19 plus their derivations) is sound but buried.
**Problem**: Verbosity makes audit difficult and obscures the substantive content. The ASN is approximately 3-4× longer than necessary for what it specifies.
**Required**: Aggressively trim meta-commentary. Present claims and their derivations directly without preamble.

### Issue 2: Worked example bloat
**ASN-0099, Worked Example section**: 11 queries with substantial overlap. Queries 4, 7, 10, and 11 all illustrate variants of invariance under non-allocating operations; Queries 1, 2, 3 redundantly establish the transclusion/match basics.
**Problem**: Reader's attention is diluted across redundant illustrations of the same phenomena.
**Required**: Reduce to 4-5 queries covering distinct phenomena: basic match, transclusion transparency (F6), filtered/scoped form (F7/F14), cross-subspace (Query 9), and multi-step preservation (one of 10 or 11, not both).

### Issue 3: F4's realizability discharge is repeated three times
**ASN-0099, F4 body**: The realizability argument appears in three separate paragraphs — "parametric factoring", "base construction at higher chain indices", "any other refinement (reachable exclusions)" — each covering similar ground with K.λ + L4 + L1c.
**Problem**: The reader reads variations of the same argument three times.
**Required**: Consolidate into one paragraph that states the universal closure once and cites K.λ's free endset choice + L4's address freedom uniformly.

### Issue 4: A1/A1a/A1b split with design rationale embedded in the spec
**ASN-0099, A1b body**: The paragraphs titled "Convergent grounding (non-constitutive)" and "Why not a substrate revision" together span more than a page of design rationale (Nelson citations at LM 2/14, 2/45, 2/29; udanax-green implementation evidence; scope/separability discussion of an alternative substrate revision).
**Problem**: Design rationale and methodological justification are mixed with normative content. The reader cannot extract A1b's actual claim without wading through extensive justification.
**Required**: Move grounding discussion and the "Why not a substrate revision" paragraph to a separate design note (or footnote). A1b's statement should be: "K.μ⁺, K.μ⁻, K.ρ preserve Σ.L by the closed-world reading of substrate effect-clause convention", with a one-sentence justification reference.

### Issue 5: Empty "Implementation Notes" section
**ASN-0099, Implementation Notes (Non-Normative)**: The section contains exactly one sentence: "Conformance is exhausted by F2 ∧ F3 — any procedure (with or without an auxiliary index) that produces `result(I, Σ) = findlinks(I, Σ)` conforms; the abstract specification is index-agnostic."
**Problem**: Empty section structure; the one sentence is already implicit in F2/F3.
**Required**: Remove the section entirely.

### Issue 6: Repeated invariance derivations across F8, F11, F15, F17, F19, F19-filt
**ASN-0099, F8/F11/F15/F17/F19/F19-filt**: All six claims share the same structural derivation pattern: equal `Σ.L` → equal `dom(Σ.L)` → equal per-slot endset → equal per-slot coverage → equal predicate evaluation → equal comprehension. F8's derivation lays out the chain in full; F11, F15, F17, F19, F19-filt each re-derive variants.
**Problem**: Each claim re-derives the same chain, inflating the spec without adding rigor.
**Required**: State the chain once as a meta-lemma (e.g., "ComprehensionInvariantUnderΣL"); cite it from each specific claim with the variant-specific details.

### Issue 7: Eight pairs of derivative claims duplicated mechanically
**ASN-0099, F2-filt/F3-filt, F2-sco/F3-sco, F2-V/F3-V, F10-filt/F10-sco, F15, F16, F17, F18, F19-filt, F19-sco**: Each derivative claim mechanically extends a base claim (F2/F3, F10, F8/F9, F19) to the filtered, scoped, or V-side form, with derivation chains that are near-mechanical lifts of the base case.
**Problem**: The bulk is redundant; the underlying structural facts could be presented once with a schema for variants.
**Required**: Present the base claims (F2/F3, F8, F9, F10, F11, F19) with a single "these properties propagate to the filtered, scoped, and V-side forms via the same structural derivation" meta-claim, or table the variants compactly.

### Issue 8: F9★ vs F9★-cor relationship is awkward
**ASN-0099, F9★ and F9★-cor**: F9★ (K.μ-only multi-step closure) is a strict subset of F9★-cor (V ∖ {K.λ} multi-step closure). The ASN keeps both, justifying F9★'s separate existence by "the operationally salient sequence in the editing surface is exactly K.μ-only".
**Problem**: Two named claims where one would do; the K.μ-only specialization is a one-line corollary of F9★-cor.
**Required**: Drop F9★; state at F9★-cor's citation sites whether the K.μ-only specialization is invoked.

### Issue 9: F10's chain-index = K.λ-event-count derivation is dense and could be lifted
**ASN-0099, F10's "presentation order recovers a creation-order property" paragraph**: The argument that "chain index = K.λ event count = T1 rank within A_L(d)" requires citing ChainMembershipForOrigin, ChainEnumerationInjectivity, TA5(a), T1 transitivity, and K.λ's subsequent-emission precondition — all in one dense paragraph.
**Problem**: Heavy citation chain in a single paragraph makes verification awkward.
**Required**: Lift the equivalence as a named sub-lemma (e.g., "ChainIndexEqualsAllocationOrder") so F10 can cite it cleanly.

### Issue 10: F2-V/F3-V's derivation status is ambiguous
**ASN-0099, F2-V/F3-V**: The ASN says F2-V/F3-V can be either derived from F2/F3 via F12 or imposed as parallel conformance obligations, depending on the implementation's internal routing.
**Problem**: A specification should pin one reading. The "either/or" framing leaves the conformance contract less precise than it could be.
**Required**: State F2-V/F3-V as the primary obligation on `result_V` and note that F2 ∧ F3 + F12 + F2-V ∧ F3-V together imply `result_V(R, d, Σ) = result(image(R, d, Σ), Σ)` when both surfaces are exposed coherently.

## OUT_OF_SCOPE

### Topic 1: Cross-server/distributed FINDLINKS semantics
**Why out of scope**: The ASN correctly defers replication concerns to a future ASN (already noted in "What We Have Not Specified").

### Topic 2: Access-control composition
**Why out of scope**: Already noted as a separate orthogonal concern in the Scope section.

### Topic 3: Inverse direction (I→V resolution for FOLLOWLINK)
**Why out of scope**: Already noted as a separate operation with its own subtleties.

### Topic 4: Performance/latency guarantees beyond "next query after K.λ commitment"
**Why out of scope**: Nelson's "without appreciable delay" is correctly framed as design intent (interactive vs batch), not a foundation invariant.

### Topic 5: Substrate revision to publish `L' = L` in K.μ⁺/K.μ⁻/K.ρ frames
**Why out of scope**: A substrate revision is a separate downstream proposal; this ASN's local adoption of A1b is the right local move.

VERDICT: REVISE
