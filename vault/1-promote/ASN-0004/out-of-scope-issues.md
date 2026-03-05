# Promotion: Out-of-Scope Issues

**Source:** ASN-0004

## Promoted

- **Concurrency semantics for INSERT / Concurrent insertion semantics**
  Source: ASN-0004 review 1, ASN-0004 review 2 (same topic deferred independently in both reviews)
  Rationale: Asks what the system must guarantee about concurrent mutation outcomes — distinct from Inquiry 13, which focuses on cross-document global index coordination rather than operation-level merge ordering
  - Title: Concurrent Operation Ordering
  - Question: What must the system guarantee about the result when multiple operations modify the same or overlapping content simultaneously? What determines the final state and what invariants must the resolution satisfy?
  - Area: concurrency
  - Nelson: 10
  - Gregory: 10

- **Journal/replay semantics**
  Source: ASN-0004 review 1
  Rationale: Asks what the system must guarantee about operation recording and reconstruction — distinct from Inquiry 9 (version graph structure) and Inquiry 16 (content lineage)
  - Title: Operation Journaling
  - Question: What must the system guarantee about recording and replaying the history of operations performed on content? What properties must an operation log satisfy for faithful state reconstruction?
  - Area: versioning
  - Nelson: 10
  - Gregory: 5

- **Allocation ordering and V-stream correspondence**
  Source: ASN-0004 review 2
  Rationale: Asks what the system must guarantee about the relationship between allocation order and document order — distinct from Inquiry 1 (general tumbler algebra) and Inquiry 3 (general I/V-space relationship)
  - Title: Allocation Order Invariants
  - Question: What must the system guarantee about the relationship between the temporal order in which content is allocated and its spatial position in V-space? Must allocation order correspond to document order?
  - Area: addressing
  - Nelson: 10
  - Gregory: 10

- **Owner preservation as frame condition**
  Source: ASN-0004 review 2
  Rationale: Identifies a systematic gap in the formal specification — no operation explicitly states frame conditions on ownership, which is a real specification deficiency, not editorial
  - Title: Frame Condition Completeness
  - Question: What must each operation explicitly guarantee about state it does not intend to modify? What frame conditions must hold across all operations to ensure unaffected properties — ownership, links, addresses — are preserved?
  - Area: operations
  - Nelson: 10
  - Gregory: 10

## Declined

- **Tiling invariant preservation under INSERT**
  Source: ASN-0004 review 1
  Rationale: Inconsequential — the tiling proof already exists in ASN-0013, which has accepted responsibility for this work; no new inquiry is needed

- **Atomicity enforcement mechanism**
  Source: ASN-0004 review 2
  Rationale: Implementation mechanism — the defer explicitly asks how to enforce atomicity (WAL, undo log, etc.), matching the rejection criterion
