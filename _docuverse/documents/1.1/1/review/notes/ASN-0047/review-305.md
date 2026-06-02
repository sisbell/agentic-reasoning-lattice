# Review of ASN-0047

## REVISE

### Issue 1: K.μ⁻ "equivalence" of constructive precondition and post-state characterization is overstated — strictness is dropped on one side

**ASN-0047, *K.μ⁻ admissible contraction shape***: "The constructive precondition is *equivalent* to the post-state characterization 'M'(d) satisfies D-CTG★/D-MIN★/D-SEQ★ with value preservation on survivors'; this equivalence is proved in *K.μ⁻ admissible contraction shape* below... justifying the constructive precondition as fully general — every contraction admissible under the post-state invariants takes the per-subspace suffix-prefix retention form."

**Problem**: The constructive precondition includes a strict-contraction conjunct — "with at least one S admitting strict contraction `n'_S < n_S`." The post-state characterization as quoted does **not**, and the reverse-direction proof explicitly hypothesizes only the *non-strict* `dom(M_cand(d)) ⊆ dom(M(d))` and concludes `n'_S ≤ n_S` ("giving `{1, ..., n'_S} ⊆ {1, ..., n_S}`, which forces `n'_S ≤ n_S`"). The identity restriction (`M_cand(d) = M(d)`, all `n'_S = n_S`) therefore satisfies the post-state characterization yet is **not** a valid K.μ⁻ — its effect clause `dom(M'(d)) ⊂ dom(M(d))` fails. So the constructive precondition (strict) is strictly *stronger* than the quoted post-state characterization (non-strict); they are not equivalent. The prose compounds this by saying "every *contraction* admissible..." (strict implied) while the proof body uses `⊆` (non-strict) — an internal mismatch between the claim and its proof.

**Required**: Either (a) include strict contraction in the post-state characterization (`dom(M'(d)) ⊂ dom(M(d))`, strict) so the biconditional genuinely holds, or (b) state explicitly that the equivalence is a *shape* equivalence (suffix-prefix retention form, `n'_S ≤ n_S`), with strict contraction being a separate firing condition discharged via the effect clause, and have the reverse-direction hypothesis match the prose.

### Issue 2: Document-ordering justification in body prose (forward-reference accretion)

**ASN-0047, *The state model*, Bridging lemma (M–E_doc)**: "(†) holds by the lockstep K.δ effect (which grows `dom(M)` and `E_doc` together by `{e}`) and the default-value convention stated immediately below."

**Problem**: "stated immediately below" is the flagged forward-reference pattern — prose whose function is to justify document ordering rather than advance the claim. The reader must locate the downstream convention to validate (†). This is the `review-mode.anti-bloat` classifier's named pattern (prose pointing at placement of a later item).

**Required**: State (†)'s justification self-containedly (the K.δ Document-case effect grows both sets by `{e}`; off-`E_doc` the convention fixes `M(d) = ∅`) without the locational pointer, or fold the default-value convention's relevant clause inline.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link/content withdrawal
**Why out of scope**: The ASN's own Open Questions already name this (interior `DELETEVSPAN` compaction vs. suffix-only K.μ⁻). Interior-deletion-with-renumbering is a distinct operation belonging to a future ASN, not a gap in the present suffix-removal model, which is internally consistent.

VERDICT: REVISE
