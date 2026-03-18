# ASN-0035 Formal Statements

*Source: ASN-0035-node-ontology.md (revised 2026-03-14) — Index: 2026-03-14 — Extracted: 2026-03-14*

## Definition — NodeAddress

A tumbler `n ∈ T` is a *node address* iff `n > 0 ∧ zeros(n) = 0`. The set of all node addresses:

`N = {n ∈ T : n > 0 ∧ zeros(n) = 0}`

## Definition — NodeParent

For node `n = [n₁, ..., nₐ]` with `a > 1`, the *parent* of `n` is:

`parent(n) = [n₁, ..., nₐ₋₁]`

Every component of `parent(n)` is positive, so `parent(n) ∈ N`.

## Definition — NodeDepth

`depth(n) = #n`, the number of components in the tumbler.

## Definition — NodeChildren

`children(p) = {n ∈ Σ.nodes : parent(n) = p}` — the set of baptized children of node `p` in the current state.

## Definition — DFSPreOrder

The *depth-first pre-order* of `(Σ.nodes, parent)` is defined recursively: visit node `p`, then for each child `c₁, c₂, ..., cₖ` of `p` in T1 order, recursively visit the subtree rooted at `cᵢ`. Write `a ≺_dfs b` when `a` precedes `b` in this traversal.

## Definition — BAPTIZE

**BAPTIZE(actor, p)** — Create a new node as a child of `p`, invoked by agent `actor`.

*Precondition:* `p ∈ Σ.nodes ∧ authorized(actor, p)`

*Postcondition:* Let `C = children(p)` before the operation.

- If `C = ∅`: the new node is `n = inc(p, 1) = [p₁, ..., pₐ, 1]`
- If `C ≠ ∅`: the new node is `n = inc(max(C), 0)`, where `max` is under T1

In both cases:

- `n ∈ N ∧ parent(n) = p`
- `post(Σ.nodes) = pre(Σ.nodes) ∪ {n}`
- `(A m ∈ C : m < n)`
- `n ∉ pre(Σ.nodes)`

*Frame:*

- `(A m ∈ pre(Σ.nodes) : m ∈ post(Σ.nodes))`

---

## Σ.nodes — BaptizedNodes (INV, predicate(State))

`Σ.nodes ⊆ N`

The set of baptized node addresses in the current system state. At genesis, `Σ.nodes = {r}` — exactly the root node, nothing else.

---

## N0 — GhostElement (LEMMA, lemma)

A node address `n ∈ N` is a valid target for spanning and linking regardless of whether any content has been allocated under `n`. The node's identity is its address; no stored representation is required for the address to be meaningful.

The well-definedness of a span `(s, ℓ)` under T12 requires only that `ℓ > 0` and the action point of `ℓ` falls within `#s` — both arithmetic conditions on the span's start and length. Whether any content or node exists in the spanned region is irrelevant to well-definedness.

---

## N1 — IdentityByAssignment (INV, predicate(Tumbler))

A node's identity is its tumbler address, assigned through baptism by the parent node's owner. Identity is permanent (T8, ASN-0034), positional (determined by ancestry in the forking tree), and independent of any content or operational state stored at or beneath the address.

---

## N2 — SingleRoot (INV, predicate(State))

There exists exactly one node of minimal depth, `r = [1]`, and `r ∈ Σ.nodes` in every reachable state. Every baptized node descends from the root:

`(A n ∈ Σ.nodes : n ≠ r ⟹ r ≼ n)`

---

## N3 — NodeTree (INV, predicate(State))

The pair `(Σ.nodes, parent)` forms a finite tree rooted at `r`:

(a) `r ∈ Σ.nodes`

(b) `(A n ∈ Σ.nodes : n ≠ r ⟹ parent(n) ∈ Σ.nodes)`

(c) `Σ.nodes` is finite

---

## N4 — BaptismMonotonicity (INV, predicate(State, State))

`(A σ, σ' : σ precedes σ' : Σ.nodes(σ) ⊆ Σ.nodes(σ'))`

---

## N5 — SequentialChildren (INV, predicate(State))

For `children(p) = {c₁, ..., cₖ}` ordered by T1:

`(A i : 1 ≤ i ≤ k : (cᵢ)_{#cᵢ} = i)`

---

## N6 — StructuralOrdering (LEMMA, lemma)

For any `a, b ∈ Σ.nodes`:

`a < b` under T1  ⟺  `a ≺_dfs b`

*Derived from N3, N5, T1.*

Inter-subtree ordering proof obligations:

(i) `p` precedes all descendants: since `p ≼ d` for every descendant `d`, T1 case (ii) gives `p < d`

(ii) Every node in subtree `Dᵢ` precedes every node in `Dᵢ₊₁`: for `cᵢ = [p₁, ..., pₐ, i]` and `cᵢ₊₁ = [p₁, ..., pₐ, i + 1]`, any `d ∈ Dᵢ` has component `i` at position `a + 1`; any `e ∈ Dᵢ₊₁` has component `i + 1` at position `a + 1`; divergence at position `a + 1` with `i < i + 1` gives `d < e` by T1 case (i)

---

## N7 — ForwardReferenceAdmissibility (LEMMA, lemma)

A reference (span, link endset, or type address) may target any address in `N`, regardless of whether that address is in `Σ.nodes`. No precondition on the referenced node's existence is imposed. This includes addresses that no chain of baptisms from `[1]` can produce — such references are syntactically valid and may resolve to empty content permanently, but they are not erroneous.

The well-definedness of a span `(s, ℓ)` under T12 depends only on the arithmetic properties of `s` and `ℓ`. A link whose endset includes addresses beneath an unbaptized node is syntactically and semantically valid.

---

## N8 — AlwaysValidStates (LEMMA, lemma)

At every point during a node's lifecycle — from unbaptized address, through empty ghost element, to populated position — the system state satisfies all node invariants. There is no transient invalid state during node admission.

*Derived from N2–N6 preservation under BAPTIZE:*

- N2 preserved: if `r ≼ p` in pre-state then `r ≼ p ≼ n` in post-state; root not removed (frame)
- N3 preserved: BAPTIZE maintains root membership (frame), tree closure (precondition ensures parent is baptized), finiteness (one element added)
- N4 preserved: postcondition `post(Σ.nodes) = pre(Σ.nodes) ∪ {n}` and frame prohibit removal
- N5 preserved: new child via `inc(max(C), 0)` advances last component by exactly 1 (TA5(c)); first child `inc(p, 1)` has last component 1
- N6 follows from N3 and N5 by structural induction

---

## N9 — SubtreeContiguity (LEMMA, lemma)

For any node `n ∈ N`, the set `{a ∈ T : n ≼ a}` is a contiguous interval under T1:

`[n ≼ a ∧ n ≼ c ∧ a ≤ b ≤ c ⟹ n ≼ b]`

---

## N10 — SubtreeDisjointness (LEMMA, lemma)

For nodes `m, n ∈ N` where neither is a prefix of the other (`m ⋠ n ∧ n ⋠ m`):

`{a ∈ T : m ≼ a} ∩ {a ∈ T : n ≼ a} = ∅`

---

## N11 — CoordinationFreeDisjointness (LEMMA, lemma)

Two allocators operating under distinct, non-nesting prefixes produce disjoint outputs without inter-allocator communication. Uniqueness of the resulting addresses follows from the tree structure alone.

*Direct application of GlobalUniqueness (ASN-0034): for allocators under `p` and `q` with `p ⋠ q ∧ q ⋠ p`, all outputs of the first lie in `{a : p ≼ a}` and all outputs of the second in `{a : q ≼ a}`; by N10 these sets are disjoint.*

---

## N12 — LocalSerializationSufficiency (LEMMA, lemma)

The only serialization required for correct allocation is within a single parent's child-allocation counter. If two BAPTIZE operations target different parents, they may execute concurrently with no coordination.

*Follows from BAPTIZE's deterministic postcondition: the new address depends only on the parent and its current children. Two operations under different parents consult disjoint portions of the state and modify disjoint portions of `Σ.nodes`.*

---

## N13 — UniformNodeType (INV, predicate(Tumbler))

There is exactly one type of node. All nodes participate identically in the address hierarchy. No structural distinction exists among nodes based on what content resides beneath them.

---

## N14 — NoNodeMutableState (INV, predicate(Tumbler))

A node carries no mutable state of its own. Its identity is its tumbler address (permanent, by T8). Its "contents" are defined extensionally as the set of entities whose addresses carry the node's tumbler as a prefix — determined by the global address space, not by any per-node record. No per-node counter, capability list, or configuration survives across operations.

---

## N15 — AllocationAuthority (PRE, requires)

BAPTIZE(actor, p) precondition:

`p ∈ Σ.nodes ∧ authorized(actor, p)`

where `authorized(actor, p)` is an abstract predicate: `actor` has the right to create children under node `p`. Refinement of `authorized` is deferred to the account ontology ASN.

---

## DC1 — AuthorityPermanence (INV, predicate(State, State))

The account ontology must define `authorized` such that authority, once established, is irrevocable:

`(A actor, p, σ : authorized(actor, p) in σ ⟹ (A σ' : σ precedes σ' : authorized(actor, p) in σ'))`

---

## N16 — PrefixPropagation (LEMMA, lemma)

For every address `a` allocated in the subtree rooted at node `n`:

`n ≼ a`

The first `#n` components of `a` are identical to those of `n`.

*Derivation:* An account under node `n` receives address `inc(n, 2)` — by TA5(d) with `k = 2`, this appends a zero separator and an initial child value, leaving the first `#n` components of `n` intact. Each subsequent `tumblerincrement` call by TA5(b) preserves all components before the action point; since the action point is always at or beyond position `#n + 1`, the first `#n` components are never modified.

`home(a) = fields(a).node`
