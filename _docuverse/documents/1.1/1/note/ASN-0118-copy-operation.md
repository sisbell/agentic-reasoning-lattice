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
`d_s ∈ dom(Σ.M)` together with a span `σ = (s, ℓ)` constrained by the foundation
primitives directly. The span is *well-formed* in the sense of T12 (ASN-0034):
`Pos(ℓ)` and `actionPoint(ℓ) ≤ #s`, so its denotation
`⟦σ⟧ = {t ∈ T : s ≤ t < s ⊕ ℓ}` is a well-defined order-convex set of tumblers.
It is *level-uniform* (ASN-0053, S6): `#s = #ℓ`, so start, width, and reach all
carry one tumbler length. It is *ordinal-level* (ASN-0053; ASN-0082): the action
point sits at the deepest component, `actionPoint(ℓ) = #ℓ`, so the span advances
along the last component alone. Its start is a well-formed V-position (ASN-0036,
S8a): `zeros(s) = 0`, `#s ≥ 2`, and every component of `s` is positive. These
four conjuncts are the entire definition of `σ`; no external operation's
definition is borrowed. A *spec-set* is a finite ordered sequence
`R = ⟨ρ₁, …, ρₚ⟩` of V-specs (`p ≥ 0`). The ordering is part of the request —
Nelson is explicit that "if you want to designate a separated series of items
exactly, including nothing else, you do this by a span-set, which is a series of
spans" (4/25): a spec-set is a *sequence*, not a set, and it designates content
*exactly*.

The *active positions* of a V-spec are those tumblers the span denotes that the
source arrangement actually binds, defined directly from the foundation
primitives as `act(ρ, Σ) = dom(Σ.M(d_s)) ∩ ⟦σ⟧` — the intersection of the source
document's bound V-positions (ASN-0036) with the span's denotation (ASN-0034,
T12). This
set is finite (subset of the finite `dom(Σ.M(d_s))`, S8-fin) and totally ordered
(subset of the totally ordered carrier `T`, T1), hence has a unique ascending
enumeration `v₁ < … < v_k`. We restrict attention to *content* spec-sets: COPY's
content-residence precondition (stated with the operation below) requires every
active position to be in the text subspace, `subspace(vⱼ) = s_C`, so by referential
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

**Precondition — content residence.** Every active position of every V-spec in `R`
lies in the text subspace:
`(A ρ ∈ R, v ∈ act(ρ, Σ) : subspace(v) = s_C)`. This promotes the resolution
section's "content spec-set" restriction to an explicit precondition of the
operation, and it is load-bearing in two places. Without it a resolved `vⱼ` could
be a link V-position (`subspace(vⱼ) = s_L`), and S3★ would place
`Σ.M(d_s)(vⱼ)` in `dom(Σ.L)` rather than `dom(Σ.C)` — falsifying CP0(a). And CP2
would then bind that link address to a content-subspace destination position
`p + i`, leaving a content V-position imaging a link address, in violation of S3★
in the post-state. The precondition discharges both obligations at once: CP0(a)'s
`cᵢ ∈ dom(Σ.C)` and CP2's content-subspace referential integrity.

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

*Effect — provenance.* Each resolved address is referenced by `d` in the
post-state:

> `(A i : 0 ≤ i < W : (cᵢ, d) ∈ Σ'.R)`     (CP8)

CP8 is a *membership* postcondition, and to see that the membership is *produced*
rather than merely *required*, we exhibit COPY as a valid ASN-0047 composite
(ValidComposite) and read the obligation off its atomic steps. The decomposition
splits on whether the insertion point has trailing content to displace; getting it
right matters, because a single K.μ⁺ cannot realize the displacement.

*Append or empty case* (`p = max+1`, or `V_{s_C}(d) = ∅`). No prior position
satisfies `v ≥ p`, so CP3a is vacuous and the effect is a pure extension: a single
K.μ⁺ step adds the `W` placement positions `[p, p+W)` bound to `c₀,…,c_{W−1}`,
leaving every prior mapping intact — exactly K.μ⁺'s strict-extension frame
`(A v ∈ dom(Σ.M(d)) : Σ'.M(d)(v) = Σ.M(d)(v))`. The resulting text run is the
contiguous block `[min, max+W]` (or `[p, p+W)` when empty), discharging K.μ⁺'s
D-CTG★/D-MIN★ precondition.

*Displacing case* (`p ≤ max`, so trailing content exists). Here a pure K.μ⁺ is
*not* a faithful decomposition, and the difference is structural. The displacement
(CP3a) rewrites the existing binding `v ↦ a` into `(v+W) ↦ a`, which *removes* `v`
from `dom(Σ.M(d))` — whereas K.μ⁺ is strict extension and leaves every prior
mapping fixed, growing the domain only. No K.μ⁺ can vacate `v`. The effect is
therefore a *contraction-then-extension* composite. Write `p = min + j` with
`0 ≤ j < N`. **(i)** A K.μ⁻ step contracts `d`'s text subspace to the retained
prefix `[min, p)` — retention count `n'_{s_C} = j` (a strict contraction, since
`j < N`) — removing the trailing positions `{min + i : j ≤ i < N}`. The
intermediate state `Σ₁` satisfies the per-state invariants: its text run
`{min + i : 0 ≤ i < j}` is a contiguous block from `min` (D-CTG★/D-MIN★ restricted
to `s_C`, the latter vacuous when `j = 0`); `Σ₁.M(d)` is a restriction of the
function `Σ.M(d)`, hence itself a function (S2) with surviving images unchanged and
still in `dom(Σ.C)` (S3★); and its domain is a subset of a finite set (S8-fin).
K.μ⁻ frames the content store, link store, and provenance unchanged
(`Σ₁.C = Σ.C`, `Σ₁.L = Σ.L`, `Σ₁.R = Σ.R`). **(ii)** A K.μ⁺ step then re-adds, on
top of the retained prefix, both the `W` placement positions `[p, p+W)` bound to
`c₀,…,c_{W−1}` (CP2) and the displaced trailing positions
`{(min+i)+W : j ≤ i < N} = [p+W, max+W]` bound to their original images
`Σ.M(d)(min+i)` (CP3a). Each retained mapping is left intact — K.μ⁺'s
strict-extension frame — and the freshly added V-positions are well-formed (I3-VP);
the resulting text run is the contiguous block `[min, max+W]`, discharging K.μ⁺'s
D-CTG★/D-MIN★ precondition. Steps (i)–(ii) together reproduce CP2, CP3a, and CP3b
(the left prefix is retained by (i) and untouched by (ii)).

To these arrangement steps the composite appends one K.ρ provenance step per
range-new address; it is these K.ρ steps that put pairs into `Σ.R`. The provenance
obligation is read off ASN-0047's couplings, which ValidComposite evaluates
*initial-to-final* (`Σ` to `Σ'`) — so the intermediate removal and re-addition of
the displaced positions across steps (i)–(ii) is invisible to the coupling check,
and only the net change in `d`'s content-subspace range matters. The discharge then
splits on whether `cᵢ` is new to that range. For
each `cᵢ` that is *range-new* — not already in the content-subspace range of
`M(d)` — the placement (CP2) makes it range-new in `Σ'`, so ASN-0047's coupling
J1★ (ExtensionRecordsProvenance) is an *obligation* on the composite: a valid COPY
must include a K.ρ step recording `(cᵢ, d)`, and J1'★ (ProvenanceRequiresExtension)
constrains that step's admissibility — no provenance record without a corresponding
range extension — so the K.ρ steps record exactly the range-new addresses and
produce `(cᵢ, d) ∈ Σ'.R` for each. For each `cᵢ` *already* referenced by `d`
(already transcluded into `d`, or, in self-transclusion CP9, already bound by one
of `d`'s own pre-state content positions), no K.ρ step is needed: `cᵢ` already lies
in the content-subspace range of `M(d)` in the pre-state, so by P4★
(`Contains_C(Σ) ⊆ R`, ASN-0047) `(cᵢ, d) ∈ Σ.R` already holds, and provenance
permanence (P2) carries it into `Σ'`. Either way the membership holds in `Σ'`;
fresh recording occurs exactly for the range-new addresses.

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
`dom(Σ'.C) = dom(Σ.C)`. This is the *defining frame condition* of COPY — a design
stipulation, not a theorem. We adopt it as the operation's content and then show
it is consistent with the placement, and that dropping it yields a different
operation (REPLICATE) entirely.

The placement (CP2) requires, for each `i`, that `Σ'.M(d)(p + i) = cᵢ` be a legal
arrangement binding — and referential integrity (S3) demands its image lie in the
content store, `cᵢ ∈ dom(Σ'.C)`. There are two ways an operation *could* discharge
this. The first is to *find* `cᵢ` already present; the second is to *allocate* a
fresh address and copy the value into it. *Given* CP1, only the first is available
— and it suffices: resolution integrity CP0(a) gives `cᵢ ∈ dom(Σ.C)`, and store
monotonicity (S1) lifts this to `cᵢ ∈ dom(Σ'.C)` with no growth. So under CP1 the
placement's referential-integrity obligation —
`(A i : 0 ≤ i < W : cᵢ ∈ dom(Σ'.C))` — is dischargeable: every address the
placement names is already present, and CP1 is in no tension with the binding it
must support. The destination binds *the very I-addresses the sources bind* — the
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
is again a well-formed, contiguous, sequential text subspace. ASN-0082's I3
lemmas supply the per-position facts — that the shifted positions stay
well-formed (I3-VP), preserve depth (I3-VD), and keep the arrangement a function
(I3-S2) and finite (I3-fin) — but they describe only the *shift* of trailing
content and so do not by themselves establish gap-filling. The no-holes tiling we
derive explicitly from ordinal arithmetic, splitting on whether the destination's
text subspace is already populated.

*Empty destination* (`V_{s_C}(d) = ∅`, so `N = 0`). Here COPY establishes the
document's first content rather than preserving prior content. The valid insertion
position is the canonical `p = [s_C, 1, …, 1]` (ValidFirstInsertionPosition); the
displacement (CP3a) and left-frame (CP3b) clauses are vacuous — there is no prior
`v ≥ p` to shift and none `v < p` to fix — and the placement (CP2) lays the `W`
positions `p, p+1, …, p+(W−1)`. The post-state run is `{p + i : 0 ≤ i < W}`, which
has minimum `p = [s_C, 1, …, 1]` (D-MIN *established*), is the sequential block of
`W` positions from that minimum (D-SEQ *established*), and has no interior hole
(D-CTG). In the empty case D-MIN and D-SEQ are established, not preserved — COPY
lays down the first content the document holds.

*Non-empty destination* (`V_{s_C}(d) ≠ ∅`, so `N ≥ 1`). Before COPY, `V_{s_C}(d)`
is the contiguous run `{min + i : 0 ≤ i < N}` with `min = [s_C, 1, …, 1]` (D-MIN)
and `N = |V_{s_C}(d)|` (D-SEQ), so its top is `max = min + (N−1)`. The valid
insertion position `p` is `min + j` for some `0 ≤ j ≤ N` (ASN-0036,
ValidInsertionPosition), i.e. `p`'s ordinal lies in `[min, max+1]`. COPY lays
the post-state out as three ordinal ranges, using `+` for the ordinal shift:

- *Left, unmoved* (CP3b): the positions `v < p`, namely `{min + i : 0 ≤ i < j}`,
  occupying the ordinal interval `[min, p)`.
- *Placement* (CP2): the `W` positions `p, p+1, …, p+(W−1)`, occupying `[p, p+W)`.
- *Shifted right* (CP3a): each `v ≥ p`, namely `{min + i : j ≤ i < N}`, moves to
  `v + W`, occupying `[p+W, max+W]`.

These three ordinal intervals are consecutive and non-overlapping: the left run
ends just below `p` where the placement begins, and the placement ends just below
`p+W` where the shifted run begins. Disjointness is ordinal arithmetic, not I3 —
shift is strictly order-preserving (ASN-0034, TS1) and a strict advance
(`v + W > v`, TS4), so no shifted position lands at or below any placement or
left position, and the half-open intervals abut without gap or overlap. Their
union is the single contiguous run `[min, max+W] = {min + i : 0 ≤ i < N+W}`. Hence
`V_{s_C}(d)` after COPY has minimum `min` unchanged (D-MIN preserved), is the
sequential block of `N+W` positions from `min` (D-SEQ preserved), and has no
interior hole (D-CTG preserved). The destination's editorial order — "this
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
bind. We record the consequence as CP4, **MultiplicityIncrease**: COPY adds `W`
new `(document, V-position)` references (one per placement, CP2), so the total
number of references into the placed set `{c₀, …, c_{W−1}}` increases by exactly
`W`. The per-address arithmetic is finer: for a fixed placed address `cᵢ`, its own
reference count increases by the number of times `cᵢ` *occurs in*
`resolve(R, Σ)` — at least one, and more only when a single source address is
resolved at several positions of the sequence. The aggregate increase `W` and the
per-address increase (the occurrence count) are distinct quantities, and they
coincide only when every resolved address is distinct. This
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
After COPY the placed addresses are in `ran(Σ'.M(d))` (CP2), so
`coverage(Σ.L(a).eⱼ) ∩ ran(Σ'.M(d)) ≠ ∅`, and the discoverability
characterisation evaluated at the post-state — `discoverable_from(a, d, Σ') ⟺
(E i : coverage(Σ'.L(a).eᵢ) ∩ ran(Σ'.M(d)) ≠ ∅)` (ASN-0098, LP12), with
`Σ'.L = Σ.L` by CP7a so coverage is unchanged — yields `a` discoverable from `d`.
The link survives the reuse of its content and is
inherited by the new transcluding document — *because* COPY shares the I-addresses
rather than copying them. Had COPY allocated fresh addresses (REPLICATE), the
fresh addresses would lie outside every existing link's coverage, and not one link
would follow the placed material; the connections would be lost, the copy "frozen
and dead." This discoverability holds regardless of the link's home document and
regardless of which *other* documents already share those addresses, because the
LP12 criterion mentions only `ran(Σ'.M(d))` — the destination's own range — and is
silent on `home(a)` and on every other document: any
document that transcludes content covered by a link can discover that link, which
is the multi-endpoint, refraction-friendly behaviour Nelson requires of windowed
content.

This is the place for a non-trivial weakest precondition. Fix a link `a` not
already discoverable from `d` at `Σ`, and ask what must hold of `Σ` for `a` to be
discoverable from `d` after COPY. Pulling the post-state criterion back through
the operation — `Σ'.L = Σ.L` (CP7a), and
`ran(Σ'.M(d)) = ran(Σ.M(d)) ∪ {c₀, …, c_{W−1}}` (CP2 adds the placed addresses;
CP3a/CP3b move prior positions but preserve their I-addresses, so the prior range
is retained) — gives

> `wp(COPY, "a discoverable from d") = (E j : coverage(Σ.L(a).eⱼ) ∩ {c₀, …, c_{W−1}} ≠ ∅)`.

The precondition is not vacuous: it fails precisely when none of the resolved
addresses lies under any of `a`'s endsets, and in that case COPY — though it
faithfully shares identity — brings `a` no closer to `d`. Discoverability is thus
*conditional on what the spec-set names*, which is exactly the lever transclusion
gives an author: to inherit a link, place content the link already covers.

Third, links anchored to the destination's *prior* content survive
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

## A worked assembly from two sources

We instantiate the operation on concrete tumblers, choosing a non-contiguous
two-source case so that CP11 has something to separate. Use the document-level
prefixes `d_A = 1.0.1.0.7`, `d_B = 1.0.1.0.8`, and destination `d = 1.0.1.0.9`
(each `zeros = 2`, a document address). Content addresses sit at `[d.0.s_C.k]`
with `s_C = 1` (ASN-0093), so they have `zeros = 3` and subspace identifier `1`.
Let the stores hold

- `a₁ = 1.0.1.0.7.0.1.1`, `a₂ = 1.0.1.0.7.0.1.2` (source A's content), and
- `b₁ = 1.0.1.0.8.0.1.1` (source B's content),

with arrangements (text subspace, depth-2 V-positions `[1, k]`)

- `Σ.M(d_A) = { [1,1] ↦ a₁, [1,2] ↦ a₂ }`,
- `Σ.M(d_B) = { [1,1] ↦ b₁ }`,
- `Σ.M(d)   = { [1,1] ↦ x₁, [1,2] ↦ x₂ }` with `x₁, x₂` allocated by `d`
  itself, so `origin(x₁) = origin(x₂) = d`.

Take the spec-set `R = ⟨(d_A, σ_A), (d_B, σ_B)⟩` with
`σ_A = ([1,1], δ(2,2)) = ([1,1], [0,2])` and `σ_B = ([1,1], δ(1,2)) = ([1,1], [0,1])`.
Both are level-uniform (`#s = #ℓ = 2`) and ordinal-level (`actionPoint(ℓ) = 2`).
Their denotations are `⟦σ_A⟧ = {t : [1,1] ≤ t < [1,3]}` and
`⟦σ_B⟧ = {t : [1,1] ≤ t < [1,2]}`, so `act((d_A,σ_A),Σ) = {[1,1],[1,2]}` and
`act((d_B,σ_B),Σ) = {[1,1]}`. Resolution reads each through its arrangement:

> `resolve(R, Σ) = ⟨a₁, a₂⟩ ⌢ ⟨b₁⟩ = ⟨a₁, a₂, b₁⟩`,  so `W = 3`.

Place at `p = [1,2]` — a valid insertion position, since with `N = 2` the
admissible positions are `[1,1], [1,2], [1,3]` (here `j = 1`). COPY yields

> `Σ'.M(d) = { [1,1] ↦ x₁, [1,2] ↦ a₁, [1,3] ↦ a₂, [1,4] ↦ b₁, [1,5] ↦ x₂ }`.

We check the claims numerically.

- **CP1 (store unchanged).** `a₁, a₂, b₁, x₁, x₂` are all pre-existing; the
  binding introduces no fresh I-address, so `dom(Σ'.C) = dom(Σ.C)`.
- **CP2 (placement).** `[1,2] ↦ a₁`, `[1,3] ↦ a₂`, `[1,4] ↦ b₁` — the `W = 3`
  resolved addresses at `p, p+1, p+2`.
- **CP3a (shift).** The one prior position `≥ p`, `[1,2] ↦ x₂`, moves to
  `[1,2] + 3 = [1,5] ↦ x₂`; CP3b leaves `[1,1] ↦ x₁` untouched. The post-state
  text run is `{[1,1], …, [1,5]}` — contiguous, `N + W = 5` positions, minimum
  `[1,1]` unchanged.
- **CP11 (origin multiset).** `origin(a₁) = origin(a₂) = 1.0.1.0.7 = d_A` and
  `origin(b₁) = 1.0.1.0.8 = d_B`, so the placed multiset is
  `{d_A, d_A, d_B}`, carried verbatim into `d`'s arrangement. `a₁, a₂` form one
  block (`a₂ = a₁ + 1`, same origin); `b₁` is a second block whose origin differs,
  so the two cannot merge (ASN-0058, M16). Two live parents are named, neither of
  them `d`. A REPLICATE would instead mint three addresses under `d` and collapse
  the multiset to `{d, d, d}`, erasing the seam between source A and source B.

The numbers exhibit the whole point: the destination's V-positions are new, but
every I-address and every origin in the assembly is borrowed, intact, from the
sources.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| CP0 | `resolve(R, Σ)` reads each active source position through its arrangement, in spec-set order, yielding `⟨c₀,…,c_{W−1}⟩` with (a) every `cᵢ ∈ dom(Σ.C)`, (b) resolution a pure read of `Σ`, (c) non-contiguity of sources preserved as distinct runs | introduced |
| CP1 | TransclusionFrame: `dom(Σ'.C) = dom(Σ.C) ∧ (A a ∈ dom(Σ.C) : Σ'.C(a) = Σ.C(a))` — COPY allocates no content; the placed material refers to existing I-addresses. The boundary distinguishing transclusion from replication | introduced |
| CP2 | Placement: `(A i : 0 ≤ i < W : Σ'.M(d)(p + i) = cᵢ)` — `W` fresh destination V-positions bind the resolved (pre-existing) I-addresses; the placed material shares the source's content identity | introduced |
| CP3 | PriorArrangementPreservation: left content unchanged (CP3b, `v < p`), trailing text content shifted forward by `W` with bindings intact (CP3a, `v ≥ p`); order-preserving, injective, non-destructive | introduced |
| CP4 | MultiplicityIncrease: total references into the placed set increase by exactly `W`; each placed `cᵢ`'s own reference count increases by its occurrence count in `resolve(R, Σ)` (≥ 1); distinct V-positions binding one address are permanently independent occurrences (S5, M14) | introduced |
| CP5 | OriginInvariance: `origin(cᵢ)` is unchanged by COPY and equals the source document that allocated `cᵢ`, never `d`; attribution and ownership remain the source's | introduced |
| CP6 | SourceIsolation: `(A d' ≠ d : Σ'.M(d') = Σ.M(d'))` and cross-subspace frame — every source and every other document is unmodified; the source's connectedness nonetheless grows (shared identity + provenance) | introduced |
| CP7 | Links: (a) `Σ'.L = Σ.L`; (b) LinkSurvivalUnderReuse — any link whose endset coverage meets `{c₀,…,c_{W−1}}` becomes discoverable from `d` in `Σ'`; links to the destination's prior content survive (I-addresses unchanged) | introduced |
| CP8 | ProvenanceRecording: `(A i : 0 ≤ i < W : (cᵢ, d) ∈ Σ'.R)` — produced by COPY's K.ρ steps for range-new addresses (J1★ obligation, J1'★ uniqueness) and supplied by P4★ + permanence P2 for addresses `d` already referenced | introduced |
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
