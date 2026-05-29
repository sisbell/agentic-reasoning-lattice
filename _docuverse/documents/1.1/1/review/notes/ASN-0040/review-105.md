# Review of ASN-0040

## REVISE

### Issue 1: B8 hedges its claim for a model this ASN does not admit

**ASN-0040, B8 (Co-reachable Uniqueness)**: "Distinct *co-reachable* baptismal acts produce distinct addresses, where two acts are co-reachable iff both lie on a single transition path s_init →* s... Under a single linear history — the only reachability this model admits... co-reachability holds of every pair of baptismal acts, so B8 coincides here with the foundation's unconditional GlobalUniqueness (ASN-0034). The restriction to co-reachable acts becomes substantive only once histories may diverge across replicas; that branching case is deferred to the cross-replica open question below."

**Problem**: This is reviser drift. The ASN states up front that the model admits only linear history, so the "co-reachable" qualifier is vacuous on every pair — the claim's own carrier excludes the case the qualifier exists to handle. The qualifier, the GlobalUniqueness coincidence remark (not used anywhere in the proof), and the deferral to the cross-replica open question are all anticipatory machinery for replication, which is explicitly OUT OF SCOPE for this ASN. A precise reader must work through a vacuous distinction and a forward pointer to reach the actual content: distinct baptismal acts produce distinct addresses.

**Required**: State B8 unconditionally for this model — "distinct baptismal acts produce distinct addresses" — and drop the co-reachability framing, the GlobalUniqueness coincidence sentence, and the cross-replica deferral. The branching/replication treatment belongs to the future ASN that introduces divergent histories, not as a hedge here.

### Issue 2: B0a gloss explains the axiom's utility rather than its content

**ASN-0040, B0a (Baptismal Closure)**: "This partition fixes the shape of every inductive step over reachable states. We call it the *s.B-frame dispatch*."

**Problem**: B0a is a design requirement (axiom-like). The naming sentence is fine — the name is used downstream — but "This partition fixes the shape of every inductive step over reachable states" is use-site rationale (why the partition is convenient for later proofs), not a statement of what B0a says. This matches the anti-bloat pattern of prose around an axiom explaining why it is needed rather than what it asserts.

**Required**: Keep the naming clause ("We call it the s.B-frame dispatch") and delete the utility sentence. The downstream proofs already cite "the s.B-frame dispatch (§B0a)"; the reader does not need to be told in advance that it shapes inductive steps.

## OUT_OF_SCOPE

None. The open-questions list correctly defers parent-prerequisite chains, the `allocated(s) ⊆ s.B` activation discipline, valid seed-set characterization, and cross-replica ordering to future work.

VERDICT: REVISE

The proofs themselves are sound — S(p,d) canonical form, B5/B5a zero counts, B6 sufficiency/necessity, B7's exhaustive length cases (including the nesting-parent witness), B1 contiguity, B2, and B9 all check out, and the trace concretely exercises d=1, d=2, and the B7 length-split. The remaining defects are residual accretion, not correctness gaps.
