# Proof Modules — Changelog

## 2026-03-12: DocumentOntology extraction + ASN-0029 deduplication

**Problem:** ASN-0029 Dafny review (review-13) flagged pervasive duplication across 26 property files. `PubStatus` defined identically in 9 files. `FirstZeroFrom`, `HasAccountLevel`, `AccountPrefix` duplicated 4–6x each. `DocState` in 4 files with 3 shapes. `ValidDocAddr` and `DocLevelPrefix` each in 4 files.

**Changes:**

- **New module: DocumentOntology** — shared types for ASN-0029 document properties: `PubStatus`, `DocState` (core shape: base + pub), `ValidDocAddr`, `DocLevelPrefix`. Depends on TumblerAlgebra, Foundation, HierarchicalParsing.

- **Extended: HierarchicalParsing** — added `FirstZeroFrom`, `HasAccountLevel`, `AccountPrefix`. These are address-parsing helpers that extract account-level structure from tumbler addresses. Placed here (not DocumentOntology) because they parse address hierarchy, not document concepts.

- **Deleted: AccountPrefix.dfy** — its entire content (FirstZeroFrom, HasAccountLevel, AccountPrefix) moved to HierarchicalParsing. The ASN-0029 "account" property (D3) is proven by the function's existence in HierarchicalParsing and by StructuralOwnership's verification that `Account(d)` produces a valid prefix.

- **Updated 14 property files** to import from shared modules instead of defining locally. Files with extended DocState variants (OwnershipRights, PublicationSurrender) use qualified `DocumentOntology.PubStatus` to avoid name collision with their local DocState.

**Result:** 25/25 property files verified. Net -225 lines duplicated, +93 lines shared. Proof module count: 64 verified, 0 errors.

## 2026-03-12: Module renames

- `AddressProperties` → `AddressAllocation` — all files concern the allocation discipline (ForwardAllocation, AllocatorDiscipline, GlobalUniqueness, etc.), not generic "properties."
- `IVSpaceProperties` → `TwoSpace` — the module models the two-space (I-space/V-space) structure, not generic properties.

## 2026-03-11: ASN-0029 modeling-1

Initial Dafny formalization of ASN-0029 document ontology. 26 property files covering D0–D17 plus supporting invariants (PublicationStatus, ValidAccountAddr, AccountPrefix, DocFieldWellFormed). All verified.

## 2026-03-10: AddressAllocation promotion

Promoted ASN-0001 address properties from `vault/3-modeling/dafny/ASN-0001/modeling-1/` into `vault/proofs/AddressAllocation/` as shared building blocks. Removed `include` directives (dfyconfig.toml handles resolution). Files: HierarchicalParsing, SubspaceDisjointness, ForwardAllocation, AllocatorDiscipline, PartitionIndependence, AddressPermanence, GlobalUniqueness.

## 2026-03-09: Foundation + TumblerAlgebra

Initial proof modules. TumblerAlgebra: Tumbler datatype, LessThan, Add/Subtract, IsPrefix. Foundation: State model (IAddr, VPos, State, J0–J2).
