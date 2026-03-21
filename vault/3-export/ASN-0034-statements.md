# ASN-0034 Formal Statements

*Source: ASN-0034-tumbler-algebra.md (revised 2026-03-21) — Extracted: 2026-03-21*

## Definition — Tumbler

A tumbler is a finite sequence of non-negative integers. `t = d₁.d₂. ... .dₙ` where each `dᵢ ∈ ℕ` and `n ≥ 1`. The set of all tumblers is **T**. `#t` denotes the length of `t`. `tᵢ` denotes the `i`-th component.

## Definition — ZeroCount

`zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`

## Definition — PrefixRelation

`p ≼ t` ("p is a prefix of t"): `#p ≤ #t ∧ (A i : 1 ≤ i ≤ #p : pᵢ = tᵢ)`.

## Definition — PositiveTumbler

A tumbler `t ∈ T` is *positive*, written `t > 0`, iff `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`. A tumbler is a *zero tumbler* iff `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.

## Definition — ActionPoint

For a positive displacement `w = [w₁, w₂, ..., wₙ]`, the *action point* is `k = min({i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0})` — the position of the first nonzero component.

## Definition — LastSignificantPosition

`sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})` when `t` has at least one nonzero component. When every component is zero, `sig(t) = #t`.

## Definition — Divergence

For tumblers `a, b ∈ T` with `a ≠ b`:

  (i) If there exists `k ≤ min(#a, #b)` such that `aₖ ≠ bₖ` and `(A i : 1 ≤ i < k : aᵢ = bᵢ)`, then `divergence(a, b) = k` — component divergence at a shared position.

  (ii) If `(A i : 1 ≤ i ≤ min(#a, #b) : aᵢ = bᵢ)` and `#a ≠ #b`, then `divergence(a, b) = min(#a, #b) + 1` — prefix divergence, where one tumbler is a proper prefix of the other.

Exactly one case applies for any `a ≠ b`.

## Definition — TumblerAdd

Let `a = [a₁, ..., aₘ]` and `w = [w₁, ..., wₙ]` with `w > 0` and action point `k`. **Precondition:** `k ≤ m`.

```
         ⎧ aᵢ           if i < k        (copy from start)
rᵢ   =  ⎨ aₖ + wₖ      if i = k        (single-component advance)
         ⎩ wᵢ           if i > k        (copy from displacement)
```

Result `a ⊕ w = [r₁, ..., rₙ]` has length `#(a ⊕ w) = #w` (*result-length identity*).

Properties of TumblerAdd:
- **No carry propagation.** The sum `aₖ + wₖ` is a single natural-number addition with no carry into position `k − 1`.
- **Tail replacement, not tail addition.** Components of `a` at positions `k + 1, ..., m` are discarded; the result's tail comes entirely from `w`.

## Definition — TumblerSub

Given `a` and `w` with `a ≥ w`. Zero-pad the shorter to length `max(#a, #w)`. When zero-padded sequences are equal, the result is the zero tumbler of length `max(#a, #w)`. Otherwise let `k` be the first position where `a` and `w` differ after zero-padding:

```
         ⎧ 0             if i < k        (matched levels — zero them)
rᵢ   =  ⎨ aₖ - wₖ      if i = k        (reverse the advance)
         ⎩ aᵢ           if i > k        (copy from end position)
```

Result has length `max(#a, #w)`. **Precondition:** `a ≥ w`; at the divergence point after zero-padding, `aₖ ≥ wₖ`.

## Definition — OrdinalDisplacement

For natural number `n ≥ 1` and depth `m ≥ 1`, `δ(n, m) = [0, 0, ..., 0, n]` of length `m` — zero at positions `1` through `m − 1`, and `n` at position `m`. Its action point is `m`.

When the depth is determined by context (typically `m = #v`), write `δₙ`.

## Definition — OrdinalShift

For a tumbler `v` of length `m` and natural number `n ≥ 1`:

`shift(v, n) = v ⊕ δ(n, m)`

By TumblerAdd: `shift(v, n)ᵢ = vᵢ` for `i < m`, and `shift(v, n)ₘ = vₘ + n`. Length: `#shift(v, n) = #δₙ = m = #v`.

---

## T0(a) — UnboundedComponentValues (AX, axiom)

`(A t ∈ T, i : 1 ≤ i ≤ #t : (A M ∈ ℕ :: (E t' ∈ T :: t' agrees with t except t'.dᵢ > M)))`

## T0(b) — UnboundedLength (AX, axiom)

`(A n ∈ ℕ : n ≥ 1 : (E t ∈ T :: #t ≥ n))`

## T1 — LexicographicOrder (DEF, function)

For tumblers `a = a₁. ... .aₘ` and `b = b₁. ... .bₙ`, define `a < b` iff there exists `k ≥ 1` such that `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either:

  (i) `k ≤ min(m, n)` and `aₖ < bₖ`, or

  (ii) `k = m + 1 ≤ n` (that is, `a` is a proper prefix of `b`).

## T2 — IntrinsicComparison (AX, axiom)

The order relation T1 is computable from the two tumblers alone, without consulting any external data structure. The comparison examines at most `min(#a, #b)` component pairs.

## T3 — CanonicalRepresentation (AX, axiom)

`(A a, b ∈ T : a₁ = b₁ ∧ ... ∧ aₙ = bₙ ∧ #a = #b ≡ a = b)`

## T4 — HierarchicalParsing (AX, axiom)

Every tumbler `t ∈ T` used as an address contains at most three zero-valued components, appearing in order as field separators, every non-separator component is strictly positive, and every field present in the address has at least one component. Formally, if `t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`, then:

  `(A i : 1 ≤ i ≤ α : Nᵢ > 0)`, `(A j : 1 ≤ j ≤ β : Uⱼ > 0)`, `(A k : 1 ≤ k ≤ γ : Dₖ > 0)`, `(A l : 1 ≤ l ≤ δ : Eₗ > 0)`, and `α ≥ 1`, `β ≥ 1` when present, `γ ≥ 1` when present, `δ ≥ 1` when present.

The function `fields(t)` extracting node, user, document, and element fields is well-defined and computable from `t` alone.

Zero count determines hierarchical level:

  - `zeros(t) = 0`: `t` is a node address (node field only),
  - `zeros(t) = 1`: `t` is a user address (node and user fields),
  - `zeros(t) = 2`: `t` is a document address (node, user, and document fields),
  - `zeros(t) = 3`: `t` is an element address (all four fields).

Equivalent syntactic conditions on the raw tumbler: no two zeros are adjacent, the tumbler does not begin with zero, and the tumbler does not end with zero.

## T5 — ContiguousSubtrees (LEMMA, lemma)

For any tumbler prefix `p`, the set `{t ∈ T : p ≼ t}` forms a contiguous interval under T1:

  `[p ≼ a ∧ p ≼ c ∧ a ≤ b ≤ c ⟹ p ≼ b]`

## T6 — DecidableContainment (COROLLARY, corollary)

For any two tumblers `a, b ∈ T`, the following are decidable from the addresses alone:

  (a) Whether `a` and `b` share the same node field.

  (b) Whether `a` and `b` share the same node and user fields.

  (c) Whether `a` and `b` share the same node, user, and document-lineage fields.

  (d) Whether the document field of `a` is a prefix of the document field of `b` (structural subordination within a document family).

## T7 — SubspaceDisjointness (COROLLARY, corollary)

`(A a, b ∈ T : a.E₁ ≠ b.E₁ ⟹ a ≠ b)`

where `a.E₁` denotes the first component of `a`'s element field.

## T8 — AllocationPermanence (AX, axiom)

If tumbler `a ∈ T` has been allocated at any point in the system's history, then for all subsequent states, `a` remains in the set of allocated addresses. No operation removes an allocated address from the address space. The set of allocated addresses is monotonically non-decreasing.

## T9 — ForwardAllocation (LEMMA, lemma)

`(A a, b : same_allocator(a, b) ∧ allocated_before(a, b) : a < b)`

## T10 — PartitionIndependence (AX, axiom)

Let `p₁` and `p₂` be prefixes such that `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`. Then for any tumbler `a` with prefix `p₁` and any tumbler `b` with prefix `p₂`, `a ≠ b`.

## T10a — AllocatorDiscipline (AX, axiom)

Each allocator produces its sibling outputs exclusively by repeated application of `inc(·, 0)` — shallow increment at the last significant position. To spawn a child allocator, the parent performs one `inc(·, k')` with `k' > 0` to establish the child's prefix, then delegates further allocation to the child. The parent's own sibling stream resumes with `inc(·, 0)`.

## T12 — SpanWellDefinedness (DEF, predicate)

A span `(s, ℓ)` is well-formed when `ℓ > 0` and the action point `k` of `ℓ` satisfies `k ≤ #s` (the TA0 precondition for `s ⊕ ℓ`). Equivalently, the number of leading zeros in `ℓ` must be strictly less than `#s`. A well-formed span denotes the set `{t ∈ T : s ≤ t < s ⊕ ℓ}`. This set is non-empty: by TA-strict, `s ⊕ ℓ > s`, so the interval contains at least `s` itself.

## TA0 — AdditionWellDefined (PRE, requires)

For tumblers `a, w ∈ T` where `w > 0` and the action point `k` of `w` satisfies `k ≤ #a`, the result `a ⊕ w` is a well-defined tumbler in `T`.

## TA1 — OrderPreservationAdditionWeak (LEMMA, lemma)

`(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) : a ⊕ w ≤ b ⊕ w)`, where `k` is the action point of `w`.

## TA1-strict — OrderPreservationAdditionStrict (LEMMA, lemma)

`(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) ∧ k ≥ divergence(a, b) : a ⊕ w < b ⊕ w)`, where `k` is the action point of `w`.

When `k < divergence(a, b)`, the original divergence is erased by tail replacement and the results are equal (the weak form holds, the strict form does not).

## TA-strict — StrictIncrease (LEMMA, lemma)

`(A a ∈ T, w > 0 : a ⊕ w > a)` where `a ⊕ w` is well-defined (i.e., `k ≤ #a` per TA0).

## TA2 — SubtractionWellDefined (PRE, requires)

For tumblers `a, w ∈ T` where `a ≥ w`, `a ⊖ w` is a well-defined tumbler in `T`.

## TA3 — OrderPreservationSubtractionWeak (LEMMA, lemma)

`(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w ≤ b ⊖ w)`

## TA3-strict — OrderPreservationSubtractionStrict (LEMMA, lemma)

`(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b : a ⊖ w < b ⊖ w)`

## TA4 — PartialInverse (LEMMA, lemma)

`(A a, w : w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊕ w) ⊖ w = a)`, where `k` is the action point of `w`.

**Corollary (Reverse inverse).** `(A a, w : a ≥ w ∧ w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊖ w) ⊕ w = a)`, where `k` is the action point of `w`.

## TA5 — HierarchicalIncrement (AX, axiom)

For tumbler `t ∈ T` and level `k ≥ 0`, `inc(t, k)` produces tumbler `t'` such that:

  (a) `t' > t` (strictly greater under T1),

  (b) `t'` agrees with `t` on all components before the increment point,

  (c) when `k = 0` (*sibling*): `#t' = #t`, and `t'` differs from `t` only at position `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`,

  (d) when `k > 0` (*child*): `#t' = #t + k`, positions `#t + 1, ..., #t + k - 1` are set to `0` (field separators), and position `#t + k` is set to `1` (the first child).

TA5 preserves T4 when `k = 0` unconditionally, when `k = 1` and `zeros(t) ≤ 3`, and when `k = 2` and `zeros(t) ≤ 2`. For `k ≥ 3`, adjacent zeros are introduced, violating T4.

## TA6 — ZeroTumblers (AX, axiom)

`(A t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0) ⟹ t is not a valid address)`

`(A s, t ∈ T : (A i : 1 ≤ i ≤ #s : sᵢ = 0) ∧ (E j : 1 ≤ j ≤ #t : tⱼ > 0) ⟹ s < t)`

## TA7a — SubspaceClosure (AX, axiom)

The canonical representation for shift arithmetic is the *ordinal-only* formulation: a position in subspace `S` with identifier `N` and ordinal `o = [o₁, ..., oₘ]` (`m ≥ 1`) is represented as `o` for arithmetic purposes, with `N` held as structural context. An element-local displacement is a positive tumbler `w` with action point `k` satisfying `1 ≤ k ≤ m`. In this formulation:

  `(A o ∈ S, w > 0 : k ≤ #o ⟹ o ⊕ w ∈ S)`

  `(A o ∈ S, w > 0 : o ≥ w ⟹ o ⊖ w ∈ S ∪ Z)`

where `Z` is the set of zero tumblers.

## TA-assoc — AdditionAssociative (LEMMA, lemma)

`(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)` whenever both sides are well-defined.

## TA-LC — LeftCancellation (LEMMA, lemma)

If `a ⊕ x = a ⊕ y` with both sides well-defined (TA0 satisfied for both), then `x = y`.

## TA-RC — RightCancellationFailure (LEMMA, lemma)

There exist tumblers `a, b, w` with `a ≠ b` and `a ⊕ w = b ⊕ w` (both sides well-defined).

## TA-MTO — ManyToOne (LEMMA, lemma)

For any displacement `w` with action point `k` and any tumblers `a, b` with `#a ≥ k` and `#b ≥ k`:

`a ⊕ w = b ⊕ w` if and only if `aᵢ = bᵢ` for all `1 ≤ i ≤ k`.

## D0 — DisplacementWellDefined (PRE, requires)

`a < b`, and the divergence `k` of `a` and `b` satisfies `k ≤ #a`.

D0 ensures `b ⊖ a` is a well-defined positive tumbler with TA0 satisfied for `a ⊕ (b ⊖ a)`. Round-trip faithfulness (D1) additionally requires `#a ≤ #b`.

## D1 — DisplacementRoundTrip (LEMMA, lemma)

For tumblers `a, b ∈ T` with `a < b`, `divergence(a, b) ≤ #a`, and `#a ≤ #b`:

`a ⊕ (b ⊖ a) = b`

## D2 — DisplacementUnique (COROLLARY, corollary)

Under D1's preconditions (`a < b`, `divergence(a, b) ≤ #a`, `#a ≤ #b`), if `a ⊕ w = b` then `w = b ⊖ a`.

## OrdinalDisplacement — OrdinalDisplacement (DEF, function)

For natural number `n ≥ 1` and depth `m ≥ 1`: `δ(n, m) = [0, ..., 0, n]` of length `m`, zero at positions `1` through `m − 1`, and `n` at position `m`. Action point is `m`.

## OrdinalShift — OrdinalShift (DEF, function)

For a tumbler `v` of length `m` and natural number `n ≥ 1`: `shift(v, n) = v ⊕ δ(n, m)`, with `#shift(v, n) = m = #v`.

## TS1 — ShiftOrderPreservation (LEMMA, lemma)

`(A v₁, v₂, n : n ≥ 1 ∧ #v₁ = #v₂ = m ∧ v₁ < v₂ : shift(v₁, n) < shift(v₂, n))`

## TS2 — ShiftInjectivity (LEMMA, lemma)

`(A v₁, v₂, n : n ≥ 1 ∧ #v₁ = #v₂ = m : shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂)`

## TS3 — ShiftComposition (LEMMA, lemma)

`(A v, n₁, n₂ : n₁ ≥ 1 ∧ n₂ ≥ 1 ∧ #v = m : shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂))`

## TS4 — ShiftStrictIncrease (COROLLARY, corollary)

`(A v, n : n ≥ 1 ∧ #v = m : shift(v, n) > v)`

## TS5 — ShiftAmountMonotonicity (COROLLARY, corollary)

`(A v, n₁, n₂ : n₁ ≥ 1 ∧ n₂ > n₁ ∧ #v = m : shift(v, n₁) < shift(v, n₂))`
