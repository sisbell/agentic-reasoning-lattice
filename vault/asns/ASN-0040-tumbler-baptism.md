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

A tumbler t is *baptized* iff t ∈ Σ.B. Initially Σ.B contains some non-empty seed set B₀ ⊆ T of root addresses established at system genesis, subject to the conformance requirement stated at B1 below. Thereafter it grows monotonically:

**(B0 — Irrevocability)** `(A Σ, Σ' : Σ → Σ' : Σ.B ⊆ Σ'.B)`.

No operation removes a tumbler from B. This is the state-level reading of T8 (AllocationPermanence). T8 says the allocator never reclaims an address; B0 says the *registry* never shrinks. The distinction matters: B0 forbids any mechanism — not just the allocator — from removing a baptized position. Administrative action, garbage collection, storage failure — none may contract B. Nelson: "New items may be continually inserted in tumbler-space while the other addresses remain valid."

B0 tells us baptism cannot be undone; its companion tells us what *can* add to B:

**(B0a — Baptismal Closure)** The registry grows only through baptism:

  `(A Σ, Σ' : Σ → Σ' : (A t : t ∈ Σ'.B \ Σ.B : t was produced by baptism(p, d) for some valid (p, d)))`

No mechanism other than baptism — no administrative action, no side effect of content operations, no bulk initialization after genesis — may insert an address into B. B0 says nothing leaves; B0a says nothing enters except through the designated gate. Without B0a, an arbitrary operation could insert c₅ into a namespace lacking c₁ through c₄, and the contiguous prefix property (B1 below) would be violated.

The binary character of this state is fundamental. Nelson's model has no third status between baptized and unbaptized: "the occupied tumbler-space — as occupied by conceptually assigned positions, even if nothing represents them in storage." A position is either conceptually assigned (in B) or not. Whether anything is *stored* at that position is a separate question, which we address below as the ghost validity property.


## The sibling stream

Consider a parent address p ∈ T and a baptismal depth d ≥ 1. From TA5, `inc(p, d)` produces a tumbler strictly greater than p that extends p by d components: d − 1 zero separators followed by 1. This is the *first child* of p at depth d. Repeated sibling increments yield a counting sequence:

  c₁ = inc(p, d)

  cₙ₊₁ = inc(cₙ, 0)    for n ≥ 1

We call the sequence c₁, c₂, c₃, ... the *sibling stream* of p at depth d, written S(p, d). By TA5(c), each sibling increment preserves the tumbler's length and advances only the last significant component by 1. Every element of S(p, d) has the form [p₁, ..., p_{#p}, 0, ..., 0, n] — the parent's components, then d − 1 zeros, then the ordinal n. The stream is strictly increasing:

**(S0)** `(A i, j : 1 ≤ i < j : cᵢ < cⱼ)`.

This follows from repeated application of TA5(a): each inc(cₙ, 0) produces cₙ₊₁ > cₙ directly. We also note:

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

This argument rests on two additional properties. First, no operation outside this namespace inserts an element into S(p, d) — established below as B7 (Namespace Disjointness). Second, no mechanism other than baptism adds elements to B at all — established above as B0a (Baptismal Closure). Without B0a, a non-baptismal operation could insert arbitrary elements into B, and the inductive step would be ungrounded.

The induction also requires a conforming base:

  **(B₀ conformance)**: `(A p, d : children(B₀, p, d) is a contiguous prefix of S(p, d))`

B₀ must satisfy B1 for every namespace at genesis. Without this, the seed set could contain {c₁, c₃} for some namespace — a gap that the inductive argument cannot repair, since baptism only appends the next sibling. B1 holds for all states reachable from a conforming B₀ under operations satisfying B0a and B7.

The gap between T9 (ForwardAllocation) and B1 is the *no-skip property*: baptism always selects the immediate successor in the stream, never an arbitrary later value. T9 says addresses increase; B1 says they increase *contiguously*. The difference is the guarantee that every ordinal from 1 through m is represented, which T9 alone does not assert.


## The high water mark

B1 has a powerful consequence: the entire allocation state of a namespace reduces to a single natural number.

  **hwm(B, p, d) = #children(B, p, d)** — the *high water mark*.

This number is everything we need. No counter distinct from the data, no free list, no reservation table. The cardinality of the existing children is a sufficient statistic for the next allocation.

**(B2 — Deterministic Allocation)** The next baptism in namespace (p, d) is a pure function of Σ.B:

  next(B, p, d) = c_{hwm(B,p,d) + 1}

Concretely: if hwm = 0, then next = inc(p, d) — the first child; if hwm = m > 0, then next = inc(cₘ, 0) — the next sibling.

The substantive wp question targets the invariants themselves. What must hold before a baptism for B1 to hold after?

  wp(baptize(p, d), B1) = B1 ∧ B0a

Let B' = B ∪ {a} where a = next(B, p, d) = c_{hwm+1}. B1 for B' requires two things. First, every previously baptized cₙ in B still has predecessors c₁, ..., c_{n−1} in B' — satisfied because B ⊆ B' (by B0). Second, the new element c_{hwm+1} has predecessors c₁, ..., c_{hwm} in B' — satisfied iff children(B, p, d) = {c₁, ..., c_{hwm}}, which is exactly B1 for the current state. The second condition also requires that no non-baptismal mechanism has altered the namespace — which is B0a.

The wp for B8 (global uniqueness) is equally revealing:

  wp(baptize(p, d), a ∉ B) = B1 ∧ B7

The new address c_{hwm+1} must not already appear in B. Within namespace (p, d), B1 ensures children is a contiguous prefix of length hwm, so c_{hwm+1} is the first unbaptized sibling — it cannot be in B ∩ S(p, d). In any other namespace (p', d'), B7 ensures S(p, d) ∩ S(p', d') = ∅, so c_{hwm+1} cannot be in B ∩ S(p', d') either. Together, B1 and B7 guarantee freshness.

Both derivations reason about a single baptism acting on a known state B — they assume sequential execution within each namespace. B4 (Namespace Serialization) discharges this assumption: by ensuring that same-namespace baptisms do not interleave, B4 guarantees that each baptism observes the complete state left by the previous one. Without B4, two concurrent baptisms could both read hwm = m, and both wp results would be invalidated.

The simpler observation also holds: wp(baptize(p, d), hwm = N + 1) = (hwm = N). But this merely says "to advance a counter, the counter must be at the previous value" — the definition of counting, not a substantive derivation. The invariant-targeting wp reveals the real dependencies: B1, B0a, B4, and B7 are mutually supporting properties, each required for the others' preservation.

Two systems beginning from the same B₀ and executing the same sequence of baptisms — same parents, same depths, same order — produce identical address spaces. The addresses are not identifiers assigned by fiat; they are the inevitable consequence of the baptism history.

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

The fourth case is a *requirement on content operations*: any operation that populates a position must have t ∈ Σ.B as a precondition. We do not establish this here — content storage is beyond this ASN's scope. We record the requirement: downstream specifications of content operations must enforce `t ∈ Σ.B` before writing content at t. But the second case is explicitly permitted and common. Structural positions — nodes, users, documents — ordinarily function as ghosts. They exist to organize the namespace, not to carry payload. Their value is the subtree they anchor.

B3 separates two questions that might otherwise be conflated. "Does address t exist?" is answered by Σ.B. "Is there content at t?" is answered by a separate concern (content storage, whose structure is beyond this ASN's scope). The baptismal registry is an existence index, not a content index.


## Atomicity

The baptism process — read the high water mark, compute the next address, commit the result — must not be interleaved with another baptism in the same namespace. If two baptisms both read hwm = m before either commits, both compute c_{m+1} and both attempt to commit the same address — violating B8.

**(B4 — Namespace Serialization)** For any two baptisms β₁, β₂ targeting the same namespace (p, d), the commitment of one precedes the computation of the other:

  `(A β₁, β₂ : ns(β₁) = ns(β₂) : commit(β₁) ≺ read(β₂) ∨ commit(β₂) ≺ read(β₁))`

where ≺ denotes temporal precedence.

B4's scope is *per-namespace*: baptisms under different (p, d) pairs need not be serialized with respect to each other, because B7 guarantees their outputs are disjoint. The minimum serialization grain is the namespace, not the entire system. This is precisely what enables decentralized baptism — two agents baptizing under different parents proceed independently, and their addresses are guaranteed distinct by the partition structure of the address space (T10).

Gregory's implementation achieves serialization through single-threaded dispatch — the event loop processes one request to completion before accepting another, and the entire path from query through increment to write runs without yielding control. But B4 is a specification-level requirement, not an implementation prescription. Any mechanism that serializes same-namespace baptisms — locking, transactions, hardware serialization — satisfies B4.


## Depth and field structure

Baptism interacts with the field hierarchy through the depth parameter. Recall from ASN-0034 that zeros(t) — the count of zero-valued components — determines the hierarchical level: 0 for node, 1 for user, 2 for document, 3 for element. When baptism crosses from one level to the next, it must introduce a new zero separator.

**(B5 — Field Advancement)** `zeros(inc(p, d)) = zeros(p) + (d − 1)`.

For d = 1: zeros is preserved — the child is at the same hierarchical level. For d = 2: zeros advances by 1 — the child descends one level.

B5 establishes the zeros count for the *first* child c₁ of a stream. The sibling stream preserves it:

**(B5a — Sibling Zeros Preservation)** `(A t : t_{sig(t)} > 0 : zeros(inc(t, 0)) = zeros(t))`

This follows from TA5(c): sibling increment preserves the tumbler's length and modifies only position sig(t), advancing a positive value by one — no zero is created or destroyed. Combined with B5, every element of S(p, d) inherits the zeros count established at c₁:

  `(A n ≥ 1 : zeros(cₙ) = zeros(p) + (d − 1))`

The B6 validity table below depends on this uniformity — all elements in a stream share the same hierarchical level.

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


## A baptism traced

We trace a concrete sequence to ground the formal development. Begin with B₀ = {[1]} — a single root node.

**Step 1: first user.** Namespace ([1], 2) — node [1], depth 2 (level crossing to user).

  next(B₀, [1], 2) = inc([1], 2) = [1, 0, 1]

TA5(d) appends d − 1 = 1 zero separator and child value 1. B5: zeros([1, 0, 1]) = 1 = 0 + (2 − 1). B6: d = 2 and zeros([1]) + 1 = 1 ≤ 3. B1: children = {[1, 0, 1]}, a prefix of length 1.

State: B₁ = {[1], [1, 0, 1]}.

**Step 2: second user.** Same namespace ([1], 2).

  next(B₁, [1], 2) = inc([1, 0, 1], 0) = [1, 0, 2]

TA5(c): sibling increment preserves length, advances position sig([1, 0, 1]) = 3, so the ordinal goes from 1 to 2. B5a: zeros([1, 0, 2]) = 1 = zeros([1, 0, 1]) — sibling preserves zeros. B1: children = {[1, 0, 1], [1, 0, 2]}, a prefix of length 2.

State: B₂ = {[1], [1, 0, 1], [1, 0, 2]}.

**Step 3: document under first user.** Namespace ([1, 0, 1], 2) — user [1, 0, 1], depth 2 (level crossing to document).

  next(B₂, [1, 0, 1], 2) = inc([1, 0, 1], 2) = [1, 0, 1, 0, 1]

B5: zeros([1, 0, 1, 0, 1]) = 2 = 1 + (2 − 1). B6: d = 2 and zeros([1, 0, 1]) + 1 = 2 ≤ 3. B1: children = {[1, 0, 1, 0, 1]}, a prefix of length 1. B7: S([1], 2) elements have length 3; S([1, 0, 1], 2) elements have length 5 — Case 1 disjointness.

State: B₃ = {[1], [1, 0, 1], [1, 0, 2], [1, 0, 1, 0, 1]}.

Nelson's "Items 2.1, 2.2, 2.3, 2.4" is exactly this mechanism — successive baptisms under parent 2 at depth 1, yielding the sibling stream 2.1, 2.2, 2.3, 2.4 by repeated application of inc(·, 0). The sequence is determined, contiguous, and the ordinals carry no semantics beyond order.

**B7 Case 3 verified.** The steps above exercise only Case 1 of B7 (different stream lengths). We now trace Case 3 — nesting prefixes with equal element lengths. Suppose node [1, 1] has been baptized via inc([1], 1) = [1, 1] (TA5(c)). Consider S([1], 2) and S([1, 1], 1). Both streams have element length 3: #[1] + 2 = #[1, 1] + 1 = 3. The prefixes nest — [1] ≼ [1, 1] — so this is Case 3 with p = [1], d = 2, p' = [1, 1], d' = 1.

At position 2 of each stream: inc([1], 2) = [1, 0, 1] — the value at position 2 is 0, the zero separator produced by TA5(d) with d − 1 = 1 intermediate zero. inc([1, 1], 1) = [1, 1, 1] — the value at position 2 is p'₂ = 1 > 0 (by T4, valid addresses do not end in zero, so the last component of [1, 1] is positive). Sibling increments inc(·, 0) modify only the last component (TA5(c)), so position 2 is invariant across both streams: always 0 in S([1], 2), always 1 in S([1, 1], 1). The streams disagree at a fixed position and are therefore disjoint.


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
| B0a | `Σ'.B \ Σ.B ⊆ {baptism outputs}` — registry grows only through baptism | introduced |
| B₀ conf. | `children(B₀, p, d)` is a contiguous prefix for all (p, d) — seed conformance | introduced |
| B1 | `cₙ ∈ B ⟹ (A i : 1 ≤ i < n : cᵢ ∈ B)` — contiguous prefix (requires conforming B₀) | introduced |
| B2 | `next(B, p, d) = c_{hwm+1}` — deterministic allocation | introduced |
| B3 | `t ∈ Σ.B` does not imply t is occupied — ghost validity | introduced |
| B4 | Same-namespace baptisms serialized: `commit(β₁) ≺ read(β₂) ∨ commit(β₂) ≺ read(β₁)` | introduced |
| B5 | `zeros(inc(p, d)) = zeros(p) + (d − 1)` — field advancement | introduced |
| B5a | `zeros(inc(t, 0)) = zeros(t)` — sibling increment preserves zeros | introduced |
| B6 | `d ∈ {1, 2}` and `zeros(p) + (d − 1) ≤ 3` — valid depth | introduced |
| B7 | `(p, d) ≠ (p', d') ⟹ S(p, d) ∩ S(p', d') = ∅` — namespace disjointness | introduced |
| B8 | Distinct baptisms produce distinct addresses — global uniqueness | introduced |
| B9 | `(A M :: hwm may reach M)` — unbounded extent | introduced |


## Open Questions

- Must a parent position be baptized before children can be baptized beneath it? Nelson's ownership model implies yes; Gregory's implementation does not check at structural levels. Resolution depends on the ownership model (Tumbler Ownership).
- What concrete seed sets B₀ are valid — which root configurations satisfy B₀ conformance while providing a viable system genesis?
- Must the specification distinguish between a ghost element that could hold content and a structural position that cannot — or is this distinction derivable from the field structure alone?
- Under what conditions may bulk allocation — baptizing a contiguous range of k positions in a single operation — satisfy B4's atomicity and B1's contiguity requirements?
- What must a distributed system guarantee about cross-replica baptism ordering to maintain global address uniqueness without centralized coordination?
- Does the abstract specification require a single canonical depth d for each parent level, or may a parent simultaneously baptize children at both d = 1 and d = 2?
- What is the minimal serialization grain for baptism — must operations be serialized per-parent per-depth, or per-parent across all depths?
- What invariants must element-level subspace partitioning (T7) satisfy so that the contiguous prefix property holds independently within each subspace?
