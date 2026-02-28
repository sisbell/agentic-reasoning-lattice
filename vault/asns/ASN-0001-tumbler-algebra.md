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

**T4 (Hierarchical parsing).** Every tumbler `t ∈ T` used as an I-space address contains at most three zero-valued components, appearing in order as field separators. The function `fields(t)` that extracts the node, user, document, and element fields is well-defined and computable from `t` alone.

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

Even addresses that have no stored content are irrevocably claimed. Nelson calls these "ghost elements": "the docuverse is the occupied tumbler-space — as occupied by conceptually assigned positions, even if nothing represents them in storage." A ghost element cannot be reused for new content; it is a permanent gap. Gaps are features, not defects.


## Monotonic allocation

T8 tells us that addresses, once assigned, are permanent. We now ask: in what order are new addresses assigned?

**T9 (Forward allocation).** Each allocator in the system controls a single ownership prefix and allocates sequentially within it. Within that sequential stream, new addresses are strictly monotonically increasing:

  `(A a, b : same_allocator(a, b) ∧ allocated_before(a, b) : a < b)`

Nelson's design is explicitly chronological: "suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." And the forking mechanism is sequential: "successive new digits to the right ... 2.1, 2.2, 2.3, 2.4 are successive items being placed under 2." The word "successive" carries the weight: 2.2 follows 2.1, never precedes it.

T9 prohibits gap-filling. If address 2.3 was allocated and address 2.5 was allocated, then 2.4 either was allocated between them or is a permanent ghost. The system never goes back to fill 2.4 after allocating 2.5. To reuse a gap would violate T8 (the gap address may have been linked to as a ghost element) and T9 (the allocation counter would retreat).

We observe that T9 is scoped to a *single allocator's sequential stream*, not to arbitrary partitions. A server-level subtree spans multiple independent allocators (one per user). Those allocators operate concurrently — T10 below guarantees they need no coordination. If user A (prefix `1.0.1`) allocates at wall-clock time `t₂` and user B (prefix `1.0.2`) allocates at time `t₁ < t₂`, neither T9 nor any other property requires that A's address exceed B's. T9 applies within each user's allocation stream independently.

**Theorem (Partition monotonicity).** Within any prefix-delimited partition of the address space, the set of allocated addresses is totally ordered by T1, and this order is consistent with the allocation order of any single allocator within that partition.

*Proof.* Consider a partition with prefix `p`. Every allocated address in this partition has prefix `p`, hence lies in the contiguous interval guaranteed by T5. Within the partition, addresses belong to sub-partitions owned by distinct allocators, whose prefixes are disjoint (T10). Each allocator's output is monotonic (T9). The sub-partitions are ordered by their prefixes under T1 — a server allocating user prefixes does so monotonically (T9 applied to the server's own allocation stream). So addresses from earlier-allocated sub-partitions precede those from later-allocated sub-partitions, and within each sub-partition, allocation order matches address order. ∎

The theorem recovers the intuition that "later addresses are larger" at every level of the hierarchy, but it does so as a *consequence* of per-allocator monotonicity (T9), prefix disjointness (T10), and the prefix ordering (T1) — not as a universal axiom that would require coordinating concurrent allocators.

Gregory confirms: I-address allocation uses `tumblerincrement` with `rightshift=0`, producing sequences like `...3.0.1.3.1`, `...3.0.1.3.2`, `...3.0.1.3.3` — strictly increasing, never retreating. The overflow check in `tumblerincrement` (fatal error when `idx + rightshift >= NPLACES`) is the point at which the implementation admits it cannot satisfy T9 for arbitrarily large addresses. The abstract specification demands T9 unconditionally; the implementation approximates it within its representable range and fails loudly at the boundary.

A consequence of T8 and T9 together is that I-space is a *growing set* in the lattice-theoretic sense: the set of allocated addresses can only increase, and new elements always appear at the frontier of each allocator's domain.


## Coordination-free uniqueness

The tumbler hierarchy exists so that independent actors can allocate addresses without communicating:

**T10 (Partition independence).** The address space is partitioned by prefix into ownership domains. Two allocators with distinct, non-nesting prefixes can allocate simultaneously, and the resulting addresses are guaranteed distinct.

Formally: let `p₁` and `p₂` be prefixes such that neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for any tumbler `a` with prefix `p₁` and any tumbler `b` with prefix `p₂`, `a ≠ b`.

This follows from the definition: if `a` has prefix `p₁` and `b` has prefix `p₂`, and the prefixes diverge at some position `k` with `p₁ₖ ≠ p₂ₖ`, then `aₖ = p₁ₖ ≠ p₂ₖ = bₖ`, so `a ≠ b`. The proof is elementary, but the property is architecturally profound. Nelson: "The owner of a given item controls the allocation of the numbers under it." No central allocator is needed. No coordination protocol is needed. The address structure itself makes collision impossible.

From T9 and T10 together:

**Theorem (Global uniqueness).** No two distinct allocations, anywhere in the system, at any time, produce the same address.

*Proof.* Consider allocations producing addresses `a` and `b` by distinct allocation events. Three cases arise.

*Case 1: Same allocator.* Both addresses are produced by the same allocator's sequential stream. T9 guarantees `a ≠ b` because allocation is strictly monotonic.

*Case 2: Different allocators at the same hierarchical level.* The allocators have prefixes `p₁` and `p₂` that are siblings — neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). T10 gives `a ≠ b` directly.

*Case 3: Different allocators at different hierarchical levels.* One allocator's prefix nests within another's — say a server (prefix `[1]`) and one of its users (prefix `[1, 0, 3]`). T10 does not apply because the prefixes nest. But addresses produced at different hierarchical levels have different numbers of zero-valued components (T4): a server-level allocation produces an address with zero zeros (a node address) or one zero (a user address), while a user-level allocation produces an address with two zeros (a document address) or three zeros (an element address). Since the zero counts differ, the addresses differ in length or in the value at some component position, so T3 gives `a ≠ b`. ∎

This theorem is the foundation of the entire addressing architecture. Every subsequent guarantee — link stability, transclusion identity, royalty tracing — depends on the uniqueness of addresses. And uniqueness is achieved without any distributed consensus, simply by the structure of the names.


## Tumbler arithmetic

We now turn to the arithmetic operations. The system's editing model requires shifting V-space positions forward on INSERT and backward on DELETE. These shifts are performed by tumbler addition and subtraction. We are careful to note that these operations apply to **V-space positions** — the mutable arrangement layer — not to I-space addresses, which are permanent by T8.

V-space positions are themselves tumblers, but they encode "where this byte appears in the document right now," and that changes with every edit. I-space addresses encode "which byte this is, forever."

### Addition for shifting

Let `⊕` denote tumbler addition, used to shift V-positions forward after insertion:

**TA0 (Well-defined addition).** For tumblers `a, w ∈ T` where `w` represents a positive displacement, `a ⊕ w` is a well-defined tumbler in `T`.

**TA1 (Order preservation under addition).** `(A a, b, w : a < b ∧ w > 0 : a ⊕ w < b ⊕ w)`.

TA1 is the critical property for INSERT correctness. If two bytes were in reading order before the insertion, they must remain in reading order after shifting. Without TA1, INSERT could scramble the relative ordering of content within a document — a catastrophic failure.

But TA1 alone does not guarantee that addition *advances* a position. It preserves relative order between two positions but is silent about the relationship between `a` and `a ⊕ w`. We need:

**TA-strict (Strict increase).** `(A a ∈ T, w > 0 : a ⊕ w > a)`.

Without TA-strict, the axioms admit a degenerate model in which `a ⊕ w = a` for all `a, w`. This no-op model satisfies TA0 (result is in T), TA1 (if `a < b` then `a < b` — the consequent is unchanged), and TA4 (`(a ⊕ w) ⊖ w = a ⊖ w = a` if subtraction is equally degenerate). Every axiom is satisfied, yet spans are empty — the interval `[s, s ⊕ ℓ)` collapses to `[s, s)`. TA-strict excludes this model and ensures that adding a positive displacement moves the position forward. T12 (span well-definedness) depends on this directly.

### Subtraction for shifting

Let `⊖` denote tumbler subtraction, used to shift V-positions backward after deletion:

**TA2 (Well-defined subtraction).** For tumblers `a, w ∈ T` where `a ≥ w`, `a ⊖ w` is a well-defined tumbler in `T`.

**TA3 (Order preservation under subtraction).** `(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w < b ⊖ w)`.

### Inverse

**TA4 (Inverse).** `(A a, w : w > 0 : (a ⊕ w) ⊖ w = a)`.

TA4 ensures that INSERT followed by DELETE at the same point restores the original V-positions. Without it, the system could accumulate drift — repeated insert-delete cycles shifting content progressively.

The reverse direction is equally necessary — DELETE followed by INSERT at the same point must also restore positions:

**Corollary (Reverse inverse).** `(A a, w : a ≥ w ∧ w > 0 : (a ⊖ w) ⊕ w = a)`.

*Proof.* Let `y = a ⊖ w`. By TA4, `(y ⊕ w) ⊖ w = y`. Suppose `y ⊕ w ≠ a`. If `y ⊕ w > a`, then applying `⊖ w` to both sides (order-preserving by TA3, both sides ≥ w since `y ⊕ w > a ≥ w`) gives `y > a ⊖ w = y`, a contradiction. If `y ⊕ w < a`, then subtracting `w` from both sides preserves order by TA3 — we verify the preconditions: `y ⊕ w ≥ w` (by TA-strict applied to `y`, or by TA4's well-definedness: `(y ⊕ w) ⊖ w = y` requires `y ⊕ w ≥ w`) and `a ≥ w` (by hypothesis). So TA3 gives `y < a ⊖ w`, contradicting `y = a ⊖ w`. So `(a ⊖ w) ⊕ w = a`. ∎

### Increment for allocation

A separate operation, distinct from the shifting arithmetic, handles address allocation. When the system allocates a new I-space address, it takes the highest existing address in a partition and produces the next one. This is not addition of a width; it is advancement of a counter at a specified hierarchical level.

We define the *last significant position* of a tumbler `t` as `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0} ∪ {#t})`. That is: the position of the last nonzero component, or if every component is zero, the last position. For `[1, 0, 3, 0]`, `sig = 3` (position of the 3). For `[1, 0, 3]`, `sig = 3` (position of the 3). For `[0, 0]`, `sig = 2` (the last position, since no component is nonzero). Note that T3 makes `[1, 0, 3, 0]` and `[1, 0, 3]` distinct tumblers with the same `sig` value — this is consistent because `sig` identifies where the increment acts, not the identity of the tumbler.

**TA5 (Hierarchical increment).** For tumbler `t ∈ T` and level `k ≥ 0`, there exists an operation `inc(t, k)` producing tumbler `t'` such that:

  (a) `t' > t` (strictly greater under T1),

  (b) `t'` agrees with `t` on all components before the increment point,

  (c) when `k = 0` (*sibling*): `#t' = #t`, and `t'` differs from `t` only at position `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`,

  (d) when `k > 0` (*child*): `#t' = #t + k`, the `k - 1` intermediate positions `#t + 1, ..., #t + k - 1` are set to `0` (field separators), and the final position `#t + k` is set to `1` (the first child).

We verify `inc(t, k) > t` for both cases. For k = 0: `t'` agrees with `t` on positions `1, ..., sig(t) - 1` and exceeds `t` at position `sig(t)` (since `t_{sig(t)} + 1 > t_{sig(t)}`), so `t' > t` by T1 case (i). For k > 0: `t'` agrees with `t` on positions `1, ..., #t`, and `#t' > #t`, so `t` is a proper prefix of `t'`, giving `t < t'` by T1 case (ii).

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

When INSERT shifts text positions forward, link positions within the same document must not be affected. Text lives in element subspace 1; links live in element subspace 2. The shift must be *confined* to the subspace it applies to:

**TA7 (Subspace confinement).** Let `S₁` and `S₂` be distinct element subspaces within a document. A shift operation (addition or subtraction of width `w`) applied to a position in `S₁` produces a result in `S₁`, and no position in `S₂` is affected.

  `(A a ∈ S₁, w : a ⊕ w ∈ S₁)` and symmetrically for `⊖`.

  `(A b ∈ S₂ : b is unchanged by any shift within S₁)`

TA7 is a single abstract property, but Gregory's analysis reveals a striking asymmetry in how the two editing operations achieve it:

For **INSERT**, the implementation uses an explicit structural guard — a "two-blade knife" that computes the boundary between subspaces. The boundary tumbler is constructed by a four-step arithmetic computation: increment at the parent level, extract the fractional tail via `beheadtumbler`, subtract the tail's leading component, and increment at the next finer level. This produces the precise tumbler at which the next subspace begins (e.g., `2.1` for the link subspace boundary when inserting in text subspace `1.x`). Entries beyond this boundary are never passed to the addition operation. Confinement is achieved by *not calling* the arithmetic on cross-subspace entries.

For **DELETE**, the implementation relies on an incidental property of the subtraction algorithm. The routine `strongsub` contains an exponent guard that returns the minuend unchanged when the subtrahend has a smaller exponent. Since text widths (fractional V-positions, exponent ≤ -1) have smaller exponents than link positions (whole-number subspace identifiers, exponent = 0), subtracting a text width from a link position is a no-op. Confinement is achieved by an *accidental arithmetic property*, not by deliberate structural design.

The abstract specification does not prescribe either mechanism. TA7 states what must hold; how it is achieved is an implementation choice. But the asymmetry teaches us something important: **TA7 is one property, but each operation may require a different proof obligation.** An implementation that "corrects" the subtraction to handle cross-exponent operands would break DELETE's subspace isolation while leaving INSERT's intact. The abstract property is stable; the implementation strategies are fragile in different ways.


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

I-space addresses are compared (T1) and containment-tested (T6), but they are never shifted. The arithmetic operations TA0–TA4 do not apply to I-space addresses.

**V-space (virtual space)** uses tumblers as mutable document positions. The applicable properties are:

  - T1 (total order): positions are ordered by reading sequence
  - TA0–TA4 (arithmetic): positions shift on INSERT and DELETE
  - TA7 (subspace confinement): shifts respect subspace boundaries

V-space has no permanence guarantee. Nelson is explicit: "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing." V-positions run contiguously from 1 to the document's current length and are rearranged by every editing operation.

**T11 (Dual-space separation).** The permanence properties (T8, T9, T10) apply exclusively to I-space. The shift-arithmetic properties (TA0–TA4, TA7) apply exclusively to V-space. No operation shifts an I-space address. No operation claims permanence for a V-space position.

T11 is the architectural core. Links attach to I-space addresses and therefore survive editing. Editing operations modify V-space positions and therefore do not violate permanence. The two spaces share the same carrier set T and the same ordering T1, but their operational contracts are disjoint.

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

**V-space arithmetic.** The document's V-space maps positions to I-addresses. Initially, V-positions run `v₁ = 1` through `v₅ = 5` (single-component tumblers for simplicity). Now INSERT two characters at position 3 — the width is `w = [2]`. All V-positions at or above 3 shift forward:

  `v₃' = [3] ⊕ [2] = [5]`, `v₄' = [4] ⊕ [2] = [6]`, `v₅' = [5] ⊕ [2] = [7]`

**TA1 (Order preservation).** Before: `v₃ = [3] < v₄ = [4]`. After: `v₃' = [5] < v₄' = [6]`. The relative order is preserved.

**TA4 (Inverse).** DELETE the same two characters (width `[2]`): `v₃' ⊖ [2] = [5] ⊖ [2] = [3] = v₃`. Positions restore exactly. By the reverse-inverse corollary, `(v₃ ⊖ [2]) ⊕ [2] = ([3] ⊖ [2]) ⊕ [2] = [1] ⊕ [2] = [3] = v₃` — the symmetry holds.

The I-space addresses `a₁` through `a₅` are unchanged by all of this. T8 guarantees their permanence; T11 confirms that shift arithmetic applies only to V-space. The five characters are the same characters at the same I-addresses — only their arrangement in the document has changed.


## Formal summary

We collect the structure. The tumbler algebra is a tuple `(T, <, ⊕, ⊖, inc, fields, Z)` where `Z = {t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0)}` is the set of zero tumblers:

- `T` is the carrier set of finite sequences of non-negative integers, with unbounded components (T0)
- `<` is the lexicographic total order on `T` (T1), intrinsically computable (T2), with canonical representation (T3)
- The hierarchical parsing function `fields` extracts four-level containment (T4), yielding contiguous subtrees (T5); decidable containment (T6, corollary of T4) and element subspace disjointness (T7, corollary of T3 + T4) follow
- `T8–T10` establish permanence, forward allocation, and partition independence for I-space
- `T11` separates the I-space and V-space contracts
- `⊕` and `⊖` are order-preserving shift operations for V-space (TA0–TA3), with strict increase (TA-strict), mutually inverse (TA4)
- `inc` is hierarchical increment for allocation (TA5)
- Zero tumblers (all components zero, any length) are sentinels, not valid addresses (TA6); positivity is defined as having at least one nonzero component
- `TA7` confines shifts to their subspace
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
| TA0–TA4, TA-strict | INSERT/DELETE correctness, span non-emptiness (T12) |
| TA5 | Address allocation |
| TA6 | Sentinel and lower bound |
| TA7 | INSERT/DELETE subspace isolation |
| TA8 | 2D enfilade correctness |

Removing any independent property breaks a system-level guarantee. T6 and T7 are derived (corollaries of T4, T3 respectively) and are stated for emphasis, not as independent axioms — removing them from the list does not weaken the algebra, since their content follows from the remaining properties.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| T0 | Every component of a tumbler is unbounded — no maximum value exists | introduced |
| T1 | Tumblers are totally ordered by lexicographic comparison, with the prefix-less-than convention | introduced |
| T2 | Tumbler comparison is computable from the two addresses alone, examining at most min(#a, #b) components | introduced |
| T3 | Each tumbler has exactly one canonical representation; component-wise identity is both necessary and sufficient for equality | introduced |
| T4 | An I-space tumbler has at most three zero-valued components, partitioning it into four hierarchical fields (node, user, document, element) | introduced |
| T5 | The set of tumblers sharing a prefix forms a contiguous interval under T1 | introduced |
| T6 | Containment (same node, same account, same document family, structural subordination) is decidable from addresses alone | corollary of T4 |
| T7 | Subspaces (text, links) within a document's element field are permanently disjoint | corollary of T3 + T4 |
| T8 | Once a tumbler is assigned to content, the assignment is permanent and the content is immutable | introduced |
| T9 | Within a single allocator's sequential stream, new addresses are strictly monotonically increasing; gaps are permanent | introduced |
| T10 | Allocators with non-nesting prefixes produce distinct addresses without coordination | introduced |
| T11 | Permanence (T8–T10) applies to I-space; shift arithmetic (TA0–TA4, TA7) applies to V-space; the contracts are disjoint | introduced |
| T12 | A span (s, ℓ) with s ∈ T and ℓ ∈ T denotes the contiguous interval {t : s ≤ t < s ⊕ ℓ} | introduced |
| TA0 | Tumbler addition a ⊕ w is well-defined for positive width w | introduced |
| TA1 | Addition preserves the total order: a < b ⟹ a ⊕ w < b ⊕ w for w > 0 | introduced |
| TA-strict | Adding a positive displacement strictly advances: a ⊕ w > a for w > 0 | introduced |
| TA2 | Tumbler subtraction a ⊖ w is well-defined when a ≥ w | introduced |
| TA3 | Subtraction preserves the total order: a < b ⟹ a ⊖ w < b ⊖ w when both are defined | introduced |
| TA4 | Addition and subtraction are mutual inverses: (a ⊕ w) ⊖ w = a | introduced |
| TA5 | Hierarchical increment inc(t, k) produces t' > t: k=0 advances component at sig(t), k>0 extends by k positions with k−1 zero separators and final component 1 | introduced |
| TA6 | Every all-zero tumbler (any length) is less than every positive tumbler and is not a valid address; positivity means at least one nonzero component | introduced |
| TA7 | Shift operations applied within one subspace produce results in that subspace and do not affect other subspaces | introduced |
| TA8 | In 2D displacement arithmetic, V and I dimensions are operated on independently with no cross-dimensional combination | introduced |


## Open Questions

Must addition preserve order universally, or only when the position and width share the same hierarchical depth — and if the latter, what precondition must the system enforce to guarantee that only same-depth additions occur?

Can addition ever produce or consume a zero-valued component, and what constraint prevents a V-space shift from crossing a field boundary?

What algebraic property of the POOM mapping must hold for span intersection to be computable from the mapping alone, without enumerating individual positions?

Must allocation counter durability across crashes be a global-history property or only a per-session property — and what recovery mechanism restores monotonicity after a crash that loses the counter state?

Under what conditions, if any, must two successive shifts `(a ⊕ w₁) ⊕ w₂` equal a single shift `a ⊕ (w₁ ⊕ w₂)`, and what system invariant guarantees this when it is needed?

What minimal auxiliary structure must the system maintain to reconstruct version-derivation history, given that it is not decidable from addresses alone?

What must the system guarantee about the zero tumbler's interaction with span arithmetic — if a span endpoint is the zero sentinel, how must containment and intersection operations behave?
