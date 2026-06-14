# ASN-0131: RETRIEVEENDSETS — Surfacing Anchoring Over a Content Region

*2026-06-13*

We have, by the time we reach this note, two stores and an arrangement family in the
system state `Σ = (Σ.C, Σ.L, Σ.E, Σ.M, Σ.R)` (ASN-0047). The content store `Σ.C : T ⇀ Val`
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
integrity places the image in content: `I ⊆ dom(Σ.C)` (S3★, ASN-0047). The region is
resolved to content through the present arrangement, and everything downstream is phrased
in I-addresses, where links live.

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

First, **overlap, not containment**. A single shared address suffices; partial overlap
is real contact. The endset need not lie inside the region, and the region need not lie
inside the endset. This is the disjunction Nelson phrases as matching "all or any part
of" the requested set: one span falling within the region qualifies the endset.

Second, the relation is **existential within an endset**. An endset is a finite *set* of
spans, possibly discontiguous (ASN-0043). `touch_W(e)` asks that *some* address in
`coverage(e)` lies in `I` — not that every span does. The other spans of a touching
endset legitimately point elsewhere; they do not disqualify it, and they are not
clipped away from it.

Third, the relation is **per-endset, not per-link**. We judge each endset on its own
coverage against the region. A link carries several endsets — by convention a from-endset
`e₁`, a to-endset `e₂`, a type-endset `e₃`, and possibly more (L3). RETRIEVEENDSETS asks
its one region of *each* endset independently. A link's from-endset may touch while its
to-endset points to a destination far outside `W`; then the from-endset is surfaced and
the to-endset is not. There is no four-set request here differentiating slot from slot
(that is the richer FINDLINKSFROMTOTHREE); there is one region, tested against every
endset, and the endsets that touch are the ones surfaced.

## The unit of the answer: anchoring without names

Now we can state what RETRIEVEENDSETS returns. We must first settle which links it ranges
over. A link, once created, is permanent and immutable in the store (L12, ASN-0043) — but
the system admits *retraction*, recorded not by deleting the link but by emitting a
withdrawal link that marks the target nullified (ASN-0086). We adopt throughout, as a
**standing assumption**, ASN-0086's *relational-layer discipline commitment*: every store
transition that adds a retraction-typed link is a `Nullify`, so retraction-typed links enter
the store through that one operation alone. ASN-0086's *unit-depth retraction discipline* —
every retraction to-set is a unit-depth span `{(t, δ(1, #t))}` at a single prior target — is
the **to-set consequence** of this commitment, discharged from it by induction (ASN-0086).
The commitment also fixes the *from-set*: `Nullify` emits its retraction with an *empty
from-set* (ASN-0086), so adopting it **excludes attributed retractions** (non-empty
from-set), which ASN-0086's Convention RetractionDirectionality would otherwise permit. The bridge to
ASN-0086 — call it the **`Σ.L`-evolution bridge** — is that `Σ.L` evolves only through
`K.λ`: the arrangement movers (`K.μ` family), entity creation `K.δ`, provenance recording
`K.ρ`, and content allocation `K.α` all frame the link store (`L' = L`). So the link store
evolves identically under ASN-0086's transition relation and under ASN-0047's, and every
ASN-0086 lemma whose conclusion constrains `Σ.L` or `nullified` holds at every
ASN-0047-reachable state.

One consequence of that shared `K.λ` semantics recurs. Write `Θ` for ASN-0086's designated
retraction type (ASN-0086's own symbol is `R`, which this note reserves for other uses, so we
rename it `Θ`). A `K.λ` step emits a *fresh* link — allocation gives `ℓ_new ∉ dom(Σ.L)`, so
`ℓ_new` enters `dom(Σ'.L)` — and whether that fresh output is *addressable* in its post-state
(`ℓ_new ∉ nullified(Σ')`) turns on whether some retraction to-set covers it. The standing
commitment's unit-depth to-set settles this for an output of *any* arity, with no appeal to
triple structure: every retraction to-set in `Σ'.L` is unit-depth at some link `t ∈ dom(Σ'.L)`,
covering `{u : t ≼ u}`, and R0a/FlatLinkDomain (ASN-0086) makes `dom(Σ'.L)` a prefix-antichain,
so any `t` distinct from `ℓ_new` is prefix-incomparable to it (`t ⋠ ℓ_new`) and cannot cover
it. The only retraction to-set that could cover `ℓ_new` is its own — present only if `ℓ_new`
is itself a retraction — and it does so exactly when `ℓ_new` retracts its own emitter address.
Hence the reusable fact — **fresh-output addressability (RE-ADDR)**: a fresh `K.λ` output that
does not retract its own emitter address is addressable in its post-state; in particular every
non-retraction emission (`K ≁ Θ`) is addressable.

A withdrawn link's anchoring should not be reported as live — a design decision that fixes
the operation as a report over the *active* population, not the full permanent store. So we range
over the links that are present and not withdrawn — the **addressable** links:

> `addressable(Σ) = dom(Σ.L) ∖ nullified(Σ)`     (over ASN-0086's `nullified`).

The operation surfaces, for each addressable link and each of its endsets that touches
the region, that endset, tagged by the slot it occupies:

> `RE(W, d, Σ)  =  { (i, e) : (∃ a : a ∈ addressable(Σ) : 1 ≤ i ≤ |Σ.L(a)| ∧ Σ.L(a).eᵢ = e ∧ touch_W(e)) }`.

The answer is a set of `(role, endset)` pairs. Each pair names the slot `i` — from, to,
type, or higher — and the endset value `e` that occupies it in some touching link.

The answer just defined is a finite, computable object. The touch test is decidable: the
image `I = image(W, d, Σ)` is finite (S8-fin, ASN-0036) and `coverage`-membership is
decidable by intrinsic comparison on its half-open T1-intervals (T12, T2, ASN-0034), so
`touch_W(e) ≡ coverage(e) ∩ I ≠ ∅` is settled by finitely many membership tests. The
addressability filter is decidable over finite sets too: `nullified(Σ)` is a computable set
(ASN-0086) and `dom(Σ.L)` is finite (L-fin, ASN-0093), so membership in
`addressable(Σ) = dom(Σ.L) ∖ nullified(Σ)` is settled without enumerating history. The
operation therefore selects its `(i, e)` pairs by finitely many decidable tests over the
finite store.

The definition **withholds the link address `a`**. The existential `(∃ a : …)` consumes the link and discards it; what
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

`RE` reads the
arrangement `Σ.M(d)` (to form the image) and the link store `Σ.L` (for endsets, and,
through `nullified`, for addressability). It never consults the content *values* `Σ.C`,
the entity set `Σ.E`, or the provenance relation `Σ.R`. And it is a pure query: it reads
state and changes none — `Σ' = Σ`. Whatever anchoring it reports, it reports as a fact
about the state it found, leaving that state untouched.

Three degenerate inputs are worth reading straight off the definition.

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

## Extent: the surfaced endset, whole and unclipped

A returned endset must be the link's *actual* anchoring, not an approximation of it, and
not a fragment of it trimmed to the region. (That every returned pair is a *genuine* slot-`i`
endset of an addressable link touching the region — its provenance — is the soundness
direction, established below as RE-SND; here we sharpen the separate question of **extent**.)
Two invariants of different strength must be kept apart, because the operation rests
squarely on one and merely adopts the other.

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
contract — each an immediate read of RE-DEF, not a theorem requiring argument.

**Soundness** is the forward direction: if `(i, e) ∈ RE(W, d, Σ)`, then `e` is a genuine
slot-`i` endset of an addressable link and `touch_W(e)` holds — the existential of RE-DEF
witnesses a real `a` with `Σ.L(a).eᵢ = e`. The operation fabricates no anchoring: nothing in
the answer fails to reach the region, a reported overlap is a true overlap, and a reader who
receives `(1, e)` may rely that some live link really attaches its from-end at the spans of
`e` and that those spans really reach the region.

**Completeness** is the converse: for every addressable link `a` and every slot `i` with
`touch_W(Σ.L(a).eᵢ)`, the pair `(i, Σ.L(a).eᵢ)` is in `RE(W, d, Σ)`. Every endset that
touches the region — by direct anchoring or through transcluded content
— appears; none is silently omitted.

Together they fix the result as *exactly* the touching set — neither more nor less.

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
  (PrefixSpanCoverage, ASN-0043) is disjoint from content: `coverage(e₃) ∩ dom(Σ.C) = ∅`.
  Take any `c ∈ dom(Σ.C)`: by S7b (ASN-0036)
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
  — the cross-end pairing RE-UNIT withholds.

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

The *intersection* law does not follow in full — but one half of it does, and
unconditionally. We must first see where the forward image fails to distribute over
intersection: in general
`image(W₁ ∩ W₂, d, Σ) ⊆ image(W₁, d, Σ) ∩ image(W₂, d, Σ)`, but the inclusion can be
strict, because distinct V-positions may map to the *same* I-address — the arrangement is
non-injective (M13, M14, ASN-0058). A position in `W₁ ∖ W₂` and a position in `W₂ ∖ W₁`
can share an I-address that then lies in both images, hence in the right-hand
intersection, while contributing nothing to `image(W₁ ∩ W₂, d, Σ)`.

The image `⊆` law that does hold, however, already settles one direction of the RE-level
intersection law. From `image(W₁ ∩ W₂, d, Σ) ⊆ image(W₁, d, Σ)` and the symmetric inclusion
for `W₂`, an endset meeting the smaller image meets each larger one, so the touch test
implies *both* of its sub-region instances:

> `touch_{W₁ ∩ W₂}(e) ⟹ touch_{W₁}(e) ∧ touch_{W₂}(e)`.

Filtering the region-independent pool `Avail(Σ)` by this implication — exactly as the union
proof filters it by the disjunction — gives

> `RE(W₁ ∩ W₂, d, Σ) = { (i, e) ∈ Avail(Σ) : touch_{W₁ ∩ W₂}(e) }
>   ⊆ { (i, e) ∈ Avail(Σ) : touch_{W₁}(e) ∧ touch_{W₂}(e) }
>   = RE(W₁, d, Σ) ∩ RE(W₂, d, Σ)`,

and, like the image `⊆` law it rests on, this needs *no* injectivity hypothesis. The
reverse inclusion, by contrast, **fails in general** — and we can exhibit the failure, not
merely fail to derive it, with a complete construction. It turns on non-injectivity (M13,
M14, ASN-0058): let `d` arrange two *distinct* V-positions to one content I-address,

> `Σ.M(d) = { [1,1] ↦ a,  [1,2] ↦ a }`,   `a ∈ dom(Σ.C)`,

and let `ℓ_e ∈ dom(Σ.L)` be a link emitted by `K.λ` carrying in slot 1 the unit-depth
from-endset `e = {(a, δ(1, #a))}` — so `Σ.L(ℓ_e).e₁ = e` and `coverage(e) = {t : a ≼ t}`
(PrefixSpanCoverage, ASN-0043) — addressable in this post-state as a non-retraction
emission, hence `ℓ_e ∉ nullified(Σ)` (RE-ADDR, taking `Σ` as the emission's post-state); so
`(1, e) ∈ Avail(Σ)`. Take the disjoint regions `W₁ = {[1,1]}` and `W₂ = {[1,2]}`:
the two distinct positions `[1,1] ∈ W₁ ∖ W₂` and `[1,2] ∈ W₂ ∖ W₁` carry the shared address
into both images, `image(W₁, d, Σ) = image(W₂, d, Σ) = {a}`, while `W₁ ∩ W₂ = ∅`. Since
`a ∈ coverage(e)` (reflexivity of `≼`), `touch_{W₁}(e)` and `touch_{W₂}(e)` both hold; with
`(1, e) ∈ Avail(Σ)` this gives `(1, e) ∈ RE(W₁, d, Σ) ∩ RE(W₂, d, Σ)`. But the intersection
region is empty, so `image(W₁ ∩ W₂, d, Σ) = ∅`, whence
`coverage(e) ∩ image(W₁ ∩ W₂, d, Σ) = ∅` — `e` meets that image nowhere — and
`RE(W₁ ∩ W₂, d, Σ) = ∅` (RE-BND); thus `(1, e) ∉ RE(W₁ ∩ W₂, d, Σ)`, refuting `⊇`
(RE-UDIST-∩). What remains open is the refinement — whether some restriction on the
arrangement, injectivity of `Σ.M(d)` the natural candidate, recovers equality
(Open Question 4).

## Existence and discoverability: which side does this answer for?

ASN-0127 separates **existence** queries — a fixed `I ⊆ T`, answering a monotone,
*historical* property of the permanent store — from **discovery** queries — `I` resolved
*through a document's current arrangement*, answering a non-monotone, *present-tense* one
(*Anchoring: existence vs discovery*; E-MONO, D-NONMONO, D-ZERO, ASN-0127). We place
RETRIEVEENDSETS on that line.

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

## Anchoring reached through borrowed content

A region need not hold content native to its own document. Through transclusion, `d` may
window content whose home is another document `d_src`; the windowed content is not a copy
but the *same content*, sharing its I-addresses with the home (ASN-0036). The question
arises: if a link resides in `d_src` (or anywhere), and reaches our region only because
`d` windows the link's content, must RETRIEVEENDSETS surface that link's endset — and must
it treat such borrowed-content anchoring the same as anchoring on native content?

It must, and the reason is structural: both the anchoring and the query are keyed to
*content identity*. The endset covers I-addresses naming the content's permanent home, not
any borrowing V-position (ASN-0043); the region's image is I-addresses; `touch_W` intersects
them, consulting nothing about where the link lives, where the content is "native," or which
document windows it. This is precisely the discovery query's document-blindness:
discoverability of a link through `d` "turns solely on `coverage ∩ ran(Σ.M(d))`," independent
of the link's home and of the origin of the covered content (LP16, ASN-0098). So if `d`'s
arrangement maps the region's V-positions to I-addresses an endset covers, that endset
touches the region — whether those I-addresses are native to `d` or borrowed from `d_src`. A
link reaching the region through transcluded content is therefore surfaced **identically** to
one reaching native content, and one endset is the same anchoring through every
co-transcluder: at the level of content identity there is nothing to distinguish.

This connects to a general invariant, independent of transclusion: **each surfaced endset's
coverage is permanent**. Links are immutable (L12, ASN-0043) and no transition alters an
endset's coverage (LP3, ASN-0098), so once an endset is surfaced the I-addresses it anchors
are a fixed fact about a permanent link (RE-IDENT). The transclusion case is one
reading of it: the *content-level* answer — which content each surfaced endset anchors to
— is invariant, even though what the region's image maps to, and how that image sits
within `d`'s order, are present-tense. The operation's content-level answer is therefore
arrangement-independent even though its *selection* of which endsets to surface is
arrangement-mediated.

## Stability: the answer as the document is edited

Because the operation is a pure function of the present state, resolved through the
present arrangement, its stability is entirely determined by how state changes move the
two things it reads: the region's image and the addressable population. By RE-IDENT each
surfaced endset's coverage is permanent, so editing can change *which* endsets are surfaced
— the membership of the answer — but never the spans of one that is. Every motion
catalogued below is a motion of membership.

**Under editing of the queried document.** The region resolves through `Σ.M(d)`, so
editing `d`'s arrangement moves the image, and the answer tracks it — present-tense,
non-monotone (D-NONMONO, ASN-0127). We read its response first against the *atomic*
arrangement movers of the transition vocabulary (ASN-0047) — extension, contraction,
reordering — each acting as a faithful tracker would:

- *Arrangement extension* `K.μ⁺` appends new V→I mappings at the contiguous frontier of
  `d`'s content subspace, leaving every existing mapping fixed and the arrangement canonical
  (D-CTG/D-SEQ, ASN-0047). The region image can only grow, and only weakly:
  `image(W, d, Σ) ⊆ image(W, d, Σ')` (F-IMG-MONO, ASN-0127). When `W` reaches the appended
  frontier positions, the new content enters the image, endsets covering it newly touch the
  region, and they are surfaced — anchoring that was always there in the store becomes
  *reachable* here without any link being created. When the fixed region does *not* include
  the frontier, the append adds nothing under `W`: the inclusion is equality, and the
  image — hence `RE` — is unchanged.

- *Arrangement contraction* `K.μ⁻` truncates the tail of `d`'s content subspace, retaining a
  canonical prefix `R` of content V-positions and dropping the rest (ASN-0047). The region
  image can only shrink, and only weakly: `image(W, d, Σ') ⊆ image(W, d, Σ)` (F-IMG-CONTR,
  ASN-0127). When `W` reaches the dropped tail, endsets that touched only through the
  departed content cease to be surfaced — the contracted image no longer meets their
  coverage, so the touch test fails where it formerly held (the contraction direction of
  LP10 and the discoverability characterisation LP12, ASN-0098). The link persists in the
  store (L12, ASN-0043), its endset coverage unchanged; it is merely no longer reachable
  *through this region of `d`*. This is a region-local loss of reach, **not** the global
  *orphaning* of LP17 (ASN-0098), whose premise — that the content is reachable from *no*
  document — a single-region contraction does not establish: the link may still touch other
  regions of `d`, or be reachable from other documents. Should the content be re-arranged
  into `d`, the region image grows again (F-IMG-MONO, LP9, ASN-0098) and the endset is
  surfaced once more. When the fixed region lies
  wholly within the retained prefix `R`, the truncation drops nothing under `W`: the
  inclusion is equality, and `RE` is unchanged.

- *Arrangement reordering* `K.μ~` permutes the region's V-positions over the same content;
  the *region image*'s membership can swing (F-IMG-SWING, ASN-0127). This is the *only* way
  a reordering changes the answer: which `(i, e)` pairs are surfaced may change as the image
  swings and some endset newly meets it or ceases to — the answer moving by membership alone
  (RE-IDENT). (A *rendered* answer — one resolved into
  `d`'s present V-order rather than content identity, where piecewise displacement could
  fragment a contiguous run (ASN-0082) — is the mode deferred to Open Question 3; the
  content-identity answer returned here is unaffected.)

The user-facing *insert* and *delete* that **shift** content are not these atomic movers;
ranging over them widens the vocabulary beyond ASN-0047's atomic transitions to ASN-0082's
displacement primitives, taken in their own right. The foundation realises them as
displacements (I3 PostInsertionShift, D-SHIFT, ASN-0082): an insertion at `p` of width `n`
carries the content at every position `v ≥ p` up to `shift(v, n)` (I3, established there at
every text depth `#p ≥ 2`), and a deletion carries the content lying above the removed span
back down (D-SHIFT, established there at text depth `#p = 2`; the foundation supplies no
gap-closing interior-span delete at greater content depths `m_{s_C} > 2` (S8-depth, S8a,
ASN-0036), the depth-general `K.μ⁻` being tail-truncation rather than interior-span deletion).
So delete-stability is scoped to text depth `#p = 2` and insert-stability to every `#p ≥ 2` —
an asymmetry in the displacement's *existence*, not in the stability argument, which would
cover a higher-depth delete were the foundation to supply one. What that argument requires of
either is not the displacement's specifics but only that it is an *arrangement edit confined to
`Σ.M(d)`* — an **M-only edit**. And this is *settled*, not assumed. ASN-0082 models these
primitives over a `(C, M)` state with no link, entity, or provenance store, and proves they
write only `Σ.M(d)` and frame `Σ.C` (I3-C, D-I: `Σ.C` unchanged). The full state
`(C, L, E, M, R)` adds only the stores `Σ.L`, `Σ.E`, `Σ.R`, which the `(C, M)` primitives
never name; so the unique lift to the full state writes `Σ.M(d)` and frames `L`, `E`, `R` —
there is nothing else for such a lift to write. The lifted edit therefore acts exactly as
every ASN-0047 atomic mover above does, at any content depth. The addressable population is
unmoved across the shift: `addressable(Σ)` and the region-independent pool `Avail(Σ)` are
functions of `Σ.L` (through `nullified`) alone, so only the region's image can move. Content
is *displaced through* `d`'s V-order, and its effect on the image is read off the displacement
directly.
Fix the region `W`. The displacement moves content *through* `W`'s fixed positions, so its
effect on the image is not one-signed the way `K.μ⁺`/`K.μ⁻` are: the shift family is
non-monotone *as a class*, and a single shift may make the fixed region's image *gain*,
*lose*, or *both*, according to where the edit falls relative to `W`. The vacated positions
`[p, shift(p, n))` the shift primitive does *not* backfill (I3-V), so the bare shift leaves an
interior gap in `V_{s_C}(d)` that violates the standing contiguity invariants D-CTG★/D-SEQ★
(ASN-0047) — and indeed ASN-0082 supplies no D-CTG-preservation lemma for the insertion shift
(only for the gap-closing delete, D-CTG-post). That gap configuration is therefore not a
reachable state; by the atomicity of transitions (SequentialTransitionAxiom, ASN-0047) it is a
non-queryable intermediate of the *non-atomic* full insert, not a state at which `RE` is
evaluated. At each reachable post-edit state, then, `RE` tracks the image's motion by
membership, each surfaced endset's spans held fixed (RE-IDENT), by the depth-independent
M-only lift established above.

Editing of *other* documents does not perturb the answer: the image reads only `Σ.M(d)`,
and a transition touching `d' ≠ d` leaves `Σ.M(d)` fixed (LP5, ASN-0098). Three further
transition kinds leave the answer fixed for the same root reason — each leaves the queried
fiber `Σ.M(d)` and the link store `Σ.L` fixed (LP8 supplying the K.δ document-registration
case). Content allocation `K.α` touches neither `Σ.M` nor `Σ.L` (frame
`M' = M; L' = L`, ASN-0093) and so changes no projection (LP6, ASN-0098); a freshly
allocated I-address enters no region image without a separate arrangement edit. Entity
creation `K.δ` — registering a new node, account, or document `e ≠ d` — leaves `Σ.M(d)`
untouched (wholly, for node/account creation, where `M' = M`; and on every pre-existing
arrangement, for document registration, LP8, ASN-0098) and leaves `Σ.L` fixed (frame), so
neither the image nor the available pool moves. Provenance recording `K.ρ` writes only
`Σ.R` (ASN-0047), which `RE` never reads (RE-LOC), so it cannot move the answer (LP14,
ASN-0098).

Finally, a whole *class* of arrangement edits to `d` *itself* leaves a content-region answer
fixed — by a route particular to the content-subspace restriction rather than to locality:
the **link-subspace-confined** edits, those touching only `d`'s link subspace. The
link-subspace extension `K.μ⁺_L` adds a single V-position `v_ℓ` with `subspace(v_ℓ) = s_L`,
mapped to a link address (ASN-0047). Because `W ⊆ s_C`, we have `v_ℓ ∉ W`, so the selecting
set `W ∩ dom(Σ.M(d))` — and with it the image `image(W, d, Σ)` — is unchanged
(F-IMG-MONO sharpened to equality under `W ⊆ s_C`, ASN-0127); and its frame leaves `Σ.L`
fixed (`L' = L`), so the available pool does not move either. A **link-subspace-only
contraction** `K.μ⁻` is secured by the identical route — one retaining the whole content
subspace (`n'_{s_C} = n_{s_C}`) while strictly contracting the link subspace
(`n'_{s_L} < n_{s_L}`, admissible whenever `V_{s_L}(d) ≠ ∅`, since `K.μ⁻` requires at least
one subspace to strictly contract): for `W ⊆ s_C`, retained-position agreement gives
`W ∩ dom(Σ'.M(d)) = W ∩ V_{s_C}(d) = W ∩ dom(Σ.M(d))`, so `image(W, d, Σ') = image(W, d, Σ)`,
while `K.μ⁻`'s frame leaves `Σ.L` fixed and `Avail(Σ)` with it. Either edit gives
`RE(W, d, Σ') = RE(W, d, Σ)`. The contraction case is RE-CWP's `Δ = ∅` instance — no content
position is dropped, so `I_R = image(W, d, Σ)` and `Δ = ∅`.
(Arrangement reordering `K.μ~` is *not* link-confined: it is link-subspace-fixing by
admissibility and requires a non-trivial content effect by its precondition, so it always
touches content — the two link-subspace-confined edits are exactly `K.μ⁺_L` and link-only
`K.μ⁻`.)

**The weakest precondition for contraction-stability.** The qualitative tracking above can
be made exact for one editing motion — a deletion. Fix a `K.μ⁻[d, R]` step on the queried
document: a contraction retaining exactly the arrangement positions in the retention set
`R` (ASN-0047), with `enabled(K.μ⁻[d, R])` its applicability condition. We ask the natural non-trivial
stability question: under what precondition on `Σ` does this step leave `RE(W, d, ·)`
*unchanged*? Two observations narrow it.

First, `K.μ⁻` touches only `Σ.M(d)`; its frame leaves `Σ.L`, and hence `nullified(Σ)`,
fixed. So the *available* pairs `Avail(Σ)` — defined at union-distributivity above and
region-independent — are identical pre- and post-state; only the `touch_W` filter can move. Second, contraction only shrinks the image. By the bridge of D-CWP
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
fresh link `ℓ_new`. By RE-ADDR, a non-retraction emission (`K ≁ Θ`) is addressable in its
post-state, so `ℓ_new ∈ addressable(Σ')`. The step frames the arrangement (`M' = M`,
ASN-0093), so the image — and every `touch_W` it determines — holds fixed; only the available
pool can move. If some endset `Σ.L(ℓ_new).eᵢ` touches the region, the pair
`(i, Σ.L(ℓ_new).eᵢ)` is *added* to the answer; if none does, the answer is unchanged. Either
way the move is monotone — a non-retraction emission (`K ≁ Θ`) can only add pairs, never
remove one — the population-grow analogue of the discovery query's E-MONO/F-LAMBDA (ASN-0127).

**Under retraction.** A link is never deleted (L12, ASN-0043), but it can be *withdrawn*:
a retraction marks it nullified (ASN-0086), and we range only over `addressable(Σ) =
dom(Σ.L) ∖ nullified(Σ)`.

A retraction is itself a link emission, and this matters for what a retraction step does to
the population. Withdrawing `ℓ` is realised as `Nullify(Σ, d_retr, ℓ) ≡ Emit_R(Σ, d_retr,
∅, {(ℓ, δ(1, #ℓ))})` (ASN-0086), and `Emit_R` *is* a `K.λ` step (Emit_K, ASN-0086): it
emits a fresh **retraction link** `b`, with `Σ'.L(b) = (∅, {(ℓ, δ(1, #ℓ))}, Θ)`. Its to-set
covers `ℓ`, not `b` (`ℓ ≠ b`, both in the flat antichain), so `b` does not retract its own
emitter address; `b` is therefore addressable in `Σ'` (`b ∉ nullified(Σ')`) by RE-ADDR. So a
single retraction does two things at once — it removes `ℓ` from `addressable` (through the
nullified marking) *and* adds the emitter `b` to it. We must ask what the emitter `b` can contribute. Its three
endsets are the from-set `∅` — empty because the standing commitment admits only `Nullify`
retractions, not the attributed ones ASN-0086 otherwise permits — a to-set
`{(ℓ, δ(1, #ℓ))}` whose single span covers `ℓ` and `ℓ`'s extensions, and the retraction
type-set `Θ`. The first two are content-disjoint
*unconditionally*, and for one shared reason worth isolating: the field-agreement argument
used for `e₃` above is sound exactly for **unit-depth** spans, where `coverage = {t : s ≼ t}`
(PrefixSpanCoverage, ASN-0043) reduces touching to the prefix relation `s ≼ c`, so the
separator-zero count carries `s`'s subspace identifier onto every covered `c`.
`coverage(∅) = ∅` touches nothing; the to-set *is* unit-depth — ASN-0086's `Nullify` fixes
its width at `δ(1, #ℓ)` — so the argument applies to it directly: a content `c` with `ℓ ≼ c`
would force `E(c)₁ = E(ℓ)₁ = s_L ≠ s_C`, rigorous because `ℓ` is genuinely element-level with
`E(ℓ)₁ = s_L` (L0, L1, ASN-0093) and `Nullify` targets a link address `ℓ ∈ dom(Σ.L)`. So
against a content image `I ⊆ dom(Σ.C)`, neither the from-set nor the to-set can touch.

The type-set `Θ` is the slot that same argument does *not* reach. A type endset may, by
design, point *anywhere* in the address space, content included (L4 EndsetGenerality, L9
TypeGhostPermission, ASN-0043), and ASN-0086 fixes the designated retraction type only as a
type endset whose coverage selects the conventional retraction address set — carrying no
structural disjointness from content, and not confined to unit depth. The field-agreement
argument used above reduces touching to the prefix relation `s ≼ c`, so it transfers to a
span-*start* but not across the interior of a *wide* span `(s, ℓ_s)`, whose interval
`{t : s ≤ t < s ⊕ ℓ_s}` may include content even when `s` lies outside it. So
`coverage(Θ) ∩ dom(Σ.C) = ∅` is a construction hypothesis, not a theorem; this note carries
it as such, its exception — a type-slot match against content — taken up by Open Question 6.

We therefore record the emitter's harmlessness **conditionally**, on that same hypothesis
`coverage(Θ) ∩ dom(Σ.C) = ∅`. With the from-set and to-set already content-disjoint, `Θ` is
the emitter's *only* possible content-region contribution — the single pair `(3, Θ)`.
*Under* the hypothesis, against a content image `I ⊆ dom(Σ.C)` the test `touch_W(Θ)` is
false, so all three of `b`'s endsets are content-disjoint, `b` is never surfaced, and a
retraction's *net* effect on `RE` is removal only. *Absent* it, `b`'s type-slot `Θ` could
meet the content image and surface the fresh pair `(3, Θ)`, making the retraction *add*
anchoring as well as remove it; the forward direction of the stability result below
therefore rests on the hypothesis.

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
`ℓ' ∈ addressable(Σ)` with `ℓ' ≠ ℓ`, bearing `e` in slot `i`. A single Nullify contributes
*exactly* its target to the nullified set — `{t : ℓ ≼ t} ∩ dom(Σ'.L) = {ℓ}` (R-Scope
SingleTupleScope, ASN-0086, arity-independent — carried to this ASN-0047 state by the
`Σ.L`-evolution bridge, R-Scope's `d_retr ∈ dom(Σ.M)` hypothesis meaningful here because
`dom(Σ.M) = E_doc` (M1, ASN-0047) is the same ASN-0093 document substrate ASN-0086 names) —
so the fresh retraction tuple `b` nullifies no link address but
`ℓ`, leaving every other store element `ℓ' ≠ ℓ` outside its reach.
Hence `ℓ'`, already `∉ nullified(Σ)` and distinct from `ℓ`, is `∉ nullified(Σ')`:
`ℓ' ∈ addressable(Σ')`. Its value is unchanged (L12, ASN-0043), so it still bears `e` in
slot `i`; the `K.λ` step frames `Σ.M(d)` (`M' = M`), leaving the image — and with it
`touch_W(e)` — fixed. Thus `ℓ'` still witnesses `(i, e)` in `Σ'`, and a pair still borne
by some other addressable link survives the retraction untouched. Our worked instance
makes the distinction concrete: `ℓ₁` and `ℓ₂` both carry `e₁` in slot 1, collapsing to the
single pair `(1, e₁)`; retracting `ℓ₁` alone leaves `(1, e₁)` in the answer, because `ℓ₂`
survives the step — R-Scope confines the fresh nullification to `ℓ₁`, so `ℓ₂` (distinct
from `ℓ₁`) remains in `addressable(Σ')` and still bears `e₁` (value fixed by L12). Only
when *both* are withdrawn does `(1, e₁)` depart.

Two senses of permanence must therefore be kept apart. The *specific retracted link's*
membership in `addressable` is gone forever (R6a) — one can never again surface anchoring
*because `ℓ₁` bears it*. But the *pair value* `(i, e)` is not permanently gone: an
identical value re-enters the answer the moment any live link — `ℓ₂` already present, or a
freshly emitted link with a new identity (R6c) — bears `e` in slot `i` and `e` touches.
The answer tracks the anchoring values of the active *population*, not the fate of any one
link; conflating link-level permanence (R6a) with pair-value-level removal is exactly the
slip RE-UNIT's deduplication guards against.

The answer's stability thus reduces to two tracked motions: the region's image under editing
(RE-EDIT, with RE-CWP the exact contraction sub-case) and the active population under emission
and retraction (RE-RET).

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| RE-DEF | `RE(W, d, Σ) = { (i, e) : (∃ a ∈ addressable(Σ) : 1 ≤ i ≤ \|Σ.L(a)\| ∧ Σ.L(a).eᵢ = e ∧ touch_W(e)) }`, where `(W, d)` has `d ∈ dom(Σ.M)` and `W ⊆ T` a content-subspace V-position set resolving to `I = image(W, d, Σ)` (F-IMG, ASN-0127); `touch_W(e) ≡ coverage(e) ∩ I ≠ ∅`; `addressable(Σ) = dom(Σ.L) ∖ nullified(Σ)` (ASN-0086); frame `Σ' = Σ`. The returned `e = Σ.L(a).eᵢ` is the whole slot endset (RE-WHOLE) | introduced |
| RE-LOC | Locality — for fixed `(W, d)`, `RE` reads `Σ.M(d)` (image) and `Σ.L` (endsets, and via `nullified` addressability) alone; `Σ.C`, `Σ.E`, `Σ.R` are never consulted. Hence `RE` is a deterministic function of `(W, d, Σ)` | introduced |
| RE-UNIT | Anchoring without names — the answer's elements are `(role, endset)` pairs, never link identities; the address is withheld, distinct links sharing an endset value collapse to one pair, multiplicity is not recoverable, and a surfaced from-endset cannot be paired with its link's to-endset | introduced |
| RE-OVL | Overlap matching — an endset is surfaced iff at least one address it covers lies in the region's image (overlap, not containment); single-address overlap suffices; the test is existential *within* an endset and applied *per-endset*, with no per-slot request differentiation | introduced |
| RE-CLIP | No clipping — every surfaced span is reported at the full extent recorded in the link, never truncated to the region boundary; universal across both the whole-endset (RE-WHOLE) and touching-spans-only readings | introduced |
| RE-WHOLE | Whole-endset surfacing (adopted convention) — a surfaced endset is returned in full, *all* its spans (not only those intersecting `W`); not forced by RE-CLIP, held **provisional** pending Open Question 1 | introduced (provisional) |
| RE-BND | Boundary cases — `RE(W, d, Σ) = ∅` whenever the image is empty (`W ∩ dom(Σ.M(d)) = ∅`) or `addressable(Σ) = ∅`; an empty endset slot has `coverage(∅) = ∅`, so `touch_W(∅)` is false and it is never surfaced | introduced |
| RE-ADDR | Fresh-output addressability — a fresh `K.λ` output that does not retract its own emitter address is addressable in its post-state (`ℓ_new ∉ nullified(Σ')`); in particular every non-retraction emission (`K ≁ Θ`) is addressable, at every arity. Conditions: the standing discipline commitment's unit-depth to-set and R0a/FlatLinkDomain (ASN-0086) | introduced |
| RE-SND | Soundness — `(i, e) ∈ RE(W, d, Σ) ⟹ e` is a genuine slot-`i` endset of an addressable link ∧ `touch_W(e)`; no false positives | introduced |
| RE-CMP | Completeness — every addressable link `a` and slot `i` with `touch_W(Σ.L(a).eᵢ)` has `(i, Σ.L(a).eᵢ) ∈ RE(W, d, Σ)`; the answer is *exactly* the touching set, native or transcluded content alike | introduced |
| RE-UDIST | Union-distributivity — `RE(W₁ ∪ W₂, d, Σ) = RE(W₁, d, Σ) ∪ RE(W₂, d, Σ)`, the RE-level analogue of F-UDIST/F-VDIST (ASN-0127) | introduced |
| RE-UDIST-∩ | Intersection (one-sided) — `RE(W₁ ∩ W₂, d, Σ) ⊆ RE(W₁, d, Σ) ∩ RE(W₂, d, Σ)` holds unconditionally, by the image `⊆` law; the reverse `⊇` **fails in general**, exhibited by a concrete counterexample whenever `Σ.M(d)` is non-injective (M13, M14, ASN-0058). Whether an arrangement restriction (injectivity) recovers equality is the open refinement (Open Question 4) | introduced |
| RE-SEL | Discovery-side selection — `sel(W, d, Σ) = findlinks_V(W, d, Σ) ∩ addressable(Σ)` (F-V, ASN-0127): the contributing links are the addressable links discoverable through the region, so `RE` is discovery-anchored — present-tense, non-monotone (D-NONMONO, D-ZERO, ASN-0127), not existence-anchored | introduced |
| RE-TRANS | Transclusion blindness — surfacing is by content identity, independent of the link's home and the covered content's origin (LP16, ASN-0098): a link reaching the region through transcluded content is surfaced identically to one on native content, each span describing content identity, not the borrowing V-position | introduced |
| RE-IDENT | Content-identity invariance — each surfaced endset's coverage is permanent (L12, ASN-0043; LP3, ASN-0098), so the content-level answer (which I-addresses each surfaced endset anchors to) is arrangement-independent, even though the *selection* of surfaced endsets is arrangement-mediated | introduced |
| RE-EDIT | Present-tense stability under editing — `RE` tracks `d`'s content-subspace arrangement, so the answer is non-monotone (D-NONMONO, ASN-0127) while each surfaced endset's spans stay invariant (RE-IDENT). The answer moves only under the content-subspace arrangement movers on `d` (`K.μ` extension/contraction/reordering, and ASN-0082's M-only shift-based insert/delete) and `K.λ` emission/retraction (RE-RET); every other transition — including all **link-subspace-confined** edits on `d` under `W ⊆ s_C` (`K.μ⁺_L` and content-retaining `K.μ⁻`) — leaves it fixed | introduced |
| RE-RET | Retraction stability — withdrawing a link `ℓ` (Nullify, ASN-0086) marks it nullified, removing it from `addressable(Σ)` permanently (R6a). Conditions: the standing discipline commitment (retractions via `Nullify` — empty from-set, unit-depth to-set) and the net-removal-only hypothesis `coverage(Θ) ∩ dom(Σ.C) = ∅` (`Θ` the retraction type, the sole remaining exception). Then a pair `(i, e)` that `ℓ` bore drops **iff `ℓ` was its sole addressable bearer in `Σ`** (RE-UNIT) | introduced |
| RE-CWP | Contraction-stability weakest precondition — for a `K.μ⁻[d, R]` step, `RE(W, d, ·) = RE(W, d, Σ)` iff `enabled(K.μ⁻[d, R]) ∧ (∀ (i, e) ∈ Avail(Σ) : coverage(e) ∩ Δ ≠ ∅ ⟹ coverage(e) ∩ I_R ≠ ∅)`, where `I_R = {Σ.M(d)(v) : v ∈ W ∩ R}` (D-CWP bridge, ASN-0127) and `Δ = image(W, d, Σ) ∖ I_R`. The boundary `R = ∅` collapses to `RE(W, d, Σ) = ∅` | introduced |

## Open Questions

Must a surfaced endset be reported in its entirety, or only those of its spans that intersect the region — and which choice is the faithful rendering of the link's anchoring?

When distinct addressable links carry an identical endset value in the same slot, must the operation's answer preserve their multiplicity, or is collapsing them to a single surfaced endset a faithful answer?

When a surfaced endset is rendered into the querying document's V-positions rather than content identity, what must the answer guarantee for endset content the document does not currently arrange?

Under what restriction on the arrangement `Σ.M(d)` — injectivity the natural candidate — is intersection-equality `RE(W₁ ∩ W₂, d, Σ) = RE(W₁, d, Σ) ∩ RE(W₂, d, Σ)` recovered, given that the bare `⊇` direction fails in general under a non-injective arrangement (RE-UDIST-∩; M13, M14, ASN-0058)?

What completeness guarantee must hold when anchoring that touches a region resides in a link store not co-resident with the queried document?

What must hold of a type-slot match against a content region for it to be meaningful, given that type endsets are matched by address and ordinarily reference classifying addresses disjoint from content?

What must a region query guarantee when its V-positions are drawn from the link subspace (`subspace(v) = s_L`) rather than the content subspace — resolving, by S3★ (ASN-0047), to an image inside `dom(Σ.L)` (link addresses, not content), so that the touch test surfaces anchoring aimed at links (the to-endsets of retraction emitters, type endsets) and the exactness of retraction stability acquires an extra term for the retraction emitter `b`, whose to-set then meets the image?
