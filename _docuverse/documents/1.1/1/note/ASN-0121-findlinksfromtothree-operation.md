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

We write the system state as ASN-0047's five-tuple `Σ = (Σ.C, Σ.L, Σ.E, Σ.M, Σ.R)` —
the content store, the link store, the entity set, the family of document arrangements,
and the provenance relation. This is the state the transition vocabulary `→` (below)
operates on, so the monotonicity arguments that underwrite the permanence claims have
the same state object to range over as the operations they reason about. The query
itself is far narrower: `findlinks(q, Σ)` reads only the *link-store projection* `Σ.L`
(values and addresses) — the retraction relation it consults is itself a sub-part of
`Σ.L` (below). The remaining components `Σ.C`, `Σ.E`, `Σ.M`, `Σ.R` enter only the
surrounding transition vocabulary, never the query; FL-DEF's frame records this
explicitly. We use `coverage(e)` (ASN-0043) for the set of I-addresses an endset
references, `home(a)` (ASN-0043) for the document-level prefix at which a link address
`a` resides, and the total order and span machinery of ASN-0034 throughout.

## What is being matched

A link `a ∈ dom(Σ.L)` carries a value `Σ.L(a) = (e₁, e₂, …)` of at least three endsets
(L3). The first three slots are, by convention, the *from-endset* `e₁`, the *to-endset*
`e₂`, and the *type-endset* `e₃`. L3 permits arity `N ≥ 3`, so a link may carry further
endsets `e₄, …, eₙ` beyond the third — the n-set form Nelson calls for (4/79). This
operation — FINDLINKS*FROMTOTHREE* — constrains exactly the first three slots: the
satisfaction rule `sat` (below) tests `e₁, e₂, e₃` and leaves any higher slots
`e₄ … eₙ` unconstrained. A higher-arity link is therefore matched on its first three
endsets alone and remains in the result space; the name fixes the three matched slots,
and the determinacy of the result is unaffected by whatever further endsets a link may
carry. This is the intended semantics for the operation. Each endset references a set of I-addresses, its
coverage. The link also resides somewhere: `home(a)` is a document-level tumbler,
extracted from the *address* `a` by field projection, **not** from the endsets. These
two facts — what a link *connects* (its endset coverages) and where it *lives* (its
home) — are the raw material the request will constrain.

A request is a four-tuple

  `q = (H, F, G, Θ) ∈ (Endset ∪ {∗})⁴`,

where each component is either an *endset* (ASN-0043's `Endset = 𝒫_fin(Span)`) or the
distinguished *wildcard* `∗` (Nelson's NOSPECS — "no specification"). This is the full
well-formedness condition on a request: there is no further typing constraint on any
component. In particular, the home-component `H` is an *arbitrary* endset (or `∗`) — the
grammar does not confine it to any address level, and `athome` (below) is well-defined as
plain coverage membership for whatever endset `H` is. By *convention*, a home request is
phrased on the *organizational-prefix* axis, its spans rooted at node-, account-, or
document-level addresses; but this rooting is intended usage, not a well-formedness
condition the type enforces. (An element-rooted `H` is admissible regardless: `athome` is
well-defined as coverage membership for any endset, so there are no ill-formed inputs to
exclude and the operation is total over the declared request type. For a *unit-depth*
element-rooted span the match is simply vacuous — its coverage `{t : p ≼ t}` is the subtree
of an element-level `p` with `zeros(p) = 3`, which contains no document-level tumbler, so
`athome` is uniformly `false`. A *wide* element-rooted span carries no such guarantee: its
coverage is the order-convex range `{t : p ≤ t < p ⊕ ℓ}`, which may straddle a length
boundary and so contain a document-level tumbler — e.g. `p = [1,0,1,0,1,0,1,1]` with
`ℓ = [0,0,0,0,1,1,1,1]` (T12-well-formed) gives `p ⊕ ℓ = [1,0,1,0,2,1,1,1]`, and the
document tumbler `q = [1,0,1,0,2]` lies in `coverage((p, ℓ))`, so `athome(a, H)` can hold
for a link with `home(a) = q`. Totality does not depend on vacuity in either case.)
The *canonical* home span is the **unit-depth prefix span** `(p, δ(1, #p))`, whose
displacement is exactly the unit-depth `δ(1, #p)` that PrefixSpanCoverage (ASN-0043)
requires; it denotes the full subtree `{t : p ≼ t}`, order-convex under T5 (ASN-0034).
A wider span `(p, ℓ)` rooted at the same `p` is equally admissible — `Endset = 𝒫_fin(Span)`
imposes no upper-displacement bound — and its coverage is then the order-convex *range*
`{t : p ≤ t < p ⊕ ℓ}` (T12, ASN-0034), a proper sub-range of the subtree, not `{t : p ≼ t}`.
The PrefixSpanCoverage citation discharges the subtree reading *only* for the unit-depth
case; for a wider `H`, `athome` still bounds residence, now to an order-convex sub-range
rather than a whole subtree. The traces below, and the canonical residence-bounding uses
(node/account/document granularity), exercise only unit-depth spans, where the subtree
reading holds. The three endset-components `F, G, Θ` are, by the same convention, phrased on
the *element-level I-address* axis. (Note `home(a)` itself is always document-level — the
field projection `N(a).0.U(a).0.D(a)` — while the *request component* `H` is not so
confined: a node- or account-rooted span tests `home(a)`'s membership in the broader
subtree it denotes, the residence bounding exercised at node granularity in Trace 6.)
Every request the grammar admits is thus phrased entirely over addresses —
all of its components denote sets of tumbler addresses — and we call it an *I-address
request*. There is exactly one kind of request in this grammar; the arrangement-mediated
*V-spec* phrasing discussed later (under editing stability) is a separable front-end
convenience that resolves to addresses before reaching `findlinks` (ASN-0127's two-phase
combinator `findlinks_V`, F-V), not a second kind of request. So the qualifier
"I-address request," wherever it appears below, is simply every
`q` the grammar admits. We phrase request components as endsets precisely so that `coverage`
(ASN-0043), which is defined on `Endset`, applies to them uniformly with the link's own
endsets; an endset denotes, through `coverage`, a set of addresses, and the wildcard
denotes "no constraint." (An endset and an ASN-0053 span-set built from the same spans
have equal address sets — `coverage(e) = ⟦Σ⟧` when `e`'s elements are exactly the
components of the sequence `Σ` — so casting the request in the unordered endset form
loses nothing: the matching rule below depends only on the address set a component
covers, never on span order.)

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
*inside* a slot — "from all or any part of" the requested set.

`touch` must be *decidable* for `findlinks` to be a realisable query and not merely a
mathematically defined set, and it is — by exactly the argument that discharged the
analogous concern in the foundation (ASN-0086 CoverageEqualityDecidable).

**FL-DEC (decidability).** For any two endsets `e, r ∈ Endset`, `touch(e, r)` is
decidable using only T2 comparisons and TumblerAdd; consequently `sat(a, q, Σ)` is
decidable per link, and `findlinks(q, Σ)` is a finite, computable set. *Proof.* By
`Endset = 𝒫_fin(Span)` (ASN-0043), `coverage(e)` and `coverage(r)` are finite unions of
half-open T1-intervals `[s, s ⊕ ℓ)` (T12, ASN-0034). Run the cell-decomposition procedure
of ASN-0086's CoverageEqualityDecidable on `e ∪ r`: each coverage is constant on every
cell between consecutive sorted span endpoints, so `coverage(e) ∩ coverage(r) ≠ ∅` iff
the representative of some nonempty cell lies in both — the same finitely many T2 tests,
run for intersection-nonemptiness rather than coverage equality. The home test
`athome(a, H) ≡ home(a) ∈ coverage(H)` is a single point against a finite interval union
— the T2 span-membership test of ASN-0086's ActiveSubset. Hence `sat` — a conjunction of
four decidable tests — is decidable. The *addressability filter* over which FL-DEF ranges
is computable by exactly ASN-0086's ActiveSubset argument: the retraction relation
`L_R^Σ` is selected from the finite `dom(Σ.L)` by CoverageEqualityDecidable (the slot-3
type-coverage test against the retraction coverage class), and `nullified(Σ)` is decided
by T2 span-membership against the finitely many retraction to-coverages, so
`addressable(Σ) = dom(Σ.L) \ nullified(Σ)` is enumerable. With both the filter and `sat`
decidable, and `findlinks(q, Σ) ⊆ dom(Σ.L)` finite by L-fin (`|dom(Σ.L)| < ∞`, ASN-0093),
the result is computed by deciding `sat` over the finitely many addressable links. ∎

The corresponding residence test, for a link `a` and a home-set `H`, asks only that the
link's residence fall in the requested region:

  `athome(a, H) ≡ home(a) ∈ coverage(H)`.

Because a *unit-depth* prefix-rooted home span `(p, δ(1, #p))` denotes the subtree
`{t : p ≼ t}` (PrefixSpanCoverage, ASN-0043 — whose precondition is exactly this
unit-depth displacement) — order-convex/contiguous under T1 (T5, ASN-0034) — `H` may bound
residence at the granularity of a node, an account, or a single document, and `athome`
tests membership of `home(a)` against that subtree. A wider home span bounds residence to
an order-convex *sub-range* of a subtree (T12, ASN-0034) rather than the whole of it;
`athome` is defined uniformly as coverage membership in either case, so nothing below
depends on `H` being unit-depth — only the subtree *reading* of the residence bound does.

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
Nelson's retracted links are "not currently addressable" (4/9). The foundation already
supplies exactly this notion, so we use it rather than reinventing it: ASN-0086 defines

  `nullified(Σ) = { a ∈ dom(Σ.L) : (E (b, F', G') ∈ L_R^Σ :: a ∈ coverage(G')) }`

— the link addresses targeted by a retraction tuple in the retraction relation `L_R^Σ` —
and *proves* it monotone non-decreasing along every transition (R6a, RetractionStability:
`a ∈ nullified(Σ) ⟹ a ∈ nullified(Σ')`). We do not posit a fresh retraction set nor
assume its monotonicity; we inherit `nullified` and its R6a guarantee. (The *mechanism* of
retraction is ASN-0086's concern; here we need only its effect on addressability.) The
currently addressable links are

  `addressable(Σ) = dom(Σ.L) \ nullified(Σ)`.

Several claims below quantify over transitions `Σ → Σ'` and over reachable `Σ →* Σ'`, so
we must say what relation `→` ranges over. We take `→` to be the full atomic transition
vocabulary of ASN-0047: the allocation operations K.α (content) and K.λ (link), document
and entity registration K.δ, the arrangement-editing family K.μ⁺, K.μ⁺_L, K.μ⁻ and the
named composite K.μ~ (extension, contraction, reordering), and provenance recording K.ρ;
`Σ →* Σ'` is the reflexive-transitive (reachability) closure of `→`. Two monotonicity
facts about this *whole* vocabulary underwrite the permanence claims, and we record them
once here. First, `dom(Σ.L)` is non-decreasing across `→`: every operation other than
K.λ preserves the link store outright — `dom(Σ'.L) = dom(Σ.L)` with per-link value
equality (F-PRES, PublishedFramePreservation, ASN-0127, covering K.α, K.δ, K.μ⁺, K.μ⁺_L,
K.μ⁻, K.ρ and the composite K.μ~) — and K.λ only extends it (L12a); ASN-0098's
StoreMonotonicity★ lifts this to `dom(Σ.L) ⊆ dom(Σ'.L)` across `→*`. Second, `nullified`
is non-decreasing across `→`. The argument is structural: `nullified(Σ)` is a function of
`Σ.L` *alone* — it is defined through the retraction relation `L_R^Σ`, which is itself a
subset of the link store — so every F-PRES step, holding `Σ'.L = Σ.L`, leaves both
`L_R^Σ` and `nullified(Σ)` unchanged. Across the one link-store-changing operation K.λ,
R6a (ASN-0086, RetractionStability:
`a ∈ nullified(Σ) ⟹ a ∈ nullified(Σ')`) supplies monotonicity. So `nullified` is constant
across every non-K.λ step (F-PRES) and monotone (R6a) across K.λ, hence non-decreasing
across all of `→` and, by induction, across `→*`. We invoke these two facts — link-store
monotonicity and `nullified` monotonicity over the full vocabulary — wherever permanence
is at issue below.

Now we may derive, rather than stipulate, the answer set. Demand of any candidate answer
`R` two things. *Soundness*: `(A a : a ∈ R : a ∈ addressable(Σ) ∧ sat(a, q, Σ))` —
nothing returned is withdrawn or fails a criterion. *Completeness*:
`(A a : a ∈ addressable(Σ) ∧ sat(a, q, Σ) : a ∈ R)` — nothing qualifying is omitted. The
addressability conjunct of soundness is essential and not implied by the matching rule:
retraction is *not* one of the four criteria, so a nullified link `a` with `sat(a, q, Σ)`
true still satisfies every criterion. Were soundness to demand only `sat(a, q, Σ)`, both
`R_min = { a ∈ addressable(Σ) : sat(a, q, Σ) }` and the larger
`R_max = { a ∈ dom(Σ.L) : sat(a, q, Σ) }` — which retains nullified-but-satisfying links —
would meet the two demands, and the answer would not be forced: the residual freedom is
exactly whether to return retracted-but-satisfying links, precisely the freedom Nelson's
"not currently addressable" (4/9) closes. The addressability conjunct removes that slack.
With it, the predicate soundness *permits* into `R` for any link is
`a ∈ addressable(Σ) ∧ sat(a, q, Σ)`; the predicate completeness *forces* into `R` is the
same. The two demands meet with no slack between them, leaving no design freedom:

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
none of them and retracts none — `dom(Σ.L) ⊆ dom(Σ'.L)`, `nullified(Σ') = nullified(Σ)`,
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
The asymmetry is observable, and we exhibit an explicit witness. Take two distinct
content I-addresses
`x = [1,0,1,0,1,0,1,5]` and `y = [1,0,1,0,1,0,1,9]` (both element-level, `zeros = 3`,
text subspace `s_C = 1`, differing only in the last component), and the unit-depth request
endsets `X = {(x, δ(1,#x))}` and `Y = {(y, δ(1,#y))}`. By PrefixSpanCoverage (ASN-0043),
`coverage(X) = {t : x ≼ t}` and `coverage(Y) = {t : y ≼ t}`; since `x` and `y` are
equal-length and distinct they are prefix-incomparable (Prefix, ASN-0034: a proper prefix
is strictly shorter), so these subtrees are disjoint (T10, PartitionIndependence,
ASN-0034) and `coverage(X) ∩ coverage(Y) = ∅`. Now let `a` be a link with from-endset
`e₁ = X` and
to-endset `e₂ = Y` (its type endset and home are immaterial here). Then
`coverage(e₁) ∩ coverage(X) ≠ ∅` (it contains `x`), `coverage(e₁) ∩ coverage(Y) = ∅`,
`coverage(e₂) ∩ coverage(Y) ≠ ∅` (contains `y`), and `coverage(e₂) ∩ coverage(X) = ∅`.
Checking both requests against FL-DEF: for `q = (∗, X, Y, ∗)`, `lift(e₁, X) = true` and
`lift(e₂, Y) = true`, so `sat(a, q, Σ)` holds and `a ∈ findlinks((∗, X, Y, ∗), Σ)`; for the
reversed `q' = (∗, Y, X, ∗)`, `lift(e₁, Y) ≡ touch(e₁, Y) = (coverage(X) ∩ coverage(Y) ≠ ∅)
= false`, so `sat(a, q', Σ)` fails and `a ∉ findlinks((∗, Y, X, ∗), Σ)`. Reversing the two
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
type (L9, TypeGhostPermission, ASN-0043) — "Link types may be ghost elements" (4/45).
*(b) Independent constraint.* Because
the type participates in `sat` on equal footing with from and to, a request may constrain
type alone — `findlinks((∗, ∗, ∗, Θ), Σ)` returns every addressable link of a kind
touching `Θ`, leaving from and to open. *(c) Hierarchy by containment.* A type request
whose span is rooted at a supertype address `p` covers the whole subtree `{t : p ≼ t}`
and so matches all and only subtypes of `p` — L10 (TypeHierarchyByContainment, ASN-0043,
via PrefixSpanCoverage) applied on the request side; the
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
unconstrained axis widens, never empties, the result. `addressable(Σ)` here ranges over
links of *every* arity `N ≥ 3`; a higher-arity link is admitted by the all-wildcard
request like any other, and under a constrained request is matched on its first three
endsets alone (its slots `e₄ … eₙ` never enter `sat`).

A wildcard must not be conflated with a *constrained* slot that happens to bound nothing.
The request grammar admits both: a slot may be left unspecified (`∗`, NOSPECS) or
specified with an endset of empty coverage (the empty endset `∅`, with `coverage(∅) = ∅`).
These are opposite elements of the conjunction.

**FL-EMP (empty constraint is the zero, not the unit).** For a constrained slot whose
endset has empty coverage, `lift(e, ∅) ≡ touch(e, ∅) ≡ coverage(e) ∩ ∅ ≠ ∅` is `false`
for every link `a` (and likewise `liftH(a, H) ≡ home(a) ∈ ∅` is `false` when `H` has empty
coverage). Hence if *any* constrained component of `q` has empty coverage,
`findlinks(q, Σ) = ∅` regardless of the store's contents. This is the polar opposite of the
wildcard: `∗` is the *unit* of the conjunction (`lift(e, ∗) = true`, drops out, admits
whatever the other slots admit), whereas the empty endset is the *zero*
(`lift(e, ∅) = false`, forces the whole conjunction to `false`). The distinction is
load-bearing: under the AND-of-ORs structure a unit slot widens the answer while a zero
slot annihilates it, so empty-spec and no-spec can never be identified. Gregory's back end
realises exactly this asymmetry — a NOSPECS slot is omitted from the intersection (the
slot is simply not consulted), whereas a constrained slot that resolves to no I-addresses
short-circuits the entire find to the empty link-set *before* `intersectlinksets` is even
reached (consultation Q7).

The `touch` test is symmetric in its two coverages, so the same zero behaviour appears
when the empty endset sits on the *link's* side rather than the request's. L3 constrains
only the type slot to be non-empty (`e₃ ≠ ∅`); a stored link may legitimately carry an
empty from- or to-endset (`e₁ = ∅` or `e₂ = ∅`). For such a link, against *any*
constrained from-request `F ≠ ∗`,

  `lift(∅, F) ≡ touch(∅, F) ≡ coverage(∅) ∩ coverage(F) = ∅ ∩ coverage(F) = ∅`,

so `lift(∅, F) = false` and the link is correctly excluded from every constrained
from-slot — *from nothing is not a from-match*. On that axis it is admitted only under
the from-wildcard `F = ∗`, where `lift(∅, ∗) = true` drops the slot from the conjunction
and the link is matched on its remaining (non-empty) slots alone. The to-side is identical
with `e₂` and the to-request `G`. Empty coverage on *either* side of `touch` — the request
component (FL-EMP above) or the link's own endset (here) — annihilates that slot's test;
the two are the same zero, and this is the intended "a link with no from-endpoint is
discoverable only as a to-match, never as a from-match" semantics.

We record a second implementation divergence here. Gregory's `intersectlinksets`, given
three empty (wildcard) slots, returns the empty set rather than the universal set — the
degenerate all-wildcard request yields nothing in the current back end (consultation
Q15). The abstract semantics, and Nelson's intent, require the universal answer. An
alternative implementation must treat the fully-unconstrained request as returning all
addressable links to meet FL-WILD. (Note this is the all-*wildcard* case; by FL-EMP an
all-*empty* request `((∅,∅,∅,∅))` correctly returns `∅` under both the abstract semantics
and the back end.)

## The result is a current snapshot

What relationship must the result bear to the link store *as it stands at the moment of
inquiry*? Exactly that of the faithful, exhaustive satisfying subset of the currently
addressable links — every addressable link meeting the four criteria, and only those.

**FL-CUR (currency).** Read at the inquiry state `Σ`,

  `a ∈ findlinks(q, Σ) ⟺ a ∈ addressable(Σ) ∧ sat(a, q, Σ)`.

The result is the faithful, exhaustive satisfying subset of the currently addressable
links. The biconditional is FL-DEF restated as a membership test, and we read off each
direction from it. *Forward* (`a ∈ findlinks(q, Σ) ⟹ a ∈ addressable(Σ) ∧ sat(a, q, Σ)`):
FL-DEF's set-builder `{ a ∈ addressable(Σ) : sat(a, q, Σ) }` supplies *both* conjuncts —
the restriction `a ∈ addressable(Σ)` from the index set and `sat(a, q, Σ)` from the
selector; FL-SND alone delivers only the `sat` conjunct, so the addressability half rests
on FL-DEF, not FL-SND. *Backward* (`a ∈ addressable(Σ) ∧ sat(a, q, Σ) ⟹ a ∈ findlinks(q, Σ)`):
this is FL-CMP, no satisfying addressable link omitted. The two directions compose into
the biconditional. Current additions are included (a newly created matching link enters the
answer); current withdrawals are excluded (a nullified link leaves it, R6a); the
surrounding mass of non-matching links is irrelevant (FL-JUNK).

Two stability facts about the snapshot follow from immutability. First, a link's match
status is *permanent once created*, modulo retraction: `Σ.L(a)` is fixed by L12 and
`home(a)` is fixed by the address, so `sat(a, q, ·)` is constant for a fixed `q` across
the link's life. Second, retraction is the *only* way for an addressable matching link to
leave the answer.

**FL-MON (monotone accumulation absent retraction).** For any reachable `Σ →* Σ'` with
`a ∉ nullified(Σ')`: if `a ∈ findlinks(q, Σ)` then `a ∈ findlinks(q, Σ')`. A matching
link, once found and not withdrawn, stays found as the store grows. (By LP13 (ASN-0098,
UnconditionalLinkPersistence) `Σ'.L(a) = Σ.L(a)` across the reachability closure `Σ →* Σ'`,
and `home(a)` is a projection of the fixed address `a`, so `sat(a, q, Σ') = sat(a, q, Σ)`;
and `a ∈ addressable(Σ')` because `a ∈ dom(Σ'.L)` by link-store monotonicity across
`Σ →* Σ'` (ASN-0098 StoreMonotonicity★) and `a ∉ nullified(Σ')` by hypothesis.)

### The only result-changing transition

FL-MON and FL-STB are monotonicity and invariance statements; they do not isolate *which*
single transition can move a link into or out of the answer. Since `findlinks(q, ·)` is a
function of `Σ.L` alone (FL-DEF's frame; the F-CIL instantiation recorded at FL-STB
below), and every operation in `→` other than K.λ preserves `Σ.L` (F-PRES, ASN-0127, as
recorded above), *K.λ is the unique result-changing transition*. (For the bare,
unfiltered existence query, ASN-0127's F-LAMBDA already characterises the K.λ step — the
result grows by exactly the fresh link when it matches; the cases below refine that
per-step increment through the four-slot `sat` and the addressability filter, neither of
which F-LAMBDA carries.) A single K.λ step can change the answer in three ways, and we
compute the weakest precondition of each:
the entry of a newly created *ordinary* link, the entry of a newly created *retraction*
link, and the survival of an existing match under a retraction-bearing K.λ. The second
case is not idle: a retraction link is a first-class link with its own address, and
Nelson's link model exempts no type from search — "there is essentially nothing in the
Xanadu system except documents and their arbitrary links" (4/41), and the search mechanism
"does not actually look at what is stored under the 'type' … it merely considers the
type's address" (4/44–4/45), so a type-`Θ` query touching the retraction class returns a
retraction link like any other. The operation is therefore obliged to surface a fresh
retraction link when it matches, and its entry has a weakest precondition we must
characterise — one that differs from the ordinary case precisely because the *same* K.λ
grows `L_R`, carrying a self-retraction term.

**FL-WP (weakest precondition for the result-changing step).**

*Scope of the wp — additional precondition given an enabled step.* Each case below opens
"Let `Σ → Σ'` be a K.λ step that allocates a fresh address …", which presupposes the step's
own applicability predicate `enabled(K.λ)` — K.λ's freshness `ℓ ∉ dom(Σ.L)`, its L3
well-formedness (`arity ≥ 3`, slot-3 type endset non-empty), and `home(ℓ) ∈ dom(Σ.M)` (ASN-0093
K.λ). The displayed conjunctions are therefore the weakest *additional* precondition under which
the named, enabled K.λ step lands `ℓ` (resp. `b`, `a`) in the answer; the full weakest
precondition is `enabled(K.λ) ∧ ⟨displayed conjunction⟩`. We carry `enabled(K.λ)` implicitly
rather than redisplay it in each case, matching ASN-0086's wp Case 2 (EmitKWeakestPrecondition),
which likewise carries the operation's applicability predicate (`enabled(K.μ⁻[d, R])`) as a wp
conjunct alongside the substantive pullback term.

*(a) Entry of a fresh ordinary link.* Let `Σ → Σ'` be a K.λ step that allocates a fresh
address `ℓ ∉ dom(Σ.L)` with value `Σ'.L(ℓ) = (F, G, Θ)` of arity `N ≥ 3`, homed at
`d = home(ℓ)`. We must cut the partition on *retraction-relation membership*, not on coverage
class alone, because ASN-0086's `L_R^Σ = {(a, F, G) : a ∈ dom(Σ.L) ∧ |Σ.L(a)| = 3 ∧ …}`
requires **arity exactly 3** in addition to the slot-3 coverage test. We therefore call the
link *ordinary (non-retraction)* exactly when it does not enter the retraction relation —
`ℓ ∉ L_R^{Σ'}` — which by ASN-0086's definition is `¬(|Σ'.L(ℓ)| = 3 ∧ coverage(Σ'.L(ℓ).e₃) = coverage(R))`,
where `R` is ASN-0086's designated retraction-type representative and the slot-3 test is the
foundation's coverage equality `coverage(Σ'.L(ℓ).e₃) = coverage(R)` (equivalently, `Σ'.L(ℓ).e₃ ∈ [R]`,
the endset lying in `R`'s `~`-class). This subsumes two sub-cases: the type endset does not match the
retraction coverage (`coverage(Θ) ≠ coverage(R)`, any arity), *or* the type endset
does match but the link's arity is not 3 (`coverage(Θ) = coverage(R)` with
`N > 3` — a higher-arity link FL-WILD keeps in scope, whose slot-3 coverage tests retraction
yet which never enters the triple-restricted `L_R`). In either sub-case `ℓ ∉ L_R^{Σ'}`, and
since `ℓ` is the only address `Σ.L` gains, no other tuple enters `L_R` either, so
`L_R^{Σ'} = L_R^Σ`. Then

  `wp(K.λ, ℓ ∈ findlinks(q, ·)) ≡ ℓ ∉ nullified(Σ') ∧ liftH_d(q.H) ∧ lift(F, q.F) ∧ lift(G, q.G) ∧ lift(Θ, q.Θ)`,

where `liftH_d(q.H) ≡ (q.H = ∗) ∨ (d ∈ coverage(q.H))`, and the addressability conjunct
unfolds, for an ordinary K.λ, as `ℓ ∉ nullified(Σ') ≡ ¬(E (b, F', G') ∈ L_R^Σ :: ℓ ∈ coverage(G'))`.
*Derivation.* By FL-DEF, `ℓ ∈ findlinks(q, Σ') ⟺ ℓ ∈ addressable(Σ') ∧ sat(ℓ, q, Σ')`. We treat
the two conjuncts in turn.

The addressability conjunct does *not* drop out by freshness alone, and we must carry it.
The ordinariness condition above — `ℓ ∉ L_R^{Σ'}` — is exactly what leaves
the retraction relation fixed: `ℓ` does not enter `L_R` (either its slot-3 coverage is not
the retraction class, or its arity exceeds 3), and `ℓ` is the only address `Σ.L` acquires,
so `L_R^{Σ'} = L_R^Σ`;
hence by ASN-0086's definition
`nullified(Σ') = { a ∈ dom(Σ'.L) : (E (b, F', G') ∈ L_R^Σ :: a ∈ coverage(G')) }`. Freshness
`ℓ ∉ dom(Σ.L)` guarantees only that *this* step emits no retraction targeting `ℓ`; it does
not exclude a *pre-existing* retraction tuple `(b, F', G') ∈ L_R^Σ` whose to-coverage already
names `ℓ`. Endset coverage may reference ghost addresses with no stored content (L4
EndsetGenerality and L9 TypeGhostPermission, ASN-0043; R5, ASN-0086; LP17/LP18
orphan/resurrection, ASN-0098), so the future address `ℓ` can be
uncovered while merely fresh against `dom(Σ.L)` yet covered once it enters `dom(Σ'.L)` — exactly
the regime in which `nullified(Σ)`, restricted to `dom(Σ.L)`, omits `ℓ` "before" allocation
while `nullified(Σ')` includes it "after." In that case `ℓ ∈ nullified(Σ')`, so
`ℓ ∉ addressable(Σ')` and `ℓ ∉ findlinks(q, Σ')` *even though* `sat(ℓ, q, Σ')` holds. The
addressability conjunct is therefore not vacuous, and the weakest precondition must retain it as
`ℓ ∉ nullified(Σ')`, equivalently `¬(E (b, F', G') ∈ L_R^Σ :: ℓ ∈ coverage(G'))`. This is the
direct analogue of the third conjunct ASN-0086 deliberately carries in its wp Case 2
(EmitKWeakestPrecondition), `¬(E (b, F', G') ∈ L_R^Σ :: a_emit(Σ, d) ∈ coverage(G'))`, and for
the same reason — the conjunct is dischargeable only under a stated retraction discipline:
ASN-0086's disciplined-domain simplification of wp Case 2 discharges it vacuously at
layer-reachable states (unit-depth retraction discipline plus R0a give
`a_emit(Σ, d) ∉ coverage(G')` for every pre-existing retraction tuple). This
ASN works over the *full* ASN-0047 transition vocabulary, which imposes no such discipline, so we
do not assert that discharge here; we keep the conjunct explicit.

The matching conjunct `sat(ℓ, q, Σ')` reads only the committed value `(F, G, Θ)` and the
committed address (via `home(ℓ) = d`) — both fixed by the operation's own arguments, with no
further pre-state dependence — so it equals the four-way conjunction
`liftH_d(q.H) ∧ lift(F, q.F) ∧ lift(G, q.G) ∧ lift(Θ, q.Θ)`. The wp is therefore the displayed
*five*-way conjunction: a fresh link enters the answer iff its just-committed value and home meet
all four lifted criteria of `q` *and* no standing retraction tuple already covers its address.

*(c) Entry of a fresh retraction link.* The ordinariness cut of case (a) sets aside
exactly one realisable K.λ result change: the entry of a fresh link that *itself* enters the
retraction relation. Because the link model exempts no type from search (consultation, Q2 — a
type-`Θ` query touching the retraction class returns such a link like any other), we compute
its weakest precondition rather than scope it out. Let `Σ → Σ'` be a K.λ step that allocates
a fresh address `b ∉ dom(Σ.L)` with value `Σ'.L(b) = (F_b, G', Θ_b)` of *arity exactly 3*
whose type endset matches the retraction coverage — `coverage(Θ_b) = coverage(R)` —
so by ASN-0086's slot-3 test (now applicable, the arity-3 conjunct met) `b ∈ L_R^{Σ'}`. This
is precisely the complement of case (a)'s `ℓ ∉ L_R^{Σ'}`, so (a) and (c) partition the
fresh-link space exhaustively. We do *not* assume the empty-from RetractionDirectionality
convention: this ASN works over the full ASN-0047 vocabulary, which admits attribution-bearing
retractions whose from-slot `F_b` may be non-empty (ASN-0086's convention reserves the from-set
for "attribution-bearing endset content *or* … empty for unattributed retractions"). By
ASN-0086's `nullified`, only the to-coverage `coverage(G')` of a retraction tuple bears on
nullification, so the targets are read from `G'` regardless of `F_b`. The retraction relation
grows by exactly this one tuple: `L_R^{Σ'} = L_R^Σ ∪ {(b, F_b, G')}` — every prior tuple
persists by L12, and `b` is the only address `Σ.L` gains. Then

  `wp(K.λ, b ∈ findlinks(q, ·)) ≡ ¬(E (c, F'', G'') ∈ L_R^Σ :: b ∈ coverage(G'')) ∧ b ∉ coverage(G') ∧ liftH_d(q.H) ∧ lift(F_b, q.F) ∧ lift(G', q.G) ∧ lift(Θ_b, q.Θ)`,

with `d = home(b)`. *Derivation.* By FL-DEF,
`b ∈ findlinks(q, Σ') ⟺ b ∈ addressable(Σ') ∧ sat(b, q, Σ')`. The matching conjunct reads
the committed value `(F_b, G', Θ_b)` and home `d` — both fixed by the operation's own
arguments — so `sat(b, q, Σ') = liftH_d(q.H) ∧ lift(F_b, q.F) ∧ lift(G', q.G) ∧ lift(Θ_b, q.Θ)`.
(In the unattributed sub-case `F_b = ∅`, FL-EMP gives `lift(∅, q.F) = false` under any
*constrained* `q.F` and `true` only under the from-wildcard, so an empty-from retraction link
is from-discoverable only when `q.F = ∗`; a non-empty `F_b` is tested exactly like any other
from-endset.) The addressability conjunct unfolds over the *extended* retraction relation: for
the fresh `b`,
`b ∈ nullified(Σ') ⟺ (E (c, F'', G'') ∈ L_R^{Σ'} :: b ∈ coverage(G''))
⟺ (E (c, F'', G'') ∈ L_R^Σ :: b ∈ coverage(G'')) ∨ b ∈ coverage(G')`, splitting the
existential over the disjoint union `L_R^Σ ∪ {(b, F_b, G')}`. The first disjunct is the
case-(a) hazard — a *pre-existing* retraction tuple already covering the ghost-allocated `b`;
the second is the *self-retraction* term `b ∈ coverage(G')`, in which the very tuple just
committed names its own address (a self-nullifying retraction). Negating,
`b ∉ nullified(Σ') ≡ ¬(E (c, F'', G'') ∈ L_R^Σ :: b ∈ coverage(G'')) ∧ b ∉ coverage(G')`.
This is precisely case (a)'s addressability conjunct with the self-retraction term
`b ∉ coverage(G')` adjoined — the term case (b) sets aside by scope, here *live* because `b`
is the fresh retractor's own address. Conjoining matching and addressability gives the
displayed *six*-way wp: a fresh retraction link enters the answer iff its committed value and
home meet all four lifted criteria of `q`, no standing retraction tuple already covered its
address, *and* it does not retract itself.

*(b) Survival of an existing match under retraction.* Let `Σ → Σ'` be a K.λ step that
commits a *retraction tuple* whose to-coverage is `coverage(G')` — by ASN-0086 this grows
`nullified` by exactly the targets in `coverage(G')` (R6b), leaving every link value and
home untouched (L12). For an existing link `a ∈ dom(Σ.L)`,

  `wp(K.λ_retract, a ∈ findlinks(q, ·)) ≡ a ∈ findlinks(q, Σ) ∧ a ∉ coverage(G')`.

*Derivation.* `sat(a, q, ·)` is constant across the step (`Σ'.L(a) = Σ.L(a)` by L12,
`home(a)` fixed), so by FL-DEF `a ∈ findlinks(q, Σ') ⟺ a ∈ addressable(Σ') ∧ sat(a, q, Σ)`.
We need the *exact* membership equation for `nullified(Σ')` on existing addresses, both
directions — the ⊆ direction is what makes this the *weakest* precondition, licensing
`a ∉ nullified(Σ')` from `a ∉ nullified(Σ) ∧ a ∉ coverage(G')`, and R6b supplies only ⊇.
The retraction-bearing K.λ commits exactly the one tuple `(b, F_b, G')` (we write its
from-slot `∅` below as a placeholder, since `nullified` reads only the to-coverage `G'` and the
from-slot — empty or attribution-bearing — is immaterial to this case), and by L12
(immutability) every prior tuple persists unchanged, so the retraction relation grows by
exactly that tuple: `L_R^{Σ'} = L_R^Σ ∪ {(b, ∅, G')}`. Unfolding ASN-0086's definition of
`nullified` at `Σ'` over this relation, for an existing `a ∈ dom(Σ.L)`:
`a ∈ nullified(Σ') ⟺ (E (c, F'', G'') ∈ L_R^{Σ'} :: a ∈ coverage(G''))
⟺ (E (c, F'', G'') ∈ L_R^Σ :: a ∈ coverage(G'')) ∨ a ∈ coverage(G')
⟺ a ∈ nullified(Σ) ∨ a ∈ coverage(G')`,
where the middle step splits the existential over the disjoint union `L_R^Σ ∪ {(b, ∅, G')}`.
This equation is stated and used only on the existing-link slice `a ∈ dom(Σ.L)`; the fresh
retractor address `b ∈ dom(Σ'.L) \ dom(Σ.L)` lies outside that slice, so the *self-retraction*
case `b ∈ coverage(G')` — in which `b` nullifies its own address — is excluded by scope and does
not bear on the conclusion drawn for existing links (its weakest precondition is the subject of
case (c) above, where it appears as the live self-retraction conjunct `b ∉ coverage(G')`). (On
the existing-link slice `dom(Σ.L)` — all this case uses — the increment is exactly
`nullified(Σ') ∩ dom(Σ.L) = (nullified(Σ) ∪ coverage(G')) ∩ dom(Σ.L)`, which the
singleton-extension premise `L_R^{Σ'} = L_R^Σ ∪ {(b, ∅, G')}` discharges alongside R6b. We do
*not* assert the corresponding equation over the full post-state index `dom(Σ'.L)`: the naive
`nullified(Σ) ∪ {t ∈ dom(Σ'.L) : t ∈ coverage(G')}` would omit the fresh retractor `b` whenever
`b ∉ coverage(G')` yet `b` is covered by a *pre-existing* tuple `(c, F'', G'') ∈ L_R^Σ` with
`b ∈ coverage(G'')` — the ghost-pre-coverage hazard of case (a) — so over the full index the
newly-nullified set is `(coverage(G') ∩ dom(Σ.L) \ nullified(Σ))` plus the fresh `b` nullified by
*either* `G'` *or* a pre-existing tuple, and the "exact" simplification fails. Case (b) needs only
the `dom(Σ.L)` slice, where the fresh-`b` terms do not arise.)
R6b discharges only the ⟸ (⊇) half — that hitting `coverage(G')` forces nullification — while
the displayed split supplies the ⟹ (⊆) half from the singleton extension of `L_R`. Negating,
`a ∈ addressable(Σ') ⟺ a ∉ nullified(Σ) ∧ a ∉ coverage(G')`. Conjoining with `sat` and
folding `a ∉ nullified(Σ) ∧ sat(a, q, Σ)` back into `a ∈ findlinks(q, Σ)` gives the stated
wp: a found link survives a retraction step exactly when the retraction's to-coverage does
not name it. Setting `a ∉ coverage(G')` to hold for all `a` already in the answer recovers
FL-MON's no-retraction hypothesis; its failure is the sole route by which a match leaves
the answer, which is FL-RET.

## Stability under content editing

If linked content is later edited, what of the result must remain stable? Xanadu links
attach to bytes — to I-addresses (content identity) — not to V-positions:

> "links can survive editing. If any of the bytes are left to which a link is attached,
> that link remains on them." (4/42)

Editing operations rewrite arrangements `Σ.M`; they do not touch the link store `Σ.L`
(F-PRES, ASN-0127; values immutable, L12) nor the content store `Σ.C` (append-only, S0),
and they do not alter the I-addresses an endset references. Because every request is phrased over I-addresses (the
content-identity regime — there is no other kind in the grammar), `sat` depends only on
`Σ.L`, on link addresses, and on the fixed `q`. None of these moves under editing.

**FL-STB (stability under editing).** For a transition `Σ → Σ'` that preserves the link
store — `Σ'.L = Σ.L` — and any
request `q` (necessarily an I-address request, the grammar's only kind),
`findlinks(q, Σ') = findlinks(q, Σ)`. This is an instance of ASN-0127's meta-lemma F-CIL
(ComprehensionInvariantUnderΣL): FL-DEF is the comprehension
`{ a ∈ dom(Σ.L) : a ∉ nullified(Σ) ∧ sat(a, q, Σ) }`, and its membership predicate
consults only `Σ.L` and query-data — `sat` reads the stored value `Σ.L(a)`, the
address-projection `home(a)`, and the fixed `q`; `nullified` is defined through the
retraction relation `L_R^Σ ⊆ Σ.L` — never `Σ.M`, `Σ.C`, `Σ.E`, or `Σ.R`. F-CIL therefore
delivers the equality from the single hypothesis `Σ'.L = Σ.L`; in particular
retraction-set preservation (`nullified(Σ') = nullified(Σ)`) is a consequence of the
link-store hypothesis, not an independent assumption. Pure-arrangement edits (insertion,
deletion, rearrangement) and content appends preserve `Σ.L` (F-PRES, ASN-0127) and so
leave the answer invariant. The membership of the result may be expressed
through different V-positions before and after the edit, but the *set of link
identities returned is unchanged*.

Nelson's one exception — a link drops from results when an *entire* endset's content is
deleted, "nothing left at one end" (4/42) — concerns a different phrasing of the request.
A *V-spec* request names its target through a document's current arrangement; ASN-0127
formalises exactly this front-end as the two-phase combinator `findlinks_V` (F-V,
TwoPhaseFactoring): a V-region `W` is first resolved through the arrangement to the
I-address set `image(W, d, Σ)`, and only then does a link query run. The fragility is
then a theorem rather than an observation: `findlinks_V` is non-monotone across
arrangement edits — extension grows it, contraction shrinks it, reordering can move it
(D-NONMONO, ASN-0127) — and it can change while `dom(Σ.L)` is fixed (D-PRES, ASN-0127).
In particular, if an endpoint's content has been fully removed from every arrangement,
no V-spec resolves to
its I-addresses, so a V-spec request cannot name it. Under the I-address regime the same
link is *orphaned* but still content-identity-findable: its endset I-addresses persist
(content is never destroyed, S0), and a direct I-address request still matches it
(consultation Q18 documents the surviving index entries; ASN-0098's LP17/LP18 give the
orphan/resurrection cycle). The abstract operation, specified over I-addresses, is stable
(FL-STB); the arrangement-mediated naming of the request is a separable front-end
convenience whose fragility under full deletion is a property of the *resolution* (F-V's
first phase), not of `findlinks`.

## Retraction is permanent absence from current inquiry

When a link is retracted, what must the system guarantee about its absence from
subsequent answers to the same four-set inquiry? Complete and consistent absence from the
current line of descent.

**FL-RET (retraction absence).** If `a ∈ nullified(Σ)`, then for every reachable
`Σ →* Σ'` and every request `q`, `a ∉ findlinks(q, Σ')`. The exclusion is total: even if
`a`'s endsets would still satisfy every endpoint criterion, `a ∉ addressable(Σ')` removes
it from FL-DEF, and the non-decrease of `nullified` across the full transition vocabulary
— R6a (ASN-0086) across the one link-store-changing operation K.λ, and constancy of
`nullified` across every other operation in `→` (all of which leave `Σ.L`, hence `L_R^Σ`,
untouched), as established for `→` and `→*` above — keeps it out forever. A retracted
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
of `Σ.L`, `nullified(Σ)`, and `q` *alone* — the arrangements `Σ.M` do not appear in
it. The search is therefore intrinsically a global content-identity sieve over the link
store, not a per-document enumeration.

**FL-REACH (cross-document reach).** For any request `q` (an I-address request, the
grammar's only kind), `findlinks(q, Σ)` is independent of `Σ.M`. Four consequences
follow. *(a) Every home is reached.* The store is
searched whole; a link is eligible regardless of which document homes it, so in-links —
stored in documents other than the one being read — are found on equal footing with
out-links. *(b) Transclusion is found once.* When the same endpoint content is shared
across documents, the link is indexed by that content's I-addresses and is found exactly
once by content identity, however many documents surface it (consultation Q20). *(c)
Whole-docuverse residence.* Setting `H = ∗` imposes no residence bound, returning all
matching links wherever homed — Nelson's "if the home-set is the whole docuverse, all
links … are returned" (4/63). *(d) Superset of the satisfying discoverable links.* It is tempting to say the reach
"subsumes" ASN-0098's per-document `discoverable_from`, but that comparison must be drawn
carefully, because `discoverable_from` is *request-independent* while `findlinks` is not.
By LP12 (ASN-0098), `discoverable_from(a, d, Σ)` holds iff *some* slot's coverage meets
`ran(Σ.M(d))` — with no reference to `q`. Hence the bare per-document union
`⋃_d { a : discoverable_from(a, d, Σ) }` is the set of *all* non-orphan links, irrespective
of the request, and for a restrictive `q` it can dwarf `findlinks(q, Σ)` — take
`q = (∗, ∅, ∗, ∗)`, a constrained empty from-slot, where FL-EMP forces
`findlinks(q, Σ) = ∅` while the discoverable union may be large. So `findlinks(q, Σ)` is
*not* in general a superset of the bare discoverable union; the headed claim must be
restricted to the *satisfying* links. Membership in the result is governed by FL-DEF, the
full conjunction `a ∈ findlinks(q, Σ) ⟺ a ∈ addressable(Σ) ∧ sat(a, q, Σ)` — the AND of
all four lifted criteria, not any single surfaced slot. The true containment is

  `findlinks(q, Σ) ⊇ ⋃_d { a : a ∈ addressable(Σ) ∧ sat(a, q, Σ) ∧ discoverable_from(a, d, Σ) }`:

every satisfying, addressable link that some document `d` surfaces is in the result. The
inclusion is *strict* whenever a satisfying, addressable *orphan* exists — an addressable
`a` with `sat(a, q, Σ)` whose endset I-addresses lie in no arrangement range, so
`discoverable_from(a, d, Σ)` fails for every `d` yet `a ∈ findlinks(q, Σ)`. The operation
is therefore at least as complete as any document-by-document enumeration of the
*satisfying* links, and strictly more so in the presence of satisfying orphans. No
qualifying link is missed for want of a document to look in.

This is precisely the reach that a docuverse-wide guarantee requires: because a link's
in-links, its home, the transclusions of its endpoints, and the versions of its
connected content all place the relevant link *outside* whatever document one happens to
be reading, a complete discovery must — and FL-REACH does — range over the entire link
store rather than the local arrangement.

## A worked instance

We verify the principal claims against one concrete store. Fix a document
`d = [1,0,1,0,1]` (`zeros(d) = 2`, document-level). Under `d` sit three text I-addresses
in subspace `s_C = 1`,

  `p = [1,0,1,0,1,0,1,1]`,  `x = [1,0,1,0,1,0,1,5]`,  `y = [1,0,1,0,1,0,1,9]`,

and two type addresses `τ = [1,0,1,0,9,0,3,1]` and `σ = [1,0,1,0,9,0,3,2]` (distinct, in a
type subspace). Three links are homed at `d` (link subspace `s_L = 2`):

  `a₁ = [1,0,1,0,1,0,2,1]`,  `a₂ = [1,0,1,0,1,0,2,2]`,  `a₃ = [1,0,1,0,1,0,2,3]`,

with values (writing each endset by a unit-depth span on the stated address, so its
coverage is that address's subtree):

| link | `e₁` (from) | `e₂` (to) | `e₃` (type) |
|------|-------------|-----------|-------------|
| `a₁` | `{x}`-subtree | `{y}`-subtree | `{τ}`-subtree |
| `a₂` | `{y}`-subtree | `{x}`-subtree | `{τ}`-subtree |
| `a₃` | `{p}`-subtree | `{x}`-subtree | `{σ}`-subtree |

The five content/type addresses are pairwise non-nesting, so their subtree coverages are
pairwise disjoint (T10, ASN-0034). Take request endsets `X, Y, P` covering the subtrees
of `x, y, p`
respectively, and `Θ_τ` covering the subtree of `τ`. Assume `nullified(Σ) = ∅`, so
`addressable(Σ) = {a₁, a₂, a₃}`.

*Trace 1 — directional from/to (exercises FL-SND, FL-CMP, FL-DIR).* For
`q = (∗, X, Y, ∗)`, evaluate `sat` per link: `a₁` has `lift(e₁, X) = true` (coverage
contains `x`) and `lift(e₂, Y) = true`, home/type wildcards drop, so `sat(a₁, q, Σ)` holds;
`a₂` has `lift(e₁, X) ≡ touch(e₁, X) = false` (its from-coverage is `y`'s subtree,
disjoint from `X`), so it fails; `a₃` has `lift(e₁, X) ≡ touch(e₁, X) = false` (from-coverage
is `p`'s subtree), so it fails. By FL-DEF,
`findlinks((∗, X, Y, ∗), Σ) = {a₁}`. Soundness (FL-SND): the one returned link does satisfy
every constrained slot. Completeness (FL-CMP): `a₂, a₃` are correctly absent, both failing
the from-slot. Reversing to `q' = (∗, Y, X, ∗)` gives `findlinks(q', Σ) = {a₂}` by the
symmetric computation — `a₁` now fails `lift(e₁, Y)`. The two answers differ, witnessing
FL-DIR: `a₁ ∈ findlinks(q,Σ) \ findlinks(q',Σ)` and `a₂ ∈ findlinks(q',Σ) \ findlinks(q,Σ)`.

*Trace 2 — type alone (FL-TYP).* For `q = (∗, ∗, ∗, Θ_τ)`, only the type slot constrains:
`a₁` and `a₂` have `lift(e₃, Θ_τ) = true` (both type-touch `τ`), while `a₃` has type `σ`,
disjoint from `Θ_τ`, so it fails. `findlinks((∗, ∗, ∗, Θ_τ), Σ) = {a₁, a₂}` — the kind-of
link query, regardless of endpoints.

*Trace 3 — wildcard vs. empty (FL-WILD, FL-EMP).* The all-wildcard request returns
everything addressable: `findlinks((∗, ∗, ∗, ∗), Σ) = {a₁, a₂, a₃}`. By contrast the
request `(∗, ∅, ∗, ∗)` — a *constrained* from-slot with empty coverage — gives
`lift(eᵢ, ∅) = false` for every link, so `findlinks((∗, ∅, ∗, ∗), Σ) = ∅`. The empty slot
annihilates; the wildcard slot widens.

*Trace 4 — retraction (FL-RET).* If instead `a₁ ∈ nullified(Σ)`, then
`addressable(Σ) = {a₂, a₃}`, and Trace 1's `q = (∗, X, Y, ∗)` now yields
`findlinks(q, Σ) = ∅` — `a₁` is excluded by FL-DEF even though its endsets still satisfy
the criteria, and by R6a it stays excluded along every reachable `Σ →* Σ'`.

*Trace 5 — empty link endset (FL-EMP link-side symmetry).* Were a fourth link `a₄` homed
at `d` with from-endset `e₁ = ∅`, to-endset `e₂ = {x}`-subtree, and some non-empty type
endset (well-formed: L3 constrains only the type slot to be non-empty, so an empty `e₁` is
permitted), then under the constrained from-request `q = (∗, X, ∗, ∗)` it fails —
`lift(e₁, X) ≡ touch(∅, X) = coverage(∅) ∩ coverage(X) = ∅`, so `false` — and is absent.
Under the to-request `q' = (∗, ∗, X, ∗)`, with the from-slot wildcarded, it is admitted —
`lift(e₂, X) = true` while `lift(e₁, ∗) = true` drops the empty from-slot. The link with no
from-endpoint is found only as a to-match, never as a from-match — the same zero as the
empty *request* component, now on the link's side.

*Trace 6 — residence axis (exercises FL-RES, and FL-SND on the home slot).* The earlier
traces all fix `H = ∗`, so the residence criterion is never exercised concretely. We do so
now. Augment the store with a second document `d' = [1,0,1,0,2]` (document-level,
`zeros(d') = 2`, non-nesting with `d` — they are equal-length and differ in the last
component) and a fourth link homed there,

  `a₅ = [1,0,1,0,2,0,2,1]`,  so `home(a₅) = N(a₅).0.U(a₅).0.D(a₅) = [1,0,1,0,2] = d'`,

carrying endpoints *identical* to `a₁`'s — from-endset `{x}`-subtree, to-endset
`{y}`-subtree, type `{τ}`-subtree. (Its endsets reference content homed under `d`;
cross-document endsets are admissible, L4.) Take three home-sets, each a unit-depth span
whose coverage is the subtree of its root (`coverage = {t : root ≼ t}`, PrefixSpanCoverage,
ASN-0043; order-convex under T5, ASN-0034):

- `H_d` rooted at the document `d = [1,0,1,0,1]`, covering `{t : d ≼ t}`;
- `H_other` rooted at the document `d' = [1,0,1,0,2]`, covering `{t : d' ≼ t}`;
- `H_node` rooted at the node `[1]`, covering `{t : [1] ≼ t}` — every address beneath node 1.

Hold the endpoint constraints fixed at `X, Y` and vary only `H`. Both `a₁` and `a₅` satisfy
the endpoint slots (`lift(e₁, X) = true`, `lift(e₂, Y) = true`), so the from/to/type axes
*cannot* separate them — any difference in the answer is residence alone.

*Document-granularity, excluding `a₁`.* For `q = (H_other, X, Y, ∗)`,
`athome(a₁, H_other) = (home(a₁) = d ∈ {t : d' ≼ t})`; since `d` and `d'` are equal-length
and non-nesting, `d ∉ coverage(H_other)`, so `liftH(a₁, H_other) = false` and `a₁` is
excluded *purely on `liftH`* — its endsets still touch `X` and `Y`. Symmetrically
`athome(a₅, H_other) = (d' ∈ {t : d' ≼ t}) = true` by reflexivity of `≼`, so
`findlinks((H_other, X, Y, ∗), Σ) = {a₅}`.

*Document-granularity, readmitting `a₁`.* For `q = (H_d, X, Y, ∗)`,
`athome(a₁, H_d) = (d ∈ {t : d ≼ t}) = true` (reflexivity), readmitting `a₁`, while
`athome(a₅, H_d) = (d' ∈ {t : d ≼ t}) = false`, so `findlinks((H_d, X, Y, ∗), Σ) = {a₁}`.
The two document-bounded requests differ only in `H` — the endpoint slots are byte-for-byte
identical — yet the result flips between `{a₅}` and `{a₁}`. Residence is varied while
endpoints are held fixed, and the answer changes: orthogonality witnessed directly, exactly
as FL-RES asserts.

*Node-granularity, admitting both (the T5 subtree reading of `athome`).* For
`q = (H_node, X, Y, ∗)`, both documents lie beneath node 1 — `[1] ≼ d` and `[1] ≼ d'`, each
extending the one-component prefix `[1]` — so `athome` holds for both and
`findlinks((H_node, X, Y, ∗), Σ) = {a₁, a₅}`. This is genuinely a residence *test*, not its
absence: a link homed outside node 1's subtree would fail `liftH(·, H_node)`, whereas the
wildcard `H = ∗` of Trace 1 imposes no test at all. The node-rooted span verifies that
`athome` reads `home(a)`'s membership in the contiguous subtree `{t : [1] ≼ t}` (T5), so
the home-set bounds residence at node — and, by the same construction, account or
document — granularity.

*Trace 7 — FL-WP's load-bearing hazards (case (a) ghost-pre-coverage, case (c)
self-retraction).* The earlier traces fix the store and vary `q`; here we exercise the two
subtle conjuncts of FL-WP against a concrete K.λ step. Fix a retraction-type representative
at address `ρ = [1,0,1,0,9,0,3,7]` in the type subspace, so `coverage(R) = {t : ρ ≼ t}`;
let `Θ_ρ` be a request type endset covering `ρ`'s
subtree. Reserve two not-yet-allocated link addresses under `d`,
`ℓ = [1,0,1,0,1,0,2,5]` and `b = [1,0,1,0,1,0,2,6]`.

*Case (a), ghost-pre-coverage.* Suppose the store already holds a *standing* retraction link
`r₁ = [1,0,1,0,1,0,2,4]` with value `(∅, G_ℓ, {ρ}-subtree)`, where `G_ℓ` is a unit-depth span
covering `{t : ℓ ≼ t}` — the subtree of the *future* address `ℓ`. Then `r₁ ∈ L_R^Σ` (arity 3,
slot-3 coverage equal to `coverage(R)`), and its to-coverage names `ℓ` although `ℓ ∉ dom(Σ.L)` —
a ghost target (L4, EndsetGenerality, ASN-0043; LP17, ASN-0098). So `nullified(Σ)`
restricted to `dom(Σ.L)` omits
`ℓ`. Now a K.λ step allocates `ℓ` with the *ordinary* value `(X, Y, {τ}-subtree)` — type `τ`,
`coverage(τ) ≠ coverage(R)`, so `ℓ ∉ L_R^{Σ'}` and `L_R^{Σ'} = L_R^Σ`. Take `q = (∗, X, Y, ∗)`.
The matching conjunct holds: `lift(X, q.F) = lift(Y, q.G) = true`, home/type wildcards drop, so
`sat(ℓ, q, Σ')`. Yet FL-WP(a)'s addressability conjunct
`¬(E (c, F', G') ∈ L_R^Σ :: ℓ ∈ coverage(G'))` is *false* — `r₁` witnesses
`ℓ ∈ coverage(G_ℓ)` — so `ℓ ∈ nullified(Σ')`, `ℓ ∉ addressable(Σ')`, and `ℓ ∉ findlinks(q, Σ')`
despite the match. The wp correctly predicts absence, exhibiting the addressability conjunct as
non-vacuous: freshness against `dom(Σ.L)` does not discharge it.

*Case (c), self-retraction.* Now a K.λ step allocates the fresh address `b` with the arity-3
retraction value `(∅, G_self, {ρ}-subtree)`, where `G_self` is a unit-depth span covering
`{t : b ≼ t}` — `b`'s *own* subtree. Then `coverage({ρ}-subtree) = coverage(R)` with arity 3,
so `b ∈ L_R^{Σ'}` and `L_R^{Σ'} = L_R^Σ ∪ {(b, ∅, G_self)}`. Take `q = (∗, ∗, ∗, Θ_ρ)`: the
type slot matches (`lift({ρ}-subtree, Θ_ρ) = true`), the other slots wildcard, so
`sat(b, q, Σ')`. But FL-WP(c)'s self-retraction conjunct `b ∉ coverage(G')` is *false* —
`b ∈ coverage(G_self)` by reflexivity of `≼` — so `b ∈ nullified(Σ')` and `b ∉ findlinks(q, Σ')`:
the link nullifies its own address. The wp's sixth conjunct is exactly what predicts this. (Had
`b` instead carried arity `N > 3` with the same retraction-class type, ASN-0086's triple
restriction would keep `b ∉ L_R^{Σ'}`, routing it to case (a) — no self-retraction term, and it
would be returned by `q` whenever no *standing* tuple covered it.)

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| FL-DEF | `findlinks(q, Σ) = { a ∈ addressable(Σ) : sat(a, q, Σ) }`, with `sat` the conjunction of the four lifted slot-criteria (AND of the ORs); `addressable(Σ) = dom(Σ.L) \ nullified(Σ)` (ASN-0086, monotone by R6a); the operation has frame `Σ` (reads only, writes nothing) | introduced |
| FL-DEC | Decidability — `touch(e, r)` is decidable by ASN-0086's CoverageEqualityDecidable cell-decomposition run for intersection-nonemptiness, and `nullified(Σ)` is computable by ASN-0086's ActiveSubset argument, so `sat` is decidable per link and `findlinks(q, Σ) ⊆ dom(Σ.L)` is a finite, computable set (L-fin, ASN-0093) | introduced |
| FL-SND | Soundness — `a ∈ findlinks(q, Σ) ⟹ sat(a, q, Σ)`; a link with any constrained slot wholly disjoint from the request is excluded; no false positives | introduced |
| FL-CMP | Completeness — every `a ∈ addressable(Σ)` with `sat(a, q, Σ)` is returned; the result is exactly the satisfying subset; no silent omission | introduced |
| FL-JUNK | Non-impedance — the result is invariant under addition of non-matching links and unaffected by their quantity; match status is decided per link | introduced |
| FL-RES | Residence–endpoint independence — the home criterion is a function of the link address alone, the endpoint criteria of the link value alone; the four slots are orthogonal constraints | introduced |
| FL-DIR | Positional directionality — `F` matches `e₁` only and `G` matches `e₂` only; reversing the from/to constraints can change the result, keeping "from X" and "to X" distinct queries | introduced |
| FL-TYP | Type by address — the type criterion tests `coverage(e₃)` by address overlap, never reads stored content; ghost types are matchable, type may be constrained alone, and prefix-rooted type spans match subtype subtrees | introduced |
| FL-WILD | Wildcard semantics — a wildcard slot drops from the conjunction (universal), not empties it; all-wildcard returns all addressable links of every arity `N ≥ 3`, with no endset entering the matching predicate `sat` (every `lift` is `true` independent of endset content); addressability is still determined by reading retraction-link endsets to compute `nullified`; under a *constrained* request a link is matched on its first three endsets `e₁, e₂, e₃` alone (slots `e₄ … eₙ` never enter `sat`) | introduced |
| FL-EMP | Empty-constraint zero — a constrained slot with empty coverage (`∅`) gives `lift = false` for every link, so any empty constrained component forces `findlinks(q, Σ) = ∅`; empty-spec (zero) is distinct from wildcard/NOSPECS (unit). By the symmetry of `touch`, the same zero applies to a *link's* own empty endset (L3 permits `e₁ = ∅` or `e₂ = ∅`): such a link is excluded from any constrained from-/to-slot and admitted on that axis only under the corresponding wildcard | introduced |
| FL-CUR | Currency — `a ∈ findlinks(q, Σ) ⟺ a ∈ addressable(Σ) ∧ sat(a, q, Σ)`, the conjunction of FL-SND and FL-CMP against `addressable(Σ)`: current additions in, current retractions out, non-matches irrelevant | introduced |
| FL-MON | Monotone accumulation absent retraction — an unretracted matching link, once found, stays found as the store grows | introduced |
| FL-WP | Weakest precondition for the unique result-changing transition (K.λ), in its three result-changing cases, partitioned by retraction-relation membership `L_R^{Σ'}` (arity 3 ∧ slot-3 coverage equality `coverage(Σ'.L(a).e₃) = coverage(R)`), not coverage match alone — `(a)` a fresh *ordinary* link (`ℓ ∉ L_R^{Σ'}`, i.e. `coverage(Θ) ≠ coverage(R)` of any arity *or* `coverage(Θ) = coverage(R)` with arity `> 3`) enters the answer iff `ℓ ∉ nullified(Σ') ∧ liftH_d(q.H) ∧ lift(F, q.F) ∧ lift(G, q.G) ∧ lift(Θ, q.Θ)`, where the addressability conjunct `ℓ ∉ nullified(Σ') ≡ ¬(E (b, F', G') ∈ L_R^Σ :: ℓ ∈ coverage(G'))` is *not* discharged by freshness alone (a pre-existing retraction tuple may cover the ghost-allocated `ℓ`; cf. ASN-0086 wp Case 2), and is carried explicitly absent a retraction discipline; `(c)` a fresh *retraction* link (`b ∈ L_R^{Σ'}`: arity 3, `coverage(Θ_b) = coverage(R)`, value `(F_b, G', Θ_b)` with arbitrary, possibly attribution-bearing, from-endset `F_b`) enters iff `¬(E (c, F'', G'') ∈ L_R^Σ :: b ∈ coverage(G'')) ∧ b ∉ coverage(G') ∧ liftH_d(q.H) ∧ lift(F_b, q.F) ∧ lift(G', q.G) ∧ lift(Θ_b, q.Θ)` — case (a)'s conjunction with `L_R` extended by `b`'s own tuple and the live self-retraction conjunct `b ∉ coverage(G')` (which depends only on slot 3 and to-coverage, hence is unaffected by `F_b`); (a) and (c) are complementary and exhaustive over the fresh-link space; `(b)` an existing match survives a retraction-bearing K.λ iff `a ∈ findlinks(q, Σ) ∧ a ∉ coverage(G')` | introduced |
| FL-STB | Stability under editing — for any request (the grammar's only kind being I-address requests), the result is invariant under any transition preserving `Σ.L`; an instance of F-CIL (ComprehensionInvariantUnderΣL, ASN-0127), FL-DEF's membership predicate consulting only `Σ.L` and query-data, so retraction-set preservation follows from the single link-store hypothesis; pure-arrangement edits and content appends (F-PRES, ASN-0127) do not change which links are returned | introduced |
| FL-RET | Retraction absence — a retracted link is permanently and completely absent from every subsequent current-state inquiry, and its absence does not impede other results | introduced |
| FL-REACH | Cross-document reach — for any request `findlinks` is independent of `Σ.M`: global over the store, finds transcluded content once, returns all links under a whole-docuverse home-set, and contains every satisfying, addressable link that any document surfaces — `findlinks(q, Σ) ⊇ ⋃_d { a : a ∈ addressable(Σ) ∧ sat(a, q, Σ) ∧ discoverable_from(a, d, Σ) }`, strict given satisfying orphans (not a superset of the bare, request-independent discoverable union) | introduced |

## Open Questions

What must a version-qualified or time-qualified link inquiry guarantee, so that a link retracted in the current state remains discoverable in the prior states or versions that captured it before retraction?

What invariant must connect an I-address request to its arrangement-mediated (V-spec) phrasing, so that the two regimes agree exactly except on endpoints whose content has been fully removed from every arrangement?

Under what conditions on the home-set's coverage is the residence criterion equivalent to a single subtree-prefix test, so that residence bounding reduces to one containment check rather than a span-set membership?

What must hold of the type endset's coverage for the subtype-by-containment reading to be exact, neither admitting addresses outside the intended supertype subtree nor omitting intended subtypes?

What completeness guarantee must hold across a federation of independently administered stores, so that a single four-set inquiry reaches links homed in stores other than the one receiving the request?
