# ASN-0034 Formal Statements

*Source: ASN-0034-tumbler-algebra.md (revised 2026-03-26) — Extracted: 2026-04-09*

## T0 — CarrierSetDefinition

`T = {d₁.d₂. ... .dₙ : each dᵢ ∈ ℕ, n ≥ 1}`. The carrier set T is the set of all finite, non-empty sequences of natural numbers. ℕ is taken with its standard properties, including closure under successor and addition.

In words: a tumbler is any finite sequence of one or more natural numbers. There is no constraint on component values or sequence length beyond membership in ℕ and non-emptiness.

*Axiom:* T is the set of all finite sequences over ℕ with length ≥ 1; ℕ is closed under successor and addition.

---

## T0(a) — UnboundedComponentValues

Every component value of a tumbler is unbounded — no maximum value exists.

In words: for any component position in any tumbler, any natural number may appear there. No component is capped by a finite maximum.

---

## T0(b) — UnboundedLength

Tumblers of arbitrary length exist in T — the hierarchy has unlimited nesting depth.

In words: for any finite depth n ≥ 1, there exist tumblers with exactly n components. The tumbler hierarchy imposes no ceiling on nesting depth.

---

## T1 — LexicographicOrder

For tumblers `a = a₁. ... .aₘ` and `b = b₁. ... .bₙ`, define `a < b` iff there exists `k ≥ 1` such that `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either:

  (i) `k ≤ min(m, n)` and `aₖ < bₖ`, or

  (ii) `k = m + 1 ≤ n` (that is, `a` is a proper prefix of `b`).

Sub-properties of `<` as a strict total order on T:

- *(a) Irreflexivity:* `(A a ∈ T :: ¬(a < a))`
- *(b) Trichotomy:* `(A a, b ∈ T :: exactly one of a < b, a = b, b < a)`
- *(c) Transitivity:* `(A a, b, c ∈ T : a < b ∧ b < c : a < c)`

In words: tumblers are totally ordered by comparing components left-to-right, with a prefix strictly less than any proper extension. The order is self-contained — comparison examines at most min(#a, #b) component pairs and requires no external index or registry. This total order underpins the tumbler line on which spans are defined as contiguous intervals.

*Definition:* `a < b` iff `∃ k ≥ 1` with `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either (i) `k ≤ min(m,n) ∧ aₖ < bₖ`, or (ii) `k = m+1 ≤ n`.

*Postconditions:* (a) Irreflexivity — `(A a ∈ T :: ¬(a < a))`. (b) Trichotomy — `(A a,b ∈ T :: exactly one of a < b, a = b, b < a)`. (c) Transitivity — `(A a,b,c ∈ T : a < b ∧ b < c : a < c)`.

## T2 — IntrinsicComparison

**T2 (IntrinsicComparison).** The order relation T1 is computable from the two tumblers alone, without consulting any external data structure. The comparison examines at most `min(#a, #b)` component pairs.

Tumbler comparison requires only the two addresses themselves — no external index, allocator state, or global registry participates in the decision. The comparison scans for the first diverging component pair and terminates as soon as one is found or the shorter tumbler is exhausted.

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` — two well-formed tumblers (finite sequences over ℕ with `#a ≥ 1` and `#b ≥ 1`, per T0).
- *Postconditions:* (a) The ordering among `a` and `b` under T1 is determined. (b) At most `min(#a, #b)` component pairs are examined. (c) The only values consulted are `{aᵢ : 1 ≤ i ≤ #a}`, `{bᵢ : 1 ≤ i ≤ #b}`, `#a`, and `#b`.
- *Frame:* No external data structure is read or modified — the comparison is a pure function of the two tumblers.


## T3 — CanonicalRepresentation

**T3 (CanonicalRepresentation).** `(A a, b ∈ T : a₁ = b₁ ∧ ... ∧ aₙ = bₙ ∧ #a = #b ≡ a = b)`.

Tumbler equality is sequence equality: two tumblers are identical if and only if they have the same length and the same component at every position. No quotient, normalization, or external identification is imposed — each abstract tumbler has exactly one representation.

*Formal Contract:*
- *Postconditions:* Tumbler equality is sequence equality: `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. No quotient, normalization, or external identification is imposed on T.


## T4 — HierarchicalParsing

An address tumbler has the form:

`t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`

where each `Nᵢ, Uⱼ, Dₖ, Eₗ > 0`. The four fields are:
- **Node field** `N₁. ... .Nₐ`: identifies the server.
- **User field** `U₁. ... .Uᵦ`: identifies the account.
- **Document field** `D₁. ... .Dᵧ`: identifies the document and version.
- **Element field** `E₁. ... .Eδ`: identifies the content element. The first component distinguishes the subspace: 1 for text content, 2 for links.

Define `zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`. The count of zero-valued components uniquely determines the hierarchical level:
- `zeros(t) = 0`: `t` is a node address (node field only),
- `zeros(t) = 1`: `t` is a user address (node and user fields),
- `zeros(t) = 2`: `t` is a document address (node, user, and document fields),
- `zeros(t) = 3`: `t` is an element address (all four fields).

**T4 (HierarchicalParsing).** Every tumbler `t ∈ T` used as an address contains at most three zero-valued components, appearing in order as field separators, every non-separator component is strictly positive, and every field present in the address has at least one component. Formally, if `t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`, then `(A i : 1 ≤ i ≤ α : Nᵢ > 0)`, `(A j : 1 ≤ j ≤ β : Uⱼ > 0)`, `(A k : 1 ≤ k ≤ γ : Dₖ > 0)`, `(A l : 1 ≤ l ≤ δ : Eₗ > 0)`, and `α ≥ 1`, `β ≥ 1` when present, `γ ≥ 1` when present, `δ ≥ 1` when present. The *positive-component constraint* holds: every component of every field is strictly positive. The non-empty field constraint — each present field has at least one component — is equivalent to three syntactic conditions: no two zeros are adjacent, the tumbler does not begin with zero, and the tumbler does not end with zero; T4a (SyntacticEquivalence) establishes this equivalence.

Address tumblers encode a four-field containment hierarchy (node, user, document, element) using zero-valued components as field separators. The count of zeros determines the hierarchical level bijectively; the positive-component constraint ensures zeros function exclusively as separators and the parse is unambiguous.

*Formal Contract:*
- *Axiom:* Valid address tumblers satisfy: `zeros(t) ≤ 3`; every non-separator component is strictly positive (positive-component constraint); every field present in the address has at least one component (non-empty field constraint).
- *Preconditions:* T3 (CanonicalRepresentation) — tumbler equality is sequence equality, guaranteeing that the component sequence of `t` is fixed and the separator positions computed by scanning for zeros are uniquely determined. Required for the T4b uniqueness result.
- *Postconditions:* (T4a) The non-empty field constraint — each present field has `≥ 1` component — is equivalent to the three syntactic conditions: no adjacent zeros, `t₁ ≠ 0`, `t_{#t} ≠ 0`. (T4b) For every valid address tumbler `t`, `fields(t)` is well-defined and computable from `t` alone; the decomposition into node, user, document, and element fields is unique. (T4c) `zeros(t) ∈ {0, 1, 2, 3}` determines the hierarchical level bijectively: `0 ↔ node`, `1 ↔ user`, `2 ↔ document`, `3 ↔ element`.


## Prefix — PrefixRelation

**Prefix (PrefixRelation).** `p ≼ q` iff `#p ≤ #q ∧ (A i : 1 ≤ i ≤ #p : qᵢ = pᵢ)`. A proper prefix `p ≺ q` requires `p ≼ q` with `p ≠ q`, entailing `#p < #q`.

`p` is a prefix of `q` when `p` is no longer than `q` and every component of `p` matches the corresponding component of `q`; a proper prefix is strictly shorter.

*Formal Contract:*
- *Definition:* `p ≼ q` iff `#p ≤ #q ∧ (A i : 1 ≤ i ≤ #p : qᵢ = pᵢ)`. Proper prefix: `p ≺ q` iff `p ≼ q ∧ p ≠ q`.


## T5 — ContiguousSubtrees

**T5 (ContiguousSubtrees).** For any tumbler prefix `p`, the set `{t ∈ T : p ≼ t}` forms a contiguous interval under T1:

`[p ≼ a ∧ p ≼ c ∧ a ≤ b ≤ c ⟹ p ≼ b]`

All tumblers sharing a common prefix occupy a contiguous interval in the T1 total order — no tumbler outside the subtree can interleave between two members of it. A span between two endpoints under the same prefix captures exactly the addresses in that subtree between them; no addresses from unrelated subtrees intrude.

*Formal Contract:*
- *Preconditions:* `a, b, c ∈ T`; `p` is a tumbler prefix with `#p ≥ 1`; `p ≼ a`; `p ≼ c`; `a ≤ b ≤ c` under the lexicographic order T1.
- *Postconditions:* `p ≼ b` — the tumbler `b` extends the prefix `p`, and therefore belongs to the same subtree as `a` and `c`.

## T6 — DecidableContainment

**T6 (DecidableContainment).** For any two tumblers `a, b ∈ T`, the following are decidable from the addresses alone:

  (a) Whether `a` and `b` share the same node field.

  (b) Whether `a` and `b` share the same node and user fields.

  (c) Whether `a` and `b` share the same node, user, and document-lineage fields.

  (d) Whether the document field of `a` is a prefix of the document field of `b` (structural subordination within a document family).

In words: containment and membership questions — same server? same account? same document family? is one document subordinate to another? — can be answered by inspecting only the two addresses, with no external registry or system state.

*Preconditions:* `a, b ∈ T` are valid tumblers satisfying T4 (positive-component constraint, at most three zeros, no adjacent zeros, no leading or trailing zero).
*Postconditions:* (a) The procedure terminates and returns YES iff `N(a) = N(b)` (componentwise). (b) The procedure terminates and returns YES iff `zeros(a) ≥ 1 ∧ zeros(b) ≥ 1 ∧ N(a) = N(b) ∧ U(a) = U(b)`; returns NO if either tumbler lacks a user field. (c) The procedure terminates and returns YES iff `zeros(a) ≥ 2 ∧ zeros(b) ≥ 2 ∧ N(a) = N(b) ∧ U(a) = U(b) ∧ D(a) = D(b)`; returns NO if either tumbler lacks a document field. (d) The procedure terminates and returns YES iff `zeros(a) ≥ 2 ∧ zeros(b) ≥ 2 ∧ #D(a) ≤ #D(b) ∧ (A k : 1 ≤ k ≤ #D(a) : D(a)ₖ = D(b)ₖ)`; returns NO if either tumbler lacks a document field. All decisions use only the tumbler representations of `a` and `b`, via `fields(t)` (T4(b)) and componentwise comparison on finite sequences of natural numbers.


## T7 — SubspaceDisjointness

**T7 (SubspaceDisjointness).** The subspace identifier (the first component of the element field) permanently separates the address space into disjoint regions. No tumbler in subspace `s₁` can equal or be confused with a tumbler in subspace `s₂ ≠ s₁`.

  `(A a, b ∈ T : a.E₁ ≠ b.E₁ ⟹ a ≠ b)`

In words: tumblers with different first element-field components belong to permanently disjoint regions of the address space and can never be equal — the subspace identifier is encoded in the address itself, so text addresses and link addresses cannot collide.

*Preconditions:* `a, b ∈ T` with `zeros(a) = zeros(b) = 3` (both are element-level addresses with well-formed field structure per T4).
*Postconditions:* `a.E₁ ≠ b.E₁ ⟹ a ≠ b`.


## NoDeallocation — NoRemovalAxiom

The system defines no operation that removes an element from the set of allocated addresses. No "deallocate", "free", or "reclaim" mechanism exists.

In words: the operation vocabulary is closed under addition only — there is no mechanism to shrink the allocated set, making allocation monotone by design constraint.

*Axiom:* The system's operation vocabulary contains no operation that removes an element from the allocated set.


## T8 — AllocationPermanence

**T8 (AllocationPermanence).** If tumbler `a ∈ T` has been allocated at any point in the system's history, then for all subsequent states, `a` remains in the set of allocated addresses. No operation removes an allocated address from the address space. The set of allocated addresses is monotonically non-decreasing.

In words: once allocated, an address is permanent — no system operation can remove it. The allocated set can only grow, which is the structural basis for the permanent-link guarantee.

*Invariant:* For every state transition s → s', `allocated(s) ⊆ allocated(s')`.
*Depends:* NoDeallocation (the system defines no removal operation — the closed-world constraint that makes the case analysis exhaustive); T10a (allocation is insert-only — sibling allocation by repeated `inc(·, 0)` and child-spawning by `inc(·, k')` with `k' > 0` — characterizing both operations that modify the allocated set).
*Frame:* Read-only operations (T1, T2, T4) and pure arithmetic (⊕, ⊖) preserve the allocated set exactly: `allocated(s') = allocated(s)`. Allocation transitions (T10a) — both sibling allocation via `inc(·, 0)` and child-spawning via `inc(·, k')` with `k' > 0` — extend the set: `allocated(s') = allocated(s) ∪ {a_new}` for some fresh address `a_new`.


## T9 — ForwardAllocation

**T9 (ForwardAllocation).** T10a below defines the allocation mechanism: each allocator advances by `inc(·, 0)`, incrementing by exactly 1 at the last significant position. Since `inc` produces a strictly greater tumbler at each step (TA5(a)), it follows that within each allocator's sequential stream, new addresses are strictly monotonically increasing:

  `(A a, b : same_allocator(a, b) ∧ allocated_before(a, b) : a < b)`

In words: within a single allocator's sibling stream, each newly allocated address is strictly greater than all previous ones — allocation proceeds forward only. This guarantee is per-allocator: globally, children spawned via deep increment are inserted between a parent and its next sibling regardless of wall-clock creation order, so the full tumbler line does not grow monotonically by time.

*Preconditions:* `a, b ∈ T` with `same_allocator(a, b) ∧ allocated_before(a, b)` — both addresses produced by the same allocator's sibling stream, `a` allocated before `b`.
*Postconditions:* `a < b` under the tumbler order T1.

## T10 — PartitionIndependence

Let `p₁, p₂ ∈ T` with `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` (neither is a prefix of the other), and let `a, b ∈ T` with `p₁ ≼ a` and `p₂ ≼ b`. Then `a ≠ b`.

In words: two allocators operating under non-nesting prefixes are guaranteed to produce distinct addresses with no coordination. The address structure itself makes collision impossible — no central allocator or protocol is required.

*Formal Contract:*
- *Preconditions:* `p₁, p₂ ∈ T` with `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`; `a, b ∈ T` with `p₁ ≼ a` and `p₂ ≼ b`.
- *Postconditions:* `a ≠ b`.


## T10a — AllocatorDiscipline

Allocators produce sibling outputs exclusively by `inc(·, 0)`. To spawn a child allocator, the parent performs exactly one `inc(·, k')` with `k' ∈ {1, 2}` satisfying the TA5a bounds (`k' = 1` when `zeros(t) ≤ 3`, `k' = 2` when `zeros(t) ≤ 2`) to establish the child's prefix, after which the parent resumes sibling production with `inc(·, 0)`. This axiom establishes four consequences:
- T10a.1 (Uniform sibling length): all siblings have length `#b` for base address `b`.
- T10a.2 (Non-nesting sibling prefixes): distinct siblings from the same allocator are prefix-incomparable.
- T10a.3 (Length separation): a child spawned via `inc(·, k')` from a parent of base length `m` produces outputs of length `m + k'`; across `d` nesting levels, separation is `m + k'₁ + … + k'_d`.
- T10a.4 (T4 preservation): every output of a conforming allocator satisfies T4.
- T10a-N (Necessity): under the relaxed rule (any `k ≥ 0` in the sibling stream), the pair `a₁ = inc(b, 0)` and `a₂ = inc(a₁, k')` with `k' > 0` satisfies `a₁ ≺ a₂`, violating the T10 precondition.

In words: the discipline pins each allocator to a single address length for its sibling stream and allows depth to grow only through controlled deep increments. This guarantees prefix-incomparability of siblings, length separation between parent and child domains, and T4 compliance throughout — and the `k = 0` restriction for siblings is not merely sufficient but necessary.

*Formal Contract:*
- *Axiom:* Allocators produce sibling outputs exclusively by `inc(·, 0)`; child-spawning uses exactly one `inc(·, k')` with `k' ∈ {1, 2}` satisfying the TA5a bounds (`k' = 1` when `zeros(t) ≤ 3`, `k' = 2` when `zeros(t) ≤ 2`) to establish the child's prefix, after which the parent resumes sibling production with `inc(·, 0)`.
- *Postconditions:*
  - T10a.1 (Uniform sibling length): For every allocator with base address b, all sibling outputs a satisfy #a = #b.
  - T10a.2 (Non-nesting sibling prefixes): For all siblings a, b from the same allocator, same_allocator(a, b) ∧ a ≠ b → a and b are prefix-incomparable, satisfying the precondition of T10.
  - T10a.3 (Length separation): For every child allocator spawned by `inc(·, k')` with k' ∈ {1, 2} from a parent with base length m, all child outputs c satisfy #c = m + k', and across d nesting levels the separation is exact: #output = m + k'₁ + k'₂ + … + k'_d.
  - T10a.4 (T4 preservation): Since siblings use `inc(·, 0)` (unconditionally T4-preserving by TA5a) and child-spawning uses `k' ∈ {1, 2}` within TA5a bounds, every output of a conforming allocator satisfies T4.
  - T10a-N (Necessity): Under the relaxed rule (any k ≥ 0 in the sibling stream), the pair a₁ = inc(b, 0) and a₂ = inc(a₁, k') with k' > 0 are sibling outputs satisfying a₁ ≺ a₂ — by TA5(b) (agreement on all positions of a₁) and TA5(d) (#a₂ > #a₁), invoking T1 case (ii). This violates the T10 precondition. The axiom is therefore both sufficient (T10a.1–T10a.3) and necessary for prefix-incomparability of sibling outputs.


## PrefixOrderingExtension — ExtensionOrderPreservation

Let `p₁, p₂ ∈ T` with `p₁ < p₂` (T1) and `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` (non-nesting). Then for every `a` with `p₁ ≼ a` and every `b` with `p₂ ≼ b`: `a < b`. Formally: `(A a, b ∈ T : p₁ ≼ a ∧ p₂ ≼ b : a < b)`.

In words: when two non-nesting prefixes are ordered under T1, that ordering propagates to all their extensions. Every address under the smaller prefix is strictly less than every address under the larger prefix, regardless of what components follow.

*Formal Contract:*
- *Preconditions:* `p₁, p₂ ∈ T` with `p₁ < p₂` (T1) and `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` (non-nesting); `a, b ∈ T` with `p₁ ≼ a` and `p₂ ≼ b`.
- *Postconditions:* `a < b` under T1.


## PartitionMonotonicity — PartitionAllocationOrdering

Within any prefix-delimited partition with prefix `p ∈ T`, the set of allocated addresses is totally ordered by T1 consistently with per-allocator allocation order. Sub-partition prefixes `t₀, t₁, t₂, …` — where `t₀ = inc(s, k)` with `k > 0` and `p ≼ s`, and `tₙ₊₁ = inc(tₙ, 0)` for `n ≥ 0` — have uniform length (T10a.1), are strictly increasing under T1 (TA5(a)), and are pairwise non-nesting. For sibling sub-partition prefixes `tᵢ < tⱼ` (`i < j`) and any `a, b ∈ T` with `tᵢ ≼ a` and `tⱼ ≼ b`: `a < b`. Within each sub-partition, all allocated addresses are totally ordered by T1 consistently with per-allocator allocation order.

In words: the prefix hierarchy imposes a total order on all allocated addresses within any partition. Sibling sub-partitions inherit the prefix ordering — every address under a smaller prefix precedes every address under a larger one — and within each sub-partition this ordering is consistent with allocation sequence.

*Formal Contract:*
- *Preconditions:* A system conforming to T10a (allocator discipline); a partition with prefix `p ∈ T`; a child prefix `t₀ = inc(s, k)` with `k > 0` and `p ≼ s`, established by the parent allocator's single deep increment; sub-partition prefixes `t₀, t₁, t₂, ...` where `t₀` is the initial child prefix and `tₙ₊₁ = inc(tₙ, 0)` for all `n ≥ 0`.
- *Postconditions:* (1) For sibling sub-partition prefixes `tᵢ < tⱼ` (with `0 ≤ i < j`) and any `a, b ∈ T` with `tᵢ ≼ a` and `tⱼ ≼ b`: `a < b`. (2) Within each sub-partition with prefix `tᵢ` (for `i ≥ 0`), for any `a, b` allocated by the same allocator: `allocated_before(a, b) ⟹ a < b`.
- *Invariant:* For every reachable system state, the set of allocated addresses within any prefix-delimited partition is totally ordered by T1 consistently with per-allocator allocation order.


## GlobalUniqueness — UniqueAddressAllocation

For any `a, b ∈ T` produced by distinct allocation events within a system conforming to T10a: `a ≠ b`. This holds regardless of whether the events originate from the same allocator, sibling allocators at the same level, or allocators at different hierarchical levels.

In words: no two distinct allocation events anywhere in the system, at any time, produce the same address. Global uniqueness is guaranteed by the structure of the names alone — no distributed consensus, coordination protocol, or central authority is required.

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` produced by distinct allocation events within a system conforming to T10a (allocator discipline).
- *Invariant:* For every pair of addresses `a, b` produced by distinct allocation events in any reachable system state: `a ≠ b`.

## T12 — SpanWellDefinedness

**T12 (SpanWellDefinedness).** A span `(s, ℓ)` is well-formed when `ℓ > 0` and the action point `k` of `ℓ` satisfies `k ≤ #s`. Equivalently, the number of leading zeros in `ℓ` must be strictly less than `#s`. A well-formed span denotes the set `{t ∈ T : s ≤ t < s ⊕ ℓ}`. This set is contiguous under T1 — there is no tumbler between two members that is not itself a member.

In words: a span is defined by a start address and a positive displacement; the displacement must act at a hierarchical level no deeper than the start address. The span denotes a non-empty, contiguous range of tumblers from the start up to (but not including) the advanced endpoint.

*Preconditions:* `s ∈ T`, `ℓ ∈ T`, `ℓ > 0`, `actionPoint(ℓ) ≤ #s`
*Definition:* `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}`
*Postconditions:* (a) `s ⊕ ℓ ∈ T` (endpoint exists, by TA0). (b) `s ∈ span(s, ℓ)` (non-empty, by TA-strict). (c) `span(s, ℓ)` is order-convex under T1 (for all `a, c ∈ span(s, ℓ)` and `b ∈ T`, `a ≤ b ≤ c` implies `b ∈ span(s, ℓ)`).


## TA0 — WellDefinedAddition

**TA0 (WellDefinedAddition).** For tumblers `a, w ∈ T` where `w > 0` and the action point `k` of `w` satisfies `k ≤ #a`, the result `a ⊕ w` is a well-defined tumbler in `T`.

For a positive displacement `w = [w₁, w₂, ..., wₙ]`, the action point is `k = min({i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0})`. The constructive definition (TumblerAdd) builds `r = a ⊕ w = [r₁, ..., rₙ]` by three rules: `rᵢ = aᵢ` for `1 ≤ i < k` (copy from start); `rₖ = aₖ + wₖ` (single-component advance); `rᵢ = wᵢ` for `k < i ≤ n` (copy from displacement).

In words: tumbler addition advances a position `a` by displacement `w`, acting at the hierarchical level of `w`'s first nonzero component. The action point must not exceed the depth of the start position; the result has the same length as the displacement.

*Preconditions:* `a ∈ T`, `w ∈ T`, `w > 0`, `actionPoint(w) ≤ #a`
*Postconditions:* `a ⊕ w ∈ T`, `#(a ⊕ w) = #w`


## TA1 — OrderPreservationUnderAddition

`(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) : a ⊕ w ≤ b ⊕ w)`, where `k` is the action point of `w`.

In words: adding the same displacement to two ordered positions preserves their relative order (weakly). If two addresses were in order before advancement, they remain in non-reversed order after — the displacement cannot flip their relative position. The precondition `k ≤ min(#a, #b)` ensures both additions are well-defined by TA0.

*Preconditions:* `a ∈ T`, `b ∈ T`, `w ∈ T`, `a < b`, `w > 0`, `actionPoint(w) ≤ min(#a, #b)`
*Postconditions:* `a ⊕ w ≤ b ⊕ w`


## Divergence — FirstDivergence

For tumblers `a, b ∈ T` with `a ≠ b`, the *divergence* `divergence(a, b)` is defined by two cases:

  (i) If there exists `k ≤ min(#a, #b)` such that `aₖ ≠ bₖ` and `(A i : 1 ≤ i < k : aᵢ = bᵢ)`, then `divergence(a, b) = k` — component divergence at a shared position.

  (ii) If `(A i : 1 ≤ i ≤ min(#a, #b) : aᵢ = bᵢ)` and `#a ≠ #b`, then `divergence(a, b) = min(#a, #b) + 1` — prefix divergence, where one tumbler is a proper prefix of the other.

Exactly one case applies for any `a ≠ b`.

In words: the divergence of two distinct tumblers is the index of their first disagreement — either the first component position where their values differ (case i), or one past the shorter tumbler's last component when one is a proper prefix of the other (case ii).

*Definition:* For `a, b ∈ T` with `a ≠ b`: (i) if `∃ k ≤ min(#a, #b)` with `aₖ ≠ bₖ` and `(A i : 1 ≤ i < k : aᵢ = bᵢ)`, then `divergence(a, b) = k`; (ii) if `(A i : 1 ≤ i ≤ min(#a, #b) : aᵢ = bᵢ)` and `#a ≠ #b`, then `divergence(a, b) = min(#a, #b) + 1`. Exactly one case applies.


## TA1-strict — StrictOrderPreservation

`(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) ∧ k ≥ divergence(a, b) : a ⊕ w < b ⊕ w)`, where `k` is the action point of `w`.

In words: strict order is preserved by addition when the displacement acts at or beyond the point where the two addresses first differ. When the action point falls before the divergence, both operands agree at the action point and receive the same increment, so the result is equal rather than strictly ordered — the strict guarantee requires the displacement to reach the original disagreement.

*Preconditions:* `a ∈ T`, `b ∈ T`, `w ∈ T`, `a < b`, `w > 0`, `actionPoint(w) ≤ min(#a, #b)`, `actionPoint(w) ≥ divergence(a, b)`
*Postconditions:* `a ⊕ w < b ⊕ w`

## TA-strict — StrictIncrease

`(A a ∈ T, w > 0 : a ⊕ w > a)` (where `a ⊕ w` is well-defined, i.e., `k ≤ #a` per TA0).

In words: advancing a tumbler by any positive displacement strictly increases its position. This excludes the degenerate model in which `a ⊕ w = a` for all inputs — a model that satisfies TA0, TA1, and TA4, yet collapses every span `[s, s ⊕ ℓ)` to the empty interval `[s, s)`.

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `w > 0`, `k ≤ #a` where `k` is the action point of `w`
- *Postconditions:* `a ⊕ w > a`


## TA2 — WellDefinedSubtraction

Let `⊖` denote tumbler subtraction: given two positions, compute the displacement between them.

**TA2 (WellDefinedSubtraction).** For tumblers `a, w ∈ T` where `a ≥ w`, `a ⊖ w` is a well-defined tumbler in `T`.

In words: subtraction is total on the ordered domain — whenever `a` dominates `w`, their difference `a ⊖ w` exists and is a valid tumbler. This guarantees that span widths can always be computed from a start and end position.

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, a ≥ w
- *Postconditions:* a ⊖ w ∈ T


## TA3 — OrderPreservationUnderSubtractionWeak

`(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w ≤ b ⊖ w)`.

In words: subtracting a common lower bound from two ordered tumblers preserves their relative order weakly. If `a` precedes `b` and both dominate `w`, then `a ⊖ w` does not exceed `b ⊖ w`. This ensures that relative position is invariant under re-basing to a common origin.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w
- *Postconditions:* a ⊖ w ≤ b ⊖ w


## TA3-strict — OrderPreservationUnderSubtractionStrict

`(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b : a ⊖ w < b ⊖ w)`.

In words: when `a` and `b` have equal depth, subtracting a common lower bound preserves strict order. The equal-length condition is necessary — without it, length differences can collapse strict inequality to equality after subtraction.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w, #a = #b
- *Postconditions:* a ⊖ w < b ⊖ w


## TA4 — PartialInverse

`(A a, w : w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊕ w) ⊖ w = a)`, where `k` is the action point of `w`.

In words: addition and subtraction are partial inverses under three joint conditions — the action point of `w` lands at `a`'s last component, `w` has no trailing components beyond that point, and all components of `a` before the action point are zero. When all three hold, the round-trip `(a ⊕ w) ⊖ w` recovers `a` exactly. These conditions are not restrictions but the precise characterization of when the inverse relationship holds; when any fails, information is structurally lost and recovery is impossible.

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `w > 0`, `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`, where `k` is the action point of `w`
- *Postconditions:* `(a ⊕ w) ⊖ w = a`

## ReverseInverse — SubtractAddRecovery

`(A a, w : a ≥ w ∧ w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊖ w) ⊕ w = a)`, where `k` is the action point of `w`.

In words: when `w` is a positive tumbler whose action point equals the full length of `a`, and all components of `a` before that action point are zero, subtracting `w` from `a` and re-adding `w` recovers `a` exactly. The two operations are mutually inverse under these structural alignment conditions.

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `a ≥ w`, `w > 0`, `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`, where `k` is the action point of `w`
- *Postconditions:* `(a ⊖ w) ⊕ w = a`


## TumblerAdd — PositionAdvance

For `a = [a₁, ..., aₘ]` and `w = [w₁, ..., wₙ]` with `a, w ∈ T` and `w > 0`, let `k = min{i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0}` be the action point of `w`. Require `k ≤ m`. The result `a ⊕ w = [r₁, ..., rₙ]` is defined component-wise:

```
         ⎧ aᵢ           if i < k        (copy from start)
rᵢ   =  ⎨ aₖ + wₖ      if i = k        (single-component advance)
         ⎩ wᵢ           if i > k        (copy from displacement)
```

**Result-length identity:** `#(a ⊕ w) = #w`.

**Closure:** `a ⊕ w ∈ T`.

Three semantic properties of this definition:
- **No carry propagation:** the advance `aₖ + wₖ` is a single natural-number addition with no carry into position `k − 1`.
- **Tail replacement, not tail addition:** components of `a` at positions `k + 1, ..., m` are discarded; trailing structure comes entirely from `w`.
- **Many-to-one:** distinct start positions that differ only in trailing components beyond the action point produce the same result.

In words: tumbler addition is a position-advance operation — given a start position and a displacement, it copies the prefix of the start up to the action point, advances the action-point component, and takes all remaining structure from the displacement. The result length equals the displacement length regardless of the start position length.

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, w > 0, actionPoint(w) ≤ #a
- *Definition:* k = min{i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0}; rᵢ = aᵢ if i < k; rₖ = aₖ + wₖ; rᵢ = wᵢ if i > k
- *Postconditions:* a ⊕ w ∈ T, #(a ⊕ w) = #w


## TumblerSub — PositionReverse

When operands have different lengths, zero-pad the shorter to `max(#a, #w)`, writing `aᵢ = 0` for `i > #a` and `wᵢ = 0` for `i > #w`. Let `k = zpd(a, w)` be the first position at which the zero-padded sequences disagree. This concept is distinct from the formal Divergence: when one operand is a proper prefix of the other, `divergence` reports `min(#a, #w) + 1` at the prefix boundary, whereas `zpd` scans past it to the first position where the padded values actually differ. When no divergence exists, `a ⊖ w = [0, ..., 0]` of length `max(#a, #w)`. Otherwise:

```
         ⎧ 0             if i < k        (these levels matched — zero them)
rᵢ   =  ⎨ aₖ - wₖ      if i = k        (reverse the advance)
         ⎩ aᵢ           if i > k        (copy from end position, zero-padded)
```

The result has length `max(#a, #w)`.

In words: tumbler subtraction recovers the start position from an end position and displacement. It locates the first zero-padded disagreement, zeroes all positions before it, subtracts at that point, and copies the remaining components from `a`. The result length is determined by the longer of the two operands.

*Formal Contract:*
- *Preconditions:* a ≥ w (when a ≠ w, at the zero-padded divergence k = zpd(a, w), aₖ ≥ wₖ)
- *Definition:* a ⊖ w computed by case analysis on k = zpd(a, w), all component references using zero-padded values (aᵢ = 0 for i > #a, wᵢ = 0 for i > #w); rᵢ = 0 for i < k, rₖ = aₖ − wₖ, rᵢ = aᵢ (zero-padded) for i > k; when no divergence exists, a ⊖ w = [0, …, 0]; #(a ⊖ w) = max(#a, #w)


## TA5 — HierarchicalIncrement

The *last significant position* `sig(t)` of a tumbler is the rightmost nonzero component position, or `#t` when all components are zero. For tumbler `t ∈ T` and level `k ≥ 0`, `inc(t, k)` produces tumbler `t'` such that:

  (a) `t' > t` (strictly greater under T1),

  (b) `t'` agrees with `t` on all components before the increment point,

  (c) when `k = 0` (*sibling*): `#t' = #t`, and `t'` differs from `t` only at position `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`,

  (d) when `k > 0` (*child*): `#t' = #t + k`, the `k − 1` intermediate positions `#t + 1, ..., #t + k − 1` are set to `0` (field separators), and the final position `#t + k` is set to `1` (the first child).

In words: `inc(t, k)` is the allocation increment — it produces the next address past `t` in a partition. With `k = 0` it advances the last significant component (next sibling at the same depth); with `k > 0` it extends the tumbler to produce a first child at depth `k` below `t`. In both cases the result is strictly greater than `t` under T1.

*Formal Contract:*
- *Definition:* `inc(t, k)` for `t ∈ T`, `k ≥ 0`: when `k = 0`, modify position `sig(t)` to `t_{sig(t)} + 1`; when `k > 0`, extend by `k` positions with `k - 1` zeros and final `1`.
- *Postconditions:* (a) `t' > t` under T1. (b) When `k = 0`: `(A i : 1 ≤ i < sig(t) : t'ᵢ = tᵢ)`. When `k > 0`: `(A i : 1 ≤ i ≤ #t : t'ᵢ = tᵢ)`. (c) When `k = 0`: `#t' = #t`, modification only at `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`. (d) When `k > 0`: `#t' = #t + k`, positions `#t + 1 ... #t + k - 1` are `0`, position `#t + k` is `1`.


## TA6 — ZeroTumblers

No zero tumbler is a valid address, and every zero tumbler is less than every positive tumbler:

  `(A t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0) ⟹ t is not a valid address)`

  `(A s, t ∈ T : (A i : 1 ≤ i ≤ #s : sᵢ = 0) ∧ (E j : 1 ≤ j ≤ #t : tⱼ > 0) ⟹ s < t)`

In words: all-zero tumblers are excluded from the address space by T4 (which requires a positive first component), and they sit strictly below every positive tumbler in the T1 order. This makes zero tumblers usable as sentinels — lower bounds that mark uninitialized values or unbounded span endpoints.

*Formal Contract:*
- *Postconditions:* (a) `(A t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0) ⟹ t is not a valid address)`. (b) `(A s, t ∈ T : (A i : 1 ≤ i ≤ #s : sᵢ = 0) ∧ (E j : 1 ≤ j ≤ #t : tⱼ > 0) ⟹ s < t)`.

## PositiveTumbler — PositiveTumbler (DEFINITION, function)

**Definition (PositiveTumbler).** A tumbler `t ∈ T` is *positive*, written `t > 0`, iff at least one of its components is nonzero: `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`. A tumbler is a *zero tumbler* iff every component is zero: `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`. Every positive tumbler is greater than every zero tumbler under T1.

In words: positivity is a component-level test — a tumbler is positive when at least one position is nonzero. Because tumblers of different lengths are distinct (T3), there are infinitely many zero tumblers `[0]`, `[0,0]`, `[0,0,0]`, …, each forming a chain under T1 and each strictly less than every positive tumbler regardless of length.

*Definition:* `t > 0` (positive) iff `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`. Zero tumbler: `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.
*Postconditions:* `(A t ∈ T, z ∈ T : t > 0 ∧ (A i : 1 ≤ i ≤ #z : zᵢ = 0) :: z < t)` — every positive tumbler is strictly greater under T1 than every zero tumbler of any length.


## TA7a — SubspaceClosure

**TA7a (SubspaceClosure).** Define **S** = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)} — ordinals with all positive components, matching T4's positive-component constraint on element fields. In the ordinal-only formulation — where a position in subspace `N` with ordinal `o` passes only `o` to the arithmetic and holds `N` as structural context outside the operands — element-local shift arithmetic satisfies:

  `(A o ∈ S, w > 0 : actionPoint(w) ≤ #o ⟹ o ⊕ w ∈ T)`

  `(A o ∈ S, w > 0 : o ≥ w ⟹ o ⊖ w ∈ T)`

In words: arithmetic on within-subspace ordinals, with the subspace identifier held as structural context rather than as an operand, always produces a result in T. The subspace identifier determines *which* positions are subject to a shift but never enters the arithmetic itself, so no shift can escape the subspace. The natural 2-component formulation `[N, x]` fails for subtraction — `[N, x] ⊖ [0, n]` finds the divergence at the subspace-identifier position and produces a no-op — making the ordinal-only formulation the canonical representation.

*Preconditions:* For `⊕`: `o ∈ S`, `w ∈ T`, `w > 0`, `actionPoint(w) ≤ #o`. For `⊖`: `o ∈ S`, `w ∈ T`, `w > 0`, `o ≥ w`.
*Postconditions:* `o ⊕ w ∈ T`, `#(o ⊕ w) = #w`. `o ⊖ w ∈ T`. For `⊕`, the result is in S when all tail components of `w` (after the action point) are positive. For `⊖` with `actionPoint(w) ≥ 2` and `#w ≤ #o`: the divergence falls at position 1, TumblerSub produces `o` itself (a no-op), and the result is in S. For `⊖` with `actionPoint(w) = 1` and divergence at position `d = 1` (i.e., `o₁ ≠ w₁`): `r₁ = o₁ - w₁ > 0` and `rᵢ = oᵢ > 0` for `i > 1`, so the result is in S when `#w ≤ #o`. For `⊖` with `actionPoint(w) = 1` and divergence at position `d > 1` (i.e., `o₁ = w₁`): the result has `r₁ = 0` and lies in `T \ S` (counterexample: `[5, 3] ⊖ [5, 1] = [0, 2]`). For `⊖` when `#w > #o`: the result inherits trailing zeros at positions `#o + 1` through `#w` and lies in `T \ S`. For `⊖` on single-component ordinals (`#o = 1`, `#w = 1`): the result is in `S ∪ Z`: `[x] ⊖ [n] ∈ S` when `x > n`, and `[x] ⊖ [n] ∈ Z` when `x = n`.
*Frame:* The subspace identifier `N`, held as structural context, is not an operand and is never modified by either operation.
*Definition:* **S** = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)} — ordinals with all positive components, matching T4's positive-component constraint on element fields.


## TA-assoc — AdditionAssociative

**TA-assoc (AdditionAssociative).** Addition is associative where both compositions are defined: `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)` whenever both sides are well-defined. Let `k_b = actionPoint(b)` and `k_c = actionPoint(c)`. The domain conditions are asymmetric: the left side requires `k_b ≤ #a` and `k_c ≤ #b`; the right requires only `min(k_b, k_c) ≤ #a` and `k_c ≤ #b`. On their intersection both sides agree. The action point of the composed displacement `b ⊕ c` satisfies `actionPoint(b ⊕ c) = min(k_b, k_c)`.

In words: applying two sequential displacements gives the same result regardless of grouping. This holds in all three configurations of action points (`k_b < k_c`, `k_b = k_c`, `k_b > k_c`), and the common result length is `#c` in every case.

*Preconditions:* `a ∈ T`, `b ∈ T`, `c ∈ T`, `b > 0`, `c > 0`, `k_b ≤ #a`, `k_c ≤ #b` (where `k_b = actionPoint(b)`, `k_c = actionPoint(c)`; these left-side conditions subsume the right-side conditions since `k_b ≤ #a` implies `min(k_b, k_c) ≤ #a`)
*Postconditions:* `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)`; `#((a ⊕ b) ⊕ c) = #(a ⊕ (b ⊕ c)) = #c`; `actionPoint(b ⊕ c) = min(k_b, k_c)`


## TA-LC — LeftCancellation

**Claim (TA1, weak form).** If `a < b`, `w > 0`, and `actionPoint(w) ≤ min(#a, #b)`, then `a ⊕ w ≤ b ⊕ w`.

**Claim (TA1-strict).** If additionally `actionPoint(w) ≥ divergence(a, b)`, then `a ⊕ w < b ⊕ w`.

**Claim (TA3, weak form).** If `a < b`, `a ≥ w`, and `b ≥ w`, then `a ⊖ w ≤ b ⊖ w`.

**Claim (TA3-strict).** If `a < b`, `a ≥ w`, `b ≥ w`, and `#a = #b`, then `a ⊖ w < b ⊖ w`.

**Claim (TA4).** `(a ⊕ w) ⊖ w = a` under the full precondition: `actionPoint(w) = #a`, `#w = #a`, `(A i : 1 ≤ i < #a : aᵢ = 0)`.

**TA-LC (LeftCancellation).** If `a ⊕ x = a ⊕ y` with both sides well-defined (TA0 satisfied for both), then `x = y`.

In words: the ordering of positions is preserved (weakly) under any common displacement applied to both, and strictly when the displacement reaches the divergence point (TA1/TA3). The round-trip `(a ⊕ w) ⊖ w = a` recovers the original position when the zero-prefix precondition holds (TA4). Left cancellation means the start position can be divided out from equal results: if two displacements applied to the same start yield the same output, the displacements must be identical.

*Preconditions:* `a, x, y ∈ T`; `x > 0`; `y > 0`; `actionPoint(x) ≤ #a`; `actionPoint(y) ≤ #a`; `a ⊕ x = a ⊕ y`
*Postconditions:* `x = y`


## TA-RC — RightCancellationFailure

**TA-RC (RightCancellationFailure).** There exist tumblers `a`, `b`, `w` with `a ≠ b` and `a ⊕ w = b ⊕ w`, both sides well-defined.

In words: knowing the displacement and the result does not uniquely determine the start position. TumblerAdd's tail-replacement rule discards all components of the start after the action point, so any two starts that agree on positions 1..k and differ only beyond k will produce the same result under any displacement with action point k — right cancellation fails.

*Postconditions:* `∃ a, b, w ∈ T : w > 0 ∧ actionPoint(w) ≤ #a ∧ actionPoint(w) ≤ #b ∧ a ≠ b ∧ a ⊕ w = b ⊕ w`

## TA-MTO — ManyToOneEquivalence

For any displacement `w` with action point `k` and any tumblers `a`, `b` with `#a ≥ k` and `#b ≥ k`:

`a ⊕ w = b ⊕ w ⟺ aᵢ = bᵢ for all 1 ≤ i ≤ k`

In words: two tumblers produce the same result under a displacement if and only if they agree on every component up to and including the action point. TumblerAdd's tail-copy rule overwrites all positions past the action point from `w` regardless of input, so only the prefix up to `k` influences the output — inputs that share this prefix are indistinguishable under `w`.

*Formal Contract:*
- *Preconditions:* w ∈ T, w > 0, a ∈ T, b ∈ T, #a ≥ actionPoint(w), #b ≥ actionPoint(w)
- *Postconditions:* a ⊕ w = b ⊕ w ⟺ (A i : 1 ≤ i ≤ actionPoint(w) : aᵢ = bᵢ)


## D0 — DisplacementWellDefined

**D0 (DisplacementWellDefined).** `a < b`, and the divergence `k` of `a` and `b` satisfies `k ≤ #a`.

Under this condition, the displacement `w = b ⊖ a` is a well-defined positive tumbler with `actionPoint(w) = divergence(a, b)` and `#w = max(#a, #b)`, and the addition `a ⊕ w` is well-defined. However, round-trip faithfulness is not guaranteed here: if `#a > #b`, the result has the wrong length and cannot equal `b`. That additional guarantee requires `#a ≤ #b` and is established by D1.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, a < b, divergence(a, b) ≤ #a
- *Postconditions:* b ⊖ a ∈ T, b ⊖ a > 0, actionPoint(b ⊖ a) = divergence(a, b), #(b ⊖ a) = max(#a, #b), a ⊕ (b ⊖ a) ∈ T, #a > #b → a ⊕ (b ⊖ a) ≠ b


## D1 — DisplacementRoundTrip

For tumblers `a`, `b ∈ T` with `a < b`, `divergence(a, b) ≤ #a`, and `#a ≤ #b`:

`a ⊕ (b ⊖ a) = b`

In words: adding the canonical displacement from `a` to `b` back onto `a` exactly recovers `b`. The three preconditions together ensure the subtraction is well-defined, the action point falls within `a`'s length, and the result length matches `b`.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, a < b, divergence(a, b) ≤ #a, #a ≤ #b
- *Postconditions:* a ⊕ (b ⊖ a) = b


## D2 — DisplacementUnique

Under D1's preconditions (`a < b`, `divergence(a, b) ≤ #a`, `#a ≤ #b`), if `a ⊕ w = b` then `w = b ⊖ a`.

In words: `b ⊖ a` is the *only* displacement that carries `a` to `b`. D1 establishes that the canonical displacement works; D2 establishes that no other displacement can. Together they completely characterize the displacement from `a` to `b`.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, divergence(a, b) ≤ #a, #a ≤ #b, a ⊕ w = b
- *Postconditions:* w = b ⊖ a


## OrdinalDisplacement — OrdinalShiftDefinition

**OrdinalDisplacement (OrdinalDisplacement).** For natural number `n ≥ 1` and depth `m ≥ 1`, the *ordinal displacement* `δ(n, m)` is the tumbler `[0, 0, ..., 0, n]` of length `m` — zero at positions `1` through `m − 1`, and `n` at position `m`. Its action point is `m`.

When the depth is determined by context (typically `m = #v` for the tumbler being shifted), we write `δₙ`.

In words: the ordinal displacement is the canonical "advance by `n` at depth `m`" — it leaves all shallower structure unchanged, steps the depth-`m` component forward by `n`, and replaces any deeper structure with nothing. It is the minimal displacement that acts purely at a single depth.

*Formal Contract:*
- *Preconditions:* n ≥ 1, m ≥ 1
- *Definition:* δ(n, m) = [0, 0, …, 0, n] of length m with action point m

## OrdinalShift — ShiftDefinition

`shift(v, n) = v ⊕ δ(n, m)`

The ordinal shift of a tumbler v by a positive integer n advances v's deepest component by exactly n, leaving all higher-level components unchanged. The result is a well-formed tumbler of the same length as v.

*Preconditions:* v ∈ T, n ≥ 1
*Definition:* shift(v, n) = v ⊕ δ(n, m) where m = #v
*Postconditions:* shift(v, n) ∈ T, #shift(v, n) = #v, shift(v, n)ᵢ = vᵢ for i < m, shift(v, n)ₘ = vₘ + n ≥ 1


## TS1 — ShiftOrderPreservation

`(A v₁, v₂, n : n ≥ 1 ∧ #v₁ = #v₂ = m ∧ v₁ < v₂ : shift(v₁, n) < shift(v₂, n))`

Shifting two equal-length tumblers by the same positive amount preserves their strict order. If v₁ precedes v₂ in tumbler order, then shift(v₁, n) still precedes shift(v₂, n) — a uniform shift cannot invert or collapse a strict ordering.

*Preconditions:* v₁ ∈ T, v₂ ∈ T, n ≥ 1, #v₁ = #v₂ = m, v₁ < v₂
*Postconditions:* shift(v₁, n) < shift(v₂, n)


## TS2 — ShiftInjectivity

`(A v₁, v₂, n : n ≥ 1 ∧ #v₁ = #v₂ = m : shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂)`

Ordinal shift is injective on equal-length tumblers: if two tumblers shifted by the same positive amount produce identical results, the original tumblers were identical. No two distinct equal-length tumblers can collide under the same shift.

*Preconditions:* v₁ ∈ T, v₂ ∈ T, n ≥ 1, #v₁ = #v₂ = m
*Postconditions:* shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂


## TS3 — ShiftComposition

`(A v, n₁, n₂ : n₁ ≥ 1 ∧ n₂ ≥ 1 ∧ #v = m : shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂))`

Two successive shifts compose into a single shift whose amount is the sum of the individual amounts. Shifting by n₁ and then by n₂ is exactly equivalent to a single shift by n₁ + n₂.

*Preconditions:* v ∈ T, n₁ ≥ 1, n₂ ≥ 1, #v = m
*Postconditions:* shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂)
*Frame:* #shift(shift(v, n₁), n₂) = #v = m (shift preserves tumbler length)


## TS4 — ShiftStrictIncrease

`(A v, n : n ≥ 1 ∧ #v = m : shift(v, n) > v)`

Every ordinal shift by a positive amount strictly increases the tumbler. The shifted result is always greater than the original — no tumbler can remain in place or retreat under a positive shift.

*Preconditions:* v ∈ T, n ≥ 1, #v = m
*Postconditions:* shift(v, n) > v

## TS5 — ShiftAmountMonotonicity

`(A v, n₁, n₂ : n₁ ≥ 1 ∧ n₂ > n₁ ∧ #v = m : shift(v, n₁) < shift(v, n₂))`

In words: shifting a tumbler by a larger amount always produces a strictly greater result. For any tumbler v and shift amounts n₁ ≥ 1, n₂ > n₁, the shift by n₂ overshoots the shift by n₁ — the shift function is strictly monotone in its second argument.

*Formal Contract:*
- *Preconditions:* v ∈ T, n₁ ≥ 1, n₂ > n₁, #v = m
- *Postconditions:* shift(v, n₁) < shift(v, n₂)


## T10a.1 — UniformSiblingLength

`(A n ≥ 0 : #tₙ = #t₀)` where `tₙ₊₁ = inc(tₙ, 0)` for `n ≥ 0`.

In words: all tumblers produced by a single allocator through repeated sibling increment have the same length as its base address. The `inc(·, 0)` operation is length-preserving, so no sibling is longer or shorter than any other.

*Formal Contract:*
- *Precondition:* Allocator with base address `t₀`, producing siblings by `inc(·, 0)`.
- *Postcondition:* `(A n ≥ 0 : #tₙ = #t₀)` — all siblings have the same length as the base address.


## T10a.2 — NonNestingSiblingPrefixes

For distinct siblings `tᵢ`, `tⱼ` with `i < j` from the same allocator: `tᵢ ⋠ tⱼ ∧ tⱼ ⋠ tᵢ`.

In words: siblings from the same allocator are prefix-incomparable — neither can be a prefix of the other. This holds because all siblings share the same length (T10a.1), and a proper prefix relationship would require unequal lengths.

*Formal Contract:*
- *Precondition:* `tᵢ`, `tⱼ` are distinct siblings from the same allocator (`i ≠ j`).
- *Postcondition:* `tᵢ ⋠ tⱼ ∧ tⱼ ⋠ tᵢ` — neither is a prefix of the other.


## T10a.3 — LengthSeparation

Let parent allocator have sibling length `γ`. A child spawned via `inc(t, k')` with `k' ∈ {1, 2}` from parent sibling `t` has all outputs of length `γ + k' > γ`. A descendant at depth `d` along a lineage with child-spawning parameters `k'₁, …, k'_d` (each `k'_i ∈ {1, 2}`) has output length exactly `γ + k'₁ + … + k'_d ≥ γ + d`.

In words: child allocator outputs are strictly longer than any parent sibling output, and this length gap accumulates additively across nesting levels. Because tumblers of different lengths are distinct (T3), outputs at different nesting depths along any lineage never collide.

*Formal Contract:*
- *Precondition:* Parent allocator with sibling length `γ`; `t` is a parent sibling (so `#t = γ` by T10a.1); child spawned via `inc(t, k')` with `k' ∈ {1, 2}` (per T10a).
- *Postcondition:* All child outputs have length `γ + k' > γ`. No child output equals any parent sibling (by T3, tumblers of different lengths are distinct). Descendant at depth `d` along a lineage with child-spawning parameters `k'₁, …, k'_d` (each `k'_i ∈ {1, 2}`) has output length exactly `γ + k'₁ + … + k'_d ≥ γ + d`; along any lineage the cumulative length is strictly increasing with depth, so outputs at different nesting depths never collide (by T3).


## T10a.4 — T4PreservationUnderDiscipline

Every output of a T10a-conforming allocator satisfies T4. The discipline permits two operations: sibling production via `inc(·, 0)` and child-spawning via `inc(·, k')` with `k' ∈ {1, 2}`. Both preserve T4 under the bounds enforced by T10a (via TA5a).

In words: the allocator discipline is closed under T4 — starting from a T4-compliant base address, every sibling and child address it produces also satisfies T4. The discipline's restriction on `k'` values is precisely calibrated to keep all outputs within the T4-valid region.

*Formal Contract:*
- *Preconditions:* Allocator conforming to T10a; parent address `t` satisfying T4.
- *Postconditions:* Every sibling and child output satisfies T4.

## T10a-N — AllocatorDisciplineNecessity

Relaxing the `k = 0` restriction for siblings permits prefix nesting, violating the precondition of T10.

If an allocator produces `t₁ = inc(t₀, 0)` followed by `t₂ = inc(t₁, 1)`, then `t₁ ≼ t₂` — the two addresses nest as prefixes.

In words: the `k = 0` sibling restriction is not merely a convention. Permitting a second allocation step at `k = 1` causes the first allocated address to become a proper prefix of the second, which invalidates T10's non-nesting precondition and collapses the partition independence guarantee.

*Formal Contract:*
- *Preconditions:* `t₀ ∈ T`; allocator produces `t₁ = inc(t₀, 0)` and `t₂ = inc(t₁, 1)` (the `k = 0` sibling restriction is relaxed for the second step).
- *Postconditions:* `t₁ ≼ t₂` — prefix nesting occurs among the produced addresses, violating T10's non-nesting precondition (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`).

---

## T4a — SyntacticEquivalence

Under the T4 positive-component constraint (`tᵢ > 0` for every non-separator component), the non-empty field constraint (each present field has `≥ 1` component) holds if and only if:

- (i) no two zeros are adjacent in `t`,
- (ii) `t₁ ≠ 0`,
- (iii) `t_{#t} ≠ 0`.

In words: whether all present fields are non-empty is fully determined by three simple syntactic checks on the raw sequence — it does not start with zero, does not end with zero, and contains no two consecutive zeros. No knowledge of field boundaries or structure is required to verify the constraint.

*Formal Contract:*
- *Preconditions:* `t` is an address tumbler satisfying T4's positive-component constraint (`tᵢ > 0` for every non-separator component).
- *Postconditions:* The non-empty field constraint (each present field has `≥ 1` component) holds if and only if (i) no two zeros are adjacent in `t`, (ii) `t₁ ≠ 0`, and (iii) `t_{#t} ≠ 0`.

---

## T4b — UniqueParse

Under the T4 constraints — at most three zero-valued components as field separators, every field component strictly positive, every present field non-empty — the function `fields(t)` that decomposes a tumbler into its node, user, document, and element sub-sequences is well-defined and uniquely determined by `t` alone.

In words: the positive-component constraint makes separator positions exactly recoverable by scanning for zeros, so there is only one valid parse of any conforming tumbler. Two distinct decompositions would require two distinct sets of separator positions, but the scan produces exactly one such set.

*Formal Contract:*
- *Preconditions:* `t` satisfies T3 (CanonicalRepresentation): the component sequence of `t` is fixed by sequence identity, with no alternative encoding yielding different component values. `t` satisfies the T4 constraints (at most three zero-valued components, positive-component constraint, non-empty field constraint).
- *Postconditions:* `fields(t)` — the decomposition into node, user, document, and element sub-sequences — is well-defined and uniquely determined by `t`.

---

## T4c — LevelDetermination

Define `zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`. Under the constraints of T4, `zeros(t) ∈ {0, 1, 2, 3}`, and the mapping from `{0, 1, 2, 3}` to the four hierarchical levels is a bijection:

- `zeros(t) = 0` → node address,
- `zeros(t) = 1` → user address,
- `zeros(t) = 2` → document address,
- `zeros(t) = 3` → element address.

In words: counting the zeros in a conforming tumbler uniquely and completely identifies its hierarchical level. The positive-component constraint is essential — without it, a zero could be either a separator or a field component, making the count ambiguous.

*Formal Contract:*
- *Preconditions:* `t` satisfies the T4 constraints.
- *Postconditions:* `zeros(t) ∈ {0, 1, 2, 3}`, and the mapping `zeros(t) → hierarchical level` is a bijection on `{0, 1, 2, 3}`.

---

## TA5-SIG — LastSignificantPosition

We define the *last significant position* of a tumbler `t ∈ T`, written `sig(t)`:

- When `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`: `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})`.
- When `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`: `sig(t) = #t`.

In both cases `1 ≤ sig(t) ≤ #t`.

In words: the last significant position is the index of the rightmost nonzero component, falling back to the tumbler's length when all components are zero. It is a well-defined value in `[1, #t]` for every tumbler.

*Formal Contract:*
- *Preconditions:* `t ∈ T` (any tumbler with `#t ≥ 1`).
- *Definition:* `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})` when `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`; `sig(t) = #t` when `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.
- *Postconditions:* `1 ≤ sig(t) ≤ #t`.

## TA5-SigValid — SigOnValidAddresses

For every valid address `t` satisfying T4, `sig(t) = #t`.

In words: the significant index of a valid address always equals its length. Because T4 guarantees every field component is strictly positive, the final component is nonzero, making it the rightmost nonzero position — so `sig` reaches exactly to the end of the tumbler.

*Formal Contract:*
- *Precondition:* `t` satisfies T4 (valid address tumbler: at most three zero-valued field separators, every field component strictly positive, every present field non-empty).
- *Guarantee:* `sig(t) = #t`.


## TA5a — IncrementPreservesT4

The operation `inc(t, k)` on a valid address `t` preserves T4 if and only if `k = 0`, or `k = 1` with `zeros(t) ≤ 3`, or `k = 2` with `zeros(t) ≤ 2`. For all `k ≥ 3`, T4 is violated regardless of `zeros(t)`.

In words: a sibling increment (`k = 0`) always produces a valid address. Descending one or two levels (`k = 1` or `k = 2`) is valid only when the address has remaining separator budget. Steps of `k ≥ 3` unconditionally fail because they introduce consecutive zero separators, creating an empty field — a structural violation regardless of how many separators remain.

*Formal Contract:*
- *Precondition:* `t` satisfies T4 (valid address tumbler), `k ≥ 0`.
- *Guarantee:* `inc(t, k)` satisfies T4 iff `k = 0`, or `k = 1 ∧ zeros(t) ≤ 3`, or `k = 2 ∧ zeros(t) ≤ 2`.
- *Failure:* For `k ≥ 3`, `inc(t, k)` violates T4 (adjacent zeros create an empty field).


## Span — ContiguousAddressRange

**Definition (Span).** A *span* is a pair `(s, ℓ)` where `s ∈ T` is a start address and `ℓ ∈ T` is a length — a positive tumbler used as a displacement — denoting the contiguous range from `s` up to but not including `s ⊕ ℓ`. The set of tumblers in the span is `{t ∈ T : s ≤ t < s ⊕ ℓ}`.

In words: a span identifies a contiguous block of addresses by a start point and a displacement length. It contains every tumbler from `s` up to but not including the address reached by adding `ℓ` — a half-open interval in tumbler order.

*Formal Contract:*
- *Definition:* `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}`, where `s ∈ T` is the start address and `ℓ ∈ T` with `ℓ > 0` is the displacement length.
