# ASN-0109: The RETRIEVEENDSETS Operation — Reading a Link by Its Address

*2026-06-04*

We are looking at a link that already exists at some address `a`, and we wish to
understand a single operation upon it: reading its endsets *directly*, by `a`,
without traversing anywhere. Nelson calls the operation RETRIEVEENDSETS; its
verbatim definition is terse — "This returns a list of all link end-sets that are
in `<spec set>`" (LM 4/70). The terseness hides three distinct questions, and our
task is to separate them. *What* does the read return? *What does the reader learn
about the relationship* that the link records — over and above the bare fact that
two pieces of content are connected? And *what invariants govern* the answer, so
that the read can be trusted: can the system ever report an endpoint the link does
not hold, and can two reads of the same link disagree?

Throughout we lean on the link model's vocabulary. A link value is a finite
sequence of endsets, `Link = (e₁, …, eₙ)` with `N ≥ 3` and each `eᵢ ∈ Endset`,
where `Endset = 𝒫_fin(Span)` is a finite set of well-formed spans (the type slot,
`e₃`, non-empty). The link store `Σ.L : T ⇀ Link` maps addresses to link values.
For an endset `e` we write `coverage(e) = (∪ (s, ℓ) : (s, ℓ) ∈ e : ⟦(s, ℓ)⟧)` for
the set of addresses it names, and we use the field-projection `home(a) =
N(a).0.U(a).0.D(a)` that recovers a document-level prefix from any address carrying
a document field. These are taken from the foundations; we add nothing to them. We
add only the operation that reads them.

## The operation

We specify the read as a pure function of the state.

> **READENDSETS** `: Σ × T ⇀ Link`.
> *Precondition.* `a ∈ dom(Σ.L)`.
> *Result.* `READENDSETS(Σ, a) = Σ.L(a)`.
> *Frame.* `Σ' = Σ`; the operation consults only `Σ.L(a)`.

The entire content of the operation is the equation `READENDSETS(Σ, a) = Σ.L(a)`,
and almost everything we want to prove is a consequence of taking that equation
seriously. Let us extract the consequences one at a time.

## What is returned, and why the report cannot lie

The first and deepest property is that the read *cannot report endpoints the link
does not hold* — and equally cannot omit endpoints it does hold. One is tempted to
phrase this as a consistency obligation between a stored "truth" and a returned
"report." But there is no such pair to keep in agreement. The link's endsets are
not a description of the link that lives somewhere else and might drift; they *are*
the link. `Σ.L(a)` is the only representation of what `a` connects. The weakest
precondition makes this exact: for any candidate result `R`,

  `wp(READENDSETS(·, a), result = R) ≡ a ∈ dom(Σ.L) ∧ Σ.L(a) = R`.

There is no second store to consult, no cache to invalidate, no projection that
could supply a span absent from `Σ.L(a)` or suppress one present in it. We record
this as faithfulness.

- **(E0) ReadDeterminacy.** READENDSETS is a total function on `{a : a ∈ dom(Σ.L)}`,
  and `READENDSETS(Σ, a) = Σ.L(a)`.

- **(E1) Faithfulness.** Writing the result as `(e₁, …, eₙ)`, we have `eᵢ =
  Σ.L(a).eᵢ` for every slot `i`. Consequently the read can neither *over-report* —
  for every span `σ` appearing in returned slot `i`, `σ ∈ Σ.L(a).eᵢ` — nor
  *under-report*: every `σ ∈ Σ.L(a).eᵢ` appears in returned slot `i`. There is no
  third possibility, because returning `Σ.L(a)` is the operation's definition.

Faithfulness is the abstract residue of what one might have feared needs a locking
discipline or a read-consistency protocol. No such machinery is required at the
level of the operation: the question "is the report consistent with what is stored?"
is ill-posed, since the report *is* what is stored. Any alternative implementation
that stores the link's connective information in exactly one place inherits E1 for
free; an implementation that maintained a separate summary would have to *add* an
invariant to recover what E1 gives by construction.

## The shape of the return: three endsets, each a set of spans

Faithfulness fixes *what* comes back; the structure of `Link` fixes its *shape*.

- **(E2) TernaryStructure.** The result has arity `N ≥ 3`. Slot 1 is the
  *from-set*, slot 2 the *to-set*, slot 3 the *type-set*; further slots, when
  present, are additional endsets. The type-set is non-empty. Each slot is an
  `Endset`, hence a finite set of spans, and the slots are positionally
  distinguishable: the read does not return an unordered heap of endpoints but a
  structure in which "from," "to," and "type" are separable.

The read therefore answers a richer question than "where does this connect?" It
returns *what kind of structure the connection is* — directional content on one
axis, categorical content on another. We must be careful, though, about what each
returned span *is*. A content endpoint is never a point.

- **(E3) SpanSetGranularity.** Every returned endset `eᵢ` is a span-set, and each
  span is boundary-defined: a start tumbler together with a width (T12). The read
  thus returns, for each connected region, its *precise boundaries* — start and
  extent — and the content lying between those boundaries is implicit in the choice
  of endpoints, not enumerated. Because an endset is an *arbitrary* finite set of
  spans, a single end may be *discontiguous*: `|eᵢ| > 1`, with its spans possibly
  resident in several distinct documents. The read returns *all* of them.

This is Nelson's "broken, discontiguous set of bytes" (LM 4/42) made precise: one
end of a link is a span-set, and reading the endset hands back the whole set, not a
representative member.

## Directionality: structural roles, open semantics

The from/to split of E2 carries directional information, but only structurally.

- **(E4) DirectionalRoles.** Slots 1 and 2 carry the from/to designation as a
  property of *position* within the link value. The read returns this position
  faithfully, but the *meaning* of "from" and "to" is not fixed by the read or by
  the link mechanism; it is supplied by the link's type and the user's convention.
  The model permits a degenerate one-sided link, in which one of `e₁, e₂` is the
  empty endset (`Endset` admits `∅`); for such a link the source/destination
  framing does not apply, and the read returns an empty directional slot rather than
  inventing a counterpart.

So the reader of a link learns *which side is structurally first* and *which
second*, and nothing more about source-versus-destination than the type permits.
The directional roles are real but semantically mute on their own — which is exactly
why the third endset matters.

## The type endset: meaning by address, and the ghost

What distinguishes a citation from a refutation from a comment, when all three may
connect the very same two regions? Not the from/to pair, which is identical across
them, but the type endset.

- **(E5) TypeByAddressReturn.** The read returns the type endset `e₃`, whose
  `coverage` records the relationship's *kind*. The kind is carried by the
  *identity of the addresses* in `coverage(e₃)`, matched by convention; the read
  does *not* dereference those addresses, and imposes no requirement that content be
  stored at them. Hence `coverage(e₃)` may include *ghost* addresses — addresses in
  `T` lying outside `dom(Σ.C) ∪ dom(Σ.L)` (ghost types are permitted by the link
  model). Two links share a type exactly when their type endsets have equal
  coverage, and this is decidable from the returned endsets alone.

The type endset is the first thing reading reveals that *following* a link cannot.
One can follow a link to its from- or to-content and arrive somewhere. One cannot
follow a link "to its type," because the type's address need not have anything
stored at it — there is no destination to arrive at. The relationship's *meaning* is
legible only by reading `e₃`'s address and never by traversing it.

## Stable identity, and why two reads agree

Reading must name content the same way every time, or the operation is worthless.
The guarantee comes for free from immutability of the stored value.

- **(E6) ReadInvariance.** Let `Σ →* Σ'` be any reachable evolution with `a ∈
  dom(Σ.L)`. By link immutability, `Σ'.L(a) = Σ.L(a)`; therefore
  `READENDSETS(Σ', a) = READENDSETS(Σ, a)`. The same link read at two different
  times returns the *same* endsets — the same spans, the same coverage —
  *regardless of any editing performed between the reads*, because READENDSETS
  consults only `Σ.L(a)` and never consults the arrangement family `Σ.M`.

The endsets name content by *address-identity* — positions on the permanent address
space — not by where that content currently sits in any document. Identity cannot
drift; positions can. The whole survivability story reduces, at the level of this
operation, to the observation that READENDSETS reads the identity layer and is
blind to the position layer. There is nothing for an edit to perturb.

It is worth pausing on the asymmetry this creates between editing and the read. An
edit to a connected document changes `Σ.M`, never `Σ.L(a)`. The read returns
`Σ.L(a)`. Therefore *editing cannot invalidate the read* — the endsets remain
exactly readable, span for span, after any deletion, insertion, or rearrangement of
the content they name. The link survives editing because the read of it does not
look where editing acts.

## Participant disclosure: naming documents the reader has never seen

A returned endset is a set of spans, and a span names its document by construction.

- **(E7) ParticipantDisclosure.** Define the participants of `a` as the set of
  document-level prefixes appearing in any returned span:

    `participants(a) = { home(s) : (s, ℓ) ∈ Σ.L(a).eᵢ, 1 ≤ i ≤ N, s carries a document field }`.

  Reading the endsets discloses every member of `participants(a)`, because the
  document field of each span's start address is *inside the address the read
  returns* and is recoverable from it by field projection alone — no further lookup.
  This holds whether or not the reader has ever encountered those documents.

There is no "summary" form of an endset that hides its participants; the
participants *are* the endset. A from-set touching three authors' works names all
three the moment it is read. We must, however, distinguish identity from content.
What the read discloses is *which* documents and *which* spans participate — their
addresses. It does not deliver their bytes: fetching content is a separate operation
(out of scope here). So a reader can learn that document `X` participates in a
relationship without thereby being able to read `X`.

## What reading reveals that following never could

We can now collect the difference between the two ways of interrogating a link.
Following privileges one direction and lands at one place; reading inspects the
whole object. Three things are visible only to the read.

- **(E8) RevelationBeyondTraversal.** From `READENDSETS(Σ, a)` the reader learns,
  and from arriving at any single endpoint the reader does *not* learn: (i) the
  *discontiguity* of each end — that a connection touches several non-adjacent spans
  as siblings of one endset (E3); (ii) the *type* — the relationship's kind, carried
  by `e₃`'s address, which has no destination to be followed to (E5); and (iii) the
  *link as a unit* — an owned, `N`-ary object with a home document `home(a)` and
  every endset laid out together, rather than a one-way arrow. Traversal collapses
  this structure to the single span it happens to reach; the read preserves it.

## The resolution layer, and where attrition lives

E6 says the *stored* endsets are immutable. But a reader frequently wants not the
permanent identity of the named content, only *where it currently sits* — its
positions in some present arrangement. This is a derived projection, and it is the
only place where partiality enters. We define it, and bound it.

> For an endset `e` and the arrangement family of state `Σ`, the **resolution** of
> `e` is
>
>   `res(Σ, e) = { (d, v) : d ∈ dom(Σ.M), v ∈ dom(Σ.M(d)), Σ.M(d)(v) ∈ coverage(e) }`,
>
> and its *resolved identity* is `resolved(Σ, e) = { Σ.M(d)(v) : (d, v) ∈ res(Σ, e)
> } = coverage(e) ∩ (∪ d : d ∈ dom(Σ.M) : ran(Σ.M(d)))`.

- **(E9) ResolutionAttrition.** `resolved(Σ, e) ⊆ coverage(e)`. A named address that
  no current arrangement places — content deleted from every version, or never
  arranged — contributes *nothing* to the resolution and is silently absent from it.
  Hence the resolution of an endset may be *partial*, or *empty* even when
  `coverage(e) ≠ ∅` (a "ghost link," whose stored endsets are intact yet resolve to
  nothing). The bound is one-directional: resolution can only *shrink* relative to
  the named identity as arrangements lose positions; it can never manufacture an
  address outside `coverage(e)`.

So over-reporting is excluded at *both* layers. At the identity layer the stored
endsets are immutable and faithfully returned (E1, E6); at the resolution layer the
projection is bounded above by the named identity (E9). What an edit can do is make
an endpoint *unresolvable* — never make the read invent one. This is the precise
sense in which survivability is "attrition only": a link's resolved endpoints can
vanish, but the link can never acquire endpoints it did not hold. The reader who
receives an empty resolution cannot, from that alone, distinguish "this link names
no content" from "this link's content is currently unplaced" — both are honest
reports that the named identity is, at present, nowhere arranged.

## Frame: a pure read with no open-document precondition

Finally, the frame. READENDSETS reads `Σ.L(a)` and nothing else.

- **(E10) PureReadNoArrangementPrecondition.** READENDSETS modifies no component of
  `Σ` and depends on no arrangement: its result is determined by `Σ.L(a)` alone, so
  it requires no document of `dom(Σ.M)` to be *open* or otherwise prepared. The sole
  precondition is `a ∈ dom(Σ.L)`. In particular, the home document `home(a)` need not
  be open to read `a`'s endsets.

This is the abstract content of the implementation's observation that endset
reading carries no open-document discipline: the read is keyed by the link's own
address, and the link store answers it directly. An open-document precondition would
attach only to a *subsequent* act — resolving (E9) into a particular arrangement, or
fetching content — not to the read of the endsets themselves.

## Coda

The four questions resolve into one structural fact and its consequences. The fact:
`Σ.L(a)` is the link, and READENDSETS returns it. From this, *what is returned* is
the full `N`-ary endset structure (E2, E3); *what the reader learns* is the
discontiguous shape of each end, the directional roles, the type-as-kind, and the
identity of every participating document (E3–E5, E7); *what this reveals beyond
following* is the type with no destination and the link as a whole owned object
(E8); and *the governing invariants* are faithfulness (E1), read-invariance under
immutability (E6), and the attrition bound on any resolution (E9) — all of which any
faithful implementation must satisfy, and none of which requires more than that the
link's endsets be stored in exactly one place and read from there.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| READENDSETS | `READENDSETS(Σ, a) = Σ.L(a)` for `a ∈ dom(Σ.L)`; pure read | introduced |
| E0 | ReadDeterminacy — total function on `dom(Σ.L)`, result `= Σ.L(a)` | introduced |
| E1 | Faithfulness — result is `Σ.L(a)` slot-for-slot; no over- or under-reporting | introduced |
| E2 | TernaryStructure — arity `N ≥ 3`; slots from(1)/to(2)/type(3), each an `Endset`, type non-empty, slots distinguishable | introduced |
| E3 | SpanSetGranularity — each endset a boundary-defined span-set; ends may be discontiguous and cross-document; read returns all spans | introduced |
| E4 | DirectionalRoles — slots 1,2 carry from/to structurally; semantics from type, not the read; one-sided (empty slot) permitted | introduced |
| E5 | TypeByAddressReturn — type endset returned; kind by address-identity, undereferenced; coverage may be ghost | introduced |
| E6 | ReadInvariance — `Σ →* Σ' ⟹ READENDSETS(Σ',a) = READENDSETS(Σ,a)`; independent of edits to `Σ.M` | introduced |
| E7 | ParticipantDisclosure — read names every participating document via field projection on returned spans; identity disclosed, content not | introduced |
| E8 | RevelationBeyondTraversal — read exposes discontiguity, type, and link-as-unit, none visible from a single endpoint | introduced |
| res / resolved | Derived projection of an endset into the current arrangement family | introduced |
| E9 | ResolutionAttrition — `resolved(Σ,e) ⊆ coverage(e)`; resolution may be partial/empty (ghost link); never over-reports | introduced |
| E10 | PureReadNoArrangementPrecondition — modifies nothing, requires no open document; sole precondition `a ∈ dom(Σ.L)` | introduced |

## Open Questions

Must reading an endset whose coverage enters a confidential document be gated by access control, or does identity disclosure override confidentiality?

What guarantee must relate the resolutions of one stored endset against two distinct arrangements that share Istream origin?

Must the positional order in which the endsets are returned carry semantic weight, or is it purely an addressing convention?

What invariant must hold between the directional from/to roles and the type endset for the directional reading of a link to be meaningful?

Under what abstract conditions may a resolution legitimately return empty for a link whose stored endsets are non-empty, and must those conditions be distinguishable by the reader?
