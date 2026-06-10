# Review of ASN-0126

The core is sound. P1, P3, P5, P6, the projection bridge, the wp refinement, and the worked illustration all check out — I verified the worked addresses arithmetically (`g = 1.1.0.1.0.1.0.2.4`, `δ(3,9)` ranges over `[…2.4, …2.7)`, `a_emit` chain `…2.1 → …2.2 → …2.3 → …2.4`) and the "born nullified" wp trace. The issues are localized to the retraction transfer and one state component.

## REVISE

### Issue 1: Single-tuple-scope transfer drops R-Scope's P-tgt hypothesis, which the gate does not enforce

**ASN-0126, "Retraction as an attributed Binary"**: "R-Scope's single-tuple-scope result `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` holds only when the app routes every retraction through the unit-depth wrapper, which writes the canonical `{(a, δ(1, #a))}` to-span by construction." and "its conclusion … transfers verbatim to our four-component `→_sh*`-reachable Σ."

**Problem**: R-Scope (ASN-0086) carries the hypothesis P-tgt — `a ∈ A_rel^Σ` *or* `a = a_emit(Σ, d_retr)`. The note carefully flags one weakening relative to ASN-0086's UnitDepthRetractionDiscipline (Binary admits non-unit G), but misses a second: the framework's Binary gate enforces only `|F| = |G| = 1`, **not** P-tgt. The unit-depth wrapper is therefore *necessary but not sufficient* for single-tuple-scope — the target must also satisfy P-tgt.

Concretely, in the note's own address space take the ghost prefix `a = 1.1.0.1.0.1.0.2` (`#a = 8`, `zeros(a) = 3`, but `#E(a) = 1`, so `a ∉ dom(Σ.L)` and `a ≠ a_emit`; P-tgt fails). The wrapper `Emit_R(Σ, d, {r}, {(a, δ(1, #a))})` has `|F| = |G| = 1`, so it **clears the Binary gate**, yet `coverage({(a, δ(1, #a))}) = {t : a ≼ t}` covers `ℓ₁, ℓ₂, …` — the *entire* link subspace of `d`. So `{t : a ≼ t} ∩ A_rel^{Σ'} ⊇ {ℓ₁, ℓ₂, …} ≠ {a}`: single-tuple-scope fails catastrophically, and nothing in `→_sh` rejects the call. A reader who concludes "use the unit-depth wrapper ⟹ single-tuple-scope" is wrong.

**Required**: State P-tgt explicitly as a condition on the wrapper's target, and say plainly that the gate does not discharge it — single-tuple-scope is an *app obligation* (supply a P-tgt-valid target), not a `→_sh` guarantee. Put it alongside the non-unit-G weakening that is already acknowledged.

### Issue 2: The R-Scope transfer mis-cites B2 and uses `Σ'` before binding it

**ASN-0126, "Retraction as an attributed Binary"**: "By the projection bridge, R-Scope holds at the `→*`-reachable `π(Σ)` (B2), and — constraining only the post-state link-address set `A_rel^{Σ'}` and the fixed target subtree `{t : a ≼ t}` — its conclusion transfers to Σ (B1, `A_rel^{π(Σ')} = A_rel^{Σ'}`)."

**Problem**: B2 transfers an ASN-0086 result that is "a predicate of a single `→*`-reachable state, or of a transition between two states each separately exhibited as `→_sh`-reachable." R-Scope is a *transition* result about the empty-from `Nullify`, whose post-state is **not** `→_sh`-reachable — the note itself establishes that empty-from Nullify has no `→_sh` image. So B2's conditions are not met; B2 does not apply to R-Scope's transition. What actually carries the result is the frame argument in the next sentence (same fresh address ⟹ identical post-state link domain), used purely at the ASN-0086 level and then lifted. Separately, `Σ'` in `A_rel^{π(Σ')} = A_rel^{Σ'}` is referenced before the frame argument introduces it as the wrapper's post-state.

**Required**: Recast the justification: R-Scope holds at the ASN-0086 state `π(Σ)` and its Nullify post-state (by ProjectionBridge, `π(Σ)` is `→*`-reachable — *not* B2); the frame argument equating link domains is the load-bearing step that carries the conclusion to the wrapper's `→_sh`-reachable post-state. Bind `Σ'` before using it, and drop the B2 citation here.

### Issue 3: The `name` component carries a permanence guarantee with no read path

**ASN-0126, "The registry"**: "a **name** — opaque payload the framework never reads; only keys are constrained unique (below), so names may collide, and a name never drifts (P1, Registry permanence)".

**Problem**: `name` is part of the formal state (`Σ.registry` value) and P1 is invoked to guarantee it "never drifts," yet no operation reads or exposes a name (Observe_K returns only `(a, F, G)`), and names may collide. A permanence guarantee about a component the framework provides no way to observe is vacuous. Contrast `shape`: P2's stability is operationally observable through emit success/failure, so it is a meaningful guarantee.

**Required**: Either expose a name-lookup (making P1's name-permanence meaningful), or state that names are out-of-band app metadata the substrate carries but never interprets — and in that case justify why a never-read, collision-permitting field sits in the formal state tuple rather than app-layer, and drop the "never drifts" framing for it.

## OUT_OF_SCOPE

### Topic 1: A gate-enforced unit-depth retraction shape
A fourth shape whose conformance requires `G = {(t, δ(1, #t))}` with `t` a live link address would make single-tuple-scope a *framework* guarantee rather than an app discipline (the fix for Issue 1 is to surface the obligation; *enforcing* it is a new shape). **Why out of scope**: a new registrable shape is additive design, not a defect in the present catalog.

### Topic 2: Registry introspection operations
Operations letting an app read back its registered shape/name (beyond inferring shape via emit behavior). **Why out of scope**: the note's contribution is the gate and the immutable registry; an introspection operation set is a successor concern (Open Question 2 neighborhood).

### Topic 3: Post-init / dynamic registration
Every guarantee (P1–P6) rests on the registry being fixed at `Σ_init`. Adding types after init is a structurally different framework. **Why out of scope**: genuinely a parallel note, gestured at by Open Question 4.

VERDICT: REVISE
