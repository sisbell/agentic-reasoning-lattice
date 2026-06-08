# Review of ASN-0107

## REVISE

### Issue 1: R2 uses bare `Δnum` where the quantity is necessarily `Δnum_disc`
**ASN-0107, R2 (ContentDeletionUnbounded)**: "Contracting an arrangement so as to remove that endpoint can drop up to `k` links from the discovery count in one operation: `Δnum ∈ {−k, …, 0}`."
**Problem**: The body writes `Δnum`, but contraction (K.μ⁻) is an arrangement transition that cannot move the existence count (E3); the claim is about the discovery count, as the claims table confirms ("drop up to `k` from the discovery count"). R1 and R6 both write `Δnum_disc` for the same kind of change. The bare `Δnum` is ambiguous and inconsistent with its neighbours.
**Required**: Write `Δnum_disc ∈ {−k, …, 0}` in R2's statement.

### Issue 2: A1a re-argues a case its own corollary-of-E3 status already excludes
**ASN-0107, A1a (FreshContentNeutrality, existence)**: after establishing the claim as "a corollary of E3: K.α changes neither `dom(Σ.L)` nor any `coverage` nor the fixed `Q`, so `match(Q, ·)` is invariant," the paragraph continues "The membership `a_new ∈ Q` does not move the existence count: if some stored link `ℓ` already covers `a_new` (a ghost reference, LP17)… `ℓ` matched before allocation and matches after… (The orphan/resurrection mechanism, LP17–LP18 … bears on discoverability, not on the existence count…)."
**Problem**: Once the claim is fixed as a corollary of E3 (K.α leaves `match(Q,·)` invariant), the entire ghost-reference / orphan-resurrection case walk is redundant — it imagines a case (`a_new` being covered) that the E3 corollary has already rendered irrelevant. This is reviser drift: a paragraph imagining a case the claim's carrier already excludes.
**Required**: Cut the ghost-reference case analysis and the LP17–LP18 parenthetical; the corollary sentence suffices.

### Issue 3: D2 extension bullet carries a use-site/exhaustiveness justification
**ASN-0107, D2 (DiscoveryNonMonotonicity), extension clause**: "Both must be named: a query part may resolve to link-subspace addresses, since `Wᵢ` may contain link-subspace V-positions whose images are link addresses (link-to-link references, L4(c); S3★ …), and K.μ⁺_L then alters `Qᵢ(Σ)` exactly as K.μ⁺ does for the content subspace."
**Problem**: "Both must be named" justifies the document's own choice to enumerate two operations rather than advancing the monotonicity claim. The load-bearing content (extension grows `Qᵢ`) holds identically for K.μ⁺ and K.μ⁺_L; the defense of *why both are listed* is meta-prose.
**Required**: State the growth conclusion once over "an extension step (K.μ⁺ or K.μ⁺_L)"; drop the "Both must be named" justification.

### Issue 4: R1's minimal-contraction split is re-derived wholesale in R6
**ASN-0107, R1 (MinimalDecrementNoStoreRetraction) and R6 (CountedLinkPreservationWP)**: R1 establishes `Δnum_disc ∈ {−1,0}` under (P-max)/(P-uniq)/(P-slot)/(P-sole) with the split on "`coverage(Σ.L(ℓ).eᵢ) ∩ Qᵢ(Σ) = {a}`"; R6's "Specialisation to R1" paragraph then re-derives the identical split as "the two truth-values of R6 at `ℓ`."
**Problem**: The two passages say the same thing in different words — R6's wp subsumes R1's four-precondition case. Carrying both at full length is the duplication the anti-bloat pass targets.
**Required**: Reduce R1 to its no-store-retraction content plus a pointer that the minimal-contraction decrement is the `k=1` case of R6, or drop R6's re-derivation and let R1 stand as the corollary. Do not state both derivations in full.

## OUT_OF_SCOPE

### Topic 1: independently-anchored, separately-evolving request parts
**Why out of scope**: The note's own Open Questions raise multi-document anchoring; it belongs to a later ASN, and the present note correctly does not specify it.

### Topic 2: agreement between the count and the cardinality the retrieval operation would return
**Why out of scope**: Retrieval (FINDLINKS / ASN-0099) is explicitly excluded; the staleness/agreement guarantee is a cross-operation property for a future note.

VERDICT: REVISE
