# ASN-0001 Formal Properties

## Definition — Zeros

`zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`

---

## Definition — Fields

The function `fields(t)` extracts the node, user, document, and element fields from a tumbler `t` of the form `N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`. It is well-defined and computable from `t` alone.

---

## Definition — LastSignificantPosition

`sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0} ∪ {#t})`

That is: the position of the last nonzero component, or if every component is zero, the last position.

---

## Definition — PositiveTumbler

A tumbler `t ∈ T` is *positive*, written `t > 0`, iff at least one of its components is nonzero: `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`. A tumbler is a *zero tumbler* iff every component is zero: `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.

---

## Definition — ActionPoint

For a positive displacement `w = [w₁, w₂, ..., wₙ]`, the action point is `k = min({i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0})` — the position of the first nonzero component.

---

## Definition — TumblerAdd

Let `a = [a₁, ..., aₘ]` and `w = [w₁, ..., wₙ]` with `w > 0`. With action point `k`:

```
         ⎧ aᵢ           if i < k        (copy from start)
rᵢ   =  ⎨ aₖ + wₖ      if i = k        (single-component advance)
         ⎩ wᵢ           if i > k        (copy from displacement)
```

The result `a ⊕ w = [r₁, ..., rₚ]` has length `p = max(k - 1, 0) + (n - k + 1)`.

**Precondition:** `k ≤ m` — the displacement's action point must fall within the start position's length.

**No carry propagation.** The sum `aₖ + wₖ` at the action point is a single natural-number addition. There is no carry into position `k - 1`.

**Tail replacement, not tail addition.** Components after the action point come entirely from `w`. The start position's components at positions `k + 1, ..., m` are discarded.

---

## Definition — TumblerSubtract

Given an end position `a` and displacement `w`, when `a = w` (no divergence exists), the result is the zero tumbler of length `#a`: `a ⊖ w = [0, ..., 0]` with `#(a ⊖ w) = #a`. Otherwise, let `k` be the first position where `a` and `w` differ:

```
         ⎧ 0             if i < k        (these levels matched — zero them)
rᵢ   =  ⎨ aₖ - wₖ      if i = k        (reverse the advance)
         ⎩ aᵢ           if i > k        (copy from end position)
```

**Precondition:** `a ≥ w` — when `a ≠ w`, at the divergence point `aₖ ≥ wₖ`.

---

## Definition — Divergence

`divergence(a, b)` is the first position at which `a` and `b` differ: `divergence(a, b) = min({i : 1 ≤ i ≤ min(#a, #b) ∧ aᵢ ≠ bᵢ})`.

---

## T0 — UnboundedComponents (INV, predicate(Tumbler))

`(A t ∈ T, i : 1 ≤ i ≤ #t : (A M ∈ ℕ :: (E t' ∈ T :: t' agrees with t except t'.dᵢ > M)))`

For every tumbler and every component position, there exists a tumbler whose value at that position exceeds any given bound.

---

## T1 — LexicographicOrder (INV, predicate(Tumbler, Tumbler))

For tumblers `a = a₁. ... .aₘ` and `b = b₁. ... .bₙ`, define `a < b` iff there exists `k ≥ 1` such that `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either:

  (i) `k ≤ min(m, n)` and `aₖ < bₖ`, or

  (ii) `k = m + 1 ≤ n` (that is, `a` is a proper prefix of `b`).

---

## T2 — IntrinsicComparison (INV, predicate(Tumbler, Tumbler))

The order relation T1 is computable from the two tumblers alone, without consulting any external data structure. The comparison examines at most `min(#a, #b)` component pairs.

---

## T3 — CanonicalRepresentation (INV, predicate(Tumbler, Tumbler))

`(A a, b ∈ T : a₁ = b₁ ∧ ... ∧ aₙ = bₙ ∧ #a = #b ≡ a = b)`

---

## T4 — HierarchicalParsing (INV, predicate(Tumbler))

Every tumbler `t ∈ T` used as an I-space address contains at most three zero-valued components, appearing in order as field separators, and every non-separator component is strictly positive. Formally, if `t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`, then `(A i : 1 ≤ i ≤ α : Nᵢ > 0)`, `(A j : 1 ≤ j ≤ β : Uⱼ > 0)`, `(A k : 1 ≤ k ≤ γ : Dₖ > 0)`, `(A l : 1 ≤ l ≤ δ : Eₗ > 0)`.

The count of zero-valued components uniquely determines the hierarchical level:

  - `zeros(t) = 0`: `t` is a node address (node field only),
  - `zeros(t) = 1`: `t` is a user address (node and user fields),
  - `zeros(t) = 2`: `t` is a document address (node, user, and document fields),
  - `zeros(t) = 3`: `t` is an element address (all four fields).

---

## T5 — ContiguousSubtrees (LEMMA, lemma)

For any tumbler prefix `p`, the set `{t ∈ T : p ≼ t}` (where `≼` denotes "is a prefix of") forms a contiguous interval under T1:

  `[p ≼ a ∧ p ≼ c ∧ a ≤ b ≤ c ⟹ p ≼ b]`

---

## T6 — DecidableContainment (LEMMA, lemma)

For any two tumblers `a, b ∈ T`, the following are decidable from the addresses alone:

  (a) Whether `a` and `b` share the same node field.

  (b) Whether `a` and `b` share the same node and user fields.

  (c) Whether `a` and `b` share the same node, user, and document-lineage fields.

  (d) Whether the document field of `a` is a prefix of the document field of `b` (structural subordination within a document family).

---

## T7 — SubspaceDisjointness (LEMMA, lemma)

The subspace identifier (the first component of the element field) permanently separates the address space into disjoint regions. No tumbler in subspace `s₁` can equal or be confused with a tumbler in subspace `s₂ ≠ s₁`.

  `(A a, b ∈ T : a.E₁ ≠ b.E₁ ⟹ a ≠ b)`

---

## T8 — AddressPermanence (INV, predicate(State, State))

If tumbler `a ∈ T` is assigned to content `c` at any point in the system's history, then for all subsequent states, `a` remains assigned to `c`. No operation removes an address from I-space. No operation changes the content at an assigned address.

---

## T9 — ForwardAllocation (INV, predicate(State, State))

Each allocator in the system controls a single ownership prefix and allocates sequentially within it. Within that sequential stream, new addresses are strictly monotonically increasing:

  `(A a, b : same_allocator(a, b) ∧ allocated_before(a, b) : a < b)`

---

## PrefixOrderingExtension — PrefixOrderingExtension (LEMMA, lemma)

Let `p₁, p₂ ∈ T` be tumblers such that `p₁ < p₂` and neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for every `a` extending `p₁` (`p₁ ≼ a`) and every `b` extending `p₂` (`p₂ ≼ b`), `a < b`.

---

## Partition monotonicity — PartitionMonotonicity (LEMMA, lemma)

Within any prefix-delimited partition of the address space, the set of allocated addresses is totally ordered by T1, and this order is consistent with the allocation order of any single allocator within that partition.

---

## T10 — PartitionIndependence (INV, predicate(Tumbler, Tumbler))

The address space is partitioned by prefix into ownership domains. Two allocators with distinct, non-nesting prefixes can allocate simultaneously, and the resulting addresses are guaranteed distinct.

Formally: let `p₁` and `p₂` be prefixes such that neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for any tumbler `a` with prefix `p₁` and any tumbler `b` with prefix `p₂`, `a ≠ b`.

---

## T10a — AllocatorDiscipline (INV, predicate(State, State))

Each allocator produces its sibling outputs exclusively by repeated application of `inc(·, 0)` — shallow increment at the last significant position. To spawn a child allocator, the parent performs one `inc(·, k')` with `k' > 0` to establish the child's prefix, then delegates further allocation to the child. The parent's own sibling stream resumes with `inc(·, 0)`.

---

## Global uniqueness — GlobalUniqueness (LEMMA, lemma)

No two distinct allocations, anywhere in the system, at any time, produce the same address.

---

## TA0 — WellDefinedAddition (PRE, requires)

For tumblers `a, w ∈ T` where `w > 0` and the action point `k` of `w` satisfies `k ≤ #a`, the result `a ⊕ w` is a well-defined tumbler in `T`.

The precondition `k ≤ #a` is essential: the constructive definition copies components `a₁, ..., aₖ₋₁` from the start position and adds `wₖ` to `aₖ`, so position `k` must exist within `a`.

---

## TA1 — WeakOrderPreservation (POST, ensures)

`(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) : a ⊕ w ≤ b ⊕ w)`, where `k` is the action point of `w`.

---

## TA1-strict — StrictOrderPreservation (POST, ensures)

`(A a, b, w : a < b ∧ w > 0 ∧ k ≥ divergence(a, b) : a ⊕ w < b ⊕ w)`, where `k` is the action point of `w` and `divergence(a, b)` is the first position at which `a` and `b` differ.

---

## TA-strict — StrictIncrease (POST, ensures)

`(A a ∈ T, w > 0 : a ⊕ w > a)` (where `a ⊕ w` is well-defined, i.e., `k ≤ #a` per TA0).

---

## TA2 — WellDefinedSubtraction (PRE, requires)

For tumblers `a, w ∈ T` where `a ≥ w`, `a ⊖ w` is a well-defined tumbler in `T`.

---

## TA3 — SubtractionPreservesOrder (POST, ensures)

`(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w < b ⊖ w)`.

---

## TA4 — MutualInverse (POST, ensures)

`(A a, w : w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊕ w) ⊖ w = a)`, where `k` is the action point of `w`.

Precondition has three parts:
- `k = #a` — the action point falls at the last component of `a`
- `#w = k` — the displacement has no trailing components beyond the action point
- `(A i : 1 ≤ i < k : aᵢ = 0)` — all components of `a` before the action point are zero

---

## Reverse inverse — ReverseInverse (LEMMA, lemma)

`(A a, w : a ≥ w ∧ w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊖ w) ⊕ w = a)`, where `k` is the action point of `w`.

---

## TA5 — HierarchicalIncrement (POST, ensures)

For tumbler `t ∈ T` and level `k ≥ 0`, there exists an operation `inc(t, k)` producing tumbler `t'` such that:

  (a) `t' > t` (strictly greater under T1),

  (b) `t'` agrees with `t` on all components before the increment point,

  (c) when `k = 0` (*sibling*): `#t' = #t`, and `t'` differs from `t` only at position `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`,

  (d) when `k > 0` (*child*): `#t' = #t + k`, the `k - 1` intermediate positions `#t + 1, ..., #t + k - 1` are set to `0` (field separators), and the final position `#t + k` is set to `1` (the first child).

**Preservation of T4:** TA5 preserves T4 when `zeros(t) + k - 1 ≤ 3`.

---

## TA6 — ZeroTumblerInvalid (INV, predicate(Tumbler))

`(A t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0) ⟹ t is not a valid address)`

Every zero tumbler is less than every positive tumbler under T1.

---

## Definition — ElementLocalDisplacement

A displacement `w` is element-local for subspace `S₁` iff `(A a ∈ S₁ : a ⊕ w` shares the document prefix and subspace identifier of `a)`. Structurally: `w` acts at positions strictly after the subspace identifier — it affects `E₂, E₃, ...` but not `E₁` or any component of the document prefix.

---

## TA7a — SubspaceClosure (POST, ensures)

Let `S₁` and `S₂` be distinct element subspaces within a document. For any element-local displacement `w`, the shift operations are closed within each subspace:

  `(A a ∈ S₁, w element-local : a ⊕ w ∈ S₁)` and symmetrically for `⊖`.

---

## TA7b — SubspaceFrame (FRAME, ensures)

An INSERT or DELETE operation within subspace `S₁` does not modify any position in a distinct subspace `S₂`:

  `(A b ∈ S₂ : post(b) = pre(b))`

where `pre(b)` and `post(b)` denote the V-space position of content `b` before and after the operation.

---

## T11 — DualSpaceSeparation (INV, predicate(State, State))

The permanence properties (T8, T9, T10) apply exclusively to I-space. The *editing shifts* — the application of `⊕` and `⊖` by INSERT and DELETE operations to modify document positions — apply exclusively to V-space; the subspace frame condition (TA7b) constrains these V-space operations. No editing operation shifts an I-space address. No operation claims permanence for a V-space position.

The operations `⊕` and `⊖` are defined on the carrier set T and are *available* in both spaces — they are arithmetic on tumblers, not inherently tied to one space. What T11 constrains is their *use by editing operations*: INSERT and DELETE apply shifts only to V-space positions.

---

## T12 — SpanWellDefined (INV, predicate(Tumbler, Tumbler))

A span `(s, ℓ)` with `ℓ > 0` denotes the set `{t ∈ T : s ≤ t < s ⊕ ℓ}`. This set is contiguous under T1 — there is no tumbler between two members that is not itself a member.

Non-emptiness follows from TA-strict: since `ℓ > 0`, TA0 gives `s ⊕ ℓ ∈ T`, and TA-strict gives `s ⊕ ℓ > s` directly.

---

## TA8 — OrthogonalDimensions (INV, predicate(Displacement))

In the 2D enfilade displacement arithmetic, V-displacements and I-displacements are added, subtracted, minimized, and maximized independently. There is no cross-dimensional operation that combines a V-value with an I-value.

  `add(⟨v₁, i₁⟩, ⟨v₂, i₂⟩) = ⟨v₁ ⊕ v₂, i₁ ⊕ i₂⟩`

  `min(⟨v₁, i₁⟩, ⟨v₂, i₂⟩) = ⟨min(v₁, v₂), min(i₁, i₂)⟩`
