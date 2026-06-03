# Channel Assignment — ASN-0071 review-9

**Date:** 2026-06-02 22:28

## Issue 1: Finiteness bound conflates elementary and composite transition counts
Reason: Internal fix. The repair is a counting correction using facts the ASN already invokes from ASN-0047 (composites decompose into finitely many elementary steps via ValidCompositeAmended; K.δ adds ≤ 1 entity; reachable states have finite composite ancestry). Either re-index `n` to elementary steps or argue finiteness without the exact bound — no design intent or implementation evidence is required.

## Issue 2: The resolve-relationship equation is asserted without derivation
Reason: Internal fix. The required derivation depends only on ASN-0058's published claims (C1a's maximally merged decomposition over `dom(f) = ⟦σ⟧ ∩ dom(M(d_s))` and B3/Consistency giving `a_j + k = M(d_s)(v_j + k)`), which are part of the spec corpus the ASN already cites. Supplying the three-step unfolding (or demoting to an informal remark) needs neither Nelson's intent nor udanax-green evidence.
