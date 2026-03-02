# ASN-0001: Tumbler Algebra

*2026-02-23*

We wish to understand what algebraic structure the Xanadu addressing system must possess. The system assigns every piece of content a permanent address — a *tumbler* — and these addresses must support comparison, containment testing, arithmetic for editing operations, and coordination-free allocation across a global network. We seek the minimal set of abstract properties that any correct implementation must provide, deriving each from the design requirements rather than from any particular implementation.

The approach is: state what the system must guarantee, then discover what properties of the address algebra are necessary and sufficient for those guarantees. We begin with the carrier set and work outward.


## The carrier set

A tumbler is a finite sequence of non-negative integers. We write `t = d₁.d₂. ... .dₙ` where each `dᵢ ∈ ℕ` and `n ≥ 1`. The set of all tumblers is **T**. Nelson describes each component as a "digit" with "no upper limit" — the term is misleading, since each "digit" is an arbitrary-precision natural number, not a single decimal digit. The variable-length encoding ("humber") is designed so that small values are compact and large values expand as needed: "very short when a number is small, and as large as it needs to be when the number is big."

This gives us our first property:

**T0 (Unbounded components).** `(A t ∈ T, i : 1 ≤ i ≤ #t : (A M ∈ ℕ :: (E t' ∈ T :: t' agrees with t except t'.dᵢ > M)))`.

In words: for every tumbler and every component position, there exists a tumbler whose value at that position exceeds any given bound. The address space within any subtree is inexhaustible.

T0 is what separates the tumbler design from fixed-width addressing. Nelson conceived the docuverse as "ever-growing": "Our kingdom is already twice the size of Spain, and every day we drift makes it bigger." A fixed-width representation inevitably exhausts; T0 guarantees this cannot happen at the abstract level.

We observe that Gregory's implementation uses a fixed 16-digit mantissa of 32-bit unsigned integers, giving a large but finite representable range. When the allocation primitive `tumblerincrement` would exceed this range, it detects the overflow and terminates fatally. The general addition routine `tumbleradd` silently truncates. Both behaviors violate T0. The abstract specification demands unbounded components; a correct implementation must either provide them or demonstrate that the reachable state space never exercises the bound. Gregory's overflow check in the allocation path is evidence that the implementers were aware of the gap — they chose detection over correctness, halting rather than corrupting.


## The total order

We require a total order on T. Nelson describes the "tumbler line" as "a flat mapping of a particular tree" — the depth-first traversal of the docuverse's containment hierarchy. The tree has servers at the root, accounts under servers, documents under accounts, elements under documents. Depth-first traversal of this tree produces a linear sequence in which every subtree occupies a contiguous interval. The ordering rule is lexicographic:

**T1 (Lexicographic order).** For tumblers `a = a₁. ... .aₘ` and `b = b₁. ... .bₙ`, define `a < b` iff there exists `k ≥ 1` such that `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either:

  (i) `k ≤ min(m, n)` and `aₖ < bₖ`, or

  (ii) `k = m + 1 ≤ n` (that is, `a` is a proper prefix of `b`).

The prefix convention — a prefix is less than any proper extension — is what makes depth-first traversal work. The server address `2` is less than every address within server `2`'s subtree, because every such address extends the prefix `2` with further components. This means server `2`'s subtree begins immediately after `2` in the order and extends until some address whose first component exceeds `2`.

T1 gives a total order: for any `a, b ∈ T`, exactly one of `a < b`, `a = b`, `a > b` holds. This is a standard mathematical fact about lexicographic orderings on well-ordered alphabets — ℕ is well-ordered, so the lexicographic extension to finite sequences is total.

Nelson requires that comparison be self-contained — no index consultation needed: "you always know where you are, and can at once ascertain the home document of any specific word or character." We state:

**T2 (Intrinsic comparison).** The order relation T1 is computable from the two tumblers alone, without consulting any external data structure. The comparison examines at most `min(#a, #b)` component pairs.

The importance of T2 is operational: span containment tests, link search, and the enfilade traversal all reduce to tumbler comparison. If comparison required a lookup, these operations would depend on auxiliary state, and the system's decentralization guarantee would collapse — one could not determine whether an address falls within a span without access to the index that manages that span.


## Canonical form

Equality of tumblers must mean component-wise identity. There must be no representation in which two distinct sequences of components denote the same abstract tumbler:

**T3 (Canonical representation).** `(A a, b ∈ T : a₁ = b₁ ∧ ... ∧ aₙ = bₙ ∧ #a = #b ≡ a = b)`.

If two tumblers have the same length and the same components at every position, they are the same tumbler. Conversely, if they differ in any component or in length, they are distinct. No normalization, no trailing-zero ambiguity, no exponent variation can create aliases.

Gregory's implementation achieves T3 through a normalization routine (`tumblerjustify`) that shifts leading zeros out of the mantissa and adjusts the exponent. After justification, the first mantissa element is nonzero (unless the tumbler is the zero tumbler), creating a unique representation for each value. A validation routine enforces the invariant with checks including `if (ptr->exp && ptr->mantissa[0] == 0) { ... "fucked up non-normalized" }`. The implementers' frustration is palpable; T3 is easy to state and surprisingly difficult to maintain through all arithmetic paths.

T3 matters because address identity is load-bearing. If two representations could denote the same tumbler, then equality tests might give false negatives, span containment checks might fail for addresses that should match, and the permanence guarantee T7 (below) could be silently circumvented — the system might allocate a "new" address that is actually an alias for an existing one.


## Hierarchical structure

Tumblers encode a containment hierarchy. Nelson uses zero-valued components as structural delimiters:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents."

> "A tumbler address may have at most three zero digits... These are interpreted as the major dividers, and have lexical significance as punctuation."

We formalize this. Define a *field separator* as a component with value zero. An I-space tumbler has the form:

`t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`

where each `Nᵢ, Uⱼ, Dₖ, Eₗ > 0`. The four fields are:

- **Node field** `N₁. ... .Nₐ`: identifies the server. Always begins with 1 ("since all other servers are descended from it").
- **User field** `U₁. ... .Uᵦ`: identifies the account.
- **Document field** `D₁. ... .Dᵧ`: identifies the document and version. Nelson notes that the boundary between base document and version within this field is not syntactically marked — "the version, or subdocument number is only an accidental extension of the document number."
- **Element field** `E₁. ... .Eδ`: identifies the content element. The first component distinguishes the *subspace*: 1 for text content, 2 for links.

Not every tumbler need have all four fields. A tumbler with zero zeros addresses a node. One zero: a user account. Two zeros: a document. Three zeros: an element. The count of zero-valued components determines the specificity level.

**T4 (Hierarchical parsing).** Every tumbler `t ∈ T` used as an I-space address contains at most three zero-valued components, appearing in order as field separators, and every non-separator component is strictly positive. Formally, if `t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`, then `(A i : 1 ≤ i ≤ α : Nᵢ > 0)`, `(A j : 1 ≤ j ≤ β : Uⱼ > 0)`, `(A k : 1 ≤ k ≤ γ : Dₖ > 0)`, `(A l : 1 ≤ l ≤ δ : Eₗ > 0)`. We call this the *positive-component constraint*: every component of every field is strictly positive. The function `fields(t)` that extracts the node, user, document, and element fields is well-defined and computable from `t` alone. Define `zeros(t) = #\{i : 1 ≤ i ≤ #t ∧ tᵢ = 0\}`. The count of zero-valued components uniquely determines the hierarchical level:

  - `zeros(t) = 0`: `t` is a node address (node field only),
  - `zeros(t) = 1`: `t` is a user address (node and user fields),
  - `zeros(t) = 2`: `t` is a document address (node, user, and document fields),
  - `zeros(t) = 3`: `t` is an element address (all four fields).

This correspondence is injective on levels: each level produces addresses with exactly one zero count, and each zero count corresponds to exactly one level. The correspondence depends on the positive-component constraint — zero components serve exclusively as field separators *because* no field component is zero. Without the positivity constraint, a tumbler like `[1, 0, 0, 3]` would have two zero-valued components but ambiguous parse: the second zero could be a separator or a zero-valued component within the user field. Since field components are strictly positive, zeros appear only as separators, the number of separators determines the number of fields, and the parse is unique.

T4, combined with the total order T1, gives us the property that makes spans work:

**T5 (Contiguous subtrees).** For any tumbler prefix `p`, the set `{t ∈ T : p ≼ t}` (where `≼` denotes "is a prefix of") forms a contiguous interval under T1:

  `[p ≼ a ∧ p ≼ c ∧ a ≤ b ≤ c ⟹ p ≼ b]`

*Proof.* From T1, if `p ≼ a` then `a` agrees with `p` on the first `#p` components. If `a ≤ b ≤ c` and both `a` and `c` share prefix `p`, then `b` must also share prefix `p`. We consider two cases.

*Case 1: `#b ≥ #p`.* If `b` diverged from `p` at some position `k ≤ #p`, then either `bₖ < pₖ` (contradicting `a ≤ b` since `aₖ = pₖ`) or `bₖ > pₖ` (contradicting `b ≤ c` since `cₖ = pₖ`). So `b` agrees with `p` on all `#p` positions, hence `p ≼ b`.

*Case 2: `#b < #p`.* Since `p ≼ a`, we have `#a ≥ #p > #b`, so `b` is shorter than `a`. By T1, `a ≤ b` requires a first divergence point `j ≤ #b` where `aⱼ < bⱼ` (since `a` cannot be a prefix of the shorter `b`). But `aⱼ = pⱼ` (because `j ≤ #b < #p` and `a` shares prefix `p`), so `bⱼ > pⱼ = cⱼ`. This contradicts `b ≤ c`, since `b` exceeds `c` at position `j` and they agree on all prior positions. ∎

This is Nelson's key insight: "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." T5 is what makes this true. A span between two endpoints under the same prefix captures exactly the addresses under that prefix between those endpoints — no addresses from unrelated subtrees can interleave.


## Decidable containment

The total order T1 determines *sequence* (which address comes first). But the system also needs *containment* — does address `a` belong to account `b`? Is document `d₁` under the same server as document `d₂`? These are not ordering questions; they are prefix questions.

**Corollary T6 (Decidable containment).** For any two tumblers `a, b ∈ T`, the following are decidable from the addresses alone:

  (a) Whether `a` and `b` share the same node field.

  (b) Whether `a` and `b` share the same node and user fields.

  (c) Whether `a` and `b` share the same node, user, and document-lineage fields.

  (d) Whether the document field of `a` is a prefix of the document field of `b` (structural subordination within a document family).

T6 is a corollary: it follows immediately from T4 — we extract the relevant fields and compare. We state it separately because the decidability claim is load-bearing for decentralized operation, but it introduces no independent content beyond T4. But we must note what T6(d) does NOT capture. The document field records the *allocation hierarchy* — who baptised which sub-number — not the *derivation history*. Version `5.3` was allocated under document `5`, but this tells us nothing about which version's content was copied to create `5.3`. Nelson is candid: "the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." Formal version-derivation requires the version graph, not just the address.

Gregory's implementation confirms the distinction between ordering and containment. The codebase provides both `tumblercmp` (total order comparison, used for sorting and interval queries) and `tumbleraccounteq` (prefix-matching predicate, used for containment). The latter truncates the candidate to the length of the parent and checks for exact match — this is the operational realization of T6, and it is a genuinely different algorithm from the ordering comparison. An implementation that tried to derive containment from the total order alone would fail: `tumblercmp(1.1.0.2, 1.1.0.2.0.5) = LESS` and `tumblercmp(1.1.0.2, 1.1.0.3.0.1) = LESS`, but only the first represents a parent-child relationship.


## Subspace disjointness

Within a document's element space, the first component after the third zero delimiter identifies the *subspace*: 1 for text, 2 for links. Nelson also mentions that the link subspace "could be further subdivided" by additional components after `2`. The critical property is permanent separation:

**Corollary T7 (Subspace disjointness).** The subspace identifier (the first component of the element field) permanently separates the address space into disjoint regions. No tumbler in subspace `s₁` can equal or be confused with a tumbler in subspace `s₂ ≠ s₁`.

  `(A a, b ∈ T : a.E₁ ≠ b.E₁ ⟹ a ≠ b)`

T7 is a corollary of T3 (canonical representation) and T4 (hierarchical parsing): if two tumblers differ in their first element-field component, they are distinct. We state it explicitly because it is load-bearing for editorial operations, but it introduces no independent content. INSERT shifts text positions forward, and the system must guarantee that no link position is affected. T7 is the structural basis for that guarantee — shifts within subspace 1 cannot produce addresses in subspace 2, because the subspace identifier is part of the address, not metadata.

The ordering T1 places all text addresses (subspace 1) before all link addresses (subspace 2) within the same document, because `1 < 2` at the subspace position. This is a consequence, not an assumption — it falls out of the lexicographic order.


## Permanence

The most consequential property of the tumbler algebra is that the mapping from addresses to content is write-once:

**T8 (Address permanence).** If tumbler `a ∈ T` is assigned to content `c` at any point in the system's history, then for all subsequent states, `a` remains assigned to `c`. No operation removes an address from I-space. No operation changes the content at an assigned address.

Nelson: "any address of any document in an ever-growing network may be specified by a permanent tumbler address." And: "those bytes remain in all other documents where they have been included." T8 is what makes links stable — links reference I-space tumblers, and because those tumblers are permanent, links survive all editing. It is what makes transclusion meaningful — transcluded content maintains its identity because its address never changes. It is what makes royalty accounting possible — the address encodes the originating server, user, and document, and this attribution can never be revised.


## Monotonic allocation

T8 tells us that addresses, once assigned, are permanent. We now ask: in what order are new addresses assigned?

**T9 (Forward allocation).** Each allocator in the system controls a single ownership prefix and allocates sequentially within it. Within that sequential stream, new addresses are strictly monotonically increasing:

  `(A a, b : same_allocator(a, b) ∧ allocated_before(a, b) : a < b)`

Nelson's design is explicitly chronological: "suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." And the forking mechanism is sequential: "successive new digits to the right ... 2.1, 2.2, 2.3, 2.4 are successive items being placed under 2." The word "successive" carries the weight: 2.2 follows 2.1, never precedes it.

T9 prohibits gap-filling. If address 2.3 was allocated and address 2.5 was allocated, then 2.4 either was allocated between them or is a permanent ghost. The system never goes back to fill 2.4 after allocating 2.5. To reuse a gap would violate T9 (the allocation counter would retreat).

Even addresses that have no stored content are irrevocably claimed. Nelson calls these "ghost elements": "the docuverse is the occupied tumbler-space — as occupied by conceptually assigned positions, even if nothing represents them in storage." A ghost element is by definition *unassigned* — no content `c` satisfies T8's precondition for it. Ghost permanence is therefore not a consequence of T8 (which governs assigned addresses) but of T9: the allocator has advanced past the ghost address and will never return to it. Since T9 requires strictly monotonic advancement, the ghost address lies behind the allocation frontier permanently. It cannot be reused for new content; it is a permanent gap. Gaps are features, not defects.

We observe that T9 is scoped to a *single allocator's sequential stream*, not to arbitrary partitions. A server-level subtree spans multiple independent allocators (one per user). Those allocators operate concurrently — T10 below guarantees they need no coordination. If user A (prefix `1.0.1`) allocates at wall-clock time `t₂` and user B (prefix `1.0.2`) allocates at time `t₁ < t₂`, neither T9 nor any other property requires that A's address exceed B's. T9 applies within each user's allocation stream independently.

We first establish a lemma that converts ordering of prefixes into ordering of all addresses under those prefixes.

**Lemma (Prefix ordering extension).** Let `p₁, p₂ ∈ T` be tumblers such that `p₁ < p₂` and neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for every `a` extending `p₁` (`p₁ ≼ a`) and every `b` extending `p₂` (`p₂ ≼ b`), `a < b`.

*Proof.* Since `p₁ < p₂` and neither is a prefix of the other, T1 case (i) applies: there exists a position `k ≤ min(#p₁, #p₂)` such that `p₁` and `p₂` agree on positions `1, ..., k-1` and `p₁ₖ < p₂ₖ`. (Case (ii) is excluded because `p₁` is not a proper prefix of `p₂`.) Now `a` extends `p₁`, so `aᵢ = p₁ᵢ` for all `i ≤ #p₁`; in particular `aₖ = p₁ₖ`. Similarly `bₖ = p₂ₖ`. On positions `1, ..., k-1`, `aᵢ = p₁ᵢ = p₂ᵢ = bᵢ`. At position `k`, `aₖ = p₁ₖ < p₂ₖ = bₖ`. So `a < b` by T1 case (i). ∎

**Theorem (Partition monotonicity).** Within any prefix-delimited partition of the address space, the set of allocated addresses is totally ordered by T1, and this order is consistent with the allocation order of any single allocator within that partition.

*Proof.* Consider a partition with prefix `p`. Every allocated address in this partition has prefix `p`, hence lies in the contiguous interval guaranteed by T5. Within the partition, addresses belong to sub-partitions owned by distinct allocators. These sub-partitions have prefixes that are siblings — they share the parent prefix `p` but diverge at the component that distinguishes one allocator from another.

We claim that sibling prefixes are non-nesting: they have the same length and diverge at the sibling-distinguishing component, so neither can be a prefix of the other. To see this, observe that the first sub-partition prefix `t₀` is produced by `inc(parent, k)` with `k > 0` — a deep increment from the parent's address, giving `#t₀ = #parent + k` (by TA5(d)). By T10a, subsequent sibling prefixes are produced by `inc(·, 0)` — shallow increment: `t₁ = inc(t₀, 0)`, `t₂ = inc(t₁, 0)`, and so on. By TA5(c), `inc(t, 0)` preserves the length of `t`: `#inc(t, 0) = #t`. So all sibling prefixes `t₀, t₁, t₂, ...` have the same length `#t₀`. Two tumblers of the same length cannot stand in a prefix relationship unless they are equal (a proper prefix is strictly shorter). Since they differ at position `sig(t)` (TA5(c) increments that component), they are unequal, hence non-nesting. Their prefixes are therefore disjoint under T10.

Each allocator's output is monotonic (T9). The sub-partitions are ordered by their prefixes under T1 — a server allocating user prefixes does so monotonically (T9 applied to the server's own allocation stream), so if sub-partition prefix `p₁` was allocated before `p₂`, then `p₁ < p₂`. Since sibling prefixes are non-nesting and `p₁ < p₂`, the prefix ordering extension lemma gives `a < b` for every address `a` under `p₁` and every address `b` under `p₂`. Within each sub-partition, allocation order matches address order by T9. ∎

The theorem recovers the intuition that "later addresses are larger" at every level of the hierarchy, but it does so as a *consequence* of per-allocator monotonicity (T9), prefix disjointness (T10), and the prefix ordering (T1) — not as a universal axiom that would require coordinating concurrent allocators.

Gregory confirms: I-address allocation uses `tumblerincrement` with `rightshift=0`, producing sequences like `...3.0.1.3.1`, `...3.0.1.3.2`, `...3.0.1.3.3` — strictly increasing, never retreating. The overflow check in `tumblerincrement` (fatal error when `idx + rightshift >= NPLACES`) is the point at which the implementation admits it cannot satisfy T9 for arbitrarily large addresses. The abstract specification demands T9 unconditionally; the implementation approximates it within its representable range and fails loudly at the boundary.

A consequence of T8 and T9 together is that I-space is a *growing set* in the lattice-theoretic sense: the set of allocated addresses can only increase, and new elements always appear at the frontier of each allocator's domain.


## Coordination-free uniqueness

The tumbler hierarchy exists so that independent actors can allocate addresses without communicating:

**T10 (Partition independence).** The address space is partitioned by prefix into ownership domains. Two allocators with distinct, non-nesting prefixes can allocate simultaneously, and the resulting addresses are guaranteed distinct.

Formally: let `p₁` and `p₂` be prefixes such that neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for any tumbler `a` with prefix `p₁` and any tumbler `b` with prefix `p₂`, `a ≠ b`.

This follows from the definition: if `a` has prefix `p₁` and `b` has prefix `p₂`, and the prefixes diverge at some position `k` with `p₁ₖ ≠ p₂ₖ`, then `aₖ = p₁ₖ ≠ p₂ₖ = bₖ`, so `a ≠ b`. The proof is elementary, but the property is architecturally profound. Nelson: "The owner of a given item controls the allocation of the numbers under it." No central allocator is needed. No coordination protocol is needed. The address structure itself makes collision impossible.

**T10a (Allocator discipline).** Each allocator produces its sibling outputs exclusively by repeated application of `inc(·, 0)` — shallow increment at the last significant position. To spawn a child allocator, the parent performs one `inc(·, k')` with `k' > 0` to establish the child's prefix, then delegates further allocation to the child. The parent's own sibling stream resumes with `inc(·, 0)`.

T10a constrains what would otherwise be an unregulated choice. Without it, an allocator could intermix shallow and deep increments — producing `inc(t₀, 0)` then `inc(t₁, 2)` then `inc(t₂, 0)` — generating outputs of varying lengths. The constraint to `k = 0` for siblings is essential: since `inc(·, 0)` preserves length (TA5(c)), all sibling outputs from a single allocator have the same length. This uniform-length property is what the partition monotonicity and global uniqueness proofs depend on. If an allocator used `k > 0` for siblings, successive outputs would have lengths `L, L + k, L + 2k, ...` (by TA5(d)), and each output would extend the previous — `t` would be a proper prefix of `inc(t, k)` — making successive siblings nest rather than stand disjoint. This nesting would break the non-nesting premise required by the Prefix Ordering Extension lemma.

The `k > 0` operation is reserved exclusively for child-spawning: a single deep increment that establishes a new prefix at a deeper level, from which a new allocator continues with its own `inc(·, 0)` stream.

Gregory's implementation confirms this discipline: element allocation within a document uses `tumblerincrement` with `rightshift=0` (shallow, sibling). Sub-document creation uses `rightshift=1` (deep, child-spawning). The `rightshift` is determined by the allocation context, not chosen per-allocation.

From T9, T10, and T10a together:

**Theorem (Global uniqueness).** No two distinct allocations, anywhere in the system, at any time, produce the same address.

*Proof.* Consider allocations producing addresses `a` and `b` by distinct allocation events. Four cases arise.

*Case 1: Same allocator.* Both addresses are produced by the same allocator's sequential stream. T9 guarantees `a ≠ b` because allocation is strictly monotonic.

*Case 2: Different allocators at the same hierarchical level.* The allocators have prefixes `p₁` and `p₂` that are siblings — neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). T10 gives `a ≠ b` directly.

*Case 3: Different allocators with nesting prefixes and different zero counts.* One allocator's prefix nests within another's — say a node allocator (prefix `[1]`) and one of its users' element allocator (prefix `[1, 0, 3, 0, 2]`). T10 does not apply because the prefixes nest. But these allocators produce addresses with different zero counts: the node allocator produces addresses with `zeros = 1` (user-level), while the element allocator produces addresses with `zeros = 3` (element-level). By T4, different zero counts imply different field structure. We show `a ≠ b` in two sub-cases.

If `#a ≠ #b`, then `a ≠ b` by T3 directly — tumblers of different lengths are distinct.

If `#a = #b`, then `zeros(a) ≠ zeros(b)` means the two tumblers have different numbers of zero-valued components despite having the same length. Suppose for contradiction that `aᵢ = bᵢ` for all `1 ≤ i ≤ #a`. Then the set `{i : aᵢ = 0}` equals the set `{i : bᵢ = 0}`, giving `zeros(a) = zeros(b)` — contradicting our premise. So there exists some position `j` where `aⱼ ≠ bⱼ`. By T3, `a ≠ b`.

*Case 4: Different allocators with nesting prefixes and the same zero count.* This arises when a parent and child allocator both produce addresses at the same hierarchical level. The key example: a user allocator producing top-level documents (document field `[D]`, a single component) and a version allocator producing versions under document 2 (document field `[2, V]`, two components). Both outputs have `zeros = 2`. Their ownership prefixes nest — the user's prefix `1.0.3.0` is a prefix of the version allocator's prefix `1.0.3.0.2`. T10 does not apply.

However, the two allocators produce outputs of different lengths, and T10a is the property that guarantees this. By T10a, the parent allocator uses `inc(·, 0)` for all its sibling allocations. Its first output has some length `γ₁`; since `inc(·, 0)` preserves length (TA5(c)), all subsequent parent siblings have the same length `γ₁`. The child allocator's prefix was established by a single `inc(parent_output, k')` with `k' > 0`, giving prefix length `γ₁ + k'` (by TA5(d)). The child allocator then uses `inc(·, 0)` for its own siblings (by T10a again); its sibling outputs all have the uniform length `γ₁ + k'`.

Since `k' ≥ 1`, the child's outputs have length strictly greater than the parent's: `γ₁ + k' > γ₁`. (The node, user, and element fields are determined by the zero count, which is the same for both, so the length difference resides entirely in the document field.) Since `#a ≠ #b` (different total tumbler lengths), T3 gives `a ≠ b`.

The argument depends critically on T10a's constraint that sibling allocations use `k = 0`. If a parent allocator could use `k > 0` for siblings, its outputs would have lengths `γ₁, γ₁ + k, γ₁ + 2k, ...`, and some parent output could match the length of a child output, collapsing the length separation. ∎

This theorem is the foundation of the entire addressing architecture. Every subsequent guarantee — link stability, transclusion identity, royalty tracing — depends on the uniqueness of addresses. And uniqueness is achieved without any distributed consensus, simply by the structure of the names.


## Tumbler arithmetic

We now turn to the arithmetic operations. The system's editing model requires shifting V-space positions forward on INSERT and backward on DELETE. These shifts are performed by tumbler addition and subtraction. We are careful to note that these operations apply to **V-space positions** — the mutable arrangement layer — not to I-space addresses, which are permanent by T8.

V-space positions are themselves tumblers, but they encode "where this byte appears in the document right now," and that changes with every edit. I-space addresses encode "which byte this is, forever."

### Addition for shifting

Let `⊕` denote tumbler addition, used to shift V-positions forward after insertion.

We require a notion of where a displacement "acts." For a positive displacement `w = [w₁, w₂, ..., wₙ]`, define the *action point* as `k = min({i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0})` — the position of the first nonzero component. The leading zeros say "stay at these hierarchical levels"; the first nonzero component says "advance here."

**TA0 (Well-defined addition).** For tumblers `a, w ∈ T` where `w > 0` and the action point `k` of `w` satisfies `k ≤ #a`, the result `a ⊕ w` is a well-defined tumbler in `T`.

The precondition `k ≤ #a` is essential: the constructive definition copies components `a₁, ..., aₖ₋₁` from the start position and adds `wₖ` to `aₖ`, so position `k` must exist within `a`. A displacement whose action point exceeds `#a` — one with more leading zeros than `a` has components — would attempt to "stay at" hierarchical levels that the start position does not have, and the operation is undefined. For example, `[1] ⊕ [0, 0, 3]` has action point 3 but `#[1] = 1`; the displacement tries to preserve two levels of structure that the start does not possess.

**TA1 (Order preservation under addition).** `(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) : a ⊕ w ≤ b ⊕ w)`, where `k` is the action point of `w`.

TA1 guarantees weak (`≤`) order preservation universally — if two positions were in reading order before shifting, they remain in non-reversed order after shifting. The weak form suffices for INSERT correctness: positions never become *reversed* by the shift, so the reading order of content within a document is preserved. (The precondition `k ≤ min(#a, #b)` inherits from TA0: both `a ⊕ w` and `b ⊕ w` must be well-defined.)

Strict order preservation holds under a tighter condition:

**TA1-strict (Strict order preservation).** `(A a, b, w : a < b ∧ w > 0 ∧ k ≥ divergence(a, b) : a ⊕ w < b ⊕ w)`, where `k` is the action point of `w` and `divergence(a, b)` is the first position at which `a` and `b` differ.

When the action point falls before the divergence — `k < divergence(a, b)` — both operands agree at position `k`, both get the same `wₖ` added, and both copy the same tail from `w` afterward. The original divergence is erased and the results are equal. For example, `a = [1, 3]`, `b = [1, 5]` (diverge at position 2), `w = [2]` (action point at position 1): `a ⊕ w = [3] = b ⊕ w`. Order degrades to equality, never reversal. Editing operations satisfy TA1-strict because element-level shifts have their action point at the element level, which is where all V-positions within a subspace diverge.

But TA1 alone does not guarantee that addition *advances* a position. It preserves relative order between two positions but is silent about the relationship between `a` and `a ⊕ w`. We need:

**TA-strict (Strict increase).** `(A a ∈ T, w > 0 : a ⊕ w > a)` (where `a ⊕ w` is well-defined, i.e., `k ≤ #a` per TA0).

Without TA-strict, the axioms admit a degenerate model in which `a ⊕ w = a` for all `a, w`. This no-op model satisfies TA0 (result is in T), TA1 (if `a < b` then `a < b` — the consequent is unchanged), and TA4 (`(a ⊕ w) ⊖ w = a ⊖ w = a` if subtraction is equally degenerate). Every axiom is satisfied, yet spans are empty — the interval `[s, s ⊕ ℓ)` collapses to `[s, s)`. TA-strict excludes this model and ensures that adding a positive displacement moves the position forward. T12 (span well-definedness) depends on this directly.

**Verification of TA-strict.** Let `k` be the action point of `w`. By the constructive definition, `(a ⊕ w)ᵢ = aᵢ` for `i < k`, and `(a ⊕ w)ₖ = aₖ + wₖ`. Since `k` is the action point, `wₖ > 0`, so `aₖ + wₖ > aₖ`. Positions `1` through `k - 1` agree; position `k` is strictly larger. By T1 case (i), `a ⊕ w > a`.

### Subtraction for shifting

Let `⊖` denote tumbler subtraction, used to shift V-positions backward after deletion:

**TA2 (Well-defined subtraction).** For tumblers `a, w ∈ T` where `a ≥ w`, `a ⊖ w` is a well-defined tumbler in `T`.

**TA3 (Order preservation under subtraction).** `(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w < b ⊖ w)`.

### Inverse

**TA4 (Inverse).** `(A a, w : w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊕ w) ⊖ w = a)`, where `k` is the action point of `w`.

The precondition has three parts. First, `k = #a` — the action point falls at the last component of `a`. This is necessary because addition replaces `a`'s trailing structure below the action point with `w`'s trailing structure (tail replacement). When `k < #a`, components `aₖ₊₁, ..., a_{#a}` are discarded by addition and cannot be recovered by subtraction. Concretely: `[1, 5] ⊕ [1, 3] = [2, 3]` (action point 1, position 2 replaced by `w`'s trailing `3`), then `[2, 3] ⊖ [1, 3] = [1, 3] ≠ [1, 5]` — the original trailing `5` is lost.

Second, `#w = k` — the displacement has no trailing components beyond the action point. This is necessary because addition copies trailing components from `w` (positions `k + 1, ..., #w`), and subtraction copies the tail from the minuend. When `#w > k`, the result `r = a ⊕ w` acquires trailing components `wₖ₊₁, ...` that were not present in `a`. Subtraction preserves these: `r ⊖ w` has positions `i > k` copied from `r`, giving `wₖ₊₁, ...`, so the result is longer than `a`. Concretely: `a = [0, 5]`, `w = [0, 3, 7]`, `k = 2 = #a`. Then `a ⊕ w = [0, 8, 7]`. Now `[0, 8, 7] ⊖ [0, 3, 7]`: divergence at position 2, result `[0, 5, 7] ≠ [0, 5] = a`. The trailing `7` from `w` persists.

Third, `(A i : 1 ≤ i < k : aᵢ = 0)` — all components of `a` before the action point are zero. This is necessary because the subtraction `⊖` discovers its action point from the first divergence between the result and `w`. If `a` has a nonzero component at some position `j < k`, then the result `r = a ⊕ w` has `rⱼ = aⱼ ≠ 0 = wⱼ`, and the subtraction's divergence falls at position `j`, not at `k` where the addition acted. The subtraction then produces the wrong recovery. Concretely: let `a = [5, 3]`, `w = [0, 7]`, so `k = 2 = #a` and `a ⊕ w = [5, 10]`. Now `[5, 10] ⊖ [0, 7]`: the first divergence is at position 1 (`5 ≠ 0`), producing `[5 - 0, 10] = [5, 10] ≠ [5, 3]`. The subtraction never reaches position `k` to undo the addition.

When all three conditions hold — `k = #a`, `#w = k`, and all preceding components of `a` are zero — the subtraction's first divergence is at position `k` (where `rₖ = aₖ + wₖ > wₖ`), there are no trailing components from `w` to corrupt the result, and recovery is exact.

TA4 ensures that INSERT followed by DELETE at the same point restores the original V-positions. Without it, the system could accumulate drift — repeated insert-delete cycles shifting content progressively. All three preconditions are satisfied by editing operations: within a subspace, the editing shift operates on the ordinal component alone — a single-component value `[x]` shifted by a single-component displacement `[n]` with `k = 1 = #w = #a`, where the zero-prefix condition is vacuously true (there are no positions before `k = 1`) and the length condition `#w = k` holds trivially. The subspace identifier is context — it selects which crums are subject to the shift — not an operand to the arithmetic.

The reverse direction is equally necessary — DELETE followed by INSERT at the same point must also restore positions:

**Corollary (Reverse inverse).** `(A a, w : a ≥ w ∧ w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊖ w) ⊕ w = a)`, where `k` is the action point of `w`. The precondition inherits from TA4 — the same restriction (action point at last component, no trailing structure in `w`, zero prefix) that makes the forward inverse exact is required for the reverse.

*Proof.* Let `y = a ⊖ w`. We verify the prerequisites for applying TA4 to `y`.

First, `y ⊕ w` must be well-defined: TA0 requires `k ≤ #y`. The subtraction algorithm produces `y` with: positions before `dₐ = divergence(a, w)` set to zero, position `dₐ` set to `a_{dₐ} - w_{dₐ}`, and positions after `dₐ` copied from `a`. Under our precondition `(A i : 1 ≤ i < k : aᵢ = 0)`, we have `aᵢ = wᵢ = 0` for all `i < k`, so `dₐ = k` (the first divergence is at position `k`). The result `y` has: positions `i < k` zero, position `k` equal to `aₖ - wₖ`, and positions `i > k` copied from `a`. Since `k = #a` and `a` has no components beyond `k`, the result is `y = [0, ..., 0, aₖ - wₖ]` with `#y = k`. So `k ≤ #y` holds.

Second, TA4 requires `k = #y`, `#w = k`, and `(A i : 1 ≤ i < k : yᵢ = 0)`. We have `#y = k` (from above), `#w = k` (by hypothesis), and `yᵢ = 0` for all `i < k` (the subtraction zeroed these positions). All three conditions hold.

By TA4, `(y ⊕ w) ⊖ w = y`. Suppose `y ⊕ w ≠ a`. If `y ⊕ w > a`, then applying `⊖ w` to both sides (order-preserving by TA3 — verified above — with preconditions `a < y ⊕ w`, `a ≥ w` by hypothesis, and `y ⊕ w ≥ w` since `(y ⊕ w) ⊖ w = y` is well-defined) gives `a ⊖ w < (y ⊕ w) ⊖ w = y`, i.e., `y > a ⊖ w = y`, a contradiction. If `y ⊕ w < a`, then TA3 with preconditions `y ⊕ w < a`, `y ⊕ w ≥ w`, and `a ≥ w` gives `(y ⊕ w) ⊖ w < a ⊖ w`, i.e., `y < y`, a contradiction. So `(a ⊖ w) ⊕ w = a`. ∎


### Constructive definition of ⊕ and ⊖

The axiomatic properties above state what `⊕` and `⊖` must satisfy. We now give a constructive definition that shows how they work. Tumbler addition is not arithmetic addition — it is a **position-advance operation**: given a start position `a` and a displacement `w`, compute where you land. The displacement encodes both the distance and the hierarchical level at which the advance occurs.

A displacement `w` is a tumbler whose leading zeros say "stay at these hierarchical levels" and whose first nonzero component says "advance here." Components after the advance point describe the structure of the landing position within the target region.

```
START:  1.0.3.0.2.0.1.777
  DIF:  0.0.0.0.0.0.0.300
        ──────────────────
AFTER:  1.0.3.0.2.0.1.1077
```

Reading the displacement `[0,0,0,0,0,0,0,300]`: seven leading zeros mean "same server, same account, same document, same subspace." Component 8 is 300: "advance 300 elements." No trailing components: the landing position has no further sub-structure.

A displacement that acts at a higher level:

```
START:  1.0.3.0.2.0.1.777
  DIF:  0.0.0.0.3.0.1.1
        ──────────────────
AFTER:  1.0.3.0.5.0.1.1
```

Reading `[0,0,0,0,3,0,1,1]`: four leading zeros mean "same server, same account." Component 5 is 3: "advance 3 documents." Trailing `[0,1,1]`: "land at element 1.1 in the target document." The start position's element field `[1,777]` is replaced by the displacement's trailing structure `[1,1]`.

**Definition (Tumbler addition).** Let `a = [a₁, ..., aₘ]` and `w = [w₁, ..., wₙ]` with `w > 0`. With action point `k`:

```
         ⎧ aᵢ           if i < k        (copy from start)
rᵢ   =  ⎨ aₖ + wₖ      if i = k        (single-component advance)
         ⎩ wᵢ           if i > k        (copy from displacement)
```

The result `a ⊕ w = [r₁, ..., rₚ]` has length `p = max(k - 1, 0) + (n - k + 1)`.

**Precondition:** `k ≤ m` — the displacement's action point must fall within the start position's length. If `w` has more leading zeros than `a` has components, the advance tries to "stay at" hierarchical levels that the start doesn't have, and the operation is undefined.

Three properties of this definition require explicit statement:

**No carry propagation.** The sum `aₖ + wₖ` at the action point is a single natural-number addition. If the result exceeds any representation limit, the abstract model produces the large value directly; the implementation detects overflow. There is no carry into position `k - 1`. This is why the operation is fast — constant time regardless of tumbler length.

**Tail replacement, not tail addition.** Components after the action point come entirely from `w`. The start position's components at positions `k + 1, ..., m` are discarded. `a ⊕ w` does not add corresponding components pairwise — it replaces the start's sub-structure with the displacement's sub-structure below the action point.

**The many-to-one property.** Because trailing components of `a` are discarded, distinct start positions can produce the same result:

```
[1, 1] ⊕ [0, 2]       = [1, 3]
[1, 1, 5] ⊕ [0, 2]    = [1, 3]
[1, 1, 999] ⊕ [0, 2]  = [1, 3]
```

This is correct and intentional: advancing to "the beginning of the next chapter" lands at the same place regardless of where you were within the current chapter. Nelson describes this as "a range of addends gives the same answer."

**Definition (Tumbler subtraction).** The inverse operation. Given an end position `a` and displacement `w`, recover the start position. When the operands have different lengths, we conceptually zero-pad the shorter to the length of the longer before scanning for divergence — this mirrors Gregory's `strongsub`, which operates on fixed-length mantissa arrays with implicit zero-padding. When `a = w` (no divergence exists after padding), the result is the zero tumbler of length `max(#a, #w)`: `a ⊖ w = [0, ..., 0]`. Otherwise, let `k` be the first position where `a` and `w` differ (treating missing components as zero):

```
         ⎧ 0             if i < k        (these levels matched — zero them)
rᵢ   =  ⎨ aₖ - wₖ      if i = k        (reverse the advance)
         ⎩ aᵢ           if i > k        (copy from end position)
```

The result has length `max(#a, #w)` — positions beyond the shorter operand's length are treated as zero during the scan and copied from the longer operand in the tail. For example, `a = [1, 0, 3, 0]` and `w = [1, 0, 3]`: zero-padding `w` to length 4 gives `[1, 0, 3, 0]`, which agrees with `a` at every position, so the result is `[0, 0, 0, 0]`. And `a = [1, 0, 3, 5]` with `w = [1, 0, 3]`: padded `w` is `[1, 0, 3, 0]`, divergence at position 4, result `[0, 0, 0, 5]`.

**Precondition:** `a ≥ w` — when `a ≠ w`, at the divergence point (after zero-padding) `aₖ ≥ wₖ`.

Gregory's implementation confirms this structure. The `strongsub` routine scans for the first position where the mantissa digits differ (`for (i = 0; aptr->mantissa[i] == bptr->mantissa[i]; ++i)`), subtracts at that position, then copies the remainder from the first operand — exactly the algorithm above.

**Verification of TA4 (mutual inverse).** We verify `(a ⊕ w) ⊖ w = a` under the full precondition: `k = #a`, `#w = k`, and `(A i : 1 ≤ i < k : aᵢ = 0)`. Let `k` be the action point of `w`. Since `k = #a`, the addition `a ⊕ w` produces a result `r` with: `rᵢ = aᵢ = 0` for `i < k` (by the zero-prefix condition), `rₖ = aₖ + wₖ`, and `rᵢ = wᵢ` for `i > k`. Crucially, there are no components of `a` beyond position `k` — the tail replacement discards nothing.

Now subtract `w` from `r`. The subtraction scans for the first divergence between `r` and `w`. For `i < k`: `rᵢ = aᵢ = 0 = wᵢ` (both are zero — `aᵢ` by the zero-prefix precondition, `wᵢ` by definition of action point). So the subtraction finds no divergence before position `k`. At position `k`: `rₖ = aₖ + wₖ` and `wₖ > 0`. Since `aₖ > 0` (by T4's positive-component constraint for valid addresses, or by the precondition `w > 0` when `k = 1 = #a`), we have `rₖ = aₖ + wₖ > wₖ`, and the first divergence is at position `k`.

The subtraction produces: positions `i < k` get zero (matching the agreed-upon prefix), position `k` gets `rₖ - wₖ = aₖ + wₖ - wₖ = aₖ`, and positions `i > k` copy from `r`, giving `rᵢ = wᵢ`. Since `k = #a`, the original `a = [0, ..., 0, aₖ]` has no components beyond `k`. For single-component displacements (`#w = k`), there are no trailing components from `w` either, and the result is `[0, ..., 0, aₖ] = a`. TA4 holds exactly.

For multi-component displacements (`#w > k`), the subtraction result has extra trailing components `wₖ₊₁, ...` from `w` beyond position `k`. These are not present in the original `a`. The inverse holds exactly only when `#w = k` (no trailing structure to append). The clean case — and the one editing operations use — is single-component displacements at the element level, where `#w = 1 = k = #a` and the zero-prefix condition is vacuously satisfied (no positions before `k = 1`).

We observe that the previous version of this verification attempted to handle the case where `aᵢ ≠ 0` for some `i < k`. That case is now excluded by the strengthened precondition. The exclusion is correct: when `a` has nonzero components before the action point, the subtraction's divergence falls at one of those positions rather than at `k`, and the recovery fails. The zero-prefix condition ensures that the subtraction's divergence-discovery mechanism finds the action point at exactly the right position.

### Verification of TA1 and TA1-strict

The constructive definition makes the domain of validity precise. We verify both the weak and strict forms.

**Claim (TA1, weak).** If `a < b`, `w > 0`, and `k ≤ min(#a, #b)`, then `a ⊕ w ≤ b ⊕ w`.

**Claim (TA1-strict).** If additionally `k ≥ divergence(a, b)`, then `a ⊕ w < b ⊕ w`.

*Proof.* Let `j = divergence(a, b)` — the first position where `a` and `b` differ (`aⱼ < bⱼ` since `a < b`). Three cases arise.

*Case 1: `k < j`.* Both `a` and `b` agree at position `k` (since `k < j`), so `(a ⊕ w)ₖ = aₖ + wₖ = bₖ + wₖ = (b ⊕ w)ₖ`. At positions after `k`, both results copy from `w`, giving identical tails. So `a ⊕ w = b ⊕ w`. The weak form (`≤`) holds. The strict form does not — the original divergence at position `j > k` is erased by tail replacement. This is the case that requires TA1-strict's precondition.

*Case 2: `k = j`.* At position `k`, `(a ⊕ w)ₖ = aₖ + wₖ < bₖ + wₖ = (b ⊕ w)ₖ` (since `aₖ < bₖ` and natural-number addition preserves strict inequality). Positions before `k` agree (both copy from their respective starts, which agree on positions `1, ..., k-1`). So `a ⊕ w < b ⊕ w` strictly.

*Case 3: `k > j`.* For `i < k`, the constructive definition gives `(a ⊕ w)ᵢ = aᵢ` and `(b ⊕ w)ᵢ = bᵢ`. Since `j < k`, the divergence at position `j` is preserved: `(a ⊕ w)ⱼ = aⱼ < bⱼ = (b ⊕ w)ⱼ`. So `a ⊕ w < b ⊕ w` strictly. ∎

In all three cases, `a ⊕ w ≤ b ⊕ w` — the weak form holds universally. Strict inequality holds in Cases 2 and 3, i.e., whenever `k ≥ j`. In the editing use case — shifting positions within a single subspace — the action point is at the element level, which is where all positions within a subspace diverge. Case 2 always applies. TA1-strict holds for editing operations.

### Verification of TA3

The subtraction algorithm differs structurally from addition — it zeros positions before the divergence point and copies the tail from the minuend, whereas addition copies the tail from the displacement. We must verify TA3 directly; the proof does not follow "by similar reasoning" from TA1.

**Claim (TA3, strict).** If `a < b`, `a ≥ w`, and `b ≥ w`, then `a ⊖ w < b ⊖ w`.

*Proof.* Let `j = divergence(a, b)` — the first position where `a` and `b` differ (`aⱼ < bⱼ` since `a < b`). Let `dₐ = divergence(a, w)` — the first position where `a` and `w` differ — and `d_b = divergence(b, w)` similarly. Three cases arise from the relationship between `dₐ` and `d_b`; Case 1 splits into two subcases on the relationship between `j` and `d`.

*Case 1: `dₐ = d_b = d` (same divergence point for both).* For `i < d`, `aᵢ = wᵢ = bᵢ`, so both results are zero at these positions. At position `d`, `(a ⊖ w)_d = a_d - w_d` and `(b ⊖ w)_d = b_d - w_d`. Since `a` and `b` agree on positions before `d`, we need `j ≥ d`. At position `j ≥ d`: if `j = d`, then `a_d - w_d < b_d - w_d` (since `aⱼ < bⱼ` and subtraction of the same `w_d` preserves strict inequality), giving `a ⊖ w < b ⊖ w`. If `j > d`, then `a_d = b_d` (since `j > d`), so `a_d - w_d = b_d - w_d`. At positions `d < i < j`, both results copy from their respective minuends: `(a ⊖ w)ᵢ = aᵢ = bᵢ = (b ⊖ w)ᵢ`. At position `j`, `(a ⊖ w)ⱼ = aⱼ < bⱼ = (b ⊖ w)ⱼ`. So `a ⊖ w < b ⊖ w`.

*Case 2: `dₐ < d_b`.* At positions before `dₐ`, both `a` and `b` agree with `w`, hence with each other — so `j ≥ dₐ`. At position `dₐ`: `aᵢ ≠ wᵢ` but `bᵢ = wᵢ` (since `d_b > dₐ`). The result `(a ⊖ w)_{dₐ} = a_{dₐ} - w_{dₐ}` and `(b ⊖ w)_{dₐ} = 0` (zeroed because `b` still matches `w`). Now `a_{dₐ} ≠ w_{dₐ}` and `b_{dₐ} = w_{dₐ}`, so `a_{dₐ} ≠ b_{dₐ}`, meaning `j = dₐ`. Since `a < b` and `j = dₐ`, we have `a_{dₐ} < b_{dₐ} = w_{dₐ}`, so `a_{dₐ} - w_{dₐ} < 0`. But `a ≥ w` requires `a_{dₐ} ≥ w_{dₐ}` at the first divergence point (by the subtraction precondition), so `a_{dₐ} > w_{dₐ}`, contradicting `a_{dₐ} < w_{dₐ}`. This case is impossible under the preconditions.

*Case 3: `dₐ > d_b`.* Symmetric to Case 2: at position `d_b`, `b_{d_b} ≠ w_{d_b}` but `a_{d_b} = w_{d_b}`. So `j = d_b` with `a_{d_b} = w_{d_b} < b_{d_b}` (since `a < b`). Since `b ≥ w`, we have `b_{d_b} > w_{d_b}`. The result `(a ⊖ w)_{d_b} = 0` (zeroed) and `(b ⊖ w)_{d_b} = b_{d_b} - w_{d_b} > 0`. So `a ⊖ w < b ⊖ w`.

In every realizable case, `a ⊖ w < b ⊖ w` holds strictly. ∎

The strict form of TA3 holds without additional preconditions — unlike TA1, there is no weak/strict split. The reason is structural: subtraction's zeroing of positions before the divergence point cannot erase the distinction between `a` and `b` in the way that addition's tail replacement can. Addition replaces all components after the action point with `w`'s tail, which is the same for both operands — this is what allows Case 1 of the TA1 verification to produce equality. Subtraction copies the tail from each respective minuend, preserving any divergence that exists after the divergence point with `w`. And Cases 2 and 3 show that when the two operands diverge from `w` at different points, the ordering is preserved or the case is impossible. The subtraction algorithm's structure inherently prevents equality-collapse.

### Increment for allocation

A separate operation, distinct from the shifting arithmetic, handles address allocation. When the system allocates a new I-space address, it takes the highest existing address in a partition and produces the next one. This is not addition of a width; it is advancement of a counter at a specified hierarchical level.

We define the *last significant position* of a tumbler `t` as `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0} ∪ {#t})`. That is: the position of the last nonzero component, or if every component is zero, the last position. For `[1, 0, 3, 0]`, `sig = 3` (position of the 3). For `[1, 0, 3]`, `sig = 3` (position of the 3). For `[0, 0]`, `sig = 2` (the last position, since no component is nonzero). Note that T3 makes `[1, 0, 3, 0]` and `[1, 0, 3]` distinct tumblers with the same `sig` value — this is consistent because `sig` identifies where the increment acts, not the identity of the tumbler.

For valid I-space addresses, `sig(t)` falls within the last populated field. This is a consequence of T4's positive-component constraint: every field component is strictly positive, so the last component of the last field is nonzero, and `sig(t) = #t`. In a four-field element address `t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`, the final component `Eδ > 0` by T4, so `sig(t) = #t` — the position of `Eδ`. Therefore `inc(t, 0)` increments the last component of the element field, modifying only within that field and preserving the hierarchical structure. This closes the gap between TA5 (which is stated for arbitrary tumblers in T) and T4 (which constrains valid addresses): for valid addresses, `inc(t, 0)` is guaranteed to act on a field component, not on a separator.

**TA5 (Hierarchical increment).** For tumbler `t ∈ T` and level `k ≥ 0`, there exists an operation `inc(t, k)` producing tumbler `t'` such that:

  (a) `t' > t` (strictly greater under T1),

  (b) `t'` agrees with `t` on all components before the increment point,

  (c) when `k = 0` (*sibling*): `#t' = #t`, and `t'` differs from `t` only at position `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`,

  (d) when `k > 0` (*child*): `#t' = #t + k`, the `k - 1` intermediate positions `#t + 1, ..., #t + k - 1` are set to `0` (field separators), and the final position `#t + k` is set to `1` (the first child).

We verify `inc(t, k) > t` for both cases. For k = 0: `t'` agrees with `t` on positions `1, ..., sig(t) - 1` and exceeds `t` at position `sig(t)` (since `t_{sig(t)} + 1 > t_{sig(t)}`), so `t' > t` by T1 case (i). For k > 0: `t'` agrees with `t` on positions `1, ..., #t`, and `#t' > #t`, so `t` is a proper prefix of `t'`, giving `t < t'` by T1 case (ii).

We verify that TA5 preserves T4. T4 imposes two constraints: (i) the positive-component constraint — every field component is strictly positive, and (ii) the zero-count constraint — an I-space address contains at most three zero-valued components.

*Positive-component constraint.* Let `t` be a valid I-space address, so every field component of `t` is strictly positive. For `k = 0`: TA5(c) increments the component at position `sig(t)` from `t_{sig(t)}` to `t_{sig(t)} + 1`. Since `t_{sig(t)} > 0` by T4's positive-component constraint (it is a field component, not a separator), incrementing it yields `t_{sig(t)} + 1 > 0`. All other components are unchanged. So all field components of `t'` are strictly positive. For `k > 0`: TA5(d) appends `k - 1` zero-valued components (field separators) and a final component set to `1`. The original field components of `t` are unchanged (by TA5(b)), so they remain positive. The new final component is `1 > 0`. The intermediate zeros are field separators, not field components. So `t'` satisfies T4's positive-component constraint.

*Zero-count constraint.* For `k = 0`: no zeros are added or removed — `inc(t, 0)` modifies only a nonzero component, leaving `zeros(t')= zeros(t) ≤ 3`. For `k > 0`: `inc(t, k)` appends `k - 1` zero-valued components, so `zeros(t') = zeros(t) + (k - 1)`. T4 requires `zeros(t') ≤ 3`, which gives the constraint `zeros(t) + k - 1 ≤ 3`, equivalently `k ≤ 4 - zeros(t)`. When `t` is an element address (`zeros(t) = 3`), only `k = 1` is permitted — one new separator, producing a single sub-element level. When `t` is a document address (`zeros(t) = 2`), `k ≤ 2`. When `t` is a user address (`zeros(t) = 1`), `k ≤ 3`. When `t` is a node address (`zeros(t) = 0`), `k ≤ 4`. The hierarchy itself enforces this: each zero-valued component introduces one new field, and the address format has exactly four fields separated by exactly three zeros. A deep increment that would introduce a fourth zero would produce a tumbler with four field separators — a five-field address — which lies outside the valid I-space address set defined by T4.

We state this as a precondition: **TA5 preserves T4 when `zeros(t) + k - 1 ≤ 3`.** For the system's allocation operations — which descend one level at a time (`k = 1`) — this is always satisfied, since the deepest valid starting point has `zeros(t) = 3` and `3 + 1 - 1 = 3 ≤ 3`. An implementation that attempted `inc(t, 2)` on an element address would produce a tumbler outside T4's valid set.

Gregory's implementation reveals the concrete mechanism. `tumblerincrement(t, 0, 1)` advances the last significant digit: `1.1.0.3` becomes `1.1.0.4`. `tumblerincrement(t, 1, 1)` extends one level deeper: `1.1.0.2` becomes `1.1.0.2.1` — one intermediate position is introduced (implicitly zero, as a field separator) and the new component is set to 1. The `rightshift` parameter controls `k`. For a zero tumbler (all components zero), the increment also *sets* the exponent to position the new digit correctly — a special-case behavior that produces the first address in a previously empty partition.

This is the mechanism by which the four-level hierarchy is populated. Creating a new account under a server uses a deep increment (`k > 0`) to produce the first child. Allocating successive documents under an account uses a shallow increment (`k = 0`) to produce the next sibling.

### The zero tumblers and positivity

We must say a word about tumblers with all components equal to zero. Under T3 (canonical representation), the tumblers `[0]`, `[0, 0]`, `[0, 0, 0]`, etc., are *distinct* elements of T — they have different lengths. Under T1, they form a chain: `[0] < [0, 0] < [0, 0, 0] < ...` by the prefix rule. There is no single "zero tumbler"; there are infinitely many all-zero tumblers.

We define *positivity* independently of any particular sentinel:

**Definition (Positive tumbler).** A tumbler `t ∈ T` is *positive*, written `t > 0`, iff at least one of its components is nonzero: `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`. A tumbler is a *zero tumbler* iff every component is zero: `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.

This definition has the property that every positive tumbler is greater than every zero tumbler under T1 — if `t` has a nonzero component at position `k`, then at position `k` either the zero tumbler has a smaller component (0 < tₖ) or has run out of components (the zero tumbler is shorter), either way placing it below `t`. Crucially, a zero tumbler of any length is *not* positive, so the condition `w > 0` in TA0 and TA4 excludes all all-zero displacements regardless of length. An all-zero displacement would be a no-op (shifting by zero) and would make TA4 trivially satisfied without constraining anything; the positivity condition prevents this.

**TA6 (Zero tumblers).** No zero tumbler is a valid address — no all-zero tumbler designates content in either I-space or V-space. Every zero tumbler is less than every positive tumbler under T1.

  `(A t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0) ⟹ t is not a valid address)`

Zero tumblers serve as *sentinels*: they mark uninitialized values, denote "unbounded" when used as span endpoints, and act as lower bounds. Gregory's implementation uses `iszerotumbler` as a guard at every entry point — operations reject zero-width spans, zero document addresses, and zero insertion points. The implementation tests whether all mantissa components are zero, which is consistent with our definition: a tumbler is zero iff no component is nonzero, regardless of length.


## Subspace confinement

When INSERT shifts text positions forward, link positions within the same document must not be affected. Text lives in element subspace 1; links live in element subspace 2. The shift must be *confined* to the subspace it applies to.

We need a notion of "displacement within a subspace." Recall that V-space positions are element-local tumblers of the form `[N, x]` — short, document-scoped values with no document prefix. The first component `N` is the subspace identifier; the second component `x` is the ordinal position within that subspace. A natural first attempt at defining an element-local displacement is `w = [0, n]` — action point `k = 2`, preserving the subspace identifier and advancing the ordinal. But applying the abstract `⊖` to full V-positions and such displacements exposes a subtlety: the subtraction's divergence scan compares `[N, x]` with `[0, n]` and finds the first difference at position 1 (where `N ≠ 0`), not at position 2 where the displacement's action point lies. The subtraction produces `[N - 0, x] = [N, x]` — a no-op. The abstract `⊖` cannot shift a V-position backward by a displacement that disagrees with the position at the subspace identifier.

Gregory's implementation reveals the resolution. The operands passed to the tumbler arithmetic during editing shifts are not full V-positions; they are *within-subspace ordinals* — the second component alone. The implementation's `deletend` and `insertnd` operate on `ptr->cdsp.dsas[V]`, which for text crums is a parent-relative offset within the text subspace (exponent -1 in the implementation's encoding). The subspace identifier is not an operand to the shift; it is structural context that determines *which* crums are subject to the shift. INSERT uses the "two-blade knife" to select only text-subspace crums; DELETE relies on an exponent guard that makes cross-subspace subtraction a no-op. In both cases, the arithmetic receives ordinals, not full V-positions.

The abstract specification captures this cleanly: an *element-local displacement* is a single-component tumbler `w = [n]` with `n > 0`, applied to the within-subspace ordinal. The subspace identifier selects which positions are subject to the shift (TA7b); the arithmetic operates on ordinals within that subspace (TA7a). This separation — context selects, arithmetic shifts — is the abstract structure underlying both INSERT's structural guard and DELETE's arithmetic guard.

**TA7a (Subspace closure).** Let `S₁` and `S₂` be distinct element subspaces within a document. For any element-local displacement `w`, the shift operations are closed within each subspace:

  `(A a ∈ S₁, w element-local : a ⊕ w ∈ S₁)` and symmetrically for `⊖`.

**Verification of TA7a.** The shift operates on the within-subspace ordinal `x` by an element-local displacement `w = [n]`. The ordinal is a single-component tumbler with `#x = 1`, and the displacement has `#w = 1` with action point `k = 1`. Both `⊕` and `⊖` are well-defined on these single-component operands.

For `⊕`: by the constructive definition, `(x ⊕ n)₁ = x₁ + n₁ = x + n`. The result is `[x + n]` — a positive single-component tumbler (since `x ≥ 1` and `n > 0`). The ordinal advances, remaining a valid within-subspace position.

For `⊖`: the divergence scan compares `[x]` and `[n]` at position 1. Since `x ≥ n` (by the subtraction precondition — we only subtract from positions at or beyond the deletion boundary), `x ≠ n` when `x > n`, and the divergence is at position 1. The result is `[x - n]`. When `x = n`, the result is the zero tumbler `[0]`, which is a sentinel (TA6) marking the subspace boundary. In either case the result is a single-component non-negative tumbler — a valid within-subspace ordinal.

The subspace identifier is never an operand to the shift. It determines *which* ordinals are subject to the shift (TA7b selects the subspace); the arithmetic operates on ordinals within that subspace. An ordinal shifted by `⊕` or `⊖` remains an ordinal — it cannot become a subspace identifier or cross into another subspace. TA7a holds.

The restriction to element-local displacements is necessary. An unrestricted displacement whose action point falls at the subspace-identifier position could produce an address in a different subspace — TA7a cannot hold for arbitrary `w`. What TA7a does guarantee is that displacements arising from editing operations (which are always element-local, since INSERT and DELETE widths measure content within a single subspace) cannot cross subspace boundaries.

**TA7b (Subspace frame).** An INSERT or DELETE operation within subspace `S₁` does not modify any position in a distinct subspace `S₂`:

  `(A b ∈ S₂ : post(b) = pre(b))`

where `pre(b)` and `post(b)` denote the V-space position of content `b` before and after the operation. TA7b is a frame condition on the operation definitions, not a property of the arithmetic. It requires that the operation restricts its shift to positions within the affected subspace — that is, the operation applies `⊕` or `⊖` only to positions `a ∈ S₁`, and TA7a guarantees those results remain in `S₁`. Together, TA7a (arithmetic stays in-subspace) and TA7b (operations only shift in-subspace positions) constitute subspace confinement.

TA7a and TA7b together form a single system-level guarantee — subspace confinement — but Gregory's analysis reveals a striking asymmetry in how the two editing operations achieve it:

For **INSERT**, the implementation uses an explicit structural guard — a "two-blade knife" that computes the boundary between subspaces. The boundary tumbler is constructed by a four-step arithmetic computation: increment at the parent level, extract the fractional tail via `beheadtumbler`, subtract the tail's leading component, and increment at the next finer level. This produces the precise tumbler at which the next subspace begins (e.g., `2.1` for the link subspace boundary when inserting in text subspace `1.x`). Entries beyond this boundary are never passed to the addition operation. Confinement is achieved by *not calling* the arithmetic on cross-subspace entries.

For **DELETE**, the implementation relies on an incidental property of the subtraction algorithm. The routine `strongsub` contains an exponent guard that returns the minuend unchanged when the subtrahend has a smaller exponent. Since text widths (fractional V-positions, exponent ≤ -1) have smaller exponents than link positions (whole-number subspace identifiers, exponent = 0), subtracting a text width from a link position is a no-op. Confinement is achieved by an *accidental arithmetic property*, not by deliberate structural design.

The abstract specification does not prescribe either mechanism. TA7a and TA7b state what must hold; how each is achieved is an implementation choice. But the asymmetry teaches us something important: **subspace confinement is one guarantee, but each operation may require a different proof obligation.** An implementation that "corrects" the subtraction to handle cross-exponent operands would break DELETE's subspace isolation while leaving INSERT's intact. The abstract property is stable; the implementation strategies are fragile in different ways.


## What tumbler arithmetic is NOT

We must state explicitly what the tumbler algebra does not guarantee. These negative results constrain what an implementer may assume.

**The algebra is not a group.** There is no additive identity — the zero tumbler is a sentinel, not a neutral element for addition. There is no additive inverse for every element — subtraction is only defined when `a ≥ w`. The algebra is not closed under subtraction in general.

**Addition is not associative.** We do NOT require `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)`. The design has no need for associativity — shifts are always applied as a single operation (shift by the inserted width), never composed from multiple smaller shifts. Gregory's implementation does not implement carry propagation in `tumbleradd` — it adds at most two digit positions, then copies the remaining digits from one input. This makes the operation fast but non-associative for operands at different exponent levels.

**Addition is not commutative.** We do NOT require `a ⊕ b = b ⊕ a`. The operands play asymmetric roles: the first is a *position*, the second is a *displacement*. Swapping them is semantically meaningless.

**There is no multiplication or division.** Gregory's analysis of the complete codebase confirms: no `tumblermult`, no `tumblerdiv`, no scaling operation of any kind. The arithmetic repertoire is: add, subtract, increment, compare. This makes sense — tumblers are *addresses*, not quantities. You don't multiply two file paths or divide an address by three. The operations that exist are exactly those needed for navigating, shifting, and allocating in a hierarchical address space.

The absence of algebraic structure beyond a monotone shift is not a deficiency. It is the *minimum* that editing requires. An ordered set with an order-preserving shift and an allocation increment is sufficient. Anything more would be unused machinery and unverified obligation.


## The two address spaces

We have so far treated tumblers as a single set. In fact the system maintains two address spaces, each using tumblers but with different algebraic contracts:

**I-space (identity space)** uses tumblers as permanent content identifiers. The applicable properties are:

  - T8 (permanence): once assigned, never removed or changed
  - T9 (forward allocation): each allocator's output is strictly monotonically increasing
  - T10 (partition independence): disjoint owners, no coordination needed
  - TA5 (hierarchical increment): allocation produces siblings or children

I-space addresses are compared (T1) and containment-tested (T6), but they are never shifted by editing operations. The arithmetic `⊕` is well-defined on I-space tumblers (TA0) — it is used to compute span endpoints (T12) — but no editing operation applies `⊕` or `⊖` to I-space addresses.

**V-space (virtual space)** uses tumblers as mutable document positions. The applicable properties are:

  - T1 (total order): positions are ordered by reading sequence
  - TA0–TA4 (arithmetic): positions shift on INSERT and DELETE
  - TA7a (subspace closure): shifts stay within their subspace; TA7b (subspace frame): operations do not modify other subspaces

V-space has no permanence guarantee. Nelson is explicit: "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing." V-positions are rearranged by every editing operation.

A V-space position is *element-local*: a short tumbler of the form `[N, x]` where `N` is the subspace identifier (1 for text, 2 for links) and `x` is the ordinal position within that subspace. V-positions carry no document prefix — each document's POOM maintains its own V-space, and the document identity is established by which POOM is being queried, not embedded in the V-address. Text positions begin at `[1, 1]` and advance by incrementing the second component: `[1, 1]`, `[1, 2]`, `[1, 3]`, and so on. Link positions begin at `[2, 1]`. Gregory's implementation confirms this representation: POOM bottom crums store V-displacements as 2-digit tumblers (`cdsp.dsas[V]`), while I-displacements in the same crum use 6–9 digit tumblers encoding the full hierarchical address. The POOM's `setwispnd` normalization stores these V-positions as parent-relative offsets; absolute V-position is reconstructed by accumulating displacements from root to leaf. The function `docidandvstream2tumbler`, which concatenates a document ISA with a V-stream position, is used only for the external output of the compare-versions API — never in the POOM's internal storage or editing paths.

**T11 (Dual-space separation).** The permanence properties (T8, T9, T10) apply exclusively to I-space. The *editing shifts* — the application of `⊕` and `⊖` by INSERT and DELETE operations to modify document positions — apply exclusively to V-space; the subspace frame condition (TA7b) constrains these V-space operations. No editing operation shifts an I-space address. No operation claims permanence for a V-space position.

We must be precise about what T11 restricts. The operations `⊕` and `⊖` are defined on the carrier set T (by TA0–TA4) and are *available* in both spaces — they are arithmetic on tumblers, not inherently tied to one space. What T11 constrains is their *use by editing operations*: INSERT and DELETE apply shifts only to V-space positions. The arithmetic properties TA0–TA4 and TA-strict hold for `⊕` and `⊖` as operations on T; the subspace closure property TA7a constrains `⊕` and `⊖` within V-space. This distinction matters because T12 (below) defines spans using `⊕`, and spans are needed in *both* spaces — links reference I-space spans, endsets are sets of I-space spans. The well-definedness of `s ⊕ ℓ` for an I-space start address `s` follows from TA0 (which is a property of `⊕` on T, not restricted to V-space); what T11 forbids is not the computation `s ⊕ ℓ` but rather an editing operation that would *reassign* the result as a new position for some content.

T11 is the architectural core. Links attach to I-space addresses and therefore survive editing. Editing operations modify V-space positions and therefore do not violate permanence. The two spaces share the same carrier set T, the same ordering T1, and the same arithmetic operations `⊕` and `⊖` — but their operational contracts differ: I-space addresses are permanent and never shifted by edits; V-space positions are mutable and shifted freely.

The document is the *mapping* between these two spaces: a function from V-positions to I-addresses. The POOM (permutation of the original media) is precisely this mapping, represented as a sequence of spans. INSERT, DELETE, and REARRANGE modify the POOM. The I-addresses it maps to are untouched — content does not move; only the arrangement changes.


## Spans

A span is a pair `(s, ℓ)` where `s ∈ T` is a start address and `ℓ ∈ T` is a length (a positive tumbler used as a displacement), denoting the contiguous range from `s` up to but not including `s ⊕ ℓ`. The length `ℓ` is a tumbler — the same kind of object as `s` — because `s ⊕ ℓ` is defined by TA0, which requires both operands in T. In practice, span lengths in the element subspace are single-component tumblers `[n]` denoting a count of `n` consecutive positions, but the algebra admits multi-component lengths, which arise when a span crosses a hierarchical boundary (e.g., a span covering all content in multiple documents under a user).

Spans are the fundamental unit of content reference: links reference spans, transclusion copies spans, the POOM is a sequence of spans.

**T12 (Span well-definedness).** A span `(s, ℓ)` with `ℓ > 0` denotes the set `{t ∈ T : s ≤ t < s ⊕ ℓ}`. This set is contiguous under T1 — there is no tumbler between two members that is not itself a member.

Contiguity is definitional: the span is an interval `[s, s ⊕ ℓ)` in a totally ordered set, and intervals in total orders are contiguous — if `s ≤ x ≤ z < s ⊕ ℓ` and `x ≤ y ≤ z`, then `s ≤ y < s ⊕ ℓ`. Non-emptiness follows from TA-strict: since `ℓ > 0`, TA0 gives `s ⊕ ℓ ∈ T`, and TA-strict gives `s ⊕ ℓ > s` directly. The interval `[s, s ⊕ ℓ)` is therefore non-empty — it contains at least `s` itself.

We reserve T5 for the distinct claim that *prefix-defined* sets are contiguous — a non-trivial property of the lexicographic order. For instance, T5 establishes that all content under server 2 forms a contiguous interval, which is not definitional but follows from the structure of T1.

Nelson makes spans self-describing at every hierarchical level: "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server — or the entire docuverse." The "1-position convention" exploits T5: because subtrees are contiguous, a span whose start is a high-level prefix (like a server address) and whose length reaches to the next sibling captures exactly that server's entire content. No enumeration needed.

And a span may be empty — populated by nothing at present — yet valid: "A span that contains nothing today may at a later time contain a million documents." The range is determined by the endpoints; what is actually stored within that range is a question about the current state of I-space, not about the tumbler algebra.


## Order structure: adjacent pairs and interpolation

We have stated the abstract properties. We now ask: what is the order-theoretic structure of T under T1?

T is *not* dense. Every tumbler `t` and its zero-extension `t.0` form an adjacent pair: `t < t.0` by the prefix rule (T1, case ii), and no tumbler lies strictly between them. For suppose `t < x < t.0`. Since `t` is a prefix of `t.0`, T5 requires that `x` also extend prefix `t` — so `x = t.x₁. ... .xₖ` for some `k ≥ 1`. The smallest such extension is `t.0` (since `x₁ ≥ 0` and if `x₁ = 0` then `x ≥ t.0`), giving `x ≥ t.0`, a contradiction. Every tumbler has an immediate successor: its zero-extension. The ordering resembles a tree's depth-first traversal order, which has adjacent pairs at every branch point.

What T0 does provide is *interpolation between non-prefix-related tumblers*. Between any two tumblers that differ at a shared position — that is, neither is a prefix of the other — there exist arbitrarily many intermediate tumblers. Between `1.3` and `1.5`, we can place `1.4`, `1.3.1`, `1.3.2`, and so on — T0 guarantees we never exhaust the space of intermediate values. This is the property that makes allocation work: within a single hierarchical level, there is always room for the next sibling.

Gregory's implementation further restricts the representable values to a fixed 16-digit mantissa of 32-bit unsigned integers, introducing additional adjacencies beyond those inherent in the abstract order. Two tumblers at maximum depth that differ by 1 in their last component are adjacent in both the abstract and concrete orders; but the implementation also makes tumblers adjacent when they would have required a 17th component to interpolate between them. A correct implementation must demonstrate that allocation never drives the system into a region where this additional adjacency matters — that the reachable allocations never need to interpolate where the representation has sealed the gap.


## Enfilade displacement arithmetic

One further use of tumbler arithmetic deserves mention: the 2D enfilade that implements the POOM stores displacements as pairs of tumblers, one for the V-dimension and one for the I-dimension. The displacement of a parent node is the component-wise minimum of its children's displacements, and children store offsets relative to their parent.

**TA8 (Orthogonal dimensions).** In the 2D enfilade displacement arithmetic, V-displacements and I-displacements are added, subtracted, minimized, and maximized independently. There is no cross-dimensional operation that combines a V-value with an I-value.

  `add(⟨v₁, i₁⟩, ⟨v₂, i₂⟩) = ⟨v₁ ⊕ v₂, i₁ ⊕ i₂⟩`

  `min(⟨v₁, i₁⟩, ⟨v₂, i₂⟩) = ⟨min(v₁, v₂), min(i₁, i₂)⟩`

Gregory confirms: the `lockadd`, `locksubtract`, `lockmin`, and `lockmax` routines each loop through dimensions, applying single-tumbler arithmetic to each independently. The dimensions never interact. This is not surprising — a V-position and an I-address have entirely different semantics, and mixing them would be meaningless — but it is worth stating because it simplifies verification: proving correctness of 2D displacement arithmetic reduces to proving correctness of each 1D tumbler operation separately.


## Worked example: a document with five characters

We instantiate the algebra on a concrete scenario. Server 1, user 3, document 2, text subspace (element field begins with 1). The document contains five characters at I-space addresses:

  `a₁ = 1.0.3.0.2.0.1.1`, `a₂ = 1.0.3.0.2.0.1.2`, `a₃ = 1.0.3.0.2.0.1.3`, `a₄ = 1.0.3.0.2.0.1.4`, `a₅ = 1.0.3.0.2.0.1.5`

**T4 (Hierarchical parsing).** Take `a₃ = 1.0.3.0.2.0.1.3`. The three zeros at positions 2, 4, 6 are the field separators. The node field is `[1]`, the user field is `[3]`, the document field is `[2]`, the element field is `[1, 3]`. The first component of the element field is `1`, placing this address in the text subspace.

**T1 (Ordering).** We verify `a₁ < a₂ < a₃ < a₄ < a₅`. All five share the prefix `1.0.3.0.2.0.1` and diverge at position 8, where the values are `1, 2, 3, 4, 5` respectively. Lexicographic comparison at the divergence point confirms the order.

**T5 (Contiguous subtrees).** The prefix `p = 1.0.3.0.2` identifies all content in document 2. Any tumbler `b` with `a₁ ≤ b ≤ a₅` must share this prefix. Suppose `b` diverged from `p` at some position `k ≤ 5`. Then `bₖ ≠ pₖ`, but `a₁` and `a₅` agree with `p` at position `k`, so `bₖ < pₖ` would violate `a₁ ≤ b` and `bₖ > pₖ` would violate `b ≤ a₅`. So `b` extends prefix `p` — it belongs to document 2.

**T6 (Decidable containment).** Do `a₃ = 1.0.3.0.2.0.1.3` and `a₅ = 1.0.3.0.2.0.1.5` belong to the same account? Extract node fields: both `[1]`. Extract user fields: both `[3]`. Yes — same node, same user. Do they belong to the same document? Document fields: both `[2]`. Yes. Is `a₃` in the same document family as an address in document `2.1` (a version)? The document field of `a₃` is `[2]`, and `[2]` is a prefix of `[2, 1]`, so T6(d) confirms structural subordination.

**T9 (Forward allocation).** The five addresses were allocated in order by a single allocator (user 3's allocation stream within document 2). Each successive address is strictly greater than its predecessor: `a₁ < a₂ < a₃ < a₄ < a₅`. No gap-filling occurred; if `1.0.3.0.2.0.1.2` had been skipped, it would remain a permanent ghost.

The document also contains a link in subspace 2. The link's I-space address is:

  `ℓ₁ = 1.0.3.0.2.0.2.1`

**T4** on `ℓ₁`: the three zeros at positions 2, 4, 6 are field separators. Node field `[1]`, user field `[3]`, document field `[2]`, element field `[2, 1]`. The first component of the element field is `2`, placing this address in the link subspace. By T7, `ℓ₁ ≠ aᵢ` for all `i` — the subspace identifiers differ (`2 ≠ 1`).

**V-space arithmetic.** The document's V-space maps positions to I-addresses. V-positions are element-local 2-component tumblers: text positions are `v₁ = [1, 1]` through `v₅ = [1, 5]` (subspace identifier 1, ordinals 1–5). The link `ℓ₁` has V-position `[2, 1]` (subspace 2, ordinal 1). Now INSERT two characters at position 3 in text subspace 1 — the displacement is `w = [0, 2]` (action point `k = 2`, advancing ordinals within the subspace). All V-positions at or above ordinal 3 in subspace 1 shift forward:

  `v₃' = [1, 3] ⊕ [0, 2] = [1, 5]`, `v₄' = [1, 4] ⊕ [0, 2] = [1, 6]`, `v₅' = [1, 5] ⊕ [0, 2] = [1, 7]`

**TA7a (Subspace closure).** The displacement `w = [0, 2]` is element-local: its action point `k = 2` falls at the ordinal position, not the subspace identifier. By the constructive definition of `⊕`, position 1 of the result copies from the start position: `r₁ = a₁ = 1`. Position 2 advances: `r₂ = a₂ + w₂ = 3 + 2 = 5`. Result: `[1, 5]` — the subspace identifier is preserved, the position remains in subspace 1.

**TA7b (Subspace frame).** The INSERT is within text subspace 1. The link `ℓ₁` is in subspace 2. TA7b requires `post(ℓ₁) = pre(ℓ₁)` — the link's V-space position is unchanged. This holds because the operation applies shifts only to positions in subspace 1; `ℓ₁`'s position in subspace 2 is outside the scope of the shift and is not modified.

**TA1 (Order preservation).** Before: `v₃ = [1, 3] < v₄ = [1, 4]`. After: `v₃' = [1, 5] < v₄' = [1, 6]`. The relative order is preserved. The positions share first component `1`; the comparison reduces to the ordinals `3 < 4` and `5 < 6`.

**TA4 (Inverse).** DELETE the same two characters (width `[0, 2]`): `v₃' ⊖ [0, 2] = [1, 5] ⊖ [0, 2]`. The subtraction's divergence scan: position 1, `1 ≠ 0` — divergence at position 1. Result: `r₁ = 1 - 0 = 1`, `r₂ = a₂ = 5`, giving `[1, 5]` — unchanged! This reveals that the abstract `⊖` applied to the full V-position `[1, 5]` and the displacement `[0, 2]` finds the divergence at the subspace identifier, not at the ordinal. The subtraction operates correctly only when applied to the within-subspace ordinal: `[5] ⊖ [2] = [3]`, restoring the original ordinal. The subspace identifier is context, not an operand. The full recovery yields `v₃ = [1, 3]`, as expected.

The I-space addresses `a₁` through `a₅` and `ℓ₁` are unchanged by all of this. T8 guarantees their permanence; T11 confirms that shift arithmetic applies only to V-space. The five characters and the link are the same objects at the same I-addresses — only the text arrangement in the document has changed.


## Formal summary

We collect the structure. The tumbler algebra is a tuple `(T, <, ⊕, ⊖, inc, fields, Z)` where `Z = {t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0)}` is the set of zero tumblers:

- `T` is the carrier set of finite sequences of non-negative integers, with unbounded components (T0)
- `<` is the lexicographic total order on `T` (T1), intrinsically computable (T2), with canonical representation (T3)
- The hierarchical parsing function `fields` extracts four-level containment (T4), yielding contiguous subtrees (T5); decidable containment (T6, corollary of T4) and element subspace disjointness (T7, corollary of T3 + T4) follow
- `T8–T10` establish permanence, forward allocation, and partition independence for I-space; `T10a` constrains each allocator to use `inc(·, 0)` for sibling outputs, reserving `k > 0` exclusively for child-spawning
- `T11` separates the I-space and V-space contracts: `⊕` and `⊖` are defined on T and used for span computation in both spaces, but editing shifts are confined to V-space
- `⊕` and `⊖` are order-preserving operations on T (TA0–TA3, with TA0 requiring `k ≤ #a`), with weak order preservation (TA1, `≤`) universally and strict preservation (TA1-strict, `<`) when `k ≥ divergence(a,b)`; strict increase (TA-strict); mutually inverse when `k = #a`, `#w = k`, and all components of `a` before `k` are zero (TA4); used by editing operations in V-space and by span definitions in both spaces
- `inc` is hierarchical increment for allocation (TA5)
- Zero tumblers (all components zero, any length) are sentinels, not valid addresses (TA6); positivity is defined as having at least one nonzero component
- `TA7a` confines element-local shifts to their subspace (algebraic closure); `TA7b` requires operations not to modify other subspaces (frame condition)
- `TA8` ensures orthogonality of V and I dimensions in displacement arithmetic
- Spans are self-describing contiguous ranges (T12)

Each property is required by at least one system guarantee:

| Property | Required by |
|----------|-------------|
| T0 | Unbounded growth of docuverse |
| T1, T2 | Span containment, link search, enfilade traversal |
| T3 | Address identity, uniqueness |
| T4, T5 | Hierarchical queries, self-describing spans |
| T6 *(corollary of T4)* | Decidable containment |
| T7 *(corollary of T3 + T4)* | Editorial subspace isolation |
| T8 | Link stability, transclusion identity |
| T9 | Per-allocator monotonicity; partition monotonicity derived from T9 + T10 + T1 |
| T10 | Decentralized allocation |
| T11 | Separation of mutable arrangement from permanent identity |
| T12 | Content reference by span |
| TA0–TA4, TA-strict | INSERT/DELETE correctness, span computation in both spaces, span non-emptiness (T12) |
| TA5 | Address allocation |
| TA6 | Sentinel and lower bound |
| TA7a, TA7b | INSERT/DELETE subspace isolation |
| TA8 | 2D enfilade correctness |

Removing any independent property breaks a system-level guarantee. T6 and T7 are derived (corollaries of T4, T3 respectively) and are stated for emphasis, not as independent axioms — removing them from the list does not weaken the algebra, since their content follows from the remaining properties.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| T0 | Every component of a tumbler is unbounded — no maximum value exists | introduced |
| T1 | Tumblers are totally ordered by lexicographic comparison, with the prefix-less-than convention | introduced |
| T2 | Tumbler comparison is computable from the two addresses alone, examining at most min(#a, #b) components | introduced |
| T3 | Each tumbler has exactly one canonical representation; component-wise identity is both necessary and sufficient for equality | introduced |
| T4 | An I-space tumbler has at most three zero-valued components as field separators, with every field component strictly positive (positive-component constraint), partitioning it into four hierarchical fields | introduced |
| T5 | The set of tumblers sharing a prefix forms a contiguous interval under T1 | introduced |
| T6 | Containment (same node, same account, same document family, structural subordination) is decidable from addresses alone | corollary of T4 |
| T7 | Subspaces (text, links) within a document's element field are permanently disjoint | corollary of T3 + T4 |
| T8 | Once a tumbler is assigned to content, the assignment is permanent and the content is immutable | introduced |
| T9 | Within a single allocator's sequential stream, new addresses are strictly monotonically increasing; gaps are permanent | introduced |
| T10 | Allocators with non-nesting prefixes produce distinct addresses without coordination | introduced |
| T11 | Permanence (T8–T10) applies to I-space; editing shifts (application of ⊕/⊖ by INSERT/DELETE) and subspace frame (TA7b) apply to V-space; ⊕/⊖ are defined on T and available in both spaces for span computation | introduced |
| T12 | A span (s, ℓ) with s ∈ T and ℓ ∈ T denotes the contiguous interval {t : s ≤ t < s ⊕ ℓ} | introduced |
| TA0 | Tumbler addition a ⊕ w is well-defined for positive width w | introduced |
| TA1 | Addition preserves the total order (weak): a < b ⟹ a ⊕ w ≤ b ⊕ w for w > 0 and k ≤ min(#a, #b) | introduced |
| TA-strict | Adding a positive displacement strictly advances: a ⊕ w > a for w > 0 | introduced |
| TA2 | Tumbler subtraction a ⊖ w is well-defined when a ≥ w | introduced |
| TA3 | Subtraction preserves the total order: a < b ⟹ a ⊖ w < b ⊖ w when both are defined | introduced |
| TA4 | Addition and subtraction are mutual inverses: (a ⊕ w) ⊖ w = a when k = #a, #w = k, and all components of a before k are zero | introduced |
| TA5 | Hierarchical increment inc(t, k) produces t' > t: k=0 advances component at sig(t), k>0 extends by k positions with k−1 zero separators and final component 1 | introduced |
| TA6 | Every all-zero tumbler (any length) is less than every positive tumbler and is not a valid address; positivity means at least one nonzero component | introduced |
| TA7a | For element-local displacements, shift operations applied within one subspace produce results in that same subspace (algebraic closure) | introduced |
| TA7b | INSERT/DELETE within one subspace does not modify positions in any other subspace (frame condition) | introduced |
| TA8 | In 2D displacement arithmetic, V and I dimensions are operated on independently with no cross-dimensional combination | introduced |


## Open Questions

What algebraic property of the POOM mapping must hold for span intersection to be computable from the mapping alone, without enumerating individual positions?

Must allocation counter durability across crashes be a global-history property or only a per-session property — and what recovery mechanism restores monotonicity after a crash that loses the counter state?

What minimal auxiliary structure must the system maintain to reconstruct version-derivation history, given that it is not decidable from addresses alone?

What must the system guarantee about the zero tumbler's interaction with span arithmetic — if a span endpoint is the zero sentinel, how must containment and intersection operations behave?


## Resolved Questions

The following open questions were resolved by the constructive definition of `⊕` and `⊖`:

**Order preservation scope (formerly open question 1).** TA1 holds strictly when the action point `k ≤ divergence(a, b)`. For editing operations (shifts within a subspace), this is always satisfied — the displacement acts at the element level, which is where all positions within a subspace diverge. TA1 in the weak (≤) sense holds universally.

**Zero-component production (formerly open question 2).** At the action point, `rₖ = aₖ + wₖ ≥ 1` (since `wₖ > 0`), so the action point never produces a zero. Trailing components copy from `w` and may include zeros — these are field separators in the displacement's hierarchical structure, not zero-valued field components. The T4 positive-component constraint propagates from the displacement.

**Shift composition (formerly open question 5).** `(a ⊕ w₁) ⊕ w₂ = a ⊕ (w₁ ⊕ w₂)` when `w₁` and `w₂` act at the same hierarchical level (same action point). It fails when they act at different levels, because tail replacement in `w₁ ⊕ w₂` changes the composite's meaning. In the editing use case (consecutive shifts at the same element level), composition holds.
