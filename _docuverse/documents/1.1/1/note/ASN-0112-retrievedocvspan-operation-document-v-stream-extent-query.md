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

We therefore take the result to be a single span `σ_d = (origin_d, extent_d)`. We record
this as **V0** (span-valued result): `RETRIEVEDOCVSPAN(d)` returns one well-formed span,
never a content sequence and never a cardinality. The caller reads `origin_d` to learn
where the V-stream begins and `extent_d` to learn how far it reaches; the content itself,
and any per-piece count, are the business of other operations.

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

**The span covers every occupied position.** We record **V2** (covering):
`O(d) ⊆ ⟦σ_d⟧`. For any `v ∈ O(d)` we have `origin_d = min O(d) ≤ v` and
`v ≤ max O(d) < shift(max O(d), 1) = reach_d` (TS4, ShiftStrictIncrease), so
`origin_d ≤ v < reach_d`, i.e. `v ∈ ⟦σ_d⟧`. The extent is well-defined: `reach_d > max O(d)
≥ origin_d` gives `reach_d > origin_d`, so `extent_d = reach_d ⊖ origin_d` is a positive
tumbler (TumblerSub), and the span `(origin_d, extent_d)` is well-formed with reach
`reach_d` (WF, ASN-0053, in the level-uniform case where `#origin_d = #reach_d`).

**The span is the tightest covering bound.** We record **V3** (bounding):
`origin_d` is the greatest lower bound and `reach_d` the least admissible upper bound of the
occupied set under the document's ordinal convention. Any span `σ'` with `O(d) ⊆ ⟦σ'⟧`
satisfies `start(σ') ≤ origin_d` (because `start(σ') ≤ min O(d)`) and
`reach(σ') > max O(d)` (because the half-open interval must contain `max O(d)`), hence
`reach(σ') ≥ reach_d` under the convention that ordinal positions advance one step at a
time. So `σ_d` sits inside every covering span: it is the bounding span of `O(d)`. This is
the formal core of Nelson's claim that origin and extent "describe the document as a whole"
*implicitly* — "there is no choice as to what lies between; this is implicit in the choice
of first and last point" (4/25). Fix the two boundaries and the whole is determined.

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
fixed. Insertion and deletion, by contrast, change `O(d)`: inserting `n` positions extends
the dense run, growing `max O(d)` by `n` ordinal steps and hence the extent by `n`, while
leaving `origin_d` untouched (insertion never falls below the canonical minimum). We record
**V10** (insertion monotonicity): an insertion of `n` content positions increases the extent
by exactly `n` and leaves the origin fixed. Gregory confirms both halves directly — the
arrangement-tree width grows by exactly the inserted count while the reported start is
unchanged across single and repeated insertions (consultation Q16).

---

## Every document answers, including the empty one

Nelson asks whether some documents have undefined origin and extent. The answer is no — and
the empty document is the case that tests it. `CREATENEWDOCUMENT` "creates an empty document"
(4/65); a freshly created or fully emptied document has `O(d) = ∅`.

We record **V11** (total answerability with zero-extent degenerate case): `RETRIEVEDOCVSPAN`
is defined for every allocated document. When `O(d) = ∅`, the result is the *zero-extent
span* — an origin with `extent_d = 0` (the zero tumbler) — a degenerate but perfectly
well-defined span. Nelson's span model admits exactly this: "a span that contains nothing
today may at a later time contain a million documents" (4/25). Emptiness is a *valid state of
the address space*, not an undefined result. A document address with nothing stored against
it — a "ghost element" (4/23) — answers identically: origin defined by position, extent
zero. Gregory's implementation returns zeros for both displacement and width when the
arrangement tree holds no content, independent of any residual tree structure left by prior
deletions (consultation Q13). So the only sense in which the origin can fail to coincide with
occupied content is the empty case, where there is no content to coincide with — and that
case is answered, not refused.

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
never negative (consultation Q18). The extent reaches zero only in the empty case (V11), never
through editing artifacts.

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
result is the zero-extent span (V11). No further argument is needed — the operation consumes
no caller-supplied position, so there is no range to validate.

---

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| V0 | `RETRIEVEDOCVSPAN(d)` returns one well-formed span `σ_d = (origin_d, extent_d)` — never a content sequence, never a count | introduced |
| V1 | When `O(d) ≠ ∅`, `origin_d = min O(d)` under T1 and `origin_d ∈ O(d)` (the origin is an occupied position) | introduced |
| V2 | `O(d) ⊆ ⟦σ_d⟧` with `reach_d = shift(max O(d), 1) > max O(d)` (the span covers every occupied position) | introduced |
| V3 | `σ_d` sits inside every span covering `O(d)` — it is the tightest bounding span (origin = greatest lower bound, reach = least admissible upper bound) | introduced |
| V4 | `extent_d` is computed from `O(d) = dom(M(d))` alone; content in `dom(C)` but absent from the arrangement (deleted, or native elsewhere) contributes nothing (Vstream-bounded, not Istream) | introduced |
| V5 | When all occupied positions share one subspace, `⟦σ_d⟧` contains no occupied-depth position outside `O(d)` (exact cover of a contiguous run) | introduced |
| V6 | When occupied positions span more than one subspace, `O(d) ⊊ ⟦σ_d⟧` — the span bridges the inter-subspace void (bounding box, not exact cover) | introduced |
| V7 | The result is always one convex region; fragmentation is unrepresentable in a single span, so multi-subspace documents are reported by enclosure (single-span contiguity) | introduced |
| V8 | While the content subspace is non-empty, `origin_d = [s_C,1,…,1]`, invariant under all editing that leaves content present (origin permanence) | introduced |
| V9 | `σ_d` is a function of `O(d)` alone; pure rearrangement preserves `O(d)` and returns the identical span (extent tracks composition, not arrangement) | introduced |
| V10 | Inserting `n` content positions increases the extent by exactly `n` and leaves the origin fixed (insertion monotonicity) | introduced |
| V11 | The operation is total over allocated documents; `O(d) = ∅` yields the zero-extent span (empty document answers, with defined origin and zero extent) | introduced |
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
