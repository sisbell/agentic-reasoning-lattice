---
name: Distinct allocation events ⟹ distinct addresses (global uniqueness)
cited_claims:
  ASN-0034:
  - T10
  - GlobalUniqueness
  - PartitionMonotonicity
  ASN-0036:
  - S4
  - S7
  - S7a
  - S7d
  ASN-0040:
  - B7
  - B8
---

# Motif — Distinct allocation events ⟹ distinct addresses (global uniqueness)

Each note proves that two allocation/baptism events in non-nesting
prefix domains, or in the same domain at distinct steps, yield
distinct addresses. The arguments factor identically: cross-domain
uniqueness from prefix divergence (T10 / S7d-via-GlobalUniqueness /
B7), same-domain uniqueness from per-stream strict monotonicity
(T9 / S8's correspondence-run injection / B8 Case 1).
