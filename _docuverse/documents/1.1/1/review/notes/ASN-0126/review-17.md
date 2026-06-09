# Review of ASN-0126

## REVISE

None. I checked each load-bearing claim:

- **P6 (GateRealizability) proof.** The R0-vs-`Emit_K` distinction is handled correctly: R0 fixes only fresh-on-chain existence over all chain indices `j > J_d`, while the `Emit_K` operation's contract pins `a_emit(Σ,d) = inc(ℓ_prev,0)` (chain index `J_d+1`, the least). The lift to `K.λ_sh` discharges (0)/(i)/(ii) by inspection, and `K ∈ T_admissible` is correctly carried from the stored representative `K_j` to the emitted `K` via coverage equality. Sound.
- **The wp derivation.** `wp(g → S, R) ≡ g ∧ wp(S, R)` is correct, and robust to whether a gate-rejection is modeled as abort or skip (a fresh `a_emit ∉ dom(Σ.L)` falsifies the active-subset postcondition either way). The enablement-vs-landing separation is real and correctly attributed: the two new conjuncts gate firing (P4), the three inherited conjuncts gate active-landing.
- **Born-nullified witness.** Numerics verified: `a_R = …2.3 ∉ coverage(G_rng)=[…2.4,…2.7)` (retraction lands active), then `a = a_emit(Σ₁,d) = inc(a_R,0) = …2.4 = g ∈ coverage(G_rng)` (citation born nullified). The third wp conjunct is genuinely false here, and the gate still fires — exactly the claimed gap. `δ(3,#g)` is T12-well-formed; addresses, `zeros`, and `s_L=2` all check.
- **Retraction re-expression.** The `F=∅ → F=[r]` move is sound: `nullified`/`L_R`/`A_K` read only `coverage(G')`, so they carry over unchanged. The note correctly declines to inherit `LayerReachable` (attributed retraction is not a `Nullify`) and conditions the wp simplification on `UnitDepthRetractionDiscipline` instead — the property that actually drives the vacuity. Binary ≠ unit-depth is stated, not overclaimed.
- **Projection π.** Base `π(Σ_init)=Σ_init^{0086}` and per-step C/M/L equivalence are established; foundation lemmas (R0, `a_emit` totality, L-ContiguousPrefix, PrefixSpanCoverage) transfer because they constrain only the shared components.
- **C0 / P1 / P2 / P3.** The two-premise structure is correct: P1 alone freezes a possibly-ill-formed registry (constant-in-state but not single-valued); C0 supplies single-valuedness via coverage-class-key uniqueness. Finiteness conjunct is needed for decidability of precondition (i) and is justified against L-fin.
- **Cross-references.** All citations resolve to foundation ASNs (0043, 0086). No non-foundation ASN is referenced by number; the span-count measure `|·|` is a new, justified measure, not a reinvention of a foundation notion.

## OUT_OF_SCOPE

### Idem semantics, behavior/predicate catalog, standard registrations, F>1 / N>3 extension
Open questions #1–6. These are correctly deferred to the operational successor. The note commits only to the flag's structural presence and state-independence (P3), and the structural catalog's silence on G-span *floors* is correctly housed one layer up. No structural commitment here depends on them.

VERDICT: CONVERGED
