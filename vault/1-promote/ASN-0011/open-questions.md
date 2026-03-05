# Promotion: Open Questions

**Source:** ASN-0011

## Promoted

- **What must the system guarantee about documents whose storage rental has lapsed — does DL0 (identity permanence) hold unconditionally, or is it conditioned on economic obligations being met?**
  Rationale: Opens genuinely new territory about whether the system's foundational permanence invariants are unconditional structural guarantees or economically conditioned — no existing inquiry covers the economics area, and the answer determines whether the entire formal framework's axioms require qualification.
  - Title: Permanence and Economic Obligations
  - Question: What must the system guarantee about its permanence invariants when economic obligations are not met — are address permanence, content immutability, and publication irrevocability unconditional or conditioned on continued payment?
  - Area: economics
  - Nelson: 10
  - Gregory: 0

## Declined

- **Must the system guarantee that a document's arrangement is recoverable after a crash that interrupts CREATENEWDOCUMENT between address allocation and POOM initialisation?**
  Rationale: A narrow operation-atomicity question that can be resolved by specifying CREATENEWDOCUMENT as atomic within the current ASN's revision scope.

- **What invariant must the allocation counter satisfy when multiple accounts reside on the same node — must per-account counters be independent, or may a global counter serve?**
  Rationale: Sub-case of Inquiry 1 (Tumbler Algebra) which covers algebraic and structural properties of the addressing system, and the question leans toward implementation mechanism choice.

- **Must the session layer guarantee that a document owner can always obtain write access to their own document, even when other readers hold it open?**
  Rationale: Falls within the scope of Inquiry 13 (Concurrency) which explicitly asks how single-writer ownership interacts with shared-read global state.

- **Must the publication transition be atomic — can a document be observed in a partially-published state by concurrent readers?**
  Rationale: Sub-case of Inquiry 13 (Concurrency) which covers consistency guarantees under concurrent operations.

- **What consistency must the system maintain between a document's session state and its arrangement if a connection terminates abnormally without executing CLOSE?**
  Rationale: A narrow session-layer failure-mode detail that is best addressed as a protocol specification concern, not an independent architectural inquiry.

- **When a user versions a document they do not own, must the system record the derivation relationship, or is the relationship visible only through shared I-space addresses?**
  Rationale: Directly covered by Inquiry 9 (Version Semantics) which asks how versions relate to each other and to shared content.

- **Must the system prevent a document from being opened for write by two connections belonging to the same owner account, or does DL19 quantify over connections regardless of the account behind them?**
  Rationale: A clarification of DL19's quantification scope that can be resolved by revising the current ASN rather than opening a new investigation.
