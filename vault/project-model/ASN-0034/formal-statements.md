# ASN-0034 Formal Statements

*Source: ASN-0034-tumbler-algebra.md (revised 2026-03-26) — Extracted: 2026-03-27*

## T0 — CarrierSetDefinition

`T = {d₁.d₂. ... .dₙ : each dᵢ ∈ ℕ, n ≥ 1}`. The natural numbers ℕ are taken with their standard properties, including closure under successor and addition.

In words: T is the set of all finite, non-empty sequences of natural numbers. This is an axiom — the carrier set is defined directly rather than derived.

*Formal Contract:*
- *Axiom:* T is the set of all finite sequences over ℕ with length ≥ 1; ℕ is closed under successor and addition.


## T0(a) — UnboundedComponentValues

`(A t ∈ T, i : 1 ≤ i ≤ #t : (A M ∈ ℕ :: (E t' ∈ T :: t' agrees with t except t'.dᵢ > M)))`.

In words: for every tumbler and every component position, there exists a tumbler whose value at that position exceeds any given bound. The address space within any subtree is inexhaustible — no component value is a ceiling.

*Formal Contract:*
- *Preconditions:* `t ∈ T`, `1 ≤ i ≤ #t`, `M ∈ ℕ`.
- *Postconditions:* There exists `t' ∈ T` such that `t'.dⱼ = t.dⱼ` for all `j ≠ i` and `t'.dᵢ > M`.
- *Frame:* `#t' = #t`; all components at positions `j ≠ i` are identical to those of `t`.
- *Axiom:* T is the set of all finite sequences over ℕ with length ≥ 1; ℕ is closed under successor.


## T0(b) — UnboundedNestingDepth

`(A n ∈ ℕ : n ≥ 1 : (E t ∈ T :: #t ≥ n))`.

In words: there is no maximum tumbler length — for every bound, a tumbler of at least that length exists in T. T0(a) ensures siblings within a level are inexhaustible; T0(b) ensures the levels themselves are inexhaustible.

*Formal Contract:*
- *Preconditions:* `n ∈ ℕ`, `n ≥ 1`.
- *Postconditions:* There exists `t ∈ T` such that `#t ≥ n`.
- *Axiom:* T is the set of all finite sequences over ℕ with length ≥ 1; there is no upper bound on the length of a finite sequence.


## T1 — LexicographicTotalOrder

For tumblers `a = a₁. ... .aₘ` and `b = b₁. ... .bₙ`, define `a < b` iff there exists `k ≥ 1` such that `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either:

  (i) `k ≤ min(m, n)` and `aₖ < bₖ`, or

  (ii) `k = m + 1 ≤ n` (that is, `a` is a proper prefix of `b`).

Sub-properties:
- (a) Irreflexivity — `(A a ∈ T :: ¬(a < a))`.
- (b) Trichotomy — `(A a,b ∈ T :: exactly one of a < b, a = b, b < a)`.
- (c) Transitivity — `(A a,b,c ∈ T : a < b ∧ b < c : a < c)`.

In words: tumblers are totally ordered by lexicographic comparison, where a proper prefix is less than any of its extensions. Any two tumblers are comparable, and comparison requires only the two sequences themselves — no external index or allocator state participates.

*Formal Contract:*
- *Definition:* `a < b` iff `∃ k ≥ 1` with `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either (i) `k ≤ min(m,n) ∧ aₖ < bₖ`, or (ii) `k = m+1 ≤ n`.
- *Postconditions:* (a) Irreflexivity — `(A a ∈ T :: ¬(a < a))`. (b) Trichotomy — `(A a,b ∈ T :: exactly one of a < b, a = b, b < a)`. (c) Transitivity — `(A a,b,c ∈ T : a < b ∧ b < c : a < c)`.

## T2 — ComparisonComputability

The order relation T1 is computable from the two tumblers alone, without consulting any external data structure. The comparison examines at most `min(#a, #b)` component pairs.

In words: tumbler comparison is a pure function of the two addresses — no external index, allocator state, or global registry participates. The comparison scans component pairs left-to-right and stops as soon as a decision is reached, examining at most `min(#a, #b)` pairs.

*Dependencies:*
- **T1 (Lexicographic order):** Defines `a < b` via witness position `k` with agreement below and either component divergence or prefix exhaustion at `k`.
- **T3 (Canonical representation):** Tumbler equality is sequence equality — same length and same components at every position.

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` — two well-formed tumblers (finite sequences over ℕ with `#a ≥ 1` and `#b ≥ 1`, per T0).
- *Postconditions:* (a) The ordering among `a` and `b` under T1 is determined. (b) At most `min(#a, #b)` component pairs are examined. (c) The only values consulted are `{aᵢ : 1 ≤ i ≤ #a}`, `{bᵢ : 1 ≤ i ≤ #b}`, `#a`, and `#b`.
- *Frame:* No external data structure is read or modified — the comparison is a pure function of the two tumblers.


### Canonical form

Equality of tumblers must mean component-wise identity. There must be no representation in which two distinct sequences of components denote the same abstract tumbler:


## T3 — CanonicalRepresentation

`(A a, b ∈ T : a₁ = b₁ ∧ ... ∧ aₙ = bₙ ∧ #a = #b ≡ a = b)`.

If two tumblers have the same length and the same components at every position, they are the same tumbler. Conversely, if they differ in any component or in length, they are distinct. No normalization, no trailing-zero ambiguity, no exponent variation can create aliases.

In words: a tumbler *is* its component sequence — no equivalence relation, quotient, or normalization map is imposed. Two tumblers are equal if and only if they have the same length and agree at every position; trailing zeros are significant and `[1, 2] ≠ [1, 2, 0]`.

*Dependencies:*
- **T0(a) (Carrier-set definition):** T is the set of all finite sequences over ℕ with length ≥ 1. A tumbler *is* its component sequence; no quotient, equivalence relation, or normalization map is imposed on T beyond sequence identity.

*Formal Contract:*
- *Postconditions:* Tumbler equality is sequence equality: `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`.
- *Frame:* No quotient, normalization, or external identification is imposed on T. Trailing zeros are significant: `[1, 2] ≠ [1, 2, 0]`.


### Hierarchical structure

Define a *field separator* as a component with value zero. An address tumbler has the form:

`t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`

where each `Nᵢ, Uⱼ, Dₖ, Eₗ > 0`. The four fields are:

- **Node field** `N₁. ... .Nₐ`: identifies the server.
- **User field** `U₁. ... .Uᵦ`: identifies the account.
- **Document field** `D₁. ... .Dᵧ`: identifies the document and version.
- **Element field** `E₁. ... .Eδ`: identifies the content element. The first component distinguishes the *subspace*: 1 for text content, 2 for links.

Not every tumbler need have all four fields. The count of zero-valued components determines the specificity level:

- `zeros(t) = 0`: node address (node field only)
- `zeros(t) = 1`: user address (node and user fields)
- `zeros(t) = 2`: document address (node, user, and document fields)
- `zeros(t) = 3`: element address (all four fields)


## T4 — FieldSeparatorConstraint

Every tumbler `t ∈ T` used as an address contains at most three zero-valued components, appearing in order as field separators, every non-separator component is strictly positive, and every field present in the address has at least one component. Formally, if `t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`, then `(A i : 1 ≤ i ≤ α : Nᵢ > 0)`, `(A j : 1 ≤ j ≤ β : Uⱼ > 0)`, `(A k : 1 ≤ k ≤ γ : Dₖ > 0)`, `(A l : 1 ≤ l ≤ δ : Eₗ > 0)`, and `α ≥ 1`, `β ≥ 1` when present, `γ ≥ 1` when present, `δ ≥ 1` when present.

The *positive-component constraint* — every component of every field is strictly positive — combined with the *non-empty field constraint* — each present field has at least one component — is equivalent to three syntactic conditions: no two zeros are adjacent, the tumbler does not begin with zero, and the tumbler does not end with zero. The function `fields(t)` that extracts the node, user, document, and element fields is well-defined and computable from `t` alone. Define `zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`.

In words: field separators are exactly the zero-valued components, every non-separator component is strictly positive, and the hierarchical level is uniquely determined by the count of zeros. Because no field component can be zero, every zero is unambiguously a separator and the parse of any address tumbler is unique and computable without external state.

*Dependencies:*
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. Used to establish that the component values of `t` are determinate — `tᵢ` is well-defined for each position — so that scanning for zeros is unambiguous.

*Formal Contract:*
- *Axiom:* Valid address tumblers satisfy `zeros(t) ≤ 3`, `(A i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0 : tᵢ > 0)`, no adjacent zeros, `t₁ ≠ 0`, `t_{#t} ≠ 0`.
- *Definition:* `zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`; `fields(t)` decomposes `t` into node, user, document, and element fields by partitioning at the zero-valued separator positions.
- *Postconditions:* (a) The non-empty field constraint is equivalent to three syntactic conditions: no adjacent zeros, `t₁ ≠ 0`, `t_{#t} ≠ 0`. (b) `fields(t)` is well-defined and uniquely determined by `t` alone. (c) `zeros(t)` determines the hierarchical level bijectively on `{0, 1, 2, 3}`.


### Contiguous subtrees

T4, combined with the total order T1, gives us the property that makes spans work:


## T5 — PrefixContiguity

For any tumbler prefix `p`, the set `{t ∈ T : p ≼ t}` (where `≼` denotes "is a prefix of") forms a contiguous interval under T1:

  `[p ≼ a ∧ p ≼ c ∧ a ≤ b ≤ c ⟹ p ≼ b]`

In words: if two tumblers share a common prefix `p`, every tumbler between them in lexicographic order also shares that prefix. No tumbler from outside the prefix subtree can interleave between two members of the subtree — a span between two prefix-sharing endpoints captures exactly the addresses under that prefix between those endpoints.

*Dependencies:*
- **T1 (Lexicographic order):** Defines `<` on T. Case (i): first divergence `k ≤ min(#a, #b)` with `aₖ < bₖ`. Case (ii): `a` is a proper prefix of `b`. Used to derive contradictions from ordering violations.
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. Distinct lengths entail distinct tumblers. Used in Case 2 to force strict inequality.

*Formal Contract:*
- *Definition:* `p ≼ t ⟺ #t ≥ #p ∧ (A i : 1 ≤ i ≤ #p : tᵢ = pᵢ)` — the tumbler `t` extends the prefix `p`.
- *Preconditions:* `a, b, c ∈ T`; `p` is a tumbler prefix with `#p ≥ 1`; `p ≼ a`; `p ≼ c`; `a ≤ b ≤ c` under the lexicographic order T1.
- *Postconditions:* `p ≼ b` — the tumbler `b` extends the prefix `p`, and therefore belongs to the same subtree as `a` and `c`.


### Decidable containment

The total order T1 determines *sequence* (which address comes first). But the system also needs *containment* — does address `a` belong to account `b`? Is document `d₁` under the same server as document `d₂`? These are not ordering questions; they are prefix questions.


## T6 — ContainmentDecidability

For any two tumblers `a, b ∈ T`, the following are decidable from the addresses alone:

  (a) Whether `a` and `b` share the same node field.

  (b) Whether `a` and `b` share the same node and user fields.

  (c) Whether `a` and `b` share the same node, user, and document-lineage fields.

  (d) Whether the document field of `a` is a prefix of the document field of `b` (structural subordination within a document family).

In words: all four containment relations — same server, same account, same document family, and document-field prefix — are decidable by finite scans of the two tumbler sequences alone, with no mapping tables, version graphs, or external state.

*Dependencies:*
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. Two finite sequences are equal iff they have the same length and agree componentwise. Used to establish that equality of finite sequences of natural numbers is decidable in finitely many steps.
- **T4 (Hierarchical parsing):** Valid address tumblers have at most three zero-valued components, every non-separator component is strictly positive, no adjacent zeros, no leading or trailing zero. (a) Non-empty field constraint. (b) `fields(t)` is well-defined and uniquely determined by `t` alone. (c) `zeros(t)` determines hierarchical level bijectively on `{0, 1, 2, 3}`. Used for field extraction and field-presence determination.

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` are valid tumblers satisfying T4 (positive-component constraint, at most three zeros, no adjacent zeros, no leading or trailing zero).
- *Definition:* `N(t)`, `U(t)`, `D(t)`, `E(t)` are the node, user, document, and element fields of `t`, extracted by `fields(t)` (T4(b)). Componentwise comparison of two finite sequences `S, R` checks `#S = #R ∧ (A i : 1 ≤ i ≤ #S : Sᵢ = Rᵢ)`. Prefix comparison of `S` against `R` checks `#S ≤ #R ∧ (A i : 1 ≤ i ≤ #S : Sᵢ = Rᵢ)`.
- *Postconditions:* (a) Returns *yes* iff `N(a) = N(b)` (componentwise); terminates in at most `#N(a) + 1` comparisons. (b) Returns *yes* iff both tumblers possess user fields and `N(a) = N(b) ∧ U(a) = U(b)` (componentwise); returns *no* if either lacks a user field; terminates in at most `#N(a) + #U(a) + 2` comparisons when both fields are present. (c) Returns *yes* iff both tumblers possess document fields and `N(a) = N(b) ∧ U(a) = U(b) ∧ D(a) = D(b)` (componentwise); returns *no* if either lacks a document field; terminates in at most `#N(a) + #U(a) + #D(a) + 3` comparisons when all fields are present. (d) Returns *yes* iff both tumblers possess document fields and `D(a)` is a prefix of `D(b)` — i.e., `#D(a) ≤ #D(b) ∧ (A k : 1 ≤ k ≤ #D(a) : D(a)ₖ = D(b)ₖ)`; returns *no* if either lacks a document field; terminates in at most `γₐ + 1` comparisons when both fields are present. All decisions use only the tumbler representations of `a` and `b`.


### Subspace disjointness

Within a document's element space, the first component after the third zero delimiter identifies the *subspace*: 1 for text, 2 for links. The critical property is permanent separation:

## T7 — Subspaces (text, links) within a document's element field are permanently dis...

`(A a, b ∈ T : a.E₁ ≠ b.E₁ ⟹ a ≠ b)`

The subspace identifier — the first component of the element field — permanently divides the address space into disjoint regions. Two element-level tumblers with different subspace identifiers are guaranteed distinct; no operation within one subspace can produce an address belonging to another.

*Dependencies:*
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. Contrapositively: tumblers that differ in length or at any component are distinct.
- **T4 (Hierarchical parsing):** (b) `fields(t)` is well-defined and uniquely determined by `t` alone. (c) `zeros(t) = 3` iff `t` is an element-level address. The positive-component constraint: every non-separator component is strictly positive, so every zero in `t` is unambiguously a field separator. The non-empty field constraint: every present field has at least one component (`α, β, γ, δ ≥ 1` for element-level addresses).

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` with `zeros(a) = zeros(b) = 3` (both are element-level addresses with well-formed field structure per T4).
- *Postconditions:* `a.E₁ ≠ b.E₁ ⟹ a ≠ b`.

## T8 — Once allocated, an address is never removed from the address space; the set o...

For every state transition `s → s'`, `allocated(s) ⊆ allocated(s')`. No operation removes an allocated address from the address space; the set of allocated addresses is monotonically non-decreasing.

This is a design requirement, not a derived property: the system specification defines no inverse operation. Addresses persist forever once allocated — including addresses with no stored content — which guarantees link stability, transclusion identity, and attribution.

*Formal Contract:*
- *Invariant:* For every state transition `s → s'`, `allocated(s) ⊆ allocated(s')`.
- *Axiom:* The system defines no operation that removes an element from the allocated set. This is a design constraint, not a derived property.

## T9 — Within a single allocator's sequential stream, new addresses are strictly mon...

`(A a, b : same_allocator(a, b) ∧ allocated_before(a, b) : a < b)`

Within a single allocator's sequential stream, each successive address is strictly greater than its predecessor under the tumbler order T1. This holds per-allocator, not globally — child addresses are inserted between the parent and the parent's next sibling regardless of wall-clock order, so the tumbler line as a whole does not grow monotonically by creation time.

*Dependencies:*
- **T10a (Allocator discipline):** Each allocator produces its sibling outputs exclusively by repeated application of `inc(·, 0)`.
- **TA5 (Hierarchical increment):** (a) `inc(t, 0)` produces `t' > t` under T1.
- **T1 (Lexicographic order):** (c) Transitivity: `a < b ∧ b < c ⟹ a < c`.

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` with `same_allocator(a, b) ∧ allocated_before(a, b)` — both addresses produced by the same allocator's sibling stream, `a` allocated before `b`.
- *Postconditions:* `a < b` under the tumbler order T1.

## T10 — Allocators with non-nesting prefixes produce distinct addresses without coord...

Let `p₁` and `p₂` be prefixes such that neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for any tumbler `a` with prefix `p₁` and any tumbler `b` with prefix `p₂`, `a ≠ b`.

Two allocators operating in distinct, non-nesting ownership domains can allocate addresses simultaneously with no coordination, and the resulting addresses are guaranteed never to collide. The address structure itself enforces uniqueness — no central authority or locking protocol is needed.

*Dependencies:*
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. Contrapositively: tumblers that differ at any component are distinct.
- **Prefix relation (from T1):** `p ≼ a` means `#p ≤ #a` and `aᵢ = pᵢ` for all `1 ≤ i ≤ #p`. Negation `p ⋠ a` means it is not the case that `p ≼ a`.

*Formal Contract:*
- *Preconditions:* `p₁, p₂ ∈ T` with `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`; `a, b ∈ T` with `p₁ ≼ a` and `p₂ ≼ b`.
- *Postconditions:* `a ≠ b`.

## T10a — Each allocator uses inc(·, 0) for siblings and inc(·, k>0) only for child-spa...

Each allocator produces its sibling outputs exclusively by repeated application of `inc(·, 0)` — shallow increment at the last significant position. To spawn a child allocator, the parent performs one `inc(·, k')` with `k' > 0` to establish the child's prefix, then delegates further allocation to the child. The parent's own sibling stream resumes with `inc(·, 0)`.

This constraint guarantees three structural properties: all siblings from a single allocator have equal length; sibling prefixes never nest (satisfying T10's non-nesting precondition); and child allocator outputs are always strictly longer than parent sibling outputs, preventing cross-level collisions. Relaxing the constraint — allowing a sibling to be produced by `inc(·, k')` with `k' > 0` — produces a proper-prefix relationship between siblings, collapsing T10's partition independence.

*Dependencies:*
- **TA5 (Hierarchical increment):** (a) `inc(t, k)` produces `t' > t` under T1. (b) `t'` agrees with `t` on all components before the increment point. (c) When `k = 0`: `#t' = #t`, and `t'` differs from `t` only at `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`. (d) When `k > 0`: `#t' = #t + k`, with `k - 1` zero field separators and final component `1`.
- **T1 (Lexicographic order):** `a < b` iff there exists `k ≥ 1` with `aᵢ = bᵢ` for all `i < k`, and either (i) `k ≤ min(#a, #b)` and `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b` (proper prefix). Irreflexivity: `¬(a < a)`.
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. Contrapositively: tumblers of different lengths are distinct.
- **T10 (Partition independence):** For non-nesting prefixes `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`, any tumbler extending `p₁` is distinct from any tumbler extending `p₂`.
- **Prefix relation (from T1):** `p ≼ a` means `#p ≤ #a` and `aᵢ = pᵢ` for all `1 ≤ i ≤ #p`. A proper prefix `p ≺ a` requires `p ≼ a` with `p ≠ a`, entailing `#p < #a`.

*Formal Contract:*
- *Axiom:* Allocators produce sibling outputs exclusively by `inc(·, 0)`; child-spawning uses exactly one `inc(·, k')` with `k' > 0`.
- *Postconditions:* (a) Uniform sibling length — `(A tᵢ, tⱼ : same_allocator(tᵢ, tⱼ) ∧ sibling(tᵢ) ∧ sibling(tⱼ) : #tᵢ = #tⱼ)`. (b) Non-nesting sibling prefixes — `(A tᵢ, tⱼ : same_allocator(tᵢ, tⱼ) ∧ sibling(tᵢ) ∧ sibling(tⱼ) ∧ tᵢ ≠ tⱼ : tᵢ ⋠ tⱼ ∧ tⱼ ⋠ tᵢ)`. (c) Length separation — child outputs have length strictly greater than parent sibling outputs: `(A t_parent, t_child : sibling(t_parent) ∧ spawned_by(t_child, t_parent) : #t_child > #t_parent)`.

## PrefixOrderingExtension — NonNestingSubtreeOrdering

Let `p₁, p₂ ∈ T` be tumblers such that `p₁ < p₂` and neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for every `a` extending `p₁` (`p₁ ≼ a`) and every `b` extending `p₂` (`p₂ ≼ b`), `a < b`.

*Dependencies:*
- **T1 (Lexicographic order):** `a < b` iff there exists least `k ≥ 1` with `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either (i) `k ≤ min(#a, #b)` with `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b` (proper prefix).
- **Prefix relation (from T1):** `p ≼ a` means `#p ≤ #a` and `aᵢ = pᵢ` for all `1 ≤ i ≤ #p`.

In words: when two tumblers are ordered and neither is a prefix of the other, every address descending from the first precedes every address descending from the second under T1. The ordering of sibling prefixes propagates unconditionally to all their extensions.

*Formal Contract:*
- *Preconditions:* `p₁, p₂ ∈ T` with `p₁ < p₂` (T1) and `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` (non-nesting); `a, b ∈ T` with `p₁ ≼ a` and `p₂ ≼ b`.
- *Postconditions:* `a < b` under T1.


## PartitionMonotonicity — Per-allocator ordering extends cross-allocator; for non-nesting sibling prefi...

Within any prefix-delimited partition of the address space, the set of allocated addresses is totally ordered by T1, and this order is consistent with the allocation order of any single allocator within that partition. Moreover, for any two sibling sub-partitions with non-nesting prefixes `p₁ < p₂`, every address extending `p₁` precedes every address extending `p₂` under T1 — the per-allocator ordering extends to a cross-allocator ordering determined by the prefix structure.

*Dependencies:*
- **T1 (Lexicographic order):** `a < b` iff there exists least `k ≥ 1` with `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either (i) `k ≤ min(#a, #b)` with `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b` (proper prefix). The relation is a strict total order on `T`.
- **T5 (Contiguous subtrees):** For any tumbler prefix `p`, the set `{t ∈ T : p ≼ t}` forms a contiguous interval under T1: `[p ≼ a ∧ p ≼ c ∧ a ≤ b ≤ c ⟹ p ≼ b]`.
- **T9 (Forward allocation):** `(A a, b : same_allocator(a, b) ∧ allocated_before(a, b) : a < b)`.
- **T10a (Allocator discipline):** Each allocator produces sibling outputs exclusively by `inc(·, 0)`. To spawn a child, it performs one `inc(·, k')` with `k' > 0`.
- **TA5 (Hierarchical increment):** (a) `inc(t, k) > t`; (b) `inc(t, k)` agrees with `t` on all components before the increment point; (c) when `k = 0`: `#inc(t, 0) = #t`, differing from `t` only at position `sig(t)` where `inc(t, 0)_{sig(t)} = t_{sig(t)} + 1`; (d) when `k > 0`: `#inc(t, k) = #t + k`, with the first `#t` components preserved, `k - 1` zero field separators at positions `#t + 1` through `#t + k - 1`, and final component `1` at position `#t + k`.
- **PrefixOrderingExtension:** For `p₁, p₂ ∈ T` with `p₁ < p₂` and `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`, every `a` extending `p₁` and every `b` extending `p₂` satisfy `a < b`.
- **Prefix relation (from T1):** `p ≼ a` means `#p ≤ #a` and `aᵢ = pᵢ` for all `1 ≤ i ≤ #p`. A proper prefix `p ≺ a` requires `p ≼ a` with `p ≠ a`, entailing `#p < #a`.

In words: the prefix tree structure imposes a global total order on all allocated addresses that is simultaneously consistent with T1, with per-allocator allocation order, and with sub-partition containment. Addresses in earlier sibling sub-partitions always precede those in later sibling sub-partitions, and within any sub-partition allocation order matches address order.

*Formal Contract:*
- *Preconditions:* A system conforming to T10a (allocator discipline); a partition with prefix `p ∈ T`; sub-partition prefixes `t₀, t₁, ...` produced by `inc(·, 0)` from an initial child prefix `t₀ = inc(s, k)` with `k > 0` and `p ≼ s`.
- *Postconditions:* (1) For sibling sub-partition prefixes `tᵢ < tⱼ` (with `i < j`) and any `a, b ∈ T` with `tᵢ ≼ a` and `tⱼ ≼ b`: `a < b`. (2) Within each sub-partition with prefix `tᵢ`: `allocated_before(a, b) ⟹ a < b`.
- *Invariant:* For every reachable system state, the set of allocated addresses within any prefix-delimited partition is totally ordered by T1 consistently with per-allocator allocation order.


## GlobalUniqueness — No two distinct allocation events anywhere in the system at any time produce ...

No two distinct allocations, anywhere in the system, at any time, produce the same address.

*Dependencies:*
- **T1 (Lexicographic order):** `a < b` iff there exists `k ≥ 1` with `aᵢ = bᵢ` for all `i < k`, and either (i) `k ≤ min(#a, #b)` and `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b` (proper prefix). Part (a): irreflexivity — `¬(a < a)`.
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. Contrapositive: `#a ≠ #b ⟹ a ≠ b`.
- **T4 (Hierarchical parsing):** The zero count `zeros(t)` — the number of zero-valued field-separator components — uniquely determines the hierarchical level. The correspondence is injective: distinct levels entail distinct zero counts.
- **T9 (Forward allocation):** `(A a, b : same_allocator(a, b) ∧ allocated_before(a, b) : a < b)`.
- **T10 (Partition independence):** For prefixes `p₁, p₂` with `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`, every `a` extending `p₁` and every `b` extending `p₂` satisfy `a ≠ b`.
- **T10a (Allocator discipline):** Each allocator produces sibling outputs exclusively by `inc(·, 0)`. To spawn a child, it performs one `inc(·, k')` with `k' > 0`.
- **TA5 (Hierarchical increment):** (a) `inc(t, k) > t`; (c) when `k = 0`: `#inc(t, 0) = #t`; (d) when `k > 0`: `#inc(t, k) = #t + k`.

In words: the tumbler addressing scheme guarantees that no two allocation events — whether from the same allocator, sibling allocators, or allocators at different hierarchical levels — can produce the same address. Uniqueness arises purely from the structure of the naming system, without any distributed coordination or consensus.

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` produced by distinct allocation events within a system conforming to T10a (allocator discipline).
- *Invariant:* For every pair of addresses `a, b` produced by distinct allocation events in any reachable system state: `a ≠ b`.


## T12 — A span (s, ℓ) is well-formed when ℓ > 0 and action point k of ℓ satisfies k ≤...

A span `(s, ℓ)` is well-formed when `ℓ > 0` and the action point `k` of `ℓ` satisfies `k ≤ #s` (the TA0 precondition for `s ⊕ ℓ`). Equivalently, the number of leading zeros in `ℓ` must be strictly less than `#s`. A well-formed span denotes the set `{t ∈ T : s ≤ t < s ⊕ ℓ}`. This set is contiguous under T1 — there is no tumbler between two members that is not itself a member.

Sub-properties:
- **(a) Endpoint existence:** `s ⊕ ℓ ∈ T` (by TA0).
- **(b) Non-emptiness:** `s ∈ span(s, ℓ)` (by TA-strict).
- **(c) Contiguity:** `span(s, ℓ)` is order-convex under T1: for all `a, c ∈ span(s, ℓ)` and `b ∈ T`, `a ≤ b ≤ c` implies `b ∈ span(s, ℓ)`.

*Dependencies:*
- **T1 (Lexicographic order):** `<` is a strict total order on T. We write `a ≤ b` for the reflexive closure: `a ≤ b` iff `a < b ∨ a = b`. T1(c) gives transitivity of `<`.
- **TA0 (Well-defined addition):** For `a, w ∈ T` with `w > 0` and action point `k ≤ #a`, `a ⊕ w ∈ T`.
- **TA-strict (Strict increase):** For `a ∈ T` and `w > 0` with action point `k ≤ #a`, `a ⊕ w > a`.

In words: a well-formed span is an interval `[s, s ⊕ ℓ)` in the tumbler address space — it is non-empty, its endpoint exists in T, and it contains every tumbler address lying between its start and end. The well-formedness condition ensures the displacement `ℓ` acts within the depth of the start position `s`.

*Formal Contract:*
- *Preconditions:* `s ∈ T`, `ℓ ∈ T`, `ℓ > 0`, `actionPoint(ℓ) ≤ #s`
- *Definition:* `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}`
- *Postconditions:* (a) `s ⊕ ℓ ∈ T` (endpoint exists, by TA0). (b) `s ∈ span(s, ℓ)` (non-empty, by TA-strict). (c) `span(s, ℓ)` is order-convex under T1 (for all `a, c ∈ span(s, ℓ)` and `b ∈ T`, `a ≤ b ≤ c` implies `b ∈ span(s, ℓ)`).


## TA0 — Tumbler addition a ⊕ w is well-defined when w > 0 and the action point k sati...

For tumblers `a, w ∈ T` where `w > 0` and the action point `k` of `w` satisfies `k ≤ #a`, the result `a ⊕ w` is a well-defined tumbler in `T`.

The precondition `k ≤ #a` is essential: the constructive definition copies components `a₁, ..., aₖ₋₁` from the start position and adds `wₖ` to `aₖ`, so position `k` must exist within `a`. A displacement whose action point exceeds `#a` — one with more leading zeros than `a` has components — would attempt to "stay at" hierarchical levels that the start position does not have, and the operation is undefined.

*Dependencies:*
- **T0 (Carrier-set definition):** T is the set of all finite sequences over ℕ with length ≥ 1; ℕ is closed under addition.
- **TumblerAdd (Constructive definition):** `(a ⊕ w)ᵢ = aᵢ` for `i < k`, `(a ⊕ w)ₖ = aₖ + wₖ`, `(a ⊕ w)ᵢ = wᵢ` for `i > k`; result length `#(a ⊕ w) = #w`.

In words: tumbler addition is well-defined precisely when the displacement's first nonzero component falls within the length of the start address. The result is a tumbler whose length equals the displacement's length — the displacement's tail replaces the start address's tail beyond the action point.

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `w > 0`, `actionPoint(w) ≤ #a`
- *Postconditions:* `a ⊕ w ∈ T`, `#(a ⊕ w) = #w`

## TA1 — Addition preserves the total order (weak)

`(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) : a ⊕ w ≤ b ⊕ w)`, where `k` is the action point of `w`.

In words: advancing two ordered positions by the same displacement never reverses their order. If `a < b` and both positions admit the displacement `w`, then `a ⊕ w ≤ b ⊕ w`. The guarantee is weak (≤): when `a` is a proper prefix of `b`, advancement erases the length difference and the results may be equal.

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `b ∈ T`, `w ∈ T`, `a < b`, `w > 0`, `actionPoint(w) ≤ min(#a, #b)`
- *Postconditions:* `a ⊕ w ≤ b ⊕ w`

## Divergence — Divergence point of two unequal tumblers (DEFINITION, function)

For tumblers `a, b ∈ T` with `a ≠ b`, `divergence(a, b)` is defined by two cases:

(i) If there exists `k ≤ min(#a, #b)` such that `aₖ ≠ bₖ` and `(A i : 1 ≤ i < k : aᵢ = bᵢ)`, then `divergence(a, b) = k`.

(ii) If `(A i : 1 ≤ i ≤ min(#a, #b) : aᵢ = bᵢ)` and `#a ≠ #b`, then `divergence(a, b) = min(#a, #b) + 1`.

In words: the divergence point is the index of the first position at which two unequal tumblers differ. In case (i) they disagree at a position both possess; in case (ii) they agree on all shared positions but one is strictly longer, so the divergence lies one past the end of the shorter tumbler.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, a ≠ b
- *Definition:* divergence(a, b) = k, where (i) if ∃ i with 1 ≤ i ≤ min(#a, #b) and aᵢ ≠ bᵢ, then k = min({i : 1 ≤ i ≤ min(#a, #b) ∧ aᵢ ≠ bᵢ}); (ii) if (A i : 1 ≤ i ≤ min(#a, #b) : aᵢ = bᵢ) and #a ≠ #b, then k = min(#a, #b) + 1

## TA1-strict — StrictOrderPreservation

`(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) ∧ k ≥ divergence(a, b) : a ⊕ w < b ⊕ w)`, where `k` is the action point of `w`.

In words: advancement by the same displacement preserves strict order whenever the action point falls at or after the first position where the two tumblers disagree. When the action point falls before the divergence, both results copy the same prefix and inherit the same tail from `w`, erasing the original difference and producing equality; TA1-strict excludes that case by requiring `k ≥ divergence(a, b)`.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, w > 0, actionPoint(w) ≤ min(#a, #b), actionPoint(w) ≥ divergence(a, b)
- *Postconditions:* a ⊕ w < b ⊕ w

## TA-strict — Adding a positive displacement strictly advances

`(A a ∈ T, w > 0 : a ⊕ w > a)` (where `a ⊕ w` is well-defined, i.e., `k ≤ #a` per TA0).

In words: adding any positive displacement moves a position strictly forward — `a ⊕ w` is always greater than `a` under the tumbler order. This rules out degenerate models where addition is a no-op, ensuring that spans have non-empty interiors and that TA1's order-preservation guarantee is substantive.

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `w > 0`, `k ≤ #a` where `k` is the action point of `w`
- *Postconditions:* `a ⊕ w > a`

## TA2 — Tumbler subtraction a ⊖ w is well-defined when a ≥ w

For tumblers `a, w ∈ T` where `a ≥ w`, `a ⊖ w` is a well-defined tumbler in `T`.

In words: when one position is at least as large as another under the tumbler order, their difference is itself a valid tumbler. The result length is `max(#a, #w)` — the longer of the two operands' lengths.

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `a ≥ w`
- *Postconditions:* `a ⊖ w ∈ T`, `#(a ⊖ w) = max(#a, #w)`

## TA3 — Subtraction preserves the total order (weak)

`(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w ≤ b ⊖ w)`

Subtracting a common lower bound from two tumblers preserves their weak order: if `a` precedes `b` and both dominate `w`, then `a ⊖ w` precedes or equals `b ⊖ w`. Equality is permitted when `a` and `b` differ only in length beyond their shared prefix relative to `w`.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w
- *Postconditions:* a ⊖ w ≤ b ⊖ w


## TA3-strict — Subtraction preserves the total order (strict) when additionally #a = #b

`(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b : a ⊖ w < b ⊖ w)`

When `a` and `b` are equal-length tumblers with `a < b` and both dominating `w`, subtracting the same lower bound preserves strict order. The equal-length constraint rules out the prefix case that permits equality in TA3, ensuring strict inequality is maintained after subtraction.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w, #a = #b
- *Postconditions:* a ⊖ w < b ⊖ w


### Partial inverse


## TA4 — Addition and subtraction are partial inverses

`(A a, w : w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊕ w) ⊖ w = a)`, where `k` is the action point of `w`.

Adding a displacement and then subtracting it recovers the original tumbler, provided three conditions hold: the action point of `w` coincides with `#a`, the displacement has no components beyond the action point, and `a` is zero at all positions before the action point. Outside these conditions, `⊕` and `⊖` are not inverses in general.

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `w > 0`, `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`, where `k` is the action point of `w`
- *Postconditions:* `(a ⊕ w) ⊖ w = a`


## ReverseInverse — SubtractAddInverse

`(A a, w : a ≥ w ∧ w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊖ w) ⊕ w = a)`, where `k` is the action point of `w`.

Subtracting a displacement and then adding it back recovers the original tumbler — the reverse direction of TA4. Together with TA4, this establishes that `⊕` and `⊖` are mutual inverses under the shared preconditions: the action point of `w` coincides with `#a`, `w` has no components beyond the action point, and `a` is zero before the action point.

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `a ≥ w`, `w > 0`, `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`, where `k` is the action point of `w`
- *Postconditions:* `(a ⊖ w) ⊕ w = a`


### Constructive definition of ⊕ and ⊖


## TumblerAdd — PositionAdvanceOperation

Let `a = [a₁, ..., aₘ]` and `w = [w₁, ..., wₙ]` with `w > 0`. With action point `k`:

```
         ⎧ aᵢ           if i < k        (copy from start)
rᵢ   =  ⎨ aₖ + wₖ      if i = k        (single-component advance)
         ⎩ wᵢ           if i > k        (copy from displacement)
```

*Result-length identity:* **`#(a ⊕ w) = #w`** — the result length is determined entirely by the displacement.

Tumbler addition `a ⊕ w` is a position-advance operation, not componentwise arithmetic: the displacement `w` encodes both the hierarchical level of the advance (its action point `k`) and the sub-structure of the landing position (its tail). Components before `k` copy from `a`, the action component adds, and components after `k` copy from `w` — discarding `a`'s trailing structure entirely.

Three definitional properties:

**No carry propagation:** `aₖ + wₖ` is a single natural-number addition; no carry propagates into position `k − 1`.

**Tail replacement, not tail addition:** Components at positions `k + 1, ..., m` of `a` are discarded; the tail of the result comes entirely from `w`.

**Many-to-one:** Distinct start positions that share a prefix through position `k` but differ in their tails produce identical results — advancing to a landmark position lands at the same place regardless of starting sub-structure below the action point.

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `w > 0`, `actionPoint(w) ≤ #a`
- *Definition:* `(a ⊕ w)ᵢ = aᵢ` for `i < k`, `(a ⊕ w)ₖ = aₖ + wₖ`, `(a ⊕ w)ᵢ = wᵢ` for `i > k`, where `k = actionPoint(w)`
- *Postconditions:* `#(a ⊕ w) = #w`

## TumblerSub — StartPositionRecovery (DEFINITION, function)

Given an end position `a` and a displacement `w`, recover the start position. When the operands have different lengths, we conceptually zero-pad the shorter to the length of the longer before scanning for divergence. When the zero-padded sequences agree at every position (no divergence exists), the result is the zero tumbler of length `max(#a, #w)`: `a ⊖ w = [0, ..., 0]`. Otherwise, let `k` be the first position where `a` and `w` differ (treating missing components as zero):

```
         ⎧ 0             if i < k        (these levels matched — zero them)
rᵢ   =  ⎨ aₖ - wₖ      if i = k        (reverse the advance)
         ⎩ aᵢ           if i > k        (copy from end position)
```

The result has length `max(#a, #w)`.

**Precondition:** `a ≥ w` — when `a ≠ w`, at the divergence point (after zero-padding) `aₖ ≥ wₖ`.

In words: tumbler subtraction recovers the starting position given an ending position and a displacement. The operation zeros all components before the first divergence, adjusts the diverging component by the displacement's value there, and copies the end position's remaining components verbatim. Subtraction is only defined when `a ≥ w`.

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `a ≥ w`
- *Definition:* Zero-pad both operands to length `max(#a, #w)`. If the padded sequences agree at every position, `a ⊖ w = [0, ..., 0]` of length `max(#a, #w)`. Otherwise, let `k` be the first divergence position: `(a ⊖ w)ᵢ = 0` for `i < k`, `(a ⊖ w)ₖ = aₖ - wₖ`, `(a ⊖ w)ᵢ = aᵢ` for `i > k`, with `#(a ⊖ w) = max(#a, #w)`.


### Verification of TA1 and TA1-strict

**Claim:** (TA1, weak form). If `a < b`, `w > 0`, and `k ≤ min(#a, #b)`, then `a ⊕ w ≤ b ⊕ w`.

**Claim:** (TA1-strict). If additionally `k ≥ divergence(a, b)`, then `a ⊕ w < b ⊕ w`.

In words: adding the same displacement to two tumblers preserves their order. Strict order is preserved when the displacement's action point meets or exceeds their divergence position; otherwise the displacement may erase the original divergence, yielding equality.


### Verification of TA3

**Claim:** (TA3, weak form). If `a < b`, `a ≥ w`, and `b ≥ w`, then `a ⊖ w ≤ b ⊖ w`.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w
- *Postconditions:* a ⊖ w ≤ b ⊖ w

**Claim:** (TA3-strict). If `a < b`, `a ≥ w`, `b ≥ w`, and `#a = #b`, then `a ⊖ w < b ⊖ w`.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w, #a = #b
- *Postconditions:* a ⊖ w < b ⊖ w

In words: subtracting the same value from two ordered tumblers preserves their order (weakly). Equal-length tumblers cannot be in a prefix relationship, which eliminates the only case that produces equality rather than strict order — so equal-length operands give strict inequality.


### Verification of TA4

**Claim.** `(a ⊕ w) ⊖ w = a` under the full precondition: `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`.

In words: addition followed by subtraction of the same displacement is the identity, provided the start position has all-zero prefix (the standard address form) and the displacement's length matches the position's length.

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `w > 0`, `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`, where `k` is the action point of `w`
- *Postconditions:* `(a ⊕ w) ⊖ w = a`


### Cancellation properties of ⊕

TumblerAdd's constructive definition determines each component of the result from exactly one input. This makes the operation left-cancellative.


## TA5 — Hierarchical increment inc(t, k) produces t' > t

For tumbler `t ∈ T` and level `k ≥ 0`, there exists an operation `inc(t, k)` producing tumbler `t'` such that:

  (a) `t' > t` (strictly greater under T1),

  (b) `t'` agrees with `t` on all components before the increment point,

  (c) when `k = 0` (*sibling*): `#t' = #t`, and `t'` differs from `t` only at position `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`,

  (d) when `k > 0` (*child*): `#t' = #t + k`, the `k - 1` intermediate positions `#t + 1, ..., #t + k - 1` are set to `0` (field separators), and the final position `#t + k` is set to `1` (the first child).

In words: `inc(t, k)` advances a tumbler to its next peer at relative depth `k`. When `k = 0`, it increments the last significant component (next sibling); when `k > 0`, it appends `k - 1` zero separators and a `1` (first child at depth `k`). The result is always strictly greater than `t` under T1.

*Dependencies:*
- **T1 (Lexicographic order):** `a < b` iff there exists `k ≥ 1` with `aᵢ = bᵢ` for all `i < k`, and either (i) `k ≤ min(#a, #b)` and `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b` (proper prefix).
- **sig(t):** The last significant position of `t`. When `t` has at least one nonzero component, `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})`; when every component of `t` is zero, `sig(t) = #t`.

*Formal Contract:*
- *Definition:* `inc(t, k)` for `t ∈ T`, `k ≥ 0`: when `k = 0`, produce the sequence that agrees with `t` everywhere except at position `sig(t)`, where the value is `t_{sig(t)} + 1`; when `k > 0`, extend `t` by `k` positions — `k - 1` zeros followed by `1`.
- *Preconditions:* `t ∈ T`, `k ∈ ℕ` with `k ≥ 0`.
- *Postconditions:* (a) `t' > t` under T1. (b) `(A i : 1 ≤ i < sig(t) : t'ᵢ = tᵢ)` when `k = 0`; `(A i : 1 ≤ i ≤ #t : t'ᵢ = tᵢ)` when `k > 0`. (c) When `k = 0`: `#t' = #t`, and `t'` differs from `t` only at position `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`. (d) When `k > 0`: `#t' = #t + k`, `(A i : #t + 1 ≤ i ≤ #t + k - 1 : t'ᵢ = 0)`, and `t'_{#t+k} = 1`.
- *Frame:* When `k = 0`: all positions except `sig(t)` are unchanged, and length is preserved. When `k > 0`: all original positions `1, ..., #t` are unchanged.


### Zero tumblers and positivity

Under T3, the tumblers `[0]`, `[0, 0]`, `[0, 0, 0]`, etc., are *distinct* elements of T — they have different lengths. Under T1, they form a chain: `[0] < [0, 0] < [0, 0, 0] < ...` by the prefix rule. There is no single "zero tumbler"; there are infinitely many all-zero tumblers.


## TA6 — Every all-zero tumbler (any length) is less than every positive tumbler and i...

No zero tumbler is a valid address — no all-zero tumbler designates content. Every zero tumbler is less than every positive tumbler under T1.

  `(A t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0) ⟹ t is not a valid address)`

  `(A s, t ∈ T : (A i : 1 ≤ i ≤ #s : sᵢ = 0) ∧ (E j : 1 ≤ j ≤ #t : tⱼ > 0) ⟹ s < t)`

In words: zero tumblers (all components zero) are never valid addresses and are strictly less than every positive tumbler in the T1 order, regardless of their respective lengths. This makes zero tumblers usable as sentinels and universal lower bounds in span operations.

*Dependencies:*
- **T1 (Lexicographic order):** `a < b` iff there exists `k ≥ 1` with `aᵢ = bᵢ` for all `i < k`, and either (i) `k ≤ min(#a, #b)` and `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b` (proper prefix).
- **T4 (Hierarchical parsing):** Every valid address satisfies the positive-component constraint — every field component is strictly positive. In particular, the first component belongs to the node field, which has at least one component, so `t₁ > 0` for every valid address.

*Formal Contract:*
- *Postconditions:* (a) `(A t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0) ⟹ t is not a valid address)`. (b) `(A s, t ∈ T : (A i : 1 ≤ i ≤ #s : sᵢ = 0) ∧ (E j : 1 ≤ j ≤ #t : tⱼ > 0) ⟹ s < t)`.

Zero tumblers serve as *sentinels*: they mark uninitialized values, denote "unbounded" when used as span endpoints, and act as lower bounds.


### Subspace closure

A position in subspace `S` with identifier `N` and ordinal `x` uses displacement `w = [0, n]` (action point `k = 2`) for element-local shifts. Addition preserves the subspace: `[N, x] ⊕ [0, n] = [N, x + n]`. Subtraction does not: `[N, x] ⊖ [0, n]` finds the first divergence at position 1 (where `N ≠ 0 = w₁`), producing `[N, x]` — a no-op. The resolution is the ordinal-only formulation: the subspace identifier `N` is structural context, not an operand to the arithmetic. Shift operations receive ordinals `[o₁, ..., oₘ]` directly, with `N` held outside the computation, ensuring no shift can escape the subspace.


## PositiveTumbler — PositiveTumblerDefinition (DEFINITION, function)

A tumbler `t ∈ T` is *positive*, written `t > 0`, iff at least one of its components is nonzero: `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`. A tumbler is a *zero tumbler* iff every component is zero: `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.

Every positive tumbler is greater than every zero tumbler under T1. The condition `w > 0` in TA0 and TA4 excludes all all-zero displacements regardless of length.

In words: positivity distinguishes tumblers that represent genuine content from zero sentinels. A positive tumbler has at least one nonzero component and is strictly greater than any zero tumbler of any length under T1.

*Dependencies:*
- **T1 (Lexicographic order):** `a < b` iff there exists `k ≥ 1` with `aᵢ = bᵢ` for all `i < k`, and either (i) `k ≤ min(#a, #b)` and `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b` (proper prefix).

*Formal Contract:*
- *Definition:* `t > 0` iff `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`; zero tumbler iff `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.
- *Postconditions:* `t > 0 ∧ (A i : 1 ≤ i ≤ #z : zᵢ = 0) ⟹ z < t` under T1.


## TA7a — Ordinal-only shift arithmetic

The canonical representation for shift arithmetic is the *ordinal-only* formulation: a position in a subspace with identifier `N` and ordinal `o = [o₁, ..., oₘ]` (where `m ≥ 1`) is represented as the tumbler `o` for arithmetic purposes, with `N` held as structural context. Define **S** = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)} — ordinals with all positive components, matching T4's positive-component constraint on element fields. An element-local displacement is a positive tumbler `w` with action point `k` satisfying `1 ≤ k ≤ m`. In this formulation:

  `(A o ∈ S, w > 0 : k ≤ #o ⟹ o ⊕ w ∈ T)`

  `(A o ∈ S, w > 0 : o ≥ w ⟹ o ⊖ w ∈ T)`

In words: when the subspace identifier is held as structural context and arithmetic operates on ordinals alone, both addition and subtraction are closed in T. The subspace identifier is never modified. The result lands in the stronger set S (all-positive components) for addition when the displacement's tail components are positive; subtraction may produce leading zeros when the operands share a leading prefix.

*Dependencies:*
- **TA0 (Well-defined addition):** For `a, w ∈ T` with `w > 0` and action point `k ≤ #a`, `a ⊕ w ∈ T` with `#(a ⊕ w) = #w`. Supplies T-membership and the result-length identity for Conjunct 1.
- **TA2 (Well-defined subtraction):** For `a, w ∈ T` with `a ≥ w`, `a ⊖ w ∈ T` with `#(a ⊖ w) = max(#a, #w)`. Supplies T-membership and the result-length identity for Conjunct 2.
- **TumblerAdd (Constructive definition):** `(a ⊕ w)ᵢ = aᵢ` for `i < k`, `(a ⊕ w)ₖ = aₖ + wₖ`, `(a ⊕ w)ᵢ = wᵢ` for `i > k`, where `k = actionPoint(w)`. Used to determine which components of `o ⊕ w` are positive (S-membership analysis).
- **TumblerSub (Constructive definition):** Zero-pad both operands to length `max(#a, #w)`, find the first divergence `d`; `rᵢ = 0` for `i < d`, `r_d = a_d - w_d`, `rᵢ = aᵢ` for `i > d`. If no divergence, the result is the zero tumbler of length `max(#a, #w)`. Used in the case analysis of S-membership under subtraction.
- **T1 (Lexicographic order):** At the first divergence position `d` with `d ≤ min(#a, #b)`, `a > b` requires `a_d > b_d`. Used to establish `o_d > w_d` in the subtraction case analysis.
- **TA6 (Zero sentinel):** The zero tumbler `[0, ..., 0]` is a member of T. Referenced for the boundary case where subtraction yields a zero tumbler.

*Formal Contract:*
- *Preconditions:* For `⊕`: `o ∈ S`, `w ∈ T`, `w > 0`, `actionPoint(w) ≤ #o`. For `⊖`: `o ∈ S`, `w ∈ T`, `o ≥ w`.
- *Postconditions:* `o ⊕ w ∈ T`. `o ⊖ w ∈ T`. For `⊕`, the result is in S when all tail components of `w` (after the action point) are positive.
- *Frame:* The subspace identifier `N`, held as structural context, is not an operand and is never modified by either operation.
- *Definition:* **S** = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)} — ordinals with all positive components, matching T4's positive-component constraint on element fields.


### What tumbler arithmetic is NOT

We must state explicitly what the tumbler algebra does not guarantee. These negative results constrain what an implementer may assume.

**The algebra is not a group.** There is no additive identity — the zero tumbler is a sentinel, not a neutral element for addition. There is no additive inverse for every element — subtraction is only defined when `a ≥ w`. The algebra is not closed under subtraction in general.

## TA-assoc — Addition is associative where both compositions are defined

`(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)` whenever both sides are well-defined. The domain conditions are asymmetric: the left side requires `k_b ≤ #a`, while the right requires only `min(k_b, k_c) ≤ #a`; but the left-side conditions subsume the right-side conditions, so on the intersection the values agree. A subsidiary identity: `actionPoint(b ⊕ c) = min(k_b, k_c)`.

In words: tumbler addition associates whenever both parenthesizations are defined. The three structural cases (action points ordered as `k_b < k_c`, `k_b = k_c`, `k_b > k_c`) each yield identical component sequences on both sides; in particular, a shallower displacement overwrites a deeper one entirely, making the deeper displacement's contribution invisible in both groupings.

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `b ∈ T`, `c ∈ T`, `b > 0`, `c > 0`, `k_b ≤ #a`, `k_c ≤ #b` (where `k_b = actionPoint(b)`, `k_c = actionPoint(c)`; these left-side conditions subsume the right-side conditions since `k_b ≤ #a` implies `min(k_b, k_c) ≤ #a`)
- *Postconditions:* `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)`; `#((a ⊕ b) ⊕ c) = #(a ⊕ (b ⊕ c)) = #c`; `actionPoint(b ⊕ c) = min(k_b, k_c)`


## TA-LC — LeftCancellation

If `a ⊕ x = a ⊕ y` with both sides well-defined (TA0 satisfied for both), then `x = y`.

In words: tumbler addition is left-cancellative — the starting position can be "divided out" to uniquely recover the displacement. Equal results from the same start imply the displacements are identical; no two distinct displacements can map the same position to the same target.

*Formal Contract:*
- *Preconditions:* `a, x, y ∈ T`; `x > 0`; `y > 0`; `actionPoint(x) ≤ #a`; `actionPoint(y) ≤ #a`; `a ⊕ x = a ⊕ y`
- *Postconditions:* `x = y`


## TA-RC — Right cancellation fails

There exist tumblers `a`, `b`, `w` with `a ≠ b` and `a ⊕ w = b ⊕ w` (both sides well-defined).

In words: right cancellation does not hold — distinct starting positions can produce the same result under the same displacement. TumblerAdd's tail-replacement rule discards all start-position components after the action point, so any two starts that agree up to the action point are indistinguishable in the output regardless of how they differ below it.

*Formal Contract:*
- *Postconditions:* `∃ a, b, w ∈ T : w > 0 ∧ actionPoint(w) ≤ #a ∧ actionPoint(w) ≤ #b ∧ a ≠ b ∧ a ⊕ w = b ⊕ w`


## TA-MTO — ManyToOneEquivalence

For any displacement `w` with action point `k` and any tumblers `a`, `b` with `#a ≥ k` and `#b ≥ k`:

`a ⊕ w = b ⊕ w  ⟺  (∀ i : 1 ≤ i ≤ k : aᵢ = bᵢ)`

In words: two starting positions produce the same result under a displacement if and only if they share the same prefix up to the action point. This is the exact characterisation of when right cancellation fails: positions that agree on the first `k` components are indistinguishable under any displacement with action point `k`, no matter how they differ at deeper levels.

*Formal Contract:*
- *Preconditions:* `w ∈ T`, `w > 0`, `a ∈ T`, `b ∈ T`, `#a ≥ actionPoint(w)`, `#b ≥ actionPoint(w)`
- *Postconditions:* `a ⊕ w = b ⊕ w ⟺ (∀ i : 1 ≤ i ≤ actionPoint(w) : aᵢ = bᵢ)`


## D0 — Displacement well-definedness

Under the conditions `a < b` and `divergence(a, b) ≤ #a`, the displacement `w = b ⊖ a` is a well-defined positive tumbler whose action point equals `divergence(a, b)`, and the addition `a ⊕ w` is well-defined. Pairs where `a` is a proper prefix of `b` are excluded: their divergence point is `#a + 1`, violating `divergence(a, b) ≤ #a`.

In words: the displacement from `a` to `b` exists and is usable as a tumbler-addition argument whenever `a < b` and their first-divergence position falls within `a`'s length. The round-trip `a ⊕ (b ⊖ a)` is defined under these conditions; faithfully recovering `b` additionally requires `#a ≤ #b` (established in D1).

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `b ∈ T`, `a < b`, `divergence(a, b) ≤ #a`
- *Postconditions:* `b ⊖ a ∈ T`, `b ⊖ a > 0`, `actionPoint(b ⊖ a) = divergence(a, b)`, `a ⊕ (b ⊖ a) ∈ T`

## D1 — Displacement round-trip

For tumblers a, b ∈ T with a < b, divergence(a, b) ≤ #a, and #a ≤ #b:

  a ⊕ (b ⊖ a) = b

In words: adding the displacement from a to b back onto a recovers b exactly. The subtraction `⊖` and addition `⊕` form a faithful round-trip: computing the gap between two ordered tumblers and applying it to the source always yields the target.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, a < b, divergence(a, b) ≤ #a, #a ≤ #b
- *Postconditions:* a ⊕ (b ⊖ a) = b


## D2 — Displacement uniqueness

Under D1's preconditions (a < b, divergence(a, b) ≤ #a, #a ≤ #b), if a ⊕ w = b then w = b ⊖ a.

In words: the canonical displacement b ⊖ a is the *only* tumbler that, when added to a, produces b. Together with D1, this characterizes displacement completely — D1 guarantees existence, D2 guarantees uniqueness.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, divergence(a, b) ≤ #a, #a ≤ #b, a ⊕ w = b
- *Postconditions:* w = b ⊖ a


## OrdinalDisplacement — OrdinalDisplacement (DEFINITION, function)

For natural number n ≥ 1 and depth m ≥ 1, the *ordinal displacement* δ(n, m) is the tumbler [0, 0, ..., 0, n] of length m — zero at positions 1 through m − 1, and n at position m. Its action point is m.

When the depth is determined by context (typically m = #v for the tumbler being shifted), we write δₙ.

In words: an ordinal displacement is a tumbler that is zero everywhere except at its deepest position, where it holds a positive value n. It is the canonical "pure advance" displacement — it shifts only the last component without touching any higher-level structure.

*Formal Contract:*
- *Preconditions:* n ≥ 1, m ≥ 1
- *Definition:* δ(n, m) = [0, ..., 0, n] of length m, action point m


## OrdinalShift — OrdinalShift (DEFINITION, function)

For a tumbler v of length m and natural number n ≥ 1:

`shift(v, n) = v ⊕ δ(n, m)`

The component-wise behavior follows directly from TumblerAdd: shift(v, n)ᵢ = vᵢ for i < m, and shift(v, n)ₘ = vₘ + n.

In words: shifting a tumbler by n advances its deepest component by exactly n while leaving all higher-level components unchanged. The result has the same depth as the input, and the deepest component remains positive since vₘ + n ≥ 1 unconditionally for n ≥ 1.

*Formal Contract:*
- *Preconditions:* v ∈ T, n ≥ 1
- *Definition:* shift(v, n) = v ⊕ δ(n, #v)
- *Postconditions:* shift(v, n)ᵢ = vᵢ for i < #v, shift(v, n) at position #v = v at position #v + n, #shift(v, n) = #v, shift(v, n) at position #v ≥ 1


## TS1 — ShiftStrictOrderPreservation

`(A v₁, v₂, n : n ≥ 1 ∧ #v₁ = #v₂ = m ∧ v₁ < v₂ : shift(v₁, n) < shift(v₂, n))`

In words: shifting two equal-depth tumblers by the same positive amount n preserves their strict ordering. Because the shift advances only the deepest component of each operand by the same value, the relative ordering at their divergence point is unaffected.

*Formal Contract:*
- *Preconditions:* v₁ ∈ T, v₂ ∈ T, n ≥ 1, #v₁ = #v₂ = m, v₁ < v₂
- *Postconditions:* shift(v₁, n) < shift(v₂, n)

## TS2 — ShiftInjectivity

`(A v₁, v₂, n : n ≥ 1 ∧ #v₁ = #v₂ = m : shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂)`

In words: ordinal shift is injective over equal-length tumblers. If two tumblers of the same length produce the same result under the same positive shift amount, they must be identical. No two distinct equal-length tumblers can collide under a shift.

*Formal Contract:*
- *Preconditions:* v₁ ∈ T, v₂ ∈ T, n ≥ 1, #v₁ = #v₂ = m
- *Postconditions:* shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂

---

## TS3 — ShiftComposition

`(A v, n₁, n₂ : n₁ ≥ 1 ∧ n₂ ≥ 1 ∧ #v = m : shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂))`

In words: two successive ordinal shifts compose into a single shift whose amount is the sum. Shifting by `n₁` and then by `n₂` is equivalent to shifting once by `n₁ + n₂`. Shift amounts accumulate additively, and the tumbler length is preserved throughout.

*Formal Contract:*
- *Preconditions:* v ∈ T, n₁ ≥ 1, n₂ ≥ 1, #v = m
- *Postconditions:* shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂)
- *Frame:* #shift(shift(v, n₁), n₂) = #v = m (shift preserves tumbler length)

---

## TS4 — ShiftStrictIncrease

`(A v, n : n ≥ 1 ∧ #v = m : shift(v, n) > v)`

In words: shifting a tumbler by any positive ordinal amount strictly advances it. The shifted result is always strictly greater than the original, regardless of the tumbler's contents or length. No positive shift is a no-op.

*Formal Contract:*
- *Preconditions:* v ∈ T, n ≥ 1, #v = m
- *Postconditions:* shift(v, n) > v

---

## TS5 — ShiftMonotonicity

`(A v, n₁, n₂ : n₁ ≥ 1 ∧ n₂ > n₁ ∧ #v = m : shift(v, n₁) < shift(v, n₂))`

In words: shifting by a larger amount produces a strictly greater result. For any fixed tumbler, the shift operation is strictly monotone in its amount: a greater shift amount always yields a greater tumbler. This means the set of shifts of a single tumbler is totally ordered by amount.

*Formal Contract:*
- *Preconditions:* v ∈ T, n₁ ≥ 1, n₂ > n₁, #v = m
- *Postconditions:* shift(v, n₁) < shift(v, n₂)

---

### Increment for allocation

A separate operation, distinct from the shifting arithmetic, handles address allocation. When the system allocates a new address, it takes the highest existing address in a partition and produces the next one. This is not addition of a width; it is advancement of a counter at a specified hierarchical level.

The *last significant position* of a tumbler `t` is defined as:

- When `t` has at least one nonzero component: `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})`
- When every component is zero: `sig(t) = #t`

For valid addresses, `sig(t) = #t`. Therefore `inc(t, 0)` on a valid address increments the last component of the last field, modifying only within that field and preserving the hierarchical structure.
