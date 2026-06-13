# ASN-0132: The FINDNUMOFLINKSFROMTOTHREE Operation

*2026-06-13*

We are asked a question of the form: *how many links match this description?* The
description is the four-set request of the link census — a **home-set** `H` bounding
where the links reside, a **from-set** `F` bounding what their first endset references, a
**to-set** `G` bounding their second endset, and a **three-set** `Θ` bounding their type
or connector endset. Nelson names the operation `FINDNUMOFLINKSFROMTOTHREE`; the system
is to return a number.

A number is a deceptively simple thing to ask for. Before we can compute it we must
settle a prior question that the request itself does not answer: *a number of what?* The
request describes links, but a link is a thing with internal multiplicity. It is strapped
to many bytes; its endsets may seize an arbitrary, broken set of spans. It may be reached
through content transcluded into many documents. It may surface at many places in many
arrangements, and refract into many versions. Each of these admits its own count. We must
decide which count the operation reports — and, this being a *specification* and not a
program, we must decide it in a way an alternative implementation could not reasonably
deviate from. The decision is not free. It is forced by what a link *is*, and most of
this note is the argument that forces it.

We write the system state as ASN-0047's five-tuple `Σ = (Σ.C, Σ.L, Σ.E, Σ.M, Σ.R)` — the
content store, the link store, the entity set, the family of document arrangements, and
the provenance relation. We use `coverage(e)` (ASN-0043) for the set of tumbler addresses
an endset references, `home(a)` (ASN-0043) for the document-level prefix at which a link
address `a` resides, and `|S|` for the cardinality of a finite set `S` (reserving `#t`
for tumbler length, ASN-0034). The four-set request is, exactly as in the sibling
enumeration, a four-tuple `q = (H, F, G, Θ) ∈ (Endset ∪ {∗})⁴` (ASN-0121), each component
an endset or the wildcard `∗`.

## The satisfying set is already named

We do not have to invent what it is for a link to match the four sets. That relation is
settled. ASN-0121 fixes the *satisfaction predicate*

  `sat(a, q, Σ) ≡ liftH(a, H) ∧ lift(Σ.L(a).e₁, F) ∧ lift(Σ.L(a).e₂, G) ∧ lift(Σ.L(a).e₃, Θ)`,

the AND of the ORs: each constrained slot demands a single-address overlap (`touch`)
between the link's endset and the request set, or, for the home slot, residence of
`home(a)` in the request region (`athome`); a wildcard slot drops out. The relation
ranges over *a link and a request* — not over any particular command. This is the load-
bearing fact for everything below: the description of *which links match* exists once, as
a property of links and requests, prior to and independent of any operation that consumes
it. We will count by consulting this relation directly, never by appeal to the operation
that enumerates.

ASN-0121 also fixes *which* links are eligible to be matched at all. A link withdrawn from
the current arrangement is not eligible; the eligible set is

  `addressable(Σ) = dom(Σ.L) \ nullified(Σ)`

(ASN-0086, ASN-0121) — the link store minus those targeted by a retraction tuple. With
the relation and the eligible set in hand, the count is the size of the agreement between
them.

> **CN-DEF (the counting operation).** For a request `q = (H, F, G, Θ)` and state `Σ`,
>
>   `countlinks_FTT(q, Σ) ≡ |{ a : a ∈ addressable(Σ) ∧ sat(a, q, Σ) }|`.
>
> The operation reads `Σ` and returns a natural number; its frame is `Σ` — it writes
> nothing, mutating no component of the state. Counting is observation, not transition.

Two things deserve immediate emphasis. First, the definition is phrased *through `sat`*,
not through the enumeration operation. We did not write "`countlinks_FTT(q, Σ) =
|findlinks_FTT(q, Σ)|`," though that equation is true (we prove it below). To define the
count as "the length of what the find returns" would make one operation conceptually
subordinate to the other, and would turn their agreement into a theorem we must re-prove
every time either is edited. Defining both as views of the one set `{a : a ∈
addressable(Σ) ∧ sat(a, q, Σ)}` makes the agreement structural. Second, the definition
quantifies over `addressable(Σ)`, so a withdrawn link is excluded before it is ever
weighed against the four sets.

**Well-definedness.** We must establish that the argument of `|·|` lies in the domain of
cardinality — that the counted set is finite. It is. The set
`{a : a ∈ addressable(Σ) ∧ sat(a, q, Σ)}` is a subset of `dom(Σ.L)`, which is finite
(L-fin, ASN-0093); a subset of a finite set is finite; and `sat` is decidable per link
(FL-DEC, ASN-0121), so the set is not merely finite but computable. Hence
`countlinks_FTT(q, Σ) ∈ ℕ` is well-defined for every `q` and every reachable `Σ`. There is
no loop to terminate and no bound function to exhibit: the count is the cardinality of a
finite comprehension, not the result of a search that might run away. (That a *particular*
back end realises the cardinality by a search that does run over the store is a matter of
cost, taken up in the final section; it does not bear on what the number *is*.)

**CN-LOC (link-store locality).** Because `sat(a, q, Σ)` consults only the stored value
`Σ.L(a)` and the address projection `home(a)`, and `addressable(Σ)` is a function of
`Σ.L` alone (FL-LOC, ASN-0121), the counted set — and therefore the count — is a function
of `Σ.L` and `q` alone. The content store `Σ.C`, the arrangements `Σ.M`, the entity set
`Σ.E`, and the provenance relation `Σ.R` are never read. We will lean on this repeatedly:
whatever lives in those four components cannot move the number.

A remark on the request as given. We take `q` to be a request already phrased over
*addresses* — its four components are endsets (address coverages) or wildcards. A front
end that lets a reader phrase the query by pointing at content in a document must first
*resolve* those pointings, through that document's arrangement, into the address sets of
`q`; the implementation does exactly this V-to-I resolution against the arrangement at the
instant of the call. That resolution is upstream of the operation we specify: it produces
`q`. Everything we say about `countlinks_FTT(q, Σ)` is said of a *resolved* request. The
separation is load-bearing: a fixed resolved `q` is what the operation measures, whereas
re-phrasing the same intent can re-resolve to a *different* `q`. Any discrepancy a reader
perceives between two such requests lives in the resolution, never in the count.

## The unit is identity

We can now answer "a number of what?" The counted set is a *set of link addresses*. By
extensionality a set contains each member once, so the cardinality counts *distinct link
addresses* — distinct link identities. A link's identity is its address `a ∈ dom(Σ.L)`,
fixed at creation and permanent thereafter (L12, ASN-0043): the address neither moves nor
is reissued. The census counts identities, and each qualifying identity contributes
exactly one. The competing units — anchoring, transclusion, appearance, and version-refraction — are
ruled out, each by a distinct property, and it is worth walking the four cases rather than
asserting the conclusion.

> **CN-UNIT (the unit of counting is link identity).** For every request `q` and state
> `Σ`, each `a ∈ addressable(Σ)` with `sat(a, q, Σ)` contributes exactly `1` to
> `countlinks_FTT(q, Σ)`, and each `a` with `¬sat(a, q, Σ)` or `a ∉ addressable(Σ)`
> contributes `0`. The contribution of a link is independent of (a) the number of spans
> or addresses its endsets reference, (b) the number of documents through which its
> endpoint content is reachable, (c) the number of arrangement positions at which it
> surfaces, and (d) the number of versions into which the documents it touches refract.

*(a) Anchoring multiplicity does not multiply the contribution.* Whether `a` is in the
counted set is the truth value of `sat(a, q, Σ)`, a single Boolean. Its from-clause is
`lift(Σ.L(a).e₁, F) ≡ touch(Σ.L(a).e₁, F) ≡ coverage(Σ.L(a).e₁) ∩ coverage(F) ≠ ∅`
(ASN-0121) — an *existential* over the addresses of the endset. An endset whose from-set
seizes five disjoint spans and whose to-set seizes three still yields *one* truth value
per slot; the link enters the set once or not at all. The AND-of-the-ORs collapses any
number of matching anchor spans into a single yes. This is the formal counterpart of
Nelson's ruling that a link whose endsets touch many passages "is counted once." The
count is not the number of matching byte-pairs, nor the number of spans an endset
presents; those quantities are consumed inside `touch` and never escape it.

*(b) Transclusion multiplicity does not multiply the contribution.* Suppose `a`'s
endpoint content is transcluded — shared by reference — into `N` documents. Transclusion
is a property of the arrangements `Σ.M`: the same I-addresses appear in the ranges of `N`
documents' arrangements, the content itself stored once (ASN-0058, ASN-0036). It adds no
link address to `Σ.L`. By CN-LOC the count never consults `Σ.M`, so the `N` documents are
structurally invisible to it; `a` is one address in `Σ.L`, counted once. The quantity that
grows with sharing — *how many documents reach the content* — is a count of documents, not
of links, and is measured by an operation over `Σ.M`, not by this one. This is the whole
content of CN-UNIT clause (b): a consequence of CN-LOC, carrying nothing beyond it, and so
needing no claim of its own.

This is exactly the conflation Nelson warns against: "many documents" is real, but it is
attached to the wrong noun. The link is one; what proliferates is the set of windows onto
it.

*(c) Appearance multiplicity does not multiply the contribution.* A link surfaces in
document `d` when `d`'s arrangement reaches its endpoint content — ASN-0098's
`discoverable_from(a, d, Σ)`, an `Σ.M`-mediated relation. A link shown at eight anchor
points across four documents is discoverable from each, yet it is one address. Again by
CN-LOC, `discoverable_from` does not enter the count. Display and surfacing are front-end
concerns; the back-end census counts what is *stored and owned*, not what a viewer is
*shown*.

*(d) Version-refraction multiplicity does not multiply the contribution.* A document may be
forked into many versions, and the design has a link *refract* across them — a link made
against one version reaches the corresponding places in all, so "a link to one version of a
document is a link to all versions." One might fear this mints a distinct link per version.
It does not. The fork composite (J4, ASN-0047) allocates the new version and populates its
arrangement over the *content* subspace alone — its V-to-I step ranges over `V_{s_C}`, and
by "no other elementary steps" it performs no link allocation (`K.λ`) and no link-subspace
extension — so a link homed at the source yields *no* copy at the new version, and `Σ.L` is
untouched by forking. A link's identity is its single address (L12, ASN-0043), and the
version DAG does not multiply it. What "refraction into many versions" actually denotes is
that each version, sharing the source's content I-addresses, *surfaces* the same one link;
that is appearance multiplicity (c) over a family of documents that happen to be versions,
already excluded by CN-LOC because the count never reads `Σ.M`. Versions are therefore not a
fourth independent unit but a special case of the third — the link is one address, stored
once, counted once, however many versions refract it.

The four cases share a shape: each rejected unit is an `Σ.M`-quantity or an inside-`touch`
quantity, and CN-LOC excludes the former while the existential structure of `touch`
absorbs the latter. The count is keyed to identity because the satisfying *set* is keyed
to identity.

*Implementation note.* Gregory's back end realises the count by materialising the matching
links into a list and walking it. The intended unit is identity — the walk is meant to
yield one entry per distinct link. The realisation does not perfectly achieve this: when a
single link's endset has been fragmented into two or more non-contiguous address regions
that the request overlaps, a defect in the list's deduplication admits the same link
address twice, so the reported number can exceed the cardinality of the identity set. This
is a deviation *from* CN-UNIT, not evidence against it: the abstract operation is the
cardinality of a set, in which an address cannot appear twice, and an implementation that
reports `2` for one identity has miscounted. The deviation is instructive precisely
because we can say *what* it deviates from.

## One description, two views

We have now defined two operations over the same satisfaction relation: the enumeration
`findlinks_FTT(q, Σ) = {a ∈ addressable(Σ) : sat(a, q, Σ)}` (ASN-0121, FL-DEF) and the
count `countlinks_FTT(q, Σ) = |{a ∈ addressable(Σ) : sat(a, q, Σ)}|` (CN-DEF). Neither
mentions the other; both bottom out at `sat`.

> **CN-SHARED (the match-description lives in the satisfaction relation).** The four-set
> matching criterion is `sat` (ASN-0121), a predicate on a link, a request, and a state.
> The enumeration is the *set* it carves out; the count is the *size* of that set. The
> specification of each is a query over `sat`; the specification of neither appeals to the
> behaviour of the other.

This factoring is what makes the relationship between count and enumeration a theorem
rather than an obligation.

> **CN-ENUM (count is the cardinality of the enumeration, at one state).**
>
>   `countlinks_FTT(q, Σ) = |findlinks_FTT(q, Σ)|`,
>
> because both sides are the cardinality of the single set `{a ∈ addressable(Σ) :
> sat(a, q, Σ)}` — the right side by FL-DEF (ASN-0121), the left by CN-DEF. The equality
> is not stipulated; it is the observation that the two operations are the size and the
> contents of one set. There is exactly one set, so the count and the enumeration cannot
> drift apart.

The qualifier *at one state* is essential and is the whole content of the consistency
guarantee. The equality holds whenever both sides are evaluated against the *same* `Σ`.
The sibling enumeration, asked at a later state `Σ'`, returns `findlinks_FTT(q, Σ')`,
whose size is `countlinks_FTT(q, Σ')` — equal to `|findlinks_FTT(q, Σ')|`, not necessarily
to `countlinks_FTT(q, Σ)`. If a link is created or retracted between a count inquiry and a
later enumeration, the two answers describe two different stores and need not agree. This
is not a failure of CN-ENUM; it is the same theorem applied twice, once per state. A
caller who needs `count = length` to hold *across* two separate inquiries needs the two
inquiries to observe one state, which is a property of the surrounding concurrency
discipline, not of either operation. The operations themselves guarantee single-state
agreement and nothing stronger, because there is nothing stronger to guarantee about two
measurements of a changing quantity.

*Implementation note.* Gregory's back end computes the count by invoking the *same*
matching routine the enumeration invokes, taking its materialised result, and reporting
its length. There is one matching routine, shared; the count carries no private copy of
the four-set logic that could drift from the enumeration's. This is the implementation's
realisation of CN-SHARED, and it makes single-state agreement automatic at the level of
code, for the same reason CN-ENUM makes it automatic at the level of specification.

## What a count of zero asserts

A returned `0` is the most informative answer the operation gives, because it makes a
universal claim, and we must say precisely which one.

> **CN-ZERO (zero is a present-store existential).**
>
>   `countlinks_FTT(q, Σ) = 0  ⟺  (A a : a ∈ addressable(Σ) : ¬sat(a, q, Σ))`.
>
> A zero count asserts that *no* addressable link in the store satisfies the four sets at
> `Σ` — that the satisfying set is empty. It is a positive statement about the contents of
> the link store, not a report that a search failed or that nothing could be displayed.

Two weaker readings must be excluded, and each is excluded by a property already in hand.

The reading "*none could be found*" — that the operation gave up amid a mass of
irrelevant links — is excluded by non-impedance (FL-JUNK, ASN-0121): the quantity of
non-satisfying links does not in principle affect which satisfying links are determined.
`sat` is decided per link; a vast body of junk neither enlarges the satisfying set nor
displaces a member from it. A zero is therefore a *verdict*, reached over the whole
addressable store, not an exhaustion artifact.

The reading "*none could be displayed*" — that nothing currently surfaces — is excluded by
CN-LOC: surfacing is an `Σ.M`-property the count does not read. A link satisfying `q` but
displayed nowhere is still counted (we return to this under CN-ORPHAN). So a zero cannot
mean "nothing fit on a screen."

There is, however, a second route to `0` that we must distinguish from store-emptiness,
on pain of misreading the guarantee. If a *constrained* component of `q` itself has empty
coverage, then its lift is `false` for every link (FL-EMP, ASN-0121), and the count is
`0` vacuously — the request asks about an empty address set. This is the *empty-request*
zero, and it is genuinely different in meaning from the *empty-store* zero of CN-ZERO,
though the two are indistinguishable in the returned number. The distinction surfaces
sharply at the resolution boundary. A reader who phrases the query by pointing at content
that has since been removed from every arrangement will have those pointings resolve to an
empty address set; the resolved `q` has an empty constrained component; the count is `0`.
That `0` does *not* assert that no link connects the intended content — it asserts that
the request, as resolved, names nothing. The link the reader meant to count may persist,
fully addressable, with its endsets intact; it is simply not reached, because the request
that was supposed to reach it collapsed during resolution. The substantive guarantee of
CN-ZERO — "the store contains no such link" — attaches to a *non-degenerate* request, one
whose constrained components have non-empty coverage. A zero must therefore be read against
which kind of request produced it.

For the contrast that makes the present-store reading precise: a zero count is a claim
about *now*. It is not a prophecy. The docuverse grows; a satisfying link may be created
an instant later, and the count will then be positive. CN-ZERO certifies present absence
from the addressable store, and is silent about the future — exactly the present-tense
reading ASN-0127 isolates for discovery zeros (D-ZERO), here applied to the existence
census over `addressable(Σ)`.

## The count and the store at the instant of inquiry

The count is a measurement, and a measurement of a changing quantity is true of the moment
it is taken.

> **CN-SNAP (the count is a snapshot, not a durable fact).** `countlinks_FTT(q, Σ)` is a
> function of the state `Σ`. No component of `Σ` records it; there is no stored counter
> that the operation reads or maintains. After any mutation `Σ → Σ'` the value
> `countlinks_FTT(q, Σ')` may differ from `countlinks_FTT(q, Σ)`, and the specification
> imposes no obligation that the earlier value remain valid. Re-establishing the count
> requires re-evaluating the cardinality at the current state.

The justification is that the count derives all of its content from `sat` and
`addressable`, both evaluated against the live `Σ`; it is a derived aggregate over mutable
sets and inherits none of the permanence guarantees that attach to the things the system
*does* preserve. Addresses, once allocated, are permanent (ASN-0093); content values, once
stored, are immutable (S0, ASN-0036); link values, once created, are fixed (L12,
ASN-0043). A count is none of these. It is not an identity, not a content value, not a
link value — it is the size of a query's answer, and the system makes no promise to honour
a stale size. The discipline this implies is *recompute-on-read*, not *cache-as-truth*:
the only way to know the current count is to take it again.

Permanence guarantees what exists and can be found again; a count is recomputed per
inquiry. That the docuverse keeps everything it ever created does *not* mean it keeps every
count it ever reported — permanence is a promise about *what exists*, a count a promise
about *how many satisfy, right now*. The first is honoured at the level of the store; the
second is recomputed at each inquiry. Both are kept, and they are kept by being different
kinds of statement.

*Implementation note.* Because the back end recomputes the count by re-running the search,
two inquiries separated by a mutation observe two states and may return different numbers;
nothing is cached, and there is no snapshot tying a count to a later enumeration. The count
is a function of whichever `Σ` is observed, and so must be read as *of the moment* it is
taken.

## Stability under content editing

Although the count is a snapshot that can change, there is a large and important class of
state changes under which it provably does *not* change: the edits that rearrange a
document's content without touching the link store.

> **CN-STAB (invariance under arrangement editing).** For a fixed request `q`, any
> transition `Σ → Σ'` that preserves the link store — `dom(Σ'.L) = dom(Σ.L)` and
> `Σ'.L(a) = Σ.L(a)` for all `a` — satisfies
> `countlinks_FTT(q, Σ') = countlinks_FTT(q, Σ)`.

The proof is immediate from CN-LOC: the count is a function of `Σ.L` (through both `sat`
and `addressable`), and the single hypothesis of link-store preservation fixes everything
the count reads. Since `nullified(Σ)` is selected from the retraction relation `L_R^Σ`,
which `Σ.L` determines, the hypothesis `Σ'.L = Σ.L` entails `nullified(Σ') = nullified(Σ)`;
hence F-PRES (ASN-0127) — link-store preservation alone — discharges the precondition. The
transitions this covers are exactly the ones that leave `Σ.L` intact. Content insertion,
deletion, and rearrangement act on a document's arrangement `Σ.M(d)` and
preserve `Σ.L` (F-PRES, ASN-0127); content allocation (K.α) and provenance recording (K.ρ)
likewise leave the link store untouched. Every such transition leaves the count exactly
where it was. Only link creation and retraction — transitions that grow `Σ.L` or
`nullified` — can move it.

This is the count-level expression of the survivability of links under editing. A link
strapped to bytes by content identity does not change which four-set descriptions it
satisfies when those bytes are rearranged, because the link's endsets reference addresses,
not positions, and editing changes positions, not addresses. A description grounded in
content identity therefore yields a stable count for as long as its links live. Insertion,
deletion, and rearrangement of content — performed on the documents the links point into,
or on the document a link is homed in, or on any document at all — leave the number alone.

A sharp instance: suppose a link's own entry in its home document's arrangement is removed
— the link is "reverse-orphaned," no longer surfaced from its home, yet still present in
the store with its endsets intact. This removal is an arrangement contraction; it
preserves `Σ.L`. By CN-STAB the count is unchanged, and in particular a *home-bounded*
count — one whose home-set `H` selects that document — still includes the link, because
`home(a)` is a projection of the permanent address `a` (L12, ASN-0043) and is unmoved by
any edit to an arrangement. Residence is determined by identity, and identity does not
shift when content does.

One caveat applies, and CN-STAB makes it precise. Stability is asserted for a *fixed* `q`.
A reader who re-phrases the same intent after an edit — pointing again at the "same"
content, now at a shifted position — submits a *different* request, because the resolution
against the edited arrangement yields different addresses. The count of that different
request may differ. What CN-STAB guarantees is that the link's *membership* in a *given*
description is stable; what it does not guarantee, and should not, is that two different
descriptions return the same number. This is the resolution principle of the opening
remark, applied to editing: any apparent movement under re-phrasing lives in the
resolution, never in the count, so a rearrangement that preserves addresses leaves every
address-phrased count exactly invariant.

## Retraction and permanence

Link retraction is the one content-preserving change that *does* move the count, and it
moves it in a direction permanence might seem to forbid. The apparent tension dissolves
once we see that retraction acts on the *addressable view*, not on the *store*.

> **CN-RETRACT (retraction excludes immediately; the link persists).** If
> `a ∈ nullified(Σ)`, then `a` contributes `0` to `countlinks_FTT(q, Σ)` for every `q`,
> and continues to contribute `0` at every reachable successor state (the nullified set
> never shrinks — R6a, ASN-0086). Yet `a` remains in `dom(Σ.L)` with its value `Σ.L(a)`
> permanently fixed (L12, ASN-0043). The count ranges over `addressable(Σ) = dom(Σ.L) \
> nullified(Σ)`; it counts the *active view*, not the *store*.

The exclusion is immediate because there is no separate tally to decrement: the count is
recomputed over `addressable(Σ)` at each inquiry (CN-SNAP), and the instant a retraction
tuple enters and places `a` in `nullified`, the next count omits `a` (FL-RET, ASN-0121).
There is no window in which a retracted link is still counted, and none in which it is lost
from the store. The two statements — *gone from the count* and *kept in the store* — are
about two different sets: the active view shrinks while the store does not. This is the
count-level form of the view/store distinction the architecture maintains everywhere:
withdrawal removes a thing from the current arrangement of what is active, never from the
permanent record of what exists. A count taken against the active view excludes the
withdrawn link at once; a count that could be taken against a prior view would still
include it. Both are honest, because each counts the set it names.

The complementary direction — growth — is governed by the same per-link logic.

> **CN-MONO (monotone accumulation absent retraction).** Across any `Σ →* Σ'` in which no
> currently-counted link becomes nullified, `countlinks_FTT(q, Σ) ≤ countlinks_FTT(q, Σ')`,
> and each newly created link that satisfies `q` and is addressable increments the count by
> exactly `1`.

This is the cardinality of FL-MON (ASN-0121): a matching, non-withdrawn link stays in the
satisfying set as the store grows, so the count cannot fall. That link creation is the only
transition which can *add* to the satisfying set is CN-STAB read with F-PRES (ASN-0127) —
every non-`K.λ` transition preserves `Σ.L`, and with it the count; that a single `K.λ` step
contributes at most one address, fresh and so not already counted, is its effect and
freshness clauses (ASN-0093); and the exact four-set increment, retraction-coverage
condition and all, is FL-WP(a) (ASN-0121), which the next paragraph derives in full. We can
make the increment exact by a weakest-precondition step. Consider a transition `Σ → Σ'` that
creates a fresh ordinary link `ℓ` — *fresh*, so `ℓ ∉ dom(Σ.L)`, and *ordinary*, so it does
not enter the retraction relation and `L_R^{Σ'} = L_R^Σ`.

First, every pre-existing link's contribution is unmoved. For `a ∈ dom(Σ.L)`
the stored value survives creation, `Σ'.L(a) = Σ.L(a)` with `a ∈ dom(Σ'.L)` (L12, ASN-0043;
LP13, ASN-0098); and `sat(a, q, ·)` reads only `Σ.L(a)` and the projection `home(a)` of the
permanent address `a` (CN-LOC), so `sat(a, q, Σ') = sat(a, q, Σ)`. Its addressability is
fixed too: because `ℓ` is not a retraction, `L_R^{Σ'} = L_R^Σ`, so the nullified set
restricted to the old domain is unchanged, `nullified(Σ') ∩ dom(Σ.L) = nullified(Σ)`, and
each pre-existing `a` is addressable at `Σ'` exactly when it was at `Σ`. The contributions
of `dom(Σ.L)` therefore sum to the same total at both states.

The whole change is thus the contribution of `ℓ` itself: `1` if `ℓ ∈ addressable(Σ') ∧
sat(ℓ, q, Σ')`, and `0` otherwise. Now `ℓ ∈ dom(Σ'.L)` holds by creation, so `ℓ ∈
addressable(Σ')` reduces to `ℓ ∉ nullified(Σ')`; and since `L_R^{Σ'} = L_R^Σ`, this is

  `¬(E (b, F', G') ∈ L_R^Σ :: ℓ ∈ coverage(G'))`

— *no pre-existing retraction tuple already covers `ℓ`'s address*. This clause is not free:
"ordinary" buys `L_R^{Σ'} = L_R^Σ`, which forbids a *new* retraction, but leaves wide open
that a *standing* one already names the fresh address. Hence

  `countlinks_FTT(q, Σ') = countlinks_FTT(q, Σ) + 1`  if `sat(ℓ, q, Σ') ∧ ℓ ∉ nullified(Σ')`, and
  `countlinks_FTT(q, Σ') = countlinks_FTT(q, Σ)`      otherwise,

and reading off the precondition for the count to rise,

  `wp(create ℓ, countlinks_FTT(q, ·) = countlinks_FTT(q, Σ) + 1)
        = sat(ℓ, q, Σ') ∧ ¬(E (b, F', G') ∈ L_R^Σ :: ℓ ∈ coverage(G'))`

— the new link must itself satisfy the four sets *and* not be born already-retracted. This
is exactly the FL-WP(a) condition of ASN-0121 (which carries that second conjunct precisely
for a fresh ordinary link), not a weakening of it. Under the unit-depth retraction
discipline (ASN-0086) the second conjunct is automatic, and the precondition collapses to
`sat(ℓ, q, Σ')`: ASN-0086's disciplined-domain simplification (wp Case 2) — resting on the
prefix-antichain structure of the link domain (R0a, ASN-0086) — already establishes that a
freshly emitted link address lies in no standing retraction tuple's to-coverage, so we
inherit that conclusion rather than re-deriving it here. The
census grows by precisely the links that are made, match, and are not born
already-retracted, and shrinks by precisely the matching links that are withdrawn; it moves
under nothing else.

A note on what retraction does *not* undo. Nullifying a link removes it from the active
count, but it does not restore any link the retracted one had itself withdrawn; a retracted
retractor's stored value continues to nullify its targets (R6b, ASN-0086). And a withdrawn
link is not brought back by editing — re-counting it in the active view requires emitting a
fresh, matching link, which receives a fresh identity (R6c, ASN-0086). The count tracks the
active view faithfully in both directions, and the active view is shaped by creation and
retraction alone.

## Counting the unsurfaced

One case remains: a link anchored to fresh content that no arrangement yet surfaces, or to
content that has dropped out of every current view. Is it counted? It is — and this is
forced by CN-LOC, but the consequence is worth stating on its own because it is where the
existence census and the discovery census visibly part.

> **CN-ORPHAN (orphans are counted).** A link `a ∈ addressable(Σ)` with `sat(a, q, Σ)` is
> counted whether or not any document surfaces its endpoint content — that is, whether or
> not `discoverable_from(a, d, Σ)` holds for any `d`. The count is an *existence* quantity
> over the addressable store, not a *discovery* quantity over arrangements.

The link's eligibility turns on `sat` and `addressable`, both `Σ.L`-local; surfacing is an
`Σ.M`-relation the count does not read. An orphaned link — one whose endpoint addresses lie
in no arrangement's range — remains in `dom(Σ.L)` with its value unchanged (LP17,
ASN-0098), so if it is addressable and matches, it is counted. Symmetrically, content
linked but not yet surfaced anywhere is still linked, and the link still counts. The count
answers "what connections exist in the store," and a connection exists whether or not a
reader can presently walk to it. Counting it tells you the link is part of the literature's
structure; surfacing it is the front end's separate job, governed by the arrangement
layer.

This explains, finally, the asymmetry we deferred. A link can be counted yet not
discoverable; the count is a *superset* of what any document surfaces (the cross-document
reach FL-REACH, ASN-0121, made a cardinality). The gap is exactly the orphans. And it is
not permanent in either direction: an orphan becomes discoverable the moment some
arrangement is extended to reach its content (resurrection, LP18, ASN-0098). But note what
that resurrection does *not* do — it does not change the count, because the link was
counted all along. Discoverability rose; existence did not. The two censuses move on
different signals, and FINDNUMOFLINKSFROMTOTHREE is the existence census.

## A census, computed

The three central rulings — that anchoring, transclusion, and appearance multiplicity each
collapse to a contribution of one (CN-UNIT); that a nullified link contributes nothing yet
persists (CN-RETRACT); and that an unsurfaced link is counted all the same (CN-ORPHAN) —
are easiest to trust against a specific store. We exhibit one.
Fix a document-level prefix `d₁ = 1.0.1.0.1` and two of its neighbours `d₂ = 1.0.1.0.2`,
`d₃ = 1.0.1.0.3` (each a `zeros = 2` document tumbler, T4). Write `⟨z⟩` for the unit-depth
span `(z, δ(1, #z))` at address `z`, whose coverage is the subtree `{t : z ≼ t}`
(PrefixSpanCoverage, ASN-0043).

The request constrains the from-set alone:

  `q = (∗, F, ∗, ∗)`,  `F = {(1.0.1.0.1.0.1.5, δ(8, 8))}`,

so `coverage(F) = {t : 1.0.1.0.1.0.1.5 ≤ t < 1.0.1.0.1.0.1.13}` — a contiguous content
region in the text subspace (`s_C = 1`) of `d₁`, holding the eight ordinals `5..12`. With
three slots wildcard, `sat(a, q, Σ)` reduces to `lift(Σ.L(a).e₁, F) ≡ touch(Σ.L(a).e₁, F)`:
a link qualifies exactly when its from-endset's coverage meets `coverage(F)`.

The link store `Σ.L` holds five addresses, all homed under `d₁` (link subspace `s_L = 2`).
Each ordinary `aᵢ` is a standard triple `(e₁, e₂, Θ₀)` with non-empty type `Θ₀` and some
to-endset `e₂`; only `e₁` is shown, the other slots being immaterial to this `q`.

| address | from-endset `e₁` | note |
|---|---|---|
| `a₁ = 1.0.1.0.1.0.2.1` | `{⟨1.0.1.0.1.0.1.6⟩, ⟨1.0.1.0.1.0.1.7⟩, ⟨1.0.1.0.1.0.1.9⟩}` | addressable; its content at `…1.7` transcluded into `d₂, d₃` |
| `a₂ = 1.0.1.0.1.0.2.2` | `{⟨1.0.1.0.1.0.1.8⟩}` | nullified by `a_R` |
| `a₃ = 1.0.1.0.1.0.2.3` | `{⟨1.0.1.0.1.0.1.11⟩}` | addressable; orphan (surfaced by no arrangement) |
| `a₄ = 1.0.1.0.1.0.2.4` | `{⟨1.0.1.0.2.0.1.3⟩}` | addressable; references `d₂` content |
| `a_R = 1.0.1.0.1.0.2.5` | `∅` (to-endset `{⟨a₂⟩}`, type `R`) | addressable; retractor of `a₂` |

`a_R` is a retraction tuple `(∅, {⟨a₂⟩}, R)` whose to-coverage `{t : a₂ ≼ t}` meets
`dom(Σ.L)` only at `a₂` (the other addresses are equal-length and distinct, hence
prefix-incomparable). So `nullified(Σ) = {a₂}` and `addressable(Σ) = {a₁, a₃, a₄, a_R}`. We
read each contribution off `sat` and `addressable`, consulting nothing else (CN-LOC).

*`a₁` contributes `1`, three multiplicities notwithstanding.* Its from-endset seizes three
pairwise-disjoint spans, and every one of them meets `F`: each of `1.0.1.0.1.0.1.6`, `.7`,
`.9` lies in `coverage(F)`, so `coverage(e₁) ∩ coverage(F) ≠ ∅` holds three times over.
But the from-clause is a single existential `touch(e₁, F)`, so three reasons to match yield
one yes, not three — `a₁` enters the satisfying set once (CN-UNIT (a)). Suppose further
that the content at `1.0.1.0.1.0.1.7` is transcluded into `d₂` and `d₃` — it lies in
`ran(M(d₁))`, `ran(M(d₂))`, `ran(M(d₃))` — and surfaces at several arrangement positions in
each. Every such fact lives in `Σ.M`, which the count does not read (CN-LOC); `a₁` is one
address in `Σ.L`, weighed once (CN-UNIT (b), (c)). Contribution: `1`.

*`a₂` contributes `0`, though it satisfies `q`.* Its from-endset meets `F`
(`1.0.1.0.1.0.1.8 ∈ coverage(F)`), so `sat(a₂, q, Σ)` is `true`. But `a₂ ∈ nullified(Σ)`,
hence `a₂ ∉ addressable(Σ)`, and CN-DEF ranges over `addressable(Σ)`: `a₂` is filtered out
before its `sat` value is ever weighed. It nonetheless remains in `dom(Σ.L)` with its value
fixed (L12, ASN-0043) — gone from the count, kept in the store (CN-RETRACT). Contribution:
`0`.

*`a₃` contributes `1`, surfaced nowhere.* Its from-endset meets `F`
(`1.0.1.0.1.0.1.11 ∈ coverage(F)`) and it is addressable, so it is counted. That the
content at `1.0.1.0.1.0.1.11` sits in no arrangement's range — `discoverable_from(a₃, d, Σ)`
fails for every `d`, making `a₃` an orphan — is invisible to the count, which reads `Σ.L`
and not `Σ.M` (CN-ORPHAN). Contribution: `1`.

*`a₄` contributes `0`, disjoint from the request.* Its sole from-span references content
under `d₂`, whose address `1.0.1.0.2.0.1.3` exceeds `coverage(F)`'s upper bound — it diverges
from the region at the document component (`2 > 1`), so it is `> 1.0.1.0.1.0.1.13`. Thus
`coverage(e₄) ∩ coverage(F) = ∅`, `touch(e₄, F)` is `false`, and `sat(a₄, q, Σ)` fails.
Addressable but non-matching, `a₄` is excluded. Contribution: `0`.

*`a_R` contributes `0`, for want of a from-endset.* The retractor's from-endset is `∅`, and
`lift(∅, F) ≡ touch(∅, F) ≡ ∅ ∩ coverage(F) = ∅` is `false` (FL-EMP, ASN-0121): an empty
constrained slot annihilates the match. So `a_R`, addressable though it is, fails `sat`.
Contribution: `0`.

Summing the contributions, `countlinks_FTT(q, Σ) = 2`, the contributors being `a₁` and
`a₃`. The same number arrives through CN-DEF directly —
`|{a ∈ addressable(Σ) : sat(a, q, Σ)}| = |{a₁, a₃}| = 2` — and through CN-ENUM, since
`findlinks_FTT(q, Σ) = {a₁, a₃}` has cardinality `2`. The satisfying orphan `a₃` is in this
set while the satisfying-but-nullified `a₂` is not — exactly the gap CN-ORPHAN and
CN-RETRACT predict.

The all-wildcard request closes the boundary at the other end. With `q* = (∗, ∗, ∗, ∗)`
every slot drops out and `sat(a, q*, Σ)` is `true` for every `a`, so the count is the size
of the whole active view:

  `countlinks_FTT(q*, Σ) = |addressable(Σ)| = |{a₁, a₃, a₄, a_R}| = 4`

— nullified `a₂` alone excluded. Constraining a slot can only narrow this, so the wildcard
census is the *maximum* any request attains over a fixed store, just as the empty-coverage
zero (FL-EMP) is the minimum. Our `q` sits between them: from-set `F` admits `a₁` and `a₃`,
declines `a₄` (disjoint) and `a_R` (empty), and never sees `a₂` (withdrawn).

The home-set, wildcard in every request so far, exercises the one structurally distinct
slot — `liftH(a, H) ≡ athome(a, H) ≡ home(a) ∈ coverage(H)`, a membership test on the
*address projection* `home(a)`, not the endset overlap `touch` the other three slots use.
Bind it to `d₁`. Let `H₁ = {⟨d₁⟩}`, with coverage `{t : d₁ ≼ t}` (PrefixSpanCoverage), and
ask

  `q_H = (H₁, F, ∗, ∗)`.

Every stored link is homed under `d₁`: `home(aᵢ) = 1.0.1.0.1 = d₁` for each of the five, the
projection `N(·).0.U(·).0.D(·)` stripping the link-subspace element field `0.2.k`. Since
`d₁ ≼ d₁` reflexively, `home(aᵢ) ∈ coverage(H₁)`, so `athome(aᵢ, H₁)` holds across the store
— the home-clause admits every link and `sat(a, q_H, Σ)` falls back to the from-clause:
`countlinks_FTT(q_H, Σ) = |{a₁, a₃}| = 2`, exactly as for `q`. The home bound selecting `d₁`
filters nothing, because the store is wholly homed at `d₁`; but the clause is genuinely
evaluated, true link by link, not silently dropped. In particular the orphan `a₃` is
admitted: its residence is read off the permanent address `a₃` and stands whether or not any
arrangement surfaces it — were `a₃`'s own entry in `d₁`'s arrangement removed
(reverse-orphaning it), `athome(a₃, H₁)` and hence this home-bounded count would not budge,
because the test consults `home(a₃)`, never `Σ.M`. This is CN-STAB's home-bounded instance
and CN-ORPHAN made concrete at once: residence is fixed by identity.

Bind the home-set to `d₂` instead and it bites. Let `H₂ = {⟨d₂⟩}`, coverage `{t : d₂ ≼ t}`,
and ask

  `q_H' = (H₂, F, ∗, ∗)`.

Now `athome(aᵢ, H₂)` demands `home(aᵢ) = d₁ ∈ {t : d₂ ≼ t}`, i.e. `d₂ ≼ d₁`; but `d₁` and
`d₂` are equal-length and diverge at the document component (`1` vs `2`), so neither
prefixes the other and the membership fails for every link. The home-clause is false across
the store, the AND drags every `sat` to `false`, and `countlinks_FTT(q_H', Σ) = 0`. This is
a genuine CN-ZERO, not a degenerate one: `coverage(H₂)` is the whole non-empty `d₂` subtree,
so the request is non-degenerate and the zero asserts *no addressable link is homed under
`d₂`* — not that the request named nothing (the empty-request zero of FL-EMP). Observe that
`a₄`, whose from-span points into `d₂` content, is excluded all the same: it is *homed* at
`d₁` and only *references* `d₂`, and the home-set tests where a link lives, never what it
points at (FL-RES, ASN-0121).

## Cost, and the meaning of asking for a number

We close with the cost and the meaning of asking for a *number* instead of the links
themselves.

About *meaning*, the answer is firm and abstract. A count of `N` asserts that exactly `N`
addressable links satisfy `q` at `Σ` — an existence-and-cardinality claim about the store.

> **CN-OBT (the count is an existence assertion, not a retrieval warranty).**
> `countlinks_FTT(q, Σ) = N` asserts that `|{a ∈ addressable(Σ) : sat(a, q, Σ)}| = N`. It
> does not assert that those `N` links are deliverable on demand. Delivery is a separate
> concern across a separate boundary (out of scope here), subject to availability the count
> never speaks to. The count promises *that `N` satisfying links exist in the store*, not
> *here are `N` handles you may fetch*.

Permanence makes the counted links obtainable *in principle* — their addresses are valid
forever (ASN-0093) — but obtainability *on demand* is a promise the count does not make and
must not be read as making. The number lives on the discovery side; carrying a per-item
retrieval guarantee across the delivery boundary would be a different and stronger claim.

About *cost*, the honest answer is a deliberate non-claim, and saying so is part of the
specification. One might hope that offering a count as its own service commits the design
to computing cardinality more cheaply than delivery — that "how many" should be answerable
without producing "which ones." This is a genuine and attractive design aspiration: a cheap
count is a planning primitive, letting a front end size a result before committing to the
expense of retrieving it. But it is *not* a correctness obligation, and we decline to
elevate it to a claim, because an alternative implementation that computes the cardinality
by materialising the satisfying set and taking its length is *correct as to value* — it
returns the same number CN-DEF specifies. The specification fixes *what* is computed (the
cardinality of the satisfying set), not *how much it costs*. Cost-asymmetry is a quality an
implementation may provide; it is not a property the answer must have, and so it is not
among the claims below.

*Implementation note.* Gregory's back end does *not* realise the asymmetry: it computes the
count by running the full matching search, materialising every match into a list, and
returning the list's length — so asking "how many?" costs what asking "which ones?" costs.
This is a faithful implementation of the *value* CN-DEF specifies and an unrealised
opportunity with respect to the *cost* aspiration. It confirms the position taken here: the
number is determined by the specification, the price is left to the implementation, and a
back end is free to pay full enumeration cost for a cardinality without being wrong.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| CN-DEF | (DEF) `countlinks_FTT(q, Σ) ≡ \|{ a : a ∈ addressable(Σ) ∧ sat(a, q, Σ) }\|`; the operation reads `Σ`, returns ℕ, and has frame `Σ` (writes nothing); defined through the shared relation `sat` (ASN-0121), not through the enumeration operation; well-defined because the counted set is a finite, computable subset of `dom(Σ.L)` (L-fin ASN-0093, FL-DEC ASN-0121) | introduced |
| CN-LOC | (LEMMA) Link-store locality — for fixed `q`, `countlinks_FTT(q, Σ)` is a function of `Σ.L` alone; `Σ.C`, `Σ.M`, `Σ.E`, `Σ.R` are never consulted (from FL-LOC, ASN-0121) | introduced |
| CN-UNIT | (THM) The unit is link identity — each addressable satisfying link contributes exactly `1`, independent of endset span/address multiplicity (absorbed by the existential in `touch`), transclusion multiplicity, arrangement-appearance multiplicity, and version-refraction multiplicity (the latter three excluded by CN-LOC; forking shares content (references the same I-addresses via J4's K.μ⁺ step, no K.α), not links — J4 ASN-0047 — so the version DAG adds no link address). Clause (b) is transclusion invariance: a link reachable through any number of documents contributes `1`, document-reach being an `Σ.M` quantity, not a link count | introduced |
| CN-SHARED | (META) The four-set match-description lives once in `sat` (ASN-0121); both the count and the enumeration are queries over `sat`, and neither operation's specification appeals to the other | introduced |
| CN-ENUM | (THM) `countlinks_FTT(q, Σ) = \|findlinks_FTT(q, Σ)\|` — count equals enumeration length at a single state, structurally (both are the cardinality of one set), and may differ across distinct states evaluated by separate inquiries | introduced |
| CN-ZERO | (THM) `countlinks_FTT(q, Σ) = 0 ⟺ (A a : a ∈ addressable(Σ) : ¬sat(a, q, Σ))` — a positive present-store existential (no addressable link satisfies `q`), distinct from "not found" (excluded by FL-JUNK) and "not displayed" (excluded by CN-LOC); a degenerate empty-coverage request also yields `0` (FL-EMP) but asserts only that the request names nothing | introduced |
| CN-SNAP | (THM) The count is a measurement of `Σ`, recomputed per inquiry, recorded in no state component; it may change under any mutation and the specification imposes no obligation that a prior count remain valid (recompute-on-read) | introduced |
| CN-STAB | (THM) For fixed `q`, any link-store-preserving transition (content insertion/deletion/rearrangement, content allocation, provenance recording — F-PRES ASN-0127) leaves the count invariant; in particular a reverse-orphaned link still contributes to a home-bounded count, residence being a projection of the permanent address | introduced |
| CN-RETRACT | (THM) A nullified link contributes `0` to every count immediately and permanently (R6a ASN-0086, FL-RET ASN-0121) while remaining in `dom(Σ.L)` with fixed value (L12 ASN-0043); the count ranges over the active view `addressable(Σ)`, reconciling immediate exclusion with store permanence | introduced |
| CN-MONO | (THM) Absent retraction of counted links, the count is non-decreasing across `Σ →* Σ'`, and creating a fresh ordinary link increments it by `1` iff that link satisfies `q` and is not already retraction-covered (`wp(create ℓ, Δcount = +1) = sat(ℓ, q, Σ') ∧ ¬(E (b, F', G') ∈ L_R^Σ :: ℓ ∈ coverage(G'))` — the FL-WP(a) conjunct of ASN-0121; automatic under the unit-depth retraction discipline, R0a ASN-0086, where it collapses to `sat(ℓ, q, Σ')`) | introduced |
| CN-ORPHAN | (THM) A satisfying addressable link is counted regardless of whether any arrangement surfaces it (`discoverable_from` irrelevant); the count is an existence census over `addressable(Σ)`, a superset of what any document surfaces, with the gap being exactly the orphans | introduced |
| CN-OBT | (THM) `countlinks_FTT(q, Σ) = N` asserts that `N` satisfying links exist in the addressable store at `Σ`; it does not warrant that those links are deliverable on demand | introduced |

## Open Questions

What invariant must connect a count phrased over content identity (address sets) to a count phrased over arrangement positions (V-specs), so that the two regimes agree exactly except where the resolving content has been wholly removed from every arrangement?

Under what concurrency discipline must two separate inquiries be evaluated for a count and a later enumeration of the same request to observe a single consistent state, so that count-equals-length holds across the pair and not merely within each?

Under what conditions may a count be cached and reported as a durable fact without violating its snapshot semantics — what must be true of the intervening transitions for a stored count to remain the cardinality of the present satisfying set?

What must the system guarantee for the reported number to remain the cardinality of distinct link identities when a single link's endsets are fragmented across non-contiguous address regions that the request overlaps?

What relationship, if any, must hold between the cost of counting and the cost of enumeration for a count to serve as a planning primitive, and is any such relationship a correctness obligation or only a quality of service?

What must a federated count guarantee across independently administered stores, so that a single four-set cardinality reflects links homed in stores other than the one receiving the inquiry rather than the satisfying set of one server's partial model?
