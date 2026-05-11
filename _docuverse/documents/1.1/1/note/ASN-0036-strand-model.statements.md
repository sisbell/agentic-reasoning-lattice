# ASN-0036 Claim Statements

*Source: ASN-0036-strand-model.md (revised 2026-04-11) — Extracted: 2026-05-11*

## Σ.C — ContentStore (DEF, function)

`Σ.C : T ⇀ Val` — the content store is a partial function from tumblers to content values.

- `dom(Σ.C) = {a ∈ T : Σ.C(a) is defined}` — the set of I-addresses at which content has been stored.

`T` is the set of tumblers (ASN-0034); `Val` is an unspecified set of content values, opaque at this level of abstraction.

## Σ.M(d) — Arrangement (DEF, function)

`Σ.M(d) : T ⇀ T` — the arrangement of document `d` is a partial function from V-position tumblers to I-address tumblers.

- `dom(Σ.M(d)) = {v ∈ T : Σ.M(d)(v) is defined}` — the set of V-positions currently active in `d`.
- `ran(Σ.M(d)) = {Σ.M(d)(v) : v ∈ dom(Σ.M(d))}` — the set of I-addresses that `d` currently references.

## S0 — ContentImmutability (AXM, axiom)

For every state transition `Σ → Σ'`:

`(A a : a ∈ dom(Σ.C) : a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))`

- Postcondition (a) Domain persistence: `a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)`
- Postcondition (b) Value preservation: `a ∈ dom(Σ.C) ⟹ Σ'.C(a) = Σ.C(a)`
- Frame: No condition on arrangements — the postcondition holds for arbitrary `Σ'.M(d)` and arbitrary changes to any document's arrangement.

## S1 — StoreMonotonicity (THM, lemma)

- Preconditions: State transition `Σ → Σ'` in a system satisfying S0 (content immutability).
- Postconditions: `dom(Σ.C) ⊆ dom(Σ'.C)`

## S2 — ArrangementFunctionality (AXM, predicate)

`Σ.M(d) : T ⇀ T` is a (partial) function:

`(A d, v, a₁, a₂ : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a₁ ∧ Σ.M(d)(v) = a₂ : a₁ = a₂)`

- Postconditions: For each `v ∈ dom(Σ.M(d))`, the image `Σ.M(d)(v)` is uniquely determined.
- Frame: Distinct V-positions may map to the same I-address (sharing — S5); injectivity is *not* asserted.

## S3 — ReferentialIntegrity (AXM, predicate)

In every state `Σ`:

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`

Equivalently: `ran(Σ.M(d)) ⊆ dom(Σ.C)`

- Preservation across transitions: For an operation that adds a V-mapping `M(d)(v) = a`, `wp(op, S3) ⟹ a ∈ dom(Σ'.C)` — the I-address must exist in the post-state.
- Frame: S3 is one-directional — content may exist in `dom(C)` without being referenced; existence does not entail arrangement.
- Depends: S1 (store monotonicity) — once a reference is valid, S1 prevents the target from being removed.

## S4 — OriginBasedIdentity (THM, lemma)

- Preconditions: `a₁, a₂ ∈ dom(Σ.C)` produced by distinct allocation events within a system conforming to T10a (allocator discipline, ASN-0034).
- Postconditions: `a₁ ≠ a₂`, regardless of whether `Σ.C(a₁) = Σ.C(a₂)`.
- Frame: The content store `C` and value domain `Val` play no role in the proof — distinctness is a property of the addressing scheme alone.

## S5 — UnrestrictedSharing (THM, lemma)

`(A N ∈ ℕ :: (E Σ :: Σ satisfies S0–S3 ∧ (E a ∈ dom(Σ.C) :: |{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N)))`

- Preconditions: `N ∈ ℕ` arbitrary.
- Postconditions: There exists a state `Σ` satisfying S0 (content immutability), S1 (store monotonicity), S2 (arrangement functionality), and S3 (referential integrity) such that for some `a ∈ dom(Σ.C)`, `|{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N`. The construction works both across documents (multiplicity `N + 1` over `N + 1` documents) and within a single document (multiplicity `N + 1` at `N + 1` distinct V-positions).

## S7a — DocumentScopedAllocation (AXM, axiom)

`(A a : a ∈ dom(Σ.C) ∧ zeros(a) ≥ 2 :: the document-level prefix N(a).0.U(a).0.D(a) is the tumbler of the document whose owner performed the allocation that placed a into dom(C))`

The conditioning `zeros(a) ≥ 2` is the well-formedness premise under which T4b's projections `N(a)`, `U(a)`, `D(a)` are defined; S7b strengthens the conclusion to hold for every `a ∈ dom(Σ.C)` by discharging the conditioning universally.

## S7b — ElementLevelIAddresses (AXM, axiom)

`(A a ∈ dom(Σ.C) :: zeros(a) = 3)`

- Postconditions: By T4's field correspondence, all four identifying fields — node, user, document, element — are present and the element field exists. The projections `N(a)`, `U(a)`, `D(a)`, `E(a)` supplied by T4b are all well-defined.

## S7c — ElementFieldDepth (AXM, axiom)

`(A a ∈ dom(Σ.C) :: #E(a) ≥ 2)`

where `E(a)` is the element-field projection supplied by T4b (UniqueParse, ASN-0034). When S7c holds, the first component of the element field is named:

`subspace_I(a) = E(a)₁`

- Consequence (a) — subspace-ordinal separation: `subspace_I(a) = E(a)₁` and the content ordinal `[E(a)₂, ..., E(a)_δ]` occupy distinct components of `E(a)`. *Derivation:* By S7b, `zeros(a) = 3`, so T4b's element-field projection `E(a)` is well-defined as a finite sequence of components. The axiom `#E(a) ≥ 2` gives the element field at least two components — `E(a)₁` and `E(a)₂` are therefore distinct positions. The content ordinal `[E(a)₂, ..., E(a)_δ]` begins at position 2 within `E(a)` and so does not overlap `E(a)₁` at position 1.
- Consequence (b) — shift action-point separation: For any `k ≥ 1`, `subspace_I(shift(a, k)) = subspace_I(a)`. This conclusion is established in full by ShiftPreservation conclusion (iv).
- Consequence (c) — TA7a operand membership: The within-subspace ordinal `[E(a)₂, ..., E(a)_δ]` is a non-empty tumbler in `S` — non-empty by S7c's own axiom `#E(a) ≥ 2`, and componentwise positive by T4's positive-component constraint on present fields — satisfying TA7a's operand precondition `o ∈ S` so that `⊕` and `⊖` are directly applicable.

## S7d — DocumentAllocationDiscipline (AXM, axiom)

Every document tumbler `d` satisfies `zeros(d) = 2` and is the result of an allocation event under T10a; distinct documents arise from distinct allocation events.

- Postconditions: By GlobalUniqueness (ASN-0034), distinct documents have distinct document-level tumblers — the cross-document uniqueness premise for S7's identification argument.

## subspace_I(a) — SubspaceI (DEF, function)

- Signature: `subspace_I : T → ℕ` — projects the first component of the element field of an I-address.
- Preconditions: `a ∈ dom(Σ.C)` (so S7b's `zeros(a) = 3` holds, making T4b's element-field projection `E(a)` well-defined); S7c's `#E(a) ≥ 2` (so that `E(a)₁` is well-defined as the first component of a non-empty element field).
- Definition: `subspace_I(a) = E(a)₁`
- Postconditions:
  - (a) `subspace_I(a) ∈ ℕ`
  - (b) `subspace_I(a) ≥ 1`
  - (c) Subspace preservation under shift: for `k ≥ 1`, `subspace_I(shift(a, k)) = subspace_I(a)`. This is ShiftPreservation conclusion (iv).

## ShiftPreservation — ShiftPreservation (LEMMA, lemma)

For any `a ∈ dom(Σ.C)` and any `k ≥ 1`, the shift `shift(a, k) = a ⊕ δ(k, #a)` preserves the structural properties of `a`:

(i) `zeros(shift(a, k)) = 3`
(ii) `shift(a, k)` is T4-valid — all four T4 conjuncts (zero-count bound, no adjacent zeros, positive endpoint components) hold
(iii) `#E(shift(a, k)) = #E(a)`
(iv) `subspace_I(shift(a, k)) = subspace_I(a)`

- Preconditions: `a ∈ dom(Σ.C)` (so S7b's `zeros(a) = 3` and S7c's `#E(a) ≥ 2` hold; T10a.4 supplies T4-validity of `a`); `k ∈ ℕ` with `k ≥ 1`.
- Postconditions: (i) `zeros(shift(a, k)) = 3`. (ii) `shift(a, k)` is T4-valid. (iii) `#E(shift(a, k)) = #E(a)`. (iv) `subspace_I(shift(a, k)) = subspace_I(a)`.
- Frame: The lemma operates on `a` and `k` alone — no state is consulted beyond the membership `a ∈ dom(Σ.C)` used to discharge S7b and S7c.

## S7 — StructuralAttribution (THM, lemma)

For every `a ∈ dom(Σ.C)`, define the *origin* as the document-level prefix obtained by truncating the element field:

`origin(a) = N(a).0.U(a).0.D(a)`

- Preconditions: `a ∈ dom(Σ.C)` in a system conforming to S7a (document-scoped allocation), S7b (element-level I-addresses), S7d (document allocation discipline), T4 (HierarchicalParsing, ASN-0034), T4b (UniqueParse, ASN-0034), T10a (allocator discipline, ASN-0034), and T10a.4 (T4PreservationUnderDiscipline, ASN-0034).
- Postconditions:
  - (a) `origin(a)` is well-defined and is a document-level tumbler with `zeros(origin(a)) = 2`.
  - (b) `origin(a)` is the tumbler of the document that allocated `a`.
  - (c) For `a₁, a₂` allocated under distinct documents, `origin(a₁) ≠ origin(a₂)`.
  - (d) `origin(a)` is invariant across all states in which `a ∈ dom(Σ.C)`.
- Frame: The content values `Σ.C(a)` and arrangement functions `Σ.M(d)` play no role — attribution is a property of the addressing scheme alone.

## S8-fin — FiniteArrangement (AXM, axiom)

For every state `Σ` and document `d`, `dom(Σ.M(d))` is a finite set.

- Postconditions: `|dom(Σ.M(d))| < ∞` — the arrangement has finite cardinality. Consequently `ran(Σ.M(d))` is finite (image of a finite set under a function).
- Frame: No constraint on the unbounded growth of `dom(C)`; only individual arrangements are required to be finite at any given state.

## S8a — VPositionWellFormedness (AXM, predicate)

`(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))`

- Postconditions: `dom(M(d)) ⊆ {t ∈ T : zeros(t) = 0 ∧ #t ≥ 2 ∧ (A i : tᵢ > 0)}` (element-field tumblers of depth at least 2); `ran(M(d)) ⊆ {t ∈ T : zeros(t) = 3}` (full element-level addresses, per S7b). As a specialisation, `v₁ ≥ 1` holds — the subspace identifier is always a positive natural number.

## subspace(v) — Subspace (DEF, function)

- Signature: `subspace : T → ℕ` — projects the first component of a tumbler.
- Preconditions: `v ∈ T`, `#v ≥ 1` (so that `v₁` is well-defined as the first component of a non-empty tumbler).
- Definition: `subspace(v) = v₁`
- Postconditions:
  - (a) `subspace(v) ∈ ℕ`
  - (b) When `v` satisfies S8a, `subspace(v) ≥ 1`
  - (c) Subspace preservation under shift: for `#v = m ≥ 2` and `n ≥ 1`, `subspace(shift(v, n)) = subspace(v)` — established by OrdShiftHom (b).

## S8-depth — FixedDepthVPositions (AXM, axiom)

`(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ subspace(v₁) = subspace(v₂) : #v₁ = #v₂)`

- Postconditions: Within a subspace `s` of document `d`, there exists a common depth `m_s ≥ 2` (by S8a) such that every V-position with `v₁ = s` has length `m_s`. Distinct subspaces may have distinct depths.

## S8 — SpanDecomposition (THM, lemma)

A *correspondence run* is a triple `(v, a, n)` — a V-position, an I-address, and a natural number `n ≥ 1` — such that:

`(A k : 0 ≤ k < n : Σ.M(d)(shift(v, k)) = shift(a, k))`

For each document `d`, the arrangement `{(v, Σ.M(d)(v)) : v ∈ dom(Σ.M(d))}` can be decomposed into a finite set of correspondence runs `{(vⱼ, aⱼ, nⱼ)}` such that:

(a) `(A v ∈ dom(Σ.M(d)) :: (E! j :: vⱼ ≤ v < shift(vⱼ, nⱼ)))`

(b) `Σ.M(d)(shift(vⱼ, k)) = shift(aⱼ, k)` for all `k` with `0 ≤ k < nⱼ`

- Preconditions: `dom(M(d))` finite (S8-fin); `M(d)` a function (S2); referential integrity (S3); `(A v ∈ dom(M(d)) :: zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))` (S8a); within each subspace, all V-positions share a common depth (S8-depth); I-addresses satisfy `zeros(a) = 3` (S7b) and `#E(a) ≥ 2` (S7c). Note: S7b and S7c are vacuous on the singleton witness exhibited in the existence proof (where only `k = 0` arises and the shift is the identity); they are load-bearing only for the corollary at `k ≥ 1`.
- Postconditions: (*Existence*) There exists a finite set of correspondence runs `{(vⱼ, aⱼ, nⱼ)}` satisfying (a) and (b). (*Corollary — subspace and field-structure preservation across a run*) For any correspondence run `(vⱼ, aⱼ, nⱼ)` satisfying conjunct (b), every image `shift(aⱼ, k)` with `0 ≤ k < nⱼ` preserves: (i) `subspace_I(shift(aⱼ, k)) = subspace_I(aⱼ)`; (ii) `zeros(shift(aⱼ, k)) = zeros(aⱼ) = 3` (S7b inherited); (iii) `#E(shift(aⱼ, k)) = #E(aⱼ) = δⱼ ≥ 2` (S7c bound preserved).

## ord(v) — OrdinalExtraction (DEF, function)

For a V-position `v` with `#v = m` and `subspace(v) = v₁`, the *ordinal* is:

`ord(v) = [v₂, ..., vₘ]`

— the tumbler of length `m − 1` obtained by stripping the subspace identifier.

- Preconditions: `v ∈ T`, `#v ≥ 2`.
- Postconditions: `ord(v) ∈ T` (length `m - 1 ≥ 1`, satisfying T0). `#ord(v) = #v - 1`. When `v` satisfies S8a, `ord(v) ∈ S` — every component of `[v₂, ..., vₘ]` is positive since every component of `v` is positive by S8a's componentwise positivity conjunct `(A i : 1 ≤ i ≤ #v : vᵢ > 0)`.

## vpos(S, o) — VPositionReconstruction (DEF, function)

For subspace identifier `S` and ordinal `o = [o₁, ..., oₖ]`:

`vpos(S, o) = [S, o₁, ..., oₖ]`

with `#vpos(S, o) = k + 1`. These are inverses: `ord(vpos(S, o)) = o` and `vpos(subspace(v), ord(v)) = v`.

- Preconditions: `S ∈ ℕ`, `o ∈ T`, `#o ≥ 1`.
- Postconditions: `vpos(S, o) ∈ T`, `#vpos(S, o) = #o + 1`, `vpos(S, o)₁ = S`.
  - (a) `ord(vpos(S, o)) = o` — since `vpos(S, o) = [S, o₁, ..., oₖ]`, stripping the first component recovers `[o₁, ..., oₖ] = o`.
  - (b) For any `v ∈ T` with `#v ≥ 2`: `vpos(subspace(v), ord(v)) = v` — since `subspace(v) = v₁` and `ord(v) = [v₂, ..., vₘ]`, reconstruction gives `[v₁, v₂, ..., vₘ] = v`.
  - When `S ≥ 1` and `(A i : 1 ≤ i ≤ #o : oᵢ > 0)`, the result satisfies S8a: `zeros(vpos(S, o)) = 0`, `#vpos(S, o) = k + 1 ≥ 2`, and `(A i : 1 ≤ i ≤ #vpos(S, o) : vpos(S, o)ᵢ > 0)`.

## w_ord — OrdinalDisplacementProjection (DEF, function)

For a displacement `w` with `w₁ = 0` and `#w = m ≥ 2`, the *ordinal projection* is:

`w_ord = [w₂, ..., wₘ]`

of length `m − 1`. The condition `w₁ = 0` ensures `actionPoint(w) ≥ 2`, so by TumblerAdd all positions before the action point are copied from the operand — position 1 (the subspace identifier) is preserved by any addition `v ⊕ w`.

- Preconditions: `w ∈ T`, `#w ≥ 2`, `w₁ = 0`.
- Postconditions: `w_ord ∈ T` (length `m - 1 ≥ 1`, satisfying T0). `#w_ord = #w - 1`. When `Pos(w)` (TA-Pos, ASN-0034), `Pos(w_ord)`. When `Pos(w)`: `actionPoint(w_ord) = actionPoint(w) - 1`.

## OrdAddHom — OrdinalAdditionHomomorphism (LEMMA, lemma)

For a V-position `v` with `#v = m ≥ 2`, and a displacement `w` with `w₁ = 0`, `#w = m`, and `Pos(w)` (TA-Pos, ASN-0034):

- Preconditions: `v ∈ T`, `#v = m ≥ 2`; `w ∈ T`, `Pos(w)` (TA-Pos, ASN-0034), `#w = m`, `w₁ = 0`.
- Postconditions:
  - (a) `ord(v ⊕ w) = ord(v) ⊕ w_ord`
  - (b) `subspace(v ⊕ w) = subspace(v)`
  - (c) `v ⊕ w = vpos(subspace(v), ord(v) ⊕ w_ord)`

## OrdAddS8a — AdditionPreservesS8a (LEMMA, lemma)

For a V-position `v` satisfying S8a with `#v = m ≥ 2`, and a displacement `w` with `w₁ = 0`, `#w = m`, `Pos(w)` (TA-Pos, ASN-0034):

- Preconditions: `v ∈ T` satisfying S8a, `#v = m ≥ 2`; `w ∈ T`, `Pos(w)` (TA-Pos, ASN-0034), `#w = m`, `w₁ = 0`.
- Postconditions: `v ⊕ w satisfies S8a ⟺ (A i : actionPoint(w) < i ≤ m : wᵢ > 0)`. Equivalently, `ord(v ⊕ w) ∈ S ⟺ v ⊕ w satisfies S8a`.

## OrdShiftHom — OrdinalShiftHomomorphism (COROLLARY, lemma)

For a V-position `v` with `#v = m ≥ 2` and `n ≥ 1`:

- Preconditions: `v ∈ T`, `#v = m ≥ 2`, `n ≥ 1`.
- Postconditions:
  - (a) `ord(shift(v, n)) = shift(ord(v), n)`
  - (b) `subspace(shift(v, n)) = subspace(v)` — derived from OrdAddHom (b) at `w = δ(n, m)`, whose `w₁ = 0` holds because `#δ(n, m) = m ≥ 2`.
  - (c) When `v` satisfies S8a, `shift(v, n)` satisfies S8a unconditionally — since `δ(n, m) = [0, ..., 0, n]` has action point `m` with no tail components beyond, the OrdAddS8a condition is vacuously satisfied.

## D-CTG — VContiguity (AXM, predicate)

For each document `d`, with `V_1(d) = {v ∈ dom(M(d)) : subspace(v) = 1}` (the text subspace):

`(A d, u, q : u ∈ V_1(d) ∧ q ∈ V_1(d) ∧ u < q : (A v : subspace(v) = 1 ∧ #v = #u ∧ u < v < q : v ∈ V_1(d)))`

- Preconditions: `subspace(v) = 1` (text subspace); V-positions share a common depth (S8-depth).
- Postconditions: `V_1(d)` is either empty or occupies every position strictly between its extremes (at the fixed text-subspace depth).
- Frame: The link subspace `V_2(d)` is exempt — sparse with tombstones is permitted. D-CTG is a constraint on well-formed text-subspace arrangements; preservation across editing operations is each operation's verification obligation.

## D-MIN — VMinimumPosition (AXM, predicate)

For each document `d` with `V_1(d)` non-empty:

`V_1(d) ≠ ∅ ⟹ min(V_1(d)) = [1, 1, ..., 1]`

where the tuple has length `m_1` (the common depth of the text subspace per S8-depth), and every component is 1.

- Preconditions: `V_1(d) ≠ ∅`; common text-subspace depth `m_1` (S8-depth) with `m_1 ≥ 2` (S8a).
- Postconditions: Every component of `min(V_1(d))` equals 1; in particular the text subspace identifier `min(V_1(d))₁ = 1` and the within-subspace ordinal starts at the minimum positive value.
- Frame: The link subspace `V_2(d)` is exempt — gaps below the minimum (e.g., from tombstoning) are admissible.

## D-CTG-depth — SharedPrefixReduction (COROLLARY, lemma)

For depth `m ≥ 3`, all positions in a non-empty `V_1(d)` share components 2 through `m − 1`. Contiguity reduces to contiguity of the last component alone.

`(A v₁, v₂ ∈ V_1(d), j : 2 ≤ j ≤ m − 1 : (v₁)ⱼ = (v₂)ⱼ)`

- Preconditions: `V_1(d)` non-empty; common depth `m` within the text subspace (S8-depth); `m ≥ 3` (the lemma's non-triviality bound, additional to S8-depth — at `m = 2` the conclusion holds vacuously since the range of shared components 2 through `m − 1` is empty).
- Postconditions: `(A v₁, v₂ ∈ V_1(d), j : 2 ≤ j ≤ m − 1 : (v₁)ⱼ = (v₂)ⱼ)`. Contiguity of `V_1(d)` reduces to contiguity of the m-th (last) component.

## D-SEQ — SequentialPositions (THM, lemma)

For each document `d`, if `V_1(d)` is non-empty, then there exists `n ≥ 1` such that:

`V_1(d) = {[1, 1, ..., 1, k] : 1 ≤ k ≤ n}`

where the tuple has length `m`, the common V-position depth in the text subspace (S8-depth).

- Preconditions: `V_1(d)` non-empty; common V-position depth `m` (S8-depth), with `m ≥ 2` inherited from S8a.
- Postconditions: `(E n : n ≥ 1 : V_1(d) = {[1, 1, ..., 1, k] : 1 ≤ k ≤ n})` where each tuple has length `m`.

## ValidInsertionPosition — ValidInsertionPosition (DEF, predicate)

Binary predicate `ValidInsertionPosition(d, v)` (non-empty case, text subspace `S = 1`):

- Signature: `ValidInsertionPosition(d, v)` — a *binary* predicate on document `d` and V-position `v`. The common V-position depth `m` is determined by `d` via S8-depth and read from state.
- Preconditions: Document `d` with `V_1(d) ⊆ dom(M(d))` non-empty; D-CTG holds on `V_1(d)`; `m ≥ 2` is the common depth of `V_1(d)` by S8-depth and S8a.
- Definition: `ValidInsertionPosition(d, v)` holds iff, writing `N = |V_1(d)|`, `v = shift(min(V_1(d)), j)` for some `j ∈ {0, 1, ..., N}` (with `shift(·, 0) = identity`).
- Postconditions:
  - (a) `subspace(v) = 1` and `#v = m` (the state-fixed common depth).
  - (b) `v` satisfies S8a: `zeros(v) = 0` and all components positive.
  - (c) For fixed `d`, exactly `N + 1` values of `v` satisfy the predicate.
  - (d) The explicit form is `v = [1, 1, ..., 1 + j]` with last component `1 + j` and all preceding components equal to 1.

## ValidFirstInsertionPosition — ValidFirstInsertionPosition (DEF, predicate)

Ternary predicate `ValidFirstInsertionPosition(d, v, m)` (empty case, text subspace `S = 1`):

- Signature: `ValidFirstInsertionPosition(d, v, m)` — a *ternary* predicate on document `d`, V-position `v`, and depth `m`. The depth `m` is an operational input chosen by the placing operation; the strand model fixes only the lower bound `m ≥ 2`.
- Preconditions: Document `d` with `V_1(d) = ∅`; `m ∈ ℕ` with `m ≥ 2`.
- Definition: `ValidFirstInsertionPosition(d, v, m)` holds iff `v = [1, 1, ..., 1]` of depth `m`.
- Postconditions:
  - (a) `subspace(v) = 1` and `#v = m`.
  - (b) `v` satisfies S8a: `zeros(v) = 0` and all components positive.
  - (c) For fixed `d` and `m`, exactly one value of `v` satisfies the predicate.
  - (d) Once the position is placed, S8-depth fixes the depth at `m` for all subsequent positions in the text subspace, after which validity of further insertion positions is governed by `ValidInsertionPosition(d, v)`.
- Frame: The specific value of `m` beyond the bound `m ≥ 2` is not fixed by the strand model.

## S9 — TwoStreamSeparation (THM, lemma)

No modification to any arrangement `Σ.M(d)` can alter the content store `Σ.C`:

`[Σ'.M(d) ≠ Σ.M(d) ⟹ (A a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))]`

- Preconditions: State transition `Σ → Σ'` such that `Σ'.M(d) ≠ Σ.M(d)` for some document `d` (an arrangement-modifying transition); system satisfies S0 (content immutability).
- Postconditions: `(A a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))` — every content entry persists with its value across the transition.
- Frame: The arrangement modification may be arbitrary (insertion, deletion, rearrangement, or any combination); S9 holds regardless of the specific transformation applied to `Σ.M(d)`.
