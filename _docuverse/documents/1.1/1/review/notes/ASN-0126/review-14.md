# Review of ASN-0126

## REVISE

### Issue 1: P6 deposits at "some fresh key," not the named `a_emit(Σ, d)`

**ASN-0126, P6 (GateRealizability) proof, step 2**: "R0 at home `d` ... yields an ASN-0086 step `π(Σ) → Σ_{0086}` depositing `(F, G, K)` at the fresh `a = a_emit(π(Σ), d)`."

**Problem**: R0 (ASN-0086) is existential in its address — it delivers *some* `a` that is "fresh against `dom(Σ.L)` and on-chain in `A_L(d)`." By L-ContiguousPrefix the homed set is a contiguous initial segment `{inc^j(...) : 0 ≤ j ≤ J_d}`, so the fresh on-chain addresses are *all* `j > J_d` — infinitely many. `a_emit` is specifically the least such (`inc(ℓ_prev, 0)`, i.e. `j = J_d+1`); R0 does not pin it. Worse, the bridge step `K.λ_sh` is `K.λ`, and ASN-0086's StateTransition says a K.λ-step extends `dom(Σ.L)` "at a fresh key" — not at `a_emit`. The `a = a_emit` binding lives in the **Emit_K operation**, not in the `K.λ` transition the proof actually lifts. So the proof establishes firing-at-some-fresh-key, while P6's conclusion (and the Worked illustration's address arithmetic, e.g. `a_emit(Σ₀,d) = inc(ℓ₂,0) = ...2.3`) commits to `a_emit` precisely.

**Required**: Either invoke the Emit_K operation (which fixes `a = a_emit`) rather than the bare R0/`K.λ` step, or weaken P6's claim to "at some fresh on-chain address `a ∈ A_L(d)`." If the former, state why the gated transition realizes the `a_emit` choice rather than an arbitrary fresh sibling.

### Issue 2: Non-emptiness shown for the representative `K_j`, not the emitted `K`

**ASN-0126, P6 proof, step 1**: "the registry stores a finite representative endset `K_j ∈ T_admissible` of K's coverage class; `T_admissible` is the non-empty endsets, so the type slot is non-empty — discharging ... L3's non-empty-type-slot clause."

**Problem**: The emitted triple's type slot is `K`, not the stored representative `K_j`. The proof shows `K_j ≠ ∅` but L3 / R0's `K ∈ T_admissible` requirement is about `K`. The missing step: "K registered" means `coverage(K) = coverage(K_j)`; since every span has `ℓ > 0`, `coverage(K_j) ≠ ∅`, hence `coverage(K) ≠ ∅`, hence `K ≠ ∅`. Without it the conclusion is asserted of the wrong object.

**Required**: Insert the one-line coverage argument carrying non-emptiness from `K_j` to the emitted `K`.

### Issue 3: Cross-ASN reference to a non-foundation ASN

**ASN-0126, C0 finiteness paragraph**: "parallels L-fin (LinkStoreFiniteness, ASN-0043) and S8-fin (FiniteArrangement, ASN-0036)."

**Problem**: ASN-0036 is not among the foundation ASNs (only ASN-0043 and ASN-0086 are). Per the self-containment rule, a numbered reference to a non-foundation ASN must be flagged. The reference is a non-load-bearing analogy — the finiteness commitment stands on C0 alone.

**Required**: Drop the ASN-0036 citation (the L-fin parallel to a foundation ASN suffices), or restate the analogy without the external ASN number.

## OUT_OF_SCOPE

### Topic 1: Operational guarantee of unit-depth retraction
The ASN is explicit that Binary registration of R does not enforce ASN-0086's UnitDepthRetractionDiscipline, leaving R-Scope's single-tuple-scope dependent on the operation's construction rather than the gate. Whether the substrate should *also* gate R's to-span shape (not just span count) is a coherent design question, but it belongs to the operational successor, not this structural framework.

### Topic 2: Idem semantics, type-semantic floors (`1 ≤ |G|`), standard registrations
The note correctly defers idem behavior, the per-type lower-bound discipline, and which types ship pre-registered to the named successor note (Open questions #1, #4). These are layered concerns, not gaps in the structural catalog.

VERDICT: REVISE
