# ASN-0038: Tumbler Baptism

*2026-03-15*

We ask: what does it mean to introduce a new address into the tumbler hierarchy? Every address in the system was, at some moment, brought into existence — committed permanently to the space of allocated positions. We call this act *baptism*: the irreversible transition of a position from potential to actual. The question is not merely operational but structural: what invariants does baptism establish, and what do they guarantee about the evolving address space?

From ASN-0034 we have the tumbler algebra: ordering (T1), field structure (T4), allocation permanence (T8), forward allocation (T9), partition independence (T10), and hierarchical increment (TA5). These give us the raw material — the digits, the ordering, the arithmetic. What we seek now is the *growth law*: the rule by which the set of allocated addresses extends, one position at a time, without violating the invariants the existing addresses satisfy.

Nelson's design intent on baptism is not recorded in the available consultations. We proceed from Gregory's implementation evidence, which is extensive and consistent. The formal properties we derive will be those that any conforming implementation must satisfy — the abstract essence behind the concrete allocation machinery.


## The sibling stream

Consider a parent address `p ∈ T` and a depth `d ≥ 1`. From TA5, `inc(p, d)` produces a tumbler strictly greater than `p` that extends `p` by `d` additional components: `d - 1` zero separators followed by `1`. This is the *first child* of `p` at depth `d`.

The first child seeds a sequence. Applying the sibling increment `inc(·, 0)` repeatedly:

  `c₁ = inc(p, d)`

  `cₙ₊₁ = inc(cₙ, 0)   for n ≥ 1`

We call the sequence `c₁, c₂, c₃, ...` the *sibling stream* of `p` at depth `d`, written `S(p, d)`. By TA5(c), each sibling increment preserves the length of the tumbler and advances only the last significant component by 1. Every element of `S(p, d)` has length `#p + d`, and the sequence is strictly increasing under T1 (by repeated application of TA-strict). We note:

**(S0)** `(A i, j : 1 ≤ i < j : cᵢ < cⱼ)`.

The `n`-th element has the form `[p₁, ..., p_{#p}, 0, ..., 0, n]` — the parent's components, followed by `d - 1` zeros, followed by the ordinal `n`. The sibling stream is a counting sequence in its final position, anchored at the parent's prefix.

**(S1)** Every element extends `p`: `(A n ≥ 1 : p ≼ cₙ)`, where `≼` denotes the prefix relation. This holds because `inc(p, d)` preserves all of `p`'s components (TA5(b)), and `inc(·, 0)` modifies only the final component. The entire stream lives within the contiguous subtree rooted at `p` (T5, ContiguousSubtrees).


## The set of baptized addresses

We introduce a single state component:

  **Σ.B ⊆ T** — the set of baptized addresses.

Every tumbler in the system is either baptized or not; there is no third status. The system begins with some initial set `B₀` (a small number of seed addresses established at genesis) and grows monotonically. By T8 (AllocationPermanence), no address ever leaves `B`:

**(B0 — Irrevocability)** `(A B, B' : B →* B' : B ⊆ B')`.

Once baptized, always baptized. There is no reclamation, no free list, no reuse. The set `B` is a ratchet — it admits only one direction of change.


## The contiguous prefix property

We define the *children* of parent `p` at depth `d` in state `B`:

  `children(B, p, d) = B ∩ S(p, d)`

— the baptized addresses that belong to the sibling stream. We claim this set is always a *prefix* of the stream: the first `m` elements for some `m ≥ 0`, with no gaps.

**(B1 — Contiguous Prefix)** `(A p, d, n : n ≥ 1 ∧ cₙ ∈ B ⟹ (A i : 1 ≤ i < n : cᵢ ∈ B))`.

Equivalently: `children(B, p, d) = {c₁, c₂, ..., c_m}` for some `m ≥ 0`, where `c_m` is the largest baptized element of `S(p, d)`.

The argument for B1 proceeds inductively. The base case is trivial: the empty set is a prefix of length zero. For the inductive step, suppose `children(B, p, d) = {c₁, ..., c_m}` with no gaps. A new baptism in this namespace produces `c_{m+1} = inc(c_m, 0)` — the immediate successor in the stream. No element is skipped: the allocation function always selects the next ordinal, because it queries the existing set for its maximum and increments by exactly one. The new set `{c₁, ..., c_m, c_{m+1}}` is a prefix of length `m + 1`. By B0, the existing elements cannot be removed. Thus B1 is preserved.

The gap between T9 (ForwardAllocation) and B1 is the *no-skip property*: baptism always selects the immediate successor in the stream, never an arbitrary larger value. T9 says addresses increase; B1 says they increase *contiguously*. The difference is the guarantee that every ordinal from 1 through `m` is occupied, which T9 alone does not assert.


## The high water mark

B1 has a powerful consequence: the entire allocation state of a namespace reduces to a single natural number.

  **hwm(B, p, d) = #children(B, p, d)** — the *high water mark*.

This number is everything we need. The next address to be baptized is `c_{hwm+1}`, and we require nothing else — no counter distinct from the data, no free list, no reservation table. The cardinality of the existing children is a sufficient statistic for the next allocation.

**(B2 — Deterministic Allocation)** The next baptism in namespace `(p, d)` is a pure function of the current state:

  `next(B, p, d) = c_{hwm(B,p,d) + 1}`

Concretely:

- If `hwm = 0`: `next = inc(p, d)` — first child.
- If `hwm > 0`: `next = inc(c_{hwm}, 0)` — next sibling.

We observe that `next` is *deterministic*: the same `B`, `p`, `d` always yield the same result. We observe further that `next` is *idempotent in its read*: evaluating `next(B, p, d)` without committing the result leaves `B` unchanged, and a second evaluation yields the same answer. The address is consumed by commitment, not by computation. If the address is computed but never committed — if baptism is aborted after determination but before commitment — no harm is done. The namespace is unchanged; the high water mark is unchanged; the next invocation will compute the same address.

This determinism means that two independent systems beginning from the same `B₀` and executing the same sequence of baptisms — same parents, same depths, same order — produce identical address spaces. The addresses are not arbitrary identifiers assigned by fiat; they are the *inevitable* consequence of the baptism history.


## Atomicity

Baptism admits no intermediate state. The transition from `B` to `B ∪ {a}` where `a = next(B, p, d)` is a single, indivisible step.

**(B3 — Atomicity)** For any baptism producing address `a`, there is no observable system state `B'` such that `B ⊂ B' ⊂ B ∪ {a}` and `a ∉ B'` during the transition. The address either is in `B` or is not.

B3 interacts critically with B2 (determinism). The address `a = next(B, p, d)` is computed from the current state. If another baptism in the same namespace could interleave between computation and commitment, the high water mark might advance, and `a` would duplicate an existing address. Atomicity prevents this: within a single namespace, computation and commitment are indivisible.

The implementation evidence confirms this: the allocation sequence — query the tree for the highest existing address, increment, write the new entry — runs to completion without yielding control. The query-and-increment produces a *candidate* that exists only in local computation; the write commits it permanently. If the query-and-increment were executed twice without an intervening write, both invocations would return the same candidate, because the tree has not changed.

We emphasize that B3 is a specification-level requirement, not an implementation prescription. Whether atomicity is achieved through single-threaded dispatch, locking, or transactional memory is beyond the scope of this specification. What matters is that no observer sees a state in which the high water mark and the committed set disagree.


## Depth and field structure

We now examine how baptism interacts with T4 (ValidAddress). Recall from ASN-0034 that `zeros(t)` counts zero-valued field separators, determining the address level:

  `zeros(t) = 0` → node,  `zeros(t) = 1` → user,  `zeros(t) = 2` → document,  `zeros(t) = 3` → element.

When baptism crosses from one level to the next — creating a child one level deeper in the hierarchy — it must introduce a new zero separator. This is exactly what `d = 2` achieves in `inc(p, d)`: one zero separator and one initial component, advancing `zeros` by 1. When baptism stays at the same level — creating a sibling or sub-entity within the same field — `d = 1` suffices and `zeros` is unchanged.

**(B4 — Field Advancement)** `zeros(inc(p, d)) = zeros(p) + (d - 1)`.

For `d = 1`: `zeros` is preserved — the child is at the same hierarchical level.
For `d = 2`: `zeros` advances by 1 — the child descends one level.

This deserves attention. The `.0.` that appears in addresses like `1.1.0.1.0.1` is not a syntactic convention — it is a *consequence* of baptism at depth 2. When `inc(p, 2)` extends `p` by two components, the first is zero (the field separator, from TA5(d)'s `d - 1 = 1` intermediate zero) and the second is one (the first child's ordinal). The field structure of tumblers is *produced* by baptism arithmetic, not imposed by a parser or enforced by a separate mechanism.

The `.0.` separator is load-bearing in three independent ways. First, it is mechanically produced by the depth parameter: crossing from one hierarchical level to the next always uses `d = 2` and therefore always inserts exactly one zero. Second, it is semantically interpreted: the zero count determines an address's level in the hierarchy, and operations that test containment — whether an address falls within a namespace — depend on comparing prefixes up to zero boundaries. Third, it is arithmetically essential: the allocation function uses the parent's length together with the depth to compute the search bounds and the truncation point for sibling detection. An address produced without the correct zero separators would corrupt the containment arithmetic for all subsequent baptisms in that namespace.

B4 constrains the set of valid baptisms:

**(B5 — Valid Depth)** Baptism at depth `d` from parent `p` preserves T4 iff:

  (i) `d ∈ {1, 2}`, and

  (ii) `zeros(p) + (d - 1) ≤ 3`.

Condition (i) follows from the "TA5 preserves T4" lemma in ASN-0034: for `d ≥ 3`, the appended sequence contains adjacent zeros, violating T4's no-adjacent-zeros constraint. Condition (ii) ensures we do not exceed the four-level hierarchy.

Together, they produce the following table of legal baptisms:

| Parent level | `d = 1` (same level) | `d = 2` (level crossing) |
|---|---|---|
| Node (`zeros = 0`) | node child | user child |
| User (`zeros = 1`) | user child | document child |
| Document (`zeros = 2`) | sub-document child | element child |
| Element (`zeros = 3`) | sub-element child | **invalid** |

At most three level crossings can occur in a valid address chain — node to user, user to document, document to element. This is exactly the four-field structure of T4, now visible as a consequence of baptism depth arithmetic rather than an independent constraint.


## The asymmetric prerequisite

Not all baptisms carry the same preconditions. We observe a fundamental asymmetry between structural levels and the element level.

**(B6 — Level-Dependent Prerequisite)** Let `a = next(B, p, d)`.

- When `zeros(a) < 3`: `p` need not be in `B`. The parent address serves as an arithmetic anchor for namespace computation — it determines the prefix of the sibling stream — but the existence of `p` as a baptized entity is not required.
- When `zeros(a) = 3`: `p ∈ B` is required. The parent must have been previously baptized.

The asymmetry is not accidental; it reflects a semantic distinction at the heart of the hierarchy. At structural levels (node, user, document), the parent address is a *coordinate*. It defines where in the address space the child will live. The sibling stream `S(p, d)` is determined by `p`'s digits and `d`'s arithmetic, regardless of whether `p` names a baptized entity. The allocation function `next` queries the set `B` for existing children under the prefix; it does not query whether the prefix itself is in `B`.

At element level, the relationship changes. An element address designates content *within* a container. Without the container, the element has no context — no structure to belong to, no namespace to be discovered under. The container's existence is not merely a namespace convenience but a semantic requirement: an element address that names content in a non-existent container is not merely unoccupied but meaningless.

We note a subtle point about the prerequisite's durability: the requirement `p ∈ B` at element level is a check on *baptism*, not on liveness. It asks whether `p` has ever entered `B` — not whether the entity at `p` is currently open, active, or populated. By B0, baptism is irrevocable. Once `p` enters `B`, it never leaves, and the prerequisite is permanently satisfied. There is no state in which a container's baptism is revoked, leaving its elements orphaned.


## Namespace independence

Each parent-depth pair defines a namespace. We require that distinct namespaces produce non-overlapping address ranges.

**(B7 — Namespace Disjointness)** For distinct valid namespace pairs `(p, d) ≠ (p', d')`:

  `S(p, d) ∩ S(p', d') = ∅`

provided both parents satisfy T4 and both depths satisfy B5.

The argument has three cases.

*Case 1: different lengths.* If `#p + d ≠ #p' + d'`, the streams have different element lengths and are disjoint by T3 (CanonicalRepresentation) — tumblers of different lengths are never equal.

*Case 2: non-nesting prefixes.* If neither `p` nor `p'` is a prefix of the other, they occupy disjoint ownership domains by T10 (PartitionIndependence). Every element of `S(p, d)` has `p` as a prefix (S1), and every element of `S(p', d')` has `p'` as a prefix. Since the prefixes are non-nesting, no element can belong to both streams.

*Case 3: nesting prefixes with equal element lengths.* Suppose `p ≼ p'` (one is a prefix of the other) and `#p + d = #p' + d'`. Since `p ≠ p'` and `p ≼ p'`, we have `#p' > #p`, hence `d > d'`. With `d, d' ∈ {1, 2}`, this forces `d = 2`, `d' = 1`, and `#p' = #p + 1`. Now consider position `#p + 1` in each stream's elements. For `S(p, 2)`: this position holds the zero separator from `inc(p, 2)`, which is `0`. For `S(p', 1)`: this position holds `p'_{#p+1}`, which is the final component of `p'`. By T4, valid addresses do not end in zero, so `p'_{#p+1} > 0`. The streams disagree at position `#p + 1` — zero versus nonzero — and are therefore disjoint.

All three cases are exhaustive for distinct `(p, d)` pairs within the constraints of B5.


## Global uniqueness

**(B8 — Global Baptism Uniqueness)** Distinct baptisms produce distinct addresses:

  `(A a, b : a and b are produced by distinct baptisms : a ≠ b)`.

This follows from B7 and B1 together. Two baptisms in the *same* namespace produce distinct addresses because B1 ensures sequential, gap-free allocation — the `n`-th and `m`-th elements of a sibling stream are distinct for `n ≠ m` (by S0). Two baptisms in *different* namespaces produce distinct addresses because B7 ensures the namespaces do not overlap.

ASN-0034 establishes GlobalUniqueness from a different angle, through T3, T4, T9, T10, and T10a. Here we arrive at the same conclusion through the lens of baptism namespaces and the contiguous prefix property. The two derivations reinforce each other: the algebraic route via allocator discipline, and the set-theoretic route via namespace disjointness.


## The phantom parent

The asymmetric prerequisite B6 reveals something about the nature of the address hierarchy that deserves explicit attention. At structural levels, a parent address need not correspond to any baptized entity. We can baptize children under a *phantom parent* — an address that serves as a namespace anchor but has never itself entered `B`.

This is not a degenerate case or an oversight. It is a direct consequence of the allocation arithmetic: the function `next(B, p, d)` queries `B` for children sharing a prefix derived from `p` — it does not query `B` for `p` itself. If no children exist under the prefix, the result is `inc(p, d)` (the first child), regardless of whether `p` has been baptized.

The consequence is that the address space is *denser* than the entity space. Not every prefix that organizes a namespace need be a baptized position. The hierarchy of addresses exists as pure arithmetic structure; the hierarchy of baptized entities is a subset. A user address may serve as the namespace root for a family of document addresses even if the user address itself was never explicitly baptized — it is the arithmetic, not the baptism, that creates the organizational structure.

But there is a boundary. At element level (B6), the parent must be real — must be in `B`. The phantom parent pattern terminates at the structural-to-element transition. Below that boundary, every parent must be concrete. Above it, the namespace hierarchy may be sparser than the address hierarchy, with phantom parents anchoring namespaces they never explicitly joined.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| S(p,d) | Sibling stream: `c₁ = inc(p, d)`, `cₙ₊₁ = inc(cₙ, 0)` | introduced |
| S0 | `(A i, j : 1 ≤ i < j : cᵢ < cⱼ)` — stream is strictly ordered | introduced |
| S1 | `(A n ≥ 1 : p ≼ cₙ)` — all stream elements extend parent as prefix | introduced |
| Σ.B | `B ⊆ T` — set of baptized addresses | introduced |
| B0 | `B ⊆ B'` for all successor states — irrevocability (extends T8) | introduced |
| B1 | `cₙ ∈ B ⟹ (A i : 1 ≤ i < n : cᵢ ∈ B)` — contiguous prefix | introduced |
| B2 | `next(B, p, d) = c_{hwm+1}` — deterministic allocation via high water mark | introduced |
| B3 | Baptism is atomic — no intermediate state between `B` and `B ∪ {a}` | introduced |
| B4 | `zeros(inc(p, d)) = zeros(p) + (d − 1)` — field advancement | introduced |
| B5 | Valid depth: `d ∈ {1, 2}` and `zeros(p) + (d − 1) ≤ 3` | introduced |
| B6 | `zeros(a) = 3 ⟹ p ∈ B` required; `zeros(a) < 3` ⟹ no prerequisite | introduced |
| B7 | `(p, d) ≠ (p', d') ⟹ S(p, d) ∩ S(p', d') = ∅` — namespace disjointness | introduced |
| B8 | Distinct baptisms produce distinct addresses — global uniqueness | introduced |


## Open Questions

- What properties must the seed set `B₀` satisfy for the contiguous prefix invariant to hold at system genesis?
- Can an address be baptized but never populated, and must the specification distinguish "baptized but empty" from "never baptized"?
- What must a replicated system guarantee about cross-replica baptism ordering to maintain global address uniqueness without centralized coordination?
- Must baptism order respect constraints across namespaces — e.g., must a parent be baptized before its children, even at structural levels where phantom parents are permitted?
- What invariants must the element-level subspace partition (T7) satisfy so that the contiguous prefix property holds independently within each subspace?
- Under what conditions may bulk allocation — baptizing a contiguous range of positions in a single operation — satisfy B3's atomicity requirement?
