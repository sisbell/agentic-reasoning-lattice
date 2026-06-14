# Channel Assignment — ASN-0134 review-26

**Date:** 2026-06-14 04:55

## Issue 1: W5's out-of-order nullify dichotomy is non-exhaustive
Reason: The fix restructures W5's two-case "Either way" into a trichotomy partitioned on the already-stated P-tgt precondition (`a ∈ A_rel^Σ ∨ a = a_emit(Σ, d_retr)`), with the third case (the retractor's own not-yet-emitted non-frontier slot) and its decline behavior following directly from P-tgt's disjunctive structure plus the chain/frontier model already in §4 (H0, FrontierUnification) — the soundness conclusion is unchanged, and the supporting T12 well-formedness of the to-span is a foundational fact from the cited dependencies (ASN-0086/0128) the author already has, not implementation or design-intent evidence.
