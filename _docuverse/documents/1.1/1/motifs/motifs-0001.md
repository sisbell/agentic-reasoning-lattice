motifs:
  - id: 1
    name: "Monotonic non-removal of the allocated set"
    cited_claims:
      ASN-0034: [T8]
      ASN-0036: [S0, S1, S9]
      ASN-0040: [B0, "B0★", B_fin]
    rationale: |
      Each note independently establishes that the set of addresses-in-use
      grows monotonically across every state transition and that no
      operation removes an element. Each gives its own per-transition
      preservation argument (T8 from the absence of removal operations in
      ASN-0034; S0 by direct quantification across Σ→Σ' in ASN-0036; B0/B0★
      via B0a's partition of Op in ASN-0040) rather than citing a common
      source.
  - id: 2
    name: "Prefix-restricted sets form contiguous intervals under T1"
    cited_claims:
      ASN-0034: [T5]
      ASN-0036: [D-CTG, D-CTG-depth, D-SEQ, S8]
      ASN-0040: [B1, B2]
    rationale: |
      Each note proves, in its own framing, that addresses sharing a
      common prefix (subtree in ASN-0034, V-positions in a subspace in
      ASN-0036, baptismal children in a namespace in ASN-0040) occupy a
      gap-free contiguous interval under the lexicographic order, and
      each uses this to reduce a multi-element invariant to a single
      scalar (interval endpoints, ordinal range 1..n, high water mark).
  - id: 3
    name: "Distinct allocation events ⟹ distinct addresses (global uniqueness)"
    cited_claims:
      ASN-0034: [T10, GlobalUniqueness, PartitionMonotonicity]
      ASN-0036: [S4, S7, S7a, S7d]
      ASN-0040: [B7, B8]
    rationale: |
      Each note proves that two allocation/baptism events in non-nesting
      prefix domains, or in the same domain at distinct steps, yield
      distinct addresses. The arguments factor identically: cross-domain
      uniqueness from prefix divergence (T10 / S7d-via-GlobalUniqueness /
      B7), same-domain uniqueness from per-stream strict monotonicity
      (T9 / S8's correspondence-run injection / B8 Case 1).
  - id: 4
    name: "T4-validity (field structure) preserved by increment and shift"
    cited_claims:
      ASN-0034: [T10a.4, TA5a]
      ASN-0036: [S7b, S7c, ShiftPreservation]
      ASN-0040: [B5, B5a, B6, B10]
    rationale: |
      Each note carries a structural invariant — zero count, no adjacent
      zeros, positive endpoint components — through its own arithmetic
      operation and proves preservation case-by-case on the increment
      depth. ShiftPreservation's four conclusions in ASN-0036, TA5a's
      d-case analysis in ASN-0034, and B6/B10's joint argument in
      ASN-0040 reach the same conclusion through three distinct proof
      structures.
  - id: 5
    name: "Prefix rule: components strictly before the action point are copied unchanged"
    cited_claims:
      ASN-0034: [TumblerAdd, "TA5(b)", "TA5(c)"]
      ASN-0036: [ShiftPreservation, OrdAddHom, OrdShiftHom]
      ASN-0040: [S1, S(p_d), B5a]
    rationale: |
      The constructive identity that addition/shift acts only at and
      beyond the action point appears in each note as the central
      mechanism by which higher-level structure (subspace identifier,
      document prefix, parent prefix) is left invariant under
      modification of a deeper component. Each note re-derives the
      consequence in its own vocabulary (length preservation, subspace
      preservation, prefix extension of stream elements).
  - id: 6
    name: "State decomposition with a frame-preserving partition of operations"
    cited_claims:
      ASN-0034: [T8, T10a]
      ASN-0036: [S0, S2, S9]
      ASN-0040: [B0a, B4]
    rationale: |
      Each note models the system state as a tuple and proves that the
      operation vocabulary partitions into operations that modify a
      specific component (allocator extensions, content/arrangement
      edits, baptisms) and operations that leave that component exactly
      frame-equal. This partition is the load-bearing structure for the
      monotonicity and uniqueness invariants in each note and is stated
      explicitly rather than imported.
  - id: 7
    name: "Iterated successor generates a strictly increasing parametrized family"
    cited_claims:
      ASN-0034: [T9, T10a, TS1, TS3, TS4, TS5]
      ASN-0036: [S8, OrdShiftHom, ShiftPreservation]
      ASN-0040: [S(p_d), S0, B2, B9]
    rationale: |
      Each note constructs a parametrized family of addresses by iterated
      application of a single-component successor (inc(·, 0) in
      ASN-0034/ASN-0040; shift(·, k) built from δ(k, m) in ASN-0036) and
      proves the family is strictly increasing, length-preserving, and
      unbounded in its parameter. The shift composition and stream
      ordering arguments are structurally the same induction on the
      parameter.
