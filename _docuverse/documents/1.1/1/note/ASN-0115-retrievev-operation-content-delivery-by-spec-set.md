# ASN-0115: RETRIEVEV — Content Delivery by Spec-Set

*2026-06-04*

## The problem

Of all the operations in the protocol, Nelson singles out exactly one as
concerned with the delivery of actual content: "Of the 17 current commands in
XU.87.1, only one command (RETRIEVEV) is concerned with delivery of the actual
content fragments" (4/61), and that command "returns the material (text and
links) determined by `<spec set>`" (4/67). Every other span-taking command
returns *descriptions* of where content lives — document identities, extents,
link identities. RETRIEVEV alone crosses the line from naming to delivering.

We are asked a precise question. The system is handed a *spec-set* — an ordered
series of spans naming positions in one or more documents — and asked to deliver
the material those spans determine. What comes back? What relationship must the
returned material bear to the spec-set that named it, and to the arrangements
that bind those spans to content? What does delivering a whole spec-set *together*
disclose — about content shared by transclusion, and about spans that cross from
the text subspace into the link subspace — that delivering one span in isolation
would conceal? And what invariants govern the material the operation may return?

The discipline of specification forces us to be exact about each of these. We
shall find that "deliver the content" decomposes into a resolution step (map each
named V-position through the arrangement to a content address) and a fetch step
(read the immutable value at that address), and that the interesting content of
the operation lives in the boundary conditions: missing positions, shared
positions, cross-subspace positions, and the permanence of the store the bytes
are drawn from.

## The substrate we build on

We take the strand model as given. The *content store* `Σ.C : T ⇀ Val`
(ASN-0036) binds content addresses to values; it is append-only and immutable —
once `a ∈ dom(Σ.C)`, `a` persists and `Σ.C(a)` never changes (ASN-0036, S0
ContentImmutability; S1 StoreMonotonicity). The *link store* `Σ.L : T ⇀ Link`
(ASN-0043, ASN-0093) is likewise permanent (ASN-0043, L12 LinkImmutability). The
*arrangement* of a document `d` is a partial function `Σ.M(d) : T ⇀ T`
(ASN-0036) from V-positions to I-addresses; it is a genuine function (S2
ArrangementFunctionality) and, unlike the two stores, it is the one component
that may lose entries through editing (ASN-0047, P3 ArrangementMutabilityOnly).

A V-position carries its subspace in its first component, `subspace(v) = v₁`
(ASN-0036), with the fixed identifiers `s_C = 1` for content and `s_L = 2` for
links (ASN-0047, SubspaceConventionAxiom). Generalized referential integrity
fixes where each kind of position resolves: for `v ∈ dom(Σ.M(d))`,
`subspace(v) = s_C ⟹ Σ.M(d)(v) ∈ dom(Σ.C)` and
`subspace(v) = s_L ⟹ Σ.M(d)(v) ∈ dom(Σ.L)` (ASN-0047, S3★), and every active
V-position lies in one of these two subspaces (S3★-aux). Content and link stores
are disjoint (ASN-0093, SD).

A span `σ = (s, ℓ)` is well-formed when `Pos(ℓ)` and `actionPoint(ℓ) ≤ #s`
(ASN-0034, T12); its denotation is the half-open tumbler interval
`⟦σ⟧ = {t ∈ T : s ≤ t < s ⊕ ℓ}` (ASN-0053). We take spans to be level-uniform
(`#s = #ℓ`) so start, width, and reach share a length and any two endpoints are
T1-comparable at equal depth (ASN-0053, S6). Every content address has a
well-defined *origin* — the document-level prefix that allocated it,
`origin(a) = N(a).0.U(a).0.D(a)` — and origin distinguishes content created by
distinct documents while identifying transcluded content as one (ASN-0036, S4
OriginBasedIdentity; S7 StructuralAttribution).

## What a spec-set is, and what delivery is

A *V-spec* is a pair `ρ = (d, σ)` naming an **allocated** document `d` — a
tumbler with `zeros(d) = 2` (ASN-0045) that is present in the arrangement family,
`d ∈ dom(Σ.M)` — and a well-formed, level-uniform, **ordinal-level** span
`σ = (s, ℓ)` whose start `s` is a *well-formed V-position*: a zero-free tumbler of
depth at least 2 with positive components,
`zeros(s) = 0 ∧ #s ≥ 2 ∧ (A i : 1 ≤ i ≤ #s : sᵢ > 0)`. This is the shape
ASN-0036's S8a requires of every *bound* position; we impose it here directly as a
constraint on the span's start, whether or not that start is itself bound. The
direct imposition is necessary: S8a is an invariant restricted to the active domain
`dom(Σ.M(d))`, and R6 below contemplates named starts absent from the arrangement,
so the shape cannot be borrowed from S8a's domain-restricted guarantee — `#s ≥ 2`
is a property of the V-position *shape*, required of the spec. Ordinal-level means
the width acts at the deepest component, `actionPoint(ℓ) = #ℓ` (ASN-0082,
OrdinalLevel). Combined with level-uniformity (`#ℓ = #s`) and the start depth
`#s ≥ 2`, this forces `actionPoint(ℓ) ≥ 2`, so both endpoints `s` and `s ⊕ ℓ`
agree on position 1. The endpoint agreement extends to the whole interval by
ContiguousSubtrees (ASN-0034, T5): taking prefix `p = [s₁]`, we have `p ≼ s` and
`p ≼ s ⊕ ℓ`, so for any `t ∈ ⟦σ⟧` — i.e. `s ≤ t < s ⊕ ℓ`, hence `s ≤ t ≤ s ⊕ ℓ` —
T5 gives `p ≼ t`. Thus every `t ∈ ⟦σ⟧` has first component `s₁`, and the span's
interval cannot cross the subspace boundary. This is
the deepest-action-point discipline R10 relies on; without it, a merely
level-uniform well-formed span may have `actionPoint(ℓ) = 1` and straddle from
the content subspace into the link subspace (e.g. `s = [1,5]`, `ℓ = [2,0]`:
`s ⊕ ℓ = [3,0]`, and `[2,3] ∈ ⟦σ⟧` has `subspace = s_L`). A single
boundary-crossing span is therefore outside this ASN, deferred to the Open
Questions; designating both subspaces together is achieved by *composing*
per-subspace ordinal spans into the spec-set, not by one straddling span. The
allocation precondition `d ∈ dom(Σ.M)` is what makes the
arrangement `Σ.M(d)` — and hence `act`, `item`, `deliver₁`, and `deliver` below —
well-defined; it is the same precondition the substrate's `project` carries
("defined when `d ∈ dom(Σ.M)`", ASN-0098). It is a precondition on the *existence*
of the named arrangement, and is therefore distinct from R6's silent-gap case,
which concerns the *absence of a binding* for a named position *within* an
arrangement that does exist. A *spec-set* is a finite **ordered** sequence
`R = ⟨ρ₁, …, ρₚ⟩` of V-specs, `p ≥ 0`. The ordering is part of the request:
Nelson's caution that "if you want to designate a separated series of items
exactly, including nothing else, you do this by a span-set, which is a series of
spans" (4/25) tells us a spec-set is a *sequence*, not a set — its order carries
meaning, and it designates content *exactly*.

For a V-spec `ρ = (d, σ)` we define its *active positions* at state `Σ`:

> `act(ρ, Σ) = dom(Σ.M(d)) ∩ ⟦σ⟧`

— the V-positions the span names that the document's arrangement actually binds.
Silent filtering is built into this definition: a named position that the
arrangement does not bind simply is not in `act`. The set `act(ρ, Σ)` is finite
because it is a subset of `dom(Σ.M(d))`, which is finite (ASN-0036, S8-fin); it is
totally ordered because it is a subset of the totally ordered carrier `T`
(ASN-0034, T1). Finiteness and total order together give it a unique ascending
enumeration `v₁ < v₂ < … < v_{k}` where `k = |act(ρ, Σ)|`.

Each active position is resolved through the arrangement to a single address
`a = Σ.M(d)(v)` (well-defined and single-valued by S2), and the *delivery item*
for `v` is determined by the position's subspace:

> `item(v, ρ, Σ) =`
> `  ⟨content, Σ.C(a)⟩`   if `subspace(v) = s_C`   (then `a ∈ dom(Σ.C)` by S3★)
> `  ⟨ref, a⟩`            if `subspace(v) = s_L`   (then `a ∈ dom(Σ.L)` by S3★)

We may write `item` without case in what follows; the two cases are
distinguished by tag. The *per-spec delivery* is the ascending-V sequence
`deliver₁(ρ, Σ) = ⟨item(v₁, ρ, Σ), …, item(v_k, ρ, Σ)⟩`, and the **delivery** of
the whole spec-set is the concatenation in spec-set order:

> `deliver(R, Σ) = deliver₁(ρ₁, Σ) ⌢ deliver₁(ρ₂, Σ) ⌢ … ⌢ deliver₁(ρₚ, Σ)`     (R0)

Everything that follows is an analysis of this object. We name `deliver` as R0;
the named claims R1–R11 record the invariants any faithful realization must
satisfy.

## Delivery returns material, not location

The first thing to settle is *what kind of thing* comes back. The contrast
Nelson draws is sharp: FINDDOCSCONTAINING "returns a list of all documents
containing any of the material … regardless of where the native copies are
located" (4/63) — locations; RETRIEVEDOCVSPAN "returns a span determining the
origin and extent" (4/68) — an address; only RETRIEVEV "returns the material"
(4/67). The span-set is the *name* of what is wanted; RETRIEVEV is what turns
that name into delivered material.

In our model this is exactly the form of `item`: for a content position the
delivered item carries `Σ.C(a)` — the value, not the address `a`; for a link
position it carries a reference to the link entity. The operation resolves the
arrangement and dereferences the content store; it does not return the V-to-I
mapping, nor the I-addresses, as its payload.

> **R1 (MaterialDelivery).** For every active content position, the delivered
> item carries the bound content value `Σ.C(Σ.M(d)(v))`, not a description of
> where that value is stored.

This is the property that distinguishes RETRIEVEV from every other span-taking
command, and any alternative implementation of "deliver the content of a
spec-set" must satisfy it. Gregory's two-phase realization — `specset2ispanset`
(resolve each V-spec through the document's arrangement to I-addresses) followed
by `ispanset2vstuffset` (fetch the bytes from the granfilade by I-address) —
is one mechanization of R0/R1; an alternative back end with a different index
structure would still owe the same two-phase semantics. We note that the link
path (`vspanset2sporglset`, which annotates I-addresses with source-document
provenance for link operations) is *not* on the content-delivery path: content
delivery needs no such annotation, because it delivers the value itself.

## Faithfulness, and where the invariant stops

What relationship must the delivered value bear to the content the span names? It
must be the content itself — no character altered, fabricated, or dropped.

> **R2 (Faithfulness).** Every delivered content item equals the value bound, in
> the content store, to the address the arrangement assigns its position:
> `item(v, ρ, Σ).val = Σ.C(Σ.M(d)(v))`. No other value may be substituted.

The justification is structural, and it is worth seeing exactly which invariants
carry it. Resolution is deterministic because `Σ.M(d)` is a function (S2). The
value at the resolved address is fixed for all time because `Σ.C` is immutable
(S0): the byte at an I-address never changes after creation. A span names an
I-address by way of the arrangement; the arrangement may be re-edited, but the
*content* the resolved address denotes is permanent. This is precisely the
storage-layer invariant Nelson's design rests on — content lives permanently at
its address, and "you always know where you are, and can at once ascertain the
home document of any specific word or character" (2/40).

We must be equally precise about where this invariant *stops*. Faithfulness is a
property of *what the operation is defined to return* — it is a semantic
guarantee about resolution and dereference, not a guarantee about a transmission
channel. Nelson disclaims the latter explicitly: storage and "attempts to
deliver such material, are at User's risk" (5/18), with "no guarantee as to the
correctness or authenticity" (5/18) of the channel. So R2 governs the
denotation of `deliver`; it does not promise that an intervening wire delivers
those bytes intact. This is a *frame limit*, not a claim: the abstract
specification asserts faithfulness of the delivered material as a function of
state, and asserts nothing about the medium.

## Exactness and arrangement-relativity

Must the delivered material correspond span-for-span to the spec-set — nothing
extra, nothing requested-and-present silently omitted? Yes, and the two halves
are visible directly in R0.

> **R3 (SpecSetExactness).** The delivery contains an item for *exactly* the
> active positions of each span, and no others: every item arises from some
> `v ∈ ⟦σⱼ⟧ ∩ dom(Σ.M(dⱼ))` (nothing extra — every delivered item is named by a
> span), and every such `v` contributes an item (nothing present-and-named is
> omitted).

The upper bound holds because `act(ρ, Σ) ⊆ ⟦σ⟧`: the half-open interval is the
exact extent the span designates, and "there is no choice as to what lies
between; this is implicit in the choice of first and last point" (4/25). The
lower bound holds because `act` includes *all* of `⟦σ⟧ ∩ dom(Σ.M(d))`. We stress
that the span width `ℓ` is a tumbler boundary, not a count — "a tumbler-span …
does not designate the number of bytes contained" (Nelson, 4/25; ASN-0034) — so
the delivered quantity equals `|act(ρ, Σ)|`, the number of *bound* positions in
the interval, which equals the nominal extent only when no position in the
interval is unbound. Where a requested boundary falls between stored positions,
an implementation must clip to the interval exactly (Gregory's `whereoncrum`
classification and `context2vtext` boundary clip realize this); the clip changes
no abstract content, it merely realizes the half-open interval precisely.

Against *which* arrangement is the resolution performed? Against the one named.

> **R4 (ArrangementRelativity).** Each V-spec `(dⱼ, σⱼ)` is resolved through the
> arrangement `Σ.M(dⱼ)` of the document it names — and through no other. The
> delivered material reflects exactly what the named arrangement binds those
> spans to.

This answers the apparent dilemma between "the content each span *currently*
designates" and "content as it stood at some version." In Xanadu the dilemma
largely dissolves, because the version is encoded in the document tumbler — "the
Document field of the tumbler may be continually subdivided, with new subfields …
indicating daughter documents and versions" (4/29), and distinct versions are
distinct document tumblers with distinct arrangements (ASN-0036, S7d). Naming
`dⱼ` *is* naming the version; there is no privileged "basic" version the system
could silently substitute — "there is thus no 'basic' version of a document set
apart from other versions" (2/19). Current and as-it-stood coincide because the
binding consulted is the one the address selects.

## Order and boundaries

In what order does the material arrive, and what governs the boundary between one
position's contribution and the next?

> **R5 (OrderFidelity).** Across V-specs, delivery follows spec-set sequence
> order: the items of `ρᵢ` wholly precede the items of `ρⱼ` whenever `i < j`,
> irrespective of the relative V-magnitudes of the two specs. Within a single
> V-spec, items are delivered in ascending T1 order of their V-positions. Each
> item's extent is fixed by its position; the boundary between consecutive items
> is implicit in the spec-set structure and the span endpoints, with nothing
> interpolated between them.

The cross-spec half is the substantive commitment: a later spec naming
numerically smaller V-positions is *not* re-sorted ahead of an earlier spec
naming larger ones. Concatenation in R0 is by sequence index `j`, not by
V-magnitude. Gregory's implementation confirms exactly this stratification —
within one V-spec the contexts are V-sorted (`incontextlistnd`), but across
V-specs the per-spec results are appended in spec-set order with no global
re-sort. An alternative implementation that globally V-sorted a multi-spec
request would deliver a *different* object and violate R5.

## Partial delivery: the gap is legal, not an error

What if part of the spec-set names content that no longer exists in the named
arrangement, or was never established there? The architecture answers: deliver
what can be delivered, signal the gap by absence, and never fail the whole.

> **R6 (SilentGapFiltering).** A named position with no binding in the consulted
> arrangement — `v ∈ ⟦σⱼ⟧ \ dom(Σ.M(dⱼ))` — contributes nothing to the delivery
> and causes no failure. Delivery succeeds and returns the items for the bound
> positions; the unbound region is represented by its absence.

This is forced by the model: `act(ρ, Σ)` is an intersection, so an unbound
position is simply not enumerated. It is also forced by Nelson's design intent. A
span addresses a *range*, and "a span that contains nothing today may at a later
time contain a million documents" (4/25) — an empty or partly-empty range is an
anticipated, legal state, not a fault. The same architecture governs the only
place Nelson states an explicit rule about unsatisfiable request parts: "THE
QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON
OTHERS" (4/60) — serve the satisfiable part, drop the rest, never fail the whole.
Gregory's resolution chain bears this out: an unresolvable V-range produces an
empty I-span set and a successful, empty contribution — indistinguishable from a
legitimately empty region. The gap is signalled *structurally* (the caller
compares what it asked for against what arrived), not by an error code.

Note the boundary R6 does *not* cover: failure of an open-document precondition
is a different matter from an unbound position within an open document. R6 is
about absence of binding, not about authorization or existence of the document
entity. An implementation may legitimately refuse a request that names a document
it cannot consult; what it may not do is fail a request merely because some named
positions within a consultable arrangement are unbound.

## Repeatability

If the same spec-set is asked again, against unchanged arrangements, must the
delivered material be identical?

> **R7 (Repeatability).** Let `Σ`, `Σ'` be two states of one evolving docuverse
> with one a reachability descendant of the other along the sequential transition
> order — without loss of generality `Σ →* Σ'` (ASN-0047,
> SequentialTransitionAxiom) — for which the consulted arrangement restrictions
> agree, `Σ.M(dⱼ)|⟦σⱼ⟧ = Σ'.M(dⱼ)|⟦σⱼ⟧` for every `j`. Then
> `deliver(R, Σ) = deliver(R, Σ')`.

The proof is short and exposes which input is the variable one. `deliver` is a
function of two things: the consulted arrangement restrictions, and the stores
the resolved values are drawn from. The restrictions are equal by hypothesis, so
`act` and the resolved addresses agree position-for-position. Fix any resolved
address `a`. Because the consulted restriction binds `a` at both states, S3★
places `a` in the appropriate store at each: `a ∈ dom(Σ.C) ∩ dom(Σ'.C)` for a
content position, `a ∈ dom(Σ.L) ∩ dom(Σ'.L)` for a link position. The hypothesis
gives `Σ →* Σ'` directly: the two states are comparable under the sequential
transition order, not merely reachable from a shared ancestor — divergent branches
of the reachability relation would not be comparable, and across them a freshly
allocated address could carry different values, so comparability is required, not
derived. Over the intervening transitions `Σ →* Σ'`, content immutability (S0) and
link immutability (L12) hold the stored entry fixed, giving `Σ.C(a) = Σ'.C(a)`
(resp. `Σ.L(a) = Σ'.L(a)`). The labelling of the two states is immaterial —
value-equality is symmetric — so naming the descendant `Σ'` costs no generality. Hence for every resolved address the delivered value or reference is
the same at both states, and the two deliveries are identical. The only mutable input to a
content delivery is the arrangement; this is exactly why repeatability is
conditioned on "unchanged arrangements" and on nothing else. Editing produces a
*new* version (a new document tumbler with its own arrangement) rather than
mutating an existing one, so "the same spec-set against the same version" is
always a well-defined, reproducible request — the foundation of permanent
citation: "any address … may be specified by a permanent tumbler address" (4/19).

## What co-delivery reveals: transclusion

Now the question that makes delivering a *whole spec-set* more than the sum of
delivering its spans one at a time. Suppose two positions in the request — in the
same spec or different specs — resolve to the same content address `a`. This is
transclusion: the same content, included by reference in two places, carrying one
permanent I-address wherever it appears (ASN-0036, S5 UnrestrictedSharing).

> **R8 (TransclusionRevelation).** If two active positions `v, v'` (within one
> spec or across specs) satisfy `Σ.M(d)(v) = Σ.M(d')(v') = a`, then the two
> positions share a single subspace: by S3★ the shared address `a` lies in
> `dom(Σ.C)` or in `dom(Σ.L)` but, by store disjointness (SD), not both, and that
> store membership fixes `subspace(v) = subspace(v')`. In the **content sub-case**
> (`subspace(v) = s_C`, `a ∈ dom(Σ.C)`): (i) the two delivered items carry the
> identical value `Σ.C(a)`, by R2; (ii) both items are resolved *through* the one
> shared address `a` — identity-preserving co-resolution — never fabricating two
> independent origins, so `origin(a)` of both is one and the same (S4, S7); and
> (iii) the operation performs no deduplication: each position yields its own item,
> so the shared content appears once per V-position. In the **link sub-case**
> (`subspace(v) = s_L`, `a ∈ dom(Σ.L)`): the two delivered items are the identical
> reference `⟨ref, a⟩` (R10), again resolved through the one shared address, with
> common provenance `home(a)` (ASN-0043, L1a); no deduplication, by the same
> exactness argument as (iii).

Three points deserve emphasis. First, *identity is structural, not incidental*.
Content identity in Xanadu is by creation, not by value: two independently
created identical strings get distinct addresses, while transcluded content
shares one address (S4). So delivering both positions by way of the same `a` is
identity-preserving by construction — it is reference, not copy, and "any
detached copy someone keeps is frozen and dead" precisely because copying severs
this. The operation *may not* return the two as genuinely unrelated content,
because it never copies; it dereferences the same address twice.

Second, *this is what single-span delivery conceals*. Delivered alone, each
position arrives as a self-contained fragment; the *relation between* the two —
their shared home `a` — is established only when both are resolved within one
request, where their common resolution is exhibited. Nelson promises the system
"will also reveal and clarify commonalities between documents and among versions"
(3/4); co-delivery is the locus where that commonality is made manifest, because
only co-resolution puts the two shared addresses side by side.

Third, *no merge*. The two items are not collapsed into one. This is forced
abstractly — two distinct V-positions are two distinct entries, and a delivery
that dropped one would violate R3 (it would silently omit a named, bound
position). It is also exactly Gregory's behavior: the consolidation step that
would merge co-referent spans is absent (the `consolidatespans` call is
commented out), so identical bytes are delivered once per V-position. An
alternative implementation is *required* to deliver both, by R3 — the absence of
deduplication is not an implementation accident but a consequence of exactness.

*Worked instance.* Let document `d` transclude one stretch of content twice: V-positions `u`
and `w` (with `u < w`, both in subspace `s_C`) both map to the same content
address `a`, i.e. `Σ.M(d)(u) = Σ.M(d)(w) = a`. Take the spec-set
`R = ⟨(d, σ_w), (d, σ_u)⟩` whose first spec names `w` and whose second names `u`.
Then `deliver(R, Σ) = ⟨⟨content, Σ.C(a)⟩, ⟨content, Σ.C(a)⟩⟩`: two items, the
*same* value both times (R8.i), in the order the specs were given — `w` before
`u`, against V-magnitude (R5) — with neither dropped (R8.iii). The two
appearances are ascertainably one content because both resolved through the
single address `a`.

## What co-delivery reveals: coherent multi-origin assembly

A single spec-set may gather spans whose content was created in different
documents. What must delivery guarantee about presenting that material?

> **R9 (CoherentMultiOriginAssembly).** A spec-set drawing on multiple origins is
> delivered as one ordered sequence (R5), assembled by resolving each spec
> against its own document's arrangement independently (R4). The *resolution* is
> provenance-traceable: each active position `v` resolves to `a = Σ.M(d)(v)`, and
> that address determines a home document — for a content position
> (`subspace(v) = s_C`, `a ∈ dom(Σ.C)`) the document-level prefix `origin(a)` (S7);
> for a link position (`subspace(v) = s_L`, `a ∈ dom(Σ.L)`) the link's home
> `home(a)` (ASN-0043, L1a), which coincides with `origin` on link addresses
> (ASN-0086, HomeOriginCoincidence) — so no fragment's provenance is collapsed by
> co-assembly. Whether that origin travels
> *inside* the delivered material or is recoverable only through the resolution
> mapping is a separate question (the delivered content item carries `Σ.C(a)`, not
> `a`, by R1); R9 asserts traceability of the resolution, not inline provenance of
> the delivered stream.

Two obligations hold simultaneously, and they pull in opposite directions. The
material must be *coherent* — one ordered stream the caller reads as a single
delivery, with fragments slotted in spec-set order regardless of where they
physically originate ("the virtual byte stream of a document may include bytes
from any other document," 4/10; non-native bytes have "an ordinal position …
just as if they were native," 4/11). And the *resolution* must remain
*traceable* — co-assembly must not collapse distinct origins into an anonymous
blob, because each active position resolves to a definite address whose home
document is determinate — `origin(a)` for a content address (S7), `home(a)` for a
link address (ASN-0043, L1a; coinciding with origin by ASN-0086,
HomeOriginCoincidence) — so the home document of every assembled fragment is
recoverable from the resolution mapping. Losing the first gives disconnected
fragments; losing the second gives an unattributable assembly. RETRIEVEV must
give one coherent delivery *and* a resolution whose origins stay determinate.
Because each spec is resolved against its own
arrangement (R4), cross-document spec-sets are resolved per document and then
concatenated — Gregory's `specset2ispanset` loop calls the per-document lookup
once per spec, reading each document's arrangement in isolation, exactly the
independence R9 requires.

## What co-delivery reveals: subspace crossing

The last revelation. A document's arrangement maps positions in two subspaces:
content (`s_C`) and links (`s_L`). A spec-set with specs in both subspaces
gathers positions of both kinds. (Whether a *single* span's denotation can itself
straddle the boundary — and what delivery must then guarantee — we leave to the
Open Questions; the V-spec definition restricts `σ` to ordinal-level spans, for
which `actionPoint(ℓ) ≥ 2`, so a text-rooted span cannot reach link positions:
both endpoints `s` and `s ⊕ ℓ` agree on position 1 = `s_C`, so by ContiguousSubtrees
(ASN-0034, T5) with prefix `[s_C]` every `t ∈ ⟦σ⟧` has first component `s_C`.)

> **R10 (SubspaceCrossingObservability).** When an active position lies in the
> link subspace (`subspace(v) = s_L`), it resolves (by S3★) to a link address
> `a ∈ dom(Σ.L)`, and the delivered item is a *reference* to that link entity —
> an item distinguishable in kind from a content-value item. A spec-set spanning
> both subspaces therefore yields a heterogeneous delivery in which the subspace
> boundary is observable as a change of item kind. A span confined to the text
> subspace never exposes link-subspace material.

This is the abstract content of "delivery is not restricted to the text
subspace." The arrangement is a single map over both subspaces; resolution
follows it wherever the named positions lead. For a content position the item
carries a value; for a link position the item carries the link's address — *not*
the link's endset structure, which is the concern of operations that read a link
by address (out of scope here). The crossing is *observable* precisely because
the two item kinds differ: co-delivery of a both-subspace spec-set exhibits the
boundary that a single text-subspace span could never reveal. Gregory's
realization discriminates exactly this way — a resolved position whose stored
crum is content yields a text item, one whose crum is a link-organizer yields an
address item — so the wire stream carries content fragments and link-address
references intermixed, with the boundary visible in the tagging. We record as an
out-of-band hazard, not an abstract claim, that an implementation which lets a
caller inject already-resolved I-addresses *bypassing* the arrangement (and thus
bypassing S3★'s subspace discipline) can dereference a link address as if it were
content and deliver meaningless bytes; the abstract precondition that positions
are resolved *through* the arrangement is exactly what rules this out.

## What governs the material: permanence of the source

Finally, what invariant governs the addresses the bytes are drawn from?

> **R11 (PermanentSourcing).** Delivery sources every content item from the
> immutable content store by I-address. Consequently a content address that has
> ever entered `dom(Σ.C)` remains deliverable for all time: if any arrangement —
> the document's own, a later version's, or a transcluding document's — binds
> some V-position to `a`, then a spec over that document resolves to `a` and
> delivers `Σ.C(a)`, even if the originally-creating document's *current*
> arrangement no longer references `a`.

Here is the decisive distinction between *deletion* and *removal of content*.
"Deletion" in Xanadu is contraction of an arrangement — the V-to-I binding leaves
`Σ.M(d)`; the bytes do not leave `Σ.C`, which is append-only and immutable
(S0, S1). The content becomes *orphaned* relative to the contracting document
(unreachable through *that* document's current arrangement) but is not absent
from the store. So deliverability turns on exactly two conditions, and we can
read them off as a weakest precondition: for the delivery of a spec to include
the value at `a`, it suffices that (i) the consulted arrangement binds some named
position to `a`, and (ii) `a ∈ dom(Σ.C)`. Immutability discharges (ii) the
instant `a` is created and forever after; (i) is the live reference. A version
created before a deletion still binds the address, and so still delivers the
content — which is what makes identity-preserving restoration possible at all,
and what makes "any portion of any version (historical or alternative)" (2/19)
retrievable. Gregory's content fetch confirms the asymmetry: the granfilade
lookup is by I-address with no liveness check; whatever was committed at an
address is returned whenever an arrangement resolves to it.

## Synthesis

RETRIEVEV is, abstractly, *resolution followed by faithful dereference, in
order*. Given a spec-set, it delivers the material the spans determine (R1):
each named, bound V-position is resolved through its own document's arrangement
(R4) to an address, and the immutable value at that address is delivered
faithfully (R2), confined exactly to the named positions (R3), in spec-set order
across specs and ascending V-order within (R5). Named positions with no binding
are filtered silently and never fail the request (R6); against unchanged
arrangements the result is bit-for-bit repeatable (R7), because the arrangement
is the only mutable input and the stores never alter what they hold.

Delivering a whole spec-set together is more than delivering its spans
separately. Co-resolution reveals transclusion — positions sharing an address
deliver identical, shared-origin material with no deduplication (R8); it
assembles multi-origin material into one coherent, still-traceable stream (R9);
and it makes the text/link subspace boundary observable as a change in item kind
(R10). Underneath all of it, the store is permanent: orphaned-but-referenced
content remains deliverable for all time (R11). Each of R1–R11 is an obligation
any faithful realization must meet; the one implementation we have evidence for
meets them, with its two-phase resolve-then-fetch structure realizing R0 and its
absent consolidation step realizing the no-deduplication corollary of R3 and R8.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| R0 | `deliver(R, Σ)` = per-spec deliveries concatenated in spec-set order; `deliver₁(ρ,Σ)` = items of `act(ρ,Σ) = dom(Σ.M(d)) ∩ ⟦σ⟧` in ascending T1 order; `item` carries `Σ.C(a)` for content positions, the reference `a` for link positions | introduced |
| R1 | MaterialDelivery: a content item carries the bound value `Σ.C(Σ.M(d)(v))`, not a description of its location | introduced |
| R2 | Faithfulness: every content item equals `Σ.C(Σ.M(d)(v))` (from S2 + S0); no value may be substituted. Frame limit: this governs the denotation of delivery, not any transmission channel | introduced |
| R3 | SpecSetExactness: items arise for exactly `⟦σⱼ⟧ ∩ dom(Σ.M(dⱼ))` — nothing outside the spans, nothing named-and-bound omitted | introduced |
| R4 | ArrangementRelativity: each V-spec is resolved through `Σ.M(dⱼ)` alone; the version named by `dⱼ` fixes the binding, so current and as-it-stood coincide | introduced |
| R5 | OrderFidelity: spec-set sequence order across specs (no global V re-sort); ascending V-order within a spec; boundaries implicit in spans | introduced |
| R6 | SilentGapFiltering: a named position unbound in the consulted arrangement contributes nothing and causes no failure; the gap is signalled by absence | introduced |
| R7 | Repeatability: equal consulted arrangement restrictions ⟹ identical delivery; the arrangement is the sole mutable input | introduced |
| R8 | TransclusionRevelation: positions sharing a resolved address deliver identical material via identity-preserving co-resolution through the one shared address, with no deduplication (one item per V-position) | introduced |
| R9 | CoherentMultiOriginAssembly: multi-origin spec-sets deliver as one ordered stream, resolved per document; the resolution is provenance-traceable (each active position's `Σ.M(d)(v)` has determinate home document — `origin(a)` for content (S7), `home(a)` for links (L1a, HomeOriginCoincidence)), not asserting inline provenance in the delivered material | introduced |
| R10 | SubspaceCrossingObservability: link-subspace positions resolve (S3★) to link addresses and deliver as references — kind-distinct from content items — making the subspace crossing observable | introduced |
| R11 | PermanentSourcing: content is sourced from the immutable store by I-address; an address ever in `dom(Σ.C)` remains deliverable whenever any arrangement binds a position to it, including orphaned-but-referenced content | introduced |

## Open Questions

What must content delivery guarantee about inline provenance — must a delivered fragment carry, within the delivered material itself, enough to ascertain its origin, or may origin be recoverable only by a separate query?

Under what conditions, if any, may a content-delivery operation be permitted to fail outright rather than deliver partially?

What invariant must govern delivery when a spec-set's resolved references include an address with no entity bound in either store?

What faithfulness, if any, may be required of the delivery channel itself, given that the storage-layer faithfulness invariant does not extend to transmission?

What must delivery guarantee when a single span's denotation straddles the subspace boundary, so that one contiguous named range yields both content items and link-reference items?
