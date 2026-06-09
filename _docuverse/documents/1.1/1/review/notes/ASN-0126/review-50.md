# Review of ASN-0126

The mathematics here is sound. I checked the gate definition, the wp derivation (`g_sh ∧ wp_{0086}` via the guarded-command rule), the projection bridge, P1–P6, and the worked illustration's address arithmetic (the `a_emit` chain `ℓ₁ → ℓ₂ → a_R → g`, the `coverage(G_rng) = {t : …2.4 ≤ t < …2.7}` computation, and the born-nullified trace through the inherited third wp conjunct). All hold. The findings below are precision and accreted-prose issues, which is what the `anti-bloat` classifier predicts.

## REVISE

### Issue 1: "single point" overstates `→_sh`'s compatibility with ASN-0086
**ASN-0126, Single-source**: "The single point where this bites ASN-0086's own vocabulary is retraction."
**Problem**: The `|F| = 1` rule removes *every* empty-from emit, not just Nullify. ASN-0086's `Emit_K : Σ × dom(Σ.M) × Endset × Endset → …` is total over `Endset × Endset`, and `∅ ∈ Endset`, so `Emit_K(Σ, d, ∅, G)` is a legitimate ASN-0086 invocation with no `→_sh` image. More concretely, R5(c) (TupleSelfTargeting, ASN-0086) is a *proven lemma* constructing `(∅, G_self, K)` — an empty from-set — which `→_sh` also excludes. Retraction is the only *named operation whose definition hardcodes* `F = ∅`, but "the single point where this bites" is false: the restriction is general.
**Required**: Scope the claim — e.g., "Nullify is the only named operation whose definition fixes `F = ∅`; the `|F| = 1` rule additionally excludes every empty-from `Emit_K` call (and R5(c)-style empty-from self-targeting) that ASN-0086 admits."

### Issue 2: the Σ_init-construction sentence is stated twice, verbatim
**ASN-0126, The shape-gated emit** vs **Registry permanence**:
- (gated emit) "the framework constructs its `Σ_init` by adjoining the registry to ASN-0086's initial three components and altering none of them, so `π(Σ_init) = Σ_init^{0086}` exactly"
- (permanence) "The framework constructs `Σ_init` by adjoining the registry to ASN-0086's three initial components, altering none of them; in particular its base link store is empty, `Σ_init.L = ∅` …"

**Problem**: Two sections in different words state the same construction. This is the "two paragraphs say the same thing" pattern. The projection bridge needs `π(Σ_init) = Σ_init^{0086}`; the permanence proof needs the same fact for P1's base case.
**Required**: State the construction once and reference it from the other site.

### Issue 3: P1–P6 are forward-referenced before they are stated, then restated
**ASN-0126, Properties established** and its forward references
**Problem**: The body refers to "(P4)" (Shape-conformance), "P3"/"P5" (The shape-gated emit), "P1"/"(P2)" (Registry permanence) — all *before* the trailing "Properties established" section that first states them, forcing the reader forward to learn what each symbol denotes. Worse, several are then doubly stated: P1's content is already concluded in Registry permanence ("So for every Σ reachable from Σ_init, `Σ.registry = Σ_init.registry`"), and **P5 is given its full formal statement and proof** in "Gate realizability" and then re-stated in prose in the summary. This is bidirectional deferral churn.
**Required**: State each property at its derivation site (or first mention) so the body is self-contained; where a property is already concluded in the body (P1, P5), reduce the summary entry to the derivation pointer rather than re-stating it.

### Issue 4: "domain-discharge ordering" is meta-prose around the gate
**ASN-0126, The shape-gated emit**: "These are read left-to-right under the **domain-discharge ordering**: (0) and (i) jointly discharge the domain condition for (ii). … A value failing arity-3 (0) or registration (i) is simply not a `→_sh`-step; the conformance test (ii) is never reached."
**Problem**: The well-definedness of (ii) (since `Sh-conf` is partial) is a real point, but it is one sentence: "(0) fixes `F, G` as the only content slots and (i) supplies `shape(K)`, so `Sh-conf(K, F, G)` is well-defined when reached." The named "domain-discharge ordering," the "read left-to-right" framing, and the closing sentence — which merely restates the short-circuit already entailed by the gate definition — are accreted elaboration that the reader must pass over.
**Required**: Compress to the well-definedness sentence; drop the naming and the restated short-circuit.

### Issue 5: `|e|` is defined twice, once with a self-satisfying forward reference
**ASN-0126, Single-source** vs **Shape-conformance**:
- (Single-source) "where for an endset `e` we write `|e|` for its *span count*, the number of spans `e` contains (Shape-conformance)."
- (Shape-conformance) "`Endset = 𝒫_fin(Span)` (ASN-0043) … so `|e|` is its cardinality as that set."

**Problem**: `|e|` is defined inline in Single-source *and* the same sentence forward-references "(Shape-conformance)" as though the definition lived there — then Shape-conformance defines it again. The forward pointer is redundant with the inline definition it accompanies. (The same Shape-conformance section also states span-count state-independence twice: "Counting spans-as-emitted keeps the measure … state-independent (P4)" and "The predicate therefore depends only on the tuple's span counts …, evaluable identically at any reachable state.")
**Required**: Define `|e|` once, at first use, and drop the forward reference; remove one of the two state-independence statements.

## OUT_OF_SCOPE

### Topic 1: runtime / dynamic type registration
The registry is immutable by design (P1), so the entire type vocabulary must exist at `Σ_init`. A registration operation that extends the registry at a reachable state is genuine new territory (Open Question 4 already gestures at it). Not an error in this note.

### Topic 2: a substrate-enforced single-tuple-scope retraction shape
The note registers R as Binary, which is "strictly weaker than ASN-0086's UnitDepthRetractionDiscipline," and leaves single-tuple scope to app discipline through the unit-depth wrapper. A future shape that *gates* `G = {(a, δ(1, #a))}` (unit-depth) at the substrate would restore R-Scope's guarantee structurally. This is honestly flagged here and belongs in the successor note.

VERDICT: REVISE
