# Review of ASN-0068

## REVISE

### Issue 1: Action-point = 1 argument is incorrect for `width₁ = 1`

**ASN-0068, "The Input" section, action-point justification paragraph**: "When `actionPoint(width(σ)) = 1`, TumblerAdd (ASN-0034) makes the first component of `reach(σ)` equal to `start(σ)₁ + width(σ)₁ > S`, so `⟦σ⟧` extends into tumblers with first component greater than `S` — leaving the subspace `S`."

**Problem**: The inference "reach₁ > S ⟹ `⟦σ⟧` contains tumblers with t₁ > S" fails when `width₁ = 1`. For `width = [1, 0, ..., 0]` of depth m_σ, reach = `[S+1, 0, ..., 0]`. By T1, any `t < reach` requires either `t₁ < S+1` (giving `t₁ ≤ S`) or `t₁ = S+1` with a later position `i` satisfying `t_i < reach_i = 0` (impossible). So `⟦σ⟧` contains no tumblers with `t₁ > S` in this case — the span stays in subspace `S`, contrary to the "leaves the subspace" conclusion. The V-position capture is nevertheless unbounded: every V-position `[S, 1, ..., 1, k]` with `k ≥ start_{m_σ}` satisfies `t₁ = S < S+1 = reach₁`, hence lies in `⟦σ⟧` by T1 case (i). The substantive issue with `actionPoint = 1, width₁ = 1` is therefore the same "captures the subspace's entire trailing extent" failure attributed to `actionPoint ≥ 2` in the next paragraph, not the "leaves the subspace" failure stated.

**Required**: Restructure the argument so the case analysis is exhaustive. The cleanest framing focuses on V-position capture: for any `actionPoint(width) < m_σ`, the divergence between `t = [S, 1, ..., 1, k]` and reach falls at some position `i < m_σ` where reach holds a strictly larger component than `t_i ∈ {S, 1}`, making T1 case (i) accept every V-position with `k ≥ start_{m_σ}`. The capture is unbounded regardless of where the action point sits below `m_σ`. The current "leaves the subspace" framing handles only the `width₁ ≥ 2` sub-case of `actionPoint = 1`.

## OUT_OF_SCOPE

(none — the ASN's Open Questions appropriately defer related topics to future ASNs)

VERDICT: REVISE
