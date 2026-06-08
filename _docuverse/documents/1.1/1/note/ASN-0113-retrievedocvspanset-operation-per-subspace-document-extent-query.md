# ASN-0113: RETRIEVEDOCVSPANSET Operation — Per-Subspace Document Extent Query

*2026-06-04*

We are trying to understand a question that looks like the bounding query of its sibling
but is not: *given only your name, how much of each kind of thing do you hold?* A document
is handed over by identity alone — no range, no position, no selection — and is expected to
report back the extent of *each* of its content kinds separately: how much text, and how
many links. Where the whole-document query answers "from here, this far" with one span,
this query must answer with *several* spans, one per kind, and the difference between one
span and several is the whole subject of this note.

Nelson fixes the shape exactly. RETRIEVEDOCVSPANSET "returns a span-set indicating both
the number of characters of text and the number of links in document `<doc id>`" (4/68).
Two facts are packed into that sentence. First, the result is a *span-set* — a series of
spans (4/25) — not a single span. Second, the spans report *two distinct kinds*: text
characters and links, because "there is essentially nothing in the Xanadu system except
documents and their arbitrary links" (4/41), and these two kinds occupy *separate
subspaces* of the document's address tree. Our task is to say, formally, what each member
of that span-set denotes, what relationship each must bear to the subspace it measures,
what the caller learns from seeing the two together that neither alone could show, and what
invariants must hold *across* the members the operation returns.

We write the operation as a pure query, `RETRIEVEDOCVSPANSET(d)`, that observes the state
and returns a value, changing nothing. The entire content of this note is: *what is that
value, and what must hold of it?*

---

## The substrate we measure

We take the strand model of state as given. A document `d` — a T4-valid tumbler with
`zeros(d) = 2` (a document-level address) — carries an *arrangement* `M(d) : T ⇀ T`, a
partial function from V-positions in the document's current virtual stream to I-addresses,
the permanent keys of a content store `C : T ⇀ Val`, and a link store `L : T ⇀ Link`.

**The operation's precondition.** The entire apparatus below presupposes that `M(d)` is
*defined* — that `d` is an *allocated* document. We record this as the operation's
precondition (**W-pre**):

> `RETRIEVEDOCVSPANSET(d)` requires `d ∈ dom(M)` (equivalently, by M0/M1 of ASN-0093,
> `Document(d) ∧ d ∈ dom(M)`: a T4-valid document-level tumbler that some K.δ event has
> placed into `dom(M)`).

This is necessary because only `Document(e)` events extend `dom(M)` (ASN-0047, K.δ): for
`d ∉ dom(M)`, `M(d)` is undefined, so `O(d)`, `V_S(d)`, `occupied(d)`, and every derived
quantity below are *undefined* — not empty. The distinction is sharp and must not be
collapsed. An *allocated empty* document (`d ∈ dom(M)`, `M(d) = ∅`) legitimately yields the
empty span-set `⟨⟩` (a defined result; see W0). An *unallocated* identity (`d ∉ dom(M)`) is
*outside the operation's domain*: it has no defined result, and a faithful implementation
signals failure rather than fabricating `⟨⟩`. Gregory's back end confirms the separation
operationally — an existing-but-empty document returns the empty span-set with success,
whereas a never-allocated identity fails and the back end signals failure rather than an
empty result (consultation). All postconditions below are stated under W-pre; we make no
claim about unallocated `d`.

We write

> `O(d) = dom(M(d))`

for the set of *occupied V-positions* of `d` (well-defined under W-pre). Unlike the whole-document query, which bounds
`O(d)` as one undifferentiated set, this query must partition `O(d)` by *kind*. Each
V-position carries a subspace identifier in its first component, `subspace(v) = v₁`
(ASN-0036), and the docuverse fixes two of them: content positions carry `subspace = s_C`
and link positions carry `subspace = s_L`, with the convention `s_C = 1`, `s_L = 2`
(SubspaceConventionAxiom). For a subspace identifier `S` write

> `V_S(d) = {v ∈ O(d) : subspace(v) = S}`

for the *active V-positions of `d` in subspace `S`*. The two kinds Nelson names — text and
links — are exactly `V_{s_C}(d)` and `V_{s_L}(d)`.

We rely on these foundation facts about the shape of each `V_S(d)`:

- **S2** (functionality): each occupied V-position has a single I-address.
- **S3★** (referential integrity): a content position maps into `dom(C)`, a link position
  into `dom(L)` (ASN-0047).
- **S8-fin** (finiteness): `O(d)` is finite, hence each `V_S(d)` is finite.
- **S8a** (well-formedness): every `v ∈ O(d)` is zero-free, of depth `≥ 2`, all components
  positive.
- **S8-depth**: within one subspace, all active V-positions share a common depth `m_S ≥ 2`.
- **D-CTG★ / D-MIN★ / D-SEQ★** (per-subspace shape, ASN-0047): for each subspace `S`, when
  `V_S(d)` is non-empty it is contiguous, its minimum is the canonical `[S,1,…,1]` of depth
  `m_S`, and it forms the dense run

  > `V_S(d) = {[S,1,…,1,k] : 1 ≤ k ≤ n_S}` for some `n_S ≥ 1`.

- **CL-OWN / CL-UNIQ** (ASN-0047): a document's link-subspace arrangement holds only its
  own links, each at exactly one V-position.
- **L12 / P0** (link and content permanence): allocated keys persist and their values never
  change.

We borrow the span machinery wholesale. A span `σ = (s, ℓ)` denotes the half-open interval
`⟦σ⟧ = {t ∈ T : s ≤ t < s ⊕ ℓ}` (T12), with `reach(σ) = s ⊕ ℓ` (ASN-0053). A span is
*well-formed* when `Pos(ℓ)` and `actionPoint(ℓ) ≤ #s`; it is *level-uniform* when
`#s = #ℓ`. The ordinal displacement `δ(n, m) = [0,…,0,n]` of length `m` (ASN-0034) is the
canonical pure depth-`m` shift, and `shift(t, n) = t ⊕ δ(n, #t)` advances `t`'s last
component by `n`. A *span-set* is a finite sequence of spans denoting the union of its
members; it is *normalized* when sorted and separated (ASN-0053). We measure the document
as a span-set, one member per kind; content delivery, region reads, the single overall
bound (RETRIEVEDOCVSPAN), and the counting and discovery of individual links are out of
scope.

---

## What the caller must be handed

Before specifying the operation we fix the *type* of its result. Nelson fixes it: a
*span-set* — "a series of spans" (4/25) — whose two members indicate "the number of
characters of text and the number of links" (4/68). This is not a content read (that would
return records, not spans) and not a pair of bare integers. A tumbler-span "does not
designate the number of bytes contained. It does not designate a number of anything"
(4/24); it designates a *region*, "from here to there," with everything between implicit
(4/25). Yet Nelson says the span-set *indicates* the two numbers. The reconciliation is
structural: each member span's *extent* encodes the count of its subspace, because the
positions in a subspace form a dense run (D-SEQ★) whose cardinality is exactly the width of
the covering span. The number is read off the boundary, not stored as a tally.

We therefore take the result to be a *normalized span-set* `Σ_d` of at most two members —
one per occupied subspace — and the *empty span-set* `⟨⟩` when the document holds nothing in
either counted subspace. We record this as **W0** (span-set-valued result): for an
*allocated* document `d` (W-pre), `RETRIEVEDOCVSPANSET(d)` returns a normalized span-set,
never a content sequence and never a cardinality; for an allocated document that is *empty in
both counted subspaces* (`d ∈ dom(M)` with `V_{s_C}(d) = V_{s_L}(d) = ∅`) it returns `⟨⟩`,
the distinguished value denoting `∅` (which is not a T12 span, since every well-formed span
is non-empty — S2, ASN-0053). This `⟨⟩` is the report of an *allocated but empty* document; it
is *not* the behavior on an unallocated identity, which W-pre places outside the operation's
domain (and which the implementation answers with the failure marker, not `⟨⟩`). The caller reads each member to learn the extent of one kind of
content; the content itself, and the identity of individual links, are the business of other
operations.

---

## The extent of a single subspace

We reason first about *one* kind in isolation: what span describes the extent of subspace
`S` in document `d`? We are looking for a region that contains exactly the active positions
`V_S(d)` and nothing else — Nelson's requirement that one designate "a separated series of
items exactly, including nothing else" (4/25).

When `V_S(d) ≠ ∅`, D-SEQ★ hands us its shape directly: a dense run
`{[S,1,…,1,k] : 1 ≤ k ≤ n_S}` of depth `m_S`, with minimum `[S,1,…,1]` (D-MIN★) and
cardinality `n_S = |V_S(d)|`. Because the run is dense and contiguous, a *single* span
covers it exactly. Define the **extent span** of subspace `S`:

> `ext(d, S) = (start_S, δ(n_S, m_S))`,  where `start_S = [S,1,…,1]` of depth `m_S`.

We record `n_S = |V_S(d)|` as the **subspace extent** (W1) and `ext(d, S)` as its **span
encoding** (W2). We must show this span is legal and that it covers exactly the run.

**The extent span is well-formed.** We record **W3**: `ext(d, S)` satisfies T12. By
OrdinalDisplacement (ASN-0034), with `n_S ≥ 1` (the run is non-empty) and `m_S ≥ 1`, the
width `δ(n_S, m_S)` is a positive tumbler with `actionPoint(δ(n_S, m_S)) = m_S`; since
`#start_S = m_S`, the action point satisfies `actionPoint(δ(n_S, m_S)) = m_S ≤ #start_S`.
T12's two preconditions hold, so the span is well-formed; moreover it is level-uniform,
`#δ(n_S, m_S) = m_S = #start_S`. Its reach is, by OrdinalShift (ASN-0034),

> `reach(ext(d, S)) = start_S ⊕ δ(n_S, m_S) = shift(start_S, n_S) = [S,1,…,1,1+n_S]`,

one ordinal step past the last active position `[S,1,…,1,n_S]`, realizing the half-open
convention under which the last occupied position is included and the next is excluded.

**The extent span covers its subspace exactly.** This is the heart of the matter — Nelson's
"complete and exclusive" requirement (4/25), the two halves being completeness (account for
every position present) and exclusivity (admit nothing foreign). To state exclusivity we
must say *foreign to what*: a span's denotation `⟦ext(d, S)⟧` necessarily contains tumblers
deeper than the V-positions (whole subtrees hang below each address), so we restrict
attention to the addressable V-positions of the subspace at its working depth. Define the
*V-slice*

> `VSlice(S, m) = {t ∈ T : t₁ = S ∧ #t = m ∧ zeros(t) = 0}`

— the depth-`m`, zero-free tumblers of subspace `S`, the population from which active
V-positions are drawn (S8a). We record **W4** (ExactCoverage):

> `⟦ext(d, S)⟧ ∩ VSlice(S, m_S) = V_S(d)`.

The derivation is direct. `⟦ext(d, S)⟧ = {t : start_S ≤ t < [S,1,…,1,1+n_S]}`. Take any
`t ∈ VSlice(S, m_S)`. Such a `t` has the form `[S, t_2, …, t_{m_S}]` with all components
positive. The bounds `start_S = [S,1,…,1]` and `reach = [S,1,…,1,1+n_S]` share the common
prefix `[S,1,…,1]` of length `m_S − 1`, so by T5 (ContiguousSubtrees), applied with
`start_S ≤ t < reach`, every interior `t` extends that prefix — its first `m_S − 1`
components are pinned to `[S,1,…,1]`. (The lower bound `start_S ≤ t` alone does *not* force
this: lexicographic order is not componentwise order, e.g. `[S,2,1] ≥ [S,1,1]` despite its
off-prefix second component; the confinement is the joint effect of both bounds via T5.) The
only remaining freedom is in the last component, which the half-open bounds then pin to
`1 ≤ t_{m_S} ≤ n_S`. These are exactly the elements
`[S,1,…,1,k]` with `1 ≤ k ≤ n_S` — which is `V_S(d)` by D-SEQ★. So the span omits no active
position (completeness) and includes no inactive V-slice tumbler (exclusivity). The relation
the member span bears to its subspace is therefore *definitional, not approximate*: its
boundaries select a region whose V-slice population coincides with the subspace's active
positions.

**The count is read off the boundary.** Because the run is dense, `n_S` is recoverable from
the span alone: it is the last component of the width `δ(n_S, m_S)`, equivalently the gap
between the last component of `reach` and that of `start_S`. This is how a span-set
"indicates the number" (4/68) without designating a number directly (4/24): the magnitude is
implicit in the boundary, and made explicit only because the subspace is contiguous.

**Exactness is contingent on contiguity.** The single covering span is exact *only because*
`V_S(d)` is a contiguous run (D-CTG★). We state the dependence as a biconditional and prove
both halves. We record **W5** (ExactnessRequiresContiguity), *under the hypothesis*
`V_S(d) ≠ ∅`: *there exists* a single
level-uniform span `σ` of subspace `S` at depth `m` satisfying
`⟦σ⟧ ∩ VSlice(S, m) = V_S(d)` *if and only if* `V_S(d)` is contiguous in `VSlice(S, m)` —
i.e. `V_S(d)` contains every V-slice tumbler lying (under T1) between its own minimum and
maximum. The existential is essential: the forward direction asserts that contiguity
*permits* an exact span (a poorly chosen `σ` may overshoot even when `V_S(d)` is
contiguous), while the converse asserts that non-contiguity *defeats every* `σ`.

The non-emptiness hypothesis excludes empty `V_S(d)`, which W5 does not cover and W0 handles
separately — an allocated document empty in a counted subspace contributes *no member* for
that subspace (and `⟨⟩` overall when both are empty).

The *forward* direction (contiguous ⟹ a single exact span exists) holds for *any* contiguous
`V_S(d)`, not only the canonical run D-CTG★/D-MIN★ produce — and so it cannot simply cite W4,
whose covering span `ext(d, S)` is anchored at `[S,1,…,1]` and is exact only when D-MIN★ pins
the run's minimum there. (For a contiguous run not anchored at the canonical minimum — say
`V_S(d) = {[S,5,3],[S,5,4]}` at depth `m = 3` — `ext(d, S) = ([S,1,1], δ(2,3))` reaches only
`[S,1,3]` and covers `{[S,1,1],[S,1,2]} ≠ V_S(d)`; the exact span is anchored at the *actual*
minimum `[S,5,3]`.) We therefore build the covering span from the run's own minimum. Let
`V_S(d)` be contiguous and non-empty, and put `a = min(V_S(d))`, `b = max(V_S(d))` under T1
(both well-defined: `V_S(d)` is finite by S8-fin and totally ordered by T1). Every element
lies in `VSlice(S, m)`, so all share depth `m`, first component `S`, and are zero-free; write
`a = [S, a_2, …, a_m]`. We claim the whole run shares the prefix `[S, a_2, …, a_{m−1}]` and
varies only in the last component. Suppose two elements diverged at some interior position
`i < m`. Then between them under T1 lie *all* V-slice tumblers obtained by raising the last
component without bound — infinitely many, since component values are unbounded (T0(a)) —
each of which contiguity would force into `V_S(d)`, contradicting finiteness (S8-fin). So the
run is confined to one prefix and its last components form a contiguous block of naturals;
with `n_S = |V_S(d)|`, that block is `a_m, a_m+1, …, a_m + n_S − 1`, and
`b = [S, a_2, …, a_{m−1}, a_m + n_S − 1]`. Now define `σ = (a, δ(n_S, m))` — level-uniform and
T12-well-formed (by OrdinalDisplacement, ASN-0034: `δ(n_S, m)` positive with action point
`m = #a`), with `reach(σ) = shift(a, n_S) = [S, a_2, …, a_{m−1}, a_m + n_S]` (OrdinalShift,
ASN-0034). By T5 on the prefix
`[S, a_2, …, a_{m−1}]` (length `m − 1`) shared by `a` and `reach(σ)`, every interior tumbler
extends that prefix, and the half-open bounds pin its last component to
`a_m ≤ t_m ≤ a_m + n_S − 1` — exactly the run. Hence `⟦σ⟧ ∩ VSlice(S, m) = V_S(d)`, an exact
single span. This `σ` coincides with `ext(d, S)` precisely when `a = [S,1,…,1]`, i.e. under
D-MIN★; in the docuverse that always holds and the W4 span serves directly, but the existence
claim itself needs only the run's own minimum, not the canonical anchor.

The *converse* (non-contiguous ⟹ no single span is exact) we establish by the structure of
the argument, then exhibit concretely. Suppose `V_S(d)` is *not* contiguous: there exist
`p, q ∈ V_S(d)` and `r ∈ VSlice(S, m)` with `p < r < q` and `r ∉ V_S(d)`. Let `σ` be any
level-uniform span with `⟦σ⟧ ∩ VSlice(S, m) ⊇ V_S(d)`. Then `p, q ∈ ⟦σ⟧`, and since a span's
denotation is order-convex (T12; S0 of ASN-0053), `p < r < q` forces `r ∈ ⟦σ⟧`. As
`r ∈ VSlice(S, m)`, we get `r ∈ ⟦σ⟧ ∩ VSlice(S, m)` while `r ∉ V_S(d)`, so the intersection
strictly exceeds `V_S(d)` — `σ` overshoots and cannot be exact. No single span escapes this:
any span covering both extremes drags in the gap point. Faithful reporting then requires a
*span-set* within the single subspace, one member per contiguous cluster.

Concretely, take `S` at depth `m = 2` with `V_S(d) = {[S,1], [S,3]}` and `[S,2]` inactive
(`[S,2] ∈ VSlice(S, 2)` but `[S,2] ∉ V_S(d)`). The unique minimum-to-maximum level-uniform
span is `σ* = ([S,1], δ(3,2))` with `reach(σ*) = [S,4]`, the smallest span containing both
`[S,1]` and `[S,3]`. Its V-slice intersection is `⟦σ*⟧ ∩ VSlice(S, 2) = {[S,1], [S,2], [S,3]}`,
which strictly contains `V_S(d)` precisely because `[S,2]` is admitted. So
`⟦σ*⟧ ∩ VSlice(S, 2) ⊋ V_S(d)`: even the tightest single span is inexact, confirming the
converse.

The docuverse maintains contiguity as an invariant (D-CTG★), so under well-formed editing the
one-span-per-subspace report is exact — but the dependence is real, and Gregory's
implementation exhibits exactly the bounding-box behavior when fed non-contiguous content
(consultation Q11, Q13): the reported span runs minimum-to-maximum and silently absorbs
interior gaps.

---

## The operation: one span per occupied subspace

We now assemble the members. Let

> `occupied(d) = {S ∈ {s_C, s_L} : V_S(d) ≠ ∅}`

be the *occupied subspaces* (W6). The operation returns the extent span of each, sorted:

> `RETRIEVEDOCVSPANSET(d) = ⟨ ext(d, S) : S ∈ occupied(d), in increasing S ⟩`,

the empty span-set `⟨⟩` when `occupied(d) = ∅`. We record this as **W7**
(OneSpanPerOccupiedSubspace): the result has exactly `|occupied(d)|` members — one per
occupied subspace, *never one per contiguous fragment and never one per individual item*.
The report is at the granularity of *kind*, not of position: a document with a thousand
characters and three links yields two members, not a thousand-and-three. This matches both
Nelson's "span-set indicating both the number of characters and the number of links" (4/68)
and Gregory's implementation, which emits at most one VSpec per subspace regardless of how
many crums populate it (consultation Q11, Q14, Q19).

**The result is a read-only observation.** We record **W8** (PureQuery): `Σ' = Σ`. The
operation reads `C`, `L`, `M`, and the document identity, and writes nothing — no
allocation, no arrangement change, no provenance. It is a function of the present state
alone.

**Only the two counted subspaces appear.** A link is internally a three-ended structure,
and its endpoint sub-addresses inhabit a *third* region of the address tree (a type/endpoint
subspace, `s = 3`). That region is not a kind of *document content* — it is internal to a
link's own storage — and so it is never a V-position of `d`. Every occupied position of `d`
lies in one of the two counted subspaces, leaving none in a third. This is precisely
S3★-aux (SubspaceExhaustiveness, ASN-0047): `(A d, v : v ∈ dom(M(d)) : subspace(v) = s_C ∨
subspace(v) = s_L)`. We record **W9** (TwoKindsOnly):

> `O(d) = V_{s_C}(d) ⊔ V_{s_L}(d)`.

The derivation: by S8a every `v ∈ O(d)` has a well-formed first component, and S3★-aux
restricts that component to `{s_C, s_L}`, so `O(d) = {v ∈ O(d) : v₁ = s_C} ∪ {v ∈ O(d) : v₁ =
s_L} = V_{s_C}(d) ∪ V_{s_L}(d)`. The union is disjoint because `s_C ≠ s_L` (SC-NEQ), so no
`v` can satisfy both predicates. There is therefore *no third subspace* in which document
content could reside, hence no third member can ever arise in the span-set — the report is
intrinsically two-kinded, grounded in the foundation rather than in implementation behavior.

**The result-cardinality, characterized as a weakest precondition.** The operation writes
nothing (W8), so the only non-trivial postcondition a caller can assert about it concerns the
*value* it returns — and the value's shape is genuinely state-dependent: the result has zero,
one, or two members according to which subspaces are occupied. We make this dependence exact.
Since `RETRIEVEDOCVSPANSET` is a pure query whose result is `⟨ ext(d, S) : S ∈ occupied(d) ⟩`
(W7), its cardinality is `|occupied(d)|`, and `occupied(d)` is fixed by which of `V_{s_C}(d)`,
`V_{s_L}(d)` is non-empty (W6). Computing the weakest precondition for each result-shape
postcondition — and conjoining W-pre, since outside `dom(M)` the result is undefined rather
than `⟨⟩` — we record **W20** (ResultCardinalityWP). The empty result:

> `wp(RETRIEVEDOCVSPANSET(d), "result = ⟨⟩") ≡ d ∈ dom(M) ∧ V_{s_C}(d) = ∅ ∧ V_{s_L}(d) = ∅`.

The two-member result:

> `wp(RETRIEVEDOCVSPANSET(d), "|result| = 2") ≡ d ∈ dom(M) ∧ V_{s_C}(d) ≠ ∅ ∧ V_{s_L}(d) ≠ ∅`.

And the one-member result, characterized as an exclusive-or:

> `wp(RETRIEVEDOCVSPANSET(d), "|result| = 1") ≡ d ∈ dom(M) ∧ (V_{s_C}(d) = ∅ ⊻ V_{s_L}(d) = ∅)`.

Each equivalence is forced. The right-to-left direction reads off W6/W7: the named occupancy
pattern fixes `occupied(d)` and hence `|occupied(d)| = |result|`; for the empty case,
`occupied(d) = ∅` gives `result = ⟨⟩` directly. The left-to-right direction is the
*weakest*-precondition obligation — no strictly weaker state predicate implies the
postcondition, because `occupied(d)` is *determined* by the two emptiness bits (W6) and the
result is a total function of `occupied(d)` (W7), so any state satisfying the postcondition
*must* exhibit the named occupancy pattern. The three preconditions partition the allocated
states (`d ∈ dom(M)`) by the pair of emptiness bits — `(∅, ∅)`, exactly one empty, neither
empty — exhausting the result's three possible cardinalities. This is the informative wp for a
pure query: the postcondition lives on the returned value, and its weakest precondition is the
exact state-characterization of when that value arises.

---

## Why text and links must be reported apart

We can now answer *why* the operation returns a span-set rather than folding both kinds into
one extent — Nelson's design choice, which our formalism makes forced rather than arbitrary.

The two subspaces are not merely labelled differently; they are *disjoint subtrees of the
address space*, and no single contiguous span can cover both. Consider the denotation of
each extent span. We record **W10** (SubspaceConfinement): `(A t : t ∈ ⟦ext(d, S)⟧ : t₁ =
S)`, for `t` of any depth. The argument is two lines on the first
component. The bounds are `start_S = [S,1,…,1]` and `reach = [S,1,…,1,1+n_S]`, both with
first component `S`. Take any `t ∈ ⟦ext(d, S)⟧`, so `start_S ≤ t < reach`. If `t₁ < S`, then
by T1 the first divergence is at position `1` and `t < start_S` — contradicting `start_S ≤
t`. If `t₁ > S`, then by T1 `t > reach` — contradicting `t < reach`. Hence `t₁ = S`, for
`t` of any depth. It follows immediately that the two member spans are disjoint — **W11**
(Disjointness):

> `⟦ext(d, s_C)⟧ ∩ ⟦ext(d, s_L)⟧ = ∅`.

For any `t` in the intersection we would need `t₁ = s_C` and `t₁ = s_L` at once (W10),
impossible since `s_C ≠ s_L` (SC-NEQ, the `1 ≠ 2` of the convention). The SC-NEQ contradiction
on the first component, under T1, suffices on its own. The text region and the link region therefore *cannot* be the
denotation of a single span: a span is a contiguous interval (T12), and `⟦ext(d, s_C)⟧` and
`⟦ext(d, s_L)⟧` are separated by every address between them — in particular the whole gap
from `[s_C,1,…,1,1+n_{s_C}]` up to `[s_L,1,…,1]`. To "designate the separated series exactly,
including nothing else" (4/25), one is *forced* into a span-set of two members. This is not a
representational convenience but a structural necessity: the honest report of two
separated regions is two spans.

---

## What the pair reveals that neither member alone could

The whole point of returning *both* extents — Nelson's "both the number of characters of
text and the number of links" (4/68) — is that the pair carries information no single
extent holds. We make this precise.

A single extent gives a *size*; the pair gives a *proportion*. Ask for the text extent
alone and you learn how much matter the document carries, but nothing about how connected it
is; ask for the link extent alone and you learn how many connections it anchors, but nothing
about how much content those connections hang on. The pair `(n_{s_C}, n_{s_L})` is the
document's *profile* — its ratio of original matter to connective structure — and this is
the one thing neither coordinate determines. We record **W12** (ProfileIrreducibility): the
map `d ↦ (n_{s_C}(d), n_{s_L}(d))` is determined by neither coordinate alone. Formally,
neither projection is injective on the profile: for any value of one coordinate there exist
states realizing distinct values of the other —

> `(A c, k₁, k₂ ∈ ℕ : k₁ ≠ k₂ : (E d₁, d₂ : n_{s_C}(d₁) = n_{s_C}(d₂) = c : n_{s_L}(d₁) = k₁ ∧ n_{s_L}(d₂) = k₂))`

and symmetrically with the roles of the subspaces exchanged.

The existential is a reachability claim: for arbitrary `(c, k) ∈ ℕ × ℕ` a document realizing
profile `(c, k)` must be constructible by a sequence of *valid composites* (ASN-0047,
ValidComposite★), each satisfying the full coupling discipline J0 ∧ J1★ ∧ J1'★ between its
initial and final state — not J0 alone. We discharge the claim by exhibiting such a sequence
over the ASN-0047 vocabulary that drives `(n_{s_C}, n_{s_L})` to any target. Starting from a
state in which `d ∈ E_doc` (allocated by K.δ, NodeBaptism then the document sub-allocator),
the two subspaces are populated by *disjoint* coupled transition kinds. A text position
cannot be added by K.μ⁺ alone: K.μ⁺ requires that each new mapping `M'(d)(v) = a` reference
an already-allocated `a ∈ dom(C)`, and a valid composite must satisfy J0 (every freshly
allocated I-address appears in some arrangement) *and* J1★ (every I-address newly entering the
content-subspace range of `M'(d)` is recorded in provenance, `(a, d) ∈ R'`) *and* J1'★ (every
new provenance entry corresponds to such a range-new I-address). So each text position is a
*coupled K.α + K.μ⁺ + K.ρ composite* — a K.α step allocating a fresh content address
`a ∈ dom(C)` (its existence guaranteed by T0(a)/T0(b), content being unboundedly
allocatable), a content-restricted K.μ⁺ step mapping a new text V-position to that `a`
(discharging J0), and a K.ρ step recording `(a, d) ∈ R'` (discharging J1★ and J1'★) — leaving
the composite valid. Performing `c` such
composites adds the dense run `{[s_C,1,…,1,j] : 1 ≤ j ≤ c}` by D-SEQ★ and drives
`n_{s_C}(d) = c`; each link position is a *coupled K.λ + K.μ⁺_L composite* — a K.λ step
allocating a fresh link address `ℓ` on the document's link sub-allocator `A_L(d)` (so that
`ℓ ∈ dom(L)` with `origin(ℓ) = d`, discharging K.μ⁺_L's elementary precondition
`ℓ ∈ dom(L) ∧ origin(ℓ) = d ∧ ℓ ∉ ran(M(d))`, ASN-0047), followed by a K.μ⁺_L step mapping a
fresh link V-position to that `ℓ` (the coupling obligations J0/J1★/J1'★ are vacuous across
this composite — no content is allocated and no content-subspace range is extended, and
J1★/J1'★ are scoped to the content subspace). Performing `k` such composites adds
`{[s_L,1,…,1,j] : 1 ≤ j ≤ k}` by D-SEQ★ and drives `n_{s_L}(d) = k`. The content-restricted
K.μ⁺ confines its new V-positions to `subspace(v) = s_C` and K.μ⁺_L to `subspace(v) = s_L`,
so the two counts are set by independent transition streams (this is the mechanism behind
W15, Independence, below); neither stream constrains the other, so every `(c, k) ∈ ℕ × ℕ` is
reachable (the empty subspace, count `0`, by performing zero extensions of that kind). To witness W12, fix `c, k₁, k₂ ∈ ℕ` with `k₁ ≠ k₂`: build `d₁` with profile
`(c, k₁)` and `d₂` with profile `(c, k₂)` by the construction above; both share text extent
`c` yet differ in link extent, so `n_{s_C}` does not determine `n_{s_L}`. The symmetric
proposition — fix the link extent at `k` and vary the text extent — is witnessed by the
*same two recipes* with only the varying axis changed: coupled `K.α + K.μ⁺ + K.ρ` content
composites drive `n_{s_C}` to the two distinct targets `c₁ ≠ c₂` while uncoupled
`K.λ + K.μ⁺_L` link composites hold `n_{s_L} = k`.

This is why the profile distinguishes documents that
one axis cannot tell apart: high text with near-zero links is original prose; near-zero text
with high link count is a purely connective document — a link-set, an annotation layer; both
substantial is a compound collage. The span-set is the report that returns *both* halves of
what a document is — its content and its connections — in one observation.

---

## Invariants across the members

We collect the constraints that must hold *among* the spans the operation returns — the
properties an alternative implementation must also satisfy for its report to be coherent.

**Uniform shape.** The result always describes the same kinds in the same order. The
candidate subspaces are the fixed pair `{s_C, s_L}` and the members are sorted by `S`, so
when both are occupied the text member precedes the link member, always. We record **W13**
(UniformShape): the result is a normalized span-set whose members occupy positions drawn
from the fixed, ordered kind-list `(s_C, s_L)`. The shape of the report is invariant across
the docuverse; only the magnitudes `n_S` differ. (That the result is already *normalized* —
sorted and separated, ASN-0053 — follows from W11: the two members are disjoint and ordered
`s_C < s_L`, with `reach(ext(d, s_C)) < start_{s_L}` by T1, so no merging is possible and the
sequence is in normal form.)

This uniformity is exactly what makes two documents' reports *comparable*: one compares like
with like, text-extent to text-extent and link-extent to link-extent. We record **W14**
(Comparability): for any two allocated documents `d₁, d₂`, the per-kind comparison `n_S(d₁)`
versus `n_S(d₂)` is well-defined for each `S ∈ {s_C, s_L}`. The comparison is total because
`n_S(d) = |V_S(d)|` counts `V_S(d)` directly (W1): it is a total function, defined for every
allocated `d` and every `S ∈ {s_C, s_L}` independently of whether the operation emits a member
for that subspace. An empty subspace has `n_S(d) = 0` as a fact about `V_S(d) = ∅`, regardless
of the report's membership. This well-definedness of `n_S` is a property of the state, separate
from how a *consumer* recovers `n_S = 0` from a span-set whose empty member is absent — that
absent-equals-zero reading is a consumer-side convention this note does not rely on and flags
as not obviously safe (see Open Questions).

**Cross-kind independence.** The extent reported for one kind does not depend on the
population of the other. We record **W15** (Independence): `n_{s_C}(d)` is a function of
`V_{s_C}(d)` alone, and `n_{s_L}(d)` of `V_{s_L}(d)` alone; consequently an edit confined to
one subspace leaves the other subspace's reported extent unchanged. This follows because each
count is read off a *disjoint* position set: `V_S(d) = {v ∈ O(d) : v₁ = S}` is selected by
the predicate `v₁ = S`, and `s_C ≠ s_L` (SC-NEQ) makes `V_{s_C}(d)` and `V_{s_L}(d)` disjoint,
so `n_{s_C} = |V_{s_C}(d)|` and `n_{s_L} = |V_{s_L}(d)|` are computed from non-overlapping data
(W1). The independence is therefore a property of the *counts*, not a property of the
transitions being single-subspace. The extension transitions happen to be single-subspace —
the amended K.μ⁺ confines its new V-positions to `subspace(v) = s_C` (content-subspace
restriction) and K.μ⁺_L confines its new V-positions to `subspace(v) = s_L` (link-subspace
restriction) — but contraction is not. ASN-0047's K.μ⁻ selects a per-subspace retention count
`n'_S` for *each* `S ∈ {s_C, s_L}` and contracts to `∪_S {[S,1,…,1,k] : 1 ≤ k ≤ n'_S}`,
subject only to at least one `S` strictly contracting; a single K.μ⁻ may therefore shrink the
text run and the link run *simultaneously*, so it is false that every V-position transition
acts within one subspace. Independence survives this anyway: even the both-contracting K.μ⁻
sets the new `n_{s_C}` by reading the retained text positions and the new `n_{s_L}` by reading
the retained link positions, each settable without reference to the other, because the two
counts are read off the disjoint sets `V_{s_C}(d)` and `V_{s_L}(d)`. As a *conditional*, then:
an edit confined to one subspace leaves the other's count untouched — a content edit cannot
alter `V_{s_L}(d)` and a link edit cannot alter `V_{s_C}(d)` — and even a joint contraction
changes each count only through its own subspace's positions, with neither change forcing the
other. The link count can grow without altering the character count, and text can be inserted
or deleted without altering the link count — the two members move independently.

**Partition of the counted content.** The members do not merely fail to overlap; together
they account for exactly the counted V-positions. We record **W16** (Partition):

> `(⊔ S : S ∈ occupied(d) : ⟦ext(d, S)⟧ ∩ VSlice(S, m_S)) = {v ∈ O(d) : v₁ ∈ {s_C, s_L}}`,

a *disjoint* union (W11 gives disjointness; W4 gives that each part is exactly `V_S(d)`; and
`O(d)` restricted to the counted subspaces is `V_{s_C}(d) ⊔ V_{s_L}(d)` by definition). No
counted position is orphaned — left outside every member — and no member claims a position
that is not active. A violation of W16 would be a corruption of the index: orphaned content
(a position active but covered by no member) or phantom extent (a member covering a position
that carries nothing). The agreement of the members with the active set is the observable
signature that the arrangement is intact.

**The extent-content relationship.** Finally, the relationship each member bears to what a
reader would *find* on retrieving that subspace. The member is a boundary designation; the
content it measures is exactly the population of the designated region. We record **W17**
(ExtentDeterminesPopulation): for each occupied `S`, the active positions of `S` are exactly
those V-slice tumblers lying within `ext(d, S)` (this is W4 restated as a fidelity claim),
and each such position carries content — `M(d)(v) ∈ dom(C)` for `S = s_C`, `M(d)(v) ∈ dom(L)`
for `S = s_L` (S3★). The reader who later asks for the region the member bounds finds
neither more nor fewer items than the extent claims. What must never happen is a mismatch
where the extent designates a region but the region's population differs from it.

---

## A worked instance

We instantiate the operation on a concrete document to check the key postconditions against
specific tumblers. Let `d` hold five characters of text and two home links, both subspaces at
the minimal working depth `m_{s_C} = m_{s_L} = 2` — the degenerate case in which the canonical
`[S,1,…,1]` form collapses to `[S,1]`, because the inner `1,…,1` segment has length
`m_S − 2 = 0`. By D-SEQ★ the active positions are

> `V_{s_C}(d) = {[1,1], [1,2], [1,3], [1,4], [1,5]}`,  `n_{s_C} = 5`,
> `V_{s_L}(d) = {[2,1], [2,2]}`,  `n_{s_L} = 2`

(recall `s_C = 1`, `s_L = 2`). The extent spans (W2) are

> `ext(d, s_C) = ([1,1], δ(5,2)) = ([1,1], [0,5])`,
> `ext(d, s_L) = ([2,1], δ(2,2)) = ([2,1], [0,2])`,

so the operation returns the normalized span-set

> `RETRIEVEDOCVSPANSET(d) = ⟨ ([1,1], δ(5,2)), ([2,1], δ(2,2)) ⟩`.

**W3 (well-formed).** For `ext(d, s_C)`: the width `δ(5,2) = [0,5]` is positive (`Pos`), its
action point is its last position `2`, and `#start = #[1,1] = 2`, so `actionPoint ≤ #start`;
level-uniform since `#[0,5] = 2 = #[1,1]`. Its reach is `[1,1] ⊕ [0,5] = shift([1,1], 5) =
[1,6] = [s_C,1+n_{s_C}]` (empty interior segment at `m_S = 2`). Identically `ext(d, s_L)` has
reach `[2,3] = [s_L,1+n_{s_L}]`. Both satisfy T12.

**W4 (exact coverage).** `⟦ext(d, s_C)⟧ = {t : [1,1] ≤ t < [1,6]}`. Intersecting with
`VSlice(s_C, 2) = {[1,j] : j ≥ 1}` pins the depth-2, prefix-`[1,·]` tumblers with last
component in `1..5`, i.e. `{[1,1],…,[1,5]} = V_{s_C}(d)`. Likewise `⟦ext(d, s_L)⟧ ∩
VSlice(s_L, 2) = {[2,1],[2,2]} = V_{s_L}(d)`. Neither span omits an active position nor admits
an inactive V-slice tumbler.

**W11 (disjointness).** Every `t ∈ ⟦ext(d, s_C)⟧` has `t₁ = 1`; every `t ∈ ⟦ext(d, s_L)⟧` has
`t₁ = 2` (W10). Since `1 ≠ 2`, `⟦ext(d, s_C)⟧ ∩ ⟦ext(d, s_L)⟧ = ∅`.

**W13 (uniform shape).** The members are listed in increasing `S`, text (`s_C = 1`) before
link (`s_L = 2`). They are separated: `reach(ext(d, s_C)) = [1,6] < [2,1] = start_{s_L}` by
T1 (first component `1 < 2`), so no merge is possible and the sequence is already normalized.

**W16 (partition).** The disjoint union of the two V-slice intersections is `{[1,1],…,[1,5]} ⊔
{[2,1],[2,2]}`, which is exactly `{v ∈ O(d) : v₁ ∈ {s_C, s_L}} = V_{s_C}(d) ⊔ V_{s_L}(d) =
O(d)` (the last equality by W9). No counted position is orphaned and no member claims an
inactive position.

The degenerate `m_S = 2` instance shows the canonical machinery surviving the collapse: with
no interior `1`'s, `start_S = [S,1]` and the count `n_S` lives entirely in the last component
of the width.

**A one-member instance.** The single-occupied-subspace boundary — the default state of a
freshly populated document with text but no links yet — sits between `⟨⟩` (W0) and the
two-member report. Let `d'` hold three characters of text and *no* links, depth
`m_{s_C} = 2`. By D-SEQ★,

> `V_{s_C}(d') = {[1,1], [1,2], [1,3]}`,  `n_{s_C} = 3`,
> `V_{s_L}(d') = ∅`,  `n_{s_L} = 0`.

The link subspace is empty, so `occupied(d') = {s_C}` (W6) and `|occupied(d')| = 1` (W7): the
operation emits exactly one member and *no* link member. The single extent span (W2) is
`ext(d', s_C) = ([1,1], δ(3,2)) = ([1,1], [0,3])`, so

> `RETRIEVEDOCVSPANSET(d') = ⟨ ([1,1], δ(3,2)) ⟩`.

**W3 (well-formed).** `δ(3,2) = [0,3]` is positive (`Pos`), its action point is its last
position `2 = #[1,1]`, and it is level-uniform (`#[0,3] = 2 = #[1,1]`); its reach is
`[1,1] ⊕ [0,3] = [1,4] = [s_C,1+n_{s_C}]` (empty interior segment at `m_S = 2`). T12 holds.

**W4 (exact coverage).** `⟦ext(d', s_C)⟧ = {t : [1,1] ≤ t < [1,4]}`; intersecting with
`VSlice(s_C, 2) = {[1,j] : j ≥ 1}` pins the last component to `1..3`, giving
`{[1,1],[1,2],[1,3]} = V_{s_C}(d')` — neither omitting an active position nor admitting an
inactive one.

**W7 / W13 (single-member normal form).** With one occupied subspace the result is the
singleton `⟨ext(d', s_C)⟩`, trivially normalized: a one-member sequence is sorted and
separated, so no merge is possible.

**W14 (absent member, zero count).** The empty link subspace contributes *no* member to the
report, yet `n_{s_L}(d') = 0` remains a fact about `V_{s_L}(d') = ∅` (W1), well-defined
independently of whether the report emits a link member. The report omits the empty subspace
while the count of that subspace is still a defined zero — the very separation W14 records.

**A depth-`3` instance: prefix-confinement is non-vacuous.** Both instances above fix
`m_S = 2`, where the canonical prefix `[S,1,…,1]` collapses to length `m_S − 1 = 1`. There the
only same-depth V-slice tumblers in play are `[S,j]` (excluded when `j > n_S` by the
last-component bound) and `[S',·]` with `S' ≠ S` (excluded by the first component). The step
that W4 and W10 actually turn on — T5's confinement of every interior tumbler to the prefix
`[S,1,…,1]`, which rules out tumblers diverging at an *interior* position while still carrying
an admissible last component — is vacuous at `m_S = 2`. We exercise it at `m_S = 3`, where the
prefix `[S,1]` has length `m_S − 1 = 2` and an interior position genuinely exists between the
subspace identifier and the last component.

Let `V_S(d)` have depth `m_S = 3` with `n_S = 2`, so by D-SEQ★

> `V_S(d) = {[S,1,1], [S,1,2]}`,  `start_S = [S,1,1]`,

and the extent span (W2) is

> `ext(d, S) = ([S,1,1], δ(2,3)) = ([S,1,1], [0,0,2])`,  `reach(ext(d, S)) = [S,1,1] ⊕ [0,0,2] = [S,1,3]`.

The half-open denotation is `⟦ext(d, S)⟧ = {t : [S,1,1] ≤ t < [S,1,3]}`. Now take the V-slice
tumbler `[S,2,1] ∈ VSlice(S, 3)` — a depth-`3`, zero-free tumbler of subspace `S` that agrees
with the active positions on the first component but *diverges at the interior position `2`*,
and whose last component `1` nonetheless lies in the admissible range `1..n_S`. This is exactly
the candidate that the last-component bound alone would *not* reject. By T1 the first
disagreement decides the order: comparing `[S,2,1]` against `reach = [S,1,3]` at position `2`
gives `2 > 1`, so `[S,2,1] > [S,1,3]`, placing it past the upper bound. It is therefore *not*
in `⟦ext(d, S)⟧`. Equivalently, T5 applied to the common prefix `[S,1]` (length `m_S − 1 = 2`)
shared by `start_S` and `reach` confines every interior tumbler to that prefix, and `[S,2,1]`
fails to extend `[S,1]` — so it cannot slip in despite its admissible last component. The
remaining V-slice tumblers within the half-open bounds are exactly `[S,1,1]` and `[S,1,2]`,
their last components pinned to `1..2`, giving

> `⟦ext(d, S)⟧ ∩ VSlice(S, 3) = {[S,1,1], [S,1,2]} = V_S(d)`,

which confirms W4 in the regime where prefix-confinement does the actual work. The
`m_S = 2` instances above check W4 only where the prefix is trivial; this instance checks it
where an off-prefix, admissible-last-component tumbler must be — and is — excluded.

---

## Permanence of the report

A last question: may a later query of the same document identity contradict an earlier one,
the document unchanged? We find that *no primitive permanence attaches to the report itself*
— and that none is needed.

The span-set is a *derived view* of the current arrangement. Its members are computed from
`V_{s_C}(d)` and `V_{s_L}(d)`, which editorial operations reshape: an insertion grows the
text run, a deletion shrinks it, a new link extends the link run. The reported extents are
properties of the *present* arrangement, not permanent attributes of the identity. We record
**W18** (DerivedReport): `RETRIEVEDOCVSPANSET(d)` is a pure function of the current state
`Σ` (by W8), so any two queries against the *same* `Σ` return identical span-sets, and any
query against a *changed* `Σ` may legitimately differ.

Permanence is therefore *inherited, not primitive* — it descends from the stability of the
state, not from any property the operation contributes. If no transition occurs between two
queries, `M(d)` is unchanged, so `V_{s_C}(d)` and `V_{s_L}(d)` are fixed, hence each `n_S` is
a deterministic function of fixed data, hence the report cannot change. (We make no claim
that arrangements are immutable in general: the foundation's vocabulary includes in-place
arrangement mutations — K.μ⁻ contracts and K.μ~ reorders an existing `M(d)`, ASN-0047 — so a
document's extents *can* change under editing. What the report cannot do is change while the
state it views stands still.) We record **W19** (StateStability): against an unchanged state
`Σ`, repeated queries return identical span-sets; a later report contradicts an earlier one
only if `M(d)` changed in between. The link
count is specifically the count of *home* links — links the document owns (CL-OWN) — so a
third party linking *into* the document, owning its link at another address, cannot perturb
the document's reported link extent. The stability the report enjoys is exactly the stability
of the arrangement it views; the operation adds none of its own and needs none.

---

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| W0 | `RETRIEVEDOCVSPANSET(d)` returns a normalized span-set (≤ 2 members), or `⟨⟩` when both counted subspaces are empty; never a content sequence or a cardinality | introduced |
| W1 | `n_S(d) = |V_S(d)|` is the extent of subspace `S` in `d` | introduced |
| W2 | `ext(d, S) = ([S,1,…,1], δ(n_S, m_S))` is the extent span encoding `n_S` | introduced |
| W3 | `ext(d, S)` is a well-formed, level-uniform T12 span with `reach = [S,1,…,1,1+n_S]` | introduced |
| W4 | ExactCoverage — `⟦ext(d, S)⟧ ∩ VSlice(S, m_S) = V_S(d)` (complete and exclusive) | introduced |
| W5 | ExactnessRequiresContiguity — *for `V_S(d) ≠ ∅`*, a single level-uniform span exactly covers `V_S(d)` iff `V_S(d)` is contiguous in `VSlice(S, m)`; forward by constructing the span at the run's *actual* minimum (T0(a)+S8-fin pin a shared prefix, T5 confines the interior), converse by order-convexity (counterexample `{[S,1],[S,3]}`); the empty case is excluded (no span denotes `∅`, S2) and handled by W0 | introduced |
| W6 | `occupied(d) = {S ∈ {s_C, s_L} : V_S(d) ≠ ∅}` | introduced |
| W7 | OneSpanPerOccupiedSubspace — result has exactly `|occupied(d)|` members, one per kind, not per fragment or item | introduced |
| W8 | PureQuery — `Σ' = Σ`; the operation reads and writes nothing | introduced |
| W9 | TwoKindsOnly — `O(d) = V_{s_C}(d) ⊔ V_{s_L}(d)` (derived from S3★-aux); no third subspace holds content, so no third member can arise | introduced |
| W10 | SubspaceConfinement — `(A t : t ∈ ⟦ext(d, S)⟧ : t₁ = S)` | introduced |
| W11 | Disjointness — `⟦ext(d, s_C)⟧ ∩ ⟦ext(d, s_L)⟧ = ∅` | introduced |
| W12 | ProfileIrreducibility — the pair `(n_{s_C}, n_{s_L})` is determined by neither coordinate alone | introduced |
| W13 | UniformShape — result is normalized, members drawn from the fixed ordered kind-list `(s_C, s_L)` | introduced |
| W14 | Comparability — per-kind comparison `n_S(d₁)` vs `n_S(d₂)` is total because `n_S = |V_S(d)|` is a total function (W1), independent of which members the report emits | introduced |
| W15 | Independence — `n_{s_C}` depends only on `V_{s_C}(d)`, `n_{s_L}` only on `V_{s_L}(d)`; subspace edits do not cross | introduced |
| W16 | Partition — the members disjointly cover exactly the counted active V-positions; no orphan, no phantom | introduced |
| W17 | ExtentDeterminesPopulation — active positions of `S` are exactly the V-slice tumblers within `ext(d, S)`, each carrying content | introduced |
| W18 | DerivedReport — the result is a pure function of current state `Σ` | introduced |
| W19 | StateStability — against an unchanged state the report is permanent; it changes only if `M(d)` changes; the link extent counts home links only | introduced |
| W20 | ResultCardinalityWP — `wp(·, "result = ⟨⟩") ≡ d ∈ dom(M) ∧ V_{s_C}(d) = ∅ ∧ V_{s_L}(d) = ∅`; `wp(·, "|result| = 2") ≡ d ∈ dom(M) ∧ V_{s_C}(d) ≠ ∅ ∧ V_{s_L}(d) ≠ ∅`; `wp(·, "|result| = 1") ≡ d ∈ dom(M) ∧ (V_{s_C}(d) = ∅ ⊻ V_{s_L}(d) = ∅)` | introduced |

---

## Open Questions

When a subspace's active positions are non-contiguous, must the per-subspace report fragment into one span per contiguous cluster, or may it return a single bounding span that overshoots interior gaps?

Given that the operation omits an empty subspace entirely (W7) and comparison treats an absent subspace as the value zero (W14), how must a *consumer* interpret an omitted member when comparing reports across documents of differing vintages — under what conditions is "subspace absent" safely read as "extent zero" rather than "subspace not yet supported"?

What permanence must the per-subspace extent report carry across a version fork that shares content with its ancestor?

What must the operation guarantee about a subspace's reported extent when some of its content is transcluded from a source document that is itself edited?

Must the per-subspace extents reported by the operation be derivable from, and consistent with, any single overall extent the document also exposes, and what would a disagreement signify?

Should the subspace convention be extended beyond text and links, what must the operation guarantee so that the kind-list remains fixed and the report stays comparable across documents of different vintages?
