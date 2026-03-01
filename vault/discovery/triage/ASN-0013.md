# Triage: ASN-0013

## Promoted

- **If the system is extended to support multiple servers with BEBE replication, what convergence guarantee must the global indexes satisfy — eventual consistency, bounded staleness, or causal consistency?** → Inquiry: Distributed Replication Consistency
  Distributed consistency across network partitions is qualitatively different from single-server concurrency and introduces CAP-theorem concerns not addressed by any existing inquiry.

## Declined

- **Must the content-location index (CΣ4) eventually converge to equality with the authoritative state, or is permanent over-approximation (stale entries from deleted arrangements) acceptable?**
  Sub-case of inquiry 13, which already asks what consistency the global indexes require; the ASN itself partially answers this with CON3a and CON9's deliberate ⊇.

- **What consistency must CREATENEWVERSION guarantee when the source version is being concurrently modified by its owner — must the new version snapshot a consistent pre- or post-operation state of the source arrangement?**
  Sub-case of inquiries 9 (version semantics) and 13 (concurrency); CON5's before-or-after atomicity already applies to CREATENEWVERSION as a FEBE operation.

- **What must the system guarantee about the ordering of link-index updates relative to the mutations that produce them — must CREATELINK's index entries be visible before the operation's acknowledgment reaches the client?**
  Sub-case of inquiry 13; CON8 already establishes that each operation's effects become visible atomically, and visibility ordering relative to acknowledgment is a refinement detail within that scope.

- **Under what conditions, if any, may orphaned I-space entries from crash-interrupted operations be reclaimed without violating CΣ1's permanence guarantee?**
  Sub-case of inquiry 2 (address permanence), which asks what operations may and may not affect address assignments; orphan reclamation is a specific instance of that question.

- **Must CON5 (before-or-after atomicity) hold across multi-operation sequences — for instance, must a session that performs INSERT followed by CREATELINK present both effects atomically to other sessions, or may the INSERT be visible before the CREATELINK?**
  Sub-case of inquiry 13; the ASN already establishes CON8's per-operation atomicity as the transaction boundary, and the remaining question is a refinement within that framework.

- **What classification of operations — single-document vs cross-document — does the concurrency model require, and what additional properties must cross-document operations (COPY, RETRIEVECONTENTS) satisfy beyond CON5's snapshot guarantee?**
  Sub-case of inquiry 13; the ASN already classifies operations and identifies CON5 as the cross-document guarantee, leaving only refinement details.
