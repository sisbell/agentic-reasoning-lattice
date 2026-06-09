# Review of ASN-0126

## REVISE

### Issue 1: Gate soundness (P4) proven, gate completeness never stated

**ASN-0126, "The shape-gated emit" / "Properties established" (P4)**: "No `→_sh`-step extends `dom(Σ.L)` with a tuple `(F, G, K)` whose K is unregistered, nor with one for which `Sh-conf(K, F, G)` fails."

**Problem**: P4 establishes only the *soundness* direction of the gate — nothing bad gets in. The dual — that every *conforming* triple (registered K, arity 3, `Sh-conf = ⊤`) at an allocated home actually *fires* a `→_sh`-step depositing it at a fresh address — is nowhere stated as a property. It is the realizability claim on which the note's central promise ("a static shape-conformance check the substrate can apply at every emit") rests: if the gate could spuriously block a conforming emit, the framework is unusable. The note has every ingredient — it imports R0 (fresh-address emission) via `π`, and the gate `(0)∧(i)∧(ii)` is satisfied by any conforming triple — but the assembly "R0 produces the underlying `K.λ` step, and for a conforming triple that step satisfies `K.λ_sh`'s preconditions, hence is a `→_sh`-step" is left to the reader and demonstrated only by the worked illustration's firing emits. A Dijkstra review will not accept the liveness half by example when the safety half (P4) got a stated property and a wp derivation.

**Required**: State and prove a completeness/realizability lemma dual to P4 — e.g. "for any `→_sh`-reachable Σ, `d ∈ dom(Σ.M)`, registered K, and `(F, G)` with `Sh-conf(K, F, G)`, there exists `Σ'` with `Σ →_sh Σ'` depositing `(F, G, K)` at a fresh `a = a_emit(Σ, d)`." Name the premises (R0 at `π(Σ)`, gate satisfaction for conforming triples) and show the imported ungated `K.λ` step is in fact a `K.λ_sh` step. Without it, the wp derivation characterizes *when a fired emit lands active* but the note never closes the loop on *when an emit fires at all*.

## OUT_OF_SCOPE

### Topic 1: Degenerate empty registry
C0 admits `Σ_init.registry = ∅` (finite partial function, possibly empty), under which precondition (i) fails for every K and `dom(Σ.L)` never grows via `→_sh`. Whether the substrate ships a non-empty standard registration set is Open Question #4; the degenerate case is a real but harmless corner that belongs with that standardization question, not here.

VERDICT: REVISE
