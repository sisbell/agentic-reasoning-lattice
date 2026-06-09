# Review of ASN-0126

## REVISE

### Issue 1: The conditional wp-simplification conditions on layer-reachability, which is unsatisfiable under →_sh

**ASN-0126, The shape-gated emit (Disciplined-domain simplification)**: "*If* the substrate is additionally operated under ASN-0086's retraction discipline — so that its reachable states are layer-reachable — then the third conjunct holds vacuously..."

**Problem**: This antecedent is internally contradictory with the framework's own retraction. ASN-0086's `LayerReachable` is defined via the discipline commitment "every →-step that grows `L_R` is a `Nullify`," and `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1,#a))})` carries `F = ∅`. But the framework re-expresses retraction as the *attributed* `Emit_R(Σ, d_retr, [r], {(a, δ(1,#a))})` with `|F| = 1`, and Single-source states outright that ASN-0086's literal `F = ∅` Nullify "is **not** expressible under `→_sh`." An attributed retraction grows `L_R` but is not a `Nullify` (its F differs), so it violates ASN-0086's discipline commitment. Therefore **the moment any attributed retraction is emitted, the state is not layer-reachable.** The stated antecedent ("its reachable states are layer-reachable") thus holds only for substrates that emit *zero* retractions (where `L_R = ∅` and the third conjunct is trivially vacuous anyway). The "layer-disciplined sub-domain" the simplification claims to characterize is essentially empty.

**Required**: Condition instead on the property that actually drives the vacuity — ASN-0086's `UnitDepthRetractionDiscipline`, which constrains only the *to-span shape* (`G' = {(t, δ(1,#t))}`) and is F-agnostic. The framework's constructed retraction writes unit-depth to-spans, so a substrate that operationally restricts every retraction emit to that form satisfies the unit-depth discipline, R0a is inherited, and the third conjunct is vacuous — all without invoking layer-reachability or F=∅ Nullify. The parenthetical already cites "the unit-depth discipline with R0a"; the named condition must be brought into line with it.

### Issue 2: `Emit_retract` is undefined and contradicts the unit-depth-by-construction retraction

**ASN-0126, Worked illustration (Born nullified, Step 1)**: "Issue `Emit_retract(Σ₀, d, [c₁], G_rng)` with attributing source `[c₁]` ... and a *single* range span `G_rng = {(g, δ(3, #g))}`..."

**Problem**: `Emit_retract` is never defined, and its use with a non-unit-depth range `G_rng` conflicts with Single-source, which characterizes the framework's retraction as `Emit_R(Σ, d_retr, [r], {(a, δ(1,#a))})` that "writes a unit-depth to-span **by construction**." If `Emit_retract` is that constructed operation, Step 1 is illegal (it could not supply a range G). If it is the *generic* `Emit_R` at the registered Binary type R — which is what the example's point requires (showing the gate enforces Binary, not unit-depth) — then the name misleadingly connotes the constructed operation. A proof should not turn on an undefined operation whose name contradicts the section that introduces it.

**Required**: Either define `Emit_retract` explicitly as the generic gated `Emit_R` at type R (distinct from the constructed unit-depth retraction wrapper), or rename it (e.g., `Emit_R`) and state plainly that the example deliberately bypasses the unit-depth construction to exercise the gate's Binary-only enforcement.

### Issue 3: Decidability of precondition (i) needs a finite representative per registry key

**ASN-0126, Registration entries / C0**: "a *finite* partial function `T_admissible/~ ⇀ (name, shape, idem)`" and "deciding `coverage(K) = coverage(K_j)` against each of the finitely many registered `K_j`."

**Problem**: The registry's domain is coverage *classes* `[K]`, abstract objects. `CoverageEqualityDecidable` (ASN-0086) operates on *endsets*, and the decidability argument silently switches to "registered `K_j`" (endsets). A coverage class cannot be stored as its coverage set directly — by the ASN's own unsatisfiability argument, prefix-coverage sets are infinite and not finitely representable. So the static check of (i) depends on each entry carrying a finite *representative endset*, which C0's formalization does not state.

**Required**: State that each registry entry stores a finite representative endset `K_j` of its coverage class (the registry being a function `T_admissible/~ ⇀ ...` realized via representatives), so that `CoverageEqualityDecidable` applies to each comparison and the "static check at every emit" is genuinely decidable.

## OUT_OF_SCOPE

### Topic 1: Operational semantics of the idem flag, behavior catalog, standard registrations

The ASN correctly defers idem semantics, predicate composition, and whether R/`retired`/`supersedes` ship pre-registered (Open questions #1–6). These are successor-note territory, not defects here. P3 establishing idem's structural state-independence without operational consequence is acceptable forward-looking vocabulary scoping, not drift.

META: (none — the ASN defines a state component, a refined transition, a conformance invariant, and stability properties at specification level; it is on-track.)

VERDICT: REVISE
