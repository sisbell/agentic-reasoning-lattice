# ASN-0034 Formal Statements

*Source: ASN-0034-tumbler-algebra.md (revised 2026-03-13) — Index: 2026-03-13 — Extracted: 2026-03-13*

## Definition — ActionPoint

For a positive displacement `w = [w₁, w₂, ..., wₙ]`, define the *action point* as `k = min({i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0})` — the position of the first nonzero component.

## Definition — LastSignificantPosition

We define the *last significant position* of a tumbler `t`. When `t` has at least one nonzero component, `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})` — the position of the last nonzero component. When every component is zero, `sig(t) = #t`.

## Definition — ZeroCount

Define `zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`.

## Definition — FieldParsing

The function `fields(t)` extracts the node, user, document, and element fields. A tumbler with the form `t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ` has:

- **Node field** `N₁. ... .Nₐ`
- **User field** `U₁. ... .Uᵦ`
- **Document field** `D₁. ... .Dᵧ`
- **Element field** `E₁. ... .Eδ`

The correspondence by `zeros(t)`:
- `zeros(t) = 0`: `t` is a node address (node field only)
- `zeros(t) = 1`: `t` is a user address (node and user fields)
- `zeros(t) = 2`: `t` is a document address (node, user, and document fields)
- `zeros(t) = 3`: `t` is an element address (all four fields)

## Definition — PositiveTumbler

A tumbler `t ∈ T` is *positive*, written `t > 0`, iff at least one of its components is nonzero: `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`. A tumbler is a *zero tumbler* iff every component is zero: `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.

## Definition — Divergence

For tumblers `a, b ∈ T` with `a ≠ b`, the *divergence* `divergence(a, b)` is defined by two cases corresponding to the two cases of T1:

  (i) If there exists `k ≤ min(#a, #b)` such that `aₖ ≠ bₖ` and `(A i : 1 ≤ i < k : aᵢ = bᵢ)`, then `divergence(a, b) = k` — component divergence at a shared position.

  (ii) If `(A i : 1 ≤ i ≤ min(#a, #b) : aᵢ = bᵢ)` and `#a ≠ #b`, then `divergence(a, b) = min(#a, #b) + 1` — prefix divergence, where one tumbler is a proper prefix of the other.

Exactly one case applies for any `a ≠ b`.

## Definition — TumblerAdd

Let `a = [a₁, ..., aₘ]` and `w = [w₁, ..., wₙ]` with `w > 0`. With action point `k`:

```
         ⎧ aᵢ           if i < k        (copy from start)
rᵢ   =  ⎨ aₖ + wₖ      if i = k        (single-component advance)
         ⎩ wᵢ           if i > k        (copy from displacement)
```

The result `a ⊕ w = [r₁, ..., rₚ]` has length `p = max(k - 1, 0) + (n - k + 1)`.

**Precondition:** `k ≤ m` — the displacement's action point must fall within the start position's length.

Three properties: (1) No carry propagation — the sum `aₖ + wₖ` is a single natural-number addition with no carry into position `k - 1`. (2) Tail replacement, not tail addition — components after the action point come entirely from `w`; positions `k + 1, ..., m` of `a` are discarded. (3) The many-to-one property — distinct start positions can produce the same result.

## Definition — TumblerSubtract

Given an end position `a` and a displacement `w`, recover the start position. When the operands have different lengths, conceptually zero-pad the shorter to the length of the longer before scanning for divergence. When `a = w` (no divergence exists after padding), the result is the zero tumbler of length `max(#a, #w)`: `a ⊖ w = [0, ..., 0]`. Otherwise, let `k` be the first position where `a` and `w` differ (treating missing components as zero):

```
         ⎧ 0             if i < k        (these levels matched — zero them)
rᵢ   =  ⎨ aₖ - wₖ      if i = k        (reverse the advance)
         ⎩ aᵢ           if i > k        (copy from end position)
```

The result has length `max(#a, #w)`.

**Precondition:** `a ≥ w` — when `a ≠ w`, at the divergence point (after zero-padding) `aₖ ≥ wₖ`.

---

## T0(a) — UnboundedComponents (LEMMA, lemma)

`(A t ∈ T, i : 1 ≤ i ≤ #t : (A M ∈ ℕ :: (E t' ∈ T :: t' agrees with t except t'.dᵢ > M)))`

## T0(b) — UnboundedLength (LEMMA, lemma)

`(A n ∈ ℕ : n ≥ 1 : (E t ∈ T :: #t ≥ n))`

## T1 — LexicographicOrder (INV, predicate(Tumbler, Tumbler))

For tumblers `a = a₁. ... .aₘ` and `b = b₁. ... .bₙ`, define `a < b` iff there exists `k ≥ 1` such that `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either:

  (i) `k ≤ min(m, n)` and `aₖ < bₖ`, or

  (ii) `k = m + 1 ≤ n` (that is, `a` is a proper prefix of `b`).

## T2 — IntrinsicComparison (INV, predicate(Tumbler, Tumbler))

The order relation T1 is computable from the two tumblers alone, without consulting any external data structure. The comparison examines at most `min(#a, #b)` component pairs.

## T3 — CanonicalRepresentation (INV, predicate(Tumbler, Tumbler))

`(A a, b ∈ T : a₁ = b₁ ∧ ... ∧ aₙ = bₙ ∧ #a = #b ≡ a = b)`

## T4 — ValidAddress (INV, predicate(Tumbler))

Every tumbler `t ∈ T` used as an address contains at most three zero-valued components, appearing in order as field separators, every non-separator component is strictly positive, and every field present in the address has at least one component. Formally, if `t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`, then `(A i : 1 ≤ i ≤ α : Nᵢ > 0)`, `(A j : 1 ≤ j ≤ β : Uⱼ > 0)`, `(A k : 1 ≤ k ≤ γ : Dₖ > 0)`, `(A l : 1 ≤ l ≤ δ : Eₗ > 0)`, and `α ≥ 1`, `β ≥ 1` when present, `γ ≥ 1` when present, `δ ≥ 1` when present.

The non-empty field constraint is equivalent to three syntactic conditions on the raw tumbler: no two zeros are adjacent, the tumbler does not begin with zero, and the tumbler does not end with zero.

## T5 — ContiguousSubtrees (LEMMA, lemma)

For any tumbler prefix `p`, the set `{t ∈ T : p ≼ t}` (where `≼` denotes "is a prefix of") forms a contiguous interval under T1:

  `[p ≼ a ∧ p ≼ c ∧ a ≤ b ≤ c ⟹ p ≼ b]`

## T6 — DecidableContainment (LEMMA, lemma)

For any two tumblers `a, b ∈ T`, the following are decidable from the addresses alone:

  (a) Whether `a` and `b` share the same node field.

  (b) Whether `a` and `b` share the same node and user fields.

  (c) Whether `a` and `b` share the same node, user, and document-lineage fields.

  (d) Whether the document field of `a` is a prefix of the document field of `b` (structural subordination within a document family).

## T7 — SubspaceDisjoint (LEMMA, lemma)

The subspace identifier (the first component of the element field) permanently separates the address space into disjoint regions. No tumbler in subspace `s₁` can equal or be confused with a tumbler in subspace `s₂ ≠ s₁`.

  `(A a, b ∈ T : a.E₁ ≠ b.E₁ ⟹ a ≠ b)`

## T8 — AllocationPermanence (INV, predicate(set\<Tumbler\>, set\<Tumbler\>))

If tumbler `a ∈ T` has been allocated at any point in the system's history, then for all subsequent states, `a` remains in the set of allocated addresses. No operation removes an allocated address from the address space. The set of allocated addresses is monotonically non-decreasing.

## T9 — ForwardAllocation (INV, predicate(Tumbler, Tumbler))

Each allocator in the system controls a single ownership prefix and allocates sequentially within it. Within that sequential stream, new addresses are strictly monotonically increasing:

  `(A a, b : same_allocator(a, b) ∧ allocated_before(a, b) : a < b)`

## T10 — PartitionIndependence (LEMMA, lemma)

The address space is partitioned by prefix into ownership domains. Two allocators with distinct, non-nesting prefixes can allocate simultaneously, and the resulting addresses are guaranteed distinct.

Formally: let `p₁` and `p₂` be prefixes such that neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for any tumbler `a` with prefix `p₁` and any tumbler `b` with prefix `p₂`, `a ≠ b`.

## T10a — AllocatorDiscipline (INV, predicate(Tumbler, nat))

Each allocator produces its sibling outputs exclusively by repeated application of `inc(·, 0)` — shallow increment at the last significant position. To spawn a child allocator, the parent performs one `inc(·, k')` with `k' > 0` to establish the child's prefix, then delegates further allocation to the child. The parent's own sibling stream resumes with `inc(·, 0)`.

## (Prefix ordering extension) — PrefixOrderingExtension (LEMMA, lemma)

Let `p₁, p₂ ∈ T` be tumblers such that `p₁ < p₂` and neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for every `a` extending `p₁` (`p₁ ≼ a`) and every `b` extending `p₂` (`p₂ ≼ b`), `a < b`.

## (Partition monotonicity) — PartitionMonotonicity (LEMMA, lemma)

Within any prefix-delimited partition of the address space, the set of allocated addresses is totally ordered by T1, and this order is consistent with the allocation order of any single allocator within that partition. Moreover, for any two sibling sub-partitions with non-nesting prefixes `p₁ < p₂`, every address extending `p₁` precedes every address extending `p₂` under T1 — the per-allocator ordering extends to a cross-allocator ordering determined by the prefix structure.

Depends on: T5, T9, T10, T10a, TA5, PrefixOrderingExtension.

## (Global uniqueness) — GlobalUniqueness (LEMMA, lemma)

No two distinct allocations, anywhere in the system, at any time, produce the same address.

Four cases:
- *Case 1: Same allocator.* T9 guarantees `a ≠ b` because allocation is strictly monotonic.
- *Case 2: Different allocators at the same hierarchical level.* Prefixes `p₁`, `p₂` are siblings — neither is a prefix of the other. T10 gives `a ≠ b`.
- *Case 3: Different allocators with nesting prefixes and different zero counts.* By T4, different zero counts imply different field structure. By T3, `a ≠ b`.
- *Case 4: Different allocators with nesting prefixes and the same zero count.* By T10a, parent allocator uses `inc(·, 0)` for siblings (all outputs have uniform length `γ₁`). Child prefix was established by `inc(parent_output, k')` with `k' > 0`, giving prefix length `γ₁ + k'`. Child outputs have uniform length `γ₁ + k'`. Since `k' ≥ 1`, child outputs are strictly longer: `γ₁ + k' > γ₁`. By T3, `a ≠ b`.

Depends on: T3, T4, T9, T10, T10a, TA5.

## TA0 — WellDefinedAddition (PRE, requires)

For tumblers `a, w ∈ T` where `w > 0` and the action point `k` of `w` satisfies `k ≤ #a`, the result `a ⊕ w` is a well-defined tumbler in `T`.

## TA1 — AdditionWeakOrder (LEMMA, lemma)

`(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) : a ⊕ w ≤ b ⊕ w)`, where `k` is the action point of `w`.

## TA1-strict — AdditionStrictOrder (LEMMA, lemma)

`(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) ∧ k ≥ divergence(a, b) : a ⊕ w < b ⊕ w)`, where `k` is the action point of `w`.

## TA-strict — StrictIncrease (POST, ensures)

`(A a ∈ T, w > 0 : a ⊕ w > a)` (where `a ⊕ w` is well-defined, i.e., `k ≤ #a` per TA0).

## TA2 — WellDefinedSubtraction (PRE, requires)

For tumblers `a, w ∈ T` where `a ≥ w`, `a ⊖ w` is a well-defined tumbler in `T`.

## TA3 — SubtractionWeakOrder (LEMMA, lemma)

`(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w ≤ b ⊖ w)`

## TA3-strict — SubtractionStrictOrder (LEMMA, lemma)

`(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b : a ⊖ w < b ⊖ w)`

## TA4 — PartialInverse (LEMMA, lemma)

`(A a, w : w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊕ w) ⊖ w = a)`, where `k` is the action point of `w`.

The precondition has three parts:
- `k = #a` — the action point falls at the last component of `a`
- `#w = k` — the displacement has no trailing components beyond the action point
- `(A i : 1 ≤ i < k : aᵢ = 0)` — all components of `a` before the action point are zero

## (Reverse inverse) — ReverseInverse (LEMMA, lemma)

`(A a, w : a ≥ w ∧ w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊖ w) ⊕ w = a)`, where `k` is the action point of `w`.

## TA5 — HierarchicalIncrement (POST, ensures)

For tumbler `t ∈ T` and level `k ≥ 0`, there exists an operation `inc(t, k)` producing tumbler `t'` such that:

  (a) `t' > t` (strictly greater under T1),

  (b) `t'` agrees with `t` on all components before the increment point,

  (c) when `k = 0` (*sibling*): `#t' = #t`, and `t'` differs from `t` only at position `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`,

  (d) when `k > 0` (*child*): `#t' = #t + k`, the `k - 1` intermediate positions `#t + 1, ..., #t + k - 1` are set to `0` (field separators), and the final position `#t + k` is set to `1` (the first child).

## (TA5 preserves T4) — IncrementPreservesValidity (LEMMA, lemma)

**TA5 preserves T4 when `k ≤ 2` and `zeros(t) + k - 1 ≤ 3`.**

- For `k = 0`: no zeros are added — `zeros(t') = zeros(t)`, no new adjacencies. T4 is preserved unconditionally.
- For `k = 1`: one component (child value `1`) is appended, no new zero separators — `zeros(t') = zeros(t)`. T4 is preserved when `zeros(t) ≤ 3`.
- For `k = 2`: one zero separator and one child value `1` are appended, giving `zeros(t') = zeros(t) + 1`. T4 is preserved when `zeros(t) ≤ 2`.
- For `k ≥ 3`: the appended sequence `[0, 0, ..., 0, 1]` contains `k - 1 ≥ 2` zeros, of which at least two are adjacent. This violates T4's non-empty field constraint. T4 is violated for all `k ≥ 3`.

## TA6 — ZeroTumblerSentinel (INV, predicate(Tumbler))

No zero tumbler is a valid address — no all-zero tumbler designates content. Every zero tumbler is less than every positive tumbler under T1.

  `(A t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0) ⟹ t is not a valid address)`

  `(A s, t ∈ T : (A i : 1 ≤ i ≤ #s : sᵢ = 0) ∧ (E j : 1 ≤ j ≤ #t : tⱼ > 0) ⟹ s < t)`

## TA7a — SubspaceClosure (LEMMA, lemma)

The canonical representation for shift arithmetic is the *ordinal-only* formulation: a position in subspace `S` with identifier `N` and ordinal `x` is represented as the single-component tumbler `[x]` for arithmetic purposes, with `N` held as structural context. An element-local displacement is `w = [n]` with `n > 0`. In this formulation:

  `(A [x] ∈ S₁, n > 0 : [x] ⊕ [n] = [x + n] ∈ S₁)`

  `(A [x] ∈ S₁, n > 0, x ≥ n : [x] ⊖ [n] = [x - n] ∈ S₁ ∪ {[0]})`

## (Associativity) — AdditionAssociative (LEMMA, lemma)

**Addition is associative where both compositions are defined.** The constructive definition yields `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)` whenever both sides are well-defined. Let `k_b` and `k_c` be the action points of `b` and `c` respectively:

- When `k_b < k_c`: both sides produce `aᵢ` for `i < k_b`, `aₖ_b + bₖ_b` at `k_b`, `bᵢ` for `k_b < i < k_c`, `bₖ_c + cₖ_c` at `k_c`, and `cᵢ` beyond — identical.
- When `k_b = k_c = k`: both sides produce `aₖ + bₖ + cₖ` at `k` and `cᵢ` beyond — identical.
- When `k_b > k_c`: both sides produce `aₖ_c + cₖ_c` at `k_c` and `cᵢ` beyond — identical.

## T12 — SpanWellDefined (INV, predicate(Tumbler, Tumbler))

A span `(s, ℓ)` is well-formed when `ℓ > 0` and the action point `k` of `ℓ` satisfies `k ≤ #s` (the TA0 precondition for `s ⊕ ℓ`). Equivalently, the number of leading zeros in `ℓ` must be strictly less than `#s`. A well-formed span denotes the set `{t ∈ T : s ≤ t < s ⊕ ℓ}`.

Non-emptiness follows from TA-strict: since `ℓ > 0` and `k ≤ #s`, TA0 gives `s ⊕ ℓ ∈ T`, and TA-strict gives `s ⊕ ℓ > s` directly. The interval `[s, s ⊕ ℓ)` contains at least `s` itself.
