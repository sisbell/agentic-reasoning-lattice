# Channel Assignment — ASN-0120 review-4

**Date:** 2026-06-09 00:40

## Issue 1: "content addresses have `#E = 2`" is the load-bearing fact, but only `#E ≥ 2` is cited
Reason: The fix is a citation swap fully internal to the formal substrate — the review already names the exact lemmas (FirstEmission, ChainDiscipline/TA5(c), ChainMembershipForOrigin, all ASN-0093) that yield `#E = 2` exactly, and the persistence-under-K.α argument follows from those plus S0/S1 already present. No design intent or implementation evidence is needed; it is a matter of citing established foundation claims correctly.

## Issue 2: ML6 claims MAKELINK can create L9-ghost types, but `ρ`-resolution forbids it
Reason: The contradiction is derivable from the ASN's own content — `ρ(R₃, Σ) ⊆ dom(Σ.C)` (ML1) and the precondition `ρ(R₃, Σ) ≠ ∅` (ML6) together entail the type's resolved addresses are always stored content, so MAKELINK cannot mint an L9 ghost type. The corrected statement is purely a consistency fix against constraints the ASN already establishes.
