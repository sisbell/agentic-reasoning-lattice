# ASN-0034 Formal Statements

*Source: ASN-0034-tumbler-algebra.md (revised 2026-03-19) — Extracted: 2026-03-19*

## Definition — ActionPoint

For a positive displacement `w = [w₁, w₂, ..., wₙ]`, the *action point* is `k = min({i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0})` — the position of the first nonzero component. The leading zeros say "stay at these hierarchical levels"; the first nonzero component says "advance here."

---

## Definition — Divergence

For tumblers `a, b ∈ T` with `a ≠ b`, `divergence(a, b)` is defined by two cases:

(i) If there exists `k ≤ min(#a, #b)` such that `aₖ ≠ bₖ` and `(A i : 1 ≤ i < k : aᵢ = bᵢ)`, then `divergence(a, b) = k` — component divergence at a shared position.

(ii) If `(A i : 1 ≤ i ≤ min(#a, #b) : aᵢ = bᵢ)` and `#a ≠ #b`, then `divergence(a, b) = min(#a, #b) + 1` — prefix divergence, where one tumbler is a proper prefix of the other.

Exactly one case applies for any `a ≠ b`.

---

## Definition — LastSignificantPosition

The *last significant position* of a tumbler `t`: when `t` has at least one nonzero component, `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})`. When every component is zero, `sig(t) = #t`.

---

## Definition — PositiveTumbler

A tumbler `t ∈ T` is *positive*, written `t > 0`, iff at least one of its components is nonzero: `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`. A tumbler is a *zero tumbler* iff every component is zero: `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.

---

## Definition — Zeros

`zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`

---

## Definition — Fields

The function `fields(t)` extracts the node, user, document, and element fields from a tumbler `t` in the form `t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`. It is well-defined and computable from `t` alone. The count `zeros(t)` uniquely determines the hierarchical level:

- `zeros(t) = 0`: `t` is a node address (node field only)
- `zeros(t) = 1`: `t` is a user address (node and user fields)
- `zeros(t) = 2`: `t` is a document address (node, user, and document fields)
- `zeros(t) = 3`: `t` is an element address (all four fields)

---

## Definition — TumblerAdd

Let `a = [a₁, ..., aₘ]` and `w = [w₁, ..., wₙ]` with `w > 0`. With action point `k`:

```
         ⎧ aᵢ           if i < k        (copy from start)
rᵢ   =  ⎨ aₖ + wₖ      if i = k        (single-component advance)
         ⎩ wᵢ           if i > k        (copy from displacement)
```

The result `a ⊕ w = [r₁, ..., rₚ]` has length `p = n = #w` (*result-length identity*: `#(a ⊕ w) = #w`).

**Precondition:** `k ≤ m` — the displacement's action point must fall within the start position's length.

**No carry propagation.** The sum `aₖ + wₖ` is a single natural-number addition with no carry into position `k − 1`.

**Tail replacement.** Components of `a` at positions `k + 1, ..., m` are discarded; positions after `k` in the result come entirely from `w`.

---

## Definition — TumblerSub

Given an end position `a` and a displacement `w`, zero-pad the shorter to the length of the longer. If the zero-padded sequences agree at every position, the result is the zero tumbler of length `max(#a, #w)`. Otherwise, let `k` be the first position where `a` and `w` differ (treating missing components as zero):

```
         ⎧ 0             if i < k        (these levels matched — zero them)
rᵢ   =  ⎨ aₖ - wₖ      if i = k        (reverse the advance)
         ⎩ aᵢ           if i > k        (copy from end position)
```

The result has length `max(#a, #w)`.

**Precondition:** `a ≥ w` — when `a ≠ w`, at the divergence point (after zero-padding) `aₖ ≥ wₖ`.

---

## T0(a) — UnboundedComponentValues (AXIOM, predicate)

`(A t ∈ T, i : 1 ≤ i ≤ #t : (A M ∈ ℕ :: (E t' ∈ T :: t' agrees with t except t'.dᵢ > M)))`

For every tumbler and every component position, there exists a tumbler whose value at that position exceeds any given bound.

---

## T0(b) — UnboundedLength (AXIOM, predicate)

`(A n ∈ ℕ : n ≥ 1 : (E t ∈ T :: #t ≥ n))`

For every bound, a tumbler of at least that length exists in T.

---

## T1 — LexicographicOrder (AXIOM, predicate)

For tumblers `a = a₁. ... .aₘ` and `b = b₁. ... .bₙ`, define `a < b` iff there exists `k ≥ 1` such that `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either:

(i) `k ≤ min(m, n)` and `aₖ < bₖ`, or

(ii) `k = m + 1 ≤ n` (that is, `a` is a proper prefix of `b`).

T1 gives a total order: for any `a, b ∈ T`, exactly one of `a < b`, `a = b`, `a > b` holds.

---

## T2 — IntrinsicComparison (AXIOM, predicate)

The order relation T1 is computable from the two tumblers alone, without consulting any external data structure. The comparison examines at most `min(#a, #b)` component pairs.

---

## T3 — CanonicalRepresentation (AXIOM, predicate)

`(A a, b ∈ T : a₁ = b₁ ∧ ... ∧ aₙ = bₙ ∧ #a = #b ≡ a = b)`

---

## T4 — HierarchicalParsing (AXIOM, predicate)

Every tumbler `t ∈ T` used as an address contains at most three zero-valued components, appearing in order as field separators, every non-separator component is strictly positive, and every field present in the address has at least one component.

Formally, if `t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`, then:

- `(A i : 1 ≤ i ≤ α : Nᵢ > 0)`
- `(A j : 1 ≤ j ≤ β : Uⱼ > 0)`
- `(A k : 1 ≤ k ≤ γ : Dₖ > 0)`
- `(A l : 1 ≤ l ≤ δ : Eₗ > 0)`
- `α ≥ 1`, `β ≥ 1` when present, `γ ≥ 1` when present, `δ ≥ 1` when present

Equivalently: no two zeros are adjacent, the tumbler does not begin with zero, and the tumbler does not end with zero.

---

## T5 — ContiguousSubtrees (LEMMA, lemma)

For any tumbler prefix `p`, the set `{t ∈ T : p ≼ t}` (where `≼` denotes "is a prefix of") forms a contiguous interval under T1:

`[p ≼ a ∧ p ≼ c ∧ a ≤ b ≤ c ⟹ p ≼ b]`

---

## T6 — DecidableContainment (COROLLARY, lemma)

*Corollary of T4.*

For any two tumblers `a, b ∈ T`, the following are decidable from the addresses alone:

(a) Whether `a` and `b` share the same node field.

(b) Whether `a` and `b` share the same node and user fields.

(c) Whether `a` and `b` share the same node, user, and document-lineage fields.

(d) Whether the document field of `a` is a prefix of the document field of `b` (structural subordination within a document family).

---

## T7 — SubspaceDisjointness (COROLLARY, lemma)

*Corollary of T3 + T4.*

`(A a, b ∈ T : a.E₁ ≠ b.E₁ ⟹ a ≠ b)`

The subspace identifier (the first component of the element field) permanently separates the address space into disjoint regions.

---

## T8 — AllocationPermanence (AXIOM, predicate)

If tumbler `a ∈ T` has been allocated at any point in the system's history, then for all subsequent states, `a` remains in the set of allocated addresses. No operation removes an allocated address from the address space. The set of allocated addresses is monotonically non-decreasing.

---

## T9 — ForwardAllocation (LEMMA, lemma)

`(A a, b : same_allocator(a, b) ∧ allocated_before(a, b) : a < b)`

Within each allocator's sequential stream, new addresses are strictly monotonically increasing. T9 is scoped to a single allocator's sequential stream; it does not hold globally across distinct allocators.

---

## T10 — PartitionIndependence (AXIOM, predicate)

Let `p₁` and `p₂` be prefixes such that neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for any tumbler `a` with prefix `p₁` and any tumbler `b` with prefix `p₂`, `a ≠ b`.

---

## T10a — AllocatorDiscipline (AXIOM, predicate)

Each allocator produces its sibling outputs exclusively by repeated application of `inc(·, 0)` — shallow increment at the last significant position. To spawn a child allocator, the parent performs one `inc(·, k')` with `k' > 0` to establish the child's prefix, then delegates further allocation to the child. The parent's own sibling stream resumes with `inc(·, 0)`.

Since `inc(·, 0)` preserves length (TA5(c)), all sibling outputs from a single allocator have the same length. The `k > 0` operation is reserved exclusively for child-spawning.

---

## T12 — SpanWellDefined (AXIOM, predicate)

A span `(s, ℓ)` is well-formed when `ℓ > 0` and the action point `k` of `ℓ` satisfies `k ≤ #s` (the TA0 precondition for `s ⊕ ℓ`). Equivalently, the number of leading zeros in `ℓ` must be strictly less than `#s`. A well-formed span denotes the set `{t ∈ T : s ≤ t < s ⊕ ℓ}`. This set is contiguous under T1. Non-emptiness follows from TA-strict: `s ⊕ ℓ > s`, so the interval `[s, s ⊕ ℓ)` contains at least `s`.

---

## TA0 — AdditionWellDefined (PRE, requires)

For tumblers `a, w ∈ T` where `w > 0` and the action point `k` of `w` satisfies `k ≤ #a`, the result `a ⊕ w` is a well-defined tumbler in `T`.

---

## TA1 — OrderPreservationAddWeak (LEMMA, lemma)

`(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) : a ⊕ w ≤ b ⊕ w)`, where `k` is the action point of `w`.

---

## TA1-strict — OrderPreservationAddStrict (LEMMA, lemma)

`(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) ∧ k ≥ divergence(a, b) : a ⊕ w < b ⊕ w)`, where `k` is the action point of `w`.

When `k < divergence(a, b)`, both operands agree at position `k`, the original divergence is erased by tail replacement, and `a ⊕ w = b ⊕ w`. TA1 (weak) covers this case; TA1-strict makes no claim about it.

---

## TA-strict — StrictIncrease (LEMMA, lemma)

`(A a ∈ T, w > 0 : a ⊕ w > a)` (where `a ⊕ w` is well-defined, i.e., `k ≤ #a` per TA0).

*Verification:* Let `k` be the action point of `w`. By TumblerAdd, `(a ⊕ w)ᵢ = aᵢ` for `i < k`, and `(a ⊕ w)ₖ = aₖ + wₖ`. Since `wₖ > 0`, `aₖ + wₖ > aₖ`. By T1 case (i), `a ⊕ w > a`.

---

## TA2 — SubtractionWellDefined (PRE, requires)

For tumblers `a, w ∈ T` where `a ≥ w`, `a ⊖ w` is a well-defined tumbler in `T`.

---

## TA3 — OrderPreservationSubWeak (LEMMA, lemma)

`(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w ≤ b ⊖ w)`

---

## TA3-strict — OrderPreservationSubStrict (LEMMA, lemma)

`(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b : a ⊖ w < b ⊖ w)`

---

## TA4 — PartialInverse (LEMMA, lemma)

`(A a, w : w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊕ w) ⊖ w = a)`, where `k` is the action point of `w`.

**Preconditions:**
- `k = #a` — action point falls at the last component of `a`
- `#w = k` — displacement has no trailing components beyond the action point
- `(A i : 1 ≤ i < k : aᵢ = 0)` — all components of `a` before the action point are zero

**Reverse inverse (corollary).** Under the same preconditions with additionally `a ≥ w`:

`(A a, w : a ≥ w ∧ w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊖ w) ⊕ w = a)`

---

## TA5 — HierarchicalIncrement (AXIOM, predicate)

For tumbler `t ∈ T` and level `k ≥ 0`, there exists an operation `inc(t, k)` producing tumbler `t'` such that:

(a) `t' > t` (strictly greater under T1)

(b) `t'` agrees with `t` on all components before the increment point

(c) when `k = 0` (*sibling*): `#t' = #t`, and `t'` differs from `t` only at position `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`

(d) when `k > 0` (*child*): `#t' = #t + k`, the `k − 1` intermediate positions `#t + 1, ..., #t + k − 1` are set to `0` (field separators), and the final position `#t + k` is set to `1` (the first child)

**T4 preservation:** TA5 preserves T4 when `k = 0` (unconditionally), `k = 1` (when `zeros(t) ≤ 3`), `k = 2` (when `zeros(t) ≤ 2`). For `k ≥ 3` the appended sequence contains adjacent zeros, violating T4.

---

## TA6 — ZeroTumblerSentinel (AXIOM, predicate)

`(A t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0) ⟹ t is not a valid address)`

`(A s, t ∈ T : (A i : 1 ≤ i ≤ #s : sᵢ = 0) ∧ (E j : 1 ≤ j ≤ #t : tⱼ > 0) ⟹ s < t)`

Under T3, `[0]`, `[0, 0]`, `[0, 0, 0]`, etc. are distinct elements of T forming a chain `[0] < [0, 0] < [0, 0, 0] < ...` by the prefix rule. There is no single "zero tumbler"; there are infinitely many all-zero tumblers.

---

## TA7a — SubspaceClosure (LEMMA, lemma)

The canonical representation for shift arithmetic is the *ordinal-only* formulation: a position in subspace `S` with identifier `N` and ordinal `o = [o₁, ..., oₘ]` (`m ≥ 1`) is represented as the tumbler `o` for arithmetic purposes, with `N` held as structural context. An element-local displacement is a positive tumbler `w` with action point `k` satisfying `1 ≤ k ≤ m`. In this formulation:

`(A o ∈ S, w > 0 : k ≤ #o ⟹ o ⊕ w ∈ S)`

`(A o ∈ S, w > 0 : o ≥ w ⟹ o ⊖ w ∈ S ∪ Z)`

where `Z` is the set of zero tumblers.

---

## TA-assoc — AdditionAssociative (LEMMA, lemma)

`(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)` whenever both sides are well-defined.

Let `k_b` and `k_c` be the action points of `b` and `c`. Three cases:
- When `k_b < k_c`: both sides produce `aᵢ` for `i < k_b`, `aₖ_b + bₖ_b` at `k_b`, `bᵢ` for `k_b < i < k_c`, `bₖ_c + cₖ_c` at `k_c`, `cᵢ` beyond.
- When `k_b = k_c = k`: both sides produce `aₖ + bₖ + cₖ` at `k`, `cᵢ` beyond.
- When `k_b > k_c`: both sides produce `aₖ_c + cₖ_c` at `k_c`, `cᵢ` beyond.

---

## TA-LC — LeftCancellation (LEMMA, lemma)

If `a ⊕ x = a ⊕ y` with both sides well-defined (TA0 satisfied for both), then `x = y`.

---

## TA-RC — RightCancellationFailure (LEMMA, lemma)

There exist tumblers `a, b, w` with `a ≠ b` and `a ⊕ w = b ⊕ w` (both sides well-defined).

*Witness:* `a = [1, 3, 5]`, `b = [1, 3, 7]`, `w = [0, 2, 4]` (action point `k = 2`): `a ⊕ w = b ⊕ w = [1, 5, 4]`.

---

## TA-MTO — ManyToOne (LEMMA, lemma)

For any displacement `w` with action point `k` and any tumblers `a, b` with `#a ≥ k` and `#b ≥ k`:

`a ⊕ w = b ⊕ w  ⟺  (A i : 1 ≤ i ≤ k : aᵢ = bᵢ)`

---

## D0 — DisplacementWellDefined (PRE, requires)

`a < b`, and `divergence(a, b) ≤ #a`.

D0 ensures `b ⊖ a` is a well-defined positive tumbler and that `a ⊕ (b ⊖ a)` is defined (TA0 satisfied). When `a` is a proper prefix of `b`, `divergence(a, b) = #a + 1 > #a`, so D0 is not satisfied and no valid displacement exists.

---

## D1 — DisplacementRoundTrip (LEMMA, lemma)

For tumblers `a, b ∈ T` with `a < b`, `divergence(a, b) ≤ #a`, and `#a ≤ #b`:

`a ⊕ (b ⊖ a) = b`

---

## D2 — DisplacementUnique (COROLLARY, lemma)

*Corollary of D1 + TA-LC.*

Under D1's preconditions (`a < b`, `divergence(a, b) ≤ #a`, `#a ≤ #b`), if `a ⊕ w = b` then `w = b ⊖ a`.
