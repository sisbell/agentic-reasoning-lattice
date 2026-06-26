# ASN-0036 Formal Statements

*Source: ASN-0036-strand-model.md (revised 2026-05-29) — Extracted: 2026-06-26*

## S3 — ReferentialIntegrity

Proves that every V-position in every arrangement resolves to a content address that exists in the content store — there are no dangling references. Combined with store monotonicity (S1), a valid reference cannot become dangling after it is established: once a content address enters the store it persists permanently. This also means unreferenced content is never reclaimed, which Nelson's versioning model requires to reconstruct historical arrangements from retained I-stream fragments.

---

## Σ.M(d) — Arrangement

Defines the arrangement of a document as a partial function that maps each currently-active V-stream position to the I-stream address it references. The domain captures which V-positions exist in the document right now; the range captures which I-addresses the document currently holds.

---

## S7 — StructuralAttribution

Defines `origin(a)` — the document-level tumbler obtained by stripping the element field from an I-address — and proves this purely structural function permanently identifies the document that allocated the address, with no external registry or annotation required. Because the allocating document is encoded in the address itself, `origin` makes the two-stream separation concrete: a reader viewing transcluded content encounters it in one document (Vstream context) while `origin` traces the content back to the document where it was created (Istream structure), a distinction that is permanent and unseverable.

*Formal Contract:*

- *Definition:* For `a ∈ dom(Σ.C)`, `origin(a) = N(a).0.U(a).0.D(a)` — the document-level tumbler obtained by truncating the element field `E(a)` from `a`, formed by concatenating the node field, a zero separator, the user field, a zero separator, and the document field.
- *Preconditions:* `a ∈ dom(Σ.C)`; `A_element ∈ 𝒯 ∧ a ∈ dom(A_element)` for the document owner's T10a-conforming element allocator (S7a) — the two memberships of distinct types that license T10a.4's instantiation at `A := A_element, t := a`, yielding `a` T4-valid; `zeros(a) = 3` (S7b, element-level I-address).
- *Postconditions:* `origin(a)` is well-defined with `zeros(origin(a)) = 2` (document-level in T4's hierarchy); `origin(a)` equals the tumbler of the document that allocated `a` (S7a); for any `a₁, a₂ ∈ dom(Σ.C)` allocated under distinct documents, `origin(a₁) ≠ origin(a₂)` (S7d's distinct allocation events lifted to distinct addresses by GlobalUniqueness; decidable by T3).
- *Invariant:* For every `Σ → Σ'`, if `a ∈ dom(Σ.C)` then `a ∈ dom(Σ'.C)` (S0) and `origin(a)` is unchanged — the attribution is permanent and unseverable.
- *Frame:* `origin(a)` is a pure function of the components of `a` alone; it reads no state beyond `dom(Σ.C)` membership and modifies nothing.

- *Depends:*
  - S0 (ContentImmutability) — supplies the persistence guarantee `a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)` used in the Permanence step to establish that `origin(a)` is unchanged across all successor states
  - S4 (OriginBasedIdentity) — cited as co-establishing that I-addresses are unique, grounding the claim in the body that origin-based attribution is permanent and unseverable
  - S7a (DocumentScopedAllocation) — supplies (i) the allocation rule that the document-level prefix of `a` equals the allocating document's tumbler, used in the Identification step to ground `origin(a) IS the allocating document's tumbler`; and (ii) the two memberships of distinct types `A_element ∈ 𝒯` (the element allocator is a node of the tree) and `a ∈ dom(A_element)` (the address lies in its domain), used in Well-definedness to license the T10a.4 instantiation at `A := A_element, t := a`
  - S7b (ElementLevelIAddresses) — supplies `zeros(a) = 3` for every `a ∈ dom(Σ.C)`, placing `a` at the element level (all four identifying fields present) so that, once T4-validity has activated T4's field-decomposition machinery, truncating the element field yields a well-defined document-level tumbler in Well-definedness
  - S7d (DocumentAllocationDiscipline) — supplies that every document's document-level tumbler arises from an allocation event under T10a's discipline and that distinct documents arise from distinct allocation *events*; the Uniqueness step feeds this event-level separation to GlobalUniqueness. (S7d does not itself state tumbler-distinctness — converting distinct events to distinct addresses is GlobalUniqueness's step, not S7d's.)
  - GlobalUniqueness (GlobalUniqueness, ASN-0034) — supplies the invariant that addresses arising from distinct allocation events are distinct; instantiated in the Uniqueness step at the two documents' allocation events (separated by S7d) to lift event-distinctness to document-level-tumbler distinctness, establishing `origin(a₁) ≠ origin(a₂)`. The same theorem S4 invokes for the I-address case.
  - T3 (CanonicalRepresentation, ASN-0034) — supplies decidable component-wise comparison, used in Uniqueness to confirm `origin(a₁) ≠ origin(a₂)` is decidable from the components of `a₁` and `a₂` alone
  - T4 (HierarchicalParsing, ASN-0034) — supplies the zero-count field-decomposition machinery and the document-level hierarchy (`zeros = 2`) used throughout Well-definedness and the Formal Contract
  - T4a (SyntacticEquivalence, ASN-0034) — supplies the equivalence that every field segment is non-empty, used in Well-definedness to confirm N(a), U(a), and D(a) each contain at least one strictly positive component
  - T4b (UniqueParse, ASN-0034) — supplies the partial projections N(a), U(a), D(a), E(a) used throughout to extract the node, user, document, and element fields from `a`, together with the postcondition that each defined projection returns a sequence over `ℕ⁺` (every component strictly positive), consumed in Well-definedness to discharge the strict positivity of each field's components
  - T10a.4 (T4PreservationUnderDiscipline, ASN-0034) — instantiated at the element allocator `A_element` and `a ∈ dom(A_element)` (the membership supplied by S7a), yields T4-validity of `a`, the precondition that licenses T4's field-decomposition machinery in Well-definedness

---

## S4 — OriginBasedIdentity

Establishes that distinct allocation events always produce distinct I-addresses, regardless of whether the stored values are equal. This is the formal basis for the transclusion/copy distinction: two document positions sharing an I-address are structurally linked (transclusion), while positions with equal values but different I-addresses are independent copies — a difference computable from addresses alone without value comparison.

*Formal Contract:*

- *Preconditions:* `a₁, a₂ ∈ dom(Σ.C)` are produced by distinct allocation events within a system conforming to T10a (allocator discipline, ASN-0034). No condition is placed on the values `Σ.C(a₁)`, `Σ.C(a₂)`.
- *Postconditions:* `a₁ ≠ a₂`.
- *Invariant:* For every pair of I-addresses `a₁, a₂` produced by distinct allocation events in any reachable system state, `a₁ ≠ a₂`, independent of whether `Σ.C(a₁) = Σ.C(a₂)`.
- *Frame:* The content store `C` is unchanged; the identity test reads addresses alone (T3, ASN-0034), neither referencing nor comparing the stored values `Σ.C(a₁)`, `Σ.C(a₂)`.

- *Depends:*
  - GlobalUniqueness (GlobalUniqueness) — supplies the invariant that distinct allocation events produce distinct addresses, which the proof instantiates directly to obtain `a₁ ≠ a₂`
  - T10a (AllocatorDiscipline) — supplies the allocator-discipline precondition under which GlobalUniqueness's invariant holds; required as a precondition in both the proof and the Formal Contract
  - T3 (CanonicalRepresentation) — supplies the canonical-representation property (tumbler equality ≡ position-wise equality) that grounds the Frame condition: the identity test reads addresses alone without comparing stored values

---

## S8a — ArrangementDomainRestriction

Establishes that every active key in the strand's arrangement is a well-formed V-position: a zero-free tumbler of depth at least 2, meaning a subspace identifier paired with at least one within-subspace ordinal. This domain restriction is the structural premise that content always lives inside a named subspace rather than at a bare top-level coordinate — a necessary invariant for the two-component strand model to be coherent.

---

## ValidInsertionPosition — ValidInsertionPosition

Defines the set of valid V-positions at which text may be inserted into a non-empty document: exactly the N+1 positions of the form [1, …, 1, 1+j] for j ∈ {0, …, N}, where N is the current document length. Each valid position lies in the text subspace (first component equals 1), has no zero components, and the N+1 positions are pairwise distinct.

*Formal Contract:*

- *Preconditions:* `V_1(d) ≠ ∅`; the common V-position depth `m` of `V_1(d)` is fixed by S8-depth and satisfies `m ≥ 2` by S8a.
- *Definition:* With `N = |V_1(d)|`, `ValidInsertionPosition(d, v)` holds iff `v = min(V_1(d))` or `v = shift(min(V_1(d)), j)` for some `j ∈ {1, ..., N}`. By D-MIN, `min(V_1(d)) = [1, ..., 1]` of depth `m`, and by OrdinalShift (ASN-0034) `shift([1, ..., 1], j) = [1, ..., 1, 1 + j]`; equivalently the satisfying set is `{[1, ..., 1, 1 + j] : j ∈ {0, ..., N}}`.
- *Postconditions:* The satisfying set contains exactly `N + 1` pairwise-distinct positions (NAT-order and T3, ASN-0034). Each satisfying `v` has `v₁ = 1` as the text subspace identifier (OrdShiftHom) and `zeros(v) = 0` with every component `≥ 1` (componentwise positivity).

- *Depends:*
  - S8-depth (FixedDepthVPositions) — supplies the common V-position depth `m` of V_1(d) asserted in the preconditions and used throughout the proof to fix the tumbler length
  - S8a (ArrangementDomainRestriction) — supplies the `m ≥ 2` lower bound on depth, invoked in the preconditions, and the zero-free / componentwise-positive predicate verified on each satisfying `v` in the postconditions
  - D-MIN (VMinimumPosition) — supplies `min(V_1(d)) = [1, …, 1]` of depth `m`, the base position from which all satisfying `v` are constructed in both the definition and the proof
  - OrdinalShift (ASN-0034) — supplies the `shift` operator and its expansion `shift([1,…,1], j) = [1,…,1, 1+j]`, the key step in deriving the satisfying-set formula in the proof and formal contract
  - OrdShiftHom (OrdinalShiftPreservation) — supplies part (a) `subspace(shift(v, n)) = subspace(v)`, invoked to establish `v₁ = 1` as the text subspace identifier for every satisfying position (postcondition)
  - T3 (ASN-0034) — supplies the distinctness criterion for length-`m` tumblers that differ at any component, used to conclude the `N + 1` satisfying positions are pairwise distinct
  - NAT-order (ASN-0034) — supplies the strict total order on natural numbers, used to establish `1 + j ≠ 1 + j'` for `j ≠ j'`, driving the distinctness count in the proof and postconditions

---

## S5 — UnrestrictedSharing

Proves that the axioms S0–S3 impose no finite upper bound on how many times a single I-address may be referenced across the system — neither across multiple documents nor within one document. Two explicit witness constructions demonstrate that for any natural number N, a valid model exists in which some address is shared more than N times. This makes unbounded transclusion — the ability for any number of documents to quote the same passage while the system recognizes them all as referencing the same content — a structural consequence of the foundational axioms alone.

*Formal Contract:*

- *Definition (witness constructions):* For each `N ∈ ℕ`, both witnesses share content store `C = {a ↦ w}` with a single I-address `a` and arbitrary `w ∈ Val`, and each is taken as the initial state of the trivial transition system whose transition relation is empty.
  - *Cross-document:* `Σ_N = (C_N, M_N)` with `C_N = {a ↦ w}`, documents `dᵢ = [1, 0, 1, 0, i]` for `i = 1, …, N + 1`, shared V-position `v = [1, 1]`, and `M_N(dᵢ) = {v ↦ a}`.
  - *Within-document:* `Σ'_N = (C'_N, M'_N)` with `C'_N = {a ↦ w}`, single document `d = [1, 0, 1, 0, 1]`, and `M'_N(d) = {vₖ ↦ a : vₖ = [1, k], k = 1, …, N + 1}`.
- *Invariant:* Each witness models S0–S3. S0 (content immutability) and S1 (store monotonicity) hold vacuously over the empty transition relation; S2 (arrangement functionality) and S3 (referential integrity, `a ∈ dom(C)`) hold on the state. Document distinctness (cross-document) and V-position distinctness (within-document) follow from distinct last components by T3 (CanonicalRepresentation, ASN-0034).
- *Postconditions:* `(A N ∈ ℕ :: (E Σ :: Σ is the initial state of a model of S0–S3 ∧ (E a ∈ dom(Σ.C) :: |{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N)))`. Hence S0–S3 entail no finite uniform bound on sharing multiplicity — neither across documents nor within a single document.

- *Depends:*
  - S0 (ContentImmutability) — supplies the transition-level invariant definition the proof discharges vacuously: the empty transition relation has no transitions to range over, so S0's universal quantifier holds; knowing S0's form is required to confirm it holds on the witness
  - S1 (StoreMonotonicity) — supplies the transition-level invariant definition discharged vacuously alongside S0: with an empty transition relation, S1's universal quantifier over transitions `Σ → Σ'` holds trivially; required to confirm the witnesses are genuine models of S1
  - S2 (ArrangementFunctionality) — supplies the state-level single-valuedness invariant verified per construction: both witnesses explicitly discharge S2 by showing each arrangement maps its domain to a single I-address `a`
  - S3 (ReferentialIntegrity) — supplies the state-level referential-integrity invariant discharged in the shared facts block: the sole I-address referenced by any arrangement is `a ∈ dom(C)`, satisfying S3's `Σ.M(d)(v) ∈ dom(Σ.C)` requirement
  - T3 (CanonicalRepresentation, ASN-0034) — supplies the tumbler extensionality principle used in both constructions to conclude pairwise distinctness from distinct last components: documents `dᵢ` (cross-document) and V-positions `vₖ` (within-document) are distinct because their last components differ
- *Forward References:*
  - S4 (OriginBasedIdentity) — cited as the peer claim that, together with S5, makes quotation a first-class structural relationship; S4's body is not consumed in S5's proof

---

## S8 — CorrespondenceRunPartition

Proves that the active V-positions of any document decompose uniquely into finitely many maximal correspondence runs, where each run is a maximal block of V-positions and content addresses that advance together in lockstep under ordinal displacement. The uniqueness and partition properties follow from a lockstep-successor function on dom(M(d)) that is injective and acyclic by shift algebra, so its graph splits into disjoint chains whose orbits are forced at every step. Each maximal run lies entirely within one subspace at one depth, the runs are pairwise disjoint and jointly cover all of dom(Σ.M(d)), and no other maximal-run decomposition exists.

*Formal Contract:*

- *Definition:* For a document `d`, a *correspondence run* is a triple `(v, a, n)` with `v ∈ dom(M(d))`, `a = M(d)(v)`, `n ≥ 1`, such that for every `k` with `0 ≤ k < n`: `shift(v, k) ∈ dom(M(d))`, `M(d)(shift(v, k)) = shift(a, k)`, and `shift(a, k) ∈ dom(Σ.C)`. The *lockstep successor* `succ` is the partial function on `dom(M(d))` with `succ(v) = shift(v, 1)` exactly when `shift(v, 1) ∈ dom(M(d))` and `M(d)(shift(v, 1)) = shift(M(d)(v), 1)`, and undefined otherwise. A *maximal chain* is an orbit of `succ` (its head has no lockstep predecessor, its tail no lockstep successor); a *maximal run* is the run read off a maximal chain.

- *Axiom:* (convention) `shift(t, 0) := t` — ordinal displacement by zero is the identity; this extends `shift` so the run conditions are stated at `k = 0` without invoking TS3 (whose preconditions require shift amounts `≥ 1`).

- *Preconditions:*
  - `M(d)` is a single-valued partial function (S2).
  - `ran(M(d)) ⊆ dom(Σ.C)` — referential integrity (S3).
  - `dom(M(d))` is finite (S8-fin).
  - Every `v ∈ dom(M(d))` is a well-formed V-position at a fixed depth `m` (S8a, S8-depth).
  - `shift` preserves subspace, depth, and well-formedness (OrdShiftHom (a), (b), and the frame `#shift(v, 1) = #v`).
  - Shift algebra over ASN-0034: ShiftInjectivity (TS2), ShiftComposition for amounts `≥ 1` (TS3), ShiftStrictIncrease (TS4), and the strict order T1 with irreflexivity.

- *Postconditions:*
  - The maximal correspondence runs are pairwise vertex-disjoint and their union is `dom(Σ.M(d))` — they partition it.
  - There are finitely many maximal runs (each finite).
  - The maximal-run decomposition is unique.
  - Within each maximal run `(v, a, n)`, for every `0 ≤ k < n`: `shift(v, k) ∈ dom(M(d))`, `M(d)(shift(v, k)) = shift(a, k)`, and `shift(a, k) ∈ dom(Σ.C)` (conjuncts (a) and (b)).

- *Invariant:* Along every lockstep link `vⁱ → vⁱ⁺¹ = succ(vⁱ)` of a chain, the image advances in lockstep: `M(d)(vⁱ⁺¹) = shift(M(d)(vⁱ), 1)`, equivalently `M(d)(shift(v, i+1)) = shift(a, i+1)` along the run.

- *Frame:* Each lockstep step preserves subspace and depth: `subspace(succ(v)) = subspace(v)` and `#succ(v) = #v`; every maximal chain therefore lies within a single subspace at one depth. The decomposition reads `Σ.M(d)` and `Σ.C` and does not modify `Σ`.

- *Depends:*
  - S2 (ArrangementFunctionality) — supplies the single-valuedness of M(d) used as a precondition throughout (well-defined label conjunct, Formal Contract precondition)
  - S3 (ReferentialIntegrity) — supplies `ran(M(d)) ⊆ dom(Σ.C)` used to verify that every lockstep image `shift(a, k)` lies in `dom(Σ.C)` (conjunct (b) and the succ-preservation argument)
  - S8a (ArrangementDomainRestriction) — supplies the well-formedness predicate (`zeros(t)=0`, `#t≥2`) that every `v ∈ dom(M(d))` satisfies; consumed by OrdShiftHom (b) to propagate well-formedness along lockstep links
  - S8-depth (FixedDepthVPositions) — supplies the subspace-wide common depth `m`: for `v ∈ dom(M(d))`, `m = #v` is the depth shared by every active position in `v`'s subspace, which is what lets the chains and `succ`'s confinement be stated at the single depth `m`. It does *not* license the succ-confinement step's per-position depth equality `#shift(v, 1) = #v`: that is an unconditional frame property of `shift` (OrdShiftHom's frame, ultimately TA0), true whether or not `shift(v, 1) ∈ dom(M(d))`, so the step grounds the depth claim there rather than in S8-depth's quantifier — which would require both `v` and `shift(v, 1)` active before it applies. Likewise it does *not* license the injectivity step's appeal to TS2: there the common depth `#u = #u'` is derived locally from `shift(u, 1) = shift(u', 1)` together with shift's depth-preservation (`#shift(t, 1) = #t`), not from S8-depth's subspace-wide assertion
  - S8-fin (FiniteArrangement) — supplies finiteness of `dom(M(d))`; used to guarantee that forward walks under `succ` terminate and that the maximal-run decomposition is finite
  - OrdShiftHom (OrdinalShiftPreservation) — supplies parts (a) and (b): subspace preservation and S8a-preservation under `shift(v,1)`, together with its depth-preservation frame `#shift(v,1) = #v` (ultimately TA0); used to show every lockstep link stays within one subspace at the same depth, the per-position depth equality grounded unconditionally in the frame rather than in S8-depth's domain-restricted quantifier
  - OrdinalShift (ASN-0034) — supplies the `shift` operator on which S8's entire formulation rests: the correspondence-run definition (`shift(v, k) ∈ dom(M(d))`, `M(d)(shift(v, k)) = shift(a, k)`), the lockstep successor `succ(v) = shift(v, 1)`, and the displacement identity carried along every run. OrdShiftHom, TS2, TS3, and TS4 are *consumers* of `shift`, not its defining claim, so they do not by themselves ground the operator. S8 invokes `shift` abstractly and never expands it as `v ⊕ δ(n, m)`; it therefore reaches the displacement `δ` only through OrdinalShift and does *not* depend on OrdinalDisplacement directly
  - TS2 (ShiftInjectivity, ASN-0034) — supplies injectivity of `shift` at a common depth; used to conclude `succ(u)=succ(u')` implies `u=u'`, establishing that `succ` is injective
  - TS3 (ShiftComposition, ASN-0034) — supplies `shift(shift(v,i),1)=shift(v,i+1)` for shift amounts ≥1; used in the induction step to collapse nested shifts and establish the displacement identity at every `k`
  - TS4 (ShiftStrictIncrease, ASN-0034) — supplies `shift(v,1)>v`; used to show each `succ`-step strictly increases under T1, ruling out cycles
  - T1 (LexicographicOrder, ASN-0034) — supplies irreflexivity (`v < v` is false); used to close the acyclicity argument by contradiction once TS4 gives `shift(v,1)>v`

---

## ValidFirstInsertionPosition — ValidFirstInsertionPosition

Defines the valid first insertion position for an empty subspace: when no v-positions exist yet, the only legal insertion point is an all-ones tumbler of some chosen depth m, which is exactly the position D-MIN will require once the subspace becomes non-empty. The ternary form (d, v, m) makes the depth choice explicit because there is no existing state from which to read it.

---

## S0 — ContentImmutability

Proves that content is immutable: once a value is stored at address `a` in the content stream, that address persists in every future state and its value never changes. This guarantees that the content stream grows monotonically and that any reference to a stored address remains valid and stable across all state transitions.

---

## D-CTG — VContiguity

Proves that the text subspace of any document is gap-free: if two V-positions at depth 1 both belong to a document, every V-position between them at that depth must also belong to it. Combined with the finiteness of the domain, this collapses to a single unbroken block of ordinals — the text subspace cannot have holes.

---

## S1 — StoreMonotonicity

Proves that the content store's address domain grows monotonically across state transitions: once an address enters dom(C), it is never removed. This follows directly from content immutability (S0) and establishes C as an append-only log — the protocol provides no mechanism to delete or overwrite stored entries.

*Formal Contract:*
- *Preconditions:* S0 (content immutability) holds across the transition `Σ → Σ'`.
- *Invariant:* For every state transition `Σ → Σ'`, `dom(Σ.C) ⊆ dom(Σ'.C)` — the address domain of the content store is monotonically non-decreasing.
- *Frame:* No address is ever removed from `dom(C)`; `C` is append-only with respect to its address domain.

- *Depends:*
  - S0 (ContentImmutability) — supplies the implication `a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)` used as the single proof step in the body of S1
- *Forward References:*
  - T9 (ForwardAllocation) — cited as guaranteeing that fresh addresses allocated in new transitions are strictly increasing within each allocator's stream; not used in S1's proof
  - T10 (PartitionIndependence) — cited alongside T9 as guaranteeing cross-allocator address uniqueness for fresh entries; not used in S1's proof

---

## S8-fin — FiniteArrangement

Establishes that every document's arrangement map is finite — no reachable system state may assign infinitely many V-positions to a single document. This is a hard design constraint, not a derived property: it rules out pathological infinite arrangements before any further structural reasoning proceeds.

---

## D-CTG-depth — SharedPrefixReduction

Proves that in any non-empty V-position set of depth m ≥ 3, all positions must agree on every intermediate component (2 through m−1), so the set's contiguity reduces to contiguity of the final component alone — the same structural condition as the depth-2 case. The argument is by contradiction: any disagreement at an intermediate component would allow constructing infinitely many distinct valid intermediates via unbounded component values, violating finiteness of the domain.

*Formal Contract:*

- *Preconditions:*
  - V_1(d) ≠ ∅ (non-empty).
  - All positions in V_1(d) share a common depth m (S8-depth), with m ≥ 3 — a scope restriction, not a derived bound: at m ≥ 3 the interior index range 2 ≤ i ≤ m − 1 is non-empty, so the shared-prefix claim has content, whereas the m = 2 case, where that range is empty and the claim is vacuous, is handled separately in D-SEQ's m = 2 case.
  - Every position p ∈ V_1(d) has subspace(p) = p₁ = 1.
  - V_1(d) ⊆ dom(M(d)), and every position in dom(M(d)) satisfies S8a: `#p ≥ 2 ∧ (A i : 1 ≤ i ≤ #p : pᵢ > 0)`.
  - V_1(d) is contiguous in the position order (D-CTG): if u, x ∈ V_1(d), u < w < x, subspace(w) = 1, #w = #u, and w satisfies S8a, then w ∈ V_1(d).
  - dom(M(d)) is finite (S8-fin).
  - Component values are unbounded: for any bound M ∈ ℕ there exists n ∈ ℕ with n > M (T0(a), ASN-0034).

- *Postconditions:*
  - `(A u, x : u ∈ V_1(d) ∧ x ∈ V_1(d) : (A i : 2 ≤ i ≤ m − 1 : uᵢ = xᵢ))` — every pair of positions in V_1(d) agrees on components 2 through m − 1.
  - Contiguity of V_1(d) is determined by component m alone, structurally identical to the depth-2 case.

- *Definition:* For positions u, x ∈ V_1(d) (u < x, both depth m) whose first disagreement is at component j with 2 ≤ j ≤ m − 1, and for any n > uⱼ₊₁, the intermediate witness w of depth m is constructed by: wᵢ = uᵢ for 1 ≤ i ≤ j; wⱼ₊₁ = n; wᵢ = 1 for j + 2 ≤ i ≤ m (an empty clause when j = m − 1).

- *Depends:*
  - S8-depth (FixedDepthVPositions) — supplies the shared depth `m` for all positions in V_1(d), consumed as the proof's starting invariant that all elements have a common depth before the contradiction is constructed
  - T1 (LexicographicOrder, ASN-0034) — supplies the component-comparison clause of the lexicographic order; invoked at three points in the proof to derive u < w and w < x from the first differing component
  - S8a (ArrangementDomainRestriction) — supplies the well-formedness predicate (`#p ≥ 2 ∧ (A i : 1 ≤ i ≤ #p : pᵢ > 0)`) that the constructed intermediate w must satisfy before D-CTG can require w ∈ V_1(d)
  - D-CTG (VContiguity) — supplies the contiguity axiom applied to force w ∈ V_1(d) from u < w < x with matching subspace, depth, and S8a well-formedness; the claim's contradiction rests on producing infinitely many such w
  - T0(a) (UnboundedComponentValues, ASN-0034) — supplies, for any bound M, a witness n > M; consumed to construct the strictly increasing sequence n₁ < n₂ < … of admissible intermediates that contradicts S8-fin
  - T3 (CanonicalRepresentation, ASN-0034) — supplies tumbler equality as component-wise identity; used to conclude that distinct values of n yield distinct depth-m positions w (differing at component j + 1)
  - S8-fin (FiniteArrangement) — supplies finiteness of dom(M(d)); the proof is by contradiction, and the infinite sequence of distinct positions in V_1(d) contradicts this finiteness
- *Forward References:*
  - T4 (HierarchicalParsing, ASN-0034) — cited as the structural reason zero is unavailable as a V-position component (zero is a field separator), grounding the 1-based ordinal convention for V-positions stated after the main proof

---

## subspace — VPositionSubspaceIdentifier

Defines the subspace projection function, which extracts the first component of a V-position tumbler to identify which subspace that position belongs to. This makes subspace membership a direct read of an address component rather than a lookup against any external structure.

---

## D-MIN — VMinimumPosition

Posits the left-anchoring design requirement: in any non-empty document the minimum V-position is the all-ones tuple [1,1,...,1] of length m, so every document's text block begins at the origin of its subspace. Imposed on well-formed states rather than derived — contiguity (D-CTG), positivity (S8a), and finiteness (S8-fin) do not entail it, as the contiguous/positive/finite witness {[1,5],[1,6],[1,7]} (whose minimum is [1,5] ≠ [1,1]) shows. Consumed downstream by D-SEQ and ValidInsertionPosition as a premise.

*Formal Contract:*

- *Design Requirement:* For each document d with V_1(d) ≠ ∅, min(V_1(d)) = [1, 1, ..., 1] — the length-m tuple (m the common V-position depth fixed by S8-depth) with every component 1; at depth 2, min(V_1(d)) = [1, 1]. This is posited as an invariant of every well-formed strand state (the left-anchoring of a document's text at its subspace origin); it is *not* entailed by D-CTG, S8a, and S8-fin, witnessed by the contiguous, positive, finite, depth-2 set {[1, 5], [1, 6], [1, 7]}, whose minimum is [1, 5] ≠ [1, 1].
- *Definition:* min(S) denotes the least element of S under T1's strict total order `<` on tumblers (LexicographicOrder, ASN-0034), which restricted to the fixed depth m is exactly lexicographic order on integer m-tuples. We apply min only to S = V_1(d), and V_1(d) ⊆ dom(Σ.M(d)) is finite by S8-fin. A strict total order has a unique least element on every finite non-empty set — fold the binary minimum (well-defined by T1's totality, order-independent by T1's transitivity) across the finitely many elements — so min(V_1(d)) exists and is unique whenever V_1(d) ≠ ∅. We need no well-ordering of the infinite position space, only the finiteness of the single set to which min is applied.

- *Depends:*
  - S8-depth (FixedDepthVPositions) — supplies the common depth m shared by all V-positions in the text subspace, so that the all-ones tuple [1, 1, ..., 1] in the statement has a definite length
  - T1 (LexicographicOrder, ASN-0034) — supplies the strict total order `<` on tumblers whose restriction to the fixed-depth m-tuples is the lexicographic total order under which `min(V_1(d))` is the least element
  - S8-fin (FiniteArrangement) — supplies the finiteness of dom(Σ.M(d)); since V_1(d) ⊆ dom(Σ.M(d)), this makes V_1(d) finite, which is what guarantees min(V_1(d)) exists (a finite non-empty totally ordered set has a least element), replacing any appeal to a well-ordering of the infinite position space

---

## Σ.C — ContentStore

Defines the content store as a partial function from Istream addresses to opaque content values, establishing which I-addresses have stored content via its domain. The content values themselves are treated as an uninterpreted set at this abstraction level, keeping the model independent of any particular content representation.

---

## S7b — ElementLevelIAddresses

Establishes that every address stored as a content key in the content store Σ.C must be a fully-qualified element-level tumbler — one that specifies all four identifying fields (node, user, document, element). This rules out partial or higher-level addresses as content-store keys, ensuring the content store is indexed exclusively at the finest granularity.

---

## S8-depth — FixedDepthVPositions

Proves that within any subspace of a document, every V-position tumbler has the same depth, meaning all V-addresses in a subspace share identical component count. This uniformity makes "consecutive V-positions" well-defined: the successor of any position v is obtained by incrementing only its final (ordinal) component via shift, while the subspace prefix and depth remain fixed.

---

## D-SEQ — SequentialPositions

Proves that the V-positions of a document's text subspace are always a contiguous sequential block: when non-empty, they take the form [1, 1, …, 1, k] for k running from 1 to some maximum n, with all components except the last fixed at 1. This is the formal correlate of Nelson's "addresses 1 through n" — the text subspace of any well-formed document is a gapless, 1-based sequence regardless of the tuple depth imposed by the subspace structure.

*Formal Contract:*

- *Preconditions:* V_1(d) is non-empty. The document state is well-formed, so the contiguity constraint D-CTG (VContiguity) and the minimality property D-MIN (VMinimumPosition) hold. All V-positions in the text subspace share a common depth m (S8-depth), with `m ≥ 2` (S8a), and dom(M(d)) is finite (S8-fin).
- *Postconditions:* There exists n ≥ 1 such that V_1(d) = {[1, 1, …, 1, k] : 1 ≤ k ≤ n}, where each tuple has length m. Equivalently, the m-th-component values attained by the positions of V_1(d) are exactly the contiguous set {1, 2, …, n}.
- *Invariant:* In every well-formed state reachable from the empty base state (dom(M(d)) = ∅), D-CTG and D-MIN hold, and consequently V_1(d) is either empty or of the sequential form {[1, 1, …, 1, k] : 1 ≤ k ≤ n}. Across each transition s → s' that preserves well-formedness, this characterization is preserved; the base state satisfies it vacuously since V_1(d) = ∅.

- *Depends:*
  - S8-depth (FixedDepthVPositions) — supplies the common-depth guarantee for V_1(d); the proof opens by fixing m as that common depth and invokes S8-depth to assert it exists
  - S8a (ArrangementDomainRestriction) — supplies the depth ≥ 2 lower bound (m ≥ 2); the claim states "the derivation below relies on this lower bound" and Step 3 re-invokes it to qualify the intermediate witness w
  - D-CTG-depth (SharedPrefixReduction) — supplies the shared-prefix result (components 2 through m − 1 identical) used in Step 1 Case m ≥ 3 to pin all but the last component to 1
  - D-MIN (VMinimumPosition) — supplies min(V_1(d)) = [1, 1, …, 1]; Step 1 (Case m ≥ 3) uses it to fix the shared-prefix value to 1, and Step 2 uses it to establish k = 1 as an attained value
  - T1 (LexicographicOrder, ASN-0034) — supplies the lexicographic comparison rule; Step 3 invokes it twice to establish v₁ < v₂ and v₁ < w < v₂ from component-wise comparisons
  - D-CTG (VContiguity) — supplies the contiguity constraint; Step 3 applies it to conclude the intermediate witness w ∈ V_1(d), making the k-values a contiguous range
  - S8-fin (FiniteArrangement) — supplies the finiteness of dom(M(d)); Step 4 uses it to conclude V_1(d) is finite, bounding the k-value range

---

## S7a — DocumentScopedAllocation

Proves that every Istream element address is permanently bound to the document that created it: the document's tumbler prefix is recoverable from the address alone, with no external registry or allocator state required. This is Nelson's baptism principle in formal dress — a document owner controls all allocations under its prefix, so the home document is always ascertainable by inspecting the address itself.

---

## OrdShiftHom — OrdinalShiftPreservation

Proves that ordinal shift preserves two structural invariants of a V-position: the text subspace coordinate (first component) is unchanged because shift acts only on the deepest component, and the S8a well-formedness condition (all components positive, depth at least two) is inherited because adding a positive integer to a positive component keeps it positive.

*Formal Contract:*

- *Preconditions:* `v` is a V-position with `#v = m ≥ 2`; `n ≥ 1`. For part (b), additionally `v` satisfies S8a (`zeros(v) = 0` and `vᵢ ≥ 1` for every `i`).
- *Postconditions:* (a) `subspace(shift(v, n)) = subspace(v)`. (b) If `v` satisfies S8a, then `shift(v, n)` satisfies S8a.
- *Frame:* `#shift(v, n) = #v = m` (depth preserved); for every `1 ≤ i < m` the component is copied unchanged (`rᵢ = vᵢ`), in particular the text subspace `r₁ = v₁` is preserved; only the action-point component changes (`rₘ = vₘ + n`).
- *Definition:* `shift(v, n) = v ⊕ δ(n, m)`, where `δ(n, m) = [0, ..., 0, n]` is the ordinal displacement of length `m` with `actionPoint(δ(n, m)) = m` (OrdinalShift, OrdinalDisplacement).

- *Depends:*
  - OrdinalShift (OrdinalShift) — supplies the `shift(v, n) = v ⊕ δ(n, m)` definition that the proof expands throughout, and the component lower bound postcondition `shift(v, n)_{#v} = v_{#v} + n ≥ 1` that discharges the action-point component `rₘ ≥ 1` in part (b), so the lemma consumes that bound instead of re-deriving it from ℕ arithmetic.
  - OrdinalDisplacement (OrdinalDisplacement) — supplies `δ(n, m) = [0,...,0,n]` and the postcondition `actionPoint(δ(n, m)) = m` invoked to confirm well-definedness and to identify the action point in the component-wise expansion.
  - TumblerAdd (TumblerAdd) — supplies the component-wise rule `rᵢ = vᵢ` for `i < m` and `rₘ = vₘ + n`; part (a) and part (b) are both built entirely on this expansion.
  - TA0 (WellDefinedAddition) — supplies `#(a ⊕ w) = #w`, instantiated as `#r = #δ(n,m) = m` (depth preserved), used in the frame condition and the S8a verification.
  - S8a (ArrangementDomainRestriction) — supplies the predicate definition (`zeros(t) = 0`, `#t ≥ 2`, all components ≥ 1`) consumed as the part (b) hypothesis and proved to hold on `shift(v, n)`.

---

## S2 — ArrangementFunctionality

Establishes that the arrangement map Σ.M(d) is single-valued: any V-position in its domain yields exactly one I-address. This is not a derived result but a direct consequence of the partial-function type declaration, which by definition prohibits multiple images for a single argument.

*Formal Contract:*
- *Axiom:* `Σ.M(d)` is declared with the partial-function type `T ⇀ T`. By the meaning of that declaration a partial function admits at most one image per domain element, so the arrangement is single-valued: `(A d, v, a₁, a₂ : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a₁ ∧ Σ.M(d)(v) = a₂ : a₁ = a₂)`. This holds by design of the state signature, not by derivation from other claims.

---

## S7d — DocumentAllocationDiscipline

Establishes that document addresses are not arbitrary tumbler values but must originate from a real allocation event governed by T10a's discipline, ensuring every document-level tumbler (zeros = 2) has a unique, traceable birthplace. Distinct documents are structurally separated by construction: no two documents share an allocation event, so their addresses cannot collide.

---

