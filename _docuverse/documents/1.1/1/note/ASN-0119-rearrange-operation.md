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
by T1 (ASN-0034); within the text subspace the active V-positions are contiguous
and share a common depth (ASN-0036, D-CTG, D-SEQ, S8-depth). These contiguity
invariants hold for the text subspace `s_C` and *not* in general for other
subspaces — the link subspace `s_L`, in particular, is exempt — which is why the
operation's scope is confined to text below.

The distinction the operation turns on is the one ASN-0034's T6 already records:
*address versus position*. An I-address is permanent content identity; a
V-position is a mutable coordinate in one document's current order. REARRANGE
lives entirely in the second of these. We will write `M(d)(v)` for the I-address
that position `v` currently denotes, and we will be watching, throughout, for the
property that this *value* is carried intact while the *key* under which it is
filed is permuted.

We confine the operation to the text subspace `s_C` of one document, at the
working V-position depth 2 (`#v = 2`). This is the precise scope at which
ASN-0036's contiguity invariants and ASN-0084's closed-form rearrangement
permutations are established; we make no claim about other subspaces or other
depths, and in particular the link subspace — lacking D-CTG/D-SEQ/D-MIN — does
not admit the cut-naming this operation relies on. We adopt ASN-0058's
ordinal-shift convention: for a V-position `v` and natural `k`, `v + k`
abbreviates `shift(v, k)` (ASN-0034) at `v`'s depth, with `v + 0 = v`; at depth 2
a text position has the form `[s_C, k]` and `ord(v) = k`. Because the active text
positions are contiguous and densely indexed (D-SEQ), a *cut* may be named by the
V-position at which it falls, and the width of an interval between two cuts is the
ordinal difference of their positions.

## Cuts and regions

A *cut sequence* is a strictly ascending list of V-positions
`c₀ < c₁ < ... < c_{n-1}` in the text subspace `s_C` at depth 2, with
`n ∈ {3, 4}` and every cut landing on a boundary of the current arrangement
(ASN-0084, CutSequence — its conditions CS3/CS4 fix exactly this subspace and
depth). Three cuts specify a *pivot*; four cuts specify a *swap*. We require that
the affected interval lie entirely within the arrangement — every depth-2 text
position from `c₀` up to the last cut is active (ASN-0084, R-PRE) — so the cuts
genuinely partition existing content rather than naming holes.

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

REARRANGE is the operation **REARRANGE_K** of ASN-0084, applied to the text
subspace at depth 2. We do not redefine it; we import its specification and erect
the system-level guarantees on top. For a 3- or 4-cut sequence `K` satisfying the
preconditions R-PRE, `REARRANGE_K(Σ, d)` produces the post-state `M'(d)` fixed by
ASN-0084's **PivotPostcondition** (`n = 3`) or **SwapPostcondition** (`n = 4`),
together with the frame conditions R-FRAME-P / R-FRAME-S. For the reader's
convenience we recall the destination equations — they are ASN-0084's, cited, not
introduced here. The pivot freezes the exterior, slides `β` to the front of the
interval, and lets `α` follow:

      v < c₀ ∨ v ≥ c₂  ⟹  M'(d)(v) = M(d)(v),                  (ASN-0084 R-EXT)
      M'(d)(c₀ + j)       = M(d)(c₁ + j),   0 ≤ j < w_β,        (ASN-0084 R-P1)
      M'(d)(c₀ + w_β + j) = M(d)(c₀ + j),   0 ≤ j < w_α.        (ASN-0084 R-P2)

The swap (four cuts) is the same shape with the middle region threaded between:

      v < c₀ ∨ v ≥ c₃  ⟹  M'(d)(v) = M(d)(v),                  (ASN-0084 R-EXT)
      M'(d)(c₀ + j)             = M(d)(c₂ + j),  0 ≤ j < w_β,   (ASN-0084 R-S1)
      M'(d)(c₀ + w_β + j)       = M(d)(c₁ + j),  0 ≤ j < w_μ,   (ASN-0084 R-S2)
      M'(d)(c₀ + w_β + w_μ + j) = M(d)(c₀ + j),  0 ≤ j < w_α.   (ASN-0084 R-S3)

ASN-0084 proves these define a total function whose induced map

      π : dom(M(d)) → dom(M(d)),   defined by   M'(d)(π(v)) = M(d)(v),

is a bijection that fixes the exterior and permutes the affected interval. Its
closed form is **R-PPERM** (pivot) and **R-SPERM** (swap); its totality and
bijectivity, together with the domain identity `dom(M'(d)) = dom(M(d))`, are
**R-PIV** and **R-SWP**. The destinations tile `[ord(c₀), ord(c_{n-1}))` exactly:
in the pivot, R-P1's destination ordinals occupy `[ord(c₀), ord(c₀)+w_β)` and
R-P2's occupy `[ord(c₀)+w_β, ord(c₀)+w_β+w_α)`, which abut and exhaust the
interval the two regions occupied before; with R-EXT covering the complement,
every position is assigned exactly once. We take these results as given and write

      dom(M'(d)) = dom(M(d))               **(P2, = ASN-0084 R-PIV / R-SWP)**

for the domain-preservation fact we lean on below. This is the formal content of
*transposition*: a reassignment of positions that loses none and invents none.

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

This is ASN-0084's range invariance R-RI restated; we label it **P1** for use
below. The document points at the same content after the rearrangement as before
— only the order of pointing has changed.

Two foundation invariants ride along on the same structural facts, and we
discharge them explicitly so that the hardest-to-maintain conjuncts of a
rearrangement are not left implicit. *Functionality* is preserved — `M'(d)` is
single-valued (ASN-0036, **S2**) — because the destinations of R-P1/R-P2 (pivot)
and R-S1/R-S2/R-S3 (swap) tile the affected interval *disjointly* (R-PIV/R-SWP),
so no V-position receives two I-addresses. *Referential integrity* is preserved —
`ran(M'(d)) ⊆ dom(C)` (ASN-0036, **S3**) — because by P1
`ran(M'(d)) = ran(M(d))`, and `ran(M(d)) ⊆ dom(C)` held in the pre-state, so the
inclusion is inherited verbatim. We may now read off the remaining obligations.

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
Conservation is immediate from P2. The active V-positions of the text subspace
`s_C` form a contiguous run by D-CTG, and `π` permutes that run onto itself, so
the run's cardinality and its endpoints are invariant:

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

## A worked transposition

We check the postconditions against explicit ordinals. Take a document `d` whose
text subspace holds five bytes "ABCDE" at the contiguous depth-2 positions
`[s_C, 1], …, [s_C, 5]`; write `a_k = M(d)([s_C, k])` for the I-address of the
k-th byte, so `ord([s_C, k]) = k`.

*Pivot.* Transpose the single-byte region `α = {B}` with the three-byte region
`β = {C, D, E}`: cuts `c₀ = [s_C, 2]`, `c₁ = [s_C, 3]`, `c₂ = [s_C, 6]`, giving
`w_α = ord(c₁) − ord(c₀) = 1` and `w_β = ord(c₂) − ord(c₁) = 3`. R-P1 fills the
front of the interval with `β` — `M'([s_C,2]) = a₃`, `M'([s_C,3]) = a₄`,
`M'([s_C,4]) = a₅`; R-P2 places `α` behind it — `M'([s_C,5]) = a₂`; R-EXT keeps
`M'([s_C,1]) = a₁`. The new reading order is

      A C D E B.

The postconditions check out numerically. The destination ordinals are `{2,3,4}`
(R-P1), `{5}` (R-P2), and `{1}` (R-EXT): pairwise disjoint and tiling `{1..5}`
exactly, so `π` is a bijection and `dom(M'(d)) = dom(M(d))` (**P2**). The range is
`{a₃, a₄, a₅, a₂, a₁} = {a₁, …, a₅} = ran(M(d))` (**P1**). The count is 5 and the
endpoints `ord 1`, `ord 5` are fixed (**P3**). Now a sample link footprint: let
`a*` be a link whose coverage holds the "C" byte `a₃`. Before the move its
footprint is `{[s_C,3]}`; since `[s_C,3] = c₁ + 0`, the pivot branch of `π` gives
`π([s_C,3]) = c₀ + 0 = [s_C,2]`, and indeed `M'([s_C,2]) = a₃`. The footprint
travels through `π` to `{[s_C,2]}` (**P7a**) — relocated, not lost.

*Swap.* Take "ABCDEF" at `[s_C,1..6]` and exchange `α = {B}` with `β = {E, F}`,
leaving the middle `μ = {C, D}` between them: cuts `c₀=[s_C,2]`, `c₁=[s_C,3]`,
`c₂=[s_C,5]`, `c₃=[s_C,7]`, so `w_α = 1`, `w_μ = 2`, `w_β = 2`. R-S1 brings `β`
to the front (`M'([s_C,2]) = a₅`, `M'([s_C,3]) = a₆`); R-S2 reseats `μ`
(`M'([s_C,4]) = a₃`, `M'([s_C,5]) = a₄`); R-S3 sends `α` to the back
(`M'([s_C,6]) = a₂`); R-EXT keeps `a₁`. The reading order is

      A E F C D B.

The middle departs `ord(c₁) = 3` and arrives `ord(c₀) + w_β = 4`, a net
displacement of `+1`, which is exactly `w_β − w_α = 2 − 1` — Gregory's `diff[2]`
(Question 11). Because `w_β > w_α`, the middle slides *forward* by precisely the
width imbalance, the unique shift that keeps `μ` contiguous between the relocated
`β` and `α`. Once more the destination ordinals `{2,3}`, `{4,5}`, `{6}`, `{1}`
tile `{1..6}` (**P2**), the range `{a₁, …, a₆}` is unchanged (**P1**), and the
extent is conserved (**P3**).

## Atomicity: two cuts at once

Why transpose *together* rather than move one region and later the other? The
single-operation form is interpreted against one arrangement, and this exposes
three ordering invariants (Question 6).

First, the document passes from one canonical total order directly to another. A
move-then-move realization manufactures an intermediate arrangement that is itself
a real, addressable, observable document state — "not a neutral scratch step." We
make this concrete on the worked pivot, whose net permutation carries
`A B C D E ↦ A C D E B` (atomic cuts `ord 2,3,6`). Realize the same `π` by two
successive pivots, each itself a legal `REARRANGE_K`:

      Move 1 (cuts ord 2,3,5):  A B C D E  ↦  A C D B E   = Σ_mid
      Move 2 (cuts ord 4,5,6):  A C D B E  ↦  A C D E B   = Σ'

We verify these arithmetically. Move 1 is a pivot of `α₁ = {B}` (ord 2) against
`β₁ = {C, D}` (ord 3,4): R-P1 gives `M_mid([s_C,2]) = a₃`, `M_mid([s_C,3]) = a₄`;
R-P2 gives `M_mid([s_C,4]) = a₂`; the exterior is frozen — order `A C D B E`.
Move 2 is a pivot of `{B}` (now ord 4) against `{E}` (ord 5): it exchanges those
two, yielding `A C D E B`. The composite reaches the same final arrangement as
the atomic pivot,

      M'(d) under T   =   M(d) under (T₁ ; T₂),                    **(P8a)**

because both realize the same `π` and the arrangement is determined by `π` applied
to the same content (P1). But the intermediate `Σ_mid = A C D B E` is a distinct,
observable arrangement realized by *neither* endpoint — concretely
`M_mid([s_C,4]) = a₂`, while `M([s_C,4]) = a₄` and `M'([s_C,4]) = a₅`, so

      M_mid(d) ≠ M(d)  ∧  M_mid(d) ≠ M'(d).                       **(P8b)**

A RETRIEVE issued between the two moves returns the order `A C D B E`, which has
no counterpart during the atomic transposition (Question 19). The existence of an
observable divergent intermediate is thus exhibited, not merely asserted: the
logical content of the final state is path-independent; the *visible history* is
not.

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

The post-state is fixed by naming each destination directly, and ASN-0084's
R-PIV (pivot) and R-SWP (swap) establish that those destinations tile the
affected interval exactly, so `π` is a bijection and the result is a legal
arrangement. We elevate this to a requirement on the operation: REARRANGE is
well-defined only when the induced map is a bijection of `dom(M(d))` onto itself
preserving the domain (P2). An alternative implementation must satisfy this no
matter how it computes positions.

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
| REARRANGE_K | Operation imported from ASN-0084: 3-/4-cut transposition in the text subspace at depth 2, specified by PivotPostcondition (R-EXT, R-P1, R-P2) or SwapPostcondition (R-EXT, R-S1, R-S2, R-S3) with frame R-FRAME-P/R-FRAME-S; this note builds the system-level guarantees below on top of it | imported (ASN-0084) |
| P0 (ContentPermanence) | `Σ'.C = Σ.C` — the content store is a verbatim frame; no I-address is created, destroyed, or rebound | imported (ASN-0084 R-FRAME-P/S) |
| P1 (IdentityCorrespondence) | `M'(d)(π(v)) = M(d)(v)`, hence `ran(M'(d)) = ran(M(d))` — I-addresses carried across the reassignment | imported (ASN-0084 R-RI) |
| P2 (Permutation) | The induced `π` (R-PPERM/R-SPERM) is a bijection of `dom(M(d))` onto itself; `dom(M'(d)) = dom(M(d))` | imported (ASN-0084 R-PIV/R-SWP) |
| S2 (FunctionalityPreserved) | `M'(d)` is single-valued — the disjoint tiling of destinations (R-PIV/R-SWP) gives each V-position one I-address (ASN-0036 S2) | preserved |
| S3 (ReferentialIntegrityPreserved) | `ran(M'(d)) ⊆ dom(C)` — by P1, `ran(M'(d)) = ran(M(d)) ⊆ dom(C)` (ASN-0036 S3) | preserved |
| P3 (VExtentConservation) | `\|dom(M'(d))\| = \|dom(M(d))\|`, and the active run's endpoints are fixed — the document's total extent is conserved | introduced |
| P5 (Discoverability) | Moved content is discoverable under its new V-position `π(v)` and resolves to its original I-address `M(d)(v)` | introduced |
| P6 (LinkStoreFrame) | `Σ'.L = Σ.L` — links are untouched; a link anchored in a moved region survives and travels with its content because endsets reference unchanged I-addresses | introduced |
| P7a (FootprintTransport) | `project(a, i, d, Σ') = π(project(a, i, d, Σ))` — a link's V-footprint is relocated through `π`; footprints split by a cut become discontiguous span-sets | introduced |
| P7b (DiscoverabilityPreserved) | `project(a, i, d, Σ') ≠ ∅ ⟺ project(a, i, d, Σ) ≠ ∅` — fragmentation never costs discoverability | introduced |
| P8a (FinalStateInvariance) | The atomic transposition and any two-move composite achieving the same net `π` reach the same final arrangement | introduced |
| P8b (IntermediateDivergence) | A two-move composite passes through an observable intermediate arrangement (exhibited: `A C D B E` for the worked pivot) realized by neither endpoint of the atomic transposition | introduced |
| P9 (DocumentIsolation) | `(∀ d' ≠ d :: M'(d') = M(d'))` together with P0, P6 — every other document, including transcluders of the rearranged I-addresses, is invariant | introduced |

## Open Questions

What must REARRANGE guarantee when a cut falls on a V-position that is shared, through transclusion, by more than one document, so that the cut is a boundary in one arrangement but interior to another?

Under what conditions may two rearrangements on the same document's content scope be applied without a serializing authority while leaving the final arrangement independent of their order?

What invariant must relate a content-based discovery index to the arrangement after a rearrangement, given that a link's footprint may fragment into arbitrarily many V-spans while its coverage is unchanged?

What must the operation guarantee about the recoverability of a prior arrangement from the permanent content store, given that REARRANGE records only the new V→I mapping and the old order is no longer expressed?

What relationship must hold between the displacement imposed on intervening content and the requirement that every subspace boundary be preserved, so that no permuted position may cross from one subspace into another?

What must a rearrangement guarantee about the well-formedness of a cut sequence whose affected interval reaches the document's first or last arranged position, so that no relocated position is carried outside the document's valid V-extent?
