# Review of ASN-0051

## REVISE

(none)

## OUT_OF_SCOPE

(none)

VERDICT: CONVERGED

The ASN is unusually rigorous. I verified:

- **SV6 proof** — the three-case dispatch (t = s, s ≺ t, divergence at j ≥ k) is exhaustive; the T4-validity of element-level t in ⟦(s, ℓ)⟧ is established case-by-case (positions 1, #t, and the boundary pair (k−1, k) under k = p₃ + 1 vs k > p₃ + 1); the field-decomposition argument transferring origin from s to t is sound.
- **SV5/SV5b** — composite-endpoint π-invariance via K.μ~'s ran-preservation; locate transformation by ψ verified against the "Reordering that changes locate" witness ({v₂, v₃} → {v₁, v₃} under v₁↔v₂ swap).
- **SV11 biconditional** — Φ surjectivity from non-empty terms to fragments gives |fragments| ≤ |non-empty terms| ≤ m·p; equality forces both (no empty terms) and (no coalescence).
- **SV11 attainment witnesses** — W(2,2), W(3,2), W(2,3), W(3,3), W(4,3) with explicit offsets and gap-width-1 verification; lift schemata (α), (β), (α_2), (β_2) preserve attainment conditions; (α)∘(β) = (β)∘(α) commutativity verified by endpoint comparison; (m=1, p≥4) per-p direct construction with offset-1 schedule maintains the size-≥3 invariant for i ≤ p.
- **Non-attainment cases** — disjoint-pair T-linear sub-case (m spans coalesce at e_max) and T-interleaving sub-case (four-case structural lemma with uniformity of j* across β_{k₂}, then pigeonhole on {e_i, e_{i+1}} for m ≥ 3 / direct adjacency for m = 2).
- **Worked example arithmetic** — initial M(d) → post-K.μ~ Σ_reord → post-K.μ⁻ Σ' gives π(F, d) = {a₂, a₄}, two blocks β₁ = (v₁, a₁, 2), β₂ = (v₃, a₄, 2), fragment count = m·p = 2.
- **SV6 example** — s = 1.0.1.0.1.0.1.2.3, ℓ with k = 9 > p₃ = 6, t = ...2.5 has origin(t) = origin(s); b = 1.0.1.0.2... has b > reach by T1(i) at position 5.
- **SV13 synthesis** — clauses (a)-(i) each cite supporting SV claims; NewLinkEvaluationDefinedness corollary discharges all four well-definedness obligations at K.λ.

Foundation citations (ASN-0034, 0036, 0040, 0043, 0047, 0053, 0058) are consistent. No cross-ASN references except foundations. State-naming table disambiguates Σ_int_kμ~ vs Σ_reord usage in SV14(d). The wp section correctly localizes K.μ⁻ as the unique vitality-falsifying transition.
