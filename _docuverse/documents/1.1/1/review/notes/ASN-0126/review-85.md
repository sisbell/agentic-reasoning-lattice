# Review of ASN-0126

I worked the technical core hard — the three-move retraction-as-Binary argument (frame-the-two-post-states), the born-nullified worked scenario's address arithmetic (`a_R = …2.3`, `g = …2.4 ∈ coverage(G_rng) = […2.4, …2.7)`), P5's manual lift of `Emit_K`'s `K.λ` step back to `K.λ_sh`, and the C2/C3 liveness split in the wp. These hold up. The single finding below is prose, surfaced under the note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: The construction-time registration paragraph circles one fact four times and closes with terminology meta-prose

**ASN-0126, "The registry"**: The paragraph beginning "Registration is confined to the construction of `Σ_init`…" states the same fact — registration is a construction-time act, immutable thereafter — across four consecutive sentences:

- "Registration is confined to the construction of `Σ_init`: an app *declares* a type by placing its `[K_j] ↦ shape` entry in `Σ_init.registry` before the dynamics begin."
- "The framework supplies **no** runtime registration operation — the operation set is the inherited `{Emit_K, Observe_K, Nullify}` … and none of these writes the registry."
- "The registry is therefore a fixed *input* to the dynamics: though carried as a component of `Σ`, no reachable state revises it (P1, Registry permanence)."
- "Every mention below of an app 'declaring' or 'registering' a type refers to this construction-time act, never to a runtime event."

The fourth sentence is pure terminology meta-prose: it instructs the reader how to read a word rather than advancing the argument — exactly the accretion to skip past. The load-bearing content is two sentences: registration populates `Σ_init.registry`; no operation in the set writes it post-construction, hence P1.

**Problem**: This is the forward-reference accretion the classifier names. The git history shows a recent revise stacked clarifications precisely here ("clarify registry is construction-time only, no runtime registration"), and the result is one fact restated until the last sentence is no longer carrying meaning. (The same point recurs at the empty-registry remark in *Worked illustration* — "no type registered at construction and no runtime registration to add one" — but there it is load-bearing for the permanently-inert conclusion and should stay.)

**Required**: Collapse to the two load-bearing sentences (registration writes `Σ_init.registry` only; no operation writes it after construction, hence P1). Delete the "Every mention below…" sentence — immutability is already pinned by P1 and needs no reading instruction.

## OUT_OF_SCOPE

### Topic 1: Disjoint-region sources

The `|F| = 1` rule forces the source to one *contiguous* span (or subtree). An app whose source is genuinely two disjoint regions cannot register under any shape — it would need `|F| ≥ 2`, which fails Unary/Binary/Multi alike. This is a real expressiveness boundary, but it is correctly deferred: Open Question 6 ("Extension beyond F=1 and N=3") owns the path that would loosen `|F| = 1`. Not an error here.

### Topic 2: Observe under the shape framework

The note refines emit (`K.λ_sh`) but leaves `Observe_K` unchanged. Whether shape unlocks read-side behaviors (typed-reverse-lookup, read-filter) is the note's own Open Question 2 (behavior catalog). Appropriately future.

VERDICT: REVISE
