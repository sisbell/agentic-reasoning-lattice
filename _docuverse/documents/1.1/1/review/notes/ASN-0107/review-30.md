# Review of ASN-0107

## REVISE

(none)

I checked the load-bearing claims and found them sound:

- **`sat`/`num` totality and degenerate cases** — `match ⊆ dom(Σ.L)` with L-fin gives totality; `Qᵢ = ∅ ⟹ num = 0` and the unconstrained `(T,T,T)` case (from/to may fail on empty endsets, type non-empty by L3) are handled correctly.
- **D2 reordering clause** — the displayed set reads `{Σ.M(d_q)(u) : u ∈ π⁻¹(Wᵢ) ∩ dom}` (single inverse, `Σ.M` not `Σ'.M`); verified consistent with the worked example (`π⁻¹({v₁}) = {v₂}`, `Σ.M(d)(v₂) = a₂`, so `Q₁(Σ') = {a₂}`). The earlier double-inverse concern does not apply.
- **Worked example** — recomputed every slot for the count (3), the `K.λ` creation path (E4/E2: +1, never falling), the contraction (3→1, R2 with `k = 3`, `Δ = −2`), the re-extension (1→3), and the reorder (3→0). All match.
- **R6 wp** — the pull-back through deterministic `K.μ⁻` is an equivalence at each step (coverage permanence E1; resolved-part substitution `Σ'.M(d_q) = Σ.M(d_q) ↾ R`); the "weakest, not merely sufficient" claim and the R1 (`k = 1`) specialisation hold. The general multi-slot contraction is covered per-link by R6's three-slot conjunction, so R1/R2's single-slot restrictions are sound illustrative specialisations, not hidden gaps.
- **Depth requirements** — derived consequences (E1→E4, R0→R6), a concrete scenario, and a non-trivial wp are all present.
- **References** — every cited ASN (0034, 0036, 0043, 0047, 0098) is a foundation; no disallowed cross-ASN references. Retrieval (FINDLINKS), pagination, MAKELINK, FOLLOWLINK, and BEBE are correctly left out, not specified.

Anti-bloat: the view-vs-store distinction recurs across D3 and R0, but each instance carries a distinct claim (zero-answer tense vs. no-retraction substrate property) and reinforces rather than duplicates; forward references are limited to E4→R0 and do not exhibit accretion.

VERDICT: CONVERGED
