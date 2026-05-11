# ASN-0036 Claim Statements

*Source: ASN-0036-strand-model.md (revised 2026-04-11) — Extracted: 2026-05-11*

## Definition — SubspaceIdentifier

For any tumbler `v` of depth `#v ≥ 1`:

`subspace(v) = v₁`

Signature: `subspace : T → ℕ` — projects the first component of a tumbler.

Postconditions: (a) `subspace(v) ∈ ℕ`. (b) When `v` satisfies S8a, `subspace(v) ≥ 1`. (c) For `#v = m ≥ 2` and `n ≥ 1`, `subspace(shift(v, n)) = subspace(v)`.

---

## Definition — ShiftExtended

For any tumbler `v` and `k ≥ 0`:

`shift(v, 0) = v` (identity); for `k ≥ 1`, `shift(v, k) = v ⊕ δ(k, #v)` per OrdinalShift (ASN-0034).

For I-addresses: `shift(a, 0) = a` and `shift(a, k) = a ⊕ δ(k, #a)` for `k ≥ 1`. The action point of `δ(k, #a)` is `#a`; TumblerAdd's prefix rule copies all earlier components unchanged, producing a result of length `#a`.

---

## Definition — TextSubspaceVPositions

`V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}` — the set of V-positions in subspace S of document d.

`V_1(d) = {v ∈ dom(M(d)) : subspace(v) = 1}` — the set of V-positions in the text subspace of document d.

---

## Definition — OriginFunction

For every `a ∈ dom(Σ.C)`:

`origin(a) = N(a).0.U(a).0.D(a)`

— the document-level prefix obtained by truncating the element field; a tumbler satisfying `zeros(origin(a)) = 2`. The projections `N(a)`, `U(a)`, `D(a)` are supplied by T4b (UniqueParse, ASN-0034).

---

## Definition — CorrespondenceRun

A *correspondence run* is a triple `(v, a, n)` — a V-position, an I-address, and a natural number `n ≥ 1` — such that the arrangement preserves ordinal displacement within the run:

`(A k : 0 ≤ k < n : Σ.M(d)(shift(v, k)) = shift(a, k))`

At `k = 0` this is the base case `M(d)(v) = a`. Each subsequent `k` increments both the V-ordinal and the I-ordinal by the same amount.

---

## Σ.C — ContentStore (DEF, state-component)

`Σ.C : T ⇀ Val` — the content store is a partial function from tumblers to content values. `T` is the set of tumblers (ASN-0034); `Val` is an unspecified set of content values, opaque at this level of abstraction.

`dom(Σ.C) = {a ∈ T : Σ.C(a) is defined}` — the set of I-addresses at which content has been stored.

---

## Σ.M(d) — Arrangement (DEF, state-component)

`Σ.M(d) : T ⇀ T` — the arrangement of document `d` is a partial function from V-position tumblers to I-address tumblers.

`dom(Σ.M(d)) = {v ∈ T : Σ.M(d)(v) is defined}` — the set of V-positions currently active in `d`.

`ran(Σ.M(d)) = {Σ.M(d)(v) : v ∈ dom(Σ.M(d))}` — the set of I-addresses that `d` currently references.

---

## S0 — ContentImmutability (AX, axiom)

For every state transition `Σ → Σ'`:

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)]`

Equivalently: `(A a : a ∈ dom(Σ.C) : a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))`.

Postconditions: (a) Domain persistence — `a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)`. (b) Value preservation — `a ∈ dom(Σ.C) ⟹ Σ'.C(a) = Σ.C(a)`.

Frame: No condition on arrangements — the postcondition holds for arbitrary `Σ'.M(d)` and arbitrary changes to any document's arrangement.

---

## S1 — StoreMonotonicity (LEMMA, lemma)

For every state transition `Σ → Σ'`:

`[dom(Σ.C) ⊆ dom(Σ'.C)]`

Preconditions: State transition `Σ → Σ'` in a system satisfying S0 (content immutability).

Postconditions: `dom(Σ.C) ⊆ dom(Σ'.C)`.

---

## S2 — ArrangementFunctionality (AX, axiom)

For each document `d`, `Σ.M(d)` is a function — each V-position maps to exactly one I-address:

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) is uniquely determined)`

Equivalently: `(A d, v, a₁, a₂ : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a₁ ∧ Σ.M(d)(v) = a₂ : a₁ = a₂)`.

Postconditions: For each `v ∈ dom(Σ.M(d))`, the image `Σ.M(d)(v)` is uniquely determined.

Frame: Distinct V-positions may map to the same I-address (sharing — S5); injectivity is *not* asserted.

---

## S3 — ReferentialIntegrity (AX, invariant)

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`

Equivalently: `ran(Σ.M(d)) ⊆ dom(Σ.C)`.

Preservation across transitions: For an operation that adds a V-mapping `M(d)(v) = a`, `wp(op, S3) ⟹ a ∈ dom(Σ'.C)` — the I-address must exist in the post-state.

Frame: S3 is one-directional — content may exist in `dom(C)` without being referenced; existence does not entail arrangement.

Depends: S1 (store monotonicity) — once a reference is valid, S1 prevents the target from being removed.

---

## S4 — OriginBasedIdentity (THM, theorem)

For I-addresses `a₁`, `a₂` produced by distinct allocation events:

`a₁ ≠ a₂`

regardless of whether `Σ.C(a₁) = Σ.C(a₂)`.

Preconditions: `a₁, a₂ ∈ dom(Σ.C)` produced by distinct allocation events within a system conforming to T10a (allocator discipline, ASN-0034).

Postconditions: `a₁ ≠ a₂`, regardless of whether `Σ.C(a₁) = Σ.C(a₂)`.

Frame: The content store `C` and value domain `Val` play no role in the proof — distinctness is a property of the addressing scheme alone.

---

## S5 — UnrestrictedSharing (THM, theorem)

The same I-address may appear in the ranges of multiple arrangements, and at multiple V-positions within a single arrangement. S0–S3 are consistent with any finite sharing multiplicity — they place no constraint on `|{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}|`:

`(A N ∈ ℕ :: (E Σ :: Σ satisfies S0–S3 ∧ (E a ∈ dom(Σ.C) :: |{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N)))`

Preconditions: `N ∈ ℕ` arbitrary.

Postconditions: There exists a state `Σ` satisfying S0, S1, S2, and S3 such that for some `a ∈ dom(Σ.C)`, `|{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N`. The construction works both across documents (multiplicity `N + 1` over `N + 1` documents) and within a single document (multiplicity `N + 1` at `N + 1` distinct V-positions).

---

## S6 — PersistenceIndependence (THM, theorem)

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)]`

regardless of any changes to any `Σ.M(d)`.

Preconditions: `a ∈ dom(Σ.C)` and state transition `Σ → Σ'` in a system satisfying S0 (content immutability).

Postconditions: `a ∈ dom(Σ'.C)`, with no condition on the arrangement functions `Σ.M(d)` or `Σ'.M(d)` for any document `d`.

Frame: The arrangement functions `M(d)` are unconstrained — S6 holds for all possible values of `Σ'.M(d)`, including `Σ'.M(d) = ∅`.

---

## S7a — DocumentScopedAllocation (AX, axiom)

`(A a : a ∈ dom(Σ.C) ∧ zeros(a) ≥ 2 :: the document-level prefix N(a).0.U(a).0.D(a) is the tumbler of the document whose owner performed the allocation that placed a into dom(C))`

The conditioning `zeros(a) ≥ 2` is the well-formedness premise under which T4b's projections `N(a)`, `U(a)`, `D(a)` are defined.

Depends: T4 (HierarchicalParsing, ASN-0034); T4b (UniqueParse, ASN-0034); S7b — universally discharges S7a's `zeros(a) ≥ 2` conditioning by supplying the strictly stronger `zeros(a) = 3 ≥ 2` for every `a ∈ dom(Σ.C)`; T10a (AllocatorDiscipline, ASN-0034); T10a.4 (T4PreservationUnderDiscipline, ASN-0034); S0 (content immutability).

---

## S7b — ElementLevelIAddresses (AX, axiom)

`(A a ∈ dom(Σ.C) :: zeros(a) = 3)`

Postconditions: By T4's field correspondence, all four identifying fields — node, user, document, element — are present and the element field exists. The projections `N(a)`, `U(a)`, `D(a)`, `E(a)` supplied by T4b are all well-defined.

Depends: T4 (HierarchicalParsing, ASN-0034); T4b (UniqueParse, ASN-0034); T10a.4 (T4PreservationUnderDiscipline, ASN-0034); S0 (content immutability).

---

## S7c — ElementFieldDepth (AX, axiom)

`(A a ∈ dom(Σ.C) :: #E(a) ≥ 2)`

where `E(a)` is the element-field projection supplied by T4b (UniqueParse, ASN-0034).

When S7c holds, the *I-address subspace identifier* is named:

`subspace_I(a) = E(a)₁`

Postconditions: (a) `subspace_I(a)` and the content ordinal `[E(a)₂, ..., E(a)_δ]` occupy distinct components. (b) For any `k ≥ 1`, the displacement `δ(k, #a)` has action point `#a`, which falls strictly after the position of `subspace_I(a)` in the full address — so `shift(a, k)` preserves `subspace_I(a)` by TumblerAdd's prefix rule. (c) The within-subspace ordinal `[E(a)₂, ..., E(a)_δ]` is a non-empty tumbler in `S` satisfying TA7a's operand precondition `o ∈ S`.

Depends: S7b; T4b (UniqueParse, ASN-0034); TA7a (ASN-0034); T10a.4 (T4PreservationUnderDiscipline, ASN-0034); S0 (content immutability).

---

## S7d — DocumentAllocationDiscipline (AX, axiom)

Every document tumbler `d` satisfies `zeros(d) = 2` and is the result of an allocation event under T10a; distinct documents arise from distinct allocation events.

Postconditions: By GlobalUniqueness (ASN-0034), distinct documents have distinct document-level tumblers.

Depends: T10a (AllocatorDiscipline, ASN-0034); T10a.4 (T4PreservationUnderDiscipline, ASN-0034); T4 (HierarchicalParsing, ASN-0034); GlobalUniqueness (ASN-0034).

---

## subspace_I(a) — IAddressSubspaceIdentifier (DEF, function)

`subspace_I(a) = E(a)₁`

Signature: `subspace_I : T → ℕ` — projects the first component of the element field of an I-address.

Preconditions: `a ∈ dom(Σ.C)` (so S7b's `zeros(a) = 3` holds, making T4b's element-field projection `E(a)` well-defined); S7c's `#E(a) ≥ 2` (so that `E(a)₁` is well-defined as the first component of a non-empty element field).

Postconditions: (a) `subspace_I(a) ∈ ℕ`. (b) `subspace_I(a) ≥ 1`. (c) *Subspace preservation under shift:* for `k ≥ 1`, `subspace_I(shift(a, k)) = subspace_I(a)`.

Depends: T0 (ASN-0034); T4b (UniqueParse, ASN-0034); T4 (HierarchicalParsing, ASN-0034); T10a.4 (T4PreservationUnderDiscipline, ASN-0034); S7b; S7c.

---

## S7 — StructuralAttribution (THM, theorem)

For every `a ∈ dom(Σ.C)`, define the *origin* as the document-level prefix obtained by truncating the element field:

`origin(a) = N(a).0.U(a).0.D(a)`

Preconditions: `a ∈ dom(Σ.C)` in a system conforming to S7a, S7b, S7d, T4 (HierarchicalParsing, ASN-0034), T4b (UniqueParse, ASN-0034), T10a (ASN-0034), and T10a.4 (T4PreservationUnderDiscipline, ASN-0034).

Postconditions: (a) `origin(a)` is well-defined and is a document-level tumbler with `zeros(origin(a)) = 2`. (b) `origin(a)` is the tumbler of the document that allocated `a`. (c) For `a₁, a₂` allocated under distinct documents, `origin(a₁) ≠ origin(a₂)`. (d) `origin(a)` is invariant across all states in which `a ∈ dom(Σ.C)`.

Frame: The content values `Σ.C(a)` and arrangement functions `Σ.M(d)` play no role — attribution is a property of the addressing scheme alone.

---

## S8-fin — FiniteArrangement (AX, axiom)

For every state `Σ` and document `d`, `dom(Σ.M(d))` is a finite set.

Postconditions: `|dom(Σ.M(d))| < ∞` — the arrangement has finite cardinality. Consequently `ran(Σ.M(d))` is finite (image of a finite set under a function).

Frame: No constraint on the unbounded growth of `dom(C)`; only individual arrangements are required to be finite at any given state.

---

## S8a — VPositionWellFormedness (AX, axiom)

`(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))`

Postconditions: `(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))`.

Depends: T0 (ASN-0034) — supplies the ℕ-valued component carrier; T4 (HierarchicalParsing, ASN-0034); NAT-zero (NatZeroMinimum, ASN-0034) — from `vᵢ ∈ ℕ` and `vᵢ ≠ 0` (delivered by `zeros(v) = 0`), NAT-zero concludes `vᵢ > 0`.

---

## S8-depth — FixedDepthVPositions (AX, axiom)

`(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`

Equivalently (using `subspace`): `(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ subspace(v₁) = subspace(v₂) : #v₁ = #v₂)`.

Postconditions: Within a subspace `s` of document `d`, there exists a common depth `m_s ≥ 2` (by S8a) such that every V-position with `v₁ = s` has length `m_s`. Distinct subspaces may have distinct depths.

Depends: S8a — for the lower bound `m_s ≥ 2`.

---

## S8 — SpanDecomposition (THM, theorem)

For each document `d`, the arrangement `{(v, Σ.M(d)(v)) : v ∈ dom(Σ.M(d))}` can be decomposed into a finite set of correspondence runs `{(vⱼ, aⱼ, nⱼ)}` such that:

(a) The runs partition the V-positions: `(A v ∈ dom(Σ.M(d)) :: (E! j :: vⱼ ≤ v < shift(vⱼ, nⱼ)))`

(b) Within each run: `Σ.M(d)(shift(vⱼ, k)) = shift(aⱼ, k)` for all `k` with `0 ≤ k < nⱼ`

**Auxiliary lemma (subspace and field-structure preservation across a correspondence run).** For any correspondence run `(vⱼ, aⱼ, nⱼ)` satisfying conjunct (b), every image `shift(aⱼ, k)` with `0 ≤ k < nⱼ` preserves three structural properties of `aⱼ`:

(i) `subspace_I(shift(aⱼ, k)) = subspace_I(aⱼ)`

(ii) `zeros(shift(aⱼ, k)) = zeros(aⱼ) = 3` — so `shift(aⱼ, k)` remains an element-level I-address (S7b inherited)

(iii) `#E(shift(aⱼ, k)) = #E(aⱼ) = δⱼ ≥ 2` — preserving S7c's depth bound

Preconditions: `dom(M(d))` finite (S8-fin); `M(d)` a function (S2); referential integrity (S3); `(A v ∈ dom(M(d)) :: zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))` (S8a); within each subspace, all V-positions share a common depth (S8-depth); I-addresses are element-level with `zeros(a) = 3` (S7b). S7c is a precondition of the auxiliary lemma only (load-bearing for coarser decompositions with run lengths `nⱼ ≥ 2`).

---

## ord(v) — OrdinalExtraction (DEF, function)

`ord(v) = [v₂, ..., vₘ]`

— the tumbler of length `m − 1` obtained by stripping the subspace identifier, where `m = #v`.

Preconditions: `v ∈ T`, `#v ≥ 2`.

Postconditions: `ord(v) ∈ T` (length `m - 1 ≥ 1`). `#ord(v) = #v - 1`. When `v` satisfies S8a, `ord(v) ∈ S` — every component of `[v₂, ..., vₘ]` is positive since every component of `v` is positive by S8a's componentwise positivity conjunct `(A i : 1 ≤ i ≤ #v : vᵢ > 0)`.

Depends: T0 (ℕ-valued carrier, ASN-0034); TA7a (ordinal-only formulation, ASN-0034) — defines the codomain S; S8a — for the S-membership postcondition.

---

## vpos(S, o) — VPositionReconstruction (DEF, function)

`vpos(S, o) = [S, o₁, ..., oₖ]`

with `#vpos(S, o) = k + 1`, where `k = #o`.

Preconditions: `S ∈ ℕ`, `o ∈ T`, `#o ≥ 1`.

Postconditions: `vpos(S, o) ∈ T`, `#vpos(S, o) = #o + 1`, `vpos(S, o)₁ = S`.

(a) `ord(vpos(S, o)) = o` — since `vpos(S, o) = [S, o₁, ..., oₖ]`, stripping the first component recovers `[o₁, ..., oₖ] = o`.

(b) For any `v ∈ T` with `#v ≥ 2`: `vpos(subspace(v), ord(v)) = v` — since `subspace(v) = v₁` and `ord(v) = [v₂, ..., vₘ]`, reconstruction gives `[v₁, v₂, ..., vₘ] = v`.

When `S ≥ 1` and `(A i : 1 ≤ i ≤ #o : oᵢ > 0)`, the result satisfies S8a: `zeros(vpos(S, o)) = 0`, `#vpos(S, o) = k + 1 ≥ 2`, and `(A i : 1 ≤ i ≤ #vpos(S, o) : vpos(S, o)ᵢ > 0)`.

Depends: T0 (ℕ-valued carrier, ASN-0034); ord (definition above); S8a — for the satisfies-S8a postcondition.

---

## w_ord — OrdinalDisplacementProjection (DEF, function)

For a displacement `w` with `w₁ = 0` and `#w = m ≥ 2`:

`w_ord = [w₂, ..., wₘ]`

of length `m − 1`.

Preconditions: `w ∈ T`, `#w ≥ 2`, `w₁ = 0`.

Postconditions: `w_ord ∈ T` (length `m - 1 ≥ 1`). `#w_ord = #w - 1`. When `Pos(w)` (TA-Pos, ASN-0034), `Pos(w_ord)` — since `w₁ = 0`, the witness `wᵢ ≠ 0` required by `Pos(w)` must have `i ≥ 2`, and this component appears in `w_ord`. When `Pos(w)`: `actionPoint(w_ord) = actionPoint(w) - 1`.

Depends: T0 (ℕ-valued carrier, ASN-0034); TumblerAdd (ASN-0034) — for the `actionPoint` relationship.

---

## OrdAddHom — OrdinalAdditionHomomorphism (LEMMA, lemma)

For a V-position `v` with `#v = m ≥ 2`, and a displacement `w` with `w₁ = 0`, `#w = m`, and `Pos(w)` (TA-Pos, ASN-0034):

`ord(v ⊕ w) = ord(v) ⊕ w_ord`

Preconditions: `v ∈ T`, `#v = m ≥ 2`; `w ∈ T`, `Pos(w)` (TA-Pos, ASN-0034), `#w = m`, `w₁ = 0`.

Postconditions:
(a) `ord(v ⊕ w) = ord(v) ⊕ w_ord`
(b) `subspace(v ⊕ w) = subspace(v)`
(c) `v ⊕ w = vpos(subspace(v), ord(v) ⊕ w_ord)`

Depends: ord, w_ord, vpos (definitions above); TumblerAdd (PositionAdvance, ASN-0034) — the three-region component formula; TA0 (length preservation, ASN-0034); ActionPoint (ASN-0034).

---

## OrdAddS8a — AdditionPreservesS8a (LEMMA, lemma)

For a V-position `v` satisfying S8a with `#v = m ≥ 2`, and a displacement `w` with `w₁ = 0`, `#w = m`, `Pos(w)` (TA-Pos, ASN-0034):

`v ⊕ w satisfies S8a ⟺ (A i : actionPoint(w) < i ≤ m : wᵢ > 0)`

Equivalently: `ord(v ⊕ w) ∈ S ⟺ v ⊕ w satisfies S8a`

Preconditions: `v ∈ T` satisfying S8a, `#v = m ≥ 2`; `w ∈ T`, `Pos(w)` (TA-Pos, ASN-0034), `#w = m`, `w₁ = 0`.

Postconditions: `v ⊕ w satisfies S8a ⟺ (A i : actionPoint(w) < i ≤ m : wᵢ > 0)`. Equivalently, `ord(v ⊕ w) ∈ S ⟺ v ⊕ w satisfies S8a`.

Depends: OrdAddHom; TumblerAdd (PositionAdvance, ASN-0034); ActionPoint (ASN-0034); S8a; NAT-addcompat (NatAdditionOrderAndSuccessor, ASN-0034); NAT-order (NatStrictTotalOrder, ASN-0034).

---

## OrdShiftHom — OrdinalShiftHomomorphism (COROLLARY, corollary)

For a V-position `v` with `#v = m ≥ 2` and `n ≥ 1`:

`ord(shift(v, n)) = shift(ord(v), n)`

Preconditions: `v ∈ T`, `#v = m ≥ 2`, `n ≥ 1`.

Postconditions:
(a) `ord(shift(v, n)) = shift(ord(v), n)`
(b) `subspace(shift(v, n)) = subspace(v)` — derived from OrdAddHom (b) at `w = δ(n, m)`, whose `w₁ = 0` holds because `#δ(n, m) = m ≥ 2`
(c) When `v` satisfies S8a, `shift(v, n)` satisfies S8a unconditionally — since `δ(n, m) = [0, ..., 0, n]` has action point `m` with no tail components beyond, the OrdAddS8a condition is vacuously satisfied

Depends: OrdAddHom, OrdAddS8a, OrdinalShift (ASN-0034), OrdinalDisplacement (ASN-0034).

---

## D-CTG — VContiguity (AX, axiom)

For each document d, `V_1(d)` (the text subspace) is either empty or occupies every intermediate position between its extremes:

`(A d, u, q : u ∈ V_1(d) ∧ q ∈ V_1(d) ∧ u < q : (A v : subspace(v) = 1 ∧ #v = #u ∧ u < v < q : v ∈ V_1(d)))`

Preconditions: `subspace(v) = 1` (text subspace); V-positions share a common depth (S8-depth).

Postconditions: V_1(d) is either empty or occupies every position strictly between its extremes (at the fixed text-subspace depth).

Frame: The link subspace `V_2(d)` is exempt — sparse with tombstones is permitted. D-CTG is a constraint on well-formed text-subspace arrangements; preservation across editing operations is each operation's verification obligation.

Depends: S8a; S8-depth; T1 (TumblerOrdering, ASN-0034).

---

## D-MIN — VMinimumPosition (AX, axiom)

For each document d with `V_1(d)` non-empty:

`min(V_1(d)) = [1, 1, ..., 1]`

where the tuple has length `m` (the common depth of V-positions in the text subspace per S8-depth), and every component is 1.

Preconditions: V_1(d) non-empty; common text-subspace depth `m_1` (S8-depth) with `m_1 ≥ 2` (S8a).

Postconditions: Every component of `min(V_1(d))` equals 1; in particular the text subspace identifier `min(V_1(d))₁ = 1` and the within-subspace ordinal starts at the minimum positive value.

Frame: The link subspace `V_2(d)` is exempt.

Depends: S8a, S8-depth, T1 (TumblerOrdering, ASN-0034).

---

## D-CTG-depth — SharedPrefixReduction (LEMMA, corollary)

At depth `m ≥ 3`, all positions in a non-empty `V_1(d)` share components 2 through `m − 1`. Contiguity reduces to contiguity of the last component alone:

`(A v₁, v₂ ∈ V_1(d), j : 2 ≤ j ≤ m − 1 : (v₁)ⱼ = (v₂)ⱼ)`

Preconditions: V_1(d) non-empty; common depth `m` within the text subspace (S8-depth); `m ≥ 3` (the lemma's non-triviality bound — at `m = 2` the conclusion holds vacuously since the range of shared components 2 through `m − 1` is empty).

Postconditions: `(A v₁, v₂ ∈ V_1(d), j : 2 ≤ j ≤ m − 1 : (v₁)ⱼ = (v₂)ⱼ)`. Contiguity of V_1(d) reduces to contiguity of the m-th (last) component.

Depends: D-CTG; S8a; S8-depth; S8-fin; T0(a) (UnboundedComponentValues, ASN-0034); T1 case (i) (TumblerOrdering, ASN-0034); T3 (CanonicalRepresentation, ASN-0034); NAT-closure, NAT-cancel, NAT-addcompat, NAT-order, NAT-zero (ASN-0034).

---

## D-SEQ — SequentialPositions (THM, theorem)

For each document d, if `V_1(d)` is non-empty, then there exists `n ≥ 1` such that:

`V_1(d) = {[1, 1, ..., 1, k] : 1 ≤ k ≤ n}`

where the tuple has length `m`, the common V-position depth in the text subspace (S8-depth). By S8a, every V-position has depth `≥ 2`, so `m ≥ 2`.

Preconditions: V_1(d) non-empty; common V-position depth m (S8-depth), with `m ≥ 2` inherited from S8a.

Postconditions: `(E n : n ≥ 1 : V_1(d) = {[1, 1, ..., 1, k] : 1 ≤ k ≤ n})` where each tuple has length m.

Depends: D-CTG; D-CTG-depth; D-MIN; S8a; S8-fin; S8-depth; T1 case (i) (TumblerOrdering, ASN-0034).

---

## ValidInsertionPosition — ValidInsertionPosition (DEF, predicate)

**Non-empty case (binary predicate).** For a document `d` with `V_1(d) ≠ ∅`:

`ValidInsertionPosition(d, v)` holds iff, writing `N = |V_1(d)|`, `v = shift(min(V_1(d)), j)` for some `j ∈ {0, 1, ..., N}` (with `shift(·, 0) = identity`).

The common V-position depth `m` is determined by `d` via S8-depth and read from state — it is *not* a parameter of the predicate. By S8a, `m ≥ 2`.

Preconditions: Document `d` with `V_1(d) ⊆ dom(M(d))` non-empty; D-CTG holds on V_1(d); `m ≥ 2` is the common depth of V_1(d) by S8-depth and S8a.

Postconditions: (a) `subspace(v) = 1` and `#v = m` (the state-fixed common depth). (b) `v` satisfies S8a: `zeros(v) = 0` and all components positive. (c) For fixed `d`, exactly `N + 1` values of `v` satisfy the predicate. (d) The explicit form is `v = [1, 1, ..., 1 + j]` with last component `1 + j` and all preceding components equal to 1.

Depends: D-MIN, D-CTG, D-CTG-depth, D-SEQ; S8a, S8-fin, S8-depth; OrdinalShift, TumblerAdd, T3 (ASN-0034).

---

## ValidFirstInsertionPosition — ValidFirstInsertionPosition (DEF, predicate)

**Empty case (ternary predicate).** For a document `d` with `V_1(d) = ∅`:

`ValidFirstInsertionPosition(d, v, m)` holds iff `m ∈ ℕ` with `m ≥ 2` and `v = [1, 1, ..., 1]` of depth `m`.

`m` is an operational input chosen by the placing operation; the strand model fixes only the lower bound `m ≥ 2`.

Preconditions: Document `d` with `V_1(d) = ∅`; `m ∈ ℕ` with `m ≥ 2`.

Postconditions: (a) `subspace(v) = 1` and `#v = m`. (b) `v` satisfies S8a: `zeros(v) = 0` and all components positive. (c) For fixed `d` and `m`, exactly one value of `v` satisfies the predicate. (d) Once the position is placed, S8-depth fixes the depth at `m` for all subsequent positions in the text subspace, after which validity of further insertion positions is governed by `ValidInsertionPosition(d, v)`.

Frame: The specific value of `m` is set by the placing operation, *not* by the strand model.

Depends: D-MIN; S8a, S8-depth; OrdinalShift, TumblerAdd, T3 (ASN-0034).

---

## S9 — TwoStreamSeparation (THM, theorem)

No modification to any arrangement `Σ.M(d)` can alter the content store `Σ.C`:

`[Σ'.M(d) ≠ Σ.M(d) ⟹ (A a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))]`

Preconditions: State transition `Σ → Σ'` such that `Σ'.M(d) ≠ Σ.M(d)` for some document `d` (an arrangement-modifying transition); system satisfies S0 (content immutability).

Postconditions: `(A a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))` — every content entry persists with its value across the transition.

Frame: The arrangement modification may be arbitrary (insertion, deletion, rearrangement, or any combination); S9 holds regardless of the specific transformation applied to `Σ.M(d)`.

Depends: S0 (content immutability) — supplies the universal guarantee that S9 specialises to arrangement-modifying transitions.
