# Review of ASN-0058

## REVISE

### Issue 1: M-int's subspace agreement step compresses the case analysis
**ASN-0058, M-int (TumblerIntervalCharacterization), "Subspace agreement" step**: "Suppose (y)_1 ≠ (x)_1. Since x ≤ y, T1(i) gives (y)_1 > (x)_1"
**Problem**: The transition elides intermediate reasoning. Under the supposition `(y)_1 ≠ (x)_1`, the case `x = y` is excluded (it would force `(y)_1 = (x)_1`), so `x < y`. T1's case (ii) is then also excluded (it would give `(x)_i = (y)_i` for all `i ≤ #x`, including `i = 1`). Only after these eliminations does T1(i) apply with divergence necessarily at position 1, yielding `(x)_1 < (y)_1`. The current phrasing makes "T1(i) gives" look like a direct invocation when it actually requires the prior case eliminations.
**Required**: Make the case-elimination explicit, e.g., "Since `(y)_1 ≠ (x)_1` and `x ≤ y`, we have `x < y`. T1 case (ii) is then excluded by prefix agreement forcing `(y)_1 = (x)_1`; T1 case (i) holds with divergence at position 1 (any later divergence would also force `(y)_1 = (x)_1`), giving `(y)_1 > (x)_1`."

### Issue 2: C0's invocation of T0(a) is indirect
**ASN-0058, C0 (OrdinalDisplacementNecessity) proof**: "By T0(a), j ranges over unboundedly many values, yielding infinitely many depth-m tumblers in ⟦σ⟧."
**Problem**: T0(a) (UnboundedComponentValues, ASN-0034) asserts the existence of a same-depth tumbler whose chosen component exceeds an arbitrary bound `M`. The proof's construction `wⱼ = [u₁, ..., u_{m-1}, j]` for each `j > uₘ` doesn't need T0(a)'s perturbation semantics — it builds specific tumblers, which follow from T0's comprehension clause (any length-`m` ℕ-sequence is in `T`) together with ℕ being infinite (NAT-carrier). T0(a) is the wrong primitive to cite for the count of distinct `wⱼ`.
**Required**: Cite T0's comprehension clause (placing each `wⱼ ∈ T`) and NAT-carrier (for unbounded `j`), or rephrase the existing citation to be about reachability of `wⱼ` for arbitrary `j` via T0(a). Update C0's dependency list accordingly.

## OUT_OF_SCOPE

(No OUT_OF_SCOPE items. The ASN stays within mapping block algebra and explicitly defers consequential topics — operations on arrangements, link semantics — to future ASNs.)

VERDICT: REVISE
