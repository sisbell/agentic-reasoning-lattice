# Review of ASN-0082

## REVISE

### Issue 1: VD classification conflict
**ASN-0082, Local Axioms**: "VD is therefore a consequence of T10a.1 together with the structural fact that no further child-spawning occurs after the initial bootstrap."
**Problem**: VD is labeled `AXIOM, local` in the statement registry but the body calls it "a consequence." An axiom is taken without derivation; a consequence is derived. The text claims both. If VD is derived, T10a.1 must appear in the statement registry as a cited dependency, and the bootstrap-discipline constraint ("no further child-spawning after initial setup") should be the explicit local axiom. If VD is an axiom, the "consequence" language is misleading and should be removed. The distinction matters: downstream ASNs that cite VD inherit different proof obligations depending on whether it is axiomatic or derived.
**Required**: Either (a) relabel VD as a lemma, state the bootstrap-discipline constraint as the local axiom, and add T10a.1 to the registry as a cited dependency; or (b) keep VD as an axiom and replace "VD is therefore a consequence of T10a.1" with motivational language (e.g., "VD is motivated by T10a.1 and the design constraint that...").

## OUT_OF_SCOPE

### Topic 1: Straddling spans
I3-S requires `s ≥ p` — the entire span lies within the shifted region. A span straddling the insertion point (`start < p < reach`) would need splitting at `p` via S4 (ASN-0053), shifting the right part by I3-S, and verifying the composite. This is a natural composition of established results but is new territory.
**Why out of scope**: I3-S establishes the within-region base case; straddling is a composition that builds on it plus S4, belonging in a future ASN about insertion's interaction with arbitrary span sets.

### Topic 2: Closed-world frame for dom(M'(d))
The five clauses specify which positions are in dom(M'(d)) (I3, I3-L, I3-X) and which are not (I3-V), but do not explicitly state that no other positions enter dom(M'(d)). Positions in subspace S that were unmapped before the shift and are not shift images are left unaddressed. The content-placement postcondition for gap positions is correctly deferred.
**Why out of scope**: The specification is intentionally partial — the full closed-world frame depends on the INSERT ASN's content-placement postcondition, which this ASN properly defers.

VERDICT: REVISE
