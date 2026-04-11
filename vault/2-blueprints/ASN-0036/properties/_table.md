| Label | Name | Statement | Status |
|-------|------|-----------|--------|
| Σ.C | ContentStore | Content store: `T ⇀ Val`, mapping I-addresses to content values | introduced |
| Σ.M(d) | Arrangement | Arrangement for document `d`: `T ⇀ T`, mapping V-positions to I-addresses | introduced |
| S0 | ContentImmutability | Content immutability: `a ∈ dom(C) ⟹ a ∈ dom(C') ∧ C'(a) = C(a)` for all transitions | design requirement |
| S1 | StoreMonotonicity | Store monotonicity: `dom(C) ⊆ dom(C')` for all transitions | from S0 |
| S2 | ArrangementFunctionality | Arrangement functionality: `M(d)` is a function — each V-position maps to exactly one I-address | axiom |
| S3 | ReferentialIntegrity | Referential integrity: `(A d, v : v ∈ dom(M(d)) : M(d)(v) ∈ dom(C))` | design requirement |
| S4 | OriginBasedIdentity | Origin-based identity: distinct allocations produce distinct I-addresses regardless of value equality | from GlobalUniqueness, T3 (ASN-0034) |
| S5 | UnrestrictedSharing | Unrestricted sharing: S0–S3 do not entail any finite bound on sharing multiplicity | consistent with S0, S1, S2, S3 |
| S6 | PersistenceIndependence | Persistence independence: `a ∈ dom(C)` is unconditional — independent of all arrangements | from S0 |
| S7a | DocumentScopedAllocation | Document-scoped allocation: every I-address is allocated under the originating document's prefix | design requirement |
| S7b | ElementLevelIAddresses | Element-level I-addresses: `(A a ∈ dom(C) :: zeros(a) = 3)` | design requirement |
| S7c | ElementFieldDepth | Element-field depth: `(A a ∈ dom(C) :: #fields(a).element ≥ 2)` — subspace identifier and content ordinal occupy distinct components | design requirement |
| S7 | StructuralAttribution | Structural attribution: `origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)` — full document prefix | from S7a, S7b, S0, S4, T4, T3, GlobalUniqueness (ASN-0034) |
| S8-fin | FiniteArrangement | Finite arrangement: `dom(M(d))` is finite for every document `d` | design requirement |
| S8a | VPositionWellFormedness | V-position well-formedness: `(A v ∈ dom(M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0)` — universal, from T4 positive-component constraint | axiom |
| S8-depth | FixedDepthVPositions | Fixed-depth V-positions: `(A d, v₁, v₂ : v₁ ∈ dom(M(d)) ∧ v₂ ∈ dom(M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)` | design requirement |
| S8 | FiniteSpanDecomposition | Span decomposition: `dom(M(d))` decomposes into finitely many correspondence runs `(vⱼ, aⱼ, nⱼ)` with `M(d)(vⱼ + k) = aⱼ + k` for `0 ≤ k < nⱼ` | theorem from S8-fin, S2, S8a, S8-depth, T1, T3, T5, T10, TA5 (ASN-0034) |
| ord(v) | OrdinalExtraction | Ordinal extraction: ord(v) = [v₂, ..., vₘ]; when v satisfies S8a, ord(v) ∈ S | introduced |
| vpos(S, o) | VPositionReconstruction | V-position reconstruction: vpos(S, o) = [S, o₁, ..., oₖ]; inverse of ord for any o ∈ T; satisfies S8a when S ≥ 1 and all oᵢ > 0 | introduced |
| w_ord | OrdinalDisplacementProjection | Ordinal displacement projection: w_ord = [w₂, ..., wₘ] for displacement w with w₁ = 0 | introduced |
| OrdAddHom | OrdinalAdditionHomomorphism | (a) ord(v ⊕ w) = ord(v) ⊕ w_ord; (b) subspace(v ⊕ w) = subspace(v); (c) v ⊕ w = vpos(subspace(v), ord(v) ⊕ w_ord) | lemma (from ord, w_ord, TumblerAdd, TA0 (ASN-0034)) |
| OrdAddS8a | AdditionPreservesS8a | v ⊕ w satisfies S8a ⟺ all tail components of w after the action point are positive; equivalently ord(v ⊕ w) ∈ S ⟺ v ⊕ w satisfies S8a | lemma (from OrdAddHom, S8a, TumblerAdd (ASN-0034)) |
| OrdShiftHom | OrdinalShiftHomomorphism | ord(shift(v, n)) = shift(ord(v), n); shift(v, n) unconditionally satisfies S8a when v does | corollary of OrdAddHom, OrdAddS8a, OrdinalShift, OrdinalDisplacement (ASN-0034) |
| D-CTG | VContiguity | V-position contiguity: within each subspace, V-positions form a contiguous ordinal range with no gaps — design constraint on well-formed document states | design requirement |
| D-MIN | VMinimumPosition | V-position minimum: minimum V-position in each non-empty subspace has all post-subspace components equal to 1 — design constraint | design requirement |
| D-CTG-depth | SharedPrefixReduction | Shared prefix reduction: at depth m ≥ 3, contiguity reduces to the last component (all positions share components 2 through m − 1) | corollary of D-CTG, S8-fin, S8-depth, T0(a), T1, T3 (ASN-0034) |
| D-SEQ | SequentialPositions | Sequential positions (m ≥ 2): non-empty V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n} for some n ≥ 1 | from D-CTG, D-CTG-depth, D-MIN, S8-fin, S8-depth, T1 (ASN-0034) |
| ValidInsertionPosition | ValidInsertionPosition | if V_S(d) ≠ ∅: v = min(V_S(d)) or v = shift(min(V_S(d)), j) with 1 ≤ j ≤ N, common depth m ≥ 2; if V_S(d) = ∅: v = [S, 1, ..., 1] of depth m ≥ 2 | introduced |
| S9 | TwoStreamSeparation | Two-stream separation: arrangement changes cannot alter stored content | theorem from S0 |
| S8-depth-C1 | IAddressRunUniformity | All I-addresses in a correspondence run share the same tumbler depth and prefix, differing only at the element ordinal | corollary of OrdinalDisplacementExtension, CorrespondenceRun, TumblerAdd (ASN-0034), S7c |
| V_S(d) | SubspaceVPositionSet | `V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}`, the set of V-positions in subspace S of document d | introduced |
| ConsecutiveVPositions | ConsecutiveVPositions | Consecutive V-positions within a subspace differ only at the ordinal (last) component; well-defined under uniform depth | introduced |
| OrdinalDisplacementExtension | OrdinalDisplacementExtension | Extends ordinal displacement notation to `k = 0` as identity for both V-positions and I-addresses | introduced |
| CorrespondenceRun | CorrespondenceRun | Triple `(v, a, n)` with `n ≥ 1` such that `M(d)(v + k) = a + k` for all `0 ≤ k < n` | introduced |
