# Review of ASN-0073

## REVISE

### Issue 1: Non-empty case subspace identity argument uses m ≥ 2 without establishing it

**ASN-0073, Valid Insertion Position, structural verification**: "since δ(j, m) has action point m and m ≥ 2, TumblerAdd copies components 1 through m − 1 unchanged"

**Problem**: The subspace identity proof pivots on m ≥ 2. Without it, TumblerAdd at action point m = 1 gives r₁ = S + j, landing in subspace S + j, not S. The non-empty case takes m (the common depth from S8-depth) as given but never states or derives m ≥ 2. The empty case correctly requires m ≥ 2, but D-SEQ and D-CTG do not forbid m = 1 for a non-empty subspace. At m = 1, D-SEQ forces V_S(d) = {[S]} (the subspace constraint collapses n to 1), and the predicate generates shift([S], 1) = [S + 1] as the append position — outside subspace S. The assertion "m ≥ 2" is load-bearing but unanchored.

**Required**: Either (a) add m ≥ 2 as an explicit precondition in the non-empty case, or (b) derive it: if V_S(d) was constructed via valid insertions starting from the empty case (which requires m ≥ 2) and S8-depth preserves depth, then m ≥ 2 holds inductively. State the constraint and its source. The properties table should also reflect m ≥ 2 for the non-empty case.

## OUT_OF_SCOPE

### Topic 1: Operation-level D-CTG preservation
**Why out of scope**: The ASN correctly defers proof that insertion at a ValidInsertionPosition preserves D-CTG, D-MIN, and S2 to operation-level ASNs. The predicate is a structural precondition, not a preservation theorem.

VERDICT: REVISE
