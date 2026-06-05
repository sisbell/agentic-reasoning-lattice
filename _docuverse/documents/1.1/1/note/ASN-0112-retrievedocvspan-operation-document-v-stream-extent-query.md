# ASN-0112: RETRIEVEDOCVSPAN Operation — Document V-Stream Extent Query

*2026-06-04*

We are trying to understand the simplest question one can put to a document: *given
only your name, where does your content begin and how far does it reach?* The caller
hands over a document identity and nothing else — no range, no position, no selection —
and expects back a single answer that bounds the whole. Our task is to say, formally,
what that answer is, what it must describe, and what may be true of it.

The operation is a *boundary query*, not a content read. It takes no span argument and
delivers no bytes. Nelson fixes its shape exactly: it "returns a span determining the
origin and extent of the V-stream of document `<doc id>`" (4/68). So the input is a bare
document identity and the output is *one span*: a pair of an origin and an extent. We must
decide what that origin and extent denote, what relationship they bear to the document's
present arrangement, what the caller gains over what the identity already disclosed, and
what invariants constrain the span the operation may legally return.

We write the operation as a pure query, `RETRIEVEDOCVSPAN(d)`, that observes the state and
returns a value, changing nothing. The entire content of this note is: *what is that
value, and what must hold of it?*

---

## The substrate we measure

We take the strand model of state as given. A document `d` carries an *arrangement*
`M(d) : T ⇀ T`, a partial function from V-positions — positions in the document's current
virtual stream — to I-addresses, the permanent keys of a content store `C : T ⇀ Val`. We
write

> `O(d) = dom(M(d))`

for the set of *occupied V-positions* of `d`: the positions that currently carry content
in the arrangement. This set is exactly what RETRIEVEDOCVSPAN must bound. We rely on these
foundation facts:

- **S2** (functionality): each occupied V-position has a single I-address.
- **S3** (referential integrity): `(A v : v ∈ O(d) : M(d)(v) ∈ dom(C))`.
- **S8-fin** (finiteness): `O(d)` is finite.
- **S8a** (well-formedness): every `v ∈ O(d)` is zero-free, of depth `≥ 2`, all
  components positive; `subspace(v) = v₁`.
- **S8-depth**: within one subspace all occupied V-positions share a common depth.
- **D-CTG / D-MIN / D-SEQ** (content-subspace shape): the content positions
  `V_{s_C}(d) = {v ∈ O(d) : subspace(v) = s_C}` are contiguous, their minimum is the
  canonical `[s_C,1,…,1]`, and they form the dense run
  `{[s_C,1,…,1,k] : 1 ≤ k ≤ n}` for some `n ≥ 1` when non-empty.
- **S0 / P0** (content immutability and permanence): once `a ∈ dom(C)`, `a` stays in
  `dom(C)` forever and `C(a)` never changes.

Two subspaces inhabit the arrangement: content positions carry `subspace = s_C` and link
positions carry `subspace = s_L`, with the fixed convention `s_C = 1`, `s_L = 2`
(SubspaceConventionAxiom). Because `s_C < s_L` at the first component, T1 places every
content position before every link position.

We borrow the span machinery wholesale. A span `σ = (s, ℓ)` denotes the half-open interval
`⟦σ⟧ = {t ∈ T : s ≤ t < s ⊕ ℓ}` (T12), with `reach(σ) = s ⊕ ℓ` (ASN-0053). A span is
*well-formed* when `Pos(ℓ)` and `actionPoint(ℓ) ≤ #s`; it is *level-uniform* when
`#s = #ℓ`. The ordinal shift `shift(t, n) = t ⊕ δ(n, #t)` advances `t`'s last component by
`n` (ASN-0034). We measure the whole document as one span; per-subspace reporting,
content delivery, and region reads are out of scope.

---

## What the caller must be handed

Before specifying the operation we must fix the *type* of its result. Nelson fixes it for
us: a span, "the origin and extent of the V-stream" (4/68). Not a sequence of records — that
would be a content read. Not a count: "a tumbler-span is not a conventional number, and it
does not designate the number of bytes contained. It does not designate a number of
anything" (4/24). The result is a *boundary description* — two tumblers, a start and a
width, whose meaning is "from here, this far," with everything between implicit (4/25).

We therefore take the result to be a single span `σ_d = (origin_d, extent_d)` whenever the
document carries content, and a *distinguished empty value* when it does not. We record this
as **V0** (span-valued result): for a non-empty document `RETRIEVEDOCVSPAN(d)` returns one
well-formed span — never a content sequence and never a cardinality — and for an empty
document (`O(d) = ∅`) it returns the *empty span-set* `⟨⟩` (ASN-0053), the distinguished
value denoting `∅`, which is *not* a T12 span. We treat `⟨⟩` as a separate inhabitant of
the result type rather than forcing a degenerate span, because no T12 span can denote `∅`
(S2, ASN-0053: every well-formed span is non-empty). The caller reads `origin_d` to learn
where the V-stream begins and `extent_d` to learn how far it reaches; the content itself,
and any per-piece count, are the business of other operations. The empty case is taken up in
full below (V11).

---

## The bounding span and its two endpoints

Reasoning from "origin and extent of the V-stream," we must produce a span that *spans the
whole document* — one region containing all of its arranged content. The occupied set
`O(d)` is finite (S8-fin) and totally ordered by T1, so when non-empty it has a least
element and a greatest element. Define

> `origin_d = min O(d)`,  `reach_d = shift(max O(d), 1)`,  `extent_d = reach_d ⊖ origin_d`,

and `σ_d = (origin_d, extent_d)`. The reach advances one ordinal step past the maximum
occupied position, realizing the half-open convention under which the last occupied
position is included and the next is excluded. We must show this is well-defined and
forced.

**The origin is an occupied position.** We record **V1**: when `O(d) ≠ ∅`,
`origin_d = min O(d)` and `origin_d ∈ O(d)`. The minimum of a finite, totally ordered,
non-empty set exists, is unique, and is a member. So the reported origin is never a
fictitious lower boundary; it is the actual V-address at which the document's first
arranged content sits. Gregory's implementation realizes exactly this: the query reads the
arrangement-tree root's V-displacement, which is maintained to equal the minimum V-address
of any content in the document (consultation Q12, Q15, Q20) — "the grasp is always
occupied" (Q20). The start it reports for a text-bearing document is `1.1`, the first
character position, not a padded `1.0` (Q15).

**The extent is a well-formed displacement.** We first establish that `σ_d` is a legal T12
span regardless of whether its endpoints share a depth. Since `reach_d = shift(max O(d), 1) >
max O(d) ≥ origin_d` (TS4, ShiftStrictIncrease), we have `origin_d < reach_d`. The first
position at which `origin_d` and `reach_d` diverge, `k = divergence(origin_d, reach_d)`,
satisfies `k ≤ #origin_d` in every case: in the single-subspace case the two tumblers share
the canonical prefix `[s_C,1,…,1]` and differ only at the last component, so `k = #origin_d`;
in the cross-subspace case they differ already at position 1 (`s_C` vs `s_L`), so `k = 1 ≤
#origin_d`. By D0 (DisplacementWellDefined, ASN-0034) — applicable because `origin_d <
reach_d` and `divergence(origin_d, reach_d) ≤ #origin_d` — the displacement `extent_d =
reach_d ⊖ origin_d` is a positive tumbler with `actionPoint(extent_d) = k ≤ #origin_d`. Hence
`(origin_d, extent_d)` satisfies T12 and is a well-formed span. *We do not assume
level-uniformity here.*

**The span covers every occupied position.** We record **V2** (covering): `O(d) ⊆ ⟦σ_d⟧`.
The denotation is `⟦σ_d⟧ = {t : origin_d ≤ t < origin_d ⊕ extent_d}`, so we must locate the
*actual* reach `r⋆ = origin_d ⊕ extent_d` and show `max O(d) < r⋆`. Two cases on the relative
depths:

- *`#origin_d ≤ #reach_d`* (in particular the level-uniform case `#origin_d = #reach_d`). By
  D1 (DisplacementRoundTrip, ASN-0034) the round-trip closes exactly: `r⋆ = origin_d ⊕
  (reach_d ⊖ origin_d) = reach_d`. Then for any `v ∈ O(d)`, `origin_d ≤ v ≤ max O(d) <
  reach_d = r⋆`, so `v ∈ ⟦σ_d⟧`.
- *`#origin_d > #reach_d`* (content deeper than the maximal link position). By D0 the
  round-trip *fails* — `r⋆ ≠ reach_d` — so we compute `r⋆` directly. With `k = 1`, TumblerAdd
  gives `r⋆` agreeing with `reach_d` (zero-padded to length `#origin_d`) on every position
  `1 ≤ i ≤ #reach_d` and carrying trailing zeros beyond, so `reach_d` is a proper prefix of
  `r⋆` and `reach_d < r⋆` (T1 case (ii)). Hence `max O(d) < reach_d < r⋆`, and again every
  `v ∈ O(d)` lies in `⟦σ_d⟧`.

In both cases `r⋆ ≥ reach_d > max O(d)`, so coverage holds *unconditionally* — it does not
route through level-uniformity or through WF. What level-uniformity buys is only that the
span's reach *equals* `reach_d` exactly: `reach(σ_d) = reach_d ⟺ #origin_d ≤ #reach_d`, which
holds whenever the occupied subspaces share a common depth (the case the implementation
always realizes — see V6).

**The span is the tightest covering bound among same-depth reaches.** We record **V3**
(bounding): `origin_d` is the greatest lower bound of `O(d)`, and `reach_d` is the *least*
admissible upper bound *among tumblers of the same depth as* `max O(d)`. We are deliberately
careful about the qualifier, because without it the claim is false. The lower bound is
unconditional: any span `σ'` with `O(d) ⊆ ⟦σ'⟧` satisfies `start(σ') ≤ min O(d) = origin_d`.
The upper bound requires an argument, not an appeal to a "one step at a time" convention —
the tumbler line has no such convention. In fact `max O(d)` has a *strictly smaller* T1
upper bound than `reach_d`: its true immediate successor is the zero-extension
`max O(d).0`, with `max O(d) < max O(d).0 < shift(max O(d), 1) = reach_d`. The first
inequality holds because `max O(d)` is a proper prefix of `max O(d).0` (T1 case (ii)); the
second because, writing `w = max O(d) = [w_1,…,w_m]`, the tumblers `max O(d).0 =
[w_1,…,w_m,0]` and `reach_d = [w_1,…,w_{m-1},w_m+1]` agree on positions `1…m-1` and diverge at
position `m` with `w_m < w_m+1` (T1 case (i)). A span with reach `max O(d).0` would already
cover `O(d)`, since `w < max O(d).0`. So `reach_d` is *not* the least admissible reach over
all of `T`.

What is true — and what V3 now claims — is that `reach_d` is the least reach among same-depth
tumblers, i.e. those that keep the bounding span level-uniform with the occupied positions.
Let `m = #max O(d)` and let `r` be any tumbler with `#r = m` and `r > max O(d)`; we show
`r ≥ reach_d`. Write `w = max O(d) = [w_1,…,w_m]`, so `reach_d = [w_1,…,w_{m-1}, w_m + 1]`
(OrdinalShift advances the last component). Since `#r = #w`, `r > w` means they first diverge
at some position `j ≤ m` with `r_j > w_j` and `r_i = w_i` for `i < j`. If `j = m`, then
`r_m ≥ w_m + 1` while `r` agrees with `w` (hence with `reach_d`) on `1…m-1`, so `r ≥ reach_d`.
If `j < m`, then `reach_d` agrees with `w` on `1…m-1` so `reach_d_j = w_j < r_j` while both
agree with `w` on `1…j-1`, giving `reach_d < r` (T1 case (i)). Either way `reach_d ≤ r`. So
`reach_d` is the least same-depth strict upper bound of `max O(d)`, and the deeper successor
`max O(d).0` is excluded precisely because it lifts the span out of level-uniformity. So
`σ_d` is the tightest *level-uniform* covering span of `O(d)`. This is the formal core of
Nelson's claim that origin and extent "describe the document as a whole" *implicitly* —
"there is no choice as to what lies between; this is implicit in the choice of first and last
point" (4/25). Fix the two boundaries and the whole is determined.

---

## The Vstream is what we measure, not the Istream

Nelson is emphatic that the report is over the *V-stream* — the present arrangement — not
the permanent content store. "This returns a span determining the origin and extent of the
**V-stream**" (4/68). The distinction is sharp and load-bearing.

Content that has been removed from the arrangement persists permanently in the store (S0,
P0) but leaves `O(d) = dom(M(d))`. Such content is, in Nelson's phrase, "not currently
addressable" (4/9): it "may remain included in other versions" (4/11) but is gone from this
document's current Vstream. We record **V4** (Vstream-bounded): `extent_d` is computed from
`O(d)` alone, so content present in `dom(C)` but absent from `dom(M(d))` — deleted-but-stored
content, or content native elsewhere and not arranged here — contributes nothing to the
reported span. The extent measures *what the arrangement currently contains*, not *what the
store has ever held*. This is Nelson's answer to whether the extent must account for all
content the document ever held: it accounts only for the content presently belonging to it.

The relationship the extent must bear to the arrangement is therefore one of *current
correspondence*: by V2 the span covers every occupied position, and by V4 it draws its
endpoints from no other source. For a document whose occupied positions lie in a single
subspace, this correspondence is *exact*.

---

## Exact cover within a subspace; a bounding box across subspaces

The decisive structural question is whether the single returned span exactly traces the
occupied content or merely encloses it. The answer depends on how many subspaces the
arrangement occupies, and the divergence is not an implementation artifact — it is forced
by the demand for *one* origin-and-extent pair.

**Single subspace: exact cover.** Suppose `O(d)` lies entirely in the content subspace.
By D-SEQ the occupied positions are `{[s_C,1,…,1,k] : 1 ≤ k ≤ n}`, a dense run with no
internal gaps. Then `origin_d = [s_C,1,…,1]` (D-MIN), `max O(d) = [s_C,1,…,1,n]`,
`reach_d = [s_C,1,…,1,n+1]`, and `⟦σ_d⟧` restricted to depth-`m` content positions is
exactly that run. We record **V5** (exact cover): when all occupied positions share one
subspace, `⟦σ_d⟧` contains no occupied-depth position outside `O(d)` — the span is a faithful
trace, "dense and contiguous," with the document forming "an unbroken sequence" (4/11). The
golden case confirms it: eleven characters of text report `1.1 for 0.11`, the half-open
interval `[1.1, 1.12)` covering exactly positions `1.1 … 1.11` (consultation Q15).

**Two subspaces: a bridging bounding box.** Now suppose `O(d)` holds both content
(`subspace = s_C`) and link (`subspace = s_L`) positions. Then `origin_d` is the content
start `[s_C,1,…]` (since `s_C < s_L`), but `max O(d)` is a link position `[s_L, …]`. The
reach crosses from subspace `s_C` into subspace `s_L`, so `⟦σ_d⟧` contains *every* position
between them — including the unoccupied void separating the two subspaces, where nothing is
arranged. We record **V6** (cross-subspace bounding box): when occupied positions span more
than one subspace, `O(d) ⊊ ⟦σ_d⟧` strictly — the span is a bounding box, not an exact cover,
and includes inter-subspace positions that carry no content. The golden case is stark: ten
characters plus one link report `1.1 for 1.2`, whose reach `[1,1] ⊕ [1,2] = [2,2]` bridges
from the text start straight across the gap into link space (consultation Q11, Q19).

A subtlety of depth must be settled here, because S8-depth permits distinct subspaces to
carry distinct depths (`m_C` for content, `m_L` for links). In the cross-subspace case
`origin_d` is a depth-`m_C` content position while `reach_d = shift(max O(d), 1)` is a
depth-`m_L` link position (OrdinalShift preserves depth), so when `m_C ≠ m_L` the span is
*not* level-uniform. The covering argument (V2) was proved without level-uniformity and so
still holds; what changes is only the *reach*: by the V2 case analysis, `reach(σ_d) = reach_d`
exactly when `#origin_d ≤ #reach_d` (i.e. `m_C ≤ m_L`), while when `m_C > m_L` the actual
reach `r⋆` strictly exceeds `reach_d` (it is `reach_d` zero-padded to depth `m_C`). In all
cases `r⋆ ≥ reach_d > max O(d)`, so the bounding-box reading of V6 stands. The implementation
evidence settles which case actually arises: content and link V-positions are *always* placed
at the same depth — both depth 2 — distinguished only by the first-component value `s_C = 1`
vs `s_L = 2`, never by depth (consultation Q2: `findvsatoappend`, `findnextlinkvsa`, and
`setlinkvsas` all emit depth-2 V-addresses). So `m_C = m_L` in every realized state, the
cross-subspace span is level-uniform, and `reach(σ_d) = reach_d` exactly. We treat the
`m_C ≠ m_L` divergence as an abstract possibility S8-depth admits but the implementation
never exercises; the well-formedness (V2, V17) and covering (V2) claims hold either way, and
only the V3 tightness claim is stated for the level-uniform reach that the uniform-depth
discipline guarantees.

This is not a defect peculiar to one engine. It is a *theorem about single spans*. A span
is by construction one contiguous region (ASN-0053 S0, convexity): "if you want to designate
a separated series of items exactly, including nothing else, you do this by a span-set, which
is a series of spans" (4/25). A document occupying two disjoint subspaces is a *separated
series*; no single span can trace it exactly. Any implementation that answers with one
origin-and-extent pair must, of necessity, bridge the gap. Recovering the per-subspace
extents exactly requires a span-*set* — a different operation, out of scope here. We record
the structural fact as **V7** (single-span contiguity): the result is always one convex
region; fragmentation is unrepresentable in a single span, so a multi-subspace document is
reported by enclosure rather than by exact decomposition.

---

## The origin is permanent; the extent tracks quantity, not order

Nelson asks whether the origin must remain fixed for the life of the document, and answers
yes: the home position is permanent, "any address … may be specified by a permanent tumbler
address" (4/19), while only the extent and internal ordering shift under editing.

We can make this precise. While the content subspace is occupied, D-MIN pins
`min V_{s_C}(d) = [s_C,1,…,1]`, and since `s_C` is the least subspace identifier, this is
also `min O(d) = origin_d` whenever content is present. We record **V8** (origin
permanence): for every document state in which the content subspace is non-empty,
`origin_d = [s_C,1,…,1]`, invariant under all editing that leaves content present. Editing
relocates I-addresses and shuffles V-positions, but it never moves the start of the stream:
"the front-end application is unaware" of where bytes natively live (4/11), and the V-origin
holds steady at the canonical first position. The origin is the stable anchor against which
every other V-address is read.

The extent behaves oppositely. Nelson distinguishes *arrangement* (order) from *composition*
(quantity): "changing how content is arranged → extent unchanged; changing how much content
there is → extent changes." We record **V9** (extent tracks composition, not arrangement).
A pure rearrangement permutes `M(d)` while preserving `O(d) = dom(M(d))` — the occupied
positions remain the dense set `{[s,1,…,1,k]}` by D-SEQ; only the values `M(d)(v)` are
permuted. Since `σ_d` is a function of `O(d)` alone, the reported span is *identical* before
and after: reorder the document and its origin and extent do not move. This matches Nelson's
classification of rearrangement as a "Pure Vstream operation" that leaves the measured extent
fixed. Insertion and deletion, by contrast, change `O(d)` — but the effect on the extent
depends on *which subspace owns the maximum*, since the reach is anchored at `max O(d)`.
Consider inserting `n` content positions. When the content subspace is the maximal occupied
subspace — in particular when the link subspace is empty — the inserted positions extend the
dense content run, growing `max O(d)` by `n` ordinal steps and hence the extent by `n`, while
leaving `origin_d` untouched (insertion never falls below the canonical minimum). When the
link subspace is occupied, however, `max O(d)` is a *link* position `[s_L, …]` (since
`s_C < s_L`), and inserting content positions `[s_C, …]` — all strictly below every link
position — does not move `max O(d)` at all; `reach_d` and `extent_d` are therefore unchanged
by the content insertion. We record **V10** (insertion monotonicity, content-maximal case):
*when the content subspace is the maximal occupied subspace* (equivalently, the link subspace
is empty), an insertion of `n` content positions increases the extent by exactly `n` and
leaves the origin fixed; *when links occupy the maximum*, content insertion leaves both reach
and extent invariant (the new positions fall inside the existing bounding box). Gregory
confirms the content-maximal half directly — the arrangement-tree width grows by exactly the
inserted count while the reported start is unchanged across single and repeated insertions
(consultation Q16).

---

## Every document answers, including the empty one

Nelson asks whether some documents have undefined origin and extent. The answer is no — and
the empty document is the case that tests it. `CREATENEWDOCUMENT` "creates an empty document"
(4/65); a freshly created or fully emptied document has `O(d) = ∅`.

We record **V11** (total answerability via a distinguished empty result): `RETRIEVEDOCVSPAN`
is defined for every allocated document. When `O(d) = ∅`, the result is the *empty span-set*
`⟨⟩` (ASN-0053), the distinguished value denoting the empty set `∅`. We are careful here:
this is *not* the "zero-extent span." A T12 span `(s, ℓ)` requires `Pos(ℓ)` (Span/T12,
ASN-0034), and the zero tumbler fails `Pos`; worse, by TA6 (ZeroTumblers, ASN-0034) the zero
tumbler is excluded from valid addresses entirely. So a pair `(origin_d, 0)` is not a
well-formed span at all, and it cannot be returned as one without contradicting V0. The empty
span-set carries no origin and no extent: `origin_d = min O(d)` is *undefined* when `O(d) = ∅`
(the minimum of the empty set does not exist), and there is no extent tumbler. This is the
honest content of the empty case — there is no first occupied position, hence no origin to
report. Nelson's span model admits exactly this absence: "a span that contains nothing today
may at a later time contain a million documents" (4/25). Emptiness is a *valid state of the
address space*, not an undefined result; a document address with nothing stored against it —
a "ghost element" (4/23) — answers identically, with the empty span-set. Gregory's
implementation realizes the distinguished value by returning zeros for both displacement and
width when the arrangement tree holds no content, independent of any residual tree structure
left by prior deletions (consultation Q13). We read those zeros as a *sentinel* — an encoding
of "no origin, no extent" — and not as a legal tumbler: the zero tumbler is precisely the
value TA6 forbids as an address. So the only sense in which the origin can fail to coincide
with occupied content is the empty case, where there is no content to coincide with and no
origin at all — and that case is answered with `⟨⟩`, not refused.

---

## What the caller learns beyond the name

The point of the operation is that it discloses something the identity alone does not.
A document's identity is its tumbler `N.0.U.0.D`: a pure locator. It tells you *where* the
document sits and *who* owns it — "you always know where you are" (2/40) — but "tumblers …
impose no categorization and no structure on the contents of a document" (4/17–4/18). The
identity says the document exists and names its place; it says nothing about how much is
currently in it.

We record **V12** (information gain): from `σ_d` the caller learns two facts not derivable
from `d`'s identity — the *live origin* (the addressing anchor for every subsequent V-address
operation on the document) and the *current extent* (the present bounds of the arrangement,
i.e. how far the live V-stream reaches *now*). Because the V-stream "may be continually
altered by editorial operations" (4/30) while the address `d` stays permanent, the span
reflects the document's *current shape* — the operational bounds a caller needs before
issuing any positioned request. Identity is static and structural; the span is dynamic and
quantitative.

---

## Independence, permanence, and stability

Three faithfulness questions remain, all about how the report relates to *other* state.

**Per-document independence.** Suppose two documents `d₁` and `d₂` share content — the same
I-address occupies a position in each. We record **V13** (independence): `σ_{d₁}` depends
only on `O(d₁) = dom(M(d₁))`, and `σ_{d₂}` only on `O(d₂)`; neither defers to, inherits from,
or is altered by the other. Shared content is referenced once in the store but belongs fully
to each document's own arrangement: a transcluded position "has an ordinal position in the
byte stream just as if it were native" (4/11) and counts toward *that* document's extent. So
`RETRIEVEDOCVSPAN(d₁)` and `RETRIEVEDOCVSPAN(d₂)` report distinct, independently computed
spans even over identical content — "no arrangement … is a priori better than other
arrangements" (2/19), and each document answers for its own bounds on its own terms.

**Permanence of the underlying content.** We record **V14** (permanence): every position the
span covers maps, through `M(d)`, to a permanent I-address in `dom(C)` (S3), and that content
is immutable and never destroyed (S0, P0). The arrangement (Vstream) is fluid; the content
identities it references are eternal. So even when the originating owner "deletes" content
from this document's current version, "those bytes remain in all other documents where they
have been included" (4/11) — sharing strengthens rather than threatens the permanence of what
any reported span ultimately denotes.

**Snapshot stability and determinism.** The returned span is a *value*, fixed at the instant
of the query. We record **V15** (snapshot stability): a span returned at state `Σ` continues
to denote the bounds it denoted then; a later edit to `d` — or to any document supplying `d`'s
transcluded content — does not retroactively alter the already-returned value. A subsequent
report against the edited state is a *fresh* query, not a mutation of the old answer. And the
report is deterministic: we record **V16** (determinism): `σ_d` is a pure function of `O(d)`,
so two queries against an unchanged arrangement return identical spans. Gregory grounds both
— the reported bounds are computed from a width summary that the arrangement tree maintains
*independent of the physical tree's shape* (enfilade confluence), so the answer depends only
on the logical arrangement, never on how the structure was built or rebalanced (consultation
Q14).

---

## The extent is a well-formed, non-negative displacement

Finally, the invariants that constrain the span the operation may return. We record **V17**
(well-formed positive extent): for a non-empty document, `extent_d` is a positive tumbler
(`Pos(extent_d)`) with `actionPoint(extent_d) ≤ #origin_d`, so `σ_d` is a legal T12 span; and
the span is non-empty, containing at least `origin_d` (TA-strict). In particular the width
tumbler can never have "negative magnitude": `reach_d > origin_d` always (V2), so
`extent_d = reach_d ⊖ origin_d` is a genuine positive displacement, never a degenerate or
sign-reversed value. Gregory confirms this is structurally guaranteed: even when prior
deletions drive intermediate arrangement entries to negative displacements, the root width is
recomputed as a maximum-minus-minimum reach and remains non-negative — the reported extent is
never negative (consultation Q18). For every non-empty document the extent is strictly
positive; there is no editing artifact that drives it to zero. The only way to obtain "no
extent" is the empty document, which returns the distinguished empty span-set `⟨⟩` (V11) and
carries no extent tumbler at all — emptiness is reported by the absence of a span, not by a
zero-width one. We note V17's `Pos` and `actionPoint` claims hold *without* assuming
level-uniformity (established in the V2 well-formedness paragraph via D0); level-uniformity is
needed only for `reach(σ_d) = reach_d` exactly, not for T12 legality.

---

## A worked report

Take the document `d = [1.0.1.0.5]` (a document-level tumbler, `zeros(d) = 2`). Give its
content subspace three positions and its link subspace one:

> `M(d) = { [1,1] ↦ a, [1,2] ↦ b, [1,3] ↦ a, [2,1] ↦ ℓ }`,

where `a, b` are content I-addresses and `ℓ` is a link I-address. The occupied set is
`O(d) = {[1,1], [1,2], [1,3], [2,1]}`, totally ordered by T1 as written (since `1 < 2` at the
first component).

Compute the span. `origin_d = min O(d) = [1,1]`. `max O(d) = [2,1]`, so
`reach_d = shift([2,1], 1) = [2,2]`. The extent is `[2,2] ⊖ [1,1]`: the tumblers first differ
at position 1 (`2 ≠ 1`), so `extent_d = [2-1, 2] = [1,2]`. Thus

> `RETRIEVEDOCVSPAN(d) = ([1,1], [1,2])`,  i.e. "1.1 for 1.2".

Verify the claims. **V1**: `origin_d = [1,1] ∈ O(d)`, an occupied content position. ✓
**V2**: `⟦σ_d⟧ = {t : [1,1] ≤ t < [2,2]}` contains all four occupied positions. ✓
**V6**: it *also* contains `[1,4], [1,5], …` and `[1, k]`-extensions in the inter-subspace
void, none occupied — the span strictly encloses `O(d)`. ✓ **V17**: `extent_d = [1,2]` is
positive with `actionPoint = 1 ≤ 2 = #origin_d`. ✓

Now drop the link, leaving `O'(d) = {[1,1], [1,2], [1,3]}`. Then `origin_d = [1,1]` (V8,
unchanged), `max = [1,3]`, `reach = [1,4]`, `extent = [1,4] ⊖ [1,1] = [0,3]`, giving
`([1,1], [0,3])` — "1.1 for 0.3", an exact cover of three contiguous positions (V5), with the
origin fixed exactly where it was (V8). Reordering these three positions — permuting which
I-address sits at each — leaves `O'(d)` unchanged and so returns the identical span (V9).

**A non-level-uniform variant.** To exercise the abstract case S8-depth permits but the
implementation never realizes (V6), let content sit at depth `m_C = 3` and the single link at
depth `m_L = 2`:

> `M(d) = { [1,1,1] ↦ a, [1,1,2] ↦ b, [2,1] ↦ ℓ }`,  `O(d) = {[1,1,1], [1,1,2], [2,1]}`.

Then `origin_d = [1,1,1]` (depth 3) and `max O(d) = [2,1]`, so `reach_d = shift([2,1], 1) =
[2,2]` (depth 2). Here `#origin_d = 3 > 2 = #reach_d`, so the span is *not* level-uniform.
The extent is `[2,2] ⊖ [1,1,1]`: zero-padding `reach_d` to `[2,2,0]` and diverging at
position 1 (`2 ≠ 1`), `extent_d = [2-1, 2, 0] = [1,2,0]` — a positive tumbler with
`actionPoint = 1 ≤ 3 = #origin_d`, so V17/WF still hold. The *actual* reach is
`r⋆ = origin_d ⊕ extent_d = [1+1, 2, 0] = [2,2,0]`, which by D0 is *not* `reach_d`: indeed
`reach_d = [2,2]` is a proper prefix of `r⋆ = [2,2,0]`, so `reach_d < r⋆` (T1 case (ii)).
Coverage nonetheless holds: `⟦σ_d⟧ = {t : [1,1,1] ≤ t < [2,2,0]}` contains `[1,1,1]`,
`[1,1,2]`, and `[2,1]` (each strictly below `[2,2,0]`). So even with `m_C ≠ m_L`, **V2** is
satisfied — the span covers `O(d)` — while the reach overshoots `reach_d` and the **V3**
tightness claim (least *same-depth* reach) no longer applies, exactly as the restricted
statements anticipate. This confirms that coverage and T12 legality survive depth divergence;
only exact reach and tightness depend on the uniform-depth discipline.

---

## Preconditions and well-definedness

For the report to be defined we require:

1. `d ∈ dom(M)` — the document is allocated (M0, M1). An unallocated identity names no
   arrangement and has nothing to report.
2. The caller may read `d`. Gregory's implementation gates the operation on the document
   being open in the caller's session (a BERT check), failing the request otherwise rather
   than returning a span (consultation Q17). Abstractly this is an *access* precondition: the
   operation reports only on a document the caller is entitled to observe. It does not change
   the value reported, only whether the report is produced.

Under precondition 1 the result is total: by S8-fin the occupied set is finite, so its
minimum and maximum (when non-empty) exist and the span is computed by V1–V2; when empty the
result is the distinguished empty span-set `⟨⟩` (V11), carrying no origin and no extent. No
further argument is needed — the operation consumes no caller-supplied position, so there is
no range to validate.

---

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| V0 | `RETRIEVEDOCVSPAN(d)` returns one well-formed span `σ_d = (origin_d, extent_d)` for a non-empty document, or the distinguished empty span-set `⟨⟩` (denoting `∅`, not a T12 span) when `O(d) = ∅` — never a content sequence, never a count | introduced |
| V1 | When `O(d) ≠ ∅`, `origin_d = min O(d)` under T1 and `origin_d ∈ O(d)` (the origin is an occupied position) | introduced |
| V2 | `O(d) ⊆ ⟦σ_d⟧` (coverage), proved unconditionally via D0/D1 without assuming level-uniformity; the actual reach `r⋆ = origin_d ⊕ extent_d ≥ reach_d = shift(max O(d), 1) > max O(d)`, with equality `r⋆ = reach_d` iff `#origin_d ≤ #reach_d`; the span `(origin_d, extent_d)` is always a well-formed T12 span | introduced |
| V3 | `origin_d` is the greatest lower bound of `O(d)`; `reach_d` is the least strict upper bound of `max O(d)` *among same-depth tumblers* (the deeper zero-extension `max O(d).0` is a smaller upper bound but breaks level-uniformity) — so `σ_d` is the tightest *level-uniform* covering span | introduced |
| V4 | `extent_d` is computed from `O(d) = dom(M(d))` alone; content in `dom(C)` but absent from the arrangement (deleted, or native elsewhere) contributes nothing (Vstream-bounded, not Istream) | introduced |
| V5 | When all occupied positions share one subspace, `⟦σ_d⟧` contains no occupied-depth position outside `O(d)` (exact cover of a contiguous run) | introduced |
| V6 | When occupied positions span more than one subspace, `O(d) ⊊ ⟦σ_d⟧` — the span bridges the inter-subspace void (bounding box, not exact cover); the span is level-uniform whenever the subspaces share a depth (`m_C = m_L`, the case the implementation always realizes per consultation Q2), and coverage holds even when `m_C ≠ m_L` | introduced |
| V7 | The result is always one convex region; fragmentation is unrepresentable in a single span, so multi-subspace documents are reported by enclosure (single-span contiguity) | introduced |
| V8 | While the content subspace is non-empty, `origin_d = [s_C,1,…,1]`, invariant under all editing that leaves content present (origin permanence) | introduced |
| V9 | `σ_d` is a function of `O(d)` alone; pure rearrangement preserves `O(d)` and returns the identical span (extent tracks composition, not arrangement) | introduced |
| V10 | When the content subspace is maximal (link subspace empty), inserting `n` content positions increases the extent by exactly `n` and leaves the origin fixed; when links occupy the maximum, content insertion leaves reach and extent invariant (insertion monotonicity, content-maximal case) | introduced |
| V11 | The operation is total over allocated documents; `O(d) = ∅` yields the distinguished empty span-set `⟨⟩` (not a T12 span), with `origin_d` undefined and no extent — the implementation's zeros are a sentinel, not a legal address (TA6) | introduced |
| V12 | The span discloses the live origin (addressing anchor) and current extent (present bounds) — neither derivable from `d`'s identity (information gain) | introduced |
| V13 | `σ_d` depends only on `O(d)`; two documents sharing content report independent spans; transcluded positions count toward the borrowing document's extent (independence) | introduced |
| V14 | Every position the span covers maps through `M(d)` to a permanent, immutable I-address (S3, S0, P0); sharing preserves what the span denotes (permanence) | introduced |
| V15 | A returned span keeps its meaning under later edits to `d` or to home documents supplying its content; a fresh report is a new query, not a mutation (snapshot stability) | introduced |
| V16 | `σ_d` is a pure function of `O(d)`; equal arrangements return identical spans, independent of how the arrangement was built (determinism) | introduced |
| V17 | For non-empty `d`, `extent_d` is a positive tumbler with `actionPoint(extent_d) ≤ #origin_d` (well-formed T12 span); `reach_d > origin_d` always, so the extent is never negative | introduced |

## Open Questions

What must a span-valued report guarantee so that the per-subspace extents of a multi-subspace document are recoverable exactly, given that a single span can only enclose disjoint subspaces rather than trace them?

What invariant must relate the reported extent to the count of occupied positions, given that a span designates boundaries and explicitly not a cardinality?

Under what conditions must the reported origin be the document's permanent tumbler identity rather than the minimum occupied V-position, and when do these coincide?

What faithfulness must a report of a designated historical version preserve relative to a report of the present arrangement of the same document?

What invariant must relate the whole-document span to the bounding spans of the document's individual correspondence runs, so that the global extent composes from local ones?

What must the report guarantee about origin and extent when content occupies V-positions whose addressing arithmetic has been driven outside the well-formed range by prior editing?
