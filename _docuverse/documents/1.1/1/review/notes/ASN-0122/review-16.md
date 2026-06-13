# Review of ASN-0122

I checked every introduced claim (Inst, res, R_Σ, corr, γ, ⟦Γ⟧, X0–X12 and sub-parts), re-derived the proofs, verified the boundary cases the standards demand, and recomputed the worked example arithmetic. I find no REVISE items. Recording the substantive checks so the verdict is auditable:

- **X11 (canonical decomposition)** — the load-bearing structural theorem. The "≤ one predecessor in the relation" step is correct: a shared successor forces `shift(u₁,1)=shift(u₂,1)` and `shift(w₁,1)=shift(w₂,1)`, and TS2 (equal-depth precondition met by S8-depth on two content positions of one document) collapses both feet. Acyclicity from TS4 is right. The fan-out case (an instance shared across two chains, as `(d₂,[1,1])` in the example) does **not** create predecessor-branching, because the *other* foot differs — verified directly. Strictness of the sort and the swap/transpose claim (X3 continued) hold.
- **X10(a)** — cardinality `n` per foot: the `k₁=0` branch correctly cites TS4 and the `k₁≥1` branch correctly cites TS5 at amounts `k₁<k₂`. Citations are exact.
- **X4c** — `K_P`, `K_Q` are integer intervals via monotonicity of `k↦u+k` plus order-convexity (T12(c)); intersection of integer intervals is an integer interval, so clipping yields ≤ one pair. Sound.
- **X7(iii) shifting contraction** — the one place injectivity is not free is discharged correctly: `id` on `L`, `σ` on `R` (D-BJ), images disjoint by `L ∩ Q₃ = ∅` (D-DP(a)). This is the right obligation and the right discharge.
- **X-T / X6** — the transport lemma is correct; the telescoping of per-step res-preservation across intermediate states in X6(b) (with `π_i` interposed for interleaved edits) is terse but genuinely closes, since no arrangement edit rewrites the address at a surviving position.
- **Subspace argument** — the `σ=([1,5],[3])` computation (`reach=[4]`, `[2,7]∈⟦σ⟧`) genuinely demonstrates that a T12-well-formed content-*start* span can denote link positions, justifying the `∩ V_{s_C}` clip; X9's three-way vacuity argument (CL-OWN, S3★/SD, CL-UNIQ) is complete.
- **Worked example** — every count recomputed independently: `corr` (3 elements), the two maximal pairs, the swap tie-break, the window clip to one pair, and the disjoint-window detector `{a,b}∩{c,b}={b}`. All match.
- **Boundary coverage** — empty spec-set, span clipping to nothing, empty regions, self-comparison (diagonal forced, off-diagonal at non-injectivity, disjoint-window detector), and fan-out are all addressed.

The note correctly avoids conflating its correspondence pairs (V-positions co-advancing, addresses arbitrary) with ASN-0058 mapping blocks (contiguous addresses) — `a_k` need not equal `a_0+k`, and the example exercises exactly this (`b,c` non-contiguous in `γ₁`).

On the anti-bloat classifier: I checked specifically for the flagged patterns. There are no axioms (so no "why-needed" sub-paragraphs), no definition enumerates downstream consumers, no document-ordering justification, and the single forward reference (region-definition → X9) is a one-clause defer, not surrounded by meta-prose. The motivational passages (line-diff framing, the completeness-as-obligation rationale) are the ASN's normative spine — they establish *why* R2 completeness is binding rather than padding a forward reference — and do not obstruct any claim's reading. No accretion finding clears the bar.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: n-way alignment, cached correspondence indices, derived-correspondence consistency
The Open Questions correctly defer these. n-way alignment composed from pairwise reports, the consistency contract for a cached/derived correspondence index across edits, and multiplicity-annotated matching reports are genuinely new territory, not gaps in this ASN.

### Topic 2: correspondence over content referenced-but-unarranged
Whether a stored span that is arranged in neither compared document should count as "part of a version" is a basis question (arrangement-presence vs. reference-presence). The ASN fixes arrangement-presence and is internally consistent; the alternative is future work, not an error here.

VERDICT: CONVERGED
