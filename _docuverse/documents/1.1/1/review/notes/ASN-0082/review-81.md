# Review of ASN-0082

I worked through every proof in this ASN: the post-insertion shift (I3 and its eight preservation lemmas), the post-contraction shift (D-SHIFT through S7-post), the ordinal-extraction machinery (OrdAddHom, OrdinalExceedsDisplacement), and both span-width corollaries (I3-S, D-S). I checked the well-definedness arguments, the disjointness of assignment regions, and every boundary case.

The arithmetic holds. Specifically I verified:

- **I3 well-definedness** — the overlap case (a position that is both a shift source and a shift destination, e.g. `[1,5]` in the worked example) is handled correctly: TS2 injectivity keeps destinations distinct, TS4 strict-advance keeps every image past the left region, and I3-V's exclusion clause correctly retains overlap positions while vacating the rest. dom(M′)∩S = left ∪ shifted-images is fully and consistently determined.
- **OrdinalExceedsDisplacement** — TA4's preconditions genuinely discharge at depth 1 (zero-prefix quantifier `1 ≤ i < 1` vacuous, `#ord(p) = #w_ord = k = 1`); the strict/weak split via TumblerAdd's `a⊕w ≥ w` plus `ord(p)` being Pos is correct.
- **D-CTG-post** (the hardest invariant, the one most often hand-waved) — the closed form `L ∪ Q₃ = {[1,k] : 1 ≤ k ≤ N−c}` is derived explicitly, the consecutive-integer boundary argument is shown, and the D-CTG quantifier is checked directly against the post-state rather than asserted. No gap.
- **Boundary coverage** — empty document, insert-at-start, insert-past-end, contraction with L=∅, R=∅, L=∅∧R=∅ (full deletion), cross-subspace in both directions, and a shifted image landing in a former tombstone slot are all worked through with per-clause verification.
- **Invariant coverage** — every ASN-0036 invariant conjunct (S2, S3, S8-depth, S8a, S8-fin, S7a/b/d, D-CTG, D-MIN, D-SEQ) has a dedicated preservation lemma; none is dispatched by "similarly."

I found no missing case, no proof-by-checkmark, and no unaddressed invariant conjunct. The off-subspace/off-document dispatch convention is genuine consolidation (it removes repetition rather than adding meta-prose), and the recent prose tightening appears to have cleared the forward-reference accretion the classifier targets — I did not find defensive justifications, exhaustiveness essays, use-site inventories, or duplicated paragraphs that obstruct a claim.

## OUT_OF_SCOPE

### Topic 1: Generalizing contraction to ordinals of depth > 1
The contraction restricts to `#p = 2` (single-component ordinals). At deeper ordinals, `σ(v) = vpos(1, ord(v) ⊖ w_ord)` would produce zero-valued intermediate components (TumblerSub on a shared `[1,…,1]` prefix zeros out positions before the divergence), colliding with S8a positivity — exactly TA4's zero-prefix obstruction.
**Why out of scope**: This is correctly identified and deferred in Open Questions 2 and 3. Lifting it requires a last-component-only shift operation (a different construction), which is new territory, not a defect in this ASN's depth-2 result.

### Topic 2: Updating external references after a shift repositions a V-position
**Why out of scope**: Already named as the first Open Question; it concerns a cross-ASN reference-tracking mechanism not in this ASN's remit.

META: (none — the ASN defines arrangement-layer state transformations and their invariant preservation abstractly; it has not drifted into implementation mechanics.)

VERDICT: CONVERGED
