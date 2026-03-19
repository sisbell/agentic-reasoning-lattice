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

But ENF0 alone does not suffice for traversal correctness. We need a
structural guarantee about how the children's ranges relate to each other
and to the parent.

**ENF0' (Sequential partition).** For a sequential enfilade with internal
node n having children c₁, ..., cₖ in order, child cᵢ covers the address
range [Lᵢ, Lᵢ + w(cᵢ)) where Lᵢ = (+ j : 1 ≤ j < i : w(cⱼ)). These
ranges are pairwise disjoint and their union is [0, w(n)):

    (a) (A i, j : 1 ≤ i < j ≤ k : [Lᵢ, Lᵢ + w(cᵢ)) ∩ [Lⱼ, Lⱼ + w(cⱼ)) = ∅)
    (b) (A p : 0 ≤ p < w(n) : (E! i : 1 ≤ i ≤ k : Lᵢ ≤ p < Lᵢ + w(cᵢ)))

ENF0' is logically independent of ENF0 — one could have additive widths
over overlapping ranges, and the sum would still be correct while the
traversal would miss entries in the overlap. The offset-accumulation
traversal locates child cᵢ at position [Lᵢ, Lᵢ + w(cᵢ)). If a leaf at
position p falls within the overlap of two children, only the first child
encountered (leftmost) would be descended into. The partition property
guarantees that exactly one child covers each position, so no qualifying
leaf can be hidden behind a sibling that the traversal has already passed.

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
child's interval independently against the query. A loose bounding box
would still be *correct* — no qualifying entries would be missed — but
would degrade pruning efficiency by causing unnecessary descent into empty
subtrees.

Gregory's implementation maintains exact tightness. The function
`setwispnd` computes `mindsp = min(children.cdsp)` componentwise, absorbs
it into the parent's displacement, normalises all children by subtracting
it, then computes `cwid = max(child.cdsp + child.cwid)`. This produces the
minimal bounding box.

We observe the critical asymmetry: ENF0 (additive) is a *correctness*
requirement for sequential enfilades, while ENF1 (bounding-box) tightness
is a structural invariant that serves two purposes: it maintains
ENF4-GLOBAL (root displacement = minimum leaf address), which is needed for
the normalisation chain to work correctly; and it enables efficient pruning
of non-qualifying subtrees during range queries. A loose bounding box would
not cause a qualifying leaf to be missed (the traversal checks every child
independently), but it would break the ENF4-GLOBAL derivation and degrade
pruning. Any reimplementation must respect this distinction.


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

where (D, ⊕, 0) is a commutative monoid — that is, ⊕ is associative,
commutative, and has identity element 0. Associativity is required so that
the order of grouping along the path does not matter. Commutativity is
required by the normalisation step: when the minimum child displacement min
is absorbed into the parent, the new path to a leaf through child c
computes (parent ⊕ min) ⊕ (child ⊖ min). Setting x = child ⊖ min, the
right-inverse property (ENF3 below) gives x ⊕ min = child, so the new
address is parent ⊕ (min ⊕ x). The old address is parent ⊕ child =
parent ⊕ (x ⊕ min). These are equal only if min ⊕ x = x ⊕ min. The same
requirement arises in re-homing: the round-trip Q.disp ⊕ ((P.disp ⊕
child.disp) ⊖ Q.disp) must equal P.disp ⊕ child.disp, which again
demands commutativity. The identity element 0 is required by ENF4: the
normalisation invariant asserts that at least one child has displacement 0,
and for this to be well-defined we need 0 ⊕ a = a ⊕ 0 = a for all a ∈ D.

But a commutative monoid does not suffice. The structure must also
*normalise* displacements during rebalancing: when the minimum displacement
among a node's children is non-zero, that minimum is absorbed into the
parent's displacement and subtracted from each child's. This normalisation
preserves absolute addresses while establishing the invariant that at least
one child has zero displacement.

The normalisation step requires:

    (parent_disp ⊕ min_child_disp) ⊕ (child_disp ⊖ min_child_disp) = parent_disp ⊕ child_disp

which reduces to requiring that ⊖ is a right inverse for ⊕:

    (a ⊖ b) ⊕ b = a

This is the *right-inverse property*: subtracting b and then adding b
recovers the original. Without it, the round-trip through normalisation
would corrupt absolute addresses. We state:

**ENF3 (Displacement right-inverse).** The displacement algebra (D, ⊕, ⊖,
0) satisfies:

    (A a, b ∈ D :: (a ⊖ b) ⊕ b = a)

That is, ⊖ is a right inverse of ⊕. As a consequence, standard
cancellation follows: from (a ⊖ b) ⊕ b = a and commutativity of ⊕, we
get b ⊕ (a ⊖ b) = a, and therefore c ⊕ a = c ⊕ b implies a = b (left
cancellation). But the right-inverse property is the primitive requirement;
cancellation is derived.

ENF3 is also required when children are re-homed during rebalancing. When a
child moves from parent P to parent Q, the system computes the child's
absolute address as `P.disp ⊕ child.disp`, then derives the new
relative displacement as `(P.disp ⊕ child.disp) ⊖ Q.disp`. For the
child's absolute address to be preserved, we need:

    ((P.disp ⊕ child.disp) ⊖ Q.disp) ⊕ Q.disp = P.disp ⊕ child.disp

which is exactly the right-inverse property again.

Gregory's implementation reveals a subtlety. The tumbler arithmetic is
*not universal* in this regard. The subtraction function `strongsub` has a
guarded case: when the subtrahend has a finer hierarchical level (smaller
exponent) than the minuend, it returns the minuend unchanged. This means
`a ⊖ b = a` when b's level is finer than a's, so `(a ⊖ b) ⊕ b = a ⊕ b ≠
a` in general. The right-inverse property holds only when the operands are
at the same hierarchical level.

This is not a defect — it is the mechanism that enforces subspace isolation.
Operations within the text subspace produce displacements at one level;
operations within the link subspace produce displacements at another. The
non-invertible cross-level arithmetic prevents a text-space shift from
accidentally affecting link-space addresses. But it means the abstract
specification must qualify ENF3:

**ENF3' (Restricted right-inverse).** The right-inverse property holds
within the operational domain: for displacements a, b produced by
operations in the same subspace (same hierarchical level), (a ⊖ b) ⊕ b =
a. The structure never forms sums of displacements across subspace
boundaries in its normalisation or re-homing operations.

This restriction is satisfied by construction — all children of a given
node cover addresses in the same subspace — rather than by a runtime
check. Any reimplementation must either use an algebra with universal
right-inverse, or must similarly guarantee that cross-subspace sums never
arise in structural operations.

To summarise: the full displacement algebra is (D, ⊕, ⊖, 0) where (D, ⊕,
0) is a commutative monoid with identity 0, and ⊖ satisfies ENF3 (right-
inverse) within same-subspace operands (ENF3'). Under the ENF3' restriction
this is a partial commutative group.


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
to the parent.

**ENF4-GLOBAL (Root displacement is subtree minimum).** For the root r of
a multi-dimensional enfilade:

    disp(r) = (min ℓ : ℓ is a leaf of r's subtree : absolute_addr(ℓ))
                                                         (componentwise)

*Proof by induction on tree height.* Define min_leaf(n) = (min ℓ : ℓ in
n's subtree : absolute_addr(ℓ)) for any node n. We show that min_leaf(n) =
absolute_disp(n) for every internal node n, where absolute_disp(n) is the
sum of displacements along the path from root to n.

*Base case.* Let n be an internal node at the lowest level, so n's children
c₁, ..., cₖ are leaves. Then:

    min_leaf(n)
    = (min i : 1 ≤ i ≤ k : absolute_addr(cᵢ))
    = (min i : 1 ≤ i ≤ k : absolute_disp(n) ⊕ disp(cᵢ))

Since ⊕ is a commutative monoid and displacement components are
non-negative, the minimum distributes over ⊕:

    = absolute_disp(n) ⊕ (min i : 1 ≤ i ≤ k : disp(cᵢ))
    = absolute_disp(n) ⊕ 0                                   {by ENF4}
    = absolute_disp(n)

*Inductive step.* Let n be an internal node at height h > 1, and assume
the result holds for all internal nodes at height < h. Then:

    min_leaf(n)
    = (min i : 1 ≤ i ≤ k : min_leaf(cᵢ))
    = (min i : 1 ≤ i ≤ k : absolute_disp(cᵢ))               {by IH}
    = (min i : 1 ≤ i ≤ k : absolute_disp(n) ⊕ disp(cᵢ))
    = absolute_disp(n) ⊕ (min i : 1 ≤ i ≤ k : disp(cᵢ))
    = absolute_disp(n) ⊕ 0                                   {by ENF4}
    = absolute_disp(n)

*At the root:* absolute_disp(root) = disp(root), since the root has no
ancestors. Therefore disp(root) = min_leaf(root). ∎

ENF4-GLOBAL ensures the root's bounding box is tight — it starts at the
true minimum leaf address. Combined with ENF1 (which gives the extent from
minimum to maximum), this means the root's displacement and width describe
the exact bounding box of the entire enfilade.

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

    result(E, Q) ⊇ { e ∈ leaves(E) : span(e) ∩ Q ≠ ∅ }

Every leaf whose address range overlaps Q is included in the result. No
qualifying leaf is omitted.

This is the *soundness* direction: completeness says nothing about whether
non-qualifying leaves might be included (they should not be, but that is
the next property). ENF5 must hold regardless of the tree's shape — after
any sequence of insertions, splits, rebalances, and deletions.

The composition laws ENF0 and ENF1 are what make ENF5 achievable through
hierarchical pruning rather than exhaustive search. We state ENF5 as an
axiom that any correct implementation must satisfy, and show that the
structural invariants make it achievable — that is, that the pruning
criteria implied by ENF0/ENF0'/ENF1 are conservative.

*For sequential enfilades:* The structural invariants ENF0 and ENF0'
guarantee that no qualifying leaf can be hidden behind a pruning decision.
ENF0' establishes that each leaf has a unique position within exactly one
child's range. ENF0 ensures that the accumulated offset correctly locates
each child's range. Therefore a traversal that descends into every child
whose range [Lᵢ, Lᵢ + w(cᵢ)) intersects Q will reach all qualifying
leaves. Two obligations fall on any correct traversal algorithm: (i) it
must visit *all* children whose ranges overlap Q (not just the first), and
(ii) after descending into a qualifying child and returning, it must
continue scanning rightward to find subsequent qualifying children. The
offset-accumulation walk satisfies both by scanning the full sibling
sequence, but these are obligations on the traversal, not consequences of
the structural invariants alone. ENF5 constrains the *result*; the
structural invariants constrain the *representation*; a correct traversal
is the bridge between them.

*For multi-dimensional enfilades:* The structural invariant ENF1 guarantees
that every leaf's address lies within its ancestor's bounding box at every
level. If a leaf at address p lies within Q, then p lies within its
parent's bounding box, which lies within the grandparent's, and so on up to
the root. Therefore a traversal that descends into every child whose
bounding box intersects Q will reach all qualifying leaves. The obligation
on a correct traversal is to check *every* child at each internal node
against Q, not merely the first qualifying one. Since sibling order is
semantically free (ENF12), there is no shortcut that avoids checking all
children.


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
needing to know or care about the internal tree structure.

**Theorem (Tree-shape independence).** For any two enfilades E₁ and E₂
with identical logical content — that is, leaves(E₁) = leaves(E₂) as sets
— but possibly different internal structures:

    result(E₁, Q) = result(E₂, Q)   for all queries Q

*Proof.* Let S = { e ∈ leaves(E₁) : span(e) ∩ Q ≠ ∅ }. Since leaves(E₁)
= leaves(E₂), S is also { e ∈ leaves(E₂) : span(e) ∩ Q ≠ ∅ }. By ENF5,
result(E₁, Q) ⊇ S and result(E₂, Q) ⊇ S. By ENF6 (uniqueness) and the
fact that no non-qualifying leaf appears in the result, result(E₁, Q) = S
and result(E₂, Q) = S as sets. By ENF7, both results are sorted by the
same dimension, so the sequences are identical. ∎

Tree-shape independence is a consequence of ENF5 + ENF6 + ENF7, not an
independent property. It confirms that the result is a function of the
content and the query alone.


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

as a set. (Since E : A ⇀ V is a partial function, each address maps to at
most one value, so the leaf set is indeed a set, not a multiset.) The set
of leaf entries is invariant under rebalancing. No leaf is created,
destroyed, or modified by structural operations.

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

  (a) ENF0/ENF0' or ENF1 holds at every internal node of E'
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


## Worked examples

We now verify the properties against concrete enfilade states.

### Sequential enfilade: INSERT with split

Consider a sequential enfilade with maximum occupancy M = 3 and three
leaves:

    root [w=9]
    ├── leaf a: addr 0, w=3  (content "abc")
    ├── leaf b: addr 3, w=3  (content "def")
    └── leaf c: addr 6, w=3  (content "ghi")

We verify the invariants. ENF0: w(root) = 3 + 3 + 3 = 9. ✓ ENF0': child
ranges are [0,3), [3,6), [6,9) — disjoint, union is [0,9). ✓ ENF8:
children(root) = 3 ≤ M = 3. ✓

Now INSERT "XY" at position 4, splitting leaf b into b₁ (addr 3, w=1,
content "d") and b₂ (addr 5, w=2, content "ef"), with a new leaf x (addr
4, w=2, content "XY") between them. The root now has 4 children, violating
ENF8 (4 > M = 3). A split is required.

After splitting root into root₁ and root₂, with a new root above them:

    new_root [w=11]
    ├── root₁ [w=5]
    │   ├── leaf a:  addr 0, w=3
    │   ├── leaf b₁: addr 3, w=1
    │   └── leaf x:  addr 4, w=2
    └── root₂ [w=6]
        ├── leaf b₂: addr 6, w=2
        └── leaf c:  addr 8, w=3

We verify post-split invariants. ENF0: w(root₁) = 3 + 1 + 2 = 6? No —
that gives 6, but the true extent is positions [0,6) which has width 6.
Let us be more careful. After INSERT at position 4, the address space has
expanded: original positions [0,4) are unchanged, the new content occupies
[4,6), and original positions [4,9) have shifted to [6,11). So:

    new_root [w=11]
    ├── root₁ [w=6]
    │   ├── leaf a:  addr 0, w=3  ("abc")
    │   ├── leaf b₁: addr 3, w=1  ("d")
    │   └── leaf x:  addr 4, w=2  ("XY")
    └── root₂ [w=5]
        ├── leaf b₂: addr 6, w=2  ("ef")
        └── leaf c:  addr 8, w=3  ("ghi")

ENF0: w(root₁) = 3 + 1 + 2 = 6. w(root₂) = 2 + 3 = 5. w(new_root) = 6 +
5 = 11. ✓ ENF0': root₁ children cover [0,3), [3,4), [4,6) — disjoint,
union [0,6). root₂ children cover [6,8), [8,11) — disjoint, union [6,11).
new_root children cover [0,6), [6,11) — disjoint, union [0,11). ✓ ENF9:
leaf set is {a, b₁, x, b₂, c}, representing all original content plus the
inserted content. No leaf was lost, duplicated, or fused. ✓ ENF10: partition
(leaves(root₁) ∪ leaves(root₂) = all leaves), occupancy (3 ≤ M, 2 ≤ M),
and composition law all hold. ✓

**Range query [3, 7) on the result.** The query starts at new_root. Offset
0, first child root₁ has range [0, 6). Since [0,6) ∩ [3,7) = [3,6) ≠ ∅,
descend into root₁. Inside root₁: offset 0, leaf a has [0,3), [0,3) ∩
[3,7) = ∅, skip. Offset 3, leaf b₁ has [3,4), [3,4) ∩ [3,7) = [3,4) ≠ ∅,
collect b₁. Offset 4, leaf x has [4,6), [4,6) ∩ [3,7) = [4,6) ≠ ∅,
collect x. Return to new_root. Offset 6, root₂ has [6,11), [6,11) ∩
[3,7) = [6,7) ≠ ∅, descend into root₂. Inside root₂: offset 6, leaf b₂
has [6,8), [6,8) ∩ [3,7) = [6,7) ≠ ∅, collect b₂. Offset 8, leaf c has
[8,11), [8,11) ∩ [3,7) = ∅, skip. Result: {b₁, x, b₂} in address order
[3,4,6]. ENF5: all qualifying leaves included. ✓ ENF6: each leaf appears
exactly once. ✓ ENF7: results in ascending address order. ✓

### Multi-dimensional enfilade: normalisation and query

Consider a POOM (V-enfilade) with two entries mapping virtual positions to
permanent I-addresses. Entry e₁ maps V-position 5 to I-address 10; entry
e₂ maps V-position 2 to I-address 7. Displacements are 2D vectors
(V-component, I-component).

After inserting e₁ first, the tree has:

    root [disp=(5,10), w=(1,1)]
    └── leaf e₁ [disp=(0,0)]

ENF4: leaf e₁ has displacement (0,0) = 0. ✓ The absolute address of e₁ is
(5,10) ⊕ (0,0) = (5,10). ✓

Now insert e₂ with address (2,7). The new leaf gets displacement (2,7)
relative to root, but normalisation must ensure ENF4. Before normalisation:

    root [disp=(5,10)]
    ├── leaf e₁ [disp=(0,0)]   absolute: (5,10) ⊕ (0,0) = (5,10)
    └── leaf e₂ [disp=(2,7)]   — wrong, not normalised yet

We must re-derive. The new leaf's absolute address must be (2,7). So its
displacement relative to the current root is (2,7) ⊖ (5,10) = (−3,−3).
But displacements must be non-negative (they represent offsets in the
tumbler space). This forces renormalisation: the minimum of children's
displacements is min((0,0), (−3,−3)) = (−3,−3). Absorb into root:

    new root disp = (5,10) ⊕ (−3,−3) = (2,7)
    e₁ new disp = (0,0) ⊖ (−3,−3) = (3,3)
    e₂ new disp = (−3,−3) ⊖ (−3,−3) = (0,0)

After normalisation:

    root [disp=(2,7), w=(4,4)]
    ├── leaf e₁ [disp=(3,3)]   absolute: (2,7) ⊕ (3,3) = (5,10) ✓
    └── leaf e₂ [disp=(0,0)]   absolute: (2,7) ⊕ (0,0) = (2,7)  ✓

ENF4: min((3,3), (0,0)) = (0,0). ✓ ENF1: origin = (2,7), far corner =
max((2+1,7+1), (5+1,10+1)) = max((3,8), (6,11)) = (6,11), extent = (6,11)
− (2,7) = (4,4). ✓ ENF4-GLOBAL: disp(root) = (2,7) = min((5,10), (2,7))
componentwise. ✓ ENF2: absolute address of e₁ = (2,7) ⊕ (3,3) = (5,10).
Commutativity: (3,3) ⊕ (2,7) = (5,10) as well. ✓

**Range query Q = [3,6) × [8,12) on V-dimension.** The root's bounding
box in V is [2, 6). Q's V-range is [3,6). Intersection: [3,6) ≠ ∅, so
descend. Check e₁: V-address 5 ∈ [3,6) and I-address 10 ∈ [8,12)? Yes.
Collect e₁. Check e₂: V-address 2 ∈ [3,6)? No. Skip. Result: {e₁}. Since
the traversal checks each child independently (no offset accumulation),
sibling order does not affect the result. ✓


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
| ENF0' | Sequential partition: children's ranges are disjoint, contiguous, and cover [0, w(n)) | introduced |
| ENF1 | Multi-dimensional enfilade parent extent = tight bounding box (componentwise min/max) of children | introduced |
| ENF2 | Absolute address = sum of displacements along root-to-leaf path; (D, ⊕, 0) is a commutative monoid | introduced |
| ENF3 | Displacement right-inverse: (a ⊖ b) ⊕ b = a | introduced |
| ENF3' | Right-inverse holds within same-subspace displacements; cross-subspace sums never arise in structural ops | introduced |
| ENF4 | Zero-minimum normalisation: min child displacement = 0 at every internal node (multi-dimensional) | introduced |
| ENF4-GLOBAL | Root displacement = componentwise minimum of all leaf addresses (theorem from ENF4) | introduced |
| ENF5 | Range query completeness: every leaf overlapping the query is included | introduced |
| ENF6 | Range query uniqueness: every qualifying leaf visited exactly once | introduced |
| ENF7 | Result ordering: range query results sorted by queried dimension | introduced |
| ENF8 | Maximum occupancy: children(n) ≤ M for all nodes | introduced |
| ENF8' | Minimum occupancy: children(n) ≥ 1 for all non-root, non-empty nodes | introduced |
| ENF9 | Rebalancing preserves the leaf set exactly | introduced |
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
