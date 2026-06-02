# Review of ASN-0086

## REVISE

### Issue 1: Nelson design-intent digression in the Nullified scope paragraph
**ASN-0086, Definition — Nullified, "Scope — retractors are standard-triple links only"**: "We record that this scoping is *narrower than Nelson's design intent*: Nelson attaches no behavioral semantics to link types and keys type-matching on the type endset's *address* alone, applying uniformly regardless of arity [LM 4/44]; a model that fixed a to-slot convention for higher arities could extend `nullified` to range over retraction-typed links of every `N ≥ 3`. The present note does not, confining retraction to the triple layer it formalizes."

**Problem**: This is essay content in a definitional slot. It imagines an alternative model the note explicitly does not build (a higher-arity to-slot convention) and editorializes on Nelson's design intent rather than advancing the definition's meaning. The earlier sentence "This exclusion is deliberate, not an oversight" is defensive justification of the same kind. The load-bearing content — that `coverage(G')` is undefined for `N > 3` links because the model fixes no canonical to-slot, so they cannot retract — is already stated immediately before this passage and survives without it.

**Required**: Cut the Nelson-intent sentence and the hypothetical-extension clause; keep only the operative statement that retractors are standard-triple links because the to-slot convention is defined only at arity 3. Drop "This exclusion is deliberate, not an oversight."

### Issue 2: Worked Sketch Step 4 exercises a Nullify call the relational-layer commitment forbids, unflagged
**ASN-0086, Definition — relational layer**: "the layer never invokes `Emit_K` at a type index `K ~ R` except through the `Nullify` alias at a P1 target (`a ∈ A_rel^Σ`)."
**ASN-0086, Worked Sketch, Step 4**: "`Σ_3 → Σ_4` via `Emit_R(Σ_3, d, ∅, {(a₃, δ(1, 8))})` — i.e. `Emit_K` at `K := R`... Here P0 holds while P1 is false (`a₃ ∉ dom(Σ_3.L)`)".

**Problem**: Step 4 is a `Nullify`/`Emit_R` invocation at `K ~ R` whose target `a₃` is **not** a P1 target (`a₃ ∉ A_rel^{Σ_3}`). The relational-layer commitment permits `Emit_K` at `K ~ R` only "through the `Nullify` alias at a P1 target." So this call is outside the layer's own discipline, yet it sits in the worked sketch beside Steps 1–3 (layer operations) with no marker that it is a direct/non-layer substrate caller. A reader tracking the commitment cannot tell whether the layer can self-nullify. (The wp Case 2 discussion does distinguish "a direct K.λ caller," but the sketch never connects Step 4 to that category.) Note also that the self-emit branch in fact *does* preserve the unit-depth discipline (the target `a₃` lands in `A_rel^{Σ_4}`), so the P1 qualifier in the commitment is stronger than the discipline requires.

**Required**: Either (a) explicitly label Step 4 as a direct, non-layer substrate caller, reconciling it with the commitment; or (b) relax the commitment's "at a P1 target" qualifier to cover the self-emit branch, since that branch also maintains the unit-depth retraction discipline. Make the sketch's framing consistent with the layer definition.

## OUT_OF_SCOPE

### Topic 1: Behavioral retraction semantics for higher-arity (`N > 3`) links
**Why out of scope**: Defining a canonical to-slot for `N > 3` links so they can serve as retractors is a genuine extension requiring a new arity convention; it belongs in a future ASN, not this triple-layer note. (This is the legitimate kernel of Issue 1 — the *extension* is future work; the *digression about it* is the bloat.)

VERDICT: REVISE
