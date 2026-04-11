# Inline Lint — ASN-0036

*Last scanned: 2026-04-11 10:17*

## D-CTG

- **definition** | D-VSUB | VSubspacePositions | Notation V_S(d) for the set of V-positions in subspace S of document d
- **derived** | D-CTGD | VContiguityDepthConstraint | D-CTG + S8-fin at depth m ≥ 3 forces all positions in a subspace to share components 2 through m−1
- **commentary** | — | — | Nelson citation motivating the contiguity requirement

## D-MIN

- **commentary** | — | — | depth-2 specialization of D-MIN combined with D-CTG and S8-fin to recover Nelson's address range
- **derived** | D-UFORM | UniformPositionForm | every V-position in a fixed subspace has the form [S, 1, …, 1, k] for varying k

## S7

- **definition** | D-ORIGIN | OriginFunction | The origin function mapping an element-level I-address to its document-level prefix tumbler N.0.U.0.D
- **commentary** | — | — | Two-stream separation: distinction between "where I am reading" (Vstream, document A) and "where this came from" (Istream, document B)

## S8-depth

- **derived** | S8-iaddr-uniformity | IAddressRunUniformity | all I-addresses in a correspondence run share the same tumbler depth and prefix, differing only at the element ordinal
- **commentary** | — | — | why non-trivial runs arise in practice (T10a/TA5(c) allocator discipline as motivation, not dependency)
- **definition** | OrdinalShiftExtension | OrdinalShiftExtension | extends ordinal displacement notation to k=0 for both V-positions and I-addresses
- **definition** | CorrespondenceRun | CorrespondenceRun | triple (v, a, n) such that M(d)(v+k) = a+k for all 0 ≤ k < n

## Σ.M(d)

- **definition** | Σ.C | ContentStore | Partial function from tumblers to content values representing the Istream address-to-content mapping
- **commentary** | — | — | Design rationale for the two-component state model and Nelson's motivation for separating content from arrangement


*33 files scanned. 5 with embedded results.*
