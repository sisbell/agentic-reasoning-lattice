# Review of ASN-0058

## REVISE

### Issue 1: M-sub closing prose cites wrong axiom for V-position depth
**ASN-0058, M-sub (SubspaceConfinement), closing paragraph**: "clause (a) further requires `#v ≥ 2`, which holds for every V-position in `dom(M(d))` since S7b/S7c (ASN-0036) place those positions in element subspaces of depth ≥ 2."
**Problem**: S7b (ElementLevelIAddresses) and S7c (ElementFieldDepth) are axioms with precondition `a ∈ dom(Σ.C)` that state, respectively, `zeros(a) = 3` and `#E(a) ≥ 2` — both at I-addresses, not V-positions. They establish nothing about positions in `dom(M(d))`. The depth bound `#v ≥ 2` for V-positions comes from S8a (VPositionWellFormedness, ASN-0036): `(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))`. A reader chasing the cited axioms will find facts about I-addresses, not the V-position fact being claimed.
**Required**: Replace the citation chain with S8a — e.g., "which holds for every V-position in `dom(M(d))` by S8a (VPositionWellFormedness, ASN-0036)." The same correction also tightens the parallel framing for clause (b), which is already correctly grounded via B3 + S3.

VERDICT: REVISE
