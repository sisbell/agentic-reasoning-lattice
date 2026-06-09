# ASN-0121: The FINDLINKSFROMTOTHREE Operation

*2026-06-08*

We are asked to characterise the operation that, given a *description of links* phrased
as four bounding sets, returns the links that fit the description. Nelson names it
`FINDLINKSFROMTOTHREE`:

> "This returns a list of all links which are (1) in `<home set>`, (2) from all or any
> part of `<from set>`, and (3) to all or any part of `<to set>` and `<three set>`."
> (4/69)

The four sets are the **home-set** (where the links reside), the **from-set** (what
their first endset references), the **to-set** (what their second endset references),
and the **three-set** (their type or connector endset). The question we must answer is
not *how* a back end finds these links — that is mechanism — but *what* the answer must
be: for an arbitrary link to belong in the result, what must hold of it, and what must
the result as a whole guarantee against the body of links as it stands at the moment of
inquiry. We want a specification an alternative implementation would also have to meet.

We write the system state as `Σ = (Σ.C, Σ.M, Σ.L)` — the content store, the family of
document arrangements, and the link store — using the foundation vocabulary. We use
`coverage(e)` (ASN-0043) for the set of I-addresses an endset references, `home(a)`
(ASN-0043) for the document-level prefix at which a link address `a` resides, and the
total order and span machinery of ASN-0034 throughout.

## What is being matched

A link `a ∈ dom(Σ.L)` carries a value `Σ.L(a) = (e₁, e₂, …)` of at least three endsets
(L3). The first three slots are, by convention, the *from-endset* `e₁`, the *to-endset*
`e₂`, and the *type-endset* `e₃`. Each endset references a set of I-addresses, its
coverage. The link also resides somewhere: `home(a)` is a document-level tumbler,
extracted from the *address* `a` by field projection, **not** from the endsets. These
two facts — what a link *connects* (its endset coverages) and where it *lives* (its
home) — are the raw material the request will constrain.

A request is a four-tuple

  `q = (H, F, G, Θ)`,

where each component is either a *span-set* over the address space or the distinguished
*wildcard* `∗` (Nelson's NOSPECS — "no specification"). The home-component `H` ranges
over document-address space; the three endset-components `F, G, Θ` range over I-address
space. A span-set denotes, through `coverage`, a set of addresses; the wildcard denotes
"no constraint."

We must say precisely what it is for a link to satisfy *one* component. Nelson's rule
is sharp:

> "A link satisfies a search request if one span of each endset satisfies a
> corresponding part of the request." (4/58)

"One span … satisfies a corresponding part" is an existential — it suffices that the
endset and the request set share a single address. We capture this as a *touch*
relation between an endset `e` and a request set `r`:

  `touch(e, r) ≡ coverage(e) ∩ coverage(r) ≠ ∅`.

`touch(e, r)` holds exactly when some address lies in both coverages — when *one span*
of `e` covers an address *also* covered by `r`. The endset need not match `r` in its
entirety; a partial, single-span overlap is enough. This is the disjunction that lives
*inside* a slot — "from all or any part of" the requested set. The corresponding
residence test, for a link `a` and a home-set `H`, asks only that the link's residence
fall in the requested region:

  `athome(a, H) ≡ home(a) ∈ coverage(H)`.

Because a span in document-address space denotes a contiguous subtree (T5,
ASN-0034), `H` may bound residence at the granularity of a node, an account, or a single
document, and `athome` tests membership of `home(a)` against whatever that subtree is.

## The satisfaction rule: the AND of the ORs

A wildcard component imposes nothing; a span-set component imposes its touch- or
residence-test. We lift each component to a per-link predicate:

  `lift(e, ∗) ≡ true`,    `lift(e, r) ≡ touch(e, r)`   for `r ≠ ∗`,
  `liftH(a, ∗) ≡ true`,   `liftH(a, H) ≡ athome(a, H)`  for `H ≠ ∗`.

The full satisfaction predicate conjoins the four lifted components:

  `sat(a, q, Σ) ≡ liftH(a, H) ∧ lift(Σ.L(a).e₁, F) ∧ lift(Σ.L(a).e₂, G) ∧ lift(Σ.L(a).e₃, Θ)`.

This is the structure Nelson calls "the AND of the ORs." *Within* each constrained slot
the test is a disjunction — one overlapping address is enough (the `≠ ∅` in `touch`).
*Across* the four slots the tests are conjoined — a link qualifies only if it resides in
the home-set **and** its from-endset touches the from-set **and** its to-endset touches
the to-set **and** its type-endset touches the three-set. Matching any single criterion
alone is insufficient; the returned link is the *intersection* of the four constraints,
each individually satisfiable by a partial match. Gregory's back end realises exactly
this conjunction: each endset slot is queried independently against its own subspace of
the link index, and the three resulting link-sets are intersected
(`intersectlinksets`), a link surviving only if it appears in every non-wildcard slot's
set — the AND — while within a slot any single span overlap admits it — the OR
(consultation Q11, Q15).

## The answer is forced

To speak of the body of links "as it stands at the moment of inquiry" we must
distinguish links that are *currently addressable* from those that have been withdrawn.
Nelson's retracted links are "not currently addressable" (4/9). We therefore posit a
retraction set `retracted(Σ) ⊆ dom(Σ.L)`, and require it to be monotone non-decreasing
along every transition — a withdrawal, once made, persists in the current line of
descent. (The *mechanism* of retraction is another operation's concern; here we need
only its effect on addressability.) The currently addressable links are

  `addressable(Σ) = dom(Σ.L) \ retracted(Σ)`.

Now we may derive, rather than stipulate, the answer set. Demand of any candidate answer
`R` two things. *Soundness*: `(A a : a ∈ R : sat(a, q, Σ))` — nothing returned fails a
criterion. *Completeness*: `(A a : a ∈ addressable(Σ) ∧ sat(a, q, Σ) : a ∈ R)` — nothing
qualifying is omitted. The weakest predicate on an addressable link that soundness
*permits* into `R` is `sat(a, q, Σ)`; the predicate that completeness *forces* into `R`
is the same `sat(a, q, Σ)`. The two demands meet with no slack between them, leaving no
design freedom:

  `findlinks(q, Σ) = { a ∈ addressable(Σ) : sat(a, q, Σ) }`.   **(FL-DEF)**

This is a pure query: it reads `Σ.L`, the retraction set, and (for residence) link
addresses, and it writes nothing. Its frame is the whole of `Σ`: `findlinks` leaves the
content store, the arrangements, and the link store unchanged.

We record soundness and completeness as named claims even though they are now immediate
from FL-DEF, because they are the load-bearing guarantees an alternative implementation
must independently demonstrate.

**FL-SND (soundness).** `(A a : a ∈ findlinks(q, Σ) : sat(a, q, Σ))`. No returned link
fails any of the four criteria. Equivalently, in contrapositive form: if any constrained
slot is *wholly disjoint* from the request — `coverage(Σ.L(a).eᵢ) ∩ coverage(Rᵢ) = ∅`
for a constrained `Rᵢ`, or `home(a) ∉ coverage(H)` for a constrained `H` — then `a` is
not returned. There are no false positives.

**FL-CMP (completeness).** `(A a : a ∈ addressable(Σ) ∧ sat(a, q, Σ) : a ∈ findlinks(q, Σ))`.
Every currently addressable link meeting all four criteria is returned; none is silently
omitted. The result is *exactly* the satisfying subset of `addressable(Σ)`.

## Non-impedance: junk links do not obstruct

Nelson's most emphatic claim about link search is a scaling guarantee:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON
> OTHERS." (4/60)

We can state its abstract content precisely. `sat` is decided per link, independently of
every other link in the store; a link's match status is a function of its own value, its
own address, its own retraction status, and the fixed request. Consequently the result
is insensitive to the presence of non-matching links.

**FL-JUNK (non-impedance).** Let `Σ → Σ'` be a transition that adds links but matches
none of them and retracts none — `dom(Σ.L) ⊆ dom(Σ'.L)`, `retracted(Σ') = retracted(Σ)`,
and `(A a : a ∈ dom(Σ'.L) \ dom(Σ.L) : ¬ sat(a, q, Σ'))` — and that preserves the
values and home-projections of existing links. Then
`findlinks(q, Σ') = findlinks(q, Σ)`. The body of irrelevant links, however vast, neither
enlarges the answer nor displaces a qualifying link from it.

The proof rests on link immutability (L12): an existing link's value `Σ.L(a)` never
changes, and `home(a)` is a projection of the fixed address `a`, so `sat(a, q, ·)` is
constant across the transition for every `a ∈ dom(Σ.L)`. The added links fail `q` by
hypothesis. Hence the satisfying addressable set is unchanged.

## Residence and endpoints are orthogonal axes

The four sets fall into two kinds, serving different purposes. The home-set bounds
*residence*; the three endset-sets bound *endpoints*. Nelson keeps them separate by
design:

> "A link need not point anywhere in its home document. Its home document indicates who
> owns it, and not what it points to." (4/12)

This separation is visible directly in `sat`. The residence conjunct `liftH(a, H)`
depends only on `home(a)`, which is the field projection `N(a).0.U(a).0.D(a)` of the
*address* `a` — the endset values never enter it. The three endpoint conjuncts depend
only on `Σ.L(a)`'s endsets — the address-as-residence never enters them.

**FL-RES (residence–endpoint independence).** The home criterion is a function of the
link address alone; the from/to/type criteria are functions of the link value alone. The
four constraints are therefore *independent* slots of the request: residence may be
constrained without constraining endpoints, and conversely. In particular, with
`F = G = Θ = ∗` the result is every addressable link residing in `H`, irrespective of
what it connects; with `H = ∗` the result is every addressable link whose endpoints
match, irrespective of where it lives.

The independence is what makes link discovery powerful. Because residence is a separate
axis, one may ask for *all* links between two passages "regardless of who made them"
(4/63) by leaving the home-set unconstrained, and one may equally ask for *all* links
owned within a given document by leaving the endpoints unconstrained. Were residence
conflated with the endpoints, one could only find links one already owned. Gregory's
retrieval path confirms the independence operationally: link end-sets are read from the
link's own structure with no consultation of the home document's residence record, and
with the open-status of the home document explicitly bypassed (consultation Q17).

We note an implementation divergence worth recording, since it sharpens what the abstract
claim demands. Gregory's back end currently *ignores* the home-set entirely: a dead-code
guard (`TRUE||!homeset`) replaces the caller's residence bound with a fixed, effectively
universal range, so every search is global in the residence axis (consultation Q12). The
abstract operation requires `liftH` to bound results by residence; the implementation
realises only the `H = ∗` case. An alternative implementation must restore the residence
constraint to meet FL-RES.

## Directionality is positional, not symmetric

A link "is typically directional. Thus it has a from-set, the bytes the link is 'from,'
and a to-set, the bytes the link is 'to'" (4/42). Discovery must respect this asymmetry,
and `sat` does: the from-component `F` is lifted against `e₁` *only*, and the
to-component `G` against `e₂` *only*. The two are never pooled.

**FL-DIR (positional directionality).** The from-criterion tests `Σ.L(a).e₁` and the
to-criterion tests `Σ.L(a).e₂`; the slots are matched by position, not symmetrically.
The asymmetry is observable: there exist endsets with disjoint coverages `X, Y` and a
link `a` with `coverage(e₁) ∩ coverage(X) ≠ ∅`, `coverage(e₁) ∩ coverage(Y) = ∅`,
`coverage(e₂) ∩ coverage(Y) ≠ ∅`, `coverage(e₂) ∩ coverage(X) = ∅`. Such an `a` is in
`findlinks((∗, X, Y, ∗), Σ)` but not in `findlinks((∗, Y, X, ∗), Σ)`. Reversing the two
endpoint constraints is therefore not a no-op.

This is exactly what keeps "links *from* X" and "links *to* X" two different, answerable
queries. Bind the from-set to `X` and leave the to-set open — `findlinks((∗, X, ∗, ∗), Σ)`
— and the result is every link *originating* at `X`. Bind the to-set to `X` and leave the
from-set open — `findlinks((∗, ∗, X, ∗), Σ)` — and the result is every link *arriving* at
`X`, the backlink query. Had the two ends been merged into one undirected set, both
collapse to "every link touching `X`," and the direction the author asserted would be
lost. Gregory stores the two ends under distinct index subspaces and queries each against
its own slot, so a reversed request finds no link by the wrong-slot match (consultation
Q16) — the directional distinction is enforced at the index level.

## The type is a first-class slot, matched by address

For links to be discoverable by their *kind* of connection, the type must be a full
endset, structurally identical to the from- and to-sets, and matched the same way.
Nelson:

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse.
> This is symmetrical with the other endsets." (4/44)

The decisive property is *what* the type slot matches against:

> "The search mechanism does not actually look at what is stored under the 'type' it is
> searching for; it merely considers the type's address." (4/44–4/45)

In our terms, the three-component `Θ` is lifted against `coverage(e₃)` — the *address
set* the type endset references — exactly as the from- and to-components are lifted
against their endset coverages. The content store `Σ.C` is never consulted at type
addresses; matching is by address identity.

**FL-TYP (type by address).** The type criterion tests `touch(Σ.L(a).e₃, Θ)`, an overlap
of address coverages, and never reads content stored at any type address. Three
consequences follow. *(a) Ghost types.* A type address need not lie in `dom(Σ.C)`; an
endset whose coverage includes addresses with no stored content is a valid, matchable
type — "Link types may be ghost elements" (4/45). *(b) Independent constraint.* Because
the type participates in `sat` on equal footing with from and to, a request may constrain
type alone — `findlinks((∗, ∗, ∗, Θ), Σ)` returns every addressable link of a kind
touching `Θ`, leaving from and to open. *(c) Hierarchy by containment.* A type request
whose span is rooted at a supertype address `p` covers the whole subtree `{t : p ≼ t}`
(PrefixSpanCoverage, ASN-0043), so a single type span matches all subtypes of `p`; the
type slot is searchable for super- and sub-types without any registry. Gregory's index
keys the type endset by its I-addresses under a dedicated type-subspace, matched by
address-overlap and never by stored value, and treats an empty type request as imposing
no type constraint (consultation Q14) — the address-matching and ghost-validity
properties are concrete there.

## Wildcards drop slots, they do not empty the result

A wildcard component is "no specification," and `lift(e, ∗) = true` makes it the
universal constraint — it drops out of the conjunction rather than contributing the empty
set.

**FL-WILD (wildcard semantics).** A wildcard slot imposes no constraint:
`findlinks` with a wildcard component returns exactly the links the *remaining*
constrained slots admit. In the limit `findlinks((∗, ∗, ∗, ∗), Σ) = addressable(Σ)` —
all currently addressable links — and a single constrained slot yields precisely the
links matching that slot alone. This is the formal reading of Nelson's "If the home-set
is the whole docuverse, all links between these two elements are returned" (4/63): an
unconstrained axis widens, never empties, the result.

We record a second implementation divergence here. Gregory's `intersectlinksets`, given
three empty (wildcard) slots, returns the empty set rather than the universal set — the
degenerate all-wildcard request yields nothing in the current back end (consultation
Q15). The abstract semantics, and Nelson's intent, require the universal answer. An
alternative implementation must treat the fully-unconstrained request as returning all
addressable links to meet FL-WILD.

## The result is a current snapshot

What relationship must the result bear to the link store *as it stands at the moment of
inquiry*? Exactly that of the faithful, exhaustive satisfying subset of the currently
addressable links — every addressable link meeting the four criteria, and only those.
This is the conjunction of FL-SND and FL-CMP read against `addressable(Σ)` at the inquiry
state `Σ`. Current additions are included (a newly created matching link enters the
answer); current withdrawals are excluded (a retracted link leaves it); the surrounding
mass of non-matching links is irrelevant (FL-JUNK).

Two stability facts about the snapshot follow from immutability. First, a link's match
status is *permanent once created*, modulo retraction: `Σ.L(a)` is fixed by L12 and
`home(a)` is fixed by the address, so `sat(a, q, ·)` is constant for a fixed `q` across
the link's life. Second, retraction is the *only* way for an addressable matching link to
leave the answer.

**FL-MON (monotone accumulation absent retraction).** For any reachable `Σ →* Σ'` with
`a ∉ retracted(Σ')`: if `a ∈ findlinks(q, Σ)` then `a ∈ findlinks(q, Σ')`. A matching
link, once found and not withdrawn, stays found as the store grows. (By immutability
`sat(a, q, Σ') = sat(a, q, Σ)`, and `a ∈ addressable(Σ')` since it is unretracted.)

## Stability under content editing

If linked content is later edited, what of the result must remain stable? Xanadu links
attach to bytes — to I-addresses (content identity) — not to V-positions:

> "links can survive editing. If any of the bytes are left to which a link is attached,
> that link remains on them." (4/42)

Editing operations rewrite arrangements `Σ.M`; they do not touch the link store `Σ.L`
(immutable, L12) nor the content store `Σ.C` (append-only, S0), and they do not alter the
I-addresses an endset references. When the request is phrased over I-addresses — the
content-identity regime — `sat` depends only on `Σ.L`, on link addresses, and on the
fixed `q`. None of these moves under editing.

**FL-STB (stability under editing).** For a transition `Σ → Σ'` that preserves the link
store and the retraction set — `Σ'.L = Σ.L`, `retracted(Σ') = retracted(Σ)` — and an
I-address request `q`, `findlinks(q, Σ') = findlinks(q, Σ)`. Pure-arrangement edits
(insertion, deletion, rearrangement) and content appends, which preserve `Σ.L` and the
retraction set, leave the answer invariant. The membership of the result may be expressed
through different V-positions before and after the edit, but the *set of link
identities returned is unchanged*.

Nelson's one exception — a link drops from results when an *entire* endset's content is
deleted, "nothing left at one end" (4/42) — concerns a different phrasing of the request.
A *V-spec* request names its target through a document's current arrangement; if an
endpoint's content has been fully removed from every arrangement, no V-spec resolves to
its I-addresses, so a V-spec request cannot name it. Under the I-address regime the same
link is *orphaned* but still content-identity-findable: its endset I-addresses persist
(content is never destroyed, S0), and a direct I-address request still matches it
(consultation Q18 documents the surviving index entries; ASN-0098's LP17/LP18 give the
orphan/resurrection cycle). The abstract operation, specified over I-addresses, is stable;
the arrangement-mediated naming of the request is a separable front-end convenience whose
fragility under full deletion is a property of the *naming*, not of `findlinks`.

## Retraction is permanent absence from current inquiry

When a link is retracted, what must the system guarantee about its absence from
subsequent answers to the same four-set inquiry? Complete and consistent absence from the
current line of descent.

**FL-RET (retraction absence).** If `a ∈ retracted(Σ)`, then for every reachable
`Σ →* Σ'` and every request `q`, `a ∉ findlinks(q, Σ')`. The exclusion is total: even if
`a`'s endsets would still satisfy every endpoint criterion, `a ∉ addressable(Σ')` removes
it from FL-DEF, and the monotonicity of `retracted` keeps it out forever. A retracted
link neither lingers as a phantom result nor obstructs retrieval of the links that still
satisfy the inquiry (FL-JUNK applies to its absence as to any non-match).

The guarantee is *scoped* to current addressability, as Nelson's "not currently
addressable" (4/9) demands and no more. A retracted link is removed from current
inquiry but not destroyed — it may remain in other versions that captured it before
retraction, and a time-qualified or version-qualified inquiry into a prior state could
still surface it. Those scopes are out of the present operation, which inquires against
the current state. We mark the version-scoped behaviour as an open question rather than a
claim.

## Cross-document reach

Must the discovery reach across all documents whose arrangements could surface the same
links? It must, and the structure of FL-DEF makes the reach automatic rather than
something to be iterated for. Under the I-address regime, `findlinks(q, Σ)` is a function
of `Σ.L`, the retraction set, and `q` *alone* — the arrangements `Σ.M` do not appear in
it. The search is therefore intrinsically a global content-identity sieve over the link
store, not a per-document enumeration.

**FL-REACH (cross-document reach).** For an I-address request `q`, `findlinks(q, Σ)` is
independent of `Σ.M`. Four consequences follow. *(a) Every home is reached.* The store is
searched whole; a link is eligible regardless of which document homes it, so in-links —
stored in documents other than the one being read — are found on equal footing with
out-links. *(b) Transclusion is found once.* When the same endpoint content is shared
across documents, the link is indexed by that content's I-addresses and is found exactly
once by content identity, however many documents surface it (consultation Q20). *(c)
Whole-docuverse residence.* Setting `H = ∗` imposes no residence bound, returning all
matching links wherever homed — Nelson's "if the home-set is the whole docuverse, all
links … are returned" (4/63). *(d) Superset of the per-document discoverable union.* If
some document `d` surfaces a matching endpoint — `coverage(eᵢ) ∩ coverage(Rᵢ) ∩ ran(Σ.M(d)) ≠ ∅`
— then `a` is discoverable from `d` (ASN-0098's `discoverable_from`) and `a ∈ findlinks(q, Σ)`;
but `findlinks` also returns links that *no* document surfaces (orphans). The operation
is therefore at least as complete as any document-by-document enumeration, and strictly
more so in the presence of orphaned links. No qualifying link is missed for want of a
document to look in.

This is precisely the reach that a docuverse-wide guarantee requires: because a link's
in-links, its home, the transclusions of its endpoints, and the versions of its
connected content all place the relevant link *outside* whatever document one happens to
be reading, a complete discovery must — and FL-REACH does — range over the entire link
store rather than the local arrangement.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| FL-DEF | `findlinks(q, Σ) = { a ∈ addressable(Σ) : sat(a, q, Σ) }`, with `sat` the conjunction of the four lifted slot-criteria (AND of the ORs); `addressable(Σ) = dom(Σ.L) \ retracted(Σ)`, `retracted` monotone non-decreasing; the operation has frame `Σ` (reads only, writes nothing) | introduced |
| FL-SND | Soundness — `a ∈ findlinks(q, Σ) ⟹ sat(a, q, Σ)`; a link with any constrained slot wholly disjoint from the request is excluded; no false positives | introduced |
| FL-CMP | Completeness — every `a ∈ addressable(Σ)` with `sat(a, q, Σ)` is returned; the result is exactly the satisfying subset; no silent omission | introduced |
| FL-JUNK | Non-impedance — the result is invariant under addition of non-matching links and unaffected by their quantity; match status is decided per link | introduced |
| FL-RES | Residence–endpoint independence — the home criterion is a function of the link address alone, the endpoint criteria of the link value alone; the four slots are orthogonal constraints | introduced |
| FL-DIR | Positional directionality — `F` matches `e₁` only and `G` matches `e₂` only; reversing the from/to constraints can change the result, keeping "from X" and "to X" distinct queries | introduced |
| FL-TYP | Type by address — the type criterion tests `coverage(e₃)` by address overlap, never reads stored content; ghost types are matchable, type may be constrained alone, and prefix-rooted type spans match subtype subtrees | introduced |
| FL-WILD | Wildcard semantics — a wildcard slot drops from the conjunction (universal), not empties it; all-wildcard returns all addressable links | introduced |
| FL-CUR | Currency — the result is the faithful, exhaustive satisfying subset of `addressable(Σ)` at the inquiry state: current additions in, current retractions out, non-matches irrelevant | introduced |
| FL-MON | Monotone accumulation absent retraction — an unretracted matching link, once found, stays found as the store grows | introduced |
| FL-STB | Stability under editing — for I-address requests, the result is invariant under any transition preserving `Σ.L` and the retraction set; pure-arrangement edits and content appends do not change which links are returned | introduced |
| FL-RET | Retraction absence — a retracted link is permanently and completely absent from every subsequent current-state inquiry, and its absence does not impede other results | introduced |
| FL-REACH | Cross-document reach — for I-address requests `findlinks` is independent of `Σ.M`: global over the store, finds transcluded content once, returns all links under a whole-docuverse home-set, and is a superset of the per-document discoverable union (including orphans) | introduced |

## Open Questions

What must a version-qualified or time-qualified link inquiry guarantee, so that a link retracted in the current state remains discoverable in the prior states or versions that captured it before retraction?

What invariant must connect an I-address request to its arrangement-mediated (V-spec) phrasing, so that the two regimes agree exactly except on endpoints whose content has been fully removed from every arrangement?

Under what conditions on the home-set's coverage is the residence criterion equivalent to a single subtree-prefix test, so that residence bounding reduces to one containment check rather than a span-set membership?

What must hold of the type endset's coverage for the subtype-by-containment reading to be exact, neither admitting addresses outside the intended supertype subtree nor omitting intended subtypes?

What completeness guarantee must hold across a federation of independently administered stores, so that a single four-set inquiry reaches links homed in stores other than the one receiving the request?
