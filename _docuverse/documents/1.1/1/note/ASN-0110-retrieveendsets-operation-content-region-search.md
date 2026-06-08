# ASN-0110: RETRIEVEENDSETS Operation (content-region search)

*2026-06-04*

We are handed a region of content and asked a deceptively simple question: *which link
endsets touch it?* To answer with any rigour we must pin down three things at once — what a
"region" is, what "touch" means, and what the operation hands back. The temptation is to
answer "the links that touch the region." But that is a different question, answered by a
different operation: content→link discovery returns link *identities*. Here we are asked for
the *endsets* — the span-sets through which links attach themselves to content. The operation
returns spans, and it withholds the addresses of the links that own them. The whole character
of the operation lives in that withholding, and most of this note is an attempt to say
precisely what survives it and what does not.

We will write `retrieveendsets` for this operation. It is a pure query: it reads state and
changes none. Its frame is therefore total — `Σ' = Σ` for any state `Σ` it is evaluated at —
and we shall not repeat this frame clause at each claim. What it *reads* is the more
interesting question, and the answer turns out to govern almost everything else.

## The state we consult, and the state we do not

We work over the substrate state `Σ = (Σ.C, Σ.L, Σ.M, …)` in which `Σ.C : T ⇀ Val` is the
content store, `Σ.L : T ⇀ Link` is the link store, and `Σ.M(d) : T ⇀ T` is document `d`'s
arrangement mapping V-positions to I-addresses (ASN-0093, ASN-0047). A link value is a finite
sequence of `N ≥ 3` endsets `(e₁, …, e_N)` with the type slot `e₃ ≠ ∅` (L3, ASN-0093); each
endset is a finite set of well-formed spans, `Endset = 𝒫_fin(Span)` (ASN-0043). For a span
`(s, ℓ)` its denotation is the half-open tumbler interval `⟦(s, ℓ)⟧ = {t ∈ T : s ≤ t < s ⊕ ℓ}`
(T12, ASN-0034), and the *coverage* of an endset is the union of its spans' denotations,

```
coverage(e) = (∪ (s, ℓ) : (s, ℓ) ∈ e : {t ∈ T : s ≤ t < s ⊕ ℓ})        (ASN-0043, ASN-0098)
```

a set of I-addresses. Coverage is a purely combinatorial property of the endset's span
representation; it consults no other state component.

The first thing to observe — and it dictates the whole semantics — is that the touching test
will be phrased against `coverage`, hence against `Σ.L` alone. The operation never reads
`Σ.C(a)`: it does not look at *what content sits at* an address, only at *which addresses an
endset references*. This is the same identity-not-value discipline that governs link
discovery (F5, ASN-0099). Two queries that differ only in stored content values must return
identical endsets. We will make this precise as determinism; for now we simply note which
doors we have refused to open.

## When does an endset touch a region?

Let the queried region be an I-region `I ⊆ T` — a set of I-addresses. (We treat regions
phrased in a document's V-space later, by reduction to this case.) For the operation to be
*realizable* the region cannot be an arbitrary, possibly infinite, subset of `T`: it must be
*finitely presented*, supplied as a finite span-set `Q ∈ 𝒫_fin(Span)` whose denotation is
`I = coverage(Q)` (RE-decide below). We continue to write the region as the abstract set `I`
throughout, since the semantics depend only on `I`'s extension and not on which span-set
presents it (RE-rep), but every realizability and termination claim leans on this finite
presentation. We say an endset `e` *touches* `I` exactly when its coverage meets the region:

> **RE-touch (definition).** `touches(e, I) ≡ coverage(e) ∩ I ≠ ∅`.

The relation asked for in the question — what must hold between a returned endset and the
region — is precisely non-empty intersection, and nothing stronger. We are not requiring the
endset to be contained in the region, nor the region in the endset; a single shared address
suffices. Unfolding the coverage union, `touches(e, I)` holds iff *some* span of `e` overlaps
`I`:

> **RE-overlap (lemma).** `touches(e, I) ⟺ (E (s, ℓ) : (s, ℓ) ∈ e : ⟦(s, ℓ)⟧ ∩ I ≠ ∅)`. When
> `I` is itself a span denotation `⟦(q, m)⟧ = [q, q ⊕ m)`, a span `(s, ℓ) ∈ e` overlaps it iff
> `q < s ⊕ ℓ` and `s < q ⊕ m` — the standard half-open interval-intersection predicate (SC,
> ASN-0053). *Boundary contact is not touching:* if `q ⊕ m = s` (the region ends exactly where
> the endset's span begins) then `s < q ⊕ m` fails, so adjacency in the sense of SC case (ii)
> produces no overlap. Only SC cases (iii)–(v) — proper overlap, containment, equality —
> qualify.

RE-overlap reduces touching to a per-span overlap test, and that reduction is what makes the
operation computable rather than merely defined. We make the obligation explicit, since an
operation stated over an arbitrary `I ⊆ T` is not discharged until its touching test is shown
decidable and its search shown to terminate.

> **RE-decide (lemma).** *With the region finitely presented as `Q ∈ 𝒫_fin(Span)`, `I =
> coverage(Q)`, the touching test is decidable and the search over the store terminates.* For a
> single endset `e` — itself a finite span-set, `Endset = 𝒫_fin(Span)` (ASN-0043) — RE-overlap
> with the coverage of `Q` unfolds `touches(e, I)` into the finite double disjunction
> `(E (s, ℓ) ∈ e, (q, m) ∈ Q : ⟦(s, ℓ)⟧ ∩ ⟦(q, m)⟧ ≠ ∅)`. Each per-pair overlap is the
> half-open interval predicate `q < s ⊕ ℓ ∧ s < q ⊕ m`, whose displaced endpoints `s ⊕ ℓ` and
> `q ⊕ m` exist by TA0 and exceed their starts by TA-strict, and whose four comparisons are
> settled by the intrinsic, terminating tumbler order T2 (ASN-0034). The enclosing search ranges
> over `dom(Σ.L)` — finite by L-fin (ASN-0093) — and within each link over finitely many slots
> `i ≤ |Σ.L(a)|` and finitely many spans per endset. A finite union of finite, decidable tests
> terminates, so `W(I, Σ)` and every `Eᵢ(I, Σ)` are computable. This is the region-search
> counterpart of the decidability arguments the foundations carry for the same `coverage ∩ I`
> shape (CoverageEqualityDecidable, ASN-0086; F4 remark, ASN-0099).

> **RE-rep (lemma).** The result depends only on the *extension* `I = coverage(Q)`, not on the
> span-set `Q` presenting it: if `coverage(Q) = coverage(Q')` then `retrieveendsets` agrees on
> the two presentations, since `touches(e, ·)` is defined through the set `I` alone (cf. LP21,
> ASN-0098; L8, ASN-0043). Distinct finite span-sets with the same coverage are interchangeable
> as queries.

Two structural facts about RE-overlap deserve emphasis because they distinguish this operation
from its neighbours. First, within an endset the test is a disjunction over spans: *one* span
landing in `I` is enough, exactly as Nelson's satisfaction rule demands ("one span of each
endset satisfies a corresponding part of the request", LM 4/58). Second — and this is the
sharp contrast with content→link discovery — there is only *one* region here, and every endset
of every role is tested against that same region independently. Content→link discovery
(FINDLINKSFROMTOTHREE) takes a region *per role* and conjoins: a link qualifies only if its
from-set meets the from-region *and* its to-set meets the to-region *and* its type-set meets
the type-region — an AND of ORs. `retrieveendsets` has no conjunction at all. It is a pure
disjunction: report every endset, of any link, of any role, that meets the single region. The
two operations sit on opposite sides of the same satisfaction algebra, and confusing them is
the classic error.

## What is returned

We first record, for the purpose of precise statement, the complete internal account of which
endsets qualify — the *witness set* of (link, slot) pairs:

> **RE-witness (definition).**
> `W(I, Σ) = {(a, i) : a ∈ dom(Σ.L) ∧ 1 ≤ i ≤ |Σ.L(a)| ∧ touches(Σ.L(a).eᵢ, I)}`.

The witness set carries link addresses; it is the object against which we state soundness and
completeness. But it is *not* what the operation returns. The operation returns endsets,
organized by role, with the link address projected away. For each role index `i ≥ 1`:

> **RE-result (definition).** For each role index `i ≥ 1`,
> `Eᵢ(I, Σ) = {Σ.L(a).eᵢ : (a, i) ∈ W(I, Σ)}`.

The operation returns these families *as a tuple*, and we must pin down its length, since a
heterogeneous store (links of arity 3, 5, 7) does not fix it by inspection of the standard
triple. The underlying object is the total function `i ↦ Eᵢ(I, Σ)` on `i ≥ 1`, and it is
*eventually empty*: writing

```
N_max(Σ) = max{|Σ.L(a)| : a ∈ dom(Σ.L)}        (N_max(Σ) = 0 when dom(Σ.L) = ∅)
```

for the greatest arity *present in the store*, no link possesses a slot beyond `N_max(Σ)`, so
`(a, i) ∈ W(I, Σ)` forces `i ≤ |Σ.L(a)| ≤ N_max(Σ)` and hence `Eᵢ(I, Σ) = ∅` for every
`i > N_max(Σ)`. The family thus collapses to a finite prefix, which we take as the returned
object:

> **RE-arity (definition).** `retrieveendsets(I, Σ) = ⟨E₁(I, Σ), …, E_{N_max(Σ)}(I, Σ)⟩`, a
> tuple of length `N_max(Σ)`. The length is fixed by the maximum arity among *all* links in the
> store — not the maximum among *touching* links, and not the maximum within the region — so it
> is stable under which region is queried. When `dom(Σ.L) = ∅` the tuple is empty.

Whether the length is read from the store's maximum arity or, equivalently, taken as the
total function `i ↦ Eᵢ` truncated at its last non-empty index is a presentational choice with
no semantic content: the two agree because `Eᵢ = ∅` for `i > N_max(Σ)`. What does carry
content is the treatment of *empty interior slots*. A role-slot `i ≤ N_max(Σ)` whose family
`Eᵢ(I, Σ) = ∅` — say an arity-4 link is present, fixing `N_max(Σ) ≥ 4`, yet no slot-4 endset
of any link touches `I` — still *occupies* position `i` in the tuple, reported as the empty
set rather than dropped. The index range is determined by the store's arities; the contents of
each slot, by the touching test; the two are independent. This matches Gregory's
implementation, which always emits the three standard slots (from, to, type) and writes a
count-zero endset for any role with no touching contribution rather than omitting the slot
(SS-RETRIEVE-ENDSETS, ST-RETRIEVE-ENDSETS).

The empty query region is the boundary that makes this length discipline visible.

> **RE-zero (lemma).** When `I = ∅`, no endset touches: `coverage(e) ∩ ∅ = ∅`, so
> `touches(e, ∅)` is false for every `e`, whence `W(∅, Σ) = ∅` and `Eᵢ(∅, Σ) = ∅` for every
> `i`. The result is therefore `⟨∅, …, ∅⟩` — a tuple of `N_max(Σ)` empty slots, *not* the
> empty tuple. The length is fixed by the store's arities (RE-arity), independent of the
> region, so an empty region yields the same shape as a non-empty one with all-empty contents,
> and the empty tuple arises only in the degenerate `dom(Σ.L) = ∅` case where `N_max(Σ) = 0`.

`I = ∅` is a reachable input, not a pathological one: it is exactly the I-side image of a
fully-deleted V-region (RE-Vside below), and RE-zero is the explicit I-side referent of the
V-side "finds nothing" reduction.

For the standard triple `N_max(Σ) = 3` and the tuple is the familiar
`⟨from-results, to-results, type-results⟩` (Q14). Each `Eᵢ` is a *set of endsets* — a set
whose members are themselves span-sets — and it is finite because `dom(Σ.L)` is finite
(L-fin, ASN-0093) and a set cannot exceed its index. The role separation is intrinsic to the
return shape: an endset appears under role `i` precisely when it is the `i`-th endset of some
touching link, and there is no cross-role contamination, because slot index is a primitive of
the link value, not a derived label (L6, ASN-0043).

> **RE-role (lemma).** `e ∈ Eᵢ(I, Σ) ⟺ (E a : a ∈ dom(Σ.L) ∧ i ≤ |Σ.L(a)| : Σ.L(a).eᵢ = e ∧
> touches(e, I))`. The same endset *value* may appear under two different roles (one link's
> from-set may equal another link's to-set), but each occurrence is filed by the slot it
> occupies, and the families `Eᵢ` are pairwise independent.

A conforming implementation's role-`i` output `resultᵢ(I, Σ)` must reproduce `Eᵢ` exactly. We
state the two halves separately because each is a genuine obligation:

> **RE-sound (lemma).** `resultᵢ(I, Σ) ⊆ Eᵢ(I, Σ)`: every returned endset touches `I`. No
> endset is returned which fails to touch the region at all — the soundness Nelson's design
> requires of the constrained side of a search.

> **RE-complete (lemma).** `Eᵢ(I, Σ) ⊆ resultᵢ(I, Σ)`: every endset that touches `I` is
> returned. None is omitted. The quantity of *non*-touching endsets elsewhere in the store
> cannot suppress a touching one (LM 4/60): completeness is a statement about the satisfaction
> set, indifferent to the size of its complement.

> **RE-exact (theorem).** `resultᵢ(I, Σ) = Eᵢ(I, Σ)`. Soundness and completeness together pin
> the result down to exactly the touching endsets, leaving an implementation no latitude in
> *which* endsets to report.

## The returned endset is whole, not clipped

A subtle point hides in RE-result. The witness condition requires only that *one* span of
`Σ.L(a).eᵢ` overlap `I`. But the object placed in `Eᵢ` is the *entire* value `Σ.L(a).eᵢ` —
every span of it, including spans whose denotation misses `I` entirely.

> **RE-full (lemma).** For `(a, i) ∈ W(I, Σ)`, the member of `Eᵢ(I, Σ)` contributed by `a` is
> the complete stored endset `Σ.L(a).eᵢ`, not the clipped span-set denoting `coverage(eᵢ) ∩ I`.

We should justify why this is the right abstract choice and not merely an implementation
accident. There are two arguments, and they agree. The first is structural: the stored value
`Σ.L(a).eᵢ` is an atomic, immutable component of the link (L12, ASN-0043). The operation
*reads* it; it does not synthesize a derived fragment. A returned object that was "the endset
intersected with the query window" would be a new value the store never held, and there is no
state in which it resides. The second is semantic, and it is Nelson's: an endset is the link's
*reach* — to follow or comprehend the link one needs the whole of what it connects, not a
truncation clipped to the accident of one's query window. A clipped endset would point only at
the part of the link that one already knew about, which defeats the purpose of asking. So the
returned endset is whole.

This is worth contrasting with the I→V resolution layer, where clipping genuinely occurs: when
an endset's coverage is *presented* in a querying document's V-space, only the portion of the
endset the document currently arranges can be named, and the rest is silently dropped
(ASN-0098 LP17; Q16). That clipping is a property of the *presentation*, not of the endset
retrieval itself. The endset, as an object, is returned in full; what a particular document's
coordinate system can *display* of it is a separate, lossy projection we treat below.

## A worked instance

The definitions above are easier to trust against concrete data. We fix a document
`d = 1.0.1.0.1` (a document-level tumbler, `zeros(d) = 2`, T4-valid) and five element-level
content addresses in its content subspace (`s_C = 1`), siblings differing only in their final
ordinal:

```
c₂ = 1.0.1.0.1.0.1.2     c₃ = 1.0.1.0.1.0.1.3     c₄ = 1.0.1.0.1.0.1.4
c₅ = 1.0.1.0.1.0.1.5     θ  = 1.0.1.0.1.0.1.7
```

Each has depth `#cₖ = 8`, so the unit ordinal displacement at that depth is
`δ(1, 8) = [0,0,0,0,0,0,0,1]`, and a span `(cₖ, δ(1, 8))` covers exactly `{cₖ}` among the
element-level addresses (its half-open interval `[cₖ, shift(cₖ, 1))` reaches up to but excludes
the next sibling). We query the **I-region** `I = {c₂, c₃}`.

The link store holds two arity-3 links, in the link subspace (`s_L = 2`):

```
a₁ = 1.0.1.0.1.0.2.1,  Σ.L(a₁) = (F₁, G₁, Θ)
    F₁ = {(c₂, δ(1,8)), (c₄, δ(1,8))}   coverage {c₂, c₄}
    G₁ = {(c₅, δ(1,8))}                 coverage {c₅}
    Θ  = {(θ,  δ(1,8))}                 coverage {θ}

a₂ = 1.0.1.0.1.0.2.2,  Σ.L(a₂) = (F₂, F₁, Θ)
    F₂ = {(c₃, δ(1,8))}                 coverage {c₃}
    e₂ = F₁  (the *same endset value* {(c₂,δ(1,8)),(c₄,δ(1,8))}, now filed in slot 2)
    e₃ = Θ
```

`F₁` is deliberately constructed with one *touching* span `(c₂, δ(1,8))` — `c₂ ∈ I` — and one
*non-touching* span `(c₄, δ(1,8))` — `c₄ ∉ I` — so the example exercises RE-full. And `a₂`
reuses the value `F₁` in its **to**-slot (slot 2), which exercises RE-role's claim that one
endset value may be filed under two different roles.

*Touching test, slot by slot.* Applying RE-touch (`coverage(e) ∩ I ≠ ∅`):

| (link, slot) | endset | coverage | `∩ I` | touches? |
|---|---|---|---|---|
| (a₁, 1) | F₁ | {c₂, c₄} | {c₂} | yes |
| (a₁, 2) | G₁ | {c₅}     | ∅     | no |
| (a₁, 3) | Θ  | {θ}      | ∅     | no |
| (a₂, 1) | F₂ | {c₃}     | {c₃} | yes |
| (a₂, 2) | F₁ | {c₂, c₄} | {c₂} | yes |
| (a₂, 3) | Θ  | {θ}      | ∅     | no |

So the witness set is `W(I, Σ) = {(a₁, 1), (a₂, 1), (a₂, 2)}`.

*The returned families.* By RE-result, collecting endset *values* per role:

```
E₁(I, Σ) = {Σ.L(a₁).e₁, Σ.L(a₂).e₁} = {F₁, F₂} = { {(c₂,δ),(c₄,δ)}, {(c₃,δ)} }
E₂(I, Σ) = {Σ.L(a₂).e₂}             = {F₁}     = { {(c₂,δ),(c₄,δ)} }
E₃(I, Σ) = ∅
```

with `N_max(Σ) = 3` (both links arity 3), so
`retrieveendsets(I, Σ) = ⟨{F₁, F₂}, {F₁}, ∅⟩` — a length-3 tuple whose third slot is the empty
set *reported in position*, per RE-arity: no slot-3 endset touches `I`, but the slot is present.

*RE-full check.* The member `F₁ ∈ E₁(I, Σ)` is returned **whole** — it includes the span
`(c₄, δ(1,8))` whose coverage `{c₄}` misses `I` entirely. The operation does not clip `F₁` to
`coverage(F₁) ∩ I = {c₂}`; the stored value `{(c₂,δ),(c₄,δ)}` is handed back intact, exactly as
RE-full requires.

*RE-role check.* The single endset value `F₁ = {(c₂,δ),(c₄,δ)}` appears in `E₁(I, Σ)` (as
`a₁`'s from-slot) *and* in `E₂(I, Σ)` (as `a₂`'s to-slot). Its two occurrences are filed by the
slot each occupies, not merged; the families `E₁` and `E₂` are independent, just as RE-role
states. Conversely, `E₁` collects `F₁` and `F₂` from two different links into one role-set,
confirming that a role-family is a union across all touching links at that slot, not a per-link
tuple.

## What the result reveals about the links — and what it withholds

The operation returns endsets and never an address. We can make the withholding precise, and
in doing so we discover that it withholds more than identity: it withholds count.

> **RE-anon (theorem).** The result `retrieveendsets(I, Σ)` does not determine the set of
> contributing link addresses. There exist states `Σ`, `Σ'` with
> `retrieveendsets(I, Σ) = retrieveendsets(I, Σ')` but `{a : (a, i) ∈ W(I, Σ) for some i} ≠
> {a : (a, i) ∈ W(I, Σ') for some i}`.

*Construction.* The link store permits two distinct addresses to hold the same endset
sequence (L11b non-injectivity, ASN-0043). Let `Σ` contain a single link `a₁` with value
`(e, e', θ)` where `touches(e, I)`. Extend to `Σ'` by allocating a fresh `a₂ ≠ a₁` with the
identical value `(e, e', θ)` — admissible by L11b and K.λ (ASN-0093). Now
`E₁(I, Σ) = {e} = E₁(I, Σ')`, because the set comprehension collapses the two identical
contributions; likewise for every role. So the results coincide. Yet the contributing-link
sets are `{a₁}` and `{a₁, a₂}` — different, and of different cardinality. ∎

The corollary is that the *number* of distinct links anchored to the region is not recoverable
from the result. Two links with coincident endsets are indistinguishable in the output, so the
result yields at most a lower bound (the number of distinct endset values present), never the
true count. This is by design and by division of labour: counting how many links touch a
region is a separate operation (FINDNUMOFLINKS), out of scope here. The guaranteed return
object per role is fixed as the *set* `Eᵢ(I, Σ)` of touching endset values (RE-result), and
RE-exact is read as literal set equality. Identical endset values contributed by distinct
links are therefore collapsed to a single member by the set comprehension — the result carries
no multiplicity information at all, and an implementation has no latitude to report a value
twice. An implementation that internally accumulates one occurrence per contributing link must
deduplicate to the underlying set before returning; multiplicity is not merely "not
guaranteed," it is structurally absent. What is guaranteed, exactly, is the *set* of touching
endset values per role.

What, then, does the result reveal? It reveals connectivity, anonymously.

> **RE-reveal (observation).** From `retrieveendsets(I, Σ)` one recovers, for each role, the
> set of content regions the queried region is connected through — namely the coverages
> `{coverage(e) : e ∈ Eᵢ(I, Σ)}`. One *cannot* recover which from-endset pairs with which
> to-endset, because the per-link tuple grouping is dissolved by role separation: the operation
> reports "here are the from-endsets that touch, here are the to-endsets that touch," never
> "this from goes with that to." Reconstructing the pairing would be tantamount to naming the
> links, which the operation refuses to do.

So the per-link grouping that link-as-unit operations must preserve (so that following a link
from one end to the other remains possible) is *exactly* the structure `retrieveendsets`
sacrifices in exchange for withholding identity. The role separation is the only grouping that
survives, and it is enough to surface connectivity while concealing which connective unit
established it.

## Endsets are I-address structure: stability under editing

The coverage of an endset is a set of I-addresses, and I-addresses are permanent content
identities, untouched by the editing operations that rearrange a document's V-space (P0/L12).
This is the source of survivability, and it lets us separate cleanly the two senses in which a
"region" can change.

> **RE-immut (lemma).** Across any transition `Σ → Σ'` and for any link `a ∈ dom(Σ.L)` and slot
> `i`, the endset value persists unchanged: `a ∈ dom(Σ'.L) ∧ Σ'.L(a).eᵢ = Σ.L(a).eᵢ`, hence
> `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)` (L12, ASN-0043; LP3★, ASN-0098). The returned
> endsets are verbatim stored values, and they reference the same content identities forever.

Because the I-side touching test reads only `Σ.L` and the supplied region `I`, the result is
invariant under every edit that leaves the link store alone:

> **RE-surv (lemma).** Let `Σ → Σ'` be any arrangement edit — a K.μ-family transition
> (`K.μ⁺`, `K.μ⁻`, `K.μ⁺_L`, or the composite `K.μ~`), each of which frames `L' = L` (A1a,
> ASN-0099). Then `retrieveendsets(I, Σ') = retrieveendsets(I, Σ)`. Insertion, deletion, and
> rearrangement of a document's V-positions do not change which endsets touch a given I-region.

This is precisely Nelson's survivability ("links between bytes can survive deletions,
insertions and rearrangements", LM 4/43), now stated as an invariance: the endsets follow the
surviving content because they *are* the content's I-addresses, and an I-region query is blind
to where those addresses currently sit in any document.

## Determinism, idempotence, and the additive, monotone structure

Gathering the read-set discipline into one statement:

> **RE-det (lemma).** `retrieveendsets(I, Σ)` is a function of `(I, Σ.L)` alone. If
> `Σ.L = Σ'.L` as partial functions then `retrieveendsets(I, Σ) = retrieveendsets(I, Σ')`. The
> test consults `dom(Σ.L)`, the per-link arities and endset values, and `coverage`; it never
> consults `Σ.M`, `Σ.C`, or any other component (cf. ComprehensionInvariantUnderΣL, ASN-0099).

This is the exact sense in which the operation is *idempotent* — and it sharpens the naive
expectation. Repeated queries return identical endsets **when the link store is unchanged**,
not merely when the *content* is unchanged. The distinction is real and Nelson-faithful: a
third party may anchor a brand-new link into the region without altering a single byte of its
content (a link's home document records who owns it, not where it points, LM 4/12). Such an
act changes `Σ.L` while leaving `Σ.C` and even the queried content untouched, and the result
*may* legitimately grow. Idempotence is conditioned on `Σ.L`-fixity, which content-fixity does
not imply.

The direction of any such change is constrained. Endsets, once touching, stay touching, and
the result only grows:

> **RE-mono (lemma).** For every reachable `Σ →* Σ'`, `Eᵢ(I, Σ) ⊆ Eᵢ(I, Σ')`. *Proof.* For
> `(a, i) ∈ W(I, Σ)`: link persistence gives `a ∈ dom(Σ'.L)` with `Σ'.L(a).eᵢ = Σ.L(a).eᵢ`
> (RE-immut), coverage is preserved, so `touches` holds at `Σ'` and the same endset value lies
> in `Eᵢ(I, Σ')`. ∎ New links allocated by `K.λ` may add further endsets; none are removed.

RE-mono tells us the result only grows, but not *what it takes* for a particular endset to
enter under a particular role. The single growth step is `K.λ` — link allocation is the unique
operation that touches `Σ.L` (A1, ASN-0099); every other transition fixes the store and leaves
all families verbatim. So the sharp question is a weakest-precondition one: given that a `K.λ`
step is about to allocate a link of value `(e₁, …, e_N)`, under what condition on that value
does a target endset land in role `j` of the post-state? This is the region-search analogue of
F9-λ (ASN-0099), and it makes the conditional-idempotence of RE-det precise.

> **RE-wp (lemma).** Let the next transition be a `K.λ` step allocating a fresh link at address
> `ℓ_new` with value `(e₁, …, e_N)` homed at `d` (the `K.λ` precondition `pre ≡ d ∈ dom(Σ.M) ∧
> N ≥ 3 ∧ e₃ ≠ ∅ ∧ ℓ_new ∉ dom(Σ.L) ∪ dom(Σ.C)`, ASN-0093). For any endset value `e` and role
> index `j`,
> ```
> wp(K.λ, "e ∈ Eⱼ(I, Σ')") = pre ∧ ( e ∈ Eⱼ(I, Σ)  ∨  (j ≤ N ∧ eⱼ = e ∧ touches(e, I)) ).
> ```
> *Proof.* `K.λ` sets `Σ'.L = Σ.L ∪ {ℓ_new ↦ (e₁, …, e_N)}` with `ℓ_new` fresh, so
> `dom(Σ'.L) = dom(Σ.L) ⊎ {ℓ_new}`. A witness for `e ∈ Eⱼ(I, Σ')` is a link `a ∈ dom(Σ'.L)` with
> `j ≤ |Σ'.L(a)|`, `Σ'.L(a).eⱼ = e`, and `touches(e, I)`. Two disjoint cases. If `a ∈ dom(Σ.L)`,
> value preservation (RE-immut) makes the witness condition identical at `Σ`, i.e. exactly
> `e ∈ Eⱼ(I, Σ)`. If `a = ℓ_new`, then `|Σ'.L(ℓ_new)| = N` and `Σ'.L(ℓ_new).eⱼ = eⱼ`, so the
> witness reduces to `j ≤ N ∧ eⱼ = e ∧ touches(e, I)`. The two cases are mutually exclusive by
> freshness, giving the disjunction. ∎

The two disjuncts cleanly separate the two phenomena. The first, `e ∈ Eⱼ(I, Σ)`, is
*unconditional persistence* — it places no constraint at all on the allocated value, and is
just RE-mono restated: whatever was touching stays touching no matter what `K.λ` does. The
second is the *genuine growth condition*, and it is gated **entirely on the allocated link
value** — the role index `j ≤ N`, the slot value `eⱼ = e`, and `touches(e, I) ⟺ coverage(e) ∩ I
≠ ∅`. It mentions neither `Σ.M` nor `Σ.C`: result growth is a pure `Σ.L` event, exactly as
RE-det demands. Specialising to a *newly entering* endset (`e ∉ Eⱼ(I, Σ)`), the weakest
precondition collapses to
```
wp(K.λ, "e newly in Eⱼ(I, Σ')") = pre ∧ j ≤ N ∧ eⱼ = e ∧ touches(e, I),
```
which is the precise statement of when a region's connectivity grows: someone files an endset
value `e` that overlaps `I` into slot `j` of a freshly allocated link. The non-emptiness
construction of RE-empty below is one instantiation of this precondition at `j = 1`.

Consequently an empty result is a faithful snapshot of present connectivity, never a permanent
property of the region:

> **RE-empty (lemma).** A region with no touching endset yields `Eᵢ(I, Σ) = ∅` for every `i` —
> a normal, supported outcome, not an error. But emptiness is not permanent: provided `I ≠ ∅`
> and `dom(Σ.M) ≠ ∅`, there is a `K.λ` extension `Σ → Σ'` after which the result is non-empty.
> *Construction.* Pick `t ∈ I`; the unit-depth span `(t, δ(1, #t))` has coverage `{t' : t ≼ t'}
> ∋ t`, so an endset `e = {(t, δ(1, #t))}` satisfies `touches(e, I)`. Allocate a link homed at
> any `d ∈ dom(Σ.M)` with this `e` in slot 1 and any non-empty type endset in slot 3 (K.λ, L3,
> ASN-0093). Then `e ∈ E₁(I, Σ')`. ∎

The result is also additive in the region, which legitimizes decomposing a large query into
sub-queries:

> **RE-add (lemma).** `Eᵢ(I₁ ∪ I₂, Σ) = Eᵢ(I₁, Σ) ∪ Eᵢ(I₂, Σ)`. *Proof.* `touches(e, I₁ ∪ I₂)
> ⟺ coverage(e) ∩ (I₁ ∪ I₂) ≠ ∅ ⟺ coverage(e) ∩ I₁ ≠ ∅ ∨ coverage(e) ∩ I₂ ≠ ∅`, and
> set-builder distributes over the disjunction (cf. F13, ASN-0099). ∎

## Regions phrased in a document's V-space

So far the region has been an I-set. But "a region of content" is most naturally given as a
V-region `R` inside a particular document `d` — a stretch of that document's arrangement. We
reduce this to the I-side query through the document's own POOM, exactly as content→link
discovery does (F12, ASN-0099). Let

```
image(R, d, Σ) = {Σ.M(d)(v) : v ∈ R ∩ dom(Σ.M(d))}                         (ASN-0099)
```

be the set of I-addresses that `d` currently maps `R` to, and define

> **RE-Vside (definition).** For `d ∈ dom(Σ.M)`,
> `retrieveendsets_V(R, d, Σ) = retrieveendsets(image(R, d, Σ), Σ)`. For `d ∉ dom(Σ.M)` the
> operation is undefined — there is no silent fallback.

Two behaviours follow from the structure of `image`, and both are forced rather than chosen.
First, the conversion is *silently partial*: V-positions of `R` that are not in
`dom(Σ.M(d))` — content the document never arranged, or arranged and since deleted —
contribute nothing to `image(R, d, Σ)` and therefore cannot drag in any endset (Q11, Q16). A
region whose content has been wholly deleted from `d` maps to the empty I-set, `image(R, d, Σ)
= ∅`, and the I-side query `retrieveendsets(∅, Σ)` returns `⟨∅, …, ∅⟩` of length `N_max(Σ)` by
RE-zero — not the empty tuple — even though links to that now-departed content persist in the
store and remain discoverable through *other* documents that still arrange it. The emptiness is
again a statement about the present arrangement, not about the links.

Second, the conversion is *document-agnostic at the touching layer*, which gives transclusion
for free:

> **RE-translucent (lemma).** If documents `d₁` and `d₂` both arrange a shared I-address `α`
> (transclusion), and `v₁ ∈ R₁`, `v₂ ∈ R₂` with `Σ.M(d₁)(v₁) = Σ.M(d₂)(v₂) = α`, then for every
> role `i`, `Eᵢ(image(R₁, d₁, Σ), Σ)` and `Eᵢ(image(R₂, d₂, Σ), Σ)` both contain every endset
> whose coverage includes `α`. The touching test sees only `α`'s identity, not which document
> phrased the query (cf. F6/LP16, ASN-0099). An endset anchored through transclusion is
> discovered from any document sharing the content.

The endsets returned by the V-side operation are, by RE-full, the whole stored endsets — their
coverage in I-space. Whether they are then *presented* back in `d`'s V-coordinates (so the
caller reads V-positions rather than raw I-addresses) is a separate projection, and it is
lossy in exactly the way `image` is: an I-address of the endset that `d` does not currently
arrange has no V-position to be named by, and is silently omitted from that presentation. The
endset's identity (its I-coverage) is unaffected; only what `d`'s coordinate system can show of
it is reduced. We leave the precise contract of that V-presentation to future work and record
it among the open questions.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| RE-touch | `touches(e, I) ≡ coverage(e) ∩ I ≠ ∅` | introduced |
| RE-overlap | `touches(e, I)` is non-empty half-open span overlap; one span suffices; boundary contact does not qualify | introduced |
| RE-decide | with region finitely presented as `Q ∈ 𝒫_fin(Span)`, the touching test is decidable (per-span overlap by T2) and the search terminates (L-fin, finite endsets) | introduced |
| RE-rep | result depends only on `I = coverage(Q)`, not on the span-set presenting it | introduced |
| RE-zero | `I = ∅` yields `⟨∅, …, ∅⟩` of length `N_max(Σ)`, not the empty tuple | introduced |
| RE-witness | `W(I, Σ) = {(a, i) : a ∈ dom(Σ.L), i ≤ |Σ.L(a)|, touches(Σ.L(a).eᵢ, I)}` | introduced |
| RE-result | `Eᵢ(I, Σ) = {Σ.L(a).eᵢ : (a, i) ∈ W(I, Σ)}` for each role `i ≥ 1` | introduced |
| RE-arity | result is the tuple `⟨E₁, …, E_{N_max(Σ)}⟩`, length `N_max(Σ) = max{|Σ.L(a)| : a ∈ dom(Σ.L)}`; empty interior slots reported in position | introduced |
| RE-role | endset appears under role `i` iff it is the slot-`i` endset of a touching link; roles independent, no cross-contamination | introduced |
| RE-sound | `resultᵢ ⊆ Eᵢ` — no returned endset fails to touch `I` | introduced |
| RE-complete | `Eᵢ ⊆ resultᵢ` — every touching endset returned, none omitted | introduced |
| RE-exact | `resultᵢ(I, Σ) = Eᵢ(I, Σ)` | introduced |
| RE-full | the returned endset is the whole stored `Σ.L(a).eᵢ`, not clipped to `I` | introduced |
| RE-anon | result does not determine the contributing link addresses, nor their count (via L11b) | introduced |
| RE-reveal | result reveals per-role connectivity but dissolves per-link from/to/type pairing | introduced |
| RE-immut | returned endsets are verbatim, immutable stored values with invariant coverage | introduced |
| RE-surv | result invariant under K.μ-family arrangement edits (which fix `Σ.L`) | introduced |
| RE-det | result is a function of `(I, Σ.L)` alone; idempotent under `Σ.L`-fixity, not content-fixity | introduced |
| RE-mono | `Eᵢ(I, Σ) ⊆ Eᵢ(I, Σ')` across reachable `Σ →* Σ'` | introduced |
| RE-wp | `wp(K.λ, e ∈ Eⱼ(I, Σ')) = pre ∧ (e ∈ Eⱼ(I, Σ) ∨ (j ≤ N ∧ eⱼ = e ∧ touches(e, I)))`; growth gated on allocated value alone | introduced |
| RE-empty | empty result permitted, not permanent; recoverable by `K.λ` when `I ≠ ∅`, `dom(Σ.M) ≠ ∅` | introduced |
| RE-add | `Eᵢ(I₁ ∪ I₂, Σ) = Eᵢ(I₁, Σ) ∪ Eᵢ(I₂, Σ)` | introduced |
| RE-Vside | `retrieveendsets_V(R, d, Σ) = retrieveendsets(image(R, d, Σ), Σ)`; silently partial under unmapped V-positions | introduced |
| RE-translucent | transclusion-shared endsets discovered from any document arranging the shared I-address | introduced |

## Open Questions

What must the operation guarantee about an endset presented in a querying document's V-space when that document arranges only part of the endset's coverage?

What invariant relates the endsets returned for a region to those returned for its sub-regions and super-regions, beyond additive union over the region?

Under what conditions is the per-link from/to/type pairing reconstructible from a role-separated result, and when is that reconstruction provably impossible?

What must the system guarantee about the relationship between the endsets a region-search returns and the count of distinct links anchored to that region?

What must hold for two regions with equal current arrangements but distinct deletion histories to be guaranteed indistinguishable to a V-side region search?
