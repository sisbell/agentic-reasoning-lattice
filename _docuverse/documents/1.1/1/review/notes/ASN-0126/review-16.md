# Review of ASN-0126

I checked the structural commitments (registry as fourth state component, the shape-gated emit `→_sh`, the six properties), the wp derivation, the P6 realizability proof, the projection bridge `π`, and the worked illustration's concrete arithmetic. The note is unusually self-aware: it anticipates the boundary cases a rigorous reviewer reaches for and discharges them in-text.

## REVISE

None. I attempted to break the following and each held:

- **Single-source vs. ASN-0086 Nullify (`F = ∅`).** The exclusion of the unattributed `F = ∅` branch is deliberate, justified, and the re-expressed `Emit_R(Σ, d_retr, [r], {(a, δ(1,#a))})` is shown Binary-conformant. The claim that `nullified`/`L_R`/active-subset machinery carry over is correct — all read `coverage(G')` only, which the from-slot change leaves untouched.
- **Binary ≠ unit-depth.** Correctly separated: registration gives Binary; unit-depth comes from the operation's construction. The conditional simplification is conditioned on `UnitDepthRetractionDiscipline`, *not* on `LayerReachable` — and the note correctly observes that the attributed (`|F|=1`) retraction leaves the layer-reachable fragment, so conditioning on layer-reachability would characterize an empty fragment.
- **wp Case 2 refinement.** `wp(g_sh → S, R) ≡ g_sh ∧ wp(S, R)` is the right guarded-command form (postcondition unattainable if the emit does not fire). Omitting arity guard (0) from the wp is sound: `(a,F,G) ∈ A_K^{Σ'}` forces `|Σ'.L(a)| = 3` via `L_K`'s arity-3 slice, so `wp(S,R) ⟹ (0)`.
- **Born-nullified worked example.** Arithmetic verified: `a_R = …2.3 ∉ coverage(G_rng) = […2.4, …2.7)` (no self-nullify); `a = g = …2.4 ∈ coverage(G_rng)` (born nullified). Demonstrates gate-vs-landing concretely, and the non-unit Binary R-emit is a genuine `→_sh`-step, so the witness lives in reachable space.
- **P6 proof.** The R0-vs-`Emit_K` distinction is load-bearing and handled: R0 gives *some* fresh on-chain address (all chain indices `> J_d` by L-ContiguousPrefix), while the `Emit_K` operation pins `a_emit`. `a_emit(π(Σ),d) = a_emit(Σ,d)` since `a_emit` reads only M/L, which `π` preserves. `K ∈ T_admissible` is correctly carried from the stored representative to the emitted slot.
- **Span-count measure.** The `|coverage(F)| = 1` rejection (unsatisfiable over `T` for prefix-coverage spans) is correct, and the abutting-span normalization burden is consistently applied to both `F` and Binary's `G`.
- **Registry decidability.** C0's finiteness + CoverageEqualityDecidable make precondition (i) terminating at every reachable state; P1 keeps the bound stable.
- **Conservative extension.** The projection argument correctly transfers ASN-0043/0086 C/M/L invariants; `→_sh` restricting `K.λ` cannot break a preserved invariant.

## OUT_OF_SCOPE

The note's six Open Questions (idem emit-semantics, behavior catalog, default predicates, standard registrations, predicate composition, F=1/N=3 extension) are correctly deferred — each layers operational meaning on top of the structural skeleton without revisiting it. The absent lower-bound G-floor (zero-target Multi) is correctly placed at the type-semantic layer, not the structural catalog. No future-territory item belongs in this revision.

VERDICT: CONVERGED
