# Review of ASN-0126

I worked the substance first. The core results hold up: P3's "only `K.λ_sh` extends `dom(Σ.L)`" argument is correct against the `→_sh ≡ K.σ ∪ K.α ∪ K.λ_sh` frame conditions; Lemma (RegisteredAdmissible) correctly transfers non-emptiness through `coverage(K) = coverage(K_j)`; the wp derivation legitimately factors as `g_sh ∧ [ASN-0086 Case-2 RHS]` and correctly identifies C3 as the conjunct *newly* live once Single-source admits non-unit retraction to-spans; P5's lift (run ungated `Emit_K` at `π(Σ)`, relabel as `K.λ_sh` using the premises) is sound; and the worked illustration's addresses all check (`a_R = …2.3 ∉ coverage(G_rng) = […2.4, …2.7)`, the citation lands at `g = …2.4 ∈ coverage(G_rng)` and is correctly born nullified). The boundary cases I probed — empty registry (gate (i) always fails, `dom(Σ.L)` frozen empty, P6 vacuous), arity > 3 (blocked by (0), deferred to OQ6), `~`-equal unregistered K (registration is by coverage class, so it *is* registered) — are all handled.

The findings below are the anti-bloat residue the `review-mode.anti-bloat` classifier asks for, not correctness gaps.

## REVISE

### Issue 1: "Properties established" verbatim-restates P1–P6
**ASN-0126, Properties established**: "**P3 (Sh-confWellFormedness)** — every value a `→_sh`-step adjoins to `dom(Σ.L)` is a standard triple `(F, G, K)` whose K is registered and for which `Sh-conf(K, F, G) = ⊤`; the gate admits no shape-violating tuple."

**Problem**: Every bullet here is (near-verbatim restatement of the home-section property) + (app-facing gloss). Compare P3's home statement under *The shape-gated emit*: "Every value a `→_sh`-step adjoins to `dom(Σ.L)` is a standard triple `(F, G, K)` whose K is registered and for which `Sh-conf(K, F, G)` holds." That is the same sentence twice. P1, P2, P4, P5, P6 are likewise each stated formally in their home section and re-stated here. This is the anti-bloat pattern "two paragraphs in the same document say the same thing in different words," with the only new content being motivational essay glosses ("never drift out from under it," "an app may read the link store and assume conformance without re-validating") sitting in a terminal structural slot.

**Required**: Pick one home for each property statement. Since the note's purpose is the app-facing contract, the cleanest fix is to let "Properties established" be the *single* statement-plus-gloss home for each P, and have the proof sections open with "P_n (stated in Properties established) — *Proof.*" rather than re-stating the property verbatim before proving it. (Or the reverse.) Do not state any property twice.

### Issue 2: forward-cite over-justifies a definitional fact in the wp derivation
**ASN-0126, The shape-gated emit**: "while leaving the C/M/L effect and the fresh address `a_emit(Σ, d)` identical (the projection argument below: a `K.λ_sh`-step acts on C/M/L exactly as `K.λ`)."

**Problem**: That `K.λ_sh` has the same C/M/L effect as `K.λ` is true *by definition* — `K.λ_sh` is "`K.λ` with three added preconditions," and adding preconditions cannot change the effect. The note itself says exactly this two clauses later ("its three added preconditions (0), (i), (ii) only *restrict* when it fires, leaving its C/M/L effect and frame identical to `K.λ`'s"). Citing "the projection argument below" to support it is a forward reference to a lemma that is in fact a *downstream consequence* of this definitional fact, not its justification — the dependency runs backwards. The projection bridge does real work in P5/P6; it does not need to be borrowed here.

**Required**: Drop the parenthetical forward-cite and let the identity stand as definitional ("identical by construction, since `K.λ_sh` adds only preconditions to `K.λ`").

## OUT_OF_SCOPE

### Topic 1: width-bounding discipline to recover single-tuple scope
Registering R as Binary deliberately weakens ASN-0086's UnitDepthRetractionDiscipline, so R-Scope's `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` no longer holds for range retractions — the "Born nullified" example shows a single Binary R-tuple pre-emptively nullifying a not-yet-allocated address. **Why out of scope**: the note correctly exhibits the *mechanism* and tells apps to route through the unit-depth wrapper when they want single-tuple scope; whether the substrate should additionally offer a width-bounding retraction *discipline* (rather than leaving it to per-app convention) is operational-semantics policy, properly deferred to the successor note already named in Open Questions 1–2.

VERDICT: REVISE
