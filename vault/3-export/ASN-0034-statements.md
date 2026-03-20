# ASN-0034 Formal Statements

*Source: ASN-0034-tumbler-algebra.md (revised 2026-03-19) — Extracted: 2026-03-19*

## Definition — ActionPoint

For a positive displacement `w = [w₁, w₂, ..., wₙ]`, the *action point* is `k = min({i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0})` — the position of the first nonzero component.

## Definition — PositiveTumbler

A tumbler `t ∈ T` is *positive*, written `t > 0`, iff at least one of its components is nonzero: `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`. A tumbler is a *zero tumbler* iff every component is zero: `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.

## Definition — PrefixRelation

`p ≼ t` ("p is a prefix of t") iff `#p ≤ #t` and `(A i : 1 ≤ i ≤ #p : pᵢ = tᵢ)`.

## Definition — ZerosCount

`zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`.

## Definition — LastSigPos

`sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})` when `t` has at least one nonzero component. When every component is zero, `sig(t) = #t`.

## Definition — Divergence

For tumblers `a, b ∈ T` with `a ≠ b`, `divergence(a, b)` is defined by two cases:

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

The result `a ⊕ w = [r₁, ..., rₚ]` has length `p = max(k - 1, 0) + (n - k + 1) = n = #w`.

*Result-length identity:* `#(a ⊕ w) = #w`.

Precondition: `k ≤ m` — the displacement's action point must fall within the start position's length.

Properties of this definition:
- **No carry propagation.** The sum `aₖ + wₖ` at the action point is a single natural-number addition with no carry into position `k − 1`.
- **Tail replacement, not tail addition.** Components after the action point come entirely from `w`; the start position's components at positions `k + 1, ..., m` are discarded.
- **Many-to-one.** Because trailing components of `a` are discarded, distinct start positions can produce the same result.

## Definition — TumblerSub

Given end position `a` and displacement `w`, conceptually zero-pad the shorter to the length of the longer before scanning for divergence. When the zero-padded sequences agree at every position (no divergence exists), the result is the zero tumbler of length `max(#a, #w)`. Otherwise, let `k` be the first position where `a` and `w` differ (treating missing components as zero):

```
         ⎧ 0             if i < k        (these levels matched — zero them)
rᵢ   =  ⎨ aₖ - wₖ      if i = k        (reverse the advance)
         ⎩ aᵢ           if i > k        (copy from end position)
```

The result has length `max(#a, #w)`.

Precondition: `a ≥ w` — when `a ≠ w`, at the divergence point (after zero-padding) `aₖ ≥ wₖ`.

## Definition — Fields

`fields(t)` extracts the node, user, document, and element fields of a valid address tumbler. If `t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`, then:
- `fields(t).node = [N₁, ..., Nₐ]`
- `fields(t).user = [U₁, ..., Uᵦ]` (when `zeros(t) ≥ 1`)
- `fields(t).doc = [D₁, ..., Dᵧ]` (when `zeros(t) ≥ 2`)
- `fields(t).elem = [E₁, ..., Eδ]` (when `zeros(t) = 3`)

---

## T0(a) — UnboundedComponents (axiom, predicate)

`(A t ∈ T, i : 1 ≤ i ≤ #t : (A M ∈ ℕ :: (E t' ∈ T :: t' agrees with t except t'.dᵢ > M)))`.

## T0(b) — UnboundedDepth (axiom, predicate)

`(A n ∈ ℕ : n ≥ 1 : (E t ∈ T :: #t ≥ n))`.

## T1 — LexOrder (axiom, predicate)

For tumblers `a = a₁. ... .aₘ` and `b = b₁. ... .bₙ`, define `a < b` iff there exists `k ≥ 1` such that `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either:

(i) `k ≤ min(m, n)` and `aₖ < bₖ`, or

(ii) `k = m + 1 ≤ n` (that is, `a` is a proper prefix of `b`).

## T2 — IntrinsicComparison (axiom, predicate)

The order relation T1 is computable from the two tumblers alone, without consulting any external data structure. The comparison examines at most `min(#a, #b)` component pairs.

## T3 — CanonicalForm (axiom, predicate)

`(A a, b ∈ T : a₁ = b₁ ∧ ... ∧ aₙ = bₙ ∧ #a = #b ≡ a = b)`.

## T4 — HierarchicalParsing (axiom, predicate)

Every tumbler `t ∈ T` used as an address contains at most three zero-valued components, appearing in order as field separators, every non-separator component is strictly positive, and every field present in the address has at least one component.

Formally, if `t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`, then:

`(A i : 1 ≤ i ≤ α : Nᵢ > 0)`, `(A j : 1 ≤ j ≤ β : Uⱼ > 0)`, `(A k : 1 ≤ k ≤ γ : Dₖ > 0)`, `(A l : 1 ≤ l ≤ δ : Eₗ > 0)`, and `α ≥ 1`, `β ≥ 1` when present, `γ ≥ 1` when present, `δ ≥ 1` when present.

The count of zero-valued components uniquely determines the hierarchical level:
- `zeros(t) = 0`: `t` is a node address (node field only)
- `zeros(t) = 1`: `t` is a user address (node and user fields)
- `zeros(t) = 2`: `t` is a document address (node, user, and document fields)
- `zeros(t) = 3`: `t` is an element address (all four fields)

Equivalently, the non-empty field constraint requires: no two zeros are adjacent, the tumbler does not begin with zero, and the tumbler does not end with zero.

## T5 — ContiguousSubtrees (lemma, lemma)

For any tumbler prefix `p`, the set `{t ∈ T : p ≼ t}` forms a contiguous interval under T1:

`[p ≼ a ∧ p ≼ c ∧ a ≤ b ≤ c ⟹ p ≼ b]`

## T6 — DecidableContainment (corollary, lemma)

For any two tumblers `a, b ∈ T`, the following are decidable from the addresses alone:

(a) Whether `a` and `b` share the same node field.

(b) Whether `a` and `b` share the same node and user fields.

(c) Whether `a` and `b` share the same node, user, and document-lineage fields.

(d) Whether the document field of `a` is a prefix of the document field of `b` (structural subordination within a document family).

## T7 — SubspaceDisjointness (corollary, lemma)

`(A a, b ∈ T : a.E₁ ≠ b.E₁ ⟹ a ≠ b)`

where `a.E₁` denotes the first component of the element field of `a`.

## T8 — AllocationPermanence (axiom, predicate)

If tumbler `a ∈ T` has been allocated at any point in the system's history, then for all subsequent states, `a` remains in the set of allocated addresses. No operation removes an allocated address from the address space. The set of allocated addresses is monotonically non-decreasing.

## T9 — ForwardAllocation (lemma, lemma)

T10a defines the allocation mechanism: each allocator advances by `inc(·, 0)`, incrementing by exactly 1 at the last significant position. Since `inc` produces a strictly greater tumbler at each step (TA5(a)), within each allocator's sequential stream, new addresses are strictly monotonically increasing:

`(A a, b : same_allocator(a, b) ∧ allocated_before(a, b) : a < b)`

## T10 — PartitionIndependence (axiom, predicate)

Let `p₁` and `p₂` be prefixes such that neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for any tumbler `a` with prefix `p₁` and any tumbler `b` with prefix `p₂`, `a ≠ b`.

## T10a — AllocatorDiscipline (axiom, predicate)

Each allocator produces its sibling outputs exclusively by repeated application of `inc(·, 0)` — shallow increment at the last significant position. To spawn a child allocator, the parent performs one `inc(·, k')` with `k' > 0` to establish the child's prefix, then delegates further allocation to the child. The parent's own sibling stream resumes with `inc(·, 0)`.

Consequence: since `inc(·, 0)` preserves length (TA5(c)), all sibling outputs from a single allocator have the same length. The `k > 0` operation is reserved exclusively for child-spawning.

## T12 — SpanWellDefined (axiom, predicate)

A span `(s, ℓ)` is well-formed when `ℓ > 0` and the action point `k` of `ℓ` satisfies `k ≤ #s` (the TA0 precondition for `s ⊕ ℓ`). Equivalently, the number of leading zeros in `ℓ` must be strictly less than `#s`. A well-formed span denotes the set `{t ∈ T : s ≤ t < s ⊕ ℓ}`.

Non-emptiness follows from TA-strict: since `ℓ > 0` and `k ≤ #s`, TA0 gives `s ⊕ ℓ ∈ T`, and TA-strict gives `s ⊕ ℓ > s`. The interval `[s, s ⊕ ℓ)` contains at least `s` itself.

## TA0 — AddWellDefined (axiom, requires)

For tumblers `a, w ∈ T` where `w > 0` and the action point `k` of `w` satisfies `k ≤ #a`, the result `a ⊕ w` is a well-defined tumbler in `T`.

## TA1 — AddOrderWeak (axiom, lemma)

`(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) : a ⊕ w ≤ b ⊕ w)`, where `k` is the action point of `w`.

## TA1-strict — AddOrderStrict (axiom, lemma)

`(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) ∧ k ≥ divergence(a, b) : a ⊕ w < b ⊕ w)`, where `k` is the action point of `w`.

When `k < divergence(a, b)`, both operands agree at position `k`, both get the same `wₖ` added, and both copy the same tail from `w` afterward — order degrades to equality, never reversal.

## TA-strict — StrictAdvance (axiom, lemma)

`(A a ∈ T, w > 0 : a ⊕ w > a)` (where `a ⊕ w` is well-defined, i.e., `k ≤ #a` per TA0).

## TA2 — SubWellDefined (axiom, requires)

For tumblers `a, w ∈ T` where `a ≥ w`, `a ⊖ w` is a well-defined tumbler in `T`.

## TA3 — SubOrderWeak (axiom, lemma)

`(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w ≤ b ⊖ w)`.

## TA3-strict — SubOrderStrict (axiom, lemma)

`(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b : a ⊖ w < b ⊖ w)`.

## TA4 — PartialInverse (axiom, lemma)

`(A a, w : w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊕ w) ⊖ w = a)`, where `k` is the action point of `w`.

Precondition breakdown:
- `k = #a` — the action point falls at the last component of `a`
- `#w = k` — the displacement has no trailing components beyond the action point
- `(A i : 1 ≤ i < k : aᵢ = 0)` — all components of `a` before the action point are zero

Reverse direction (*Corollary*): `(A a, w : a ≥ w ∧ w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊖ w) ⊕ w = a)`.

## TA5 — HierarchicalIncrement (axiom, function)

For tumbler `t ∈ T` and level `k ≥ 0`, there exists an operation `inc(t, k)` producing tumbler `t'` such that:

(a) `t' > t` (strictly greater under T1),

(b) `t'` agrees with `t` on all components before the increment point,

(c) when `k = 0` (*sibling*): `#t' = #t`, and `t'` differs from `t` only at position `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`,

(d) when `k > 0` (*child*): `#t' = #t + k`, the `k - 1` intermediate positions `#t + 1, ..., #t + k - 1` are set to `0` (field separators), and the final position `#t + k` is set to `1` (the first child).

T4-preservation: `k = 0` always preserves T4; `k = 1` preserves T4 when `zeros(t) ≤ 3`; `k = 2` preserves T4 when `zeros(t) ≤ 2`; `k ≥ 3` violates T4 (adjacent zeros, empty field).

## TA6 — ZeroSentinel (axiom, predicate)

`(A t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0) ⟹ t is not a valid address)`

`(A s, t ∈ T : (A i : 1 ≤ i ≤ #s : sᵢ = 0) ∧ (E j : 1 ≤ j ≤ #t : tⱼ > 0) ⟹ s < t)`

## TA7a — SubspaceClosure (axiom, lemma)

The canonical representation for shift arithmetic is the *ordinal-only* formulation: a position in subspace `S` with identifier `N` and ordinal `o = [o₁, ..., oₘ]` (where `m ≥ 1`) is represented as the tumbler `o` for arithmetic purposes, with `N` held as structural context. An element-local displacement is a positive tumbler `w` with action point `k` satisfying `1 ≤ k ≤ m`. In this formulation:

`(A o ∈ S, w > 0 : k ≤ #o ⟹ o ⊕ w ∈ S)`

`(A o ∈ S, w > 0 : o ≥ w ⟹ o ⊖ w ∈ S ∪ Z)`

where `Z` is the set of zero tumblers.

## TA-assoc — AddAssociative (axiom, lemma)

Addition is associative where both compositions are defined: `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)` whenever both sides are well-defined.

Three cases: when `k_b < k_c`, when `k_b = k_c`, when `k_b > k_c` (where `k_b`, `k_c` are action points of `b` and `c`). On the intersection of their domains, the values agree.

## TA-LC — LeftCancellation (lemma, lemma)

If `a ⊕ x = a ⊕ y` with both sides well-defined (TA0 satisfied for both), then `x = y`.

## TA-RC — RightCancellationFailure (lemma, lemma)

There exist tumblers `a, b, w` with `a ≠ b` and `a ⊕ w = b ⊕ w` (both sides well-defined).

## TA-MTO — ManyToOne (lemma, lemma)

For any displacement `w` with action point `k` and any tumblers `a, b` with `#a ≥ k` and `#b ≥ k`:

`a ⊕ w = b ⊕ w  ⟺  (A i : 1 ≤ i ≤ k : aᵢ = bᵢ)`

Forward: if `aᵢ = bᵢ` for all `1 ≤ i ≤ k`, then for `i < k` both results copy from start (equal), at `i = k` both compute `aₖ + wₖ = bₖ + wₖ`, and for `i > k` both copy from `w` — results equal by T3.

Converse: for `i < k`, position falls in the copy-from-start region, so `(a ⊕ w)ᵢ = aᵢ` and `(b ⊕ w)ᵢ = bᵢ`; equality gives `aᵢ = bᵢ`. At `i = k`: `aₖ + wₖ = bₖ + wₖ` gives `aₖ = bₖ` by cancellation in ℕ. Components after `k` are unconstrained.
