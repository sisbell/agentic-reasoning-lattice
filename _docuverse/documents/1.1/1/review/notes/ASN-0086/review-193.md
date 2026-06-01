# Review of ASN-0086

## REVISE

### Issue 1: "Unit-depth retraction discipline" states a false equivalence — the ASN's own Worked Sketch is a counterexample

**ASN-0086, Definition — Unit-depth retraction discipline**: "A state Σ is *unit-depth-disciplined* iff every `(b, F', G') ∈ L_R^Σ` has to-endset `G' = {(t, δ(1, #t))}` for some target `t ∈ A_rel^Σ` — equivalently, every `L_R^Σ` tuple was produced by a *P1-satisfying* `Nullify(Σ, d_retr, t)` call (one whose target satisfies P1, `t ∈ A_rel^Σ`)."

**Problem**: The two characterizations are presented as equivalent, but only one direction holds. Characterization (2) ⟹ (1) is fine (a P1 target stays in `A_rel` by L12a, and Nullify builds a unit-depth span). The converse fails, and Worked Sketch Step 4 exhibits the counterexample inside this same document: the direct `Emit_R(Σ_3, d, ∅, {(a₃, δ(1, 8))})` deposits `(a₃, ∅, {(a₃, δ(1, 8))}) ∈ L_R^{Σ_4}`. At emission `a₃ = a_emit(Σ_3, d) ∉ A_rel^{Σ_3}` (the note states explicitly "This is *not* a relational-layer `Nullify`... `a₃ ∉ dom(Σ_3.L)`"), so the producing call is **not** P1-satisfying — characterization (2) fails. Yet at `Σ_4` the target `a₃ ∈ A_rel^{Σ_4}` and the span is unit-depth, so characterization (1) **holds**. Hence (1) ⇏ (2): `Σ_4`-like states are (1)-disciplined but not (2)-disciplined.

**Required**: Demote "equivalently" to a one-directional statement — (2) is sufficient for (1), not equivalent — or pin characterization (1)'s target-membership to the producing call's pre-state (matching P1's timing) so the two coincide. (The wp Case 2 derivation only consumes characterization (1)'s shape + `A_rel`-membership, so the result survives either fix; only the definition's claim of equivalence is wrong.)

### Issue 2: K-Step Conformance Preservation discharges clauses (b)/(c) only for K.λ

**ASN-0086, Lemma — K-Step Conformance Preservation (proof)**: "every K.σ/K.α/K.λ `→`-step satisfies (a) by its ASN-0093 invariant-preservation contract; (b) because each K.λ emits a single key at one home; and (c) because K.λ's first/subsequent emission rule deposits exactly `[d.0.s_L.1]`... or `inc(ℓ_prev, 0)`..."

**Problem**: The claim ranges over all three K-ops, but the justification for (b) and (c) names only K.λ. Clauses (b) (at-most-one-link-key-per-home) and (c) (frontier-landing) are *about* link-key emission; K.σ and K.α emit zero link keys, so they satisfy (b)/(c) vacuously — but the proof never says so, leaving the universally-quantified claim under-discharged for two of the three cases. This is exactly the "show each case" standard.

**Required**: State that (b) and (c) hold vacuously for K.σ and K.α because neither adds a fresh link key (so the "at most one"/"frontier-landing" obligations on link keys are trivially met).

### Issue 3: Forward-reference / meta-prose accretion (anti-bloat classifier)

**ASN-0086, Definition — Emit_K, partiality paragraph**: "Over a merely state-local-conforming Σ the emission can be undefined because the chain frontier may be ill-formed: were a non-frontier nested key (Remark — NestedLinkWitness) the apparent `ℓ_prev` at home `d`, the subsequent-emission `inc(ℓ_prev, 0)` would be off-chain..."

**Problem**: The `NestedLinkWitness` construction is re-narrated across four sites — the Remark itself, this Emit_K partiality paragraph, Definition — state-local-conforming state ("witnessed by the NestedLinkWitness construction above"), and wp Case 2 ("a state-local-conforming but non-substrate-conforming Σ of the kind Remark — NestedLinkWitness constructs"). This is the "multiple paragraphs in different sections defer to the same downstream location" and "prose around a definition explains *why* rather than *what*" pattern. The Emit_K paragraph in particular re-derives the off-chain failure mode rather than stating the domain ("Emit_K is total over substrate-conforming Σ, partial elsewhere").

**Required**: State the partiality fact once at Emit_K (total over substrate-conforming, partial over state-local-conforming, undefined where the frontier is ill-formed) and let the single `Remark — NestedLinkWitness` carry the construction; drop the re-narrations at the other three sites to a bare citation.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity of Emit vs Observe and ordering of Observe results
**Why out of scope**: The note's Open Questions already park these (consistency model, Observe ordering, atomicity). They are new territory requiring a transition-interleaving model this ASN does not introduce, not defects in the present static/`→*` development.

VERDICT: REVISE
