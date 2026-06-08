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
`k`-th position of this run as `q_k = [S, 1, …, 1, k]` of depth `m`, and
observe the single arithmetic fact that does all the work below:

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

We elevate this to the governing principle of allocation. Let `a` denote the
I-start chosen for an insertion of width `n`. We require `a` to be **fresh**
against the content store and to carry the document's origin:

> `a ∉ dom(C)`, `origin(a) = d`, `subspace_I(a) = s_C`.

For a span of `n` units, the evidence shows the `n` addresses are allocated
*contiguously* in one pass: the allocator fixes the start and advances by the
full length, consolidating the run into a single I-span (Q14). Using the same
ordinal shift on the content layer — `inc(a, 0) = shift(a, 1)` for a valid
address, since its significant position is its last — the allocated addresses
are exactly

> `A_new = {shift(a, k) : 0 ≤ k < n}`,

and we require the whole run fresh: `A_new ∩ dom(C) = ∅`. This is the answer to
*what is allocated to hold the new material*: `n` fresh, contiguous,
origin-stamped I-addresses, and the content values written there.

We name the freshness-and-distinctness guarantee, because it is the load-bearing
abstract claim and an alternative implementation could not omit it:

**P0 (OriginIdentity).** *For each `k` with `0 ≤ k < n`, `shift(a, k) ∉ dom(C)`,
and `shift(a, k)` is distinct from every I-address in `dom(C)` regardless of
whether `C(shift(a, k))` equals the content stored at any existing address.*

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

*Precondition.* `d ∈ dom(M)`; `n ≥ 1`; `S = subspace(p)`; `p` is S8a-well-formed
of the common depth `m` of `V_S(d)`; `p` is a valid insertion position (`p = q_1`
if `V_S(d) = ∅`, else `p = q_J` for some `1 ≤ J ≤ N+1`); `a` is the fresh
origin-`d` content I-start with `A_new ∩ dom(C) = ∅`.

*Effect.*
- (I-ALLOC) `dom(C') = dom(C) ∪ A_new`, with `C'(shift(a, k)) = w_k` for
  `0 ≤ k < n`.
- (I-IMM) `(A b : b ∈ dom(C) : C'(b) = C(b))`.
- (I-SHIFT) `(A v : v ∈ V_S(d) ∧ v ≥ p : shift(v, n) ∈ dom(M'(d)) ∧
  M'(d)(shift(v, n)) = M(d)(v))`.
- (I-LEFT) `(A v : v ∈ V_S(d) ∧ v < p : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`.
- (I-NEW) `(A k : 0 ≤ k < n : shift(p, k) ∈ dom(M'(d)) ∧
  M'(d)(shift(p, k)) = shift(a, k))`.
- (I-DOM) `{v ∈ dom(M'(d)) : subspace(v) = S} =
  {q_1, …, q_{J-1}} ∪ {q_J, …, q_{J+n-1}} ∪ {q_{J+n}, …, q_{N+n}}`.

*Frame.*
- (F-SUB) `(A S' : S' ≠ S : {v ∈ dom(M'(d)) : subspace(v) = S'} =
  {v ∈ dom(M(d)) : subspace(v) = S'}` and `M'(d)` agrees with `M(d)` there`)`.
- (F-DOC) `(A d' : d' ≠ d : M'(d') = M(d'))`.

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

which is again the canonical dense run, now of length `N' = N + n`. D-SEQ,
D-MIN (`min(V_S(d')) = q_1`), and D-CTG (contiguity) are preserved with the new
count. No position is skipped — no gap; no position is doubly assigned — the
three index intervals are disjoint, so `M'(d)` is single-valued and remains a
function. This is the answer to *how the insertion sits within the V-stream as
a connected region*: the new material occupies exactly the interval
`{q_J, …, q_{J+n-1}}`, a connected, ordered, gap-free block, and the whole
stream around it stays a single coherent ordinal sequence.

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
document `d` is the set of V-positions of `d` mapping into that coverage. Two
facts hold:

- *The link's target is unchanged.* For any endset `e`, `coverage(e)` is a
  function of I-addresses alone; INSERT alters no existing I-address and the new
  addresses `A_new` are fresh, hence absent from any endset created before this
  operation. So `coverage(e)` is identical in `Σ` and `Σ'` for every prior
  endset.
- *The resolved V-positions reflect the new layout.* A link whose coverage
  includes `M(d)(v)` for some shifted `v ≥ p` is now found at `shift(v, n)`,
  because `M'(d)(shift(v, n)) = M(d)(v)` (I-SHIFT) carries the same I-address to
  the new slot. The link did not move to *different content*; the content it
  always named simply sits at a higher V-address.

This is the precise sense of Nelson's survivability clause restricted to
insertion (4/43): because insertion removes nothing, *every* link survives, and
each comes to rest on the same bytes it designated before. We record it.

**P4 (LinkSurvival).** *For every endset `e` existing in `Σ`,
`coverage_{Σ'}(e) = coverage_{Σ}(e)`; and for every V-position `v ≥ p` in
`V_S(d)` whose image lies in `coverage(e)`, the witness in `Σ'` is
`shift(v, n)`. No link's designated content changes; only its resolved
V-positions reflect the post-insert arrangement.*

**Isolation of documents sharing I-addresses.** Suppose another document `d'`
arranges some of the same content `d` does — `ran(M(d')) ∩ ran(M(d)) ≠ ∅`. The
question is whether inserting into `d` can perturb `d'`. It cannot, and the
proof is the conjunction of three facts already in hand. By F-DOC,
`M'(d') = M(d')` — `d'`'s arrangement is untouched. By P2/P3, the shared
I-addresses retain their content — the bytes `d'` reads are immutable. And by
P0, the addresses `A_new` are fresh, so they appear in no endset and no
arrangement that existed before, in particular not in `M(d')`. Therefore `d'`
resolves every one of its V-positions to the same content, in the same order,
before and after: its arrangement *and its reader's experience* are identical
(Q8). The isolation is a structural consequence of the two-layer split: INSERT
writes the arrangement of exactly one document (F-DOC) and appends to the global
content store without disturbing any existing entry (P2). Sharing is by
reference to immutable identity, so an insertion into one sharer is invisible to
the others.

**P5 (DocumentIsolation).** *For every `d' ≠ d`: `M'(d') = M(d')`, and for every
`v' ∈ dom(M(d'))`, `M'(d')(v') ∈ dom(C')` with `C'(M'(d')(v')) =
C(M(d')(v'))`. The arrangement and resolved content of every other document are
invariant under INSERT on `d`.*

## What we have established

Two effects, two layers, kept clean. On the content layer INSERT is a
freshness-respecting, monotone append (`P0`, `P2`, `P3`): `n` contiguous,
origin-stamped I-addresses are minted and filled, and nothing prior is touched.
On the arrangement layer INSERT is a uniform ordinal shift confined to one
subspace of one document (I-SHIFT, I-LEFT, I-NEW, F-SUB, F-DOC), opening a
gap-free block of exactly the right width and re-coordinating the suffix around
fixed content identities. The well-formedness of the V-stream is preserved
(D-SEQ/D-MIN/D-CTG with `N' = N + n`), the inserted span enters as a single
connected run (`P1`), every link survives because it anchors on immutable
identity (`P4`), and every other document is isolated because identity is shared
by reference, not by arrangement (`P5`). The whole specification is, at bottom,
the discipline of never letting an ephemeral position pretend to be a permanent
identity.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| INSERT | Operation: place `n` fresh content units at valid V-position `p` in document `d`; allocate, append, shift | introduced |
| P0 (OriginIdentity) | The `n` allocated I-addresses `{shift(a,k) : 0 ≤ k < n}` are fresh and distinct from all prior addresses, independent of content value | introduced |
| P1 (InsertedRun) | The inserted material forms one correspondence run: `M'(d)(shift(p,k)) = shift(a,k)`, V- and I-addresses advancing in lockstep over a contiguous block | introduced |
| P2 (ContentAppendOnly) | `dom(C) ⊆ dom(C')` and existing values preserved; INSERT is purely additive on content | introduced |
| P3 (AddressPermanence) | No existing I-address is removed or rebound; every new binding is at a fresh address | introduced |
| P4 (LinkSurvival) | Every prior endset's coverage is unchanged; shifted links resolve at `shift(v,n)`, designating the same content | introduced |
| P5 (DocumentIsolation) | Every other document's arrangement and resolved content are invariant under INSERT on `d` | introduced |
| I-ALLOC | `dom(C') = dom(C) ∪ A_new`, `C'(shift(a,k)) = w_k` | introduced |
| I-SHIFT | V-positions `≥ p` in subspace `S` move to `shift(v,n)`, carrying their I-address | introduced |
| I-LEFT | V-positions `< p` in subspace `S` are unchanged | introduced |
| I-NEW | The vacated block `{shift(p,k)}` maps to the fresh run `{shift(a,k)}` | introduced |
| I-DOM | `V_S(d')` is the dense run `{q_1, …, q_{N+n}}`; D-SEQ/D-MIN/D-CTG preserved with `N' = N+n` | introduced |
| F-SUB | Positions in subspaces `S' ≠ S` are unchanged (subspace confinement of the shift) | introduced |
| F-DOC | Arrangements of all documents `d' ≠ d` are unchanged | introduced |

## Open Questions

What must INSERT guarantee when the insertion point names a position that is currently shared, by transclusion, with another document's arrangement?

Under what conditions, if any, may two concurrent insertions into the same document's content scope both claim freshness without a serializing authority?

What invariant relates the fresh I-addresses of an insertion to the document's recorded provenance, and must INSERT establish that relation atomically with allocation?

What must the operation guarantee about the well-formedness of an insertion position whose subspace is currently empty, so that the first inserted unit fixes the subspace depth consistently for all later insertions?

What relationship must hold between the inserted run's contiguity at creation and the system's obligations after later editing fragments that run?
