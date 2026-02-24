# ASN-0012: Enfilade Properties

*2026-02-24*

We wish to understand what abstract properties the system's indexing
structures must satisfy. The system maintains several mappings — from
virtual positions to permanent content addresses, from permanent addresses
to stored bytes, from link identities to their endpoint spans — and each
mapping must support efficient range queries over a space that grows
monotonically and mutates structurally with every edit. The question is not
what data structure implements these mappings (that is mechanism), but what
*guarantees* any such structure must provide. We seek properties that an
alternative implementation — a B-tree, a skip list, a persistent balanced
tree, any structure at all — would also need to satisfy for the system to
function correctly.

The investigation is motivated by a tension. The system demands two things
simultaneously: composability (the extent of a compound region must be
derivable from the extents of its parts) and faithful range retrieval (a
query for a contiguous interval must return exactly the entries that overlap
it, in address order, without omission or duplication). These are
independent requirements — a structure could satisfy composability without
supporting range queries, or could answer range queries without composable
widths — but the system requires both, and it requires that they survive
arbitrary sequences of insertions, deletions, rearrangements, splits, and
rebalancing operations. The interplay between composability and retrieval
correctness is the core of this specification.


## The abstract structure

We are looking for the minimal abstract interface that the system's
internal indexing must present. Whatever the concrete tree shape, node
layout, or rebalancing strategy, the structure must look like this from the
outside.

An *enfilade* over a carrier set A (the address type) and a value set V is
a finite mapping E : A ⇀ V that supports:

  (a) *Point query*: given a ∈ A, determine whether a ∈ dom(E) and if so
      return E(a).

  (b) *Range query*: given an interval [p, q) ⊂ A, return the restriction
      of E to dom(E) ∩ [p, q), in A-order.

  (c) *Mutation*: insertion of new entries, deletion of existing entries,
      modification of the mapping at existing addresses.

This is unremarkable — any dictionary with ordered keys offers these
operations. What distinguishes an enfilade is a set of *composition
properties* on the internal representation that make (a) and (b) efficient
by enabling hierarchical pruning. We now derive these properties from the
system's requirements.


## Width composition

Nelson describes the enfilade as a structure where "all changes, once made,
left the file remaining in canonical order, which was an internal mandate
of the system." The "canonical order" is maintained through a
*composable width* — a summary value at each internal node that describes
the extent of the subtree rooted there.

We observe that the system uses two fundamentally different composition
laws, one for each kind of mapping.

**The sequential case.** The content store (mapping permanent addresses to
bytes) is one-dimensional: entries are ordered along a single address axis,
and within any subtree the entries partition a contiguous interval. If an
internal node has children c₁, c₂, ..., cₖ in order, the children's
address ranges are non-overlapping and adjacent. The parent's total width
is the sum of its children's widths.

We state this precisely. Let w(n) denote the width of node n — the number
of entries (or the extent of the address range) covered by n's subtree.

**ENF0 (Additive width composition).** For a sequential enfilade with
internal node n having children c₁, ..., cₖ:

    w(n) = (+ i : 1 ≤ i ≤ k : w(cᵢ))

This is the fundamental property that makes sequential range queries work.
To find the entry at position p, we walk children left to right,
accumulating an offset. When the running offset plus the current child's
width exceeds p, we descend into that child. The running offset is the
cumulative sum of all previously-skipped children's widths. If ENF0 held
only approximately — if w(n) were merely an upper bound — then the
accumulated offset after skipping a child would be uncertain, and
subsequent children would be sought at wrong positions. An overestimate of
one child's width causes every subsequent sibling to appear shifted.

Gregory's implementation confirms this rigorously. The function
`setwidseq` computes `parent.cwid = Σ child.cwid` by iterating all
children and summing. The sequential traversal function `findcbcseq`
accumulates `offset += sibling.cwid` as it scans left to right, and
`whereoncrum` tests whether an address falls in `[offset, offset + cwid)`.
If the sum were inexact, this traversal would fail — addresses beyond the
overestimate but before the true position would be unreachable.

ENF0 is not a choice among alternatives; it is forced by the sequential
traversal algorithm. Any structure that navigates by offset accumulation
requires exact additive composition.

**The multi-dimensional case.** The arrangement mapping (virtual positions
to permanent addresses) is two-dimensional: each entry has both a V-address
(position in the document) and an I-address (identity of the content). An
internal node's subtree contains entries scattered across a
two-dimensional region. The children's entries do not, in general,
partition a rectangle — they may be sparse, with gaps between them.

For this case the system uses a different composition law: the parent's
extent is the *tight bounding box* of its children's extents.

**ENF1 (Bounding-box width composition).** For a multi-dimensional
enfilade with internal node n having children c₁, ..., cₖ, let
`origin(cᵢ)` and `extent(cᵢ)` denote the displacement and width of child
cᵢ. Then:

    origin(n) = (min i : 1 ≤ i ≤ k : origin(cᵢ))      (componentwise)
    extent(n) = (max i : 1 ≤ i ≤ k : origin(cᵢ) + extent(cᵢ)) − origin(n)

The parent's origin is the componentwise minimum of all children's
origins; the parent's far corner is the componentwise maximum of all
children's far corners; the parent's width spans from origin to far corner.

Unlike ENF0, this composition law is not exact in the sense that the
parent's width may exceed the total content of its subtree — the bounding
box may cover empty regions between children. This is acceptable because
multi-dimensional traversal does not use offset accumulation. Each child
carries its own absolute displacement, and the traversal checks each
child's interval independently against the query. A tight bounding box
serves only for pruning: if the query does not intersect the parent's
bounding box, no child can contain a qualifying entry. A loose bounding box
would still be *correct* — no qualifying entries would be missed — but
would degrade pruning efficiency by causing unnecessary descent into empty
subtrees. The system requires tightness for efficiency, not for
correctness.

Gregory's implementation maintains exact tightness. The function
`setwispnd` computes `mindsp = min(children.cdsp)` componentwise, absorbs
it into the parent's displacement, normalises all children by subtracting
it, then computes `cwid = max(child.cdsp + child.cwid)`. This produces the
minimal bounding box. The bounding-box invariant also underpins the
emptiness predicate — an enfilade is empty when both displacement and width
are zero — so a loose box would break the empty-detection contract.

We observe the critical asymmetry: ENF0 (additive) is a *correctness*
requirement for sequential enfilades, while ENF1 (bounding-box) is a
*correctness* requirement for emptiness detection and a *performance*
requirement for range-query pruning in multi-dimensional enfilades. Any
reimplementation must respect this distinction.


## The displacement algebra

Every entry in the structure has an absolute address in the carrier set A.
The structure stores these addresses *relatively* — as displacements from
parent to child — so that structural modifications (splits, merges, height
changes) need only adjust local offsets rather than rewriting every leaf's
address. This design requires an algebra on displacements.

We formalise the requirement. Let D be the type of displacements. For a
path from root to leaf through nodes n₀ (root), n₁, ..., nₕ (leaf), the
absolute address of the leaf is the accumulated sum of displacements along
the path:

    addr(leaf) = (+ j : 0 ≤ j ≤ h : disp(nⱼ))

where disp(nⱼ) is the stored displacement at node nⱼ and + is the
displacement addition operation. This path-accumulation is the mechanism by
which the structure recovers absolute addresses from relative storage.

**ENF2 (Additive path accumulation).** For any leaf ℓ with root-to-leaf
path n₀, n₁, ..., nₕ = ℓ:

    absolute_addr(ℓ) = disp(n₀) ⊕ disp(n₁) ⊕ ... ⊕ disp(nₕ)

where ⊕ is an associative binary operation on displacements. Associativity
is required so that the order of grouping along the path does not matter —
we must be able to combine partial sums without affecting the result.

But associativity and a binary operation do not suffice. The structure must
also *normalise* displacements during rebalancing: when the minimum
displacement among a node's children is non-zero, that minimum is absorbed
into the parent's displacement and subtracted from each child's. This
normalisation preserves absolute addresses while establishing the invariant
that at least one child has zero displacement.

The normalisation step requires:

    (parent_disp + min_child_disp) ⊕ (child_disp ⊖ min_child_disp) = parent_disp ⊕ child_disp

which reduces to requiring that ⊖ inverts ⊕:

    (a ⊖ b) ⊕ b = a

This is the *cancellation* property. Without it, the round-trip through
normalisation would corrupt absolute addresses. We state:

**ENF3 (Displacement cancellation).** The displacement algebra (D, ⊕, ⊖)
satisfies left cancellation:

    (A a, b ∈ D :: (a ⊖ b) ⊕ b = a)

ENF3 is also required when children are re-homed during rebalancing. When a
child moves from parent P to parent Q, the system computes the child's
absolute address as `P.disp ⊕ child.disp`, then derives the new
relative displacement as `(P.disp ⊕ child.disp) ⊖ Q.disp`. For the
child's absolute address to be preserved, we need:

    ((P.disp ⊕ child.disp) ⊖ Q.disp) ⊕ Q.disp = P.disp ⊕ child.disp

which is exactly cancellation again.

Gregory's implementation reveals a subtlety. The tumbler arithmetic is
*not universally cancellative*. The subtraction function `strongsub` has a
guarded case: when the subtrahend has a finer hierarchical level (smaller
exponent) than the minuend, it returns the minuend unchanged. This means
`a ⊖ b = a` when b's level is finer than a's, so `(a ⊖ b) ⊕ b = a ⊕ b ≠
a` in general. The cancellation property holds only when the operands are
at the same hierarchical level.

This is not a defect — it is the mechanism that enforces subspace isolation.
Operations within the text subspace produce displacements at one level;
operations within the link subspace produce displacements at another. The
non-cancellative cross-level arithmetic prevents a text-space shift from
accidentally affecting link-space addresses. But it means the abstract
specification must qualify ENF3:

**ENF3' (Restricted cancellation).** Cancellation holds within the
operational domain: for displacements a, b produced by operations in the
same subspace (same hierarchical level), (a ⊖ b) ⊕ b = a. The structure
never forms sums of displacements across subspace boundaries in its
normalisation or re-homing operations.

This restriction is satisfied by construction — all children of a given
node cover addresses in the same subspace — rather than by a runtime
check. Any reimplementation must either use an algebra with universal
cancellation, or must similarly guarantee that cross-subspace sums never
arise in structural operations.


## The normalisation invariant

The normalisation step in multi-dimensional enfilades establishes a
specific post-condition at every internal node:

**ENF4 (Zero-minimum normalisation).** For every internal node n in a
multi-dimensional enfilade with children c₁, ..., cₖ:

    (min i : 1 ≤ i ≤ k : disp(cᵢ)) = 0

At least one child has zero displacement (componentwise). The parent's
displacement absorbs the collective minimum of its children.

This invariant is maintained by the composition law ENF1: whenever
`setwispnd` runs, it subtracts the minimum from all children and adds it
to the parent. The property holds inductively — if children's displacements
are already normalised (their own children have the zero-minimum property),
then the minimum of children's displacements accurately reflects the
minimum absolute address in each child's subtree. Finding the minimum of
direct children therefore finds the minimum of the entire subtree.

**ENF4-GLOBAL (Root displacement is subtree minimum).** For the root r of
a multi-dimensional enfilade:

    disp(r) = (min ℓ : ℓ is a leaf of r's subtree : absolute_addr(ℓ))
                                                         (componentwise)

*Derivation.* The local invariant ENF4 says that at every internal node,
one child has displacement 0. The child with displacement 0 at the root
level is the child whose subtree contains the minimum-addressed leaf. That
child's own displacement was already the minimum of its subtree's leaves
(by the inductive application of ENF4 at lower levels). So the root's
displacement, which absorbed all the successive minima from bottom to top,
equals the global minimum leaf address.

This is not merely a convenience. The root's displacement and width
together form the bounding box of the entire enfilade, and the emptiness
check depends on both being zero for an empty structure. ENF4-GLOBAL
ensures the bounding box is tight.

We note that ENF4 is specific to multi-dimensional enfilades. Sequential
enfilades do not store child displacements at all — the position of each
child is derived from the accumulated widths of its left siblings. The
displacement concept is unnecessary (and absent in the implementation) for
the sequential case.


## Traversal completeness

The point of all this structural machinery is to answer range queries
correctly. We now state what "correctly" means.

**ENF5 (Range query completeness).** For any interval Q = [p, q) in
address space A and any enfilade E:

    result(E, Q) = { e ∈ leaves(E) : span(e) ∩ Q ≠ ∅ }

Every leaf whose address range overlaps Q is included in the result. No
qualifying leaf is omitted.

This is the *soundness* direction: completeness says nothing about whether
non-qualifying leaves might be included (they should not be, but that is
the next property). ENF5 must hold regardless of the tree's shape — after
any sequence of insertions, splits, rebalances, and deletions.

The composition laws ENF0 and ENF1 are what make ENF5 achievable through
hierarchical pruning rather than exhaustive search. We can verify ENF5 by
showing that the pruning criteria are *conservative* — they never discard a
subtree that contains a qualifying leaf.

*For sequential enfilades under ENF0:* The traversal accumulates an offset
and compares the query address to `[offset, offset + w(child))`. If a leaf
at absolute position p is within Q, then its parent's width covers p
(because the parent's width is the sum of children's widths, and the
children partition the parent's range). By induction upward, every ancestor
of a qualifying leaf has a range that intersects Q. The traversal descends
into every such ancestor. Therefore no qualifying leaf is missed.

*For multi-dimensional enfilades under ENF1:* The traversal checks each
child's bounding box against Q using `whereoncrum`. If a leaf at address p
is within Q, then p lies within the child's bounding box (since the
bounding box is the hull of all descendants' ranges), and the child's
bounding box lies within the parent's (since the parent's box is the hull
of children's boxes). By induction, every ancestor's bounding box
intersects Q. The traversal tests every child at each level and descends
into all qualifying subtrees. No qualifying leaf is skipped.


## Traversal uniqueness

Completeness is half the contract. The other half:

**ENF6 (Range query uniqueness).** Each qualifying leaf is visited
exactly once:

    #result(E, Q) = #{e ∈ leaves(E) : span(e) ∩ Q ≠ ∅}

No leaf appears twice in the result.

Uniqueness follows from the *tree* structure — every leaf has exactly one
parent, one root-to-leaf path, and the traversal follows a deterministic
path through the tree. Since the structure is a tree (not a DAG), no
leaf is reachable by two distinct paths. The sibling walk at each level is
strictly left-to-right, advancing via a next-sibling pointer that never
revisits a node. Once a sibling is processed (descended into or skipped),
the traversal moves on.

Gregory's implementation confirms: both `findcbcinspanseq` (sequential) and
`findcbcinarea2d` (multi-dimensional) walk siblings via `getrightbro` in a
forward-only loop. The data structure invariants in `enf.h` ensure that
`leftbroorfather` / `rightbro` / `leftson` form an unambiguous tree with no
shared nodes.

ENF6 combined with ENF5 gives the *exactness* of range queries: the result
contains each qualifying leaf precisely once.

We note one edge case observed in Gregory's implementation: the
`retrieveinspan` wrapper for sequential enfilades appends the last leaf a
second time when the query extends past the enfilade's boundary
(`spanend > document.width`). This is an implementation anomaly in the
wrapper, not a violation of ENF6 in the core traversal. Any
reimplementation should ensure that boundary handling does not introduce
duplicates. The abstract specification is clear: exactly once, for all
queries, without exception.


## Result ordering

The third guarantee of range retrieval:

**ENF7 (V-sorted result).** The result of a range query is returned in
ascending order of the queried address dimension, regardless of the
internal tree shape:

    (A i, j : 0 ≤ i < j < #result : addr(result.i) < addr(result.j))

For sequential enfilades, tree-traversal order *is* address order, because
the sibling sequence matches the address sequence. The left-to-right walk
produces results in address order without additional sorting.

For multi-dimensional enfilades, tree-traversal order does *not* match
address order in the queried dimension. This is a fundamental consequence
of three independent facts:

First, leaves are appended as the rightmost child during insertion, not
placed in address-sorted position. A leaf inserted at V-address 3 after a
leaf at V-address 7 becomes the *right* sibling of the first leaf, despite
having a smaller V-address.

Second, when an insertion's address is smaller than the subtree's current
minimum, the normalisation step shifts all existing children's
displacements upward to accommodate the new minimum, and the new leaf is
appended to the right. This inverts the physical ordering relative to the
logical ordering.

Third, the rebalancing algorithm for multi-dimensional enfilades sorts
internal nodes by the *diagonal sum* of their displacement components
(`I-displacement + V-displacement`), not by any single dimension. The
diagonal ordering is a spatial locality heuristic — it groups nodes with
similar combined coordinates — but it bears no relationship to V-order or
I-order individually.

Because all three effects are produced by ordinary, non-pathological
operations, the tree's left-to-right order is essentially arbitrary
relative to any single address dimension. The structure must therefore
*sort* the result after collection to satisfy ENF7. Gregory's implementation
does this through `incontextlistnd`, which performs an insertion sort by the
queried dimension as each result is accumulated. The sort is load-bearing,
not defensive.

ENF7 ensures that the caller receives results in the order it expects —
V-sorted for arrangement queries, I-sorted for provenance queries — without
needing to know or care about the internal tree structure. This is
the *tree-shape independence* property: the observable result of a range
query depends only on the logical content of the enfilade, not on how
splits, merges, and rebalancing have arranged the nodes internally.

**ENF7-IND (Tree-shape independence).** For any two enfilades E₁ and E₂
with identical logical content (same set of leaf entries) but possibly
different internal structures:

    result(E₁, Q) = result(E₂, Q)   for all queries Q

The result is a function of the content and the query alone.


## Bounded occupancy

The structure must limit the number of children per node to ensure
logarithmic height and thus logarithmic query cost. We state the upper
bound:

**ENF8 (Maximum occupancy).** There exists a constant M > 1
(parameterised by enfilade type and tree level) such that for every
internal node n:

    children(n) ≤ M

When an insertion causes children(n) > M, the node is split.

Nelson describes the performance requirement as the "soft corridor" — the
system must not slow down by half as its size doubles. Logarithmic query
cost (O(log n) for n leaves) satisfies this, and logarithmic height
requires bounded fanout. ENF8 is the mechanism.

We must ask: does the system also require a minimum occupancy bound?
Classical B-tree analysis requires ⌈M/2⌉ minimum children per node
(except the root) to guarantee logarithmic height with bounded space
waste. The system's requirements are weaker.

Gregory's implementation reveals that no minimum occupancy is enforced.
The split strategy for multi-dimensional enfilades *peels off a single
child* — the one with the largest displacement in one dimension — creating a
new sibling with exactly one child. The predicate `toofewsons` exists in
the codebase but is dead code (defined but never called). The rebalancing
algorithm `recombinend` opportunistically merges underpopulated siblings
when their combined child count fits within M, but this is a heuristic, not
a guarantee. A node with one child adjacent to a sibling with M children
(combined count > M) will not be merged.

The abstract specification therefore requires only the upper bound:

**ENF8' (Minimum occupancy).** For every node n that is not the root and
not empty:

    children(n) ≥ 1

This is the weakest possible lower bound — it says only that non-root nodes
are non-empty. Stronger lower bounds (≥ 2, ≥ ⌈M/2⌉) would provide tighter
height guarantees, but the system does not require or enforce them. An
implementation is free to maintain stronger bounds if it wishes; the
abstract specification does not demand it.

The consequence is that the height of the tree is not bounded by
⌈log_M(n)⌉ as in a classical B-tree — pathological split sequences could
produce trees of height approaching n. Nelson's "soft corridor" performance
aspiration thus depends on the editing patterns encountered in practice,
not on a structural guarantee. The abstract specification captures what is
enforced (bounded maximum, unit minimum), not what is hoped for
(logarithmic height).


## Content identity preservation

The structure must never merge, fuse, or conflate distinct logical entries
during rebalancing. This seems obvious, but it requires statement because
rebalancing moves entries between nodes, and one might imagine a
rebalancing strategy that coalesces "adjacent" entries to reduce node
count.

**ENF9 (Rebalance preserves entries).** For any rebalancing operation R
(split, merge, or re-homing of children) applied to enfilade E producing
E':

    leaves(E') = leaves(E)

as a multiset. The set of leaf entries is invariant under rebalancing. No
leaf is created, destroyed, or modified by structural operations.

Specifically, two leaves that are adjacent in V-space but map to different
I-addresses must remain distinct entries. Adjacency in one dimension does
not justify fusion when other dimensions disagree. The only point at which
two entries may be coalesced is *insertion time*, when a newly inserted
entry extends an existing entry's range in *all* dimensions
simultaneously (same origin document, contiguous I-addresses, contiguous
V-addresses). This coalescence is a semantic judgment about content
identity, not a structural optimisation — and it happens at insertion, not
during rebalancing.

Gregory's implementation enforces this rigorously. The rebalancing code
(`recombinend`, `eatbrossubtreend`, `takenephewnd`) operates only at
height ≥ 2, shuffling height-1 subtrees between height-2 parents. It never
inspects the content of leaf nodes. The function `isanextensionnd`, which
tests whether a new insertion can be coalesced with an existing leaf,
checks both V-address contiguity *and* I-address contiguity *and* origin
document identity — all three must match. This three-way gate ensures that
transclusion boundaries (same V-address range, different I-origin) are
never silently erased by the indexing structure.

ENF9 is what makes the enfilade a *faithful* index: the tree is a
presentation of the data, not a transformation of it. Rebalancing changes
the presentation; it never changes what is presented.


## Split and merge correctness

When occupancy bounds are violated, the structure must split or merge nodes
while preserving all other invariants. We state the obligations:

**ENF10 (Split post-conditions).** After splitting node n into n₁ and n₂:

  (a) leaves(n₁) ∪ leaves(n₂) = leaves(n)          (no entries lost or gained)
  (b) leaves(n₁) ∩ leaves(n₂) = ∅                   (no duplication)
  (c) children(n₁) ≤ M ∧ children(n₂) ≤ M          (occupancy restored)
  (d) children(n₁) ≥ 1 ∧ children(n₂) ≥ 1          (neither sibling empty)
  (e) ENF0 or ENF1 holds for n₁, n₂, and their parent
  (f) ENF4 holds for n₁ and n₂ (multi-dimensional case)

**ENF11 (Merge post-conditions).** After merging siblings n₁ and n₂ into
n:

  (a) leaves(n) = leaves(n₁) ∪ leaves(n₂)           (no entries lost or gained)
  (b) children(n) ≤ M                               (occupancy not violated)
  (c) ENF0 or ENF1 holds for n and its parent
  (d) ENF4 holds for n (multi-dimensional case)

The composition laws (ENF0/ENF1) must be re-established after any split or
merge. For multi-dimensional enfilades, this requires recomputation of
displacement and width from scratch — scanning all children at the modified
node, then propagating upward. There is no valid incremental shortcut.

*Why incremental update fails for multi-dimensional enfilades:* After a
split removes some children from node n, the minimum displacement among
n's remaining children may have changed to any of the survivors. Computing
the new minimum requires scanning all remaining children. Furthermore, the
normalisation step (subtracting the new minimum from all children) requires
*writing* all children. The new sibling's displacement has not been
established when the parent first needs updating, so a single bottom-up
pass may need to be repeated. Gregory's implementation handles this by
calling `setwispupwards` separately for each affected node — potentially
recomputing the same ancestor multiple times — relying on idempotence and
convergence rather than on single-pass precision.

For sequential enfilades, the situation is simpler: the parent's width is
the sum of children's widths, and after removing k children with known
widths, the new sum is the old sum minus the removed widths. Incremental
update is possible in principle, though the implementation uses
from-scratch recomputation (`setwidseq`) for uniformity.


## Rebalancing freedom

The specification must be clear about what is *not* required of
rebalancing, to avoid over-constraining implementations.

**ENF12 (Ordering freedom for multi-dimensional enfilades).** The sibling
order of children within an internal node of a multi-dimensional enfilade
is not semantically significant. Any permutation of children that preserves
ENF1 (bounding-box composition) and ENF4 (zero-minimum normalisation)
produces an equivalent enfilade.

This follows from the traversal algorithm for multi-dimensional enfilades:
the traversal checks every child independently against the query, using
each child's own displacement and width, with no offset accumulation across
siblings. The result is then sorted by the queried dimension (ENF7). No
step of this process depends on sibling order.

Gregory's implementation exploits this freedom by sorting internal-node
children by the *diagonal sum* of their two displacement coordinates —
a spatial locality heuristic that groups nodes with similar combined
addresses. The code comment identifies this explicitly as "the compare
crums diagonally hack." Any total order would produce a correct tree; the
diagonal sort is chosen for cache locality and merge quality, not for
correctness.

*Contrast with the sequential case:* For sequential enfilades, sibling
order *is* semantically significant. The left-to-right sequence of siblings
defines the address ordering, and the traversal accumulates offsets in
sibling order. Reordering children of a sequential enfilade changes the
meaning of the index. ENF12 applies only to multi-dimensional enfilades.


## The composition laws as a taxonomy

We have derived two composition laws (ENF0, ENF1), two traversal mechanisms
(offset-accumulating for sequential, independent-check for
multi-dimensional), and two result-ordering strategies (inherent for
sequential, post-hoc sort for multi-dimensional). These are not independent
choices — they form a coherent package determined by the dimensionality of
the address space.

| Property | Sequential (1D) | Multi-dimensional (2D) |
|----------|-----------------|----------------------|
| Width composition | ENF0: exact sum | ENF1: tight bounding box |
| Displacement storage | None — positions from cumulative widths | Per-child relative displacement |
| Sibling order | Semantically significant | Semantically free (ENF12) |
| Traversal | Offset accumulation, left-to-right | Independent child checks, all siblings |
| Result ordering | Inherent from traversal | Post-hoc sort required |
| Overestimate effect | **Correctness failure** — wrong offsets | Performance degradation only |
| Recomputation after split | Sum can be updated incrementally | Full scan required |
| Out-of-range query | Walk to leaf in some paths | O(1) prune at root |

The two columns describe two different *species* of enfilade, unified by
the same structural framework (tree with composable widths, bounded
occupancy, normalisation) but with fundamentally different algebraic
properties. Any reimplementation must identify which species applies to
each mapping and implement the corresponding composition law.


## Invariant preservation under operations

Every operation that modifies the enfilade must preserve all structural
invariants. We state the frame condition:

**ENF-FRAME.** After any mutation (insertion, deletion, rearrangement) of
enfilade E producing E':

  (a) ENF0 or ENF1 holds at every internal node of E'
  (b) ENF4 holds at every internal node of E' (multi-dimensional case)
  (c) ENF8 and ENF8' hold at every node of E'
  (d) ENF5, ENF6, ENF7 hold for E' — i.e., range queries on the modified
      enfilade are complete, unique, and ordered
  (e) ENF9 holds — the leaf set reflects the intended mutation, with no
      unintended additions, deletions, or fusions

ENF-FRAME is not a single property but a *meta-obligation*: every operation
proof must demonstrate that all structural invariants are re-established
before the operation completes. The composition laws are maintained by
`setwispupwards` / `setwidseq` propagation; occupancy bounds are
maintained by `splitcrumupwards` / `recombine`; result correctness
follows from the structural invariants plus the traversal algorithm.

Nelson expresses this as the "canonical order mandate" — "all changes, once
made, left the file remaining in canonical order." In our framework,
"canonical order" is ENF-FRAME: the conjunction of all structural
invariants, re-established after every operation.


## What the specification does not require

We must be explicit about what is left to implementation choice:

**Not required: logarithmic height.** The specification bounds occupancy
(ENF8, ENF8') but does not require balanced height. An implementation may
provide stronger balance guarantees; the abstract specification does not
demand them.

**Not required: specific split strategy.** ENF10 constrains the
post-conditions of a split but does not prescribe how children are
partitioned. Gregory's implementation peels off a single child for
multi-dimensional enfilades and splits in half for sequential ones. Other
strategies (median split, geometric split, etc.) are permitted as long as
ENF10 is satisfied.

**Not required: specific merge strategy.** ENF11 constrains the
post-conditions of a merge but does not prescribe when merges occur or how
siblings are selected. The implementation's opportunistic merge
(`recombinend`) is one strategy; eager rebalancing, lazy compaction, or no
merging at all are permitted.

**Not required: crash atomicity.** Nelson does not specify recovery
behaviour for interrupted structural operations. The composition laws must
hold at quiescent states; their status during an in-progress operation is
outside this specification.

**Not required: specific complexity bounds.** Nelson's "soft corridor"
aspires to logarithmic degradation, and the enfilade design enables it, but
the abstract specification does not mandate O(log n) queries. The bounds
follow from the balance properties of a specific implementation, not from
the abstract invariants.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| ENF0 | Sequential enfilade parent width = exact sum of children widths | introduced |
| ENF1 | Multi-dimensional enfilade parent extent = tight bounding box (componentwise min/max) of children | introduced |
| ENF2 | Absolute address = sum of displacements along root-to-leaf path (associative) | introduced |
| ENF3 | Displacement algebra satisfies cancellation: (a ⊖ b) ⊕ b = a | introduced |
| ENF3' | Cancellation holds within same-subspace displacements; cross-subspace sums never arise in structural ops | introduced |
| ENF4 | Zero-minimum normalisation: min child displacement = 0 at every internal node (multi-dimensional) | introduced |
| ENF4-GLOBAL | Root displacement = componentwise minimum of all leaf addresses | introduced |
| ENF5 | Range query completeness: every leaf overlapping the query is included | introduced |
| ENF6 | Range query uniqueness: every qualifying leaf visited exactly once | introduced |
| ENF7 | Result ordering: range query results sorted by queried dimension | introduced |
| ENF7-IND | Tree-shape independence: query results depend only on logical content, not internal structure | introduced |
| ENF8 | Maximum occupancy: children(n) ≤ M for all nodes | introduced |
| ENF8' | Minimum occupancy: children(n) ≥ 1 for all non-root, non-empty nodes | introduced |
| ENF9 | Rebalancing preserves the leaf multiset exactly | introduced |
| ENF10 | Split post-conditions: partition, occupancy, composition laws re-established | introduced |
| ENF11 | Merge post-conditions: union, occupancy, composition laws re-established | introduced |
| ENF12 | Sibling ordering freedom for multi-dimensional enfilades | introduced |
| ENF-FRAME | Every mutation re-establishes all structural invariants before completion | introduced |


## Open Questions

Must the tight bounding box of ENF1 be maintained as a hard invariant, or would eventual tightening (lazy propagation) suffice for correctness while only degrading performance?

What liveness property, if any, must the rebalancing strategy satisfy to prevent unbounded height growth under adversarial editing patterns?

Does the system require a bound on the number of leaves visited during a range query as a function of the result size, or is proportionality to result size merely an aspiration?

Can the displacement algebra be generalised to support concurrent modifications (two independent insertions producing displacements that must be composed in either order), or does the current algebra assume sequential application?

What must the structure guarantee about the cost of re-establishing ENF-FRAME after a single insertion — is bounded propagation depth required, or may a single insertion trigger restructuring proportional to total tree size?

Must the emptiness predicate (zero displacement and zero width) be decidable in O(1) from the root alone, or may it require descent?

Under what conditions, if any, may an implementation coalesce two leaves that were originally inserted as separate entries but have become adjacent in all dimensions through subsequent operations?
