# ASN-0010: Content Retrieval

*2026-02-24*

We wish to understand what the system must guarantee about returned content.
The question is not how bytes travel from storage to the user — that is
mechanism — but what *relationship* must hold between what was stored and
what is delivered. This relationship must survive transclusion (content
shared across documents), versioning (content viewed through independent
arrangements), and the fundamental split between permanent identity and
mutable position. The retrieval contract is where these architectural
commitments become user-visible promises.

The investigation is motivated by a deceptively simple observation: the
system maintains two address spaces, and the user interacts with only one
of them. Content lives permanently in I-space; documents present content
through V-space arrangements. Retrieval must bridge this gap — resolving
positions in the user's space to content in the system's permanent store —
and the guarantees of retrieval emerge entirely from the properties of this
bridge.


## State Components

We require a minimal model of the state that retrieval observes. Let Σ
denote the system state.

**RΣ1.** Σ.content : IAddr → Byte is a partial function from I-space
addresses to content bytes. The domain dom(Σ.content) is the set of all
allocated I-addresses. We take as given two properties of this function:

- *Permanence*: for any state transition Σ → Σ', dom(Σ.content) ⊆
  dom(Σ'.content). Addresses are never reclaimed.
- *Immutability*: for any transition Σ → Σ' and any a ∈ dom(Σ.content),
  Σ'.content(a) = Σ.content(a). Content at an address never changes.

These are not retrieval properties — they are foundational commitments of
the storage layer. We state them here because retrieval depends on them
absolutely.

**RΣ2.** For each document d, Σ.poom(d) : VPos ⇀ IAddr is the
*arrangement mapping* — a partial function from V-space positions to
I-space addresses. The domain dom(Σ.poom(d)) is the set of positions at
which d currently has content.

We observe that V-positions are not bare natural numbers but tumblers,
carrying hierarchical structure. A document's V-space is conventionally
partitioned into subspaces: the *text subspace* (positions with leading
digit 1, conventionally written 1.x) containing character content, and the
*link subspace* (positions with leading digit 2, conventionally written
2.x) containing link registrations. We write Σ.poom(d)|text and
Σ.poom(d)|link for the respective restrictions.

**RΣ3.** Within the text subspace of a document, V-positions are *dense*:
if positions p and q are both in dom(Σ.poom(d)|text) with p < q, then
every position between them is also in the domain. There are no gaps in the
text subspace. (The link subspace may have sparse occupation, and a gap
always exists between the two subspaces.)

This density property is what makes "the span from position p to position
q" a well-defined retrieval request — every intermediate position maps to
some I-address.


## The Resolution Function

We are now in a position to define retrieval. The definition is the
specification.

**RET0 (Retrieval Resolution).** For document d and V-span S = [p, q)
(where p and q are V-positions with p ≤ q), retrieval is defined as:

    retrieve(d, S) = (++ v : v ∈ S ∩ dom(Σ.poom(d)) : Σ.content(Σ.poom(d)(v)))

where ++ denotes concatenation in ascending V-address order, and the
quantification ranges over all V-positions in the span that are in the
domain of d's arrangement.

This is a *composition*: first, resolve each V-position through the
document's arrangement mapping to obtain an I-address; second, look up the
content byte at that I-address; third, assemble the results in V-order.
The entire retrieval contract flows from this definition and the properties
of the two layers it composes.

We must verify well-definedness. The expression Σ.content(Σ.poom(d)(v))
requires that Σ.poom(d)(v) ∈ dom(Σ.content) — that every I-address in
the arrangement's range actually has content stored at it. This is
referential integrity, the foundational invariant connecting V-space to
I-space:

**RET-RI (Referential Integrity).** For all documents d in the system:

    (A v : v ∈ dom(Σ.poom(d)) : Σ.poom(d)(v) ∈ dom(Σ.content))

We take this as an invariant maintained by every state-modifying
operation. INSERT establishes it for freshly allocated addresses by storing
content before installing the V→I mapping. COPY preserves it because the
source addresses are already in dom(Σ.content) and content permanence
guarantees they remain. CREATENEWVERSION preserves it for the same reason.
DELETE removes V-positions from the domain, which trivially preserves the
universal quantifier.

Under RET-RI, the resolution function is total over its stated domain: for
every v ∈ S ∩ dom(Σ.poom(d)), the composition is well-defined. Retrieval
cannot produce a "dangling reference" error on a well-formed system state.

Nelson captures this concretely: "THE PART YOU WANT COMES WHEN YOU ASK FOR
IT" — the system materialises content on demand from the permanent store,
and the part-pounce model requires that every requested fragment actually
exists.


## Fidelity

The first consequence of RET0 is that retrieval returns the exact bytes
stored at the I-addresses — no transformation, no interpretation, no
encoding.

**RET1 (Byte Fidelity).** For any v ∈ dom(Σ.poom(d)) with Σ.poom(d)(v)
= a:

    the byte returned at position v = Σ.content(a)

This is not a separate property but a direct reading of the definition.
We state it explicitly because its consequences are non-trivial. Fidelity
means the retrieval layer is *transparent* — it adds nothing, removes
nothing, transforms nothing. The bytes that arrive are the bytes that were
stored. Nelson's design intent is explicit: content at an I-address is
immutable and singular, and "native bytes of a document are those actually
stored under its control and found directly in storage under its control;
all other bytes are obtained by front-end or back-end requests to their
home locations."

Fidelity composes with immutability to yield a stronger guarantee:
retrieval of the same I-address at different times returns the same byte.
If Σ.poom(d)(v) = a in state Σ, and the mapping is unchanged in state Σ',
then retrieve returns Σ'.content(a) = Σ.content(a) by immutability. The
returned byte depends only on the I-address, not on when the query is
issued.

We should note that this guarantee is *contractual*, not *cryptographic*.
Nelson explicitly disclaims technical verification of content integrity:
"User acknowledges that all material on the network is stored by users
under similar arrangements to User's own, without verification or
assurance of truth, authenticity, accuracy." The specification promises
fidelity; it does not provide a mechanism to prove fidelity. Trust rests
on the storage vendor franchise, not on bit-level verification.


## Transclusion Transparency

We now examine what happens when content is shared across documents. If
document d₁ contains content natively (allocated by INSERT into d₁), and
document d₂ includes that same content by transclusion (COPY from d₁), do
the two retrievals differ?

The answer is that they cannot. We observe that the resolution function
makes no reference to the *origin* of content — only to its I-address.
Whether Σ.poom(d₁)(v₁) = a because d₁ allocated a, or
Σ.poom(d₂)(v₂) = a because d₂ transcluded content from d₁, is invisible
to the resolution function. Both resolve to Σ.content(a), and the byte
returned is the same.

**RET2 (Transclusion Transparency).** For any documents d₁, d₂ and
positions v₁, v₂ such that Σ.poom(d₁)(v₁) = Σ.poom(d₂)(v₂) = a:

    retrieve(d₁, {v₁}) = retrieve(d₂, {v₂}) = Σ.content(a)

This is a theorem, not an axiom — it follows from RET0 and the fact that
Σ.content is a function (each I-address maps to exactly one byte). Two
documents that share an I-address in their arrangements necessarily yield
the same byte when that address is resolved.

The property is architecturally significant because it is what makes
transclusion meaningful. Nelson's design replaces copying with reference
sharing: "No copying operations are required among the documents throughout
the system, and thus we solve the problems of update." If transcluded
content could diverge from the original, this claim would be hollow. RET2
guarantees that transclusion preserves content identity at the retrieval
level.

Nelson describes the presentation layer for transcluded content: "Bytes
native elsewhere have an ordinal position in the byte stream just as if
they were native to the document. Non-native byte-spans are called
inclusions or virtual copies." The word *virtual* is precise — these are
references, not independent copies. The retrieval layer makes no
distinction between native and transcluded bytes; they occupy sequential
V-positions and resolve to I-addresses by the same mechanism.

Implementation evidence confirms this structurally. When COPY transcludes
content from d₁ into d₂, no new content is written to the permanent store.
The operation writes new V→I mappings into d₂'s arrangement — mappings
that point to the same I-addresses that d₁'s arrangement references. Both
documents' arrangement mappings are independent tree structures, but they
converge on the same I-addresses, and from that point the retrieval path
through the permanent store is identical.


## Self-Transclusion

A special case arises when the same I-address appears at multiple
V-positions within a single document. This can happen through COPY within
the same document — a passage transcluded twice into different positions.

**RET3 (Self-Transclusion Identity).** For document d and positions
v₁ ≠ v₂ with Σ.poom(d)(v₁) = Σ.poom(d)(v₂) = a:

    the byte at v₁ = the byte at v₂ = Σ.content(a)

This falls out of RET0 immediately. The resolution function treats each
V-position independently; each resolves to the same I-address; each yields
the same byte. The two V-positions are "two windows in the same sheet of
glass looking at the same underlying content" and "necessarily show the
same thing."

We note a subtlety confirmed by implementation evidence: when a retrieval
request spans both copies, the results are returned in ascending V-address
order. If v₁ < v₂ and both are within the query span, the byte at v₁
appears first in the output, followed by the byte at v₂. The ordering
guarantee (which we formalise below as RET5) holds regardless of the
I-address pattern — even when I-addresses repeat. The arrangement mapping
is a multimap in such cases (multiple V-positions mapping to the same
I-address), and the retrieval layer handles this by sorting discovered
entries by V-coordinate, regardless of the order in which the arrangement
index reveals them.


## Seamless Assembly

We now consider what happens at the boundaries between arrangement entries.
A document's V-space may map adjacent positions to non-contiguous I-address
ranges — this is typical after content from different sources is composed
into a single document. Position v maps to I-address a₁, and position v+1
maps to I-address a₂, where a₂ ≠ a₁+1. Must the retrieval layer expose
this discontinuity?

**RET4 (Seamless Assembly).** The sequence returned by retrieve(d, S) is a
single contiguous byte sequence with no boundary markers, gaps, or
structural indicators of I-address discontinuity:

    retrieve(d, [p, q)) is a single sequence of (q - p) bytes
    (when [p, q) ⊆ dom(Σ.poom(d)|text))

regardless of how many distinct I-address ranges the arrangement maps
those positions to.

This is the property Nelson calls "materialising" — the system assembles a
coherent result from distributed fragments, but what the user receives is
the materialised whole. "When you 'go to' a certain part of a document,
the whole document is not ready to show; yet the system gives you that part
instantly, materializing it for you from the many fragments of its actual
storage."

Implementation evidence confirms this precisely. The retrieval pipeline
collects one I-span per arrangement entry within the query range, fetches
bytes from the permanent store for each I-span independently, and then
concatenates all consecutive text items into a single output packet. The
wire protocol emits one length field and one byte stream — the caller
receives no indication of the underlying I-address structure.

The I-address non-contiguity is an internal detail of the permanent store.
It remains visible to identity-aware operations (such as version
comparison, which reports shared I-address spans), but it is invisible at
the content-delivery level. This is the separation of concerns that makes
compound documents usable: the reader sees a coherent document, not a
mosaic of fragments.


## V-Order Preservation

Retrieval must return content in the order the document presents it, not
in the order the permanent store organises it.

**RET5 (V-Order).** The bytes in retrieve(d, S) appear in ascending
V-address order:

    for positions v₁ < v₂ both in S ∩ dom(Σ.poom(d)),
    the byte for v₁ precedes the byte for v₂ in the output

This is embedded in RET0's "ascending V-address order" clause, but we
state it separately because its enforcement is non-trivial. The arrangement
mapping is a permutation — it maps V-positions to I-addresses in an order
that need not correspond to I-address order. Content allocated early may
appear late in the document; content from a remote source may appear
between two locally-allocated passages. The retrieval layer must untangle
this permutation and present the result in V-order.

The guarantee holds regardless of the internal structure of the
arrangement index. Whether the index is a B-tree, a skip list, or a sorted
array, the output must be V-sorted. Implementation evidence shows this is
achieved by an insertion-sort during index traversal — discovered entries
are placed into a sorted list by V-coordinate, regardless of the order in
which the tree walk encounters them. The mechanism is implementation-
specific; the guarantee is abstract.


## Precision

When a retrieval request partially overlaps an arrangement entry — say,
requesting V:[p, p+2) when a single entry covers V:[p-3, p+5) — the
system must return only the requested sub-range, not the full entry.

**RET6 (Sub-Range Precision).** For any S' ⊆ S, both subsets of
dom(Σ.poom(d)):

    retrieve(d, S') = the subsequence of retrieve(d, S)
    consisting of bytes at positions in S'

In particular, if [p, q) ⊆ [p₀, q₀) and a single arrangement entry maps
[p₀, q₀) to I-addresses [a₀, a₀ + (q₀ - p₀)), then the retrieval for
[p, q) returns exactly Σ.content(a₀ + (p - p₀)) through
Σ.content(a₀ + (q - p₀) - 1).

This property follows from RET0's per-position resolution: each V-position
is resolved independently, so narrowing the query span simply omits
positions outside it. But the property has architectural significance
because it requires the arrangement mapping to support proportional
slicing within entries. A single arrangement entry maps a V-range to an
I-range with a linear correspondence — advancing one position in V-space
corresponds to advancing one position in I-space. Implementation evidence
confirms this: the clipping arithmetic shifts the I-start by the V-gap
and retracts the I-end by the V-overshoot, returning exactly the
proportional sub-range.


## Version Stability

We now turn to the interaction between retrieval and versioning. When a
version is created from a document, the version captures a snapshot of the
document's text arrangement. We ask: must retrieval from the version
return the same content even after the source document has been edited?

The answer follows from three facts. First, the version has its own
independent arrangement mapping — Σ.poom(d') is distinct from Σ.poom(d).
Second, editing the source document modifies only the source's arrangement
mapping; no operation on one document touches another's arrangement.
Third, the I-addresses that both arrangements reference are in the
permanent, immutable content store.

**RET7 (Version Stability).** Let d' be created by versioning d at state
Σ₀. For any subsequent state Σ (reached by arbitrary operations on d or
other documents):

    retrieve(d', S) in state Σ = retrieve(d', S) in state Σ₀

provided no operations have been performed on d' itself.

*Proof.* Retrieval from d' depends on two things: Σ.poom(d') and
Σ.content. Since no operation has been performed on d', Σ.poom(d') =
Σ₀.poom(d'). Since content is immutable, for all a ∈ ran(Σ₀.poom(d')),
Σ.content(a) = Σ₀.content(a). The composition is unchanged. ∎

This is the property that makes version retrieval exact. Nelson states it
directly: "when you ask for a given part of a given version at a given
time, it comes to your screen." The version's content is frozen at
creation — not because it is copied into a separate store, but because its
arrangement points to immutable content. Later versions "have no special
authority over earlier ones"; supersession links inform the reader that a
newer version exists, but "the older version remains fully retrievable at
its original content."

The transclusion subtlety is worth noting. If version d' transcludes
content from document d₃, and d₃ is later edited, what does d' show? The
answer: d' shows what it showed at creation. The transclusion is stored as
a reference to specific I-addresses, and I-addresses are immutable.
Editing d₃ means creating a new V-space arrangement for d₃; the I-space
bytes that d' references are not affected. Nelson describes a front-end
choice between "time-fixed" and "location-fixed" windows — whether
to show the original content or the current version's equivalent — but
this is a presentation concern. The arrangement itself is fixed.


## Cross-Version Content Identity

A corollary of version stability and transclusion transparency is that
shared content across versions returns identical results.

**RET8 (Cross-Version Identity).** Let d' be a version of d. For any
positions v₁ ∈ dom(Σ.poom(d)) and v₂ ∈ dom(Σ.poom(d')) such that
Σ.poom(d)(v₁) = Σ.poom(d')(v₂):

    the byte at (d, v₁) = the byte at (d', v₂)

This is RET2 specialised to the version case. It is what makes the
correspondence operation meaningful: when the system reports that position
v₁ in d corresponds to position v₂ in d', it is asserting shared
I-address identity, and the user may rely on the content being the same.

Nelson notes that "users may create new published documents out of old
ones indefinitely, making whatever changes seem appropriate — without
damaging the originals." The "without damaging" clause is precisely RET8:
the shared content bytes are identical regardless of how many versions
exist and how they have diverged. The bytes at the shared I-addresses are
the same bytes, accessed through the same permanent store.


## Provenance Separation

Retrieval returns content. It does not return provenance — the information
about where content originated. These are architecturally independent
capabilities served by different operations.

**RET9 (Provenance Separation).** The output of retrieve(d, S) contains
no metadata indicating which bytes are native to d and which are
transcluded from other documents. Provenance is determinable through
separate query operations but is not bundled with content delivery.

Nelson is explicit on both halves. The front end is "unaware" of
I-addresses during normal operation — "the address of a byte in its native
document is of no concern to the user or to the front end; indeed, it may
be constantly changing." At the same time, provenance is always
discoverable: "you always know where you are, and can at once ascertain
the home document of any specific word or character."

The reconciliation is that the "always" and the "unaware" operate at
different layers. The front end does not track I-addresses during
rendering and editing. The user can always query the system to discover
provenance — the capability is always available, but it does not arrive
unbidden.

This separation is a design choice, not a logical necessity. One could
imagine a system that annotates every byte with its origin document. Nelson
explicitly chooses not to: "Note that a quote-link is not the same as an
inclusion, which is not ordinarily indicated." Inclusions appear
seamlessly; quote-windows show boundaries at the front end's discretion.
The principle is: *seamless by default, transparent on demand*.


## Subspace Typing

A document's V-space has two subspaces — text and links — and retrieval
behaves differently for each.

**RET10 (Text Retrieval).** For V-positions in the text subspace, retrieve
returns byte content — the character data stored at the corresponding
I-addresses:

    retrieve(d, S) where S ⊆ dom(Σ.poom(d)|text) yields bytes

**RET11 (Link Retrieval).** For V-positions in the link subspace, retrieve
returns link *identifiers* — the I-space addresses of link structures —
not the internal structure of the link:

    retrieve(d, S) where S ⊆ dom(Σ.poom(d)|link) yields link identities

The link subspace does not store serialised byte content in the same sense
as the text subspace. A link is a structured object — three endsets, each
a set of spans — stored in its own arrangement structure. The link's
V-position in the document records its *presence*; the link's *content*
(its endsets) is accessible only through link-specific query operations.

This asymmetry is architecturally significant. A naive retrieval of the
bounding span of a document — covering both text and link subspaces —
would produce a mixed result: byte content from the text region and link
identifiers from the link region, with a V-space gap between them
containing nothing. Implementation evidence shows that such a bounding-
span retrieval produces type-tagged items (text bytes with one tag, link
addresses with another) rather than a single undifferentiated byte stream.

The consequence for clients is that text and link content should be
retrieved and processed separately. The document's arrangement provides
per-subspace extent information (the span of the text subspace and the
span of the link subspace) precisely to support this separation.


## V-Address Mutability Under Editing

We observe one final property that completes the retrieval picture. After
an editing operation (INSERT, DELETE, REARRANGE) modifies a document's
arrangement, what happens to retrieval at positions that existed before the
edit?

**RET12 (Current-State Resolution).** Retrieval always resolves against the
*current* arrangement mapping. There is no history, no "as of" semantics,
no stale reference:

    retrieve(d, S) in state Σ uses Σ.poom(d)

This has a specific and perhaps surprising consequence for INSERT. When
INSERT at position p shifts existing content to higher positions, the old
V-address p now maps to the newly inserted content. Retrieval at position
p returns the new content, not the content that previously occupied that
position. The original content is still accessible — it has moved to
position p + n (where n is the insertion length) — but the old address no
longer reaches it.

    if Σ.poom(d)(p) = a  and  INSERT(d, p, text) → Σ'
    then Σ'.poom(d)(p) = a'  (the fresh I-address for text[0])
    and  Σ'.poom(d)(p + n) = a  (the old content, shifted)

V-addresses are *coordinates in a mutable space*, not stable identifiers.
I-addresses are the stable layer. This duality is the whole point of
maintaining two address spaces: V-space absorbs the impact of editing,
while I-space provides the permanence that survives it.

The implication for system users is clear. If you need to retrieve the
*same content* after edits, you must track it by I-address (or by a
version snapshot that freezes the arrangement). If you retrieve by
V-address, you get whatever currently occupies that position — which may
be different after any editing operation.


## Retrieval as Pure Query

We close with the frame condition for retrieval itself.

**RET-F (Retrieval Frame).** Retrieval modifies no component of the system
state:

    retrieve(d, S) : Σ → Σ  (identity on state)

Retrieval is a pure function from state and query parameters to a byte
sequence. It creates no new addresses, modifies no arrangement, updates no
index. The system state before and after a retrieval is identical.

This is architecturally important because it means retrieval operations are
freely composable. Any number of concurrent retrievals can execute without
interfering with each other or with the system state. The content they
observe is the content at their respective I-addresses, which is immutable.
Two concurrent retrievals of the same V-span from the same document must
return the same result — not as a concurrency guarantee (which is an
implementation concern) but as a logical necessity: they evaluate the same
function on the same arguments.


## Summary of the Argument

The retrieval contract is remarkably simple in structure. It is the
composition of two functions: a mutable, per-document arrangement mapping
(V→I) and an immutable, global content store (I→Byte). The properties of
retrieval all follow from this composition:

- *Fidelity* follows because the composition adds nothing.
- *Transparency* follows because the composition does not inspect origin.
- *Seamlessness* follows because the composition iterates over V-order,
  not I-order.
- *Precision* follows because the composition resolves each position
  independently.
- *Version stability* follows because the arrangement is independent per
  document and the content is immutable.
- *Provenance separation* follows because the composition discards the
  I-address after fetching the byte — the user receives content, not
  addresses.

The entire specification rests on one invariant (RET-RI, referential
integrity), one definition (RET0, the resolution function), and the
foundational properties of the two address spaces (permanence,
immutability). Everything else is theorem.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| RΣ1 | Σ.content : IAddr → Byte; permanent and immutable | introduced |
| RΣ2 | Σ.poom(d) : VPos ⇀ IAddr; per-document arrangement mapping | introduced |
| RΣ3 | Text subspace of Σ.poom(d) is dense (no gaps between occupied positions) | introduced |
| RET0 | retrieve(d, S) = (++ v : v ∈ S ∩ dom(Σ.poom(d)) : Σ.content(Σ.poom(d)(v))) | introduced |
| RET-RI | (A v : v ∈ dom(Σ.poom(d)) : Σ.poom(d)(v) ∈ dom(Σ.content)) — referential integrity | introduced |
| RET1 | Byte fidelity: the byte returned at position v is Σ.content(Σ.poom(d)(v)) | introduced |
| RET2 | Transclusion transparency: shared I-address ⇒ identical bytes across documents | introduced |
| RET3 | Self-transclusion identity: same I-address at distinct V-positions ⇒ same byte | introduced |
| RET4 | Seamless assembly: retrieval produces a single contiguous byte sequence regardless of I-address discontinuity | introduced |
| RET5 | V-order: output is in ascending V-address order | introduced |
| RET6 | Sub-range precision: retrieve(d, S') for S' ⊆ S returns exactly the subsequence at S' | introduced |
| RET7 | Version stability: retrieval from an unmodified version is constant across all subsequent states | introduced |
| RET8 | Cross-version identity: shared I-address across versions ⇒ identical byte | introduced |
| RET9 | Provenance separation: retrieval returns content only, not origin metadata | introduced |
| RET10 | Text retrieval: text-subspace positions yield byte content | introduced |
| RET11 | Link retrieval: link-subspace positions yield link identifiers, not link structure | introduced |
| RET12 | Current-state resolution: retrieval uses the arrangement mapping at query time | introduced |
| RET-F | Retrieval frame: retrieval modifies no system state | introduced |


## Open Questions

What must a system guarantee about retrieval when the storage vendor holding the I-space content for a transcluded span is unreachable — must it fail atomically or may it return partial results?

Must retrieval of a span that crosses the text/link subspace boundary produce a well-typed result, or is such a query malformed by precondition?

If multiple versions of a document share a V-position range with different I-address mappings, what must a correspondence query guarantee about the relationship between the two retrieval results?

Does retrieval carry any obligation regarding the ordering of link identifiers in the link subspace — must they appear in creation order, or is any order satisfying V-address ordering acceptable?

When a document's arrangement is modified concurrently with a retrieval, must the retrieval observe a consistent snapshot, or may it reflect a partially-updated arrangement?

What must retrieval guarantee about content whose storage rental has expired — must the system distinguish between "content exists but is unpaid" and "content does not exist"?

Must the retrieval of a V-span that extends beyond the document's current extent return a truncated result, or is such a query an error?
