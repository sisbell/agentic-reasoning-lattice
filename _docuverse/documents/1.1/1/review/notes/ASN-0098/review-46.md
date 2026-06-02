# Review of ASN-0098

The ASN is mathematically careful and the central machinery (the static-coverage / live-projection separation, the per-operation displacement lemmas, the wp derivation) is sound. The findings below are a table/body inconsistency, one under-cited "partition" claim, and forward-reference accretion that the anti-bloat classifier asks me to surface.

## REVISE

### Issue 1: LP12a summary table drops the enabledness conjunct the body insists on
**ASN-0098, Claims Introduced table, LP12a row**: "`wp(K.μ⁻[d, R], discoverable_from(a, d, ·)) ≡ (E i : project(a, i, d, Σ) ∩ R ≠ ∅)`"
**Problem**: The body states the wp as `enabled(K.μ⁻[d, R]) ∧ (E i : … project ∩ R ≠ ∅)` and then argues at length that the enabledness conjunct "is required for total correctness: at a state where K.μ⁻ is not applicable, no post-state exists, so the second conjunct … can hold vacuously while `discoverable_from(a, d, Σ')` is unrealisable." The table presents the weaker (wlp) form as if it were the wp, directly contradicting the body's own derivation. A reader consulting the summary gets a result the body declares insufficient.
**Required**: Restore `enabled(K.μ⁻[d, R]) ∧ …` in the table row (or drop the body's total-correctness emphasis), so the two statements of LP12a agree.

### Issue 2: LP20's "partition" of the projection range is asserted without the disjointness premise
**ASN-0098, LP20 corollary**: "this gives a complete characterisation of `{Σ.M(d)(v) : v ∈ project(e, d, Σ)}` as a partition into a content-subspace component (contained in `coverage(e) ∩ dom(Σ.C)`) and a link-subspace component (contained in `coverage(e) ∩ dom(Σ.L)`), with no other contributions."
**Problem**: "Partition" asserts the two image components are disjoint. The exhaustiveness of the union is justified (S3★-aux), but the *disjointness* of the two summands depends on `dom(Σ.C) ∩ dom(Σ.L) = ∅` (SD / L14 of the foundations), which is never invoked here. Without it the corollary establishes only an exhaustive union, not a partition.
**Required**: Cite the store-disjointness invariant (SD, ASN-0093 / L14, ASN-0047) at the point where "partition" is claimed, or downgrade the word to "exhaustive union."

### Issue 3: Forward-referencing meta-prose explaining LP-Fin's significance before LP-Fin is stated
**ASN-0098, Boundary and Width Behaviour**: "`F` is countably infinite — by T0(a) and T0(b) of ASN-0034 … The tightness predicate's universal `(A t ∈ F : s ≤ t < s ⊕ ℓ : …)` therefore ranges over an infinite domain; LP-Fin's finiteness of `F ∩ [s, s ⊕ ℓ)` for a canonical span is the fact that renders that predicate decidable."
**Problem**: This paragraph advances no claim. It pre-justifies why the still-unstated LP-Fin matters (decidability of the tightness quantifier) — the "explains why the result is needed rather than what it says" + downstream-deferral pattern. The decidability consequence is already made at the tight definition's use-site, where it belongs.
**Required**: Delete the paragraph; LP-Fin stands on its own statement, and the decidability remark already lives at the tight definition.

### Issue 4: LP19 hypothesis carries a scope-disclaimer that imagines an excluded case and defers to LP9
**ASN-0098, LP19**: "V-positions added at the same K.μ⁺ step whose image is *not* freshly allocated on the prefix — typically transclusion entries whose image lies in `dom(Σ_n.C) ∪ dom(Σ_n.L)` — fall outside this lemma's hypothesis and are governed instead by LP9's general growth characterisation, which admits growth when the transcluded image lies in `coverage(e)`."
**Problem**: LP19's hypothesis already restricts to freshly-allocated images per V-position; this trailing sentence narrates a case the hypothesis excludes and defers it to LP9. It is the "paragraph imagines a case the precondition already excludes" + "defers to downstream location" pattern. The per-V-position quantification in the preceding sentence is sufficient.
**Required**: Drop the disclaimer sentence; the hypothesis's per-V-position selection already scopes the lemma.

### Issue 5: LP-Fin restates the same divergence argument twice
**ASN-0098, LP-Fin proof**: the bound argument's "Sub-case (ii)" ("`d` disagrees with `d_0` at some position `j ≤ #d_0` … by T1 case (i) at position `j`, either `d_j < d_{0,j}` … or `d_j > d_{0,j}` …") and the later "Finiteness from the bound" paragraph ("Suppose … `d` disagrees with `d_0` at some position `j` with `1 ≤ j ≤ #d` … by T1 case (i) at position `j`, either `d_j < d_{0,j}` … or `d_j > d_{0,j}` …").
**Problem**: These are the same T1-divergence contradiction run twice over nested index ranges (`j ≤ #d_0` then `j ≤ #d`, with `#d ≤ #d_0` already in hand). Two paragraphs establishing the same fact in different words — the second is a sub-range of the first.
**Required**: Establish "`d` is a length-`#d` prefix of `d_0`" once and reuse it, rather than re-deriving the divergence contradiction in the finiteness step.

## OUT_OF_SCOPE

### Topic 1: Reverse-discovery, V-order reflection, link-to-link induced discovery
**Why out of scope**: These are correctly parked in Open Questions; they introduce new primitives (reverse lookup, V-order/I-order correspondence under K.μ~, link-referencing-link discovery) that belong in successor ASNs, not as gaps in this one.

### Topic 2: Link-canonical contraction disjointness
**Why out of scope**: The final Open Question (link-canonical endset under content-subspace-emptying contraction, where LP12b's disjointness argument inverts) is genuine future territory; LP12b deliberately treats only the content-canonical class and flags the inversion honestly.

VERDICT: REVISE
