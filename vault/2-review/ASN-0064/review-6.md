# Review of ASN-0064

## REVISE

### Issue 1: F1 proof — incorrect claim about element-level members of I-span denotation

**ASN-0064, F1 proof**: "the span denotation ⟦(aⱼ + c, δ(w, d_I))⟧ is a superset of the run (it includes extension tumblers of greater depth), but the element-level members are exactly the run's I-addresses"

**Problem**: The claim that element-level members are exactly the run's I-addresses is false. Extension tumblers of depth greater than d_I can still be element-level (zeros = 3). For example, if aⱼ + c = 1.0.1.0.1.0.1.5 (depth 8, zeros at positions 2,4,6), then 1.0.1.0.1.0.1.5.x (depth 9, x > 0) has zeros at positions 2,4,6 — still three zeros, still element-level by T4. These tumblers fall within the span denotation (by T1(ii), 1.0.1.0.1.0.1.5 < 1.0.1.0.1.0.1.5.x < 1.0.1.0.1.0.1.6) but are not in the run {aⱼ + c, ..., aⱼ + c + w − 1}.

The main claim of F1 (the m-run bound) is unaffected — the overlap test uses `coverage(e) ∩ Q` where Q contains only addresses from dom(C) at the arrangement's I-address depth, so the extra element-level tumblers never appear in Q. But the factual statement about span denotation is wrong.

**Required**: Either remove the parenthetical claim, or qualify it: "the element-level members *at depth d_I* are exactly the run's I-addresses; the span denotation also includes element-level tumblers at greater depths."

### Issue 2: F4 labeled INV — should be LEMMA

**ASN-0064, F4**: "F4 — Completeness (INV). [...] Both follow directly from the definition of findlinks(Q) = {a ∈ dom(Σ.L) : satisfies(a, Q)}."

**Problem**: F4 is a definitional consequence, not a state invariant. INV in the foundation ASNs means a predicate that must be preserved across state transitions (e.g., S3 requires each new K.μ⁺ to maintain referential integrity). F4 cannot be violated by any state transition because findlinks is a pure set comprehension (F11) that is correct by construction. Labeling it INV signals to future ASN authors that new operations must prove F4 preservation — a wild goose chase, since the property is tautological. The correct label is LEMMA (trivially derived from the definition).

**Required**: Relabel F4 as LEMMA in both the section header and the properties table.

## OUT_OF_SCOPE

### Topic 1: Link creation transition and LinkEntityCoherence
**Why out of scope**: The ASN correctly identifies this as an assumption pending a link-creation ASN. The analog of K.α for the link store would establish `origin(a) ∈ E_doc` as a postcondition. This is new machinery, not an error in ASN-0064.

### Topic 2: Integration of Σ.L into the system state
**Why out of scope**: The ASN acknowledges that "the link store Σ.L, defined in ASN-0043, is not yet integrated into the formal system state Σ = (C, E, M, R) of ASN-0047." This integration — adding L to the state tuple, defining link-subspace elementary transitions, proving reachable-state invariants for L — is a future ASN's responsibility.

### Topic 3: Access control formalization
**Why out of scope**: The predicates `published(d)` and `authorized(u, d)` are left undefined. Formalizing these requires an ownership and permission model that the foundations do not yet provide.

VERDICT: REVISE
