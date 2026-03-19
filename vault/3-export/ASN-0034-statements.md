# ASN-0034 Formal Statements

*Source: ASN-0034-tumbler-algebra.md (revised 2026-03-13) — Extracted: 2026-03-19*

## Definition — ActionPoint

For a positive displacement `w = [w₁, w₂, ..., wₙ]`, the *action point* is `k = min({i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0})` — the position of the first nonzero component.

## Definition — LastSigPos

When `t` has at least one nonzero component, `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})`. When every component is zero, `sig(t) = #t`.

## Definition — Divergence

For tumblers `a, b ∈ T` with `a ≠ b`, `divergence(a, b)` is:

  (i) If there exists `k ≤ min(#a, #b)` such that `aₖ ≠ bₖ` and `(A i : 1 ≤ i < k : aᵢ = bᵢ)`, then `divergence(a, b) = k`.

  (ii) If `(A i : 1 ≤ i ≤ min(#a, #b) : aᵢ = bᵢ)` and `#a ≠ #b`, then `divergence(a, b) = min(#a, #b) + 1`.

Exactly one case applies for any `a ≠ b`.

## Definition — IsPositive

A tumbler `t ∈ T` is *positive*, written `t > 0`, iff `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`. A tumbler is a *zero tumbler* iff `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.

## Definition — ZeroCount

`zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`

## Definition — IsPrefix

`p ≼ t` holds iff `#t ≥ #p` and `(A i : 1 ≤ i ≤ #p : tᵢ = pᵢ)`.

## Definition — TumblerAdd

Let `a = [a₁, ..., aₘ]` and `w = [w₁, ..., wₙ]` with `w > 0`. Let `k` be the action point of `w`. Precondition: `k ≤ m`.

```
         ⎧ aᵢ           if i < k
rᵢ   =  ⎨ aₖ + wₖ      if i = k
         ⎩ wᵢ           if i > k
```

Result `a ⊕ w = [r₁, ..., rₙ]` has length `#w` (*result-length identity*: `#(a ⊕ w) = #w`).

## Definition — TumblerSub

Given `a` and `w` with `a ≥ w`. Zero-pad the shorter to length `max(#a, #w)`. If the zero-padded sequences agree at every position, result is the zero tumbler of length `max(#a, #w)`. Otherwise let `k` be the first position where `a` and `w` differ (treating missing components as zero):

```
         ⎧ 0             if i < k
rᵢ   =  ⎨ aₖ - wₖ      if i = k
         ⎩ aᵢ           if i > k
```

Result has length `max(#a, #w)`.

---

## T0(a) — UnboundedComponents (AX, axiom)

`(A t ∈ T, i : 1 ≤ i ≤ #t : (A M ∈ ℕ :: (E t' ∈ T :: t' agrees with t except t'.dᵢ > M)))`.

## T0(b) — UnboundedLength (AX, axiom)

`(A n ∈ ℕ : n ≥ 1 : (E t ∈ T :: #t ≥ n))`.

## T1 — LexOrder (DEF, predicate)

For tumblers `a = a₁. ... .aₘ` and `b = b₁. ... .bₙ`, define `a < b` iff there exists `k ≥ 1` such that `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either:

  (i) `k ≤ min(m, n)` and `aₖ < bₖ`, or

  (ii) `k = m + 1 ≤ n` (that is, `a` is a proper prefix of `b`).

## T2 — IntrinsicComparison (INV, predicate)

The order relation T1 is computable from the two tumblers alone, without consulting any external data structure. The comparison examines at most `min(#a, #b)` component pairs.

## T3 — CanonicalForm (AX, predicate)

`(A a, b ∈ T : a₁ = b₁ ∧ ... ∧ aₙ = bₙ ∧ #a = #b ≡ a = b)`.

## T4 — HierarchicalParsing (INV, predicate)

Every tumbler `t ∈ T` used as an address contains at most three zero-valued components appearing in order as field separators, every non-separator component is strictly positive, and every present field has at least one component. Formally, if `t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`, then:

  `(A i : 1 ≤ i ≤ α : Nᵢ > 0)`, `(A j : 1 ≤ j ≤ β : Uⱼ > 0)`, `(A k : 1 ≤ k ≤ γ : Dₖ > 0)`, `(A l : 1 ≤ l ≤ δ : Eₗ > 0)`

  and `α ≥ 1`, `β ≥ 1` when present, `γ ≥ 1` when present, `δ ≥ 1` when present.

Equivalently: no two zeros are adjacent, the tumbler does not begin with zero, and the tumbler does not end with zero.

The zero count uniquely determines the hierarchical level:

  - `zeros(t) = 0`: `t` is a node address
  - `zeros(t) = 1`: `t` is a user address
  - `zeros(t) = 2`: `t` is a document address
  - `zeros(t) = 3`: `t` is an element address

## T5 — ContiguousSubtrees (LEMMA, lemma)

For any tumbler prefix `p`, the set `{t ∈ T : p ≼ t}` forms a contiguous interval under T1:

  `[p ≼ a ∧ p ≼ c ∧ a ≤ b ≤ c ⟹ p ≼ b]`

## T6 — DecidableContainment (LEMMA, lemma)

For any two tumblers `a, b ∈ T`, the following are decidable from the addresses alone:

  (a) Whether `a` and `b` share the same node field.

  (b) Whether `a` and `b` share the same node and user fields.

  (c) Whether `a` and `b` share the same node, user, and document-lineage fields.

  (d) Whether the document field of `a` is a prefix of the document field of `b` (structural subordination within a document family).

## T7 — SubspaceDisjointness (LEMMA, lemma)

`(A a, b ∈ T : a.E₁ ≠ b.E₁ ⟹ a ≠ b)`

where `a.E₁` denotes the first component of the element field of `a`.

## T8 — AllocationPermanence (INV, predicate)

If tumbler `a ∈ T` has been allocated at any point in the system's history, then for all subsequent states, `a` remains in the set of allocated addresses. No operation removes an allocated address from the address space. The set of allocated addresses is monotonically non-decreasing.

## T9 — ForwardAllocation (LEMMA, lemma)

`(A a, b : same_allocator(a, b) ∧ allocated_before(a, b) : a < b)`

Within each allocator's sequential stream, new addresses are strictly monotonically increasing.

## T10 — PartitionIndependence (LEMMA, lemma)

Let `p₁` and `p₂` be prefixes such that `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`. Then for any tumbler `a` with `p₁ ≼ a` and any tumbler `b` with `p₂ ≼ b`, `a ≠ b`.

## T10a — AllocatorDiscipline (INV, predicate)

Each allocator produces its sibling outputs exclusively by repeated application of `inc(·, 0)`. To spawn a child allocator, the parent performs one `inc(·, k')` with `k' > 0` to establish the child's prefix, then delegates further allocation to the child. The parent's own sibling stream resumes with `inc(·, 0)`.

## T12 — SpanWellDefined (DEF, predicate)

A span `(s, ℓ)` is well-formed when `ℓ > 0` and the action point `k` of `ℓ` satisfies `k ≤ #s`. Equivalently, the number of leading zeros in `ℓ` must be strictly less than `#s`. A well-formed span denotes the set `{t ∈ T : s ≤ t < s ⊕ ℓ}`.

## TA0 — AddWellDefined (PRE, requires)

For tumblers `a, w ∈ T` where `w > 0` and the action point `k` of `w` satisfies `k ≤ #a`, the result `a ⊕ w` is a well-defined tumbler in `T`.

## TA1 — AddOrderPreservation (LEMMA, lemma)

`(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) : a ⊕ w ≤ b ⊕ w)`, where `k` is the action point of `w`.

## TA1-strict — AddStrictOrderPreservation (LEMMA, lemma)

`(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) ∧ k ≥ divergence(a, b) : a ⊕ w < b ⊕ w)`, where `k` is the action point of `w`.

## TA-strict — AddStrictIncrease (LEMMA, lemma)

`(A a ∈ T, w > 0 : a ⊕ w > a)`, where `a ⊕ w` is well-defined (`k ≤ #a` per TA0).

## TA2 — SubWellDefined (PRE, requires)

For tumblers `a, w ∈ T` where `a ≥ w`, `a ⊖ w` is a well-defined tumbler in `T`.

## TA3 — SubOrderPreservation (LEMMA, lemma)

`(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w ≤ b ⊖ w)`.

## TA3-strict — SubStrictOrderPreservation (LEMMA, lemma)

`(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b : a ⊖ w < b ⊖ w)`.

## TA4 — PartialInverse (LEMMA, lemma)

`(A a, w : w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊕ w) ⊖ w = a)`, where `k` is the action point of `w`.

**Corollary (ReverseInverse).** `(A a, w : a ≥ w ∧ w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊖ w) ⊕ w = a)`, where `k` is the action point of `w`.

## TA5 — HierarchicalIncrement (DEF, function)

For tumbler `t ∈ T` and level `k ≥ 0`, `inc(t, k)` produces `t'` such that:

  (a) `t' > t`

  (b) `t'` agrees with `t` on all components before the increment point

  (c) when `k = 0`: `#t' = #t`, and `t'` differs from `t` only at position `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`

  (d) when `k > 0`: `#t' = #t + k`, positions `#t + 1, ..., #t + k - 1` are set to `0`, and position `#t + k` is set to `1`

**T4-preservation constraint.** `inc(t, k)` preserves T4 when:
  - `k = 0`: unconditionally
  - `k = 1`: when `zeros(t) ≤ 3`
  - `k = 2`: when `zeros(t) ≤ 2`
  - `k ≥ 3`: never (produces adjacent zeros)

## TA6 — ZeroSentinel (AX, predicate)

`(A t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0) ⟹ t is not a valid address)`

`(A s, t ∈ T : (A i : 1 ≤ i ≤ #s : sᵢ = 0) ∧ (E j : 1 ≤ j ≤ #t : tⱼ > 0) ⟹ s < t)`

## TA7a — SubspaceClosure (LEMMA, lemma)

A position in subspace `S` with identifier `N` and ordinal `o = [o₁, ..., oₘ]` (`m ≥ 1`) is represented as the tumbler `o` for arithmetic purposes, with `N` held as structural context. An element-local displacement is a positive tumbler `w` with action point `k` satisfying `1 ≤ k ≤ m`. Let `Z` be the set of zero tumblers.

  `(A o ∈ S, w > 0 : k ≤ #o ⟹ o ⊕ w ∈ S)`

  `(A o ∈ S, w > 0 : o ≥ w ⟹ o ⊖ w ∈ S ∪ Z)`

---

## PrefixOrderingExtension — PrefixOrderingExtension (LEMMA, lemma)

Let `p₁, p₂ ∈ T` such that `p₁ < p₂` and `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`. Then for every `a` with `p₁ ≼ a` and every `b` with `p₂ ≼ b`, `a < b`.
