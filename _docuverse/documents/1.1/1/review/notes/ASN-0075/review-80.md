# Review of ASN-0075

I worked the central proofs (D-WIT, D-EXH, D-DISCR, D-DISJ) against the foundation contracts and re-derived the worked example. The ASN holds up.

## Verification notes

**D-WIT** — The chain `a ∈ ran(M(d))` → fix `v` → L14 gives `a ∉ dom(L)` → contrapositive of S3★'s link clause forces `subspace(v) ≠ s_L` → S3★-aux closes `subspace(v) = s_C` → `(a,d) ∈ Contains_C(Σ)` → P4★ gives `(a,d) ∈ R`. Every step is licensed, and the composite-boundary hypothesis is correctly required (P4★ is a boundary property, not a per-state invariant).

**D-EXH** — The 2×2 cross-product is total; the impossible row (Yes/No) is excluded by D-WIT under the `a ∈ dom(C)` hypothesis; the three surviving rows get exactly one label each. Sound.

**D-DISCR** — Both histories are valid composites: J0 is satisfied (in History 2 the freshly-allocated `a` lands in `M(d')`, not necessarily its origin `d`), J1★/J1'★ record provenance for the documents that gain range-new content, and the K.μ⁻ strict-contraction precondition (`n' < n`) is met. The `(C,L,E,M)` agreement table is correct — `a = [d.0.s_C.1]` is fixed by the first-emission rule from `d` alone, and the same `v_a` is stipulated, so even the value level agrees. The classification divergence rests solely on `(a,d) ∈ R_1 \ R_2`. The impossibility argument and D-NEED corollary follow.

**D-DISJ** — The three-group partition (only-A, only-B, neither) is exhaustive under disjointness, and each group falsifies both report conjuncts (via D-WIT for the CURRENT exclusions, directly for the DELETED first-conjunct failures). Correct.

**Worked example** — Re-traced the reorder-then-truncate on `d_A` (drops `b`) and the direct truncate on `d_B` (drops `c`, already trailing). Classification table and output `({b},{c})` check out, including the witness discussion.

## Other checks

- Cross-ASN references are all to foundation ASNs (0034, 0036, 0047, 0058) — no violation.
- Depth requirements met: concrete worked example present; non-trivial wp for Q1 (one-half non-emptiness) and Q0 (joint vacuity); consequences derived (D-IDENT, D-ORIG, D-ORD, D-SYM).
- Edge cases covered: disjoint content, both-empty, self-comparison (`d_A = d_B` falsified by contradictory range-membership), asymmetric population.
- No accreted forward-reference meta-prose: the lone forward pointer `(D-OBS)` in the wp section is a bare citation, not a justifying paragraph. The notational setup in D-DISCR is load-bearing for composite validity, not essay content.
- Scope is appropriate — the operation specifies observational state, output sets, and guarantees abstractly; per-occurrence (Vstream) removal is explicitly and correctly scoped out.

No REVISE items.

VERDICT: CONVERGED
