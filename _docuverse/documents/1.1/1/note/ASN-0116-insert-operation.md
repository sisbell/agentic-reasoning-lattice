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
`d` in subspace `S`. We work inside ASN-0047's extended state
`Σ = (C, L, E, M, R)`; beyond `C` and `M` the one further component INSERT
touches is the **provenance relation** `Σ.R ⊆ T_elem × E_doc` (pairs of an
element-level I-address and a document), the record coupling each content
I-address to the document that placed it, where `E_doc = dom(M)` is the set of
allocated documents. The consultation is emphatic that this
coupling is *not* a separately-maintained relation but is established by the
act of insertion itself — "the origin IS the address," minted as content
enters the document (4/11, theory answer). INSERT therefore carries an
obligation to grow `R` in lockstep with allocation.

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
significant position is its last, so `inc(·, 0)` increments the final component —
**TA5-SigValid** and **TA5(c)**, ASN-0034). The allocated run is therefore exactly

> `A_new = {shift(a, k) : 0 ≤ k < n}`,

contiguous on `d`'s content chain and fresh as a whole — `A_new ∩ dom(C) = ∅` —
because each K.α step is fresh against the store as it stands after the previous
step (Q14). The run `A_new` is thus `n` fresh, contiguous, origin-stamped
I-addresses, with the content values written there.

**P0 (OriginIdentity)** *(restatement of K.α freshness + **S4 (OriginBasedIdentity,
ASN-0036)**: I-addresses from distinct allocation events are distinct regardless of
stored value).* *For each `k` with
`0 ≤ k < n`, `shift(a, k) ∉ dom(C)`, and `shift(a, k)` is distinct from every
I-address in `dom(C)` regardless of whether `C(shift(a, k))` equals the content
stored at any existing address.*

Identity is intensional (by origin), not extensional (by value). Were two
equal-valued insertions to share an address, a link to one would silently
become a link to the other, and the "strap between bytes" (4/42) would bind the
wrong bytes.

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

The consultation is sharp on the relationship the displaced positions bear to the
prior arrangement (Q2): a V-position never *binds* content; it is an ordinal slot,
not a container. After the insertion,
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

*Precondition.* `d ∈ dom(M) = E_doc` (the document is an allocated entity, so the
provenance step below has a legal home); `Σ` is reachable from `Σ₀` by a valid
transition trace — hence a composite boundary — so the per-state invariants together
with the composite-boundary properties of ExtendedReachableStateInvariants
(ASN-0047), in particular P7a (ProvenanceCoverage), hold at the pre-state; `n ≥ 1`; `(A k : 0 ≤ k < n : w_k ∈ Val)` — each
inserted unit is a well-formed content value, the typing obligation the K.α step
below carries (ASN-0093: K.α commits `a ↦ v` only for `v ∈ Val`); `S = subspace(p) = s_C`;
`m := #p ≥ 2`, and when `V_S(d) ≠ ∅` this `m` equals the common depth that
S8-depth fixes on `V_S(d)`; `p` is S8a-well-formed; and `p` is a valid insertion
position in the foundation sense (ASN-0036). Link placement is a distinct
operation drawing on K.λ, not K.α. The position predicates are:

- if `V_S(d) = ∅`: `ValidFirstInsertionPosition(d, p, m)` — `p` is the canonical
  first position `[S, 1, …, 1]` of depth `m`, and this first insertion *fixes*
  the subspace depth at `m` for every later insertion;
- if `V_S(d) ≠ ∅`: `ValidInsertionPosition(d, p)` — `p = q_J` for some
  `1 ≤ J ≤ N+1`, with `J = N+1` the *append* case `p = shift(max(V_S(d)), 1)`.

Allocation supplies `a` as the K.α-fresh origin-`d` content I-start (above),
with `A_new ∩ dom(C) = ∅`.

*Effect.* INSERT is the composite of `n` content allocations (K.α, ASN-0093), an
arrangement contraction–extension pair `K.μ⁻` then `K.μ⁺` (degenerating to a single
`K.μ⁺` when no suffix moves) whose net effect realises the post-insertion shift of
ASN-0082's I3 family, and `n` provenance recordings (K.ρ, ASN-0047) that couple each
allocated address to `d`. We record first the **block-disjointness
fact**: as ordinals `q`, the three index intervals `{1, …, J-1}` (left),
`{J, …, J+n-1}` (block), and `{J+n, …, N+n}` (shifted suffix) are consecutive —
with no integer gap — and pairwise disjoint, their union being `{1, …, N+n}`
(immediate from `0 < J ≤ N+1`: the right endpoint of each interval is one below the
left endpoint of the next). We name the clauses but derive them by citation, not from
scratch:

- (I-ALLOC) `dom(C') = dom(C) ∪ A_new`, with `C'(shift(a, k)) = w_k` for
  `0 ≤ k < n` — the K.α effect (ASN-0093), iterated `n` times along `A_C(d)`.
- (I-IMM) `(A b : b ∈ dom(C) : C'(b) = C(b))` — K.α append-only (C0, ASN-0093).
- (I-SHIFT) `(A v : v ∈ V_S(d) ∧ v ≥ p : shift(v, n) ∈ dom(M'(d)) ∧
  M'(d)(shift(v, n)) = M(d)(v))` — by ASN-0082 **I3 (PostInsertionShift)** together
  with the block-disjointness fact above. I3 fixes these values on ASN-0082's
  *gapped* arrangement `M'₀(d)`, whose domain (by I3-V/I3-CS) excludes the inserted
  block; INSERT's post-state is `M'(d) = M'₀(d) ∪ {block fill}`. Since the block
  (index interval `{J, …, J+n-1}`) is disjoint from the shifted-suffix positions
  (index interval `{J+n, …, N+n}`), the union adds no entry at any shifted-suffix
  slot and I3's values transfer unchanged.
- (I-LEFT) `(A v : v ∈ V_S(d) ∧ v < p : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))` —
  by ASN-0082 **I3-L (PostInsertionLeftFrame)** together with the block-disjointness
  fact above: the block (index interval `{J, …, J+n-1}`) is disjoint from the left
  positions `{1, …, J-1}`, so the union `M'₀(d) ∪ {block fill}` leaves I3-L's values
  on the left region unchanged.
- (I-NEW) `(A k : 0 ≤ k < n : shift(p, k) ∈ dom(M'(d)) ∧
  M'(d)(shift(p, k)) = shift(a, k))` — the INSERT-specific fill of the block that
  ASN-0082's gapped arrangement leaves vacated, mapped in lockstep to the K.α run
  `A_new`. A block position is `shift(p, k) = q_{J+k}` for `0 ≤ k < n`, lying in
  `dom(M(d))` iff its index `J+k ≤ N`. Its absence from the gapped arrangement is
  attributed by index: a position of index `≤ N` (hence `≥ p` and not in the shifted
  image) is withheld by I3-V (PostInsertionVacating, which quantifies over
  `v ∈ dom(M(d))`); a position of index `> N` (never in `dom(M(d))`) is withheld
  instead by the domain-closure characterisation I3-CS. The attribution is sound
  because no block position is a shifted-suffix image: such an image is
  `q_i = shift(u, n)` for some `u = q_{i−n}` of index `i − n ≥ J`, whereas every
  block index satisfies `i ≤ J + n − 1`, so `i − n ≤ J − 1 < J`, forcing `u < p` —
  outside the shifted-suffix range I3-CS quantifies over. So I3-CS adds no entry at
  any block position.
- (I-DOM) `{v ∈ dom(M'(d)) : subspace(v) = S} =
  {q_1, …, q_{J-1}} ∪ {q_J, …, q_{J+n-1}} ∪ {q_{J+n}, …, q_{N+n}}`. The left
  prefix `{q_1, …, q_{J-1}}` and shifted suffix `{q_{J+n}, …, q_{N+n}}` are the
  gapped domain that ASN-0082 I3-CS (PostInsertionSubspaceClosure) characterises —
  the subspace-`S` closure being exactly the domain this equation ranges over; the
  middle block `{q_J, …, q_{J+n-1}}` — exactly the interval
  I3-V vacates and I3-CS excludes — is contributed by INSERT's own I-NEW fill.
- (I-PROV) `R' = R ∪ {(shift(a, k), d) : 0 ≤ k < n}` — the `n` provenance records
  coupling each freshly allocated I-address to its inserting document, by **K.ρ
  (ProvenanceRecording, ASN-0047)** iterated `n` times. Each K.ρ step's precondition
  `shift(a, k) ∈ dom(C') ∧ d ∈ E_doc` is met: `shift(a, k)` is in the store the
  moment its K.α step commits it, and `d ∈ dom(M) = E_doc` by precondition. The
  record is `(shift(a, k), d)` with `shift(a, k)` element-level content (S7b/C1) and
  `d` document-level, matching `Σ.R ⊆ T_elem × E_doc`. These are the only additions
  to `R`; INSERT removes nothing from it (P2 of ASN-0047, R monotone).

*Frame.*
- (F-SUB) `(A S' : S' ≠ S : {v ∈ dom(M'(d)) : subspace(v) = S'} =
  {v ∈ dom(M(d)) : subspace(v) = S'}` and `M'(d)` agrees with `M(d)` there`)` —
  ASN-0082 **I3-X (PostInsertionCrossSubspaceFrame)**.
- (F-DOC) `(A d' : d' ≠ d : M'(d') = M(d'))` — ASN-0082 **I3-D
  (PostInsertionCrossDocumentFrame)**.
- (F-LINK) `Σ'.L = Σ.L` — the link store is untouched. INSERT's only K-atomics are
  K.α (content), K.μ⁻/K.μ⁺ (arrangement), and K.ρ (provenance); none touches `Σ.L`.
- (F-ENT) `Σ'.E = Σ.E` — the entity set is untouched. INSERT registers no entity
  (it requires `d ∈ dom(M) = E_doc` already).

We derive once, from these clauses, the range identity of the post-state
arrangement:

- (RAN) **Range identity.** `ran(M'(d)) = ran(M(d)) ∪ A_new`, and the I-addresses
  *new to the content-subspace range* of `M'(d)` are exactly
  `A_new = {shift(a, k) : 0 ≤ k < n}`. In the content subspace, I-LEFT keeps the
  left images verbatim, I-SHIFT carries each suffix image to its new slot (so those
  addresses are range-old — already in `ran(M(d))`, merely re-slotted), and I-NEW
  adds exactly `A_new`; hence the content-subspace range gains precisely `A_new` and
  loses nothing. Across the other subspaces F-SUB fixes the per-position images
  (`{M'(d)(v) : subspace(v) = S'} = {M(d)(v) : subspace(v) = S'}` for every
  `S' ≠ S`), so the cross-subspace range is unchanged. Taking the union of the
  content-subspace and cross-subspace contributions gives the full-range identity
  `ran(M'(d)) = ran(M(d)) ∪ A_new`.

## INSERT as a valid composite over the K-vocabulary

The Effect names its clauses by citation, but ASN-0047's reachable-state machinery —
**ExtendedReachableStateInvariants** for the post-state, and the coupling constraints
discharged below — applies only to a *valid composite* (**ValidComposite★**): a finite
sequence of atomic transitions in which (clause 1) each step's precondition holds at the
*intermediate* state it acts on, and (clause 2) the coupling constraints J0, J1★, J1'★
hold *only* between the initial and final states. INSERT sequences just four of the
atomics — `K.α`, `K.μ⁻`, `K.μ⁺`, `K.ρ` — and we discharge clause 2 at the boundary
below. The arrangement change is *not*
itself one of these atomics. It rewrites
the I-address at *existing* suffix positions — `M(d)(q_k)` at `q_k` becomes
`M'(d)(q_{k+n})` at `q_{k+n}` — which K.μ⁺'s prior-domain agreement
(`M'(d)(v) = M(d)(v)` for `v ∈ dom(M(d))`) forbids, while it strictly *grows* the
domain, which K.μ⁻ and K.μ~ (the latter by K.μ~-FIX, `dom(M'(d)) = dom(M(d))`) both
forbid. ASN-0082's I3 family is a displacement *postcondition spec*, not a
K-transition. We therefore exhibit INSERT as an explicit sequence and discharge each
step's precondition.

*Suffix-present case `1 ≤ J ≤ N`* (a genuine suffix `{q_J, …, q_N}` must move). The
sequence, read left to right with each step evaluated against the state its
predecessors leave, is

> `K.α₁, …, K.αₙ`  →  `K.μ⁻`  →  `K.μ⁺`  →  `K.ρ₁, …, K.ρₙ`.

- *`K.α₁, …, K.αₙ` (allocate).* Each commits one fresh content address along `A_C(d)`;
  the `k`-th acts on a store already holding `{shift(a, 0), …, shift(a, k−1)}`, against
  which **SubsequentEmissionFreshness** gives `shift(a, k) ∉ dom(C) ∪ dom(L)`. The
  precondition `d ∈ dom(M)` holds throughout — no K.α step touches `M`. After these `n`
  steps `dom(C)` has grown by `A_new` and `M(d)` is still the original `{q_1, …, q_N}`.
- *`K.μ⁻` (vacate the suffix).* Acting on `d ∈ E_doc`, retain the content-subspace
  prefix `n'_{s_C} = J−1` and the link subspace in full (`n'_{s_L} = n_{s_L}`). Since
  `J−1 < N = n_{s_C}`, the content subspace contracts strictly, so K.μ⁻'s "at least one
  subspace strictly contracts" precondition is met; the retained domain is
  `{q_1, …, q_{J−1}} ∪ V_{s_L}(d)`. The intermediate text subspace is now the prefix
  alone, the link subspace untouched. At the front-insertion extreme `J = 1` this
  branch still fires with `n'_{s_C} = 0`: the content subspace clears entirely (the
  retained prefix `{q_1, …, q_0}` is empty), strict contraction `0 < N` still holding,
  so the whole suffix is vacated and re-installed `n` higher by the following K.μ⁺ —
  distinct from the append case (where K.μ⁻ is dropped) and the empty subspace (where
  there is no suffix to shift).
- *`K.μ⁺` (install block and shifted suffix).* Acting on `d`, add the I-NEW block
  and the I-SHIFT shifted suffix — the same mappings the Effect fixes (the values are
  pinned there, via I3); this step installs them as one domain-extending transition
  and discharges its preconditions. Clause 1 at this intermediate state: (i) every added target lies in
  `dom(C)` — the block targets `A_new`, just committed by K.α, and the shifted-suffix
  targets are the old suffix addresses `{M(d)(q_J), …, M(d)(q_N)} ⊆ dom(C)` — which is
  exactly why the allocations must precede this step; (ii) every added V-position is
  S8a-well-formed of depth `m` (shown below); (iii) the resulting content subspace
  `{q_1, …, q_{N+n}}` is the dense run, so S8-depth, D-CTG★, D-MIN★ hold; (iv) every
  added position sits in subspace `s_C`, meeting the amended K.μ⁺ content-subspace
  restriction; and (v) the domain grows strictly (`J−1 < N+n`). The prior positions
  `{q_1, …, q_{J−1}}` are untouched, so prior-domain agreement holds — K.μ⁺ never
  rewrites an existing entry.
- *`K.ρ₁, …, K.ρₙ` (record provenance).* The `k`-th records `(shift(a, k), d)`; its
  precondition `shift(a, k) ∈ dom(C') ∧ d ∈ E_doc` holds because `shift(a, k)` entered
  the store at its K.α step and `d ∈ dom(M) = E_doc`.

The `K.μ⁻` then `K.μ⁺` pair is the K-atomic realization of the Effect's
I-LEFT/I-SHIFT/I-NEW clauses — prefix fixed, suffix vacated and re-installed `n`
higher, block filled.

*Append case `J = N+1` and empty case `V_S(d) = ∅`* (no suffix moves). I-SHIFT is
vacuous and no contraction is needed; the sequence collapses to

> `K.α₁, …, K.αₙ`  →  `K.μ⁺`  →  `K.ρ₁, …, K.ρₙ`,

the single K.μ⁺ adding only the new block `{q_J, …, q_{J+n−1}} → A_new` above the
untouched prefix `{q_1, …, q_N}` (empty when `V_S(d) = ∅`). Its preconditions are
discharged exactly as in (i)–(v) above, with prior-domain agreement again holding
because the prefix is left in place. Dropping K.μ⁻ here is forced, not optional: with
`J−1 = N = n_{s_C}` the content subspace would not contract strictly, so K.μ⁻ is
*inapplicable* — and unnecessary, since nothing is vacated.

In both cases the coupling constraints (clause 2) are checked only at the composite
boundary, discharged in the provenance section below. With clause 1 verified
step-by-step and clause 2 at the boundary, INSERT is a valid composite; since `Σ` is
reachable from `Σ₀`
(precondition), the post-state is reachable too, and the appeal to
ExtendedReachableStateInvariants for its post-state is licensed.

## The document remains one coherent sequence

We must check that the result is well-formed — that we have not opened a gap,
overlaid two positions, or broken the density that lets spans name contiguous
regions. The computation is immediate from `shift(q_k, n) = q_{k+n}` and is
worth doing once in full, because it is the formal content of Nelson's
assurance (Q10) that reading end to end yields the original content with the
new material interleaved at the chosen point.

The post-state text domain `V_S(d')` is the union of I-DOM's three index
intervals over `q` — `{1, …, J-1}` (prefix), `{J, …, J+n-1}` (new),
`{J+n, …, N+n}` (shifted suffix) — and equals the canonical dense run
`{q_1, …, q_{N+n}}` of length `N' = N + n`. These three index intervals are
consecutive, pairwise disjoint, and union to `{1, …, N+n}` — the
**block-disjointness fact** stated in the Effect, which the arguments below rest on.
We must be
careful about what is inherited and what is INSERT's own obligation, because
ASN-0082's post-insertion arrangement is *not* the filled post-state we want: its
domain closure I3-CS characterises `dom(M'(d)) ∩ S` as left positions ∪ shifted
positions *only*, with the block `{shift(p, k) : 0 ≤ k < n}` deliberately
withheld — *per block position*: by I3-V where the position pre-existed
(`shift(p, k) ∈ dom(M(d))`, index `≤ N`) and by the I3-CS domain closure itself
where it did not (`shift(p, k) ∉ dom(M(d))`, index `> N`, never in `dom(M(d))` for
I3-V to range over). ASN-0082's `M'(d)` is the *gapped*, room-made arrangement, and
its preservation lemmas establish well-formedness only for those two regions.
The new block is not covered by any of them; each of its properties is an INSERT
obligation that we discharge here. Two of ASN-0082's preservation lemmas do not
transfer even on the left and shifted regions: **I3-S3** (referential integrity) and
**I3-S7** (content-store invariants) are both proved under the content frame **I3-C**
(`dom(C') = dom(C)`), which INSERT breaks via I-ALLOC; and the contiguity lemmas
**D-SEQ-post**/**D-MIN-post**/**D-CTG-post** are *contraction* results (post-state
`{[S, 1, …, 1, k] : 1 ≤ k ≤ N − c}`), inapplicable to a fill. We therefore discharge
referential integrity, content-store invariants, and contiguity directly below.

*Left and shifted regions.* For the positions `{q_1, …, q_{J-1}}` (left) and
`{q_{J+n}, …, q_{N+n}}` (shifted suffix), well-formedness is exactly ASN-0082's
family: **I3-VD** (depth uniformity) and **I3-VP** (S8a) for the positions,
**I3-S2** for single-valuedness, **I3-fin** for finiteness. Referential integrity is
discharged directly: each left or shifted position `v` lies in subspace `S = s_C`,
so `M(d)(v) ∈ dom(C)` (S3★ at the pre-state, content-subspace clause
`subspace(v) = s_C ⟹ M(d)(v) ∈ dom(C)`), and `dom(C) ⊆ dom(C')` by append-only
monotonicity (P2), so the image lies in `dom(C')` and S3★ holds for both regions.

*Content-store invariants for the freshly allocated run.* The post-state's
content-store invariants for `A_new` — `zeros(a) = 3` (S7b), `#E(a) ≥ 2` (C1b),
`origin(a) = d` (S7a/C2), allocator conformance (C1c) — are discharged at the source:
each `shift(a, k) ∈ A_new` is a K.α emission, and K.α establishes exactly these
(ASN-0093: **C1** for `zeros = 3`, **C1b** for `#E ≥ 2`, **C1c** for allocator
conformance, **C2** for `origin(a) = d`). The unchanged addresses `b ∈ dom(C)` retain
them by P2 (append-only: domains grow, values fixed). Thus every content address in
`dom(C')` — old and new — is structurally valid element-level content, as
ExtendedReachableStateInvariants (ASN-0047) demands.

*Proved here for the new block* `{shift(p, k) : 0 ≤ k < n}`, mapped by I-NEW to
`{shift(a, k) : 0 ≤ k < n}`:

- *S8a and depth uniformity.* `p = q_J` satisfies S8a (precondition) with `#p = m`.
  The block index runs `0 ≤ k < n`, which we split at the boundary. For `k = 0`,
  `shift(p, 0) = p` is S8a-well-formed directly by precondition, with `#p = m` —
  OrdShiftHom does not apply here, since its shift amount precondition is `n ≥ 1`.
  For `1 ≤ k < n`, **OrdShiftHom** (ASN-0036) applies: each `shift(p, k)` is
  zero-free with all components positive, `subspace(shift(p, k)) = S`, and
  `#shift(p, k) = m` (the result-length identity of TumblerAdd). So every new-block
  position is S8a-well-formed and shares depth `m` with the left and shifted
  regions — depth uniformity holds across the whole filled subspace.
- *Single-valuedness.* The new-block index set `{J, …, J+n-1}` (as ordinals `q_k`)
  is disjoint from the left set `{1, …, J-1}` and the shifted-suffix set
  `{J+n, …, N+n}` — by the block-disjointness fact. Hence no
  new-block position coincides with any left or shifted image, and
  within the block the map `k ↦ shift(p, k) = q_{J+k}` is injective (distinct `k`
  give distinct ordinals). `M'(d)` is therefore single-valued on the union.
- *Referential integrity.* Each new-block image is `shift(a, k) ∈ A_new ⊆ dom(C')`
  by I-ALLOC, and `subspace(shift(p, k)) = S = s_C` matches `subspace_I(shift(a, k))
  = s_C`, so S3★ is satisfied for the block: a content-subspace position maps to a
  content address.

*Contiguity of the filled post-state.* By the block-disjointness fact, the prefix
`{1, …, J-1}`, new `{J, …, J+n-1}`, and shifted suffix `{J+n, …, N+n}` are
consecutive — no gap — and pairwise disjoint — no double assignment — with
union `{1, …, N+n}`. Therefore `V_S(d') = {q_1, …, q_{N+n}}` is the canonical dense
run: `min(V_S(d')) = q_1` and the run is gap-free at the fixed depth `m`. This *is*
the D-SEQ/D-MIN/D-CTG property of the post-state, established for INSERT rather
than borrowed. The new material occupies exactly the interval
`{q_J, …, q_{J+n-1}}`, a connected, ordered, gap-free block, and the whole stream
around it stays a single coherent ordinal sequence.

*Per-subspace run decomposition.* **S8★ (PerSubspaceSpanDecomposition)** holds at
the filled post-state directly by ExtendedReachableStateInvariants (ASN-0047): the
pre-state `Σ` is reachable from `Σ₀` (precondition) and INSERT is a valid composite,
so the post-state is reachable as well, and the theorem's per-state invariants —
S8★ among them — hold there. It is a post-state invariant, not a precondition of any
composite step, so it carries no INSERT-specific obligation. P1 records the narrower
fact that the inserted material forms *one* such run.

*Provenance coupling — the obligation allocation incurs.* Because INSERT both
allocates content (I-ALLOC) and places it into the content subspace of `ran(M'(d))`
(I-NEW), ASN-0047 binds it to three coupling constraints between the initial and
final states of the composite, plus a composite-boundary coverage property —
mandatory, not optional, by the composite-validity discipline established above
(ValidComposite★ clause 2). The consultation settles that this coupling is intrinsic to
insertion — the inserting document's identity is minted into the address as content
enters, and the implementation makes the binding concrete by writing a DOCISPAN
provenance record per inserted I-span (KB synthesis; theory answer "provenance
follows creation, and for native insertion creation and placement are the same
act"). I-PROV is the abstract counterpart of that record. We discharge each
constraint directly.

The range identity (RAN) drives all four: the I-addresses *new to the
content-subspace range* of `M'(d)` are precisely `A_new = {shift(a, k) : 0 ≤ k < n}`,
the shifted-suffix addresses being range-old.

- **J0 (AllocationPlacementCoupling).** Every freshly allocated I-address must appear
  in some arrangement of the post-state. The fresh addresses are `A_new`, and I-NEW
  places each `shift(a, k)` at the V-position `shift(p, k) ∈ dom(M'(d))` with
  `d ∈ E_doc`. So J0 holds.
- **J1★ (ExtensionRecordsProvenance).** Every I-address new to the content-subspace
  range of `M'(d)` must carry a record `(a, d) ∈ R'`. The range-new addresses are
  exactly `A_new` (range identity above), and I-PROV records `(shift(a, k), d)` for
  each `0 ≤ k < n`. So J1★ holds. The shifted-suffix addresses, being range-old,
  impose no new obligation — and indeed J1'★ forbids recording them.
- **J1'★ (ProvenanceRequiresExtension).** Every new provenance entry `(a, d) ∈ R' ∖ R`
  must correspond to an I-address range-new in `M'(d)`. The new entries are exactly
  `{(shift(a, k), d) : 0 ≤ k < n}` (I-PROV adds only these, and `R` is otherwise
  untouched), and each `shift(a, k) ∈ A_new` is range-new. So J1'★ holds. This is the
  reason I-PROV records *only* `A_new` and not the shifted suffix: recording a
  range-old address would manufacture an entry with no range-new witness, violating
  J1'★.

The post-state is a composite boundary, so it must also satisfy **P7a
(ProvenanceCoverage)**: every `a ∈ dom(C')` carries some record `(a, d') ∈ R'`. Split
`dom(C') = dom(C) ∪ A_new` (I-ALLOC). For prior addresses `b ∈ dom(C)`: by
precondition `Σ` is reachable, hence a composite boundary, so P7a holds at the
pre-state, giving some `(b, d') ∈ R`; and `R ⊆ R'` (I-PROV is purely additive), so `(b, d') ∈ R'`. For the new addresses
`shift(a, k) ∈ A_new`: I-PROV supplies `(shift(a, k), d) ∈ R'` directly. Hence every
content address — old and new — is covered, and P7a holds at the post-state.
Symmetrically **P7 (ProvenanceGrounding)** — every `(a, d') ∈ R'` has `a ∈ dom(C')` —
is preserved: prior entries by P2-monotonicity of the store, the new entries because
each `shift(a, k) ∈ A_new ⊆ dom(C')`. We record the coupling as a claim.

**PROV (InsertionProvenance).** *INSERT records `R' = R ∪ {(shift(a, k), d) :
0 ≤ k < n}` (I-PROV), which discharges the coupling constraints J0, J1★, J1'★ of
ASN-0047 between the composite's initial and final states, and — together with the
pre-state's coverage — establishes P7a and P7 at the post-state. Provenance is thus
established atomically-with-allocation as part of the operation, not deferred: every
freshly minted content address `shift(a, k)` enters `R` coupled to its inserting
document `d` in the same composite that allocates and places it.*

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

The I-address-permanence half is already carried by P0 (every new binding is at a
fresh address) and P2 (no existing address removed or rebound); we therefore reserve
the boxed claim for the V-position-impermanence half, which the prose above argues
but no prior claim captures.

**P3 (PositionImpermanence).** *A V-position binds no permanent content. When the
insertion point is occupied (`J ≤ N`), the block slots `{q_k : J ≤ k ≤
min(J+n−1, N)}` lie in `dom(M(d)) ∩ dom(M'(d))` yet `M'(d)(q_k) = shift(a, k−J) ≠
M(d)(q_k)` — the same slot now resolves to freshly minted content, since
`shift(a, k−J) ∈ A_new` is fresh (P0) while `M(d)(q_k) ∈ ran(M(d)) ⊆ dom(C)`. The
permanence guarantee attaches to the I-address (P0, P2), never to the slot.*

**Link anchoring across the displacement.** A link's endsets reference
I-addresses, not V-positions (4/42, 4/30). Since INSERT removes no I-address
(P2) and adds only fresh ones (P0), every link designates *exactly the same
content* after the operation as before. We can state this without modelling the
link store in detail, using only the foundation notion that a link endpoint is
an endset whose `coverage` is a set of I-addresses, and that its appearance in
document `d` is the set of V-positions of `d` mapping into that coverage. Three
facts hold — the first about the target, the next two about the resolved
witnesses:

- *The link's target is unchanged.* For any endset `e`, `coverage(e)` is a
  function of `e`'s spans alone, and INSERT never edits a stored link value. Since
  INSERT is the composite of `n` content allocations (K.α) and one arrangement
  transition — `Σ → Σ'` spans `n+1` steps — we cite the multi-step lemmas: link
  immutability **L12 (LinkImmutability, ASN-0043)** lifted across the composite
  fixes `Σ'.L(a) = Σ.L(a)` for every prior link `a`, so **LP3★
  (MultiStepCoverageInvariance, ASN-0098)** gives
  `coverage_{Σ'}(e) = coverage_{Σ}(e)` for every prior endset. Coverage-invariance
  rests on endset immutability, not on freshness. Foundation **L4 (EndsetGenerality)**
  and **L9 (TypeGhostPermission)** let an endset reference *any* tumbler, including
  ghost addresses not yet in `dom(C)`, so a pre-existing endset may already name an
  address that INSERT now mints into `A_new`.
- *The shifted-suffix witnesses move uniformly.* A link whose coverage includes
  `M(d)(v)` for some shifted `v ≥ p` is now found at `shift(v, n)`, because
  `M'(d)(shift(v, n)) = M(d)(v)` (I-SHIFT) carries the same I-address to the new
  slot. The link did not move to *different content*; the content it always named
  simply sits at a higher V-address.
- *New-block witnesses.* Precisely because a prior endset `e` may reference an
  address in `A_new` (the ghost-reference case above), INSERT can *add* witnesses
  to such a link — whether or not that link was already discoverable elsewhere.
  After the operation the new block carries `M'(d)(shift(p, k)) = shift(a, k)`; if
  `shift(a, k) ∈ coverage(e)` for some `0 ≤ k < n`, the V-position `shift(p, k)`
  newly resolves into `coverage(e)`. This new-block gain occurs for *any* link with
  `coverage(e) ∩ A_new ≠ ∅`, including a link already discoverable through other
  witnesses. Only in the special sub-case where the link is *orphaned* at `Σ` —
  discoverable from no document at all — is the gain a **resurrection in the sense
  of LP18 (ASN-0098)**: an orphaned reference becoming discoverable exactly when an
  arrangement entry to its target appears. These witnesses live at the inserted
  block, not at any `shift(v, n)`.

This is the precise sense of Nelson's survivability clause restricted to
insertion (4/43): because insertion removes nothing, *every* link survives with
its designated content unchanged. The resolved witnesses are V-positions, and the
suffix witnesses are *relabelled* by `v ↦ shift(v, n)` — so the post-insert
V-position set is *not* a superset of the prior one. What is monotone is the
*count* of witnesses and the *resolved content*: each prior witness maps
injectively to a surviving one (left verbatim, suffix shifted, cross-subspace
verbatim), and the new block can only add witnesses, never remove or redirect. We
record it.

**P4 (LinkSurvival).** *For every endset `e` existing in `Σ`,
`coverage_{Σ'}(e) = coverage_{Σ}(e)` (by L12 + LP3★ across the composite) — no link's designated content
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
  `{shift(p, k) : 0 ≤ k < n ∧ shift(a, k) ∈ coverage(e)}` (a resurrection in the
  sense of LP18 only when the link was orphaned at `Σ`).*

*The prior witness set `project(e, d, Σ)` partitions into left, suffix, and
cross-subspace witnesses, and INSERT maps these injectively into the post-insert
set: left and cross-subspace verbatim, suffix by the bijection `v ↦ shift(v, n)`
(I-SHIFT). The two sets are therefore **not** in a set-inclusion relation — the
shifted witnesses occupy new V-positions — but the map is a bijection from the
prior set onto (left ∪ shifted-suffix ∪ cross-subspace). Hence the witness
**count** is non-decreasing,*

> `|project(e, d, Σ')| = |project(e, d, Σ)| + |{shift(p, k) : 0 ≤ k < n ∧ shift(a, k) ∈ coverage(e)}|`,

*and the resolved **content** grows monotonically,*

> `coverage(e) ∩ ran(M(d)) ⊆ coverage(e) ∩ ran(M'(d))`,

*with equality in both iff the new-block part is empty, i.e. iff
`coverage(e) ∩ A_new = ∅`.*

**Isolation of documents sharing I-addresses.** Suppose another document `d'`
arranges some of the same content `d` does — `ran(M(d')) ∩ ran(M(d)) ≠ ∅`. The
question is whether inserting into `d` can perturb `d'`. It cannot, and the
proof is the conjunction of three facts already in hand. By F-DOC,
`M'(d') = M(d')` — `d'`'s arrangement is untouched. By P2, the shared
content I-addresses retain their content — the bytes `d'` reads are immutable
(and by F-LINK any link-subspace images retain their link values). And the
fresh addresses `A_new` cannot already inhabit `ran(M(d'))`: every arrangement
obeys generalized referential integrity, `ran(M(d')) ⊆ dom(C) ∪ dom(L)` (S3★),
while `A_new ∩ (dom(C) ∪ dom(L)) = ∅` by K.α's whole-store freshness
(FirstEmissionFreshness/SubsequentEmissionFreshness, ASN-0093), so
`A_new ∩ ran(M(d')) = ∅`. Therefore `d'` resolves
every one of its V-positions to the same content, in the same order, before and
after: its arrangement *and its reader's experience* are identical (Q8). The isolation is a structural consequence of the two-layer split: INSERT
writes the arrangement of exactly one document (F-DOC) and appends to the global
content store without disturbing any existing entry (P2). Sharing is by
reference to immutable identity, so an insertion into one sharer is invisible to
the others.

**P5 (DocumentIsolation).** *For every `d' ≠ d`: `M'(d') = M(d')`, and for every
`v' ∈ dom(M(d'))` the resolved entity is invariant per subspace —
`subspace(v') = s_C ⟹ M'(d')(v') ∈ dom(C')` with `C'(M'(d')(v')) = C(M(d')(v'))`
(content value fixed by P2), and `subspace(v') = s_L ⟹ M'(d')(v') ∈ dom(L')` with
`L'(M'(d')(v')) = L(M(d')(v'))` (link value fixed by F-LINK). The arrangement and
resolved content of every other document are invariant under INSERT on `d`.*

## A weakest precondition: when is discoverability preserved?

P4 leaves one question pointed but unanswered: under what condition does INSERT
preserve, rather than merely not-shrink, the set of links discoverable from `d`?
It is tempting to assume the answer is "always" — insertion removes nothing.
Computing the weakest precondition shows otherwise, and the place it fails is
exactly the new-block-witness gap P4 now records.

Write `D(d, Σ) = {a ∈ dom(Σ.L) : discoverable_from(a, d, Σ)}` for the links
discoverable from `d` (foundation `discoverable_from`, ASN-0098). We seek

> `wp(INSERT, "D(d, Σ') = D(d, Σ)")`.

By **LP12 (DiscoverabilityCharacterisation, ASN-0098)**, a link `a` is
discoverable from `d` iff some slot's coverage meets the document's I-address
range: `discoverable_from(a, d, Σ) ⟺ (E i : coverage(Σ.L(a).eᵢ) ∩ ran(M(d)) ≠
∅)`. LP12 consumes the *full* `ran(M(d))` — content and cross-subspace alike — so
the entire question reduces to how INSERT changes `ran(M(d))`. The full-range
identity is RAN above:

> `ran(M'(d)) = ran(M(d)) ∪ A_new`,

whose cross-subspace contribution is fixed by F-SUB and whose content-subspace
contribution gains exactly `A_new`. Substituting the
full-range identity RAN into
LP12, for every prior link `a` — and noting that the unsubscripted `coverage(eᵢ)`
below is well-defined because each slot's coverage is invariant pre-to-post across
the whole composite (L12 + **LP3★ (MultiStepCoverageInvariance, ASN-0098)**, so
`coverage_{Σ'}(eᵢ) = coverage_{Σ}(eᵢ)`) —

```
  discoverable_from(a, d, Σ')
    ⟺ (E i : coverage(eᵢ) ∩ (ran(M(d)) ∪ A_new) ≠ ∅)
    ⟺ discoverable_from(a, d, Σ)  ∨  (E i : coverage(eᵢ) ∩ A_new ≠ ∅).
```

Therefore `D(d, Σ') = D(d, Σ) ∪ Added`, where
`Added = {a ∈ dom(Σ.L) : (E i : coverage(Σ.L(a).eᵢ) ∩ A_new ≠ ∅)}` is the set of
links the freshly minted run would newly witness. Since `D(d, Σ')` is the *union*
of the prior set with `Added`, the two coincide iff `Added ⊆ D(d, Σ)` — **not** iff
`Added = ∅`. The distinction is exactly the configuration L4/L9 permit: a link
whose endset has one span into `A_new` (a ghost reference) *and* another span
already meeting `ran(M(d))` lies in `Added` yet was *already* discoverable, so
adding its new-block witness leaves `D(d)` unchanged. The weakest precondition is
thus the operation's precondition conjoined with a *containment*, not an
emptiness. We record it as a named claim, parallel to P0–P5:

**P6 (DiscoverabilityWP).** *The weakest precondition under which INSERT preserves
the set of links discoverable from `d` is*

> `wp(INSERT, D(d, Σ') = D(d, Σ)) ≡ INSERT-pre ∧
> {a ∈ dom(Σ.L) : (E i : coverage(Σ.L(a).eᵢ) ∩ A_new ≠ ∅)} ⊆ D(d, Σ)`.

In words: discoverability from `d` is preserved precisely when every link the new
run would newly witness was *already* discoverable from `d`. The strictly stronger
*sufficient* condition `(A a ∈ dom(Σ.L), i : coverage(Σ.L(a).eᵢ) ∩ A_new = ∅)` —
no prior endset references the allocated run at all — discharges the containment by
emptying `Added`, but it over-rejects: it refuses the ghost-plus-live-span
pre-states above, on which discoverability is in fact preserved. Two corollaries fall out. (i) A
sufficient condition discharging the wp for free is a tight-endset discipline: if
every prior endset is tight at its creation state (foundation `tight`, ASN-0098),
then **LP19a (TightFreshness)** gives `A_new ∩ coverage(e) = ∅` for every K.α-fresh
address, so `Added = ∅ ⊆ D(d, Σ)` and the wp reduces to `INSERT-pre`. (ii) Absent
that discipline, the containment wp is the sharpest statement available, and it is
the formal witness that "insertion preserves discoverability" is a *conditional*,
not a theorem.

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

**Links over the insertion (P4, P5, P6).** Equip `d` with two links to drive the
link claims against this concrete shift.

*A link that both shifts and resurrects.* Let `ℓ` carry an endset `e` with
`coverage(e) = {a_3, [d.0.s_C.8]}`. At the pre-state `a_3 = M(d)(q_3) ∈ ran(M(d))`,
while `[d.0.s_C.8]` is a *ghost* — not yet in `dom(C)` — which L4/L9 permit an
endset to name. So `project(e, d, Σ) = {q_3}`: one witness, at `q_3`. After the
insert, P4's four parts are: left `∅`; cross-subspace `∅`; shifted-suffix
`{q_5}`, since `q_3 ≥ p` carries `a_3` to `shift(q_3, 2) = q_5`; new-block
`{q_4}`, since `shift(a, 1) = [d.0.s_C.8] ∈ coverage(e)` puts a witness at
`shift(p, 1) = q_4`. Hence `project(e, d, Σ') = {q_4, q_5}`. The prior witness set
`{q_3}` is **not** a subset of `{q_4, q_5}` — the witness was *relabelled*
(`q_3 → q_5`), not retained — confirming P4's bijection-not-inclusion form. The
count rose by exactly the one new-block witness (`1 → 2`), and the resolved content
grew monotonically: `coverage(e) ∩ ran(M(d)) = {a_3} ⊆ {a_3, [d.0.s_C.8]} =
coverage(e) ∩ ran(M'(d))`. ✓ P4.

*The P6 trap.* Was discoverability of `ℓ` from `d` *newly* gained? No — `ℓ` was
*already* discoverable via `a_3` (`coverage(e) ∩ ran(M(d)) = {a_3} ≠ ∅`), so
`ℓ ∈ D(d, Σ)`. Yet `ℓ ∈ Added`, since `coverage(e) ∩ A_new = {[d.0.s_C.8]} ≠ ∅`.
This is precisely the pre-state the *sufficient* emptiness form would reject and
the *weakest* containment form accepts: `ℓ ∈ Added ⊆ D(d, Σ)` leaves `D(d)`
unchanged. ✓ P6 (containment, not emptiness).

*A genuine resurrection.* Let `ℓ'` carry `coverage(e') = {[d.0.s_C.7]}`, a single
ghost address, orphaned at `Σ` (`coverage(e') ∩ ran(M(d)) = ∅`, and discoverable
from no document). After the insert the new block carries
`M'(d)(q_3) = [d.0.s_C.7] ∈ coverage(e')`, so `q_3 ∈ project(e', d, Σ')`: `ℓ'`
becomes discoverable from `d`. Here `ℓ' ∈ Added ∖ D(d, Σ)`, so `D(d, Σ') ⊋
D(d, Σ)` — a real change to the discoverable set, and a **resurrection in LP18's
sense** because `ℓ'` was orphaned. ✓ P4 new-block, P6 escape branch.

*Isolation (P5).* Suppose `d'` also arranges `a_3`: `M(d')(q'_1) = a_3`. INSERT on
`d` leaves `M'(d') = M(d')` (F-DOC), and `a_3 ∈ dom(C)` retains its value (P2),
while `A_new ∩ ran(M(d')) = ∅` because `ran(M(d')) ⊆ dom(C) ∪ dom(L)` (S3★) and
`A_new ∩ (dom(C) ∪ dom(L)) = ∅` (K.α whole-store freshness). So `d'` resolves
`q'_1` to `a_3`'s content exactly as
before — untouched by the insertion into `d`. ✓ P5.

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

Two effects, two layers, kept clean: on the content layer INSERT is the `n`-fold
allocation K.α with its coupled provenance K.ρ, and on the arrangement layer the
contraction–extension pair `K.μ⁻` then `K.μ⁺` realising ASN-0082's shift. The claims
established are catalogued below.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| INSERT | Operation: place `n` fresh content units at valid V-position `p` in document `d`, as the valid ASN-0047 composite `K.α`(×n) → `K.μ⁻` → `K.μ⁺` → `K.ρ`(×n) (K.μ⁻ dropped in the append/empty cases), whose arrangement net effect realises ASN-0082's I3 shift | introduced (composite) |
| P0 (OriginIdentity) | The `n` allocated I-addresses `{shift(a,k) : 0 ≤ k < n}` are fresh and distinct from all prior addresses, independent of content value | restated (K.α freshness + S4, ASN-0036/0093) |
| P1 (InsertedRun) | The inserted material forms one correspondence run: `M'(d)(shift(p,k)) = shift(a,k)`, V- and I-addresses advancing in lockstep over a contiguous block | introduced |
| P2 (ContentAppendOnly) | `dom(C) ⊆ dom(C')` and existing values preserved; INSERT is purely additive on content | restated (C0, ASN-0093) |
| P3 (PositionImpermanence) | A V-position binds no permanent content: an occupied block slot `q_k` (J ≤ k ≤ min(J+n−1, N)) satisfies `M'(d)(q_k) = shift(a,k−J) ≠ M(d)(q_k)`, resolving to fresh content; permanence attaches to the I-address (P0, P2), not the slot | introduced |
| P4 (LinkSurvival) | Every prior endset's coverage is unchanged (L12+LP3★ across the composite); post-insert witness set = left ∪ shifted-suffix ∪ cross-subspace ∪ new-block; prior witnesses map bijectively onto the first three parts (suffix relabelled by `shift(·,n)`), so witness count is non-decreasing and resolved content grows monotonically (new-block is LP18 resurrection only when the link was orphaned) | introduced |
| P6 (DiscoverabilityWP) | `wp(INSERT, D(d,Σ')=D(d,Σ)) ≡ INSERT-pre ∧ {a : (∃i) coverage(Σ.L(a).eᵢ) ∩ A_new ≠ ∅} ⊆ D(d,Σ)` (containment, not emptiness); the emptiness form is sufficient but strictly stronger; discharged free under tight-endset discipline (LP19a) | introduced |
| P5 (DocumentIsolation) | Every other document's arrangement and resolved content are invariant under INSERT on `d` | introduced |
| PROV (InsertionProvenance) | `R' = R ∪ {(shift(a,k), d) : 0 ≤ k < n}` discharges ASN-0047's J0, J1★, J1'★ across the composite and re-establishes P7a/P7 at the post-state; provenance is recorded atomically with allocation | introduced |
| I-ALLOC | `dom(C') = dom(C) ∪ A_new`, `C'(shift(a,k)) = w_k` | cited (K.α, ASN-0093), iterated |
| I-IMM | `(A b : b ∈ dom(C) : C'(b) = C(b))` — existing content values unchanged | cited (C0, ASN-0093) |
| I-PROV | `R' = R ∪ {(shift(a,k), d) : 0 ≤ k < n}` — provenance record per allocated address | cited (K.ρ, ASN-0047), iterated |
| I-SHIFT | V-positions `≥ p` in subspace `S` move to `shift(v,n)`, carrying their I-address | cited (I3, ASN-0082) |
| I-LEFT | V-positions `< p` in subspace `S` are unchanged | cited (I3-L, ASN-0082) |
| I-NEW | The vacated block `{shift(p,k)}` maps to the fresh run `{shift(a,k)}` | introduced (composition glue) |
| I-DOM | `V_S(d')` is the dense run `{q_1, …, q_{N+n}}`; D-SEQ/D-MIN/D-CTG of the filled post-state established here with `N' = N+n` | introduced (interval argument; prefix+suffix from I3-CS, ASN-0082; middle block from I-NEW) |
| F-SUB | Positions in subspaces `S' ≠ S` are unchanged (subspace confinement of the shift) | cited (I3-X, ASN-0082) |
| F-DOC | Arrangements of all documents `d' ≠ d` are unchanged | cited (I3-D, ASN-0082) |
| F-LINK | `Σ'.L = Σ.L` — the link store is untouched | cited (frame; no K-atomic touches `Σ.L`) |
| F-ENT | `Σ'.E = Σ.E` — the entity set is untouched | cited (frame; INSERT registers no entity) |

## Open Questions

What must INSERT guarantee when the insertion point names a position that is currently shared, by transclusion, with another document's arrangement?

Under what conditions, if any, may two concurrent insertions into the same document's content scope both claim freshness without a serializing authority?

What must provenance guarantee when content is placed into a document not by fresh allocation but by transclusion of an address whose provenance already names a different origin document?

What relationship must hold between the inserted run's contiguity at creation and the system's obligations after later editing fragments that run?
