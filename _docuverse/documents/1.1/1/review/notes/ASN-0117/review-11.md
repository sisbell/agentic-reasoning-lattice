# Review of ASN-0117

I read the ASN as a specification of DELETE: an operation on the two-layer state that removes a span's V→I correspondences from one document's arrangement while leaving the content store wholly in frame. I checked the displacement arithmetic, the K.μ⁻/K.μ⁺ realization, every invariant discharge, the wp derivation, and all boundary cases against the foundations.

## Findings

The mathematics is sound and the proofs are grounded, not hand-waved. Spot checks that held:

- **Containment ↔ ASN-0082 precondition.** `p = q_J`, `w = [0,c]` give `p₂ + w₂ − 1 ≤ N ⟺ J + c ≤ N + 1`. ✓ `r = p ⊕ w = q_{J+c}` verified via TumblerAdd (action point 2 ≤ #p = 2).
- **Composite ≡ ASN-0082 displacement.** K.μ⁻ (retain `L`, `n'_{s_C} = J−1`) then K.μ⁺ (re-place survivors at `q_J…q_{N−c}` carrying `M(d)(q_{J+c})…M(d)(q_N)`) reproduces D-L, D-SHIFT (`σ(q_k)=q_{k−c}`), D-DOM exactly. Strict contraction `J−1 < N` always holds (since `J−1 ≤ N−c < N`), so K.μ⁻ is enabled; strict extension `≥ 1` survivor holds because `R ≠ ∅`.
- **R = ∅ realized as lone K.μ⁻.** Correctly identifies that an empty K.μ⁺ would violate strict-extension, and that `J−1 = N−c` makes the retained prefix already canonical; J2 supplies all frames directly. ✓
- **Coupling discharge (J0/J1★/J1'★).** All vacuous: no allocated content (P0), `range(M'(d)|s_C) ⊆ range(M(d)|s_C)` so no range-new content, no new provenance. P4★/P7a preserved via `Contains_C` shrinkage + `R'=R` + `dom(C')=dom(C)`. ✓
- **DEL-REMOVE under sharing.** The count-plus-top-c-label-vacancy formulation (rather than per-pair absence) correctly anticipates the S5/M13 reoccupation case. ✓
- **S3★ split.** The explicit refusal to claim `ran(M'(d)) ⊆ dom(C')` (false for link-bearing documents, by SD) and the text/link decomposition is correct and rigorous.
- **wp derivation.** `ran(M'(d)) = ran(M(d)) \ A_del^{excl}` correctly carries link-subspace images through; the per-link existential (vs. per-slot universal) is the genuinely weakest condition; shrink-only monotonicity gives the `⊇` direction automatically.
- **Worked examples.** `q_3,c=2` → `a_1,a_2,a_5`; `q_2,c=1` (multi-position shift) → `a_1,a_3,a_4,a_5`; suffix-delete, delete-everything, within-doc sharing, and cross-document transclusion all verified against the named clauses.

Edge cases the standards mandate are present: entire-document deletion, last-position (suffix) deletion, within-document sharing, transclusion isolation. Density/tiling is proven explicitly via consecutive index sets `{1,…,J−1} ∪ {J,…,N−c} = {1,…,N−c}`, not asserted. Depth requirements (concrete examples, non-trivial wp, derived consequences such as orphan/resurrection and the LP10-inapplicability argument) are met.

The ASN defines abstract state-transition semantics and system-level guarantees (P0–P5), using implementation evidence only as support. No drift into implementation mechanics. All cross-references are to foundation ASNs.

No REVISE items found.

VERDICT: CONVERGED
