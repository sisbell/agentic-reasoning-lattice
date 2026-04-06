## Format Review: ASN-0034

### 1. Table Structure

(none)

### 2. Status Vocabulary

(none)

### 3. Header Format

All 29 findings are names with spaces where PascalCase is required.

| # | Actual header | Required name |
|---|---------------|---------------|
| 1 | `**T0(a) (Unbounded component values).**` | `UnboundedComponentValues` |
| 2 | `**T0(b) (Unbounded length).**` | `UnboundedLength` |
| 3 | `**T1 (Lexicographic order).**` | `LexicographicOrder` |
| 4 | `**T2 (Intrinsic comparison).**` | `IntrinsicComparison` |
| 5 | `**T3 (Canonical representation).**` | `CanonicalRepresentation` |
| 6 | `**T4 (Hierarchical parsing).**` | `HierarchicalParsing` |
| 7 | `**T5 (Contiguous subtrees).**` | `ContiguousSubtrees` |
| 8 | `**T6 (Decidable containment).**` | `DecidableContainment` |
| 9 | `**T7 (Subspace disjointness).**` | `SubspaceDisjointness` |
| 10 | `**T8 (Allocation permanence).**` | `AllocationPermanence` |
| 11 | `**T9 (Forward allocation).**` | `ForwardAllocation` |
| 12 | `**T10 (Partition independence).**` | `PartitionIndependence` |
| 13 | `**T10a (Allocator discipline).**` | `AllocatorDiscipline` |
| 14 | `**PrefixOrderingExtension (Prefix ordering extension).**` | `PrefixOrderingExtension` |
| 15 | `**PartitionMonotonicity (Partition monotonicity).**` | `PartitionMonotonicity` |
| 16 | `**GlobalUniqueness (Global uniqueness).**` | `GlobalUniqueness` |
| 17 | `**TA0 (Well-defined addition).**` | `WellDefinedAddition` |
| 18 | `**TA1 (Order preservation under addition).**` | `OrderPreservationUnderAddition` |
| 19 | `**TA1-strict (Strict order preservation).**` | `StrictOrderPreservation` |
| 20 | `**TA-strict (Strict increase).**` | `StrictIncrease` |
| 21 | `**TA2 (Well-defined subtraction).**` | `WellDefinedSubtraction` |
| 22 | `**TA3 (Order preservation under subtraction, weak).**` | `OrderPreservationUnderSubtractionWeak` |
| 23 | `**TA3-strict (Order preservation under subtraction, strict).**` | `OrderPreservationUnderSubtractionStrict` |
| 24 | `**TA4 (Partial inverse).**` | `PartialInverse` |
| 25 | `**ReverseInverse (Reverse inverse).**` | `ReverseInverse` |
| 26 | `**TA5 (Hierarchical increment).**` | `HierarchicalIncrement` |
| 27 | `**TA6 (Zero tumblers).**` | `ZeroTumblers` |
| 28 | `**TA7a (Subspace closure).**` | `SubspaceClosure` |
| 29 | `**T12 (Span well-definedness).**` | `SpanWellDefinedness` |

### 4. Missing Table Entries

(none)

### 5. Missing Prose Sections

(none)

### 6. Duplicate Labels

(none)

---

`RESULT: 29 FINDINGS`