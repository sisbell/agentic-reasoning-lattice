# Review of ASN-0068

## REVISE

[None]

## OUT_OF_SCOPE

[None]

I traced each proof systematically:

**CV-IN action-point necessity:** The V-position capture argument is sound. Given `actionPoint(width(σ)) = k < m_σ`, TumblerAdd's piecewise structure gives `reach(σ)_k ≥ start(σ)_k + 1`, and for any `t = [S, 1, ..., 1, j]` with `j ≥ s_m`, T1 case (i) at divergence position `k` yields `t < reach(σ)`. The unbounded capture follows since `j` ranges freely. The argument is parametric in `k`, covering the full range `1 ≤ k < m_σ`.

**CV-PRED:** The five clauses (convention, existence, uniqueness, inverse, dual inverse) all hold. Uniqueness via TS2 with the equation `v' ⊕ δ(j, m) = v` is correct; the candidate `[S, 1, ..., 1, v_m - j]` is in S8a iff `v_m ≥ j + 1`.

**CV-MAX existence:** Walks terminate — right by S8-fin (the distinct `v_a + k` positions cannot all be in finite `dom(M(d_a))`), left by S8a's positive-component bound (`(v_a)_{m_a} - 1`). The constructed `R = (v_a - j, v_b - j, j + n_R)` is a correspondence run by the left-region/right-region case split, using M-aux + predecessor-inverse to identify offsets. Maximality follows from each walk's maximality.

**CV-MAX uniqueness:** The δ = j²_a - j¹_a = j²_b - j¹_b synchronization argument correctly forces both sides to shift in lockstep (via OrdinalShift's last-component formula and T3). Case δ = 0 contradicts right-maximality of the shorter run; case δ > 0 contradicts left-maximality of R² via the `(v²_a - 1, v²_b - 1) = (v¹_a + (δ-1), v¹_b + (δ-1))` identification, witnessed by R¹'s run conditions at the valid offset `0 ≤ δ - 1 < n¹`.

**Examples:** All four traced correctly. Example 3 confirms CV-MAX's unique-witness property concretely — four pairs in `corr_{a,a}` partition across three runs as (2, 1, 1).

**CV-FIN injectivity into corr:** The starting-pair map is injective by uniqueness — two runs sharing a starting pair would witness it twice at offset 0.

**CV-SPAN-VIEW:** Well-formedness via T12 (action point of δ(n, m_σ) equals m_σ = #v), injectivity via T3 on the displacement equality.

**CV-LINK-DEGEN, CV-LINK-SELF, CV-SELF:** Correctly derived from CL-OWN + S7 (origin functional), CL-UNIQ (link-subspace injection), and trichotomy respectively.

**CV-ATOM:** Width-1 admissibility and aggregation-by-uniqueness both follow from CV-MAX's existence + uniqueness. The absence-of-threshold claim is supported by syntactic absence in the definitions.

**Foundation references:** All cross-ASN citations are to foundation ASNs (0034, 0036, 0047, 0053, 0058).

**Scope:** Stays within the operation's contract. Link-subspace handling (CV-LINK-DEGEN, CV-LINK-SELF) explains operation behavior; doesn't redefine link semantics.

VERDICT: CONVERGED
