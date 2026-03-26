# ASN-0034 Formal Statements

*Source: ASN-0034-tumbler-algebra.md (revised 2026-03-26) — Extracted: 2026-03-26*

## T0(a) — Every component value of a tumbler is unbounded

`(A t ∈ T, i : 1 ≤ i ≤ #t : (A M ∈ ℕ :: (E t' ∈ T :: t' agrees with t except t'.dᵢ > M)))`.

In words: for every tumbler and every component position, there exists a tumbler whose value at that position exceeds any given bound.


## T0(b) — Tumblers of arbitrary length exist in T

`(A n ∈ ℕ : n ≥ 1 : (E t ∈ T :: #t ≥ n))`.

In words: there is no maximum tumbler length — for every bound, a tumbler of at least that length exists in T.

T0(b) follows from T's definition as the set of all finite sequences over ℕ — for any `n`, the constant sequence `[1, 1, ..., 1]` of length `n` is a member.


### The total order

We require a total order on T. The ordering rule is lexicographic:


## T1 — Tumblers are totally ordered by lexicographic comparison, with the prefix-less-than convention

For tumblers `a = a₁. ... .aₘ` and `b = b₁. ... .bₙ`, define `a < b` iff there exists `k ≥ 1` such that `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either:

  (i) `k ≤ min(m, n)` and `aₖ < bₖ`, or

  (ii) `k = m + 1 ≤ n` (that is, `a` is a proper prefix of `b`).

In words: tumblers are compared lexicographically; a proper prefix is strictly less than any proper extension.

T1 gives a total order: for any `a, b ∈ T`, exactly one of `a < b`, `a = b`, `a > b` holds. This is a standard mathematical fact about lexicographic orderings on well-ordered alphabets — ℕ is well-ordered, so the lexicographic extension to finite sequences is total.


## T2 — Tumbler comparison is computable from the two addresses alone, examining at most min(#a, #b) component pairs

The order relation T1 is computable from the two tumblers alone, without consulting any external data structure. The comparison examines at most `min(#a, #b)` component pairs.

In words: tumbler comparison requires no external state; all needed information is intrinsic to the two addresses.

*Proof.* The definition of T1 determines `a < b` by scanning component pairs `(aᵢ, bᵢ)` at successive positions `i = 1, 2, ...` until either (i) a divergence `aₖ ≠ bₖ` is found at some `k ≤ min(m, n)`, or (ii) all `min(m, n)` positions are exhausted without divergence, in which case the shorter tumbler is a proper prefix of the longer. In case (i), exactly `k ≤ min(m, n)` component pairs are examined. In case (ii), exactly `min(m, n)` component pairs are examined, and the result is then determined by comparing the lengths `m` and `n`. In both cases, at most `min(m, n)` component pairs are compared, and the only values consulted are the components `aᵢ`, `bᵢ` and the lengths `m`, `n` — all intrinsic to the two tumblers. No external data structure participates in the decision. ∎


### Canonical form

Equality of tumblers must mean component-wise identity. There must be no representation in which two distinct sequences of components denote the same abstract tumbler:

## T3 — ExtensionalEquality

`(A a, b ∈ T : a₁ = b₁ ∧ ... ∧ aₙ = bₙ ∧ #a = #b ≡ a = b)`

Two tumblers are equal if and only if they have the same length and agree at every component position.

## T4 — FieldSeparatorConstraint

Every tumbler `t ∈ T` used as an address contains at most three zero-valued components, appearing in order as field separators, every non-separator component is strictly positive, and every field present in the address has at least one component. Formally, if `t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`, then `(A i : 1 ≤ i ≤ α : Nᵢ > 0)`, `(A j : 1 ≤ j ≤ β : Uⱼ > 0)`, `(A k : 1 ≤ k ≤ γ : Dₖ > 0)`, `(A l : 1 ≤ l ≤ δ : Eₗ > 0)`, and `α ≥ 1`, `β ≥ 1` when present, `γ ≥ 1` when present, `δ ≥ 1` when present.

The *positive-component constraint*: every component of every field is strictly positive.

The *non-empty field constraint* — each present field has at least one component — is equivalent to three syntactic conditions: no two zeros are adjacent, the tumbler does not begin with zero, and the tumbler does not end with zero.

The function `fields(t)` that extracts the node, user, document, and element fields is well-defined and computable from `t` alone.

Define `zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`. The count of zero-valued components uniquely determines the hierarchical level:

  - `zeros(t) = 0`: `t` is a node address (node field only),
  - `zeros(t) = 1`: `t` is a user address (node and user fields),
  - `zeros(t) = 2`: `t` is a document address (node, user, and document fields),
  - `zeros(t) = 3`: `t` is an element address (all four fields).

This correspondence is injective on levels: each level produces addresses with exactly one zero count, and each zero count corresponds to exactly one level. The correspondence depends on the positive-component constraint — zero components serve exclusively as field separators because no field component is zero.

## T5 — PrefixContiguity

For any tumbler prefix `p`, the set `{t ∈ T : p ≼ t}` (where `≼` denotes "is a prefix of") forms a contiguous interval under T1:

  `[p ≼ a ∧ p ≼ c ∧ a ≤ b ≤ c ⟹ p ≼ b]`

In words: if `a` and `c` both share prefix `p` and `a ≤ b ≤ c`, then `b` also shares prefix `p`.

*Proof.* From T1, if `p ≼ a` then `a` agrees with `p` on the first `#p` components. If `a ≤ b ≤ c` and both `a` and `c` share prefix `p`, then `b` must also share prefix `p`. We consider two cases.

*Case 1: `#b ≥ #p`.* If `b` diverged from `p` at some position `k ≤ #p`, then either `bₖ < pₖ` (contradicting `a ≤ b` since `aₖ = pₖ`) or `bₖ > pₖ` (contradicting `b ≤ c` since `cₖ = pₖ`). So `b` agrees with `p` on all `#p` positions, hence `p ≼ b`.

*Case 2: `#b < #p`.* Since `p ≼ a`, we have `#a ≥ #p > #b`, so `b` is shorter than `a`. By T1, `a ≤ b` requires a first divergence point `j ≤ #b` where `aⱼ < bⱼ` (since `a` cannot be a prefix of the shorter `b`). But `aⱼ = pⱼ` (because `j ≤ #b < #p` and `a` shares prefix `p`), so `bⱼ > pⱼ = cⱼ`. This contradicts `b ≤ c`, since `b` exceeds `c` at position `j` and they agree on all prior positions. ∎

## T6 — ContainmentDecidability

For any two tumblers `a, b ∈ T`, the following are decidable from the addresses alone:

  (a) Whether `a` and `b` share the same node field.

  (b) Whether `a` and `b` share the same node and user fields.

  (c) Whether `a` and `b` share the same node, user, and document-lineage fields.

  (d) Whether the document field of `a` is a prefix of the document field of `b` (structural subordination within a document family).

T6 is a corollary of T4: extract the relevant fields and compare.

T6(d) captures allocation hierarchy, not derivation history. The document field records who allocated which sub-number. Version `5.3` was allocated under document `5`, but the document field conveys nothing about content derivation. Formal version-derivation requires the version graph, not the address.

## T7 — SubspaceDisjointness

The subspace identifier (the first component of the element field) permanently separates the address space into disjoint regions:

  `(A a, b ∈ T : a.E₁ ≠ b.E₁ ⟹ a ≠ b)`

In words: no tumbler in subspace `s₁` can equal any tumbler in subspace `s₂ ≠ s₁`.

*Proof (corollary of T3, T4).* Both `a` and `b` have element fields, so `zeros(a) = zeros(b) = 3` (T4). Write their field lengths as `(α, β, γ, δ)` and `(α', β', γ', δ')`, so that `E₁` sits at position `pₐ = α + β + γ + 4` in `a` and `pᵦ = α' + β' + γ' + 4` in `b`.

*Case 1* (`pₐ = pᵦ`): The tumblers have `a[pₐ] = Eₐ₁ ≠ Eᵦ₁ = b[pₐ]`, so `a ≠ b` by T3.

*Case 2* (`pₐ ≠ pᵦ`): If `#a ≠ #b`, then `a ≠ b` by T3 (distinct lengths). If `#a = #b`, the zero-position sets of `a` — at `α + 1`, `α + β + 2`, `α + β + γ + 3` — and of `b` — at `α' + 1`, `α' + β' + 2`, `α' + β' + γ' + 3` — cannot all coincide: matching the first gives `α = α'`, then the second gives `β = β'`, then the third gives `γ = γ'`, whence `pₐ = pᵦ`, contradicting the case hypothesis. So there exists a position `j` that is a separator in one tumbler but not the other. At `j`, one tumbler has value 0 and the other has a field component, which is strictly positive by T4's positive-component constraint. They differ at `j`, giving `a ≠ b` by T3. ∎

The total order T1 places all text addresses (subspace 1) before all link addresses (subspace 2) within the same document, because `1 < 2` at the subspace position.

## T8 — AllocationPermanence

For every state transition s → s', `allocated(s) ⊆ allocated(s')`. The set of allocated addresses is monotonically non-decreasing.

In words: once a tumbler address is allocated, it is never removed from the address space.

*Proof.* The system defines three operation classes:

1. **Comparison and parsing** (T1, T2, T4): read-only; `allocated` is unchanged.
2. **Arithmetic** (⊕, ⊖, inc): pure functions on T; `allocated` is unchanged.
3. **Allocation**: each allocator advances via `inc` (TA5), producing a strictly greater address, and inserts it into the allocated set. Allocation is strictly additive — no element is removed.

The specification defines no inverse operation ("deallocate", "free", "reclaim"). Since every transition either leaves `allocated` unchanged or strictly grows it, `allocated(s) ⊆ allocated(s')` holds for every transition. By induction over transition sequences, the invariant holds for all reachable states. ∎

## T9 — MonotonicAllocatorStream

Within a single allocator's sequential stream, new addresses are strictly monotonically increasing:

  `(A a, b : same_allocator(a, b) ∧ allocated_before(a, b) : a < b)`

In words: within each allocator's stream, later-allocated addresses are strictly greater.

T10a constrains each allocator to advance by `inc(·, 0)` at each step. Since `inc` produces a strictly greater tumbler at each step (TA5(a)), successive outputs within a single allocator's stream are strictly increasing.

T9 is scoped to a single allocator's sequential stream, not to the tumbler line globally. When a parent address forks a child, the child is inserted between the parent and the parent's next sibling on the tumbler line; address `2.1.1` may be created long after `2.2` but sits between them: `2.1 < 2.1.1 < 2.2`. Children always precede the parent's next sibling in depth-first linearization, regardless of creation order.

T9 is also scoped per allocator. A server-level subtree spans multiple independent allocators (one per user). T10 guarantees they need no coordination. If user A (prefix `1.0.1`) allocates at wall-clock time `t₂` and user B (prefix `1.0.2`) allocates at time `t₁ < t₂`, neither T9 nor any other property requires that A's address exceed B's. T9 applies within each user's allocation stream independently.

A consequence of T8 and T9 together: the set of allocated addresses is a growing set in the lattice-theoretic sense — it can only increase, and new elements always appear at the frontier of each allocator's domain.

## T10 — CoordinationFreeUniqueness

Let `p₁` and `p₂` be prefixes such that neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for any tumbler `a` with prefix `p₁` and any tumbler `b` with prefix `p₂`, `a ≠ b`.

In words: allocators with non-nesting prefixes produce distinct addresses without coordination.

*Proof.* If `a` has prefix `p₁` and `b` has prefix `p₂`, and the prefixes diverge at some position `k` with `p₁ₖ ≠ p₂ₖ`, then `aₖ = p₁ₖ ≠ p₂ₖ = bₖ`, so `a ≠ b`. ∎

## T10a — AllocatorIncrementConstraint

Each allocator produces its sibling outputs exclusively by repeated application of `inc(·, 0)` — shallow increment at the last significant position. To spawn a child allocator, the parent performs one `inc(·, k')` with `k' > 0` to establish the child's prefix, then delegates further allocation to the child. The parent's own sibling stream resumes with `inc(·, 0)`.

In words: siblings use shallow increment; child-spawning uses exactly one deep increment.

Since `inc(·, 0)` preserves length (TA5(c)), all sibling outputs from a single allocator have the same length. This uniform-length property is what the partition monotonicity and global uniqueness proofs depend on. If an allocator used `k > 0` for siblings, successive outputs would have increasing lengths and each output would extend the previous — making successive siblings nest rather than stand disjoint. This nesting would break the non-nesting premise required by the Prefix Ordering Extension lemma.

The `k > 0` operation is reserved exclusively for child-spawning: a single deep increment that establishes a new prefix at a deeper level, from which a new allocator continues with its own `inc(·, 0)` stream.

## PrefixOrderingExtension — NonNestingOrderPreservation

Let `p₁, p₂ ∈ T` be tumblers such that `p₁ < p₂` and neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for every `a` extending `p₁` (`p₁ ≼ a`) and every `b` extending `p₂` (`p₂ ≼ b`), `a < b`.

In words: if two non-nesting prefixes are ordered, all addresses extending them inherit that order.

*Proof.* Since `p₁ < p₂` and neither is a prefix of the other, T1 case (i) applies: there exists a position `k ≤ min(#p₁, #p₂)` such that `p₁` and `p₂` agree on positions `1, ..., k-1` and `p₁ₖ < p₂ₖ`. (Case (ii) is excluded because `p₁` is not a proper prefix of `p₂`.) Now `a` extends `p₁`, so `aᵢ = p₁ᵢ` for all `i ≤ #p₁`; in particular `aₖ = p₁ₖ`. Similarly `bₖ = p₂ₖ`. On positions `1, ..., k-1`, `aᵢ = p₁ᵢ = p₂ᵢ = bᵢ`. At position `k`, `aₖ = p₁ₖ < p₂ₖ = bₖ`. So `a < b` by T1 case (i). ∎

## PartitionMonotonicity — CrossAllocatorOrdering

Within any prefix-delimited partition with prefix `p`, the set of allocated addresses is totally ordered by T1, consistent with the allocation order of any single allocator within that partition. For any two sibling sub-partitions with non-nesting prefixes `p₁ < p₂`, every address extending `p₁` precedes every address extending `p₂` under T1.

In words: per-allocator allocation order extends to a cross-allocator total order determined by the prefix structure.

*Proof.* Consider a partition with prefix `p`. Every allocated address has prefix `p`, hence lies in the contiguous interval guaranteed by T5. Sub-partitions have sibling prefixes — they share `p` but diverge at the component distinguishing one allocator from another.

**Sibling prefixes are non-nesting.** The first sibling prefix `t₀` is produced by `inc(parent, k)` with `k > 0`, giving `#t₀ = #parent + k` (by TA5(d)). By T10a, subsequent sibling prefixes are produced by `inc(·, 0)`: `t₁ = inc(t₀, 0)`, `t₂ = inc(t₁, 0)`, etc. By TA5(c), `inc(t, 0)` preserves length: `#inc(t, 0) = #t`. All sibling prefixes have the same length `#t₀`. Two tumblers of the same length cannot stand in a prefix relationship unless equal. Since they differ at position `sig(t)` (TA5(c) increments that component), they are unequal, hence non-nesting.

Each allocator's output is monotonic (T9). Sub-partitions are ordered by their prefixes under T1. The prefix ordering extension lemma gives `a < b` for every address `a` under an earlier prefix and every address `b` under a later prefix. Within each sub-partition, allocation order matches address order by T9. ∎


## GlobalUniqueness — AllocationUniqueness

`(A distinct allocation events e₁, e₂ : addr(e₁) ≠ addr(e₂))`

No two distinct allocations, anywhere in the system, at any time, produce the same address.

*Proof.* Consider allocations producing addresses `a` and `b` by distinct allocation events. Four cases arise.

*Case 1: Same allocator.* Both addresses are produced by the same allocator's sequential stream. T9 guarantees `a ≠ b` because allocation is strictly monotonic.

*Case 2: Different allocators at the same hierarchical level.* The allocators have sibling prefixes `p₁` and `p₂` — neither is a prefix of the other. T10 gives `a ≠ b` directly.

*Case 3: Different allocators with nesting prefixes and different zero counts.* One allocator's prefix nests within another's. These allocators produce addresses with different zero counts: the node allocator produces addresses with `zeros = 1` (user-level), while the element allocator produces addresses with `zeros = 3`. By T4, different zero counts imply different field structure. If `#a ≠ #b`, then `a ≠ b` by T3. If `#a = #b`, then `zeros(a) ≠ zeros(b)` means there exists a position where one is zero and the other nonzero — by T3, `a ≠ b`.

*Case 4: Different allocators with nesting prefixes and the same zero count.* By T10a, the parent allocator uses `inc(·, 0)` for all its sibling allocations. Its first output has length `γ₁`; since `inc(·, 0)` preserves length (TA5(c)), all subsequent parent siblings have length `γ₁`. The child allocator's prefix was established by `inc(parent_output, k')` with `k' > 0`, giving prefix length `γ₁ + k'` (by TA5(d)). The child uses `inc(·, 0)` for its own siblings — all its outputs have length `γ₁ + k'`. Since `k' ≥ 1`, child outputs are strictly longer than parent outputs: `γ₁ + k' > γ₁`. By T3, `a ≠ b`. One pair requires separate treatment: the parent's child-spawning output that established the child's prefix has the same length as the child's sibling outputs (both `γ₁ + k'`). However, this output IS the child's base address, and every child sibling output is strictly greater than its base (by TA5(a)), hence distinct. The length separation is additive across nesting levels — each `inc(·, k')` with `k' ≥ 1` adds at least one component, so a descendant `d` nesting levels below has output length at least `γ₁ + d > γ₁`. Allocators at different branches that are not ancestors of each other have non-nesting prefixes and are handled by Case 2.

The argument depends critically on T10a's constraint that sibling allocations use `k = 0`. If a parent allocator could use `k > 0` for siblings, its outputs would have increasing lengths, and some parent output could match the length of a child output, collapsing the length separation. ∎


## T12 — WellFormedSpan

A span `(s, ℓ)` is well-formed when `ℓ > 0` and the action point `k` of `ℓ` satisfies `k ≤ #s` (the TA0 precondition for `s ⊕ ℓ`). Equivalently, the number of leading zeros in `ℓ` must be strictly less than `#s`. A well-formed span denotes `{t ∈ T : s ≤ t < s ⊕ ℓ}`. This set is contiguous under T1 and non-empty.

In words: a span is an interval in the tumbler total order; well-formedness ensures the endpoint is defined and strictly greater than the start.

*Proof.* Contiguity is definitional: the span is an interval `[s, s ⊕ ℓ)` in a totally ordered set, and intervals in total orders are contiguous. Non-emptiness follows from TA-strict: since `ℓ > 0` and `k ≤ #s`, TA0 gives `s ⊕ ℓ ∈ T`, and TA-strict gives `s ⊕ ℓ > s`. The interval `[s, s ⊕ ℓ)` is non-empty — it contains at least `s`. ∎


## TA0 — AdditionWellDefined

For tumblers `a, w ∈ T` where `w > 0` and the action point `k` of `w` satisfies `k ≤ #a`, the result `a ⊕ w` is a well-defined tumbler in `T`.

In words: tumbler addition is well-defined when the displacement's action point does not exceed the length of the start position.

The precondition `k ≤ #a` is essential: the constructive definition copies components `a₁, ..., aₖ₋₁` from the start position and adds `wₖ` to `aₖ`, so position `k` must exist within `a`.

**Verification of TA0.** By the constructive definition, `a ⊕ w = [r₁, ..., r_{#w}]` where: `rᵢ = aᵢ` for `i < k`, `rₖ = aₖ + wₖ`, and `rᵢ = wᵢ` for `i > k`. The result has length `#w`, finite and at least 1 since `w ∈ T`. Each prefix component `rᵢ = aᵢ ∈ ℕ` (inherited from `a ∈ T`); the action-point component `rₖ = aₖ + wₖ ∈ ℕ` (ℕ is closed under addition); each tail component `rᵢ = wᵢ ∈ ℕ` (inherited from `w ∈ T`). The result is a finite sequence of non-negative integers with at least one component — a member of `T`. ∎


## TA1 — OrderPreservationWeak

`(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) : a ⊕ w ≤ b ⊕ w)`, where `k` is the action point of `w`.

In words: if two positions were ordered before advancement by the same displacement, they remain in non-reversed order after.

The precondition `k ≤ min(#a, #b)` inherits from TA0: both operations must be well-defined.

## Divergence — DivergencePoint (DEFINITION, function)

For tumblers `a, b ∈ T` with `a ≠ b`, the *divergence* `divergence(a, b)` is defined by two cases corresponding to the two cases of T1:

  (i) If there exists `k ≤ min(#a, #b)` such that `aₖ ≠ bₖ` and `(A i : 1 ≤ i < k : aᵢ = bᵢ)`, then `divergence(a, b) = k`.

  (ii) If `(A i : 1 ≤ i ≤ min(#a, #b) : aᵢ = bᵢ)` and `#a ≠ #b`, then `divergence(a, b) = min(#a, #b) + 1`.

Exactly one case applies for any `a ≠ b`. In words: the divergence is the first position where `a` and `b` differ, or one past the shorter tumbler's last component if one is a proper prefix of the other.

## TA1-strict — StrictOrderPreservation

`(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) ∧ k ≥ divergence(a, b) : a ⊕ w < b ⊕ w)`, where `k` is the action point of `w`.

In words: addition preserves strict order when the action point of the displacement falls at or past the divergence of the operands.

## TA-strict — StrictAdvancement

`(A a ∈ T, w > 0 : a ⊕ w > a)` (where `a ⊕ w` is well-defined, i.e., `k ≤ #a` per TA0).

In words: adding a positive displacement to any tumbler produces a strictly larger tumbler.

**Verification of TA-strict.** Let `k` be the action point of `w`. By the constructive definition, `(a ⊕ w)ᵢ = aᵢ` for `i < k`, and `(a ⊕ w)ₖ = aₖ + wₖ`. Since `k` is the action point, `wₖ > 0`, so `aₖ + wₖ > aₖ`. Positions `1` through `k - 1` agree; position `k` is strictly larger. By T1 case (i), `a ⊕ w > a`.

## TA2 — SubtractionWellDefined

For tumblers `a, w ∈ T` where `a ≥ w`, `a ⊖ w` is a well-defined tumbler in `T`.

In words: subtracting a smaller-or-equal tumbler always yields a valid tumbler.

**Verification of TA2.** By TumblerSub, two cases arise. If the zero-padded sequences of `a` and `w` agree at every position, the result is the zero tumbler of length `max(#a, #w)` — a member of `T`. Otherwise, let `k` be the first divergence position (after zero-padding). The result `a ⊖ w = [r₁, ..., r_p]` has length `p = max(#a, #w)`, which is finite and at least 1. Each pre-divergence component `rᵢ = 0 ∈ ℕ`. At the divergence point: `a ≥ w` ensures `aₖ > wₖ` — if `a > w` by T1 case (i), the divergence falls at `k ≤ min(#a, #w)` with `aₖ > wₖ` directly; if `a > w` by T1 case (ii), `w` is a proper prefix of `a`, so `k > #w` and `wₖ = 0` (zero-padded), with `aₖ > 0` (otherwise no divergence at `k`). In either case, `rₖ = aₖ - wₖ ∈ ℕ`. Each tail component `rᵢ = aᵢ ∈ ℕ` (inherited from `a ∈ T`, or `0` when `i > #a`). The result is a finite sequence of non-negative integers with at least one component — a member of `T`.

## TA3 — SubtractionOrderPreservation

`(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w ≤ b ⊖ w)`.

In words: subtracting the same tumbler from two ordered operands preserves their relative order (weakly).

## TA3-strict — Subtraction preserves the total order (strict) when additionally #a = #b

`(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b : a ⊖ w < b ⊖ w)`.

In words: equal-length tumblers that are strictly ordered remain strictly ordered under subtraction of a common displacement.

### Partial inverse


## TA4 — Addition and subtraction are partial inverses

`(A a, w : w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊕ w) ⊖ w = a)`, where `k` is the action point of `w`.

In words: when the start position ends at the action point, the displacement has no trailing components, and all prefix components of the start are zero, adding then subtracting the displacement recovers the original.


## ReverseInverse — SubtractAddRecovery

`(A a, w : a ≥ w ∧ w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊖ w) ⊕ w = a)`, where `k` is the action point of `w`.

In words: under the same compatibility conditions as TA4, subtracting then adding the displacement recovers the original.

*Proof.* Let `y = a ⊖ w`. We verify the prerequisites for applying TA4 to `y`. Under the precondition `(A i : 1 ≤ i < k : aᵢ = 0)`, we have `aᵢ = wᵢ = 0` for all `i < k`, so the divergence falls at position `k`. The result `y` has: positions `i < k` zero, position `k` equal to `aₖ - wₖ`, and no components beyond `k` (since `k = #a`). So `#y = k`, `yᵢ = 0` for `i < k`, and `#w = k`. All preconditions for TA4 hold. By TA4, `(y ⊕ w) ⊖ w = y`. Suppose `y ⊕ w ≠ a`. We wish to apply TA3-strict, which requires three preconditions beyond strict ordering: `y ⊕ w ≥ w`, `a ≥ w`, and `#(y ⊕ w) = #a`. The equal-length condition holds: `#(y ⊕ w) = #w = k = #a` (the first step by the result-length identity; `#w = k` and `k = #a` are given). The condition `a ≥ w` is given. We verify `y ⊕ w ≥ w`: since `y ⊕ w ≠ a` and `yₖ = aₖ - wₖ`, we have `yₖ > 0` (if `yₖ = 0` then `aₖ = wₖ`, and since `yᵢ = wᵢ = 0` for `i < k` and `#y = k = #w`, we would have `y = [0,...,0]` and `y ⊕ w = w`; but `a ≥ w` and `aₖ = wₖ` with agreement on all prior positions gives `a = w` when `#a = #w = k`, so `y ⊕ w = w = a`, contradicting our assumption). So `yₖ > 0`, giving `(y ⊕ w)ₖ = yₖ + wₖ > wₖ` with agreement on positions before `k`, hence `y ⊕ w > w`. Now apply TA3-strict. If `y ⊕ w > a`, then `(y ⊕ w) ⊖ w > a ⊖ w = y`, giving `y > y`, a contradiction. If `y ⊕ w < a`, then `(y ⊕ w) ⊖ w < a ⊖ w`, giving `y < y`, a contradiction. So `(a ⊖ w) ⊕ w = a`. ∎


## TumblerAdd — PositionAdvanceDefinition

Let `a = [a₁, ..., aₘ]` and `w = [w₁, ..., wₙ]` with `w > 0`. With action point `k`:

```
         ⎧ aᵢ           if i < k        (copy from start)
rᵢ   =  ⎨ aₖ + wₖ      if i = k        (single-component advance)
         ⎩ wᵢ           if i > k        (copy from displacement)
```

In words: advance the start position at the action-point component and replace the tail with the displacement's tail.

The result `a ⊕ w = [r₁, ..., rₚ]` has length `p = max(k - 1, 0) + (n - k + 1)`. Since `w > 0` implies `k ≥ 1`, this simplifies to `p = (k - 1) + (n - k + 1) = n = #w`. *Result-length identity:* **`#(a ⊕ w) = #w`**.

**Precondition:** `k ≤ m` — the displacement's action point must fall within the start position's length.

**No carry propagation:** The sum `aₖ + wₖ` at the action point is a single natural-number addition. There is no carry into position `k - 1`.

**Tail replacement, not tail addition:** Components after the action point come entirely from `w`. The start position's components at positions `k + 1, ..., m` are discarded.

**The many-to-one property:** Because trailing components of `a` are discarded, distinct start positions can produce the same result. Formally: if `a` and `b` agree on positions `1, ..., k` (where `k` is the action point of `w`), then `a ⊕ w = b ⊕ w`.


## TumblerSub — DivergenceRecoveryDefinition

Given an end position `a` and a displacement `w`, recover the start position. When the operands have different lengths, zero-pad the shorter to the length of the longer before scanning for divergence. When the zero-padded sequences agree at every position (no divergence exists), the result is the zero tumbler of length `max(#a, #w)`: `a ⊖ w = [0, ..., 0]`. Otherwise, let `k` be the first position where `a` and `w` differ (treating missing components as zero):

```
         ⎧ 0             if i < k        (these levels matched — zero them)
rᵢ   =  ⎨ aₖ - wₖ      if i = k        (reverse the advance)
         ⎩ aᵢ           if i > k        (copy from end position)
```

In words: zero the matched prefix, reverse the advance at the divergence, and copy the remainder from the end position.

The result has length `max(#a, #w)`.

**Precondition:** `a ≥ w` — when `a ≠ w`, at the divergence point (after zero-padding) `aₖ ≥ wₖ`.


### Verification of TA1 and TA1-strict

**Claim:** (TA1, weak form). If `a < b`, `w > 0`, and `k ≤ min(#a, #b)`, then `a ⊕ w ≤ b ⊕ w`.

**Claim:** (TA1-strict). If additionally `k ≥ divergence(a, b)`, then `a ⊕ w < b ⊕ w`.

*Proof.* Let `j = divergence(a, b)`. In case (i) of the Divergence definition, `aⱼ < bⱼ`; in case (ii), `j = min(#a, #b) + 1` exceeds both tumblers' shared positions and the ordering `a < b` follows from the prefix rule. Three cases arise.

*Case 1: `k < j`.* Both `a` and `b` agree at position `k` (since `k < j`), so `(a ⊕ w)ₖ = aₖ + wₖ = bₖ + wₖ = (b ⊕ w)ₖ`. At positions after `k`, both results copy from `w`, giving identical tails. So `a ⊕ w = b ⊕ w`. The weak form (`≤`) holds. The strict form does not — the original divergence is erased by tail replacement.

*Case 2: `k = j`.* At position `k`, `(a ⊕ w)ₖ = aₖ + wₖ < bₖ + wₖ = (b ⊕ w)ₖ` (since `aₖ < bₖ` and natural-number addition preserves strict inequality). Positions before `k` agree. So `a ⊕ w < b ⊕ w` strictly.

*Case 3: `k > j`.* For `i < k`, the constructive definition gives `(a ⊕ w)ᵢ = aᵢ` and `(b ⊕ w)ᵢ = bᵢ`. Since `j < k`, the divergence at position `j` is preserved: `(a ⊕ w)ⱼ = aⱼ < bⱼ = (b ⊕ w)ⱼ`. So `a ⊕ w < b ⊕ w` strictly. ∎

In all three cases, `a ⊕ w ≤ b ⊕ w`. Strict inequality holds in Cases 2 and 3, i.e., whenever `k ≥ j = divergence(a, b)`.


### Verification of TA3

**Claim:** (TA3, weak form). If `a < b`, `a ≥ w`, and `b ≥ w`, then `a ⊖ w ≤ b ⊖ w`.

*Proof.* By TA2, since `a ≥ w` and `b ≥ w`, both `a ⊖ w` and `b ⊖ w` are well-formed tumblers in `T`, making the order comparisons below well-defined. We first handle the case where `a < b` by the prefix rule (T1 case (ii)), then the component-divergence cases.

*Case 0: `a` is a proper prefix of `b`.* Then `#a < #b` and `aᵢ = bᵢ` for all `i ≤ #a`.

We first handle the sub-case `a = w`. Then `a ⊖ w = [0, ..., 0]` (the zero tumbler of length `max(#a, #w) = #w = #a`). Since `b > a = w` and `a` is a proper prefix of `b`, we have `bᵢ = wᵢ` for all `i ≤ #w`. Two sub-sub-cases arise. If `b ⊖ w` is a positive tumbler — some component of `b` beyond `#w` is nonzero — then every zero tumbler is less than every positive tumbler (TA6), so `a ⊖ w < b ⊖ w`. If `b ⊖ w` is itself a zero tumbler — all components of `b` beyond `#w` are zero, so zero-padded `w` equals `b` — then `b ⊖ w = [0, ..., 0]` of length `max(#b, #w) = #b`. Both results are zero tumblers, but `#(a ⊖ w) = #a < #b = #(b ⊖ w)` (since `a` is a proper prefix of `b`). The shorter zero tumbler is a proper prefix of the longer, so `a ⊖ w < b ⊖ w` by T1 case (ii). In either sub-sub-case, `a ⊖ w ≤ b ⊖ w`. The sub-case is resolved.

For `a > w`: two sub-cases arise depending on the structure of the divergence between `a` and `w` (after zero-padding).

*Sub-case `a > w` with divergence.* If `a > w` by T1 case (i), the divergence `dₐ` is at a shared position `≤ min(#a, #w) ≤ #a`. If `a > w` by T1 case (ii), `w` is a proper prefix of `a`; after zero-padding `w` to length `#a`, we compare: if at least one component `aᵢ > 0` for `i > #w`, the divergence falls at the smallest such `i`, satisfying `#w < dₐ ≤ #a`. In either T1 case, `dₐ ≤ #a`. Since `bᵢ = aᵢ` for all `i ≤ #a` and `dₐ ≤ #a`, the comparison of `b` (zero-padded) against `w` (zero-padded) agrees with that of `a` at all positions up to `dₐ`. So `d_b = dₐ = d`.

Now apply the subtraction formula to both. At positions `i < d`: both results are zero. At position `d`: both compute `a_d - w_d = b_d - w_d`, since `a_d = b_d` for `d ≤ #a`. At positions `d < i ≤ #a`: both copy from the minuend, giving `aᵢ = bᵢ`. The two results agree on all positions `1, ..., #a`.

Beyond position `#a`, the results may differ. The result `a ⊖ w` has length `max(#a, #w)`. At positions `#a < i ≤ max(#a, #w)` (present only when `#w > #a`): `(a ⊖ w)ᵢ = 0` (from `a`'s zero padding). For `(b ⊖ w)ᵢ`: when `i ≤ #b`, the value is `bᵢ` (copied in the tail phase since `i > d`); when `i > #b`, the value is `0` (from `b`'s zero padding). In either case `(a ⊖ w)ᵢ ≤ (b ⊖ w)ᵢ`. The result `b ⊖ w` has length `max(#b, #w) ≥ max(#a, #w)` (since `#b > #a`). If `max(#b, #w) > max(#a, #w)`, the extra positions come from `b`'s components beyond `max(#a, #w)` when `#b > #w` (copied from the minuend), or are zero when `#w > #b` (from `b`'s zero padding). Now `a ⊖ w` is no longer than `b ⊖ w`, and they agree on positions `1, ..., #a`. We compare lexicographically. If no disagreement exists on positions `1, ..., max(#a, #w)`, then `a ⊖ w` is a prefix of `b ⊖ w` (since `#(a ⊖ w) ≤ #(b ⊖ w)`), giving `a ⊖ w ≤ b ⊖ w` by T1 case (ii). If a first disagreement exists at some position `j > #a`, then `(a ⊖ w)ⱼ = 0 ≤ (b ⊖ w)ⱼ` (where `(b ⊖ w)ⱼ = bⱼ` when `j ≤ #b`, or `0` when `j > #b`). If the disagreement is strict (`(a ⊖ w)ⱼ = 0 < (b ⊖ w)ⱼ`), we have `a ⊖ w < b ⊖ w` by T1 case (i). If `(b ⊖ w)ⱼ = 0` at all positions `#a < j ≤ max(#a, #w)`, then `a ⊖ w` and `b ⊖ w` agree through position `max(#a, #w)`, and `a ⊖ w` is a prefix of the longer `b ⊖ w`, giving `a ⊖ w ≤ b ⊖ w` by T1 case (ii). In either case, `a ⊖ w ≤ b ⊖ w`.

*Sub-case `a > w` without divergence (zero-padded equality).* If `a > w` by T1 case (ii) and `aᵢ = 0` for all `i > #w`, then after zero-padding `w` to length `#a`, the padded sequences are identical — no divergence exists. The subtraction `a ⊖ w` yields the zero tumbler of length `max(#a, #w) = #a`. For `b ⊖ w`: since `b > a > w` and `#b > #a ≥ #w`, `b` agrees with `w` (hence with `a`) on positions `1, ..., #a`. Beyond `#a`, `b` has components that `a` lacks. The result `b ⊖ w` has length `max(#b, #w) = #b > #a`. The zero tumbler `a ⊖ w` of length `#a` is a proper prefix of the zero tumbler of length `#b` (if `b ⊖ w` is all zeros), giving `a ⊖ w < b ⊖ w` by T1 case (ii). If `b ⊖ w` has any positive component, then `a ⊖ w` (all zeros) is less than `b ⊖ w` by TA6. In either case, `a ⊖ w ≤ b ⊖ w`. The sub-case is resolved.

*Case 0a: `a < b` by component divergence and `a` zero-padded-equal to `w`.* There exists `j ≤ min(#a, #b)` with `aⱼ < bⱼ`. Since `a` and `w` agree at every position under zero-padding, `a ⊖ w` is the zero tumbler of length `max(#a, #w)`. At position `j`, `wⱼ = aⱼ` (from zero-padded equality), so `bⱼ > aⱼ = wⱼ`. The pair `(b, w)` diverges at or before `j`, making `b ⊖ w` positive. By TA6, `a ⊖ w < b ⊖ w`.

For the remaining cases, `a < b` by T1 case (i) and `a` is not zero-padded-equal to `w`, so `dₐ = divergence(a, w)` is well-defined. Let `d_b = divergence(b, w)` (under zero-padding).

*Case 1: `dₐ = d_b = d`.* For `i < d`, both results are zero. At position `d`, we need `j ≥ d` (since `a` and `b` agree with `w` before `d`). If `j = d`: `a_d - w_d < b_d - w_d`, so `a ⊖ w < b ⊖ w`. If `j > d`: `a_d = b_d`, so both results agree at `d`; at positions `d < i < j`, both copy from their respective minuends which agree; at position `j`, `aⱼ < bⱼ`. So `a ⊖ w < b ⊖ w`.

*Case 2: `dₐ < d_b`.* At position `dₐ`: `a_{dₐ} ≠ w_{dₐ}` but `b_{dₐ} = w_{dₐ}`. Since `a < b` and they agree with `w` before `dₐ`, we have `j = dₐ` with `a_{dₐ} < b_{dₐ} = w_{dₐ}`. But `a ≥ w` requires `a_{dₐ} ≥ w_{dₐ}` at the divergence — contradiction. This case is impossible under the preconditions.

*Case 3: `dₐ > d_b`.* At position `d_b`: `b_{d_b} ≠ w_{d_b}` but `a_{d_b} = w_{d_b}`. So `j = d_b` with `a_{d_b} = w_{d_b} < b_{d_b}`. The result `(a ⊖ w)_{d_b} = 0` and `(b ⊖ w)_{d_b} = b_{d_b} - w_{d_b} > 0`. So `a ⊖ w < b ⊖ w`. ∎

**Claim:** (TA3-strict). If `a < b`, `a ≥ w`, `b ≥ w`, and `#a = #b`, then `a ⊖ w < b ⊖ w`.

*Proof.* The equal-length precondition eliminates Case 0 entirely — two tumblers of the same length cannot be in a prefix relationship unless equal, and `a < b` rules out equality. Cases 0a and 1–3 remain, all of which produce strict inequality. ∎


### Verification of TA4

**Claim.** `(a ⊕ w) ⊖ w = a` under the full precondition: `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`.

*Proof.* Let `k` be the action point of `w`. Since `k = #a`, the addition `a ⊕ w` produces a result `r` with: `rᵢ = aᵢ = 0` for `i < k` (by the zero-prefix condition), `rₖ = aₖ + wₖ`, and `rᵢ = wᵢ` for `i > k`. Crucially, there are no components of `a` beyond position `k` — the tail replacement discards nothing. By the result-length identity, `#r = #w = k`, so `r = [0, ..., 0, aₖ + wₖ]`.

Now subtract `w` from `r`. The subtraction scans for the first divergence between `r` and `w`. For `i < k`: `rᵢ = 0 = wᵢ` (both are zero — `aᵢ` by the zero-prefix precondition, `wᵢ` by definition of action point). Two sub-cases arise at position `k`.

*Sub-case (i): `aₖ > 0`.* Then `rₖ = aₖ + wₖ > wₖ`, and the first divergence is at position `k`. The subtraction produces: positions `i < k` get zero, position `k` gets `rₖ - wₖ = aₖ`, and positions `i > k` copy from `r`, giving `rᵢ = wᵢ`. Since `k = #a` and `#w = k`, there are no trailing components. The result is `[0, ..., 0, aₖ] = a`.

*Sub-case (ii): `aₖ = 0`.* Then `a` is a zero tumbler. The addition gives `rₖ = wₖ`. Since `#r = #w` (result-length identity) and `#w = k` (precondition), we have `r = w`. The subtraction `w ⊖ w` yields the zero tumbler of length `k`, which is `a`. ∎


### Cancellation properties of ⊕

TumblerAdd's constructive definition determines each component of the result from exactly one input. This makes the operation left-cancellative.

## TA5 — Hierarchical increment inc(t, k) produces t' > t

For tumbler `t ∈ T` and level `k ≥ 0`, there exists an operation `inc(t, k)` producing tumbler `t'` such that:

  (a) `t' > t` (strictly greater under T1),

  (b) `t'` agrees with `t` on all components before the increment point,

  (c) when `k = 0` (*sibling*): `#t' = #t`, and `t'` differs from `t` only at position `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`,

  (d) when `k > 0` (*child*): `#t' = #t + k`, the `k - 1` intermediate positions `#t + 1, ..., #t + k - 1` are set to `0` (field separators), and the final position `#t + k` is set to `1` (the first child).

In words: `inc(t, k)` produces the next peer (`k = 0`) or a child at depth `k` (`k > 0`), strictly greater than `t` under T1.

We verify `inc(t, k) > t` for both cases. For `k = 0`: `t'` agrees with `t` on positions `1, ..., sig(t) - 1` and exceeds `t` at position `sig(t)`, so `t' > t` by T1 case (i). For `k > 0`: `t'` agrees with `t` on positions `1, ..., #t`, and `#t' > #t`, so `t` is a proper prefix of `t'`, giving `t < t'` by T1 case (ii).

**TA5 preserves T4 when `k ≤ 2` and `zeros(t) + k - 1 ≤ 3`.** Two constraints must hold simultaneously: the zero-count bound and a structural constraint against adjacent zeros.

For `k = 0`: no zeros are added — `zeros(t') = zeros(t)`, and no new adjacencies are introduced. T4 is preserved unconditionally.

For `k = 1`: one component is appended (the child value `1`), with no new zero separators — `zeros(t') = zeros(t)`. Since the appended component is positive and the last component of `t` is positive (by T4), no adjacent zeros are created. T4 is preserved when `zeros(t) ≤ 3`.

For `k = 2`: one zero separator and one child value `1` are appended, giving `zeros(t') = zeros(t) + 1`. The appended sequence is `[0, 1]` — the zero is flanked by the last component of `t` (positive, by T4's non-empty field constraint) and the new child `1`, so no adjacent zeros are created. T4 is preserved when `zeros(t) ≤ 2`.

For `k ≥ 3`: the appended sequence `[0, 0, ..., 0, 1]` contains `k - 1 ≥ 2` zeros, of which at least two are adjacent. This violates T4's non-empty field constraint — the adjacent zeros create an empty field. Consider `inc([1], 3)` producing `[1, 0, 0, 1]`: zero count is 2 (≤ 3), but positions 2 and 3 are adjacent zeros, parsing as node `[1]`, separator, *empty user field*, separator, document `[1]`. The empty field violates T4 regardless of the zero count. T4 is violated for all `k ≥ 3`.

The effective constraints are: `k = 0` (always valid), `k = 1` (when `zeros(t) ≤ 3`), `k = 2` (when `zeros(t) ≤ 2`). The hierarchy enforces this naturally: each `inc(·, k)` with `k > 0` introduces one new hierarchical level, and the address format has exactly four fields with three separators, so at most three new separators can be introduced from a node address (the three `inc(·, 2)` steps from node to element level, with `zeros(t) = 0, 1, 2` respectively before each step, each satisfying `zeros(t) ≤ 2`).


### Zero tumblers and positivity

Under T3, the tumblers `[0]`, `[0, 0]`, `[0, 0, 0]`, etc., are *distinct* elements of T — they have different lengths. Under T1, they form a chain: `[0] < [0, 0] < [0, 0, 0] < ...` by the prefix rule. There is no single "zero tumbler"; there are infinitely many all-zero tumblers.


## TA6 — Every all-zero tumbler is less than every positive tumbler and is not a valid address

  `(A t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0) ⟹ t is not a valid address)`

  `(A s, t ∈ T : (A i : 1 ≤ i ≤ #s : sᵢ = 0) ∧ (E j : 1 ≤ j ≤ #t : tⱼ > 0) ⟹ s < t)`

In words: all-zero tumblers fail T4 (invalid as addresses) and are strictly below all positive tumblers in T1's total order.

*Proof (from T1, T4).* **Conjunct 1** (invalidity): Let `t` be a zero tumbler. Then `t₁ = 0`. T4 requires that a valid address does not begin with zero — the first component must be a positive node-field component. Since `t₁ = 0`, `t` fails T4 and is not a valid address.

**Conjunct 2** (ordering): Let `s` be a zero tumbler of length `m` and `t` a positive tumbler of length `n`. Since `t` is positive, there exists a first nonzero component; let `k = min({i : 1 ≤ i ≤ n : tᵢ > 0})`. For all `i < k`, `tᵢ = 0` (by minimality of `k`).

*Case 1* (`m ≥ k`): At positions `1, ..., k − 1`, `sᵢ = 0 = tᵢ` — no disagreement. At position `k`, `sₖ = 0 < tₖ`. By T1 case (i), `s < t`.

*Case 2* (`m < k`): For all `i ≤ m`, `sᵢ = 0 = tᵢ` (since `i ≤ m < k` and `tᵢ = 0` for `i < k`). The tumblers agree on every position of `s`, and `#s = m < k ≤ n = #t`, so `s` is a proper prefix of `t`. By T1 case (ii), `s < t`. ∎


### Subspace closure

An element-local position within subspace `S` has two components: the subspace identifier `N` and the ordinal `x`. A natural first attempt at an element-local displacement is `w = [0, n]` — action point `k = 2`, preserving the subspace identifier and advancing the ordinal. Addition: `[N, x] ⊕ [0, n] = [N, x + n]`, preserving the subspace. Subtraction: `[N, x] ⊖ [0, n]` finds the first divergence at position 1 (where `N ≠ 0`), not at position 2 where the intended action lies, producing `[N - 0, x] = [N, x]` — a no-op. The abstract `⊖` cannot shift a position backward by a displacement that disagrees at the subspace identifier position.

The operands passed to shift arithmetic are not full element-local positions; they are *within-subspace ordinals* — the second component alone. The subspace identifier is not an operand to the shift; it is structural context that determines *which* positions are subject to the shift.


## PositiveTumbler — TumblerPositivityDefinition

A tumbler `t ∈ T` is *positive*, written `t > 0`, iff at least one of its components is nonzero: `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`. A tumbler is a *zero tumbler* iff every component is zero: `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.

In words: positive means at least one nonzero component; zero tumbler means all components are zero.

Every positive tumbler is greater than every zero tumbler under T1: if `t` has a nonzero component at position `k`, then at position `k` either the zero tumbler has a smaller component (`0 < tₖ`) or has run out of components, either way placing it below `t`. The condition `w > 0` in TA0 and TA4 excludes all all-zero displacements regardless of length.


## TA7a — Ordinal-only shift arithmetic

In the ordinal-only formulation, a subspace ordinal `o = [o₁, ..., oₘ]` has `m ≥ 1` components all positive; define **S** = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)}. An element-local displacement is a positive tumbler `w` with action point `k`, `1 ≤ k ≤ m`. The subspace identifier `N` is held as structural context and is never an operand.

  `(A o ∈ S, w > 0 : k ≤ #o ⟹ o ⊕ w ∈ T)`

  `(A o ∈ S, w > 0 : o ≥ w ⟹ o ⊖ w ∈ T)`

In words: with the subspace identifier held as context, both operations on ordinals produce results in T without modifying the subspace identifier.

Both operations produce results in T, and the subspace identifier — held as context — is never modified.

For `⊕`, a stronger result holds: components before the action point are preserved positive from `o ∈ S`, and `oₖ + wₖ > 0` since both are positive. When all components of `w` after `k` are also positive, the result is in S. For single-component ordinals (the common case), `[x] ⊕ [n] = [x + n] ∈ S` unconditionally.

The subspace identifier is context — it determines which positions are subject to the shift — not an operand to the arithmetic.

For single-component ordinals, `⊖` gives closure in S ∪ Z: `[x] ⊖ [n]` is `[x - n] ∈ S` when `x > n`, or `[0] ∈ Z` when `x = n` (a sentinel, TA6). When the element field has deeper structure (`δ > 1` in T4), the ordinal `o` has multiple components. A displacement with action point `k ≥ 2` preserves all ordinal components before position `k` — the constructive definition copies `o₁, ..., oₖ₋₁` from the start position unchanged. For example, spanning from ordinal `[1, 3, 2]` to `[1, 5, 7]` requires displacement `[0, 2, 7]` (action point `k = 2`); `[1, 3, 2] ⊕ [0, 2, 7] = [1, 5, 7]` — position 1 of the ordinal is copied, preserving the ordinal prefix. The subspace closure holds in all cases because the subspace identifier is never an operand.

**Verification of TA7a.** In the ordinal-only formulation, the shift operates on `o = [o₁, ..., oₘ]` with all `oᵢ > 0` (since `o ∈ S`), by displacement `w` with action point `k` satisfying `1 ≤ k ≤ m`.

*For `⊕`:* By the constructive definition, `(o ⊕ w)ᵢ = oᵢ` for `i < k` (positive, preserved from `o`), and `(o ⊕ w)ₖ = oₖ + wₖ > 0` (both positive). Components after `k` come from `w`. The result has length `#w` (by the result-length identity). The result is in T; it is in S when additionally all components of `w` after `k` are positive. The subspace identifier, held as context, is unchanged.

*For `⊖`:* We analyze by action point. When `#w > m`, TumblerSub produces a result of length `max(m, #w) = #w > m` with trailing zeros at positions `m + 1` through `#w` (from the zero-padded minuend); this result lies in T \ S. The S-membership claims below assume the typical case `#w ≤ m`.

*Case `k ≥ 2`:* The displacement has `wᵢ = 0` for `i < k`. Since `o ∈ S`, `o₁ > 0`. The divergence falls at position 1 (where `o₁ > 0 = w₁`). TumblerSub produces: `r₁ = o₁ - 0 = o₁`, and `rᵢ = oᵢ` for `1 < i ≤ m` (copied from the minuend since `i > d = 1`). When `#w ≤ m`, the result has length `m` and equals `o` itself — a no-op; the result is trivially in S.

*Case `k = 1`:* The displacement has `w₁ > 0`. Let `d = divergence(o, w)`. If `d = 1` (i.e., `o₁ ≠ w₁`): since `o ≥ w`, `o₁ > w₁`. TumblerSub yields `r₁ = o₁ - w₁ > 0` and `rᵢ = oᵢ > 0` for `1 < i ≤ m`. When `#w ≤ m`, all components are positive and the result is in S. If `d > 1` (i.e., `o₁ = w₁`, divergence later): TumblerSub zeros positions before `d`, giving `r₁ = 0`. The result has a zero first component and is not in S. Counterexample: `o = [5, 3]`, `w = [5, 1]` (action point `k = 1`, divergence `d = 2`). Result: `[0, 2] ∈ T` but `[0, 2] ∉ S ∪ Z`. This sub-case arises when `o` and `w` share a leading prefix — the subtraction produces a displacement with leading zeros rather than a valid ordinal position.

In all cases the subspace identifier, held as context, is never modified. TA7a holds. ∎

The restriction to element-local displacements is necessary. An unrestricted displacement whose action point falls at the subspace-identifier position could produce an address in a different subspace — TA7a cannot hold for arbitrary `w`.


### What tumbler arithmetic is NOT

These negative results constrain what an implementer may assume.

**The algebra is not a group.** There is no additive identity — the zero tumbler is a sentinel, not a neutral element for addition. There is no additive inverse for every element — subtraction is only defined when `a ≥ w`. The algebra is not closed under subtraction in general.


## TA-assoc — Addition is associative where both compositions are defined

`(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)` whenever both sides are well-defined.

In words: tumbler addition is associative on the intersection of the two domains, though the domain conditions are asymmetric.

Three cases exhaust the possibilities. Let `k_b` and `k_c` be the action points of `b` and `c` respectively. When `k_b < k_c`: both sides produce `aᵢ` for `i < k_b`, `aₖ_b + bₖ_b` at `k_b`, `bᵢ` for `k_b < i < k_c`, `bₖ_c + cₖ_c` at `k_c`, and `cᵢ` beyond — identical. When `k_b = k_c = k`: both sides produce `aₖ + bₖ + cₖ` at `k` (natural-number addition is associative) and `cᵢ` beyond — identical. When `k_b > k_c`: both sides produce `aₖ_c + cₖ_c` at `k_c` and `cᵢ` beyond — identical (the deeper displacement `b` is overwritten by the shallower `c` in both cases). The domain conditions are asymmetric — the left side requires `k_b ≤ #a`, while the right requires only `min(k_b, k_c) ≤ #a` — but on the intersection, the values agree.

**Addition is not commutative.** `a ⊕ b ≠ b ⊕ a`. The operands play asymmetric roles: the first is a *position*, the second is a *displacement*.

**There is no multiplication or division.** The arithmetic repertoire is: add, subtract, increment, compare.

**Tumbler differences are not counts.** The difference between two addresses specifies *boundaries*, not *cardinality*. What lies between those boundaries depends on the actual population of the tree, which is dynamic and unpredictable.


### Spans

A span is a pair `(s, ℓ)` where `s ∈ T` is a start address and `ℓ ∈ T` is a length (a positive tumbler used as a displacement), denoting the contiguous range from `s` up to but not including `s ⊕ ℓ`. The form of `ℓ` depends on the hierarchical level at which the span operates, because the action point of `ℓ` must match the level of the start address `s`.

In words: a span is the half-open interval `[s, s ⊕ ℓ)` in the tumbler order; the action point of `ℓ` must match the level of `s`.

The 1-position convention exploits T5: because subtrees are contiguous, a span whose start is a high-level prefix and whose length reaches to the next sibling captures exactly that subtree's content.

A span may be empty yet valid. The range is determined by the endpoints; what is actually stored within that range is a question about the current state of the system, not about the tumbler algebra.

## TA-LC — LeftCancellation

If a ⊕ x = a ⊕ y with both sides well-defined (TA0 satisfied for both), then x = y.

In words: TumblerAdd is left-cancellative — equal results under the same start position imply equal displacements.

*Proof.* Let k₁ and k₂ be the action points of x and y. If k₁ < k₂, then (a ⊕ x)_{k₁} = a_{k₁} + x_{k₁} while (a ⊕ y)_{k₁} = a_{k₁} (position k₁ falls in the "copy from start" range of y). Equality gives x_{k₁} = 0, contradicting k₁ being the action point of x. Symmetrically k₂ < k₁ is impossible. So k₁ = k₂ = k.

At position k: a_k + x_k = a_k + y_k gives x_k = y_k. For i > k: x_i = (a ⊕ x)_i = (a ⊕ y)_i = y_i. For i < k: x_i = 0 = y_i. It remains to establish #x = #y. By T3, a ⊕ x = a ⊕ y implies #(a ⊕ x) = #(a ⊕ y). From TumblerAdd's result-length formula, #(a ⊕ w) = max(k − 1, 0) + (#w − k + 1) for any w with action point k. Since both x and y share the same action point k, we get #x = #y. By T3 (same length, same components), x = y.  ∎


## TA-RC — Right cancellation fails

There exist tumblers a, b, w with a ≠ b and a ⊕ w = b ⊕ w (both sides well-defined).

In words: TumblerAdd is not right-cancellative — equal results under the same displacement do not imply equal start positions.

*Proof by example.* Let a = [1, 3, 5], b = [1, 3, 7], and w = [0, 2, 4] (action point k = 2). Then:

  a ⊕ w = [1, 3 + 2, 4] = [1, 5, 4]
  b ⊕ w = [1, 3 + 2, 4] = [1, 5, 4]  (component 3 of b is discarded — tail replacement)

So a ⊕ w = b ⊕ w = [1, 5, 4] despite a ≠ b — the difference at position 3 is erased by tail replacement.  ∎


## TA-MTO — ManyToOneEquivalence

For any displacement w with action point k and any tumblers a, b with #a ≥ k and #b ≥ k: a ⊕ w = b ⊕ w if and only if a_i = b_i for all 1 ≤ i ≤ k.

In words: a and b produce the same result under w if and only if they agree on their first k components, where k is the action point of w.

*Proof (forward).* Assume a_i = b_i for all 1 ≤ i ≤ k. From TumblerAdd's definition: for i < k, (a ⊕ w)_i = a_i = b_i = (b ⊕ w)_i. At i = k, (a ⊕ w)_k = a_k + w_k = b_k + w_k = (b ⊕ w)_k. For i > k, (a ⊕ w)_i = w_i = (b ⊕ w)_i. The results have the same length (max(k − 1, 0) + (#w − k + 1) depends only on k and #w). By T3, a ⊕ w = b ⊕ w.  ∎

*Proof (converse).* Suppose a ⊕ w = b ⊕ w. Let k be the action point of w. We must show a_i = b_i for all 1 ≤ i ≤ k.

(a) For i < k: position i falls in the "copy from start" region of TumblerAdd, so (a ⊕ w)_i = a_i and (b ⊕ w)_i = b_i. From a ⊕ w = b ⊕ w we get a_i = b_i.

(b) At i = k: (a ⊕ w)_k = a_k + w_k and (b ⊕ w)_k = b_k + w_k. Equality gives a_k + w_k = b_k + w_k, hence a_k = b_k by cancellation in ℕ.

Components after k are unconstrained: for i > k, (a ⊕ w)_i = w_i = (b ⊕ w)_i regardless of a_i and b_i.  ∎


## D0 — Displacement well-definedness

a < b, and the divergence k of a and b satisfies k ≤ #a.

In words: the displacement b ⊖ a is well-defined and TA0 is satisfied for a ⊕ (b ⊖ a) exactly when a is strictly less than b and their divergence point lies within the length of a.


## D1 — Displacement round-trip

For tumblers a, b ∈ T with a < b, divergence(a, b) ≤ #a, and #a ≤ #b:

  a ⊕ (b ⊖ a) = b

In words: when D0 holds and a is no longer than b, applying the displacement from a to b recovers b exactly.

*Proof.* Let k = divergence(a, b). By hypothesis k ≤ #a ≤ #b, so this is type (i) divergence with aₖ < bₖ. Define w = b ⊖ a by TumblerSub: wᵢ = 0 for i < k, wₖ = bₖ − aₖ, wᵢ = bᵢ for i > k. The result has length max(#a, #b) = #b. Now w > 0 since wₖ > 0, and the action point of w is k ≤ #a, so TA0 is satisfied. Applying TumblerAdd: (a ⊕ w)ᵢ = aᵢ = bᵢ for i < k (before divergence), (a ⊕ w)ₖ = aₖ + (bₖ − aₖ) = bₖ, and (a ⊕ w)ᵢ = wᵢ = bᵢ for i > k. The result has length #w = #b; every component matches b, so a ⊕ w = b by T3.  ∎

## D2 — Displacement uniqueness

Under D1's preconditions (a < b, divergence(a, b) ≤ #a, #a ≤ #b), if a ⊕ w = b then w = b ⊖ a.

In words: given the preconditions of D1, the displacement that recovers b from a is unique.

*Proof.* By D1, a ⊕ (b ⊖ a) = b. So a ⊕ w = a ⊕ (b ⊖ a), and by TA-LC, w = b ⊖ a.  ∎


### Ordinal displacement and shift


## OrdinalDisplacement — ZeroPrefixedDepthMTumbler (DEFINITION, function)

For natural number n ≥ 1 and depth m ≥ 1, the *ordinal displacement* δ(n, m) is the tumbler [0, 0, ..., 0, n] of length m — zero at positions 1 through m − 1, and n at position m. Its action point is m.

In words: δ(n, m) is the unique depth-m displacement whose only nonzero component is n at position m.

When the depth is determined by context (typically m = #v for the tumbler being shifted), we write δₙ.


## OrdinalShift — ShiftByOrdinal (DEFINITION, function)

For a tumbler v of length m and natural number n ≥ 1:

`shift(v, n) = v ⊕ δ(n, m)`

In words: shift(v, n) advances the deepest component of v by n, leaving all higher-level components unchanged.

TA0 is satisfied: the action point of δ(n, m) is m = #v, so k ≤ #v holds trivially. By TumblerAdd: shift(v, n)ᵢ = vᵢ for i < m, and shift(v, n)ₘ = vₘ + n.

When m ≥ 2, shift(v, n)₁ = v₁. When m = 1, shift([S], n) = [S + n]. Furthermore, #shift(v, n) = #δₙ = m = #v. Since n ≥ 1, component positivity holds: shift(v, n)ₘ = vₘ + n ≥ 1 unconditionally for all vₘ ≥ 0.


## TS1 — ShiftPreservesStrictOrder

`(A v₁, v₂, n : n ≥ 1 ∧ #v₁ = #v₂ = m ∧ v₁ < v₂ : shift(v₁, n) < shift(v₂, n))`

In words: shift preserves strict order between same-depth tumblers.

*Derivation.* Fix n ≥ 1. Since #v₁ = #v₂ = m and v₁ ≠ v₂, the divergence point satisfies divergence(v₁, v₂) ≤ m. The action point of δₙ is m ≥ divergence(v₁, v₂). By TA1-strict: v₁ ⊕ δₙ < v₂ ⊕ δₙ. ∎


## TS2 — ShiftInjectivity

`(A v₁, v₂, n : n ≥ 1 ∧ #v₁ = #v₂ = m : shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂)`

In words: shift is injective on same-depth tumblers.

*Derivation.* Fix n ≥ 1. By TA-MTO: v₁ ⊕ δₙ = v₂ ⊕ δₙ iff (A i : 1 ≤ i ≤ m : v₁ᵢ = v₂ᵢ). The action point of δₙ is m, and agreement at positions 1..m for tumblers of length m means v₁ = v₂ by T3 (CanonicalRepresentation). ∎

## TS3 — ShiftComposition

`(A v, n₁, n₂ : n₁ ≥ 1 ∧ n₂ ≥ 1 ∧ #v = m : shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂))`

In words: composing two shifts is equivalent to a single shift by the sum of the amounts.

*Derivation.* We expand both sides component-wise using TumblerAdd's constructive definition.

Left side: let u = shift(v, n₁) = v ⊕ δ(n₁, m). By TumblerAdd, uᵢ = vᵢ for i < m, uₘ = vₘ + n₁, and #u = m. Now shift(u, n₂) = u ⊕ δ(n₂, m). By TumblerAdd, the result has components uᵢ = vᵢ for i < m, and uₘ + n₂ = vₘ + n₁ + n₂ at position m. Length is m.

Right side: shift(v, n₁ + n₂) = v ⊕ δ(n₁ + n₂, m). By TumblerAdd, components are vᵢ for i < m, and vₘ + (n₁ + n₂) at position m. Length is m.

Both sides have length m and agree at every component (natural-number addition is associative: vₘ + n₁ + n₂ = vₘ + (n₁ + n₂)). By T3: they are equal. ∎

## TS4 — ShiftStrictlyIncreases

`(A v, n : n ≥ 1 ∧ #v = m : shift(v, n) > v)`

In words: every positive shift strictly increases the tumbler.

*Derivation.* δ(n, m) > 0 since its m-th component is n ≥ 1. By TA-strict: v ⊕ δ(n, m) > v. ∎

## TS5 — ShiftAmountMonotone

`(A v, n₁, n₂ : n₁ ≥ 1 ∧ n₂ > n₁ ∧ #v = m : shift(v, n₁) < shift(v, n₂))`

In words: a larger shift amount produces a strictly larger tumbler.

*Derivation.* Write n₂ = n₁ + (n₂ − n₁) where n₂ − n₁ ≥ 1. By TS3: shift(v, n₂) = shift(shift(v, n₁), n₂ − n₁). By TS4: shift(shift(v, n₁), n₂ − n₁) > shift(v, n₁). ∎

### Increment for allocation

We define the *last significant position* of a tumbler `t`. When `t` has at least one nonzero component, `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})` — the position of the last nonzero component. When every component is zero, `sig(t) = #t`.

For valid addresses, `sig(t)` falls within the last populated field. This is a consequence of T4's positive-component constraint: every field component is strictly positive, so the last component of the last field is nonzero, and `sig(t) = #t`. Therefore `inc(t, 0)` on a valid address increments the last component of the last field, modifying only within that field and preserving the hierarchical structure.
