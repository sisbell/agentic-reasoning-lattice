# Review of ASN-0035

## REVISE

### Issue 1: Weakest precondition analysis absent for BAPTIZE

**ASN-0035, Baptism**: BAPTIZE is defined with precondition `p ∈ Σ.nodes` and five postconditions. The freshness derivation establishes *sufficiency* via a clean two-step structural argument — step (a) rules out sibling collision, step (b) rules out cross-parent collision. No weakest precondition analysis establishes *necessity*.

**Problem**: The forward proof shows `p ∈ Σ.nodes ⟹ postconditions hold`. The reverse question — "what is the weakest condition under which all postconditions and invariant-preservation obligations are met?" — is not addressed. The precondition is the contract boundary for every future operation that triggers node creation. If it could be weakened, the ASN over-constrains callers; if it cannot, that fact should be demonstrated.

**Required**: State the WP explicitly. The critical obligation is N3(b) preservation: `parent(n) ∈ Σ.nodes`. Since `parent(n) = p` by construction, N3(b) requires `p ∈ Σ.nodes` — this is necessary, not merely sufficient. Combined with the sufficiency already shown by the freshness derivation, the stated precondition is exact. A short paragraph framing the freshness derivation as WP analysis and noting necessity via N3(b) closes this.

## OUT_OF_SCOPE

### Topic 1: Authorization model for BAPTIZE
**Why out of scope**: The ASN explicitly defers "Who is authorized to invoke BAPTIZE for a given parent node?" to Account Ontology. Nelson's ownership principle ("the owner of a given item controls the allocation of the numbers under it") requires an actor and delegation model not yet formalized. The structural properties here are independent of who calls BAPTIZE.

### Topic 2: Genesis semantics for the root
**Why out of scope**: Whether `r = [1]` is axiomatic or produced by an explicit genesis operation is listed in the ASN's own Open Questions. The current treatment — `Σ.nodes = {r}` as initial condition — is sufficient for every derivation in this ASN. Genesis semantics would introduce questions about pre-docuverse state that belong in a dedicated foundation.

VERDICT: REVISE
