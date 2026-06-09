# ASN-0116: INSERT Operation

*2026-06-08*

## The problem

We are asked what happens when new material is placed into a document. The
question sounds elementary — make room, drop the content in — but each word
of it hides an obligation. *New material* must acquire an identity. *Make
room* must displace what was there without destroying it. *Drop it in* must
leave the document a single coherent sequence, and must do so without
disturbing the links that point into the displaced region, nor the other
documents that may be reading the very same content through shared addresses.

Nelson states the operation in one sentence: an INSERT "inserts `<text set>`
in document `<doc id>` at `<doc vsa>`. The v-stream addresses of any following
characters in the document are increased by the length of the inserted text"
(4/66). Two effects hide in that sentence. Something is *added* — the text set
acquires a home and an identity. Something *shifts* — the following addresses
increase. We will find that these two effects live in two different layers of
the system, and that almost every invariant we must preserve is a statement
about keeping those layers from contaminating each other.

We work in the address space `T` of tumblers under the lexicographic total
order T1, with the displacement algebra `⊕`, `⊖`, and the ordinal shift
`shift(v, n) = v ⊕ δ(n, #v)` that advances a tumbler's final component by `n`
while fixing its prefix (foundation: OrdinalShift, OrdinalDisplacement). We
take as given the two-layer state: a **content store** `Σ.C : T ⇀ Val`, the
append-only ground truth of what content exists, and a per-document
**arrangement** `Σ.M(d) : T ⇀ T`, the partial function from V-positions to
I-addresses that records how document `d` currently arranges that content. A
V-position carries a subspace identifier in its first component, written
`subspace(v) = v₁`; content lives in the text subspace `s_C`, links in `s_L`.
We write `V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}` for the V-positions of
`d` in subspace `S`.

The standing well-formedness facts we will lean on, all inherited from the
arrangement model: every active V-position is zero-free of depth `m ≥ 2` with
all components positive (S8a); within one subspace of one document the
positions share a common depth (S8-depth); the text subspace is *dense* —
`V_S(d) = {[S, 1, …, 1, k] : 1 ≤ k ≤ N}` for some `N ≥ 0` (D-SEQ, with `N = 0`
the empty case), so it occupies a contiguous, gap-free run of ordinals
starting at the canonical first position `[S, 1, …, 1]`. We abbreviate the
`k`-th position of this run as `q_k = [S, 1, …, 1, k]` of depth `m`. The
depth `m` deserves care: S8-depth fixes a single common depth only when
`V_S(d) ≠ ∅`. When the subspace is empty there is no "common depth of
`V_S(d)`" to speak of — the depth is instead supplied by the insertion
position itself, `m := #p`, since the first insertion into an empty subspace
is what *fixes* the depth for all later insertions (foundation:
ValidFirstInsertionPosition, which takes an explicit `m ≥ 2` for exactly this
reason). We carry `m = #p ≥ 2` throughout, equal to the S8-depth of `V_S(d)`
whenever that set is non-empty. With `m` so pinned, we observe the single
arithmetic fact that does all the work below:

> `shift(q_k, n) = q_{k+n}` — advancing the last component by `n` carries the
> `k`-th slot to the `(k+n)`-th, leaving the shared prefix `[S, 1, …, 1]`
> untouched (by OrdinalShift, since `actionPoint(δ(n, m)) = m = #q_k`).

## What is allocated, and why it must be fresh

Consider first the content being inserted. The consultation is unanimous and
emphatic on a single point: at the instant new content enters the document it
acquires a *permanent identity* — an I-address — that is strictly distinct
from the document's *arrangement* of it. "The address of a byte in its native
document is of no concern to the user or to the front end; indeed, it may be
constantly changing… but since the links are to the bytes themselves, any
links to those bytes remain stably attached to them" (4/11, 4/30). Identity is
permanent; arrangement is ephemeral. INSERT is the moment identity is minted.

What identity? Gregory's evidence settles the mechanism precisely. The address
is not drawn from a global counter; it is *derived from the current state* of
the document's own content region. The allocator finds the greatest I-address
already present beneath the document's content scope and returns its successor
— `findpreviousisagr` followed by an increment of one (granf2.c:164, 169). Two
consequences follow that an abstract specification must record. First,
allocation is **monotonic**: the new address strictly exceeds every content
address previously allocated under this document. Second, allocation consults
*position*, never *content* — there is "no hash table, no byte comparison, no
deduplication mechanism anywhere in the insert path" (Q17). Inserting the same
bytes twice yields two distinct addresses.

This is exactly the content-allocation transition of the substrate, and we do
not re-derive it: allocating one unit is the foundation operation **K.α
(ContentAllocation, ASN-0093)**, which commits a fresh content address `a`
scoped to `d`, with

> `a ∉ dom(C)`, `origin(a) = d`, `subspace_I(a) = s_C`.

Its freshness is proved, not assumed — **FirstEmissionFreshness** (when `d`'s
content region is empty) and **SubsequentEmissionFreshness** (otherwise)
discharge `a ∉ dom(C) ∪ dom(L)` against the whole store. The
`findpreviousisagr`-and-increment evidence above is the concrete realisation of
K.α's subsequent-emission branch `a = inc(a_prev, 0)`, where
`a_prev = max{a' ∈ dom(C) : origin(a') = d}`.

For a span of `n` units, INSERT is the `n`-fold composition of K.α along the
single content sub-allocator chain `A_C(d)`: the start `a` is fixed and each
successive address advances by `inc(·, 0) = shift(·, 1)` (a valid address's
significant position is its last). The allocated run is therefore exactly

> `A_new = {shift(a, k) : 0 ≤ k < n}`,

contiguous on `d`'s content chain and fresh as a whole — `A_new ∩ dom(C) = ∅` —
because each K.α step is fresh against the store as it stands after the previous
step (Q14). This is the answer to *what is allocated to hold the new material*:
`n` fresh, contiguous, origin-stamped I-addresses, and the content values written
there.

We record the freshness-and-distinctness guarantee the K.α composition carries,
since it is the load-bearing fact the rest of the argument leans on. It is not
new content: its freshness half is K.α's FirstEmission/SubsequentEmissionFreshness,
and its value-independence half is **S4 (OriginBasedIdentity, ASN-0036)** —
I-addresses from distinct allocation events are distinct regardless of stored
value.

**P0 (OriginIdentity)** *(restatement of K.α freshness + S4).* *For each `k` with
`0 ≤ k < n`, `shift(a, k) ∉ dom(C)`, and `shift(a, k)` is distinct from every
I-address in `dom(C)` regardless of whether `C(shift(a, k))` equals the content
stored at any existing address.*

Why must this hold for *any* implementation? Because everything downstream —
links that survive editing, transclusion, version correspondence, historical
reconstruction — anchors on identity, and identity is intensional (by origin),
not extensional (by value). Were two equal-valued insertions to share an
address, a link to one would silently become a link to the other, and the
"strap between bytes" (4/42) would bind the wrong bytes. The freshness of `P0`
is precisely what lets the rest of the system trust that an I-address names one
content event for all time.

## What shifts, and what the shift must preserve

Now the second effect. The text set is to be placed at a V-position `p`, and
"the v-stream addresses of any following characters… are increased by the
length of the inserted text" (4/66). We must say exactly which positions
follow, by how much, and — the subtle part — what relationship the displaced
positions bear to what they held before.

Let `S = subspace(p)` and let `p = q_J` be a **valid insertion position**:
either `V_S(d)` is empty and `p = q_1` is the canonical first position, or
`V_S(d) = {q_1, …, q_N}` and `p = q_J` for some `1 ≤ J ≤ N+1` (with `J = N+1`
the *append* case, where `p = shift(max(V_S(d)), 1)` is one past the end). This
is the full precondition on the insertion point: depth-`m`, subspace-`S`,
S8a-well-formed, and seated at or one-past an existing slot so that no gap can
open.

The displacement is then completely determined. Reading off `shift(q_k, n) =
q_{k+n}`:

- **Suffix shifts uniformly.** For `v = q_k ∈ V_S(d)` with `v ≥ p` (i.e.
  `k ≥ J`): the position moves to `shift(v, n) = q_{k+n}`, and *it carries its
  content with it*: `M'(d)(shift(v, n)) = M(d)(v)`. The shift is by the same
  constant `n` for every following position, so their relative order is
  preserved exactly.
- **Prefix is untouched.** For `v = q_k ∈ V_S(d)` with `v < p` (i.e. `k < J`):
  `M'(d)(v) = M(d)(v)`. No position before the cut moves.
- **The vacated slots receive the new content.** The positions
  `q_J, …, q_{J+n-1}` — that is, `{shift(p, k) : 0 ≤ k < n}` — are now free, and
  map in lockstep to the freshly allocated run:
  `M'(d)(shift(p, k)) = shift(a, k)` for `0 ≤ k < n`.

Here is the answer to *what relationship the displaced positions bear to the
prior arrangement*. The consultation is sharp on this (Q2): a V-position never
*binds* content; it is an ordinal slot, not a container. After the insertion,
the relation "position `q_J` holds content `X`" is gone — `q_J` now holds new
content, and `X` has moved to `q_{J+n}`. What is preserved is the orthogonal
relation: *content `X` keeps its I-address, and the arrangement re-coordinates
itself around that fixed identity.* The shift is a relabelling of slots, not a
transport of bindings. The invariant runs in the content layer
(`X ↦ I-address`, immutable), never in the position layer (`slot ↦ X`,
deliberately fluid).

We must also state what the operation leaves alone. The displacement is
confined to subspace `S`. Gregory's evidence makes this structural rather than
incidental: the insertion cut is bounded above by the *next subspace boundary*,
so a text insertion at `1.x` shifts text positions but never reaches link
positions at `2.x` (Q12, Q13). Abstractly this is forced by the subspace
identifier sitting in the V-position's first component (foundation: T7): an
ordinal shift advances the last component and cannot cross into another
subspace's region. Hence:

- **Cross-subspace frame.** For every `S' ≠ S`, the positions of `d` in
  subspace `S'` are unchanged in both domain and value.
- **Cross-document frame.** For every `d' ≠ d`, `M'(d') = M(d')`.

We collect the arrangement effect as a named operation.

**INSERT(`d`, `p`, `w₀ … w_{n-1}`).**

*Precondition.* `d ∈ dom(M)`; `n ≥ 1`; `S = subspace(p) = s_C`; `m := #p ≥ 2`,
and when `V_S(d) ≠ ∅` this `m` equals the common depth that S8-depth fixes on
`V_S(d)`; `p` is S8a-well-formed; and `p` is a valid insertion position in the
foundation sense (ASN-0036). The constraint `S = s_C` is load-bearing, not
cosmetic: the allocation below is **K.α (ContentAllocation)**, which yields only
content-subspace addresses (`subspace_I(a) = s_C`). Were `p` to sit in the link
subspace (`S = s_L`), I-NEW would map link-subspace positions `shift(p, k)` —
which OrdinalShift keeps in subspace `s_L` — to content addresses
`shift(a, k)` in subspace `s_C`, violating generalized referential integrity
(S3★, ASN-0047: `subspace(v) = s_L ⟹ M(d)(v) ∈ dom(L)`). INSERT-as-content-
insertion is well-defined only for the text subspace; link placement is a
distinct operation drawing on K.λ, not K.α. The position predicates are:

- if `V_S(d) = ∅`: `ValidFirstInsertionPosition(d, p, m)` — `p` is the canonical
  first position `[S, 1, …, 1]` of depth `m`, and this first insertion *fixes*
  the subspace depth at `m` for every later insertion;
- if `V_S(d) ≠ ∅`: `ValidInsertionPosition(d, p)` — `p = q_J` for some
  `1 ≤ J ≤ N+1`, with `J = N+1` the *append* case `p = shift(max(V_S(d)), 1)`.

Allocation supplies `a` as the K.α-fresh origin-`d` content I-start (above),
with `A_new ∩ dom(C) = ∅`.

*Effect.* INSERT is the composite of `n` content allocations (K.α, ASN-0093) and
one arrangement transition realising the post-insertion shift of ASN-0082's I3
family. We name its clauses but derive them by citation, not from scratch:

- (I-ALLOC) `dom(C') = dom(C) ∪ A_new`, with `C'(shift(a, k)) = w_k` for
  `0 ≤ k < n` — the K.α effect (ASN-0093), iterated `n` times along `A_C(d)`.
- (I-IMM) `(A b : b ∈ dom(C) : C'(b) = C(b))` — K.α append-only (C0, ASN-0093).
- (I-SHIFT) `(A v : v ∈ V_S(d) ∧ v ≥ p : shift(v, n) ∈ dom(M'(d)) ∧
  M'(d)(shift(v, n)) = M(d)(v))` — verbatim ASN-0082 **I3 (PostInsertionShift)**.
- (I-LEFT) `(A v : v ∈ V_S(d) ∧ v < p : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))` —
  ASN-0082 **I3-L (PostInsertionLeftFrame)**.
- (I-NEW) `(A k : 0 ≤ k < n : shift(p, k) ∈ dom(M'(d)) ∧
  M'(d)(shift(p, k)) = shift(a, k))` — the INSERT-specific fill of the block that
  I3 leaves vacated (the positions I3-V withholds from `dom(M'(d))` until they are
  re-populated), mapped in lockstep to the K.α run `A_new`.
- (I-DOM) `{v ∈ dom(M'(d)) : subspace(v) = S} =
  {q_1, …, q_{J-1}} ∪ {q_J, …, q_{J+n-1}} ∪ {q_{J+n}, …, q_{N+n}}` — the domain
  closure ASN-0082 I3-CS/I3-CX specialised to the dense text subspace.

*Frame.*
- (F-SUB) `(A S' : S' ≠ S : {v ∈ dom(M'(d)) : subspace(v) = S'} =
  {v ∈ dom(M(d)) : subspace(v) = S'}` and `M'(d)` agrees with `M(d)` there`)` —
  ASN-0082 **I3-X (PostInsertionCrossSubspaceFrame)**.
- (F-DOC) `(A d' : d' ≠ d : M'(d') = M(d'))` — ASN-0082 **I3-D
  (PostInsertionCrossDocumentFrame)**.

## The document remains one coherent sequence

We must check that the result is well-formed — that we have not opened a gap,
overlaid two positions, or broken the density that lets spans name contiguous
regions. The computation is immediate from `shift(q_k, n) = q_{k+n}` and is
worth doing once in full, because it is the formal content of Nelson's
assurance (Q10) that reading end to end yields the original content with the
new material interleaved at the chosen point.

The three pieces of I-DOM are, as index sets over `q`:
`{1, …, J-1}` (prefix), `{J, …, J+n-1}` (new), `{J+n, …, N+n}` (shifted suffix).
These are consecutive integer intervals with no gap and no overlap; their union
is `{1, …, N+n}`. Therefore

> `V_S(d') = {q_1, …, q_{N+n}}`,

which is again the canonical dense run, now of length `N' = N + n`. We must be
careful about what is inherited and what is INSERT's own obligation, because
ASN-0082's post-insertion arrangement is *not* the filled post-state we want: its
domain closure I3-CS characterises `dom(M'(d)) ∩ S` as left positions ∪ shifted
positions *only*, with the block `{shift(p, k) : 0 ≤ k < n}` deliberately
withheld (I3-V). ASN-0082's `M'(d)` is the *gapped*, room-made arrangement, and
its preservation lemmas establish well-formedness only for those two regions.
The new block is not covered by any of them; each of its properties is an INSERT
obligation that we discharge here.

*Inherited for the left and shifted regions.* For the positions `{q_1, …, q_{J-1}}`
(left) and `{q_{J+n}, …, q_{N+n}}` (shifted suffix), well-formedness is exactly
ASN-0082's family: **I3-VD** (depth uniformity) and **I3-VP** (S8a) for the
positions, **I3-S2** for single-valuedness, **I3-fin** for finiteness, **I3-S3**
for referential integrity. These say nothing about the new block, which is absent
from ASN-0082's `M'(d)`.

*Proved here for the new block* `{shift(p, k) : 0 ≤ k < n}`, mapped by I-NEW to
`{shift(a, k) : 0 ≤ k < n}`:

- *S8a and depth uniformity.* `p = q_J` satisfies S8a (precondition) with `#p = m`.
  By **OrdShiftHom** (ASN-0036), each `shift(p, k)` is zero-free with all
  components positive, `subspace(shift(p, k)) = S`, and `#shift(p, k) = m` (the
  result-length identity of TumblerAdd). So every new-block position is
  S8a-well-formed and shares depth `m` with the left and shifted regions — depth
  uniformity holds across the whole filled subspace.
- *Single-valuedness.* The new-block index set `{J, …, J+n-1}` (as ordinals `q_k`)
  is disjoint from the left set `{1, …, J-1}` and the shifted-suffix set
  `{J+n, …, N+n}` — the three integer intervals are pairwise disjoint (shown
  below). Hence no new-block position coincides with any left or shifted image, and
  within the block the map `k ↦ shift(p, k) = q_{J+k}` is injective (distinct `k`
  give distinct ordinals). `M'(d)` is therefore single-valued on the union.
- *Referential integrity.* Each new-block image is `shift(a, k) ∈ A_new ⊆ dom(C')`
  by I-ALLOC, and `subspace(shift(p, k)) = S = s_C` matches `subspace_I(shift(a, k))
  = s_C`, so S3★ is satisfied for the block: a content-subspace position maps to a
  content address.

*Contiguity is INSERT's own theorem, not an inherited lemma.* There is no
insertion-side contiguity lemma to cite: ASN-0082's gapped `M'(d)` *fails*
contiguity until the block is filled, and the D-family lemmas **D-SEQ-post**,
**D-MIN-post**, **D-CTG-post** are *contraction* results (their post-state is
`{[S, 1, …, 1, k] : 1 ≤ k ≤ N − c}` for a contraction amount `c`) — inapplicable
here. The contiguity of the *filled* post-state is the load-bearing argument we
now give directly. The three index intervals over `q` are `{1, …, J-1}` (prefix),
`{J, …, J+n-1}` (new), `{J+n, …, N+n}` (shifted suffix). These are consecutive
integer intervals — no gap — and pairwise disjoint — no double assignment — with
union `{1, …, N+n}`. Therefore `V_S(d') = {q_1, …, q_{N+n}}` is the canonical dense
run: `min(V_S(d')) = q_1` and the run is gap-free at the fixed depth `m`. This *is*
the D-SEQ/D-MIN/D-CTG property of the post-state, established for INSERT rather
than borrowed. This is also the answer to *how the insertion sits within the
V-stream as a connected region*: the new material occupies exactly the interval
`{q_J, …, q_{J+n-1}}`, a connected, ordered, gap-free block, and the whole stream
around it stays a single coherent ordinal sequence.

Two finer points the consultation insists on. First, inserting a *span* rather
than a single byte is, at the V-layer, no different in kind — the same uniform
shift opens a block of exactly the right size and the suffix slides over by
precisely `n` (Q5). The span enters as a single contiguous run; it is under no
obligation to *stay* contiguous under later editing, but at the moment of
insertion it is connected and ordered (Q4). Second, the new region is
*seamless in arrangement yet distinguishable in identity* (Q9): in the V-stream
there is no marker at the boundary `q_{J-1} | q_J | q_{J+n}` — reading flows
across it without interruption — while in the I-stream every inserted unit
carries a fresh, origin-stamped address that records exactly which span was
introduced. The seam is erased in the arrangement and preserved in the
identity. We record the connected-region fact as a claim:

**P1 (InsertedRun).** *The inserted material forms a single correspondence run:
for `0 ≤ k < n`, `M'(d)(shift(p, k)) = shift(a, k)`, so V-positions and
I-addresses advance in lockstep over a contiguous block. The block
`{shift(p, k) : 0 ≤ k < n}` is order-isomorphic to its image
`{shift(a, k) : 0 ≤ k < n}` under T1.*

## Invariants the operation must preserve

We now discharge the four invariants the question names. Each is a statement
about keeping the content layer and the arrangement layer from contaminating
each other.

**Content immutability.** Nothing already in the document is rewritten; only
arrangement changes (Q3). Formally this is I-IMM together with I-ALLOC's
disjointness: `dom(C)` grows by the fresh run `A_new`, and every prior
`b ∈ dom(C)` retains its value. The store is append-only — `dom(C') ⊇ dom(C)`,
monotone — and the only writes are to addresses that did not previously exist.
We name the layer invariant:

**P2 (ContentAppendOnly).** *`dom(C) ⊆ dom(C')` and
`(A b : b ∈ dom(C) : C'(b) = C(b))`.* INSERT is purely additive on the content
layer.

**Position permanence.** The consultation distinguishes two senses of
"position" with opposite answers (Q6). The *I-address* — content identity — is
permanent: never reused, never reassigned, never made to point at different
content. The *V-position* — the slot in the current arrangement — is
deliberately impermanent: the same slot `q_J` denotes different content before
and after the insert. INSERT honours both halves. It honours I-address
permanence because, by P0, the only new bindings `shift(a, k) ↦ w_k` are at
addresses that *did not exist*, so no existing `b ↦ C(b)` is disturbed and no
address is repurposed. It honours V-position impermanence because that is
exactly what the shift performs — `q_J` now resolves to fresh content while the
content formerly at `q_J` resolves from `q_{J+n}`. The permanence guarantee
attaches to identity, not to arrangement; INSERT is the operation that exploits
the gap between them.

**P3 (AddressPermanence).** *No I-address in `dom(C)` is removed or rebound by
INSERT: `(A b : b ∈ dom(C) : b ∈ dom(C') ∧ C'(b) = C(b))`, and every new
binding is at a fresh address (P0).*

**Link anchoring across the displacement.** A link's endsets reference
I-addresses, not V-positions (4/42, 4/30). Since INSERT removes no I-address
(P3) and adds only fresh ones (P0), every link designates *exactly the same
content* after the operation as before. We can state this without modelling the
link store in detail, using only the foundation notion that a link endpoint is
an endset whose `coverage` is a set of I-addresses, and that its appearance in
document `d` is the set of V-positions of `d` mapping into that coverage. Three
facts hold — the first about the target, the next two about the resolved
witnesses:

- *The link's target is unchanged.* For any endset `e`, `coverage(e)` is a
  function of `e`'s spans alone, and INSERT never edits a stored link value: link
  immutability **L12 (LinkImmutability, ASN-0043)** fixes `Σ'.L(a) = Σ.L(a)` for
  every prior link `a`, so **LP3 (CoverageInvariance, ASN-0098)** gives
  `coverage_{Σ'}(e) = coverage_{Σ}(e)` for every prior endset. We stress what
  does *not* underwrite this: it is *not* that `A_new` is fresh against `dom(C)`.
  Foundation **L4 (EndsetGenerality)** and **L9 (TypeGhostPermission)** let an
  endset reference *any* tumbler, including ghost addresses not yet in `dom(C)`,
  so a pre-existing endset may already name an address that INSERT now mints into
  `A_new`. Coverage-invariance rests on endset immutability, not on freshness.
- *The shifted-suffix witnesses move uniformly.* A link whose coverage includes
  `M(d)(v)` for some shifted `v ≥ p` is now found at `shift(v, n)`, because
  `M'(d)(shift(v, n)) = M(d)(v)` (I-SHIFT) carries the same I-address to the new
  slot. The link did not move to *different content*; the content it always named
  simply sits at a higher V-address.
- *New-block witnesses (resurrection).* Precisely because a prior endset `e` may
  reference an address in `A_new` (the ghost-reference case above), INSERT can
  *add* witnesses to such a link. After the operation the new block carries
  `M'(d)(shift(p, k)) = shift(a, k)`; if `shift(a, k) ∈ coverage(e)` for some
  `0 ≤ k < n`, the V-position `shift(p, k)` newly resolves into `coverage(e)` — a
  resurrection in the sense of **LP18 (ASN-0098)**, an orphaned reference becoming
  discoverable exactly when an arrangement entry to its target appears. These
  witnesses live at the inserted block, not at any `shift(v, n)`.

This is the precise sense of Nelson's survivability clause restricted to
insertion (4/43): because insertion removes nothing, *every* link survives with
its designated content unchanged. What insertion can do is *enlarge* a link's
resolved-witness set — never shrink it, never redirect it. We record it.

**P4 (LinkSurvival).** *For every endset `e` existing in `Σ`,
`coverage_{Σ'}(e) = coverage_{Σ}(e)` (by L12 + LP3) — no link's designated content
changes. The post-insert resolved-witness set of `e` in `d` is
`project(e, d, Σ') = {v ∈ dom(M'(d)) : M'(d)(v) ∈ coverage(e)}`, which decomposes
into four disjoint parts:*

- *Left witnesses: `{v ∈ V_S(d) : v < p ∧ M(d)(v) ∈ coverage(e)}`, preserved
  verbatim by I-LEFT.*
- *Shifted-suffix witnesses: `{shift(v, n) : v ∈ V_S(d) ∧ v ≥ p ∧ M(d)(v) ∈
  coverage(e)}`, carried to the new slot by I-SHIFT.*
- *Cross-subspace witnesses: `{v ∈ dom(M(d)) : subspace(v) ≠ S ∧ M(d)(v) ∈
  coverage(e)}`, preserved verbatim by F-SUB (a link's coverage may include images
  of `d`'s positions in another subspace).*
- *New-block witnesses, present iff `coverage(e) ∩ A_new ≠ ∅`:
  `{shift(p, k) : 0 ≤ k < n ∧ shift(a, k) ∈ coverage(e)}` (resurrection, LP18).*

*The left and cross-subspace parts are common to the prior witness set
`project(e, d, Σ)`; the shifted-suffix part is the image of the prior suffix
witnesses under `v ↦ shift(v, n)`. Hence the post-insert set is a superset of the
prior set, equal to it iff the new-block part is empty, i.e. iff
`coverage(e) ∩ A_new = ∅`.*

**Isolation of documents sharing I-addresses.** Suppose another document `d'`
arranges some of the same content `d` does — `ran(M(d')) ∩ ran(M(d)) ≠ ∅`. The
question is whether inserting into `d` can perturb `d'`. It cannot, and the
proof is the conjunction of three facts already in hand. By F-DOC,
`M'(d') = M(d')` — `d'`'s arrangement is untouched. By P2/P3, the shared
I-addresses retain their content — the bytes `d'` reads are immutable. And the
fresh addresses `A_new` cannot already inhabit `ran(M(d'))`: every arrangement
obeys referential integrity, `ran(M(d')) ⊆ dom(C)` (S3), while `A_new ∩ dom(C) =
∅` by P0, so `A_new ∩ ran(M(d')) = ∅`. (This step turns on *arrangements*, not
endsets: it is valid here precisely because `ran(M(d')) ⊆ dom(C)`, whereas the
analogous "fresh ⇒ not in any endset" inference fails — endsets may name ghost
addresses, L4/L9. The isolation guarantee is about `d'`'s arrangement, so the
valid arrangement-side argument is the one we need.) Therefore `d'` resolves
every one of its V-positions to the same content, in the same order, before and
after: its arrangement *and its reader's experience* are identical (Q8). The isolation is a structural consequence of the two-layer split: INSERT
writes the arrangement of exactly one document (F-DOC) and appends to the global
content store without disturbing any existing entry (P2). Sharing is by
reference to immutable identity, so an insertion into one sharer is invisible to
the others.

**P5 (DocumentIsolation).** *For every `d' ≠ d`: `M'(d') = M(d')`, and for every
`v' ∈ dom(M(d'))`, `M'(d')(v') ∈ dom(C')` with `C'(M'(d')(v')) =
C(M(d')(v'))`. The arrangement and resolved content of every other document are
invariant under INSERT on `d`.*

## A weakest precondition: when is discoverability preserved?

P4 leaves one question pointed but unanswered: under what condition does INSERT
preserve, rather than merely not-shrink, the set of links discoverable from `d`?
It is tempting to assume the answer is "always" — insertion removes nothing.
Computing the weakest precondition shows otherwise, and the place it fails is
exactly the resurrection gap P4 now records.

Write `D(d, Σ) = {a ∈ dom(Σ.L) : discoverable_from(a, d, Σ)}` for the links
discoverable from `d` (foundation `discoverable_from`, ASN-0098). We seek

> `wp(INSERT, "D(d, Σ') = D(d, Σ)")`.

By **LP12 (DiscoverabilityCharacterisation, ASN-0098)**, a link `a` is
discoverable from `d` iff some slot's coverage meets the document's I-address
range: `discoverable_from(a, d, Σ) ⟺ (E i : coverage(Σ.L(a).eᵢ) ∩ ran(M(d)) ≠
∅)`. So the entire question reduces to how INSERT changes `ran(M(d))`. We read it
off the Effect: left positions keep their I-addresses (I-LEFT), shifted positions
carry their I-addresses to new slots (I-SHIFT), and the new block adds exactly
`A_new` (I-NEW). Hence

> `ran(M'(d)) = ran(M(d)) ∪ A_new`.

This is one direction of **LP9 (ExtensionMonotonicity, ASN-0098)** made exact for
the dense subspace: the arrangement range grows by precisely the freshly
allocated run. Substituting into LP12, for every prior link `a`,

```
  discoverable_from(a, d, Σ')
    ⟺ (E i : coverage(eᵢ) ∩ (ran(M(d)) ∪ A_new) ≠ ∅)
    ⟺ discoverable_from(a, d, Σ)  ∨  (E i : coverage(eᵢ) ∩ A_new ≠ ∅).
```

Therefore `D(d, Σ') = D(d, Σ) ∪ {a ∈ dom(Σ.L) : (E i : coverage(Σ.L(a).eᵢ) ∩
A_new ≠ ∅)}`. The two sets coincide iff that added set is empty. The weakest
precondition is thus *not* trivially `true`; it is the operation's precondition
conjoined with a genuine side condition on the allocated run:

> `wp(INSERT, D(d, Σ') = D(d, Σ)) ≡ INSERT-pre ∧ (A a ∈ dom(Σ.L), i :
> coverage(Σ.L(a).eᵢ) ∩ A_new = ∅)`.

The derived consequence is exact and informative. Discoverability from `d` is
preserved precisely when the freshly minted addresses lie outside every prior
endset's coverage — that is, when no ghost reference is being resurrected. Had P4
asserted unconditional preservation, this computation would have refuted it: the
escape branch `coverage(eᵢ) ∩ A_new ≠ ∅` is non-empty exactly in the
ghost-reference case that L4/L9 permit. Two corollaries fall out. (i) A
*sufficient* condition discharging the side condition for free is a tight-endset
discipline: if every prior endset is tight at its creation state (foundation
`tight`, ASN-0098), then **LP19a (TightFreshness)** gives `A_new ∩ coverage(e) =
∅` for every K.α-fresh address, so the wp reduces to `INSERT-pre`. (ii) Absent
that discipline, the wp is the sharpest statement available, and it is the formal
witness that "insertion preserves discoverability" is a *conditional*, not a
theorem.

## A worked insertion

Fix the text subspace `S = s_C` at depth `m = 2`, so `q_k = [s_C, k]` and
`shift(q_k, n) = [s_C, k+n] = q_{k+n}`. Let `d` currently hold `N = 5` text
positions, `V_S(d) = {q_1, …, q_5}`, with I-addresses
`M(d)(q_k) = a_k` for `k = 1, …, 5`. Suppose `d`'s content chain has greatest
I-address `a_max = [d.0.s_C.6]`, so K.α's next emission is
`a = inc(a_max, 0) = [d.0.s_C.7]`.

**Insert `XY` (`n = 2`) at `p = q_3`.** Here `J = 3`, `S = s_C`, `m = #p = 2`,
and `1 ≤ J ≤ N+1`, so `ValidInsertionPosition(d, q_3)` holds.

*Allocation (I-ALLOC, P0).* `A_new = {shift(a, 0), shift(a, 1)} = {[d.0.s_C.7],
[d.0.s_C.8]}`, both fresh (`a_max` was `[d.0.s_C.6]`, so neither `.7` nor `.8`
was in `dom(C)`), contiguous, origin-`d`. Content written: `C'([d.0.s_C.7]) =
X`, `C'([d.0.s_C.8]) = Y`. ✓ P0, P2.

*Shift (I-SHIFT, I-LEFT).* Prefix `q_1, q_2` unchanged (I-LEFT). Suffix `q_k`
with `k ≥ 3` moves by `shift(·, 2)`:

```
  q_3 → q_5  carrying a_3      q_4 → q_6  carrying a_4      q_5 → q_7  carrying a_5
```

*New block (I-NEW, P1).* The vacated block `{shift(p, 0), shift(p, 1)} = {q_3,
q_4}` maps in lockstep to `A_new`: `M'(d)(q_3) = [d.0.s_C.7]`, `M'(d)(q_4) =
[d.0.s_C.8]`. The pair `q_3 < q_4` is order-isomorphic to `[d.0.s_C.7] <
[d.0.s_C.8]`. ✓ P1.

*Domain (I-DOM).* The three index intervals are `{1, 2}` (prefix), `{3, 4}`
(new), `{5, 6, 7}` (shifted suffix) — consecutive, disjoint, union `{1, …, 7}`.
So `V_S(d') = {q_1, …, q_7}`, the dense run with `N' = N + n = 7`. ✓ I-DOM.

*Reading end to end* now yields `a_1, a_2, X, Y, a_3, a_4, a_5` — the original
content with `XY` interleaved between the second and third units, exactly
Nelson's promise (Q10).

**Boundary — append (`J = N + 1 = 6`).** Take `p = q_6 = shift(max(V_S(d)), 1) =
shift(q_5, 1)`, `ValidInsertionPosition(d, q_6)`. No position `v ≥ q_6` lies in
`V_S(d)`, so I-SHIFT is vacuous; I-LEFT preserves all of `q_1, …, q_5`; the new
block `{q_6, q_7}` receives `A_new`. `V_S(d') = {q_1, …, q_5} ∪ {q_6, q_7} =
{q_1, …, q_7}`, `N' = 7`. The inserted material lands at the end, no suffix
moves. ✓ I-DOM, I-NEW, P1.

**Boundary — empty subspace (`V_S(d) = ∅`).** The first insertion fixes the
depth. Choose `m = 2` and `p = q_1 = [s_C, 1]`, so
`ValidFirstInsertionPosition(d, p, 2)` holds. Insert `XY` (`n = 2`): no prefix,
no suffix; the new block `{q_1, q_2}` receives `A_new`. `V_S(d') = {q_1, q_2}`,
`N' = 0 + 2 = 2`, and the subspace depth is now pinned at `m = 2` for every later
insertion. ✓ I-DOM (with `J = 1`, prefix and suffix intervals empty), I-NEW, P1.

## What we have established

Two effects, two layers, kept clean — and, crucially, *composed from foundation
transitions rather than re-derived*. On the content layer INSERT is the `n`-fold
content allocation K.α (ASN-0093), freshness-respecting and monotone (`P0`, `P2`,
`P3`): `n` contiguous, origin-stamped I-addresses are minted and filled, and
nothing prior is touched. On the arrangement layer INSERT is ASN-0082's
post-insertion shift (I3, I3-L, I3-X, I3-D), a uniform ordinal shift confined to
one subspace of one document, opening a gap-free block of exactly the right width
and re-coordinating the suffix around fixed content identities. The
well-formedness of the left and shifted regions is inherited from the I3-VD/I3-VP
family, the new block's well-formedness is discharged directly (S8a via
OrdShiftHom, depth uniformity, single-valuedness, S3★), and the contiguity of the
filled run (`N' = N + n`) is INSERT's own theorem — the consecutive-disjoint
interval argument — not a borrowed contraction lemma; the inserted span enters as
a single connected run (`P1`); every
link survives because it anchors on immutable identity, its coverage fixed by
endset immutability L12+LP3 — and its resolved-witness set can *grow* (never
shrink or redirect) when a prior endset already referenced an address INSERT now
mints (`P4`, resurrection LP18). Every other document is isolated because
identity is shared by reference, not by arrangement (`P5`). And the weakest
precondition for preserving discoverability is not `true` but the side condition
`coverage(e) ∩ A_new = ∅` — discharged for free under a tight-endset discipline,
genuinely binding otherwise. The whole specification is, at bottom, the
discipline of never letting an ephemeral position pretend to be a permanent
identity.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| INSERT | Operation: place `n` fresh content units at valid V-position `p` in document `d`, as the composite K.α (×n) + ASN-0082 I3 shift + new-block fill | introduced (composite) |
| P0 (OriginIdentity) | The `n` allocated I-addresses `{shift(a,k) : 0 ≤ k < n}` are fresh and distinct from all prior addresses, independent of content value | restated (K.α freshness + S4, ASN-0036/0093) |
| P1 (InsertedRun) | The inserted material forms one correspondence run: `M'(d)(shift(p,k)) = shift(a,k)`, V- and I-addresses advancing in lockstep over a contiguous block | introduced |
| P2 (ContentAppendOnly) | `dom(C) ⊆ dom(C')` and existing values preserved; INSERT is purely additive on content | restated (C0, ASN-0093) |
| P3 (AddressPermanence) | No existing I-address is removed or rebound; every new binding is at a fresh address | restated (C0 + P0) |
| P4 (LinkSurvival) | Every prior endset's coverage is unchanged (L12+LP3); post-insert witness set = left ∪ shifted-suffix ∪ cross-subspace ∪ (new-block iff `coverage(e) ∩ A_new ≠ ∅`), a superset of the prior set (resurrection, LP18) | introduced |
| P6 (DiscoverabilityWP) | `wp(INSERT, D(d,Σ')=D(d,Σ)) ≡ INSERT-pre ∧ (∀ prior endset e : coverage(e) ∩ A_new = ∅)`; preservation is conditional, discharged free under tight-endset discipline (LP19a) | introduced |
| P5 (DocumentIsolation) | Every other document's arrangement and resolved content are invariant under INSERT on `d` | introduced |
| I-ALLOC | `dom(C') = dom(C) ∪ A_new`, `C'(shift(a,k)) = w_k` | cited (K.α, ASN-0093), iterated |
| I-SHIFT | V-positions `≥ p` in subspace `S` move to `shift(v,n)`, carrying their I-address | cited (I3, ASN-0082) |
| I-LEFT | V-positions `< p` in subspace `S` are unchanged | cited (I3-L, ASN-0082) |
| I-NEW | The vacated block `{shift(p,k)}` maps to the fresh run `{shift(a,k)}` | introduced (composition glue) |
| I-DOM | `V_S(d')` is the dense run `{q_1, …, q_{N+n}}`; D-SEQ/D-MIN/D-CTG of the filled post-state established here with `N' = N+n` | introduced (interval argument; domain closure cites I3-CS/I3-CX, ASN-0082) |
| F-SUB | Positions in subspaces `S' ≠ S` are unchanged (subspace confinement of the shift) | cited (I3-X, ASN-0082) |
| F-DOC | Arrangements of all documents `d' ≠ d` are unchanged | cited (I3-D, ASN-0082) |

## Open Questions

What must INSERT guarantee when the insertion point names a position that is currently shared, by transclusion, with another document's arrangement?

Under what conditions, if any, may two concurrent insertions into the same document's content scope both claim freshness without a serializing authority?

What invariant relates the fresh I-addresses of an insertion to the document's recorded provenance, and must INSERT establish that relation atomically with allocation?

What relationship must hold between the inserted run's contiguity at creation and the system's obligations after later editing fragments that run?
