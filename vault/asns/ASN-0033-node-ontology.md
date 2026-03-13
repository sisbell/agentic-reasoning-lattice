# ASN-0033: Node Ontology

*2026-03-12*

We are looking for a precise characterization of what a *node* is in the Xanadu docuverse. The word suggests physical infrastructure — a server, a machine, a network endpoint — but this is misleading. An abstract specification must identify the structural role the node plays in the address space independently of any physical realization. We need to answer three questions: what is a node, how does a node enter the docuverse, and what invariants must the set of all nodes satisfy?

Our primary evidence comes from Nelson's design writings and Gregory's implementation. Nelson establishes the conceptual architecture; Gregory's code reveals the structural consequences. Where the two converge, we have confidence. Where they diverge, we note the gap and choose the principle that would bind any correct implementation.


## The node as position

We begin with what the tumbler algebra already tells us. By T4 (HierarchicalParsing), every I-space address `t` is parsed into four fields — node, user, document, element — separated by zero-valued components. The count of zeros determines the hierarchical level:

- `zeros(t) = 0`: node address
- `zeros(t) = 1`: user (account) address
- `zeros(t) = 2`: document address
- `zeros(t) = 3`: element address

A node address is therefore a positive tumbler with no zero components — it consists of the node field alone.

**Definition (Node address).** A tumbler `n ∈ T` is a *node address* iff `n > 0 ∧ zeros(n) = 0`. We write `N = {n ∈ T : n > 0 ∧ zeros(n) = 0}` for the set of all node addresses.

Membership in `N` is decidable from the tumbler alone (T2, T3). No external data structure need be consulted. The tumbler `[1, 3, 7]` is recognizable as a node address by inspection: three positive components, no zeros. The tumbler `[1, 0, 3]` is not — it contains a zero separator and is therefore an account address.

Now we must confront a subtlety that many treatments miss. A node is not a stored object. Nelson calls nodes *ghost elements*: "conceptual positions on the tumbler line." The system need not store anything to represent a node. One may link to a node address, span across it, refer to everything beneath it — all without any "node record" existing in storage. Nelson is explicit: "no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." And yet "these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them."

Gregory confirms this architecturally. The granfilade and spanfilade are single global structures — there is no per-node storage partition. When a node is created, the implementation allocates an empty POOM orgl at the node's address, but this is a bookkeeping entry in the global tree, not a "node object." There is no node-level data structure that indexes accounts under a node; the relationship is implicit in the tumbler prefix convention.

This gives us our first property — a constraint that any implementation must respect:

**N0 (Ghost Element).** A node address `n ∈ N` is a valid target for spanning and linking regardless of whether any content has been allocated under `n`. The node's identity is its address; no stored representation is required for the address to be meaningful.

The ghost element principle holds because the tumbler algebra is self-contained. The ordering (T1), the prefix relation (PrefixOf), and span well-definedness (T12) are all computable from tumblers alone. A span covering `[1, 5]` through `[1, 7]` is well-defined even if node `[1, 6]` has never been occupied — "a span that contains nothing today may at a later time contain a million documents." The address space pre-exists its population. An implementation that required a stored node record before allowing spans or links to reference the node's address would violate N0.

This separates *identity* from *occupation*. The set `N` of all possible node addresses is infinite — every positive zero-free tumbler qualifies. But the set of *baptized* nodes, those deliberately brought into the docuverse, is finite and grows over time. We introduce the state component that tracks this:

**Σ.nodes** — The set of baptized node addresses in the current system state, with `Σ.nodes ⊆ N`. At genesis, `Σ.nodes` contains at least the root node.

The distinction between `N` (all possible positions) and `Σ.nodes` (occupied positions) is the ghost element principle made formal. Addresses in `N \ Σ.nodes` are meaningful — they can be spanned, linked to, compared — but they have not been baptized and cannot yet serve as parents for further allocation.


## The node tree

The set `N` carries a natural tree structure inherited from the prefix relation.

**Definition (Node parent).** For node `n = [n₁, ..., nₐ]` with `a > 1`, the *parent* of `n` is `parent(n) = [n₁, ..., nₐ₋₁]`. Since every component of `n` is strictly positive, every component of `parent(n)` is strictly positive, and so `parent(n) ∈ N`.

**Definition (Node depth).** `depth(n) = #n`, the number of components in the tumbler.

We observe that `parent(n) ≼ n` (proper prefix) and `depth(parent(n)) = depth(n) - 1`. The ancestor relation — the transitive closure of `parent` — is well-founded: every ascending chain terminates after at most `depth(n) - 1` steps. But does it terminate at a *unique* root?

Nelson is unambiguous: "The server address always begins with the digit 1, since all other servers are descended from it. This ... permits referring to the entire docuverse by '1' on the first position." A single root is not merely convention — it is what makes the docuverse a single unified space. Multiple roots would fragment the address space into disconnected components, each unreachable from the others by prefix traversal. The contiguous-subtree property (T5) would hold within each fragment but not across them; a span starting at one root could never cover content under another.

**N1 (Single Root).** There exists exactly one node of minimal depth, `r = [1]`, and `r ∈ Σ.nodes` in every reachable state. Every node `n ∈ N` with `n ≠ r` satisfies `r ≼ n`.

The first component of every node address is `1`. Since `r = [1]` is a single-component tumbler, it is a prefix of every node address by the definition of PrefixOf. The structural branching begins at position 2: `[1, 1]`, `[1, 2]`, `[1, 3]` are the first-generation children. The root `r` is the address of the entire docuverse — a span starting at `r` covers everything.

We now state the invariant on baptized nodes.

**N2 (Node Tree).** The pair `(Σ.nodes, parent)` forms a finite tree rooted at `r`:

  (a) `r ∈ Σ.nodes` — the root is always baptized.

  (b) `(A n ∈ Σ.nodes : n ≠ r ⟹ parent(n) ∈ Σ.nodes)` — the tree is closed under `parent`.

  (c) `Σ.nodes` is finite — at any moment, only finitely many nodes have been baptized.

Clause (b) is the *closure invariant*: one cannot baptize a node without its parent already existing. The tree has no gaps — no orphan nodes floating without ancestry. This is a constraint on the operation that creates nodes, to which we now turn.


## Baptism

Nodes enter the docuverse through *baptism* — the creation of a new node address as a child of an existing baptized node. Nelson uses the term deliberately: "Whoever owns a specific node ... may in turn designate ... new nodes ... by forking their integers. We often call this the 'baptism' of new numbers."

The mechanism follows from the hierarchical increment of ASN-0001. For a baptized node `p = [p₁, ..., pₐ]`:

- The *first child* is produced by `inc(p, 1)`. By TA5(d) with `k = 1`, this yields `[p₁, ..., pₐ, 1]` — the parent extended by one component set to `1`. Since `k - 1 = 0`, no zero separator is introduced. All components of the result are positive, so the result lies in `N`.

- *Subsequent children* are produced by `inc(lastChild, 0)`. By TA5(c), `[p₁, ..., pₐ, c]` becomes `[p₁, ..., pₐ, c + 1]`. Again no zero appears; the result lies in `N`.

We observe a crucial asymmetry. The node-to-node transition uses `inc(·, 1)` followed by `inc(·, 0)` — increment depth 1, introducing no zero separator. The child extends the parent by a single positive digit within the *same field* of the T4 hierarchy. By contrast, the transition from one T4 level to the next (e.g., creating a document under an account) uses `inc(·, 2)`, which by TA5(d) with `k = 2` introduces one zero separator and crosses a field boundary.

This asymmetry explains why the node field can be arbitrarily deep: `[1, 2, 3, 7, 4]` is a valid five-level node address, all within the first field, before any `.0.` separator. Nodes nest within nodes without punctuation. The depth of nesting is bounded only by T0 (UnboundedComponents) — every component can grow without limit, and positions can be added without limit.

Gregory's implementation confirms this directly. The allocation code uses `makehint(NODE, NODE, ...)` with `depth = 1` for node creation: when `supertype == subtype`, `depth = 1`; the zero separator appears only when the types differ, yielding `depth = 2`. Golden test evidence shows node addresses `[1, 1, 0, 1, 1]`, `[1, 1, 0, 1, 2]`, `[1, 1, 0, 1, 3]` — each exactly one mantissa digit beyond the parent, with no `.0.` boundary crossed at the node level.

We now state the operation formally.

**Definition (Children).** `children(p) = {n ∈ Σ.nodes : parent(n) = p}` — the set of baptized children of node `p` in the current state.

**BAPTIZE(p)** — Create a new node as a child of `p`.

*Precondition:* `p ∈ Σ.nodes`

*Postcondition:* Let `C = children(p)` before the operation.

  - If `C = ∅`: the new node is `n = inc(p, 1) = [p₁, ..., pₐ, 1]`
  - If `C ≠ ∅`: the new node is `n = inc(max(C), 0)`, where `max` is under T1

In both cases:

  - `n ∈ N ∧ parent(n) = p` — the result is a node address whose parent is `p`
  - `post(Σ.nodes) = pre(Σ.nodes) ∪ {n}` — exactly one node is added
  - `(A m ∈ C : m < n)` — the new child exceeds all prior children under T1

*Frame:*

  - `(A m ∈ pre(Σ.nodes) : m ∈ post(Σ.nodes))` — no existing node removed
  - `(A a ∈ I : post(content(a)) = pre(content(a)))` — no I-space content modified

The postcondition is deterministic: the new address is uniquely determined by the parent and the current set of children. This follows from T10a (AllocatorDiscipline), which prescribes `inc(·, 0)` as the exclusive mechanism for sibling production, and T9 (ForwardAllocation), which requires strict monotonic increase.

*Verification that BAPTIZE preserves N2.* The root `r` is not removed (frame condition), so N2(a) holds. The new node `n` has `parent(n) = p ∈ Σ.nodes` (precondition), so N2(b) holds for `n`; all other nodes' parents are unchanged (frame). The set grows by exactly one element, so N2(c) holds. BAPTIZE is well-defined for any baptized parent — by T0, there is always room for the next child.

We now state the invariants that BAPTIZE maintains across all operations.

**N3 (Baptism Monotonicity).** The set of baptized nodes grows monotonically:

  `(A σ, σ' : σ precedes σ' : Σ.nodes(σ) ⊆ Σ.nodes(σ'))`

No operation removes a node from `Σ.nodes`. This is T8 (AddressPermanence) specialized to node addresses: once a position in the tree is occupied, it is occupied forever. Nelson: "any address of any document in an ever-growing network may be specified by a permanent tumbler address."

**N4 (Sequential Children).** The children of any node form a sequential, gap-free sequence. For `children(p) = {c₁, ..., cₖ}` ordered by T1:

  `(A i : 1 ≤ i < k : (cᵢ)_{depth(cᵢ)} + 1 = (cᵢ₊₁)_{depth(cᵢ₊₁)})`

Consecutive siblings differ by exactly 1 in their last component. This follows from T10a: `inc(·, 0)` advances the last significant component by 1, and no other mechanism produces siblings. Combined with T9, if `[p, 3]` is baptized, then `[p, 1]` and `[p, 2]` were necessarily baptized earlier.

*Remark.* N4 implies that siblings cannot be sparse in the *baptism* sense. Nelson's discussion of ghost elements — "you may have nodes 1.1 and 1.3 without 1.2 ever existing" — refers to the potential for baptized nodes to be *empty* (no accounts, no documents, no content stored beneath them), not to gaps in the baptism sequence itself. A baptized but empty node is a ghost element par excellence: it occupies a position in `Σ.nodes` but nothing is stored under it.


## The content hierarchy

Every I-space address carries its node of origin as a prefix. This follows necessarily from the allocation discipline and has important consequences.

**N5 (Prefix Propagation).** For every I-space address `a` allocated under node `n`:

  `n ≼ a`

*Proof sketch.* Address allocation works by extending from a parent address. An account under node `n` receives an address of the form `n.0.u` — the node prefix `n` followed by a zero separator and the account identifier. A document under that account sits at `n.0.u.0.d`. An element within that document sits at `n.0.u.0.d.0.e`. At each level, the new address is formed by appending to the parent via TA5 increments. Since TA5 never modifies any component before the action point, and the action point is always at or beyond position `#n + 1`, the first `#n` components of `a` equal those of `n`. By the definition of PrefixOf, `n ≼ a`. □

Gregory confirms this through the allocation code. Every `tumblerincrement` call places new content at `idx + rightshift` where `idx` is the last nonzero position of the parent address. The parent's prefix is structurally preserved. An explicit containment guard (Bug Fix #2 in the source) was added because without it, a search for the highest address under one parent could return an address under a *different* parent — the flat storage structure does not enforce prefix containment, so the allocator must.

We can now extract the home node from any I-address.

**Definition (Home node).** For I-space address `a`, define `home(a) = fields(a).node` — the node field extracted by the T4 parsing function. By N5, `home(a)` is the node under which `a` was originally allocated. We call this the *home node* of `a`.

The home node is permanent — it is structurally embedded in the I-address, and no operation can modify it (T8). Nelson makes the design intent clear: "The I-address encodes origin, not current physical location." Content may physically reside on many nodes through replication, but its identity — its permanent I-address — records where it was born.

**N6 (Content Home Partition).** The function `home` partitions all allocated I-addresses by node. For distinct nodes `m ≠ n`:

  `{a ∈ I : home(a) = m} ∩ {a ∈ I : home(a) = n} = ∅`

Every content address belongs to exactly one node, and this assignment is permanent. The partition is by *origin*, not by physical location.

*Proof.* By T4, every I-space address has exactly one node field. Since T4 guarantees that the node field consists of all leading positive components before the first zero separator, and T3 (CanonicalRepresentation) ensures tumbler identity is component-wise, two addresses with different node fields are under different nodes. The `home` function is therefore well-defined and injective over nodes. □

Two structural consequences follow from the tree and prefix properties together.

**N7 (Subtree Disjointness).** For nodes `m, n ∈ N` where `m ⋠ n ∧ n ⋠ m` (neither is a prefix of the other):

  `{a ∈ T : m ≼ a} ∩ {a ∈ T : n ≼ a} = ∅`

This is T10 (PartitionIndependence) applied to node prefixes. The subtrees of non-ancestrally-related nodes are disjoint — content allocated under one cannot collide with content allocated under the other.

Gregory's implementation provides an instructive negative example. The global granfilade is a single flat B-tree containing all addresses from all nodes, interleaved by tumbler order. There is no structural partition by node; the `findpreviousisagr` search walks the entire tree, guided by an upper-bound tumbler. The original allocation code, lacking a post-search containment check, produced a cross-account allocation: searching under `[1, 1, 0, 2]` found `[1, 1, 0, 1, 0, 1]` (under a different account) and incremented it, yielding `[1, 1, 0, 1, 0, 2]` — an address under the *wrong* parent. The fix added an explicit `tumblertruncate`/`tumblereq` guard after each search. The lesson for the abstract specification is clear: N7 is a property that the allocation discipline must *maintain*, not one that the storage structure *enforces*.

**N8 (Subtree Contiguity).** For any node `n ∈ N`, the set `{a ∈ T : n ≼ a}` is a contiguous interval under T1:

  `[n ≼ a ∧ n ≼ c ∧ a ≤ b ≤ c ⟹ n ≼ b]`

This is T5 (ContiguousSubtrees) applied to the node prefix. The consequence is that a single span can address the entirety of a node's content — "everything under node `[1, 3]`" is a well-defined, contiguous range on the tumbler line. This is what makes hierarchical addressing useful for range queries and aggregation. Nelson: "A link to or search of an account or node will find any of the documents under it."


## The allocation boundary

We have established what a node is (a position in the address tree), how nodes enter (baptism), and how content relates to nodes (prefix propagation and home partition). It remains to clarify what authority the node position confers — and, equally important, what it does not.

**N9 (Allocation Authority).** Only an agent authorized by the parent node `p` can invoke BAPTIZE(p). The node position confers the right to create new positions within its subtree.

This is Nelson's "owned numbers" principle: "The owner of a given item controls the allocation of the numbers under it." No central registry participates. The parent baptizes children by local decision — "No coordination with any other node is required. No central registry." This locality is what makes the tree extensible without global consensus: each owner extends their own branch independently, and T10 (PartitionIndependence) guarantees the extensions cannot collide.

We emphasize that N9 is strictly about *position allocation* — the creation of new addresses in the tree. It says nothing about what is later stored at those addresses. Nelson draws this distinction with care: "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." The allocation authority flows downward at the point of baptism, but once a subtree is delegated, the recipient's authority over that subtree is permanent and irrevocable. The node is a custodial position, not a governing one.

We note two further properties that the node does *not* impose:

**N10 (No Visibility Boundary).** A node imposes no visibility restriction on its content. All published content within every node is universally addressable across the entire docuverse. The node field in an I-address indicates storage provenance, not access scope.

Nelson: "The function of BEBE is to meld the contents of separate Xanadu servers into a single unified space." The tumbler line (T1) provides a single total order over all addresses regardless of node. Links created on one node may reference content on any other, and "the target node plays no role in establishing that link" — link creation is a unilateral, local operation; only link *traversal* involves communication with the target. Visibility boundaries, where they exist, are per-document (private vs. published), orthogonal to node membership.

The docuverse is one space. Nodes are positions within it, not walls around portions of it.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| Σ.nodes | `Σ.nodes ⊆ N` — the set of baptized node addresses in system state | introduced |
| N0 | Ghost element: a node address is valid for spanning and linking without stored content | introduced |
| N1 | Single root: `r = [1]` is the unique minimal-depth node; `(A n ∈ N : r ≼ n)` | introduced |
| N2 | `(Σ.nodes, parent)` is a finite tree rooted at `r`, closed under `parent` | introduced |
| N3 | Baptism monotonicity: `pre(Σ.nodes) ⊆ post(Σ.nodes)` for all operations | introduced |
| N4 | Sequential children: consecutive siblings differ by 1 in their last component | introduced |
| N5 | Prefix propagation: `(A a ∈ I, n ∈ N : a` allocated under `n ⟹ n ≼ a)` | introduced |
| N6 | Content home partition: `home(a)` assigns each I-address to exactly one node, permanently | introduced |
| N7 | Subtree disjointness: `m ⋠ n ∧ n ⋠ m ⟹ {a : m ≼ a} ∩ {a : n ≼ a} = ∅` | introduced |
| N8 | Subtree contiguity: `{a ∈ T : n ≼ a}` is contiguous under T1 | introduced |
| N9 | Allocation authority: only the parent's authorized agent can invoke BAPTIZE | introduced |
| N10 | No visibility boundary: nodes impose no access restriction on their content | introduced |


## Open Questions

- What invariants must govern the delegation of allocation authority from a node to the accounts beneath it?
- Must the root node `[1]` be baptized by an explicit genesis operation, or is it implicitly present in every reachable state?
- What must the system guarantee about content addressability when a node's operator permanently ceases to function?
- Can a node address be *reserved* — preventing its allocation to another party — without being baptized?
- What properties must the home-node assignment satisfy when content is transcluded into a document residing on a different node?
- Must every baptized node eventually contain at least one account, or can permanently empty ghost nodes persist indefinitely?
- Is the depth of the node tree abstractly unbounded, or must an implementation guarantee reachability below some maximum depth?
- Under what conditions, if any, may allocation authority for a subtree be transferred from one agent to another?
