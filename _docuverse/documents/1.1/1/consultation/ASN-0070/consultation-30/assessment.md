# Channel Assignment — ASN-0070 review-30

**Date:** 2026-06-02 22:43

## Issue 1: Case analysis in F-canonical Step 1 does not state exhaustiveness
Reason: Internal fix. The exhaustiveness bound `1 ≤ actionPoint(ℓ) ≤ #ℓ = m_S(d)` comes from the ActionPoint postcondition (ASN-0034), already cited in the note; adding the one sentence requires no design intent or implementation evidence.

## Issue 2: DEF/THM cataloguing paragraph is meta-prose
Reason: Internal fix. Pure deletion of self-referential labelling prose; no semantic content to verify against either channel.

## Issue 3: F-multi Depends carries "cited only for X, not Y" disclaimers
Reason: Internal fix. Rewriting dependencies positively uses roles already stated in the note (S5 as cardinality witness, K.μ⁺ non-injectivity for reachability); no new claim about Nelson's intent or Gregory's code is needed.

## Issue 4: State-Dependence section restates without advancing
Reason: Internal fix. The operative point (L12-invariance of `L(ℓ)` vs. variation of `M(d)`) is already established in the note's own F-state corollary and L12 citation; trimming rhetoric needs no external channel.
