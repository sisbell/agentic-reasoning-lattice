# Review of ASN-0087

I read this note as a manuscript to be broken, and spent most of my effort on the two places these specs usually fail: the contiguity invariant (D-CTG★) and the operation's boundary behavior. Both survived.

## Verification performed

**Invariant coverage is complete.** Cross-checking against ASN-0047's `ExtendedReachableStateInvariants` list, all 32 per-state invariants are discharged (link: L0, L1, L1a, L1b, L1c, L3, L14, L-fin; arrangement: S2, S3★, S3★-aux, S8a, S8-depth, S8-fin, S8★, CL-OWN, CL-UNIQ, D-MIN★, D-CTG★, D-SEQ★; frame-inherited: S4, S7a, S7b, C1b, C1c, C-fin, P6, P7, P8, M0, NodeLineage, ActivatedEmission; plus S7d, L11a). Composite-boundary properties (P4★, P4a, P7a) and transition invariants (M1, L12, P0–P3) are addressed. Nothing in the list was skipped.

**The hard invariant is proved, not hand-waved.** D-CTG★ is established at *arbitrary* post-state depth `m ≥ 2` via explicit T1 case-(i) analysis on interior positions — not assumed at `m = 2`. The S2 discharge correctly splits into within-subspace (`v_ℓ ∉ V_{s_L}(d)` by the `n_L+1 > n_L` strict inequality) and cross-subspace (`(v_ℓ)₁ = s_L ≠ s_C` by SC-NEQ) exclusions rather than the weaker `v_ℓ ∉ V_{s_L}(d)` alone. D-MIN★ and D-SEQ★ each carry the empty/non-empty case split.

**Boundary cases are handled.** Empty endset slots (`eᵢ = ∅`, `i ≠ 3`) via `coverage(∅) = ∅`; first-link placement (`V_{s_L}(d) = ∅`); `N > 3`; and the reflexive endset case all appear with explicit treatment. The worked example's prefix tests (`a₁ ⋠ a₂` at position 8, `a₁ ⋠ ℓ` at position 7) check out against the expanded tumblers.

**The wp analysis is non-trivial.** Case 2 (`d_target = d`) isolates a genuine second route — the reflexive disjunct `(E i :: ℓ ∈ coverage(eᵢ))` forced by the post-state witness `v_ℓ ↦ ℓ` — and the reduction under standard authoring (via M-FreshExcl at `x = ℓ`, with `ℓ ∈ F` established structurally) is sound. The `ℓ ∉ ran(M(d))` derivation through the S3★ + S3★-aux + freshness chain is the right level of rigor, not an assumed `ℓ ∉ dom(L)`.

**Consequences are derived, not stated.** The retroactive-discoverability side effect on prior links (M-PriorLinkDisc), with the backward freshness transfer `Σ_{ℓ'} →* Σ_ℓ` via Store Monotonicity★, is the kind of derived consequence the standard demands.

Cross-ASN references are all to the listed foundation ASNs (0034, 0036, 0043, 0047, 0093, 0098), which is permitted. `StandardAuthoring`/M-FreshExcl parallel ASN-0098's `Tight`/LP19a but are a deliberately weaker predicate (covered-F-addresses-in-store, without canonical-span or full-interval residency), load-bearing for the reflexive-route exclusion — not reinvented notation.

## Anti-bloat scan

The `review-mode.anti-bloat` patterns do not survive here at a flaggable level. The recent consolidation appears to have done its job: the empty/non-empty positioning case is stated once (Effect) and cross-referenced rather than repeated; the M-FreshExcl lemma is defined once and reused; the invariant table is a roadmap to in-section discharges, not duplicated prose. The Side Effects section's connections to LP9/LP18 carry concrete content (the witness set `{v_ℓ}`), not bare name-dropping. No document-ordering justifications, no consumer inventories, no multi-section deferrals to a single downstream location.

VERDICT: CONVERGED
