# ASN Status Register

*Last updated: 2026-03-14*

## Phase 3.2 (active) — Constrained, dependent

| ASN | Title | Status | Notes |
|-----|-------|--------|-------|
| ASN-0034 | Tumbler Algebra | **Foundation** | Converged. 124 Dafny verified, proofs promoted to vault/proofs/TumblerAlgebra/. Foundation root. |
| ASN-0035 | Node Ontology | **Inquiry** | Regeneration of ASN-0033 with tighter out_of_scope. Foundation: ASN-0034. |
| ASN-0036 | Two Space | **Inquiry** | Regeneration of ASN-0026 with tighter out_of_scope. Foundation: ASN-0034. |

## Phase 3.1 (abandoned) — Controlled, dependent

First attempt at dependent ASNs with foundation lists and promotion gates, but without `out_of_scope` constraints. This phase discovered where the boundaries needed to be — the scope audit of ASN-0001 revealed that properties it had claimed (T11 Dual-Space Separation, TA7b Subspace Frame, TA8 Orthogonal Dimensions) belonged in downstream layers, while T8 bundled allocation permanence with content immutability. Without negative constraints telling the agents what to exclude, scope bleed from the foundation root propagated upward through the chain. Phase 3.1 identified the need for `out_of_scope` as a first-class pipeline feature, leading to the foundation regeneration as ASN-0034 in Phase 3.2.

| ASN | Title | Notes |
|-----|-------|-------|
| ASN-0026 | I-Space and V-Space | Supersedes ASN-0003. Converged review 4. Dafny proofs were promoted to `vault/proofs/TwoSpace/`. |
| ASN-0027 | Address Permanence | Drafted without ASN-0029 in foundation — silently assumes D2 (DocumentPermanence) without citing it. Dafny 35/35 still valid. |
| ASN-0028 | Document Lifecycle | Contaminated — drafted with ASN-0027 in foundations, creating circular dependency. Superseded by ASN-0029. |
| ASN-0029 | Document Ontology | Supersedes ASN-0011 scope. 18 properties (D0-D17). Provides D2 (DocumentPermanence). Converged. |
| ASN-0030 | Address Permanence | References endsets, resolvability, ghost links without link datatype defined. Alloy 22/22 valid. |
| ASN-0031 | Account Creation | Fills D0 precondition gap from ASN-0029. AC0-AC3. |
| ASN-0032 | Link Ontology | 19 properties (L0-L19). Depends on ASN-0001, ASN-0026, ASN-0029. |
| ASN-0033 | Node Ontology | Foundation gap: ASN-0031 assumes nodes exist. Layer 2 in foundation stack. |

## Phase 2 (completed, now deprecated)

Phase 2 established controlled, independent inquiries — each ASN prompted independently with no foundation injection and no dependency chain. The isolation revealed which constructions kept appearing independently across ASNs, discovering the foundation DAG. Phase 2 is complete — its purpose was served. All ASNs are now deprecated as they will be regenerated under Phase 3.2 with proper `out_of_scope` constraints and foundation dependencies.

| ASN | Title | Notes |
|-----|-------|-------|
| ASN-0001 | Tumbler Algebra | Replaced by ASN-0034. Dafny proofs were promoted to `vault/proofs/TumblerAlgebra/` and `AddressAllocation/`. |
| ASN-0002 | Address Permanence | Superseded by ASN-0025. |
| ASN-0003 | I-Space and V-Space | Superseded by ASN-0026. Mixes foundation with operations. |
| ASN-0004 | Content Insertion | Has proof index + formal statements (old types). |
| ASN-0005 | Content Deletion | |
| ASN-0006 | Transclusion (COPY) | |
| ASN-0007 | Links and Endsets | Link datatype, endsets, spanindex, discovery, resolution. |
| ASN-0008 | Link Discovery | May fold into ASN-0007. |
| ASN-0009 | Version Semantics | |
| ASN-0010 | Content Retrieval | |
| ASN-0011 | Document Lifecycle | Superseded by ASN-0029. Scope absorbed into ASN-0029. |
| ASN-0012 | Enfilade Properties | |
| ASN-0013 | Concurrency and Global Indexes | |
| ASN-0014 | Distributed Replication Consistency | |
| ASN-0015 | Permanence and Economic Obligations | |
| ASN-0016 | Content Provenance | |
| ASN-0017 | Rearrange Operation | |
| ASN-0018 | Concurrent Operation Ordering | |
| ASN-0019 | Operation Journaling | |
| ASN-0020 | Allocation Order Invariants | |
| ASN-0021 | Frame Condition Completeness | |
| ASN-0022 | Ghost Link Discoverability | |
| ASN-0023 | Deletion Economics | |
| ASN-0024 | Operational Fragmentation Bounds | |
| ASN-0025 | Address Permanence | Superseded by ASN-0027. Dafny modeling-1 orphaned. |
