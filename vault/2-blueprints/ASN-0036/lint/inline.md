# Inline Lint — ASN-0036

*Last scanned: 2026-04-11 10:27*

## D-CTG

- **definition** | D-VSUB | VSubspacePositions | Notation V_S(d) for the set of V-positions in subspace S of document d
- **derived** | D-CTGD | VContiguityDepthConstraint | D-CTG + S8-fin at depth m ≥ 3 forces all positions in a subspace to share components 2 through m−1
- **commentary** | — | — | Nelson citation motivating the contiguity requirement
- **definition** | D-VSET | SubspacePositionSet | V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}, the set of V-positions in subspace S of document d
- **derived** | D-CTG-UNIF | SubspaceComponentUniformity | At depth m ≥ 3, D-CTG + S8-fin forces all positions in V_S(d) to share components 2 through m−1
- **definition** | D-CTG-SUB | SubspaceVPositions | V_S(d) = set of V-positions in subspace S of document d
- **derived** | D-CTG-DEPTH | DepthUniformity | D-CTG + S8-fin forces all V-positions in a subspace to share components 2 through m−1 at depth m≥3
- **definition** | DEF-SVS | SubspaceVPositionSet | notation V_S(d) for the set of V-positions belonging to a given subspace within a document
- **derived** | D-SHR | SubspaceHomogeneityRestriction | D-CTG + S8-fin forces all depth-m≥3 positions in a subspace to share components 2 through m−1
- **definition** | D-VSS | SubspaceVPositionSet | The set V_S(d) of all V-positions in subspace S of document d, used to state contiguity and uniformity conditions
- **derived** | D-CTG-U | SubspaceComponentUniformity | D-CTG and S8-fin jointly force all depth-m≥3 positions in a subspace to share components 2 through m−1
- **definition** | DEF-VSUB | VSubspacePositions | Notation V_S(d) for the set of V-positions in subspace S of document d
- **derived** | D-UPRFX | UniformSubspacePrefix | At depth m ≥ 3, D-CTG + S8-fin forces all positions in V_S(d) to share components 2 through m − 1

## D-MIN

- **commentary** | — | — | depth-2 specialization of D-MIN combined with D-CTG and S8-fin to recover Nelson's address range
- **derived** | D-UFORM | UniformPositionForm | every V-position in a fixed subspace has the form [S, 1, …, 1, k] for varying k
- **derived** | D-UNIF | UniformPositionForm | all positions in V_S(d) have form [S, 1, …, 1, k] for varying k

## OrdShiftHom

- **derived** | ShiftS8aClosure | ShiftS8aClosure | shift preserves S8a: if v satisfies S8a then shift(v, n) satisfies S8a
- **derived** | OrdShiftS8a | OrdinalShiftS8aPreservation | shift preserves S8a when v satisfies S8a, proved via OrdAddS8a vacuous condition

## S0

- **commentary** | — | — | design rationale explaining why content immutability is required via Nelson's transclusion/versioning guarantees
- **derived** | S0a | WeakestPreconditionContentImmutability | wp characterization of S0 constraining operations to fresh addresses only

## S3

- **derived** | S3-WP | AddMappingPrecondition | weakest precondition for S3 under add-mapping is a ∈ dom(Σ.C)
- **commentary** | — | — | logical vs temporal dependency: atomic ops satisfy S3 without sequential precedence
- **derived** | S3a | AddMappingPrecondition | wp(add-mapping, S3) requires target I-address already in dom(C)

## S6

- **definition** | S6-D1 | OrphanContent | Content in dom(C) unreachable from any Vstream entry point because it appears in no current arrangement
- **commentary** | — | — | Design rationale: Nelson's explicit rejection of GC for unreferenced content, historical backtrack motivation

## S7

- **definition** | D-ORIGIN | OriginFunction | The origin function mapping an element-level I-address to its document-level prefix tumbler N.0.U.0.D
- **commentary** | — | — | Two-stream separation: distinction between "where I am reading" (Vstream, document A) and "where this came from" (Istream, document B)

## S8

- **definition** | D-RUNS | RunCount | Notation #runs(d) for the number of correspondence runs in document d's current arrangement
- **commentary** | — | — | Architectural and performance implications of run fragmentation: representation cost, run splitting/removal under editing, Gregory's 40% CPU hotspot evidence, and the abandoned run-consolidation function

## S8-depth

- **derived** | S8-iaddr-uniformity | IAddressRunUniformity | all I-addresses in a correspondence run share the same tumbler depth and prefix, differing only at the element ordinal
- **commentary** | — | — | why non-trivial runs arise in practice (T10a/TA5(c) allocator discipline as motivation, not dependency)
- **definition** | OrdinalShiftExtension | OrdinalShiftExtension | extends ordinal displacement notation to k=0 for both V-positions and I-addresses
- **definition** | CorrespondenceRun | CorrespondenceRun | triple (v, a, n) such that M(d)(v+k) = a+k for all 0 ≤ k < n
- **definition** | DEF-ConsecutiveVPositions | ConsecutiveVPositions | positions within a subspace are consecutive iff they differ only at the ordinal (last) component
- **derived** | S8a-IRunUniformity | IRunUniformity | all I-addresses within a correspondence run share the same tumbler depth and prefix, differing only at the element ordinal
- **definition** | DEF-OrdinalDisplacementExtension | OrdinalDisplacementExtension | extends ordinal displacement notation to k=0 via v+0=v (identity) for both V-positions and I-addresses
- **definition** | DEF-CorrespondenceRun | CorrespondenceRun | triple (v, a, n) with n≥1 such that M(d)(v+k)=a+k for all 0≤k<n
- **definition** | S8-consec | ConsecutiveVPositions | Consecutive V-positions within a subspace differ only at the ordinal (last) component
- **derived** | S8-irun-uniform | IRunDepthUniformity | I-addresses within a correspondence run share depth and prefix, following from TumblerAdd's prefix-copy rule
- **definition** | S8-ord-ext | OrdinalDisplacementExtension | Extends ordinal displacement notation to k=0 as identity for both V-positions and I-addresses
- **definition** | S8-corrrun | CorrespondenceRun | A correspondence run is a triple (v, a, n) such that M(d)(v+k) = a+k for all 0 ≤ k < n
- **definition** | S8-ord-zero | OrdinalShiftZeroExtension | extends ordinal displacement notation to k=0 as identity for V-positions and I-addresses
- **definition** | S8-run | CorrespondenceRun | a triple (v, a, n) where M(d)(v+k) = a+k for all 0 ≤ k < n
- **definition** | D-consec-vpos | ConsecutiveVPositions | V-positions s.x and s.(x+1) within a subspace are consecutive iff they differ only at the ordinal component
- **definition** | D-ordshift-zero | OrdinalDisplacementZero | Extension of ordinal displacement notation to k=0 for both V-positions and I-addresses
- **definition** | D-corrrun | CorrespondenceRun | Triple (v, a, n) with arrangement condition M(d)(v+k) = a+k for 0 ≤ k < n
- **derived** | S8-iaddr-uniform | IAddressRunUniformity | All I-addresses in a correspondence run share the same tumbler depth and prefix, differing only at the element ordinal
- **definition** | DEF-consecutive-v-positions | ConsecutiveVPositions | Consecutive V-positions within a subspace differ only at the ordinal (last) component
- **derived** | S8b-run-uniformity | RunIAddressUniformity | I-addresses within a correspondence run share the same depth and prefix, differing only at the element ordinal
- **definition** | DEF-ordinal-displacement-zero | OrdinalDisplacementZero | Extension of ordinal displacement notation to k=0: v+0=v and a+0=a
- **definition** | DEF-correspondence-run | CorrespondenceRun | Triple (v, a, n) such that M(d)(v+k) = a+k for all 0 ≤ k < n

## Σ.M(d)

- **definition** | Σ.C | ContentStore | Partial function from tumblers to content values representing the Istream address-to-content mapping


*10 properties with embedded results.*
