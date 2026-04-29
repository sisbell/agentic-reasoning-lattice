# Review of ASN-0063

## REVISE

No issues found.

## OUT_OF_SCOPE

### Topic 1: FINDLINKSFROMTOTHREE operation semantics
**Why out of scope**: The discovery function `disc` is defined as a derived function on system state, but the full three-way link search operation (given content, find links filtered by from/to/type simultaneously) is new territory requiring its own operation definition with preconditions, postconditions, and efficiency guarantees.

### Topic 2: Link withdrawal mechanism
**Why out of scope**: The ASN identifies the tension between suffix-only contraction (from D-CTG) and Nelson's "inactive link" design (LM 4/9) but correctly defers the precise withdrawal invariants. This requires new state machinery (active/inactive status) or relaxation of D-CTG for the link subspace — neither belongs in the CREATELINK ASN.

### Topic 3: Link inheritance under forking
**Why out of scope**: The ASN correctly notes that J4 (Fork) with the K.μ⁺ content-subspace amendment does not copy link-subspace mappings, and that a mechanism for link inheritance would require K.μ⁺_L steps in the fork composite. This is a separate design decision with its own invariant implications.

### Topic 4: Type namespace conventions
**Why out of scope**: Whether type endsets must reference addresses in a designated type namespace or may reference arbitrary I-addresses is a policy question above the structural level. L9 (TypeGhostPermission) already permits type endsets to reference addresses outside dom(C) ∪ dom(L); constraining this further is new territory.

### Topic 5: Resolution atomicity under concurrent arrangement changes
**Why out of scope**: The open question about what happens when the arrangement changes between user selection and resolution execution involves concurrency semantics not yet formalized in the transition framework.

VERDICT: CONVERGED
