# Review of ASN-0082

## OUT_OF_SCOPE

### Topic 1: Generalization of contraction to depth > 2
**Why out of scope**: The `#p = 2` depth scoping axiom is justified rigorously via the TA4 obstruction analysis ("Necessity from TA4"). The collision between TA4's zero-prefix requirement and S8a's componentwise positivity at depths > 2 is structural, not a proof gap. Generalization requires new arithmetic infrastructure (strengthened TA4 or alternative left-inverse derivation) — substantive future work, not a revision. The ASN's Open Questions section explicitly flags this.

### Topic 2: Full INSERT operation specification
**Why out of scope**: I3 is explicitly scoped as the "shift sub-operation" of INSERT, with content placement at the gap positions [p, shift(p, n)) deferred. I3-C (`dom(C') = dom(C)`) will weaken to S0 under composition with content allocation; D-CTG/D-MIN/D-SEQ must be re-established by the composing operation. The asymmetry with DELETE (which has no content-side counterpart per S0 immutability) is correctly explained.

### Topic 3: Link-subspace contraction with tombstoning
**Why out of scope**: Contraction is scoped to S = 1 by axiom. Link-subspace mutation uses tombstoning (foundation's D-CTG frame note exempts V_2(d) from contiguity), a different mechanism than the shift-to-close-gap semantics specified here. Belongs in a future link-operations ASN.

### Topic 4: External reference updates under shifts
**Why out of scope**: The first Open Question raises this. Cross-system reference tracking requires citation-graph machinery beyond the intra-arrangement scope of this ASN.

VERDICT: CONVERGED
