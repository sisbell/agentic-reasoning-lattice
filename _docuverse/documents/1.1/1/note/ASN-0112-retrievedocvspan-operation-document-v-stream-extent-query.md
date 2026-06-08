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
- **S3★** (generalized referential integrity, ASN-0047): each occupied V-position maps
  into the store appropriate to its subspace —
  `(A v : v ∈ O(d) : subspace(v) = s_C ⟹ M(d)(v) ∈ dom(C)) ∧ (A v : v ∈ O(d) : subspace(v) = s_L ⟹ M(d)(v) ∈ dom(L))`.
- **S3★-aux** (subspace exhaustiveness, ASN-0047): every occupied V-position carries one
  of exactly two subspaces — `(A v : v ∈ O(d) : subspace(v) = s_C ∨ subspace(v) = s_L)`.
  There is no third subspace, so an arrangement occupies the content subspace, the link
  subspace, both, or neither.
- **S8-fin** (finiteness): `O(d)` is finite.
- **S8a** (well-formedness): every `v ∈ O(d)` is zero-free, of depth `≥ 2`, all
  components positive; `subspace(v) = v₁`.
- **S8-depth**: within one subspace all occupied V-positions share a common depth.
- **D-CTG★ / D-MIN★ / D-SEQ★** (per-subspace shape, ASN-0047): for *each* non-empty
  subspace `S ∈ {s_C, s_L}`, the positions `V_S(d) = {v ∈ O(d) : subspace(v) = S}` are
  contiguous, their minimum is the canonical `[S,1,…,1]`, and they form the dense run
  `{[S,1,…,1,k] : 1 ≤ k ≤ n_S}` for some `n_S ≥ 1`. We write the content instance
  `D-MIN`/`D-SEQ` for `S = s_C` and the link instance for `S = s_L`; both inherit the same
  dense-run shape.
- **S0 / P0** (content immutability and permanence): once `a ∈ dom(C)`, `a` stays in
  `dom(C)` forever and `C(a)` never changes.
- **L12** (link immutability, ASN-0043): once `a ∈ dom(L)`, `a` stays in `dom(L)` forever
  and the link value `L(a)` never changes — the link-store analogue of S0/P0.

Two subspaces inhabit the arrangement: content positions carry `subspace = s_C` and link
positions carry `subspace = s_L`, with the fixed convention `s_C = 1`, `s_L = 2`
(SubspaceConventionAxiom). Because `s_C < s_L` at the first component, T1 places every
content position before every link position.

We borrow the span machinery wholesale. A span `σ = (s, ℓ)` denotes the half-open interval
`⟦σ⟧ = {t ∈ T : s ≤ t < s ⊕ ℓ}` (T12), with `reach(σ) = s ⊕ ℓ` (ASN-0053). A span is
*well-formed* when `Pos(ℓ)` and `actionPoint(ℓ) ≤ #s`; it is *level-uniform* when
`#s = #ℓ` (S6, ASN-0053). The ordinal shift `shift(t, n) = t ⊕ δ(n, #t)` advances `t`'s last
component by `n` (ASN-0034).

---

## What the caller must be handed

Before specifying the operation we must fix the *type* of its result. Nelson fixes it for
us: a span, "the origin and extent of the V-stream" (4/68). Not a sequence of records — that
would be a content read. Not a count: "a tumbler-span is not a conventional number, and it
does not designate the number of bytes contained. It does not designate a number of
anything" (4/24). The result is a *boundary description* — two tumblers, a start and a
width, whose meaning is "from here, this far," with everything between implicit (4/25).

We therefore fix the result type *once and explicitly*: the operation returns either one
well-formed span or a distinguished empty value — never a content sequence, never a
cardinality. We record this as **V0** (span-or-empty result), the tagged union

> `RETRIEVEDOCVSPAN : dom(M) → Span + {⟨⟩}`,

where `Span` is the type of T12 spans (a pair `(s, ℓ)`) and `⟨⟩` is the empty span-set of
ASN-0053, the distinguished value denoting `∅`. For a non-empty document `RETRIEVEDOCVSPAN(d)`
returns one well-formed span `σ_d = (origin_d, extent_d)`; for an empty document
(`O(d) = ∅`) it returns `⟨⟩`. The two summands are genuinely distinct: `⟨⟩` cannot be a
degenerate span, because no T12 span can denote `∅` (S2, ASN-0053: every well-formed span is
non-empty).

The caller reads `origin_d` to learn where the V-stream begins and `extent_d` to learn how far it
reaches; the content itself, and any per-piece count, are the business of other operations.

---

## The bounding span and its two endpoints

Nelson's intent is that origin and extent describe the document as a whole implicitly —
"there is no choice as to what lies between; this is implicit in the choice of first and last
point" (4/25). Reasoning from "origin and extent of the V-stream," we must produce a span that
*spans the whole document* — one region containing all of its arranged content. The occupied set
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
satisfies `k ≤ #origin_d` in every case: in the single-subspace case both tumblers lie in one
subspace `s` (content or link), so by S8-depth they share the common depth of that subspace —
`#origin_d = #max O(d) = #reach_d` (OrdinalShift preserves depth) — and the first divergence of
two equal-length tumblers cannot exceed their shared length, giving `k ≤ min(#origin_d, #reach_d)
= #origin_d`; in the cross-subspace case they differ already at position 1 (`s_C` vs `s_L`), so
`k = 1 ≤ #origin_d`. By D0 (DisplacementWellDefined, ASN-0034) — applicable because `origin_d <
reach_d` and `divergence(origin_d, reach_d) ≤ #origin_d` — the displacement `extent_d =
reach_d ⊖ origin_d` is a positive tumbler with `actionPoint(extent_d) = k ≤ #origin_d`. Hence
`(origin_d, extent_d)` satisfies T12 and is a well-formed span.

**The span covers every occupied position.** We record **V2** (covering): `O(d) ⊆ ⟦σ_d⟧`.
The denotation is `⟦σ_d⟧ = {t : origin_d ≤ t < origin_d ⊕ extent_d}`, so we must locate the
*actual* reach `r⋆ = origin_d ⊕ extent_d` and show `max O(d) < r⋆`. Two cases on the relative
depths:

- *`#origin_d ≤ #reach_d`* (in particular the case `#origin_d = #reach_d`, i.e. `level_compat(origin_d, reach_d)`). By
  D1 (DisplacementRoundTrip, ASN-0034) the round-trip closes exactly: `r⋆ = origin_d ⊕
  (reach_d ⊖ origin_d) = reach_d`. Then for any `v ∈ O(d)`, `origin_d ≤ v ≤ max O(d) <
  reach_d = r⋆`, so `v ∈ ⟦σ_d⟧`.
- *`#origin_d > #reach_d`* (content deeper than the maximal link position). Unequal endpoint
  depths force the cross-subspace case — single-subspace endpoints are equidepth by S8-depth —
  so `k = divergence(origin_d, reach_d) = 1` (divergence at the subspace component, `s_C` vs
  `s_L`). By D0 the round-trip *fails* — `r⋆ ≠ reach_d` — so we compute `r⋆` directly. With
  `k = 1`, TumblerAdd gives `r⋆` agreeing with `reach_d` (zero-padded to length `#origin_d`) on every position
  `1 ≤ i ≤ #reach_d` and carrying trailing zeros beyond, so `reach_d` is a proper prefix of
  `r⋆` and `reach_d < r⋆` (T1 case (ii)). Hence `max O(d) < reach_d < r⋆`, and again every
  `v ∈ O(d)` lies in `⟦σ_d⟧`.

In both cases `r⋆ ≥ reach_d > max O(d)`, so coverage holds. What the endpoint relation governs is
only the *reach*: the **reach biconditional** `reach(σ_d) = reach_d ⟺ #origin_d ≤ #reach_d`
(D1 closes the round-trip when `#origin_d ≤ #reach_d`; D0 makes it fail when
`#origin_d > #reach_d`). The reach equals `reach_d` whenever the occupied subspaces share a
common depth.

**The span is the tightest covering bound among same-depth reaches.** We record **V3**
(bounding): `origin_d` is the greatest lower bound of `O(d)`, and `reach_d` is the *least*
admissible upper bound of `max O(d)` among tumblers of its depth — dropping the same-depth
qualifier makes the claim false, since the deeper zero-extension `max O(d).0` is a smaller
upper bound. The lower bound is unconditional: any span `σ'` with `O(d) ⊆ ⟦σ'⟧` satisfies
`start(σ') ≤ min O(d) = origin_d`. The upper bound requires an argument. Write `w = max O(d)`.
Because every V-position is zero-free with all components positive (S8a), the rightmost nonzero
component of `w` is its last, so `sig(w) = #w` (TA5-SIG, ASN-0034); hence
`reach_d = shift(w, 1) = w ⊕ δ(1, #w)` coincides with `inc(w, 0)`, since OrdinalShift
(ASN-0034) advances the same last component that `inc(·, 0)` modifies at `sig(w)`. ASN-0034's
TA5 (HierarchicalIncrement) settles the tightness directly: `inc(w, 0)` is the smallest
same-length tumbler strictly greater than `w`, while the true T1-immediate successor of `w` is
the deeper zero-extension `w.0` (by the prefix convention, T1 case (ii)), satisfying
`w < w.0 < inc(w, 0) = reach_d`. So `reach_d` is *not* the least admissible reach over all of
`T` (a span with reach `w.0` already covers `O(d)`), but it is the least strict upper bound of
`w` at `w`'s depth — V3's claim. Whether `σ_d`'s own reach attains `reach_d` is governed by the
V2 reach biconditional.

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
store has ever held*.

The relationship the extent must bear to the arrangement is therefore one of *current
correspondence*: by V2 the span covers every occupied position, and by V4 it draws its
endpoints from no other source. For a document whose occupied positions lie in a single
subspace, this correspondence is *exact*.

---

## Exact cover within a subspace; a bounding box across subspaces

The decisive structural question is whether the single returned span exactly traces the
occupied content or merely encloses it. The answer depends on how many subspaces the
arrangement occupies, and the divergence is not an implementation artifact — it is forced
by the demand for *one* origin-and-extent pair. By S3★-aux a non-empty `O(d)` occupies
exactly one subspace or exactly both, so the two cases below are jointly exhaustive.

**Single subspace: exact cover.** Suppose `O(d)` lies entirely in one subspace `s` — either
content (`s = s_C`) or, in the link-only case (content empty, one or more links arranged,
reachable by `CREATENEWDOCUMENT` then `K.λ` + `K.μ⁺_L` with endsets referencing content
elsewhere per L4/L9), the link subspace (`s = s_L`). By D-SEQ★ (the per-subspace dense-run
shape, ASN-0047, instantiated at `S = s`) the occupied positions are
`{[s,1,…,1,k] : 1 ≤ k ≤ n_s}`, a dense run with no internal gaps. Then `origin_d = [s,1,…,1]`
(D-MIN★), `max O(d) = [s,1,…,1,n_s]`, `reach_d = [s,1,…,1,n_s+1]`, and `⟦σ_d⟧` restricted to
depth-`m_s` positions of subspace `s` is exactly that run — D-CTG★ rules out any occupied-depth
position of `s` lying between `origin_d` and `reach_d` but outside the run. We record **V5**
(exact cover): when all occupied positions share one subspace, `⟦σ_d⟧` contains no
occupied-depth position outside `O(d)` — the span is a faithful trace, "dense and contiguous,"
with the document forming "an unbroken sequence" (4/11). The density is supplied by the
per-subspace D-SEQ★, so the claim holds for a link-only document exactly as for a content-only
one. The golden case confirms the content instance: eleven characters of text report
`1.1 for 0.11`, the half-open interval `[1.1, 1.12)` covering exactly positions
`1.1 … 1.11` (consultation Q15).

**Two subspaces: a bridging bounding box.** Now suppose `O(d)` holds both content
(`subspace = s_C`) and link (`subspace = s_L`) positions. Then `origin_d` is the content
start `[s_C,1,…]` (since `s_C < s_L`), but `max O(d)` is a link position `[s_L, …]`. The
reach crosses from subspace `s_C` into subspace `s_L`, so `⟦σ_d⟧` contains *every* position
between them — including the unoccupied void separating the two subspaces, where nothing is
arranged. We record **V6** (cross-subspace bounding box): when occupied positions span more
than one subspace, `O(d) ⊊ ⟦σ_d⟧` strictly — the span is a bounding box, not an exact cover,
and includes inter-subspace positions that carry no content. The enclosure is forced rather
than incidental: a span denotes one convex region (`⟦σ_d⟧` is order-convex under T1, ASN-0053
S0), and a document occupying two disjoint subspaces is a *separated series* — "if you want to
designate a separated series of items exactly, including nothing else, you do this by a
span-set, which is a series of spans" (4/25). Fragmentation is unrepresentable in a single
span, so a multi-subspace document can only be reported by enclosure, never by exact
decomposition. The golden case is stark: ten
characters plus one link report `1.1 for 1.2`, whose reach `[1,1] ⊕ [1,2] = [2,2]` bridges
from the text start straight across the gap into link space (consultation Q11, Q19).

The bounding-box reading of V6 holds independent of the endpoint depth relation (V2). The
implementation in fact realizes only `m_C = m_L`: content and link V-positions are placed at the same depth — both
depth 2 — distinguished only by the first-component value `s_C = 1` vs `s_L = 2`, never by depth
(consultation Q2: `findvsatoappend`, `findnextlinkvsa`, and `setlinkvsas` all emit depth-2
V-addresses), so the cross-subspace endpoints are level-compatible and `reach(σ_d) = reach_d`
exactly.

---

## The origin is permanent; the extent tracks quantity, not order

The origin remains fixed for the life of the document: the home position is permanent, "any
address … may be specified by a permanent tumbler address" (4/19), while only the extent and
internal ordering shift under editing.

We can make this precise. While the content subspace is occupied, D-MIN pins
`min V_{s_C}(d) = [s_C,1,…,1]`, and since `s_C` is the least subspace identifier, this is
also `min O(d) = origin_d` whenever content is present. We record **V8** (origin
permanence): for every document state in which the content subspace is non-empty,
`origin_d = [s_C,1,…,1]`, invariant under all editing that leaves content present. (The depth
`m_C` is fixed throughout any content-present regime, by S8-depth.) Editing
relocates I-addresses and shuffles V-positions, but it never moves the start of the stream:
"the front-end application is unaware" of where bytes natively live (4/11), and the V-origin
holds steady at the canonical first position. The origin is the stable anchor against which
every other V-address is read.

The extent behaves oppositely. Nelson distinguishes *arrangement* (order) from *composition*
(quantity): "changing how content is arranged → extent unchanged; changing how much content
there is → extent changes." We record **V9** (extent tracks composition, not arrangement).
A pure rearrangement permutes `M(d)` while preserving `O(d) = dom(M(d))` — the occupied
positions remain the dense set `{[s,1,…,1,k]}` by D-SEQ; only the values `M(d)(v)` are
permuted. Since `origin_d = min O(d)` and `extent_d = shift(max O(d), 1) ⊖ origin_d` depend
on `O(d)` alone — never on the values `M(d)(v)` — the reported span is *identical* before and
after: reorder the document and its origin and extent do not move. This matches
Nelson's classification of rearrangement as a "Pure Vstream operation" that leaves the measured
extent fixed.

One edit consequence is specific to this query, because it *bounds V8*. V8's origin permanence
is asserted *while content is present* — that hypothesis is exactly the boundary, and the origin
moves precisely at the transitions that change whether the content subspace is occupied. There
are two such transitions, symmetric across the content/link boundary. We record **V18** (origin
migration bounds V8). *Content-clearing*: deletion empties the content subspace
(`V_{s_C}(d) = ∅`) while one or more links survive (`V_{s_L}(d) ≠ ∅`); the document is *not*
empty (V11 does not fire), but V8's hypothesis fails and `origin_d` migrates *up* from the
content anchor `[s_C,1,…,1]` to the link minimum `[s_L,1,…,1]` (D-MIN★ at `S = s_L`).
*First-content insertion*: into a link-only document (V5), where `origin_d = [s_L,1,…,1]`,
inserting the first content position occupies `[s_C,1,…,1]`, and since `s_C < s_L` the origin
migrates *down* to the content anchor `[s_C,1,…,1]`, restoring V8's regime (D-MIN★ at
`S = s_C`). Every other editing transition leaves the content-occupancy status unchanged and so
fixes the origin. Gregory confirms the content-clearing case: deleting all text while links
remain is a permitted, non-empty state reporting the link span (`2.1 for 0.1` in the golden
link-only configuration), not the empty result (deletion consultation).

---

## Every document answers, including the empty one

Nelson asks whether some documents have undefined origin and extent. The answer is no — and
the empty document is the case that tests it. `CREATENEWDOCUMENT` "creates an empty document"
(4/65); a freshly created or fully emptied document has `O(d) = ∅`.

We record **V11** (total answerability via a distinguished empty result): `RETRIEVEDOCVSPAN`
is defined for every allocated document. When `O(d) = ∅`, the result is the *empty span-set*
`⟨⟩` (V0). The empty
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

**Permanence of the underlying content.** We record **V14** (permanence): every *occupied*
position in `O(d)` — every position the span covers that actually carries content — maps,
through `M(d)`, to a permanent, immutable image, the store depending on the position's
subspace (S3★). A *content* position (`subspace(v) = s_C`) maps to an I-address in `dom(C)`,
permanent and immutable by content permanence (S0, P0); a *link* position
(`subspace(v) = s_L`) maps to a link address in `dom(L)`, permanent and immutable by link
permanence (L12). The split is forced: S0/P0 constrain the content store only, so they say
nothing about a link image, while L12 supplies exactly the matching guarantee on the link
store. The restriction to `O(d)` is essential: in the cross-subspace case
V6 establishes `O(d) ⊊ ⟦σ_d⟧` strictly, so the span also covers inter-subspace and unoccupied
positions (e.g. `[1,4]` in the worked example) on which `M(d)` is simply undefined; for those
covered-but-unoccupied positions there is no image through `M(d)`, and the permanence claim
makes no assertion about them. The arrangement (Vstream) is fluid; the content
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

Finally, the invariant that grounds the span the operation may return in the implementation.
V2 already established `σ_d`'s T12 legality — `Pos(extent_d)` and
`actionPoint(extent_d) ≤ #origin_d`, holding regardless of endpoint depths — so the abstract
non-degeneracy of the extent is settled. What remains is that the implementation actually
delivers this positive width: editing can drive *intermediate* arrangement entries negative,
and we must show those transients never surface in the reported extent. We record **V17**
(implementation non-negativity). Gregory confirms it is structurally guaranteed: even when
prior deletions drive intermediate arrangement-tree entries to negative displacements, the
root width is recomputed as a maximum-minus-minimum reach and remains non-negative — the
reported extent is never negative (consultation Q18). So there is no editing artifact that
drives the extent to zero or below. The only way to obtain "no extent" is the empty document,
which returns the distinguished empty span-set `⟨⟩` (V11) and carries no extent tumbler at
all — emptiness is reported by the absence of a span, not by a zero-width one.

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

**An endpoint-depth-divergent variant (one line).** When `m_C = 3 > m_L = 2`:
`M(d) = { [1,1,1] ↦ a, [1,1,2] ↦ b, [2,1] ↦ ℓ }` gives `origin_d = [1,1,1]`, `reach_d = [2,2]`,
`extent_d = [1,2,0]` of depth 3, and the actual reach `r⋆ = [2,2,0]` overshoots `reach_d` exactly
as V2's second covering case predicts (coverage and T12 legality survive; only the V3 same-depth
tightness lapses).

---

## Preconditions and well-definedness

For the report to be defined we require:

1. `d ∈ dom(M)` — the document is allocated (M0, M1). An unallocated identity names no
   arrangement and has nothing to report.

Authorization is a deployment-level access gate outside the value semantics this ASN
specifies.

Under precondition 1 the result is total: by S8-fin the occupied set is finite, so its
minimum and maximum (when non-empty) exist and the span is computed by V1–V2; when empty the
result is the distinguished empty span-set `⟨⟩` (V11), carrying no origin and no extent. No
further argument is needed — the operation consumes no caller-supplied position, so there is
no range to validate.

The precondition for *legality* is trivial, but a caller wanting to know *what kind* of answer
it will get — a faithful trace or a mere bounding box — is asking a non-trivial weakest-
precondition question, and we can answer it. Take the distinguished result
property `Exact ≡ "⟦σ_d⟧ contains no occupied-depth position outside O(d)"` (vacuously true on
the `⟨⟩` result, where there is no `σ_d`). Reasoning backward from `Exact`, we ask which states
`Σ` guarantee it. We claim

> `wp(RETRIEVEDOCVSPAN(d), Exact) = (O(d) occupies at most one subspace)`.

The derivation runs through V5 and V6. If `O(d)` is empty the result is `⟨⟩` and `Exact` holds
vacuously by definition; if `O(d)` lies in a single subspace `s`, V5 gives `Exact` directly: the
dense run `{[s,1,…,1,k]}` is covered with no
occupied-depth position left over (D-CTG★ closing the gaps). Conversely, if `O(d)` occupies
*both* subspaces, V6 gives `O(d) ⊊ ⟦σ_d⟧` strictly — the reach crosses the inter-subspace void,
admitting unoccupied positions inside the denotation — so `¬Exact`. The two directions exhaust
the cases by S3★-aux. So the single-subspace condition is both necessary and sufficient, hence
the *weakest* precondition. The companion reach property factors
the same way along the orthogonal endpoint axis: take `ReachTight ≡ "reach(σ_d) = reach_d"`
(vacuously true on the `⟨⟩` result). By the V2 reach
biconditional, `wp(RETRIEVEDOCVSPAN(d), ReachTight) = (O(d) = ∅ ∨ #origin_d ≤ #reach_d)`. A caller can thus decide *before* querying whether the answer will be exact
(check single-subspace occupancy) and whether its reach is the tight `reach_d` (check the
endpoint depths), without inspecting the returned span.

---

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| V0 | `RETRIEVEDOCVSPAN : dom(M) → Span + {⟨⟩}` (tagged union): one well-formed span `σ_d = (origin_d, extent_d)` for a non-empty document, or the distinguished empty span-set `⟨⟩` (denoting `∅`, not a T12 span) when `O(d) = ∅` — never a content sequence, never a count | introduced |
| V1 | When `O(d) ≠ ∅`, `origin_d = min O(d)` under T1 and `origin_d ∈ O(d)` (the origin is an occupied position) | introduced |
| V2 | `O(d) ⊆ ⟦σ_d⟧` (coverage), proved unconditionally via D0/D1 without assuming level-uniformity; the actual reach `r⋆ = origin_d ⊕ extent_d ≥ reach_d = shift(max O(d), 1) > max O(d)`, with equality `r⋆ = reach_d` iff `#origin_d ≤ #reach_d`; the span `(origin_d, extent_d)` is always a well-formed T12 span | introduced |
| V3 | `origin_d` is the greatest lower bound of `O(d)`; `reach_d` is the least strict upper bound of `max O(d)` *among tumblers at the depth of `max O(d)`* (`= #reach_d`; the deeper zero-extension `max O(d).0` is a smaller upper bound but lies at greater depth) — so `σ_d` is the tightest covering span whose reach is at the depth of `max O(d)` | introduced |
| V4 | `extent_d` is computed from `O(d) = dom(M(d))` alone; content in `dom(C)` but absent from the arrangement (deleted, or native elsewhere) contributes nothing (Vstream-bounded, not Istream) | introduced |
| V5 | When all occupied positions share one subspace, `⟦σ_d⟧` contains no occupied-depth position outside `O(d)` (exact cover of a contiguous run) | introduced |
| V6 | When occupied positions span more than one subspace, `O(d) ⊊ ⟦σ_d⟧` — the span bridges the inter-subspace void (bounding box, not exact cover); forced because a span denotes one convex region (ASN-0053 S0) and cannot trace a separated series | introduced |
| V8 | While the content subspace is non-empty, `origin_d = [s_C,1,…,1]`, invariant under all editing that leaves content present (origin permanence) | introduced |
| V9 | A pure rearrangement preserves `O(d) = dom(M(d))`; since `origin_d` and `extent_d` depend on `O(d)` alone (not on the values `M(d)(v)`), the reported span is identical before and after (extent tracks composition, not arrangement) | introduced |
| V11 | The operation is total over allocated documents; `O(d) = ∅` yields the distinguished empty span-set `⟨⟩` (V0), with `origin_d` undefined and no extent — the implementation's zeros are a sentinel, not a legal address (TA6) | introduced |
| V12 | The span discloses the live origin (addressing anchor) and current extent (present bounds) — neither derivable from `d`'s identity (information gain) | introduced |
| V13 | `σ_d` depends only on `O(d)`; two documents sharing content report independent spans; transcluded positions count toward the borrowing document's extent (independence) | introduced |
| V14 | Every *occupied* position in `O(d)` maps through `M(d)` to a permanent, immutable image, by subspace (S3★): content positions to `dom(C)` (S0, P0), link positions to `dom(L)` (L12); covered-but-unoccupied positions in the cross-subspace case (V6) carry no `M(d)` image; sharing preserves what the span denotes (permanence) | introduced |
| V15 | A returned span keeps its meaning under later edits to `d` or to home documents supplying its content; a fresh report is a new query, not a mutation (snapshot stability) | introduced |
| V16 | `σ_d` is a pure function of `O(d)`; equal arrangements return identical spans, independent of how the arrangement was built (determinism) | introduced |
| V17 | The reported extent is never negative in the implementation: prior deletions may drive intermediate arrangement-tree entries negative, but the root width is recomputed as a max-minus-min reach (Q18), so no editing artifact surfaces a zero-or-below extent (abstract positivity is V2's) | introduced |
| V18 | Origin permanence (V8) holds exactly while content is present; the origin moves only at the two transitions that toggle content occupancy — content-clearing migrates `origin_d` up to the link minimum `[s_L,1,…,1]`, first-content insertion into a link-only document migrates it down to the content anchor `[s_C,1,…,1]` (origin migration bounds V8) | introduced |

## Open Questions

In the *multi-subspace* case — where the inter-subspace void places unoccupied positions between the endpoints — what invariant, if any, can relate the reported extent to the count of occupied positions, given that the dense single-subspace coincidence (final component `= |O(d)|`, settled by V5) fails there and a span designates boundaries, not a cardinality?

Under what conditions must the reported origin be the document's permanent tumbler identity rather than the minimum occupied V-position, and when do these coincide?

What faithfulness must a report of a designated historical version preserve relative to a report of the present arrangement of the same document?

What invariant must relate the whole-document span to the bounding spans of the document's individual correspondence runs, so that the global extent composes from local ones?

What must the report guarantee about origin and extent when content occupies V-positions whose addressing arithmetic has been driven outside the well-formed range by prior editing?
