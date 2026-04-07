# Proof Verification: D-MIN

Looking at D-MIN as an axiom (design constraint):

**Axiom statement**: Sound. D-MIN asserts `min(V_S(d)) = [S, 1, ..., 1]` as a convention, justified by Nelson's numbering-from-1 practice and T4's exclusion of zero from non-separator positions. The formal contract correctly classifies this as an axiom.

**Dependency usage**: D-CTG, D-CTG-depth, S8-depth, S8-fin, and T4 are all referenced in the justification and corollary. All are used as claimed.

**Formal contract**: Matches the narrative — axiom with the correct quantification (every d, every S with V_S(d) non-empty).

**Corollary**: The reasoning is correct — D-CTG-depth pins components 2 through m−1 to shared values, D-MIN forces those shared values to be 1, D-CTG forbids gaps in the last component, D-MIN gives minimum k = 1, and S8-fin bounds the maximum. But the text ends with:

> D-CTG restricted to the last component forbids gaps among the k values; D-MIN gives the minimum k = 1; S8-fin bounds the maximum at some finite n. Thus:

The conclusion after "Thus:" is never stated. The corollary builds the full derivation but the formal result — `V_S(d) = {[S, 1, …, 1, k] : 1 ≤ k ≤ n}` for some finite n ≥ 1 — is missing.

```
RESULT: FOUND

**Problem**: The corollary (general form) trails off at "Thus:" with no
conclusion. The reasoning is complete but the derived statement is absent.

**Required**: State the corollary's conclusion after "Thus:", e.g.:
`V_S(d) = {[S, 1, …, 1, k] : 1 ≤ k ≤ n}` for some finite `n ≥ 1`,
matching the depth-2 illustration ("addresses 1 through 100") that
the surrounding text motivates.
```
