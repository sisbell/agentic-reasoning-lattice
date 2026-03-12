# ASN Status Register

*Last updated: 2026-03-11*

| ASN | Title | Layer | Status | Notes |
|-----|-------|-------|--------|-------|
| ASN-0001 | Tumbler Algebra | Foundation | **Final** | Dafny proofs promoted to `vault/proofs/TumblerAlgebra/` and `AddressProperties/` |
| ASN-0002 | Address Permanence | — | **Deprecated** | Superseded by ASN-0025. |
| ASN-0003 | I-Space and V-Space | — | **Deprecated** | Superseded by ASN-0026. Mixes foundation with operations. |
| ASN-0004 | Content Insertion | Operation | **Draft** | Needs redraft. Has proof index + formal statements (old types). |
| ASN-0005 | Content Deletion | Operation | **Draft** | Needs redraft. |
| ASN-0006 | Transclusion (COPY) | Operation | **Draft** | Needs redraft. |
| ASN-0007 | Links and Endsets | Links | **Draft** | Needs redraft. Link datatype, endsets, spanindex, discovery, resolution. |
| ASN-0008 | Link Discovery | Links | **Draft** | May fold into ASN-0007. |
| ASN-0009 | Version Semantics | Version | **Draft** | |
| ASN-0010 | Content Retrieval | Operation | **Draft** | |
| ASN-0011 | Document Lifecycle | — | **Deprecated** | Superseded by ASN-0029. Scope absorbed into ASN-0029. |
| ASN-0012 | Enfilade Properties | System | **Draft** | |
| ASN-0013 | Concurrency and Global Indexes | Concurrency | **Draft** | |
| ASN-0014 | Distributed Replication Consistency | Concurrency | **Draft** | |
| ASN-0015 | Permanence and Economic Obligations | Economics | **Draft** | |
| ASN-0016 | Content Provenance | System | **Draft** | |
| ASN-0017 | Rearrange Operation | Operation | **Draft** | Needs redraft. |
| ASN-0018 | Concurrent Operation Ordering | Concurrency | **Draft** | |
| ASN-0019 | Operation Journaling | Concurrency | **Draft** | |
| ASN-0020 | Allocation Order Invariants | System | **Draft** | |
| ASN-0021 | Frame Condition Completeness | System | **Draft** | |
| ASN-0022 | Ghost Link Discoverability | Links | **Draft** | |
| ASN-0023 | Deletion Economics | Economics | **Draft** | |
| ASN-0024 | Operational Fragmentation Bounds | System | **Draft** | |
| ASN-0025 | Address Permanence | — | **Deprecated** | Superseded by ASN-0027. Dafny modeling-1 orphaned. |
| ASN-0026 | I-Space and V-Space | Foundation | **Final** | Supersedes ASN-0003. Converged review 4. Dafny proofs promoted to `vault/proofs/IVSpaceProperties/`. |
| ASN-0027 | Address Permanence | — | **Deprecated** | Drafted without ASN-0029 in foundation — silently assumes D2 (DocumentPermanence) without citing it. Dafny 35/35 still valid. Needs redraft with ASN-0029 in foundation stack. |
| ASN-0028 | Document Lifecycle | — | **Deprecated** | Contaminated — drafted with ASN-0027 in foundations, creating circular dependency. Superseded by ASN-0029. |
| ASN-0029 | Document Ontology | Foundation | **Converged** | Supersedes ASN-0011 scope. 18 properties (D0-D17). Provides D2 (DocumentPermanence) needed by ASN-0027. |
