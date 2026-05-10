# Review of ASN-0084

## REVISE

### Issue 1: PermutationDisplacement domain does not cover R-DISP's exterior case
**ASN-0084, Definition — PermutationDisplacement**: "For a position v in the affected range, define Δ(v) = ord(π(v)) − ord(v) (an integer, possibly negative)."
**Problem**: R-DISP claims "Δ = 0 on exterior" and quantifies "For all v₁, v₂ in the same region (exterior, α, μ, or β)." The exterior is not part of the affected range, so Δ(v) is undefined for exterior positions under the current definition. R-DISP references a value outside the domain of its defining term.
**Required**: Extend the definition to all of dom(M(d)): "For a position v ∈ dom(M(d)), define Δ(v) = ord(π(v)) − ord(v)." The natural extension gives Δ = 0 for exterior positions (where π(v) = v), grounding R-DISP's exterior clause.

## OUT_OF_SCOPE

### Topic 1: Uniqueness of maximally merged block decomposition
**Why out of scope**: R-BLK establishes that the reassembled blocks satisfy B1–B3, and the worked examples show merging to a canonical form. But the uniqueness of the maximally merged decomposition (independent of merge order) is not proven. This is a valid property to establish but belongs in a future ASN on block decomposition theory, not in this one — R-BLK's correctness does not depend on it.

### Topic 2: k-cut generalization and composition
**Why out of scope**: Already identified as open questions by the ASN. These extend the theory beyond the two-region transposition class defined here.

VERDICT: REVISE
