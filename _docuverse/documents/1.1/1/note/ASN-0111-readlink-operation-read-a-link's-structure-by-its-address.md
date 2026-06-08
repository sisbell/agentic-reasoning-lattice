# ASN-0111: READLINK — Reading a Link's Structure by Its Own Address

*2026-06-04*

## The problem

A Xanadu link is not markup buried in content; it is a first-class object with its own
permanent address in the link subspace. Because it is addressable, we can name it
directly and ask the system a question that has nothing to do with where the link points:
*what relationship does this object record?* This note specifies the operation that answers
that question — the direct read of a link by its own identity. We call it `readlink`.

We must be careful to separate `readlink` from three neighbouring operations that are out
of scope here. *Following* a link takes one of its endsets and resolves it against a chosen
document's arrangement to obtain current positions. *Searching* for a link supplies content
regions and asks which links touch them. *Counting* asks how many do. All three consult
something beyond the link object — an arrangement, or a query's spec-set. `readlink` consults
nothing beyond the link itself. It is the operation by which the link discloses, in full and
unconditionally, the relationship it was built to hold.

The reasoning below proceeds by asking, repeatedly, *what must be true for the read to deliver
the recorded relationship?* — and refining the specification each time the answer forces a new
commitment.

## The link as a readable object

We take from the foundations the shape of a stored link. The *link store* `Σ.L : T ⇀ Link`
(ASN-0043) maps addresses to link values, where a link value is a finite sequence of endsets

> `Link = {(e₁, e₂, ..., eₙ) : N ≥ 3, each eᵢ ∈ Endset}`,  `Endset = 𝒫_fin(Span)`

with the standard-triple convention assigning slot 1 the *from*-endset, slot 2 the *to*-endset,
and slot 3 the *type*-endset. Each endset is a finite set of spans over the tumbler line; each
span `(s, ℓ)` denotes a contiguous region `{t : s ≤ t < s ⊕ ℓ}` (T12, ASN-0034). The relationship
a link records is therefore not a pair of points but a triple of *span-sets*, each reaching —
possibly discontiguously — anywhere in the docuverse. The address-set a span-set denotes is its
`coverage` (ASN-0043):

> `coverage(e) = (∪ (s, ℓ) : (s, ℓ) ∈ e : {t ∈ T : s ≤ t < s ⊕ ℓ})`.

Every link address is, by the substrate invariants, an element-level, T4-valid tumbler in the
link subspace: `zeros(a) = 3`, `subspace_I(a) = s_L`, `#E(a) ≥ 2` (L0, L1, L1b, L0b of ASN-0043).
These facts are what make a link nameable in the same address space as content, and they are
what `readlink` will exploit.

## Deriving the read

A standing precondition governs everything below: `readlink` is specified over `→*`-reachable,
invariant-satisfying states `Σ` (ASN-0047, ASN-0093). Where we write "for a state `Σ`," read "for a
reachable, invariant-satisfying `Σ`."

We are looking for an operation that, given an address, returns the relationship recorded there.
The minimal honest specification is a lookup in the link store. For such a state `Σ` and address `a`:

> `readlink(a, Σ)`
>   *defined when*  `a ∈ dom(Σ.L)`
>   `≡  Σ.L(a) = (e₁, e₂, ..., eₙ)`.

It is a pure read: its frame condition is that it changes nothing, `Σ' = Σ`. The whole interest
of the operation lies not in this one line but in what the one line *commits us to* — the
properties the returned value must have, and what those properties let a reader learn.

The first commitment is on the domain. The read is defined exactly on allocated link addresses.

**RL0 (Definedness).** `readlink(a, Σ)` is defined iff `a ∈ dom(Σ.L)`. Reasoning backward from
the postcondition "the result is the recorded relationship at `a`," the weakest precondition is
precisely membership:

> `wp(readlink request at a, result = Σ.L(a)) ≡ a ∈ dom(Σ.L)`.

The link-shape of an address is necessary but not sufficient for definedness: an address may parse
as a well-formed link tumbler yet name no allocated link.

A reader holding a candidate tumbler can test the *necessary* structural conditions from the
address alone — `zeros(a) = 3 ∧ subspace_I(a) = s_L` — by T4 parsing and the subspace projection
(ASN-0034). These conditions are necessary but not sufficient: an address may have link-shaped
structure yet name no allocated link. Definedness is a fact about `dom(Σ.L)`, not about the
address's syntax, so the read either delivers the whole relationship or reports that no link
lives at `a`. There is no partial-success middle state at the level of *whether* a link is there.

## Completeness: the read returns the whole relationship

The defining contrast between reading a link and finding one is *what counts as an answer*.
A search is satisfied by a witness: a link is returned when *one* span of each endset meets the
request, so a search confirms relevance without delivering the endset. A direct read has no
request to satisfy and therefore no notion of a satisfying fragment. It must return the endsets
*entire*.

**RL1 (Completeness).** For each slot `i` and each span, the read omits nothing:

> `(A i, (s, ℓ) : 1 ≤ i ≤ |Σ.L(a)| ∧ (s, ℓ) ∈ Σ.L(a).eᵢ : (s, ℓ) ∈ readlink(a, Σ).eᵢ)`,

and conversely the read introduces no span not recorded. Equivalently `readlink(a, Σ) = Σ.L(a)`
componentwise. The justification is immediate from the definition, but the *content* of the
claim is the rejection of the satisfaction model: an alternative implementation that returned
only the spans matching some implicit predicate would not be reading the link — it would be
searching it. Reading is exhaustive by construction; satisfaction is irrelevant because there is
no query against which to be satisfied.

This is why the read recovers the arbitrary, broken collections that endsets are permitted to be.
An endset may scatter spans across many documents and across discontiguous regions within one;
the read returns every piece, because completeness is over the recorded structure, not over any
region a caller happened to name.

## The structure the read must preserve

Completeness says no span is lost. It does not yet say the spans arrive *organised*. The link's
meaning lives in its organisation: a span in the from-set asserts something different from the
same span in the to-set or the type-set. So the read carries an obligation beyond returning a
bag of spans.

**RL2 (Role preservation).** Completeness (RL1) already forces per-slot set equality
`readlink(a, Σ).eᵢ = Σ.L(a).eᵢ` for every `i`; what RL2 adds is the *structural* status of that
equality. The read preserves the link's arity and exposes each endset under its slot index as a
model primitive — slot position is part of the value, not a label a reader reconstructs from an
unordered pool:

> `|readlink(a, Σ)| = |Σ.L(a)|`,  and for each `1 ≤ i ≤ |Σ.L(a)|` the positional accessor
> `readlink(a, Σ).eᵢ` is a model primitive (L6, ASN-0043), with link equality componentwise.

The quantifier ranges over *all* `|Σ.L(a)|` slots, not a fixed three: in the dominant arity-3 case
slot 1 is *from*, slot 2 is *to*, and slot 3 is *type*, while the model admits `N > 3` (L3, ASN-0043,
requires only `N ≥ 3`), with slots 4…N returned faithfully under their own indices and no privileged
role assigned by this operation. A read that collapsed the endsets into one pool, or that swapped two
differing slots, would return a *different* relationship (link equality is componentwise, L6). The
read must keep every endset aligned with its slot — the directional from/to pair, the separate type
endset, and any further slots alike — this is exactly the alignment that any role-respecting use of
the link depends upon.

Within a single endset, however, no further order is owed.

**RL3 (Intra-endset set semantics).** The spans inside `readlink(a, Σ).eᵢ` carry no positional
meaning. The read exposes membership, not sequence: there is no operator selecting "the j-th
span" of an endset (L5, ASN-0043). An endset is an arbitrary collection of spans, and each span's
denotation is fixed by its own boundaries, independent of any position in a list. Two reads that
present the same endset's spans in different incidental orders have returned the same endset.

We can summarise RL1–RL3 in one sentence: the read returns the *complete* relationship,
*grouped by role*, *unordered within each role*.

## What the read reveals that the endpoints do not

We now ask the question that motivates direct read at all. Suppose a reader could instead arrive
at the content the link connects — stand at a from-span and at a to-span and read the bytes there.
What would still be missing?

Everything that makes the relationship a relationship. The bytes at the two ends announce neither
why they are connected nor by whom. Four things are recoverable only from the link object, and
the direct read is what delivers them.

*The type.* The kind of connection — citation, refutation, comment — is the third endset, not a
property of either endpoint. Two links whose endpoints are byte-for-byte identical may be a
citation and a refutation; only `readlink(a, Σ).e₃` tells them apart. Because the read returns the
type endset alongside from and to (RL2), the reader learns the nature of the connection, not just
its termini.

*The direction.* Standing at an endpoint, one cannot tell whether one is at the source or the
target of the assertion. The read encodes the asymmetry: slot 1 is "from," slot 2 is "to."

*The ownership.* A relationship is a *claim*, and a claim has an author. The link's home document
records who owns it, and it is derivable from the link's own address without consulting any endset.

**RL4 (Home disclosure).** `home(a) = N(a).0.U(a).0.D(a)` is determined by the read key `a` alone,
by T4 field projection, and is independent of the returned endsets (L2, ASN-0043). Because the read
is keyed by the address and the address encodes the home, the read reveals ownership for free, even
of a link that points nowhere near its home document — the home indicates *who owns* the link, not
*what it points to*.

*The whole at once.* Arriving at an endpoint gives one location. The read gives both ends and the
type simultaneously, as a single structure. The reader sees the relationship whole, which is what
permits any judgement about it — whether a supersession claim comes from the original author or a
third party, for instance — to be made at all.

## Type is interpreted by address, not by content

The type endset deserves separate treatment, because it is the one part of the structure whose
spans need not reference anything that exists.

**RL5 (Type-by-address).** The relationship the type records is fixed by `coverage(e₃)` — the set
of addresses the type-set names — and not by whatever is, or is not, stored at those addresses.
Two links share a type exactly when their type endsets have equal coverage (L8, ASN-0043), a
relation on address sets, decided without dereferencing a single one. The read therefore delivers
a fully interpretable type even when the type address holds nothing at all: ghost types are
permitted (L9, ASN-0043), and the read of a ghost-typed link is no less complete than any other.

## Faithful disclosure of nesting

Because links live in the same address space as content, an endset may name another link. The
to-set of a link can carry a span of width one over a link's own address (the canonical reflexive
span of L13, ASN-0043), making the link's target itself a link. Compound and faceted structures
are built this way.

**RL6 (Nesting fidelity).** If `a' ∈ dom(Σ.L)` and `a' ∈ coverage(readlink(a, Σ).eᵢ)`, the read
discloses `a'` as the tumbler address it is — it does not flatten the reference into the content,
if any, that further reading of `a'` might yield. The read is address-faithful: a target address is
returned as an address, whether it names content or another link. One direct read returns one
link's structure; the addresses it contains may themselves be read, but the read does not silently
recurse, nor does it hide that a returned address is a link rather than content. Whether and how a
reader chooses to follow the nesting by issuing further reads is the reader's affair; the read's
obligation is fidelity at the level it returns.

## Determinacy and the immutability of the recorded relationship

A read is only as trustworthy as the stability of what it reads. The link store is append-only and
its values are frozen: once allocated, a link's address persists and its value never changes
(L12, L12a of ASN-0043). The read inherits this stability.

**RL7 (Determinacy).** `readlink` is a pure function of `(a, Σ.L)`: two reads of the same address
in the same link store return identical values. Moreover, the read is stable across the whole
future:

> `(A Σ, Σ' : Σ →* Σ' ∧ a ∈ dom(Σ.L) : readlink(a, Σ') = readlink(a, Σ))`.

We are careful about the quantifier here. L12 (ASN-0043) is a *single-step* guarantee: for one
transition `Σ → Σ'`, an allocated link persists in the domain and keeps its value. The claim above
quantifies over the reflexive-transitive closure `Σ →* Σ'`, so it needs the multi-step lift, not
L12 alone. That lift is already available: LP13 (UnconditionalLinkPersistence, ASN-0098) discharges
both halves across the closure — `a ∈ dom(Σ.L) ⟹ a ∈ dom(Σ'.L)` (so `readlink(a, Σ')` is defined)
and `Σ'.L(a) = Σ.L(a)` (so the read value is preserved) — for every reachable `Σ →* Σ'`. With
definedness and value preservation both carried across the closure,
`readlink(a, Σ') = Σ'.L(a) = Σ.L(a) = readlink(a, Σ)`.

A reader who has once read a link may rely on that reading permanently. This is the counterpart, at
the read interface, of the design commitment that to record a *different* relationship one must
make a *different* link: there is no operation that re-types or re-aims an existing link in place,
so the structure the read returns today is the structure it will return forever.

## Recorded relationship versus resolved position

We can now state the deepest distinction the operation embodies, the one that separates `readlink`
from following or searching. A link records its endsets as spans over the *permanent* address space.
Resolving those spans against a particular document's arrangement — mapping them to current
positions — is a separate act, the business of traversal and projection, and it is conditional on
the arrangement. The direct read performs no such resolution. It returns the recorded spans as they
stand.

**RL8 (Recorded, not resolved).** `readlink(a, Σ)` depends only on `Σ.L`; it is independent of every
document arrangement. Consequently the read succeeds and returns the complete structure even for an
*orphaned* link — one whose endpoint content is currently arranged in no document, so that resolving
its endsets would yield nothing (cf. the ghost-projection situation, ASN-0098). The link's structure
persists unconditionally (L12; LP13 of ASN-0098), and the read surfaces it unconditionally.

This is what direct read reveals that following or searching cannot. A follow that found no current
position, or a search whose spec-set the orphaned content no longer occupies, would report
emptiness — not because the relationship has ceased to exist, but because no arrangement currently
witnesses it. The read distinguishes *the relationship is gone* from *the relationship is
unwitnessed*, and answers, for an allocated link, always the latter at worst: the structure is
there, complete, and the read returns it.

## Invariants governing the returned structure

Finally we collect the invariants that constrain *what* a well-formed read may return — the
guarantees a reader may assume of any value `readlink` produces, *under the standing precondition
that `Σ` is reachable and invariant-satisfying* (established above). These are not new obligations but
the foundation invariants viewed through the read interface; an alternative implementation's read
must honour them because the stored values of any reachable state do. They are claims about the
reachable class of states, not about arbitrary stores.

**RL-WF (Well-formedness).** Each returned endset is a finite set of T12-well-formed spans
(`Endset = 𝒫_fin(Span)`). Every span `(s, ℓ)` in the result satisfies `Pos(ℓ) ∧ actionPoint(ℓ) ≤ #s`,
so each denotes a non-empty contiguous region (ASN-0034). The read can never return a malformed or
empty span.

**RL-ARITY (Triple-or-more, typed).** The returned value has arity at least three, and its type slot
is non-empty:

> `|readlink(a, Σ)| ≥ 3  ∧  readlink(a, Σ).e₃ ≠ ∅`   (from L3, ASN-0043).

A conforming link always carries a classifying type; the read therefore always returns a usable
type endset. The from- and to-endsets, by contrast, may individually be empty — `∅` is a valid
endset — so the read may legitimately return an empty connective slot while never returning an empty
type slot. This is the read-side image of the structural rule that a link's type is mandatory and
its directional reach is permissive.

**RL-GEN (Endset generality).** The spans the read returns may point anywhere: across documents,
within the link's own home document, or into the link subspace at other links (L4, ASN-0043). The
read imposes no confinement on coverage beyond well-formedness; whatever the link recorded, the read
returns.

**RL-REP (Representation independence of meaning).** The relationship the read conveys is the
*coverage* of each endset, not the particular span decomposition. Two recorded endsets with equal
coverage record the same relationship and are interchangeable for every coverage-based use (the
type relation of L8; projection independence, LP21 of ASN-0098). A reader interpreting the result
should read it as a triple of address-sets-with-roles; the exact spans are one representation of
those sets.

## A worked read

The claims above are abstract; we check them against one concrete link. Fix the subspace
convention `s_C = 1`, `s_L = 2` (ASN-0093). Take two documents

> `d₁ = [1.0.1.0.1]`,  `d₂ = [1.0.1.0.2]`  (each `zeros = 2`, T4-valid),

and a link homed in `d₁` at address

> `a = [1.0.1.0.1.0.2.1]`   (`zeros(a) = 3`; element field `E(a) = [2, 1]`, so
> `subspace_I(a) = E(a)₁ = s_L`, `#E(a) = 2` — the first emission of `d₁`'s link sub-allocator).

Let the stored value `Σ.L(a) = (F, G, Θ)` be the standard triple

- **from-set** `F = {([1.0.1.0.1.0.1.1], δ(2, 8)), ([1.0.1.0.2.0.1.1], δ(1, 8))}` — two spans
  scattered across *two* documents. `coverage(F)` is a *union of two half-open intervals*, not a
  finite list of points. The first span runs from `[1.0.1.0.1.0.1.1]` up to but not including
  `[1.0.1.0.1.0.1.1] ⊕ δ(2, 8) = [1.0.1.0.1.0.1.3]`; by T1 case (ii) that interval contains the
  entire subtrees beneath `…1.1` and `…1.2` (e.g. `[1.0.1.0.1.0.1.1.0]`, `[1.0.1.0.1.0.1.2.5]`),
  an infinite tumbler set, *not* the two addresses `…1.1` and `…1.2` alone. The second span is the
  interval `[ [1.0.1.0.2.0.1.1], [1.0.1.0.2.0.1.2] )` under `d₂`. The element-level content
  I-addresses *lying within* `coverage(F)` — the `dom(C)` members inside the coverage intervals,
  reserving "arranged" for the `Σ.M` sense used in RL8 — are `[1.0.1.0.1.0.1.1]` and
  `[1.0.1.0.1.0.1.2]` under `d₁` and `[1.0.1.0.2.0.1.1]` under `d₂` — three I-addresses that host
  content and lie *inside* `coverage(F)`, to be distinguished from the coverage intervals themselves.
- **to-set** `G = ∅` — a legitimately empty connective slot.
- **type-set** `Θ = {([1.0.1.0.9.0.1.1], δ(1, 8))}` — a single span whose address sits under a
  document `[1.0.1.0.9]` that hosts no content: a *ghost* type, a label by location.

A direct read returns the whole triple, grouped by slot:

> `readlink(a, Σ) = (F, ∅, Θ)`,
> with `readlink(a, Σ).e₁ = F`, `readlink(a, Σ).e₂ = ∅`, `readlink(a, Σ).e₃ = Θ`.

We can now check the load-bearing postconditions against this instance.

- *RL1 (completeness).* The read returns *both* from-spans, the empty to-set, and the type-span —
  every recorded span and nothing more. Contrast a *search* given the content region under `d₁`:
  it would return `a` as a witness because *one* from-span meets the region, but it would not
  deliver `F` entire, would say nothing about the empty `G`, and would not surface the ghost `Θ`.
  The read delivers the structure; the search confirms relevance.
- *RL2 (role preservation).* The three endsets come back under slots 1/2/3, not pooled. Were the
  read to return the bag `F ∪ Θ`, the reader could no longer tell that `[1.0.1.0.9.0.1.1]`
  classifies the link while the others are its source — a different relationship (L6). The read
  copies the stored `Σ.L(a).eᵢ` into `readlink(a, Σ).eᵢ` by a per-index rule that names no other
  slot (link equality is componentwise, L6), so verifying slots 1–3 establishes the claim for every
  `N ≥ 3`: an arity-4 value `(F, ∅, Θ, e₄)` returns `e₄` under slot 4 by exactly the same copy, with
  no slot-count-dependent step to recheck.
- *RL5 (ghost-type completeness).* `Θ`'s address holds nothing, yet the read returns it intact.
  Its single span `([1.0.1.0.9.0.1.1], δ(1, 8))` is the canonical unit-depth span (`#s = 8 = #δ(1, 8)`),
  so by PrefixSpanCoverage (ASN-0043) `coverage(Θ) = {t : [1.0.1.0.9.0.1.1] ≼ t}` — the *subtree*
  beneath that address, an infinite tumbler set, not the single point `[1.0.1.0.9.0.1.1]`. As with
  the from-set above, the type is interpreted as this coverage *address-set* (L8) and matched against
  another type's coverage without dereferencing anything stored there. The read of this ghost-typed
  link is no less complete than any other.
- *RL-ARITY.* Arity is 3 and `Θ ≠ ∅`, while the connective slot `G = ∅` is permitted — exactly
  the mandatory-type / permissive-direction split.

*A nested instance (RL6).* Links share the address space with content, so an endset may target
another link. Let `a' = inc(a, 0) = [1.0.1.0.1.0.2.2]` be a second link homed in `d₁` — the next
sibling on `d₁`'s link sub-allocator, so `a' ∈ dom(Σ.L)` — and consider a third link
`c = [1.0.1.0.1.0.2.3]`, also homed in `d₁`, whose to-set is the canonical reflexive span over `a'`:

> `Σ.L(c) = (∅, G_c, Θ)`,  `G_c = {([1.0.1.0.1.0.2.2], δ(1, 8))}`   (`#a' = 8 = #δ(1, 8)`, the
> canonical unit-depth span of L13, ASN-0043; `c` reuses the ghost type `Θ`, so it is a conforming
> arity-3 link with non-empty type slot).

The read returns `readlink(c, Σ).e₂ = G_c`, the span intact. By PrefixSpanCoverage (ASN-0043) its
coverage is the subtree `coverage(G_c) = {t : a' ≼ t}`, so `a' ∈ coverage(readlink(c, Σ).e₂)`. The
read discloses `a'` *as the tumbler address it is*: it does not flatten the reference into whatever
`a'` — itself a link — records, and it does not silently recurse into a read of `a'`. One read of
`c` returns one link's structure; the returned address `a'` may be read in turn, but that is a
separate `readlink(a', Σ)` the caller chooses to issue. This verifies RL6 against a concrete
link→link target — the construction underlying compound and faceted structures.

*An orphaned instance (RL8).* Suppose that at state `Σ` no document arrangement maps any
V-position to the three content I-addresses lying within `coverage(F)` — the connected content is
arranged nowhere. Discoverability quantifies over slots (LP12, ASN-0098:
`discoverable_from(a, d, Σ) ⟺ (E i : coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)`), so we dispatch all
three. We do not re-derive here which substrate addresses each coverage interval contains: every
span of `F` and of `Θ` is a *canonical* span whose start lies in the substrate-emittable set, so
LP-Fin Corollary (CanonicalIntervalCharacterisation, ASN-0098) fixes `coverage ∩ (dom(Σ.C) ∪
dom(Σ.L))` to the span's own sub-allocator chain — every such member carries the start's subspace
identifier and origin. Each start here sits under subspace `s_C`, while every `dom(Σ.L)` member
carries `s_L` (L0, ASN-0093); the two are disjoint, so the link store meets neither coverage:
`coverage(F) ∩ dom(Σ.L) = coverage(Θ) ∩ dom(Σ.L) = ∅`. *Slot 1 (from):* by the same corollary,
`coverage(F) ∩ dom(Σ.C)` is exactly the three named chain-member I-addresses, unarranged by
hypothesis; with the link store empty and every arrangement range confined to `dom(Σ.C) ∪ dom(Σ.L)`
(LP20 RangeConfinement, ASN-0098, via S3★ of ASN-0047), `coverage(F) ∩ ran(Σ.M(d)) = ∅` for every
`d`. *Slot 2 (to):* `G = ∅`, so `coverage(∅) = ∅` and the slot is trivially unwitnessed. *Slot 3
(type):* the ghost document `[1.0.1.0.9]` hosts no content, so `coverage(Θ) ∩ dom(Σ.C) = ∅`; with
the link store also disjoint (above), `coverage(Θ) ∩ ran(Σ.M(d)) = ∅` for every `d`, independent of
whether `[1.0.1.0.9]` hosts anything. With all three slots unwitnessed, `discoverable_from(a, d, Σ)`
is false for every `d`, and the link is orphaned — exactly the ghost-projection situation (LP17,
ASN-0098). A *follow* of `F` against any arrangement would resolve to the empty set, and a *search*
would find nothing to match. The direct read is unaffected: it consults only `Σ.L`, so
`readlink(a, Σ) = (F, ∅, Θ)` still returns the complete structure. The read thus distinguishes *the
relationship is unwitnessed* (true here) from *the relationship is gone* (false — `a ∈ dom(Σ.L)` and
its value is fixed by L12 / LP13).

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| `readlink` | `readlink(a, Σ) ≡ Σ.L(a)`, defined when `a ∈ dom(Σ.L)`; pure read, frame `Σ' = Σ` | introduced |
| RL0 | The read is defined iff `a ∈ dom(Σ.L)`; `wp = a ∈ dom(Σ.L)`; link-shape of the address is necessary but not sufficient | introduced |
| RL1 | Completeness — the read returns every recorded span of every endset and no other; `readlink(a, Σ) = Σ.L(a)` (rejects the satisfaction model) | introduced |
| RL2 | Role preservation — the read preserves arity (`|readlink(a, Σ)| = |Σ.L(a)|`) and exposes slot position as a model primitive (L6); from/to/type grouping delivered as structure, not reconstructed from RL1's per-slot equality | introduced |
| RL3 | Intra-endset set semantics — spans within a returned endset are unordered; membership, not sequence, is exposed | introduced |
| RL4 | Home disclosure — `home(a)` is determined by the read key alone, independent of endsets; the read reveals ownership | introduced |
| RL5 | Type-by-address — the type is interpreted via `coverage(e₃)`, not via content at those addresses; ghost types read completely | introduced |
| RL6 | Nesting fidelity — link addresses in an endset's coverage are returned as addresses, unflattened and unrecursed | introduced |
| RL7 | Determinacy — `readlink` is a pure function of `(a, Σ.L)` and stable across all `Σ →* Σ'` by link immutability | introduced |
| RL8 | Recorded, not resolved — the read depends only on `Σ.L`, succeeds for orphaned links, and returns the complete structure independent of any arrangement | introduced |
| RL-WF | Each returned endset is a finite set of T12-well-formed spans | introduced |
| RL-ARITY | The returned value has arity ≥ 3 with non-empty type slot; connective slots may be empty | introduced |
| RL-GEN | Returned spans may reference any address (cross-document, intra-home, link-subspace) | introduced |
| RL-REP | The conveyed relationship is each endset's coverage; equal-coverage endsets are interchangeable in meaning | introduced |

## Open Questions

What must the system guarantee a reader can conclude about a relationship's continued validity from a direct read alone, given that the read does not consult any arrangement?

What must a read guarantee about the distinguishability of a connective endset that is legitimately empty from one whose spans reference only currently-unwitnessed content?

What guarantee must hold so that reading two distinct links with identical recorded structure always yields results distinguishable by the reader, given that addresses, not values, carry link identity?
