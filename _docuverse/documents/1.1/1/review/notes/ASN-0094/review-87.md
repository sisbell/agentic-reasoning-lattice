# Review of ASN-0094

## REVISE

### Issue 1: "Coverage-class disjointness from R" derivation restated 5+ times

**ASN-0094, multiple sections**: The argument "shape(K) ≠ shape(R) ⟹ K ≁ R via per-class constancy of shape" appears as a standalone derivation in:

1. FDD preservation, Case A: "per-class constancy of shape(·) and the shape-tuple inequality between FDD's (1, 1, A_doc, A_doc, ⊤) and R's (*, 1, A, A_rel, ⊤) force K ≁ R for every FDD-registered K..."
2. FDD preservation, Case B: "FDD's shape (1, 1, A_doc, A_doc, ⊤) differs componentwise from R's (*, 1, A, A_rel, ⊤), so per-class constancy forces K ≁ R..."
3. SHCD preservation, Case A: "per-class constancy of shape(·) and the shape-tuple inequality with R force K ≁ R for every SHCD-registered K..."
4. BundledDirectedPair "Coverage class disjointness from R" paragraph: "The BundledDirectedPair shape tuple ... differs from R's ...; per-class constancy ... gives K ≁ R for every K at this shape..."
5. EffectiveWpSimplification "Coverage-class disjointness from R at every non-R catalog row" paragraph: "For any K registered at a catalog row whose shape tuple differs from R's ... per-class constancy of shape(·) ... gives the contrapositive ... so K ≁ R follows immediately..."

**Problem**: Five separate restatements of the same contrapositive derivation. Each instance chains the same two premises (per-class constancy of `shape(·)`, shape-tuple inequality with R) to the same conclusion. The phrasing varies but the substance is identical. This is the "two paragraphs saying the same thing in different words" anti-bloat pattern.

**Required**: Factor into a single named lemma — e.g., "Lemma — NonRSeparation: For every K ∈ T_cat with shape(K) ≠ shape(R), K ≁ R, by the contrapositive of per-class constancy of shape" — and have downstream sites cite it. Each consumer keeps the local shape-tuple-difference observation but cites the named lemma rather than re-deriving the contrapositive five times.

### Issue 2: EffectiveWpSimplification's proof has forward references to Sh1, Sh3, and RetractionSelfFreshness

**ASN-0094, "Corollary — EffectiveWpSimplification" section**: The corollary's proof references three later lemmas:

- Step 1: "For every (b̂, F', G') ∈ L_R^Σ, Sh1 at K := R gives G' canonical-slot with |slot_addrs(G')| = 1; Sh3 at K := R gives slot_addrs(G') ⊆ A_rel^Σ."
- Step 4 sub-case (b), K ~ R: "Self-nullification (witness = τ_new): this is exactly Lemma — RetractionSelfFreshness part (i)..."

The document's section order is:

1. Lemma — LinkAddressNotPrefixOfEmit
2. **Corollary — EffectiveWpSimplification** (cites Sh1, Sh3, RetractionSelfFreshness — all forward)
3. Cardinality (Sh0, Sh1)
4. Target Domain (Sh2, Sh3)
5. Lemma — RetractionSelfFreshness

A reader following the document linearly encounters the corollary's proof before its supporting lemmas, with no warning that the citations are forward.

**Problem**: The forward references are logically non-circular (Sh1, Sh3, and RetractionSelfFreshness are proved without depending on this corollary), so soundness is intact. But linear readability is broken: the reader must skip past EffectiveWpSimplification, read sections 3–5, then return. The topological dependency order would have EffectiveWpSimplification appear last among the four.

**Required**: Either (a) reorder so EffectiveWpSimplification appears after RetractionSelfFreshness, placing the corollary in topological order; or (b) add a brief note at the corollary stating that the cited Sh1, Sh3, and RetractionSelfFreshness are proved in later sections without depending on this corollary, so the forward references are non-circular. Option (a) is preferred — the "wp discharge" narrative role is preserved without sacrificing linear readability.

### Issue 3: Retraction is the only shape in the canonical catalog without an inline walkthrough

**ASN-0094, Retraction section**: Seven of the eight canonical shapes (Classifier, Tuple-Classifier, DirectedPair via FDD, NonIdempotentDirectedPair via SHCD, Resolution, BundledDirectedPair, Provenance) have inline worked examples in their template-walkthrough subsections — each exercising Sh-conf admission, at least one rejection pattern, and template evaluation at a concrete state. The Retraction subsection describes templates and the bare-vs-attributed dichotomy but contains no walkthrough.

**Problem**: The K = comment worked example exercises retraction *as a tool* via Nullify (bare Emit_R with F = ∅), but no walkthrough exercises Retraction *as a shape* directly. The attributed-retraction variant (c_F ≥ 1 with distinct from-slot values) is described as the migration recipe for audit-multiset semantics — load-bearing because it is the framework's answer to the "set vs. multiset" semantic departure called out at the top of the document — yet it is not demonstrated anywhere. The asymmetry against the other seven shapes is salient.

**Required**: Add a brief inline walkthrough for Retraction (modeled after BundledDirectedPair's regime-exhibiting structure) showing at least: (i) bare emission (F = ∅), (ii) attributed emission with distinct from-slot values, (iii) Sh4 suppression at duplicate slot-pair attributed emissions, (iv) template evaluation at a state where bare and attributed retractions coexist. The migration recipe becomes concrete rather than abstract.

## OUT_OF_SCOPE

The Open Questions section enumerates several extensions appropriately scoped as future work: (0, 0) shape admissibility, Provenance split, idempotency as separable axis, per-K opt-in as sixth shape component, ghost-targeting slot semantics, composite shapes, cross-process consistency, A_M target-domain symbol, empty-link-store baseline relaxation. These are correctly flagged as design or refinement candidates rather than current revisions.

VERDICT: REVISE
