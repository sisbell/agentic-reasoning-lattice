# ASN-0011: Document Lifecycle

*2026-02-24*

We wish to understand what a document *is* in this system, and what
invariants govern its passage from creation through modification to
publication. The question is not how documents are stored — that is
mechanism — but what guarantees the system must uphold about document
identity, ownership, and the relationships between documents in an
ever-growing universe of content.

The investigation is motivated by an observation that will turn out to be
fundamental: in this system, a document's identity is not metadata attached
to it but a structural consequence of its address. Ownership is not a table
to be consulted but a prefix to be computed. And the "lifecycle" of a
document, unlike the lifecycle of a file, has no death phase. Documents are
born, grow, and persist — but never perish. We seek the formal properties
that make this possible.


## State Components

We need a model of documents before we can reason about their lifecycle. Let
Σ denote the system state.

**DΣ1 (documents).** Σ.docs : Set(Tumbler) is the set of all allocated
document addresses. Each element is a tumbler — a finite sequence of
non-negative integers — that uniquely identifies one document in the system.

**DΣ2 (accounts).** Σ.accounts : Set(Tumbler) is the set of all allocated
account addresses. Every account is also a tumbler. We require:

    (A d : d ∈ Σ.docs : (E a : a ∈ Σ.accounts : prefix(a, d)))

That is, every document's address has some account address as a proper
prefix. The function prefix(a, d) holds when a is a proper prefix of d in
the tumbler hierarchy — concretely, when the mantissa of a matches the
initial segment of the mantissa of d up to a's length, with the appropriate
zero-separator structure.

We define the *owner* of a document as the account whose address is a
prefix of the document's address:

    owner(d) = (THE a : a ∈ Σ.accounts : prefix(a, d))

The uniqueness of this account follows from the tumbler hierarchy: account
addresses are separated by zero-field boundaries that prevent one account
from being a prefix of another. We write owner(d) throughout, understanding
it as a function derived from the address, not stored separately.

**DΣ3 (content).** Σ.ispace : IAddr ⇀ Byte is the permanent content store,
a partial function from I-space addresses to content bytes. We take as
given:

- *Permanence*: dom(Σ.ispace) ⊆ dom(Σ'.ispace) for all subsequent Σ'.
- *Immutability*: Σ'.ispace(a) = Σ.ispace(a) for all a ∈ dom(Σ.ispace).

**DΣ4 (arrangement).** For each document d ∈ Σ.docs, Σ.poom(d) : VPos ⇀
IAddr is the arrangement mapping — a partial function from V-space
positions to I-space addresses. The domain dom(Σ.poom(d)) is the set of
positions at which d currently has content.

**DΣ5 (allocation counter).** Σ.next : Tumbler → Tumbler records, for each
account, the next available document address under that account. This is a
monotonically advancing counter — it never retreats:

    Σ.next(a) ≤ Σ'.next(a)    for all subsequent Σ' and accounts a

**DΣ6 (session state).** Σ.sessions : Set(SessionEntry) where each entry
records (connection, document, access-level). This component tracks which
documents are currently open in which sessions. It is orthogonal to document
content.


## Document Identity

We begin with the most fundamental property. A document's identity is its
address, and that address is permanent.

**DL0 (identity permanence).** Once a document address has been allocated, it
remains in the document set forever:

    d ∈ Σ.docs  ⟹  d ∈ Σ'.docs    for all subsequent Σ'

This is the document-level manifestation of the system's permanence
guarantee. Nelson states it as a structural consequence of the addressing
design: "any address of any document in an ever-growing network may be
specified by a permanent tumbler address" [LM 4/19]. If an address could
cease to denote a document, references made by other users — links, bookmarks,
transclusions — would break. DL0 prevents this.

**DL1 (address uniqueness).** No two distinct documents share an address:

    (A d₁, d₂ : d₁ ∈ Σ.docs ∧ d₂ ∈ Σ.docs ∧ d₁ ≠ d₂ : d₁.addr ≠ d₂.addr)

This is trivially satisfied when documents *are* their addresses (as
elements of Set(Tumbler)), but we state it explicitly because the
consequence is important: a tumbler address unambiguously identifies one
document across all time.

**DL2 (address non-reuse).** Once allocated, a document address is never
assigned to a different document:

    d ∈ Σ.docs  ⟹  (A Σ' : Σ' subsequent to Σ :
      identity(d, Σ) = identity(d, Σ'))

where identity(d, Σ) denotes whatever state was associated with d at its
creation. This follows from DL0 (the address remains in docs) together
with the fact that no operation removes a document from docs and re-inserts
it with different initial state. The forking mechanism that generates
addresses only advances — there is no "reclaim" or "recycle" operation in
the protocol.

Nelson explains the architectural rationale: "new items may be continually
inserted in tumbler-space while the other addresses remain valid" [LM
4/19]. The forking mechanism creates addresses by appending sub-digits (2.1,
2.2, 2.3, ...). It never revisits an earlier position.


## Document Creation

We now define what it means to bring a document into existence.

**CREATENEWDOCUMENT.** The operation CREATENEWDOCUMENT(a) creates a new
document under account a. Let Σ be the state before and Σ' after.

*Precondition:*

    PRE-DOC:  a ∈ Σ.accounts

The account must exist. This is the sole precondition — no content is
required, no session state, no prior documents under the account.

*Postcondition:*

    DL3 (fresh allocation):  d ∈ Σ'.docs ∧ d ∉ Σ.docs

The returned address d is fresh — it was not in the document set before.
This is not merely a requirement but a structural consequence of the
allocation mechanism: the counter Σ.next(a) advances monotonically, and the
new address is produced by incrementing beyond all existing addresses under
account a.

    DL4 (empty arrangement):  dom(Σ'.poom(d)) = ∅

A freshly created document has no content. Its arrangement mapping is the
empty partial function. Nelson is explicit: "This creates an empty document.
It returns the id of the new document" [LM 4/65].

We pause to note the significance. An empty document is a valid, first-class
entity. It has an address (permanent), an owner (derived from the address),
and an arrangement (empty). It can be linked to. It can be opened. It is a
position in the docuverse — baptized, named, owned — waiting for content.
Nelson's metaphor is precise: the owner "designates new addresses by
forking" [LM 4/17], and designation precedes population.

    DL5 (ownership from address):  owner(d) = a

The new document's owner is the account under which it was allocated. This
is not stored as a separate field — it is derived from the address itself,
because a is a prefix of d. The document at address `1.0.2.0.5` is owned by
account `1.0.2` because `1.0.2` is its account-level prefix. No ownership
table is consulted; the tumbler encodes the relationship structurally.

Gregory's implementation confirms this: ownership is determined by
`tumbleraccounteq`, which performs prefix matching on the tumbler mantissa —
comparing digits until the account's double-zero terminator, then declaring
the document to be "under" that account. The abstract property is: ownership
is a prefix relation, not an association table.

    DL6 (counter advance):  Σ'.next(a) > Σ.next(a)

The allocation counter for account a strictly advances. This, together with
the fact that all future allocations use Σ'.next(a) or later values,
guarantees DL3 — freshness follows from the monotonicity of allocation.

*Frame conditions:*

    DL-F1 (existing documents unchanged):
      (A d' : d' ∈ Σ.docs : d' ∈ Σ'.docs ∧ Σ'.poom(d') = Σ.poom(d'))

    DL-F2 (content unchanged):  Σ'.ispace = Σ.ispace

    DL-F3 (other accounts unchanged):
      (A a' : a' ∈ Σ.accounts ∧ a' ≠ a : Σ'.next(a') = Σ.next(a'))

The frame conditions are as important as the postconditions. DL-F1 says that
no existing document's arrangement is disturbed. DL-F2 says that no I-space
content is created or modified. DL-F3 says that other accounts' allocation
counters are unaffected.

Nelson derives DL-F1 from three converging principles: tumbler permanence
(addresses don't break), ownership (creating B cannot modify A, because B's
creator might not own A), and I-space immutability (no content changes).
"Thus users may create new published documents out of old ones indefinitely,
making whatever changes seem appropriate — without damaging the originals"
[LM 2/45]. Though stated in the context of versioning, the non-damage
principle holds a fortiori for the simpler case of creating a fresh
empty document.

Gregory's implementation corroborates: CREATENEWDOCUMENT's entire execution
path (`do1.c:234–241`) consists of a `makehint` call and a
`createorglingranf` call. The latter allocates an address in the granfilade
and initialises an empty POOM. It touches neither the spanfilade nor any
other document's orgl. The operation creates one granfilade entry and one
empty POOM tree — nothing else.


## The Empty Document

We noted that DL4 establishes dom(Σ'.poom(d)) = ∅. This deserves further
examination, because the empty document state has structural consequences.

**DL7 (empty document retrievability).** For any document d with
dom(Σ.poom(d)) = ∅, retrieval of any V-span returns the empty sequence:

    retrieve(d, S) = ε    for all spans S

This is immediate: retrieval resolves V-positions through the arrangement
mapping, and the empty mapping has no positions to resolve. An empty
document is readable — it simply has nothing to say.

**DL8 (empty document linkability).** An empty document d ∈ Σ.docs may be
the target of a link. Links reference I-space addresses in their endsets,
and a link may also reference the document's address as a structural
designator (e.g., a metalink identifying document-level properties). Nelson
confirms: if one can link to a *node* or an *account* with no stored
content — "it is possible to link to a node, or an account, even though
there is nothing stored in the docuverse corresponding to them" [LM 4/23] —
then one can certainly link to a created document that happens to be empty.

The empty state is not a degenerate case to be avoided. The typical workflow
is CREATENEWDOCUMENT followed by INSERT to add content. Between creation and
first insertion, the document exists as a valid entity: owned, addressed,
and available for use. The empty document is the system's analogue of
allocating an identifier before initialising the object it names.


## Ownership

We have already derived that ownership is a prefix relation (DL5). We now
develop the consequences.

**DL9 (ownership permanence).** Once a document is created under an account,
the ownership relation holds forever:

    d ∈ Σ.docs  ⟹  owner(d) = owner_Σ(d)    for all subsequent Σ'

*Proof.* owner(d) is derived from d's tumbler address by prefix extraction.
The address is immutable (DL0 — the document remains; DL2 — the address is
never reassigned). The account set only grows (accounts are permanent). So
the prefix relation cannot change.  ∎

Nelson states the user-facing consequence: "once assigned a User account,
the user will have full control over its subdivision forevermore" [LM 4/29].
The "forevermore" is a structural guarantee, not a policy choice — to
change ownership, one would have to rewrite the tumbler, which contradicts
permanence.

**DL10 (exclusive modification).** Only the owner may modify a document's
arrangement:

    For any editing operation op applied to document d:
      pre(op, d) ⟹ caller = owner(d)

where editing operations are INSERT, DELETE, REARRANGE, COPY-into-d, and
APPEND. Nelson is unequivocal: "Only the owner has a right to withdraw a
document or change it" [LM 2/29].

This has a profound consequence for concurrency. If only one account can
modify a document, then "multiple users modifying the same document" is not
a scenario the specification must address. Nelson resolves the concurrent
modification problem not through locking but through ownership exclusivity:
each person controls their own documents. Collaboration happens through
transclusion, versioning, and linking — through creating new documents that
reference shared I-space content — not through shared mutable state.

**DL11 (owner controls out-links).** The document's outgoing links (links
homed in the document) are under the owner's control:

    For CREATELINK creating a link homed in document d:
      pre(CREATELINK, d) ⟹ caller = owner(d)

Nelson distinguishes out-links (under owner control) from in-links (not
under owner control): "These out-links are under control of its owner,
whereas its in-links are not" [LM 2/31]. A link's home document determines
who owns the link, but any user may create a link that *points to* any
published document.

**DL12 (ownership does not imply control after publication).** Publication
relinquishes certain ownership prerogatives:

    published(d) ⟹
      ¬ may_prevent_linking(owner(d), d)
    ∧ ¬ may_prevent_transclusion(owner(d), d)
    ∧ ¬ may_easily_withdraw(owner(d), d)

Nelson is explicit about this tradeoff: "each author of a published work
is relinquishing the right to control links into that work. This
relinquishment must also be part of the publishing contract" [LM 2/43].
And for transclusion: "permission has already been granted: for part of
the publication contract is the provision, 'I agree that anyone may link
and window to my document'" [LM 2/45].

Ownership means exclusive modification rights. It does not mean exclusive
control over how published content is used. The system enforces
compensation (automatic royalty), not permission. This separation of
compensation from control is a deliberate design choice — Nelson explicitly
states that the two traditional goals of copyright are decoupled [LM 2/45].


## Version Creation and Document Relationship

CREATENEWVERSION produces a new document that shares I-space content with
its source. The resulting entity is simultaneously distinct (its own
address, its own owner, its own arrangement) and connected (the same
permanent content bytes, the same I-addresses). We develop the properties
that govern this relationship.

**DL13 (version is a new document).** CREATENEWVERSION(source, user)
produces a fresh document v:

    v ∈ Σ'.docs ∧ v ∉ Σ.docs

This follows the same freshness guarantee as DL3 — version creation IS
document creation, with the additional property that the new document's
arrangement is initialised from the source rather than left empty.

**DL14 (version address placement).** The new version's address encodes
its derivation. When the creating user owns the source document:

    v.addr = source.addr ∥ s    for some suffix s with #s > 0

That is, v's address extends the source's address — a sub-address beneath
the original. This places the version in the source document's address
subtree. Nelson describes this as "new subfields in the tumbler indicating
daughter documents and versions" [LM 4/29].

When the creating user does *not* own the source, the version is allocated
under the creating user's own account instead:

    prefix(user.account, v.addr)
    ∧ ¬ prefix(source.addr, v.addr)

This asymmetry has a structural consequence: owner(v) = user.account in both
cases. When the user owns the source, this is consistent (the version lives
under the same account). When the user does not own the source, the version
lands in the user's own address space — reflecting that they now own this
derivative work.

Gregory's implementation confirms: `docreatenewversion` (`do1.c:268–275`)
tests `tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)`.
Owned documents use `makehint(DOCUMENT, DOCUMENT, ...)` with depth=1
(sub-address of source); unowned documents use `makehint(ACCOUNT,
DOCUMENT, ...)` with depth=2 (new document under the user's account,
identical to CREATENEWDOCUMENT).

**DL15 (content sharing).** The new version's arrangement references the
same I-space addresses as the source's text content:

    img(Σ'.poom(v)) = img(Σ.poom(source)|text)

where img denotes the image (the set of I-addresses referenced). Content is
not copied — it is shared by reference through I-space addresses. Both
documents' arrangement mappings point to the same permanent bytes.

Gregory's implementation confirms: CREATENEWVERSION allocates one document
orgl (`do1.c:281`), then `insertpm` copies existing I-addresses into the
new POOM (`do1.c:297`). No fresh content is allocated in I-space. The
content bytes exist once; the arrangements reference them multiply.

**DL16 (source unchanged).** CREATENEWVERSION does not modify the source:

    Σ'.poom(source) = Σ.poom(source)

The source document's arrangement, links, and content are completely
unaffected. This is Nelson's non-destruction guarantee applied to
versioning: "without damaging the originals" [LM 2/45]. Combined with
DL15 (content sharing), this means the operation is purely additive — it
creates new state (the version's document entry and arrangement) without
altering existing state.

**DL17 (version equality).** No version is distinguished as primary:

    (A op : op ∈ Operations :
      the preconditions and postconditions of op, when applied to any
      document d, depend only on d's state, not on whether d was created
      by CREATENEWDOCUMENT or CREATENEWVERSION)

Nelson rejects any notion of a "main" version: "There is thus no 'basic'
version of a document set apart from other versions — 'alternative'
versions — any more than one arrangement of the same materials is a priori
better than other arrangements" [LM 2/19]. He calls this *prismatic
storage*: all versions are equally valid views of a shared body of content.


## The Session Layer

We now turn to a part of the specification that Nelson deliberately left
open and Gregory's implementation filled in. The question is: what
coordination is needed when multiple connections interact with documents?

Nelson's 17 FEBE commands are stateless — "What the Xanadu storage and
hypertext system does — and thus is — is defined by the commands to which
it responds" [LM 4/61]. There is no OPEN command, no CLOSE command, no
session lifecycle in the design specification. Nelson's protocol names a
document by tumbler address, issues a command, and receives a response.
There is no concept of a "currently open document."

Yet any implementation must address practical coordination: what happens
when two connections attempt to modify the same document? Gregory's BERT
(Back-End Request Token) mechanism provides the answer, and we abstract its
properties here — not because they are Nelson's specification, but because
they represent the minimal coordination any implementation must provide.

**DL18 (session entry).** A session entry records a triple
(connection, document, access-level) where access-level ∈ {READ, WRITE}:

    entry = (c, d, level) ∈ Σ.sessions

Session entries gate access to operations. A connection must hold a session
entry for a document before operating on it.

**DL19 (write exclusivity).** At most one connection holds write access to
any document at any time:

    (A d : d ∈ Σ.docs :
      #{ c : (c, d, WRITE) ∈ Σ.sessions } ≤ 1)

Multiple readers may coexist, but the system guarantees that a document has
at most one writer. This is the minimal coordination property needed to
prevent interleaved modifications to a single document's arrangement.

**DL20 (write denial triggers version creation).** When a write access
request is denied — because another connection holds a conflicting session,
or because the requesting user does not own the document — the system may
redirect the request by creating a new version:

    If request(c, d, WRITE) is denied:
      CREATENEWVERSION(d, user(c)) may be invoked,
      producing v, and request(c, v, WRITE) succeeds.

This is the session layer's most characteristic property. Write denial is
not an error — it is a redirection. The user always succeeds in writing,
possibly to a new document. Nelson does not specify this mechanism, but it
is consistent with his design intent that "users may create new published
documents out of old ones indefinitely, making whatever changes seem
appropriate — without damaging the originals" [LM 2/45]. Gregory
implements this through BERT's "COPYIF" mode, which automatically branches
on write denial.

**DL21 (session orthogonality).** Session state is orthogonal to document
content. Opening or closing a document does not alter its arrangement,
I-space content, or links:

    If Σ' differs from Σ only by a session open or close:
      Σ'.poom(d) = Σ.poom(d)    for all d
      Σ'.ispace = Σ.ispace
      Σ'.docs = Σ.docs

A session entry is an access control token, not a document state component.
Gregory's implementation confirms this precisely: CLOSEDOCUMENT
(`bert.c:325–336`) removes the BERT entry from the hash table and nothing
else. It makes no calls to `fetchorglgr`, `orglfree`, or any function that
touches the document's enfilade. The orgl remains in the node cache,
protected by its `orglincore` flag, until memory pressure evicts it —
completely independent of whether any session holds it open.

**DL22 (no in-place access upgrade).** A session cannot upgrade from READ
to WRITE access on the same document:

    (c, d, READ) ∈ Σ.sessions  ⟹
      ¬ may_add(c, d, WRITE) to Σ'.sessions without first removing (c, d, READ)

The path from reader to writer requires closing the read session and opening
a new write session — or, under the COPYIF mode, creating a new version
and writing to that instead. There is no mutation of the access-level field
in an existing session entry.

Gregory's implementation makes this vivid: the `bertentry` struct stores
`type` (READBERT or WRITEBERT) which is set once at allocation
(`bert.c:145`) and never modified. The `checkforopen` function
(`bert.c:52–87`) returns -1 (denied) when a WRITEBERT request encounters
the same connection's existing READBERT entry — the function returns before
it even examines other connections' entries. The denial is triggered by
the requester's *own* prior read access.


## Publication Boundary

We close with the property that governs a document's transition from
private to public.

**DL23 (publication is voluntary).** A document's publication status
changes only by explicit owner action:

    published(d) in Σ' ∧ ¬published(d) in Σ  ⟹
      the transition was initiated by owner(d)

No operation by another user can force publication, and no system process
publishes documents automatically. Publication is "a solemn event, to be
undertaken cautiously" [LM 2/42].

**DL24 (publication permanence).** Once published, a document cannot be
easily withdrawn:

    published(d) in Σ  ⟹  published(d) in Σ'
      for all subsequent Σ', subject to extraordinary due-process exceptions

This is a near-invariant — Nelson acknowledges that withdrawal is "not
absolutely impossible" but requires "lengthy due process" [LM 2/43]. The
design intent is that publication creates a permanence obligation: "other
readers and users will come to depend on its accessibility" [LM 2/43].

The economic tension is unresolved: Nelson's model requires ongoing storage
rental, but does not specify what happens when payment lapses. The vendor
contract requires "orderly transition of all customer-stored materials to
other Xanadu locations" [LM 5/16] upon cancellation, but the indefinite
permanence of content in the absence of a paying party remains an open
question.

**DL25 (publication grants access, not control).** Publication makes
content universally readable and referenceable, but does not transfer any
modification rights:

    published(d)  ⟹
      (A u : u ∈ Users : may_read(u, d) ∧ may_link_to(u, d) ∧ may_transclude(u, d))
    ∧ (A u : u ∈ Users ∧ u ≠ owner(d) : ¬ may_modify(u, d))

The non-owner's recourse is CREATENEWVERSION — creating a derivative
document under their own control: "Another user, however, is free to
create his or her own alternative version of the document he or she does
not own. This, then, becomes a windowing document using the shared materials
by including them" [LM 2/37].


## Document Isolation

We conclude the main development with a theorem that unifies several of the
frame conditions stated above.

**Theorem DL-ISO (document creation isolation).** Neither CREATENEWDOCUMENT
nor CREATENEWVERSION modifies any existing document's observable state.
Formally, for any d' ∈ Σ.docs:

    Σ'.poom(d') = Σ.poom(d')                           — arrangement preserved
    ∧ Σ'.ispace|dom(Σ.ispace) = Σ.ispace               — content preserved
    ∧ links_homed_in(d', Σ') = links_homed_in(d', Σ)   — links preserved

*Proof.* CREATENEWDOCUMENT: by DL-F1 and DL-F2 directly.
CREATENEWVERSION: by DL16 (source unchanged) and the frame condition that
all documents other than the source and the new version are unaffected. The
new version is fresh (DL13), so it is not in Σ.docs and the quantification
over Σ.docs excludes it. ∎

The isolation guarantee follows from four converging principles: tumbler
permanence (addresses never invalidated), ownership exclusivity (creating B
cannot touch A if B's creator does not own A), I-space immutability (content
never changes), and the append-only address space (new documents are added,
never substituted). Nelson does not state isolation as a single axiom, but
it is a necessary consequence of his architectural choices.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| DΣ1 | Σ.docs : Set(Tumbler) — the set of allocated document addresses | introduced |
| DΣ2 | Σ.accounts : Set(Tumbler) — account addresses; every document prefixed by some account | introduced |
| DΣ3 | Σ.ispace : IAddr ⇀ Byte — permanent content store (permanent, immutable) | introduced |
| DΣ4 | Σ.poom(d) : VPos ⇀ IAddr — arrangement mapping per document | introduced |
| DΣ5 | Σ.next : Tumbler → Tumbler — per-account allocation counter, monotonically advancing | introduced |
| DΣ6 | Σ.sessions : Set(connection, document, access-level) — session state | introduced |
| owner(d) | owner(d) = (THE a : a ∈ Σ.accounts : prefix(a, d)) — ownership derived from address prefix | introduced |
| DL0 | d ∈ Σ.docs ⟹ d ∈ Σ'.docs — document identity is permanent | introduced |
| DL1 | distinct documents have distinct addresses | introduced |
| DL2 | allocated addresses are never reassigned to different documents | introduced |
| PRE-DOC | CREATENEWDOCUMENT requires only a ∈ Σ.accounts | introduced |
| DL3 | CREATENEWDOCUMENT produces a fresh address: d ∈ Σ'.docs ∧ d ∉ Σ.docs | introduced |
| DL4 | freshly created document has empty arrangement: dom(Σ'.poom(d)) = ∅ | introduced |
| DL5 | owner(d) = a — ownership derived from address at creation | introduced |
| DL6 | allocation counter strictly advances on creation | introduced |
| DL-F1 | existing documents' arrangements unchanged by CREATENEWDOCUMENT | introduced |
| DL-F2 | I-space unchanged by CREATENEWDOCUMENT | introduced |
| DL-F3 | other accounts' counters unchanged by CREATENEWDOCUMENT | introduced |
| DL7 | retrieval from an empty document returns the empty sequence | introduced |
| DL8 | an empty document may be the target of a link | introduced |
| DL9 | ownership is permanent — owner(d) never changes | introduced |
| DL10 | only the owner may modify a document's arrangement | introduced |
| DL11 | owner controls out-links (links homed in the document) | introduced |
| DL12 | publication relinquishes owner control over linking, transclusion, and withdrawal | introduced |
| DL13 | CREATENEWVERSION produces a fresh document | introduced |
| DL14 | version address encodes derivation (sub-address of source if same owner; user's account otherwise) | introduced |
| DL15 | version shares I-space addresses with source's text content (no new allocation) | introduced |
| DL16 | CREATENEWVERSION does not modify the source document | introduced |
| DL17 | no operation distinguishes "primary" vs "derivative" versions | introduced |
| DL18 | session entry is (connection, document, access-level) | introduced |
| DL19 | at most one write session per document at any time | introduced |
| DL20 | write denial may trigger version creation (redirection, not error) | introduced |
| DL21 | session open/close does not alter document content, ispace, or doc set | introduced |
| DL22 | no in-place READ→WRITE access upgrade on same session entry | introduced |
| DL23 | publication is voluntary — only owner initiates | introduced |
| DL24 | publication is near-permanent — withdrawal requires extraordinary process | introduced |
| DL25 | publication grants universal read/link/transclude access but not modification | introduced |
| DL-ISO | neither creation operation modifies any existing document's observable state (theorem) | introduced |


## Open Questions

Must the system guarantee that a document's arrangement is recoverable after a crash that interrupts CREATENEWDOCUMENT between address allocation and POOM initialisation?

What invariant must the allocation counter satisfy when multiple accounts reside on the same node — must per-account counters be independent, or may a global counter serve?

Must the session layer guarantee that a document owner can always obtain write access to their own document, even when other readers hold it open?

What must the system guarantee about documents whose storage rental has lapsed — does DL0 (identity permanence) hold unconditionally, or is it conditioned on economic obligations being met?

Must the publication transition be atomic — can a document be observed in a partially-published state by concurrent readers?

What consistency must the system maintain between a document's session state and its arrangement if a connection terminates abnormally without executing CLOSE?

When a user versions a document they do not own, must the system record the derivation relationship, or is the relationship visible only through shared I-space addresses?

Must the system prevent a document from being opened for write by two connections belonging to the same owner account, or does DL19 quantify over connections regardless of the account behind them?
