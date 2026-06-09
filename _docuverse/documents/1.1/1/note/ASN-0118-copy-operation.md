# ASN-0118: The COPY Operation — Transclusion as Shared Reference

*2026-06-08*

## The problem

Nelson draws one line through the whole architecture and asks us never to cross
it: "inclusion by reference, not copy." When content already living in the
docuverse is placed into a new document, the system must reuse the *identity* of
that content rather than manufacture a second copy of it. The operation that
performs this placement is COPY, and Nelson calls its effect *transclusion*.

We are asked to be exact about what that means. The system is handed a *spec-set*
— an ordered series of spans naming content in one or more existing documents —
together with a destination document and a V-position within it. COPY places the
named material at that position. The question is a question about *boundaries*:
what is reused from the existing content store and what is recorded fresh in the
destination; what relationship the placed material must bear to its source's
identity, to the destination's prior arrangement, and to any other document that
already shares those addresses; what assembling content from several
non-contiguous sources discloses about shared identity, ownership independence,
and the line between reuse and replication; and what invariants COPY must
preserve about content immutability, the permanence of the source's identity
inside the destination, the survival of links anchored to the reused content, and
the isolation of the source from the act of being copied from.

We shall find that "place content by reference" decomposes into a *resolution*
step (read the spec-set through its source arrangements to recover a sequence of
content addresses) and a *placement* step (bind those very addresses to fresh
V-positions in the destination), and that the entire content of the operation —
the thing that makes it transclusion rather than copying — is one frame
condition: **the content store does not grow.** Every other property follows from
that, from the permanence of the address space, and from the fact that the
destination owns its arrangement but not the content it arranges.

## The substrate we build on

**Standing precondition (reachability).** Throughout, every state `Σ` ranges over
states reachable from the initial state `Σ₀` under the sequential transition order
(ASN-0047, SequentialTransitionAxiom). This is what licenses the per-state
invariant citations below — S0/S1 (content permanence), S2/S3★ (arrangement
functionality and referential integrity), S7 (structural attribution), S8-fin and
D-SEQ (finite, contiguous, sequential arrangements), L12 (link permanence) — each
of which ASN-0047 collects in `ExtendedReachableStateInvariants` and guarantees
only of reachable states. At a non-reachable state these may fail, and so the
scoping is load-bearing, not decorative; the project's foundation ASNs scope the
same way (ASN-0086, ASN-0098).

We take the strand model as given. The *content store* `Σ.C : T ⇀ Val`
(ASN-0036) binds content addresses — *I-addresses* — to values. It is append-only
and immutable: once `a ∈ dom(Σ.C)`, `a` persists and `Σ.C(a)` never changes
(ASN-0036, S0 ContentImmutability; S1 StoreMonotonicity). The *arrangement* of a
document `d` is a partial function `Σ.M(d) : T ⇀ T` (ASN-0036) from V-positions to
I-addresses; it is a genuine function (S2 ArrangementFunctionality) whose every
image lies in the content store (S3 ReferentialIntegrity), and it is the one
component of state that may be edited in place. The *link store* `Σ.L : T ⇀ Link`
(ASN-0043, ASN-0093) is permanent (L12 LinkImmutability). A document records,
besides its arrangement, a *provenance* relation `Σ.R ⊆ T × T` (ASN-0047): a pair
`(a, d)` records that document `d` has referenced I-address `a`.

We write `V_S(d) = {v ∈ dom(Σ.M(d)) : subspace(v) = S}` for the V-positions of
document `d` in subspace `S`, where `subspace(v) = v₁` (ASN-0036). The text
subspace is `s_C` and the link subspace `s_L` (ASN-0047, SubspaceConventionAxiom);
this ASN concerns transclusion of *content*, so its placements land in `s_C`. We
use the ordinal-shift abbreviation `t + k ≡ shift(t, k)` for a tumbler `t` and
natural `k`, with `t + 0 = t` (ASN-0034, OrdinalShift; ASN-0058,
OrdinalShiftBase). For an I-address `a ∈ dom(Σ.C)`, `origin(a) = N(a).0.U(a).0.D(a)`
is the document-level prefix recovered from the address by field projection
(ASN-0036, S7); it is the tumbler of the document that allocated `a`, and it is
invariant across every state in which `a` is stored (S7(d)).

## What a spec-set names, and what resolution recovers

A *V-spec* is a pair `ρ = (d_s, σ)` naming an allocated source document
`d_s ∈ dom(Σ.M)` and a well-formed, level-uniform, ordinal-level span `σ` whose
start is a well-formed V-position, exactly as ASN-0115 fixes for RETRIEVEV; we
adopt that definition unchanged. A *spec-set* is a finite ordered sequence
`R = ⟨ρ₁, …, ρₚ⟩` of V-specs (`p ≥ 0`). The ordering is part of the request —
Nelson is explicit that "if you want to designate a separated series of items
exactly, including nothing else, you do this by a span-set, which is a series of
spans" (4/25): a spec-set is a *sequence*, not a set, and it designates content
*exactly*.

The *active positions* of a V-spec are those the span names and the source
arrangement actually binds, `act(ρ, Σ) = dom(Σ.M(d_s)) ∩ ⟦σ⟧` (ASN-0115). This
set is finite (subset of the finite `dom(Σ.M(d_s))`, S8-fin) and totally ordered
(subset of the totally ordered carrier `T`, T1), hence has a unique ascending
enumeration `v₁ < … < v_k`. We restrict attention to *content* spec-sets: every
active position is in the text subspace, `subspace(vⱼ) = s_C`, so by referential
integrity (S3★) each resolves to a content address `Σ.M(d_s)(vⱼ) ∈ dom(Σ.C)`.

We define **resolution** as the ordered sequence of I-addresses obtained by
reading each active position through its source arrangement and concatenating in
spec-set order:

> `resolve(R, Σ) = ⟨ Σ.M(d₁)(v) : v ∈ act(ρ₁,Σ) ascending ⟩ ⌢ … ⌢ ⟨ Σ.M(dₚ)(v) : v ∈ act(ρₚ,Σ) ascending ⟩`     (CP0)

Write `resolve(R, Σ) = ⟨c₀, c₁, …, c_{W−1}⟩`, with `W = |resolve(R,Σ)|` the total
count of resolved addresses. Three facts about this object are immediate, and we
record them as the *resolution integrity* claim CP0:

- **(a) Every resolved address already exists.** `cᵢ ∈ dom(Σ.C)` for `0 ≤ i < W`,
  by S3★ applied at each active position. *Nothing named by the spec-set is
  invented; it is all found.* This is the precondition that the placement to come
  will require, and it is met by the source arrangements alone.
- **(b) Resolution is a pure read.** `resolve` is a function of `Σ`; it modifies no
  component — not `Σ.C`, not any `Σ.M(d)`, not `Σ.L`, not `Σ.R`. The source
  document is consulted, never altered, by the act of resolving a spec-set against
  it. This is the seed of source isolation (CP6 below).
- **(c) Non-contiguity survives resolution.** When a single V-span covers content
  that the source itself assembled from several disjoint I-regions, the ascending
  positions `v₁ < … < v_k` resolve to addresses that are *not* one contiguous run:
  `resolve` returns each region's addresses in turn, so the resolved sequence
  records as many distinct origins as the source content had homes (CP11 below).

The empty spec-set resolves to the empty sequence, `resolve(⟨⟩, Σ) = ⟨⟩` and
`W = 0`; we exclude it from the operation below by requiring `W ≥ 1`, since
placing nothing is a no-op.

## The COPY operation

We now specify the placement. Let the destination be an allocated document
`d ∈ dom(Σ.M)` and let `p` be a V-position in its text subspace at which the
material is to land — a *valid insertion position*: `p = min(V_{s_C}(d))` or a
shift thereof when `V_{s_C}(d) ≠ ∅` (ASN-0036, ValidInsertionPosition), or the
canonical first position `[s_C, 1, …, 1]` when `V_{s_C}(d) = ∅`
(ValidFirstInsertionPosition). Let `resolve(R, Σ) = ⟨c₀, …, c_{W−1}⟩` with
`W ≥ 1`.

**COPY(`Σ, d, p, R`)** is the transition `Σ → Σ'` with the following effect on the
destination arrangement, displacement of its prior content, and recording of
provenance, and with the frame conditions that say what it leaves alone.

*Effect — placement.* The `W` resolved addresses are bound, in order, to the `W`
V-positions starting at `p`:

> `(A i : 0 ≤ i < W : Σ'.M(d)(p + i) = cᵢ)`     (CP2)

*Effect — displacement.* Prior text content at or beyond `p` is shifted forward by
`W` to make room, its bindings carried intact:

> `(A v : v ∈ V_{s_C}(d) ∧ v ≥ p : Σ'.M(d)(v + W) = Σ.M(d)(v))`     (CP3a)

This is the post-insertion shift of ASN-0082 (I3, PostInsertionShift) instantiated
at width `W`; we borrow its arithmetic and its preservation lemmas wholesale —
that the shifted positions remain well-formed (I3-VP), preserve depth (I3-VD),
keep the arrangement a function (I3-S2) and finite (I3-fin), and that the
post-state remains contiguous and sequential (D-CTG, D-SEQ preserved). The
placement positions `p, p+1, …, p+(W−1)` occupy exactly the ordinal gap that the
shift vacates, and the two ranges are disjoint by the order-preservation of shift
(ASN-0034, TS4).

*Effect — provenance.* Each resolved address that is new to the destination's
content range is recorded as referenced by `d`:

> `(A i : 0 ≤ i < W : (cᵢ, d) ∈ Σ'.R)`     (CP8)

This is the K.ρ provenance recording demanded of any valid arrangement extension
by ASN-0047's coupling J1★ (ExtensionRecordsProvenance): when an I-address enters
the content-subspace range of `M'(d)`, the pair `(cᵢ, d)` must enter `R`.

*Frame — left of the insertion point.*

> `(A v : v ∈ V_{s_C}(d) ∧ v < p : Σ'.M(d)(v) = Σ.M(d)(v))`     (CP3b)

*Frame — content store.*

> `dom(Σ'.C) = dom(Σ.C) ∧ (A a : a ∈ dom(Σ.C) : Σ'.C(a) = Σ.C(a))`     (CP1)

*Frame — link store, other subspaces, other documents.*

> `Σ'.L = Σ.L`     (CP7a)
>
> `(A v : v ∈ dom(Σ.M(d)) ∧ subspace(v) ≠ s_C : Σ'.M(d)(v) = Σ.M(d)(v))`
>
> `(A d' : d' ≠ d : Σ'.M(d') = Σ.M(d'))`     (CP6)

The last clause includes every source document `d_s ≠ d` and every other document
in the docuverse. The single self-reference case `d_s = d` — *self-transclusion* —
is admitted: resolution (CP0) reads the *pre-state* `Σ.M(d)`, so the addresses
`cᵢ` are fixed before any displacement, and the effect then re-binds them at fresh
positions of the same document. We return to this case under CP9.

## The transclusion frame: content is referenced, never allocated

The single claim that makes COPY *transclusion* and not *copying* is CP1:
`dom(Σ'.C) = dom(Σ.C)`. We derive it as a necessity, not a stipulation, by
reasoning backward from the placement.

The placement (CP2) requires, for each `i`, that `Σ'.M(d)(p + i) = cᵢ` be a legal
arrangement binding — and referential integrity (S3) demands its image lie in the
content store, `cᵢ ∈ dom(Σ'.C)`. There are exactly two ways to discharge this. The
first is to *find* `cᵢ` already present: resolution integrity CP0(a) gives
`cᵢ ∈ dom(Σ.C)`, and store monotonicity (S1) lifts this to `cᵢ ∈ dom(Σ'.C)` with
no growth required. The second is to *allocate* a fresh address and copy the value
into it. The first leaves `dom(Σ.C)` fixed; the second strictly enlarges it. COPY
takes the first. This is the whole of the matter:

> `wp(COPY, "placed material refers to existing content") = (A i : 0 ≤ i < W : cᵢ ∈ dom(Σ.C))`,

and that precondition is met by the source arrangements alone. No allocation step
is reachable from a state where resolution already names existing addresses, and
so CP1 holds. The destination binds *the very I-addresses the sources bind* — the
placed material and its source share one content identity, not two equal copies of
one value.

The contrast with the rejected alternative is the formal content of Nelson's
"inclusion by reference, not copy." Suppose an operation REPLICATE did the second
thing: allocate fresh `c'ᵢ ∉ dom(Σ.C)`, set `Σ'.C(c'ᵢ) = Σ.C(cᵢ)`, and bind
`Σ'.M(d)(p+i) = c'ᵢ`. Then `dom(Σ'.C) ⊋ dom(Σ.C)`, and — by the document-scoped
allocation discipline (S7a) — `origin(c'ᵢ) = d`, the destination. The placed
material would carry the destination's name, not the source's; its value would be
free to diverge from the source's future edits; and no address would connect it
back to where it came from. CP1 is precisely the prohibition of REPLICATE: *COPY
must add Vstream references to existing Istream content and must never mint new
Istream content for the included material.* The moment an operation stores fresh
native content for what it includes, it has manufactured a second identity, and it
is replication.

We record the immutability consequence as CP10: because `Σ.C` is untouched
(CP1), content immutability S0 is preserved trivially across the COPY transition —
every previously stored address keeps its value, and in particular the reused
`cᵢ` carry into the destination *the same bytes* they hold at the source, because
they are the same bytes.

## What stays the source's, and what the destination makes its own

The split the operation enforces is sharp, and it falls along the
Istream/Vstream seam. We tabulate it because the question turns on it.

| Aspect | Status under COPY | By |
|---|---|---|
| I-address (content identity) | **shared** with source — same address bound | CP2 |
| content value (bytes) | **identical** — store unchanged | CP1, CP10 |
| `origin` / home document | **identical** — the source's, computed from the address | CP5 |
| ownership of the content | **the source's**, unchanged | CP5 |
| V-position (arrangement slot) | **the destination's own**, freshly bound | CP2 |
| provenance record `(cᵢ, d)` | **the destination's own**, freshly recorded | CP8 |

The destination owns its arrangement — the *placement* of the material in its own
virtual byte stream — and the provenance entry recording that it now refers to the
content. It does not own, and COPY does not transfer to it, the content's
identity, value, or home. This is CP5, **OriginInvariance**: for every placed
address, `origin(cᵢ)` is unchanged by the transition (CP1 keeps `cᵢ` in the store,
and S7(d) makes `origin` constant while it is stored), and it equals the document
that allocated `cᵢ` — a source, never `d` (unless `d` was itself that allocator).
Attribution is *structural*: it is read off the address, not stored as detachable
metadata, so the placement cannot strip it. The owner of the source content
retains the content; the destination has acquired an arrangement and a reference,
nothing more. This is exactly Nelson's "Document A can include Document B, even
though Document B is owned by someone else" (2/35), made into a frame condition.

## The destination's prior arrangement is preserved

Placing material at `p` must not damage what the destination already held. CP3
discharges this in three parts. Content strictly before `p` is untouched (CP3b).
Content at or beyond `p` is shifted forward uniformly by `W` (CP3a), its bindings
carried intact — no existing V-position loses its content, and the relative order
of any two prior positions is preserved because shift is strictly
order-preserving (ASN-0034, TS1: `u < v ⟹ u + W < v + W`) and injective (TS2).
Nothing prior is deleted, reordered relative to its neighbours, or rebound to
different content. The only change to prior content is a uniform forward
displacement of the trailing region's V-addresses.

Two consequences matter beyond bookkeeping. First, because the prior content's
*I-addresses* are unchanged — only its V-positions move — anything anchored to
those I-addresses survives the placement unmoved; links attach to content
identity, not arrangement position (CP7 below). Second, the post-state arrangement
is again a well-formed, contiguous, sequential text subspace: the placement fills
exactly the vacated gap, so `V_{s_C}(d)` after COPY is `{p' : min ≤ p' ≤ max+W}`
with no holes, and D-CTG, D-MIN, D-SEQ are preserved (inherited from ASN-0082's
I3 preservation lemmas at width `W`). The destination's editorial order — "this
order may be continually altered by editorial operations" (4/30) — has been
extended, not corrupted.

## Source isolation, and the asymmetry of awareness

CP6 states that COPY modifies no document but the destination: every source `d_s`
distinct from `d`, and every other document, has `Σ'.M(d_s) = Σ.M(d_s)`. Combined
with the read-only character of resolution (CP0(b)) and the content and link
frames (CP1, CP7a), this says the source is untouched by the act of being copied
from. The COPY transition writes to `Σ.M(d)`, `Σ.R`, and nothing else.

Yet *isolation of the act* is not *unawareness of the connection*, and the two
must not be confused. Because the placed material shares the source's I-address
(CP2), the connection from source to destination is recoverable from the source
side: the source's content now appears, by the same address, inside `d`, and any
query that asks "which documents refer to this address?" — the provenance relation
`Σ.R`, which CP8 has just extended with `(cᵢ, d)` — answers with `d` among them.
This is the architectural opposite of what copying does. A true copy severs the
source from the destination; Nelson's "detached copy ... is frozen and dead,
lacking access to the new linkage" (2/48). Transclusion, by sharing identity,
keeps the source permanently and discoverably connected while changing nothing
about it. The source document's *state* is isolated from the copy; the source
content's *connectedness* is enlarged by it. COPY is the operation that achieves
both at once — and it can do so only because it never copies.

## Shared identity across documents

CP2 binds destination V-positions to addresses that other documents may already
bind. We record the consequence as CP4, **MultiplicityIncrease**: after COPY, the
number of `(document, V-position)` pairs mapping to a placed address `cᵢ` is
strictly greater than before — by at least the `W` new placements, and more if a
single source address appears more than once in the resolved sequence. This
realizes the unrestricted-sharing capacity of the strand model (ASN-0036, S5): one
I-address may be referenced from arbitrarily many V-positions across arbitrarily
many documents. Each such reference is an independent arrangement entry. Two
distinct V-positions binding the same `cᵢ` cannot be merged or identified — they
are permanently independent occurrences of one shared identity (ASN-0058, M14
IndependentOccurrences, M14a). The documents that already shared `cᵢ` are
unaffected (CP6); the destination simply joins the set of references to a single,
unchanged identity. *The shared thing is one identity referenced from many places,
never many copies of one identity* — which is precisely what makes attribution
traceable, correspondence between the appearances computable, and a change to the
content coherent across every reference.

Self-transclusion (`d_s = d`) is the same phenomenon within one document. CP9
records it: when the source and destination are one document, resolution reads the
pre-state, so the placed addresses are those the document's own positions bound
*before* the displacement; the effect then adds new V-positions, in the same
document, referring to the same I-addresses. The result is a document with two (or
more) V-positions mapping to one address — admitted by S5 and permanently
independent by M14. No content is duplicated; the arrangement simply references
the same identity twice.

## Survival of links anchored to the reused content

A link's endpoints are *endsets* — sets of spans over I-addresses (ASN-0043) — and
a link is discoverable from a document `d` exactly when some endset's address
coverage meets the document's arrangement range, `coverage(e) ∩ ran(Σ.M(d)) ≠ ∅`
(ASN-0098, LP12). Links bind to content identity, not arrangement position. CP7
collects what COPY must guarantee about them.

First, the link store is framed: `Σ'.L = Σ.L` (CP7a). COPY creates, alters, and
deletes no link. Second — and this is the substantive guarantee, CP7b
**LinkSurvivalUnderReuse** — placing the resolved addresses into the destination's
range makes every link anchored to them discoverable from the destination. Let `a`
be a link with `coverage(Σ.L(a).eⱼ) ∩ {c₀, …, c_{W−1}} ≠ ∅` for some endset `j`.
Before COPY, `a` may not have been discoverable from `d`; after COPY, the placed
addresses are in `ran(Σ'.M(d))` (CP2), so
`coverage(Σ.L(a).eⱼ) ∩ ran(Σ'.M(d)) ≠ ∅`, and `a` is discoverable from `d`
(ASN-0098, LP18 Resurrection; the symmetric form LP16
TransclusionDiscoverability). The link survives the reuse of its content and is
inherited by the new transcluding document — *because* COPY shares the I-addresses
rather than copying them. Had COPY allocated fresh addresses (REPLICATE), the
fresh addresses would lie outside every existing link's coverage, and not one link
would follow the placed material; the connections would be lost, the copy "frozen
and dead." This discoverability holds regardless of the link's home document and
regardless of which *other* documents already share those addresses (LP16): any
document that transcludes content covered by a link can discover that link, which
is the multi-endpoint, refraction-friendly behaviour Nelson requires of windowed
content. Third, links anchored to the destination's *prior* content survive
untouched, because that content's I-addresses are unchanged by the displacement
(CP3) — the strap stays on the same bytes even as their V-positions slide forward.

## Non-contiguous assembly, and the boundary between reuse and replication

A copy from a single contiguous source is the case where transclusion and
replication look most alike: one block of content in, one block out, and only the
*identity* of the resulting addresses — shared versus minted — tells them apart.
Assembling from several non-contiguous sources is the case that forces the
distinction into the open, and CP11 makes this precise.

By CP0(c), a spec-set drawn from non-contiguous sources resolves to a sequence
`⟨c₀, …, c_{W−1}⟩` whose addresses fall into several maximal contiguous runs,
each run drawn from one source region. The placement (CP2) lays these out as a
block decomposition of the destination's new region, one mapping block per run
(ASN-0058, bundle algebra). Within a block, all addresses share an origin
(`origin(cᵢ + 1) = origin(cᵢ)` for contiguous addresses, ASN-0058 M16a); across a
block boundary where the origins differ, the blocks *cannot be merged* (ASN-0058,
M16 CrossOriginMergeImpossibility). Therefore the multiset of origins carried by
the placed material,

> `{ origin(cᵢ) : 0 ≤ i < W }`,

is preserved verbatim into the destination's arrangement: each fragment retains
its distinct home, and each home remains queryable from the destination address
that binds it. This is CP11, **OriginMultisetPreservation**.

Now contrast replication. REPLICATE would allocate `W` fresh contiguous addresses
under the destination and copy the values; every placed address would have
`origin = d`, collapsing the origin multiset to `{d, d, …, d}` and erasing the
seams between the source regions. So discontiguity is a *test* that distinguishes
the two operations even when a single-source copy would not: COPY's non-contiguous
placement names `k` distinct parents, each still live, each still owed
attribution; REPLICATE's names one, the destination, and the provenances are
gone. Nelson's "annotated collage" assembled from many windows (2/45) is exactly
the structure CP11 preserves, and the inert single-origin mass is exactly what
CP1 forbids. The boundary the design must hold is the boundary of CP1 — *add
references, never mint content* — and the non-contiguous case is where holding it
or breaking it becomes visible at every seam.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| CP0 | `resolve(R, Σ)` reads each active source position through its arrangement, in spec-set order, yielding `⟨c₀,…,c_{W−1}⟩` with (a) every `cᵢ ∈ dom(Σ.C)`, (b) resolution a pure read of `Σ`, (c) non-contiguity of sources preserved as distinct runs | introduced |
| CP1 | TransclusionFrame: `dom(Σ'.C) = dom(Σ.C) ∧ (A a ∈ dom(Σ.C) : Σ'.C(a) = Σ.C(a))` — COPY allocates no content; the placed material refers to existing I-addresses. The boundary distinguishing transclusion from replication | introduced |
| CP2 | Placement: `(A i : 0 ≤ i < W : Σ'.M(d)(p + i) = cᵢ)` — `W` fresh destination V-positions bind the resolved (pre-existing) I-addresses; the placed material shares the source's content identity | introduced |
| CP3 | PriorArrangementPreservation: left content unchanged (CP3b, `v < p`), trailing text content shifted forward by `W` with bindings intact (CP3a, `v ≥ p`); order-preserving, injective, non-destructive | introduced |
| CP4 | MultiplicityIncrease: after COPY the count of references to each placed `cᵢ` strictly increases; distinct V-positions binding one address are permanently independent occurrences (S5, M14) | introduced |
| CP5 | OriginInvariance: `origin(cᵢ)` is unchanged by COPY and equals the source document that allocated `cᵢ`, never `d`; attribution and ownership remain the source's | introduced |
| CP6 | SourceIsolation: `(A d' ≠ d : Σ'.M(d') = Σ.M(d'))` and cross-subspace frame — every source and every other document is unmodified; the source's connectedness nonetheless grows (shared identity + provenance) | introduced |
| CP7 | Links: (a) `Σ'.L = Σ.L`; (b) LinkSurvivalUnderReuse — any link whose endset coverage meets `{c₀,…,c_{W−1}}` becomes discoverable from `d` in `Σ'`; links to the destination's prior content survive (I-addresses unchanged) | introduced |
| CP8 | ProvenanceRecording: `(A i : 0 ≤ i < W : (cᵢ, d) ∈ Σ'.R)` — the destination records fresh provenance for each reused address (J1★) | introduced |
| CP9 | SelfTransclusionAdmissibility: when `d_s = d`, resolution reads the pre-state, so placement adds independent V-positions of `d` referring to addresses `d` already bound; no content is duplicated | introduced |
| CP10 | ImmutabilityPreservation: S0 preserved across COPY (corollary of CP1); reused content carries identical bytes into the destination because they are the same bytes | introduced |
| CP11 | OriginMultisetPreservation: `{origin(cᵢ) : 0 ≤ i < W}` is preserved into the destination's arrangement; cross-origin blocks cannot merge (M16). Replication would collapse it to `{d,…,d}` — the reveal that separates reuse from replication | introduced |

## Open Questions

What must COPY guarantee when a named V-span is only partially bound — some
positions in the span resolve to content and others to no current binding?

What invariant fixes the placement order when a spec-set names overlapping or
repeated source spans that resolve a single I-address to multiple positions in the
resolved sequence?

What must the operation preserve about level-uniformity when a spec-set assembles
source spans of differing element-field depth into one destination region?

Under what conditions must a link discoverable from the destination after COPY
become undiscoverable again if the destination later removes the transcluded
positions?

What relationship must hold between the shared identity COPY establishes and the
correspondence relation that lets a reference to one appearance of content serve
as a reference to all its appearances?

What must transclusion into the link subspace guarantee, and how does placing a
link by reference differ from placing content by reference?
