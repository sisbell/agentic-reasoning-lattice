# Review of ASN-0117

This is a technically strong, thorough note: the K.μ⁻+K.μ⁺ vs. lone-K.μ⁻ split on `R = ∅` is correct (K.μ⁻ is a *prefix-retention truncation* and cannot do an interior shift, so the composite is genuinely required), the coupling discharge (J0/J1★/J1'★ vacuous) is sound, the range computation `ran(M'(d)) = ran(M(d)) \ A_del^{excl}` checks out including the link-subspace carry-through, and the boundary coverage (leading-span, suffix, delete-everything, within-document sharing, cross-document transclusion) is genuinely exhaustive. The wp is non-trivial and the per-link-existential quantifier structure is correctly defended.

The findings are anti-bloat, consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Use-site inventory / licensing prose in the Effect section
**ASN-0117, Effect**: "the K.μ⁻ + K.μ⁺ decomposition (or the lone K.μ⁻ when `R = ∅`) is what places DELETE inside ASN-0047's *valid-composite* vocabulary, licensing our appeal to the properties proven over that fuller model — the per-subspace well-formedness package, the referential-integrity invariant S3★, and the link/discoverability lemmas of ASN-0098, all quantified over reachable states and valid transitions of `Σ`."
**Problem**: This enumerates downstream consumers and explains *why* the composite framing licenses later appeals, rather than advancing the contraction's meaning. The valid-composite membership is established by the preceding two paragraphs; the inventory of what it "licenses" is meta-prose the reader must skip. The adjacent aside "in the same sense that K.μ~ (ArrangementReordering) is itself a named K.μ⁻ + K.μ⁺ composite" is a justificatory analogy of the same kind.
**Required**: Delete the licensing sentence and the K.μ~ analogy; cite the specific ASN-0047/0098 properties at the points where they are actually used.

### Issue 2: Provenance-of-clause prose in DEL-LIMM
**ASN-0117, Frame (DEL-LIMM)**: "This is *stronger* than L12 (LinkImmutability, ASN-0043) ... The arrangement state ASN-0082 governs carries no link store, so this frame is imposed here directly, not inherited."
**Problem**: The final sentence explains the *provenance* of the clause (where it comes from, why it is stated rather than inherited) rather than its content. That is meta-prose about document construction. The L12 comparison itself is informative and may stay.
**Required**: Drop the "imposed here directly, not inherited" sentence; keep the L12-strength contrast.

### Issue 3: Counterfactual / significance commentary in the wp section
**ASN-0117, weakest-precondition section**: "Had P4 asserted unconditional preservation of discoverability, this computation would have refuted it..." and "The wp is the formal witness that 'deletion preserves discoverability' is a *conditional*, not a theorem: deletion can only orphan, never resurrect, discoverability from `d`."
**Problem**: These restate the result as significance commentary, imagining a counterfactual (P4 asserting something it does not). The wp formula and the "last witness" reading already deliver the conditional character; the counterfactual adds no derivation.
**Required**: Remove the counterfactual sentence and the "formal witness" gloss; the derived condition and its plain-language reading suffice.

### Issue 4: "A span, not a position" section re-derives already-established claims
**ASN-0117, binding versus being**: "DEL-REMOVE strips the span's V→I correspondences from `M'(d)` ... DEL-CIMM leaves `A_del ⊆ dom(C')` ... Nelson's three-clause annotation (4/9) is precisely these two facts plus their consequence..."
**Problem**: This middle passage restates DEL-REMOVE + DEL-CIMM and the Nelson-4/9 mapping already given in "What is removed, and what must survive." Two passages say the same thing in different words. (The binding-vs-being *analogy* itself is fine and on-topic; the re-derivation of the clauses is the duplication.)
**Required**: Compress to the conceptual point (span = the unit carrying both arrangement-extent and existence) and reference the earlier P0/DEL-REMOVE statements instead of re-deriving them.

## OUT_OF_SCOPE

### Topic 1: Deletion at text-position depth `m > 2`
**Why out of scope**: The note fixes `m = #p = 2`, inherited verbatim from foundation ASN-0082's depth-2 contraction. Generalizing the displacement to deeper text subspaces is a foundation matter, not an error in this ASN; the note correctly does not claim generality.

VERDICT: REVISE
