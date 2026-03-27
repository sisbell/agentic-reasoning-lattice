# ASN-0034 Formal Statements

*Source: ASN-0034-tumbler-algebra.md (revised 2026-03-26) — Extracted: 2026-03-27*

## T0 — Carrier-set definition

`T = {d₁.d₂. ... .dₙ : each dᵢ ∈ ℕ, n ≥ 1}`. This is an axiom: we posit the carrier set by definition, not by derivation. The natural numbers ℕ are taken with their standard properties, including closure under successor and addition.

T is the set of all finite, non-empty sequences of natural numbers. This is a foundational axiom from which all tumbler properties are derived.

*Formal Contract:*
- *Axiom:* T is the set of all finite sequences over ℕ with length ≥ 1; ℕ is closed under successor and addition.


## T0(a) — Every component value of a tumbler is unbounded

`(A t ∈ T, i : 1 ≤ i ≤ #t : (A M ∈ ℕ :: (E t' ∈ T :: t' agrees with t except t'.dᵢ > M)))`.

In words: for every tumbler and every component position, there exists a tumbler whose value at that position exceeds any given bound. The address space within any subtree is inexhaustible.

*Formal Contract:*
- *Preconditions:* `t ∈ T`, `1 ≤ i ≤ #t`, `M ∈ ℕ`.
- *Postconditions:* There exists `t' ∈ T` such that `t'.dⱼ = t.dⱼ` for all `j ≠ i` and `t'.dᵢ > M`.
- *Frame:* `#t' = #t`; all components at positions `j ≠ i` are identical to those of `t`.
- *Axiom:* T is the set of all finite sequences over ℕ with length ≥ 1; ℕ is closed under successor.


## T0(b) — Tumblers of arbitrary length exist in T

`(A n ∈ ℕ : n ≥ 1 : (E t ∈ T :: #t ≥ n))`.

In words: there is no maximum tumbler length — for every bound, a tumbler of at least that length exists in T. The hierarchy has unlimited nesting depth. T0(a) ensures siblings within a level are inexhaustible; T0(b) ensures nesting levels are inexhaustible.

*Formal Contract:*
- *Preconditions:* `n ∈ ℕ`, `n ≥ 1`.
- *Postconditions:* There exists `t ∈ T` such that `#t ≥ n`.
- *Axiom:* T is the set of all finite sequences over ℕ with length ≥ 1; there is no upper bound on the length of a finite sequence.


## T1 — Tumblers are totally ordered by lexicographic comparison, with the prefix-less-than convention

For tumblers `a = a₁. ... .aₘ` and `b = b₁. ... .bₙ`, define `a < b` iff there exists `k ≥ 1` such that `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either:

  (i) `k ≤ min(m, n)` and `aₖ < bₖ`, or

  (ii) `k = m + 1 ≤ n` (that is, `a` is a proper prefix of `b`).

In words: `<` on T is a strict total order — component-wise lexicographic, with any proper prefix less than all of its extensions. For any two tumblers, exactly one of `a < b`, `a = b`, `b < a` holds.

*Dependencies:*
- **T0(a) (Carrier-set definition):** T is the set of all finite sequences over ℕ with length ≥ 1.
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`.

*Formal Contract:*
- *Definition:* `a < b` iff `∃ k ≥ 1` with `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either (i) `k ≤ min(m,n) ∧ aₖ < bₖ`, or (ii) `k = m+1 ≤ n`.
- *Postconditions:* (a) Irreflexivity — `(A a ∈ T :: ¬(a < a))`. (b) Trichotomy — `(A a,b ∈ T :: exactly one of a < b, a = b, b < a)`. (c) Transitivity — `(A a,b,c ∈ T : a < b ∧ b < c : a < c)`.

## T2 — Tumbler comparison is computable from the two tumblers alone, without consulting any external data structure

The order relation T1 is computable from the two tumblers alone, without consulting any external data structure. The comparison examines at most `min(#a, #b)` component pairs.

Tumbler comparison is a pure function of its two arguments. No external index, allocator state, or global registry participates in the decision. The procedure scans component pairs left-to-right and terminates after at most `min(#a, #b)` examinations.

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` — two well-formed tumblers (finite sequences over ℕ with `#a ≥ 1` and `#b ≥ 1`, per T0).
- *Postconditions:* (a) The ordering among `a` and `b` under T1 is determined. (b) At most `min(#a, #b)` component pairs are examined. (c) The only values consulted are `{aᵢ : 1 ≤ i ≤ #a}`, `{bᵢ : 1 ≤ i ≤ #b}`, `#a`, and `#b`.
- *Frame:* No external data structure is read or modified — the comparison is a pure function of the two tumblers.

---

## T3 — Each tumbler has exactly one canonical representation; component-wise identity is equality

`(A a, b ∈ T : a₁ = b₁ ∧ ... ∧ aₙ = bₙ ∧ #a = #b ≡ a = b)`

If two tumblers have the same length and the same components at every position, they are the same tumbler. Conversely, if they differ in any component or in length, they are distinct. No normalization, no trailing-zero ambiguity, no exponent variation can create aliases.

Tumbler equality is sequence equality. There is no quotienting, normalization map, or equivalence relation on T beyond component-wise identity. Trailing zeros are significant: `[1, 2] ≠ [1, 2, 0]`.

*Formal Contract:*
- *Postconditions:* Tumbler equality is sequence equality: `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`.
- *Frame:* No quotient, normalization, or external identification is imposed on T. Trailing zeros are significant: `[1, 2] ≠ [1, 2, 0]`.

---

## T4 — An address tumbler has at most three zero-valued components as field separators; the positive-component constraint ensures unique hierarchical parsing

Every tumbler `t ∈ T` used as an address contains at most three zero-valued components, appearing in order as field separators, every non-separator component is strictly positive, and every field present in the address has at least one component. Formally, if `t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`, then `(A i : 1 ≤ i ≤ α : Nᵢ > 0)`, `(A j : 1 ≤ j ≤ β : Uⱼ > 0)`, `(A k : 1 ≤ k ≤ γ : Dₖ > 0)`, `(A l : 1 ≤ l ≤ δ : Eₗ > 0)`, and `α ≥ 1`, `β ≥ 1` when present, `γ ≥ 1` when present, `δ ≥ 1` when present.

The non-empty field constraint — each present field has at least one component — is equivalent to three syntactic conditions on the raw tumbler: no two zeros are adjacent, the tumbler does not begin with zero, and the tumbler does not end with zero.

Define `zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`. The count of zero-valued components uniquely determines the hierarchical level:

- `zeros(t) = 0`: `t` is a node address (node field only),
- `zeros(t) = 1`: `t` is a user address (node and user fields),
- `zeros(t) = 2`: `t` is a document address (node, user, and document fields),
- `zeros(t) = 3`: `t` is an element address (all four fields).

Address tumblers are partitioned into at most four fields by zero-valued separators. The constraint that no field component is zero and no field is empty guarantees that the parse into node, user, document, and element fields is unambiguous and unique, and that the number of separators determines the hierarchical level bijectively.

*Formal Contract:*
- *Axiom:* Valid address tumblers satisfy `zeros(t) ≤ 3`, `(A i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0 : tᵢ > 0)`, no adjacent zeros, `t₁ ≠ 0`, `t_{#t} ≠ 0`.
- *Definition:* `zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`; `fields(t)` decomposes `t` into node, user, document, and element fields by partitioning at the zero-valued separator positions.
- *Postconditions:* (a) The non-empty field constraint is equivalent to three syntactic conditions: no adjacent zeros, `t₁ ≠ 0`, `t_{#t} ≠ 0`. (b) `fields(t)` is well-defined and uniquely determined by `t` alone. (c) `zeros(t)` determines the hierarchical level bijectively on `{0, 1, 2, 3}`.

---

## T5 — The set of tumblers sharing a prefix forms a contiguous interval under T1

For any tumbler prefix `p`, the set `{t ∈ T : p ≼ t}` (where `≼` denotes "is a prefix of") forms a contiguous interval under T1:

`[p ≼ a ∧ p ≼ c ∧ a ≤ b ≤ c ⟹ p ≼ b]`

The set of all tumblers sharing a common prefix is contiguous under the total order T1. No tumbler from outside a subtree can interleave between two members of that subtree. Every subtree of the tumbler hierarchy maps to a contiguous range on the address line, so a span between any two same-prefix endpoints captures exactly the addresses under that prefix between those endpoints.

*Formal Contract:*
- *Definition:* `p ≼ t ⟺ #t ≥ #p ∧ (A i : 1 ≤ i ≤ #p : tᵢ = pᵢ)` — the tumbler `t` extends the prefix `p`.
- *Preconditions:* `a, b, c ∈ T`; `p` is a tumbler prefix with `#p ≥ 1`; `p ≼ a`; `p ≼ c`; `a ≤ b ≤ c` under the lexicographic order T1.
- *Postconditions:* `p ≼ b` — the tumbler `b` extends the prefix `p`, and therefore belongs to the same subtree as `a` and `c`.

---

## T6 — Containment (same node, same account, same document family, structural subordination) is decidable from the addresses alone

For any two tumblers `a, b ∈ T`, the following are decidable from the addresses alone:

(a) Whether `a` and `b` share the same node field.

(b) Whether `a` and `b` share the same node and user fields.

(c) Whether `a` and `b` share the same node, user, and document-lineage fields.

(d) Whether the document field of `a` is a prefix of the document field of `b` (structural subordination within a document family).

Each hierarchical containment query — shared server, shared account, shared document family, or document-field prefix — can be answered by a finite scan of the two tumblers with no external data. Write `N(t)`, `U(t)`, `D(t)`, `E(t)` for the fields extracted by `fields(t)` (T4). Each query extracts the relevant fields and performs componentwise comparison; queries (b)–(d) return *no* if a required field is absent from either tumbler.

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` are valid tumblers satisfying T4 (positive-component constraint, at most three zeros, no adjacent zeros, no leading or trailing zero).
- *Definition:* `N(t)`, `U(t)`, `D(t)`, `E(t)` are the node, user, document, and element fields of `t`, extracted by `fields(t)` (T4(b)). Componentwise comparison of two finite sequences `S, R` checks `#S = #R ∧ (A i : 1 ≤ i ≤ #S : Sᵢ = Rᵢ)`. Prefix comparison of `S` against `R` checks `#S ≤ #R ∧ (A i : 1 ≤ i ≤ #S : Sᵢ = Rᵢ)`.
- *Postconditions:* (a) Same-node-field query terminates and returns a boolean, requiring at most `#N(a) + 1` comparisons. (b) Same-node-and-user query terminates and returns a boolean; returns *no* if either tumbler lacks a user field. (c) Same-node-user-document query terminates and returns a boolean; returns *no* if either tumbler lacks a document field. (d) Document-field prefix query terminates and returns a boolean in at most `γₐ + 1` steps; returns *no* if either tumbler lacks a document field. All decisions use only the tumbler representations of `a` and `b`.

## T7 — Subspaces (text, links) within a document's element field are permanently dis...

The subspace identifier (the first component of the element field) permanently separates the address space into disjoint regions. No tumbler in subspace `s₁` can equal or be confused with a tumbler in subspace `s₂ ≠ s₁`.

`(A a, b ∈ T : a.E₁ ≠ b.E₁ ⟹ a ≠ b)`

*Dependencies:*
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. Contrapositively: tumblers that differ in length or at any component are distinct. Used in every case to conclude `a ≠ b`.
- **T4 (Hierarchical parsing):** (b) `fields(t)` is well-defined and uniquely determined by `t` alone. (c) `zeros(t) = 3` iff `t` is an element-level address. The positive-component constraint: every non-separator component is strictly positive, so every zero in `t` is unambiguously a field separator. Used to locate `E₁` and to distinguish separators from field components.

In words: two element-level tumblers with different subspace identifiers are always distinct addresses. This guarantees that arithmetic within one content subspace (e.g., text, subspace 1) cannot produce an address in another subspace (e.g., links, subspace 2), because the subspace identifier is encoded directly in the tumbler, not held as external metadata.

*Preconditions:* `a, b ∈ T` with `zeros(a) = zeros(b) = 3` (both are element-level addresses with well-formed field structure per T4).
*Postconditions:* `a.E₁ ≠ b.E₁ ⟹ a ≠ b`.

---

## T8 — Once allocated, an address is never removed from the address space; the set o...

If tumbler `a ∈ T` has been allocated at any point in the system's history, then for all subsequent states, `a` remains in the set of allocated addresses. No operation removes an allocated address from the address space. The set of allocated addresses is monotonically non-decreasing.

*Dependencies:*
- **T10a (Allocation mechanism):** Each allocator advances its frontier by `inc(·, 0)`, producing an address strictly greater than the previous, and inserts it into the allocated set. This is the sole mechanism by which the allocated set grows.
- **TA5 (Hierarchical increment):** (a) `inc(t, 0)` produces `t' > t` under T1. Used to establish that each newly allocated address is fresh.
- **TumblerAdd (Constructive definition of ⊕), TumblerSub (Constructive definition of ⊖):** Pure functions on component sequences: each accepts tumbler arguments, computes a new component sequence, and returns a tumbler value. Neither operation consults or modifies the allocated set.
- **T1 (Lexicographic order), T2 (Decidable comparison), T4 (Hierarchical parsing):** Read-only operations that inspect tumbler values without modifying any system state.

In words: once an address enters the allocated set, it stays there permanently — no operation can remove or reclaim it. The allocated set grows monotonically across all state transitions. This holds even for addresses whose positions hold no stored content; such addresses permanently occupy their positions on the tumbler line.

*Invariant:* For every state transition `s → s'`, `allocated(s) ⊆ allocated(s')`.
*Axiom:* The system defines no operation that removes an element from the allocated set. This is a design constraint, not a derived property.
*Frame:* Read-only operations (T1, T2, T4) and pure arithmetic (⊕, ⊖, inc) preserve the allocated set exactly: `allocated(s') = allocated(s)`.

---

## T9 — Within a single allocator's sequential stream, new addresses are strictly mon...

T10a defines the allocation mechanism: each allocator advances by `inc(·, 0)`, incrementing by exactly 1 at the last significant position. Since `inc` produces a strictly greater tumbler at each step (TA5(a)), within each allocator's sequential stream, new addresses are strictly monotonically increasing:

`(A a, b : same_allocator(a, b) ∧ allocated_before(a, b) : a < b)`

*Dependencies:*
- **T10a (Allocator discipline):** Each allocator produces its sibling outputs exclusively by repeated application of `inc(·, 0)`. This is the mechanism under proof: the sequence `t₀, t₁, t₂, ...` with `tₙ₊₁ = inc(tₙ, 0)` is the allocator's entire sibling stream.
- **TA5 (Hierarchical increment):** (a) `inc(t, 0)` produces `t' > t` under T1. Supplies the strict increase at each step.
- **T1 (Lexicographic order):** (c) Transitivity: `a < b ∧ b < c ⟹ a < c`. Chains consecutive strict increases across multiple steps.

In words: within a single allocator's output stream, each new address is strictly greater than all previously allocated addresses from that allocator. T9 is scoped per-allocator — the global tumbler line does not grow monotonically by creation time, since child addresses are inserted between parent and next-sibling regardless of when they were created.

*Preconditions:* `a, b ∈ T` with `same_allocator(a, b) ∧ allocated_before(a, b)` — both addresses produced by the same allocator's sibling stream, `a` allocated before `b`.
*Postconditions:* `a < b` under the tumbler order T1.

---

## T10 — Allocators with non-nesting prefixes produce distinct addresses without coord...

The address space is partitioned by prefix into ownership domains. Two allocators with distinct, non-nesting prefixes can allocate simultaneously, and the resulting addresses are guaranteed distinct.

Formally: let `p₁` and `p₂` be prefixes such that neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for any tumbler `a` with prefix `p₁` and any tumbler `b` with prefix `p₂`, `a ≠ b`.

*Dependencies:*
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. Used contrapositively: tumblers that differ at any component are distinct.
- **Prefix relation (from T1):** `p ≼ a` means `#p ≤ #a` and `aᵢ = pᵢ` for all `1 ≤ i ≤ #p`. Negation `p ⋠ a` means it is not the case that `p ≼ a`.

In words: two allocators whose ownership prefixes neither contains the other can allocate concurrently without any coordination, and their outputs are guaranteed never to collide. Uniqueness is enforced by the address structure itself — no central registry or locking protocol is required.

*Preconditions:* `p₁, p₂ ∈ T` with `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`; `a, b ∈ T` with `p₁ ≼ a` and `p₂ ≼ b`.
*Postconditions:* `a ≠ b`.

---

## T10a — Each allocator uses inc(·, 0) for siblings and inc(·, k>0) only for child-spa...

Each allocator produces its sibling outputs exclusively by repeated application of `inc(·, 0)` — shallow increment at the last significant position. To spawn a child allocator, the parent performs one `inc(·, k')` with `k' > 0` to establish the child's prefix, then delegates further allocation to the child. The parent's own sibling stream resumes with `inc(·, 0)`.

*Dependencies:*
- **TA5 (Hierarchical increment):** (a) `inc(t, k)` produces `t' > t` under T1. (b) `t'` agrees with `t` on all components before the increment point. (c) When `k = 0`: `#t' = #t`, and `t'` differs from `t` only at `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`. (d) When `k > 0`: `#t' = #t + k`, with `k - 1` zero field separators and final component `1`.
- **T1 (Lexicographic order):** `a < b` iff there exists `k ≥ 1` with `aᵢ = bᵢ` for all `i < k`, and either (i) `k ≤ min(#a, #b)` and `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b` (proper prefix). Irreflexivity: `¬(a < a)`.
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. Contrapositively: tumblers of different lengths are distinct.
- **T10 (Partition independence):** For non-nesting prefixes `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`, any tumbler extending `p₁` is distinct from any tumbler extending `p₂`.
- **Prefix relation (from T1):** `p ≼ a` means `#p ≤ #a` and `aᵢ = pᵢ` for all `1 ≤ i ≤ #p`. A proper prefix `p ≺ a` requires `p ≼ a` with `p ≠ a`, entailing `#p < #a`.

In words: restricting siblings to `inc(·, 0)` ensures all siblings share the same length and have non-nesting prefixes, which is the precondition T10 requires for partition independence. Allowing a deeper increment for a sibling (instead of a child) would cause the sibling to nest under a prior sibling, collapsing the uniqueness guarantee. This axiom is both sufficient and necessary for the three consequences it guarantees.

*Axiom:* Allocators produce sibling outputs exclusively by `inc(·, 0)`; child-spawning uses exactly one `inc(·, k')` with `k' > 0`.
*Postconditions:* (a) Uniform sibling length — `(A tᵢ, tⱼ : same_allocator(tᵢ, tⱼ) ∧ sibling(tᵢ) ∧ sibling(tⱼ) : #tᵢ = #tⱼ)`. (b) Non-nesting sibling prefixes — `(A tᵢ, tⱼ : same_allocator(tᵢ, tⱼ) ∧ sibling(tᵢ) ∧ sibling(tⱼ) ∧ tᵢ ≠ tⱼ : tᵢ ⋠ tⱼ ∧ tⱼ ⋠ tᵢ)`. (c) Length separation — child outputs have length strictly greater than parent sibling outputs: `(A t_parent, t_child : sibling(t_parent) ∧ spawned_by(t_child, t_parent) : #t_child > #t_parent)`.

## PrefixOrderingExtension — PrefixOrderingExtension

Let `p₁, p₂ ∈ T` with `p₁ < p₂` and `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`. Then `(A a, b ∈ T : p₁ ≼ a ∧ p₂ ≼ b : a < b)`.

The strict ordering between two non-nested tumblers propagates to all their descendants. If `p₁` precedes `p₂` in the lexicographic order and neither is a prefix of the other, then every tumbler rooted at `p₁` is strictly less than every tumbler rooted at `p₂`.

*Preconditions:* `p₁, p₂ ∈ T` with `p₁ < p₂` (T1) and `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` (non-nesting); `a, b ∈ T` with `p₁ ≼ a` and `p₂ ≼ b`.
*Postconditions:* `a < b` under T1.


## PartitionMonotonicity — AllocatorSubpartitionOrdering

Within any prefix-delimited partition with prefix `p`, sub-partition prefixes `t₀, t₁, ...` produced by repeated `inc(·, 0)` from an initial child base `t₀ = inc(s, k)` with `k > 0` and `p ≼ s` are pairwise non-nesting and strictly increasing under T1. For sibling sub-partition prefixes `tᵢ < tⱼ` (`i < j`) and any `a, b ∈ T` with `tᵢ ≼ a` and `tⱼ ≼ b`: `a < b`. Within each sub-partition with prefix `tᵢ`: `allocated_before(a, b) ⟹ a < b`.

The set of allocated addresses within any prefix-delimited partition is totally ordered by T1 with two consistency guarantees: addresses in an earlier sub-partition always precede addresses in a later sub-partition (cross-allocator ordering follows prefix structure), and within each sub-partition, allocation order coincides with address order (intra-allocator ordering follows T9).

*Preconditions:* A system conforming to T10a (allocator discipline); a partition with prefix `p ∈ T`; sub-partition prefixes `t₀, t₁, ...` produced by `inc(·, 0)` from an initial child prefix `t₀ = inc(s, k)` with `k > 0` and `p ≼ s`.
*Postconditions:* (1) For sibling sub-partition prefixes `tᵢ < tⱼ` (with `i < j`) and any `a, b ∈ T` with `tᵢ ≼ a` and `tⱼ ≼ b`: `a < b`. (2) Within each sub-partition with prefix `tᵢ`: `allocated_before(a, b) ⟹ a < b`.
*Invariant:* For every reachable system state, the set of allocated addresses within any prefix-delimited partition is totally ordered by T1 consistently with per-allocator allocation order.


## GlobalUniqueness — GlobalUniqueness

For any `a, b ∈ T` produced by distinct allocation events within a system conforming to T10a: `a ≠ b`.

The tumbler addressing scheme guarantees global uniqueness without distributed consensus. Structural properties of the names alone — lexicographic order, hierarchical increment, and allocator discipline — ensure that every allocation event produces an address distinct from every other, regardless of when or where in the hierarchy the allocation occurs.

*Preconditions:* `a, b ∈ T` produced by distinct allocation events within a system conforming to T10a (allocator discipline).
*Invariant:* For every pair of addresses `a, b` produced by distinct allocation events in any reachable system state: `a ≠ b`.


### Tumbler arithmetic

We now turn to the arithmetic operations. The system requires operations that advance a position by a displacement (for computing span endpoints and shifting positions) and that recover the displacement between two positions (for computing span widths). These operations — tumbler addition and subtraction — are not arithmetic on numbers but position-advance operations in a hierarchical address space.

A displacement `w` is a tumbler whose leading zeros say "stay at these hierarchical levels" and whose first nonzero component says "advance here." Components after the advance point describe the structure of the landing position within the target region.

### Addition for position advancement

Let `⊕` denote tumbler addition: given a start position `a` and a displacement `w`, compute the advanced position.

We require a notion of where a displacement "acts." For a positive displacement `w = [w₁, w₂, ..., wₙ]`, define the *action point* as `k = min({i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0})` — the position of the first nonzero component. The leading zeros say "stay at these hierarchical levels"; the first nonzero component says "advance here."


## T12 — SpanWellFormedness

A span `(s, ℓ)` is well-formed when `ℓ > 0` and `actionPoint(ℓ) ≤ #s` (equivalently, the number of leading zeros in `ℓ` is strictly less than `#s`). The well-formed span denotes `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}`, which satisfies:

(a) `s ⊕ ℓ ∈ T` — the endpoint exists in `T`, by TA0.
(b) `s ∈ span(s, ℓ)` — the span is non-empty; `s` is its minimum element, by TA-strict.
(c) `span(s, ℓ)` is order-convex under T1: for any `a, c ∈ span(s, ℓ)` and `b ∈ T`, `a ≤ b ≤ c` implies `b ∈ span(s, ℓ)`.

A well-formed span denotes a non-empty, contiguous set of tumblers from `s` up to but not including `s ⊕ ℓ`. The constraint that `ℓ`'s leading-zero count is less than `#s` ensures the displacement acts within the existing hierarchical depth of `s`, making the endpoint computable and the interval well-defined.

*Preconditions:* `s ∈ T`, `ℓ ∈ T`, `ℓ > 0`, `actionPoint(ℓ) ≤ #s`
*Definition:* `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}`
*Postconditions:* (a) `s ⊕ ℓ ∈ T` (endpoint exists, by TA0). (b) `s ∈ span(s, ℓ)` (non-empty, by TA-strict). (c) `span(s, ℓ)` is order-convex under T1 (for all `a, c ∈ span(s, ℓ)` and `b ∈ T`, `a ≤ b ≤ c` implies `b ∈ span(s, ℓ)`).


## TA0 — TumblerAdditionWellDefined

For `a, w ∈ T` with `w > 0` and `actionPoint(w) ≤ #a`, the constructive rule (TumblerAdd) builds `a ⊕ w = [r₁, ..., rₙ]` where `n = #w` and `k = actionPoint(w)`:

- `rᵢ = aᵢ` for `1 ≤ i < k`
- `rₖ = aₖ + wₖ`
- `rᵢ = wᵢ` for `k < i ≤ n`

The result satisfies `a ⊕ w ∈ T` and `#(a ⊕ w) = #w`.

Tumbler addition is well-defined whenever the displacement's action point falls at or within the length of the base address — i.e., the leading zeros in `w` do not outnumber the components of `a`. The result is always a valid tumbler, and its length equals the length of the displacement, not the base.

*Preconditions:* `a ∈ T`, `w ∈ T`, `w > 0`, `actionPoint(w) ≤ #a`
*Postconditions:* `a ⊕ w ∈ T`, `#(a ⊕ w) = #w`

## TA1 — Addition preserves the total order (weak)

`(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) : a ⊕ w ≤ b ⊕ w)`, where `k` is the action point of `w`.

In words: if two tumbler positions are ordered before advancement by the same displacement, they remain non-reversed after. Weak (`≤`) order preservation holds whenever both additions are well-defined — that is, the action point falls within both operands. The positions may collapse to equality but cannot exchange order.

*Preconditions:* `a ∈ T`, `b ∈ T`, `w ∈ T`, `a < b`, `w > 0`, `actionPoint(w) ≤ min(#a, #b)`
*Postconditions:* `a ⊕ w ≤ b ⊕ w`

---

## Divergence — Divergence point of two unequal tumblers (DEFINITION, function)

For tumblers `a, b ∈ T` with `a ≠ b`, `divergence(a, b) = k`, where exactly one of:
- (i) `∃ i` with `1 ≤ i ≤ min(#a, #b)` and `aᵢ ≠ bᵢ`: then `k = min({i : 1 ≤ i ≤ min(#a, #b) ∧ aᵢ ≠ bᵢ})` — component divergence at a shared position.
- (ii) `(A i : 1 ≤ i ≤ min(#a, #b) : aᵢ = bᵢ)` and `#a ≠ #b`: then `k = min(#a, #b) + 1` — prefix divergence, one past the shorter tumbler's last component.

In words: `divergence(a, b)` identifies the first position where two distinct tumblers differ. In case (i) both tumblers have that position; in case (ii) one is a proper prefix of the other and the divergence falls just beyond the shorter one's end. For prefix-related pairs, `divergence(a, b) > min(#a, #b)`, which makes the TA1-strict precondition `actionPoint(w) ≥ divergence(a, b)` unsatisfiable — confirming that addition of a prefix-related pair collapses to equality rather than preserving strict order.

*Preconditions:* `a ∈ T`, `b ∈ T`, `a ≠ b`
*Definition:* `divergence(a, b) = k`, where (i) if `∃ i` with `1 ≤ i ≤ min(#a, #b)` and `aᵢ ≠ bᵢ`, then `k = min({i : 1 ≤ i ≤ min(#a, #b) ∧ aᵢ ≠ bᵢ})`; (ii) if `(A i : 1 ≤ i ≤ min(#a, #b) : aᵢ = bᵢ)` and `#a ≠ #b`, then `k = min(#a, #b) + 1`

---

## TA1-strict — Addition preserves the total order (strict) when k ≤ min(#a, #b) ∧ k ≥ diverg...

`(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) ∧ k ≥ divergence(a, b) : a ⊕ w < b ⊕ w)`, where `k` is the action point of `w`.

In words: strict order is preserved under addition when the displacement's action point falls at or beyond the first position where the two operands disagree. When the action point falls strictly before the divergence, both operands agree at the action point, receive the same increment, and copy the same tail — erasing the original difference and collapsing to equality. The condition `k ≥ divergence(a, b)` is precisely what prevents that erasure.

*Preconditions:* `a ∈ T`, `b ∈ T`, `w ∈ T`, `a < b`, `w > 0`, `actionPoint(w) ≤ min(#a, #b)`, `actionPoint(w) ≥ divergence(a, b)`
*Postconditions:* `a ⊕ w < b ⊕ w`

---

## TA-strict — Adding a positive displacement strictly advances

`(A a ∈ T, w > 0 : a ⊕ w > a)` (where `a ⊕ w` is well-defined, i.e., `k ≤ #a` per TA0).

In words: advancing a tumbler position by any positive displacement always moves it strictly forward in the lexicographic order. Without this, the axioms admit a degenerate model where addition is a no-op and every span interval `[s, s ⊕ ℓ)` collapses to empty. TA-strict rules out that model and is a direct prerequisite for span well-definedness (T12).

*Preconditions:* `a ∈ T`, `w ∈ T`, `w > 0`, `k ≤ #a` where `k` is the action point of `w`
*Postconditions:* `a ⊕ w > a`

---

## TA2 — Tumbler subtraction a ⊖ w is well-defined when a ≥ w

For tumblers `a, w ∈ T` with `a ≥ w`, `a ⊖ w` is a well-defined member of `T` with `#(a ⊖ w) = max(#a, #w)`.

In words: tumbler subtraction is total on the domain `{(a, w) : a ≥ w}` — whenever the minuend is at least as large as the subtrahend, the result is always a valid tumbler. The result length equals the longer of the two operands, not the minuend alone, because the subtraction construction zero-pads both operands to the maximum length before computing the difference.

*Preconditions:* `a ∈ T`, `w ∈ T`, `a ≥ w`
*Postconditions:* `a ⊖ w ∈ T`, `#(a ⊖ w) = max(#a, #w)`

## TA3 — Subtraction preserves the total order (weak)

`(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w ≤ b ⊖ w)`

In words: subtracting a common lower bound from two ordered tumblers preserves their ordering. If `a` precedes `b` and both dominate `w`, then `a ⊖ w` is at most `b ⊖ w`.

*Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w
*Postconditions:* a ⊖ w ≤ b ⊖ w


## TA3-strict — Subtraction preserves the total order (strict) when additionally #a = #b

`(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b : a ⊖ w < b ⊖ w)`

In words: when two tumblers have equal length, subtracting a common lower bound preserves their strict ordering. The equal-length condition rules out the proper-prefix case and guarantees strict (not just weak) inequality in the result.

*Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w, #a = #b
*Postconditions:* a ⊖ w < b ⊖ w

### Partial inverse


## TA4 — Addition and subtraction are partial inverses

`(A a, w : w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊕ w) ⊖ w = a)`, where `k` is the action point of `w`.

In words: adding a displacement then subtracting it recovers the original tumbler, provided the displacement's action point coincides with the tumbler's length, the displacement has no trailing components beyond that point, and all prefix components of the tumbler are zero. These three conditions are necessary — the inverse relationship does not hold in general.

*Preconditions:* `a ∈ T`, `w ∈ T`, `w > 0`, `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`, where `k` is the action point of `w`
*Postconditions:* `(a ⊕ w) ⊖ w = a`


## ReverseInverse — SubtractAddInverse

`(A a, w : a ≥ w ∧ w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊖ w) ⊕ w = a)`, where `k` is the action point of `w`.

In words: subtracting a displacement then adding it back recovers the original tumbler, under the same conditions as TA4. Together with TA4, this establishes that `⊕` and `⊖` are mutual inverses within the constrained domain where both precondition sets hold.

*Preconditions:* `a ∈ T`, `w ∈ T`, `a ≥ w`, `w > 0`, `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`, where `k` is the action point of `w`
*Postconditions:* `(a ⊖ w) ⊕ w = a`


### Constructive definition of ⊕ and ⊖


## TumblerAdd — PositionAdvanceDefinition

Let `a = [a₁, ..., aₘ]` and `w = [w₁, ..., wₙ]` with `w > 0`. With action point `k`:

```
         ⎧ aᵢ           if i < k        (copy from start)
rᵢ   =  ⎨ aₖ + wₖ      if i = k        (single-component advance)
         ⎩ wᵢ           if i > k        (copy from displacement)
```

Result length: `#(a ⊕ w) = #w`.

In words: tumbler addition is a position-advance operation. Given start position `a` and displacement `w`, the result copies `a`'s prefix up to the action point, advances a single component at the action point, and replaces `a`'s trailing structure with `w`'s trailing components. The result length is determined entirely by the displacement, not the start position.

*Preconditions:* `a ∈ T`, `w ∈ T`, `w > 0`, `actionPoint(w) ≤ #a`
*Definition:* `(a ⊕ w)ᵢ = aᵢ` for `i < k`, `(a ⊕ w)ₖ = aₖ + wₖ`, `(a ⊕ w)ᵢ = wᵢ` for `i > k`, where `k = actionPoint(w)`
*Postconditions:* `#(a ⊕ w) = #w`

## TumblerSub — StartRecovery (DEFINITION, function)

Given an end position `a` and a displacement `w`, recover the start position. When the operands have different lengths, zero-pad the shorter to the length of the longer before scanning for divergence. When the zero-padded sequences agree at every position, `a ⊖ w = [0, ..., 0]` of length `max(#a, #w)`. Otherwise, let `k` be the first position where `a` and `w` differ (treating missing components as zero):

```
         ⎧ 0             if i < k        (these levels matched — zero them)
rᵢ   =  ⎨ aₖ - wₖ      if i = k        (reverse the advance)
         ⎩ aᵢ           if i > k        (copy from end position)
```

The result has length `max(#a, #w)`.

**Precondition:** `a ≥ w` — when `a ≠ w`, at the divergence point (after zero-padding) `aₖ ≥ wₖ`.

In words: TumblerSub is the inverse of TumblerAdd — given an end position and the displacement that produced it, it recovers the starting position. Positions before the first divergence are zeroed, the advance is reversed at the divergence point, and subsequent positions copy directly from the end position.

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `a ≥ w`
- *Definition:* Zero-pad both operands to length `max(#a, #w)`. If the padded sequences agree at every position, `a ⊖ w = [0, ..., 0]` of length `max(#a, #w)`. Otherwise, let `k` be the first divergence position: `(a ⊖ w)ᵢ = 0` for `i < k`, `(a ⊖ w)ₖ = aₖ - wₖ`, `(a ⊖ w)ᵢ = aᵢ` for `i > k`, with `#(a ⊖ w) = max(#a, #w)`.


### Verification of TA1 and TA1-strict

**Claim (TA1, weak form):** If `a < b`, `w > 0`, and `k ≤ min(#a, #b)`, then `a ⊕ w ≤ b ⊕ w`.

**Claim (TA1-strict):** If additionally `k ≥ divergence(a, b)`, then `a ⊕ w < b ⊕ w`.

In words: Adding the same displacement to two ordered tumblers preserves their order. Strict order is preserved when the displacement's action point meets or exceeds the tumblers' first divergence position; if the action point falls earlier, tail-replacement can erase the original gap, collapsing strict order to equality.


### Verification of TA3

**Claim (TA3, weak form):** If `a < b`, `a ≥ w`, and `b ≥ w`, then `a ⊖ w ≤ b ⊖ w`.

**Claim (TA3-strict):** If `a < b`, `a ≥ w`, `b ≥ w`, and `#a = #b`, then `a ⊖ w < b ⊖ w`.

In words: Subtracting the same displacement from two ordered tumblers preserves their order, provided both are at least as large as the displacement. Equal-length tumblers preserve strict order; tumblers of unequal length may collapse strict order to equality via the prefix convention.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w
- *Postconditions:* a ⊖ w ≤ b ⊖ w

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w, #a = #b
- *Postconditions:* a ⊖ w < b ⊖ w


### Verification of TA4

**Claim:** `(a ⊕ w) ⊖ w = a` under: `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`.

In words: Addition then subtraction of the same displacement is the identity, when the displacement's action point equals the tumbler's length and the tumbler has zeros at all positions before the action point. This round-trip fidelity property justifies using ⊕ and ⊖ as a matched pair for advancing and recovering positions.

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `w > 0`, `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`, where `k` is the action point of `w`
- *Postconditions:* `(a ⊕ w) ⊖ w = a`


### Cancellation properties of ⊕

TumblerAdd's constructive definition determines each component of the result from exactly one input. This makes the operation left-cancellative.

In words: Because each output component of `a ⊕ w` derives from a unique source — prefix from `a`, action point as a sum, tail from `w` — the start position `a` is uniquely recoverable from the result and the displacement, with no ambiguity.


## TA5 — Hierarchical increment inc(t, k) produces t' > t

For tumbler `t ∈ T` and level `k ≥ 0`, `inc(t, k)` produces tumbler `t'` such that:

  (a) `t' > t` (strictly greater under T1),

  (b) `t'` agrees with `t` on all components before the increment point,

  (c) when `k = 0` (*sibling*): `#t' = #t`, and `t'` differs from `t` only at position `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`,

  (d) when `k > 0` (*child*): `#t' = #t + k`, the `k - 1` intermediate positions `#t + 1, ..., #t + k - 1` are set to `0` (field separators), and the final position `#t + k` is set to `1` (the first child).

In words: `inc(t, k)` advances a tumbler to the next peer at the same hierarchical level (`k = 0`) or creates the first descendant `k` levels deeper (`k > 0`). Both forms produce a strictly larger tumbler under T1 and leave all original components unchanged.

*Formal Contract:*
- *Definition:* `inc(t, k)` for `t ∈ T`, `k ≥ 0`: when `k = 0`, produce the sequence that agrees with `t` everywhere except at position `sig(t)`, where the value is `t_{sig(t)} + 1`; when `k > 0`, extend `t` by `k` positions — `k - 1` zeros followed by `1`.
- *Preconditions:* `t ∈ T`, `k ∈ ℕ` with `k ≥ 0`.
- *Postconditions:* (a) `t' > t` under T1. (b) `(A i : 1 ≤ i < sig(t) : t'ᵢ = tᵢ)` when `k = 0`; `(A i : 1 ≤ i ≤ #t : t'ᵢ = tᵢ)` when `k > 0`. (c) When `k = 0`: `#t' = #t`, and `t'` differs from `t` only at position `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`. (d) When `k > 0`: `#t' = #t + k`, `(A i : #t + 1 ≤ i ≤ #t + k - 1 : t'ᵢ = 0)`, and `t'_{#t+k} = 1`.
- *Frame:* When `k = 0`: all positions except `sig(t)` are unchanged, and length is preserved. When `k > 0`: all original positions `1, ..., #t` are unchanged.

**TA5 preserves T4 when `k ≤ 2` and `zeros(t) + k - 1 ≤ 3`.** The effective constraints are: `k = 0` (always valid), `k = 1` (when `zeros(t) ≤ 3`), `k = 2` (when `zeros(t) ≤ 2`). For `k ≥ 3`, T4 is violated — the appended `k - 1 ≥ 2` zeros include at least two adjacent zeros, creating an empty field regardless of the zero count.


### Zero tumblers and positivity

Under T3, the tumblers `[0]`, `[0, 0]`, `[0, 0, 0]`, etc., are *distinct* elements of T — they have different lengths. Under T1, they form a chain: `[0] < [0, 0] < [0, 0, 0] < ...` by the prefix rule. There is no single "zero tumbler"; there are infinitely many all-zero tumblers.

In words: Zero tumblers are individuated by length — `[0]` and `[0, 0]` are distinct elements of T, with the longer strictly greater than the shorter. This matters for span endpoints and sentinels, where the specific zero-tumbler length carries meaning.


## TA6 — Every all-zero tumbler (any length) is less than every positive tumbler and is not a valid address

`(A t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0) ⟹ t is not a valid address)`

`(A s, t ∈ T : (A i : 1 ≤ i ≤ #s : sᵢ = 0) ∧ (E j : 1 ≤ j ≤ #t : tⱼ > 0) ⟹ s < t)`

In words: No all-zero tumbler can designate content — valid addresses require `t₁ > 0` by T4. Every zero tumbler is strictly less than every positive tumbler under T1, making zero tumblers unconditional lower bounds in any ordered collection of addresses.

*Formal Contract:*
- *Postconditions:* (a) `(A t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0) ⟹ t is not a valid address)`. (b) `(A s, t ∈ T : (A i : 1 ≤ i ≤ #s : sᵢ = 0) ∧ (E j : 1 ≤ j ≤ #t : tⱼ > 0) ⟹ s < t)`.


### Subspace closure

An element-local position within subspace `S` has two components: the subspace identifier `N` and the ordinal `x`. Addition with displacement `w = [0, n]` (action point `k = 2`) preserves the subspace: `[N, x] ⊕ [0, n] = [N, x + n]`. Subtraction with the same form is a no-op: `[N, x] ⊖ [0, n]` finds divergence at position 1 (where `N > 0 = 0`) and produces `[N, x]`. The canonical resolution is ordinal-only arithmetic: pass only the within-subspace ordinal to the arithmetic operations, holding `N` as structural context external to the operands.

In words: The two-component representation `[N, x]` cannot support backward shifts because the subspace identifier forces a spurious divergence at position 1, making subtraction a no-op rather than a genuine reverse shift. Correct shift arithmetic requires stripping the identifier from the operands and treating it as structural context, not an arithmetic argument.


## PositiveTumbler — TumblerPositivity (DEFINITION, function)

A tumbler `t ∈ T` is *positive*, written `t > 0`, iff at least one of its components is nonzero: `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`. A tumbler is a *zero tumbler* iff every component is zero: `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.

Every positive tumbler is greater than every zero tumbler under T1. The condition `w > 0` in TA0 and TA4 excludes all all-zero displacements regardless of length.

In words: Positivity is the minimal condition for a tumbler to act as a meaningful displacement — at least one component must be nonzero. The definition applies uniformly by structure: a length-5 all-zero tumbler is a zero tumbler, not a positive one, regardless of its length.

*Formal Contract:*
- *Definition:* `t > 0` iff `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`; zero tumbler iff `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.
- *Postconditions:* `t > 0 ∧ (A i : 1 ≤ i ≤ #z : zᵢ = 0) ⟹ z < t` under T1.


## TA7a — Ordinal-only shift arithmetic

**S** = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)} — ordinals with all positive components, matching T4's positive-component constraint on element fields. An element-local displacement is a positive tumbler `w` with action point `k` satisfying `1 ≤ k ≤ #o`.

`(A o ∈ S, w > 0 : k ≤ #o ⟹ o ⊕ w ∈ T)`

`(A o ∈ S, w > 0 : o ≥ w ⟹ o ⊖ w ∈ T)`

In words: Performing addition or subtraction on within-subspace ordinals — with the subspace identifier held as external structural context — always produces a result in T. The subspace identifier is never an operand and cannot be modified by either operation, guaranteeing that no shift can escape the subspace.

*Formal Contract:*
- *Preconditions:* For `⊕`: `o ∈ S`, `w ∈ T`, `w > 0`, `actionPoint(w) ≤ #o`. For `⊖`: `o ∈ S`, `w ∈ T`, `o ≥ w`.
- *Postconditions:* `o ⊕ w ∈ T`. `o ⊖ w ∈ T`. For `⊕`, the result is in S when all tail components of `w` (after the action point) are positive.
- *Frame:* The subspace identifier `N`, held as structural context, is not an operand and is never modified by either operation.
- *Definition:* **S** = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)} — ordinals with all positive components, matching T4's positive-component constraint on element fields.


### What tumbler arithmetic is NOT

**The algebra is not a group.** There is no additive identity — the zero tumbler is a sentinel, not a neutral element for addition. There is no additive inverse for every element — subtraction is only defined when `a ≥ w`. The algebra is not closed under subtraction in general.

In words: Tumbler arithmetic satisfies none of the standard algebraic laws for integers — no identity, no inverses, no unconditional closure. Implementations must treat each operation as a partial function with explicit preconditions and must not assume group-theoretic identities.

## TA-assoc — Addition is associative where both compositions are defined

`(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)` whenever both sides are well-defined. Three cases exhaust the possibilities. Let `k_b` and `k_c` be the action points of `b` and `c` respectively. When `k_b < k_c`: both sides produce `aᵢ` for `i < k_b`, `aₖ_b + bₖ_b` at `k_b`, `bᵢ` for `k_b < i < k_c`, `bₖ_c + cₖ_c` at `k_c`, and `cᵢ` beyond. When `k_b = k_c = k`: both sides produce `aₖ + bₖ + cₖ` at `k` and `cᵢ` beyond. When `k_b > k_c`: both sides produce `aₖ_c + cₖ_c` at `k_c` and `cᵢ` beyond. The domain conditions are asymmetric — the left side requires `k_b ≤ #a`, the right requires only `min(k_b, k_c) ≤ #a` — but on the intersection the values agree.

In words: tumbler addition associates on the intersection of both sides' well-definedness domains. The three cases, determined by the relative order of the two displacements' action points, all yield identical component sequences on both sides.

*Dependencies:*
- **TA0 (Well-defined addition):** For `a, w ∈ T` with `w > 0` and action point `k ≤ #a`, `a ⊕ w ∈ T` with `#(a ⊕ w) = #w`. Supplies the result-length identity and domain conditions.
- **TumblerAdd (Constructive definition):** `(x ⊕ w)ᵢ = xᵢ` for `i < k`, `(x ⊕ w)ₖ = xₖ + wₖ`, `(x ⊕ w)ᵢ = wᵢ` for `i > k`, where `k = actionPoint(w)`. The three-region rule expanded throughout.
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. Used to conclude equality from length agreement and componentwise agreement.

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `b ∈ T`, `c ∈ T`, `b > 0`, `c > 0`, `k_b ≤ #a`, `k_c ≤ #b` (where `k_b = actionPoint(b)`, `k_c = actionPoint(c)`; these left-side conditions subsume the right-side conditions since `k_b ≤ #a` implies `min(k_b, k_c) ≤ #a`)
- *Postconditions:* `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)`; `#((a ⊕ b) ⊕ c) = #(a ⊕ (b ⊕ c)) = #c`; `actionPoint(b ⊕ c) = min(k_b, k_c)`

## TA-LC — LeftCancellation

If `a ⊕ x = a ⊕ y` with both sides well-defined (TA0 satisfied for both), then `x = y`.

In words: tumbler addition is left-cancellative. When two additions share the same starting position and produce equal results, the displacements must be identical — the common start can be cancelled out to recover the displacement uniquely.

*Formal Contract:*
- *Preconditions:* a, x, y ∈ T; x > 0; y > 0; actionPoint(x) ≤ #a; actionPoint(y) ≤ #a; a ⊕ x = a ⊕ y
- *Postconditions:* x = y

## TA-RC — Right cancellation fails

There exist tumblers `a`, `b`, `w` with `a ≠ b` and `a ⊕ w = b ⊕ w` (both sides well-defined).

In words: right cancellation fails for tumbler addition. Distinct starting positions can yield identical results under the same displacement, because TumblerAdd's tail-copy rule replaces all start components after the action point with the displacement's tail, discarding any differences between the two starts at those positions.

*Dependencies:*
- **TA0 (Well-defined addition):** For `a, w ∈ T` with `w > 0` and action point `k ≤ #a`, `a ⊕ w ∈ T` with `#(a ⊕ w) = #w`.
- **TumblerAdd (Constructive definition):** `(a ⊕ w)ᵢ = aᵢ` for `i < k`, `(a ⊕ w)ₖ = aₖ + wₖ`, `(a ⊕ w)ᵢ = wᵢ` for `i > k`; result length `#(a ⊕ w) = #w`.
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`.

*Formal Contract:*
- *Postconditions:* `∃ a, b, w ∈ T : w > 0 ∧ actionPoint(w) ≤ #a ∧ actionPoint(w) ≤ #b ∧ a ≠ b ∧ a ⊕ w = b ⊕ w`

## TA-MTO — ManyToOneEquivalence

For any displacement `w` with action point `k` and any tumblers `a`, `b` with `#a ≥ k` and `#b ≥ k`: `a ⊕ w = b ⊕ w` if and only if `aᵢ = bᵢ` for all `1 ≤ i ≤ k`.

In words: two tumblers produce the same result under a displacement if and only if they agree on every component up through and including the action point. This precisely characterises the equivalence classes collapsed by right addition — only the first `k` components of the start position influence the result, and any differences at deeper positions are silently overwritten.

*Dependencies:*
- **TA0 (Well-defined addition):** For `a, w ∈ T` with `w > 0` and action point `k ≤ #a`, `a ⊕ w ∈ T` with `#(a ⊕ w) = #w`. Used to establish that both additions `a ⊕ w` and `b ⊕ w` are well-defined.
- **TumblerAdd (Constructive definition):** `(a ⊕ w)ᵢ = aᵢ` for `i < k`, `(a ⊕ w)ₖ = aₖ + wₖ`, `(a ⊕ w)ᵢ = wᵢ` for `i > k`; result length `#(a ⊕ w) = #w`. Used to expand both sums componentwise and to establish that result length is independent of the start position.
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. Used in the forward direction to conclude equality from componentwise agreement, and contrapositively in the converse to extract componentwise agreement from equality.

*Formal Contract:*
- *Preconditions:* `w ∈ T`, `w > 0`, `a ∈ T`, `b ∈ T`, `#a ≥ actionPoint(w)`, `#b ≥ actionPoint(w)`
- *Postconditions:* `a ⊕ w = b ⊕ w ⟺ (A i : 1 ≤ i ≤ actionPoint(w) : aᵢ = bᵢ)`

## D0 — Displacement well-definedness

`a < b`, and the divergence `k` of `a` and `b` satisfies `k ≤ #a`.

In words: when `a` strictly precedes `b` and their first point of divergence lies within `a`'s length, the displacement `b ⊖ a` is a well-formed positive tumbler whose action point is exactly that divergence position, and the addition `a ⊕ (b ⊖ a)` is well-defined. The condition `k ≤ #a` excludes the case where `a` is a proper prefix of `b`, for which no well-defined addition back to `b` exists.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, a < b, divergence(a, b) ≤ #a
- *Postconditions:* b ⊖ a ∈ T, b ⊖ a > 0, actionPoint(b ⊖ a) = divergence(a, b), a ⊕ (b ⊖ a) ∈ T

## D1 — Displacement round-trip

For tumblers a, b ∈ T with a < b, divergence(a, b) ≤ #a, and #a ≤ #b:

  a ⊕ (b ⊖ a) = b

In words: the displacement from a to b, when added back to a, recovers b exactly. Displacement and addition are inverse operations under the stated preconditions — computing how far b is ahead of a and then applying that offset to a returns b component-by-component.

*Dependencies:*
- **D0 (DisplacementWellDefined):** Under `a < b` and `divergence(a, b) ≤ #a`: the displacement `w = b ⊖ a` is a well-defined positive tumbler with `actionPoint(w) = divergence(a, b)`, and `a ⊕ w ∈ T`.
- **TumblerSub (Constructive definition):** Zero-pad both operands to length `max(#b, #a)`. Let `k` be the first divergence; `(b ⊖ a)ᵢ = 0` for `i < k`, `(b ⊖ a)ₖ = bₖ - aₖ`, `(b ⊖ a)ᵢ = bᵢ` for `i > k`; result length `#(b ⊖ a) = max(#b, #a)`.
- **TumblerAdd (Constructive definition):** `(a ⊕ w)ᵢ = aᵢ` for `i < k`, `(a ⊕ w)ₖ = aₖ + wₖ`, `(a ⊕ w)ᵢ = wᵢ` for `i > k`, where `k = actionPoint(w)`; result length `#(a ⊕ w) = #w`.
- **Divergence definition:** For `a ≠ b`, `divergence(a, b)` is the least `k` where they differ; in case (i) `k ≤ min(#a, #b)` with `aₖ ≠ bₖ` and `aᵢ = bᵢ` for `i < k`; in case (ii) `k = min(#a, #b) + 1`.
- **T1 (Lexicographic order):** `a < b` iff `∃ k ≥ 1` with agreement before `k` and either (i) `k ≤ min(#a, #b)` and `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b`.
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, a < b, divergence(a, b) ≤ #a, #a ≤ #b
- *Postconditions:* a ⊕ (b ⊖ a) = b


## D2 — Displacement uniqueness

Under D1's preconditions (a < b, divergence(a, b) ≤ #a, #a ≤ #b), if a ⊕ w = b then w = b ⊖ a.

In words: the canonical displacement `b ⊖ a` is the only tumbler that produces b when added to a. D1 and D2 together fully characterize displacement: D1 guarantees `b ⊖ a` reaches b; D2 guarantees nothing else does.

*Dependencies:*
- **D0 (DisplacementWellDefined):** Under `a < b` and `divergence(a, b) ≤ #a`: the displacement `b ⊖ a` is a well-defined positive tumbler with `actionPoint(b ⊖ a) = divergence(a, b)`, and `a ⊕ (b ⊖ a) ∈ T`.
- **D1 (DisplacementRoundTrip):** Under `a < b`, `divergence(a, b) ≤ #a`, `#a ≤ #b`: `a ⊕ (b ⊖ a) = b`.
- **TA0 (Well-defined addition):** For tumblers `a, w ∈ T` where `w > 0` and `actionPoint(w) ≤ #a`, the result `a ⊕ w` is a well-defined tumbler in `T`.
- **TA-LC (LeftCancellation):** If `a ⊕ x = a ⊕ y` with both sides well-defined (TA0 satisfied for both), then `x = y`.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, divergence(a, b) ≤ #a, #a ≤ #b, a ⊕ w = b
- *Postconditions:* w = b ⊖ a


### Ordinal displacement and shift


## OrdinalDisplacement — ZeroPrefixLeafDisplacement

For natural number n ≥ 1 and depth m ≥ 1, the *ordinal displacement* δ(n, m) is the tumbler [0, 0, ..., 0, n] of length m — zero at positions 1 through m − 1, and n at position m. Its action point is m.

When the depth is determined by context (typically m = #v for the tumbler being shifted), we write δₙ.

In words: an ordinal displacement is a tumbler that is entirely zero above the deepest level and carries a positive value n at that level. It acts as a "pure advance" at depth m, leaving all higher-level structure untouched when used in addition.

*Formal Contract:*
- *Preconditions:* n ≥ 1, m ≥ 1
- *Definition:* δ(n, m) = [0, ..., 0, n] of length m, action point m


## OrdinalShift — DeepestComponentAdvance

For a tumbler v of length m and natural number n ≥ 1:

`shift(v, n) = v ⊕ δ(n, m)`

By OrdinalDisplacement, δ(n, m) = [0, ..., 0, n] of length m with action point m; since n ≥ 1, δ(n, m) > 0. The preconditions of TA0 are satisfied: δ(n, m) > 0 and action point k = m = #v. By TumblerAdd: shift(v, n)ᵢ = vᵢ for i < m, and shift(v, n)ₘ = vₘ + n. The shift preserves tumbler depth: #shift(v, n) = #v.

In words: shifting a tumbler by n increments its deepest component by exactly n while leaving every higher-level component unchanged. The result has the same depth as the input, and the deepest component remains positive since vₘ ≥ 0 and n ≥ 1.

*Formal Contract:*
- *Preconditions:* v ∈ T, n ≥ 1
- *Definition:* shift(v, n) = v ⊕ δ(n, #v)
- *Postconditions:* shift(v, n)ᵢ = vᵢ for i < #v, shift(v, n) at position #v = v at position #v + n, #shift(v, n) = #v, shift(v, n) at position #v ≥ 1


## TS1 — ShiftOrderPreservation

`(A v₁, v₂, n : n ≥ 1 ∧ #v₁ = #v₂ = m ∧ v₁ < v₂ : shift(v₁, n) < shift(v₂, n))`

In words: shifting two equal-depth tumblers by the same positive amount preserves their strict order. Because the shift only modifies the deepest component — which lies at or below the divergence point of any two distinct same-depth tumblers — it cannot alter which one is larger.

*Dependencies:*
- **OrdinalShift (Definition):** `shift(v, n) = v ⊕ δ(n, #v)`. Reduces the shift to tumbler addition with an ordinal displacement.
- **OrdinalDisplacement (Definition):** `δ(n, m) = [0, ..., 0, n]` of length `m`, with action point `m`. Supplies the displacement structure and its action point.
- **TA1-strict (Strict order preservation):** For `a < b`, `w > 0`, action point `k ≤ min(#a, #b)`, `k ≥ divergence(a, b)`: `a ⊕ w < b ⊕ w`.
- **Divergence (Definition):** For `a ≠ b` with `#a = #b = m`, `divergence(a, b) = min({j : 1 ≤ j ≤ m ∧ aⱼ ≠ bⱼ})`. Supplies the bound `divergence(v₁, v₂) ≤ m` needed in precondition (iv).

*Formal Contract:*
- *Preconditions:* v₁ ∈ T, v₂ ∈ T, n ≥ 1, #v₁ = #v₂ = m, v₁ < v₂
- *Postconditions:* shift(v₁, n) < shift(v₂, n)

## TS2 — ShiftInjectivity

`(A v₁, v₂, n : n ≥ 1 ∧ #v₁ = #v₂ = m : shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂)`

In words: the ordinal shift is injective over equal-length tumblers — if two tumblers of the same length produce the same result under the same positive shift, they must be identical. Knowing the shifted value and the shift amount uniquely determines the original tumbler.

*Preconditions:* v₁ ∈ T, v₂ ∈ T, n ≥ 1, #v₁ = #v₂ = m
*Postconditions:* shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂

---

## TS3 — ShiftComposition

`(A v, n₁, n₂ : n₁ ≥ 1 ∧ n₂ ≥ 1 ∧ #v = m : shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂))`

In words: composing two ordinal shifts produces the same result as a single shift by the sum of the amounts. Shift amounts combine additively, so `n₁` followed by `n₂` is indistinguishable from `n₁ + n₂` applied directly.

*Preconditions:* v ∈ T, n₁ ≥ 1, n₂ ≥ 1, #v = m
*Postconditions:* shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂)
*Frame:* #shift(shift(v, n₁), n₂) = #v = m (shift preserves tumbler length)

---

## TS4 — ShiftStrictIncrease

`(A v, n : n ≥ 1 ∧ #v = m : shift(v, n) > v)`

In words: any positive ordinal shift strictly advances a tumbler — the shifted result is always greater than the original. There is no positive shift that leaves a tumbler unchanged or moves it backward.

*Preconditions:* v ∈ T, n ≥ 1, #v = m
*Postconditions:* shift(v, n) > v

---

## TS5 — ShiftMonotonicity

`(A v, n₁, n₂ : n₁ ≥ 1 ∧ n₂ > n₁ ∧ #v = m : shift(v, n₁) < shift(v, n₂))`

In words: shift is strictly monotone in its amount parameter — a larger shift always produces a larger tumbler. Applying a smaller shift and a larger shift to the same tumbler yields two strictly ordered results, with the larger shift producing the greater address.

*Preconditions:* v ∈ T, n₁ ≥ 1, n₂ > n₁, #v = m
*Postconditions:* shift(v, n₁) < shift(v, n₂)

---

### Increment for allocation

A separate operation handles address allocation. We define the *last significant position* of a tumbler `t`:

- When `t` has at least one nonzero component: `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})`
- When every component is zero: `sig(t) = #t`

For valid addresses, `sig(t) = #t`, since T4's positive-component constraint ensures the last field component is nonzero. Therefore `inc(t, 0)` increments the last component of the last field, modifying only within that field and preserving the hierarchical structure.
