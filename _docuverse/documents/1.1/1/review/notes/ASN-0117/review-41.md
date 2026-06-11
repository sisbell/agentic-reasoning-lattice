# Review of ASN-0117

I checked the arithmetic of the contraction, the two-realisation case split against K.μ⁻/K.μ⁺'s preconditions, the coupling discharge (J0, J1★, J1'★), the range identity behind the wp, and every worked example's index bookkeeping. Summary of the load-bearing verifications:

- **Case split is sound.** For `R ≠ ∅`: `J + c ≤ N` with `c ≥ 1` gives `J − 1 ≤ N − 2 < N`, so K.μ⁻'s strict-contraction obligation holds, and `N − c − (J − 1) ≥ 1` survivors satisfy K.μ⁺'s strict-extension precondition. For `R = ∅`: `n'_{s_C} = N − c < N` since `c ≥ 1`, and the empty K.μ⁺ extension is correctly ruled out, forcing the single-step realisation. The composite's post-arrangement (`q_k ↦ a_k` for `k < J`, `q_k ↦ a_{k+c}` for `J ≤ k ≤ N − c`) matches ASN-0082's D-SHIFT/D-L/D-DOM exactly under the substitution `k' = k − c`.
- **J1★ discharge is correct.** Every post-state content-subspace image of `d` equals `M(d)(v)` for some pre-state content-subspace `v` (retained via D-L or carried via D-SHIFT), so the range-new trigger conjunct is false for every address; `d' ≠ d` is immediate from DEL-FDOC; J0 and J1'★ are vacuous (`dom(C') = dom(C)`, `Σ'.R = Σ.R`). The appeal to J2 for the lone-K.μ⁻ realisation is the right citation.
- **The wp's range identity is exact.** I verified `ran(M(d)) \ A_del^{excl} = M(d)(L) ∪ M(d)(R) ∪ ran(M(d)|_{V_{s_L}}) = ran(M'(d))` by element chase: `A_del^{excl}` excludes `M(d)(L ∪ R)` by definition and is disjoint from the link images by S3★ + SD, and S3★-aux leaves no third subspace. The per-link existential (rather than per-slot universal) is correctly argued as both necessary and sufficient; gains in `D(d, ·)` are impossible since the post-range is a subset of the pre-range and the link store is fixed.
- **Invariant coverage is structurally complete.** Rather than re-proving the package, the ASN realises DELETE in ASN-0047's atomic vocabulary, validates the composite, and invokes ExtendedReachableStateInvariants — then explicitly walks the conjuncts the operation materially reshapes (the D-*-post family, S3★ with the per-subspace split, and the S8★ run re-cut argument, which correctly notes S8★ pins no decomposition across states and re-supplies S8's preconditions conjunct by conjunct at the post-state).
- **Boundary cases are all present and computed**, not asserted: leading delete (`J = 1`, K.μ⁺ into an emptied subspace re-pinning S8-depth), suffix delete and delete-everything (`R = ∅`, including `n'_{s_C} = 0`), multi-position uniform shift (`|R| ≥ 2` exercising D-BJ), within-document sharing (`A_del^{excl} = ∅` with the only-possible coincidence mechanism noted via S2), and cross-document transclusion with the shared-position-vocabulary subtlety made explicit.
- **D-SEP's vacuous positional reading at `R = ∅`** is handled correctly in P2 (algebraic identity unconditional, positional reading gated on `R ≠ ∅`).

I also checked for forward-reference accretion per the anti-bloat flag: the internal cross-references resolve to one discharge site (the Effect coupling paragraph), the F0-naming parenthetical and the J1★ parenthetical are tight responses to prior-cycle concerns rather than drift, and the explanatory asides (count-vs-pair form of DEL-REMOVE, per-subspace split of S3★) each carry content a reader needs. No paragraph imagines a precondition-excluded case as live, and no duplicated prose pair survives scrutiny — the P4 and wp sections divide labor rather than repeat it.

## REVISE

(no items)

## OUT_OF_SCOPE

### Topic 1: DELETE for text subspaces pinned at depth m > 2
**Why out of scope**: The precondition fixes `#p = 2` equal to the S8-depth common depth, inherited from ASN-0082's contraction, which is stated only for depth-2. The model (S8-depth, ASN-0047's `m_S(d)`) admits subspaces re-pinned at any depth `≥ 2`; a DELETE acting on a deeper text arrangement would need a generalised foundation contraction first. This is a future-ASN generalisation, not an error here.

### Topic 2: Link-subspace contraction (de-arranging a link from a document)
**Why out of scope**: DELETE is deliberately confined to `subspace(p) = s_C`, holding the link subspace at full retention. K.μ⁻'s per-subspace form permits `n'_{s_L} < n_{s_L}`, so an operation withdrawing a link placement from a document's arrangement is expressible in the foundation vocabulary but is a distinct operation with its own discoverability consequences — new territory, not a gap in this ASN.

VERDICT: CONVERGED
