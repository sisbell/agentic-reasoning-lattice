## Assessment

This is a strong digest. I checked the headline commitments, the displacement arithmetic, the run-count claims, and every Green source-level reference against the note, the formal claims, and the evidence, and found no material problem.

Specifically solid, worth recording rather than re-deriving:

- **The forced/conventional split is accurate.** "Mutates only arrangement (C'=C)," "relabeling not edit (dom/ran fixed, π bijective)," "two shapes, w_μ≥1 forced," "partial/precondition-gated," and "m_1=2 as hard scope" are all genuinely forced; representing M(d) as the run partition is correctly marked *conventional* (S8 gives it but doesn't mandate it as storage). No miscategorization.
- **The displacement arithmetic is right, including the trap.** μ shifts by `w_β − w_α` (signed); α/β by `w_β+w_μ` / `w_α+w_μ` (4-cut); the digest even *improves* on the note's loose "fixed middle" intro by stating the middle shifts.
- **The implicit-vs-absolute analysis is the strongest section and is sound** — implicit positions produce the same M'(d), so they don't violate the spec; treating π/displacement as oracle rather than algorithm is correct; the per-subspace coupling is well-argued.
- **Every Green claim is grounded in the evidence** (subspace-blind REARRANGE, cross-subspace corruption, `sortknives`/`tumbleradd`/`makeoffsetsfor3or4cuts`, response-before-check + `abort()`, `logbertmodified`, text at V=1.x), and the two beyond-note sections (durability; run-count bound) are explicitly flagged as such. The `|Δ canonical runs| ≤ n` bound checks out and is tight (a single run split by all *n* cuts yields Δ=+n).
- **The width-positivity argument** (needs *both* strict order and coverage, with a correct counterexample `V_S(d)={[1,1]}`, cuts `[1,1],[1,2],[1,3]`) and the **(ii)-subsumed-by-coverage** observation are both correct.

## Revision list

1. **`[SHARPENING]` "Implementation approaches → decisive sub-choice": the displacement-example parenthetical "(forward by `w_β`, backward by `w_α + w_μ`, the μ sub-cases)" mixes a 3-cut displacement (`forward by w_β` is the 3-cut α case) into a passage about the 4-cut μ trap.** Every item is true, but list the 4-cut set consistently (α forward by `w_β+w_μ`, β backward by `w_α+w_μ`, μ by `w_β−w_α`) so the example matches the case under discussion.

2. **`[SHARPENING]` "Canonicalization (merge)": the no-cascade bound is argued at proof altitude (lemmas (a)/(b) spelled out fully) inside a design digest.** It earns its place by justifying why eager seam-merge need only inspect ≤ n seams, but it can be compressed to the operative reason — *a uniform per-region translation preserves interior non-adjacency, and a seam-merge product's outer neighbors are those non-adjacent interior runs, so it can't cascade* — leaving `|Δ| ≤ n` as the takeaway. Keeps the section at design rather than proof altitude.

3. **`[SHARPENING]` "How it fits": "structural attribution (element-level I-addresses)" under-glosses S7.** It is accurate (S7b is exactly element-level, zeros=3) but narrow; tie it forward to the *Origin/ownership carried verbatim* commitment — structural attribution is *why* I-addresses encode origin, which is what makes "carried verbatim" the load-bearing fact for the find-documents lever — so the cross-reference is explicit rather than left for the reader to assemble.

VERDICT: CONVERGED
