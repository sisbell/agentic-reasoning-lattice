# ASN-0104: The RETRIEVEV Operation

*2026-06-04*

We wish to understand what it *means* to read a fragment of content from
the docuverse by its address. The question sounds trivial — surely reading
is just looking something up — but the design hangs a great deal on this
single act. Nelson isolates content delivery into exactly one operation:
"Of the 17 current commands in XU.87.1, only one command (RETRIEVEV) is
concerned with delivery of the actual content fragments." Every other
retrieval hands back *references* — spans, link identities, document lists.
RETRIEVEV is the one place where the system crosses the line from naming
content to *delivering* it. So whatever the read contract is, it is the
contract for the entire system's relationship between stored identity and
delivered material.

We are not interested in how bytes travel from storage to caller; that is
mechanism. We are interested in the *relationship* the read must maintain:
between the address the caller presents and the content the caller
receives, between two reads of the same address separated in time, and
between the act of reading and the state of the fragment read. The read is
correct not because of what it does but because of what it leaves
invariant.

We take as foundation the strand model of ASN-0036 and its extension in
ASN-0047. The content store `Σ.C : T ⇀ Val` is a partial function from
tumbler addresses to content values, with domain `dom(Σ.C)` the set of
allocated I-addresses (`Σ.C`, S0–S4). For each document `d`, the
arrangement `Σ.M(d) : T ⇀ T` maps V-position tumblers to I-addresses
(`Σ.M(d)`, S2, S3). The two are bridged by the foundational guarantees we
will lean on absolutely: content is immutable and the store is monotone
(S0, S1), the arrangement is single-valued (S2), and every active V-position
maps to an address that actually holds content — referential integrity
(S3). `Val` is an opaque codomain; in the implementation it is the byte
alphabet, one byte per element-level I-address, but the read contract never
inspects its structure.

## What is delivered: content, not a reference

The first thing to fix is *what comes back*. Nelson is explicit that
RETRIEVEV "returns the material (text and links) determined by `<spec
set>`" — the actual content, materialized on demand. He calls this pounce:
"THE PART YOU WANT COMES WHEN YOU ASK FOR IT." Gregory's implementation
confirms the abstract shape: the resolved address indexes the content store
and the stored value is copied out verbatim, by raw byte move, with no
transformation. So the result of a read is an element of `Val` (or its
absence), never a tumbler.

We name the codomain of the operation. Let `Val⊥ = Val ∪ {⊥}`, where `⊥`
denotes *no content delivered*, and where `⊥ ∉ Val` — the sentinel is a
fresh element disjoint from every content value, not some distinguished
member of `Val`. This disjointness is load-bearing: several claims below
read off "the result is `⊥`" or "the result is not `⊥`" to decide whether
content was delivered, and that decision is meaningful only because no
content value can equal `⊥`. We will see that `⊥` is a legitimate,
designed-for result, not an error.

We are looking for a function `retrieve` of the state and a *specification*.
A specification is the address the caller presents. Two forms exist, and the
distinction between them is the spine of this note.

## Deriving the operation by working backward

Take the simplest form first: the caller presents an I-address `a ∈ T`
directly. We want a procedure `r := retrieveI(Σ, a)` establishing the
postcondition

> `R0 : (a ∈ dom(Σ.C) ∧ r = Σ.C(a)) ∨ (a ∉ dom(Σ.C) ∧ r = ⊥)`.

This `R0` is total — it prescribes a result for *every* address, whether
populated or not. The guarded command

```
if a ∈ dom(Σ.C) → r := Σ.C(a)  []  a ∉ dom(Σ.C) → r := ⊥ fi
```

has `wp(·, R0) = true`: the guards are exhaustive and the assignment in each
branch matches the corresponding disjunct of `R0`. Well-definedness of the
first branch requires only that `Σ.C(a)` be defined, which its guard
supplies. Nothing else is needed. The read by identity asks one question of
one partial function.

Now the form the caller usually presents: a *V-spec* `(d, v)` — a document
together with a V-position. The read must resolve the position to an
address before it can resolve the address to content. We want
`r := retrieveV(Σ, d, v)` establishing

> `R1 : (v ∈ dom(Σ.M(d)) ∧ r = Σ.C(Σ.M(d)(v))) ∨ (v ∉ dom(Σ.M(d)) ∧ r = ⊥)`.

The guarded command resolves V then I:

```
if v ∈ dom(Σ.M(d)) → r := retrieveI(Σ, Σ.M(d)(v))
[] v ∉ dom(Σ.M(d)) → r := ⊥
fi
```

Here we must discharge a well-definedness obligation that did not arise for
the direct read. In the first branch we call `retrieveI` on `Σ.M(d)(v)`. For
`R1` to hold we need that inner call to deliver `Σ.C(Σ.M(d)(v))` and not
`⊥` — that is, we need `Σ.M(d)(v) ∈ dom(Σ.C)`. This is *exactly* what
referential integrity (S3) guarantees: `v ∈ dom(Σ.M(d)) ⟹ Σ.M(d)(v) ∈
dom(Σ.C)`. Without S3, a V-read could resolve to a dangling address and the
first branch would silently degrade to `⊥`. With S3, it cannot. We record
this as the dangling-freedom property:

> `R2 : retrieveV(Σ, d, v) = ⊥ ⟺ v ∉ dom(Σ.M(d))`.

The read returns nothing *only* when the position is unoccupied — never
because a live position pointed at vanished content. The single-valuedness
of `Σ.M(d)` (S2) is what makes `Σ.M(d)(v)` denote a unique address, so the
resolution is a function and not a relation; without S2, `retrieveV` would
not be well-defined as a function at all. So two foundation invariants are
load-bearing for the V-read to even be a function with a deterministic
result: S2 (uniqueness of resolution) and S3 (no dangling resolution).

We collect the composite shape: where it does not yield `⊥`,

> `retrieveV(Σ, d, v) = (Σ.C ∘ Σ.M(d))(v)`.

Reading by position is the composition of the arrangement map with the
content map. This composition is the whole bridge between the user's V-space
and the system's permanent I-space.

## The read changes nothing

Both procedures are *pure queries*. Neither appears with an effect on `Σ`;
the frame of each is total:

> `R3 (non-destruction) : retrieve leaves every component of Σ unchanged —
> dom(Σ.C), Σ.C, and Σ.M(d) for every d are identical before and after.`

Nelson insists on this: the store is append-only and "Content is immutable —
it never changes after creation," so there is no mechanism by which a read
could mutate what it reads. Even an explicit DELETE does not remove bytes
from the store (it edits an arrangement); a non-destructive read certainly
cannot. Gregory confirms the read path performs only lookups and a copy-out.
A fragment is, in Nelson's phrase, *summoned, never spent*.

Two consequences follow immediately. First, reading is *idempotent over
state*: performing `retrieve` and then `retrieve` again leaves `Σ` as it was
and yields the same result both times — there is no first-read/second-read
distinction. Second, an arbitrary number of callers may read the same
fragment concurrently or in sequence with no interference, because none of
them perturbs the state the others observe.

(We note one effect the abstract model deliberately omits. Nelson's economic
layer increments a usage counter on delivery — "a royalty on every byte
transmitted." That counter is a separate state component, external to the
content fragment; it does not appear in `Σ = (C, M, …)` here, and on the
fragment itself the read has no effect. An accounting model would add it as a
disjoint component; it would not weaken R3 over the content state.)

## Permanence and immutability of what is delivered

We can now state the guarantee that gives the read its value: *the same
address, read at two different times, delivers the identical content.* This
is the formal content of Nelson's permanence promise, and it belongs to the
I-address, derived directly from store immutability.

> `R4 (read determinacy across time) : for any reachable transition sequence
> Σ →* Σ' and any a ∈ dom(Σ.C),  retrieveI(Σ', a) = retrieveI(Σ, a).`

*Proof.* By store monotonicity (S1), `dom(Σ.C) ⊆ dom(Σ'.C)`, so `a ∈
dom(Σ'.C)`; both readers take the first branch of `R0`. By content
immutability (S0b), `Σ'.C(a) = Σ.C(a)`. Hence both deliver the same value.
∎

R4 is the load-bearing invariant of the whole system stated as a read
property. It is what Nelson means when he says an I-address "will always
return that exact content." We stress two boundaries on it.

First, R4 is a guarantee about *identity addresses*, not *positions*. The
V-read carries no such guarantee:

> `R5 (V-read is not time-invariant) : there exist states Σ →* Σ', a
> document d, and a position v with v ∈ dom(Σ.M(d)) ∩ dom(Σ'.M(d)) and
> retrieveV(Σ, d, v) ≠ retrieveV(Σ', d, v).`

This is unavoidable and intended: editing rearranges the V→I mapping, so
"position 5 of this document" may resolve to different content after an
insertion or reordering, even though every underlying byte is immutable at
its I-address. Nelson: "The address of a byte in its native document is of
no concern to the user or to the front end; indeed, it may be constantly
changing." The permanence guarantee attaches to identity, which is why links
and durable references seize I-addresses and not V-positions.

Second, R4 is an immutability guarantee *by construction of the model*, not
a tamper-detection guarantee. Nelson is candid that the system provides "no
verification or assurance" cryptographically — the invariant rests on the
honesty of the storage layer, not on hashing or signing. An alternative
implementation must *maintain* S0; the abstract specification cannot compel
it to *prove* it maintained it. We take S0 as a modeling assumption and
inherit R4 from it; detection of its violation is out of scope.

A corollary of R4 worth isolating is permanent readability:

> `R6 (permanent readability) : once a ∈ dom(Σ.C), then in every later state
> Σ', a ∈ dom(Σ'.C) and retrieveI(Σ', a) = Σ.C(a) ≠ ⊥.`

A fragment, once readable by its identity, is readable forever, with an
unchanging result. There is no expiry, no eviction from the abstract store,
no second read that fails where the first succeeded.

## The read by identity is independent of every arrangement

The two specification forms expose a structural fact: `retrieveI` consults
`C` alone and never touches any `M(d)`. This means the readability of a
fragment by its I-address is wholly independent of whether any document
currently arranges it.

> `R7 (arrangement-independence of identity read) : retrieveI(Σ, a) depends
> only on Σ.C. In particular, if a transition removes v from dom(Σ.M(d))
> with Σ.M(d)(v) = a, then retrieveI(Σ', a) = retrieveI(Σ, a).`

*Proof.* `retrieveI` is defined by `R0` purely in terms of `dom(Σ.C)` and
`Σ.C`. An arrangement contraction changes only `M(d)`; by P0/S0 it leaves
`C` and `dom(C)` untouched, so `a ∈ dom(Σ'.C)` and `Σ'.C(a) = Σ.C(a)`. ∎

This is the abstract content of the "deleted-but-permanent fragment":
removing content from a document's arrangement (the only thing DELETE does)
strands the V-position but not the bytes. A caller who still holds the
I-address `a` reads the original content unchanged. Reachability *through a
document* is lost; reachability *by identity* is not. The two reads diverge
precisely because one consults `M` and the other does not — which is why the
design exposes both.

## The read is total: naming nothing is not an error

We deliberately made `R0` and `R1` total, prescribing `⊥` rather than
failure when an address holds no content. This is not laxity; it is Nelson's
ghost-element principle made into a read postcondition. "Things may be
addressed even though nothing is there to represent them in storage… It is
possible to link to a node, or an account, even though there is nothing
stored." A well-formed address is always a legitimate *question*, whether or
not anything answers it. The address space is an abstract coordinate system;
occupancy is sparse and dynamic; asking about an empty coordinate must yield
emptiness, not an exception.

> `R8 (totality) : retrieveI and retrieveV are total. For every Σ, every a ∈
> T, and every (d, v), the result is defined and lies in Val⊥; it equals ⊥
> exactly when the addressed coordinate is unpopulated.`

One sharp consequence: the empty result carries *no diagnostic content*. A
caller receiving `⊥` from `retrieveV(Σ, d, v)` cannot tell from the result
alone whether the position was never occupied, was occupied and then
cleared, or denotes a zero-width request. All collapse to the same `⊥`.
Gregory confirms the implementation makes exactly this conflation — a gap
read and a zero-width read are indistinguishable at the protocol level, both
returning success with an empty item set. If a future design needs to
distinguish "absent" from "present but empty," it must enrich `Val⊥` with
distinct sentinels; the present contract does not.

## Transclusion transparency

Because the value delivered depends only on the resolved I-address, two
reads that resolve to the *same* address deliver the *same* content,
regardless of which document or position each came through.

> `R9 (transclusion transparency) : if Σ.M(d₁)(v₁) = Σ.M(d₂)(v₂) = a, then
> retrieveV(Σ, d₁, v₁) = retrieveV(Σ, d₂, v₂) = Σ.C(a).`

*Proof.* Both V-reads take their first branch (both positions are in their
arrangements' domains) and compose to `Σ.C(a)` by definition. ∎

This is what makes transclusion *inclusion by reference* rather than
copying. The shared content is one fragment with one identity; appearing in
many arrangements does not duplicate it, and reading it through any
arrangement reaches the same immutable bytes. By origin-based identity (S4),
two fragments that merely *look alike* but were created independently carry
distinct addresses and are distinct reads; only genuinely shared identity
produces R9's equality. The read path is identical whether the content was
natively inserted into `d` or transcluded into it — the arrangement records a
V→I mapping in both cases, and the read does not and cannot distinguish how
that mapping arose.

## Opacity: the value is delivered verbatim

Finally, the read interprets nothing. The result is the stored value
unchanged.

> `R10 (verbatim delivery) : the result is drawn from {Σ.C(a), ⊥}; retrieve
> applies no transformation to Σ.C(a) before delivering it.`

`Val` is an uninterpreted codomain. An alternative implementation must
deliver the stored element as stored; it may not normalize, re-encode, or
validate it. Gregory's implementation makes this concrete and stark: content
is moved out by a raw byte copy with no character-boundary awareness, so a
sub-fragment read that begins or ends inside a multi-byte encoded character
delivers the fractured byte sequence as-is. That fracturing is an
*implementation observation* about sub-element granularity — the
implementation assigns one byte per element-level address, and any encoding
discipline is the caller's responsibility — not an abstract claim. The
abstract claim is only R10: whatever the unit of `Val`, it is delivered
without interpretation.

## What the caller must know to ask

We can now answer the access half of the question precisely, in terms of the
two specification forms.

To read by **identity**, the caller must possess the I-address `a`.
Possession of `a` is *necessary* (the read is keyed on it) and, modulo the
access policy noted below, *sufficient*: by allocation permanence (T8, S1)
the address, once allocated, remains a valid key in every future state, so
the caller's knowledge of `a` never goes stale. R6 then guarantees the read
succeeds with a fixed result forever. The identity read requires nothing
about any document's state — in particular it does not require the document
to be "open."

To read by **position**, the caller must possess the V-spec `(d, v)` and the
document `d` must be in a state where its arrangement is consultable. The
V-position is ephemeral (R5) and meaningful only relative to `d`'s current
arrangement.

Crucially, the caller need **not** have known the precise address in
advance. Nelson separates *delivery* (which consumes an address) from
*discovery* (which produces one): a fragment may be reached by containment,
by relationship, or by content, and the precise address is the *output* of
reaching it, which RETRIEVEV then consumes. The address is a prerequisite of
*delivery*, not of *reaching*. (The discovery operations that produce
addresses are out of scope for this note.)

Two boundaries on "sufficient" deserve flagging, both observations rather
than claims of this note. First, in Nelson's design an address is a
permanent *name*, not a bearer capability: for published content, possessing
the address grants read access; for private content, access is restricted to
the owner and associates, and the address alone is not a key — though Nelson
notes the prototype did not yet enforce this. Second, R4's bit-for-bit
promise is contractual, not cryptographic, as discussed above. Both concern
an authorization/verification layer this content-read contract does not
model.

## Implementation observations

These ground the abstract claims but are not themselves abstract — an
alternative implementation could satisfy R0–R10 by other means.

- The operation registered as `RETRIEVEV` resolves a V-spec to I-spans
  through the per-document arrangement (POOM), then indexes the content store
  (granfilade) by those I-spans, copying bytes out by `memmove`. This is the
  `Σ.C ∘ Σ.M(d)` composition realized as POOM-lookup followed by
  granfilade-lookup.
- The same operation accepts a *raw I-span* specification that bypasses the
  arrangement lookup entirely and indexes the content store directly. This is
  the concrete witness for `retrieveI` and for R7: it requires no document to
  be open and reaches deleted-but-permanent content by identity.
- The V-keyed path additionally requires the document to be open in the
  caller's access list before the arrangement is consulted; the I-keyed path
  imposes no such precondition. This realizes the asymmetry in "what the
  caller must know."
- Content granularity is one byte per element-level address, so `Val` is the
  byte alphabet and `vspan_width` equals byte count; sub-fragment reads clip
  by byte offset, producing the encoding-fracture behavior noted under R10.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| R0 | `retrieveI(Σ, a)` is total: yields `Σ.C(a)` if `a ∈ dom(Σ.C)`, else `⊥` | introduced |
| R1 | `retrieveV(Σ, d, v)` yields `Σ.C(Σ.M(d)(v))` if `v ∈ dom(Σ.M(d))`, else `⊥` | introduced |
| R2 | `retrieveV(Σ, d, v) = ⊥ ⟺ v ∉ dom(Σ.M(d))` (no dangling resolution; rests on S3) | introduced |
| R3 | `retrieve` is a pure query — it leaves every component of Σ unchanged (non-destruction, idempotent over state) | introduced |
| R4 | For `Σ →* Σ'` and `a ∈ dom(Σ.C)`, `retrieveI(Σ', a) = retrieveI(Σ, a)` (read determinacy across time) | introduced |
| R5 | The V-read is not time-invariant: a fixed `(d, v)` may deliver different content across states | introduced |
| R6 | Once `a ∈ dom(Σ.C)`, `retrieveI` succeeds with an unchanging result in every later state (permanent readability) | introduced |
| R7 | `retrieveI(Σ, a)` depends only on `Σ.C`; arrangement contraction does not affect it (arrangement-independence) | introduced |
| R8 | `retrieveI` and `retrieveV` are total over Val⊥; `⊥` denotes an unpopulated coordinate, not an error | introduced |
| R9 | If `Σ.M(d₁)(v₁) = Σ.M(d₂)(v₂) = a`, both V-reads deliver `Σ.C(a)` (transclusion transparency) | introduced |
| R10 | The result is drawn from `{Σ.C(a), ⊥}`; no transformation is applied (verbatim delivery) | introduced |
| Val⊥ | `Val⊥ = Val ∪ {⊥}`, the codomain of the read | introduced |

## Open Questions

What must the system guarantee about a read when the addressed content is native to another server, so that resolution by identity remains well-defined across the home-location boundary?

Under what conditions may possession of an address confer read authorization, and what invariant must the access-control layer maintain so that authorization tracks content identity rather than position?

What invariant must hold for an aggregate read over a span of positions to equal the position-wise composition of single-fragment reads, when the span's endpoints are fixed by identity rather than by current position?

What must a read guarantee about the relationship between a delivered fragment and its origin attribution, given that origin is determined by identity and is invariant under arrangement editing?

What must the system guarantee to let a reader independently confirm that delivered bytes match the content originally stored at an address, given that the present immutability guarantee is contractual rather than verifiable?
