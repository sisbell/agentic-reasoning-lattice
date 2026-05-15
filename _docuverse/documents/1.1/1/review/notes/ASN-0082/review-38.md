# Review of ASN-0082

## REVISE

### Issue 1: D-SEQ-post cardinality identification skips three distinct facts
**ASN-0082, D-SEQ-post proof, "It remains to identify n" paragraph**: "The pre-state has N positions; the contraction removes c positions (the set X with |X| = c), so |L ∪ Q₃| = N − c. Hence n = N − c."

**Problem**: The transition from "removes c positions" to "|L ∪ Q₃| = N − c" telescopes three independent cardinality facts without citation: (i) the trichotomy partition |V_1(d)| = |L| + |X| + |R| = N, (ii) |Q₃| = |R| via D-BJ's bijection σ : R → Q₃, (iii) L ∩ Q₃ = ∅ via D-DP(a). The prior sentence ("finite by S8-fin") only establishes finiteness via a loose bound (|V_1(d)| + |V_1(d)|), not the tight cardinality. The proof structure (cite D-CTG-post → D-MIN-post → S8-depth-post → S8a-post for the form, then identify n by cardinality) is sound, but the cardinality step itself needs the chain spelled out.

**Required**: Replace the one-sentence identification with the explicit chain: |L ∪ Q₃| = |L| + |Q₃| (D-DP(a) disjointness) = |L| + |R| (D-BJ bijectivity) = N − |X| (trichotomy partition |V_1(d)| = |L| + |X| + |R| = N) = N − c (|X| = c from D-SEP(b)'s explicit form X = {[1, k] : p₂ ≤ k < p₂ + c}).

## OUT_OF_SCOPE

### Topic 1: Contraction at ordinal depth > 1 (V-position depth > 2)
**Why out of scope**: The "Necessity from TA4" subsection establishes that S8a's componentwise positivity collides with TA4's zero-prefix precondition at depth > 2. A direct TumblerSub computation produces the same obstruction. This is acknowledged in the open questions; the generalization requires a different round-trip technique or a relaxation of S8a, both substantive new analysis.

### Topic 2: DELETE at non-text subspaces (link tombstoning)
**Why out of scope**: The subspace scoping axiom S = 1 reflects the foundation's text-only D-CTG/D-MIN/D-SEQ; link-subspace deletion uses tombstoning rather than shift-to-close-gap and is the subject of a separate future ASN. The ASN explicitly defers this.

### Topic 3: Full INSERT operation (content placement composed with the shift sub-operation)
**Why out of scope**: I3 is intentionally scoped to the shift sub-operation. The composing INSERT (with dom(C) extension for the n new I-addresses, gap-fill in M(d), and re-derivation of D-CTG/D-MIN/D-SEQ) is the natural subject of a downstream INSERT ASN.

### Topic 4: Cross-document V-position reference tracking
**Why out of scope**: Acknowledged in the open questions; concerns external state and is not a property of the V-arrangement transformation itself.

VERDICT: REVISE
