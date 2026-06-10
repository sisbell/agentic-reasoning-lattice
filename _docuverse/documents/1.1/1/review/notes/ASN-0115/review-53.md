# Review of ASN-0115

I worked each of R0–R11 and the Confinement lemma against the substrate. The mathematics is sound: Confinement discharges cleanly from T5; R6's no-interior-hole rests correctly on D-SEQ★ contiguity; R7's active-set agreement correctly handles the non-empty-restriction-but-override case and the comparability requirement for S0; R8's subspace-sharing and link-vacuity (CL-OWN + CL-UNIQ) are valid; R11's wp is genuinely non-trivial. Worked instances, wp analysis, and explicit derivations are all present. One consequential choice is left unmotivated.

## REVISE

### Issue 1: The `act` override forces empty without rationale, despite subspace-wide consequences

**ASN-0115, "What a spec-set is" (act definition)**: "In the override branch — any consulting-state depth mismatch, `V_S(d) ≠ ∅ ∧ #s ≠ m_S(d)` — the active set is forced empty, *overriding* the geometric `dom(Σ.M(d)) ∩ ⟦σ⟧`."

**Problem**: The note motivates making `depthcompat` *consulting-state* ("`m_S(d)` is mutable — ASN-0047 re-pins a cleared subspace"), but the force-empty *override* — returning `∅` rather than the geometric intersection — is asserted definitionally with no reason. This is the one place RETRIEVEV's denotation is non-obvious, and the stakes are dramatic, not cosmetic. When `#s < m_S(d)` the geometric intersection is generally non-empty, and in the worst case it is the *entire* subspace: take `m_S(d) = 3`, so by D-SEQ★ `V_S(d) = {[S,1,k] : 1 ≤ k ≤ n_S}`, and a depth-2 spec with start `s = [S,1]` and any ordinal width `[0,w]` (`w ≥ 1`). Then `[S,1] ≺ [S,1,k]` and `[S,1,k] < [S,1+w]` for every `k`, so `V_S(d) ⊆ ⟦σ⟧` and `dom(M(d)) ∩ ⟦σ⟧ = V_S(d)` — geometrically the whole subspace — while the override delivers nothing. The note explicitly flags that it is "overriding the geometric `… ∩ …`" (so it recognizes the choice is non-trivial) yet never says why force-empty is the correct denotation rather than the equally-definable geometric one. The omission is conspicuous precisely because the note motivates its other choices (ordinal-level via Confinement, consulting-state via `m_S` mutability) — force-empty is the lone consequential branch left bare.

**Required**: One clause grounding the choice — that force-empty regularizes an otherwise discontinuous geometry (a depth-2 start at `[S,1,…,1]` would capture the entire subspace while a depth-2 start at `[S,2]` captures nothing), and that a spec stale against a re-pinned subspace should deliver nothing rather than vacuum the re-pinned content. This is rationale for the choice, not a re-derivation of its effect (the act-definition prose already states the effect), so it does not reintroduce the depth-case prose trimmed in prior cycles.

## OUT_OF_SCOPE

None. The note stays within content delivery, delivers only link *references* for link-subspace positions (deferring link-structure reading), and correctly relegates straddling-span semantics to an Open Question rather than handling it.

VERDICT: REVISE
