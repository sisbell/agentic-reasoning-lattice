# ASN-0131: RETRIEVEENDSETS — Surfacing Anchoring Over a Content Region

*2026-06-13*

We have, by the time we reach this note, three stores in the system state
`Σ = (Σ.C, Σ.L, Σ.E, Σ.M, Σ.R)` (ASN-0047). The content store `Σ.C : T ⇀ Val`
(ASN-0036) maps I-addresses to immutable content. The arrangement family `Σ.M`, with
`Σ.M(d) : T ⇀ T` (ASN-0036), maps each V-position of a document `d` to the I-address it
currently occupies. The link store `Σ.L : T ⇀ Link` (ASN-0043) maps link addresses to
link values, where a link value is a sequence of at least three endsets (L3, ASN-0043)
and an endset is a finite set of well-formed spans (`Endset = 𝒫_fin(Span)`, ASN-0043). A
link does not anchor to a position; it anchors to *content* — its endsets reference
I-addresses, and `coverage(e)` (ASN-0098, ASN-0043) is the set of addresses an endset
denotes. This is why links survive editing: the strap is tied to the content's identity,
not to any document's current ordering of it.

We already possess, in the foundation, a query that asks of a region "what is reachable
here?" and answers with *link identities*: `findlinks_V(W, d, Σ)` (F-V, ASN-0127). The
present note studies its sibling. We ask the very same question of a region — *what
touches here?* — but we demand a different answer. We do not want the names of the links.
We want the *anchoring itself*: the endsets, the spans where links attach. We want to be
told **that** this content is bound, and **how** it is bound — at which spans, on which
side of the link — without being told **which** links bind it. Why one would want such
an answer; what it can and cannot certify; and what it must guarantee as the document
beneath it is edited and as links are withdrawn — these are the questions of this note.

We name the operation `RETRIEVEENDSETS`, after the FEBE operation that realises it, and
write `RE(W, d, Σ)` for its result.

## The region, and what it resolves to

A region is not a set of I-addresses handed to us directly. One asks the question *of a
place in a document* — "of this passage, what anchoring touches it?" — and the system
must first discover what content presently occupies that place. So a region is a pair
`(W, d)` with `d ∈ dom(Σ.M)` a document and `W ⊆ T` a set of V-positions, which we require
to lie in the **content subspace**: `(∀ v ∈ W : subspace(v) = s_C)`, where `subspace(v) =
v₁` is the V-position's subspace identifier and `s_C` the content one (ASN-0047). These are
the text positions of `d` — typically the V-positions of a span in `d`'s text. The
restriction is a caller obligation, not a check the operation performs. Its **content-image** is

> `I = image(W, d, Σ) = {Σ.M(d)(v) : v ∈ W ∩ dom(Σ.M(d))}`     (F-IMG, ASN-0127),

the I-addresses that the region's V-positions currently map to through `d`'s
arrangement. Because every `v ∈ W` carries `subspace(v) = s_C`, generalized referential
integrity places the image in content: `I ⊆ dom(Σ.C)` (S3★, ASN-0047). We do not rebuild
this machinery — it is ASN-0127's, and we lean on it: the region is resolved to content
through the present arrangement, and everything downstream is phrased in I-addresses, where
links live.

## When does an endset touch the region?

Fix the region `(W, d)` and its image `I`. We must say, of a single endset `e`, what it
is for `e` to *touch* the region. The endset denotes `coverage(e) ⊆ T` (ASN-0098). The
region denotes `I ⊆ T`. We are looking for the weakest relation between these two sets
that faithfully captures "this anchoring reaches into the region."

Consider the candidates. *Containment* — `coverage(e) ⊆ I` — would require the entire
endset to lie inside the region. But this is plainly too strong, and we can see why by
asking what it would discard. An endset may cover a whole chapter and intersect our
one-line region in a single place; under containment we would not surface it, yet its
anchoring manifestly reaches our line. Worse, an endset straddling the region boundary —
covering content both inside and outside `W` — would be silently dropped, when it is
exactly such an anchoring we most want to see. Containment answers a different question
("which anchorings live *wholly within* here?"), not ours.

The relation we want is *overlap*: the endset touches the region exactly when it covers
at least one address the region also covers. We define, for the fixed region,

> `touch_W(e)  ≡  coverage(e) ∩ image(W, d, Σ) ≠ ∅`

— the subscript naming the region's V-position set `W`, the one parameter that varies when
we later compose regions.

Three properties of this definition are worth stating, because each is a claim an
alternative implementation would also have to honour.

First, **overlap, not containment**. A single shared address suffices; partial overlap
is real contact. The endset need not lie inside the region, and the region need not lie
inside the endset. This is the disjunction Nelson phrases as matching "all or any part
of" the requested set: one span falling within the region qualifies the endset.

Second, the relation is **existential within an endset**. An endset is a finite *set* of
spans, possibly discontiguous (ASN-0043). `touch_W(e)` asks that *some* address in
`coverage(e)` lies in `I` — not that every span does. The other spans of a touching
endset legitimately point elsewhere; they do not disqualify it, and (as we shall see)
they are not clipped away from it.

Third, the relation is **per-endset, not per-link**. We judge each endset on its own
coverage against the region. A link carries several endsets — by convention a from-endset
`e₁`, a to-endset `e₂`, a type-endset `e₃`, and possibly more (L3). RETRIEVEENDSETS asks
its one region of *each* endset independently. A link's from-endset may touch while its
to-endset points to a destination far outside `W`; then the from-endset is surfaced and
the to-endset is not. There is no four-set request here differentiating slot from slot
(that is the richer FINDLINKSFROMTOTHREE); there is one region, tested against every
endset, and the endsets that touch are the ones surfaced.

The touch test is decidable, so the operation is a realisable query and not merely a
defined set. The image `I = image(W, d, Σ)` is a *finite* set of I-addresses — the forward
image of `W` under `Σ.M(d)`, whose domain is finite (S8-fin, ASN-0036). We settle
`touch_W(e) ≡ coverage(e) ∩ I ≠ ∅` by testing each of the finitely many members of `I` for
membership in `coverage(e)`. Membership `t ∈ coverage(e)` is decidable span-by-span:
`coverage(e)` is a finite union of half-open T1-intervals (T12, ASN-0034), so
`t ∈ [s, s ⊕ ℓ)` is the two intrinsic comparisons `s ≤ t < s ⊕ ℓ` (T2, IntrinsicComparison,
ASN-0034). The addressability filter is decidable on the same footing: `nullified(Σ)` is a
computable set (ASN-0086), so membership in `addressable(Σ) = dom(Σ.L) ∖ nullified(Σ)` is
settled without enumerating history. With `I` finite (S8-fin, ASN-0036), `dom(Σ.L)` finite
(L-fin, ASN-0093), and both the touch test and the addressability filter decidable over
these finite sets, the answer is a finite, computable object.

## The unit of the answer: anchoring without names

Now we can state what RETRIEVEENDSETS returns. We must first settle which links it ranges
over. A link, once created, is permanent and immutable in the store (L12, ASN-0043) — but
the system admits *retraction*, recorded not by deleting the link but by emitting a
withdrawal link that marks the target nullified (ASN-0086). A withdrawn link's anchoring
should not be reported as live (we argue this below). So we range over the links that are present and
not withdrawn — the **addressable** links:

> `addressable(Σ) = dom(Σ.L) ∖ nullified(Σ)`     (over ASN-0086's `nullified`).

The operation surfaces, for each addressable link and each of its endsets that touches
the region, that endset, tagged by the slot it occupies:

> `RE(W, d, Σ)  =  { (i, e) : (∃ a : a ∈ addressable(Σ) : 1 ≤ i ≤ |Σ.L(a)| ∧ Σ.L(a).eᵢ = e ∧ touch_W(e)) }`.

The answer is a set of `(role, endset)` pairs. Each pair names the slot `i` — from, to,
type, or higher — and the endset value `e` that occupies it in some touching link.

Read what this definition does, and as importantly, what it withholds. It **withholds the
link address `a`**. The existential `(∃ a : …)` consumes the link and discards it; what
escapes into the answer is `(i, e)`, the anchoring structure, never the identity. This is
the defining character of the operation: it surfaces *that* anchoring is present, and its
shape, without ever naming the anchored link. Two distinct links sharing an identical
endset value in the same slot — permitted, since the link store is non-injective (L11b,
ASN-0043) — collapse to a single pair `(i, e)`. The answer therefore does not let one
count the links, recover their identities, or — and this is the deeper limit — *pair* a
surfaced from-endset with the to-endset of the same link. A from-span and a to-span may
both appear in the answer, drawn from one link, yet the answer carries nothing that binds
them as one link's two ends. The anchoring is laid bare; the connection is not made
followable.

It is worth recording what the operation reads and what it does not. `RE` reads the
arrangement `Σ.M(d)` (to form the image) and the link store `Σ.L` (for endsets, and,
through `nullified`, for addressability). It never consults the content *values* `Σ.C`,
the entity set `Σ.E`, or the provenance relation `Σ.R`. And it is a pure query: it reads
state and changes none — `Σ' = Σ`. Whatever anchoring it reports, it reports as a fact
about the state it found, leaving that state untouched.

Three degenerate inputs are worth reading straight off the definition, because each fixes
a corner an alternative implementation must also get right.

- *Empty image.* When `W ∩ dom(Σ.M(d)) = ∅` — the region selects no arranged position, as
  for a freshly registered document whose arrangement is still empty (`dom(Σ.M(d)) = ∅`) —
  the image is `I = ∅`, so `touch_W(e) ≡ coverage(e) ∩ ∅ ≠ ∅` is false for *every* endset,
  and `RE(W, d, Σ) = ∅`. A region resolving to no content touches no anchoring.

- *No addressable links.* When `addressable(Σ) = ∅` — the store holds no links, or every
  link present is nullified — the existential `(∃ a ∈ addressable(Σ) : …)` in RE-DEF has no
  witness, so `RE(W, d, Σ) = ∅` whatever the region. Anchoring can only be surfaced from a
  live link.

- *Empty endset slot.* An endset may itself be empty: ASN-0043 admits `∅` in the from- and
  to-slots, and only the type-slot is required non-empty (L3, ASN-0043). Since
  `coverage(∅) = ∅`, `touch_W(∅)` is false against any region, so an empty slot is *never*
  surfaced. The operation reports anchoring only where some span genuinely covers a region
  address.

## Faithfulness: the surfaced endset is the link's own, unclipped

A returned endset must be the link's *actual* anchoring, not an approximation of it, and
not a fragment of it trimmed to the region. Two demands sharpen this.

The first is **faithfulness of provenance**: every `(i, e) ∈ RE(W, d, Σ)` is a genuine
slot-`i` endset of some addressable link, with `e` touching the region. The operation
fabricates no anchoring. This is immediate from the definition — the existential
witnesses a real `a` with `Σ.L(a).eᵢ = e` — but it is the substantive contract: a reader
who receives `(1, e)` may rely that some live link really attaches its from-end at the
spans of `e`, and that those spans really reach the region.

The second concerns **extent**, and here we must separate two invariants of different
strength, because the operation rests squarely on one and merely adopts the other.

The load-bearing invariant is **no clipping (RE-CLIP)**: whatever span the answer
reports, it reports at the full extent recorded in the link, never truncated to the
region boundary. The reasoning is Nelson's, and it is decisive: clipping would
*misrepresent the anchoring*. An endset whose span straddles the region boundary would be
reported as a shorter span than the link actually attaches to — a falsehood about the
link's grip. One searches *from* a region in order to learn the true shape of what
attaches there, including how far it reaches beyond; to clip would be to answer that
falsehood. So no reported span is ever shortened to fit the query, and this holds under
*every* reading of the operation.

The reading we *adopt* makes a stronger, separable commitment — **whole-endset surfacing
(RE-WHOLE)**: we return `e = Σ.L(a).eᵢ` in full, *all* of its spans, not merely the slice
of `e` whose spans fall inside `W`. A discontiguous endset is then surfaced with the spans
pointing outside the region intact, since those are precisely the parts that say where
else this anchoring lives. But this is a *convention*, not a forced consequence: an
implementation that surfaces only the touching spans of a touching endset — economical,
volunteering less of the anchoring's extent — would still honour no clipping, violating
only whole-endset surfacing. Whether entirety is demanded, or only the touching spans, is
reopened as Open Question 1; we therefore hold RE-WHOLE **provisional** pending its
resolution, while RE-CLIP stands firm under either answer.

## Soundness and completeness: the answer is exactly the touching anchoring

The definition is a biconditional, and its two directions are the operation's correctness
contract.

**Soundness** is the forward direction: if `(i, e) ∈ RE(W, d, Σ)`, then `e` is a genuine
slot-`i` endset of an addressable link and `touch_W(e)` holds. Nothing in the answer fails
to reach the region; no anchoring is reported that does not actually grip the content
asked about. This is the half that makes the answer trustworthy as a structural claim
about the literature: *this reaches here*, never the mere appearance of reach. A reported
overlap is a true overlap — some address of `e` genuinely lies in the region's image.

**Completeness** is the converse: for every addressable link `a` and every slot `i` with
`touch_W(Σ.L(a).eᵢ)`, the pair `(i, Σ.L(a).eᵢ)` is in `RE(W, d, Σ)`. Every endset that
touches the region — by direct anchoring or, as we shall see, through transcluded content
— appears; none is silently omitted. The result is *exactly* the touching set: neither
more (soundness) nor less (completeness). An implementation that returned a strict subset,
or admitted a near-miss, would not be realising this operation.

These two together are the whole of the operation's relation to the region: it surfaces
the touching anchoring, all of it and only it.

## A worked instance

It is worth grounding these claims in a state small enough to compute by hand, yet
arranged to exercise every distinctive postcondition at once. Let `d ∈ dom(Σ.M)` arrange
four pieces of text content at consecutive V-positions of its text subspace (`s_C = 1`):

> `Σ.M(d) = { [1,1] ↦ a₁,  [1,2] ↦ a₂,  [1,3] ↦ a₃,  [1,4] ↦ a₄ }`,

with `a₁ < a₂ < a₃ < a₄` four content I-addresses in `dom(Σ.C)`, consecutive siblings
under `d`'s content sub-allocator (so `a₂ = shift(a₁, 1)`, `a₃ = shift(a₂, 1)`,
`a₄ = shift(a₃, 1)`). Two links inhabit the store. The first, at address `ℓ₁`, is the
standard triple `L₁ = (e₁, e₂, e₃)`:

- from-endset `e₁ = {(a₂, δ(2, #a₂)),  (a₄, δ(1, #a₄))}` — a *discontiguous* endset of two
  spans, one touching the region we are about to draw and one pointing wholly outside it.
  Its first span is width-2 ordinal, reaching from `a₂` across its successor so that
  `{a₂, a₃} ⊆ coverage(e₁)` (the upper bound is exclusive, so this span stops short of
  `a₄`); it *straddles the region boundary*, covering `a₂`, which the region will hold, and
  `a₃`, which it will not. Its second span is unit-depth at `a₄`, with
  `coverage({(a₄, δ(1, #a₄))}) = {t : a₄ ≼ t}` (PrefixSpanCoverage, ASN-0043), reaching
  only `a₄` and its descendants — content the region does not reach;
- to-endset `e₂ = {(a₁, δ(1, #a₁))}` — with `coverage(e₂) = {t : a₁ ≼ t}`
  (PrefixSpanCoverage, ASN-0043), containing none of `a₂`, `a₃`, `a₄` (each is a sibling of
  `a₁`, not a descendant);
- type-endset `e₃ = {(θ, δ(1, #θ))}` — `θ` a classifying address in a *type* subspace,
  T4-valid and element-level (`zeros(θ) = 3`) with subspace identifier `E(θ)₁ = s_type ≠
  s_C`, non-empty as L3 demands. Its coverage `coverage(e₃) = {t : θ ≼ t}`
  (PrefixSpanCoverage, ASN-0043) is disjoint from content — the example needs exactly
  `coverage(e₃) ∩ dom(Σ.C) = ∅` — and the argument runs over content addresses alone, the
  only addresses we intersect `coverage(e₃)` with. Take any `c ∈ dom(Σ.C)`: by S7b (ASN-0036)
  it is T4-valid with `zeros(c) = 3`, and by content allocation `E(c)₁ = s_C` (L0,
ASN-0093). Were `c ∈
  coverage(e₃)`, i.e. `θ ≼ c`, then `c` agrees with `θ` on positions `1..#θ` (Prefix,
  ASN-0034). The agreement carries all three of `θ`'s separator zeros onto `c`; as `c` has
  only three zeros in all (`zeros(c) = 3`), these *are* `c`'s separators, so `θ` and `c`
  share a third-zero position and hence a subspace-identifier position one past it — forcing
  `E(c)₁ = E(θ)₁ = s_type`. But content allocation gave `E(c)₁ = s_C ≠ s_type` — a
  contradiction. So no content address extends `θ`, giving `coverage(e₃) ∩ dom(Σ.C) = ∅`.

The second, at a distinct address `ℓ₂ ≠ ℓ₁`, is `L₂ = (e₁, e₂′, e₃′)`: it carries the
*same from-endset value* `e₁` in slot 1, which the non-injective store permits (L11b,
ASN-0043). Its remaining two slots we leave abstract but constrain exactly where the
argument needs it — both *miss the region we draw below*:

> `coverage(e₂′) ∩ {a₂} = coverage(e₃′) ∩ {a₂} = ∅`

(equivalently, neither `e₂′` nor `e₃′` covers `a₂`). Concretely one may take `e₂′ = e₂`
and `e₃′ = e₃`, making `L₂` a value-identical twin of `L₁` — which L11b permits, the
distinct address notwithstanding — but the analysis below uses only the stated
disjointness. Both links are addressable.

We ask of the single middle position, `W = {[1,2]}`. The region resolves to its image

> `I = image(W, d, Σ) = { Σ.M(d)([1,2]) } = {a₂}`.

Run the touch test against each endset in play:

- `touch_W(e₁) = coverage(e₁) ∩ {a₂}`. Since `a₂ ∈ coverage(e₁)` — via the first, width-2
  span — this is non-empty: `e₁` **touches**, through `a₂`. Its other covered addresses lie
  outside the region: `a₃` (also under the first span) and `a₄` together with its
  descendants (under the second span); none helps or hinders the test.
- `touch_W(e₂) = {t : a₁ ≼ t} ∩ {a₂} = ∅` — `e₂` reaches `a₁`, arranged at `[1,1] ∉ W`,
  and does not reach `a₂`; it **misses**.
- `touch_W(e₃) = {t : θ ≼ t} ∩ {a₂} = ∅` — `a₂ ∈ dom(Σ.C)` and `coverage(e₃) ∩ dom(Σ.C) = ∅`,
  so `a₂ ∉ coverage(e₃)`; it **misses**.
- `touch_W(e₂′) = coverage(e₂′) ∩ {a₂} = ∅` and `touch_W(e₃′) = coverage(e₃′) ∩ {a₂} = ∅`
  — directly by the disjointness stipulated on `L₂`'s two non-from slots; both **miss**.

The only endset that touches the region is `e₁`, carried in slot 1 by both `ℓ₁` and `ℓ₂`;
every other slot of either link — `e₂`, `e₃`, `e₂′`, `e₃′` — misses. The answer is
therefore a single role-tagged endset,

> `RE(W, d, Σ) = { (1, e₁) }`,

and each of the operation's distinctive claims can be read off it directly:

- **Overlap, not containment (RE-OVL).** `e₁` is surfaced although `coverage(e₁) ⊋ I` — it
  covers `a₃` and `a₄`, which the region does not. A single shared address, `a₂`, sufficed.
  Under a containment test (`coverage(e₁) ⊆ I`) the from-endset would have been wrongly
  discarded, precisely because it straddles the boundary.
- **Unclipped extent (RE-CLIP).** The touching (first) span of the surfaced `e₁` is
  returned at its full recorded extent — the width-2 span `(a₂, δ(2, #a₂))`, reaching
  across `a₃` — not trimmed to the region. A clipping implementation would have returned
  the width-1 span `(a₂, δ(1, #a₂))` covering `a₂` alone, falsely shrinking the link's grip
  to fit the query. No-clipping holds under *either* reading of the operation: both the
  whole-endset and the touching-spans-only readings return this touching span unclipped.
- **Whole-endset surfacing (RE-WHOLE).** The surfaced `e₁` is returned *entire* — both
  spans, including the unit span at `a₄`, which touches nothing the region holds. Here the
  reading is exercised in earnest, and its distinctive consequence is concrete: the answer
  volunteers anchoring — `a₄` and its descendants — that points *wholly outside* the
  queried region. This is exactly where the two readings part, and where RE-CLIP alone
  cannot separate them: a *touching-spans-only* implementation would surface only the
  touching span, returning `{(a₂, δ(2, #a₂))}` — honest about extent (RE-CLIP) yet silent
  about the `a₄` span — whereas the *whole-endset* reading we adopt returns
  `{(a₂, δ(2, #a₂)),  (a₄, δ(1, #a₄))}` in full.
- **Per-endset surfacing (RE-OVL).** Only slot 1 appears, and from each link separately. Of
  `L₁`, the to-endset `e₂` and the type-endset `e₃` miss the region and are absent, so the
  link's from-end is reported without its to-end. Of `L₂`, the two non-from slots `e₂′` and
  `e₃′` likewise miss — by the disjointness stipulated above — leaving only its shared
  slot-1 `e₁` to contribute. No slot but the first survives the touch test, from either
  link.
- **Anchoring without names (RE-UNIT).** `ℓ₁` and `ℓ₂` both bear `e₁` in slot 1; they
  contribute the *one* pair `(1, e₁)`, which appears once. The answer holds no `ℓ₁`, no
  `ℓ₂`, no count. From `{(1, e₁)}` alone one cannot tell that two links grip here, cannot
  recover either identity, and cannot learn that `e₁`'s links also anchor a to-end at `a₁`
  — the from-end is laid bare; the connection is not made followable.

## Composing regions: union-distributivity

One naturally asks whether a region query decomposes — whether asking of `W₁ ∪ W₂` is the
same as asking of `W₁` and of `W₂` separately and taking the union. For unions it is, and
the proof is short, because it rests on a property the forward image enjoys
unconditionally.

The image of a union is the union of images:

> `image(W₁ ∪ W₂, d, Σ) = image(W₁, d, Σ) ∪ image(W₂, d, Σ)`,

with no injectivity hypothesis. This is immediate from the definition: writing
`f = Σ.M(d)`, we have `image(W, d, Σ) = {f(v) : v ∈ W ∩ dom(f)}`, and
`(W₁ ∪ W₂) ∩ dom(f) = (W₁ ∩ dom(f)) ∪ (W₂ ∩ dom(f))`, so the comprehension over the union
is the union of the comprehensions. (A forward image always distributes over union; it is
*intersection* it fails to respect, as we note below.)

The touch test then distributes as a disjunction. The subscript on `touch_W` (the
predicate fixed above) names the region it tests against, so it specialises to each
sub-region — `touch_{W₁}`, `touch_{W₂}` — and to their union,

> `touch_{W₁ ∪ W₂}(e) ≡ coverage(e) ∩ (image(W₁, d, Σ) ∪ image(W₂, d, Σ)) ≠ ∅ ≡
> touch_{W₁}(e) ∨ touch_{W₂}(e)`,

since a set meets a union of sets exactly when it meets one of them. Now `RE` selects each
*available* slot-endset by exactly this test — and the pool of available pairs,
`Avail(Σ) = { (i, e) : (∃ a ∈ addressable(Σ) : 1 ≤ i ≤ |Σ.L(a)| ∧ Σ.L(a).eᵢ = e) }`, is a
function of `(Σ.L, nullified(Σ))` and does not depend on the region. So

> `RE(W₁ ∪ W₂, d, Σ) = { (i, e) ∈ Avail(Σ) : touch_{W₁ ∪ W₂}(e) }
>   = { (i, e) ∈ Avail(Σ) : touch_{W₁}(e) ∨ touch_{W₂}(e) }
>   = RE(W₁, d, Σ) ∪ RE(W₂, d, Σ)`.

This is the RETRIEVEENDSETS analogue of the discovery query's union-distributivity
(F-UDIST, F-VDIST, ASN-0127): a region query is composable from any cover of the region by
its parts. Querying a passage is the union of querying its lines.

The *intersection* law does not follow, and for a structural reason worth recording. The
forward image does not distribute over intersection: in general
`image(W₁ ∩ W₂, d, Σ) ⊆ image(W₁, d, Σ) ∩ image(W₂, d, Σ)`, but the inclusion can be
strict, because distinct V-positions may map to the *same* I-address — the arrangement is
non-injective (M13, M14, ASN-0058). A position in `W₁ ∖ W₂` and a position in `W₂ ∖ W₁`
can share an I-address that then lies in both images, hence in the right-hand
intersection, while contributing nothing to `image(W₁ ∩ W₂, d, Σ)`. Intersection-
composability is therefore a genuinely separate question, and we leave it open.

## Existence and discoverability: which side does this answer for?

We now reach the conceptual heart. The content-region link query foundation draws a sharp
line (ASN-0127, *Anchoring: existence vs discovery*) between two ways the I-address
argument to a link query can be obtained, and the choice fixes the temporal character of
the answer: an **existence** query takes a *fixed* `I ⊆ T` and answers a monotone,
*historical* property of the permanent store (E-MONO, D-ZERO, ASN-0127), while a
**discovery** query resolves its `I` *through a document's current arrangement* and answers
a non-monotone, *present-tense* reading of it (D-NONMONO, D-ZERO, ASN-0127). We cite that
taxonomy rather than rebuild it; the contribution here is to place RETRIEVEENDSETS on it.

RETRIEVEENDSETS takes a region `(W, d)` and resolves it through `image(W, d, Σ)`. **It is
discovery-anchored.** Its selection of which links contribute is exactly the discovery
query, filtered to the addressable:

> `sel(W, d, Σ) = { a ∈ addressable(Σ) : (∃ i : touch_W(Σ.L(a).eᵢ)) } = findlinks_V(W, d, Σ) ∩ addressable(Σ)`,

because `findlinks_V(W, d, Σ) = {a ∈ dom(Σ.L) : (∃ i : coverage(Σ.L(a).eᵢ) ∩ image(W,d,Σ) ≠ ∅)}`
(F-V, F-FIND, F-MATCH, ASN-0127). So the links whose endsets RETRIEVEENDSETS surfaces are
precisely the addressable links discoverable through the region — and the operation
inherits the discovery side's temporal character wholesale: present-tense, non-monotone,
arrangement-mediated. A RETRIEVEENDSETS zero — *no anchoring surfaced* — is therefore a
statement of the present (nothing is reachable through this region as it now stands), not
of history (D-ZERO, ASN-0127). The anchoring may well exist, permanently, in links whose
content the region no longer arranges.

This sits in apparent tension with the designer's reading, which calls the operation a
report of *existence* rather than *discoverability*. The designer and the foundation are
slicing different axes.

- The foundation's axis is the **query mode**: is the I-argument a fixed set (existence)
  or read from the live arrangement (discovery)? On this axis RETRIEVEENDSETS is squarely
  discovery — it consults `d`'s present arrangement.

- The designer's axis is the **deliverable**: does the answer *name the links*, making
  them followable, or does it merely surface *that anchoring is present* and its shape?
  To be *shown* a connection — in the designer's sense — is to have it named and made
  followable. RETRIEVEENDSETS withholds the names; one cannot follow an endset one cannot
  name, nor pair a from-end with its to-end. So on the deliverable axis the operation
  reports the **existence of anchoring** — the content-level fact "links are bound here,
  thus" — without delivering followable discovery.

The two axes are orthogonal, and RETRIEVEENDSETS lands on a definite corner of each: its
**query is discovery-anchored** (present-tense, arrangement-resolved — the foundation's
discovery side), while its **deliverable is existence-of-anchoring** (structure without
identity — the designer's existence reading). It uses the discovery machinery to answer an
existence-of-anchoring question. The right one-line characterisation is: *RETRIEVEENDSETS
reads, off the region's present arrangement, the presence and shape of the anchoring that
touches it — and stops short of the identities that would make that anchoring followable.*

## Anchoring reached through borrowed content

A region need not hold content native to its own document. Through transclusion, `d` may
window content whose home is another document `d_src`; the windowed content is not a copy
but the *same content*, sharing its I-addresses with the home (ASN-0036). The question
arises: if a link resides in `d_src` (or anywhere), and reaches our region only because
`d` windows the link's content, must RETRIEVEENDSETS surface that link's endset — and must
it treat such borrowed-content anchoring the same as anchoring on native content?

It must, and the reason is structural: anchoring is keyed to *content identity*, and our
query is keyed to *content identity*. The endset covers I-addresses; the region's image is
I-addresses; `touch_W` intersects them. Nothing in the test consults where the link lives,
where the content is "native," or which document windows it. The discovery query is
document-blind in exactly this sense: discoverability of a link through `d` "turns solely
on `coverage ∩ ran(Σ.M(d))`," independent of the link's home and of the origin of the
covered content (LP16, ASN-0098). So if `d`'s arrangement maps the region's V-positions to
I-addresses an endset covers, that endset touches the region — whether those I-addresses
are native to `d` or borrowed from `d_src`. A link reaching the region through transcluded
content is surfaced **identically** to one reaching native content; the operation cannot
and does not distinguish them, because at the level of content identity there is nothing
to distinguish.

This forces what the returned span must *describe*. The endset's spans are over content
identity — the I-addresses of the content's permanent home — not over the V-positions
where `d` currently displays the borrowed content. Were the span to name the borrowing
position, it would name a coordinate local to `d`, transient and meaningless to any other
document windowing the same content; the anchoring would fracture into one description per
window and break the moment `d` re-edited. Because the span names content identity, a
single endset is the *same* endset no matter which window reaches it — the same anchoring
seen through `d` and through `d_src` and through every co-transcluder. This is the
property that lets one make a link against borrowed content and have it hold, automatically,
on the original and on every other document that includes those bytes.

A delicate consequence: the *content-level* answer — which content (which I-addresses)
each surfaced endset anchors to — is invariant. The endset's coverage is permanent: links
are immutable (L12, ASN-0043), and no transition alters an endset's coverage (LP3,
ASN-0098). What the region's image maps to, and how that image is positioned within `d`'s
order, are present-tense; but the identity of the anchored content, once surfaced, is a
fixed fact about a permanent link. The operation's content-level answer is therefore
arrangement-independent even though its *selection* of which endsets to surface is
arrangement-mediated.

## Stability: the answer as the document is edited

Because the operation is a pure function of the present state, resolved through the
present arrangement, its stability is entirely determined by how state changes move the
two things it reads: the region's image and the addressable population.

**Determinism first.** `RE(W, d, Σ)` is a function of `(W, d, Σ)` and nothing else — no
hidden state, no dependence on the order or time of asking. Asking the same region twice
with no intervening state change returns the same anchoring both times. This is the
bedrock under everything that follows: every *change* in the answer is the image of a
*change* in `Σ`.

**Under editing of the queried document.** The region resolves through `Σ.M(d)`, so
editing `d`'s arrangement moves the image, and the answer tracks it — present-tense,
non-monotone (D-NONMONO, ASN-0127). The three editing motions act as one would expect of
a faithful tracker:

- *Insertion* into the region brings new content under `W`'s positions; the *region image*
  grows (F-IMG-MONO, ASN-0127), and endsets covering the newly-arranged content newly touch
  the region — the touch test composing on top of the larger image — and are surfaced.
  Anchoring that was always there in the store becomes *reachable* here without any link
  being created.

- *Deletion* of region content unmaps its I-addresses from `d`'s arrangement; the *region
  image* shrinks (F-IMG-CONTR, ASN-0127), and endsets that touched only through the
  departed content cease to be surfaced — the contracted image no longer meets their
  coverage, so the touch test fails where it formerly held (the contraction direction of
  LP10 and the discoverability characterisation LP12, ASN-0098). The link persists in the
  store (L12, ASN-0043), its endset coverage unchanged; it is merely no longer reachable
  *through this region of `d`*. This is a region-local loss of reach, **not** the global
  *orphaning* of LP17 (ASN-0098), whose premise — that the content is reachable from *no*
  document — a single-region deletion does not establish: the link may still touch other
  regions of `d`, or be reachable from other documents. Should the content be re-arranged
  into `d`, the region image grows again (F-IMG-MONO, LP9, ASN-0098) and the endset is
  surfaced once more. The genuinely global *orphaning* of LP17 — and the *resurrection* of
  LP18 (ASN-0098) on later re-arrangement — obtains only in the limiting case where the
  departed content comes to be arranged by no document at all.

- *Rearrangement* permutes the region's V-positions over the same content; the *region
  image*'s membership can swing (F-IMG-SWING, ASN-0127). This is the *only* way a
  rearrangement changes the answer. Which `(i, e)` pairs are surfaced may change, as the
  image swings and some endset newly meets it or ceases to; but each surfaced endset's
  coverage is permanent (RE-IDENT), so under `K.μ~` no surfaced endset's spans change
  shape — the answer moves by *membership alone*. (A *rendered* answer — one resolved into
  `d`'s present V-order rather than content identity, where piecewise displacement could
  fragment a contiguous run (ASN-0082) — is the mode deferred to Open Question 3; the
  content-identity answer returned here is unaffected.)

Through all of this the invariant of the previous section holds: the *content identity* of
each surfaced endset never moves, and it is that identity RETRIEVEENDSETS returns. What
changes under editing is only *which* endsets are reachable through the region — the
membership of the answer — never the spans of an endset the answer carries; how the
content sits in `d`'s present order is a fact about the V-order display, not about these
content-identity spans.

Editing of *other* documents does not perturb the answer: the image reads only `Σ.M(d)`,
and a transition touching `d' ≠ d` leaves `Σ.M(d)` fixed (LP5, ASN-0098). Three further
transition kinds leave the answer fixed for the same root reason — each touches none of the
state `RE` reads (RE-LOC). Content allocation `K.α` touches neither `Σ.M` nor `Σ.L` (frame
`M' = M; L' = L`, ASN-0093) and so changes no projection (LP6, ASN-0098); a freshly
allocated I-address enters no region image without a separate arrangement edit. Entity
creation `K.δ` — registering a new node, account, or document `e ≠ d` — leaves `Σ.M(d)`
untouched (wholly, for node/account creation, where `M' = M`; and on every pre-existing
arrangement, for document registration, LP8, ASN-0098) and leaves `Σ.L` fixed (frame), so
neither the image nor the available pool moves. Provenance recording `K.ρ` writes only
`Σ.R` (ASN-0047), which `RE` never reads (RE-LOC), so it cannot move the answer (LP14,
ASN-0098).

Finally, one arrangement edit to `d` *itself* leaves a content-region answer fixed — by a
route particular to the content-subspace restriction rather than to locality. The
link-subspace extension `K.μ⁺_L` adds a single V-position `v_ℓ` with `subspace(v_ℓ) = s_L`,
mapped to a link address (ASN-0047). Because `W ⊆ s_C`, we have `v_ℓ ∉ W`, so the selecting
set `W ∩ dom(Σ.M(d))` — and with it the image `image(W, d, Σ)` — is unchanged
(F-IMG-MONO sharpened to equality under `W ⊆ s_C`, ASN-0127); and its frame leaves `Σ.L`
fixed (`L' = L`), so the available pool does not move either. It is the one arrangement edit
on `d` that cannot perturb a content-region answer, and the content-subspace restriction is
exactly what secures it.

**The weakest precondition for contraction-stability.** The qualitative tracking above can
be made exact for one editing motion — a deletion. Fix a `K.μ⁻[d, R]` step on the queried
document: a contraction retaining exactly the arrangement positions in the retention set
`R` (ASN-0047) — a set of V-positions, distinct from the provenance relation `Σ.R` of the
same ASN, which `RE` never reads (RE-LOC) — with `enabled(K.μ⁻[d, R])` its applicability
condition. We ask the natural non-trivial
stability question: under what precondition on `Σ` does this step leave `RE(W, d, ·)`
*unchanged*? Two observations narrow it.

First, `K.μ⁻` touches only `Σ.M(d)`; its frame leaves `Σ.L`, and hence `nullified(Σ)`,
fixed. So the *available* pairs `Avail(Σ) = { (i, e) : (∃ a ∈ addressable(Σ) :
1 ≤ i ≤ |Σ.L(a)| ∧ Σ.L(a).eᵢ = e) }` are identical pre- and post-state; only the `touch_W`
filter can move. Second, contraction only shrinks the image. By the bridge of D-CWP
(ASN-0127), `image(W, d, Σ') = I_R` where `I_R = {Σ.M(d)(v) : v ∈ W ∩ R}`; writing
`Δ = image(W, d, Σ) ∖ I_R` for the dropped I-addresses, `I_R ⊆ image(W, d, Σ)`. A touch
against the smaller post-image therefore implies a touch against the pre-image, so
`RE(W, d, Σ') ⊆ RE(W, d, Σ)` unconditionally. "Unchanged" reduces to "nothing dropped."

A pair `(i, e)` is dropped exactly when its endset touched the region *only* through the
departing addresses — `coverage(e) ∩ image(W, d, Σ) ≠ ∅` (surfaced pre) yet
`coverage(e) ∩ I_R = ∅` (gone post), which together say `coverage(e) ∩ Δ ≠ ∅` and
`coverage(e) ∩ I_R = ∅`. Demanding that no available pair be dropped:

> `wp(K.μ⁻[d, R],  RE(W, d, ·) = RE(W, d, Σ))  ≡`
> `enabled(K.μ⁻[d, R]) ∧ (∀ (i, e) ∈ Avail(Σ) : coverage(e) ∩ Δ ≠ ∅ ⟹ coverage(e) ∩ I_R ≠ ∅)`

— every available endset that reaches a dropped address must also reach an address
*retained within the region*. Both `I_R` and `Δ` are functions of the pre-state `Σ` and
the retention set `R` alone, so the condition is checkable before the edit.

This is the per-endset refinement of the discovery query's contraction-stability (D-CWP,
ASN-0127), and it is strictly finer. D-CWP asks that every *link* reaching `Δ` also reach
`I_R` — `findlinks(Δ, Σ) ⊆ findlinks(I_R, Σ)`, an existential over slots on each side, so a
link may satisfy it by reaching `Δ` through its from-endset and `I_R` through its
to-endset. RETRIEVEENDSETS surfaces the *endsets*, not the links, so it demands the *same*
endset reach both: a link whose from-endset touches only `Δ` while its to-endset rescues
`I_R` survives in `findlinks_V` yet still drops the pair `(1, from-endset)` from `RE`. The
boundary is D-CWP's, read through the finer lens: at `R = ∅` (full clearance), `I_R = ∅`
and the condition collapses to `(∀ (i, e) ∈ Avail(Σ) : coverage(e) ∩ Δ ≠ ∅ ⟹ false)` —
i.e. no available endset touches `image(W, d, Σ)` at all, which is `RE(W, d, Σ) = ∅`.
Clearing the region preserves the answer exactly when the answer was already empty.

**Under link emission.** The one population-*growing* mover is a `K.λ` step that emits a
fresh link `ℓ_new`. Allocation gives `ℓ_new ∉ dom(Σ.L)`, so `ℓ_new` enters `dom(Σ'.L)` and
is addressable there — `ℓ_new ∉ nullified(Σ')` — by the discipline-and-`R0a` reasoning the
retraction emitter `b` will instance below: under ASN-0086's unit-depth retraction
discipline every pre-existing retraction to-set is unit-depth at a prior target, while
R0a/FlatLinkDomain (ASN-0086) makes `dom(Σ'.L)` a prefix-antichain, so no such to-set covers
the fresh, distinct address `ℓ_new`. The step frames the arrangement (`M' = M`, ASN-0093),
so the image — and every `touch_W` it determines — holds fixed; only the available pool can
move. If some endset `Σ.L(ℓ_new).eᵢ` touches the region, the pair `(i, Σ.L(ℓ_new).eᵢ)` is
*added* to the answer; if none does, the answer is unchanged. Either way the move is
monotone — a fresh emission can only add pairs, never remove one — the population-grow
analogue of the discovery query's E-MONO/F-LAMBDA (ASN-0127). Retraction is the
distinguished sub-case in which the emitted link is a *withdrawal*; there the same `K.λ`
machinery produces a *net* removal, which we take up now.

**Under retraction.** A link is never deleted (L12, ASN-0043), but it can be *withdrawn*:
a retraction marks it nullified (ASN-0086), and we range only over `addressable(Σ) =
dom(Σ.L) ∖ nullified(Σ)`. Retraction is permanent at the *link* level — once nullified, a
link stays nullified (R6a, ASN-0086) and is never returned to the active population; the
only way an identical anchoring value re-enters the store is by emitting a *fresh* link
with a new identity (R6c, ASN-0086).

A retraction is itself a link emission, and this matters for what a retraction step does to
the population. Withdrawing `ℓ` is realised as `Nullify(Σ, d_retr, ℓ) ≡ Emit_R(Σ, d_retr,
∅, {(ℓ, δ(1, #ℓ))})` (ASN-0086), and `Emit_R` *is* a `K.λ` step (Emit_K, ASN-0086): it
emits a fresh **retraction link** `b`, with `Σ'.L(b) = (∅, {(ℓ, δ(1, #ℓ))}, Θ)` — writing
`Θ` for ASN-0086's designated retraction type, kept distinct from the retention set `R` of
the contraction analysis above — that enters `dom(Σ'.L)` and is itself addressable in `Σ'`.
Its addressability — `b ∉ nullified(Σ')` — is not free: it holds because no pre-existing
retraction to-set covers the fresh emitter (the vacuity of `wp` Case 2's third conjunct
under ASN-0086's unit-depth retraction discipline and R0a/FlatLinkDomain), and `b`'s own
unit-depth to-set covers `ℓ`, not `b` (`ℓ ≠ b`, both in the flat antichain). So a single retraction
does two things at once — it removes `ℓ` from `addressable` (through the nullified marking)
*and* adds the emitter `b` to it. We must ask what the emitter `b` can contribute. Its three
endsets are the empty from-set `∅`, a to-set `{(ℓ, δ(1, #ℓ))}` whose single span covers `ℓ`
and `ℓ`'s extensions, and the retraction type-set `Θ`. The first two are content-disjoint
*unconditionally*, and for one shared reason worth isolating: the field-agreement argument
used for `e₃` above is sound exactly for **unit-depth** spans, where `coverage = {t : s ≼ t}`
(PrefixSpanCoverage, ASN-0043) reduces touching to the prefix relation `s ≼ c`, so the
separator-zero count carries `s`'s subspace identifier onto every covered `c`.
`coverage(∅) = ∅` touches nothing; the to-set *is* unit-depth — ASN-0086's `Nullify` fixes
its width at `δ(1, #ℓ)` — so the argument applies to it directly: a content `c` with `ℓ ≼ c`
would force `E(c)₁ = E(ℓ)₁ = s_L ≠ s_C`, rigorous because `ℓ` is genuinely element-level with
`E(ℓ)₁ = s_L` (L0, L1, ASN-0093) and `Nullify` targets a link address `ℓ ∈ dom(Σ.L)`. So
against a content image `I ⊆ dom(Σ.C)`, neither the from-set nor the to-set can touch.

The type-set `Θ` is the slot that same argument does *not* reach — and here we must not
overclaim. A type endset may, by design, point *anywhere* in the address space, content
included (L4 EndsetGenerality, L9 TypeGhostPermission, ASN-0043); ASN-0086 fixes the
designated retraction type only as a type endset whose coverage selects the conventional
retraction address set, carrying no structural disjointness from content. Nor does ASN-0086
confine `Θ`'s spans to unit depth, and this is decisive: a *wide* type span `(s, ℓ_s)`
denotes the half-open interval `{t : s ≤ t < s ⊕ ℓ_s}`, whose members need not satisfy
`s ≼ t`. Placing the span-*starts* of `Θ` outside content therefore does *not*, on its own, place
the whole interval outside content — the field-agreement argument transfers to a span-start
but not across a wide span's interior, so "exactly as the worked instance seated `θ`" (whose
`e₃` span *was* unit-depth) does not carry over to an arbitrary `Θ`. Hence
`coverage(Θ) ∩ dom(Σ.C) = ∅` is neither a consequence of `Θ`'s being a type nor secured by
start-placement alone; this note does not establish it, carrying it only as a hypothesis
whose exception — a type-slot match against content — is taken up by Open Question 6.

We therefore record the emitter's harmlessness **conditionally**, on the hypothesis
`coverage(Θ) ∩ dom(Σ.C) = ∅`. *Under* it, against a content image `I ⊆ dom(Σ.C)` the test
`touch_W(Θ)` is false, so all three of `b`'s endsets are content-disjoint, `b` is never
surfaced by a content-region query, and a retraction's *net* effect on `RE` is removal only.
*Absent* it, a `Θ` meeting the image surfaces the emitter as the fresh pair `(3, Θ)`, making
the retraction *add* anchoring as well as remove it. The emitter's *only* possible
content-region contribution is that single pair `(3, Θ)` — and, contrary to what one might
hope, it need not be distinct from a pair the retracted link itself bore: when `ℓ` is
*itself* a retraction link, `Σ.L(ℓ).e₃ = Θ`, so `ℓ` bears `(3, Θ)` too. The forward direction
of the stability result below therefore rests on the hypothesis. Under it `(3, Θ)` is never a
surfaced pair and the coincidence is invisible to a content-region query, so the emitter
keeps no surfaced pair alive; absent it, `b` re-witnesses the very `(3, Θ)` its target bore —
the lone exception to the forward direction, and exactly the type-slot-against-content match
that Open Question 6 takes up.

But the answer deduplicates, and we must read its stability at the granularity it actually
has. Its elements are `(role, endset)` pairs with link identity discarded (RE-UNIT): a
pair `(i, e)` is present exactly when *some* addressable link bears `e` in slot `i` and `e`
touches the region. So withdrawing one link `ℓ` does not, by itself, remove the pairs it
bore. Retracting `ℓ` removes `ℓ` from `addressable(Σ)` permanently (R6a); the same step adds
the emitter `b`, whose only possible content-region contribution is the fresh pair `(3, Θ)`
(just shown). Under the net-removal-only hypothesis `coverage(Θ) ∩ dom(Σ.C) = ∅` — adopted
for this result, its sole exception flagged above — that pair fails the touch test against a
content image, so `b` surfaces nothing and re-witnesses no pair the answer carries. A pair
`(i, e)` that `ℓ` contributed therefore leaves the answer **iff `ℓ` was its sole addressable
bearer in `Σ`**. The forward half — sole bearer ⟹ the pair drops — is the conjunction just
assembled: `ℓ` leaves `addressable` permanently (R6a) and, under the hypothesis, the emitter
`b` surfaces nothing, so neither keeps `(i, e)` alive. The backward half — some *other* live bearer ⟹
the pair survives — is not free: it asserts that the other bearer outlives the very step
that withdraws `ℓ`, and a retraction, being a state transition, could a priori nullify
more than its named target. We discharge it by bounding the retraction's reach. Take
`ℓ' ∈ addressable(Σ)` with `ℓ' ≠ ℓ`, bearing `e` in slot `i`. Both lie in `dom(Σ.L)`, a
tumbler-prefix antichain (R0a FlatLinkDomain, ASN-0086), so `ℓ ⋠ ℓ'`: the address `ℓ'`
lies outside `ℓ`'s prefix-cone. A single Nullify contributes *exactly* its target to the
nullified set — `{t : ℓ ≼ t} ∩ dom(Σ'.L) = {ℓ}` (R-Scope SingleTupleScope, ASN-0086,
arity-independent) — so the fresh retraction tuple `b` nullifies no link address but `ℓ`.
Hence `ℓ'`, already `∉ nullified(Σ)` and outside `ℓ`'s cone, is `∉ nullified(Σ')`:
`ℓ' ∈ addressable(Σ')`. Its value is unchanged (L12, ASN-0043), so it still bears `e` in
slot `i`; the `K.λ` step frames `Σ.M(d)` (`M' = M`), leaving the image — and with it
`touch_W(e)` — fixed. Thus `ℓ'` still witnesses `(i, e)` in `Σ'`, and a pair still borne
by some other addressable link survives the retraction untouched. Our worked instance
makes the distinction concrete: `ℓ₁` and `ℓ₂` both carry `e₁` in slot 1, collapsing to the
single pair `(1, e₁)`; retracting `ℓ₁` alone leaves `(1, e₁)` in the answer, because `ℓ₂`
survives the step — `ℓ₁ ⋠ ℓ₂` (R0a) puts it outside the retraction's cone, R-Scope
confines the fresh nullification to `ℓ₁`, so `ℓ₂ ∈ addressable(Σ')` still bears `e₁`
(value fixed by L12). Only when *both* are withdrawn does `(1, e₁)`
depart.

Two senses of permanence must therefore be kept apart. The *specific retracted link's*
membership in `addressable` is gone forever (R6a) — one can never again surface anchoring
*because `ℓ₁` bears it*. But the *pair value* `(i, e)` is not permanently gone: an
identical value re-enters the answer the moment any live link — `ℓ₂` already present, or a
freshly emitted link with a new identity (R6c) — bears `e` in slot `i` and `e` touches.
The answer tracks the anchoring values of the active *population*, not the fate of any one
link; conflating link-level permanence (R6a) with pair-value-level removal is exactly the
slip RE-UNIT's deduplication guards against.

So the answer's stability has exactly two faces, and both are consequences of its being a
present-tense reading of the live state: it tracks the *arrangement* (content moving in
and out of the region as it is inserted, deleted, and rearranged) and it respects the
*active population* (a freshly emitted link adding the pairs it newly witnesses, a withdrawn
link vanishing from it and taking with it any pair it solely bore). Neither is a defect to be
engineered away; both are what it *means* for the operation to answer, faithfully, "what
anchoring touches here, now."

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| RE-DEF | `RE(W, d, Σ) = { (i, e) : (∃ a ∈ addressable(Σ) : 1 ≤ i ≤ \|Σ.L(a)\| ∧ Σ.L(a).eᵢ = e ∧ touch_W(e)) }`, where the region `(W, d)` has `d ∈ dom(Σ.M)` and `W ⊆ T` a **content-subspace** V-position set (`∀ v ∈ W : subspace(v) = s_C`, a caller obligation, so the image lies in content — `I ⊆ dom(Σ.C)` by S3★, ASN-0047), resolving to `I = image(W, d, Σ)` (F-IMG, ASN-0127); `touch_W(e) ≡ coverage(e) ∩ I ≠ ∅` (ASN-0098, ASN-0043), and `addressable(Σ) = dom(Σ.L) ∖ nullified(Σ)` (ASN-0086); the answer is a finite, computable set of role-tagged endsets, and the operation has frame `Σ' = Σ` (reads only, writes nothing) | introduced |
| RE-LOC | Locality — for fixed `(W, d)`, `RE` is a function of `(Σ.M, Σ.L)` alone: it reads `Σ.M(d)` for the image and `Σ.L` for endsets and (via `nullified`) addressability; the content *values* `Σ.C`, the entity set `Σ.E`, and the provenance relation `Σ.R` are never consulted | introduced |
| RE-UNIT | Anchoring without names — the answer's elements are `(role, endset)` pairs (anchoring structure), never link identities; the link address is withheld, distinct links sharing an endset value collapse to one pair, link multiplicity is not recoverable, and a surfaced from-endset cannot be paired with the to-endset of the same link | introduced |
| RE-OVL | Overlap matching — an endset is surfaced iff at least one address it covers lies in the region's image (overlap, not containment); partial, single-address overlap suffices; the test is existential *within* an endset and applied *per-endset* against the one region, with no per-slot request differentiation | introduced |
| RE-CLIP | No clipping (load-bearing) — no reported span is ever truncated to the region boundary; every surfaced span is reported at the full extent recorded in the link. This is universal across both the whole-endset (RE-WHOLE) and touching-spans-only readings; clipping would misrepresent the link's grip (a straddling span would be falsely shortened) | introduced |
| RE-WHOLE | Whole-endset surfacing (adopted convention) — the reading adopted here returns a surfaced endset in full, *all* of its spans (not only those intersecting `W`), so a discontiguous endset retains the spans pointing outside the region. This is a convention, not a forced consequence of RE-CLIP: a touching-spans-only implementation would still satisfy RE-CLIP while violating RE-WHOLE. Held **provisional** pending Open Question 1 | introduced (provisional) |
| RE-BND | Boundary cases — `RE(W, d, Σ) = ∅` whenever the image is empty (`W ∩ dom(Σ.M(d)) = ∅`, in particular a freshly registered document with empty arrangement) or `addressable(Σ) = ∅` (no links, or all nullified); and an empty endset slot (`∅`, admitted in non-type slots by ASN-0043, only the type-slot non-empty per L3) has `coverage(∅) = ∅`, so `touch_W(∅)` is false and it is never surfaced | introduced |
| RE-SND | Soundness — `(i, e) ∈ RE(W, d, Σ) ⟹ e` is a genuine slot-`i` endset of an addressable link ∧ `touch_W(e)`; no anchoring is fabricated and none is reported that does not genuinely reach the region (no false positives) | introduced |
| RE-CMP | Completeness — every addressable link `a` and slot `i` with `touch_W(Σ.L(a).eᵢ)` has `(i, Σ.L(a).eᵢ) ∈ RE(W, d, Σ)`; the answer is *exactly* the touching set, with no silent omission, whether reached by native or transcluded content | introduced |
| RE-UDIST | Union-distributivity — `RE(W₁ ∪ W₂, d, Σ) = RE(W₁, d, Σ) ∪ RE(W₂, d, Σ)`: the forward image distributes over union unconditionally, so `touch_{W₁∪W₂}` is the disjunction `touch_{W₁} ∨ touch_{W₂}`, and the available slot-endset pool `Avail(Σ)` is region-independent; the RE-level analogue of F-UDIST/F-VDIST (ASN-0127). Intersection-distributivity does *not* follow — the forward image fails to distribute over intersection under the non-injective arrangement (M13, M14, ASN-0058) — and is left open | introduced |
| RE-SEL | Discovery-side selection — `sel(W, d, Σ) = findlinks_V(W, d, Σ) ∩ addressable(Σ)` (F-V, ASN-0127): the contributing links are the addressable links discoverable through the region, so the operation is discovery-anchored — present-tense, non-monotone, arrangement-mediated (D-NONMONO, D-ZERO, ASN-0127), not existence-anchored (fixed-`I`, historical, monotone) | introduced |
| RE-EXST | Existence-of-anchoring deliverable — by withholding identity the answer certifies the *presence and shape* of anchoring without making it followable; the foundation's existence/discovery axis (query mode: fixed vs arrangement-resolved) and the designer's existence/discovery axis (deliverable: structure vs named-and-followable) are orthogonal — RE is discovery on the first, existence-of-anchoring on the second | introduced |
| RE-TRANS | Transclusion blindness — surfacing is by content identity, independent of the link's home and of the covered content's origin (LP16, ASN-0098): a link reaching the region only through transcluded content is surfaced identically to one reaching native content, and each returned span describes the content's permanent home identity, not the borrowing V-position | introduced |
| RE-IDENT | Content-identity invariance — each surfaced endset's coverage is permanent (L12, ASN-0043; LP3, ASN-0098), so the content-level answer (which I-addresses each surfaced endset anchors to) is arrangement-independent, even though the *selection* of which endsets are surfaced is arrangement-mediated | introduced |
| RE-EDIT | Present-tense stability under editing — `RE` tracks `d`'s content-subspace arrangement, so the answer is non-monotone (D-NONMONO, ASN-0127) while each surfaced endset's spans stay invariant (RE-IDENT). Over the transition vocabulary (ASN-0047), only the content-subspace edits to `d` — insertion `K.μ⁺`, content deletion `K.μ⁻`, rearrangement `K.μ~` — and `K.λ` (emission may add a pair, retraction removes — RE-RET) can move the answer; every other transition leaves it fixed, including the link-subspace edits `K.μ⁺_L` and link-subspace-only `K.μ⁻` (image fixed under `W ⊆ s_C`). A region-local deletion is *not* the global orphaning/resurrection of LP17/LP18 (ASN-0098). | introduced |
| RE-RET | Retraction stability — a retraction is a `K.λ` step (Nullify/Emit_K, ASN-0086) that marks `ℓ` nullified (removing it from `addressable(Σ)` permanently, R6a) and emits a fresh addressable retraction link `b` with endsets `(∅, {(ℓ, δ(1, #ℓ))}, Θ)` (`Θ` the retraction type, ASN-0086). Because the answer deduplicates and discards identity (RE-UNIT), a pair `(i, e)` that `ℓ` bore drops **iff `ℓ` was its sole addressable bearer in `Σ`**: backward (other bearer ⟹ survives) unconditional; forward (sole bearer ⟹ drops) under the net-removal-only hypothesis `coverage(Θ) ∩ dom(Σ.C) = ∅`, with sole exception the type-slot-against-content match routed to Open Question 6. Link-level permanence (R6a) is not pair-value-level permanence — an identical pair re-enters only via a separately identified live link (R6c, ASN-0086). | introduced |
| RE-CWP | Contraction-stability weakest precondition — for a `K.μ⁻[d, R]` step, `RE(W, d, ·) = RE(W, d, Σ)` iff `enabled(K.μ⁻[d, R]) ∧ (∀ (i, e) ∈ Avail(Σ) : coverage(e) ∩ Δ ≠ ∅ ⟹ coverage(e) ∩ I_R ≠ ∅)`, where `I_R = {Σ.M(d)(v) : v ∈ W ∩ R}` (D-CWP bridge, ASN-0127), `Δ = image(W, d, Σ) ∖ I_R`, and `Avail(Σ)` is the region-independent pool of addressable slot-endsets. `RE` is monotone-decreasing under contraction, the condition is strictly finer than D-CWP's per-link form, and `R = ∅` collapses it to `RE(W, d, Σ) = ∅`. | introduced |
| RE-DET | Determinism — `RE(W, d, Σ)` is a function of `(W, d, Σ)`; with no intervening state change the same region query returns the same anchoring, so every change in the answer is the image of a change in `Σ` | introduced |

## Open Questions

Must a surfaced endset be reported in its entirety, or only those of its spans that intersect the region — and which choice is the faithful rendering of the link's anchoring?

When distinct addressable links carry an identical endset value in the same slot, must the operation's answer preserve their multiplicity, or is collapsing them to a single surfaced endset a faithful answer?

When a surfaced endset is rendered into the querying document's V-positions rather than content identity, what must the answer guarantee for endset content the document does not currently arrange?

Must the surfaced anchoring distribute over *intersections* of the queried region — composing a region query from overlapping parts — given that the forward image fails to distribute over intersection under the non-injective arrangement (M13, M14, ASN-0058)? (The union half is derived above as RE-UDIST.)

What completeness guarantee must hold when anchoring that touches a region resides in a link store not co-resident with the queried document?

What must hold of a type-slot match against a content region for it to be meaningful, given that type endsets are matched by address and ordinarily reference classifying addresses disjoint from content?

What must a region query guarantee when its V-positions are drawn from the link subspace (`subspace(v) = s_L`) rather than the content subspace — resolving, by S3★ (ASN-0047), to an image inside `dom(Σ.L)` (link addresses, not content), so that the touch test surfaces anchoring aimed at links (the to-endsets of retraction emitters, type endsets) and the exactness of retraction stability acquires an extra term for the retraction emitter `b`, whose to-set then meets the image?
