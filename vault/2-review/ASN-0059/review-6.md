# Review of ASN-0059

## REVISE

*No issues identified.*

## OUT_OF_SCOPE

### Topic 1: Link discoverability after V-position shift
The ASN correctly notes that links reference I-addresses (content identity), so they survive INSERT unchanged at the I-level. But a system that indexes links by V-position would need to update its index after the shift. How the link enfilade (or any position-based index) responds to V-position displacement is a question for the link ontology ASN, not this one.
**Why out of scope**: INSERT's contract is fully specified at the arrangement level; link indexing is a separate mechanism.

### Topic 2: Allocator existence guarantee
I0 asserts "there exist a₁, ..., aₙ" satisfying freshness and contiguity. The derivation from T9/T10a establishes that *if* the allocator produces addresses, they are contiguous — but the *existence* of n fresh addresses is assumed from the unboundedness axioms (T0(a), T0(b)) and the allocator's ability to always apply inc. A future ASN on allocation mechanics could make this explicit.
**Why out of scope**: The system's ability to allocate is a foundational assumption, not an INSERT-specific concern.

### Topic 3: VContiguity as system invariant vs caller precondition
The ASN correctly identifies this as an open design decision. The postcondition (I1–I5) is well-defined regardless; I9 is conditional on the caller providing p in range. Whether the system enforces the range constraint or merely preserves contiguity when the caller cooperates is a policy question for the operations layer.
**Why out of scope**: This is a system-level design decision that affects all mutating operations, not just INSERT.

VERDICT: CONVERGED
