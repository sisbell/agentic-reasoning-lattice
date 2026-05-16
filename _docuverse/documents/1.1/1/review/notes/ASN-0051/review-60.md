# Review of ASN-0051

I traced each SV claim through its proof, verified the witnesses against explicit tumbler arithmetic, and cross-checked foundation citations.

## REVISE

(No revision items identified.)

The proofs handle the substantive cases with appropriate care:

- **SV6's sandwich proof** properly establishes both `#t ≥ k` and prefix agreement on `1..k-1` via the no-early-divergence sub-claim, then performs exhaustive case analysis on (α) `t = s`, (β) `s ≺ t`, (γ) divergence at some `j`. The T4-validity verification of `t` correctly handles the boundary pair `(k-1, k)` in both sub-cases `k = p₃ + 1` and `k > p₃ + 1`. The element-level zero-confinement argument is rigorous.

- **SV11's biconditional** is properly stated with both directions proved. The non-attainment cases (disjoint-pair with T-linear and T-interleaving sub-cases; non-injective small-block with `min_k n_k < 2m − 1`) are structurally analyzed. The attainment witnesses cover (m ≥ 1, p = 1), (m = 1, p ≥ 2), (m ≥ 2, p = 2 with overlapping I-extents), and (m = 2, p = 3) with explicit tumbler arithmetic. I verified the (m = 2, p = 3) witness independently — the gap-at-a₉ pattern produces width-1 gaps in every block, satisfying non-adjacency.

- **The SV10 witness** is constructed through an explicit chain (InitialState bootstrap → K.δ account → K.δ document → K.α content → K.λ link → K.μ⁺ + K.ρ) with verifiable tumbler values (i₁ = 1.0.1.0.1.0.1.1, ℓ_span with action point k = 8 > p₃ = 6). The CrossDocumentDecoupling extension correctly applies SV6 to derive `π(F, d₂) = ∅`.

- **Worked Example** correctly traces M(d) through K.μ~ + K.μ⁻ to remove a₃, exhibits both the degenerate "After reordering" case (locate set preserved) and the non-degenerate "Reordering that changes locate" case (locate set strictly transformed by ψ).

- **wp analysis** correctly identifies K.μ⁻ as the unique vitality-threatening transition with the D-SEQ-admissibility precondition properly handled; K.μ⁺/K.μ⁺_L wp captures both pre-state vitality and new-coverage disjuncts.

- **Foundation citations** are consistent throughout: ASN-0034 for tumbler algebra, ASN-0036 for arrangement, ASN-0043 for links, ASN-0047 for transitions, ASN-0053 for span convexity, ASN-0058 for blocks and OrdinalShiftBase. No non-foundation cross-references.

- **NoStaleResolutionState** is properly cast as a schema inspection (architectural remark, not SV-labelled), with per-transition verification that no field stores V-positions across allocation.

- **SV13 synthesis** assembles the survivability theorem with proper attribution to component SV claims, including the K.μ~ composite-level caveat and the m·p state-dependence note.

## OUT_OF_SCOPE

(None to flag — the open questions section already enumerates legitimate future work: dormant link revival, canonical fragment ordering, multi-link interactions, discovery latency, bilateral vitality across forks, home document/vitality relationship.)

VERDICT: CONVERGED
