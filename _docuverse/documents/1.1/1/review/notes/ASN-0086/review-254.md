# Review of ASN-0086

## REVISE

### Issue 1: Unit-depth-discipline discharge has a non-exhaustive case split and rests on a dual-phrased commitment

**ASN-0086, "Definition — relational layer" and the discharge paragraph following "Definition — layer-reachable"**: "Its one *discipline commitment* constrains only the type-`R` growth of `Σ.L`: every `L_R`-growing step is a `Nullify` — the layer never invokes `Emit_K` at a type index `K ~ R` except through the `Nullify` alias." … "Hence by the commitment, every transition that grows `L_R` is an `Emit_K` at `K ~ R`, i.e. a `Nullify`."

**Problem**: The commitment is stated in two non-equivalent phrasings joined by an em-dash. The first clause — "every `L_R`-growing step is a `Nullify`" — is strong enough to exclude a *raw* arity-3 `K.λ` step at a type coverage-equivalent to `R` with a non-unit-depth to-span. The second clause — "never invokes `Emit_K` at `K ~ R` except through `Nullify`" — constrains only `Emit_K` *invocations*, and a raw `K.λ` step (which `→ ≡ K.σ ∪ K.α ∪ K.λ` admits) is not an `Emit_K` invocation. The discharge then enumerates step kinds (K.σ/K.α, `Emit_K` at `K ≁ R`, higher-arity K.λ) but **omits the case of a raw arity-3 `K.λ` at `K ~ R` not routed through `Emit_K`/`Nullify`**, concluding "every transition that grows `L_R` is an `Emit_K` at `K ~ R`." That conclusion follows only under the strong reading of the commitment, not under the `Emit_K`-only elaboration the discharge actually cites.

This is load-bearing: the wp Case 2 derivation explicitly invokes "Disciplinedness — derived for layer-reachable states … gives that no pre-existing retraction covers the fresh `a`." If a layer-reachable trajectory could contain a raw deep-to-span type-`R` `K.λ` (e.g., a to-span rooted at a document prefix covering everything under it), that coverage could contain the fresh emission address, and wp Case 2's "no pre-existing retraction nullifies `a`" step would fail.

**Required**: State the commitment once, as a single predicate over every `L_R`-growing `→` step (not over `Emit_K` invocations), or restrict "layer-reachable" so that all link-store emissions route through the layer's operation set `{Emit_K, Observe_K, Nullify}`. Then add the omitted case to the discharge's case split: explicitly exclude (or handle) a raw arity-3 `K.λ` at `K ~ R`.

### Issue 2: `addr` onto-ness is non-advancing meta-prose repeated three times

**ASN-0086, "Definition — TypedRelation", "Definition — TupleAddress", and the Properties table (`addr` row)**:
- TypedRelation: "higher-arity links (`|Σ.L(a)| > 3`), which then inhabit `A_rel^Σ = dom(Σ.L)` but index no tuple of any `L_K`."
- TupleAddress: "The map is an *injection into* the codomain … with image the arity-3 slice … onto-ness is governed by the higher-arity carve-out of *Definition — TypedRelation* (onto exactly when that carve-out is empty)."
- Properties table: "injection into codomain … onto-ness per the TypedRelation higher-arity carve-out."

**Problem**: The substantive content of `addr` is that it is an injection. The onto-ness aside ("onto exactly when that carve-out is empty") adds nothing to any downstream argument and is restated across three locations, with TupleAddress and the table both deferring to the TypedRelation carve-out. This is the "definition's introduction enumerating downstream consumers / two paragraphs saying the same thing" pattern the anti-bloat classifier targets — a reader must skip past the onto-ness chatter to reach the load-bearing injectivity fact.

**Required**: State `addr` is an injection with image the arity-3 slice, once, in the definition. Drop the onto-ness parenthetical from TupleAddress and the table unless onto-ness is actually consumed by a later claim (it is not).

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity model for `Emit` vs `Observe`
**Why out of scope**: ASN-0093's SequentialTransitionAxiom gives serialized atomic transitions; a consistency model under which concurrent `Observe` sees `A_K` transitions is genuinely new territory (already noted by the author in Open Questions), not an error in this note.

### Topic 2: Cardinality bound of `nullified(Σ)` relative to `dom(Σ.L)`
**Why out of scope**: Whether unbounded retraction is permitted or some structural ratio must hold is a new invariant for a future ASN; this note correctly leaves it open.

VERDICT: REVISE
