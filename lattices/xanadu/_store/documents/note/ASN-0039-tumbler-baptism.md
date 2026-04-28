# ASN-0039: Tumbler Baptism

*2026-03-15*

We seek to understand what it means for an address to *exist*. The tumbler algebra (ASN-0034) defines an infinite space of well-formed addresses: ordering (T1), field structure (T4), allocation permanence (T8), hierarchical increment (TA5). But the algebra alone cannot distinguish between an address that has been assigned and one that merely could be. We need a concept that marks the transition from arithmetic possibility to system fact.

Nelson calls this *baptism*:

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers."

Three properties are packed into this sentence. Baptism is *authorized* — it flows through ownership. Baptism is *hierarchical* — it descends level by level, each level baptized by the owner of the level above. And baptism is *permanent* — an address, once baptized, is a fact of the docuverse forever. Nelson elsewhere: "Any address, once assigned, remains valid forever."

Gregory's implementation reveals the operational anatomy: baptism is a two-phase process. First, the system queries the existing address space for the current maximum under a given parent prefix and increments to produce a candidate address. Second, it writes that address into the persistent store. The write — not the query — is the moment of baptism. A candidate computed but never written does not exist; if the query is repeated without an intervening write, it returns the same candidate. The address becomes real at the instant of commitment.

We formalize baptism as the growth law of the address space.


## The baptismal registry

We introduce the central state component:

  **Σ.B** ⊆ T — the set of baptized tumblers.

A tumbler t is *alive* iff t ∈ Σ.B. Initially, Σ.B contains some non-empty seed set B₀ ⊆ T of root addresses. Thereafter it grows monotonically:

**(B0 — Irrevocability)** `(A Σ, Σ' : Σ → Σ' : Σ.B ⊆ Σ'.B)`.

No operation removes a tumbler from B. This is the state-level reading of T8 (AllocationPermanence). T8 says the allocator never reclaims; B0 says the registry never shrinks. The distinction matters: B0 forbids *any* mechanism — not just the allocator — from removing addresses. Garbage collection, administrative fiat, storage failure — none may shrink B.


## The sibling stream

Consider a parent address p ∈ T and a baptismal depth d ≥ 1. From TA5, `inc(p, d)` produces a tumbler strictly greater than p that extends p by d components: d − 1 zero separators followed by 1. This is the *first child* of p at depth d. Repeated sibling increments yield:

  c₁ = inc(p, d)

  cₙ₊₁ = inc(cₙ, 0)    for n ≥ 1

We call the sequence c₁, c₂, c₃, ... the *sibling stream* of p at depth d, written S(p, d). By TA5(c), sibling increment preserves length and advances only the last component by 1. Each element of S(p, d) has the form `[p₁, ..., p_{#p}, 0, ..., 0, n]` — the parent's components, then d − 1 zeros, then the ordinal n. The stream is strictly increasing (TA-strict applied repeatedly) and lives entirely within the contiguous subtree rooted at p (T5):

**(S0)** `(A i, j : 1 ≤ i < j : cᵢ < cⱼ)` — strict ordering within the stream.

**(S1)** `(A n ≥ 1 : p ≼ cₙ)` — every stream element extends p as prefix.

S1 holds because `inc(p, d)` preserves all of p's components (TA5(b)), and `inc(·, 0)` modifies only the final component.

Nelson describes the process: "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right." The word "successive" is deliberate — it means the stream is traversed in order, not sampled arbitrarily. Items "2.1, 2.2, 2.3, 2.4... are successive items being placed under 2."


## The contiguous prefix property

We define the *children* of parent p at depth d in state B:

  children(B, p, d) = B ∩ S(p, d)

— the baptized addresses that belong to the sibling stream. We claim this set is always a *prefix* of the stream: the first m elements for some m ≥ 0, with no gaps.

**(B1 — Contiguous Prefix)** `(A p, d, n : n ≥ 1 ∧ cₙ ∈ B ⟹ (A i : 1 ≤ i < n : cᵢ ∈ B))`.

Equivalently: children(B, p, d) = {c₁, ..., cₘ} for some m ≥ 0.

The argument proceeds inductively on the sequence of baptisms within a namespace. The base case is trivial: the empty set is a prefix of length zero. For the inductive step, suppose children(B, p, d) = {c₁, ..., cₘ}. A new baptism in this namespace must produce c_{m+1} — the immediate successor — because the allocation function queries B for its maximum in S(p, d) and increments by exactly one. No element is skipped; no earlier ordinal is revisited. By B0, existing elements are never removed, so the prefix only grows. This argument also requires that baptism outside the namespace never inserts into S(p, d), which we establish below (B10, Namespace Disjointness).

The gap between T9 (ForwardAllocation) and B1 is the *no-skip* property: baptism always selects the immediate successor, never an arbitrary later value. T9 says addresses increase; B1 says they increase *contiguously*. The difference is the guarantee that every ordinal from 1 through m is represented, which T9 alone does not assert.

We define the *high water mark*:

  **hwm(B, p, d) = #children(B, p, d)** — the count of baptized children.

By B1, this single number is a sufficient statistic for the namespace's allocation state. The next address is determined:

**(B2 — Deterministic Allocation)** The next baptism in namespace (p, d) is a pure function of Σ.B:

  next(B, p, d) = c_{hwm(B,p,d) + 1}

In wp terms:

  wp(baptize(p, d), hwm = N + 1) = (hwm = N)

The weakest precondition for advancing the high water mark to N + 1 is precisely that it stands at N. No other state is consulted; no randomness enters. Two systems starting from the same B₀ and executing the same sequence of baptisms produce identical address spaces. The addresses are not assigned by fiat — they are the inevitable consequence of the baptism history.

We observe that next is *idempotent in its read*: evaluating next(B, p, d) without committing the result leaves B unchanged, and a second evaluation yields the same answer. The address is consumed by commitment, not by computation.


## Ownership and delegation

Who is authorized to baptize? Nelson's answer is explicit and architecturally load-bearing:

> "The owner of a given item controls the allocation of the numbers under it."

We introduce a second state component:

  **Σ.owner** : Σ.B → Agent — assigns each baptized position an owning agent.

**(B3 — Ownership Gate)** Only the owner of p may baptize children under p:

  `(A p, d :: baptize(p, d) requires Σ.owner(p) = requesting_agent)`

This is the mechanism that prevents collision in a decentralized system. Nelson designed for a world without central coordination:

> "For all these things it had to be assumed that no one would be in charge of the docuverse; that while it was growing continually, there would be no center."

The ownership partition solves the problem structurally. Two agents can baptize simultaneously iff they own different positions. Since each agent controls only their own subtree, independent baptisms produce addresses in non-overlapping regions (T10, PartitionIndependence). No lock, no consensus protocol, no central registry is required. The address space is pre-partitioned by ownership; the partition *is* the coordination mechanism.

We note that B3 presupposes p ∈ Σ.B, since Σ.owner is defined only on Σ.B — querying the owner of an unbaptized position is undefined. The ownership gate therefore implicitly requires the hierarchical prerequisite we formalize below (B9).

**(B4 — Ownership Delegation)** When the owner of p baptizes a new child c, the owner assigns Σ.owner(c) to any agent (including themselves):

  `baptize(p, d) establishes Σ.owner(next(B, p, d)) ∈ Agent`

The assigning agent retains ownership of p and may continue baptizing further children. Delegation is downward only and irrevocable: once c is baptized and assigned an owner, that owner permanently controls c's subtree. B0 ensures c is never removed; the ownership cannot be revoked because the position it attaches to cannot be revoked.

This creates a delegation tree. Nelson: "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions." Root owners delegate to level-1 owners, who delegate to level-2 owners, and so on. The entire docuverse is, as Nelson puts it, "all really one big forking document" — a single tree of ownership growing from the root through successive delegation.


## Ghost elements: baptism without content

A baptized position need not contain anything. Nelson names these *ghost elements*:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements."

A ghost element is "virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." The position is real — it is in Σ.B, it has an owner, it anchors a namespace for children — but nothing is stored there.

**(B5 — Ghost Validity)** Baptism and content occupation are independent predicates. For any t ∈ T:

  - t ∈ Σ.B ∧ t occupied: normal populated position
  - t ∈ Σ.B ∧ t unoccupied: ghost element (permitted)
  - t ∉ Σ.B ∧ t unoccupied: unbaptized position (the default)
  - t ∉ Σ.B ∧ t occupied: forbidden (content requires prior baptism)

The fourth case is excluded: one cannot store content at an address that has never been baptized. But the second case is explicitly permitted and common. Structural positions — nodes, users, documents — normally function as ghosts. They exist to organize the namespace, not to hold data. Their value is the subtree they anchor, not any payload they carry.

B5 separates two questions that might otherwise be conflated. "Does address t exist?" is answered by Σ.B. "Is there content at address t?" is answered by a separate concern (the content store, whose structure is beyond this ASN's scope). The baptismal registry is an existence index, not a content index.


## Atomicity

Baptism admits no intermediate state.

**(B6 — Atomicity)** For any baptism producing address a = next(B, p, d), there is no observable state B' such that B ⊂ B' ⊂ B ∪ {a} and a ∉ B' during the transition.

B6 interacts critically with B2. The address a is computed from the current state — specifically, from hwm(B, p, d). If another baptism in the same namespace could interleave between computation and commitment, the high water mark might advance, and a would collide with an already-baptized address. Atomicity prevents this: within a single namespace, computation and commitment are indivisible.

Gregory's implementation achieves this through single-threaded dispatch — the event loop processes one request to completion before considering the next. The entire path from query through increment to write runs without yielding control. But B6 is a specification-level requirement, not an implementation prescription. Any mechanism that prevents interleaving within a namespace — locking, transactions, hardware serialization — satisfies B6.

We note the scope of the atomicity requirement. It is *per-namespace*: baptisms under different (p, d) pairs need not be serialized with respect to each other, because B10 (below) guarantees their outputs are disjoint. The minimum serialization grain is the namespace, not the entire system. This is precisely what enables decentralized baptism without global coordination.


## Depth and field structure

Baptism interacts with the field hierarchy through the depth parameter. Recall from ASN-0034 that zeros(t) — the count of zero-valued components — determines the hierarchical level: 0 for node, 1 for user, 2 for document, 3 for element.

**(B7 — Field Advancement)** `zeros(inc(p, d)) = zeros(p) + (d − 1)`.

For d = 1: zeros is preserved — the child stays at the same hierarchical level. For d = 2: zeros advances by 1 — the child descends one level. The `.0.` that appears in addresses like `1.0.1.0.1` is not a syntactic convention — it is a *consequence* of baptism at d = 2. When `inc(p, 2)` extends p by two components, the first is zero (the field separator, from TA5(d)'s d − 1 = 1 intermediate zero) and the second is 1 (the first child's ordinal). The field structure of tumblers is *produced* by baptism arithmetic, not imposed by a parser.

Gregory's implementation confirms the structural necessity in three independent ways. First, the zero separator is mechanically produced by the depth parameter computed from the type hierarchy. Second, it is semantically interpreted by the containment function, which treats zero positions as namespace boundaries during prefix comparison. Third, it is arithmetically essential for the allocation function's truncation and search-bound logic. An address produced without the correct zero separators corrupts containment testing and all subsequent baptisms in the affected namespace.

**(B8 — Valid Depth)** Baptism at depth d from parent p preserves T4 iff:

  (i) d ∈ {1, 2}, and

  (ii) zeros(p) + (d − 1) ≤ 3.

Condition (i) follows from the ASN-0034 lemma "TA5 preserves T4": for d ≥ 3, the appended sequence contains adjacent zeros, violating T4's non-empty-field constraint. Condition (ii) ensures no address exceeds the four-level hierarchy. Together they produce:

| Parent level | d = 1 (intra-level) | d = 2 (cross-level) |
|---|---|---|
| Node (zeros = 0) | sub-node | user child |
| User (zeros = 1) | sub-user | document child |
| Document (zeros = 2) | version / sub-document | element child |
| Element (zeros = 3) | sub-element | **invalid** |

At most three level crossings can occur in a valid address chain — node to user, user to document, document to element. This is exactly the four-field structure of T4, now visible as a consequence of baptism depth arithmetic rather than an independent syntactic constraint.


## The prerequisite chain

Must a parent be baptized before its children? Nelson's answer is unambiguous. Ownership presupposes existence: "Whoever owns a specific node, account, document or version may in turn designate new nodes, accounts, documents and versions, by forking their integers." You cannot own what was never baptized. The delegation chain from root to leaf flows through baptized, owned positions at every link.

**(B9 — Hierarchical Prerequisite)** To baptize under p, the position p must itself be baptized:

  `(A p, d :: baptize(p, d) requires p ∈ Σ.B)`

B9 ensures the baptismal relation forms a well-founded tree. Every non-root position has a baptized parent, and the ancestor chain — obtained by successively removing the last field or last component — terminates at a root in finitely many steps (since tumblers have finite length).

Gregory's implementation reveals a nuance. At structural levels — creating documents under users, sub-nodes under nodes — the allocation function uses the parent address as an arithmetic anchor but does not verify that the parent itself appears in the registry. It computes `max existing child + 1` under the parent prefix; if no children exist, it produces `inc(p, d)` directly. Whether p is registered is irrelevant to the arithmetic.

At element level, the check is present and enforced: inserting content within a document requires an explicit verification that the document address exists in the store. Failure to find the parent is immediate rejection.

We record B9 as the abstract specification — the design requires parent existence at all levels — while noting that an implementation may tolerate phantom parents at structural levels if it can guarantee by other means (e.g., operational protocol or session state) that parents are baptized before children. The element-level prerequisite is non-negotiable: content requires its container. The asymmetry reflects a semantic distinction. At structural levels, the parent is a *coordinate* — it defines where in the space the child will live, and the allocation arithmetic operates on coordinates without consulting the registry. At element level, the parent is a *container* — an element address designates content *within* something, and without the container, the element has no context.


## Namespace independence and global uniqueness

Distinct parent-depth pairs must produce non-overlapping address ranges, or global uniqueness collapses.

**(B10 — Namespace Disjointness)** For distinct valid pairs (p, d) ≠ (p', d'):

  `S(p, d) ∩ S(p', d') = ∅`

provided both parents satisfy T4 and both depths satisfy B8.

Three cases exhaust the possibilities.

*Case 1: different stream lengths.* If #p + d ≠ #p' + d', the streams have different element lengths and are disjoint by T3 — tumblers of different lengths are never equal.

*Case 2: non-nesting prefixes.* If neither p nor p' is a prefix of the other, they occupy disjoint ownership domains. Every element of S(p, d) extends p (S1), and every element of S(p', d') extends p'. Since the prefixes are non-nesting, T10 guarantees no overlap.

*Case 3: nesting prefixes with equal element lengths.* Suppose p ≼ p' and #p + d = #p' + d'. Since p ≠ p' and p ≼ p', we have #p' > #p, hence d > d'. With d, d' ∈ {1, 2}, this forces d = 2, d' = 1, and #p' = #p + 1. Consider position #p + 1 in each stream's elements. For S(p, 2): this position holds the zero separator from `inc(p, 2)`, value 0. For S(p', 1): this position holds the last component of p', which by T4 is nonzero (valid addresses do not end in zero). The streams disagree at this position and are disjoint.

All three cases are exhaustive for distinct (p, d) pairs within the constraints of B8.

**(B11 — Global Uniqueness)** Distinct baptisms produce distinct addresses:

  `(A a, b : produced by distinct baptismal acts : a ≠ b)`

Within the same namespace, B1 ensures sequential, gap-free allocation — the n-th and m-th elements of a sibling stream are distinct for n ≠ m (by S0). Across namespaces, B10 ensures non-overlapping ranges. Together, no two baptisms anywhere in the system, at any time, produce the same tumbler.

ASN-0034 establishes GlobalUniqueness from the algebraic angle through T3, T9, T10, and T10a. Here we reach the same conclusion through the set-theoretic lens of namespace disjointness and contiguous prefixes. The two derivations reinforce each other: the algebraic route via allocator discipline, and the set-theoretic route via the contiguous prefix property.


## Unbounded growth

Nelson insists that the address space imposes no capacity limits:

> "A tumbler consists of a series of integers. Each integer has no upper limit."

**(B12 — Unbounded Extent)** `(A p ∈ Σ.B, d valid, M ∈ ℕ :: the system permits hwm(B, p, d) to reach M)`.

No architectural limit constrains how many children a position may have. This follows from T0(a) (UnboundedComponents): since each tumbler component is an unbounded natural number and the child ordinal occupies a single component, the ordinal can grow without bound. Combined with B1, the children of any parent can grow to form an arbitrarily long contiguous prefix {1, 2, ..., N} for any N.

Nelson designed this deliberately: "New items may be continually inserted in tumbler-space while the other addresses remain valid." The word "continually" carries the weight — the process of baptism never exhausts any namespace. Between physical resource limits and address space design, there is a deliberate gap: the design guarantees infinite headroom, leaving capacity as a pure engineering concern.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| Σ.B | B ⊆ T — the set of baptized tumblers (baptismal registry) | introduced |
| Σ.owner | owner : B → Agent — assigns each baptized position an owning agent | introduced |
| S(p,d) | Sibling stream: c₁ = inc(p, d), cₙ₊₁ = inc(cₙ, 0) | introduced |
| hwm(B,p,d) | High water mark: #children(B, p, d) — allocation counter | introduced |
| next(B,p,d) | Deterministic next address: c_{hwm+1} | introduced |
| S0 | `(A i, j : 1 ≤ i < j : cᵢ < cⱼ)` — stream strictly ordered | introduced |
| S1 | `(A n ≥ 1 : p ≼ cₙ)` — all stream elements extend parent | introduced |
| B0 | `Σ.B ⊆ Σ'.B` for all transitions — irrevocability (extends T8) | introduced |
| B1 | `cₙ ∈ B ⟹ (A i : 1 ≤ i < n : cᵢ ∈ B)` — contiguous prefix | introduced |
| B2 | `next(B, p, d) = c_{hwm+1}` — deterministic allocation | introduced |
| B3 | `baptize(p, d)` requires `Σ.owner(p) = requesting_agent` — ownership gate | introduced |
| B4 | Baptism assigns Σ.owner to new child; delegation is downward and irrevocable | introduced |
| B5 | `t ∈ Σ.B` does not imply t is occupied — ghost validity | introduced |
| B6 | No observable intermediate state during baptism — atomicity | introduced |
| B7 | `zeros(inc(p, d)) = zeros(p) + (d − 1)` — field advancement | introduced |
| B8 | `d ∈ {1, 2}` and `zeros(p) + (d − 1) ≤ 3` — valid depth | introduced |
| B9 | `baptize(p, d)` requires `p ∈ Σ.B` — hierarchical prerequisite | introduced |
| B10 | `(p, d) ≠ (p', d') ⟹ S(p, d) ∩ S(p', d') = ∅` — namespace disjointness | introduced |
| B11 | Distinct baptisms produce distinct addresses — global uniqueness | introduced |
| B12 | `(A M :: hwm may reach M)` — unbounded extent | introduced |


## Open Questions

- What invariants must the seed set B₀ satisfy for the contiguous prefix and ownership delegation properties to hold at system genesis?
- Must ownership transfer between agents be possible after initial delegation, and if so, what must it preserve about the subtree below?
- Does the abstract specification require a single canonical depth d for each parent level, or may a parent simultaneously baptize children at both d = 1 and d = 2?
- What must an implementation guarantee about the visibility of a newly baptized position to agents other than the baptizer?
- Under what conditions may bulk allocation — baptizing a contiguous range of k positions in a single operation — satisfy the atomicity and contiguity invariants?
- What relationship must hold between ghost elements and content occupation at system boundaries — when does a ghost position become a mandatory container for child content?
- What is the minimal serialization grain for baptism — must operations be serialized per-parent per-depth, or per-parent across all depths?
