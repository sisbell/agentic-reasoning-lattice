# Review of ASN-0051

I've worked through the ASN systematically, checking proofs, witnesses, and edge cases.

## Verification Summary

**SV6 (CrossOriginExclusion)** — The three-sub-case proof structure ({1} t = s, {2} s ≺ t, {3} divergence) is exhaustive over `s ≤ t`. The T4-validity argument for t (including the boundary case-split at `k = p₃ + 1` vs `k > p₃ + 1` for no-adjacent-zeros at position (k − 1, k)) is rigorous.

**SV10 + CrossDocumentDecoupling witness** — Verified the explicit tumblers: i₁ = 1.0.1.0.1.0.1.1, i₂ = 1.0.1.0.1.0.1.2, i₃ = 1.0.1.0.1.0.1.3, ℓ_span = 0.0.0.0.0.0.0.3 (k = 8 > p₃ = 6). All SV6 preconditions discharge correctly. The cross-document extension to j = 1.0.1.0.2.0.1.1 with origin 1.0.1.0.2 properly exhibits π(F, d₂) = ∅.

**SV11 attainment biconditional** — The Φ surjectivity argument from non-empty terms to maximal fragments correctly forces the (⇒) direction at attainment. The witness coverage spans all (m ≥ 1, p ≥ 1):
- Single-block sibling family for p = 1
- W(1, p) via offset-1 schedule for p ≥ 2 (size-≥3 invariant maintained at each step)
- W(2, 2), W(3, 2), W(2, 3), W(3, 3), W(4, 3) explicit
- Lift schemata (α), (β), (α_2), (β_2) with commutativity verified
- Disjoint-pair non-attainment via T-linear separation (suffix coalescence at e_max) and T-interleaving (four-case structural lemma + pigeonhole on {e_i, e_{i+1}})
- Small-block non-attainment via the 2m − 1 threshold

**SV14(d) witness** — The K.λ allocation of a' with F' = {(a₃, a₄ ⊖ a₃)} followed by the K.μ~ + K.μ⁻ excision correctly exhibits strict shrinkage of discover_through_from(d).

**Worked Example K.μ~ admissibility** — The K.μ⁻ + K.μ⁺ decomposition with upward-tail removal {v₃, v₄, v₅} at cut n' = 2 is correctly D-SEQ-admissible. J1★ at composite endpoints is satisfied via P2 persistence of pre-existing R-entries.

**SV13 synthesis** — Each clause (a)–(h) and (i₁)–(i₄) correctly cites its underlying claim.

**Foundation citations** — The recent revision corrected M0/M3 → B3 for the per-block mapping rule citation. Verified B3's statement matches the consumed identity M(d)(v) = a_k + (v − v_k).

## Cross-ASN References

All citations are to foundation ASNs (ASN-0034, ASN-0036, ASN-0043, ASN-0047, ASN-0053, ASN-0058). No non-foundation references found.

## Edge Cases Checked

- Empty endsets (F = ∅, G = ∅): handled by SlotwiseVitality vs BilateralVitality split
- Empty arrangements (p = 0): explicit boundary-case treatment in SV11
- K.μ~ with `dom_C(M(d)) = ∅`: ψ = id, expansion is zero elementary steps
- Within-locate-set vs across-locate-set swaps: SV5/SV5b correctly distinguish I-set invariance from V-set transformation
- New link evaluation at Σ': NewLinkEvaluationDefinedness corollary discharges all four definedness obligations

## REVISE

No issues identified. The ASN's proofs are detailed, the witnesses are explicit and verifiable, and the boundary cases are systematically handled. The most recent revision (commit 12cce9a9) addressed the prior review's citation issue.

## OUT_OF_SCOPE

None to flag — the Open Questions section appropriately defers forward-looking topics, and the Scope note correctly excludes link type semantics and replication.

VERDICT: CONVERGED
