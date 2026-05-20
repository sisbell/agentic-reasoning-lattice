# Channel Assignment — ASN-0047 review-138

**Date:** 2026-05-19 23:43

## Issue 1: Worked example uses "non-vacuously" parenthetical that obscures the claim
Reason: Pure clarity/wording fix in a worked example. S8-depth and `subspace(v)` are already defined in the ASN; the rewrite uses only those definitions, no external evidence needed.

## Issue 2: Matrix entry "restriction of decomposition" for S8★ under K.μ⁻ understates the discharge
Reason: The trivial length-1 decomposition for S8★(s_L) is already established in the ASN body under S8★'s definition. The fix extends that mechanism to the matrix cell — internally consistent with what's already proved.

## Issue 3: K.μ⁻ admissible contraction shape — quantifier ambiguity in cited per-state invariants
Reason: Proof-structure clarification. The ASN already contains all required material (D-CTG★, D-MIN★, D-SEQ★, φ_S bijection); the fix reorganises the hypothesis statement to mark the candidate post-state explicitly.

## Issue 4: GlobalLineage proof for link addresses introduces unstated TA5(d) length identity at k=1
Reason: Missing citation of TA5(d) (ASN-0034), already a foundation property cited elsewhere in this ASN. The required content is the foundation rule itself; adding the citation line is internal.

## Issue 5: K.μ~ dependency chain — Step (A) names L14 as a premise
Reason: L14's preservation at every reachable state is in ExtendedReachableStateInvariants as a Class (a) per-state invariant. The fix adds an explicit per-state quantification at the head of *Decomposition of K.μ~* — derivable from the ASN's own inductive structure.
