# Divergences — S7 (StructuralAttribution)

- **Line 76**: The ASN states that origin "uniquely identifies the allocating document." This provenance guarantee depends on the allocation protocol (S7a, T9/T10 from ASN-0034) — a system-level invariant that cannot be expressed as a structural precondition. The lemma captures the structural core: origin is well-defined, equals the field decomposition, and is a prefix of the address.
