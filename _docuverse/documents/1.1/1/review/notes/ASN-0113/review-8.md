# Review of ASN-0113

## REVISE

### Issue 1: W10's full-generality claim rests on a derivation that only covered one depth

**ASN-0113, "Why text and links must be reported apart" (W10/W11)**: "We record W10 (SubspaceConfinement): `(A t : t ∈ ⟦ext(d, S)⟧ : t₁ = S)`. ... Every `t ∈ ⟦ext(d, S)⟧` shares the prefix `[S,1,…,1]` (the derivation of W4 established this via T5), so its first component is `S`."

**Problem**: W10 quantifies over *all* `t ∈ ⟦ext(d, S)⟧` — tumblers of arbitrary depth, including the entire subtree hanging below each V-position. But the derivation of W4 explicitly restricts to V-slice tumblers: "Take any `t ∈ VSlice(S, m_S)`. Such a `t` has the form `[S, t_2, …, t_{m_S}]`..." — i.e. `#t = m_S`. The T5 application in W4 confines only depth-`m_S` tumblers. The deeper tumblers in the denotation (e.g. `[S,1,0,1]`, which lies in `⟦ext(d,S)⟧` for `m_S = 2`, `n_S ≥ 1`) are never addressed by W4's argument, yet they make up the bulk of the denotation. W10 is *true* — but only via a direct T1 argument on the first component (if `t₁ < S` then `t < start_S`; if `t₁ > S` then `t > reach`, both contradictions), which is **not** the cited W4 derivation. This is load-bearing: W11 (Disjointness) reasons "For any `t` in the intersection we would need `t₁ = s_C` and `t₁ = s_L` at once (W10)" over the *full* denotation intersection, so it requires W10 in the generality the cited derivation does not supply.

**Required**: Give W10 its own derivation covering arbitrary-depth `t` — the two-line first-component T1 argument — rather than citing W4's depth-`m_S`-restricted reasoning.

### Issue 2: The parenthetical characterization of the denotation's tumblers is false

**ASN-0113, "Why text and links must be reported apart" (W11)**: "(We do not invoke T7... whereas the tumblers here are V-positions and their subtrees — zeros = 0, distinguished by `t₁ = subspace(v)`...)"

**Problem**: `⟦ext(d, S)⟧` is the T1-interval `{t : start_S ≤ t < reach}`, which contains tumblers with zeros. For `m_S = 2`, `n_S ≥ 1`, the tumbler `[S,1,0,1]` satisfies `start_S = [S,1] < [S,1,0,1] < [S,1+n_S] = reach`, and `zeros([S,1,0,1]) = 1 ≠ 0`. So "their subtrees — zeros = 0" is incorrect: the subtrees of a V-position include tumblers with zero components. The conclusion (T7 is unnecessary, SC-NEQ on `t₁` suffices) is sound, but the stated reason rests on a false property of the denotation.

**Required**: Correct the characterization — the disjointness follows from `t₁ = S` for every `t` in each denotation (Issue 1's argument) combined with SC-NEQ, independent of any zero-count claim about denotation tumblers.

## OUT_OF_SCOPE

The Open Questions (non-contiguous fragmentation reporting, consumer-side absent-equals-zero convention, version-fork permanence, transclusion stability, consistency with a single overall extent, subspace-convention extension) are correctly deferred and match the stated Scope exclusions. No action needed.

VERDICT: REVISE
