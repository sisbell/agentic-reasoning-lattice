# ASN-0040: Tumbler Baptism

*2026-03-15*

We seek to understand what it means for a position to enter the tumbler hierarchy. The algebra (ASN-0034) gives us an infinite space of well-formed addresses — ordered by T1, structured into fields by T4, permanently allocated by T8, strictly increasing by T9. But the algebra cannot distinguish between a position that *has been assigned* and one that merely *could be*. Something marks the transition from arithmetic possibility to system fact.

Nelson calls this transition *baptism*:

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers."

Three observations are compressed into that sentence. Baptism is *hierarchical* — it descends level by level through the field structure. Baptism is *sequential* — Nelson elsewhere describes creation as "successive new digits to the right," emphasizing that positions arrive in order, not arbitrarily. And baptism is *permanent* — "Any address, once assigned, remains valid forever." We defer the authorization aspect (who may baptize) to a future ASN on tumbler authorization. Here we characterize the structural mechanism: how the set of baptized positions grows, and what it preserves as it grows.

Gregory's implementation reveals the operational anatomy. Baptism is a two-phase process: first, the system queries the existing address space for the highest allocated position under a given parent prefix and increments to produce a candidate; second, it writes that candidate into the persistent store. The write — not the query — is the moment of baptism. A candidate computed but never written does not exist; if the query were repeated without an intervening write, it would return the same candidate. The address becomes real at the instant of commitment.

We formalize baptism as the growth law of the address space.


## The baptismal registry

We introduce the central state component:

  **Σ.B** ⊆ T — the set of baptized tumblers.

A tumbler t is *baptized* iff t ∈ Σ.B. Initially Σ.B contains some non-empty seed set B₀ ⊆ T of root addresses established at system genesis. Thereafter it grows monotonically:

**(B0 — Irrevocability)** `(A Σ, Σ' : Σ → Σ' : Σ.B ⊆ Σ'.B)`.

No operation removes a tumbler from B. This is the state-level reading of T8 (AllocationPermanence). T8 says the allocator never reclaims an address; B0 says the *registry* never shrinks. The distinction matters: B0 forbids any mechanism — not just the allocator — from removing a baptized position. Administrative action, garbage collection, storage failure — none may contract B. Nelson: "New items may be continually inserted in tumbler-space while the other addresses remain valid."

The binary character of this state is fundamental. Nelson's model has no third status between baptized and unbaptized: "the occupied tumbler-space — as occupied by conceptually assigned positions, even if nothing represents them in storage." A position is either conceptually assigned (in B) or not. Whether anything is *stored* at that position is a separate question, which we address below as the ghost validity property.


## The sibling stream

Consider a parent address p ∈ T and a baptismal depth d ≥ 1. From TA5, `inc(p, d)` produces a tumbler strictly greater than p that extends p by d components: d − 1 zero separators followed by 1. This is the *first child* of p at depth d. Repeated sibling increments yield a counting sequence:

  c₁ = inc(p, d)

  cₙ₊₁ = inc(cₙ, 0)    for n ≥ 1

We call the sequence c₁, c₂, c₃, ... the *sibling stream* of p at depth d, written S(p, d). By TA5(c), each sibling increment preserves the tumbler's length and advances only the last significant component by 1. Every element of S(p, d) has the form [p₁, ..., p_{#p}, 0, ..., 0, n] — the parent's components, then d − 1 zeros, then the ordinal n. The stream is strictly increasing:

**(S0)** `(A i, j : 1 ≤ i < j : cᵢ < cⱼ)`.

This follows from repeated application of TA-strict. We also note:

**(S1)** `(A n : n ≥ 1 : p ≼ cₙ)` — every stream element extends p as a prefix.

S1 holds because inc(p, d) preserves all of p's components (TA5(b)), and inc(·, 0) modifies only the final component. The entire stream lives within the contiguous subtree rooted at p (T5).

Nelson describes exactly this process: "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right." The word "successive" is precise — positions arrive in order, c₁ before c₂ before c₃. "Items 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." The stream is traversed monotonically, not sampled.


## The contiguous prefix property

We define the *children* of parent p at depth d in state B:

  children(B, p, d) = B ∩ S(p, d)

— the baptized addresses that belong to the sibling stream. We claim this set is always a *prefix* of the stream: the first m elements for some m ≥ 0, with no gaps.

**(B1 — Contiguous Prefix)** `(A p, d, n : n ≥ 1 ∧ cₙ ∈ B ⟹ (A i : 1 ≤ i < n : cᵢ ∈ B))`.

Equivalently: children(B, p, d) = {c₁, ..., cₘ} for some m ≥ 0.

The argument proceeds by induction on the sequence of baptisms within a namespace. The base case is vacuous: when no child has been baptized, the empty set is trivially a prefix. For the inductive step, suppose children(B, p, d) = {c₁, ..., cₘ} is a contiguous prefix of length m. The next baptism in this namespace queries B for the maximum element of S(p, d) — which is cₘ — and increments by one to produce c_{m+1}. No element is skipped: the allocation mechanism always selects the immediate successor, because it finds the current maximum and adds exactly one ordinal. By B0, existing elements persist, so the prefix only grows. The new set {c₁, ..., c_{m+1}} is a prefix of length m + 1.

This argument also requires that no operation *outside* this namespace inserts an element into S(p, d). We establish this below (B7, Namespace Disjointness).

The gap between T9 (ForwardAllocation) and B1 is the *no-skip property*: baptism always selects the immediate successor in the stream, never an arbitrary later value. T9 says addresses increase; B1 says they increase *contiguously*. The difference is the guarantee that every ordinal from 1 through m is represented, which T9 alone does not assert.


## The high water mark

B1 has a powerful consequence: the entire allocation state of a namespace reduces to a single natural number.

  **hwm(B, p, d) = #children(B, p, d)** — the *high water mark*.

This number is everything we need. No counter distinct from the data, no free list, no reservation table. The cardinality of the existing children is a sufficient statistic for the next allocation.

**(B2 — Deterministic Allocation)** The next baptism in namespace (p, d) is a pure function of Σ.B:

  next(B, p, d) = c_{hwm(B,p,d) + 1}

Concretely: if hwm = 0, then next = inc(p, d) — the first child; if hwm = m > 0, then next = inc(cₘ, 0) — the next sibling. In wp terms:

  wp(baptize(p, d), hwm = N + 1) = (hwm = N)

The weakest precondition for advancing the high water mark to N + 1 is precisely that it stands at N. No other state is consulted; no randomness enters. Two systems beginning from the same B₀ and executing the same sequence of baptisms — same parents, same depths, same order — produce identical address spaces. The addresses are not identifiers assigned by fiat; they are the inevitable consequence of the baptism history.

We observe that next is *idempotent in its read*: evaluating next(B, p, d) without committing the result leaves B unchanged, and a second evaluation returns the same answer. The address is consumed by commitment, not by computation. If baptism is aborted after determination but before commitment, no harm is done — the namespace is unchanged, the high water mark is unchanged, the next invocation will compute the same address.

Gregory's implementation confirms this precisely. The query-and-increment function produces a candidate address in a local variable; the candidate exists only as bits in memory. If the function were called twice without an intervening write, both invocations would return the same address — because the persistent tree has not changed and the search would find the same maximum both times. The address enters reality only when the subsequent insertion function writes it into the tree.


## Ghost elements: baptism without content

A baptized position need not contain anything. Nelson names these *ghost elements*:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements."

A ghost element is "virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." The position is in Σ.B — it has been baptized, it is permanent, it anchors a namespace for children — but nothing is stored at that address.

**(B3 — Ghost Validity)** Baptism and content occupation are independent predicates. For any t ∈ T:

  - t ∈ Σ.B ∧ t occupied: a populated position
  - t ∈ Σ.B ∧ t unoccupied: a ghost element (permitted)
  - t ∉ Σ.B: an unbaptized position (not addressable)
  - t ∉ Σ.B ∧ t occupied: **forbidden**

The fourth case is excluded by construction: content requires an address, and an address requires baptism. But the second case is explicitly permitted and common. Structural positions — nodes, users, documents — ordinarily function as ghosts. They exist to organize the namespace, not to carry payload. Their value is the subtree they anchor.

B3 separates two questions that might otherwise be conflated. "Does address t exist?" is answered by Σ.B. "Is there content at t?" is answered by a separate concern (content storage, whose structure is beyond this ASN's scope). The baptismal registry is an existence index, not a content index.


## Atomicity

Baptism admits no intermediate state. The transition from B to B ∪ {a}, where a = next(B, p, d), is a single indivisible step.

**(B4 — Atomicity)** For any baptism producing address a = next(B, p, d), there is no observable state B' such that B ⊂ B' ⊂ B ∪ {a} and a ∉ B' during the transition.

B4 interacts critically with B2. The address a is computed from the current high water mark. If another baptism in the same namespace could interleave between computation and commitment, the high water mark might advance, and a would collide with an existing address. Atomicity prevents this: within a namespace, computation and commitment are indivisible.

We emphasize the scope of the atomicity requirement. It is *per-namespace*: baptisms under different (p, d) pairs need not be serialized with respect to each other, because B8 (below) guarantees their outputs are disjoint. The minimum serialization grain is the namespace, not the entire system. This is precisely what enables decentralized baptism — two agents baptizing under different parents proceed independently, and their addresses are guaranteed distinct by the partition structure of the address space (T10).

Gregory's implementation achieves atomicity through single-threaded dispatch — the event loop processes one request to completion before accepting another, and the entire path from query through increment to write runs without yielding control. But B4 is a specification-level requirement, not an implementation prescription. Any mechanism that prevents interleaving within a namespace — locking, transactions, hardware serialization — satisfies B4.


## Depth and field structure

Baptism interacts with the field hierarchy through the depth parameter. Recall from ASN-0034 that zeros(t) — the count of zero-valued components — determines the hierarchical level: 0 for node, 1 for user, 2 for document, 3 for element. When baptism crosses from one level to the next, it must introduce a new zero separator.

**(B5 — Field Advancement)** `zeros(inc(p, d)) = zeros(p) + (d − 1)`.

For d = 1: zeros is preserved — the child is at the same hierarchical level. For d = 2: zeros advances by 1 — the child descends one level.

This deserves attention. The `.0.` that appears in addresses like `1.1.0.1.0.1` is not a syntactic convention imposed by a parser — it is a *consequence* of baptism at depth 2. When inc(p, 2) extends p by two components, the first is zero (the field separator, from TA5(d)'s d − 1 = 1 intermediate zero) and the second is 1 (the first child's ordinal). The field structure of tumblers is *produced* by baptism arithmetic.

Gregory's evidence confirms the structural necessity in three independent ways. First, the zero separator is mechanically produced by the depth parameter computed from the type hierarchy — crossing from one hierarchical level to the next always uses d = 2 and therefore always inserts exactly one zero. Second, it is semantically interpreted by the containment operation, which treats zero positions as namespace boundaries during prefix comparison. Third, it is arithmetically essential for allocation: the search-bound and truncation logic depend on measuring the parent's length against the zero boundary. An address produced without the correct zero separators corrupts containment testing and all subsequent baptisms in the affected namespace.

**(B6 — Valid Depth)** Baptism at depth d from parent p preserves T4 iff:

  (i) d ∈ {1, 2}, and

  (ii) zeros(p) + (d − 1) ≤ 3.

Condition (i) follows from the ASN-0034 lemma "TA5 preserves T4": for d ≥ 3, the appended sequence contains adjacent zeros, violating T4's non-empty-field constraint. Condition (ii) ensures no address exceeds the four-level hierarchy. Together:

| Parent level | d = 1 (same level) | d = 2 (level crossing) |
|---|---|---|
| Node (zeros = 0) | node child | user child |
| User (zeros = 1) | user child | document child |
| Document (zeros = 2) | sub-document / version | element child |
| Element (zeros = 3) | sub-element | **invalid** |

At most three level crossings can occur in a valid address chain: node → user, user → document, document → element. This is the four-field structure of T4, now visible as a consequence of baptism depth arithmetic rather than an independent syntactic constraint.


## Namespace disjointness

Each parent-depth pair defines a namespace. Distinct namespaces must produce non-overlapping address ranges, or global uniqueness collapses.

**(B7 — Namespace Disjointness)** For distinct valid pairs (p, d) ≠ (p', d'):

  S(p, d) ∩ S(p', d') = ∅

provided both parents satisfy T4 and both depths satisfy B6.

Three cases exhaust the possibilities.

*Case 1: different stream lengths.* If #p + d ≠ #p' + d', the streams have different element lengths and are disjoint by T3 — tumblers of different lengths are never equal.

*Case 2: non-nesting prefixes.* If neither p nor p' is a prefix of the other, they occupy disjoint subtrees. Every element of S(p, d) extends p (S1), and every element of S(p', d') extends p'. Since the prefixes are non-nesting, T10 guarantees no overlap.

*Case 3: nesting prefixes with equal element lengths.* Suppose p ≼ p' and #p + d = #p' + d'. Since p ≠ p' and p ≼ p', we have #p' > #p, hence d > d'. With d, d' ∈ {1, 2}, this forces d = 2, d' = 1, and #p' = #p + 1. Consider position #p + 1 in each stream's elements. For S(p, 2): this position holds the zero separator from inc(p, 2), value 0. For S(p', 1): this position holds p'_{#p+1}, the last component of p'. By T4, valid addresses do not end in zero, so p'_{#p+1} > 0. The streams disagree at position #p + 1 — zero versus nonzero — and are therefore disjoint.

All three cases are exhaustive for distinct (p, d) pairs within the constraints of B6.


## Global uniqueness

**(B8 — Global Uniqueness)** Distinct baptisms produce distinct addresses:

  `(A a, b : produced by distinct baptismal acts : a ≠ b)`.

Within the same namespace, B1 ensures sequential, gap-free allocation — the n-th and m-th elements of a sibling stream are distinct for n ≠ m (by S0). Across namespaces, B7 ensures non-overlapping ranges. Together, no two baptisms anywhere in the system, at any time, produce the same tumbler.

ASN-0034 establishes GlobalUniqueness from the algebraic angle through T3, T9, T10, and T10a. Here we reach the same conclusion through the set-theoretic lens of baptism namespaces and the contiguous prefix property. The two derivations are complementary: the algebraic route proceeds from allocator discipline (per-stream monotonicity), while the set-theoretic route proceeds from namespace partitioning (per-stream contiguity plus cross-stream disjointness). The algebraic route answers "why is each stream collision-free?"; the set-theoretic route answers "why are different streams collision-free with each other?"


## Unbounded growth

Nelson insists that the address space imposes no capacity limits:

> "A tumbler consists of a series of integers. Each integer has no upper limit."

**(B9 — Unbounded Extent)** `(A p ∈ Σ.B, d valid, M ∈ ℕ :: the system permits hwm(B, p, d) to reach M)`.

No architectural limit constrains how many children a position may have. This follows from T0(a) (UnboundedComponents): since each tumbler component is an unbounded natural number and the child ordinal occupies a single component, the ordinal can grow without bound. Combined with B1, the children of any parent can grow to form an arbitrarily long contiguous prefix {c₁, ..., cₘ} for any m.

Nelson designed this deliberately: "New items may be continually inserted in tumbler-space while the other addresses remain valid." The word "continually" carries the weight — the process of baptism never exhausts any namespace. Between physical resource limits and address space design, there is a deliberate gap: the design guarantees infinite headroom, leaving capacity as a pure engineering concern.

Nelson reinforces this at every level: "A server node, or station, has ancestors and may have possible descendant nodes. An account, too, and a document, all have possible descendants." The word "possible" does not mean "a finite number of possible" — it means the tree can always grow further. The address space is designed not for a known population but for indefinite proliferation.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| Σ.B | B ⊆ T — the set of baptized tumblers (baptismal registry) | introduced |
| S(p,d) | Sibling stream: c₁ = inc(p, d), cₙ₊₁ = inc(cₙ, 0) | introduced |
| hwm(B,p,d) | High water mark: #children(B, p, d) — sufficient allocation statistic | introduced |
| next(B,p,d) | Deterministic next address: c_{hwm+1} | introduced |
| S0 | `(A i, j : 1 ≤ i < j : cᵢ < cⱼ)` — stream strictly ordered | introduced |
| S1 | `(A n : n ≥ 1 : p ≼ cₙ)` — all stream elements extend parent | introduced |
| B0 | `Σ.B ⊆ Σ'.B` for all transitions — irrevocability (extends T8) | introduced |
| B1 | `cₙ ∈ B ⟹ (A i : 1 ≤ i < n : cᵢ ∈ B)` — contiguous prefix | introduced |
| B2 | `next(B, p, d) = c_{hwm+1}` — deterministic allocation | introduced |
| B3 | `t ∈ Σ.B` does not imply t is occupied — ghost validity | introduced |
| B4 | No observable intermediate state during baptism — atomicity | introduced |
| B5 | `zeros(inc(p, d)) = zeros(p) + (d − 1)` — field advancement | introduced |
| B6 | `d ∈ {1, 2}` and `zeros(p) + (d − 1) ≤ 3` — valid depth | introduced |
| B7 | `(p, d) ≠ (p', d') ⟹ S(p, d) ∩ S(p', d') = ∅` — namespace disjointness | introduced |
| B8 | Distinct baptisms produce distinct addresses — global uniqueness | introduced |
| B9 | `(A M :: hwm may reach M)` — unbounded extent | introduced |


## Open Questions

- Must a parent position be baptized before children can be baptized beneath it? Nelson's ownership model implies yes; Gregory's implementation does not check at structural levels. Resolution depends on the ownership model (Tumbler Ownership).
- What properties must the seed set B₀ satisfy for the contiguous prefix and namespace disjointness invariants to hold at system genesis?
- Must the specification distinguish between a ghost element that could hold content and a structural position that cannot — or is this distinction derivable from the field structure alone?
- Under what conditions may bulk allocation — baptizing a contiguous range of k positions in a single operation — satisfy B4's atomicity and B1's contiguity requirements?
- What must a distributed system guarantee about cross-replica baptism ordering to maintain global address uniqueness without centralized coordination?
- Does the abstract specification require a single canonical depth d for each parent level, or may a parent simultaneously baptize children at both d = 1 and d = 2?
- What is the minimal serialization grain for baptism — must operations be serialized per-parent per-depth, or per-parent across all depths?
- What invariants must element-level subspace partitioning (T7) satisfy so that the contiguous prefix property holds independently within each subspace?
