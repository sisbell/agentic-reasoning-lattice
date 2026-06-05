# ASN-0103: CREATENEWDOCUMENT Operation

*2026-06-04*

## The Question

A user, owning some account, asks the system for a new, empty document. What exactly happens? Four sub-questions structure the inquiry:

- *What is allocated* — what new state comes into being in the content store, the entity set, and the document's arrangement?
- *What is preserved* — what does the operation guarantee about every document that already existed, and about the shared content store?
- *What distinguishes the result from a document made by forking* — at the level of what the new document shares with prior documents?
- *What invariants must the completed operation maintain* — and atomically, so that no observable intermediate state violates them?

The answer must be sharp enough to measure an implementation against, and abstract enough that two implementations meeting it are externally indistinguishable.

## Background: A Place Is Not Content

The foundation separates two things that ordinary file systems conflate. The **content store** `C : T ⇀ Val` binds content values to I-addresses; once `a ∈ dom(C)`, the binding is permanently fixed (S0, ASN-0036). The **entity set** `E ⊆ T` records the allocated organisational addresses — nodes, accounts, documents — that are *not* content (ASN-0047). A document is an entity, not a content value: documents inhabit `E`, never `dom(C)`.

This separation is the whole point of the operation we are specifying. Nelson is explicit that creating a document allocates a *place* and adds no *content*:

> "CREATENEWDOCUMENT: This creates an empty document. It returns the id of the new document." (4/65)

What is returned is an *id* — a tumbler address — not stored bytes. The deeper principle is that of *ghost elements*: an address may be a real, addressable position on the tumbler line with nothing stored beneath it.

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." (4/23)

So the entire effect of CREATENEWDOCUMENT divides cleanly along the place/content seam: it modifies the *entity set* (one new document position) and leaves the *content store* untouched. Gregory's implementation confirms the seam exactly — document creation writes a new entry into the document index but never advances the content I-address high-water mark; in his words, "content granfilade unchanged, document granfilade modified." We shall see that every claim about the operation flows from this single asymmetry: **an address is allocated; no content is.**

## The Operation's Input

CREATENEWDOCUMENT takes one argument: an **account** `A` under which the document is to be created, with `A ∈ E` and `Account(A)` (so `T4-valid(A) ∧ zeros(A) = 1`, ASN-0045). It is invoked on behalf of a principal who owns `A` — a principal `π` with `pfx(π) ≼ A` in the ownership-prefix order (ASN-0042). The operation returns the address `d` of the new document.

We take the account as given. The provisioning of nodes and accounts is a separate concern (out of scope); here the account already exists in `E`, and our task is to baptise exactly one new document beneath it.

There is no content argument. This is not an omission — it is the defining shape of the operation. Content enters a document only through later operations (INSERT, COPY, MAKELINK), each of which deposits bytes or links. Creation deposits nothing.

## Discovering the Effects

We reason from Nelson's intent backward to the formal post-state. Three effects must obtain together; the third is the largest, because it is a frame.

### Effect One: One Address Is Baptised

The new document must occupy a fresh, permanent, unique position beneath the account. In the foundation's allocator vocabulary this is the account's **document sub-allocator** `A_doc(A)` (AllocatorHierarchy, ASN-0047): its first emission is `inc(A, 2)`, a document-level address with `zeros = 2` and `parent(·) = A`; successive emissions advance by `inc(·, 0)`.

We split on whether `A` already has documents. Here we must be careful: not every document-level entity whose parent is `A` belongs to `A_doc(A)`. A **version** is forked off a *document* (`inc(d_src, 1)`, ASN-0047); by `K.δ-ID.zeros-0/1` and `K.δ-ID.parent-0/1` it preserves both zero-count and parent, so a version `v` satisfies `Document(v) ∧ parent(v) = A` just as a true document does — yet it lives in the *version* chain `A_v(d_src) = S(d_src, 1)`, not in `A_doc(A)`. Selecting the frontier by parent alone would let a version masquerade as a document and collide a future allocation with a future fork. Length separates the two cleanly. `A_doc(A)` is the SiblingStream `S(A, 2)` (ASN-0040): its first emission `inc(A, 2)` has length `#A + 2` (TA5(d), ASN-0034) and every sibling step `inc(·, 0)` preserves length (TA5(c)), so every document-chain emission has length exactly `#A + 2`. Versions, forked one level deeper, carry length `≥ #A + 3`. We therefore restrict the document frontier by length:

  `D_A = {e ∈ E : Document(e) ∧ parent(e) = A ∧ #e = #A + 2}`,

which collects exactly the entities of `E` carrying the document chain's structural signature beneath `A`. We claim `D_A = E ∩ S(A, 2)`, and prove both inclusions, because it is the *reverse* direction — that every member of `D_A` has the canonical stream form `[A, 0, j]` — that the load-bearing facts below actually consume. The easy direction is immediate: every `A_doc(A) = S(A, 2)` emission present in `E` is a document of length `#A + 2` with parent `A`, so `E ∩ S(A, 2) ⊆ D_A`. The load-bearing direction `D_A ⊆ S(A, 2)` follows from the unique parse (T4b, ASN-0034). Take any `e ∈ D_A`. Since `Document(e)`, `e` parses canonically as `e = N(e).0.U(e).0.D(e)`; since `parent(e) = A`, the document-case parent projection gives `N(e).0.U(e) = A` (parent, ASN-0047), so `e = A.0.D(e)`. Then `#e = #A + 1 + #D(e)`, and the length constraint `#e = #A + 2` forces `#D(e) = 1`, whence `e = [A, 0, D(e)₁]` — exactly the form of an `S(A, 2)` element. Hence `D_A ⊆ S(A, 2)`, and with the easy inclusion `D_A = E ∩ S(A, 2)`. Three consequences, each used below, now follow: when `D_A ≠ ∅`, `d_prev = max(D_A) ∈ S(A, 2)`, so `inc(d_prev, 0) ∈ S(A, 2)` lands on the stream with `sig = #A + 2`; and every member `d_i ∈ D_A` carries the canonical form `[A, 0, i]` that the version-dominance argument relies on. Then the allocated address is

  `d = inc(A, 2)` if `D_A = ∅`,
  `d = inc(d_prev, 0)` otherwise, where `d_prev = max(D_A)`.

The maximum is well-defined: `E` is finite at every reachable state — `Σ₀.E = {n₀}` is a singleton (ASN-0047) and each transition adjoins at most one entity (`K.δ`: `E' = E ∪ {e}`) — so its subset `D_A` is finite and, when non-empty, has a T1-maximum. We claim only what the load-bearing facts below require: in both cases `d` lies on `A_doc(A) = S(A, 2)` and strictly exceeds every member of `D_A`. For `D_A = ∅`, `d = inc(A, 2)` is the stream's first element; otherwise `d = inc(max(D_A), 0)` is the sibling step immediately past the current frontier `max(D_A)`. We do not assert that `D_A` is a contiguous initial prefix of the stream — that would make `d` *the* next unallocated emission, a stronger claim than freshness, monotonicity, and uniqueness need. We must verify three structural facts and one separation fact.

*Document level.* For the first case, `inc(A, 2)` is a depth-2 descent: by the increment law (TA5, ASN-0034) it appends two components, and by the field-advancement law `zeros(inc(A, 2)) = zeros(A) + 1 = 2` (B5, ASN-0040), so `Document(d)` holds. For the subsequent case, `inc(d_prev, 0)` is a sibling step: it preserves length and zero-count (TA5(c), B5a; ASN-0040), so `zeros(d) = zeros(d_prev) = 2` and `parent(d) = parent(d_prev) = A` (K.δ-ID.parent-0, ASN-0047). Either way `Document(d) ∧ parent(d) = A`.

*Validity.* The baptism produces a T4-valid address. Depth-2 descent off an account satisfies the validity bound `zeros(A) + (2 − 1) = 2 ≤ 3` (B6, ValidDepth; ASN-0040), and the sibling step preserves T4 (TA5a, ASN-0034). So `T4-valid(d)`.

*Freshness.* The address is new: `d ∉ E`. The cited freshness lemmas of ASN-0093 (FirstEmission, ChainEnumerationInjectivity) are stated only for the content and link sub-allocators `A_C(d)`, `A_L(d)`; the document sub-allocator `A_doc(A)` is not in their scope. But `A_doc(A) = S(A, 2)` is a SiblingStream, so it inherits the requisite properties directly from ASN-0040. Its enumeration is strictly increasing under T1 (S0, StreamOrdering; ASN-0040): for a subsequent emission `d = inc(d_prev, 0) > d_prev ≥ e` for every prior `e ∈ D_A`, placing `d` strictly past the entire existing document chain; for the first emission `D_A = ∅`, so `d = inc(A, 2)` is the stream's first element and no document under `A` precedes it. Distinctness from the version chains is structural rather than ordinal: each `A_v(d_i) = S(d_i, 1)` is a *distinct namespace* from `A_doc(A) = S(A, 2)` — the parent–depth pairs `(d_i, 1)` and `(A, 2)` differ — so `S(A, 2) ∩ S(d_i, 1) = ∅` by namespace disjointness (B7, ASN-0040). Hence `d` collides with no version address, present or future, and with no other document-chain emission (B8, Uniqueness; ASN-0040). Cross-account collisions are excluded by partition independence (T10, ASN-0034): `d` extends the account prefix `A`, and any address under a different account `A' ≠ A` is prefix-incomparable to it, hence distinct.

*Strict advance over every prior address under `A`.* We claim `d` strictly exceeds every document address ever baptised under `A` — document-chain emission or version — including documents created but never written into. For same-allocator (document-chain) emissions this is S0 above. For a version `v` we cannot appeal to T9 (ForwardAllocation), which orders only same-allocator pairs: `v` lives in `A_v(d_i)`, a different allocator from `A_doc(A)`. We argue directly by lexicographic order. Every `A_doc(A)` emission has the form `[A, 0, j]` — the depth-2 descent `inc(A, 2)` fixes positions `#A+1, #A+2` to `0, 1`, and `inc(·, 0)` advances only position `#A+2`. Write `d = [A, 0, p]`. A version `v` extends some document `d_i = [A, 0, i] ∈ D_A` as a prefix, and `d_i ≤ d_prev = [A, 0, p−1]`, so `i ≤ p − 1 < p`. Then `d` and `v` agree on positions `1..#A+1` and at position `#A+2` carry `p` versus `i < p`; hence `d > v` by T1 case (i) (ASN-0034), regardless of how deep `v` nests. The frontier counter at position `#A+2` dominates every version counter beneath an earlier document. The high-water mark is read from the live entity set — an empty document is still in `E`, so the next allocation steps over it — and there is no mechanism by which a later document is baptised onto an already-occupied position (B8, Uniqueness; ASN-0040). This is the abstract content of Nelson's permanence guarantee:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid." (4/19)

### Effect Two: The Arrangement Is Empty

The document is born holding nothing. Its arrangement is the empty partial function:

  `M'(d) = ∅`, i.e. `dom(M'(d)) = ∅` and `ran(M'(d)) = ∅`.

There are no V-positions, hence no V→I mappings, hence no I-addresses referenced. This is the formal reading of "creates an empty document" (4/65). Because the Vstream is dense — a contiguous sequence of positions — a document with zero references occupies zero V-addresses; there is no inherent starting state, no default text, no placeholder the user can rely on. Content is added only by subsequent operations.

We note one consequence immediately, to be discharged as an invariant below: with `ran(M'(d)) = ∅`, referential integrity `ran(M'(d)) ⊆ dom(C')` (S3★, ASN-0047) holds *vacuously* for `d`. An empty document cannot dangle.

### Effect Three: Nothing Else Changes

This is the largest effect and the heart of the user's guarantee. Creating `d` must leave the identities and content of every existing document wholly untouched. We enumerate the frame.

*The content store is untouched.* `C' = C`. No byte is added, no value altered, no address removed:

  `dom(C') = dom(C) ∧ (A a : a ∈ dom(C) : C'(a) = C(a))`.

This is the abstract statement of "adds a place, not content." The document is, at the instant of creation, a ghost element: a position in `E` with nothing stored beneath it in `C`.

*The link store is untouched.* `L' = L`. Creation makes no link.

*The provenance relation is untouched.* `R' = R`. Provenance records which document referenced which content (ASN-0047); with no content and no reference, there is nothing to record.

*Every existing entity persists.* `E ⊆ E'`, and the only new member is `d`:

  `E' = E ∪ {d}` with `d ∉ E`.

In particular every existing document, account, and node keeps its address. Entity permanence (P1, ASN-0047) is preserved, and the document population grows by *exactly one* (CND.E): `|E'_doc| = |E_doc| + 1`.

*Every existing document's arrangement is untouched.* `(A d' : d' ∈ E_doc : M'(d') = M(d'))`. No other document's Vstream, content, or links shift. This is the cross-document frame: the operation reaches into no subtree but the one it baptises.

These frames exhaust the state components `(C, L, E, M, R)`. The only net change is `E' = E ∪ {d}` together with `M'(d) = ∅`. Everything else is held fixed. The operation is, in Nelson's phrase, strictly additive: it forks one new permanent address beneath the creator's account and disturbs nothing that exists.

### A Note on Sub-Allocator Activation

One consequence of Effect One is worth stating explicitly because it underwrites every later operation on `d`. The entity-allocation event that places `d` into `E_doc` *activates* two element-level sub-allocators scoped to `d`: the content sub-allocator `A_C(d)` with anchor `[d.0.s_C]` and the link sub-allocator `A_L(d)` with anchor `[d.0.s_L]` (SubAllocatorBundle, ASN-0047). Activation is not population: at the post-state both chains have emitted nothing, so the anchors are not yet in `dom(C') ∪ dom(L')`. They stand ready. The first INSERT into `d` will draw `[d.0.s_C.1]` from `A_C(d)`; the first MAKELINK will draw `[d.0.s_L.1]` from `A_L(d)`. Creation is what makes those subspaces *available* — lazily materialised, never pre-filled.

### A Worked Example

Fix `A = [1, 0, 1]` — an account (`zeros(A) = 1`, `#A = 3`). Suppose its first document already exists, `d1 = inc(A, 2) = [1, 0, 1, 0, 1]` (`#d1 = 5 = #A + 2`, `zeros = 2`), and `d1` has been forked once, producing a version `v1 = inc(d1, 1) = [1, 0, 1, 0, 1, 1]` (`#v1 = 6`, with `zeros(v1) = zeros(d1) = 2` by B5 and `parent(v1) = parent(d1) = A`). So `v1` is `Document(·)` with `parent = A` — it satisfies the *unrestricted* document predicate — yet it is a version, inhabiting `A_v(d1) = S(d1, 1)`, not `A_doc(A) = S(A, 2)`.

Now invoke CREATENEWDOCUMENT(A). The length filter is decisive: `#A + 2 = 5`, so `D_A = {e : Document(e) ∧ parent(e) = A ∧ #e = 5} = {d1}` — `v1`, of length 6, is excluded. Thus `d_prev = max(D_A) = d1` and

  `d = inc(d1, 0) = [1, 0, 1, 0, 2]`  (`#d = 5`, `zeros = 2`, `parent(d) = A`).

Check the claims. *CND.alloc:* `d = [1,0,1,0,2]` is the second emission of `A_doc(A) = S(A, 2)` (first `[1,0,1,0,1] = d1`, then `inc(d1,0)`), with `Document(d)`, `zeros(d) = 2`, `parent(d) = A`, `T4-valid(d)`. *CND.empty:* `M'(d) = ∅`. *CND.E:* `E' = E ∪ {[1,0,1,0,2]}` and `[1,0,1,0,2] ∉ E`. *CND.monotone:* `d > d1` (first divergence at position 5: `2 > 1`) and `d > v1` (agree on positions 1–4, diverge at position 5: `2 > 1`) — the cross-allocator comparison `d > v1` resolves by T1 with no same-allocator premise. Crucially, had we used the *unrestricted* `D_A`, we would have taken `d_prev = max{d1, v1} = v1` (since `d1 ≺ v1`) and emitted `inc(v1, 0) = [1, 0, 1, 0, 1, 2]` — which is exactly the *next version* of `d1`, the second emission of `A_v(d1)`. A subsequent fork of `d1` would then re-baptise `[1, 0, 1, 0, 1, 2]`, a direct collision violating B8. The length filter is precisely what averts this.

## What Distinguishes Creation From Forking

The user asked what separates a freshly authored document from one born by versioning. The distinction is sharp and lies entirely in **what is shared with prior documents at the level of I-address identity**.

A freshly created document shares *nothing* by default. Its arrangement is empty: `ran(M'(d)) = ∅`. There is no I-address in common with any other document — not because the bytes differ, but because there are no bytes. And the sharing cannot arise by accident later, either: any content subsequently inserted into `d` is drawn from `A_C(d)` and carries `origin(·) = d`. By origin-based identity (S4, ASN-0036), two content units produced by distinct allocation events are distinct addresses *regardless of their values*. So even if `d` comes to hold byte-for-byte the same text as some other document, the two hold it at *different* I-addresses. A fresh document has no automatic correspondence to anything.

Contrast a document born by forking (CREATENEWVERSION — formalised elsewhere, out of scope here). Such a document begins as a complete inclusion of its source: its arrangement is *populated* at creation, mapping V-positions onto the *same* I-addresses the source references. That shared Istream origin is exactly what makes refractive link-following and version intercomparison possible — and it is exactly what a fresh document lacks. The two creation paths are also structurally distinct in the allocator: a fresh document is a depth-2 descent off an *account* (`zeros` increases by one, `parent = A`), whereas a version is a sibling-class step off a *document* (`zeros` unchanged, `parent` inherited from the source). We do not formalise the forking path; we only fix the contrast at the one place it matters:

> "CREATENEWDOCUMENT ... creates an empty document"; "CREATENEWVERSION ... creates a new document with the contents of document `<doc id>`." (4/65–66)

Empty versus inherited. That is the whole distinction, and it is visible in our post-state as `ran(M'(d)) = ∅`.

## Ownership and Immediate Referability

Two guarantees attach to the new address the instant it exists.

**Ownership is structural.** The document is bound to the account that created it not by metadata but by its address. The creating principal `π` was authorised because it owns the account: `pfx(π) ≼ A` (CND.pre), and the allocation is performed under that prefix (O5, SubdivisionAuthority; ASN-0042). The allocation forks `d` beneath `A`: `parent(d) = A`, and every `A_doc(A)` emission has the form `[A, 0, j]` (Effect One), so `A ≼ d`. By transitivity of the prefix order, `pfx(π) ≼ A ≼ d`, hence `owns(π, d) ≡ pfx(π) ≼ d` (O1, PrefixDetermination; ASN-0042): the new address lies in the creating principal's ownership domain `odom(π)`. This much is fixed by the post-state `(C, L, E, M, R)` alone, and it is the ownership guarantee CREATENEWDOCUMENT delivers.

Creating a document is, in Nelson's terms, a baptismal act — "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers" (4/17) — and the owned-number tree *is* the record of ownership, not a side table maintained alongside it. The sharper, *effective-owner* statement one would like — `ω_{Σ'}(d) = ω_Σ(A)`, that `d`'s longest-prefix owner is exactly the account's owner — is not derivable over this state model, and we are careful not to assert it. The function `ω` is defined over ASN-0042's baptismal registry `B`; CREATENEWDOCUMENT is specified over ASN-0047's state `(C, L, E, M, R)`, which carries no `B` component, and ASN-0047's `K.δ` never touches `B`. To evaluate `ω_{Σ'}(d)` one needs two things the present foundations do not supply over this state: (i) a registry component against which `ω` is defined, and (ii) a coupling invariant identifying the entity-set document chain with the registry's sibling stream — e.g. `{e ∈ E : Document(e) ∧ parent(e) = A ∧ #e = #A + 2} = Σ.B ∩ S(A, 2)` for every reachable `Σ`, preserved by `K.δ`. No foundation result establishes this `E`↔`B` agreement: ASN-0040 is stated purely over `B`, ASN-0047 purely over `E`, and ASN-0042's registry couplings (O17b, O18) are stated for *principal* prefixes, not arbitrary document entities. We therefore defer the `ω`-valued conclusion to an ASN whose state carries the registry, where the document-tier `K.δ` step can be exhibited as a genuine `Bop(A, 2)` baptism (ASN-0040) — the depth-2 descent off `A` already satisfies `B6(A, 2)`, the validity bound `zeros(A) + (2 − 1) = 2 ≤ 3` discharged in Effect One — and the coupling (ii) discharged so that `d = next(Σ.B, A, 2)` and the registry extension `Σ'.B = Σ.B ∪ {d}` are *forced* rather than merely bounded by O17b. Over its own state, what creation guarantees is the structural ownership `pfx(π) ≼ d`, together with the design intent that no document exists except as a number forked beneath an owning account.

**Referability is immediate.** The moment `d` exists, it is a permanent, unique, unambiguously referable position. A link may target `d` before a single byte is stored, because referability attaches to the *address*, not the content — the ghost-element principle again:

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." (4/23)

Uniqueness is decentralised: because `d` is baptised under an account `π` already owns, no other owner could mint the same address (B8, ASN-0040), and no central registry is consulted. And the identity is permanent: for as long as the system endures, `d` continues to name this document and no other. The address assigned at creation *is* the document's identity, immutable even as the document's arrangement, content, and storage location later evolve.

## The Operation: Formal Contract

CREATENEWDOCUMENT is a **substrate composite** in the sense of ValidComposite★ (ASN-0047) — a finite sequence of elementary transitions from the substrate's K-vocabulary, governed at the boundary by the coupling constraints J0, J1★, J1'★. It is not a new primitive. Remarkably, the sequence has length one.

**Operation:** `CREATENEWDOCUMENT(A) → d`

**Substrate decomposition.** A single `K.δ` firing (EntityCreation, ASN-0047), case (ii):

  - if `D_A = ∅`: operand `t = A`, increment `k = 2`, yielding `d = inc(A, 2)`;
  - otherwise: operand `t = d_prev = max(D_A)`, increment `k = 0`, yielding `d = inc(d_prev, 0)`,

where `D_A = {e ∈ E : Document(e) ∧ parent(e) = A ∧ #e = #A + 2}` is the document-chain frontier (length-restricted to exclude versions, which carry length `≥ #A + 3`). In both branches `Document(d) ∧ parent(d) = A ∧ T4-valid(d) ∧ d ∉ E`. The `K.δ` Document sub-case registers the document with an empty arrangement.

**State preconditions** (against pre-state `Σ`):

  - `A ∈ E ∧ Account(A)` — the account exists and is account-level;
  - the invoking principal `π` satisfies `pfx(π) ≼ A` — it owns the account (O5, ASN-0042).

(The freshness `d ∉ E` is discharged by the allocator discipline, not imposed on the caller.)

**Effect** (post-state `Σ'`):

  - `E' = E ∪ {d}`, with `Document(d)`, `parent(d) = A`, `d ∉ E`;
  - `M'(d) = ∅`;
  - `(A d' : d' ∈ E_doc : M'(d') = M(d'))`;
  - `C' = C`; `L' = L`; `R' = R`.

**Returns** `d`.

**Coupling.** The composite trivially satisfies J0, J1★, J1'★ (ASN-0047): each couples content allocation, placement, and provenance, and this operation performs none — there is no `K.α`, no content-subspace `K.μ⁺`, and `R' = R`. So all coupling constraints hold vacuously.

**Atomicity.** Because the decomposition is a single elementary transition, atomicity is immediate from the sequential-transition axiom (ASN-0093): `K.δ` evaluates its precondition against `Σ` and commits its effect to `Σ'` in one indivisible step. There is no observable intermediate state, hence no window in which an invariant is violated.

## Invariants Maintained

We verify that the post-state `Σ'` satisfies the operative invariants. Most are discharged by frame; the two non-trivial ones concern the new document itself.

*Content permanence (P0, ASN-0047 / S0, ASN-0036).* `C' = C`, so `dom(C) ⊆ dom(C')` and every value is preserved pointwise. Trivially maintained — indeed the content store is held identically.

*Entity permanence (P1, ASN-0047).* `E' = E ∪ {d} ⊇ E`. No entity is removed. The document population increases by exactly one.

*Document well-formedness (M0, ASN-0093).* `T4-valid(d) ∧ zeros(d) = 2`, established in Effect One.

*Empty arrangement.* `M'(d) = ∅` is the defining post-state of the new document — the abstract content of Nelson's "empty document."

*Referential integrity (S3★, ASN-0047).* For `d`: `ran(M'(d)) = ∅ ⊆ dom(C')`, vacuously. For every `d' ≠ d`: `M'(d') = M(d')` and `C ⊆ C'`, so integrity is inherited from `Σ`.

*Arrangement functionality (S2, ASN-0036).* `M'(d) = ∅` is a (degenerate) function; other documents inherit functionality unchanged.

*Existential coherence (P6, ASN-0047).* No new content address is created, so every `a ∈ dom(C') = dom(C)` retains its existing origin document, which still exists in `E' ⊇ E`.

*Entity hierarchy (P8, ASN-0047).* `parent(d) = A ∈ E ⊆ E'`, so the new non-node entity has its parent present.

*Address permanence and distinctness (T8, GlobalUniqueness; ASN-0034).* Every previously valid address remains valid (`E ⊆ E'`, `dom(C) ⊆ dom(C')`), and `d` collides with no existing or future address by baptismal uniqueness. The document's identity is permanently distinct from every other document, including ones created later.

*The balance of `ExtendedReachableStateInvariants` (ASN-0047).* The binding correctness criterion is the full conjunction of that theorem plus the transition invariant P3; the conjuncts not named above are discharged on the vacuity premise `dom(M'(d)) = ∅` together with the frame `C' = C ∧ L' = L ∧ R' = R ∧ E' = E ∪ {d} ∧ (A d' ≠ d : M'(d') = M(d'))`.

- *Vacuous for the empty arrangement of `d`, frame-inherited for `d' ≠ d`* (each quantifies over `dom(M'(d))` or `V_S(d)`, empty for `d`): S3★-aux, S8a, S8-fin, S8-depth, S8★, D-CTG★, D-MIN★, D-SEQ★, CL-OWN, CL-UNIQ.
- *Frame-inherited — no content, link, or provenance change* (each ranges over `dom(C') = dom(C)`, `dom(L') = dom(L)`, or `R' = R`): S4, S7a, S7b, C1b, C1c, C-fin, P7, L0, L1, L1a, L1b, L1c, L3, L14, L-fin, and NodeLineage (no node minted).
- *Composite-boundary properties, frame-inherited* (over `Contains_C` and `R`, both unchanged): P4★, P4a, P7a.
- *Concerning `d` directly, established in Effect One*: S7d (`d` is a document with `zeros(d) = 2` arising from a T10a allocation event) and ActivatedEmission (`d` is an emission of the activated entity-level sub-allocator `A_doc(A)`).

*Arrangement-mutability-only (P3, transition invariant; ASN-0047).* The only component that may lose information is `M`. Here `dom(C) ⊆ dom(C')`, `dom(L) ⊆ dom(L')`, `E ⊆ E'`, `R ⊆ R'` with all values preserved, and `M` only *gains* the empty entry `M'(d) = ∅`; so P3 holds.

Every conjunct of `ExtendedReachableStateInvariants` and the transition invariant P3 is thereby discharged — verified directly, vacuous for the empty arrangement, or frame-inherited. So `Σ'` satisfies the full correctness criterion, and since the composite is a single atomic transition, no observable intermediate state exists and the invariants hold throughout. The operation is correct.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| CND.def | CREATENEWDOCUMENT(A) is a substrate composite Σ →* Σ' under ValidComposite★ (ASN-0047) realised as a single K.δ firing (case (ii): k=2 off A when D_A=∅, else k=0 off max(D_A)) registering d into E_doc with M(d)=∅; it returns d | introduced |
| CND.pre | Preconditions: A ∈ E ∧ Account(A); the invoking principal π owns the account (pfx(π) ≼ A, O5; ASN-0042). No content argument | introduced |
| CND.alloc | Allocates exactly one fresh document address d from A_doc(A)=S(A,2): d = inc(A,2) if D_A=∅ else inc(max(D_A),0), where D_A = {e ∈ E : Document(e) ∧ parent(e)=A ∧ #e=#A+2} is the length-restricted document-chain frontier (versions, length ≥ #A+3, excluded); with Document(d), zeros(d)=2, parent(d)=A, T4-valid(d), d ∉ E | introduced |
| CND.empty | M'(d) = ∅: dom(M'(d)) = ∅ and ran(M'(d)) = ∅ — the new document holds no V-positions, no V→I mappings, no content | introduced |
| CND.C-frame | C' = C: the content store is entirely unchanged — no byte added, no value altered. Creation adds a place, not content (ghost element) | introduced |
| CND.L-frame | L' = L: the link store is unchanged | introduced |
| CND.R-frame | R' = R: the provenance relation is unchanged | introduced |
| CND.E | E' = E ∪ {d} with d ∉ E: every existing entity persists (E ⊆ E') and the document population grows by exactly one (\|E'_doc\| = \|E_doc\| + 1) | introduced |
| CND.doc-frame | (A d' ∈ E_doc : M'(d') = M(d')): every existing document's arrangement is wholly untouched | introduced |
| CND.monotone | d strictly exceeds every document address ever baptised under A (document-chain emission or version), including never-populated ones; existing addresses remain valid; d is never a reuse. Same-allocator ordering by S0 (ASN-0040); cross-allocator/version ordering by direct T1 lexicographic dominance at position #A+2 (T9 does not apply across allocators); disjointness/uniqueness by B7, B8 (ASN-0040); permanence T8, GlobalUniqueness (ASN-0034) | introduced |
| CND.subAlloc | Creation activates A_C(d) and A_L(d) (content and link sub-allocators, anchors [d.0.s_C], [d.0.s_L]) without emission; both subspaces are available but empty at Σ' (SubAllocatorBundle, ASN-0047) | introduced |
| CND.no-sharing | The fresh document shares no I-address with any prior document: ran(M'(d)) = ∅; and future content drawn from A_C(d) has origin = d, so by S4 (ASN-0036) it shares no I-address with any other document regardless of value coincidence | introduced |
| CND.own | Ownership is structural and derivable over ASN-0047's state (C,L,E,M,R): parent(d)=A and A ≼ d (every A_doc(A) emission has form [A,0,j]), so with pfx(π) ≼ A (CND.pre) and prefix transitivity, owns(π,d) ≡ pfx(π) ≼ d (O1; ASN-0042) — d ∈ odom(π); allocation authorised by O5 (ASN-0042). The effective-owner statement ω_{Σ'}(d) = ω_Σ(A) is NOT asserted here: ω is defined over ASN-0042's registry B, absent from this state model, and no foundation result couples E to B on the document chain (the needed invariant {e ∈ E : Document(e) ∧ parent(e)=A ∧ #e=#A+2} = Σ.B ∩ S(A,2) is unestablished); the ω-valued claim is deferred to a registry-carrying ASN where the K.δ step is a genuine Bop(A,2) baptism (B6(A,2) holds) | introduced |
| CND.refer | d is immediately, permanently, and unambiguously referable: a link may target d at Σ' before any content exists; uniqueness is decentralised (B8, ASN-0040) and identity is immutable for the life of the system | introduced |
| CND.atomicity | The single-K.δ decomposition is atomic by the sequential-transition axiom (ASN-0093); no observable intermediate state exists, so all invariants hold throughout. Coupling constraints J0, J1★, J1'★ hold vacuously | introduced |
| CND.inv | Σ' satisfies the full ExtendedReachableStateInvariants (ASN-0047) and the transition invariant P3: P0, P1, M0, S2, S3★, P6, P8, S7d, ActivatedEmission, and address permanence/distinctness (T8, GlobalUniqueness; ASN-0034) verified directly; the empty-arrangement family (S3★-aux, S8a, S8-fin, S8-depth, S8★, D-CTG★, D-MIN★, D-SEQ★, CL-OWN, CL-UNIQ) vacuous for d via dom(M'(d))=∅; the content/link/provenance families (S4, S7a, S7b, C1b, C1c, C-fin, P7, P7a, P4★, P4a, L0, L1, L1a, L1b, L1c, L3, L14, L-fin, NodeLineage) frame-inherited; P3 holds since only M gains the empty entry M'(d)=∅ | introduced |

## Open Questions

- What must an implementation guarantee to recover the canonical post-state after a partial failure during the (single-transition) creation, given that the returned id must already name a usable document?
- What does the abstract specification require of concurrent CREATENEWDOCUMENT calls under the same account from independent agents — must they serialise, and on what basis is the order of the two new addresses chosen?
- What guarantee, if any, binds the returned document id to immediate write-readiness for the creating session, as distinct from the document's bare existence in the entity set?
- Under what conditions, if any, may a created-but-never-populated document be removed from the entity set, and what address-permanence guarantee would such removal have to respect?
- What must the system guarantee about the relationship between a document's creation-time address and its eventual content origins, so that attribution remains derivable from the address alone?
- What coupling between the entity set and the baptismal registry must hold in every reachable state for an entity-level document allocation to coincide with a registry baptism, so that the effective-owner reading of ownership becomes derivable rather than asserted?
