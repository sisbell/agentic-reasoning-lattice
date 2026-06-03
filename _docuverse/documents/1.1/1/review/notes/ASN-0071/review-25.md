# Review of ASN-0071

I checked the operation definitions, the resolution machinery, every worked composite, and the boundary cases. The ASN is unusually thorough, so I focused on where rigor typically fails: the span-confinement arguments, the cross-depth vs. interior-action-point discrimination, the multi-block resolution, and the finiteness induction.

**Verified directly:**

- **Prefix confinement (PC).** The proof is complete, not hand-waved. The totality sub-argument (`#t ≥ #u` via T1 case (ii) exclusion) is established *before* the componentwise comparison, so `t_j` is shown to exist before it is compared — the usual gap in such proofs is closed here. Subspace confinement is correctly derived as the position-1 instance, gated on `actionPoint(ℓ) ≥ 2` so that `1 < actionPoint(ℓ)`.
- **The discrimination claim.** I checked both depth-3 examples. The interior-action-point span `σ' = ([s_C,1,2],[0,1,0])` reaches `[s_C,2,2]` and over-collects positions 2–3 (breadth-wise sweep, correctly rejected by `actionPoint(ℓ)=#u`); the cross-depth shallow span reaches `[s_C,2]` and captures the full depth-3 subtree (depth-wise, correctly permitted). The asymmetry is principled and concretely exhibited against `d_E`, not just asserted.
- **Multi-block resolution.** For `Q_D`, the three width-1 blocks are correct: cross-origin non-adjacency (`origin(a₁)=d_A ≠ d_C=origin(a₂)`) blocks both candidate merges via M16, and the set-flattening dedup of the repeated `a₁` is exercised — the case the singleton query could not reach.
- **Composite validity.** Each of the five composites discharges J0/J1★/J1'★ at its boundary, with J0 correctly vacuous on the transcluding (no-K.α) composites.
- **F-FIN.** The induction is sound: `(E₀)_doc = ∅`, K.δ adds ≤ 1 entity per elementary step, reachable states have finite elementary ancestry, and the bound is correctly stated against `n_elem` rather than composite count.
- **Boundary cases.** Empty query (F-EMPTY), unresolvable positions (F-FILT), single-address vs. disjoint-fragment overlap (F-PART/F-SOUND against the concrete non-member `d_C`), and the over-deep vspec (resolves to ∅ via PC totality + F-FILT) are all handled correctly.

The biconditional decomposition into F-COMP/F-SOUND, the currency/permanence reconciliation through versioning (and its honest "convention, not guarantee" caveat), and the `R`-vs-`find` history/currency distinction are derived, not stated. Cross-references are confined to the foundation stack (ASN-0047/0053/0058 and the tumbler/transition foundations they themselves rest on). No implementation drift — this specifies state, an operation on it, and its invariants abstractly.

I found nothing skipped that rises to a revision.

VERDICT: CONVERGED
