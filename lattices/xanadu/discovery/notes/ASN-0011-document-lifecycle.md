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

We require two further properties. First, accounts are permanent:

**DL-A0 (account permanence).**

    a ∈ Σ.accounts  ⟹  a ∈ Σ'.accounts    for all subsequent Σ'

This is necessary for owner(d) to remain well-defined: if the witnessing
account could disappear, the prefix relation would lose its witness and the
ownership function would become partial. Nelson treats accounts as permanent
structural positions in the tumbler hierarchy — they are allocated by the
node operator and persist indefinitely [LM 4/29].

Second, no account address is a prefix of another:

**DL-A1 (account prefix-freeness).**

    (A a₁, a₂ : a₁ ∈ Σ.accounts ∧ a₂ ∈ Σ.accounts ∧ a₁ ≠ a₂ :
      ¬prefix(a₁, a₂) ∧ ¬prefix(a₂, a₁))

This follows from the tumbler hierarchy's zero-field structure: account
addresses occupy a single level in the hierarchy, separated by zero-field
boundaries. An account address has the form node.0.user, and no such
address can be a proper prefix of another address at the same level —
extending an account address crosses a zero-field boundary into the document
level. DL-A1 is what makes the definite description below well-defined.

We define the *owner* of a document as the account whose address is a
prefix of the document's address:

    owner(d) = (THE a : a ∈ Σ.accounts : prefix(a, d))

The existence of such an account is guaranteed by DΣ2. The uniqueness
follows from DL-A1: if two distinct accounts a₁ and a₂ were both prefixes
of d, then — since the tumbler ordering is hierarchical — one would
necessarily be a prefix of the other, contradicting DL-A1. We write
owner(d) throughout, understanding it as a function derived from the
address, not stored separately.

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

We require that the allocation mechanism produces addresses under the
account's own prefix:

**DL-ALLOC (allocation produces subtree addresses).**

    (A a : a ∈ Σ.accounts : prefix(a, Σ.next(a)))

That is, the next available address under account a has a as a proper
prefix. Since the counter only advances within the account's subtree (by
tumbler forking, which appends sub-digits), every allocated address inherits
the account prefix. This is what makes DL5 (ownership from address)
derivable from the allocation mechanism.

**DΣ6 (session state).** Σ.sessions : Set(SessionEntry) where each entry
records (connection, document, access-level). This component tracks which
documents are currently open in which sessions. It is orthogonal to document
content.

**DΣ7 (links).** For each document d ∈ Σ.docs, Σ.links(d) : Set(Link) is
the set of links homed in d. Each link has three endsets (from, to, type),
each being a set of I-space address spans. We state this component
explicitly because frame conditions must address links alongside
arrangements.


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
recycled — no future allocation produces the same address:

    d ∈ Σ.docs  ⟹
      (A d' : d' is freshly allocated in any Σ' subsequent to Σ : d' ≠ d)

This follows from the monotonicity of the allocation counter (DΣ5): since
Σ.next(a) only advances, and the fresh address is always at or beyond the
current counter value, no previously allocated address can be produced
again. Together with DL0 (the address remains in docs) and DL1 (addresses
are unique), DL2 establishes that a tumbler is a permanently unique
identifier — it denotes one document and one document only, across all time.

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
and an arrangement (empty). It can be opened. It is a position in the
docuverse — baptized, named, owned — waiting for content. Nelson's metaphor
is precise: the owner "designates new addresses by forking" [LM 4/17], and
designation precedes population.

    DL5 (ownership from address):  owner(d) = a

The new document's owner is the account under which it was allocated. This
is not stored as a separate field — it is derived from the address itself,
because a is a prefix of d. The document at address `1.0.2.0.5` is owned by
account `1.0.2` because `1.0.2` is its account-level prefix. No ownership
table is consulted; the tumbler encodes the relationship structurally.

The derivation is: DL-ALLOC guarantees that the address produced by
advancing Σ.next(a) has a as a proper prefix. Since owner(d) is defined as
the unique account that is a prefix of d (DΣ2, DL-A1), and a is that
account, we have owner(d) = a.

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

    DL-F4 (links unchanged):
      (A d' : d' ∈ Σ.docs : Σ'.links(d') = Σ.links(d'))

The frame conditions are as important as the postconditions. DL-F1 says that
no existing document's arrangement is disturbed. DL-F2 says that no I-space
content is created or modified. DL-F3 says that other accounts' allocation
counters are unaffected. DL-F4 says that no document's links are altered —
creating an empty document introduces no links.

Nelson derives DL-F1 from three converging principles: tumbler permanence
(addresses don't break), ownership (creating B cannot modify A, because B's
creator might not own A), and I-space immutability (no content changes).
"Thus users may create new published documents out of old ones indefinitely,
making whatever changes seem appropriate — without damaging the originals"
[LM 2/45]. Though stated in the context of versioning, the non-damage
principle holds a fortiori for the simpler case of creating a fresh
empty document.

CREATENEWDOCUMENT's effect is entirely additive: it allocates one address
and initialises one empty arrangement. It touches neither the content store
nor any other document's state.


## The Empty Document

We noted that DL4 establishes dom(Σ'.poom(d)) = ∅. This deserves further
examination, because the empty document state has structural consequences.

**DL7 (empty document retrievability).** For any document d with
dom(Σ.poom(d)) = ∅, retrieval of any V-span returns the empty sequence:

    retrieve(d, S) = ε    for all spans S

This is immediate: retrieval resolves V-positions through the arrangement
mapping, and the empty mapping has no positions to resolve. An empty
document is readable — it simply has nothing to say.

**DL8 (empty document addressability).** An empty document d ∈ Σ.docs can
be identified by its tumbler address — it can be opened, queried, and named
as a target of operations. However, it cannot be the target of a link's
content endsets, because link endsets reference I-space addresses and an
empty document has no I-space content: img(Σ.poom(d)) = ∅, so there are no
I-addresses to reference.

Nelson confirms that the system can address entities with no stored content:
"it is possible to link to a node, or an account, even though there is
nothing stored in the docuverse corresponding to them" [LM 4/23]. But
"link to" here means "address" or "identify" — the entity is reachable in
the tumbler space. For a link's endset to reference specific content within
a document, that content must first exist. An empty document is addressable
but not yet linkable-to at the content level.

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
never recycled). The account set only grows (DL-A0 — accounts are
permanent). So the witnessing account remains in Σ.accounts, and the prefix
relation — being a structural property of the tumbler — cannot change.  ∎

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
derivative work. The owned-source case places the version as a sub-address
(depth 1: a child of the source), while the unowned-source case allocates a
fresh document under the user's account (depth 2: identical in structure to
CREATENEWDOCUMENT).

**DL15 (content sharing).** The new version's arrangement preserves the
source's text arrangement — not merely the same set of I-addresses, but
the same V-to-I mapping structure restricted to the text subspace:

    Σ'.poom(v) = Σ.poom(source)|text

where f|text denotes the *domain restriction* of the arrangement mapping
f to V-positions in the text subspace. A document's arrangement maps
V-positions across two subspaces: text (subspace 1.x) and links (subspace
0.x). Versioning copies the text arrangement but not the link arrangement —
the new version begins with no links of its own. The restriction is a
domain restriction: for each V-position p in the text subspace of the
source, Σ'.poom(v)(p) = Σ.poom(source)(p), and the new version has no
other mappings.

A consequence is that no new I-space content is allocated. The I-addresses
referenced by Σ'.poom(v) are exactly those already referenced by the
source's text arrangement. Content bytes exist once in I-space;
arrangements reference them multiply.

**DL16 (source unchanged).** CREATENEWVERSION does not modify the source:

    Σ'.poom(source) = Σ.poom(source)

The source document's arrangement is completely unaffected. This is Nelson's
non-destruction guarantee applied to versioning: "without damaging the
originals" [LM 2/45]. Combined with DL15 (content sharing), this means the
operation is purely additive — it creates new state (the version's document
entry and arrangement) without altering existing state.

*Frame conditions:*

    DL-V1 (existing documents unchanged):
      (A d' : d' ∈ Σ.docs ∧ d' ≠ source :
        Σ'.poom(d') = Σ.poom(d'))

    DL-V2 (content unchanged):  Σ'.ispace = Σ.ispace

    DL-V3 (other accounts unchanged):
      (A a' : a' ∈ Σ.accounts ∧ a' ≠ user.account :
        Σ'.next(a') = Σ.next(a'))

    DL-V4 (links unchanged):
      (A d' : d' ∈ Σ.docs : Σ'.links(d') = Σ.links(d'))

DL-V1 together with DL16 covers all existing documents: the source is
unchanged (DL16), and every other existing document is unchanged (DL-V1).
DL-V2 says no I-space content is created — the version references existing
I-addresses. DL-V3 says allocation counters for other accounts are
unaffected. DL-V4 says no existing document's links are altered; the new
version begins with an empty link set (Σ'.links(v) = ∅), which does not
affect any existing document.

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
open and that any implementation must address. The question is: what
coordination is needed when multiple connections interact with documents?

Nelson's 17 FEBE commands are stateless — "What the Xanadu storage and
hypertext system does — and thus is — is defined by the commands to which
it responds" [LM 4/61]. There is no OPEN command, no CLOSE command, no
session lifecycle in the design specification. Nelson's protocol names a
document by tumbler address, issues a command, and receives a response.
There is no concept of a "currently open document."

Yet any implementation must address practical coordination: what happens
when two connections attempt to modify the same document? We abstract the
minimal coordination properties here — not because they are Nelson's
specification, but because they represent what any implementation must
provide to uphold the lifecycle guarantees above.

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
appropriate — without damaging the originals" [LM 2/45]. The redirection
is a session-layer policy that automatically branches on write denial.

**DL21 (session orthogonality).** Session state is orthogonal to document
content. Opening or closing a document does not alter its arrangement,
I-space content, or links:

    If Σ' differs from Σ only by a session open or close:
      Σ'.poom(d) = Σ.poom(d)    for all d
      Σ'.ispace = Σ.ispace
      Σ'.docs = Σ.docs

A session entry is an access control token, not a document state component.
Session operations manipulate only the session table — they do not touch
document arrangements, the content store, or the link index. A document's
state is entirely independent of whether any session holds it open.

**DL22 (no in-place access upgrade).** A session cannot upgrade from READ
to WRITE access on the same document:

    (c, d, READ) ∈ Σ.sessions  ⟹
      ¬ may_add(c, d, WRITE) to Σ'.sessions without first removing (c, d, READ)

The path from reader to writer requires closing the read session and opening
a new write session — or, under the redirection policy (DL20), creating a
new version and writing to that instead. There is no mutation of the
access-level field in an existing session entry.

The abstract justification is that session entries are immutable tokens: a
session is created with a fixed access level and destroyed as a unit. This
is the minimal property needed to prevent a read-to-write escalation from
bypassing write exclusivity (DL19) — if a reader could silently become a
writer, two writers could coexist (one original, one upgraded). The denial
applies even when the requesting connection is the one already holding the
read entry: the requester's *own* prior read session blocks the write
request.


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

*Proof.* CREATENEWDOCUMENT: by DL-F1 (arrangements unchanged) and DL-F2
(I-space unchanged) directly.

CREATENEWVERSION: for d' = source, DL16 gives Σ'.poom(source) =
Σ.poom(source). For d' ≠ source, DL-V1 gives Σ'.poom(d') = Σ.poom(d').
So all existing documents' arrangements are preserved. DL-V2 gives
Σ'.ispace = Σ.ispace, so I-space content is preserved.

The new version is fresh (DL13), so it is not in Σ.docs and the
quantification over d' ∈ Σ.docs excludes it.  ∎

*Note on links.* The frame conditions DL-F4 and DL-V4 establish that
neither operation modifies any existing document's link set. We could
strengthen DL-ISO to include Σ'.links(d') = Σ.links(d'), and the proof
would follow directly from these frame conditions. We state this separately
because DΣ7 (the link state component) was introduced for this purpose, and
the link isolation property depends entirely on the frame conditions rather
than any deeper structural argument.

The isolation guarantee follows from four converging principles: tumbler
permanence (addresses never invalidated), ownership exclusivity (creating B
cannot touch A if B's creator does not own A), I-space immutability (content
never changes), and the append-only address space (new documents are added,
never substituted). Nelson does not state isolation as a single axiom, but
it is a necessary consequence of his architectural choices.


## Worked Example

We verify the properties against a concrete scenario.

*Initial state Σ₀.* Account `1.0.2` exists: `1.0.2` ∈ Σ₀.accounts.
Account `1.0.3` exists: `1.0.3` ∈ Σ₀.accounts. Both allocation counters
are at their initial values: Σ₀.next(`1.0.2`) = `1.0.2.0.1`,
Σ₀.next(`1.0.3`) = `1.0.3.0.1`. The document set, I-space, and link
sets are all empty.

*Step 1: CREATENEWDOCUMENT(`1.0.2`) → Σ₁.*

Check PRE-DOC: `1.0.2` ∈ Σ₀.accounts. ✓

This produces document d₁ = `1.0.2.0.1`.

- DL3 (fresh): `1.0.2.0.1` ∈ Σ₁.docs ∧ `1.0.2.0.1` ∉ Σ₀.docs. ✓
- DL4 (empty): dom(Σ₁.poom(d₁)) = ∅. ✓
- DL5 (ownership): owner(d₁) = `1.0.2`, because prefix(`1.0.2`, `1.0.2.0.1`). ✓
  (DL-ALLOC guarantees the allocated address has the account prefix.)
- DL6 (counter): Σ₁.next(`1.0.2`) = `1.0.2.0.2` > `1.0.2.0.1`. ✓
- DL-F2 (content unchanged): Σ₁.ispace = Σ₀.ispace = ∅. ✓
- DL-F3 (other accounts): Σ₁.next(`1.0.3`) = `1.0.3.0.1` = Σ₀.next(`1.0.3`). ✓
- DL-F4 (links unchanged): no links exist; Σ₁.links = Σ₀.links. ✓

*Step 2: INSERT into d₁ — content "AB" at position 1.* This produces Σ₂.

The INSERT operation allocates two I-space addresses (say i₁, i₂) with
Σ₂.ispace(i₁) = 'A' and Σ₂.ispace(i₂) = 'B', and sets Σ₂.poom(d₁)
to map V-position 1 → i₁, V-position 2 → i₂.

Now dom(Σ₂.poom(d₁)) = {1, 2} and img(Σ₂.poom(d₁)) = {i₁, i₂}.

*Step 3: CREATENEWVERSION(d₁, user `1.0.2`) → Σ₃.* Same owner versions.

- DL13 (fresh): produces v₁ = `1.0.2.0.1.0.1`. v₁ ∈ Σ₃.docs ∧ v₁ ∉ Σ₂.docs. ✓
- DL14 (address placement, same owner): v₁ = d₁ ∥ `0.1`, so
  prefix(`1.0.2.0.1`, `1.0.2.0.1.0.1`). The version is a sub-address of the source. ✓
- DL5 (ownership): owner(v₁) = `1.0.2` (the same account). ✓
- DL15 (content sharing): Σ₃.poom(v₁) = Σ₂.poom(d₁)|text. Since d₁ has
  only text content (no links), this is Σ₃.poom(v₁) = Σ₂.poom(d₁):
  V-position 1 → i₁, V-position 2 → i₂. Same mapping, same I-addresses. ✓
- DL16 (source unchanged): Σ₃.poom(d₁) = Σ₂.poom(d₁). ✓
- DL-V2 (content unchanged): Σ₃.ispace = Σ₂.ispace. No new I-addresses allocated. ✓
- DL-V4 (links unchanged): Σ₃.links(d₁) = Σ₂.links(d₁). ✓

*Step 4: CREATENEWVERSION(d₁, user `1.0.3`) → Σ₄.* Cross-user versioning.

User `1.0.3` does not own d₁, so the version is allocated under `1.0.3`:

- DL13 (fresh): produces v₂ = `1.0.3.0.1`. v₂ ∈ Σ₄.docs ∧ v₂ ∉ Σ₃.docs. ✓
- DL14 (address placement, different owner):
  prefix(`1.0.3`, `1.0.3.0.1`) ∧ ¬prefix(`1.0.2.0.1`, `1.0.3.0.1`).
  The version lives under the versioning user's account, not the source's. ✓
- DL5 (ownership): owner(v₂) = `1.0.3`. The cross-user versioner owns
  their derivative. ✓
- DL15 (content sharing): Σ₄.poom(v₂) = Σ₃.poom(d₁)|text. Same
  I-addresses i₁, i₂. Content is shared, not copied. ✓
- DL16 (source unchanged): Σ₄.poom(d₁) = Σ₃.poom(d₁). ✓
- DL-V1 (other documents): Σ₄.poom(v₁) = Σ₃.poom(v₁). The earlier
  version is also unaffected. ✓
- DL-V3 (other accounts): Σ₄.next(`1.0.2`) = Σ₃.next(`1.0.2`). Account
  `1.0.2`'s counter is unaffected by `1.0.3`'s allocation. ✓

*Final state.* Σ₄.docs = {d₁, v₁, v₂}. All three documents reference
the same I-space content {i₁, i₂}. d₁ and v₁ are owned by `1.0.2`; v₂
is owned by `1.0.3`. No document's creation disturbed any other's state.
DL-ISO holds at every step.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| DΣ1 | Σ.docs : Set(Tumbler) — the set of allocated document addresses | introduced |
| DΣ2 | Σ.accounts : Set(Tumbler) — account addresses; every document prefixed by some account | introduced |
| DΣ3 | Σ.ispace : IAddr ⇀ Byte — permanent content store (permanent, immutable) | introduced |
| DΣ4 | Σ.poom(d) : VPos ⇀ IAddr — arrangement mapping per document | introduced |
| DΣ5 | Σ.next : Tumbler → Tumbler — per-account allocation counter, monotonically advancing | introduced |
| DΣ6 | Σ.sessions : Set(connection, document, access-level) — session state | introduced |
| DΣ7 | Σ.links(d) : Set(Link) — links homed in each document | introduced |
| DL-A0 | a ∈ Σ.accounts ⟹ a ∈ Σ'.accounts — account permanence | introduced |
| DL-A1 | no account address is a prefix of another — prefix-freeness | introduced |
| DL-ALLOC | Σ.next(a) produces addresses with prefix(a, _) — allocation stays in account subtree | introduced |
| owner(d) | owner(d) = (THE a : a ∈ Σ.accounts : prefix(a, d)) — ownership derived from address prefix | introduced |
| DL0 | d ∈ Σ.docs ⟹ d ∈ Σ'.docs — document identity is permanent | introduced |
| DL1 | distinct documents have distinct addresses | introduced |
| DL2 | allocated addresses are never recycled — no future allocation reuses a past address | introduced |
| PRE-DOC | CREATENEWDOCUMENT requires only a ∈ Σ.accounts | introduced |
| DL3 | CREATENEWDOCUMENT produces a fresh address: d ∈ Σ'.docs ∧ d ∉ Σ.docs | introduced |
| DL4 | freshly created document has empty arrangement: dom(Σ'.poom(d)) = ∅ | introduced |
| DL5 | owner(d) = a — ownership derived from DL-ALLOC and prefix structure | introduced |
| DL6 | allocation counter strictly advances on creation | introduced |
| DL-F1 | existing documents' arrangements unchanged by CREATENEWDOCUMENT | introduced |
| DL-F2 | I-space unchanged by CREATENEWDOCUMENT | introduced |
| DL-F3 | other accounts' counters unchanged by CREATENEWDOCUMENT | introduced |
| DL-F4 | existing documents' links unchanged by CREATENEWDOCUMENT | introduced |
| DL7 | retrieval from an empty document returns the empty sequence | introduced |
| DL8 | an empty document is addressable but not linkable-to at the content level | introduced |
| DL9 | ownership is permanent — owner(d) never changes (proof from DL0, DL2, DL-A0) | introduced |
| DL10 | only the owner may modify a document's arrangement | introduced |
| DL11 | owner controls out-links (links homed in the document) | introduced |
| DL12 | publication relinquishes owner control over linking, transclusion, and withdrawal | introduced |
| DL13 | CREATENEWVERSION produces a fresh document | introduced |
| DL14 | version address encodes derivation (sub-address of source if same owner; user's account otherwise) | introduced |
| DL15 | version's text arrangement equals source's text arrangement (domain restriction to text subspace) | introduced |
| DL16 | CREATENEWVERSION does not modify the source document | introduced |
| DL-V1 | existing documents' (other than source) arrangements unchanged by CREATENEWVERSION | introduced |
| DL-V2 | I-space unchanged by CREATENEWVERSION | introduced |
| DL-V3 | other accounts' counters unchanged by CREATENEWVERSION | introduced |
| DL-V4 | existing documents' links unchanged by CREATENEWVERSION | introduced |
| DL17 | no operation distinguishes "primary" vs "derivative" versions | introduced |
| DL18 | session entry is (connection, document, access-level) | introduced |
| DL19 | at most one write session per document at any time | introduced |
| DL20 | write denial may trigger version creation (redirection, not error) | introduced |
| DL21 | session open/close does not alter document content, ispace, or doc set | introduced |
| DL22 | no in-place READ→WRITE access upgrade on same session entry | introduced |
| DL23 | publication is voluntary — only owner initiates | introduced |
| DL24 | publication is near-permanent — withdrawal requires extraordinary process | introduced |
| DL25 | publication grants universal read/link/transclude access but not modification | introduced |
| DL-ISO | neither creation operation modifies any existing document's arrangement or I-space (theorem) | introduced |


## Open Questions

Must the system guarantee that a document's arrangement is recoverable after a crash that interrupts CREATENEWDOCUMENT between address allocation and POOM initialisation?

What invariant must the allocation counter satisfy when multiple accounts reside on the same node — must per-account counters be independent, or may a global counter serve?

Must the session layer guarantee that a document owner can always obtain write access to their own document, even when other readers hold it open?

What must the system guarantee about documents whose storage rental has lapsed — does DL0 (identity permanence) hold unconditionally, or is it conditioned on economic obligations being met?

Must the publication transition be atomic — can a document be observed in a partially-published state by concurrent readers?

What consistency must the system maintain between a document's session state and its arrangement if a connection terminates abnormally without executing CLOSE?

When a user versions a document they do not own, must the system record the derivation relationship, or is the relationship visible only through shared I-space addresses?

Must the system prevent a document from being opened for write by two connections belonging to the same owner account, or does DL19 quantify over connections regardless of the account behind them?
