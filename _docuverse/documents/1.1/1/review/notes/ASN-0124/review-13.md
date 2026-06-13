# Review of ASN-0124

I verified this note adversarially, with particular attention to the operations and composites (where specifications fail) and to the active anti-bloat concern. The proofs hold; the boundary cases are covered; the bloat scan turns up only conventional framing.

## REVISE

No REVISE items.

The following high-risk claims were checked in full and are sound:

- **FD-FRESH** — the clear+rebuild composite (K.α^n; K.μ⁻ at `n'_{s_C}=0`; one K.μ⁺ rebuild; K.ρ^n) is a valid composite. Intra-composite sequencing holds (rebuild images are all in `dom(C)` — old by P0, fresh by the prior K.α); the couplings hold initial-to-final (range-new = `A_new` since every old image is in both initial and final range; the mid-composite absence of old images is harmless under initial-to-final J1★/J1'★). The conclusion `finddocs(I, Σ_post) = finddocs(I, Σ_pre)` for pre-resolved `I ⊆ dom(Σ_pre.C)` follows step-by-step from FD-FRAME and FD-STEP, with `A_new ∩ I = ∅` discharged by allocation freshness. The first-insertion (`V_{s_C}(d)=∅`, clear omitted) and pure-append (`p=N+1`, no clear) sub-cases are correctly carved out.
- **FD-VERS** — `ran_C(d_new, Σ') = ran(M'(d_new)) = ran(M(d_op)|_{V_{s_C}(d_op)}) = ran_C(d_op, Σ)` (J4 copies content subspace only via the bijection φ); `d_op` is framed, reconciling the two statements of the contingency.
- **FD-WITNESS / FD-COINC** — both directions check (P4a for ⊆, P4★∘P2∘M1 for ⊇); the range-non-decreasing chaining carries the witness `a ∈ ran_C(d, Σ_k) ⊆ … ⊆ ran_C(d, Σ)`. The parenthetical noting that a reorder's K.μ⁻ decomposition fails the *syntactic* "no K.μ⁻" condition while still meeting the *semantic* range-non-decreasing hypothesis is a correct, non-bloated caveat.
- **FD-VDYN(d)** — the swing `image_C(W, d_q, Σ') = image_C(π⁻¹(W), d_q, Σ)` follows from K.μ~-FIX, subspace-preservation, and the bijection equation; the necessary-but-not-sufficient analysis and the absorption construction (`d_q` and `d_x` both arranging `{a,b}`, image moving `{a}→{b}` while `finddocs_V` stands) are verified.
- Boundary coverage is complete: `Q=∅`, `W=∅`, `I=∅` (including the empty-intersection universe convention in FD-COOC), freshly-registered documents, full-clear contraction (FD-CWP), ghost and link-store addresses (FD-GROUND), single-region biconditional (FD-SELF). The worked illustration is internally consistent across reach, fragments, the silent `d_C` drop under reorder, the severance, and the ghost split.

The historical-companion cluster (FD-HIST…FD-COINC) derives from declared dependencies (ASN-0047 P2/P4★/P4a/M1) and is load-bearing for the central deviation thesis; consistent with the prior reviser's deliberation, it is not bloat.

## OUT_OF_SCOPE

The note's own Open Questions section already enumerates the future-ASN territory (interior-state coherence, provenance *timing*, attribution-bearing answer refinement, past-state reach, distributed availability without silent omission, asker authority, provenance compaction, multiplicity exposure), and the Scope paragraph correctly excludes link discovery, endset search, version comparison, origin reporting, content delivery, the editing operations, and BEBE. Nothing additional to flag — the deferrals are honest and complete.

VERDICT: CONVERGED
