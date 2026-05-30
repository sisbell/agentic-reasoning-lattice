# Review of ASN-0043

The technical core is sound. I checked the load-bearing proofs — CPP's prefix-preservation (the `#tᵢ > #s` constraint correctly makes sibling advances operate strictly beyond `p`), the L0a/T7 disjointness discharge, FSP's per-invariant bullets, L9's Case A/B fresh-address construction, L11a's single-tree argument via S7d, and PrefixSpanCoverage's mutual-inclusion derivation. The five-state worked example exercises the non-vacuous cases (higher arity at a₃, type discrimination at a₄, reflexive addressing at a₂) and verifies the coverage computations correctly. No skipped boundary case of REVISE caliber.

The findings below are all anti-bloat: accreted essay/meta-prose this note's classifier flags. Each makes a precise claim harder to follow by interposing design commentary.

## REVISE

### Issue 1: L13 carries a design-intent digression that does not advance the invariant
**ASN-0043, L13 — ReflexiveAddressing**: "This model takes the other route admitted by its own n-set provision (L3, NEndsetStructure): a faceted link relating more than three roles is realized directly as a single link of arity N... Link-to-link composition (L13) remains available for compound structures that a flat endset sequence cannot express, but it is not how this model expresses the faceted link. Nelson's chain construction is thus historical design intent, not the model's structural commitment for the faceted link."
**Problem**: L13's claim is that link addresses are valid endset targets (canonical span coverage). The cons-cell analogy is legitimate, but the closing three sentences are a digression adjudicating *how the model chooses to express faceted links* — a comparison between L3 (arity-N) and L13 (chaining) plus a verdict on Nelson's intent. None of it bears on whether `coverage({(b, δ(1, #b))}) = {t : b ≼ t}`. This is essay content in a lemma slot; the reader must skip it to reach the next claim.
**Required**: Cut from "This model takes the other route..." through "...structural commitment for the faceted link." Retain at most a one-clause note that faceted links may be realized either as arity-N links (L3) or by chaining (L13).

### Issue 2: L8 wraps a derived consequence in editorial framing
**ASN-0043, L8 — TypeByAddress**: "This is a profound design choice. It decouples classification from content retrieval entirely. A search for 'all links of type X' never fetches the bytes at address X — it only matches the address. This means:"
**Problem**: "This is a profound design choice" is pure editorializing — it asserts significance without adding reasoning. The substantive consequence (classification decouples from retrieval, motivating ghost types in L9) survives without the evaluative wrapper. Defensive significance-claims of this shape are exactly the meta-prose the precise reader works around.
**Required**: Drop "This is a profound design choice." Lead directly with the decoupling consequence ("Type matching decouples classification from content retrieval: a search for type X never fetches the bytes at X...").

### Issue 3: L3's tail mixes a use-site implementation inventory with a "why-the-conjunct" gloss
**ASN-0043, L3 — NEndsetStructure**: "Gregory's implementation fixes N = 3 — the V-subspace assignment function `setlinkvsas` hardcodes three V-addresses, the query function `intersectlinksets` takes exactly three input lists, and the wire protocol (`FINDLINKSFROMTOTHREE`) encodes three endset parameters. The integer namespace for a fourth endset type is already consumed (`DOCISPAN = 4`), blocking extension without renumbering. The implementation can store sub-arity links... such states lie outside this ASN's conforming link store. The non-emptiness conjunct `Σ.L(a).e₃ ≠ ∅` is precisely this exclusion..."
**Problem**: Two patterns compound here. First, a four-item implementation inventory (`setlinkvsas`, `intersectlinksets`, `FINDLINKSFROMTOTHREE`, `DOCISPAN = 4`) catalogues where the codebase fixes N=3 — but L3 *admits* N≥3, so this inventory documents a divergence the invariant deliberately permits, not a property it establishes. Second, "The non-emptiness conjunct... is precisely this exclusion" explains *why the conjunct is needed* rather than what it constrains. The grounding that arity-3 is the dominant/standard form is already made by the StandardTriple convention earlier; this tail re-litigates it.
**Required**: Collapse the implementation inventory to a single clause noting the implementation fixes N=3 while the model admits N≥3. Drop the "is precisely this exclusion" gloss — the conjunct `e₃ ≠ ∅` states itself.

## OUT_OF_SCOPE

### Topic 1: Allocation-ordering of link vs content addresses within a document
**Why out of scope**: Listed in the ASN's own Open Questions and concerns allocation event sequencing, which is operation/allocation territory excluded by the scope list.

### Topic 2: Global content-subspace invariant lifting L0a disjointness from the `s_C`-slice to all of `dom(Σ.C)`
**Why out of scope**: The scoped disjointness is correctly derived; promoting it to unscoped requires a content-side invariant that belongs in the content-model ASN, not here. The ASN flags this itself in Open Questions.

VERDICT: REVISE
