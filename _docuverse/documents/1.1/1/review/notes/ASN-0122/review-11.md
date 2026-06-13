# Review of ASN-0122

I read this as a derivation, not a posit, and checked each claim against its cited foundations and against boundary behavior. Summary of what I verified before reaching a verdict:

- **Basis (X1, X2, X9).** The address-equality definition is correctly justified over value-equality: X2's reachable-state construction is a valid composite under ValidComposite★ (K.δ vacuous on coupling; K.α/K.μ⁺/K.ρ discharge J0/J1★/J1'★), and S4 forces `a₁ ≠ a₂`. X9's subspace decomposition is exhaustive — cross-document (CL-OWN + single-valued `origin`), cross-store (SD/L14), same-document (CL-UNIQ) each force the link contribution to the `P ∩ Q` diagonal.
- **Structure (X0, X4, X4c, X5).** Finiteness (S8-fin), windowing as exact restriction (common-predicate comprehension), single-span clipping to an integer interval (monotone shift via TS4/TS5 + span convexity T12(c), reassembled with TS3), and the locality factoring `(P,Q,res|P,res|Q)` with exact non-redundancy — all sound.
- **Report (X10, X11).** Cardinality-`n` feet (TS4/TS5), succ single-valuedness, unique in-relation predecessor (TS2 at equal depth via S8-depth), acyclicity (TS4) → unique maximal-run partition; the lex order is strict-total because distinct pairs differ in `(first start, second start)`. Cross-document depth differences do not break the per-foot TS2 application.
- **Self-comparison (X8)** and the **worked example**: I recomputed the arrangements, the three-element relation with fan-out, both maximal pairs, the swap (tie-break exercised), the `([1,3],δ(2,2)) → [1,5]` clip to `{[1,3],[1,4]}`, and the disjoint-window detector `{a,b}∩{c,b}={b}`. Every count is forced by the definitions. I also checked the region-definition's `σ=([1,5],[3]) ⊕ → [4]` example yields `[2,7]∈⟦σ⟧` at subspace 2.
- **Stability (X-T, X6, X7).** The transport lemma is correct; X7 instantiates it faithfully across the full edit vocabulary, and the shifting-contraction case (X7(iii)) does not assume injectivity for free — it discharges the piecewise-map collision via `L ∩ Q₃ = ∅` (D-DP(a)). X6's chain composition explicitly names its two premises (endpoint persistence, interleaved intermediate edits) and composes injective res-preserving factors. The contraction/reordering wp forms are non-trivial.
- **Citations** are all to foundation ASNs and resolve correctly; no cross-ASN references to non-foundations; no notation reinvented. The operation is a pure observation (`Σ'=Σ`), so invariant preservation is trivial and the stability theorems correctly target result durability instead.

On the anti-bloat lens: the interpretive prose (line-diff analogy, Nelson design-intent readings, the X8 closing reading) falls under the note's own carve-outs for analogies and operation-meaning statements, and the appended consequences (X5's three readings, X6(d)) are the required derived-consequence depth, not filler. Such forward references as exist ("X9 shows…", "transport theorems below") are isolated single pointers, appended after rather than interleaved within claims, so a precise reader is not made to skip past noise to follow any claim. I found no reviser-drift pattern (no excluded-case paragraphs, no relocated-finding residue, no ordering justifications, no duplicate-claim-in-different-words above the bar).

## REVISE

None.

## OUT_OF_SCOPE

### Topic 1: Reference-presence vs arrangement-presence as the basis of correspondence
The region clip `∩ V_{s_C}(d_i)` makes correspondence a fact about positions the documents *currently arrange*; content shared but arranged in neither operand is invisible. This is the correct basis for "which parts of two versions are the same," and the ASN already lists the alternative as an open question. Extending correspondence to span-referenced-but-unarranged content is new territory for a future ASN, not a gap here.

### Topic 2: n-way and cached correspondence
Composition of pairwise reports into n-way alignment, and the consistency contract a derived correspondence index must satisfy to keep cached reports exact across edits, are genuinely downstream — the kernel transitivity law (X6(d)) and the locality factoring (X5) give the right primitives, but the composition guarantees belong elsewhere.

VERDICT: CONVERGED
