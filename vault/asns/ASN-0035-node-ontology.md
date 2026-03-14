# ASN-0035: Node Ontology

*2026-03-14*

We are looking for a precise characterization of what a *node* is in the Xanadu docuverse. The word suggests physical infrastructure — a server, a machine, a network endpoint — but this is misleading. An abstract specification must identify the structural role the node plays in the address space independently of any physical realization. Three questions guide us: what is a node, how do nodes enter the docuverse, and what invariants must the set of all nodes satisfy?

Our primary evidence comes from two authorities. Nelson establishes the conceptual architecture through Literary Machines — "the docuverse is the occupied tumbler-space, as occupied by conceptually assigned positions, even if nothing represents them in storage." Gregory's implementation in udanax-green reveals the structural consequences — a node turns out to be nothing more than a tumbler prefix, carrying no mutable state of its own. Where these two accounts converge, we have high confidence. Where they diverge, we choose the principle that would bind any correct implementation.


## The node as position

We begin where the tumbler algebra begins. By the field parsing definition of T4 (ValidAddress, ASN-0034), every address in the system is parsed into up to four fields — node, user, document, element — separated by zero-valued components. The zero count determines the hierarchical level:

- `zeros(t) = 0`: node address (node field only)
- `zeros(t) = 1`: user address (node and user fields)
- `zeros(t) = 2`: document address (node, user, and document fields)
- `zeros(t) = 3`: element address (all four fields)

**Definition (Node address).** A tumbler `n ∈ T` is a *node address* iff `n > 0 ∧ zeros(n) = 0`. We write `N = {n ∈ T : n > 0 ∧ zeros(n) = 0}` for the set of all node addresses.

Membership in `N` is decidable from the tumbler alone — T2 (IntrinsicComparison) and T3 (CanonicalRepresentation) guarantee this. The tumbler `[1, 3, 7]` is recognizable as a node address by inspection: three positive components, no zeros. The tumbler `[1, 0, 3]` is not — one zero separator places it at account level.

Now we confront the central question: what *is* a node, beyond an address? Nelson's answer is startling in its minimalism. A node is a conceptual position on the developing tumbler line. The system need not store anything to represent it:

> "No specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements."

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them."

A node exists the moment its address is baptized — before any content is stored there, before any accounts are created under it. At its most minimal, a node needs only a tumbler address, bestowed by its parent. The address carries two facts: ancestry (the node descends from a parent in the forking tree) and ownership (someone baptized this number and controls what spawns beneath it). That is the conceptual minimum.

Gregory confirms this architecturally. When `docreatenode_or_account` creates a node, it allocates a tumbler address and an empty POOM orgl in the global granfilade. There is no `struct node` anywhere in the codebase — no node-level data structure that indexes accounts, no capability list, no configuration record. The `GRANORGL` record for a node is identical to that for a document. The `NODE` constant in `xanadu.h` is a routing tag used at allocation time to choose the right address sub-range; it leaves no trace in the stored record. The node *is* the address. The address *is* the node.

This gives us our first property:

**N0 (Ghost Element).** A node address `n ∈ N` is a valid target for spanning and linking regardless of whether any content has been allocated under `n`. The node's identity is its address; no stored representation is required for the address to be meaningful.

The ghost element principle holds because the tumbler algebra is self-contained. The ordering (T1), the prefix relation, and span well-definedness (T12) are all computable from tumblers alone, without consulting any data structure. A span covering `[1, 5]` through `[1, 7]` is well-defined even if no content exists under node `[1, 6]` — T12 requires only that `ℓ > 0` and the action point of `ℓ` falls within `#s`, both arithmetic conditions on the span's start and length. For linking, the reduction is equally direct: a link's endsets are sets of spans (by definition from the shared vocabulary), so link well-formedness reduces to the well-formedness of each constituent span, which is again arithmetic (T12). No stored representation at the target address participates in either check. Nelson: "A span that contains nothing today may at a later time contain a million documents." The address space pre-exists its population. An implementation that required a stored node record before allowing spans or links to reference the node's address would violate N0.

To track which positions in `N` have been deliberately created, we introduce a state component:

**Σ.nodes** — The set of baptized node addresses in the current system state, with `Σ.nodes ⊆ N`. At genesis, `Σ.nodes = {r}` — exactly the root node, nothing else.

The distinction between `N` (all possible node positions) and `Σ.nodes` (occupied positions) is the ghost element principle made formal. Addresses in `N \ Σ.nodes` are syntactically valid — they can be compared, spanned, targeted by links — but they have not been baptized and cannot serve as parents for further allocation.


## Identity: assigned, not derived

We must establish how node identity relates to content. Nelson is explicit that identity is *assigned* through a delegation mechanism, not derived from what the node contains:

> "Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node ... may in turn designate ... new nodes ... by forking their integers. We often call this the 'baptism' of new numbers."

> "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document."

The tumbler carries ancestry and ownership but no semantic information about what the node contains or does. Two nodes may hold identical content without becoming identical; conversely, an empty node and a richly populated one are equally valid positions on the tumbler line. This is not content-addressing. The I-address encodes provenance — where content was first created — not a hash of what it contains. Two identical strings created independently on different nodes receive different addresses with different node prefixes.

**N1 (Identity by Assignment).** A node's identity is its tumbler address, assigned through baptism by the parent node's owner. Identity is permanent (T8, ASN-0034), positional (determined by ancestry in the forking tree), and independent of any content or operational state stored at or beneath the address.

Gregory confirms the assignment model directly. The reference implementation hardcodes the node's own tumbler as a compile-time constant: `defaultaccount = {0,0,0,0, 1,1,0,1,0,...}` in `be.c:37`, installed at startup via `movetumbler(&defaultaccount, &task.account)`. There is no configuration file key for the node address (`rcfile.c` supports port, host, and directory names, but no tumbler field). There is no discovery protocol, no negotiation, no content-based derivation. The backend declares "I am `1.1`" and that declaration is permanent. A multi-node deployment would assign different constants to different installations. The address is a name given at birth, not a hash computed from behavior.

A consequence: two distinct nodes *can* hold identical content. Nelson describes this not as an edge case but as a core feature of the architecture. Content moves between nodes for rapid access, load rebalancing, and redundancy. Each node holds a "microcosm" — a subset that "shrinks and grows." What distinguishes nodes is not their contents but their addresses.


## The node tree

The set `N` carries a natural tree structure inherited from the prefix relation.

**Definition (Node parent).** For node `n = [n₁, ..., nₐ]` with `a > 1`, the *parent* of `n` is `parent(n) = [n₁, ..., nₐ₋₁]`. Every component of `parent(n)` is positive (since every component of `n` is positive), so `parent(n) ∈ N`.

**Definition (Node depth).** `depth(n) = #n`, the number of components in the tumbler.

We observe that `parent(n) ≼ n` (proper prefix) and `depth(parent(n)) = depth(n) - 1`. The ancestor relation — the transitive closure of `parent` — is well-founded: every ascending chain terminates after at most `depth(n) - 1` steps. But does it terminate at a unique root?

Nelson is unambiguous: "The server address always begins with the digit 1, since all other servers are descended from it. This ... permits referring to the entire docuverse by '1' on the first position." A single root is not convention — it is what makes the docuverse a single unified space. Multiple roots would fragment the address space into disconnected components, each unreachable from the others by prefix traversal. The contiguous-subtree property (T5, ASN-0034) would hold within each fragment but not across them; a span starting at one root could never cover content under another.

**N2 (Single Root).** There exists exactly one node of minimal depth, `r = [1]`, and `r ∈ Σ.nodes` in every reachable state. Every baptized node descends from the root:

  `(A n ∈ Σ.nodes : n ≠ r ⟹ r ≼ n)`

*Derivation.* We proceed by induction on the reachable states. In the initial state, `Σ.nodes = {r}`, and the claim holds vacuously. For the inductive step, assume the claim holds in state `σ` and consider a BAPTIZE(actor, p) operation producing child `n`. By BAPTIZE's precondition, `p ∈ Σ.nodes`. If `p = r`, then `n = inc(r, 1) = [1, 1]` or `n = inc(max(children(r)), 0) = [1, c + 1]`; in either case `r ≼ n`. If `p ≠ r`, then by the inductive hypothesis `r ≼ p`; since `n` extends `p` by one component (TA5), we have `p ≼ n`, so `r ≼ p ≼ n` gives `r ≼ n`.

We note that the syntactic set `N` is broader than `Σ.nodes` — it includes addresses like `[2]`, `[3, 5]`, `[42]` that satisfy the zero-count condition but have no chain of baptisms from `[1]`. These addresses are syntactically valid node addresses (useful for N7's forward-reference principle) but cannot appear in `Σ.nodes` in any reachable state. The root prefix constraint is a consequence of the allocation discipline, not a syntactic filter.

Since `r = [1]` is a single-component positive tumbler with no zeros, it is a valid node address. Structural branching begins at position 2: `[1, 1]`, `[1, 2]`, `[1, 3]` are the first-generation children. The root `r` is the address of the entire docuverse — a span starting at `r` covers everything.

We now state the invariant on baptized nodes.

**N3 (Node Tree).** The pair `(Σ.nodes, parent)` forms a finite tree rooted at `r`:

  (a) `r ∈ Σ.nodes` — the root is always baptized.

  (b) `(A n ∈ Σ.nodes : n ≠ r ⟹ parent(n) ∈ Σ.nodes)` — the tree is closed under `parent`.

  (c) `Σ.nodes` is finite — at any moment, only finitely many nodes have been baptized.

Clause (b) is the *closure invariant*: one cannot baptize a node without its parent already being in `Σ.nodes`. The tree has no gaps — no orphan nodes floating without ancestry. This is a constraint on the operation that creates nodes, to which we now turn.


## Baptism

Nodes enter the docuverse through *baptism* — the creation of a new node address as a child of an existing baptized node. Nelson uses the term deliberately: "Whoever owns a specific node ... may in turn designate ... new nodes ... by forking their integers. We often call this the 'baptism' of new numbers."

The mechanism follows from the hierarchical increment TA5 (HierarchicalIncrement, ASN-0034). For a baptized node `p = [p₁, ..., pₐ]`:

- The *first child* is produced by `inc(p, 1)`. By TA5(d) with `k = 1`, this yields `[p₁, ..., pₐ, 1]` — the parent extended by one component set to `1`. Since `k - 1 = 0`, no zero separator is introduced. All components of the result are positive, so the result lies in `N`.

- *Subsequent children* are produced by `inc(lastChild, 0)`. By TA5(c), `[p₁, ..., pₐ, c]` becomes `[p₁, ..., pₐ, c + 1]`. Again no zero appears; the result lies in `N`.

We observe a crucial asymmetry. The node-to-child-node transition uses `inc(·, 1)` followed by `inc(·, 0)` — introducing no zero separator. The child extends the parent by a single positive digit *within the same field* of the T4 hierarchy. By contrast, the transition from one hierarchical level to the next (e.g., creating an account under a node) uses `inc(·, 2)`, which by TA5(d) with `k = 2` introduces one zero separator and crosses a field boundary.

This asymmetry explains why the node field can be arbitrarily deep: `[1, 2, 3, 7, 4]` is a valid five-level node address, all within the first field, before any `.0.` separator. Nodes nest within nodes without punctuation. The depth of nesting is bounded only by T0(b) (UnboundedLength, ASN-0034).

Gregory's implementation confirms this directly. The allocation code `docreatenode_or_account` at `do1.c:243-258` uses `makehint(NODE, NODE, ...)`, which yields `depth = 1` because `supertype == subtype`. It then calls `findisatoinsertnonmolecule`, which finds the highest existing sibling under the parent prefix and increments. Each child receives the next sequential address.

**Definition (Children).** `children(p) = {n ∈ Σ.nodes : parent(n) = p}` — the set of baptized children of node `p` in the current state.

We introduce an abstract authorization predicate: `authorized(actor, p)` holds when `actor` has the right to create children under node `p`. Nelson establishes the structural law: "The owner of a given item controls the allocation of the numbers under it." The predicate captures this law without committing to concrete mechanisms — who counts as an owner, how ownership is established, and whether delegation is possible are deferred to the account ontology ASN.

**BAPTIZE(actor, p)** — Create a new node as a child of `p`, invoked by agent `actor`.

*Precondition:* `p ∈ Σ.nodes ∧ authorized(actor, p)`

*Postcondition:* Let `C = children(p)` before the operation.

  - If `C = ∅`: the new node is `n = inc(p, 1) = [p₁, ..., pₐ, 1]`
  - If `C ≠ ∅`: the new node is `n = inc(max(C), 0)`, where `max` is under T1

In both cases:

  - `n ∈ N ∧ parent(n) = p` — the result is a valid node address whose parent is `p`
  - `post(Σ.nodes) = pre(Σ.nodes) ∪ {n}` — exactly one node is added
  - `(A m ∈ C : m < n)` — the new child exceeds all prior children under T1
  - `n ∉ pre(Σ.nodes)` — the address is fresh

*Frame:*

  - `(A m ∈ pre(Σ.nodes) : m ∈ post(Σ.nodes))` — no existing node is removed

The postcondition is deterministic: the new address is uniquely determined by the parent and the current set of children. This follows from T10a (AllocatorDiscipline, ASN-0034), which prescribes `inc(·, 0)` as the exclusive mechanism for sibling production, and T9 (ForwardAllocation, ASN-0034), which requires strict monotonic increase within each allocator's stream.

*Concrete trace.* We verify BAPTIZE through a three-step sequence, starting from genesis: `Σ.nodes = {[1]}`.

(1) BAPTIZE(actor, `[1]`). We have `C = children([1]) = ∅`, so `n = inc([1], 1) = [1, 1]` by TA5(d). Check: `[1, 1] ∈ N` (two positive components, no zeros). `parent([1, 1]) = [1] ∈ Σ.nodes`. Result: `Σ.nodes = {[1], [1, 1]}`. N3 holds: root present (a), `parent([1, 1]) = [1] ∈ Σ.nodes` (b), finite (c). N5 holds: `([1,1])_2 = 1`, confirming the first child has last component 1.

(2) BAPTIZE(actor, `[1]`). Now `C = {[1, 1]}`, so `n = inc([1, 1], 0) = [1, 2]` by TA5(c). Check: `[1, 2] ∈ N`. `parent([1, 2]) = [1] ∈ Σ.nodes`. `[1, 1] < [1, 2]` by T1 (divergence at position 2: `1 < 2`). Last components are 1 and 2, matching positions `i = 1` and `i = 2` — N5 holds. Result: `Σ.nodes = {[1], [1, 1], [1, 2]}`.

(3) BAPTIZE(actor, `[1, 1]`). Here `C = children([1, 1]) = ∅`, so `n = inc([1, 1], 1) = [1, 1, 1]` by TA5(d). Check: `[1, 1, 1] ∈ N`. `parent([1, 1, 1]) = [1, 1] ∈ Σ.nodes`. Depth increases: `depth([1, 1, 1]) = 3 > depth([1, 1]) = 2`. N3(b) satisfied. Result: `Σ.nodes = {[1], [1, 1], [1, 1, 1], [1, 2]}`. The tumbler ordering is `[1] < [1, 1] < [1, 1, 1] < [1, 2]` — depth-first linearization of the tree (N6).

*Verification that BAPTIZE preserves N3.* The root `r` is not removed (frame), so N3(a) holds. The new node `n` has `parent(n) = p ∈ Σ.nodes` (precondition), so N3(b) holds for `n`; all other nodes' parents are unchanged (frame). The set grows by one element, so N3(c) holds. BAPTIZE is well-defined for any baptized parent — by T0 (ASN-0034), there is always room for the next child.


## Monotonicity and sequential children

Two invariants govern the growth of the node set.

**N4 (Baptism Monotonicity).** The set of baptized nodes grows monotonically:

  `(A σ, σ' : σ precedes σ' : Σ.nodes(σ) ⊆ Σ.nodes(σ'))`

No operation removes a node from `Σ.nodes`. This is T8 (AllocationPermanence, ASN-0034) specialized to node addresses: once a position in the tree is occupied, it is occupied forever.

Why must this be so? Because every address allocated *under* a node — every account, document, and element — carries the node's tumbler as a prefix (this is a structural consequence of T4 and TA5: each allocation extends the parent via `tumblerincrement`, preserving the parent's prefix). Removing a node from the address space would invalidate every address beneath it. Since addresses, once allocated, are permanent (T8), the node that anchors them must be permanent too.

Nelson acknowledges that physical infrastructure can change: "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations." Content migrates; the address stays. A decommissioned node becomes a ghost element — addressable, linkable, but with no physical representation. Its content lives elsewhere; its address endures. Nelson also accepts that nodes go offline routinely: "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." Temporary unavailability is not removal from the address space.

**N5 (Sequential Children).** The children of any node form a complete initial segment of the positive integers in their last component. For `children(p) = {c₁, ..., cₖ}` ordered by T1:

  `(A i : 1 ≤ i ≤ k : (cᵢ)_{#cᵢ} = i)`

The first child has last component 1, and each subsequent child increments by exactly 1 — the children are `[p₁, ..., pₐ, 1], [p₁, ..., pₐ, 2], ..., [p₁, ..., pₐ, k]` with no gaps and no offset. This follows from T10a (AllocatorDiscipline, ASN-0034): `inc(·, 0)` advances the last significant component by 1, and no other mechanism produces siblings. Combined with T9 (ForwardAllocation, ASN-0034), if `[p₁, ..., pₐ, 3]` is baptized, then `[p₁, ..., pₐ, 1]` and `[p₁, ..., pₐ, 2]` were necessarily baptized earlier.

N5 means that siblings cannot be sparse in the *baptism* sense. Nelson's discussion of ghost elements — the possibility that baptized nodes may be entirely empty — is about *occupation*, not about gaps in the baptism sequence. A baptized but empty node is a ghost element: it occupies a position in `Σ.nodes` but nothing is stored under it.


## Structural ordering

We are looking for the relationship between the ordering of node addresses and the temporal sequence of their creation. Nelson resolves this directly:

> "Note that 'time' is not included in the tumbler. Time is kept track of separately."

The tumbler line carries a total ordering (T1), and every node address participates in it. But this ordering reflects the depth-first linearization of the forking tree, not the calendar. Consider: under the root `[1]`, node `[1, 1]` is baptized, then node `[1, 1, 1]` beneath it, then node `[1, 2]` as a second child of the root. On the tumbler line, the ordering is `[1, 1] < [1, 1, 1] < [1, 2]`. But `[1, 2]` was baptized *after* `[1, 1, 1]` and yet follows it on the line — not because `[1, 2]` was created later, but because the depth-first traversal visits all descendants of `[1, 1]` before moving to the next sibling.

Among siblings of a single parent, tumbler order *does* coincide with creation order — N5 (Sequential Children) ensures that children are numbered `1, 2, 3, ...` in the order of baptism. But across different branches, the relationship vanishes entirely.

**N6 (Structural, Not Temporal, Ordering).** The total order T1 restricted to `Σ.nodes` reflects the depth-first linearization of the node tree. Among siblings of a single parent, tumbler order coincides with baptism order. Across different branches, tumbler order reflects tree structure only. Time of baptism is metadata maintained separately from the address.

We observe why this must be so. A global temporal ordering would require either a central sequencer (violating the decentralized allocation principle of T10, ASN-0034) or consensus among independent allocators (violating the locality that makes the system practical). Nelson chose tree-structural ordering instead, which requires only local information: the parent assigns the next sibling number.


## Forward references

A cautious design might require that every reference target an existing entity. Nelson's architecture explicitly rejects this requirement:

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them."

> "A span that contains nothing today may at a later time contain a million documents."

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements."

This is not an edge case or a tolerated anomaly — it is a named, deliberate feature. Nelson goes further: the link type system *depends* on ghost elements as a core pattern. Link types are matched by *address*, not by content: "The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." A type address may designate a category even if nothing is ever stored there.

**N7 (Forward Reference Admissibility).** A reference (span, link endset, or type address) may target any address in `N`, regardless of whether that address is in `Σ.nodes`. No precondition on the referenced node's existence is imposed. This includes addresses like `[2, 3]` that no chain of baptisms from `[1]` can produce — such references are syntactically valid (the target is in `N`) and may resolve to empty content permanently, but they are not erroneous.

Formally, the well-definedness of a span `(s, ℓ)` under T12 (SpanWellDefined, ASN-0034) depends only on the arithmetic properties of `s` and `ℓ` — on whether `ℓ > 0` and the action point of `ℓ` falls within `#s`. Whether any content or node exists in the spanned region is irrelevant to well-definedness. A link whose endset includes addresses beneath an unbaptized node is syntactically and semantically valid; it may resolve to empty content, but it is not erroneous.

The deeper design principle: the address space is populated by *positions*, not by *objects*. The forking mechanism makes pre-existence requirements impractical in a decentralized system. Addresses are created by subdivision — the owner of `[1, 2]` can create `[1, 2, 1]`, `[1, 2, 2]`, `[1, 2, 3]` at will (T10a, ASN-0034). There is no way to atomically verify that a target address is populated before creating a reference to it, because the creator and the target may be on different nodes with no shared state. Nelson sidesteps this entirely: all addresses are valid; population is optional.

The docuverse is sparse by design. Only two kinds of entities are actually stored: bytes and links. Everything else — servers, accounts, documents — are "positions on the developing tumbler line." The address space is "the occupied tumbler-space — as occupied by conceptually assigned positions, even if nothing represents them in storage." Requiring pre-existence of referenced entities would contradict this fundamental architecture.


## Gradual admission

We are looking for whether node admission is an atomic event — the node is either fully present in the docuverse or fully absent — with no intermediate state. Nelson's answer is that admission is *explicitly gradual*:

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere."

The phrase "from the null case on up" names the starting state: empty. A new node begins with nothing and accumulates incrementally. Each increment leaves it in "canonical operating condition." There is no bootstrap phase where the node is partially broken, no transient invalid state during which invariants fail.

We identify at least three distinguishable phases in a node's lifecycle:

1. **Unbaptized** — the position exists in `N` but not in `Σ.nodes`. It can be targeted by references (N7) but cannot serve as a parent for further baptism.

2. **Baptized, empty** — the position is in `Σ.nodes`. It is a ghost element in the fullest sense. Accounts, documents, and content may be created beneath it at any future time. It is valid, addressable, and linkable, but stores nothing.

3. **Baptized, populated** — accounts, documents, and elements exist under the node's prefix. The node's content grows as further allocations occur.

The transition between these phases is progressive. No intermediate state is invalid. This is not merely a design aspiration but a structural consequence: BAPTIZE adds exactly one element to `Σ.nodes` while preserving all existing state. The act of address assignment is itself atomic (the address is either in `Σ.nodes` or it is not), but the *population* of the node is an unbounded, ongoing process.

**N8 (Always-Valid Intermediate States).** At every point during a node's lifecycle — from unbaptized address, through empty ghost element, to populated position — the system state satisfies all node invariants. There is no transient invalid state during node admission.

We verify this by enumerating the state-dependent and structural invariants separately. The state-dependent invariants require preservation proofs for BAPTIZE (the sole operation that modifies `Σ.nodes`):

- **N2 (Single Root):** BAPTIZE adds a new node `n` with `parent(n) = p ∈ Σ.nodes`. By the inductive derivation given in the N2 section, if `r ≼ p` in the pre-state (inductive hypothesis), then `r ≼ p ≼ n` in the post-state. The root `r` is not removed (frame). N2 is preserved.
- **N3 (Node Tree):** Preservation is shown above — BAPTIZE maintains root membership (frame), tree closure (precondition ensures parent is baptized), and finiteness (one element added).
- **N4 (Baptism Monotonicity):** BAPTIZE only adds to `Σ.nodes` (postcondition: `post(Σ.nodes) = pre(Σ.nodes) ∪ {n}`), and its frame condition prohibits removal. No operation decreases the set.
- **N5 (Sequential Children):** BAPTIZE produces the new child via `inc(max(C), 0)` when `C ≠ ∅`, advancing the last component by exactly 1 (TA5(c)). When `C = ∅`, the first child `inc(p, 1)` has last component 1, starting the gap-free sequence. In both cases, the complete initial segment property is maintained. (The initial state `Σ.nodes = {r}` satisfies N5 vacuously — the root has no children.)

The structural properties hold unconditionally from the tumbler algebra, independent of `Σ.nodes`:

- **N9 (Subtree Contiguity):** Follows from T5 (ContiguousSubtrees, ASN-0034) applied to the node prefix — no state dependency.
- **N10 (Subtree Disjointness):** Follows from T10 (PartitionIndependence, ASN-0034) applied to non-nesting node prefixes — no state dependency.
- **N16 (Prefix Propagation):** Follows from TA5 (HierarchicalIncrement, ASN-0034) — each `inc` operation preserves all components before the action point — no state dependency.

N8 follows from the same principle that makes the docuverse open-ended. Nelson: "A span that contains nothing today may at a later time contain a million documents." The empty state is as canonical as any other. An implementation that required a minimum level of population before declaring a node "valid" would violate both N0 (Ghost Element) and N8.


## Subtree properties

The node position anchors a subtree of the address space. Two structural properties follow from the tumbler algebra.

**N9 (Subtree Contiguity).** For any node `n ∈ N`, the set `{a ∈ T : n ≼ a}` is a contiguous interval under T1:

  `[n ≼ a ∧ n ≼ c ∧ a ≤ b ≤ c ⟹ n ≼ b]`

This is T5 (ContiguousSubtrees, ASN-0034) applied to the node prefix. A single span can address the entirety of a node's content. Nelson: "A link to or search of an account or node will find any of the documents under it." Contiguity is what makes hierarchical addressing useful for range queries and aggregation.

**N10 (Subtree Disjointness).** For nodes `m, n ∈ N` where neither is a prefix of the other (`m ⋠ n ∧ n ⋠ m`):

  `{a ∈ T : m ≼ a} ∩ {a ∈ T : n ≼ a} = ∅`

This is T10 (PartitionIndependence, ASN-0034) applied to node prefixes. The subtrees of non-ancestrally-related nodes are disjoint — addresses allocated under one cannot collide with addresses allocated under the other. This is the structural foundation for coordination-free allocation: because the subtrees do not overlap, independent allocators cannot produce conflicting addresses.

Gregory's code provides an instructive confirmation and warning. The global granfilade is a single flat tree containing all addresses from all nodes, interleaved by tumbler order. There is no structural partition by node in the storage layer. An early allocation bug caused `findpreviousisagr` to return an address under the *wrong* parent, because the search walked across prefix boundaries without a containment check. The fix — an explicit `tumblertruncate`/`tumblereq` guard at `granf2.c:228-233` — confirms that N10 is a property the allocation discipline must *maintain*, not one that any particular storage structure automatically *enforces*.


## Concurrent creation and structural disjointness

We are looking for what the system must guarantee when multiple allocators simultaneously create nodes. Nelson does not explicitly address this scenario in Literary Machines, but the tumbler architecture makes the answer fall out structurally.

The baptism mechanism operates through *owned numbers*: "The owner of a given item controls the allocation of the numbers under it." If Alice owns node `[1, 2]` and Bob owns node `[1, 3]`, Alice creates children `[1, 2, 1], [1, 2, 2], ...` and Bob creates `[1, 3, 1], [1, 3, 2], ...`. They operate in structurally disjoint subtrees. By T10 (PartitionIndependence, ASN-0034), their outputs are guaranteed distinct without any coordination.

**N11 (Coordination-Free Disjointness).** Two allocators operating under distinct, non-nesting prefixes produce disjoint outputs without inter-allocator communication. Uniqueness of the resulting addresses follows from the tree structure alone.

This is a direct application of GlobalUniqueness (ASN-0034). The architectural insight is that Nelson designed away the distributed consensus problem. Two nodes in different parts of the world can each create thousands of children per second without consulting each other, because their subtrees are structurally guaranteed disjoint. The hard problem of distributed uniqueness is eliminated by prefix partitioning.

The only point requiring serialization is within a *single parent's* allocation counter:

**N12 (Local Serialization Sufficiency).** The only serialization required for correct allocation is within a single parent's child-allocation counter. If two BAPTIZE operations target different parents, they may execute concurrently with no coordination.

This follows from BAPTIZE's deterministic postcondition: the new address depends only on the parent and its current children. Two operations under different parents consult disjoint portions of the state and modify disjoint portions of `Σ.nodes`.

Gregory's implementation uses a strictly stronger mechanism: a single-process, single-threaded event loop in `bed.c` that serializes all operations globally. The `select()` loop iterates over ready file descriptors and dispatches each request to completion before starting the next. This eliminates concurrency entirely — correct, but far more restrictive than what the abstract specification demands. A multi-process implementation need only serialize allocations sharing a parent, not globally. The reference implementation's global serialization is an engineering choice that happens to satisfy the weaker abstract requirement.


## Node homogeneity

We are looking for whether the design distinguishes different kinds of nodes — content-bearing vs. linking, primary vs. replica, master vs. subordinate. Nelson is emphatic that no such distinction exists:

> "The Xanadu document is the unit of the system. There is almost nothing in the Xanadu system but Xanadu documents."

> "By this convention, then, everything in the system is part of a document. No free-floating materials exist."

> "The link mechanism ties together the whole corpus of materials on the Xanadu system. There is essentially nothing in the Xanadu system except documents and their arbitrary links."

There is no "content node" vs "link node" vs "versioning node." The document is the sole organizational unit, and exactly two stored primitives exist within it: bytes and links. A document containing only links is just as valid as one containing only text. Versioning produces a new document with a new identity — not a new node type. "There is thus no 'basic' version of a document set apart from other versions," Nelson writes; versions are just documents whose addresses happen to be sub-addresses of other documents.

The node, being merely an address prefix, inherits this radical uniformity:

**N13 (Uniform Node Type).** There is exactly one type of node. All nodes participate identically in the address hierarchy. No structural distinction exists among nodes based on what content resides beneath them.

Gregory confirms this with negative evidence: there is no `struct node` in any header file. When `docreatenode_or_account` creates a node at `do1.c:243-258`, it calls the same `createorglgr` function used for documents and accounts, producing the same `GRANORGL` record type (a tumbler key plus an empty POOM enfilade). The `NODE`, `ACCOUNT`, `DOCUMENT` constants in `xanadu.h:140-143` are not runtime type tags — they are arguments to `makehint` that select the address sub-range. After `createorglgr` returns, no record of the hint's type persists in the granfilade leaf.

We can now state the strongest version of the node's ontological minimalism:

**N14 (No Node-Level Mutable State).** A node carries no mutable state of its own. Its identity is its tumbler address (permanent, by T8). Its "contents" are defined extensionally as the set of entities whose addresses carry the node's tumbler as a prefix — determined by the global address space, not by any per-node record. No per-node counter, capability list, or configuration survives across operations.

The BERT access-control table in Gregory's code (`bert.c`) tracks open/close state per *document per connection* — there is no BERT entry at the node level. The ownership check `isthisusersdocument` at `socketbe.c:197-201` compares the document's prefix against the current connection's account tumbler via `tumbleraccounteq` — a pure address computation, not a lookup in a per-node capability store.

The implication is clear: a node is not an object in any conventional sense. It is a *name* — a position on the tumbler line that anchors a subtree. Everything that makes a node "real" — accounts, documents, links, content — exists in that subtree, not in the node itself. The node is the address; the address, once assigned, is immutable.


## Allocation authority

The node position confers one fundamental right: the right to create new positions within its subtree.

**N15 (Allocation Authority).** BAPTIZE(actor, p) requires `authorized(actor, p)` — the abstract predicate introduced with the operation's specification. The authority is established at the moment of baptism and is permanent: once a subtree is delegated, the recipient's authority over it is irrevocable.

Nelson: "The owner of a given item controls the allocation of the numbers under it." And: "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore."

The authority flows downward at the point of baptism and does not require ongoing coordination with the parent. This is the architectural complement of N11 (Coordination-Free Disjointness): because each owner's subtree is structurally disjoint, local authority is sufficient for global consistency. No central registry participates.

Gregory's code reflects this through the per-connection `player[user].account` in `bed.c`. Each connected frontend operates under its own account tumbler, set via the `XACCOUNT` FEBE request at `fns.c:364-373`. The ownership check `isthisusersdocument` verifies that operations target addresses within the connection's own subtree. A single backend process can serve multiple account tumblers simultaneously — up to `MAX_PLAYERS = 25` concurrent connections in `socketbe.c`, each independently authorized under its own prefix. The serialization is at the allocation level (N12), not at the authorization level.


## Prefix propagation

One structural consequence deserves explicit statement because it connects the node to the hierarchy beneath it. Every address allocated under a node carries that node's tumbler as a prefix. This follows necessarily from the allocation discipline.

**N16 (Prefix Propagation).** For every address `a` allocated in the subtree rooted at node `n`:

  `n ≼ a`

The first `#n` components of `a` are identical to those of `n`.

*Derivation.* An account under node `n` receives address `inc(n, 2)` — by TA5(d) with `k = 2`, this appends a zero separator and an initial child value, leaving the first `#n` components of `n` intact. A document under that account is formed by further `tumblerincrement` calls, each of which by TA5(b) preserves all components before the action point. Since the action point is always at or beyond position `#n + 1`, the first `#n` components are never modified.

The home node of any address — the node from which it structurally descends — is therefore extractable by T4 field parsing: `home(a) = fields(a).node`. This assignment is permanent (by T8, no component of `a` ever changes) and partitions all allocated addresses by node of origin (by N10, non-nesting node prefixes produce disjoint subtrees). Two addresses with different node fields cannot be equal (by T3, CanonicalRepresentation).


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| Σ.nodes | `Σ.nodes ⊆ N` — the set of baptized node addresses in system state | introduced |
| N0 | Ghost element: a node address is valid for spanning and linking without stored content | introduced |
| N1 | Identity by assignment: node identity is its tumbler, assigned by baptism, permanent and content-independent | introduced |
| N2 | Single root: `r = [1]` is the unique minimal-depth node; `(A n ∈ Σ.nodes : n ≠ r ⟹ r ≼ n)` | introduced |
| N3 | `(Σ.nodes, parent)` is a finite tree rooted at `r`, closed under `parent` | introduced |
| N4 | Baptism monotonicity: `pre(Σ.nodes) ⊆ post(Σ.nodes)` for all operations | introduced |
| N5 | Sequential children: `(A i : 1 ≤ i ≤ k : (cᵢ)_{#cᵢ} = i)` — complete initial segment starting at 1 | introduced |
| N6 | Structural ordering: tumbler order reflects tree structure, not temporal sequence of creation | introduced |
| N7 | Forward reference admissibility: references may target any address in `N`, even if unbaptized | introduced |
| N8 | Always-valid intermediate states: every phase of a node's lifecycle satisfies all invariants | introduced |
| N9 | Subtree contiguity: `{a ∈ T : n ≼ a}` is contiguous under T1 | introduced |
| N10 | Subtree disjointness: non-ancestrally-related nodes have disjoint subtrees | introduced |
| N11 | Coordination-free disjointness: distinct-prefix allocators need no inter-allocator communication | introduced |
| N12 | Local serialization sufficiency: only same-parent allocations require serialization | introduced |
| N13 | Uniform node type: exactly one type of node; no structural subtyping | introduced |
| N14 | No node-level mutable state: a node carries no mutable state beyond its permanent address | introduced |
| N15 | Allocation authority: `authorized(actor, p)` — abstract precondition on BAPTIZE; account ontology refines | introduced |
| N16 | Prefix propagation: every address under node `n` carries `n` as a prefix; `home(a) = fields(a).node` | introduced |


## Open Questions

- Must the root node `[1]` be established by an explicit genesis operation, or is it an axiom present in every reachable state without having been created?
- What invariants must govern the transition from ghost element to operationally active node — is there a minimal readiness condition beyond address existence?
- What must the system guarantee about the addressability of content beneath a node whose operator has permanently ceased to function?
- Can allocation authority for a subtree be transferred from one agent to another without invalidating existing addresses?
- Must every baptized node eventually contain at least one account, or may permanently empty ghost nodes persist indefinitely?
- Is the depth of the node tree abstractly unbounded, or must a correct implementation guarantee reachability only below some finite maximum depth?
- What consistency properties must hold when a single physical infrastructure serves multiple node addresses simultaneously?
- Under what conditions may two nodes sharing a common ancestor merge their serialization domains for allocation efficiency?
