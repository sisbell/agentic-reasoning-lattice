# Review of ASN-0126

## REVISE

### Issue 1: The declared operation set lists an inherited `Nullify` that has no `→_sh` image

**ASN-0126, "The registry"**: "The *operation set* — the methods an app invokes against the link store — is the inherited `{Emit_K, Observe_K, Nullify}` (ASN-0086)."

**Problem**: The note's own dynamics retire this `Nullify`. In "The shape-gated emit" it proves that "ASN-0086's `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` ... has no `→_sh` image" — precondition (ii) fails because `|F| = 0`. "Retraction as an attributed Binary" then realizes retraction through a *different* operation, the Binary wrapper `Emit_R(Σ, d_retr, {r}, {(a, δ(1, #a))})`, which is an instance of `Emit_K`, not of `Nullify`. So the declared set simultaneously (a) lists a dead operation — an app invoking the inherited `Nullify` produces no transition at *any* `→_sh`-reachable state — and (b) omits the live retraction operation the framework actually supplies. An implementer who builds `Nullify` to the inherited spec ships a method that always fails the gate. The inconsistency is compounded one sentence later: "Neither these operations [incl. `Nullify`] nor any of `→_sh`'s three steps writes the registry" treats `Nullify` as a live step kind, which the note elsewhere denies.

**Required**: Reconcile the operation-set declaration with `→_sh`. Either (i) drop the inherited empty-from `Nullify` and name the Binary `Emit_R` wrapper as the framework's retraction operation, or (ii) state at the point of declaration that inherited `Nullify` has no `→_sh` image and is superseded by the wrapper (defined in "Retraction as an attributed Binary"), so that the set apps actually invoke is `{Emit_K, Observe_K, Nullify_Binary}`.

### Issue 2 (minor, wording): "K.σ and K.α are unchanged" is contradicted by the registry-framing added later

**ASN-0126, "The shape-gated emit"**: "K.σ and K.α are unchanged."
**ASN-0126, "Registry permanence"**: "We extend every step's frame condition with the registry as an additional framed component: K.σ: `Σ'.C = Σ.C`, `Σ'.L = Σ.L`, `Σ'.registry = Σ.registry`; K.α: ... `Σ'.registry = Σ.registry`; ..."

**Problem**: K.σ and K.α each gain the frame conjunct `Σ'.registry = Σ.registry`, so they are not literally "unchanged." The intended claim — that only `K.λ` is refined into a new step kind, with K.σ/K.α keeping their preconditions and C/M/L effects — is recoverable, but the bald "unchanged" is walked back, and P1's proof in fact *relies* on K.σ/K.α framing the registry.

**Required**: Qualify, e.g.: "K.σ and K.α keep their preconditions and C/M/L effects; like K.λ_sh they additionally frame the registry (Registry permanence)."

## OUT_OF_SCOPE

### Topic 1: A gate that enforces the unit-depth retraction discipline

"Retraction as an attributed Binary" correctly shows Binary registration is strictly weaker than ASN-0086's UnitDepthRetractionDiscipline in two independent ways, so single-tuple-scope becomes an app obligation (route through the unit-depth wrapper **and** supply a P-tgt-valid target), not a guarantee `→_sh` discharges. Restoring that guarantee at the substrate — a dedicated retraction shape pinning both `|G| = 1` and the `{(a, δ(1, #a))}` form, or a discipline-enforcing gate — is a genuine future direction.
**Why out of scope**: This framework's remit is the shape catalog, the static gate, and the immutable registry; enforcing operation-specific disciplines is operational semantics, which the note explicitly defers to its successor (Open questions). The regression is honestly flagged and assigned, not hidden.

---

The proof content is in good shape. I checked the inductions for P1–P6, ProjectionBridge, RegisteredAdmissible, and the three-move R-Scope transfer for the Binary wrapper (the "frame the two post-states together" step — `a_emit` blind to F, hence `dom(π(Σ').L) = dom(Ψ.L)` — is the load-bearing move and is sound). The worked-illustration arithmetic is correct, including the born-nullified address chain (`a_R = ...2.3`, `a = g = ...2.4 ∈ coverage(G_rng) = [...2.4, ...2.7)`) and the ghost-root counterexample (`a = ...0.2`, `#E(a) = 1`, so P-tgt fails on both disjuncts). The wp derivation correctly isolates C3 as the newly-live conjunct under `→_sh`. The findings above are about definitional consistency and one wording fix, not proof errors.

VERDICT: REVISE
