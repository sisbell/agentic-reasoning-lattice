# Review of ASN-0099

I checked the operation definitions (image, findlinks, findlinks_V, findlinks_filtered, findlinks_scoped), the match predicate F1, and the proof chains F2–F23, plus the worked example. The mathematical content is solid: the union-over-single-slot-filters identity, F13's existential-over-disjunction step, F10/empty-query boundary handling, and the F21/F22/F23 weakest-precondition derivations all cover their cases, including the degenerate ones (ℛ=∅, dom(Σ.L)=∅, R disjoint from arrangement, link-subspace images). No skipped case found in the core proofs. The findings below are precision and accretion items.

## REVISE

### Issue 1: F21 describes K.μ⁻ as retaining an arbitrary subset
**ASN-0099, "Persistent Discoverability (I-Side)" / F21**: "Let K.μ⁻[d, ℛ] denote the contraction of d's arrangement that retains exactly the V-position subset ℛ ⊆ dom(Σ.M(d))."
**Problem**: K.μ⁻ does not retain arbitrary subsets. Per ASN-0047's K.μ⁻, the retained domain is a per-subspace canonical initial segment `⋃ {[S,1,…,1,k] : 1 ≤ k ≤ n'_S}` (required to preserve D-CTG★/D-MIN★). The foundation lemma F21 composes with — LP12a — is careful to parameterize by retention counts `(n'_{s_C}, n'_{s_L})` and construct the retained set explicitly. F21 generalizes the parameter to an unconstrained ℛ. The wp formula stays correct because `enabled(K.μ⁻[d, ℛ])` evaluates to false for non-canonical ℛ, but the prose "retains exactly the V-position subset ℛ ⊆ dom(Σ.M(d))" invites a reader to instantiate ℛ as any subset and follow the derivation to a meaningless post-state.
**Required**: State that ℛ ranges only over canonical (enabled) retention domains, matching LP12a's retention-count parameterization, or note inline that `enabled(K.μ⁻[d, ℛ])` is false unless ℛ is a per-subspace initial segment.

### Issue 2: F15's introductory paragraph previews its own proof
**ASN-0099, "Scope" / before F15**: "Determinism, survivability, and monotonicity transfer to both the filtered and scoped forms by a single argument: their membership predicates consult only Σ.L and query-data (so ComprehensionInvariantUnderΣL applies), and they are closed under intersection with the query-supplied S …"
**Problem**: This paragraph compresses the same content given immediately after F15 in the per-clause proof ("(a) Determinism: the filtered universal consults only Σ.L and query-data, so ComprehensionInvariantUnderΣL gives…; (b) Survivability: A1a gives Σ.L = Σ'.L …; (c) Monotonicity: LP13 + PerLinkInvariance …"). The note carries the `review-mode.anti-bloat` classifier; this is the "two paragraphs in the same document say the same thing in different words" pattern — a summary slot duplicating the proof slot.
**Required**: Drop the preview sentence and let the F15 statement plus its per-clause proof carry the argument, or keep the one-line intuition and remove the redundant restatement from the proof.

## OUT_OF_SCOPE

### Topic 1: Combined filtered-and-scoped operation
The note lists `findlinks_filtered_scoped(C, S, Σ)` under "What We Have Not Specified." Correctly deferred — composing the two narrowings is a natural future increment, not a gap in this ASN.

VERDICT: REVISE
