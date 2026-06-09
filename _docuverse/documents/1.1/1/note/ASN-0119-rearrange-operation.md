# ASN-0119: REARRANGE Operation

*2026-06-08*

## The problem

We are asked what happens when two regions of a document are transposed. Nelson
states the operation flatly: "Rearrange transposes two regions of text. With
three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3...
With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4"
(4/67). The sentence describes a *motion* — content that was here is now there,
content that was there is now here. It says nothing about what is *conserved*
under that motion, and the conservation is the whole of the matter.

The word *transposes* must be read against the design's deepest commitment: a
document is a mapping from positions to content, not the content itself. "The
address of a byte in its native document is of no concern to the user or to the
front end; indeed, it may be constantly changing; the front-end application is
unaware of this" (4/11). What an editorial operation rearranges is the mapping,
not what is mapped. Nelson is explicit that this is why links endure: "Note that
this order may be continually altered by editorial operations, but since the
links are to the bytes themselves, any links to those bytes remain stably
attached to them" (4/30).

So the task is to specify a permutation. We must say precisely which positions
are reassigned, what each one now denotes, what is left untouched, and then
discharge a list of obligations: that no content is created or destroyed, that
the document's total extent is conserved, that moved content remains findable
under its new position, that links survive the reordering, and that any other
document sharing the rearranged content is wholly unaffected. We will find that
every one of these obligations follows from a single structural fact — that
REARRANGE rewrites only the arrangement and never touches an I-address.

## The two streams

We work in the state `Σ = (C, M, L)` of the strand and link models. The *content
store* `Σ.C : T ⇀ Val` (ASN-0036, S0) is append-only and immutable; an address
`a ∈ dom(C)`, once allocated, denotes its value forever. This is the Istream:
the permanent record of *what content exists*. The *arrangement*
`Σ.M(d) : T ⇀ T` of a document `d` maps V-positions to I-addresses; it is the
Vstream, the record of *how content is currently ordered* in `d`. The *link
store* `Σ.L : T ⇀ Link` (ASN-0043) records typed associations whose endsets
reference content by address. V-positions and I-addresses are tumblers ordered
by T1 (ASN-0034); within a subspace the active V-positions are contiguous and
share a common depth (ASN-0036, D-CTG, D-SEQ, S8-depth).

The distinction the operation turns on is the one ASN-0034's T6 already records:
*address versus position*. An I-address is permanent content identity; a
V-position is a mutable coordinate in one document's current order. REARRANGE
lives entirely in the second of these. We will write `M(d)(v)` for the I-address
that position `v` currently denotes, and we will be watching, throughout, for the
property that this *value* is carried intact while the *key* under which it is
filed is permuted.

We confine the operation to a single subspace `S` of one document — the text
subspace `s_C` is the case of interest — and adopt ASN-0058's ordinal-shift
convention: for a V-position `v` and natural `k`, `v + k` abbreviates
`shift(v, k)` (ASN-0034) at `v`'s depth, with `v + 0 = v`. Because the active
text positions are contiguous and densely indexed (D-SEQ), a *cut* may be named
by the V-position at which it falls, and the width of an interval between two
cuts is the ordinal difference of their positions.

## Cuts and regions

A *cut sequence* is a strictly ascending list of V-positions
`c₀ < c₁ < ... < c_{n-1}` in subspace `S`, with `n ∈ {3, 4}` and every cut
landing on a boundary of the current arrangement (ASN-0084, CutSequence). Three
cuts specify a *pivot*; four cuts specify a *swap*. We require that the affected
interval lie entirely within the arrangement — every depth-`S` position from
`c₀` up to the last cut is active (ASN-0084, R-PRE) — so the cuts genuinely
partition existing content rather than naming holes.

For three cuts the affected interval `[c₀, c₂)` splits into two regions

      α = { v : c₀ ≤ v < c₁ },    β = { v : c₁ ≤ v < c₂ },

with widths `w_α = ord(c₁) − ord(c₀)` and `w_β = ord(c₂) − ord(c₁)`. For four
cuts the interval `[c₀, c₃)` splits into three,

      α = [c₀, c₁),    μ = [c₁, c₂),    β = [c₂, c₃),

where `μ` is the *intervening region* belonging to neither moved block. We write
`w_μ = ord(c₂) − ord(c₁)`. Both region widths of the moved blocks are strictly
positive (a cut sequence with a zero-width region is degenerate), and in the
four-cut case `w_μ ≥ 1` as well.

The cuts are interpreted against *one* arrangement. This is the first thing the
"two cuts at once" formulation reveals, and we record it before going further:
all of `c₀, …, c_{n-1}` are coordinates in the same `M(d)`, so the geometry of
the regions is fixed before any reassignment occurs. We return to its
consequences in the section on atomicity.

## The transposition as a permutation

The pivot exchanges `α` and `β`. We specify the post-state `M'(d)` directly. The
exterior is frozen,

      v < c₀  ∨  v ≥ c₂   ⟹   M'(d)(v) = M(d)(v),                  (R-EXT)

the block `β` slides to the front of the interval,

      M'(d)(c₀ + j)        = M(d)(c₁ + j),    0 ≤ j < w_β,          (R-P1)

and `α` follows it,

      M'(d)(c₀ + w_β + j)  = M(d)(c₀ + j),    0 ≤ j < w_α.          (R-P2)

The swap (four cuts) is the same shape with the middle region threaded between:

      v < c₀  ∨  v ≥ c₃   ⟹   M'(d)(v) = M(d)(v),                  (R-EXT)
      M'(d)(c₀ + j)               = M(d)(c₂ + j),  0 ≤ j < w_β,     (R-S1)
      M'(d)(c₀ + w_β + j)         = M(d)(c₁ + j),  0 ≤ j < w_μ,     (R-S2)
      M'(d)(c₀ + w_β + w_μ + j)   = M(d)(c₀ + j),  0 ≤ j < w_α.     (R-S3)

These equations are the specification of REARRANGE. Everything else in this note
is a property derived from them.

The first thing to verify is that they describe a *function* on a fixed domain,
and indeed a bijection of the document's V-positions onto themselves. In the
pivot, the destination ordinals of R-P1 occupy `[ord(c₀), ord(c₀)+w_β)` and those
of R-P2 occupy `[ord(c₀)+w_β, ord(c₀)+w_β+w_α)`; these are disjoint, abut exactly,
and together tile `[ord(c₀), ord(c₂))` — the very interval the two regions
occupied before. With R-EXT covering the complement, every position is assigned
exactly once. The map

      π : dom(M(d)) → dom(M(d)),   defined by   M'(d)(π(v)) = M(d)(v),

is therefore a bijection that fixes the exterior and permutes the affected
interval; in closed form, for the pivot,

      π(v) = v                        (exterior),
      π(c₀ + j) = c₀ + w_β + j        (0 ≤ j < w_α, region α),
      π(c₁ + j) = c₀ + j              (0 ≤ j < w_β, region β),

and analogously for the swap with the three branches `α ↦ c₀+w_β+w_μ+·`,
`μ ↦ c₀+w_β+·`, `β ↦ c₀+·` (ASN-0084, R-PPERM, R-SPERM). Because `dom(M(d))` is
finite (S8-fin) and `π` is an injection of it into itself, `π` is onto, and the
post-state domain is unchanged:

      dom(M'(d)) = dom(M(d)).                                       **(P2)**

This is the formal content of *transposition*: a reassignment of positions that
loses none and invents none.

## What is preserved: I-address correspondence

The defining equation `M'(d)(π(v)) = M(d)(v)` says exactly what the consultation
calls for. Each rearranged region "must consist of exactly the same content it
held before — the same bytes with the same permanent Istream identity"
(Question 2). The value filed at the moved position is the value that was filed
at the source position; the I-address is copied across the reassignment, never
recomputed. No operation in the specification reads or writes the content store:

      Σ'.C = Σ.C.                                                   **(P0)**

So content permanence holds in its strongest form — not merely that I-addresses
survive (Question 9), but that the store is a verbatim frame. The relationship
each rearranged region bears to the positions it formerly occupied is therefore
one of *identity correspondence*: position `π(v)` now denotes precisely what
position `v` denoted, and "every byte in a transposed region corresponds to the
same byte before the move" (Question 2). What changes is the V-position; what is
preserved is the I-address, and with it the origin, the attribution, and every
relationship anchored to that address.

A consequence we will lean on repeatedly: the *set* of I-addresses the document
references is invariant. Since `π` is a bijection,

      ran(M'(d)) = { M'(d)(π(v)) : v ∈ dom(M(d)) }
                 = { M(d)(v)     : v ∈ dom(M(d)) }
                 = ran(M(d)).                                       **(P1)**

The document points at the same content after the rearrangement as before — only
the order of pointing has changed. We may now read off the remaining obligations.

## The intervening content

The four-cut case carries a region `μ` that is part of neither moved block, yet
cannot stay where it sits. The design must guarantee that this content is
"preserved in identity and connectivity even though its virtual position changes"
(Question 3). Our equations discharge this precisely. R-S2 reassigns each
position of `μ` while preserving its denotation:
`M'(d)(c₀ + w_β + k) = M(d)(c₁ + k)` for `0 ≤ k < w_μ`. The middle region is
moved as a block — its internal order is untouched — and its I-addresses are
carried intact, so it satisfies P0 and P1 exactly as the moved blocks do.

What is the *net* displacement of the middle? It departs ordinal `ord(c₁)` and
arrives at ordinal `ord(c₀) + w_β`. The displacement is

      (ord(c₀) + w_β) − ord(c₁) = w_β − w_α = (c₃ − c₂) − (c₁ − c₀),

the difference in the widths of the two swapped regions. Gregory's implementation
computes exactly this quantity for the middle slice — "the middle region
receives `diff[2] = |right_region| − |left_region|`, the difference in sizes of
the two swapped regions" (Question 11) — and the sign tells the direction: if the
block arriving at the front is wider than the block leaving it, the middle slides
forward; if narrower, backward; if the two are equal, the middle does not move at
all. This is not an arbitrary offset. It is the unique displacement that keeps the
middle *contiguous* with its new neighbours: for `μ` to tile the gap left between
the relocated `β` and the relocated `α`, it must shift by precisely the size
imbalance. The intervening content is thus conserved in identity and order, and
its position is determined — not chosen — by the geometry of the two regions
around it.

## V-extent conservation

The document's total extent must be unchanged: "the same bytes are present, in
the same quantity, merely permuted into a different order" (Question 7).
Conservation is immediate from P2. The active V-positions of subspace `S` form a
contiguous run by D-CTG, and `π` permutes that run onto itself, so the run's
cardinality and its endpoints are invariant:

      | dom(M'(d)) | = | dom(M(d)) |,    min and max V-position fixed.   **(P3)**

REARRANGE is, in the language of conservation laws, a permutation of a fixed
multiset. Gregory's evidence confirms that the extent is conserved structurally
rather than by repair: the implementation rewrites only V-displacements and never
allocates, frees, or resizes a span, and the recomputation of the document's
width after the operation "should do nothing" — the author's own comment marks it
as a defensive no-op precisely because the extent cannot have changed
(Questions 7, 13). The boundaries of the affected interval are themselves fixed:
the regions tile `[c₀, c_{n-1})` before and after, so the exterior never moves and
the document neither grows nor shrinks.

## Links

A link's endsets reference content by *address*. The link store is not consulted
by any clause of the operation, so

      Σ'.L = Σ.L                                                    **(P6)**

— domain and value both frozen. Nothing about a link changes when content is
rearranged; the operation does not even read `L`. This is the whole secret of
link survival, and it specializes cleanly to the cases the consultation poses.

*A link anchored entirely within a moved region* (Question 4). Its endset
references I-addresses, all of which belong to the moved block. REARRANGE deletes
no content, so every referenced byte survives; the link "is not an editing
casualty" and "moves with its content" because its endsets are I-addresses, which
the operation never changes (Question 4). The link itself does nothing — it
continues to denote the same I-addresses — and those addresses now happen to be
arranged at new V-positions.

To make "moves with its content" precise we use the projection of a link into a
document. For a link `a` with slot `i`, let `coverage(a, i)` be the set of
I-addresses its endset references (ASN-0098), and define the link's footprint in
`d` as the V-positions that resolve to those addresses,

      project(a, i, d, Σ) = { v ∈ dom(M(d)) : M(d)(v) ∈ coverage(a, i) }.

Coverage is a property of the endset's spans alone and is untouched by the
operation. Since `M'(d)(π(v)) = M(d)(v)`, a position `v` lies in the footprint
before exactly when `π(v)` lies in it after:

      project(a, i, d, Σ') = π( project(a, i, d, Σ) ).              **(P7a)**

The footprint is carried *through* `π`: it is neither lost nor enlarged, only
relocated to where the content now sits.

*A link spanning both moved regions, or running from a moved region into
stationary content* (Question 5). Here the footprint is split by a cut. Before the
operation the footprint may be a single contiguous run of V-positions; after it,
P7a relocates each part by whatever branch of `π` governs the region it fell in,
and those branches apply *different* displacements. The two halves therefore
generally land at non-adjacent V-positions, and the endset, when resolved against
the new arrangement, becomes a *discontiguous span-set*. This is exactly the
behaviour Nelson describes — "a link end that was a single contiguous span before
the rearrange may become discontiguous afterward, because the bytes it holds onto
have moved to new virtual positions" (Question 5) — and which Gregory observes
directly as endset fragmentation (Question 16). The link still connects precisely
the same bytes; only its picture in the current order has broken into pieces. The
operative principle is the one Nelson states: the link "must" do nothing except
continue holding its bytes; the system re-expresses the affected endset as a
span-set in the new ordering.

*Discoverability under fragmentation.* Because `π` is a bijection, the footprint
is nonempty after exactly when it was nonempty before:

      project(a, i, d, Σ') ≠ ∅   ⟺   project(a, i, d, Σ) ≠ ∅.      **(P7b)**

A link discoverable from `d` before the rearrangement is discoverable from `d`
after it. Discovery answers by *address* — it tests `coverage(a, i) ∩ ran(M(d))`,
and by P1 that intersection is invariant — so the link surfaces at whatever
V-positions the content now occupies (Question 8). Fragmentation changes how many
spans the footprint comprises; it does not change *whether* the link is found.

## Discoverability of moved content

A user who navigates to a moved region's new position must find the content and
everything attached to it. This is the dual of P7. To look "under the new
position" is to evaluate `M'(d)(π(v))`, and that equals `M(d)(v)` by P1 — the same
I-address the content always had. Position is resolved to identity, and identity
is what every index, link, and attribution is keyed on. So a navigation to `π(v)`
recovers exactly the content that lived at `v`, together with its origin (P0
leaves `origin` invariant) and its links (P7a places their footprints at `π(v)`).
"A user looking under the new position finds the content *and* every link,
annotation, and attribution it carried before the move — nothing is lost by
relocation" (Question 8). We record the consequence:

      moved content is discoverable under its new V-position,
      and resolves to its original I-address.                      **(P5)**

## Atomicity: two cuts at once

Why transpose *together* rather than move one region and later the other? The
single-operation form is interpreted against one arrangement, and this exposes
three ordering invariants (Question 6).

First, the document passes from one canonical total order directly to another. A
move-then-move realization manufactures an intermediate arrangement that is itself
a real, addressable, observable document state — "not a neutral scratch step."
The two realizations can agree on the final mapping while differing on what is
observable in between: a RETRIEVE issued after the first move but before the
second returns a partially-rearranged order that has no counterpart during the
atomic transposition (Question 19). We state the equality and the difference
together. Let `T` be the atomic transposition `Σ → Σ'`, and let `T₁ ; T₂` be any
two-move composite achieving the same net permutation. Then their final
arrangements coincide,

      M'(d) under T   =   M(d) under (T₁ ; T₂),                    **(P8a)**

because both realize the same `π` and the arrangement is determined by `π`
applied to the same content (P1); but the intermediate state of `T₁ ; T₂` is a
distinct, observable arrangement absent from `T`,

      ∃ observable Σ_mid with  M_mid(d) ≠ M(d) ∧ M_mid(d) ≠ M'(d). **(P8b)**

The logical content of the final state is path-independent; the *visible history*
is not.

Second, the cut coordinates resolve against a single, unshifted frame. All of
`c₀, …, c_{n-1}` are coordinates in one `M(d)`, so the regions' boundaries cannot
drift out from under each other mid-operation. A sequential realization would have
to recompute the second move's cuts in a coordinate frame the first move already
perturbed; the atomic form fixes the frame so every cut is valid simultaneously
(Question 6). This is why the equations of the operation may use `c₀, …, c_{n-1}`
as if they were all meaningful at once: they are.

Third, the operation treats both regions as moving relative to each other. There
is no privileged stationary block; position is relational, defined by neighbours
rather than by an absolute index, and what survives the swap is connectivity (P6),
not any region's claim to have stayed put.

## Document isolation

If the rearranged content is shared with another document by transclusion, that
document's arrangement must be untouched. Every clause of the operation that
mutates state writes only `M(d)`; the frame is explicit:

      (∀ d' ≠ d :: M'(d') = M(d'))   ∧   Σ'.C = Σ.C   ∧   Σ'.L = Σ.L.  **(P9)**

The isolation is structural, not a courtesy. Sharing in this model is by reference
to the Istream, not by copy: each document is its own V→I mapping over the common,
immutable content. REARRANGE rewrites `d`'s mapping. A document `d'` that
transcludes some of `d`'s content holds an *independent* mapping `M(d')` over the
same I-addresses, and P0 guarantees those I-addresses are unmoved. Even when
`ran(M(d)) ∩ ran(M(d')) ≠ ∅` — the two documents genuinely share content —
permuting `d`'s arrangement reaches nothing in `d'`'s. "The transposition
reshuffles one document's references; it cannot touch the underlying content or
the independent arrangement of any document that includes it" (Question 10).
Gregory's evidence makes the same point at the level of mechanism: the operation
runs over a single document's arrangement tree, and a second document's tree is
"simply structurally unreachable from a single-document REARRANGE call"
(Question 20).

## Well-definedness, and a caveat on the arithmetic

The equations specify the post-state by naming each destination directly, and we
proved above that those destinations tile the affected interval exactly, so `π` is
a bijection and the result is a legal arrangement. We elevate this to a
requirement on the operation: REARRANGE is well-defined only when the induced map
is a bijection of `dom(M(d))` onto itself preserving the domain (P2). An
alternative implementation must satisfy this no matter how it computes positions.

We flag, as an observation rather than a claim, that computing destinations by a
*uniform displacement formula* per region — rather than by the tiling above — is
correct only when the two moved regions have equal width. Gregory's analysis shows
that the green implementation displaces region `α` by `c₂ − c₀` regardless of the
widths, and that when `w_β > w_α` this drives the middle region to overlap the
relocated `α`, producing a V-position collision that violates the bijection
requirement (Question 14); the same unguarded arithmetic can push a text position
across a subspace boundary (Question 17). These are defects relative to the
abstract operation, which is specified by its target arrangement and admits no
such collision. The width imbalance that the middle region's displacement must
absorb (the section on intervening content) is exactly the quantity a uniform
formula mishandles. An implementation conforming to this specification must make
the regions tile, not merely shift each by a local offset.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| REARRANGE | Operation: given a 3- or 4-cut sequence in subspace `S` of document `d`, transpose the two named regions by reassigning their V-positions; specified by R-EXT and R-P1/R-P2 (pivot) or R-S1/R-S2/R-S3 (swap) | introduced |
| R-EXT | Exterior frame: positions below `c₀` or at/above the last cut keep their mapping, `M'(d)(v) = M(d)(v)` | introduced |
| R-P1, R-P2 | Pivot postcondition: `β` slides to the front of `[c₀, c₂)`, `α` follows; the two tile the interval exactly | introduced |
| R-S1, R-S2, R-S3 | Swap postcondition: `β` to front, intervening `μ` next (net displacement `w_β − w_α`), `α` last; the three tile `[c₀, c₃)` exactly | introduced |
| P0 (ContentPermanence) | `Σ'.C = Σ.C` — the content store is a verbatim frame; no I-address is created, destroyed, or rebound | introduced |
| P1 (IdentityCorrespondence) | `M'(d)(π(v)) = M(d)(v)`; I-addresses are carried across the reassignment, and `ran(M'(d)) = ran(M(d))` | introduced |
| P2 (Permutation) | The induced `π` is a bijection of `dom(M(d))` onto itself; `dom(M'(d)) = dom(M(d))` — a required well-definedness condition | introduced |
| P3 (VExtentConservation) | `\|dom(M'(d))\| = \|dom(M(d))\|`, and the active run's endpoints are fixed — the document's total extent is conserved | introduced |
| P5 (Discoverability) | Moved content is discoverable under its new V-position `π(v)` and resolves to its original I-address `M(d)(v)` | introduced |
| P6 (LinkStoreFrame) | `Σ'.L = Σ.L` — links are untouched; a link anchored in a moved region survives and travels with its content because endsets reference unchanged I-addresses | introduced |
| P7a (FootprintTransport) | `project(a, i, d, Σ') = π(project(a, i, d, Σ))` — a link's V-footprint is relocated through `π`; footprints split by a cut become discontiguous span-sets | introduced |
| P7b (DiscoverabilityPreserved) | `project(a, i, d, Σ') ≠ ∅ ⟺ project(a, i, d, Σ) ≠ ∅` — fragmentation never costs discoverability | introduced |
| P8a (FinalStateInvariance) | The atomic transposition and any two-move composite achieving the same net `π` reach the same final arrangement | introduced |
| P8b (IntermediateDivergence) | A two-move composite passes through an observable intermediate arrangement that the atomic transposition does not realize | introduced |
| P9 (DocumentIsolation) | `(∀ d' ≠ d :: M'(d') = M(d'))` together with P0, P6 — every other document, including transcluders of the rearranged I-addresses, is invariant | introduced |

## Open Questions

What must REARRANGE guarantee when a cut falls on a V-position that is shared, through transclusion, by more than one document, so that the cut is a boundary in one arrangement but interior to another?

Under what conditions may two rearrangements on the same document's content scope be applied without a serializing authority while leaving the final arrangement independent of their order?

What invariant must relate a content-based discovery index to the arrangement after a rearrangement, given that a link's footprint may fragment into arbitrarily many V-spans while its coverage is unchanged?

What must the operation guarantee about the recoverability of a prior arrangement from the permanent content store, given that REARRANGE records only the new V→I mapping and the old order is no longer expressed?

What relationship must hold between the displacement imposed on intervening content and the requirement that every subspace boundary be preserved, so that no permuted position may cross from one subspace into another?

What must a rearrangement guarantee about the well-formedness of a cut sequence whose affected interval reaches the document's first or last arranged position, so that no relocated position is carried outside the document's valid V-extent?
