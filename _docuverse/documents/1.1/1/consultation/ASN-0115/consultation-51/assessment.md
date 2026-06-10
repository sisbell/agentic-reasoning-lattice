# Channel Assignment — ASN-0115 review-51

**Date:** 2026-06-10 05:12

## Issue 1: "tacitly rely on" mischaracterizes the downstream dependency
Reason: Internal fix. The correct logical relationship is already established in the ASN — R6 takes `V_S(d) ≠ ∅` as hypothesis (which entails `S ∈ {s_C, s_L}` via S3★-aux), and `item` totality rests on S3★-aux applied to the active position `v`, not the start's subspace `S`. Dropping the misstated forward-inventory clause requires no design intent or implementation evidence; the preceding sentence already disposes of the case.

## Issue 2: design-rationale essay and a compressed claim in the `act` definition
Reason: Internal fix. Trimming the too-shallow/too-deep rationale and removing the self-forward-reference is editorial, and the compressed "empty by Confinement" claim is unpacked entirely from machinery already present — the Confinement lemma, S8-depth, prefix ordering, and T1 — with the review itself naming the missing steps (`m_S(d) = #s − 1` forces a proper prefix, hence `< s`, hence outside `⟦σ⟧`). No channel needed.
