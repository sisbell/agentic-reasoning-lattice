# ASN-0009: Version Semantics

*2026-02-23*

We wish to understand what it means to create a new version of a document.
The operation appears simple — "copy this document's text into a new
document" — but its consequences ramify through the entire system: through
link discovery, through content identity, through the permanence guarantee
itself. What, precisely, does versioning preserve? What does it establish?
And what relationship persists between parent and child as they
independently evolve?

The central tension is this: versions must be independent enough that
editing one never affects another, yet connected enough that the system can
compute what they share. We seek the formal properties that make both
guarantees simultaneously achievable.


## State Components

We need a model of documents before we can reason about versioning them.
A document d in system state Σ has:

- d.addr : Tumbler — the permanent address of the document
- d.vmap : VPos → IAddr — the arrangement mapping (V-space to I-space)
- d.links : Set(LinkId) — links homed in this document
- d.owner : UserId — the document's owner
- d.parent : DocId ∪ {⊥} — the document from which this was versioned, or ⊥ if not created by versioning

The arrangement d.vmap is what makes a document a document. It maps virtual
positions — the sequential reading order — to permanent I-space addresses
where content resides. Two documents may map different positions to the same
I-address; when they do, they share content identity at that address.

We write img(d.vmap) for the image of d.vmap — the set of I-addresses that
d references:

    img(d.vmap) = { a : (∃ v : v ∈ dom(d.vmap) : d.vmap(v) = a) }

A document's arrangement has two subspaces: the text subspace (positions
conventionally prefixed 1.x) and the link subspace (positions prefixed
0.x). We write d.vmap|text for the restriction to the text subspace and
d.vmap|link for the restriction to the link subspace.

The system state Σ also includes:

- Σ.docs : Set(Doc) — all documents in the system
- Σ.ispace : IAddr → Content — the permanent content store (append-only)
- Σ.spanindex : IAddr → Set(DocId) — which documents contain which content
- Σ.linkindex : IAddr → Set(LinkId) — which links touch which content
- Σ.alloc : IAddr — the next I-address to be assigned

The span index records, for each I-address, every document whose
arrangement references it. The link index records, for each I-address,
every link whose endsets touch it. Both are global — scoped to the system,
not to individual documents.


## The Version Operation

We define CREATENEWVERSION(d, u) — user u creates a new version of
document d — by precondition, postcondition, and frame conditions. Let Σ
be the state before and Σ' the state after.

**Precondition.** The source document must exist:

    PRE-VER:  d ∈ Σ.docs

That is the entire precondition. There is no ownership restriction — any
user may version any document. This is not an oversight but a deliberate
design choice. Nelson's pluralistic publishing model depends on non-owners
creating derivative works freely. The original is never damaged; the
version is a new document under the creating user's control:

> "Thus users may create new published documents out of old ones
> indefinitely, making whatever changes seem appropriate — without
> damaging the originals." [LM 2/45]

The access model explicitly redirects denial into divergence. If a user
cannot modify a document, they create a version. The system should never
produce a permanent dead end — only a fork into a new document under the
user's ownership.

**Postcondition — what is established.** The operation produces a fresh
document d' satisfying six properties:

**VER0** (fresh document). d' is new — it did not exist before:

    d' ∈ Σ'.docs  ∧  d' ∉ Σ.docs

**VER1** (arrangement isomorphism). The version's arrangement is
order-isomorphic to the source's text subspace. That is, there exists an
order-preserving bijection φ : dom(d.vmap|text) → dom(d'.vmap) such that:

    (A v : v ∈ dom(d.vmap|text) : d'.vmap(φ(v)) = d.vmap|text(v))

The version has the same content in the same reading order — not merely the
same set of I-addresses. Image equality (img(d'.vmap) = img(d.vmap|text))
follows as a corollary, but is too weak on its own: it would permit
deduplication, scrambling, or padding. VER1 constrains both which I-addresses
appear and how they are arranged.

No new content is created; the version is a new arrangement over existing
permanent content that preserves the source's sequential structure. We
emphasise: the restriction is to the text subspace. The link subspace is
excluded.

**VER2** (empty link space). The version starts with no home links:

    d'.links = ∅

Links are owned by their home document. They do not migrate when a version
is created. The source document's links remain the source's property.

At first this seems like a loss — the version inherits no annotations, no
connections. But the apparent loss is illusory. We shall see (VER8 below)
that links made *to* the source's content are discoverable from the
version through shared I-space identity. What the version lacks is
*ownership* of those links; what it retains is *access* to them.

**VER3** (address ancestry). The version's address extends the source's
address by a version suffix:

    (E s : #s > 0 : d'.addr = d.addr ∥ s)

where ∥ denotes tumbler concatenation — d'.addr has d.addr as a proper
prefix, extended by one or more additional components. We call d'.addr a
*sub-address* of d.addr when this prefix relationship holds.

The tumbler addressing system records parentage conventionally — the new
document's address indicates which document it was versioned from. Nelson
notes an important qualification: "the version, or subdocument number is
only an accidental extension of the document number, and strictly implies
no specific relationship of derivation" [LM 4/29]. The address *indicates*
ancestry by placement; it does not *entail* derivation logically. The
stronger record of parentage is the shared I-space content (VER1), which is
structural and irrevocable.

**VER4** (ownership). The version belongs to whoever created it:

    d'.owner = u

This holds regardless of who owns d. A non-owner who versions a published
document becomes the owner of the version. The original's owner retains
full control of the original; the versioner gains full control of the
derivative.

**VER5** (span index registration). Every I-address in the version's
arrangement is registered in the span index:

    (A a : a ∈ img(d'.vmap) : d' ∈ Σ'.spanindex(a))

This registration is what makes the version discoverable. A query of
"which documents contain this content?" will find the version alongside the
original, because both are registered against the same I-addresses.

**VER-P** (parentage). The version records its source:

    d'.parent = d

This is the sole operation that establishes parentage. For documents created
by other means (CREATENEWDOCUMENT), parent is ⊥. No operation modifies
parent once established — it is set at creation and never written again.

**Frame conditions — what is preserved.**

**VER-F1** (source unchanged). The source document is entirely unaffected:

    d.vmap in Σ' = d.vmap in Σ
    d.links in Σ' = d.links in Σ
    d.owner in Σ' = d.owner in Σ
    d.parent in Σ' = d.parent in Σ

**VER-F2** (no content allocation). I-space does not grow:

    Σ'.ispace = Σ.ispace
    Σ'.alloc = Σ.alloc

This is the sharpest distinction between versioning and insertion. INSERT
extends I-space — it allocates fresh addresses and stores new content.
CREATENEWVERSION does not. It creates a new arrangement over *existing*
content. Versioning is a purely structural operation.

**VER-F3** (other documents unchanged).

    (A e : e ∈ Σ.docs ∧ e ≠ d : e is unchanged in Σ')

**VER-F4** (link index unchanged).

    Σ'.linkindex = Σ.linkindex

No links are created, destroyed, or modified by versioning.


## Version Isolation

The most important consequence of versioning is mutual independence. Once
a version exists, it and its source evolve without interference. We state
this as a theorem, not an axiom, because it follows from a more basic
property.

We first make explicit the load-bearing premise.

**VER-SCOPE** (operation scoping). Every editing operation (INSERT, DELETE,
REARRANGE, COPY) *writes* to exactly one document's arrangement, identified
by the document address passed as an explicit argument.

Note that some operations *read* from multiple documents — COPY reads a
source document and writes to a target. VER-SCOPE constrains the write
side: each operation modifies exactly one document's vmap. The read side
is immaterial to isolation, since reading does not alter state.

**Theorem VER-ISO** (version isolation). For any operation op applied to
document d after CREATENEWVERSION(d) has produced d':

    d'.vmap after op = d'.vmap before op

and symmetrically, for any operation applied to d':

    d.vmap after op = d.vmap before op

*Proof.* By VER-SCOPE, each editing operation writes to exactly one
document's arrangement, located by its address. Since d'.addr ≠ d.addr
(by VER0 — d' is fresh, so its address differs from d's), no operation
targeting d can locate d'.vmap for writing, and no operation targeting d'
can locate d.vmap for writing. ∎

The proof rests on VER-SCOPE and address distinctness. We do not need to
verify isolation for each operation separately; it follows from the scoping
property universally.

Nelson states the user-facing consequence directly: "the owner of a
document may delete bytes from the owner's current version, but those bytes
remain in all other documents where they have been included" [LM 4/11].
The I-space content that two versions share is immutable; only the V-space
arrangements change, and each arrangement changes independently.


## Content Identity and Correspondence

The relationship between versions is not organisational — it is structural.
Two documents that share I-addresses share content identity, and this
identity is computable from the addresses alone.

**Definition COR** (correspondence). For documents d₁ and d₂, positions v₁
in d₁ and v₂ in d₂ *correspond* when they map to the same I-address:

    correspond(d₁, v₁, d₂, v₂) ≡ d₁.vmap(v₁) = d₂.vmap(v₂)

This is a pointwise definition. It extends naturally to spans: positions
[v₁, v₁ + w) in d₁ correspond to [v₂, v₂ + w) in d₂ when correspondence
holds at every position in the range:

    (A i : 0 ≤ i < w : correspond(d₁, v₁ + i, d₂, v₂ + i))

We note that such span correspondence does not require the I-addresses to
form a contiguous range. After editing operations, contiguous V-positions
routinely map to non-contiguous I-addresses (an INSERT in the middle of a
span splits its I-address continuity). The pointwise definition remains
well-defined regardless; the span is contiguous in V-space even when the
underlying I-addresses are not.

**VER6** (initial bijective correspondence). Immediately after
CREATENEWVERSION(d) produces d', the correspondence is a bijection between
the text domain of d and the entire domain of d'. By VER1, the
order-preserving bijection φ establishes:

    (A v : v ∈ dom(d.vmap|text) : correspond(d, v, d', φ(v)))

Every text position in the source has a unique corresponding position in the
version, and conversely, every position in d' corresponds to exactly one
text position in d. The bijection φ from VER1 witnesses both directions.

As the two documents are independently edited, correspondence may shrink.
If a passage is deleted from one version's arrangement, the positions that
mapped to those I-addresses no longer exist in that version's domain, and
correspondence at those positions ceases. But correspondence never grows
by coincidence: two independently typed copies of the word "hello" receive
different I-addresses and do not correspond, even though they contain the
same bytes. Correspondence is identity of *origin*, not equality of
*content*.

**VER7** (correspondence durability). The I-addresses that underlie
correspondence are permanent:

    (A a : a ∈ dom(Σ.ispace) : a ∈ dom(Σ'.ispace))    for all subsequent Σ'

Even if both versions delete a passage from their arrangements, the shared
I-addresses persist in I-space. The system can in principle still determine
that the two documents once shared that content. What is lost is the
V-space mapping — the positions — not the I-space identity.

The operation SHOWRELATIONOF2VERSIONS computes the correspondence relation
by converting both documents' V-space arrangements to I-space addresses and
intersecting. The result is a set of span pairs — positions in d₁ paired
with positions in d₂ that map to the same I-addresses. This computation
requires no metadata beyond the arrangement mappings and the I-space
addresses themselves. Correspondence is not tracked; it is *derived*.


## Link Discoverability Across Versions

We arrive at a subtle but critical property. A link created against content
in one document must be discoverable from any other document that shares
the same I-addresses — including versions created before or after the link.

The mechanism is the global link index. A link's endsets reference I-space
addresses. Link discovery converts a query document's V-space positions to
I-space addresses, then searches the link index for intersections. The
query is over I-space, not over documents.

**VER8** (content-identity link discovery). For any link ℓ whose endset
references I-address a, and any document d such that a ∈ img(d.vmap):

    ℓ is discoverable from d at a

This holds regardless of which document ℓ was created in, and regardless
of temporal ordering. A link created on the original *after* the version
fork is discoverable from the version, because the version shares the
I-addresses that the link's endsets touch. Symmetrically, a link created
on the version is discoverable from the original.

We can state the symmetry precisely. Let discover(d, v) denote the set of
links discoverable from document d at position v. The discovery procedure
is: (1) convert v to I-address a via d.vmap; (2) query the link index for
all links whose endsets touch a; (3) return the result.

**VER9** (symmetric discoverability). If d₁.vmap(v₁) = d₂.vmap(v₂) = a,
then:

    discover(d₁, v₁) = discover(d₂, v₂)

That is, any two positions that map to the same I-address discover exactly
the same links. The documents' identities are irrelevant; only the
I-address matters.

This is what Nelson calls "refractive following": "Links may be
refractively followed from a point or span in one version to corresponding
places in any other version. Thus a link to one version of a Prismatic
Document is a link to all versions" [LM 2/26]. The symmetry is not a
feature added on top of versioning — it falls out of the architecture.
Content identity IS the link discovery mechanism, and versions share
content identity.

Together, VER2 and VER8 describe an elegant partition. The version *owns*
no links (VER2 — its link space is empty). But the version has *access* to
every link that touches its content (VER8 — through shared I-addresses).
Link ownership and link discoverability are independent dimensions, and
versioning preserves the latter while deliberately not copying the former.


## The Divergence Model

We must now address what versions are *not*. The system provides no merge
operation. Versions diverge and can be compared, but never converge.

**VER10** (divergence only). No primitive operation combines the
arrangements of two documents relative to a common ancestor.

This absence is deliberate. Three-way merge requires three capabilities,
none of which the system provides as primitives:

(a) *Ancestor identification.* The system would need a "find common
    ancestor" operation. Address ancestry is conventional (VER3), not a
    formal derivation record, and no "find parent" query exists.

(b) *Differential computation.* SHOWRELATIONOF2VERSIONS computes what two
    documents *share*, not what each *changed* relative to a base. Without
    a base, there is no notion of "A's changes" versus "B's changes."

(c) *Conflict resolution.* Merging requires editorial judgement about what
    to keep when changes conflict. Nelson explicitly leaves such judgement
    to the human.

A user who wishes to combine elements from two divergent versions can
construct a new document using COPY (transclusion). The result is a third
document that shares I-addresses with both parents. But this is not merging
— it produces a new divergent version that draws from two sources. The
parent versions remain unchanged and independent.

**VER11** (operational symmetry). No operation's precondition or
postcondition references a "primary version" designator. Formally: the
set of operations available on document d₁ and their semantics are
identical to those available on d₂, for any d₁, d₂ ∈ Σ.docs:

    (A op : op ∈ Operations :
      pre(op, d₁) and post(op, d₁) have the same form as
      pre(op, d₂) and post(op, d₂))

This is a claim about the operation set, not a universally quantified
statement about all system properties. System quantities such as address
length (VER3) and creation time do distinguish versions — what VER11
asserts is that these distinctions carry no operational weight. There is
no trunk, no main branch, no current version.

Nelson states this directly: "There is thus no 'basic' version of a
document set apart from other versions — 'alternative' versions — any
more than one arrangement of the same materials is a priori better than
other arrangements" [LM 2/19].

The entire pluralistic publishing model rests on this equality. If one
version were privileged, divergence would be a defect. When all versions
are operationally equal, divergence is a feature — multiple viewpoints
coexisting permanently.


## Version Ancestry

Versions form a forest. Each document has at most one parent from which it
was versioned, the ancestry relation is acyclic, and the forest has
unbounded depth.

The parent relation is a state component (d.parent in our state model),
not a derived quantity. CREATENEWVERSION is the sole operation that
establishes it (postcondition VER-P: d'.parent = d), and no operation
modifies it once set (frame condition VER-F1 preserves d.parent for the
source; VER-F3 preserves it for all other documents). We define the
convenience function parent(d) = d.parent, and for documents not created
by versioning, parent(d) = ⊥.

**VER12** (ancestry is a forest). The parent relation satisfies three
conditions:

(i) *Functionality.* parent(d) is uniquely defined for each d — this is
    immediate from parent being a state component (a function, not a
    relation).

(ii) *Well-foundedness.* Each document's parent, when not ⊥, exists:

    (A d : d ∈ Σ.docs : parent(d) = ⊥  ∨  parent(d) ∈ Σ.docs)

(iii) *Acyclicity.* No document is its own ancestor:

    (A d : d ∈ Σ.docs : d ∉ parent⁺(d))

where parent⁺ is the transitive closure.

The acyclicity follows from VER0: each CREATENEWVERSION produces a fresh
document, so parent(d') = d implies d' ∉ Σ.docs at the time d existed.
Since documents are permanent (VER14) and parent is immutable, a backward
edge would require parent(d) = d' for some d that existed before d', but
parent(d) was already set (to some value or ⊥) before d' was created and
cannot be changed. This argument relies on sequential execution — document
creation is totally ordered — which we assume throughout this ASN.

The forest has unbounded depth — a version can itself be versioned, and
that version versioned again, without limit. The tumbler addressing system
accommodates this through hierarchical sub-addressing: if d has address A,
its first version has address A.1, whose first version has address A.1.1,
and so on. Tumbler arithmetic uses arbitrary-precision integers, so no
depth limit exists.

**VER13** (ancestry permanence). Once established, parentage never changes:

    parent(d) = x in Σ  ⟹  parent(d) = x in Σ'    for all subsequent Σ'

This follows from the frame conditions: only CREATENEWVERSION writes
d'.parent, and it does so only for the freshly created d'. No operation
writes d.parent for any existing document d.


## Version Permanence

Each version is independently permanent. Its existence depends on no other
document — not its parent, not its siblings, not any document it
transcludes from.

**VER14** (independent permanence). Once a version exists, it persists:

    d ∈ Σ.docs  ⟹  d ∈ Σ'.docs    for all subsequent Σ'

This holds for all documents, but it bears special emphasis for versions
because one might wrongly imagine that a version "depends on" its parent.
The version's arrangement references I-space addresses, which are permanent
by the append-only property of I-space. The content that parent and child
both reference persists not because either version "keeps it alive," but
because I-space content is permanent by construction.

Nelson rejects any notion of version hierarchy: "There is thus no 'basic'
version" [LM 2/19]. If no version is basic, then no version can be the
foundation on which others depend. They are all equal arrangements over
permanent I-space content.


## The Versioning–Transclusion Equivalence

We close by observing a deep structural equivalence. At the I-space level,
CREATENEWVERSION and COPY (transclusion) perform the same fundamental
action: they create an arrangement that references existing I-space
addresses without allocating new content.

The no-allocation property is already captured by VER-F2 (Σ'.alloc =
Σ.alloc). This distinguishes versioning from INSERT (which allocates fresh
I-addresses) and aligns it with COPY (which references existing ones).

The differences between versioning and transclusion are structural, not
semantic:

| Property             | CREATENEWVERSION           | COPY                     |
|----------------------|----------------------------|--------------------------|
| Creates new document | Yes                        | No (into existing)       |
| Scope                | Entire text content        | Specified span           |
| Link ownership       | Empty (VER2)               | Unchanged in target      |
| Address ancestry     | Encodes parentage (VER3)   | No ancestry relation     |

But at the I-space level, the effect is identical: I-addresses are shared,
not duplicated. A version is, in a precise sense, a document-scoped
transclusion of the source's entire text content into a fresh document.

This equivalence has a derivable consequence. Consider a chain: document A
transcludes from B, and B is versioned to create B'. If some I-address a
appears in both B's and A's arrangement, and B' inherits B's text content
(VER1), then:

    a ∈ img(B.vmap|text) ∧ a ∈ img(B'.vmap)  — by VER1
    a ∈ img(A.vmap) ∧ a ∈ img(B.vmap)          — by the transclusion

All three documents — A, B, and B' — reference the same I-address. Link
discovery (VER9) applies at each: any link touching a is discoverable from
all three. More generally, if d₂ is created by CREATENEWVERSION(d₁), and
d₃ by CREATENEWVERSION(d₂), then by two applications of VER1:

    img(d₃.vmap) ⊆ img(d₂.vmap) ⊆ img(d₁.vmap|text)

at their respective creation times (subsequent edits may narrow these sets).
Content identity propagates through arbitrarily long chains of versioning
and transclusion because I-addresses are the invariant — they do not change
as they pass through operations that share rather than copy.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| PRE-VER | CREATENEWVERSION requires only d ∈ Σ.docs; no ownership restriction | introduced |
| VER0 | version is a fresh document: d' ∈ Σ'.docs ∧ d' ∉ Σ.docs | introduced |
| VER1 | d'.vmap is order-isomorphic to d.vmap\|text via bijection φ preserving I-addresses | introduced |
| VER2 | d'.links = ∅ — version starts with no home links | introduced |
| VER3 | d'.addr = d.addr ∥ s for some s with #s > 0 — sub-address (prefix extension) | introduced |
| VER4 | d'.owner = u — version owned by creating user | introduced |
| VER5 | (A a : a ∈ img(d'.vmap) : d' ∈ Σ'.spanindex(a)) — span index registration | introduced |
| VER-P | d'.parent = d — parentage established at creation | introduced |
| VER-F1 | source document unchanged by CREATENEWVERSION (including d.parent) | introduced |
| VER-F2 | Σ'.ispace = Σ.ispace ∧ Σ'.alloc = Σ.alloc — no content allocation | introduced |
| VER-F3 | all other documents unchanged | introduced |
| VER-F4 | link index unchanged | introduced |
| VER-SCOPE | each editing operation writes to exactly one document's arrangement | introduced |
| VER-ISO | editing one version does not affect any other version's arrangement (theorem from VER-SCOPE) | introduced |
| COR | correspond(d₁, v₁, d₂, v₂) ≡ d₁.vmap(v₁) = d₂.vmap(v₂) — pointwise | introduced |
| VER6 | initial correspondence is bijective (both directions), via φ from VER1 | introduced |
| VER7 | I-addresses underlying correspondence are permanent (durability) | introduced |
| VER8 | link discoverable from any document whose arrangement references the endset I-address | introduced |
| VER9 | discover(d₁, v₁) = discover(d₂, v₂) when d₁.vmap(v₁) = d₂.vmap(v₂) (symmetry) | introduced |
| VER10 | no primitive operation merges two documents relative to a common ancestor | introduced |
| VER11 | no operation's precondition or postcondition references a primary-version designator | introduced |
| Σ.d.parent | d.parent : DocId ∪ {⊥} — parentage as state component | introduced |
| VER12 | parent is functional, well-founded, and acyclic (forest); acyclicity by VER0 + sequential execution | introduced |
| VER13 | parent(d) is permanent once established (follows from frame conditions) | introduced |
| VER14 | each version is independently permanent | introduced |


## Open Questions

What must a version's arrangement contain when the source document includes transcluded content from documents the versioning user cannot read?

Must correspondence computation (SHOWRELATIONOF2VERSIONS) be total — must it find every shared I-address — or is an approximation acceptable?

What invariant must the span index satisfy for FINDDOCSCONTAINING to return complete results across version chains of arbitrary depth?

Must the address ancestry (VER3) hold universally, or may the system place a non-owner's version outside the source document's address subtree?

What consistency must the system guarantee between a version's arrangement and the span index if the version operation is interrupted mid-execution?

When both versions of a document are deleted from their V-space arrangements, what must remain queryable about their former correspondence?

Must royalty accounting decompose correctly across version chains — if A versions B which versions C, and a reader reads A, must the system attribute content to C's original author?
