# Review of ASN-0084

I'll review this ASN against the Dijkstra standards: every case shown, every invariant addressed, no hand-waves.

## REVISE

### Issue 1: D-SEQ citation invokes a foundation property outside its domain
**ASN-0084, R-PIV proof and R-SWP proof**: "By D-SEQ, these are distinct positions in V_S(d) (since R-PRE(iv) guarantees all ordinals from p to p + w_α + w_β − 1 are occupied)."
**Problem**: D-SEQ in ASN-0036 is stated only for the text subspace V_1(d), not for arbitrary V_S(d). The actual argument relies on R-PRE(iv) plus depth-2 sequential ordinals, which is local contiguity supplied by the precondition — not D-SEQ. Same loose citation appears in R-SWP's exhaustiveness step.
**Required**: Replace the D-SEQ citation with R-PRE(iv) (and S8a's positivity at depth 2 if needed). Same fix for R-SWP's "ordinals are consecutive by D-SEQ" clause. If D-SEQ generalisation to arbitrary subspaces is intended, derive it explicitly from R-PRE(iv) restricted to depth 2.

### Issue 2: Backward-extension argument in canonical decomposition uses Merge implicitly
**ASN-0084, canonical decomposition part (b), v₁ = v₂ case**: "so shift(M(d)([S, ord(v₁) − 1]), 1) = a₁ = M(d)(v₁). This shows b₁ can be extended backward while maintaining S8(b), contradicting maximality."
**Problem**: The argument explicitly verifies only S8(b) at offset 1 of the extended run. The full extension to ([S, ord(v₁)−1], a_new, n₁+1) requires verifying S8(b) at offsets 0 through n₁. This is implicitly an application of the Merge lemma (defined just above) to ([S, ord(v₁)−1], a_new, 1) and b₁, but Merge is never named. Same implicit Merge use in the n₁ = n₂ argument's "extends b₁ forward at offset n₁".
**Required**: Either invoke Merge explicitly ("by Merge applied to the singleton run (...) and b₁, the extended run is valid") or verify S8(b) at all offsets, including the offset-2-through-n₁ chain using S8(b) of b₁ at offsets 0 through n₁−1.

### Issue 3: Empty-exterior edge cases not verified
**ASN-0084, R-PIV/R-SWP and worked examples**: Both worked examples have non-empty left and right exteriors. R-PRE permits c₀ = [S, 1] (empty left exterior) and c_{n-1} = [S, N+1] (empty right exterior) — the implicit bound noted in the "Outside ⋃_k V(b_k)" paragraph.
**Problem**: The boundary cases — affected range covering all of V_S(d), or starting at the first position, or ending one past the last position — are handled implicitly by vacuous quantification in R-EXT. No proof step or worked example demonstrates this. The prompt's "Boundary cases mandatory — Empty, zero, first, last" applies.
**Required**: Either add a small worked example with empty exterior (e.g., 3-cut on V_S(d) = {[1,1], [1,2]} with cuts [1,1], [1,2], [1,3]) or add an explicit sentence in R-PIV/R-SWP confirming that R-EXT's quantification is vacuous when c₀ = min(V_S(d)) or c_{n-1} = max(V_S(d)) + 1.

### Issue 4: R-DISP's 4-cut μ-case statement is not self-contained
**ASN-0084, R-DISP statement**: "for 4-cut, Δ = +(w_β + w_μ) on α, Δ on μ depends on the comparison of w_β and w_α (the three sub-cases above), Δ = −(w_α + w_μ) on β, Δ = 0 on exterior."
**Problem**: The lemma statement refers to "the three sub-cases above" without restating them. A lemma should be self-contained — a reader citing R-DISP shouldn't need to scroll up to reconstruct the μ branch.
**Required**: In R-DISP, list the three sub-cases inline: Δ = +(w_β − w_α) when w_β > w_α; Δ = −(w_α − w_β) when w_β < w_α; Δ = 0 when w_β = w_α.

### Issue 5: Disjointness justification is imprecise
**ASN-0084, R-PIV proof**: "The R-P1 ordinal range is [p, p + w_β). The R-P2 ordinal range is [p + w_β, p + w_β + w_α). Since w_β ≥ 1, these ranges are disjoint."
**Problem**: Disjointness of [p, p + w_β) and [p + w_β, p + w_β + w_α) follows from the half-open interval structure (right endpoint of first equals left endpoint of second, neither contains its right endpoint), not from w_β ≥ 1. The role of w_β ≥ 1 is to ensure both intervals are non-empty.
**Required**: Reword as "Both ranges are non-empty (since w_β ≥ 1 and w_α ≥ 1), and they are disjoint because [a, b) ∩ [b, c) = ∅."

### Issue 6: Subspace m_S = 2 restriction is implicit
**ASN-0084, State and Vocabulary**: "We restrict to depth-2 V-positions (#v = 2, ordinal depth 1) throughout this ASN."
**Problem**: CS4 fixes cut depth at 2. By S8-depth (ASN-0036), within subspace S all V-positions share a common depth m_S. So this ASN only applies to subspaces with m_S = 2. The implicit restriction is not stated.
**Required**: State explicitly that the ASN's operations apply only to subspaces S of document d with m_S = 2, since CS4 forces this via S8-depth.

## OUT_OF_SCOPE

### Topic 1: k-cut generalisations for k > 4
**Why out of scope**: Open Question #1 explicitly defers; CS1 restricts n ∈ {3, 4}. Extending to k > 4 is future work.

### Topic 2: Composition of rearrangements
**Why out of scope**: Open Question #2 defers. Composition properties (is the composition of two cut-point rearrangements always a cut-point rearrangement?) belong in a downstream ASN once a richer operation calculus exists.

### Topic 3: Run-count growth bounds and canonical-boundary constraints
**Why out of scope**: Open Questions #3 and #4 defer. The ASN notes "The partition B' is valid but not necessarily maximal" — bounds analysis is future work.

### Topic 4: V-positions at depth > 2
**Why out of scope**: Explicitly declared a strict scope boundary.

### Topic 5: Interaction with content-store operations (INSERT, DELETE, COPY)
**Why out of scope**: This ASN concerns arrangement rearrangements only — operations that modify M(d) with C' = C. Content-store-modifying operations belong in separate ASNs.

### Topic 6: Inverse rearrangements
**Why out of scope**: Related to composition (Topic 2). Not addressed but a natural follow-up.

VERDICT: REVISE
