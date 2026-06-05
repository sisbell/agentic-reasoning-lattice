# ASN-0105: RETRIEVEDOCVSPAN Operation

*2026-06-04*

We are trying to understand what it means to *read a span of a document at once*.
A reader names a contiguous stretch of one document and asks the system to deliver
"what is there." The question looks innocent, but every word in it hides a decision.
*What* comes back? In *what order*? What relationship does the returned thing bear to
the document as it stands at the instant of the read? And what happens at positions
inside the named stretch where nothing lives?

Nelson's own framing is the right place to start. A document, to him, is not a stored
object lying ready on a shelf; it is an *arrangement* — a virtual byte stream — that the
system *materializes from fragments* when you point at it. "THE PART YOU WANT COMES WHEN
YOU ASK FOR IT" (2/16). He calls this *part-pounce*: "You pounce like a cat on a given
thing, and it seems to be there, having been constructed while you are, as it were, in
midair" (2/16). So a read is not a lookup of a thing; it is the *on-demand reconstruction
of an arrangement over a named range*. Our task is to say, formally, what that
reconstruction must produce and what it must preserve.

We will write the operation as a pure query, `RETRIEVEDOCVSPAN(d, σ)`, that observes the
state and returns a value, changing nothing. The whole content of this note is: *what is
that value, and what must be true of it?*

---

## The substrate we read from

We take the strand model of state as given. A document `d` carries an *arrangement*
`M(d) : T ⇀ T`, a partial function from V-positions (positions in the document's current
virtual stream) to I-addresses (permanent content-store keys). Content lives in a store
`C : T ⇀ Val`. We rely on exactly these foundation facts:

- **S2** (functionality): each active V-position has at most one I-address.
- **S3** (referential integrity): `(A v : v ∈ dom(M(d)) : M(d)(v) ∈ dom(C))` — every
  active position points at allocated content.
- **S8-fin** (finiteness): `dom(M(d))` is finite.
- **S8a** (well-formedness): every active V-position is zero-free, of depth `≥ 2`, with
  all components positive.
- **S8-depth**: within one subspace all active V-positions share a common depth `m`.
- **S0 / P0** (content immutability and permanence): once `a ∈ dom(C)`, `a` stays in
  `dom(C)` forever and `C(a)` never changes.
- **S7 / S7b** (structural attribution): every `a ∈ dom(C)` has `zeros(a) = 3`, and
  `origin(a) = N(a).0.U(a).0.D(a)` names the home document of the content.

A span `σ = (s, ℓ)` denotes the position interval `⟦σ⟧ = {t ∈ T : s ≤ t < s ⊕ ℓ}`
(T12), with `reach(σ) = s ⊕ ℓ`. The subspace of a position is its first component,
`subspace(v) = v₁`; the content subspace is `s_C = 1`.

We address only a single document's content subspace, read as one span. Single-address
reads, multi-span and multi-document reads, and link traversal are out of scope.

---

## What the reader must be handed

Before we can specify the operation we must decide the *type* of its result. Reasoning
backward from the reader's need fixes it.

The reader's need is twofold (Nelson, 2/40): to obtain the content occupying the range,
and to "at once ascertain the home document of any specific word or character." The first
need is met by content values; the second is met only if each returned piece carries an
*identity*. Nelson is explicit that V-position cannot be that identity, because it shifts
under editing — "the address of a byte in its native document … may be constantly
changing" (4/11). The invariant identity is the I-address, whose `origin` field encodes
the home document. So each returned unit must carry *both* its V-position (where it sits
in the arrangement) and its I-address (which content it is).

We therefore take the result to be a finite sequence of records over `T × T`. For a
record `ρ.j = (v, a)` we write `pos(ρ.j) = v` and `iaddr(ρ.j) = a`; the content itself is
recovered as `C(a)`, and the home document as `origin(a)`. This carries no more and no
less than the reader needs: the arrangement position, the content identity, and (through
the store and `origin`) the content and its attribution.

We do *not* return a single undifferentiated blob. Nelson insists a span is structured —
"a depth-first spanning tree" (4/25) — and that boundaries between distinct pieces survive
retrieval. A per-position record sequence preserves every boundary maximally: no two
pieces are ever fused. We return to this in the boundary discussion below.

---

## The canonical result and its uniqueness

Let `A = dom(M(d)) ∩ ⟦σ⟧` be the *active positions* of the span — the V-positions in the
named range that actually carry content. By S8-fin, `A` is finite. By T1 (total order),
`A` admits exactly one strictly ascending enumeration `v₁ < v₂ < … < v_k`. Define

> `RETRIEVEDOCVSPAN(d, σ) = ⟨ (v₁, M(d)(v₁)), …, (v_k, M(d)(v_k)) ⟩`.

This is well-defined: each `M(d)(vⱼ)` exists and is single-valued by S2, and lies in
`dom(C)` by S3, so `C(M(d)(vⱼ))` and `origin(M(d)(vⱼ))` are defined. The enumeration
terminates because `A` is finite.

We now show this definition is not arbitrary — it is *forced* by what faithfulness
demands. Call a candidate result `ρ` **faithful** when three predicates hold:

- **(ordered)** `(A j : 1 ≤ j < #ρ : pos(ρ.j) < pos(ρ.{j+1}))` — V-positions strictly
  ascending under T1;
- **(sound)** `(A j : 1 ≤ j ≤ #ρ : pos(ρ.j) ∈ A ∧ iaddr(ρ.j) = M(d)(pos(ρ.j)))` — every
  record names an active position and its true I-address;
- **(complete)** `(A v : v ∈ A : (E j : 1 ≤ j ≤ #ρ : pos(ρ.j) = v))` — no active position
  is omitted.

We claim faithfulness determines `ρ` uniquely. Reasoning backward from the conjunction:
*sound* forces `{pos(ρ.j) : 1 ≤ j ≤ #ρ} ⊆ A`, and *complete* forces the reverse
inclusion, so the multiset of positions is exactly `A` — provided no position repeats. But
*ordered* is strict, so positions cannot repeat, and `pos ∘ ρ` is a strictly ascending
enumeration of `A`. A finite subset of a totally ordered set (T1) has exactly one such
enumeration; hence `pos(ρ.j) = vⱼ` for every `j`. Then *sound* pins
`iaddr(ρ.j) = M(d)(vⱼ)`, single-valued by S2. So `ρ` is exactly the canonical result. We
record the three predicates as **R1** (ordered), **R2** (pointwise fidelity), **R0**
(domain: `{pos(ρ.j)} = A`), and their joint consequence as **R3** (faithful results are
unique).

The force of R3 is that *the arrangement on the span has exactly one faithful rendering*.
An implementation has no latitude in what to return; it has latitude only in how to compute
it. This is the formal content of Nelson's "exact correspondence": the read "never returns
an approximate or stale view of the version it is reading" (synthesis of 2/15–2/16).

**Order is the arrangement's order, not storage order.** R1 orders by V-position, the
position in the document's *current* virtual stream, precisely the ordering Nelson means
by "the byte position in the current ordering of bytes … its virtual stream address"
(4/30). The I-addresses `iaddr(ρ.j)` may run in any order whatsoever — they may even be
non-monotone or repeat — because they are storage identities, not arrangement positions.
Gregory's implementation confirms this is the operative behavior: the retrieval path sorts
discovered pieces by V-address (`incontextlistnd` insertion-sorts on the V-dimension),
*not* by I-address, even when a prior link allocation has left the two orderings divergent
(consultation Q13). An alternative implementation that returned content in I-address order
would violate R1 and fail R3.

---

## Positions that hold nothing

The reader names a range, not a population. Some positions in `⟦σ⟧` may carry no content —
either interior gaps, or a tail extending past where the document's content ends. What must
the system do there?

The answer is dictated by R0 and needs no new machinery: the result is keyed on
`A = dom(M(d)) ∩ ⟦σ⟧`, so a position `v ∈ ⟦σ⟧ \ dom(M(d))` simply **contributes no
record**. There is no placeholder, no filler, no error. We name this **R4**
(gap transparency): for `v ∈ ⟦σ⟧` with `v ∉ dom(M(d))`, no record of `ρ` has
`pos = v`, and consequently `#ρ = |A|`, which may be strictly less than the number of
positions the span nominally spans.

This is exactly Nelson's account of the span. A span "does not designate the number of
bytes contained. It does not designate a number of anything" (4/24); its contents are
"implicit in the choice of first and last point" (4/25). A range that happens to be empty
is a legitimate, addressable region — "a span that contains nothing today may at a later
time contain a million documents" (4/25). Emptiness is a *valid state of the address space*,
not a fault. So the contentless portion yields nothing, the named range remains a valid
address, and the result is shorter than the request rather than padded or rejected.

The over-extension case (the span reaching beyond the last active position) is not a
separate rule; it is R4 specialized. We record it as **R5** (over-extension), stated
precisely and guarded against the empty case: *when `A ≠ ∅`*, the final record of `ρ` is
`(max(A), M(d)(max(A)))` and `#ρ = |A|`, no matter how far `reach(σ)` extends beyond
`max(A)` — every position `t ∈ ⟦σ⟧` with `t > max(A)` lies in `⟦σ⟧ \ dom(M(d))` and so
contributes nothing by R4; *when `A = ∅`*, `ρ` is the empty sequence. The result terminates
at the last active position, never at a padded boundary. Gregory's evidence agrees: the engine
collects only the crums that physically intersect the span; positions past content end have
no crum and are invisible to the traversal (consultation Q12, Q15). An implementation that
returned trailing blanks to "fill" the requested width would violate R4 and R5.

**A frame remark on gaps.** R4 also tells us what the result does *not* assert. It carries
no claim that the gap positions are empty *for all time* — only that they are empty *now*,
in the arrangement read. Re-reading the same span after content is inserted into a former
gap yields a longer result, with no contradiction: each read is faithful to the arrangement
at its own instant.

---

## Identity and attribution

R2 attaches `iaddr(ρ.j) = M(d)(vⱼ)` to every record, and S3 guarantees that I-address is
in `dom(C)`. From this two attributions follow with no further assumptions.

**Content.** `C(iaddr(ρ.j))` is defined (S3) and delivers the content occupying position
`vⱼ`. We record **R6a**: every record resolves to allocated content.

**Home document.** Because `iaddr(ρ.j) ∈ dom(C)` has `zeros = 3` (S7b), `origin(iaddr(ρ.j))`
is a well-defined document-level tumbler (S7), naming the document that allocated the
content. We record **R6b**: every record resolves to a home document via `origin`. This is
the formal form of Nelson's guarantee that one can "ascertain the home document of any
specific word or character" (2/40).

R6b is what makes transcluded and native content distinguishable in the result. A position
`vⱼ` whose content was authored in `d` and a position `vₖ` whose content was transcluded
from another document are *positionally identical* in the arrangement — both are ordinary
active positions. They are told apart only by `origin(iaddr)`: native content satisfies
`origin(iaddr) = d`, transcluded content does not. Nelson: non-native bytes "have an
ordinal position in the byte stream just as if they were native" (4/11), yet remain
distinguishable by home location. Without R6b the reader could not separate the author's
words from a quotation. Any implementation that returned content without recoverable
per-piece identity would fail R6b.

---

## Self-transclusion and boundary preservation

Two readers' worries are answered by the same structural fact: the result is keyed on
*V-position*, not on I-address.

**Self-transclusion.** Suppose one I-address `a` occupies two distinct V-positions in the
span — `M(d)(v) = M(d)(v') = a` with `v ≠ v'`, both in `A`. By R0 both `v` and `v'` are
active positions in the span, so by R3 the faithful result contains a record for each. We
record **R7** (occurrence fidelity): each active V-position yields its own record, so an
I-address that appears at `n` positions in the span appears in `n` records. The read is
*position-faithful, not content-deduplicated*. This matches Nelson's model exactly — both
occurrences "OriginalOrig" are present in the virtual stream and the read reproduces each.
Gregory confirms the implementation performs no deduplication: the I-spans are fetched once
per V-occurrence (consultation Q17). An implementation that collapsed repeated I-addresses
would lose positions present in the arrangement and violate R3.

**Boundary preservation.** Nelson insists a span "is never an undifferentiated whole"
(4/25) — the distinctions among its constituent pieces must survive. The per-position result
preserves them maximally: **R8** (boundary preservation): no two records are ever fused;
each carries its own `(pos, iaddr)`, and adjacent records `ρ.j, ρ.{j+1}` are separable by
their independent identities and origins. In particular, where the content drawn from two
home documents abuts in the arrangement, the boundary sits exactly between two records and
is recoverable from `origin(iaddr(ρ.j)) ≠ origin(iaddr(ρ.{j+1}))`.

A consequence worth stating is **R9** (re-segmentability): the index map `j ↦ pos(ρ.j)` is
an order isomorphism from `{1, …, #ρ}` onto `A`. A reader who knows the result's length and
each record's V-position can re-segment the returned stream and map every returned position
back to its place in the document — Nelson's "you always know where you are" (2/40). This is
the abstract content of the length-and-order correspondence: a span of `k` active positions
yields exactly `k` records in V-order, and position `j` of the result denotes V-position
`vⱼ`.

---

## A worked read

Abstract claims are easiest to trust once instantiated. Take the document
`d = [1.0.1.0.5]` (a document-level tumbler, `zeros(d) = 2`). Its content subspace has
depth `m = 2`, and we give it three active positions:

> `M(d) = { [1,1] ↦ a, [1,2] ↦ b, [1,3] ↦ a }`,

where the I-addresses are element-level content keys (`zeros = 3`):

> `a = [1.0.1.0.5.0.1.1]`,  `b = [1.0.1.0.8.0.1.1]`.

By S7, `origin(a) = [1.0.1.0.5] = d` (so `a` is *native* to `d`) and
`origin(b) = [1.0.1.0.8] ≠ d` (so `b` is *transcluded* from document `[1.0.1.0.8]`). Note `a`
appears at two distinct V-positions, `[1,1]` and `[1,3]` — a self-transclusion.

We read the span `σ = (s, ℓ)` with `s = [1,1]` and `ℓ = [0,3]`. Check the preconditions:
`#s = #ℓ = 2 = m` (level-uniform), and `actionPoint(ℓ) = 2 = #ℓ` (ordinal-level, the first
nonzero of `[0,3]` sitting at position 2), so precondition 3 is met. The reach is
`reach(σ) = s ⊕ ℓ = [1,1] ⊕ [0,3] = [1, 1+3] = [1,4]` (TumblerAdd copies position 1 below
the action point, sums at position 2), so `⟦σ⟧ = {t : [1,1] ≤ t < [1,4]}` covers the
depth-2 content positions `[1,1], [1,2], [1,3]`.

Now run the operation. The active set is `A = dom(M(d)) ∩ ⟦σ⟧ = {[1,1], [1,2], [1,3]}`,
ascending under T1, so

> `ρ = ⟨ ([1,1], a), ([1,2], b), ([1,3], a) ⟩`.

Verify the claims against this sequence:

- **R0**: `{pos(ρ.j)} = {[1,1],[1,2],[1,3]} = A`. ✓
- **R1**: `[1,1] < [1,2] < [1,3]` strictly ascending. ✓ (Note the I-addresses are *not*
  monotone: `a, b, a` — R1 orders by V-position, not storage identity, as claimed.)
- **R2**: `iaddr(ρ.1) = a = M(d)([1,1])`, `iaddr(ρ.2) = b = M(d)([1,2])`,
  `iaddr(ρ.3) = a = M(d)([1,3])`. ✓
- **R3**: any reordering breaks R1; any omission breaks R0; so `ρ` is the unique faithful
  rendering. ✓
- **R7**: `a` occupies two V-positions and surfaces in *two* records (`ρ.1` and `ρ.3`) — no
  deduplication. ✓
- **R8**: the boundary between `ρ.2` and `ρ.3` is a cross-origin boundary, recoverable from
  `origin(iaddr(ρ.2)) = [1.0.1.0.8] ≠ [1.0.1.0.5] = origin(iaddr(ρ.3))`. ✓

Finally R5: had we instead read the over-extended span `σ' = ([1,1], [0,6])` with
`reach(σ') = [1,7]`, the active set would be unchanged — `[1,4], [1,5], [1,6]` are in
`⟦σ'⟧ \ dom(M(d))` and contribute nothing — so `ρ` would be identical, terminating at
`max(A) = [1,3]` with `#ρ = |A| = 3`.

---

## Faithfulness across time: snapshot stability and determinism

Two faithfulness questions remain, both about *time*.

**The read reflects the present arrangement.** R0–R3 are evaluated against the state `Σ`
at which the read resolves — `dom(M(d))`, `M(d)`, and `C` as they stand. By default this is
the document's current Vstream, the live arrangement. Nelson notes a historical version may
instead be addressed explicitly — "a given part of a given version at a given time" (2/15) —
but that is a different arrangement reached by addressing a different version, and is out of
scope here. We record the default as **R10** (present-arrangement correspondence): the
result is faithful to `Σ.M(d)` at the instant of the read, neither a prior arrangement nor a
later one. Editing operations rearrange the Vstream — "this order may be continually altered
by editorial operations" (4/30) — and a read after the edit reflects the post-edit ordering
exactly, because R0–R3 are re-evaluated against the new `M(d)`.

**An already-returned result stays true.** Suppose the read produces `ρ` at `Σ`, and the
state then advances to any reachable `Σ'`. Does a later rearrangement retroactively falsify
`ρ`? It cannot. The result is a value, not a live view; and its meaning is anchored to
content identity, which is immutable. Formally, **R11** (snapshot stability): for every
record `(v, a)` of `ρ`,

> `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a) ∧ origin(a) unchanged`,

by P0 (permanence) and S0 (immutability), with `origin` a pure function of the address.
The V→I *mapping* `M(d)` may have moved underneath — `a` may now sit at a different
V-position, or at none — but the record continues to denote exactly the content it denoted
at read time. The read-time arrangement is itself never destroyed (it survives as a prior
version), so `ρ` never becomes orphaned or unverifiable. Nelson: edits are performed
"without damaging the originals" (2/45). If a caller wants to know what those positions
*became*, that is a fresh read against `Σ'`, not a mutation of `ρ`.

A subtle strengthening: R11 holds even if a *home document supplying transcluded content*
is concurrently edited. Editing a home document `d_h` changes `M(d_h)` and the home
document's own arrangement — it never changes `C`. Since `ρ`'s records denote content by
I-address, and `C` is immutable, the transcluded bytes named by a fixed I-address are stable
regardless of what happens to `d_h`'s arrangement. The read of `d` is insulated from edits
to every other document, not merely from edits to `d`.

**Determinism.** From immutability we get reproducibility. Because `C` never changes
(S0/P0), the result depends on the state only through `M(d)|⟦σ⟧`. We record **R12**
(determinism): if `Σ.M(d)|⟦σ⟧ = Σ'.M(d)|⟦σ⟧` then `RETRIEVEDOCVSPAN` returns identical
sequences at `Σ` and `Σ'`. In particular, two reads of the same span with no intervening
edit to `d`'s arrangement return content identical in substance *and* order. "No intervening
edit" need only mean no edit to `M(d)` on the span — by the strengthening above, edits to
home documents are irrelevant, because they touch neither `C` nor `M(d)`. Gregory's evidence
agrees: retrieval reads live in-memory arrangement nodes, with no snapshot cache and no
staleness window, so repeated reads of an unchanged arrangement are byte-identical and
independent of the physical tree's shape (consultation Q11, Q20).

---

## Frame: a read changes nothing

`RETRIEVEDOCVSPAN` is a query. We record **R13** (frame): the operation leaves every state
component unchanged —

> `Σ'.C = Σ.C`,  `Σ'.M = Σ.M`,  and every entity/link/provenance component unchanged.

In particular, a read whose endpoints fall in the *interior* of existing content does not
split or restructure the arrangement; it clips its returned records to the requested range
by arithmetic and leaves `M(d)` untouched. Gregory confirms: the slicing primitive used by
DELETE is never reached on a read path; reads collect whole pieces and trim the returned
bytes without mutating the enfilade (consultation Q14). An implementation whose read
silently mutated state to "normalize" boundaries would violate R13.

---

## Preconditions and well-definedness

For the result to be the faithful rendering of a *content* span, the read must be confined
to one subspace. We require:

1. `d ∈ dom(M)` — the document is allocated.
2. `σ = (s, ℓ)` satisfies T12 — `Pos(ℓ)` and `actionPoint(ℓ) ≤ #s`, so `⟦σ⟧` is a
   well-defined position interval.
3. **Content-subspace confinement.** `subspace(s) = s_C`; `σ` is level-uniform at the
   content-subspace depth (`#s = #ℓ = m`, where `m` is the common depth of `V_1(d)` by
   S8-depth); and the displacement is *ordinal-level*: `actionPoint(ℓ) = #ℓ = m`. When
   `V_1(d) = ∅` the result is the empty sequence, trivially faithful.

Confinement is load-bearing. The arrangement maps both content (subspace 1) and link
(subspace 2) V-positions; a span crossing from one into the other would, by R0–R3, return
link-orgl identities interleaved with content, and resolving those through `C` is
meaningless (a link I-address is not a content key). Gregory's evidence is blunt: the
storage layer is subspace-agnostic and will happily return intermixed identities, so the
discipline of confining a read to one subspace is a *caller obligation*, not an engine
guarantee (consultation Q19). We discharge it here as a precondition.

We do not need to assume confinement holds at every interior position separately — it
follows from the endpoints, and this is where the ordinal-level constraint of precondition 3
earns its place. Because `actionPoint(ℓ) = m` and `m ≥ 2`, the displacement `ℓ` is zero at
every position `i < m` and positive only at position `m`. By TumblerAdd, `reach(σ) = s ⊕ ℓ`
copies `s` below the action point, so `reach(σ)ᵢ = sᵢ` for `i < m`; in particular
`reach(σ)₁ = s₁ = s_C`. Both endpoints of the half-open interval thus carry the prefix
`[s_C]`.

This is exactly the hypothesis foundation **T5** (ContiguousSubtrees) needs. Take any `t`
with `s ≤ t < reach(σ)`. Then `s ≤ t ≤ reach(σ)`, with `[s_C] ≼ s` and `[s_C] ≼ reach(σ)`
(both established above), so T5 with prefix `p = [s_C]` gives `[s_C] ≼ t`, i.e. `t₁ = s_C`.
The ordinal-level constraint is load-bearing: without it `actionPoint(ℓ)` could be `1`, the
displacement could carry the first component upward (e.g. `s = [1,1]`, `ℓ = [2,1]` is
level-uniform with `actionPoint(ℓ) = 1 ≤ #s`, giving `reach(σ) = [3,1]` and admitting the
subspace-2 position `[2,1]` into `⟦σ⟧`), and the prefix argument would collapse. With it,
`reach(σ)₁ = s_C` holds, a single subspace-1 ordinal-level span automatically stays within
subspace 1, and R0's `A = dom(M(d)) ∩ ⟦σ⟧` contains only content positions. This is Nelson's
claim that "there is no choice as to what lies between" the endpoints (4/25) made precise:
the endpoints determine the subspace of the whole interval.

---

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| R0 | The result's V-positions are exactly `A = dom(M(d)) ∩ ⟦σ⟧` (active positions of the span) | introduced |
| R1 | Records are strictly ascending in V-position under T1 (arrangement order, not storage order) | introduced |
| R2 | Each record's I-address equals `M(d)(pos)` (pointwise fidelity) | introduced |
| R3 | R0 ∧ R1 ∧ R2 determine the result uniquely — the faithful rendering of a span is unique | introduced |
| R4 | Positions in `⟦σ⟧ \ dom(M(d))` yield no record; `#ρ = |A|`; no placeholder, no error (gap transparency) | introduced |
| R5 | When `A ≠ ∅`: the final record is `(max(A), M(d)(max(A)))` and `#ρ = \|A\|`, independent of how far `reach(σ)` extends past `max(A)`; when `A = ∅`: `ρ` is empty (over-extension) | introduced |
| R6a | Every record resolves to allocated content `C(iaddr)` (well-defined by S3) | introduced |
| R6b | Every record resolves to a home document `origin(iaddr)` (well-defined by S7b) | introduced |
| R7 | Each active V-position yields its own record; an I-address at `n` positions appears `n` times (occurrence fidelity) | introduced |
| R8 | No two records are fused; adjacent records are separable by identity/origin (boundary preservation) | introduced |
| R9 | `j ↦ pos(ρ.j)` is an order isomorphism onto `A`, enabling re-segmentation | introduced |
| R10 | The result is faithful to `Σ.M(d)` at the instant of reading — the present arrangement by default | introduced |
| R11 | An already-returned result stays true under later edits: its I-addresses resolve to identical content and origin in every reachable `Σ'` (snapshot stability) | introduced |
| R12 | The result is a pure function of `M(d)|⟦σ⟧`; equal arrangements-on-span give identical results (determinism / idempotence) | introduced |
| R13 | The read changes no state component (frame) | introduced |

## Open Questions

What must a read guarantee when the span's endpoints designate positions at different hierarchical depths within one subspace, given that S8-depth fixes a single depth per subspace?

What faithfulness must a read of a designated historical version preserve relative to a read of the present arrangement over the same positions?

What must the result guarantee about the relative order of co-located content and link material when a reader is permitted to request both at one position?

Under what conditions must two reads issued against the same arrangement but expressed as different but denotationally equal spans return identical results?

What invariant must relate the result of reading a span to the results of reading a partition of that span into adjacent sub-spans, so that piecewise reads compose to the whole?

What must a read guarantee about faithfulness when content occupies V-positions whose addressing arithmetic has been driven outside the well-formed range by prior editing?
