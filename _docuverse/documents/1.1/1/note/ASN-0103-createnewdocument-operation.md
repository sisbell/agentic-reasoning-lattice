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

We split on whether `A` already has documents. Let `D_A = {e ∈ E : Document(e) ∧ parent(e) = A}` be the documents currently under `A`. Then the allocated address is

  `d = inc(A, 2)` if `D_A = ∅`,
  `d = inc(d_prev, 0)` otherwise, where `d_prev = max(D_A)`.

In both cases `d` is the next emission of `A_doc(A)`. We must verify three structural facts and one separation fact.

*Document level.* For the first case, `inc(A, 2)` is a depth-2 descent: by the increment law (TA5, ASN-0034) it appends two components, and by the field-advancement law `zeros(inc(A, 2)) = zeros(A) + 1 = 2` (B5, ASN-0040), so `Document(d)` holds. For the subsequent case, `inc(d_prev, 0)` is a sibling step: it preserves length and zero-count (TA5(c), B5a; ASN-0040), so `zeros(d) = zeros(d_prev) = 2` and `parent(d) = parent(d_prev) = A` (K.δ-ID.parent-0, ASN-0047). Either way `Document(d) ∧ parent(d) = A`.

*Validity.* The baptism produces a T4-valid address. Depth-2 descent off an account satisfies the validity bound `zeros(A) + (2 − 1) = 2 ≤ 3` (B6, ValidDepth; ASN-0040), and the sibling step preserves T4 (TA5a, ASN-0034). So `T4-valid(d)`.

*Freshness.* The address is new: `d ∉ E`. For the first emission this is FirstEmission freshness; for a subsequent emission the enumeration of `A_doc(A)` is strictly increasing (ChainEnumerationInjectivity, ASN-0093), so `d = inc(d_prev, 0) > d_prev ≥ e` for every prior `e ∈ D_A`, placing `d` strictly past the entire existing chain. Cross-account collisions are excluded by partition independence (T10, ASN-0034): `d` extends the account prefix `A`, and any address under a different account `A' ≠ A` is prefix-incomparable to it, hence distinct.

*Strict advance over never-populated siblings.* The advance is past *every* address ever baptised under `A`, including documents created but never written into. The high-water mark is read from the live entity set — an empty document is still in `E`, so the next allocation steps over it. There is no mechanism by which a later document is baptised onto an already-occupied position (B8, Uniqueness; ASN-0040). This is the abstract content of Nelson's permanence guarantee:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid." (4/19)

### Effect Two: The Arrangement Is Empty

The document is born holding nothing. Its arrangement is the empty partial function:

  `M'(d) = ∅`, i.e. `dom(M'(d)) = ∅` and `ran(M'(d)) = ∅`.

There are no V-positions, hence no V→I mappings, hence no I-addresses referenced. This is the formal reading of "creates an empty document" (4/65). Because the Vstream is dense — a contiguous sequence of positions — a document with zero references occupies zero V-addresses; there is no inherent starting state, no default text, no placeholder the user can rely on. Content is added only by subsequent operations.

We note one consequence immediately, to be discharged as an invariant below: with `ran(M'(d)) = ∅`, referential integrity `ran(M'(d)) ⊆ dom(C')` (S3, ASN-0036) holds *vacuously* for `d`. An empty document cannot dangle.

### Effect Three: Nothing Else Changes

This is the largest effect and the heart of the user's guarantee. Creating `d` must leave the identities and content of every existing document wholly untouched. We enumerate the frame.

*The content store is untouched.* `C' = C`. No byte is added, no value altered, no address removed:

  `dom(C') = dom(C) ∧ (A a : a ∈ dom(C) : C'(a) = C(a))`.

This is the abstract statement of "adds a place, not content." The document is, at the instant of creation, a ghost element: a position in `E` with nothing stored beneath it in `C`.

*The link store is untouched.* `L' = L`. Creation makes no link.

*The provenance relation is untouched.* `R' = R`. Provenance records which document referenced which content (ASN-0047); with no content and no reference, there is nothing to record.

*Every existing entity persists.* `E ⊆ E'`, and the only new member is `d`:

  `E' = E ∪ {d}` with `d ∉ E`.

In particular every existing document, account, and node keeps its address. Entity permanence (P1, ASN-0047) is preserved, and the document population grows by *exactly one* (Q10): `|E'_doc| = |E_doc| + 1`.

*Every existing document's arrangement is untouched.* `(A d' : d' ∈ E_doc : M'(d') = M(d'))`. No other document's Vstream, content, or links shift. This is the cross-document frame: the operation reaches into no subtree but the one it baptises.

These frames exhaust the state components `(C, L, E, M, R)`. The only net change is `E' = E ∪ {d}` together with `M'(d) = ∅`. Everything else is held fixed. The operation is, in Nelson's phrase, strictly additive: it forks one new permanent address beneath the creator's account and disturbs nothing that exists.

### A Note on Sub-Allocator Activation

One consequence of Effect One is worth stating explicitly because it underwrites every later operation on `d`. The entity-allocation event that places `d` into `E_doc` *activates* two element-level sub-allocators scoped to `d`: the content sub-allocator `A_C(d)` with anchor `[d.0.s_C]` and the link sub-allocator `A_L(d)` with anchor `[d.0.s_L]` (SubAllocatorBundle, ASN-0047). Activation is not population: at the post-state both chains have emitted nothing, so the anchors are not yet in `dom(C') ∪ dom(L')`. They stand ready. The first INSERT into `d` will draw `[d.0.s_C.1]` from `A_C(d)`; the first MAKELINK will draw `[d.0.s_L.1]` from `A_L(d)`. Creation is what makes those subspaces *available* — lazily materialised, never pre-filled.

## What Distinguishes Creation From Forking

The user asked what separates a freshly authored document from one born by versioning. The distinction is sharp and lies entirely in **what is shared with prior documents at the level of I-address identity**.

A freshly created document shares *nothing* by default. Its arrangement is empty: `ran(M'(d)) = ∅`. There is no I-address in common with any other document — not because the bytes differ, but because there are no bytes. And the sharing cannot arise by accident later, either: any content subsequently inserted into `d` is drawn from `A_C(d)` and carries `origin(·) = d`. By origin-based identity (S4, ASN-0036), two content units produced by distinct allocation events are distinct addresses *regardless of their values*. So even if `d` comes to hold byte-for-byte the same text as some other document, the two hold it at *different* I-addresses. A fresh document has no automatic correspondence to anything.

Contrast a document born by forking (CREATENEWVERSION — formalised elsewhere, out of scope here). Such a document begins as a complete inclusion of its source: its arrangement is *populated* at creation, mapping V-positions onto the *same* I-addresses the source references. That shared Istream origin is exactly what makes refractive link-following and version intercomparison possible — and it is exactly what a fresh document lacks. The two creation paths are also structurally distinct in the allocator: a fresh document is a depth-2 descent off an *account* (`zeros` increases by one, `parent = A`), whereas a version is a sibling-class step off a *document* (`zeros` unchanged, `parent` inherited from the source). We do not formalise the forking path; we only fix the contrast at the one place it matters:

> "CREATENEWDOCUMENT ... creates an empty document"; "CREATENEWVERSION ... creates a new document with the contents of document `<doc id>`." (4/65–66)

Empty versus inherited. That is the whole distinction, and it is visible in our post-state as `ran(M'(d)) = ∅`.

## Ownership and Immediate Referability

Two guarantees attach to the new address the instant it exists.

**Ownership is structural.** The document is bound to the account that created it not by metadata but by its address: `d` is forked beneath `A`, so `parent(d) = A` and `A ≼ d`. The creating principal `π` was authorised because it owns the account (`pfx(π) ≼ A`); the allocation places `d` strictly under that prefix (O5, SubdivisionAuthority; ASN-0042). Since `d` is fresh and no finer principal sits between `A` and `d`, the new document's effective owner is the account's owner: `ω_{Σ'}(d) = ω_Σ(A)`. The binding is the act of creation itself — there is no document except as a number forked beneath an owning account.

**Referability is immediate.** The moment `d` exists, it is a permanent, unique, unambiguously referable position. A link may target `d` before a single byte is stored, because referability attaches to the *address*, not the content — the ghost-element principle again:

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." (4/23)

Uniqueness is decentralised: because `d` is baptised under an account `π` already owns, no other owner could mint the same address (B8, ASN-0040), and no central registry is consulted. And the identity is permanent: for as long as the system endures, `d` continues to name this document and no other. The address assigned at creation *is* the document's identity, immutable even as the document's arrangement, content, and storage location later evolve.

## The Operation: Formal Contract

CREATENEWDOCUMENT is a **substrate composite** in the sense of ValidComposite★ (ASN-0047) — a finite sequence of elementary transitions from the substrate's K-vocabulary, governed at the boundary by the coupling constraints J0, J1★, J1'★. It is not a new primitive. Remarkably, the sequence has length one.

**Operation:** `CREATENEWDOCUMENT(A) → d`

**Substrate decomposition.** A single `K.δ` firing (EntityCreation, ASN-0047), case (ii):

  - if `D_A = ∅`: operand `t = A`, increment `k = 2`, yielding `d = inc(A, 2)`;
  - otherwise: operand `t = d_prev = max(D_A)`, increment `k = 0`, yielding `d = inc(d_prev, 0)`,

where `D_A = {e ∈ E : Document(e) ∧ parent(e) = A}`. In both branches `Document(d) ∧ parent(d) = A ∧ T4-valid(d) ∧ d ∉ E`. The `K.δ` Document sub-case registers the document with an empty arrangement.

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

All invariants hold at `Σ'`, and since the composite is a single atomic transition, they hold at every observable state. The operation is correct.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| CND.def | CREATENEWDOCUMENT(A) is a substrate composite Σ →* Σ' under ValidComposite★ (ASN-0047) realised as a single K.δ firing (case (ii): k=2 off A when D_A=∅, else k=0 off max(D_A)) registering d into E_doc with M(d)=∅; it returns d | introduced |
| CND.pre | Preconditions: A ∈ E ∧ Account(A); the invoking principal π owns the account (pfx(π) ≼ A, ASN-0042). No content argument | introduced |
| CND.alloc | Allocates exactly one fresh document address d from A_doc(A): d = inc(A,2) if D_A=∅ else inc(max(D_A),0); with Document(d), zeros(d)=2, parent(d)=A, T4-valid(d), d ∉ E | introduced |
| CND.empty | M'(d) = ∅: dom(M'(d)) = ∅ and ran(M'(d)) = ∅ — the new document holds no V-positions, no V→I mappings, no content | introduced |
| CND.C-frame | C' = C: the content store is entirely unchanged — no byte added, no value altered. Creation adds a place, not content (ghost element) | introduced |
| CND.L-frame | L' = L: the link store is unchanged | introduced |
| CND.R-frame | R' = R: the provenance relation is unchanged | introduced |
| CND.E | E' = E ∪ {d} with d ∉ E: every existing entity persists (E ⊆ E') and the document population grows by exactly one (\|E'_doc\| = \|E_doc\| + 1) | introduced |
| CND.doc-frame | (A d' ∈ E_doc : M'(d') = M(d')): every existing document's arrangement is wholly untouched | introduced |
| CND.monotone | d strictly exceeds every document address ever baptised under A, including never-populated ones; existing addresses remain valid; d is never a reuse (T8, T9, GlobalUniqueness; ASN-0034) | introduced |
| CND.subAlloc | Creation activates A_C(d) and A_L(d) (content and link sub-allocators, anchors [d.0.s_C], [d.0.s_L]) without emission; both subspaces are available but empty at Σ' (SubAllocatorBundle, ASN-0047) | introduced |
| CND.no-sharing | The fresh document shares no I-address with any prior document: ran(M'(d)) = ∅; and future content drawn from A_C(d) has origin = d, so by S4 (ASN-0036) it shares no I-address with any other document regardless of value coincidence | introduced |
| CND.own | Ownership is structural: parent(d) = A and A ≼ d, so ω_{Σ'}(d) = ω_Σ(A); the binding is the act of creation, authorised by O5 (ASN-0042) | introduced |
| CND.refer | d is immediately, permanently, and unambiguously referable: a link may target d at Σ' before any content exists; uniqueness is decentralised (B8, ASN-0040) and identity is immutable for the life of the system | introduced |
| CND.atomicity | The single-K.δ decomposition is atomic by the sequential-transition axiom (ASN-0093); no observable intermediate state exists, so all invariants hold throughout. Coupling constraints J0, J1★, J1'★ hold vacuously | introduced |
| CND.inv | Σ' maintains P0, P1, M0, S2, S3★, P6, P8 (ASN-0047/0036/0093) and address permanence/distinctness (T8, GlobalUniqueness; ASN-0034); referential integrity for d holds vacuously via the empty arrangement | introduced |

## Open Questions

- What must an implementation guarantee to recover the canonical post-state after a partial failure during the (single-transition) creation, given that the returned id must already name a usable document?
- What does the abstract specification require of concurrent CREATENEWDOCUMENT calls under the same account from independent agents — must they serialise, and on what basis is the order of the two new addresses chosen?
- What guarantee, if any, binds the returned document id to immediate write-readiness for the creating session, as distinct from the document's bare existence in the entity set?
- Under what conditions, if any, may a created-but-never-populated document be removed from the entity set, and what address-permanence guarantee would such removal have to respect?
- What must the system guarantee about the relationship between a document's creation-time address and its eventual content origins, so that attribution remains derivable from the address alone?
