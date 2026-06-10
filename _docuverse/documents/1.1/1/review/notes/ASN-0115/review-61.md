# Review of ASN-0115

I read the note as a query specification — RETRIEVEV modifies no state, so the usual "operation preserves invariant Y" obligations are vacuous; the rigor burden falls on the denotational claims R1–R11 and the well-definedness of `deliver`. I checked each proof, the boundary behavior of `act`/`depthcompat`, and the anti-bloat dimension flagged by the classifier.

## Key verifications performed

- **Confinement lemma.** The T5 application is sound: `p = [s₁,…,s_{m−1}]` satisfies `p ≼ s` and `p ≼ reach(σ)` (TumblerAdd copies the prefix below the action point `m`), and `s ≤ t ≤ reach(σ)` gives `p ≼ t`. The `#p ≥ 1` precondition of T5 holds because `#s ≥ 2`. Boundary `m = 2` reduces correctly to subspace agreement only.
- **The `act` override.** The deep-case argument is correct: a bound `v ∈ dom(M(d)) ∩ ⟦σ⟧` has `#v = m_S(d)` (S8-depth) and `#v ≥ #s−1` (Confinement), forcing `#s = m_S(d)+1`, whence `p ≼ v` with `#p = #v` collapses to `v = p ≺ s`, contradicting `v ∈ ⟦σ⟧`. So the geometric intersection is empty when `#s > m_S(d)`, and the override genuinely bites only in the shallow case. The guarded `∨` in `depthcompat` is well-defined under short-circuit reading, as the note states.
- **R6 no-interior-hole.** The canonical-start derivation (`act ≠ ∅` ⟹ `s = [S,1,…,1,s_{m_S}]` via a witness `v ∈ act` + Confinement + D-SEQ★) is shown in full, and the unbound slice members are exactly `k > n_S` — a terminal tail. The honest restriction to the bindable (depth-`m_S`) slice is appropriate.
- **R7 Repeatability.** Tight and complete. The three cases (non-empty restriction depth-compat-agree; non-empty restriction with override-at-both; empty restriction) all yield equal active sets, `m_S(d)` is pinned equal at both states by a shared witness, and the `Σ →* Σ'` comparability hypothesis is correctly required (not derived) for S0 to chain content values. The link case correctly needs no store invariant (the `⟨ref,a⟩` item carries the equal resolved address).
- **R8 link vacuity & subspace-sharing.** CL-OWN forces `d = d' = origin(a)` and CL-UNIQ forces `v = v'` for shared link addresses — distinct active link positions cannot co-resolve, so transclusion is content-only. The subspace-sharing step (S3★-aux to land `subspace(v) ∈ {s_C,s_L}`, then the S3★ contrapositive against SD) is valid.
- **R11 wp & worked instance.** The single-live-condition wp (binding an active content position, with store membership as automatic consequence via S3★/S0) is genuinely non-trivial, and the deletion-as-contraction worked instance checks out (K.μ⁻ frame leaves `d'`'s arrangement, S0/S1 keep `a` in the store).
- **Worked instances** in R6/R8/R9/R10/R11 all recompute correctly (verified `reach`, `⟦σ⟧` slices, and `act` in each).

## REVISE

None.

## OUT_OF_SCOPE

The scoped-out operations (RETRIEVEDOCVSPAN, READLINK, etc.) are correctly excluded — the note defines no claims for them. The five Open Questions (inline provenance, permitted failure, dangling references under relaxed S3★, channel faithfulness, straddling-span delivery) are appropriately forward-looking and do not represent gaps in this ASN.

I specifically examined the anti-bloat candidates and concluded none rise to REVISE: the override paragraph carries design rationale and a deep-case-empty characterization that no R-claim consumes, but it is legitimate boundary analysis of a non-obvious definitional choice (force-empty vs. geometric intersection) rather than forward-reference accretion; the "harmless subspace" paragraph handles a case the preconditions genuinely admit (`s₁ ∉ {s_C,s_L}` is well-formed); and the document-allocation precondition (vs. R6's silent position-filtering) is a correctly-drawn distinction — Nelson's "span containing nothing today" robustness applies to empty regions, not to references naming non-existent documents, so the asymmetry is justified by the nature of the cases. The Confinement lemma re-proves a fact adjacent to ASN-0058's C0a, but generalizes it to spans whose start need not be bound (C0a's content-reference preconditions do not directly apply), so the local proof is warranted, not reinvention.

VERDICT: CONVERGED
