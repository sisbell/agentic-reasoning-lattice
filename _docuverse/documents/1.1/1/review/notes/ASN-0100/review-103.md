# Review of ASN-0100

I checked the proofs (S2 functionality, S3★, the D-SEQ★/D-CTG★/D-MIN★ sequential structure, S8★, the composite-boundary atomicity, the provenance couplings, and the projection-shift correspondence), the edge cases, and the anti-bloat patterns flagged for this note.

## Verification notes (no issues found)

- **Disjointness / functionality (S2).** The three-region disjointness argument correctly establishes the shared prefix via D-SEQ★ + D-CTG-depth *before* reducing comparison to the last component, and correctly splits the `k = 0` / `k ≥ 1` cases (since `δ(k, m_C)` is undefined at `k = 0`). The reuse of I3-S2 for Left ∪ Shifted-right combined with explicit cross-region disjointness for the Insertion region is sound — ASN-0082's `M'(d)` is the vacated-gap arrangement, and the ASN correctly treats the Insertion region as outside I3's scope.
- **Sequential structure.** The closed-interval reduction properly handles the `m ≥ 3` off-prefix tuples and the arbitrary-pair (not just extremes) quantifier of D-CTG★.
- **Edge cases.** `j = 0` (front), `j = N` (append, K.μ⁻ omitted), empty content subspace (K.μ⁻ omitted), the residual-content branch of K.α (subsequent-emission off the persisted frontier), and `m_C ≥ 3` are all covered. `(INS.μ⁻-fires)` correctly characterizes the two omission cases via `Right = ∅`.
- **Atomicity.** Per-state invariants are discharged at each intermediate (including the no-I3-counterpart post-K.μ⁻ contraction state) rather than hand-waved; the strict-contraction obligation (`n'_{s_C} = p_m − 1 < n_{s_C}`) is correctly tied to `Right ≠ ∅`. The forced-ordering analysis (three K.α-induced, one conditional K.μ⁻→K.μ⁺) is correct, and the "K.μ⁺ may be split" claim is properly hedged by the per-intermediate-invariant proviso (a Shifted-right-first split would gap D-CTG★).
- **Depth requirements.** Two non-trivial wp analyses (discoverability preservation with the tight-endset collapse; provenance membership via chain-index determinism), three concrete worked examples, and derived consequences (cross-document allocation independence, projection-shift) are all present.

## Anti-bloat check

The forward references are load-bearing rather than accretive: each "coincides with I3" restatement cites a *distinct* I3 sub-lemma (I3-S2, I3-S3, I3-VP/I3-VD, I3-fin), and the cross-section deferrals ("established once in §…") each route a *different* invariant to its single proof site, not multiple paragraphs circling one downstream location. The recent compression of the empty-doc re-insertion note appears to have already removed the prior accretion. The per-invariant inheritance bullets in §Atomicity are the required rigor (the opposite of "maintained by the same reasoning"), not noise. No reviser-drift paragraphs (imagined excluded cases, relocated findings, axiom-rationale sub-paragraphs) were found.

All cross-references are to foundation ASNs (0034, 0036, 0047, 0058, 0082, 0093, 0098); no non-foundation references and no reinvented notation.

VERDICT: CONVERGED
