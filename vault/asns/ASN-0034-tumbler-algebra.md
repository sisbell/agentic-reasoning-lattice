# ASN-0034: Tumbler Algebra

*2026-03-12*

We wish to understand what algebraic structure the Xanadu addressing system must possess. The system assigns every entity a permanent address — a *tumbler* — and requires these addresses to support comparison, containment testing, arithmetic for span computation and position advancement, and coordination-free allocation across a global network. We seek the minimal set of abstract properties that any correct implementation must provide, deriving each from design requirements rather than from any particular representation.

The approach is: state what the system must guarantee, then discover what properties of the address algebra are necessary and sufficient for those guarantees. We begin with the carrier set and work outward.

Nelson conceived this system as "the tumbler line" — a flat linearization of a hierarchical tree, yielding a total order on all addresses. Gregory implemented it as fixed-width sign-magnitude arithmetic over 16-digit mantissas. Between these two accounts we find the abstract algebra: what must hold for any correct implementation, regardless of representation.


## The carrier set

A tumbler is a finite sequence of non-negative integers. We write `t = d₁.d₂. ... .dₙ` where each `dᵢ ∈ ℕ` and `n ≥ 1`. The set of all tumblers is **T**. Nelson describes each component as a "digit" with "no upper limit" — the term is misleading, since each "digit" is an arbitrary-precision natural number, not a single decimal digit. The variable-length encoding ("humber") ensures small values are compact and large values expand as needed.

This gives us our first property:

**T0 (Unbounded components).** `(A t ∈ T, i : 1 ≤ i ≤ #t : (A M ∈ ℕ :: (E t' ∈ T :: t' agrees with t except t'.dᵢ > M)))`.

In words: for every tumbler and every component position, there exists a tumbler whose value at that position exceeds any given bound. The address space within any subtree is inexhaustible.

T0 is what separates the tumbler design from fixed-width addressing. Nelson: "New items may be continually inserted in tumbler-space while the other addresses remain valid." The word "continually" carries the weight — it means the process of creating new addresses never terminates. Between any two sibling addresses, the forking mechanism can always create children: "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right." Each daughter can have daughters without limit, and each digit is itself unbounded.

T0 is required doubly: each component is unbounded (unlimited siblings at any level) AND the number of components is unbounded (unlimited nesting depth). Together these make the address space infinite in two dimensions, which Nelson calls "finite but unlimited" — at any moment finitely many addresses exist, but there is no bound on how many can be created: "A span that contains nothing today may at a later time contain a million documents."

We observe that Gregory's implementation uses a fixed 16-digit mantissa of 32-bit unsigned integers, giving a large but finite representable range. When the allocation primitive `tumblerincrement` would exceed this range structurally (requiring a 17th digit), it detects the overflow and terminates fatally. The general addition routine `tumbleradd` silently wraps on digit-value overflow. Both behaviors violate T0. The abstract specification demands unbounded components; a correct implementation must either provide them or demonstrate that the reachable state space never exercises the bound. The comment `NPLACES 16 /* increased from 11 to support deeper version chains */` records that the original bound of 11 was concretely hit in practice — version chains deeper than 3–4 levels caused fatal crashes.


## The total order

We require a total order on T. Nelson describes the "tumbler line" as a single linear sequence: "In a sense the tumbler line is like the real line, i.e., the line of integers and all the numbers in between." The system maps a hierarchical tree — servers containing accounts containing documents containing elements — onto this flat line via depth-first traversal. The traversal inherently produces a total order: for any two nodes in a tree, depth-first traversal visits one before the other. The ordering rule is lexicographic:

**T1 (Lexicographic order).** For tumblers `a = a₁. ... .aₘ` and `b = b₁. ... .bₙ`, define `a < b` iff there exists `k ≥ 1` such that `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either:

  (i) `k ≤ min(m, n)` and `aₖ < bₖ`, or

  (ii) `k = m + 1 ≤ n` (that is, `a` is a proper prefix of `b`).

The prefix convention — a prefix is less than any proper extension — is what makes depth-first traversal work. The server address `2` is less than every address within server `2`'s subtree, because every such address extends the prefix `2` with further components. This means server `2`'s subtree begins immediately after `2` in the order and extends until some address whose first component exceeds `2`.

T1 gives a total order: for any `a, b ∈ T`, exactly one of `a < b`, `a = b`, `a > b` holds. This is a standard mathematical fact about lexicographic orderings on well-ordered alphabets — ℕ is well-ordered, so the lexicographic extension to finite sequences is total.

Nelson's assertion that the tumbler line is total — that two addresses are never incomparable — is architecturally load-bearing. Spans are defined as contiguous regions on the tumbler line: "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse." If two addresses were incomparable, the interval between them would be undefined, and the entire machinery of span-sets, link endsets, and content reference would collapse.

Nelson requires that comparison be self-contained — no index consultation needed:

**T2 (Intrinsic comparison).** The order relation T1 is computable from the two tumblers alone, without consulting any external data structure. The comparison examines at most `min(#a, #b)` component pairs.

The importance of T2 is operational: span containment tests, link search, and index traversal all reduce to tumbler comparison. If comparison required a lookup, these operations would depend on auxiliary state, and the system's decentralization guarantee would collapse — one could not determine whether an address falls within a span without access to the index that manages that span.

Gregory's implementation confirms T2. The comparison function `tumblercmp` delegates to `abscmp`, which performs a purely positional comparison: exponent first (a proxy for the number of leading zeros), then lexicographic mantissa slot-by-slot. No tree structure, no index, no external state is consulted.


## Canonical form

Equality of tumblers must mean component-wise identity. There must be no representation in which two distinct sequences of components denote the same abstract tumbler:

**T3 (Canonical representation).** `(A a, b ∈ T : a₁ = b₁ ∧ ... ∧ aₙ = bₙ ∧ #a = #b ≡ a = b)`.

If two tumblers have the same length and the same components at every position, they are the same tumbler. Conversely, if they differ in any component or in length, they are distinct. No normalization, no trailing-zero ambiguity, no exponent variation can create aliases.

Gregory's implementation achieves T3 through a normalization routine (`tumblerjustify`) that shifts leading zeros out of the mantissa and adjusts the exponent. After justification, the first mantissa element is nonzero (unless the tumbler is the zero tumbler), creating a unique representation for each value. A validation routine enforces the invariant — one branch labels the failure `"fucked up non-normalized"`; the frustration testifies to the difficulty.

Gregory's analysis reveals precisely what happens when T3 is violated. The comparison function begins with zero-detection: `iszerotumbler` checks only the first mantissa slot. An unnormalized tumbler with a leading zero and a nonzero digit buried at a later position is *misclassified as zero* — it never reaches the magnitude comparison logic. Two such tumblers representing different positive values compare as EQUAL to each other and to the genuine zero tumbler, producing ordering contradictions. Suppose `T₁` has `mantissa = [0, 0, 5, ...]` (logically positive) and `T₂` has `mantissa = [0, 7, ...]` (logically positive with different value). Both are misclassified as zero: `tumblercmp(T₁, T₂) = EQUAL` and `tumblercmp(T₁, 0) = EQUAL`, yet after normalization `T₁ ≠ T₂`. Transitivity of the total order is broken. T3 — maintained by normalization after every arithmetic operation — prevents this corruption.

T3 matters because address identity is load-bearing. If two representations could denote the same tumbler, equality tests might give false negatives, span containment checks might fail for addresses that should match, and the system might allocate a "new" address that is actually an alias for an existing one.


## Hierarchical structure

Tumblers encode a containment hierarchy. Nelson uses zero-valued components as structural delimiters:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents."

> "A tumbler address may have at most three zero digits... These are interpreted as the major dividers, and have lexical significance as punctuation."

We formalize this. Define a *field separator* as a component with value zero. An address tumbler has the form:

`t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`

where each `Nᵢ, Uⱼ, Dₖ, Eₗ > 0`. The four fields are:

- **Node field** `N₁. ... .Nₐ`: identifies the server. "The server address always begins with the digit 1, since all other servers are descended from it."
- **User field** `U₁. ... .Uᵦ`: identifies the account. "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore."
- **Document field** `D₁. ... .Dᵧ`: identifies the document and version. Nelson notes the boundary between base document and version is not syntactically marked — "the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation."
- **Element field** `E₁. ... .Eδ`: identifies the content element. The first component distinguishes the *subspace*: 1 for text content, 2 for links.

Not every tumbler need have all four fields. A tumbler with zero zeros addresses a node. One zero: a user account. Two zeros: a document. Three zeros: an element. The count of zero-valued components determines the specificity level.

**T4 (Hierarchical parsing).** Every tumbler `t ∈ T` used as an address contains at most three zero-valued components, appearing in order as field separators, and every non-separator component is strictly positive. Formally, if `t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`, then `(A i : 1 ≤ i ≤ α : Nᵢ > 0)`, `(A j : 1 ≤ j ≤ β : Uⱼ > 0)`, `(A k : 1 ≤ k ≤ γ : Dₖ > 0)`, `(A l : 1 ≤ l ≤ δ : Eₗ > 0)`. We call this the *positive-component constraint*: every component of every field is strictly positive. The function `fields(t)` that extracts the node, user, document, and element fields is well-defined and computable from `t` alone. Define `zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`. The count of zero-valued components uniquely determines the hierarchical level:

  - `zeros(t) = 0`: `t` is a node address (node field only),
  - `zeros(t) = 1`: `t` is a user address (node and user fields),
  - `zeros(t) = 2`: `t` is a document address (node, user, and document fields),
  - `zeros(t) = 3`: `t` is an element address (all four fields).

This correspondence is injective on levels: each level produces addresses with exactly one zero count, and each zero count corresponds to exactly one level. The correspondence depends on the positive-component constraint — zero components serve exclusively as field separators *because* no field component is zero. Without the positivity constraint, a tumbler like `[1, 0, 0, 3]` would have two zero-valued components but ambiguous parse: the second zero could be a separator or a zero-valued component within the user field. Since field components are strictly positive, zeros appear only as separators, the number of separators determines the number of fields, and the parse is unique.

A subtlety deserves emphasis: the hierarchy is *convention layered over flat arithmetic*, not enforcement by the algebra. Gregory's analysis reveals that the comparison, addition, subtraction, and increment operations treat every mantissa slot identically. There is no `isparent`, `isancestor`, or `ischild` primitive in the arithmetic layer. The algebra operates on flat sequences of non-negative integers; the hierarchical interpretation is projected onto those sequences by the allocation machinery and the field-parsing function `fields(t)`. This is a deliberate design choice. The arithmetic layer is kept flat so that comparison and span computation are simple, uniform operations with no parsing of semantic structure.

Hierarchy is constructed by the allocation machinery, not by the algebra. The `.0.` separator is produced when the allocation `depth` parameter equals 2 — creating a child at a *different hierarchical type* than its parent (e.g., an ACCOUNT creating a DOCUMENT). When creating a same-type child (DOCUMENT creating DOCUMENT = versioning), `depth = 1`, and no zero separator is introduced. Gregory confirms: there was even a bug where the first document under an account failed to receive its `.0.` separator — the convention had to be explicitly constructed by the allocator, not enforced by any algebraic invariant.


## Contiguous subtrees

T4, combined with the total order T1, gives us the property that makes spans work:

**T5 (Contiguous subtrees).** For any tumbler prefix `p`, the set `{t ∈ T : p ≼ t}` (where `≼` denotes "is a prefix of") forms a contiguous interval under T1:

  `[p ≼ a ∧ p ≼ c ∧ a ≤ b ≤ c ⟹ p ≼ b]`

*Proof.* From T1, if `p ≼ a` then `a` agrees with `p` on the first `#p` components. If `a ≤ b ≤ c` and both `a` and `c` share prefix `p`, then `b` must also share prefix `p`. We consider two cases.

*Case 1: `#b ≥ #p`.* If `b` diverged from `p` at some position `k ≤ #p`, then either `bₖ < pₖ` (contradicting `a ≤ b` since `aₖ = pₖ`) or `bₖ > pₖ` (contradicting `b ≤ c` since `cₖ = pₖ`). So `b` agrees with `p` on all `#p` positions, hence `p ≼ b`.

*Case 2: `#b < #p`.* Since `p ≼ a`, we have `#a ≥ #p > #b`, so `b` is shorter than `a`. By T1, `a ≤ b` requires a first divergence point `j ≤ #b` where `aⱼ < bⱼ` (since `a` cannot be a prefix of the shorter `b`). But `aⱼ = pⱼ` (because `j ≤ #b < #p` and `a` shares prefix `p`), so `bⱼ > pⱼ = cⱼ`. This contradicts `b ≤ c`, since `b` exceeds `c` at position `j` and they agree on all prior positions. ∎

This is Nelson's key insight: "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." T5 is what makes this true. A span between two endpoints under the same prefix captures exactly the addresses under that prefix between those endpoints — no addresses from unrelated subtrees can interleave.

Because the hierarchy is projected onto a flat line (T1), containment in the tree corresponds to contiguity on the line. Nelson: "A span may be visualized as a zone hanging down from the tumbler line — what is called in computer parlance a depth-first spanning tree." Every subtree maps to a contiguous range, and every contiguous range within a subtree stays within the subtree.


## Decidable containment

The total order T1 determines *sequence* (which address comes first). But the system also needs *containment* — does address `a` belong to account `b`? Is document `d₁` under the same server as document `d₂`? These are not ordering questions; they are prefix questions.

**Corollary T6 (Decidable containment).** For any two tumblers `a, b ∈ T`, the following are decidable from the addresses alone:

  (a) Whether `a` and `b` share the same node field.

  (b) Whether `a` and `b` share the same node and user fields.

  (c) Whether `a` and `b` share the same node, user, and document-lineage fields.

  (d) Whether the document field of `a` is a prefix of the document field of `b` (structural subordination within a document family).

T6 is a corollary: it follows immediately from T4 — we extract the relevant fields and compare. We state it separately because the decidability claim is load-bearing for decentralized operation, but it introduces no independent content beyond T4.

We must note what T6(d) does NOT capture. The document field records the *allocation hierarchy* — who baptised which sub-number — not the *derivation history*. Version `5.3` was allocated under document `5`, but this tells us nothing about which version's content was copied to create `5.3`. Nelson: "the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." Formal version-derivation requires the version graph, not just the address.

Nelson confirms that shared prefix means shared containing scope: "The owner of a given item controls the allocation of the numbers under it." The prefix IS the path from root to common ancestor. But he cautions: "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." Shared prefix guarantees containment and ownership, never semantic categorization.

Gregory's implementation confirms the distinction between ordering and containment. The codebase provides both `tumblercmp` (total order comparison) and `tumbleraccounteq` (prefix-matching predicate with zero-as-wildcard semantics). The latter truncates the candidate to the length of the parent and checks for exact match — this is the operational realization of T6, and it is a genuinely different algorithm from the ordering comparison.


## Subspace disjointness

Within a document's element space, the first component after the third zero delimiter identifies the *subspace*: 1 for text, 2 for links. Nelson also mentions that the link subspace "could be further subdivided." The critical property is permanent separation:

**Corollary T7 (Subspace disjointness).** The subspace identifier (the first component of the element field) permanently separates the address space into disjoint regions. No tumbler in subspace `s₁` can equal or be confused with a tumbler in subspace `s₂ ≠ s₁`.

  `(A a, b ∈ T : a.E₁ ≠ b.E₁ ⟹ a ≠ b)`

T7 is a corollary of T3 (canonical representation) and T4 (hierarchical parsing): if two tumblers differ in their first element-field component, they are distinct. We state it explicitly because it is load-bearing for the guarantee that operations within one content type do not interfere with another. T7 is the structural basis — arithmetic within subspace 1 cannot produce addresses in subspace 2, because the subspace identifier is part of the address, not metadata.

The ordering T1 places all text addresses (subspace 1) before all link addresses (subspace 2) within the same document, because `1 < 2` at the subspace position. This is a consequence, not an assumption — it falls out of the lexicographic order.


## Allocation permanence

The most consequential property of the address system is that once an address is allocated, it persists forever:

**T8 (Allocation permanence).** If tumbler `a ∈ T` has been allocated at any point in the system's history, then for all subsequent states, `a` remains in the set of allocated addresses. No operation removes an allocated address from the address space. The set of allocated addresses is monotonically non-decreasing.

Nelson: "any address of any document in an ever-growing network may be specified by a permanent tumbler address." The guarantee is about the address itself — its persistence, its permanent occupancy of its position on the tumbler line.

Even addresses that have no stored content are irrevocably claimed. Nelson calls these "ghost elements": "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." A ghost element occupies a position on the tumbler line, and that position cannot be reclaimed.

T8 is required for link stability (links reference addresses, which must remain valid), for transclusion identity (transcluded content maintains its address), and for attribution (the address encodes the originating server, user, and document, and this attribution cannot be revised). What a given address *maps to* — whether content, and what content — is a property of the mapping layer, not the algebra.


## Monotonic allocation

T8 tells us that addresses, once allocated, are permanent. We now ask: in what order are new addresses assigned?

**T9 (Forward allocation).** Each allocator in the system controls a single ownership prefix and allocates sequentially within it. Within that sequential stream, new addresses are strictly monotonically increasing:

  `(A a, b : same_allocator(a, b) ∧ allocated_before(a, b) : a < b)`

Nelson's design is explicitly sequential: "successive new digits to the right ... 2.1, 2.2, 2.3, 2.4 are successive items being placed under 2." The word "successive" carries the weight: 2.2 follows 2.1, never precedes it.

T9 prohibits gap-filling within a single allocator's stream. If address 2.3 was allocated and address 2.5 was allocated, then 2.4 either was allocated between them or is a permanent ghost. The system never goes back to fill 2.4 after allocating 2.5. Since T9 requires strictly monotonic advancement, the ghost address lies behind the allocation frontier permanently. It cannot be reused for new content; it is a permanent gap. Gaps are features, not defects.

But the tumbler line as a whole does NOT grow monotonically by creation time. Nelson: "Starting from a given tumbler address, it may only be possible arithmetically to get to some places in the Docuverse — those notationally after that address." When a parent address forks a child, the child is *inserted* between the parent and the parent's next sibling on the tumbler line. Address `2.1.1` may be created long after `2.2`, but it sits between them: `2.1 < 2.1.1 < 2.2`. The depth-first linearization means children always precede the parent's next sibling, regardless of creation order. T9 holds per-allocator, not globally.

We observe that T9 is scoped to a *single allocator's sequential stream*, not to arbitrary partitions. A server-level subtree spans multiple independent allocators (one per user). Those allocators operate concurrently — T10 below guarantees they need no coordination. If user A (prefix `1.0.1`) allocates at wall-clock time `t₂` and user B (prefix `1.0.2`) allocates at time `t₁ < t₂`, neither T9 nor any other property requires that A's address exceed B's. T9 applies within each user's allocation stream independently.

A consequence of T8 and T9 together: the set of allocated addresses is a *growing set* in the lattice-theoretic sense — it can only increase, and new elements always appear at the frontier of each allocator's domain.


## Coordination-free uniqueness

The tumbler hierarchy exists so that independent actors can allocate addresses without communicating:

**T10 (Partition independence).** The address space is partitioned by prefix into ownership domains. Two allocators with distinct, non-nesting prefixes can allocate simultaneously, and the resulting addresses are guaranteed distinct.

Formally: let `p₁` and `p₂` be prefixes such that neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for any tumbler `a` with prefix `p₁` and any tumbler `b` with prefix `p₂`, `a ≠ b`.

This follows from the definition: if `a` has prefix `p₁` and `b` has prefix `p₂`, and the prefixes diverge at some position `k` with `p₁ₖ ≠ p₂ₖ`, then `aₖ = p₁ₖ ≠ p₂ₖ = bₖ`, so `a ≠ b`. The proof is elementary, but the property is architecturally profound. Nelson: "The owner of a given item controls the allocation of the numbers under it." No central allocator is needed. No coordination protocol is needed. The address structure itself makes collision impossible.

Nelson: "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." Baptism is the mechanism by which ownership domains are established — the owner of a number creates sub-numbers beneath it, and those sub-numbers belong exclusively to the owner.

**T10a (Allocator discipline).** Each allocator produces its sibling outputs exclusively by repeated application of `inc(·, 0)` — shallow increment at the last significant position. To spawn a child allocator, the parent performs one `inc(·, k')` with `k' > 0` to establish the child's prefix, then delegates further allocation to the child. The parent's own sibling stream resumes with `inc(·, 0)`.

T10a constrains what would otherwise be an unregulated choice. Without it, an allocator could intermix shallow and deep increments, generating outputs of varying lengths. The constraint to `k = 0` for siblings is essential: since `inc(·, 0)` preserves length (TA5(c) below), all sibling outputs from a single allocator have the same length. This uniform-length property is what the partition monotonicity and global uniqueness proofs depend on. If an allocator used `k > 0` for siblings, successive outputs would have increasing lengths and each output would extend the previous — making successive siblings nest rather than stand disjoint. This nesting would break the non-nesting premise required by the Prefix Ordering Extension lemma below.

The `k > 0` operation is reserved exclusively for child-spawning: a single deep increment that establishes a new prefix at a deeper level, from which a new allocator continues with its own `inc(·, 0)` stream.

We first establish a lemma that converts ordering of prefixes into ordering of all addresses under those prefixes.

**Lemma (Prefix ordering extension).** Let `p₁, p₂ ∈ T` be tumblers such that `p₁ < p₂` and neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for every `a` extending `p₁` (`p₁ ≼ a`) and every `b` extending `p₂` (`p₂ ≼ b`), `a < b`.

*Proof.* Since `p₁ < p₂` and neither is a prefix of the other, T1 case (i) applies: there exists a position `k ≤ min(#p₁, #p₂)` such that `p₁` and `p₂` agree on positions `1, ..., k-1` and `p₁ₖ < p₂ₖ`. (Case (ii) is excluded because `p₁` is not a proper prefix of `p₂`.) Now `a` extends `p₁`, so `aᵢ = p₁ᵢ` for all `i ≤ #p₁`; in particular `aₖ = p₁ₖ`. Similarly `bₖ = p₂ₖ`. On positions `1, ..., k-1`, `aᵢ = p₁ᵢ = p₂ᵢ = bᵢ`. At position `k`, `aₖ = p₁ₖ < p₂ₖ = bₖ`. So `a < b` by T1 case (i). ∎

**Theorem (Partition monotonicity).** Within any prefix-delimited partition of the address space, the set of allocated addresses is totally ordered by T1, and this order is consistent with the allocation order of any single allocator within that partition.

*Proof.* Consider a partition with prefix `p`. Every allocated address in this partition has prefix `p`, hence lies in the contiguous interval guaranteed by T5. Within the partition, addresses belong to sub-partitions owned by distinct allocators. These sub-partitions have prefixes that are siblings — they share the parent prefix `p` but diverge at the component that distinguishes one allocator from another.

We claim that sibling prefixes are non-nesting. The first sub-partition prefix `t₀` is produced by `inc(parent, k)` with `k > 0`, giving `#t₀ = #parent + k` (by TA5(d)). By T10a, subsequent sibling prefixes are produced by `inc(·, 0)`: `t₁ = inc(t₀, 0)`, `t₂ = inc(t₁, 0)`, and so on. By TA5(c), `inc(t, 0)` preserves the length of `t`: `#inc(t, 0) = #t`. So all sibling prefixes have the same length `#t₀`. Two tumblers of the same length cannot stand in a prefix relationship unless they are equal (a proper prefix is strictly shorter). Since they differ at position `sig(t)` (TA5(c) increments that component), they are unequal, hence non-nesting.

Each allocator's output is monotonic (T9). The sub-partitions are ordered by their prefixes under T1. The prefix ordering extension lemma gives `a < b` for every address `a` under an earlier prefix and every address `b` under a later prefix. Within each sub-partition, allocation order matches address order by T9. ∎

**Theorem (Global uniqueness).** No two distinct allocations, anywhere in the system, at any time, produce the same address.

*Proof.* Consider allocations producing addresses `a` and `b` by distinct allocation events. Four cases arise.

*Case 1: Same allocator.* Both addresses are produced by the same allocator's sequential stream. T9 guarantees `a ≠ b` because allocation is strictly monotonic.

*Case 2: Different allocators at the same hierarchical level.* The allocators have prefixes `p₁` and `p₂` that are siblings — neither is a prefix of the other. T10 gives `a ≠ b` directly.

*Case 3: Different allocators with nesting prefixes and different zero counts.* One allocator's prefix nests within another's. But these allocators produce addresses with different zero counts: the node allocator produces addresses with `zeros = 1` (user-level), while the element allocator produces addresses with `zeros = 3`. By T4, different zero counts imply different field structure. If `#a ≠ #b`, then `a ≠ b` by T3 directly. If `#a = #b`, then `zeros(a) ≠ zeros(b)` means there exists a position where one is zero and the other nonzero — by T3, `a ≠ b`.

*Case 4: Different allocators with nesting prefixes and the same zero count.* This arises when a parent and child allocator both produce addresses at the same hierarchical level. By T10a, the parent allocator uses `inc(·, 0)` for all its sibling allocations. Its first output has some length `γ₁`; since `inc(·, 0)` preserves length (TA5(c)), all subsequent parent siblings have length `γ₁`. The child allocator's prefix was established by `inc(parent_output, k')` with `k' > 0`, giving prefix length `γ₁ + k'` (by TA5(d)). The child then uses `inc(·, 0)` for its own siblings — all its outputs have the uniform length `γ₁ + k'`. Since `k' ≥ 1`, the child's outputs are strictly longer than the parent's: `γ₁ + k' > γ₁`. By T3, `a ≠ b`.

The argument depends critically on T10a's constraint that sibling allocations use `k = 0`. If a parent allocator could use `k > 0` for siblings, its outputs would have increasing lengths, and some parent output could match the length of a child output, collapsing the length separation. ∎

This theorem is the foundation of the addressing architecture. Every subsequent guarantee — link stability, transclusion identity, royalty tracing — depends on the uniqueness of addresses. And uniqueness is achieved without any distributed consensus, simply by the structure of the names.


## Tumbler arithmetic

We now turn to the arithmetic operations. The system requires operations that advance a position by a displacement (for computing span endpoints and shifting positions) and that recover the displacement between two positions (for computing span widths). These operations — tumbler addition and subtraction — are not arithmetic on numbers but position-advance operations in a hierarchical address space.

A displacement `w` is a tumbler whose leading zeros say "stay at these hierarchical levels" and whose first nonzero component says "advance here." Components after the advance point describe the structure of the landing position within the target region.

### Addition for position advancement

Let `⊕` denote tumbler addition: given a start position `a` and a displacement `w`, compute the advanced position.

We require a notion of where a displacement "acts." For a positive displacement `w = [w₁, w₂, ..., wₙ]`, define the *action point* as `k = min({i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0})` — the position of the first nonzero component. The leading zeros say "stay at these hierarchical levels"; the first nonzero component says "advance here."

**TA0 (Well-defined addition).** For tumblers `a, w ∈ T` where `w > 0` and the action point `k` of `w` satisfies `k ≤ #a`, the result `a ⊕ w` is a well-defined tumbler in `T`.

The precondition `k ≤ #a` is essential: the constructive definition copies components `a₁, ..., aₖ₋₁` from the start position and adds `wₖ` to `aₖ`, so position `k` must exist within `a`. A displacement whose action point exceeds `#a` — one with more leading zeros than `a` has components — would attempt to "stay at" hierarchical levels that the start position does not have, and the operation is undefined.

**TA1 (Order preservation under addition).** `(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) : a ⊕ w ≤ b ⊕ w)`, where `k` is the action point of `w`.

TA1 guarantees weak (`≤`) order preservation universally — if two positions were in order before advancement, they remain in non-reversed order after. The precondition `k ≤ min(#a, #b)` inherits from TA0: both operations must be well-defined.

Strict order preservation holds under a tighter condition:

**TA1-strict (Strict order preservation).** `(A a, b, w : a < b ∧ w > 0 ∧ k ≥ divergence(a, b) : a ⊕ w < b ⊕ w)`, where `k` is the action point of `w` and `divergence(a, b)` is the first position at which `a` and `b` differ.

When the action point falls before the divergence — `k < divergence(a, b)` — both operands agree at position `k`, both get the same `wₖ` added, and both copy the same tail from `w` afterward. The original divergence is erased and the results are equal. For example, `a = [1, 3]`, `b = [1, 5]` (diverge at position 2), `w = [2]` (action point at position 1): `a ⊕ w = [3] = b ⊕ w`. Order degrades to equality, never reversal.

But TA1 alone does not guarantee that addition *advances* a position. It preserves relative order between two positions but is silent about the relationship between `a` and `a ⊕ w`. We need:

**TA-strict (Strict increase).** `(A a ∈ T, w > 0 : a ⊕ w > a)` (where `a ⊕ w` is well-defined, i.e., `k ≤ #a` per TA0).

Without TA-strict, the axioms admit a degenerate model in which `a ⊕ w = a` for all `a, w`. This no-op model satisfies TA0 (result is in T), TA1 (if `a < b` then `a < b` — the consequent is unchanged), and TA4 (`(a ⊕ w) ⊖ w = a ⊖ w = a` if subtraction is equally degenerate). Every axiom is satisfied, yet spans are empty — the interval `[s, s ⊕ ℓ)` collapses to `[s, s)`. TA-strict excludes this model and ensures that advancing by a positive displacement moves forward. T12 (span well-definedness) depends on this directly.

**Verification of TA-strict.** Let `k` be the action point of `w`. By the constructive definition (below), `(a ⊕ w)ᵢ = aᵢ` for `i < k`, and `(a ⊕ w)ₖ = aₖ + wₖ`. Since `k` is the action point, `wₖ > 0`, so `aₖ + wₖ > aₖ`. Positions `1` through `k - 1` agree; position `k` is strictly larger. By T1 case (i), `a ⊕ w > a`.

### Subtraction for width computation

Let `⊖` denote tumbler subtraction: given two positions, compute the displacement between them.

**TA2 (Well-defined subtraction).** For tumblers `a, w ∈ T` where `a ≥ w`, `a ⊖ w` is a well-defined tumbler in `T`.

**TA3 (Order preservation under subtraction, weak).** `(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w ≤ b ⊖ w)`.

**TA3-strict (Order preservation under subtraction, strict).** `(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b : a ⊖ w < b ⊖ w)`.

### Partial inverse

**TA4 (Partial inverse).** `(A a, w : w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊕ w) ⊖ w = a)`, where `k` is the action point of `w`.

The precondition has three parts. First, `k = #a` — the action point falls at the last component of `a`. This is necessary because addition replaces `a`'s trailing structure below the action point with `w`'s trailing structure (tail replacement, defined below). When `k < #a`, components `aₖ₊₁, ..., a_{#a}` are discarded by addition and cannot be recovered by subtraction. Concretely: `[1, 5] ⊕ [1, 3] = [2, 3]` (action point 1, position 2 replaced by `w`'s trailing `3`), then `[2, 3] ⊖ [1, 3] = [1, 3] ≠ [1, 5]`.

Second, `#w = k` — the displacement has no trailing components beyond the action point. When `#w > k`, the result acquires trailing components from `w` that were not present in `a`. The trailing `7` from `w` persists through subtraction: `[0, 5] ⊕ [0, 3, 7] = [0, 8, 7]`, then `[0, 8, 7] ⊖ [0, 3, 7]` yields `[0, 5, 7] ≠ [0, 5]`.

Third, `(A i : 1 ≤ i < k : aᵢ = 0)` — all components of `a` before the action point are zero. This ensures the subtraction's divergence-discovery mechanism finds the action point at the right position. If `a` has a nonzero component at some position `j < k`, then the result of addition has `rⱼ = aⱼ ≠ 0`, and the subtraction's divergence falls at `j`, not at `k`. Concretely: `[5, 3] ⊕ [0, 7] = [5, 10]`, then `[5, 10] ⊖ [0, 7]`: divergence at position 1, producing `[5, 10] ≠ [5, 3]`.

When all three conditions hold, recovery is exact. The restriction is not a deficiency but a precise statement of when the operations are inverses.

Gregory's analysis confirms that `⊕` and `⊖` are NOT inverses in general. The implementation's `absadd` is asymmetric: the first argument supplies the high-level prefix, the second supplies the low-level suffix. When `d = a ⊖ b` strips a common prefix (reducing the exponent), `b ⊕ d` puts the difference in the wrong operand position — `absadd`'s else branch discards the first argument entirely and returns the second. The operand-order asymmetry causes total information loss even before any digit overflow.

The reverse direction is equally necessary:

**Corollary (Reverse inverse).** `(A a, w : a ≥ w ∧ w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊖ w) ⊕ w = a)`, where `k` is the action point of `w`.

*Proof.* Let `y = a ⊖ w`. We verify the prerequisites for applying TA4 to `y`. Under the precondition `(A i : 1 ≤ i < k : aᵢ = 0)`, we have `aᵢ = wᵢ = 0` for all `i < k`, so the divergence falls at position `k`. The result `y` has: positions `i < k` zero, position `k` equal to `aₖ - wₖ`, and no components beyond `k` (since `k = #a`). So `#y = k`, `yᵢ = 0` for `i < k`, and `#w = k`. All preconditions for TA4 hold. By TA4, `(y ⊕ w) ⊖ w = y`. Suppose `y ⊕ w ≠ a`. Apply TA3-strict (the equal-length precondition holds: `#a = k = #(y ⊕ w)`). If `y ⊕ w > a`, then `(y ⊕ w) ⊖ w > a ⊖ w = y`, giving `y > y`, a contradiction. If `y ⊕ w < a`, then `(y ⊕ w) ⊖ w < a ⊖ w`, giving `y < y`, a contradiction. So `(a ⊖ w) ⊕ w = a`. ∎


### Constructive definition of ⊕ and ⊖

The axiomatic properties above state what `⊕` and `⊖` must satisfy. We now give a constructive definition that shows how they work. Tumbler addition is not arithmetic addition — it is a **position-advance operation**: given a start position `a` and a displacement `w`, compute where you land. The displacement encodes both the distance and the hierarchical level at which the advance occurs.

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

**Precondition:** `k ≤ m` — the displacement's action point must fall within the start position's length.

Three properties of this definition require explicit statement:

**No carry propagation.** The sum `aₖ + wₖ` at the action point is a single natural-number addition. There is no carry into position `k - 1`. This is why the operation is fast — constant time regardless of tumbler length.

**Tail replacement, not tail addition.** Components after the action point come entirely from `w`. The start position's components at positions `k + 1, ..., m` are discarded. `a ⊕ w` does not add corresponding components pairwise — it replaces the start's sub-structure with the displacement's sub-structure below the action point.

**The many-to-one property.** Because trailing components of `a` are discarded, distinct start positions can produce the same result:

```
[1, 1] ⊕ [0, 2]       = [1, 3]
[1, 1, 5] ⊕ [0, 2]    = [1, 3]
[1, 1, 999] ⊕ [0, 2]  = [1, 3]
```

This is correct and intentional: advancing to "the beginning of the next chapter" lands at the same place regardless of where you were within the current chapter.

**Definition (Tumbler subtraction).** Given an end position `a` and a displacement `w`, recover the start position. When the operands have different lengths, we conceptually zero-pad the shorter to the length of the longer before scanning for divergence. When `a = w` (no divergence exists after padding), the result is the zero tumbler of length `max(#a, #w)`: `a ⊖ w = [0, ..., 0]`. Otherwise, let `k` be the first position where `a` and `w` differ (treating missing components as zero):

```
         ⎧ 0             if i < k        (these levels matched — zero them)
rᵢ   =  ⎨ aₖ - wₖ      if i = k        (reverse the advance)
         ⎩ aᵢ           if i > k        (copy from end position)
```

The result has length `max(#a, #w)`.

**Precondition:** `a ≥ w` — when `a ≠ w`, at the divergence point (after zero-padding) `aₖ ≥ wₖ`.


### Verification of TA1 and TA1-strict

**Claim (TA1, weak).** If `a < b`, `w > 0`, and `k ≤ min(#a, #b)`, then `a ⊕ w ≤ b ⊕ w`.

**Claim (TA1-strict).** If additionally `k ≥ divergence(a, b)`, then `a ⊕ w < b ⊕ w`.

*Proof.* Let `j = divergence(a, b)` — the first position where `a` and `b` differ (`aⱼ < bⱼ` since `a < b`). Three cases arise.

*Case 1: `k < j`.* Both `a` and `b` agree at position `k` (since `k < j`), so `(a ⊕ w)ₖ = aₖ + wₖ = bₖ + wₖ = (b ⊕ w)ₖ`. At positions after `k`, both results copy from `w`, giving identical tails. So `a ⊕ w = b ⊕ w`. The weak form (`≤`) holds. The strict form does not — the original divergence is erased by tail replacement.

*Case 2: `k = j`.* At position `k`, `(a ⊕ w)ₖ = aₖ + wₖ < bₖ + wₖ = (b ⊕ w)ₖ` (since `aₖ < bₖ` and natural-number addition preserves strict inequality). Positions before `k` agree. So `a ⊕ w < b ⊕ w` strictly.

*Case 3: `k > j`.* For `i < k`, the constructive definition gives `(a ⊕ w)ᵢ = aᵢ` and `(b ⊕ w)ᵢ = bᵢ`. Since `j < k`, the divergence at position `j` is preserved: `(a ⊕ w)ⱼ = aⱼ < bⱼ = (b ⊕ w)ⱼ`. So `a ⊕ w < b ⊕ w` strictly. ∎

In all three cases, `a ⊕ w ≤ b ⊕ w`. Strict inequality holds in Cases 2 and 3, i.e., whenever `k ≥ j = divergence(a, b)`.


### Verification of TA3

The subtraction algorithm differs structurally from addition — it zeros positions before the divergence point and copies the tail from the minuend, whereas addition copies the tail from the displacement. We must verify TA3 directly.

**Claim (TA3, weak).** If `a < b`, `a ≥ w`, and `b ≥ w`, then `a ⊖ w ≤ b ⊖ w`.

*Proof.* We first handle the case where `a < b` by the prefix rule (T1 case (ii)), then the component-divergence cases.

*Case 0: `a` is a proper prefix of `b`.* Then `#a < #b` and `aᵢ = bᵢ` for all `i ≤ #a`. Under zero-padding, both subtractions produce the same result on positions `1, ..., max(#a, #w)` (since `a` and `b` agree on these positions). If `max(#a, #w) < max(#b, #w)`, then `a ⊖ w` is shorter than `b ⊖ w` and is a prefix of it — by T1 case (ii), `a ⊖ w < b ⊖ w`. If `max(#a, #w) = max(#b, #w)` and `b` has a nonzero component beyond `#a`, the component-divergence analysis below gives strict inequality. Otherwise the padded tumblers are identical, giving `a ⊖ w = b ⊖ w`. In either subcase, `a ⊖ w ≤ b ⊖ w`.

For the remaining cases, `a < b` by T1 case (i): there exists `j ≤ min(#a, #b)` with `aⱼ < bⱼ`. Let `dₐ = divergence(a, w)` and `d_b = divergence(b, w)` (under zero-padding).

*Case 1: `dₐ = d_b = d`.* For `i < d`, both results are zero. At position `d`, we need `j ≥ d` (since `a` and `b` agree with `w` before `d`). If `j = d`: `a_d - w_d < b_d - w_d`, so `a ⊖ w < b ⊖ w`. If `j > d`: `a_d = b_d`, so both results agree at `d`; at positions `d < i < j`, both copy from their respective minuends which agree; at position `j`, `aⱼ < bⱼ`. So `a ⊖ w < b ⊖ w`.

*Case 2: `dₐ < d_b`.* At position `dₐ`: `a_{dₐ} ≠ w_{dₐ}` but `b_{dₐ} = w_{dₐ}`. Since `a < b` and they agree with `w` before `dₐ`, we have `j = dₐ` with `a_{dₐ} < b_{dₐ} = w_{dₐ}`. But `a ≥ w` requires `a_{dₐ} ≥ w_{dₐ}` at the divergence — contradiction. This case is impossible under the preconditions.

*Case 3: `dₐ > d_b`.* At position `d_b`: `b_{d_b} ≠ w_{d_b}` but `a_{d_b} = w_{d_b}`. So `j = d_b` with `a_{d_b} = w_{d_b} < b_{d_b}`. The result `(a ⊖ w)_{d_b} = 0` and `(b ⊖ w)_{d_b} = b_{d_b} - w_{d_b} > 0`. So `a ⊖ w < b ⊖ w`. ∎

**Claim (TA3-strict).** If `a < b`, `a ≥ w`, `b ≥ w`, and `#a = #b`, then `a ⊖ w < b ⊖ w`.

*Proof.* The equal-length precondition eliminates Case 0 entirely — two tumblers of the same length cannot be in a prefix relationship unless equal, and `a < b` rules out equality. Only Cases 1–3 apply, all of which produce strict inequality. ∎


### Verification of TA4

**Claim.** `(a ⊕ w) ⊖ w = a` under the full precondition: `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`.

*Proof.* Let `k` be the action point of `w`. Since `k = #a`, the addition `a ⊕ w` produces a result `r` with: `rᵢ = aᵢ = 0` for `i < k` (by the zero-prefix condition), `rₖ = aₖ + wₖ`, and `rᵢ = wᵢ` for `i > k`. Crucially, there are no components of `a` beyond position `k` — the tail replacement discards nothing.

Now subtract `w` from `r`. The subtraction scans for the first divergence between `r` and `w`. For `i < k`: `rᵢ = 0 = wᵢ` (both are zero — `aᵢ` by the zero-prefix precondition, `wᵢ` by definition of action point). Two sub-cases arise at position `k`.

*Sub-case (i): `aₖ > 0`.* Then `rₖ = aₖ + wₖ > wₖ`, and the first divergence is at position `k`. The subtraction produces: positions `i < k` get zero, position `k` gets `rₖ - wₖ = aₖ`, and positions `i > k` copy from `r`, giving `rᵢ = wᵢ`. Since `k = #a` and `#w = k`, there are no trailing components. The result is `[0, ..., 0, aₖ] = a`. For valid addresses, T4's positive-component constraint guarantees `aₖ > 0`, so this sub-case always applies in the address context.

*Sub-case (ii): `aₖ = 0`.* Then `a` is a zero tumbler. The addition gives `rₖ = wₖ`. Since `#r = #w = k`, we have `r = w`. The subtraction `w ⊖ w` yields the zero tumbler of length `k`, which is `a`. ∎


## Increment for allocation

A separate operation, distinct from the shifting arithmetic, handles address allocation. When the system allocates a new address, it takes the highest existing address in a partition and produces the next one. This is not addition of a width; it is advancement of a counter at a specified hierarchical level.

We define the *last significant position* of a tumbler `t`. When `t` has at least one nonzero component, `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})` — the position of the last nonzero component. When every component is zero, `sig(t) = #t`.

For valid addresses, `sig(t)` falls within the last populated field. This is a consequence of T4's positive-component constraint: every field component is strictly positive, so the last component of the last field is nonzero, and `sig(t) = #t`. Therefore `inc(t, 0)` on a valid address increments the last component of the last field, modifying only within that field and preserving the hierarchical structure.

**TA5 (Hierarchical increment).** For tumbler `t ∈ T` and level `k ≥ 0`, there exists an operation `inc(t, k)` producing tumbler `t'` such that:

  (a) `t' > t` (strictly greater under T1),

  (b) `t'` agrees with `t` on all components before the increment point,

  (c) when `k = 0` (*sibling*): `#t' = #t`, and `t'` differs from `t` only at position `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`,

  (d) when `k > 0` (*child*): `#t' = #t + k`, the `k - 1` intermediate positions `#t + 1, ..., #t + k - 1` are set to `0` (field separators), and the final position `#t + k` is set to `1` (the first child).

We verify `inc(t, k) > t` for both cases. For `k = 0`: `t'` agrees with `t` on positions `1, ..., sig(t) - 1` and exceeds `t` at position `sig(t)`, so `t' > t` by T1 case (i). For `k > 0`: `t'` agrees with `t` on positions `1, ..., #t`, and `#t' > #t`, so `t` is a proper prefix of `t'`, giving `t < t'` by T1 case (ii).

Gregory's analysis reveals a critical distinction: `inc(t, 0)` does NOT produce the immediate successor of `t` in the total order. It produces the *next peer* at the same hierarchical depth — the smallest tumbler with the same length that is strictly greater than `t`. The gap between `t` and `inc(t, 0)` contains the entire subtree of `t`: all tumblers of the form `t.x₁. ... .xₘ` for any `m ≥ 1` and any `x₁ ≥ 0`. The true immediate successor in the total order is `t.0` — the zero-extension — by the prefix convention (T1 case (ii)). When `k > 0`, `inc(t, k)` produces the first child at depth `k` below `t`, which IS the immediate successor of `t` when `k = 1` and the first intermediate position is 0 (giving `t.0.1` — but this is `t.0` extended, not `t.0` itself). For address allocation, the distinction is harmless: allocation cares about advancing the counter past all existing addresses, not about visiting every point in the total order.

**TA5 preserves T4 when `zeros(t) + k - 1 ≤ 3`.** For `k = 0`: no zeros are added — `zeros(t') = zeros(t)`. For `k > 0`: `k - 1` zero-valued components are appended, so `zeros(t') = zeros(t) + k - 1`. T4 requires `zeros(t') ≤ 3`, giving the constraint `k ≤ 4 - zeros(t)`. When `t` is an element address (`zeros(t) = 3`), only `k = 1` is permitted. When `t` is a node address (`zeros(t) = 0`), `k ≤ 4`. The hierarchy itself enforces this: each zero introduces one new field, and the address format has exactly four fields with three separators.


## Zero tumblers and positivity

Under T3, the tumblers `[0]`, `[0, 0]`, `[0, 0, 0]`, etc., are *distinct* elements of T — they have different lengths. Under T1, they form a chain: `[0] < [0, 0] < [0, 0, 0] < ...` by the prefix rule. There is no single "zero tumbler"; there are infinitely many all-zero tumblers.

**Definition (Positive tumbler).** A tumbler `t ∈ T` is *positive*, written `t > 0`, iff at least one of its components is nonzero: `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`. A tumbler is a *zero tumbler* iff every component is zero: `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.

Every positive tumbler is greater than every zero tumbler under T1 — if `t` has a nonzero component at position `k`, then at position `k` either the zero tumbler has a smaller component (0 < tₖ) or has run out of components, either way placing it below `t`. The condition `w > 0` in TA0 and TA4 excludes all all-zero displacements regardless of length.

**TA6 (Zero tumblers).** No zero tumbler is a valid address — no all-zero tumbler designates content. Every zero tumbler is less than every positive tumbler under T1.

  `(A t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0) ⟹ t is not a valid address)`

Zero tumblers serve as *sentinels*: they mark uninitialized values, denote "unbounded" when used as span endpoints, and act as lower bounds.


## Subspace closure

When arithmetic advances a position within one element subspace, the result must remain in that subspace. Text positions must not cross into link space, and vice versa.

An element-local position within subspace `S` has two components: the subspace identifier `N` and the ordinal `x`. A natural first attempt at an element-local displacement is `w = [0, n]` — action point `k = 2`, preserving the subspace identifier and advancing the ordinal. Addition works: `[N, x] ⊕ [0, n] = [N, x + n]`, preserving the subspace. But subtraction exposes a subtlety: `[N, x] ⊖ [0, n]` finds the first divergence at position 1 (where `N ≠ 0`), not at position 2 where the intended action lies. The subtraction produces `[N - 0, x] = [N, x]` — a no-op. The abstract `⊖` cannot shift a position backward by a displacement that disagrees with the position at the subspace identifier.

Gregory's implementation reveals the resolution. The operands passed to the arithmetic during shifts are not full element-local positions; they are *within-subspace ordinals* — the second component alone. The subspace identifier is not an operand to the shift; it is structural context that determines *which* positions are subject to the shift. The arithmetic receives ordinals, not full positions.

**TA7a (Subspace closure).** The canonical representation for shift arithmetic is the *ordinal-only* formulation: a position in subspace `S` with identifier `N` and ordinal `x` is represented as the single-component tumbler `[x]` for arithmetic purposes, with `N` held as structural context. An element-local displacement is `w = [n]` with `n > 0`. In this formulation:

  `(A [x] ∈ S₁, n > 0 : [x] ⊕ [n] = [x + n] ∈ S₁)`

  `(A [x] ∈ S₁, n > 0, x ≥ n : [x] ⊖ [n] = [x - n] ∈ S₁ ∪ {[0]})`

The subspace identifier is context — it determines which positions are subject to the shift — not an operand to the arithmetic. Both operations produce genuine shifts in the ordinal-only view; the 2-component view gives a genuine shift for `⊕` but a vacuous closure for `⊖`. The ordinal-only formulation is adopted because, as the verification shows, applying `⊖` to full 2-component positions finds the divergence at the subspace identifier, producing a no-op rather than a genuine shift.

**Verification of TA7a.** In the ordinal-only formulation, the shift operates on `[x]` by `w = [n]`. The ordinal is a single-component tumbler with `#x = 1`, and the displacement has `#w = 1` with action point `k = 1`. For `⊕`: `([x] ⊕ [n])₁ = x + n`, a positive single-component tumbler. For `⊖`: the divergence is at position 1 (since `x ≥ n`); the result is `[x - n]`. When `x = n`, the result is `[0]`, a sentinel (TA6). In either case the result is a single-component non-negative tumbler — a valid within-subspace ordinal. The subspace identifier is never modified. TA7a holds.

The restriction to element-local displacements is necessary. An unrestricted displacement whose action point falls at the subspace-identifier position could produce an address in a different subspace — TA7a cannot hold for arbitrary `w`.


## What tumbler arithmetic is NOT

We must state explicitly what the tumbler algebra does not guarantee. These negative results constrain what an implementer may assume.

**The algebra is not a group.** There is no additive identity — the zero tumbler is a sentinel, not a neutral element for addition. There is no additive inverse for every element — subtraction is only defined when `a ≥ w`. The algebra is not closed under subtraction in general.

**Addition is not associative.** We do NOT require `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)`. The design has no need for associativity — shifts are applied as single operations, never composed from multiple smaller shifts. Gregory's implementation does not implement carry propagation in `tumbleradd` — it adds at most one digit position, then copies the remaining digits from one input. This makes the operation fast but non-associative for operands at different hierarchical levels.

**Addition is not commutative.** We do NOT require `a ⊕ b = b ⊕ a`. The operands play asymmetric roles: the first is a *position*, the second is a *displacement*. Swapping them is semantically meaningless. Gregory's `absadd` confirms: the first argument supplies the prefix, the second the suffix — the reverse call gives a different (and typically wrong) result.

**There is no multiplication or division.** Gregory's analysis of the complete codebase confirms: no `tumblermult`, no `tumblerdiv`, no scaling operation of any kind. The arithmetic repertoire is: add, subtract, increment, compare. Tumblers are *addresses*, not quantities. You don't multiply two file paths or divide an address by three.

**Tumbler differences are not counts.** Nelson is emphatic: "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." The difference between two addresses specifies *boundaries*, not *cardinality*. What lies between those boundaries depends on the actual population of the tree, which is dynamic and unpredictable. Between sibling addresses 3 and 7, document 5 might have arbitrarily many descendants — the span from 3 to 7 encompasses all of them, and their count is unknowable from the addresses alone. The arithmetic is an *addressing calculus*, not a *counting calculus*.

The absence of algebraic structure beyond a monotone shift is not a deficiency. It is the *minimum* that addressing requires. An ordered set with an order-preserving shift and an allocation increment is sufficient. Anything more would be unused machinery and unverified obligation.


## Spans

A span is a pair `(s, ℓ)` where `s ∈ T` is a start address and `ℓ ∈ T` is a length (a positive tumbler used as a displacement), denoting the contiguous range from `s` up to but not including `s ⊕ ℓ`. The form of `ℓ` depends on the hierarchical level at which the span operates, because the action point of `ℓ` must match the level of the start address `s`.

Nelson makes spans self-describing at every hierarchical level: "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server — or the entire docuverse." The "1-position convention" exploits T5: because subtrees are contiguous, a span whose start is a high-level prefix and whose length reaches to the next sibling captures exactly that subtree's content.

And a span may be empty — populated by nothing at present — yet valid: "A span that contains nothing today may at a later time contain a million documents." The range is determined by the endpoints; what is actually stored within that range is a question about the current state of the system, not about the tumbler algebra.

**T12 (Span well-definedness).** A span `(s, ℓ)` with `ℓ > 0` denotes the set `{t ∈ T : s ≤ t < s ⊕ ℓ}`. This set is contiguous under T1 — there is no tumbler between two members that is not itself a member.

Contiguity is definitional: the span is an interval `[s, s ⊕ ℓ)` in a totally ordered set, and intervals in total orders are contiguous. Non-emptiness follows from TA-strict: since `ℓ > 0`, TA0 gives `s ⊕ ℓ ∈ T`, and TA-strict gives `s ⊕ ℓ > s` directly. The interval `[s, s ⊕ ℓ)` is therefore non-empty — it contains at least `s` itself.

We reserve T5 for the distinct claim that *prefix-defined* sets are contiguous — a non-trivial property of the lexicographic order.


## Order structure: adjacency and interpolation

We have stated the abstract properties. We now ask: what is the order-theoretic structure of T under T1?

T is *not* dense. Every tumbler `t` and its zero-extension `t.0` form an adjacent pair: `t < t.0` by the prefix rule (T1 case ii), and no tumbler lies strictly between them. For suppose `t < x < t.0`. Since `t` is a prefix of `t.0`, T5 requires that `x` also extend prefix `t` — so `x = t.x₁. ... .xₖ` for some `k ≥ 1`. The smallest such extension is `t.0` (since `x₁ ≥ 0` and if `x₁ = 0` then `x ≥ t.0`), giving `x ≥ t.0`, a contradiction. Every tumbler has an immediate successor: its zero-extension. The ordering resembles a tree's depth-first traversal order, which has adjacent pairs at every branch point.

What T0 does provide is *interpolation between non-prefix-related tumblers*. Between any two tumblers that differ at a shared position — that is, neither is a prefix of the other — there exist arbitrarily many intermediate tumblers. Between `1.3` and `1.5`, we can place `1.4`, `1.3.1`, `1.3.2`, and so on — T0 guarantees we never exhaust the space of intermediate values. This is the property that makes allocation work: within a single hierarchical level, there is always room for the next sibling.

Nelson describes the whole system as designed for this inexhaustibility: "the docuverse is ... finite but unlimited." At any moment the tree has finitely many nodes. But it can always grow. The address space between any two non-adjacent addresses can absorb unlimited new content.

Gregory's implementation further restricts the representable values to a fixed 16-digit mantissa of 32-bit unsigned integers, introducing additional adjacencies beyond those inherent in the abstract order. At the maximum mantissa depth (16 components), tumblers differing by 1 in their last component are adjacent even in the abstract order. But the implementation also makes tumblers adjacent when they would have required a 17th component to interpolate between — the `strongsub` exponent guard and the `tumblerincrement` overflow check are the two points where this limitation surfaces explicitly. A correct implementation must demonstrate that allocation never drives the system into a region where this additional adjacency matters.


## Worked example

We instantiate the algebra on a concrete scenario. Server 1, user 3, document 2, text subspace. The document contains five characters at element addresses:

  `a₁ = 1.0.3.0.2.0.1.1`, `a₂ = 1.0.3.0.2.0.1.2`, `a₃ = 1.0.3.0.2.0.1.3`, `a₄ = 1.0.3.0.2.0.1.4`, `a₅ = 1.0.3.0.2.0.1.5`

**T4 (Hierarchical parsing).** Take `a₃ = 1.0.3.0.2.0.1.3`. The three zeros at positions 2, 4, 6 are the field separators. Node field: `[1]`. User field: `[3]`. Document field: `[2]`. Element field: `[1, 3]`. The first component of the element field is `1`, placing this address in the text subspace. Every non-separator component is strictly positive, confirming T4.

**T1 (Ordering).** We verify `a₁ < a₂ < a₃ < a₄ < a₅`. All five share the prefix `1.0.3.0.2.0.1` and diverge at position 8, where the values are `1, 2, 3, 4, 5` respectively. Lexicographic comparison at the divergence point confirms the order.

**T5 (Contiguous subtrees).** The prefix `p = 1.0.3.0.2` identifies all content in document 2. Any tumbler `b` with `a₁ ≤ b ≤ a₅` must share this prefix. If `b` diverged from `p` at some position `k ≤ 5`, then `bₖ ≠ pₖ`, but `a₁` and `a₅` agree with `p` at position `k`, so `bₖ < pₖ` would violate `a₁ ≤ b` and `bₖ > pₖ` would violate `b ≤ a₅`. So `b` extends prefix `p` — it belongs to document 2.

**T6 (Decidable containment).** Do `a₃` and `a₅` belong to the same account? Extract user fields: both `[3]` under node `[1]`. Yes. Are they in the same document? Document fields: both `[2]`. Yes. Is `a₃` in the same document family as an address in document `2.1` (a version)? The document field `[2]` is a prefix of `[2, 1]`, so T6(d) confirms structural subordination.

**T7 (Subspace disjointness).** The document also contains a link at `ℓ₁ = 1.0.3.0.2.0.2.1`. Element field: `[2, 1]` — first component is `2`, placing this in the link subspace. By T7, `ℓ₁ ≠ aᵢ` for all `i` — the subspace identifiers differ.

**T9 (Forward allocation).** The five text addresses were allocated by a single allocator (user 3's element allocator within document 2, text subspace). Each address exceeds its predecessor: `a₁ < a₂ < a₃ < a₄ < a₅`. No gap-filling occurred.

**TA5 (Increment).** Allocating the sixth character: `inc(a₅, 0)`. Position `sig(a₅) = 8` (the last nonzero component). TA5(c): `a₆ = 1.0.3.0.2.0.1.6`. This preserves `#a₆ = #a₅ = 8` and differs only at position 8: `6 = 5 + 1`. By TA5(a), `a₆ > a₅`.

**T12 (Span computation).** The addresses `a₂` through `a₄` form a natural span — three consecutive elements. We construct `(s, ℓ)` with `s = a₂ = 1.0.3.0.2.0.1.2`. An element-level displacement must have action point `k = 8`: `ℓ = [0, 0, 0, 0, 0, 0, 0, 3]`. By the constructive definition of `⊕`: positions 1–7 copy from `s` (giving `1.0.3.0.2.0.1`), position 8 advances: `2 + 3 = 5`. So `s ⊕ ℓ = 1.0.3.0.2.0.1.5 = a₅`. The span denotes `{t : a₂ ≤ t < a₅} = {a₂, a₃, a₄}`. A single-component length `[3]` would give the wrong result: action point `k = 1`, and `a₂ ⊕ [3] = [4]` — a node-level address. The action point of the span length must match the hierarchical level of the start address.

**TA7a (Subspace closure).** Consider advancing text position ordinal `[3]` by displacement `[2]`: `[3] ⊕ [2] = [5]`. The result is a single-component ordinal — it remains within the text subspace. The subspace identifier `1` is held as context, unchanged. Subtracting: `[5] ⊖ [2] = [3]`. Recovery is exact (TA4 applies: `k = 1 = #a = #w`, zero-prefix condition vacuously satisfied).


## Formal summary

We collect the structure. The tumbler algebra is a tuple `(T, <, ⊕, ⊖, inc, fields, Z)` where `Z = {t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0)}` is the set of zero tumblers:

- `T` is the carrier set of finite sequences of non-negative integers, with unbounded components (T0)
- `<` is the lexicographic total order on `T` (T1), intrinsically computable (T2), with canonical representation (T3)
- The hierarchical parsing function `fields` extracts four-level containment (T4), yielding contiguous subtrees (T5); decidable containment (T6, corollary of T4) and element subspace disjointness (T7, corollary of T3 + T4) follow
- `T8` establishes allocation permanence — once allocated, an address is never removed from the set of allocated addresses
- `T9–T10` establish forward allocation and partition independence; `T10a` constrains each allocator to use `inc(·, 0)` for sibling outputs, reserving `k > 0` exclusively for child-spawning
- `⊕` and `⊖` are order-preserving operations on T (TA0–TA3, with TA0 requiring `k ≤ #a`), with weak order preservation universally (TA1 `≤`, TA3 `≤`) and strict preservation under tighter conditions (TA1-strict when `k ≥ divergence(a,b)`, TA3-strict when `#a = #b`); strict increase (TA-strict); partially inverse when `k = #a`, `#w = k`, and all components of `a` before `k` are zero (TA4)
- `inc` is hierarchical increment for allocation (TA5)
- Zero tumblers (all components zero, any length) are sentinels, not valid addresses (TA6); positivity is defined as having at least one nonzero component
- `TA7a` confines element-local shifts to their subspace (algebraic closure)
- Spans are self-describing contiguous ranges (T12)

Each property is required by at least one system guarantee:

| Property | Required by |
|----------|-------------|
| T0 | Unbounded growth of docuverse |
| T1, T2 | Span containment, link search, index traversal |
| T3 | Address identity, uniqueness, total order consistency |
| T4, T5 | Hierarchical queries, self-describing spans |
| T6 *(corollary of T4)* | Decidable containment |
| T7 *(corollary of T3 + T4)* | Subspace isolation |
| T8 | Link stability, transclusion identity, attribution |
| T9 | Per-allocator monotonicity; partition monotonicity derived from T9 + T10 + T1 |
| T10, T10a | Decentralized allocation, global uniqueness |
| T12 | Content reference by span |
| TA0–TA4, TA-strict | Span computation, position advancement, span non-emptiness (T12) |
| TA5 | Address allocation |
| TA6 | Sentinel and lower bound |
| TA7a | Subspace isolation (algebraic closure) |

Removing any independent property breaks a system-level guarantee. T6 and T7 are derived (corollaries of T4, T3 respectively) and are stated for emphasis, not as independent axioms.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| T0 | Every component of a tumbler is unbounded — no maximum value exists | introduced |
| T1 | Tumblers are totally ordered by lexicographic comparison, with the prefix-less-than convention | introduced |
| T2 | Tumbler comparison is computable from the two addresses alone, examining at most min(#a, #b) components | introduced |
| T3 | Each tumbler has exactly one canonical representation; component-wise identity is both necessary and sufficient for equality | introduced |
| T4 | An address tumbler has at most three zero-valued components as field separators, with every field component strictly positive (positive-component constraint), partitioning it into four hierarchical fields | introduced |
| T5 | The set of tumblers sharing a prefix forms a contiguous interval under T1 | introduced |
| T6 | Containment (same node, same account, same document family, structural subordination) is decidable from addresses alone | corollary of T4 |
| T7 | Subspaces (text, links) within a document's element field are permanently disjoint | corollary of T3 + T4 |
| T8 | Once allocated, an address is never removed from the address space; the set of allocated addresses is monotonically non-decreasing | introduced |
| T9 | Within a single allocator's sequential stream, new addresses are strictly monotonically increasing; gaps are permanent | introduced |
| T10 | Allocators with non-nesting prefixes produce distinct addresses without coordination | introduced |
| T10a | Each allocator uses inc(·, 0) for siblings and inc(·, k>0) only for child-spawning; this constrains sibling outputs to uniform length | introduced |
| T12 | A span (s, ℓ) with s ∈ T and ℓ > 0 denotes the contiguous interval {t : s ≤ t < s ⊕ ℓ}, which is non-empty by TA-strict | introduced |
| TA0 | Tumbler addition a ⊕ w is well-defined when w > 0 and the action point k satisfies k ≤ #a | introduced |
| TA1 | Addition preserves the total order (weak): a < b ⟹ a ⊕ w ≤ b ⊕ w | introduced |
| TA1-strict | Addition preserves the total order (strict) when k ≥ divergence(a, b) | introduced |
| TA-strict | Adding a positive displacement strictly advances: a ⊕ w > a | introduced |
| TA2 | Tumbler subtraction a ⊖ w is well-defined when a ≥ w | introduced |
| TA3 | Subtraction preserves the total order (weak): a < b ⟹ a ⊖ w ≤ b ⊖ w when both are defined | introduced |
| TA3-strict | Subtraction preserves the total order (strict) when additionally #a = #b | introduced |
| TA4 | Addition and subtraction are partial inverses: (a ⊕ w) ⊖ w = a when k = #a, #w = k, and all components of a before k are zero | introduced |
| TA5 | Hierarchical increment inc(t, k) produces t' > t: k=0 advances at sig(t), k>0 extends by k positions with separators and first child | introduced |
| TA6 | Every all-zero tumbler (any length) is less than every positive tumbler and is not a valid address | introduced |
| TA7a | For element-local displacements in ordinal-only formulation, shift operations applied within one subspace produce results in that same subspace | introduced |


## Open Questions

What constraints must an implementation's representable range satisfy to ensure that no reachable allocation state exceeds the representation — can these constraints be stated as a finite-model property of the abstract algebra?

Must allocation counter durability across crashes be a global-history property or only a per-session property, and what recovery mechanism restores monotonicity after a crash that loses the counter state?

What minimal auxiliary structure must the system maintain to reconstruct version-derivation history, given that it is not decidable from addresses alone (T6(d))?

What must the system guarantee about the zero tumbler's interaction with span arithmetic — if a span endpoint is the zero sentinel, how must containment and intersection operations behave?

Under what conditions can shift composition hold — when does `(a ⊕ w₁) ⊕ w₂ = a ⊕ (w₁ ⊕ w₂)` — and what system guarantees depend on the answer?
