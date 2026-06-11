# Channel Assignment — ASN-0115 review-73

**Date:** 2026-06-10 23:06

## Issue 1: R7 invokes `deliver(R, Σ')` without discharging its definedness precondition
Reason: Internal fix. The review identifies the exact missing step and the ASN's substrate already supplies it — M1 (ArrangementMonotonicity, ASN-0047/0093) lifts `dⱼ ∈ dom(Σ.M)` to the descendant state, and pinning spec-set-hood to the earlier state of the pair resolves the WLOG ambiguity; no design intent or implementation evidence is involved.

## Issue 2: the "nominal extent" sentence in §Exactness is incorrect as written
Reason: Internal fix. The corrected statement is fully derivable from the ASN's own R6 frontier analysis — D-SEQ★ gives the canonical start and bound frontier `n_S`, so `|act| = ℓ_{#ℓ}` iff depth-compatible and `s_{#s} + ℓ_{#ℓ} − 1 ≤ n_S` follows in both directions from material already in the note; neither channel adds anything.

## Issue 3: duplicated formulation-justification prose around R6 (forward-reference accretion)
Reason: Internal fix. This is editorial consolidation — keep the one unique fact (`m_S(d)` undefined when `V_S(d) = ∅`, hence the slice is pinned at depth `#s`) as a parenthetical and delete the redundant restatements; no semantic content changes, so no consultation is needed.
