# Review of ASN-0079

## REVISE

No issues found.

## OUT_OF_SCOPE

### Topic 1: Span-based search constraints for type hierarchy queries
The SearchConstraint requires a finite set P, but L10 (TypeHierarchyByContainment, ASN-0043) models type hierarchies via prefix spans over a potentially unbounded type-address space. A richer constraint language — allowing spans or prefix patterns as first-class constraint terms — would let a caller express "all links of type X or any subtype" without enumerating allocated subtypes.
**Why out of scope**: The ASN defines the core finite-set intersection mechanism. Extending the constraint language to span-based or prefix-based patterns is new specification territory, not an error in the existing definitions.

### Topic 2: Index structure specification
F19 requires sublinear overhead from non-matching links but does not specify which index structures achieve this guarantee. The choice of indexing strategy (enfilade-based, hash-based, tree-based) and the invariants such an index must maintain are implementation-level concerns.
**Why out of scope**: F19 correctly captures the design constraint at the abstract level. The index specification belongs in an implementation or architecture ASN.

### Topic 3: Concurrency and isolation semantics
The open questions correctly identify that concurrent link creation and search raise isolation questions (cursor stability, snapshot consistency). These are transactional concerns beyond the single-state semantics this ASN establishes.
**Why out of scope**: The ASN's definitions are evaluated at a fixed state Σ. Concurrent-access semantics require a separate treatment of transaction isolation.

VERDICT: CONVERGED
