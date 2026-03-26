# ASN-0034 Formal Statements

*Source: ASN-0034-tumbler-algebra.md (revised 2026-03-25) — Extracted: 2026-03-26*

## T0(a) — Every component value of a tumbler is unbounded

In words: for every tumbler and every component position, there exists a tumbler whose value at that position exceeds any given bound. The address space within any subtree is inexhaustible.

## T0(b) — Tumblers of arbitrary length exist in T

In words: there is no maximum tumbler length — for every bound, a tumbler of at least that length exists in T. The hierarchy has unlimited nesting depth. T0(b) follows from T's definition as the set of all finite sequences over ℕ — for any `n`, the constant sequence `[1, 1, ..., 1]` of length `n` is a member. We state it explicitly because it carries independent architectural weight: T0(a) ensures siblings within a level are inexhaustible, while T0(b) ensures levels themselves are inexhaustible.

T0 is what separates the tumbler design from fixed-width addressing. Nelson: "New items may be continually inserted in tumbler-space while the other addresses remain valid." The word "continually" carries the weight — it means the process of creating new addresses never terminates. Between any two sibling addresses, the forking mechanism can always create children: "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right." Each daughter can have daughters without limit, and each digit is itself unbounded.

The address space is unbounded in two dimensions: T0(a) ensures each component is unbounded (unlimited siblings at any level) and T0(b) ensures the number of components is unbounded (unlimited nesting depth). Together they make the address space infinite in both dimensions, which Nelson calls "finite but unlimited" — at any moment finitely many addresses exist, but there is no bound on how many can be created: "A span that contains nothing today may at a later time contain a million documents."

We observe that Gregory's implementation uses a fixed 16-digit mantissa of 32-bit unsigned integers, giving a large but finite representable range. When the allocation primitive `tumblerincrement` would exceed this range structurally (requiring a 17th digit), it detects the overflow and terminates fatally. The general addition routine `tumbleradd` silently wraps on digit-value overflow. Both behaviors violate T0. The abstract specification demands unbounded components; a correct implementation must either provide them or demonstrate that the reachable state space never exercises the bound. The comment `NPLACES 16 /* increased from 11 to support deeper version chains */` records that the original bound of 11 was concretely hit in practice — version chains deeper than 3–4 levels caused fatal crashes.


### The total order

We require a total order on T. Nelson describes the "tumbler line" as a single linear sequence: "In a sense the tumbler line is like the real line, i.e., the line of integers and all the numbers in between." The system maps a hierarchical tree — servers containing accounts containing documents containing elements — onto this flat line via depth-first traversal. The traversal inherently produces a total order: for any two nodes in a tree, depth-first traversal visits one before the other. The ordering rule
[...truncated...]

## T1 — Tumblers are totally ordered by lexicographic comparison, with the prefix-les...

(i) `k ≤ min(m, n)` and `aₖ < bₖ`, or

  (ii) `k = m + 1 ≤ n` (that is, `a` is a proper prefix of `b`).

The prefix convention — a prefix is less than any proper extension — is what makes depth-first traversal work. The server address `2` is less than every address within server `2`'s subtree, because every such address extends the prefix `2` with further components. This means server `2`'s subtree begins immediately after `2` in the order and extends until some address whose first component exceeds `2`.

T1 gives a total order: for any `a, b ∈ T`, exactly one of `a < b`, `a = b`, `a > b` holds. This is a standard mathematical fact about lexicographic orderings on well-ordered alphabets — ℕ is well-ordered, so the lexicographic extension to finite sequences is total.

Nelson's assertion that the tumbler line is total — that two addresses are never incomparable — is architecturally load-bearing. Spans are defined as contiguous regions on the tumbler line: "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse." If two addresses were incomparable, the interval between them would be undefined, and the entire machinery of span-sets, link endsets, and content reference would collapse.

Nelson requires that comparison be self-contained — no index consultation needed:

## T2 — Tumbler comparison is computable from the two addresses alone, examining at m...

The importance of T2 is operational: span containment tests, link search, and index traversal all reduce to tumbler comparison. If comparison required a lookup, these operations would depend on auxiliary state, and the system's decentralization guarantee would collapse — one could not determine whether an address falls within a span without access to the index that manages that span.

Gregory's implementation confirms T2. The comparison function `tumblercmp` delegates to `abscmp`, which performs a purely positional comparison: exponent first (a proxy for the number of leading zeros), then lexicographic mantissa slot-by-slot. No tree structure, no index, no external state is consulted.


### Canonical form

Equality of tumblers must mean component-wise identity. There must be no representation in which two distinct sequences of components denote the same abstract tumbler:

## T3 — Each tumbler has exactly one canonical representation; component-wise identit...

If two tumblers have the same length and the same components at every position, they are the same tumbler. Conversely, if they differ in any component or in length, they are distinct. No normalization, no trailing-zero ambiguity, no exponent variation can create aliases.

Gregory's implementation achieves T3 through a normalization routine (`tumblerjustify`) that shifts leading zeros out of the mantissa and adjusts the exponent. After justification, the first mantissa element is nonzero (unless the tumbler is the zero tumbler), creating a unique representation for each value. A validation routine enforces the invariant — one branch labels the failure `"fucked up non-normalized"`; the frustration testifies to the difficulty.

Gregory's analysis reveals precisely what happens when T3 is violated. The comparison function begins with zero-detection: `iszerotumbler` checks only the first mantissa slot. An unnormalized tumbler with a leading zero and a nonzero digit buried at a later position is *misclassified as zero* — it never reaches the magnitude comparison logic. Two such tumblers representing different positive values compare as EQUAL to each other and to the genuine zero tumbler, producing ordering contradictions. Suppose `T₁` has `mantissa = [0, 0, 5, ...]` (logically positive) and `T₂` has `mantissa = [0, 7, ...]` (logically positive with different value). Both are misclassified as zero: `tumblercmp(T₁, T₂) = EQUAL` and `tumblercmp(T₁, 0) = EQUAL`, yet after normalization `T₁ ≠ T₂`. Transitivity of the total order is broken. T3 — maintained by normalization after every arithmetic operation — prevents this corruption.

T3 matters because address identity is load-bearing. If two representations could denote the same tumbler, equality tests might give false negatives, span containment checks might fail for addresses that should match, and the system might allocate a "new" address that is actually an alias for an existing one.


### Hierarchical structure

Tumblers encode a containment hierarchy. Nelson uses zero-valued components as structural delimiters:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents."

> "A tumbler address may have at most three zero digits... These are interpreted as the major dividers, and have lexical significance as punctuation."

We formalize this. Define a *field separator* as a component with value zero. An address tumbler has the form:

`t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`

where each `Nᵢ, Uⱼ, Dₖ, Eₗ > 0`. The four fields are:

- **Node field** `N₁. ... .Nₐ`: identifies the server. "The server address always begins with the digit 1, since all other servers are descended from it."
- **User field** `U₁. ... .Uᵦ`: identifies the account. "Typically, the user will have no control over the
[...truncated...]

## T4 — An address tumbler has at most three zero-valued components as field separato...

- `zeros(t) = 0`: `t` is a node address (node field only),
  - `zeros(t) = 1`: `t` is a user address (node and user fields),
  - `zeros(t) = 2`: `t` is a document address (node, user, and document fields),
  - `zeros(t) = 3`: `t` is an element address (all four fields).

This correspondence is injective on levels: each level produces addresses with exactly one zero count, and each zero count corresponds to exactly one level. The correspondence depends on the positive-component constraint — zero components serve exclusively as field separators *because* no field component is zero. Without the positivity constraint, a tumbler like `[1, 0, 0, 3]` would have two zero-valued components but ambiguous parse: the second zero could be a separator or a zero-valued component within the user field. Since field components are strictly positive, zeros appear only as separators, the number of separators determines the number of fields, and the parse is unique.

A subtlety deserves emphasis: the hierarchy is *convention layered over flat arithmetic*, not enforcement by the algebra. Gregory's analysis reveals that the comparison, addition, subtraction, and increment operations treat every mantissa slot identically. There is no `isparent`, `isancestor`, or `ischild` primitive in the arithmetic layer. The algebra operates on flat sequences of non-negative integers; the hierarchical interpretation is projected onto those sequences by the allocation machinery and the field-p
[...truncated...]

## T5 — The set of tumblers sharing a prefix forms a contiguous interval under T1

`[p ≼ a ∧ p ≼ c ∧ a ≤ b ≤ c ⟹ p ≼ b]`

*Proof.* From T1, if `p ≼ a` then `a` agrees with `p` on the first `#p` components. If `a ≤ b ≤ c` and both `a` and `c` share prefix `p`, then `b` must also share prefix `p`. We consider two cases.

*Case 1: `#b ≥ #p`.* If `b` diverged from `p` at some position `k ≤ #p`, then either `bₖ < pₖ` (contradicting `a ≤ b` since `aₖ = pₖ`) or `bₖ > pₖ` (contradicting `b ≤ c` since `cₖ = pₖ`). So `b` agrees with `p` on all `#p` positions, hence `p ≼ b`.

*Case 2: `#b < #p`.* Since `p ≼ a`, we have `#a ≥ #p > #b`, so `b` is shorter than `a`. By T1, `a ≤ b` requires a first divergence point `j ≤ #b` where `aⱼ < bⱼ` (since `a` cannot be a prefix of the shorter `b`). But `aⱼ = pⱼ` (because `j ≤ #b < #p` and `a` shares prefix `p`), so `bⱼ > pⱼ = cⱼ`. This contradicts `b ≤ c`, since `b` exceeds `c` at position `j` and they agree on all prior positions. ∎

This is Nelson's key insight: "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." T5 is what makes this true. A span between two endpoints under the same prefix captures exactly the addresses under that prefix between those endpoints — no addresses from unrelated subtrees can interleave.

Because the hierarchy is projected onto a flat line (T1), containment in the tree corresponds to contiguity on the line. Nelson: "A span may be visualized as a zone hanging down from the tumbler line — what is called in computer parlance a depth-first spanning tree." Every subtree maps to a contiguous range, and every contiguous range within a subtree stays within the subtree.


### Decidable containment

The total order T1 determines *sequence* (which address comes first). But the system also needs *containment* — does address `a` belong to account `b`? Is document `d₁` under the same server as document `d₂`? These are not ordering questions; they are prefix questions.

## T6 — Containment (same node, same account, same document family, structural subord...

(a) Whether `a` and `b` share the same node field.

  (b) Whether `a` and `b` share the same node and user fields.

  (c) Whether `a` and `b` share the same node, user, and document-lineage fields.

  (d) Whether the document field of `a` is a prefix of the document field of `b` (structural subordination within a document family).

T6 is a corollary: it follows immediately from T4 — we extract the relevant fields and compare. We state it separately because the decidability claim is load-bearing for decentralized operation, but it introduces no independent content beyond T4.

We must note what T6(d) does NOT capture. The document field records the *allocation hierarchy* — who baptised which sub-number — not the *derivation history*. Version `5.3` was allocated under document `5`, but this tells us nothing about which version's content was copied to create `5.3`. Nelson: "the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." Formal version-derivation requires the version graph, not just the address.

Nelson confirms that shared prefix means shared containing scope: "The owner of a given item controls the allocation of the numbers under it." The prefix IS the path from root to common ancestor. But he cautions: "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." Shared prefix guarantees containment and ownership, never semantic categorization.

Gregory's implementation confirms the distinction between ordering and containment. The codebase provides both `tumblercmp` (total order comparison) and `tumbleraccounteq` (prefix-matching predicate with zero-as-wildcard semantics). The latter truncates the candidate to the length of the parent and checks for exact match — this is the operational realization of T6, and it is a genuinely different algorithm from the ordering comparison.


### Subspace disjointness

Within a document's element space, the first component after the third zero delimiter identifies the *subspace*: 1 for text, 2 for links. Nelson also mentions that the link subspace "could be further subdivided." The critical property is permanent separation:

## T7 — Subspaces (text, links) within a document's element field are permanently dis...

`(A a, b ∈ T : a.E₁ ≠ b.E₁ ⟹ a ≠ b)`

T7 is a corollary of T3 (canonical representation) and T4 (hierarchical parsing): if two tumblers differ in their first element-field component, they are distinct. We state it explicitly because it is load-bearing for the guarantee that operations within one content type do not interfere with another. T7 is the structural basis — arithmetic within subspace 1 cannot produce addresses in subspace 2, because the subspace identifier is part of the address, not metadata.

The ordering T1 places all text addresses (subspace 1) before all link addresses (subspace 2) within the same document, because `1 < 2` at the subspace position. This is a consequence, not an assumption — it falls out of the lexicographic order.


### Allocation permanence

The most consequential property of the address system is that once an address is allocated, it persists forever:

## T8 — Once allocated, an address is never removed from the address space; the set o...

Nelson: "any address of any document in an ever-growing network may be specified by a permanent tumbler address." The guarantee is about the address itself — its persistence, its permanent occupancy of its position on the tumbler line.

Even addresses that have no stored content are irrevocably claimed. Nelson calls these "ghost elements": "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." A ghost element occupies a position on the tumbler line, and that position cannot be reclaimed.

T8 is required for link stability (links reference addresses, which must remain valid), for transclusion identity (transcluded content maintains its address), and for attribution (the address encodes the originating server, user, and document, and this attribution cannot be revised). What a given address *maps to* — whether content, and what content — is a property of the mapping layer, not the algebra.


### Monotonic allocation

T8 tells us that addresses, once allocated, are permanent. We now ask: in what order are new addresses assigned?

## T9 — Within a single allocator's sequential stream, new addresses are strictly mon...

`(A a, b : same_allocator(a, b) ∧ allocated_before(a, b) : a < b)`

Nelson's design is explicitly sequential: "successive new digits to the right ... 2.1, 2.2, 2.3, 2.4 are successive items being placed under 2." The word "successive" carries the weight: 2.2 follows 2.1, never precedes it. Under T10a, no gaps arise within a single allocator's sibling stream — each address is exactly one increment beyond the previous.

Positions on the tumbler line that have been allocated but have no stored content are what Nelson calls "ghost elements" (T8 above). Ghosts are about absent content, not absent addresses — every allocated position is permanently claimed whether or not anything is stored there.

But the tumbler line as a whole does NOT grow monotonically by creation time. Nelson: "Starting from a given tumbler address, it may only be possible arithmetically to get to some places in the Docuverse — those notationally after that address." When a parent address forks a child, the child is *inserted* between the parent and the parent's next sibling on the tumbler line. Address `2.1.1` may be created long after `2.2`, but it sits between them: `2.1 < 2.1.1 < 2.2`. The depth-first linearization means children always precede the parent's next sibling, regardless of creation order. T9 holds per-allocator, not globally.

We observe that T9 is scoped to a *single allocator's sequential stream*, not to arbitrary partitions. A server-level subtree spans multiple independent allocators (one per user). Those allocators operate concurrently — T10 below guarantees they need no coordination. If user A (prefix `1.0.1`) allocates at wall-clock time `t₂` and user B (prefix `1.0.2`) allocates at time `t₁ < t₂`, neither T9 nor any other property requires that A's address exceed B's. T9 applies within each user's allocation stream independently.

A consequence of T8 and T9 together: the set of allocated addresses is a *growing set* in the lattice-theoretic sense — it can only increase, and new elements always appear at the frontier of each allocator's domain.


### Coordination-free uniqueness

The tumbler hierarchy exists so that independent actors can allocate addresses without communicating:

## T10 — Allocators with non-nesting prefixes produce distinct addresses without coord...

Formally: let `p₁` and `p₂` be prefixes such that neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for any tumbler `a` with prefix `p₁` and any tumbler `b` with prefix `p₂`, `a ≠ b`.

This follows from the definition: if `a` has prefix `p₁` and `b` has prefix `p₂`, and the prefixes diverge at some position `k` with `p₁ₖ ≠ p₂ₖ`, then `aₖ = p₁ₖ ≠ p₂ₖ = bₖ`, so `a ≠ b`. The proof is elementary, but the property is architecturally profound. Nelson: "The owner of a given item controls the allocation of the numbers under it." No central allocator is needed. No coordination protocol is needed. The address structure itself makes collision impossible.

Nelson: "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." Baptism is the mechanism by which ownership domains are established — the owner of a number creates sub-numbers beneath it, and those sub-numbers belong exclusively to the owner.

## T10a — Each allocator uses inc(·, 0) for siblings and inc(·, k>0) only for child-spa...

T10a constrains what would otherwise be an unregulated choice. Without it, an allocator could intermix shallow and deep increments, generating outputs of varying lengths. The constraint to `k = 0` for siblings is essential: since `inc(·, 0)` preserves length (TA5(c) below), all sibling outputs from a single allocator have the same length. This uniform-length property is what the partition monotonicity and global uniqueness proofs depend on. If an allocator used `k > 0` for siblings, successive outputs would have increasing lengths and each output would extend the previous — making successive siblings nest rather than stand disjoint. This nesting would break the non-nesting premise required by the Prefix Ordering Extension lemma below.

The `k > 0` operation is reserved exclusively for child-spawning: a single deep increment that establishes a new prefix at a deeper level, from which a new allocator continues with its own `inc(·, 0)` stream.

We first establish a lemma that converts ordering of prefixes into ordering of all addresses under those prefixes.

## PrefixOrderingExtension — PrefixOrderingExtension

*Proof.* Since `p₁ < p₂` and neither is a prefix of the other, T1 case (i) applies: there exists a position `k ≤ min(#p₁, #p₂)` such that `p₁` and `p₂` agree on positions `1, ..., k-1` and `p₁ₖ < p₂ₖ`. (Case (ii) is excluded because `p₁` is not a proper prefix of `p₂`.) Now `a` extends `p₁`, so `aᵢ = p₁ᵢ` for all `i ≤ #p₁`; in particular `aₖ = p₁ₖ`. Similarly `bₖ = p₂ₖ`. On positions `1, ..., k-1`, `aᵢ = p₁ᵢ = p₂ᵢ = bᵢ`. At position `k`, `aₖ = p₁ₖ < p₂ₖ = bₖ`. So `a < b` by T1 case (i). ∎

## PartitionMonotonicity — Per-allocator ordering extends cross-allocator; for non-nesting sibling prefi...

*Proof.* Consider a partition with prefix `p`. Every allocated address in this partition has prefix `p`, hence lies in the contiguous interval guaranteed by T5. Within the partition, addresses belong to sub-partitions owned by distinct allocators. These sub-partitions have prefixes that are siblings — they share the parent prefix `p` but diverge at the component that distinguishes one allocator from another.

We claim that sibling prefixes are non-nesting. The first sub-partition prefix `t₀` is produced by `inc(parent, k)` with `k > 0`, giving `#t₀ = #parent + k` (by TA5(d)). By T10a, subsequent sibling prefixes are produced by `inc(·, 0)`: `t₁ = inc(t₀, 0)`, `t₂ = inc(t₁, 0)`, and so on. By TA5(c), `inc(t, 0)` preserves the length of `t`: `#inc(t, 0) = #t`. So all sibling prefixes have the same length `#t₀`. Two tumblers of the same length cannot stand in a prefix relationship unless they are equal (a proper prefix is strictly shorter). Since they differ at position `sig(t)` (TA5(c) increments that component), they are unequal, hence non-nesting.

Each allocator's output is monotonic (T9). The sub-partitions are ordered by their prefixes under T1. The prefix ordering extension lemma gives `a < b` for every address `a` under an earlier prefix and every address `b` under a later prefix. Within each sub-partition, allocation order matches address order by T9. ∎

## GlobalUniqueness — No two distinct allocation events anywhere in the system at any time produce ...

*Proof.* Consider allocations producing addresses `a` and `b` by distinct allocation events. Four cases arise.

*Case 1: Same allocator.* Both addresses are produced by the same allocator's sequential stream. T9 guarantees `a ≠ b` because allocation is strictly monotonic.

*Case 2: Different allocators at the same hierarchical level.* The allocators have prefixes `p₁` and `p₂` that are siblings — neither is a prefix of the other. T10 gives `a ≠ b` directly.

*Case 3: Different allocators with nesting prefixes and different zero counts.* One allocator's prefix nests within another's. But these allocators produce addresses with different zero counts: the node allocator produces addresses with `zeros = 1` (user-level), while the element allocator produces addresses with `zeros = 3`. By T4, different zero counts imply different field structure. If `#a ≠ #b`, then `a ≠ b` by T3 directly. If `#a = #b`, then `zeros(a) ≠ zeros(b)` means there exists a position where one is zero and the other nonzero — by T3, `a ≠ b`.

*Case 4: Different allocators with nesting prefixes and the same zero count.* This arises when a parent and child allocator both produce addresses at the same hierarchical level. By T10a, the parent allocator uses `inc(·, 0)` for all its sibling allocations. Its first output has some length `γ₁`; since `inc(·, 0)` preserves length (TA5(c)), all subsequent parent siblings have length `γ₁`. The child allocator's prefix was established by `inc(parent_output, k')` with `k' > 0`, giving prefix length `γ₁ + k'` (by TA5(d)). The child then uses `inc(·, 0)` for its own siblings — all its outputs have the uniform length `γ₁ + k'`. Since `k' ≥ 1`, the child's outputs are strictly longer than the parent's: `γ₁ + k' > γ₁`. By T3, `a ≠ b`. One pair requires separate treatment: the parent's child-spawning output that established the child's prefix has the same length as the child's sibling outputs (both `γ₁ + k'`). However, this output IS the child's base address, and every child sibling output is strictly greater than its base (by TA5(a)), hence distinct. The length separation is additive across nesting levels — each `inc(·, k')` with `k' ≥ 1` adds at least one component, so a descendant `d` nesting levels below has output length at least `γ₁ + d > γ₁`. Allocators at different branches that are not ancestors of each other have non-nesting prefixes and are handled by Case 2.

The argument depends critically on T10a's constraint that sibling allocations use `k = 0`. If a parent allocator could use `k > 0` for siblings, its outputs would have increasing lengths, and some parent output could match the length of a child output, collapsing the length separation. ∎

This theorem is the foundation of the addressing architecture. Every subsequent guarantee — link stability, transclusion identity, royalty tracing — depends on the 
[...truncated...]

## T12 — A span (s, ℓ) is well-formed when ℓ > 0 and action point k of ℓ satisfies k ≤...

Contiguity is definitional: the span is an interval `[s, s ⊕ ℓ)` in a totally ordered set, and intervals in total orders are contiguous. Non-emptiness follows from TA-strict: since `ℓ > 0` and `k ≤ #s`, TA0 gives `s ⊕ ℓ ∈ T`, and TA-strict gives `s ⊕ ℓ > s` directly. The interval `[s, s ⊕ ℓ)` is therefore non-empty — it contains at least `s` itself.

We reserve T5 for the distinct claim that *prefix-defined* sets are contiguous — a non-trivial property of the lexicographic order.

## TA0 — Tumbler addition a ⊕ w is well-defined when w > 0 and the action point k sati...

The precondition `k ≤ #a` is essential: the constructive definition copies components `a₁, ..., aₖ₋₁` from the start position and adds `wₖ` to `aₖ`, so position `k` must exist within `a`. A displacement whose action point exceeds `#a` — one with more leading zeros than `a` has components — would attempt to "stay at" hierarchical levels that the start position does not have, and the operation is undefined.

## TA1 — Addition preserves the total order (weak)

TA1 guarantees weak (`≤`) order preservation universally — if two positions were in order before advancement, they remain in non-reversed order after. The precondition `k ≤ min(#a, #b)` inherits from TA0: both operations must be well-defined.

Strict order preservation holds under a tighter condition. We first need a precise notion of where two tumblers first differ.

## Divergence — Divergence point of two unequal tumblers (DEFINITION, function)

(i) If there exists `k ≤ min(#a, #b)` such that `aₖ ≠ bₖ` and `(A i : 1 ≤ i < k : aᵢ = bᵢ)`, then `divergence(a, b) = k` — component divergence at a shared position.

  (ii) If `(A i : 1 ≤ i ≤ min(#a, #b) : aᵢ = bᵢ)` and `#a ≠ #b`, then `divergence(a, b) = min(#a, #b) + 1` — prefix divergence, where one tumbler is a proper prefix of the other.

Exactly one case applies for any `a ≠ b`. In case (i), `a` and `b` differ at a component both possess. In case (ii), they agree on all shared positions but one is longer — the divergence lies "just past" the shorter tumbler's last component.

For prefix-related pairs, `divergence(a, b) = min(#a, #b) + 1 > min(#a, #b)`. Since TA0 requires `k ≤ min(#a, #b)`, the condition `k ≥ divergence(a, b)` in TA1-strict below is unsatisfiable for prefix-related operands. This is correct: when `a` is a proper prefix of `b` (or vice versa), Case 1 of the verification below shows that addition erases the divergence, producing equality rather than strict inequality. TA1-strict makes no claim about prefix-related pairs — TA1 (weak) covers them, guaranteeing non-reversal.

## TA1-strict — Addition preserves the total order (strict) when k ≤ min(#a, #b) ∧ k ≥ diverg...

When the action point falls before the divergence — `k < divergence(a, b)` — both operands agree at position `k`, both get the same `wₖ` added, and both copy the same tail from `w` afterward. The original divergence is erased and the results are equal. For example, `a = [1, 3]`, `b = [1, 5]` (diverge at position 2), `w = [2]` (action point at position 1): `a ⊕ w = [3] = b ⊕ w`. Order degrades to equality, never reversal.

But TA1 alone does not guarantee that addition *advances* a position. It preserves relative order between two positions but is silent about the relationship between `a` and `a ⊕ w`. We need:

## TA-strict — Adding a positive displacement strictly advances

Without TA-strict, the axioms admit a degenerate model in which `a ⊕ w = a` for all `a, w`. This no-op model satisfies TA0 (result is in T), TA1 (if `a < b` then `a < b` — the consequent is unchanged), and TA4 (`(a ⊕ w) ⊖ w = a ⊖ w = a` if subtraction is equally degenerate). Every axiom is satisfied, yet spans are empty — the interval `[s, s ⊕ ℓ)` collapses to `[s, s)`. TA-strict excludes this model and ensures that advancing by a positive displacement moves forward. T12 (span well-definedness) depends on this directly.

**Verification of TA-strict.** Let `k` be the action point of `w`. By the constructive definition (below), `(a ⊕ w)ᵢ = aᵢ` for `i < k`, and `(a ⊕ w)ₖ = aₖ + wₖ`. Since `k` is the action point, `wₖ > 0`, so `aₖ + wₖ > aₖ`. Positions `1` through `k - 1` agree; position `k` is strictly larger. By T1 case (i), `a ⊕ w > a`.

### Subtraction for width computation

Let `⊖` denote tumbler subtraction: given two positions, compute the displacement between them.

## TA2 — Tumbler subtraction a ⊖ w is well-defined when a ≥ w

## TA3 — Subtraction preserves the total order (weak)

## TA3-strict — Subtraction preserves the total order (strict) when additionally #a = #b

### Partial inverse

## TA4 — Addition and subtraction are partial inverses

The precondition has three parts. First, `k = #a` — the action point falls at the last component of `a`. This is necessary because addition replaces `a`'s trailing structure below the action point with `w`'s trailing structure (tail replacement, defined below). When `k < #a`, components `aₖ₊₁, ..., a_{#a}` are discarded by addition and cannot be recovered by subtraction. Concretely: `[1, 5] ⊕ [1, 3] = [2, 3]` (action point 1, position 2 replaced by `w`'s trailing `3`), then `[2, 3] ⊖ [1, 3] = [1, 3] ≠ [1, 5]`.

Second, `#w = k` — the displacement has no trailing components beyond the action point. When `#w > k`, the result acquires trailing components from `w` that were not present in `a`. The trailing `7` from `w` persists through subtraction: `[0, 5] ⊕ [0, 3, 7] = [0, 8, 7]`, then `[0, 8, 7] ⊖ [0, 3, 7]` yields `[0, 5, 7] ≠ [0, 5]`.

Third, `(A i : 1 ≤ i < k : aᵢ = 0)` — all components of `a` before the action point are zero. This ensures the subtraction's divergence-discovery mechanism finds the action point at the right position. If `a` has a nonzero component at some position `j < k`, then the result of addition has `rⱼ = aⱼ ≠ 0`, and the subtraction's divergence falls at `j`, not at `k`. Concretely: `[5, 3] ⊕ [0, 7] = [5, 10]`, then `[5, 10] ⊖ [0, 7]`: divergence at position 1, producing `[5, 10] ≠ [5, 3]`.

When all three conditions hold, recovery is exact. The restriction is not a deficiency but a precise statement of when the operations are inverses.

Gregory's analysis confirms that `⊕` and `⊖` are NOT inverses in general. The implementation's `absadd` is asymmetric: the first argument supplies the high-level prefix, the second supplies the low-level suffix. When `d = a ⊖ b` strips a common prefix (reducing the exponent), `b ⊕ d` puts the difference in the wrong operand position — `absadd`'s else branch discards the first argument entirely and returns the second. The operand-order asymmetry causes total information loss even before any digit overflow.

The reverse direction is equally necessary:

## ReverseInverse — ReverseInverse

*Proof.* Let `y = a ⊖ w`. We verify the prerequisites for applying TA4 to `y`. Under the precondition `(A i : 1 ≤ i < k : aᵢ = 0)`, we have `aᵢ = wᵢ = 0` for all `i < k`, so the divergence falls at position `k`. The result `y` has: positions `i < k` zero, position `k` equal to `aₖ - wₖ`, and no components beyond `k` (since `k = #a`). So `#y = k`, `yᵢ = 0` for `i < k`, and `#w = k`. All preconditions for TA4 hold. By TA4, `(y ⊕ w) ⊖ w = y`. Suppose `y ⊕ w ≠ a`. We wish to apply TA3-strict, which requires three preconditions beyond strict ordering: `y ⊕ w ≥ w`, `a ≥ w`, and `#(y ⊕ w) = #a`. The equal-length condition holds: `#(y ⊕ w) = #w = k = #a` (the first step by the result-length identity; `#w = k` and `k = #a` are given). The condition `a ≥ w` is given. We verify `y ⊕ w ≥ w`: since `y ⊕ w ≠ a` and `yₖ = aₖ - wₖ`, we have `yₖ > 0` (if `yₖ = 0` then `aₖ = wₖ`, and since `yᵢ = wᵢ = 0` for `i < k` and `#y = k = #w`, we would have `y = [0,...,0]` and `y ⊕ w = w`; but `a ≥ w` and `aₖ = wₖ` with agreement on all prior positions gives `a = w` when `#a = #w = k`, so `y ⊕ w = w = a`, contradicting our assumption). So `yₖ > 0`, giving `(y ⊕ w)ₖ = yₖ + wₖ > wₖ` with agreement on positions before `k`, hence `y ⊕ w > w`. Now apply TA3-strict. If `y ⊕ w > a`, then `(y ⊕ w) ⊖ w > a ⊖ w = y`, giving `y > y`, a contradiction. If `y ⊕ w < a`, then `(y ⊕ w) ⊖ w < a ⊖ w`, giving `y < y`, a contradiction. So `(a ⊖ w) ⊕ w = a`. ∎


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

## TumblerAdd — TumblerAdd (DEFINITION, function)

```
         ⎧ aᵢ           if i < k        (copy from start)
rᵢ   =  ⎨ aₖ + wₖ      if i = k        (single-component advance)
         ⎩ wᵢ           if i > k        (copy from displacement)
```

The result `a ⊕ w = [r₁, ..., rₚ]` has length `p = max(k - 1, 0) + (n - k + 1)`. Since `w > 0` implies `k ≥ 1`, this simplifies to `p = (k - 1) + (n - k + 1) = n = #w`. We record this as the *result-length identity*: **`#(a ⊕ w) = #w`** — the length of the sum is determined entirely by the displacement, not the start position. This identity is load-bearing: the reverse inverse proof and the TA4 verification both depend on knowing the result length.

**Precondition:** `k ≤ m` — the displacement's action point must fall within the start position's length.

Three properties of this definition require explicit statement:

**No carry propagation:** The sum `aₖ + wₖ` at the action point is a single natural-number addition. There is no carry into position `k - 1`. This is why the operation is fast — constant time regardless of tumbler length.

**Tail replacement, not tail addition:** Components after the action point come entirely from `w`. The start position's components at positions `k + 1, ..., m` are discarded. `a ⊕ w` does not add corresponding components pairwise — it replaces the start's sub-structure with the displacement's sub-structure below the action point.

**The many-to-one property:** Because trailing components of `a` are discarded, distinct start positions can produce the same result:

```
[1, 1] ⊕ [0, 2]       = [1, 3]
[1, 1, 5] ⊕ [0, 2]    = [1, 3]
[1, 1, 999] ⊕ [0, 2]  = [1, 3]
```

This is correct and intentional: advancing to "the beginning of the next chapter" lands at the same place regardless of where you were within the current chapter.

## TumblerSub — TumblerSub (DEFINITION, function)

```
         ⎧ 0             if i < k        (these levels matched — zero them)
rᵢ   =  ⎨ aₖ - wₖ      if i = k        (reverse the advance)
         ⎩ aᵢ           if i > k        (copy from end position)
```

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

The subtraction algorithm differs structurally from addition — it zeros positions before the divergence point and copies the tail from the minuend, whereas addition copies the tail from the displacement. We must verify TA3 directly.

**Claim:** (TA3, weak form). If `a < b`, `a ≥ w`, and `b ≥ w`, then `a ⊖ w ≤ b ⊖ w`.

*Proof.* We first handle the case where `a < b` by the prefix rule (T1 case (ii)), then the component-divergence cases.

*Case 0: `a` is a proper prefix of `b`.* Then `#a < #b` and `aᵢ = bᵢ` for all `i ≤ #a`.

We first handle the sub-case `a = w`. Then `a ⊖ w = [0, ..., 0]` (the zero tumbler of length `max(#a, #w) = #w = #a`). Since `b > a = w` and `a` is a proper prefix of `b`, we have `bᵢ = wᵢ` for all `i ≤ #w`. Two sub-sub-cases arise
[...truncated...]

## TA5 — Hierarchical increment inc(t, k) produces t' > t

(a) `t' > t` (strictly greater under T1),

  (b) `t'` agrees with `t` on all components before the increment point,

  (c) when `k = 0` (*sibling*): `#t' = #t`, and `t'` differs from `t` only at position `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`,

  (d) when `k > 0` (*child*): `#t' = #t + k`, the `k - 1` intermediate positions `#t + 1, ..., #t + k - 1` are set to `0` (field separators), and the final position `#t + k` is set to `1` (the first child).

We verify `inc(t, k) > t` for both cases. For `k = 0`: `t'` agrees with `t` on positions `1, ..., sig(t) - 1` and exceeds `t` at position `sig(t)`, so `t' > t` by T1 case (i). For `k > 0`: `t'` agrees with `t` on positions `1, ..., #t`, and `#t' > #t`, so `t` is a proper prefix of `t'`, giving `t < t'` by T1 case (ii).

Gregory's analysis reveals a critical distinction: `inc(t, 0)` does NOT produce the immediate successor of `t` in the total order. It produces the *next peer* at the same hierarchical depth — the smallest tumbler with the same length that is strictly greater than `t`. The gap between `t` and `inc(t, 0)` contains the entire subtree of `t`: all tumblers of the form `t.x₁. ... .xₘ` for any `m ≥ 1` and any `x₁ ≥ 0`. The true immediate successor in the total order is `t.0` — the zero-extension — by the prefix convention (T1 case (ii)). For any `k > 0`, `inc(t, k)` does NOT produce the immediate successor of `t` in the total order. For `k = 1` the result is `t.1`; for `k = 2` the result is `t.0.1`. In both cases, `t.0` (the true immediate successor) lies strictly between `t` and the result. The gap between `t` and `inc(t, k)` contains `t`'s entire subtree of zero-extensions. For address allocation, the distinction is harmless: allocation cares about advancing the counter past all existing addresses, not about visiting every point in the total order.

**TA5 preserves T4 when `k ≤ 2` and `zeros(t) + k - 1 ≤ 3`.** Two constraints must hold simultaneously: the zero-count bound and a structural constraint against adjacent zeros.

For `k = 0`: no zeros are added — `zeros(t') = zeros(t)`, and no new adjacencies are introduced. T4 is preserved unconditionally.

For `k = 1`: one component is appended (the child value `1`), with no new zero separators — `zeros(t') = zeros(t)`. Since the appended component is positive and the last component of `t` is positive (by T4), no adjacent zeros are created. T4 is preserved when `zeros(t) ≤ 3`.

For `k = 2`: one zero separator and one child value `1` are appended, giving `zeros(t') = zeros(t) + 1`. The appended sequence is `[0, 1]` — the zero is flanked by the last component of `t` (positive, by T4's non-empty field constraint) and the new child `1`, so no adjacent zeros are created. T4 is preserved when `zeros(t) ≤ 2`.

For `k ≥ 3`: the appended sequence `[0, 0, ..., 0, 1]` contains `k - 1 ≥ 2` zeros, of whic
[...truncated...]

## TA6 — Every all-zero tumbler (any length) is less than every positive tumbler and i...

`(A t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0) ⟹ t is not a valid address)`

  `(A s, t ∈ T : (A i : 1 ≤ i ≤ #s : sᵢ = 0) ∧ (E j : 1 ≤ j ≤ #t : tⱼ > 0) ⟹ s < t)`

Zero tumblers serve as *sentinels*: they mark uninitialized values, denote "unbounded" when used as span endpoints, and act as lower bounds.


### Subspace closure

When arithmetic advances a position within one element subspace, the result must remain in that subspace. Text positions must not cross into link space, and vice versa.

An element-local position within subspace `S` has two components: the subspace identifier `N` and the ordinal `x`. A natural first attempt at an element-local displacement is `w = [0, n]` — action point `k = 2`, preserving the subspace identifier and advancing the ordinal. Addition works: `[N, x] ⊕ [0, n] = [N, x + n]`, preserving the subspace. But subtraction exposes a subtlety: `[N, x] ⊖ [0, n]` finds the first divergence at position 1 (where `N ≠ 0`), not at position 2 where the intended action lies. The subtraction produces `[N - 0, x] = [N, x]` — a no-op. The abstract `⊖` cannot shift a position backward by a displacement that disagrees with the position at the subspace identifier.

Gregory's implementation reveals the resolution. The operands passed to the arithmetic during shifts are not full element-local positions; they are *within-subspace ordinals* — the second component alone. The subspace identifier is not an operand to the shift; it is structural context that determines *which* positions are subject to the shift. The arithmetic receives ordinals, not full positions.

## PositiveTumbler — PositiveTumbler (DEFINITION, function)

Every positive tumbler is greater than every zero tumbler under T1 — if `t` has a nonzero component at position `k`, then at position `k` either the zero tumbler has a smaller component (0 < tₖ) or has run out of components, either way placing it below `t`. The condition `w > 0` in TA0 and TA4 excludes all all-zero displacements regardless of length.

## TA7a — Ordinal-only shift arithmetic

`(A o ∈ S, w > 0 : k ≤ #o ⟹ o ⊕ w ∈ T)`

  `(A o ∈ S, w > 0 : o ≥ w ⟹ o ⊖ w ∈ T)`

Both operations produce results in T, and the subspace identifier — held as context — is never modified. The core guarantee is subspace closure: arithmetic on ordinals cannot escape the subspace.

For `⊕`, a stronger result holds: components before the action point are preserved positive from `o ∈ S`, and `oₖ + wₖ > 0` since both are positive. When all components of `w` after `k` are also positive, the result is in S. For single-component ordinals (the common case), `[x] ⊕ [n] = [x + n] ∈ S` unconditionally.

The subspace identifier is context — it determines which positions are subject to the shift — not an operand to the arithmetic. Both operations produce genuine shifts in the ordinal-only view; the 2-component view gives a genuine shift for `⊕` but a vacuous closure for `⊖`. The ordinal-only formulation is adopted because applying `⊖` to full 2-component positions finds the divergence at the subspace identifier, producing a no-op rather than a genuine shift.

For single-component ordinals, `⊖` gives closure in S ∪ Z: `[x] ⊖ [n]` is `[x - n] ∈ S` when `x > n`, or `[0] ∈ Z` when `x = n` (a sentinel, TA6). When the element field has deeper structure (`δ > 1` in T4), the ordinal `o` has multiple components. A displacement with action point `k ≥ 2` preserves all ordinal components before position `k` — the constructive definition copies `o₁, ..., oₖ₋₁` from the start position unchanged. For example, spanning from ordinal `[1, 3, 2]` to `[1, 5, 7]` requires displacement `[0, 2, 7]` (action point `k = 2`); `[1, 3, 2] ⊕ [0, 2, 7] = [1, 5, 7]` — position 1 of the ordinal is copied, preserving the ordinal prefix. The subspace closure holds in all cases because the subspace identifier is never an operand.

**Verification of TA7a.** In the ordinal-only formulation, the shift operates on `o = [o₁, ..., oₘ]` with all `oᵢ > 0` (since `o ∈ S`), by displacement `w` with action point `k` satisfying `1 ≤ k ≤ m`.

*For `⊕`:* By the constructive definition, `(o ⊕ w)ᵢ = oᵢ` for `i < k` (positive, preserved from `o`), and `(o ⊕ w)ₖ = oₖ + wₖ > 0` (both positive). Components after `k` come from `w`. The result has length `#w` (by the result-length identity). The result is in T; it is in S when additionally all components of `w` after `k` are positive. The subspace identifier, held as context, is uncha
[...truncated...]

## TA-assoc — Addition is associative where both compositions are defined

The design does not depend on associativity. Shifts are applied as single operations in practice, never composed from multiple smaller shifts. An implementation with finite representations may break associativity through overflow at the action-point component, but the abstract algebra carries no such limitation.

**Addition is not commutative.** We do NOT require `a ⊕ b = b ⊕ a`. The operands play asymmetric roles: the first is a *position*, the second is a *displacement*. Swapping them is semantically meaningless. Gregory's `absadd` confirms: the first argument supplies the prefix, the second the suffix — the reverse call gives a different (and typically wrong) result.

**There is no multiplication or division.** Gregory's analysis of the complete codebase confirms: no `tumblermult`, no `tumblerdiv`, no scaling operation of any kind. The arithmetic repertoire is: add, subtract, increment, compare. Tumblers are *addresses*, not quantities. You don't multiply two file paths or divide an address by three.

**Tumbler differences are not counts.** Nelson is emphatic: "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." The difference between two addresses specifies *boundaries*, not *cardinality*. What lies between those boundaries depends on the actual population of the tree, which is dynamic and unpredictable. Between sibling addresses 3 and 7, document 5 might have arbitrarily many descendants — the span from 3 to 7 encompasses all of them, and their count is unknowable from the addresses alone. The arithmetic is an *addressing calculus*, not a *counting calculus*.

The absence of algebraic structure beyond a monotone shift is not a deficiency. It is the *minimum* that addressing requires. An ordered set with an order-preserving shift and an allocation increment is sufficient. Anything more would be unused machinery and unverified obligation.


### Spans

A span is a pair `(s, ℓ)` where `s ∈ T` is a start address and `ℓ ∈ T` is a length (a positive tumbler used as a d
[...truncated...]

## TA-LC — TA-LC

*Proof.* Let k₁ and k₂ be the action points of x and y. If k₁ < k₂, then (a ⊕ x)_{k₁} = a_{k₁} + x_{k₁} while (a ⊕ y)_{k₁} = a_{k₁} (position k₁ falls in the "copy from start" range of y). Equality gives x_{k₁} = 0, contradicting k₁ being the action point of x. Symmetrically k₂ < k₁ is impossible. So k₁ = k₂ = k.

At position k: a_k + x_k = a_k + y_k gives x_k = y_k. For i > k: x_i = (a ⊕ x)_i = (a ⊕ y)_i = y_i. For i < k: x_i = 0 = y_i. It remains to establish #x = #y. By T3, a ⊕ x = a ⊕ y implies #(a ⊕ x) = #(a ⊕ y). From TumblerAdd's result-length formula, #(a ⊕ w) = max(k − 1, 0) + (#w − k + 1) for any w with action point k. Since both x and y share the same action point k, we get #x = #y. By T3 (same length, same components), x = y.  ∎

TumblerAdd is *left-cancellative*: the start position can be "divided out" from equal results, recovering the displacement uniquely. This is a direct consequence of TumblerAdd's constructive definition — each component of the result is determined by exactly one input, so equality of results propagates back to equality of inputs.

*Worked example.* Let a = [2, 5] and suppose a ⊕ x = a ⊕ y = [2, 8]. We recover x and y uniquely. First, the action points must agree: if k_x = 1, then (a ⊕ x)₁ = a₁ + x₁ = 2 + x₁ = 2, giving x₁ = 0, which contradicts k_x = 1. So k_x = 2, and by the same argument k_y = 2. At position k = 2: a₂ + x₂ = 5 + x₂ = 8 gives x₂ = 3, and a₂ + y₂ = 5 + y₂ = 8 gives y₂ = 3. For i < k: x₁ = 0 = y₁. From the result-length formula with k = 2: #(a ⊕ x) = max(1, 0) + (#x − 1) = #x, so #x = 2 = #y. By T3, x = y = [0, 3].


### Right cancellation and the many-to-one property

The converse — right cancellation — does not hold. TumblerAdd's many-to-one property (noted informally in the definition of TumblerAdd above) means distinct starts can produce the same result under the same displacement.

## TA-RC — Right cancellation fails

*Proof by example.* Let a = [1, 3, 5], b = [1, 3, 7], and w = [0, 2, 4] (action point k = 2). Then:

  a ⊕ w = [1, 3 + 2, 4] = [1, 5, 4]
  b ⊕ w = [1, 3 + 2, 4] = [1, 5, 4]  (component 3 of b is discarded — tail replacement)

So a ⊕ w = b ⊕ w = [1, 5, 4] despite a ≠ b — the difference at position 3 is erased by tail replacement.  ∎

The mechanism is TumblerAdd's tail replacement: components of the start position after the action point are discarded and replaced by the displacement's tail. Any two starts that agree on components 1..k and differ only on components after k will produce the same result under any displacement with action point k. Formally:

## TA-MTO — TA-MTO

*Proof (forward).* Assume a_i = b_i for all 1 ≤ i ≤ k. From TumblerAdd's definition: for i < k, (a ⊕ w)_i = a_i = b_i = (b ⊕ w)_i. At i = k, (a ⊕ w)_k = a_k + w_k = b_k + w_k = (b ⊕ w)_k. For i > k, (a ⊕ w)_i = w_i = (b ⊕ w)_i. The results have the same length (max(k − 1, 0) + (#w − k + 1) depends only on k and #w). By T3, a ⊕ w = b ⊕ w.  ∎

*Proof (converse).* Suppose a ⊕ w = b ⊕ w. Let k be the action point of w. We must show a_i = b_i for all 1 ≤ i ≤ k.

(a) For i < k: position i falls in the "copy from start" region of TumblerAdd, so (a ⊕ w)_i = a_i and (b ⊕ w)_i = b_i. From a ⊕ w = b ⊕ w we get a_i = b_i.

(b) At i = k: (a ⊕ w)_k = a_k + w_k and (b ⊕ w)_k = b_k + w_k. Equality gives a_k + w_k = b_k + w_k, hence a_k = b_k by cancellation in ℕ.

Components after k are unconstrained: for i > k, (a ⊕ w)_i = w_i = (b ⊕ w)_i regardless of a_i and b_i.  ∎

This gives a precise characterization of the equivalence classes: *a and b produce the same result under w if and only if they agree on the first k components, where k is the action point of w.*


### Displacement identities

Given two positions a and b on the tumbler line, a natural question is whether b ⊖ a yields a displacement w such that a ⊕ w faithfully recovers b. We establish the well-definedness condition for such displacement recovery and the round-trip identity that guarantees faithfulness.

From TumblerAdd, a ⊕ w acts at the action point k of w: it copies a₁..aₖ₋₁, advances aₖ by wₖ, and replaces the tail with w's tail. So if a ⊕ w = b, then a and b agree on components 1..k−1 and diverge at k, with bₖ = aₖ + wₖ and bᵢ = wᵢ for i > k. Reading off the width:

  wᵢ = 0  for i < k,    wₖ = bₖ − aₖ,    wᵢ = bᵢ  for i > k

where k = divergence(a, b). This is exactly the formula for b ⊖ a from TumblerSub. We write w = b ⊖ a and call it the *displacement from a to b*. The displacement is well-defined when:

## D0 — Displacement well-definedness

D0 ensures the displacement b ⊖ a is a well-defined positive tumbler, and that a ⊕ (b ⊖ a) is defined (TA0 satisfied, since the displacement is positive and its action point k ≤ #a). Round-trip faithfulness additionally requires #a ≤ #b. The displacement w = b ⊖ a has length max(#a, #b), and the result a ⊕ w has length #w (by the result-length identity from TumblerAdd). When #a > #b, #w = #a > #b, so the result cannot equal b (by T3). When #a ≤ #b, #w = #b, giving the correct result length; combined with the component-by-component argument at the action point (k ≤ #a for arithmetic, #w = #b for length), this establishes a ⊕ w = b (D1 below).

When a is a proper prefix of b (divergence type (ii)), the divergence is #a + 1, exceeding #a, and D0 is not satisfied — no valid displacement exists.

## D1 — Displacement round-trip

a ⊕ (b ⊖ a) = b

*Proof.* Let k = divergence(a, b). By hypothesis k ≤ #a ≤ #b, so this is type (i) divergence with aₖ < bₖ. Define w = b ⊖ a by TumblerSub: wᵢ = 0 for i < k, wₖ = bₖ − aₖ, wᵢ = bᵢ for i > k. The result has length max(#a, #b) = #b. Now w > 0 since wₖ > 0, and the action point of w is k ≤ #a, so TA0 is satisfied. Applying TumblerAdd: (a ⊕ w)ᵢ = aᵢ = bᵢ for i < k (before divergence), (a ⊕ w)ₖ = aₖ + (bₖ − aₖ) = bₖ, and (a ⊕ w)ᵢ = wᵢ = bᵢ for i > k. The result has length #w = #b; every component matches b, so a ⊕ w = b by T3.  ∎

## D2 — Displacement uniqueness

*Proof.* By D1, a ⊕ (b ⊖ a) = b. So a ⊕ w = a ⊕ (b ⊖ a), and by TA-LC, w = b ⊖ a.  ∎

D1 and D2 together characterize the displacement completely: D1 says b ⊖ a recovers b, D2 says nothing else does.

When a = b, no displacement is needed; the degenerate case is handled separately since b ⊖ a produces the zero tumbler and a ⊕ (b ⊖ a) is not well-formed (TA0 requires w > 0). D0 ensures the displacement is well-defined; D1 ensures the round-trip is faithful when additionally #a ≤ #b.

*Worked example.* Consider a = [1, 2, 3] and b = [1, 5, 1]. We have #a = #b = 3.

*D0 check.* divergence(a, b) = 2, since a₁ = b₁ = 1 and a₂ = 2 ≠ 5 = b₂. The condition k = 2 ≤ #a = 3 is satisfied.

*Displacement.* By TumblerSub, w = b ⊖ a: w₁ = 0 (i < k), w₂ = 5 − 2 = 3 (i = k), w₃ = 1 (i > k, from b). So w = [0, 3, 1].

*Round-trip.* The action point of w is 2. By TumblerAdd, a ⊕ [0, 3, 1]: position 1 copies a₁ = 1, position 2 computes 2 + 3 = 5, position 3 copies w₃ = 1. Result: [1, 5, 1] = b.  ✓

The generalization to #a < #b can be seen with a' = [1, 2] and the same b = [1, 5, 1]. Here #a' = 2 < 3 = #b, the divergence is still 2 (a'₂ = 2 ≠ 5 = b₂), and k = 2 ≤ #a' = 2 satisfies D0. TumblerSub (zero-padding a' to length 3) gives the same w = [0, 3, 1] of length 3. The round-trip a' ⊕ [0, 3, 1] produces [1, 5, 1] = b — the result has length #w = 3 = #b, matching the target.


### Ordinal displacement and shift

## OrdinalDisplacement — OrdinalDisplacement (DEFINITION, function)

When the depth is determined by context (typically m = #v for the tumbler being shifted), we write δₙ.

## OrdinalShift — OrdinalShift (DEFINITION, function)

`shift(v, n) = v ⊕ δ(n, m)`

TA0 is satisfied: the action point of δ(n, m) is m = #v, so k ≤ #v holds trivially. By TumblerAdd: shift(v, n)ᵢ = vᵢ for i < m, and shift(v, n)ₘ = vₘ + n. The shift advances the deepest component by exactly n, leaving all higher-level components unchanged.

Additionally, shift preserves structural properties. When m ≥ 2, the action point of δₙ leaves position 1 unchanged — shift(v, n)₁ = v₁. When m = 1, shift([S], n) = [S + n] changes the first component. Furthermore, #shift(v, n) = #δₙ = m = #v by the result-length identity of TumblerAdd. The shift preserves tumbler depth, and — since n ≥ 1 — component positivity: shift(v, n)ₘ = vₘ + n ≥ 1 unconditionally for all vₘ ≥ 0.

## TS1 — TS1

`(A v₁, v₂, n : n ≥ 1 ∧ #v₁ = #v₂ = m ∧ v₁ < v₂ : shift(v₁, n) < shift(v₂, n))`

*Derivation.* Fix n ≥ 1. Since #v₁ = #v₂ = m and v₁ ≠ v₂, the divergence point satisfies divergence(v₁, v₂) ≤ m. The action point of δₙ is m ≥ divergence(v₁, v₂). By TA1-strict: v₁ ⊕ δₙ < v₂ ⊕ δₙ. ∎

## TS2 — TS2

`(A v₁, v₂, n : n ≥ 1 ∧ #v₁ = #v₂ = m : shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂)`

*Derivation.* Fix n ≥ 1. By TA-MTO: v₁ ⊕ δₙ = v₂ ⊕ δₙ iff (A i : 1 ≤ i ≤ m : v₁ᵢ = v₂ᵢ). The action point of δₙ is m, and agreement at positions 1..m for tumblers of length m means v₁ = v₂ by T3 (CanonicalRepresentation). ∎

## TS3 — TS3

`(A v, n₁, n₂ : n₁ ≥ 1 ∧ n₂ ≥ 1 ∧ #v = m : shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂))`

*Derivation.* We expand both sides component-wise using TumblerAdd's constructive definition.

Left side: let u = shift(v, n₁) = v ⊕ δ(n₁, m). By TumblerAdd, uᵢ = vᵢ for i < m, uₘ = vₘ + n₁, and #u = m. Now shift(u, n₂) = u ⊕ δ(n₂, m). By TumblerAdd, the result has components uᵢ = vᵢ for i < m, and uₘ + n₂ = vₘ + n₁ + n₂ at position m. Length is m.

Right side: shift(v, n₁ + n₂) = v ⊕ δ(n₁ + n₂, m). By TumblerAdd, components are vᵢ for i < m, and vₘ + (n₁ + n₂) at position m. Length is m.

Both sides have length m and agree at every component (natural-number addition is associative: vₘ + n₁ + n₂ = vₘ + (n₁ + n₂)). By T3: they are equal. ∎

## TS4 — TS4

`(A v, n : n ≥ 1 ∧ #v = m : shift(v, n) > v)`

*Derivation.* δ(n, m) > 0 since its m-th component is n ≥ 1. By TA-strict: v ⊕ δ(n, m) > v. ∎

## TS5 — TS5

`(A v, n₁, n₂ : n₁ ≥ 1 ∧ n₂ > n₁ ∧ #v = m : shift(v, n₁) < shift(v, n₂))`

*Derivation.* Write n₂ = n₁ + (n₂ − n₁) where n₂ − n₁ ≥ 1. By TS3: shift(v, n₂) = shift(shift(v, n₁), n₂ − n₁). By TS4: shift(shift(v, n₁), n₂ − n₁) > shift(v, n₁). ∎

*Worked example.* Let v = [2, 3, 7] (m = 3) and n = 4. Then δ(4, 3) = [0, 0, 4] with action point 3. TA0: k = 3 ≤ 3 = #v. By TumblerAdd: shift(v, 4) = [2, 3, 7 + 4] = [2, 3, 11].

For TS1: take v₁ = [2, 3, 5] < v₂ = [2, 3, 9] with n = 4. Then shift(v₁, 4) = [2, 3, 9] < [2, 3, 13] = shift(v₂, 4). ✓

For TS3: shift(shift([2, 3, 7], 4), 3) = shift([2, 3, 11], 3) = [2, 3, 14] = shift([2, 3, 7], 7). ✓


### Increment for allocation

A separate operation, distinct from the shifting arithmetic, handles address allocation. When the system allocates a new address, it takes the highest existing address in a partition and produces the next one. This is not addition of a width; it is advancement of a counter at a specified hierarchical level.

We define the *last significant position* of a tumbler `t`. When `t` has at least one nonzero component, `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})` — the position of the last nonzero component. When every component is zero, `sig(t) = #t`.

For valid addresses, `sig(t)` falls within the last populated field. This is a consequence of T4's positive-component constraint: every field component is strictly positive, so the last component of the last field is nonzero, and `sig(t) = #t`. Therefore `inc(t, 0)` on a valid address increments the last component of the last field, modifying only within that field and preserving the hierarchical structure.

