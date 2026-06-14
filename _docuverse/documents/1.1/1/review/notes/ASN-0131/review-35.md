# Review of ASN-0131

I checked the core definition, the worked instance, and each derived claim (RE-UDIST, RE-SEL, RE-CWP, RE-RET, and the stability catalogue). The math is, with one exception, sound and unusually careful — the worked example exercises every postcondition by hand, the contraction weakest-precondition is genuinely non-trivial and correctly derived, and the retraction analysis properly refuses to over-claim about the type slot `Θ` (carrying `coverage(Θ) ∩ dom(Σ.C) = ∅` as a flagged hypothesis rather than a theorem). The one substantive error is a uniqueness claim in the stability section that contradicts the note's own RE-CWP.

## REVISE

### Issue 1: "the one arrangement edit on `d` that cannot perturb a content-region answer" is false

**ASN-0131, Stability section ("Under editing of the queried document," final paragraph)**: "The link-subspace extension `K.μ⁺_L`… **It is the one arrangement edit on `d` that cannot perturb a content-region answer**, and the content-subspace restriction is exactly what secures it."

**Problem**: K.μ⁺_L is not unique in this. A per-subspace `K.μ⁻` contraction that retains the entire content subspace (`n'_{s_C} = n_{s_C}`) while strictly contracting the link subspace (`n'_{s_L} < n_{s_L}`, admissible whenever `V_{s_L}(d) ≠ ∅` since at least one subspace strictly contracts) is *also* an arrangement edit on `d` itself that cannot perturb a content-region answer (`W ⊆ s_C`), by the identical content-subspace-restriction route: for `W ⊆ s_C`, `W ∩ dom(Σ'.M(d)) = W ∩ V_{s_C}(d) = W ∩ dom(Σ.M(d))` with retained-position agreement, so `image(W, d, Σ') = image(W, d, Σ)`; and K.μ⁻ frames `Σ.L`, so `Avail(Σ)` is unchanged. Hence `RE(W, d, Σ') = RE(W, d, Σ)`.

This is not a mere omission — it contradicts the note's own **RE-CWP**, which establishes `RE(W, d, ·) = RE(W, d, Σ)` for any `K.μ⁻[d, R]` with `Δ = ∅`, and a content-fully-retaining (in particular link-only) contraction is exactly the `Δ = ∅` case. The prose and RE-CWP disagree about whether a link-subspace-only contraction can perturb the answer. RE-EDIT carries the same incompleteness: "every other transition — including the link-subspace edit `K.μ⁺_L` under `W ⊆ s_C` — leaves it fixed" names only K.μ⁺_L as the representative fixed-leaving link-subspace edit.

(For the record, there is no symmetric "link-only K.μ~" to worry about: K.μ~ is link-subspace-fixing by admissibility (v) and requires a non-trivial content effect by its precondition, so it always touches content. The two link-subspace-confined edits are exactly K.μ⁺_L and link-only K.μ⁻.)

**Required**: Replace "the one arrangement edit" with the correct statement — the content-subspace restriction secures *every* link-subspace-confined arrangement edit on `d` (link extension `K.μ⁺_L` and any link-subspace-only `K.μ⁻` contraction) against perturbing a content-region answer. Amend RE-EDIT's "including the link-subspace edit `K.μ⁺_L`" to name the class (or both edits), and state the consistency with RE-CWP's `Δ = ∅` case explicitly.

### Issue 2: meta-prose accreted around the ASN-0086 applicability bridge

**ASN-0131, "The unit of the answer" section (standing-assumption paragraph)**: "So the link store evolves identically under ASN-0086's transition relation and under ASN-0047's — *the very transitions that populate an arrangement leave `Σ.L` fixed* — and every ASN-0086 lemma that constrains `Σ.L` alone holds verbatim at every ASN-0047-reachable state, including the *populated-arrangement* states whose arrangements ASN-0086's own (empty-arrangement) layer never reaches. **We invoke each such lemma where it is used.**"

**Problem**: The em-dash clause "the very transitions that populate an arrangement leave `Σ.L` fixed" restates the immediately preceding sentence ("the arrangement movers … all frame the link store (`L' = L`)") in different words. "We invoke each such lemma where it is used" is a content-free citation promise that advances no reasoning — exactly the kind of meta-prose the precise reader must skip past. The genuinely load-bearing claim is one sentence: because `Σ.L` evolves only through `K.λ`, every ASN-0086 lemma constraining `Σ.L` alone holds at every ASN-0047-reachable state.

**Required**: Cut the restatement clause and the closing promise; keep the single load-bearing sentence (the bridge itself is sound and needed — only the surrounding accretion should go).

## OUT_OF_SCOPE

None. The Open Questions are correctly scoped as future work (rendered-into-V-order output OQ3, intersection-distributivity OQ4, non-co-resident link store OQ5, type-slot-versus-content OQ6, link-subspace regions OQ7), and the note does not smuggle claims for the out-of-scope sibling operations — FINDLINKSFROMTOTHREE and the rest are named only as contrasts, never specified.

VERDICT: REVISE
