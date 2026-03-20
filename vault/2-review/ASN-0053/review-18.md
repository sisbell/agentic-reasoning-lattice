# Integration Review of ASN-0053

## REVISE

(none)

**S11a** (DifferenceSeparated): The disjoint-cases argument is direct from SC's classification and set difference identity. The claim of exactly 1 span follows from ⟦α⟧ being non-empty (T12/TA-strict). Clean.

**S11b** (DifferenceEqual): Trivially correct — set minus itself is empty.

**S11c** (DifferenceOverlap): Both sub-cases are handled explicitly with element-chasing. Case 1 correctly identifies {t : start(α) ≤ t < start(β)} as the difference (positions in α before β starts; positions at or past start(β) fall in β since reach(α) < reach(β)). Case 2 correctly identifies {t : reach(β) ≤ t < reach(α)} (positions in α before reach(β) fall in β since start(β) < start(α)). D1 preconditions are fully verified in both cases via the level-uniformity chain (#reach = #start for each span, #start(α) = #start(β) by level_compat). T12 verified for both constructed spans. Level-uniformity of the result verified. The "exactly 1" claim is correct — in proper overlap, the difference is always non-empty (Case 1: start(α) < start(β); Case 2: reach(β) < reach(α)).

**S11d** (GeneralDifferenceBound): The table is exhaustive over all five SC cases, with SC(iv) correctly split into forward containment (→ S11, at most 2 spans) and reverse containment (→ ⟦α⟧ ⊆ ⟦β⟧, 0 spans). The reverse containment derivation is explicit and correct. Maximum of 2 across all cases is established.

**Integration quality**: New sections are placed after S11 (their dependency) and before the implementation observations. S11d references S11a, S11b, S11c which all precede it. Notation (⟦·⟧, ⊕, ⊖, SC, level_compat, level-uniform) is consistent with the rest of the document. Registry entries have correct labels, types, and status.

VERDICT: CONVERGED
