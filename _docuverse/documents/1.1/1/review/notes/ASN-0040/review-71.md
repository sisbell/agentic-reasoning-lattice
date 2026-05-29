# Review of ASN-0040

This note carries the anti-bloat classifier, and the mathematics is sound: the stream construction, B5/B5a zero-counting, B6 sufficiency/necessity, B7 disjointness (correctly requiring B6, since S2 shows it would otherwise fail), and the B1→B2→B8/B9 chain all hold. The findings below are forward-reference accretion and defensive meta-prose that the precise reader must work around.

## REVISE

### Issue 1: Defensive "what is not needed" clause in S0
**ASN-0040, S0 proof**: "The base c₁ = inc(p, d) ∈ T (TA5(d)) and each cₙ ∈ T (TA5(c)) supply the well-formed operands these comparisons require; no T4-validity of the base is needed."
**Problem**: The trailing clause "no T4-validity of the base is needed" advances nothing about S0; it pre-empts an objection a reader did not raise. This is defensive justification of the kind that compounds across cycles.
**Required**: Delete the clause. State only that the operands lie in T.

### Issue 2: Redundant meta-prose about condition (iii) being subsumed by (i)
**ASN-0040, B6 necessity, "Condition (iii) is independently necessary at d = 2"**: "At d = 1, condition (iii) reduces to zeros(p) ≤ 3, which is already implied by condition (i) (T4-validity of p); there it adds nothing and is subsumed by (i) rather than independent."
**Problem**: The same observation — (iii) only bites at d=2 — is made in sufficiency ("the same bound that condition (iii) reduces to at d = 1"), again here, and gestured at in the table caption. Explaining the redundancy structure of the conditions is reviser drift: prose about the claim's bookkeeping rather than the claim.
**Required**: State once, at the point of definition of B6, that (iii) is binding only at d=2; remove the repeated subsumption commentary from the proof.

### Issue 3: Forward use-site pointer in B5a follow-up
**ASN-0040, after B5a**: "The B6 validity table below depends on this uniformity — all elements in a stream share the same hierarchical level."
**Problem**: This is a downstream-consumer pointer ("the … below depends on this"). The uniformity result `(A n ≥ 1 : zeros(cₙ) = zeros(p) + (d − 1))` stands on its own; naming who consumes it does not advance it.
**Required**: Keep the derived uniformity statement; drop the "the B6 table below depends on this" clause.

### Issue 4: B8 single-path scoping stated three times
**ASN-0040, B8**: the statement says "B8 establishes uniqueness only along a single transition path"; the postcondition repeats "(The claim is scoped to co-reachable acts: two baptisms on incomparable branches … may compute the same address …)"; the preconditions restate the co-reachability definition a third time.
**Problem**: Two paragraphs/slots saying the same thing in different words. The co-reachable definition is already inlined in the headline statement.
**Required**: State the scope once (in the headline statement). Remove the postcondition parenthetical and the precondition restatement.

### Issue 5: Redundant unboundedness restatement in B9 proof
**ASN-0040, B9 proof**: "This element is well-defined, and its existence is what the construction actually consumes. … Nothing in TA5(c) or in successor closure bounds the ordinal, so the construction may be iterated through every natural number, and the stream never exhausts its namespace."
**Problem**: The induction already produces c_{m+k+1} at each step and concludes hwm = M after M−m steps. The two sentences re-argue unboundedness essayistically ("is what the construction actually consumes", "never exhausts its namespace") after the work is done.
**Required**: Reduce to the single load-bearing fact: c_{m+k+1} ∈ T at every step by NAT-closure (successor) and TA5(c). Cut the rest.

### Issue 6: Defensive "what it is not" clause in B4 prose
**ASN-0040, B4**: "Atomicity is an invariant of the operation vocabulary Σ, not a caller-checked precondition."
**Problem**: This contrasts B4 against a misreading rather than stating what B4 says. The preceding sentence already establishes the read-against-precondition-state semantics.
**Required**: Delete the "not a caller-checked precondition" contrast; the structural placement on Σ already carries it.

### Issue 7: Defensive parenthetical in S2 statement
**ASN-0040, S2**: "The length bound #p ≥ 2 guarantees p′ ∈ T (T0 requires #p′ ≥ 1); it excludes only the singleton p = [0], which violates T4 in any case."
**Problem**: "which violates T4 in any case" is a defensive aside that does not bear on the stream identity. (It is also loose: #p ≥ 2 excludes every length-1 parent, not only [0]; only among trailing-zero parents is [0] the sole length-1 case.)
**Required**: Either drop the parenthetical, or tighten to "among trailing-zero parents the only length-1 case is [0]" and remove the T4 aside.

## OUT_OF_SCOPE

None to flag beyond the declared scope list. B3's ghost-element forward requirement and the activation-discipline / `allocated(s) ⊆ s.B` question are correctly parked in Open Questions rather than asserted here.

VERDICT: REVISE
