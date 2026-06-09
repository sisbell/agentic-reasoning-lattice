# ASN-0117: DELETE Operation

*2026-06-08*

## The problem

We are asked what happens when content over a span of a document is deleted.
The word *delete* arrives loaded with a meaning we must immediately discard.
In almost every system one has ever used, to delete is to destroy — to
overwrite, to free, to make the bytes cease to be. Nelson's design inverts
this completely. His annotation for the deleted state reads: "DELETED BYTES
(not currently addressable, awaiting historical backtrack functions, may
remain included in other versions.)" (4/9). Three clauses, and every one of
them asserts that the bytes are *still there*. Deletion in Xanadu removes
content from a document's *arrangement* while the content itself survives,
permanent and untouched, in the store.

The operation Nelson names is terse: "DELETEVSPAN: This removes the given span
from the given document" (4/66). The whole subtlety hides in the word
*removes*. What is removed is not the content but the document's current
*placement* of it — the mapping that said "here, at this position in my
sequence, sits that content." Gregory's evidence makes the layering exact: the
delete path operates entirely on the document's arrangement enfilade and
"leaves the granfilade entirely untouched, such that the I-addresses
underlying the deleted span remain resolvable to their original bytes even
though no POOM currently references them" (Q15). One layer changes; the other
does not — and this time the discipline is even sharper than for insertion,
because deletion writes *nothing* to the permanent store at all.

We work in the address space `T` of tumblers under the lexicographic total
order T1, with the displacement algebra `⊕`, `⊖`, and the ordinal shift
`shift(v, n) = v ⊕ δ(n, #v)` that moves a tumbler's final component while
fixing its prefix (foundation: OrdinalShift, OrdinalDisplacement, ASN-0034).
We take the two-layer state as given: a **content store** `Σ.C : T ⇀ Val`, the
append-only ground truth of what content exists (Nelson's Istream, the
permascroll), and a per-document **arrangement** `Σ.M(d) : T ⇀ T`, the partial
function from V-positions to I-addresses recording how document `d` currently
arranges that content (Nelson's Vstream). A V-position carries a subspace
identifier in its first component, `subspace(v) = v₁`; content lives in the
text subspace `s_C`, links in `s_L`. We write
`V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}`.

The standing well-formedness facts, inherited from the arrangement model:
every active V-position is zero-free of depth `m ≥ 2` with all components
positive (S8a, ASN-0036); within one subspace of one document the positions
share a common depth (S8-depth); the text subspace is *dense* —
`V_S(d) = {[S, 1, …, 1, k] : 1 ≤ k ≤ N}` for some `N ≥ 0` (D-SEQ), a
contiguous, gap-free run of ordinals from the canonical first position. We
abbreviate the `k`-th slot of this run `q_k = [S, 1, …, 1, k]` of depth `m`,
and carry the depth-2 text case `m = 2` of the foundation displacement work,
so `q_k = [S, k]` and `ord(q_k) = [k]`. The single arithmetic fact that does
all the work below:

> `σ(q_k) = q_{k−c}` for `k ≥ J + c` — *left*-shifting the last component by
> the deletion width `c` carries the `k`-th slot to the `(k−c)`-th, leaving the
> shared prefix `[S, 1, …, 1]` untouched. This is the ordinal subtraction
> `ord(q_k) ⊖ w_ord` of the foundation contraction (ASN-0082), well-defined and
> order-preserving on the surviving suffix.

## What is removed, and what must survive

The consultation is unanimous and emphatic on the central point. When content
over a span is deleted, the operation "removes that content from the document's
**Vstream** (its current arrangement) while the content itself survives
permanently in the **Istream**" (Q1). The bytes "remain in all other documents
where they have been included" (4/11); previous versions still contain them;
links still resolve to them; historical backtrack can reconstruct any prior
arrangement (Q1, Q8). The deletion changes only where — and whether — the
*deleting document* presently places the content. It changes nothing about
whether the content *exists*.

Our state model makes this a statement of one line. The deleted material
occupies a span of V-positions `{q_J, …, q_{J+c−1}}` in `d`, mapping to the
I-addresses

> `A_del = {M(d)(q_k) : J ≤ k < J + c}`.

What "removal" does is delete those `c` mappings from `M(d)` — and *only* that.
The content store is a strict frame condition of the operation: the granfilade
is never consulted, never written, never freed (Q15). This is exactly the
foundation contraction's **ContentStoreFrame**, which fixes `Σ'.C = Σ.C` —
both domain and per-address value (ASN-0082 **D-I**). Every I-address in
`A_del` is still in `dom(C')` with its value intact; the bytes are, in
Nelson's phrase, "not currently addressable" *from `d`'s present view*, never
"not existing." We record the core guarantee, the one any implementation of
non-destructive editing must satisfy.

**P0 (NonDestruction).** *DELETE does not touch the content store:
`dom(C') = dom(C)` and `(A b : b ∈ dom(C) : C'(b) = C(b))`. In particular every
deleted I-address survives: `A_del ⊆ dom(C')` with content preserved.*

Why must this hold for *any* implementation? Because everything Nelson builds
on top of editing — historical backtrack, transclusion across documents,
links that survive editing, version comparison — presumes the bytes endure.
"Virtually all of computerdom is built around the destructive replacement of
successive whole copies… Instead, suppose we create an append-only storage
system" (2/14). Append-only is not a performance choice; it is the foundation
of every downstream guarantee. An implementation that freed the deleted bytes
would satisfy the immediate semantics of "the span is gone from this document"
while silently breaking transclusion, backtrack, and link survival all at once.
Gregory confirms the architecture enforces this structurally: the codebase
maintains *two distinct deletion primitives*, and the document-span delete
calls only the one that operates on the arrangement enfilade, never the one
that would touch the permanent store (Q15). The non-destruction guarantee is a
frame condition, not a courtesy.

## What shifts, and what the shift must preserve

Now the arrangement effect. The deleted span is removed and the surrounding
content must re-close into a single gap-free sequence. Nelson states the rule
for insertion verbatim — "the v-stream addresses of any following characters…
are increased by the length of the inserted text" (4/66) — and deletion is its
exact symmetric inverse: the V-addresses of characters following the deleted
span are *decreased* by the span's length, so the survivors "close the gap"
and the document "stays in canonical order" (Q2, Q9). The governing constraint
is the enfilade requirement that "all changes, once made, left the file
remaining in canonical order" (1/34): the Vstream is dense, with no holes.

Let `S = subspace(p) = s_C`, `p = q_J` the first deleted position, `w` the
deletion width with `w₁ = 0`, `#w = #p = 2`, `Pos(w)`, and write `c = ord(w)`
for the count of deleted slots, so the deleted block is `{q_J, …, q_{J+c−1}}`
and `r = p ⊕ w = q_{J+c}` is the first surviving position past the gap. By the
foundation SubspaceConventionAxiom (ASN-0047/ASN-0093) the text subspace
identifier is `s_C = 1`, so `V_S(d) = V_1(d)` and ASN-0082's contraction —
stated literally for `S = 1` on `V_1(d)` — applies here verbatim, licensing every
D-clause we cite below at `S = s_C`. The three regions of the foundation
contraction (ASN-0082 **ThreeRegions**) partition `V_S(d)` by trichotomy of T1:

- `L = {v ∈ V_S(d) : v < p}` — the prefix, untouched;
- `X = {v ∈ V_S(d) : p ≤ v < r}` — the deleted block, `|X| = c`;
- `R = {v ∈ V_S(d) : v ≥ r}` — the suffix, shifted left.

The displacement is then completely determined, and we do not re-derive it: it
is the foundation contraction of ASN-0082. Reading off its clauses:

- **Suffix shifts uniformly left.** For `v = q_k ∈ R` (i.e. `k ≥ J + c`), the
  position moves to `σ(v) = vpos(S, ord(v) ⊖ w_ord) = q_{k−c}`, and *it carries
  its content with it*: `M'(d)(σ(v)) = M(d)(v)` (ASN-0082 **D-SHIFT**). The shift
  is by the same constant `c` for every following position, so the relative
  order of the survivors is preserved exactly (ASN-0082 **D-BJ**: `σ` is an
  order-preserving injection).
- **Prefix is untouched.** For `v ∈ L`: `M'(d)(v) = M(d)(v)` (ASN-0082 **D-L**).
  No position before the cut moves.
- **The gap closes exactly.** The first surviving suffix position lands precisely
  where the deletion began: `ord(r) ⊖ w_ord = ord(p)`, so `σ(q_{J+c}) = q_J`
  (ASN-0082 **D-SEP**). There is no gap and no overlap between `L` and the shifted
  suffix (ASN-0082 **D-DP**, dense partition).

Here is the answer to *what relationship the remaining content bears to its
prior V-positions*. The consultation draws the distinction with care (Q2, Q9):
a V-position never *binds* content; it is an ordinal slot, not a container.
After the deletion, the relation "position `q_k` holds content `X`" has been
rewritten — `X`, if it survived in `R`, now sits at `q_{k−c}`. What is preserved
is the orthogonal relation: *each surviving piece of content keeps its
I-address, and the arrangement re-coordinates itself around that fixed
identity.* The left-shift is a relabelling of slots, not a transport of
bindings. The exact-gap-closure happens *only in the Vstream*; the permanent
I-addresses of the survivors do not change at all. The deletion's boundaries are
reflected precisely in the virtual renumbering and not at all in the content
identity.

The displacement is confined to the subspace `S`. Gregory's evidence makes this
structural: a text deletion at `1.x` cannot reach link positions at `2.x`,
because the displacement acts on the deepest ordinal component and a
cross-subspace shift would require subtracting a finer-grained width from a
coarser address — which the arithmetic refuses (Q18). Abstractly this is forced
by the subspace identifier sitting in the V-position's first component
(foundation: T7, ASN-0034): an ordinal shift advances the last component and
cannot cross into another subspace's region. Hence the cross-subspace and
cross-document frames hold (ASN-0082 **D-CS**, **D-CD**).

We collect the arrangement effect as a named operation.

**DELETE(`d`, `p`, `w`).**

*Precondition.* `d ∈ dom(M)`; `S = subspace(p) = s_C`; `m = #p = 2`, equal to
the common depth S8-depth fixes on `V_S(d)`; `p ∈ V_S(d)` is S8a-well-formed;
`w₁ = 0`, `#w = #p`, `Pos(w)`, with `c = ord(w) ≥ 1`; and *containment* — the
deleted span lies within the arranged run: `p = q_J` and `r = p ⊕ w = q_{J+c}`
with `1 ≤ J` and `J + c ≤ N + 1` (the case `J + c = N + 1` deletes a suffix,
leaving `R = ∅`). This is exactly the foundation contraction's precondition
(ASN-0082).

*Effect.* DELETE is one arrangement contraction realising ASN-0082's
displacement family, with the content store held in frame. Which ASN-0047
realisation it is splits on whether any suffix survives the cut — on whether
`R = ∅`: when a non-empty suffix survives (`R ≠ ∅`), DELETE is the K.μ⁻ + K.μ⁺
composite; when the deletion reaches the end of the run (`R = ∅`), no survivor
shifts and DELETE is a lone K.μ⁻. The foundation transition
**K.μ⁻ (ArrangementContraction)** is a *prefix-retention truncation*: it keeps a
contiguous prefix of each subspace run *at the survivors' original V-positions* —
its postcondition fixes `M'(d)(v) = M(d)(v)` on the retained domain
`R := ∪_S {[S, 1, …, 1, k] : 1 ≤ k ≤ n'_S}`. We take the two cases in turn.

*Case `R ≠ ∅` (`J + c ≤ N`): the K.μ⁻ + K.μ⁺ composite.* When survivors remain
past the gap, DELETE is the foundation *composite* of two atomic transitions of the
extended-state model `Σ = (C, L, E, M, R)` (ASN-0047), in the same sense that K.μ~
(ArrangementReordering) is itself a named K.μ⁻ + K.μ⁺ composite:

1. a **K.μ⁻** step that contracts the text subspace to its surviving prefix
   `L = {q_1, …, q_{J−1}}` (retention count `n'_{s_C} = J − 1`), while holding
   the link subspace at full retention (`n'_{s_L} = n_{s_L}`); the text count
   `J − 1 < N` supplies K.μ⁻'s required strictly-contracting subspace;
2. a **K.μ⁺** step that re-places the `N − c − (J − 1)` survivors at the
   closed-up text positions `{q_J, …, q_{N−c}}`, each carrying the I-address it
   held before — the former images of `q_{J+c}, …, q_N` (each in `dom(C)`, so
   K.μ⁺'s `a ∈ dom(C)` placement precondition is met) — yielding the dense run
   `{q_1, …, q_{N−c}}` that discharges K.μ⁺'s D-CTG/D-MIN obligations. Because
   `R ≠ ∅`, at least one survivor is re-placed (`N − c − (J − 1) ≥ 1`), so this
   K.μ⁺ adds at least one mapping and meets K.μ⁺'s strict-extension precondition
   (`dom(M'(d)) ⊃ dom(M(d))`, ASN-0047).

*Case `R = ∅` (`J + c = N + 1`): K.μ⁻ alone.* When the deletion reaches the end of
the run there is no suffix to shift: the survivors are exactly the prefix
`L = {q_1, …, q_{J−1}}` *at their original V-positions*, and since `J + c = N + 1`
gives `J − 1 = N − c`, that prefix is already the closed-up dense run
`{q_1, …, q_{N−c}}`. No re-placement is needed, and a K.μ⁺ step would have
`N − c − (J − 1) = 0` survivors to add — an *empty* extension, which K.μ⁺'s
strict-extension precondition (`dom(M'(d)) ⊃ dom(M(d))`) forbids, so the two-step
composite has no realisation here. DELETE is instead a *single* **K.μ⁻** step: a
prefix-retention truncation of the text subspace to count `n'_{s_C} = J − 1 = N − c`
(with `n'_{s_C} < N` since `c ≥ 1`, supplying the strictly-contracting subspace),
the link subspace held at full retention. The delete-everything sub-case
`J = 1, c = N` is this with `n'_{s_C} = 0`. As an *elementary* transition K.μ⁻ is
self-sufficient — it requires no coupling and carries
`C' = C ∧ L' = L ∧ E' = E ∧ R' = R` directly (J2, ContractionIsolation, ASN-0047)
— so every coupling and frame obligation below holds for this single-step
realisation outright, without recourse to a second step.

In both cases the net effect on `M(d)` is exactly ASN-0082's left-shift
displacement (vacuous on the suffix when `R = ∅`), which is why we read DELETE's
clauses off ASN-0082 below; the K.μ⁻ + K.μ⁺ decomposition (or the lone K.μ⁻ when
`R = ∅`) is what places DELETE inside ASN-0047's *valid-composite* vocabulary,
licensing our appeal to the properties proven over that fuller model — the
per-subspace well-formedness package, the referential-integrity invariant S3★, and
the link/discoverability lemmas of ASN-0098, all quantified over reachable states
and valid transitions of `Σ`.

DELETE's coupling and frame obligations are discharged identically in both
realisations. For the `R = ∅` single step, J2 (ContractionIsolation) already
supplies `C' = C ∧ L' = L ∧ E' = E ∧ R' = R` outright, so every obligation below
holds trivially and the elementary K.μ⁻ carries no composite-coupling clause at
all. For the `R ≠ ∅` composite we discharge ValidComposite clause 2 (J0, J1★, J1'★
evaluated *only* between the initial state `Σ` and the final state `Σ'`)
explicitly, all vacuously. **J0** (every freshly allocated I-address appears in some
arrangement) holds because DELETE allocates no content — `dom(C') = dom(C)` (P0)
— so its antecedent `dom(C') ∖ dom(C)` is empty. **J1★** (every I-address *new to*
`d`'s content-subspace range must be recorded in `R`) holds because DELETE
introduces *no* range-new content: every survivor's I-address that the K.μ⁺ step
re-places was already in the content-subspace range of `M(d)` at its old position
in the initial state, so it fails J1★'s "new to the range" trigger — the conjunct
`¬(E v ∈ dom(M(d)) : subspace(v) = s_C ∧ M(d)(v) = a)` is false for each — and the
deleted addresses are simply absent from the final range. **J1'★** (every new
provenance entry requires range-new content) holds because DELETE adds no
provenance, so its antecedent `R' ∖ R` is empty. Both component steps fix the
entity set and the provenance relation (`E' = E`, `R' = R`: K.μ⁻'s frame and
K.μ⁺'s frame each list both — clauses DEL-FENT, DEL-FPROV below), so the
composite does too, and the two provenance invariants that coexist with S3★ are
preserved across DELETE: P4★ (`Contains_C(Σ') ⊆ R'`) holds because `Contains_C`
can only *shrink* under the net contraction while `R' = R` is unchanged, and P7a
(every content address carries a provenance record) holds because
`dom(C') = dom(C)` (P0) and `R' = R` leave every existing `(a, d)` record in
place. We name DELETE's clauses but derive them by citation:

- (DEL-REMOVE) The arrangement loses exactly `c` V→I correspondences in subspace
  `S`: the surviving domain contracts by precisely the deletion width,
  `|{v ∈ dom(M'(d)) : subspace(v) = S}| = N − c`, and the top `c` position
  *labels* leave the domain, `(A k : N − c < k ≤ N : q_k ∉ dom(M'(d)))`. We state
  the contraction as a count, plus the vacating of the top `c` labels, rather than
  as the absence of each specific old pair — because a deleted-span label `q_k`
  with `k ≤ N − c` does *not* vacate the domain: it remains in `dom(M'(d))` but is
  reoccupied by the shifted survivor (DEL-SHIFT), binding `M'(d)(q_k) = M(d)(q_{k+c})`.
  In the generic (no-sharing) case this is a *different* I-address than `M(d)(q_k)`,
  so the old pair `(q_k, M(d)(q_k))` is absent; but under within-document sharing
  (S5/M13 of the arrangement model), where `d` already arranges one address at two
  positions, the reoccupant `M(d)(q_{k+c})` may coincide with the old image
  `M(d)(q_k)`, and then the per-pair absence `(q_k, M(d)(q_k)) ∉ M'(d)` *fails* even
  though the count contraction still holds. This is why the robust statement of
  removal is the count `N − c` together with the top-`c` label vacancy, not a
  universal over deleted pairs. The deleted I-addresses `A_del` are *not* removed
  from anything else; they persist in `C` (P0) and may be mapped by other positions
  of `d` or by other documents.
- (DEL-SHIFT) `(A v : v ∈ R : σ(v) ∈ dom(M'(d)) ∧ M'(d)(σ(v)) = M(d)(v))` —
  verbatim ASN-0082 **D-SHIFT**, with `σ(q_k) = q_{k−c}`.
- (DEL-LEFT) `(A v : v ∈ L : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))` —
  ASN-0082 **D-L**.
- (DEL-DOM) `{v ∈ dom(M'(d)) : subspace(v) = S} = L ∪ {σ(v) : v ∈ R}` —
  ASN-0082 **D-DOM**.
- (DEL-CIMM) `Σ'.C = Σ.C` — ASN-0082 **D-I**, the content-store frame (P0).

*Frame.*
- (DEL-LIMM) `Σ'.L = Σ.L` — the link store is held entirely fixed, in both
  domain and per-address value: `dom(Σ'.L) = dom(Σ.L)` and
  `(A a : a ∈ dom(Σ.L) : Σ'.L(a) = Σ.L(a))`. DELETE allocates no link and edits
  none. This is *stronger* than L12 (LinkImmutability, ASN-0043), which fixes
  only the values of links already present and would still permit
  `dom(Σ'.L) ⊋ dom(Σ.L)`; DELETE's contract forbids any growth of `dom(L)`. The
  arrangement state ASN-0082 governs carries no link store, so this frame is
  imposed here directly, not inherited.
- (DEL-FSUB) `(A S' : S' ≠ S : {v ∈ dom(M'(d)) : subspace(v) = S'} =
  {v ∈ dom(M(d)) : subspace(v) = S'}` and `M'(d)` agrees there`)` —
  ASN-0082 **D-CS**. In particular the document's *links* (subspace `s_L`) are
  not moved by a text deletion.
- (DEL-FDOC) `(A d' : d' ≠ d : M'(d') = M(d'))` — ASN-0082 **D-CD**.
- (DEL-FENT) `Σ'.E = Σ.E` — the entity set is held fixed, by the composite-frame
  argument given in the Effect section above. P1 (EntityPermanence) and P8
  (EntityHierarchy) survive DELETE trivially.
- (DEL-FPROV) `Σ'.R = Σ.R` — the provenance relation is held fixed, by the
  composite-frame argument given in the Effect section above. Together with
  `dom(C') = dom(C)` (P0) this preserves P4★ and P7a.

DELETE allocates nothing and frees nothing: the content layer sees *no change
whatsoever* (DEL-CIMM). All of DELETE's work is in the arrangement layer, where
it shifts the surviving suffix left to close the gap.

## The document remains one coherent sequence

We must check that the result is well-formed — that closing the gap has not
left a hole, overlaid two positions, or broken the density that lets spans
name contiguous regions. We do not re-derive the post-contraction domain: it is
exactly ASN-0082's dense run **D-SEQ-post**,

> `V_S(d') = {q_1, …, q_{N−c}}`,

of length `N' = N − c`. The prefix `L = {q_1, …, q_{J−1}}` abuts the shifted
suffix `{q_J, …, q_{N−c}}` (the images of `q_{J+c}, …, q_N` under
`σ(q_k) = q_{k−c}`) flush — the gap-closure `σ(q_{J+c}) = q_J` (D-SEP) seats the
two with no hole and no overlap. We do not re-prove
well-formedness either: it is exactly ASN-0082's post-contraction preservation family —
**D-SEQ-post**/**D-MIN-post** (`min(V_S(d')) = q_1`)/**D-CTG-post** for the dense
run, **S8a-post** and **S8-depth-post** for the positions, **S2-post** for
single-valuedness, **S8-fin-post** for finiteness, and **S3-post** for
referential integrity — read at the two-subspace level as S3★
(GeneralizedReferentialIntegrity, ASN-0047): the *text* V-positions resolve into
`dom(C')` and the *link* V-positions into `dom(L')`. The content clause
`ran(M'(d)\!\restriction\!V_{s_C}(d)) ⊆ dom(C')` holds because every surviving
text image already appeared in `ran(M(d)\!\restriction\!V_{s_C}(d)) ⊆ dom(C)`
(DEL-LEFT and DEL-SHIFT preserve each survivor's I-address) and `C' = C`
(DEL-CIMM); the link clause `ran(M'(d)\!\restriction\!V_{s_L}(d)) ⊆ dom(L')`
holds because DEL-FSUB carries the link-subspace positions through verbatim and
DEL-LIMM holds the link store fixed. Stating the whole range as
`ran(M'(d)) ⊆ dom(C')` would be false for any document containing a link, since
its preserved link positions map into `dom(L)`, which by store disjointness (SD,
ASN-0093) is disjoint from `dom(C)`. This is the answer to *how the survivors
sit within the V-stream after the cut*: reading end to end yields the original
content with exactly the deleted span omitted, the stream around it re-closed
into a single coherent ordinal sequence (Q2).

One subtlety the evidence insists on. The cut at the span's boundaries is
*clean*: because the deletion endpoints `p` and `r` fall on existing position
boundaries, the surviving blocks are split at exact boundaries and no
zero-width or degenerate position is ever produced (Q11, Q12). A boundary that
fell strictly interior to a single addressed unit would require splitting it,
but at the abstract level of whole-unit V-positions the deletion either contains
a position or does not — there is no half-contained slot. Every surviving
position is a full, S8a-well-formed ordinal, and `V_S(d')` is the dense run
above with no fragments. We record the survivor-structure fact.

**P2 (GapClosure).** *The surviving content closes into the dense run
`V_S(d') = {q_1, …, q_{N−c}}` of length `N − c`. The prefix `L` is fixed; the
suffix `R` shifts left uniformly by `c` via the order-preserving injection `σ`,
carrying each survivor's I-address unchanged (`M'(d)(σ(v)) = M(d)(v)`). The
underlying arithmetic identity `ord(r) ⊖ w_ord = ord(p)` holds unconditionally
(ASN-0082 D-SEP(a)); when `R ≠ ∅` it reads positionally as the gap closing
exactly — `σ(q_{J+c}) = q_J`, the first survivor landing where the deletion began
(ASN-0082 D-SEP(b)). In the suffix-delete case `J + c = N + 1`, `R = ∅` and
`q_{J+c} = q_{N+1}` is not an arranged position: there is no gap to close, and the
positional reading is vacuous. Relative order and density are preserved; no hole,
no overlap, no degenerate position.*

And the dual fact, the arrangement-side removal:

**P1 (ArrangementContraction).** *The arrangement loses exactly `c` V→I
correspondences in subspace `S`, removed from the arrangement only:
`|{v ∈ dom(M'(d)) : subspace(v) = S}| = N − c`, with the top `c` position labels
leaving the domain, `(A k : N − c < k ≤ N : q_k ∉ dom(M'(d)))`; and every deleted
I-address persists in `C` (P0). The count-plus-label-vacancy form, rather than a
per-pair absence, is required for the reason given at DEL-REMOVE above. The
deletion subtracts `c` V→I correspondences; it subtracts no content.*

## A span, not a position: binding versus being

The question asks what deleting a *span* — rather than a single position —
reveals. The answer is the sharpest articulation of the two-layer architecture
the operations afford, and it deserves its own argument.

A single V-position is a boundary: an ordinal slot in the arrangement. By
itself it designates no content — it is a place *between* or *at*, the index of
a correspondence, not a container of bytes. A span, by contrast, has *extent*:
it covers a contiguous run of V-positions, and each of those maps to a
permanent I-address whose bytes exist independently of where — or whether — any
document arranges them. The span is therefore the smallest unit that carries
*both* aspects at once: an *arrangement* feature (its V-extent, a from-here-to-
there in the Vstream) and an *existence* fact (the I-addressed bytes it covers).
"There is no choice as to what lies between; this is implicit in the choice of
first and last point" (4/25, Q4). Deleting the span is the operation that pulls
the two aspects apart.

In our model the separation is two disjoint facts. DEL-REMOVE strips the span's
V→I correspondences from `M'(d)` — the *arrangement* ceases to bind that content.
DEL-CIMM leaves `A_del ⊆ dom(C')` with values intact — the *content* does not
cease to exist. Nelson's three-clause annotation (4/9) is precisely these two
facts plus their consequence: "not currently addressable" is DEL-REMOVE (the
loss is to *this arrangement's* reach); "may remain included in other versions"
is the cross-document survival we prove next (P5); "awaiting historical
backtrack" is the reconstructibility that P0 makes possible. A position-deletion
would reveal none of this, because a position binds no content — there would be
nothing underneath it that could "still exist." Only a span, with extent, exposes
the seam between *binding* and *being*.

What witnesses that the seam is real — that arrangement-ceasing-to-bind is a
genuinely different act from content-ceasing-to-exist? The links, and the other
documents that share the content. A link survives because it anchors on the
still-existing bytes (established formally at P4 below); the other documents that
still arrange the content continue to resolve it (P5) — both impossible if the
bytes were gone. Each is direct evidence that DELETE removed a binding and left
the existence intact. The span is the seam between binding and being; deleting it
is what shows the seam was there all along.

## Invariants the operation must preserve

We discharge the invariants the question names. Each is a statement about
keeping the content layer and the arrangement layer from contaminating each
other — and, this time, the content layer is touched not at all, which makes
three of the four nearly immediate.

**Content permanence.** This is P0, and it is the whole non-destruction
guarantee. The store is unchanged in domain and value (DEL-CIMM). No I-address
is removed; none is rebound; the deleted bytes remain at their permanent
addresses forever. We name the address-level half separately because the
question lists it as a distinct obligation.

**P3 (AddressPermanence).** *No I-address in `dom(C)` is removed or rebound by
DELETE: `(A b : b ∈ dom(C) : b ∈ dom(C') ∧ C'(b) = C(b))`. DELETE allocates no
new address and frees no existing one — the content layer is invariant.*

A remark on well-definedness, in Dijkstra's spirit of establishing that an
argument is in a function's domain before using it. The left-shift
`ord(v) ⊖ w_ord` is defined and yields a *positive* ordinal only when the
surviving positions genuinely lie past the deleted width — which the
containment precondition (`p = q_J`, `r = q_{J+c}`, `J ≥ 1`) guarantees, via
the foundation lemma **OrdinalExceedsDisplacement** (ASN-0082): for every
`v ∈ R`, `ord(v) ⊖ w_ord` is well-defined, positive, and equal to `ord(p)` at
`v = r`.

**Cross-document arrangement isolation.** Suppose another document `d'` arranges
some of the same content `d` does — `ran(M(d')) ∩ A_del ≠ ∅`, the transclusion
case. Can deleting from `d` perturb `d'`? It cannot, and the proof is the
conjunction of two facts already in hand. By DEL-FDOC, `M'(d') = M(d')` — `d'`'s
arrangement is a separate object, named and modified by nothing in DELETE's
effect. By P0/P3, the shared I-addresses retain their content — the bytes `d'`
reads are immutable. Therefore `d'` resolves every one of its V-positions to the
same content, in the same order, before and after: "the owner of a document may
delete bytes from the owner's current version, but those bytes remain in all
other documents where they have been included" (4/11, Q3, Q5, Q10). This is the
F0 cross-document frame the evidence confirms structurally — DELETE resolves
exactly one document's arrangement and reaches no other (Q17). Sharing is by
reference to immutable identity, so a deletion in one sharer is invisible to the
rest.

**P5 (DocumentIsolation).** *For every `d' ≠ d`: `M'(d') = M(d')`, and for every
`v' ∈ dom(M(d'))`, `M'(d')(v') ∈ dom(C')` with `C'(M'(d')(v')) = C(M(d')(v'))`.
The arrangement and resolved content of every other document — including any
that transcludes the deleted I-addresses — are invariant under DELETE on `d`.*

**Link survival, and discoverability across documents.** A link's endsets
reference I-addresses, not V-positions (4/42, 4/30). DELETE removes no I-address
(P3) and adds, removes, or edits no link, so the link store is held entirely
fixed — `Σ'.L = Σ.L` in both domain and value (DEL-LIMM, strictly stronger than
L12's value-only guarantee) — and every endset's *coverage* is unchanged across
the (possibly two-step) transition (**LP3★ (MultiStepCoverageInvariance)**,
ASN-0098, the closure of the single-step LP3): every link designates exactly the
same content after the deletion as before. The link is anchored to bytes that still
exist; the strap stays attached. This is Nelson's survivability clause (4/43,
Q6, Q19).

What deletion *can* change is the link's discoverability *from `d`* — and here
the layering is precise. A link `a` is discoverable from a document iff some
slot's coverage meets that document's arranged I-address range:
`discoverable_from(a, d, Σ) ⟺ (E i : coverage(Σ.L(a).eᵢ) ∩ ran(M(d)) ≠ ∅)`
(foundation **LP12 (DiscoverabilityCharacterisation)**, ASN-0098). DELETE
shrinks `d`'s range — `ran(M'(d)) ⊆ ran(M(d))` — directly from its own clauses,
accounting for *both* subspaces. The surviving domain splits into the text
positions `L ∪ σ(R)` (DEL-DOM) and the link positions `V_{s_L}(d)` carried
through verbatim (DEL-FSUB), so the full post-state range decomposes as
`ran(M'(d)) = M(d)(L) ∪ M(d)(R) ∪ ran(M(d)\!\restriction\!V_{s_L}(d))`. Each
summand lies in `ran(M(d))`: the two text summands because DEL-LEFT and DEL-SHIFT
preserve every surviving position's I-address value (`M'(d)(v) = M(d)(v)` on `L`,
`M'(d)(σ(v)) = M(d)(v)` on the image of `R`), and the link summand because
DEL-FSUB holds the `s_L` positions and their images fixed. DEL-REMOVE drops the
deleted correspondences, contributing nothing new. Hence
`ran(M'(d)) ⊆ ran(M(d))`. If the
deletion removes the *last* V-position of `d` mapping into a link's coverage,
that link becomes *undiscoverable from `d`*: an orphaned reference in the sense
of **LP17 (GhostProjection)** (ASN-0098). But three things remain true, and they
are exactly Nelson's design intent:

- *The link persists.* `a ∈ dom(Σ'.L)` with `Σ'.L(a) = Σ.L(a)` (L12). The link
  orgl survives in storage; only the V→I bridge through `d`'s arrangement that
  *let `d` find it* has been severed. Following the link directly still resolves
  to the still-existing bytes (Q19).
- *The deleted material stays discoverable from any document that still arranges
  it.* Discoverability from a document `d'` depends only on
  `coverage(eᵢ) ∩ ran(M(d'))` (LP12), and `d'`'s arrangement is untouched (P5)
  while the I-addresses persist (P0). So if `d'` still maps an address in
  `A_del`, the link — and the content — remain discoverable from `d'` regardless
  of `d`'s deletion (foundation **LP16 (TransclusionDiscoverability)**, ASN-0098).
  This is the answer to *the discoverability of deleted material from other
  documents that still arrange it* (Q5, Q7): yes, unconditionally.
- *The link is re-discoverable from `d` if the content is re-arranged.* Because
  the I-addresses never left `C`, any later operation that places one of them
  back into `d`'s arrangement makes the link discoverable from `d` again —
  *resurrection* in the sense of **LP18** (ASN-0098). Deletion is not a
  one-way door at the content layer.

**P4 (LinkSurvival).** *For every endset `e` existing in `Σ`,
`coverage_{Σ'}(e) = coverage_{Σ}(e)` (DEL-LIMM + LP3★, which closes single-step
LP3 over the composite; the lone-K.μ⁻ `R = ∅` case needs only LP3) — no link's designated
content changes, and the link store is untouched (`Σ'.L = Σ.L`). A link discoverable from `d` before
the deletion remains discoverable from `d` iff some surviving V-position of `d`
still maps into its coverage; otherwise it is orphaned from `d` (LP17) yet
persists (L12), remains discoverable from every other document that still
arranges its coverage (LP16), and is re-discoverable from `d` should the content
be re-arranged (LP18).*

## A weakest precondition: when is discoverability preserved?

P4 leaves one question pointed but unanswered: under what condition does DELETE
*preserve*, rather than possibly shrink, the set of links discoverable from `d`?
The wp below is conditional in the *shrinking* direction, and the place it fails
is exactly the orphaning P4 records.

Write `D(d, Σ) = {a ∈ dom(Σ.L) : discoverable_from(a, d, Σ)}`. We seek

> `wp(DELETE, "D(d, Σ') = D(d, Σ)")`.

We read `ran(M'(d))` off the Effect. Note `ran(M'(d))` is the *full-document*
range, spanning both subspaces. Left text positions keep their I-addresses
(DEL-LEFT); shifted text positions carry their I-addresses to new slots
(DEL-SHIFT); the deleted block contributes nothing (DEL-REMOVE); and the
link-subspace positions (subspace `s_L`) are preserved verbatim (DEL-FSUB),
contributing `ran(M(d)\!\restriction\!V_{s_L}(d))` unchanged. Hence, writing
`M(d)\!\restriction\!Y` for the image of the position set `Y`,

> `ran(M'(d)) = (M(d)(L) ∪ M(d)(R)) ∪ ran(M(d)\!\restriction\!V_{s_L}(d)) = ran(M(d)) \ A_del^{excl}`,

where `A_del^{excl} = A_del \ M(d)(L ∪ R)` is the set of deleted I-addresses
that *no surviving position of `d` also maps* — the addresses `d` loses from its
range entirely. The second equality is justified, not asserted: `A_del` consists
of *text* content addresses (`subspace_I = s_C`, by S7b/L0), hence disjoint from
the unchanged `s_L` images, so removing exactly `A_del^{excl}` from the full prior
range `ran(M(d))` — which already contained those same `s_L` images verbatim —
yields precisely the full post-state range. The intermediate text-subspace term
`M(d)(L) ∪ M(d)(R)` alone would *not* equal `ran(M'(d))`; the link-subspace
images must be carried through, and they are. This matters because LP12 evaluates
discoverability against the full `ran(M(d))`, and a link's coverage may reference
link-subspace addresses (L4(c), cross-subspace endsets). (If a deleted I-address is also arranged elsewhere in `d` — the
within-document sharing that S5/M13 of the arrangement model permit — it does
not leave the range.) The link store is fixed throughout — `dom(Σ'.L) = dom(Σ.L)`
(DEL-LIMM) — so `D(d, ·)` is computed over the *same* index set before and after,
and the quantification "for every prior link `a ∈ dom(Σ.L)`" below exhausts
`dom(Σ'.L)` as well; were DELETE permitted to add a link, `D(d, Σ')` could acquire
a member with no pre-image and the identity `D(d, Σ') = D(d, Σ)` would fail.
Substituting into LP12, for every prior link `a`,

```
  discoverable_from(a, d, Σ')
    ⟺ (E i : coverage(eᵢ) ∩ (ran(M(d)) \ A_del^{excl}) ≠ ∅).
```

A link drops from `D(d, ·)` precisely when *all* of its witnesses in `d` lay in
`A_del^{excl}` — when the deleted span carried the link's last anchor in `d`.
Therefore

> `wp(DELETE, D(d, Σ') = D(d, Σ)) ≡ DELETE-pre ∧ (A a ∈ dom(Σ.L) :`
> `(E i : coverage(Σ.L(a).eᵢ) ∩ ran(M(d)) ≠ ∅) ⟹ (E i : coverage(Σ.L(a).eᵢ) ∩ (ran(M(d)) \ A_del^{excl}) ≠ ∅))`.

The quantifier structure is essential. Discoverability of a link is *existential*
over its slots — `discoverable_from(a, d, Σ) ⟺ (E i : coverage(eᵢ) ∩ ran(M(d)) ≠ ∅)`
(LP12) — so preservation must be stated per *link*, not per *slot*. A per-slot
universal would wrongly reject a link that loses all witnesses in one slot but
keeps a witness in another: that link is still discoverable (some slot survives),
so `D(d, ·)` retains it, yet a per-slot reading would falsify the implication on
the emptied slot. The per-link existential above is exactly the weakest condition,
matching the "last witness" reading below; a per-slot universal would be merely
sufficient, not necessary.

The derived consequence is exact and informative. Discoverability from `d` is
preserved precisely when the deleted span removed *no link's last witness* — when
every link still has something left at each end *within `d`*. This is Nelson's
survivability qualifier "if anything is left at each end" (4/43) read at the
level of one document's discoverability: the link itself never dies (P4), but a
*document's ability to find it* survives exactly when the deletion spared at
least one of that document's anchors to it. Had P4 asserted unconditional
preservation of discoverability, this computation would have refuted it: the
escape branch — every slot of `a` whose coverage met `ran(M(d))` has that meeting
contained in `A_del^{excl}`, so no slot retains a witness — is realised exactly in
the last-witness case. The wp is the formal witness that "deletion preserves
discoverability" is a *conditional*, not a theorem: deletion can only orphan,
never resurrect, discoverability from `d`.

## A worked deletion

Fix the text subspace `S = s_C` at depth `m = 2`, so `q_k = [s_C, k]` and
`σ(q_k) = q_{k−c}`. Let `d` hold `N = 5` text positions,
`V_S(d) = {q_1, …, q_5}`, with `M(d)(q_k) = a_k` for `k = 1, …, 5`. Each `a_k`
is a permanent I-address in `dom(C)`.

**Delete the span at `p = q_3` of width `c = 2`** (removing `q_3, q_4`). Here
`J = 3`, `w = [0, 2]`, `r = p ⊕ w = q_5`, `R = {q_5}`, `L = {q_1, q_2}`,
`X = {q_3, q_4}`. Containment holds: `J = 3 ≥ 1` and `J + c = 5 ≤ N + 1 = 6`.

*Content frame (DEL-CIMM, P0).* `Σ'.C = Σ.C`. The deleted I-addresses
`A_del = {a_3, a_4}` remain in `dom(C')` with their bytes intact. Nothing is
allocated or freed. ✓ P0, P3.

*Removal (DEL-REMOVE, P1).* The two correspondences `q_3 ↦ a_3` and `q_4 ↦ a_4`
leave the arrangement. The position labels that actually vacate the domain are the
top `c = 2`, namely `q_4, q_5`; the deleted-span label `q_3` stays in `dom(M'(d))`
but is reoccupied by the shifted survivor `q_5 → q_3`, so `M'(d)(q_3) = a_5`
(DEL-SHIFT). The surviving domain is `{q_1, q_2, q_3}` (DEL-DOM). ✓ P1.

*Shift (DEL-SHIFT, DEL-LEFT).* Prefix `q_1, q_2` unchanged (DEL-LEFT). The lone
suffix position shifts left by `c = 2`:

```
  q_5 → q_3   carrying a_5      (σ(q_5) = q_{5−2} = q_3,  M'(d)(q_3) = a_5)
```

The gap closes exactly: `σ(r) = σ(q_5) = q_3 = q_J` (D-SEP). ✓ DEL-SHIFT, D-SEP.

*Domain (DEL-DOM, P2).* Surviving index set `{1, 2}` (prefix) ∪ `{3}` (shifted
suffix) = `{1, 2, 3}`, consecutive and gap-free. So `V_S(d') = {q_1, q_2, q_3}`,
the dense run with `N' = N − c = 3`. ✓ P2, D-SEQ-post.

*Reading end to end* now yields `a_1, a_2, a_5` — the original content with the
third and fourth units omitted and the stream re-closed, exactly Nelson's
canonical-order guarantee (Q2). The bytes `a_3, a_4` are not gone: they sit in
`C`, recoverable by backtrack, still resolved by any link or any other document
that names them.

**A multi-position suffix shift (`|R| ≥ 2`).** The primary scenario moved a lone
suffix position, so it never exercised DELETE's signature effect: the *uniform*
left-shift of an entire suffix of two or more positions, all by the same `c`,
with their relative order preserved. Take the same `N = 5` document and **delete
the span at `p = q_2` of width `c = 1`** (removing `q_2`). Here `J = 2`,
`w = [0, 1]`, `r = p ⊕ w = q_3`, `L = {q_1}`, `X = {q_2}`,
`R = {q_3, q_4, q_5}` — three suffix positions. Containment holds: `J = 2 ≥ 1`
and `J + c = 3 ≤ N + 1 = 6`.

*Shift (DEL-SHIFT, DEL-LEFT).* Prefix `q_1` unchanged (DEL-LEFT). All three
suffix positions shift left by `c = 1`, each carrying its I-address:

```
  q_3 → q_2   carrying a_3      (σ(q_3) = q_{3−1} = q_2,  M'(d)(q_2) = a_3)
  q_4 → q_3   carrying a_4      (σ(q_4) = q_{4−1} = q_3,  M'(d)(q_3) = a_4)
  q_5 → q_4   carrying a_5      (σ(q_5) = q_{5−1} = q_4,  M'(d)(q_4) = a_5)
```

Every following position moves by the *same* constant `c = 1`, and the source
order `q_3 < q_4 < q_5` is carried to the image order `q_2 < q_3 < q_4` — the
shift is the order-preserving injection `σ` (D-BJ), demonstrated here across
multiple positions rather than one. The gap closes exactly: `σ(r) = σ(q_3) = q_2
= q_J` (D-SEP).

*Domain (DEL-DOM, P2).* Surviving index set `{1}` (prefix) ∪ `{2, 3, 4}` (shifted
suffix) = `{1, 2, 3, 4}`, consecutive and gap-free. So `V_S(d') = {q_1, …, q_4}`,
the dense run with `N' = N − c = 4`. Reading end to end yields `a_1, a_3, a_4, a_5`
— the second unit omitted, the remaining three re-closed in their original
relative order. ✓ DEL-SHIFT, D-BJ, P2.

**Boundary — leading-span delete (`J = 1`, `R ≠ ∅`).** None of the cases above
exercises the most delicate composite interaction: step-1 K.μ⁻ *emptying* the
text subspace and step-2 K.μ⁺ re-adding survivors *into the emptied subspace*,
re-pinning S8-depth from scratch. This is exactly the first-position-with-
survivors case. Take the same `N = 5` document and **delete the opening span at
`p = q_1` of width `c = 1`** (removing `q_1`). Here `J = 1`, `w = [0, 1]`,
`r = p ⊕ w = q_2`, `L = ∅`, `X = {q_1}`, `R = {q_2, q_3, q_4, q_5}`. Containment
holds: `J = 1 ≥ 1` and `J + c = 2 ≤ N + 1 = 6`. Since `R ≠ ∅`, DELETE is the
K.μ⁻ + K.μ⁺ composite.

*Step 1 (K.μ⁻ to empty).* The text subspace contracts to its surviving prefix
`L = ∅` — retention count `n'_{s_C} = J − 1 = 0` — while the link subspace holds
at full retention. After this step `d`'s text arrangement is *empty*:
`V_{s_C}(d) = ∅`. The strict-contraction obligation is met (`0 < N = 5`).

*Step 2 (K.μ⁺ from empty).* The `N − c − (J − 1) = 4` survivors are re-placed at
the closed-up text positions `{q_1, q_2, q_3, q_4}`, each carrying the I-address
it held before — the former images of `q_2, q_3, q_4, q_5`:

```
  q_1 ↦ a_2     q_2 ↦ a_3     q_3 ↦ a_4     q_4 ↦ a_5
```

Because step 1 emptied the text subspace, this K.μ⁺ inserts into an *empty*
subspace and re-pins S8-depth from scratch at `m = 2` (S8a, S8-depth), seating
the canonical first position `min(V_{s_C}(d')) = q_1` (D-MIN) and the dense run
`{q_1, …, q_4}` (D-CTG). Each placed I-address is in `dom(C)` (P0), so K.μ⁺'s
placement precondition is met, and four mappings are added — the strict-extension
precondition is satisfied. Equivalently `σ(q_k) = q_{k−1}` carries each `v ∈ R`
left by `c = 1` with its content (DEL-SHIFT).

*Net effect.* `V_S(d') = {q_1, …, q_4} = {q_1, …, q_{N−1}}`, the dense run with
`N' = N − c = 4`, every survivor's I-address carried unchanged from its pre-state
slot. The gap closes exactly: `σ(r) = σ(q_2) = q_1 = q_J` (D-SEP). Reading end to
end yields `a_2, a_3, a_4, a_5` — the opening unit omitted, the rest re-closed in
order. The deleted `a_1` persists in `C` (P0). ✓ DEL-SHIFT, D-BJ, D-SEP, P2,
D-SEQ-post.

**Boundary — suffix delete (`J + c = N + 1`).** Take `p = q_4`, `c = 2`, so
`r = q_6`, `R = ∅`. This is the `R = ∅` case, realised as a *single* K.μ⁻ step (no
K.μ⁺): a prefix-retention truncation of the text subspace to count
`n'_{s_C} = J − 1 = N − c = 3`. No position is shifted (DEL-SHIFT vacuous);
`q_4, q_5` are removed; the surviving prefix `{q_1, q_2, q_3}` stays at its
original positions, already the closed-up dense run, so `V_S(d') = {q_1, q_2, q_3}`,
`N' = 3`. Deleting the tail moves nothing. K.μ⁻'s self-sufficiency (J2) supplies
the frames directly: `Σ'.C = Σ.C` (P0, DEL-CIMM), `Σ'.E = Σ.E` (DEL-FENT),
`Σ'.R = Σ.R` (DEL-FPROV), and the link store fixed (DEL-LIMM). S3★ holds because
every surviving text image is unchanged with `C' = C`, and the link positions are
untouched; P4★ and P7a hold by the Effect-section preservation argument.
✓ DEL-DOM, P2, S3★, DEL-FENT, DEL-FPROV, P4★, P7a.

**Boundary — delete everything (`J = 1`, `c = N`).** Take `p = q_1`, `c = 5`,
`r = q_6`. This too is the `R = ∅` case, realised as a single K.μ⁻ step — here a
prefix-retention truncation to count `n'_{s_C} = J − 1 = 0` (the empty prefix). All
five mappings are removed; `R = ∅`; `V_S(d') = ∅`, the empty arrangement. By J2 the
frames hold directly: the content store is still `Σ.C` — every `a_k` survives
(P0, DEL-CIMM) — the entity set and provenance relation are fixed (DEL-FENT,
DEL-FPROV), and the link store is untouched (DEL-LIMM). S3★ is vacuous over the
now-empty text arrangement and verbatim on the untouched link positions; P4★ and
P7a hold by the Effect-section preservation argument. The document now arranges no text, yet all of
its former content remains permanent and reconstructible (Q20); the resulting
empty text arrangement denotes the empty partial function. ✓ P0, P2 (with
`N' = 0`), S3★, DEL-FENT, DEL-FPROV, P4★, P7a.

**Within-document sharing.** Suppose additionally `M(d)(q_2) = a_5` — `d`
arranges the content `a_5` at *two* positions. Delete `p = q_5`, `c = 1`. Then
`A_del = {a_5}` but `A_del^{excl} = ∅`, because `a_5` is still mapped by the
surviving `q_2`. A link whose coverage contains `a_5` remains discoverable from
`d` *despite* the deletion — the wp's preservation condition holds because
something was left at that end within `d`. ✓ P4, wp.

**Cross-document transclusion (P5 in the concrete).** The scenarios above all
live inside the single document `d`; none exercises the operation's signature
isolation guarantee. So introduce a *second* document `d'` that transcludes some
of `d`'s content. Concretely, let `d'` arrange the deleted I-addresses: with
`V_S(d') = {q'_1, q'_2}` (`d'`'s own canonical run, depth `m = 2`, at its own
document prefix) and `M(d')(q'_1) = a_3`, `M(d')(q'_2) = a_4` — the very two
addresses `A_del = {a_3, a_4}` that the primary scenario deletes from `d`. This is
transclusion by reference: `d'` shares `d`'s content identity without copying,
since both arrange the *same* permanent I-addresses (S5/M13 across documents).

Now perform exactly the primary deletion on `d` — `p = q_3`, `c = 2`, removing
`q_3, q_4` from `d`. We check the two facts P5 names against this concrete `d'`:

- *Arrangement untouched (DEL-FDOC).* `d' ≠ d`, so `M'(d') = M(d')` verbatim:
  `q'_1 ↦ a_3` and `q'_2 ↦ a_4` are exactly the bindings they were before. DELETE
  resolves `d`'s arrangement enfilade alone and names no position of `d'`; the
  left-shift, the gap-closure, the domain contraction all happen inside `d`. ✓
  DEL-FDOC, P5.
- *Resolved content unchanged (P0).* `Σ'.C = Σ.C`, so `a_3, a_4 ∈ dom(C')` with
  `C'(a_3) = C(a_3)`, `C'(a_4) = C(a_4)`. Hence `d'` resolves `q'_1` to the same
  bytes `C(a_3)` and `q'_2` to the same bytes `C(a_4)` after the deletion as
  before. Reading `d'` end to end yields exactly what it yielded before `d`'s
  deletion. ✓ P0, P5.

The deletion in `d` is therefore *invisible* to `d'`: `d'`'s arrangement and the
content it resolves are bit-for-bit identical across the transition, even though
the same I-addresses just vanished from `d`'s present view. This is the formal
content of Nelson's "may remain included in other versions" (4/9, 4/11) — the
deleted bytes "remain in all other documents where they have been included."
Were DELETE to free `a_3, a_4` from the store, `d'` would resolve `q'_1, q'_2` to
nothing and the transclusion would shatter; non-destruction (P0) is precisely
what keeps the sharer whole. And any link whose coverage contains `a_3` or `a_4`
stays discoverable from `d'` regardless of `d`'s deletion, since
`coverage(eᵢ) ∩ ran(M'(d')) = coverage(eᵢ) ∩ ran(M(d')) ≠ ∅` is untouched
(LP16, TransclusionDiscoverability) — the orphaning the wp computes is strictly
*local to `d`*. ✓ P5, P4.

## What we have established

One effect, one layer touched, the other held in perfect frame. On the content
layer DELETE does *nothing*: `Σ'.C = Σ.C`, append-only taken to its limit — not
even an append (P0, P3). The deleted bytes survive at their permanent
I-addresses forever; this is the non-destruction guarantee, and it is a frame
condition, not a courtesy. On the arrangement layer DELETE is a uniform left-
shift confined to one subspace of one document (DEL-REMOVE, DEL-SHIFT, DEL-LEFT,
DEL-DOM, DEL-FSUB, DEL-FDOC), closing the gap exactly and re-coordinating the
suffix around fixed content identities. The well-formedness of the V-stream is
preserved (D-SEQ/D-MIN/D-CTG-post with `N' = N − c`), the survivors re-close into
a single dense run (P2), every link survives because it anchors on immutable
identity (P4), the deleted material stays discoverable from every other document
that still arranges it (P4, P5), and every other document is isolated because
identity is shared by reference, not by arrangement (P5). The bytes endure;
only their placement in this one document's present view is withdrawn.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| DELETE | Operation: remove the span `(p, w)` of width `c` from document `d`'s arrangement; shift the suffix left to close the gap; touch the content store not at all | introduced |
| P0 (NonDestruction) | `dom(C') = dom(C)` with all values preserved; every deleted I-address `A_del` survives in `C` — the permanent content store is untouched | introduced |
| P1 (ArrangementContraction) | The deleted span's `c` V→I mappings are removed from the arrangement only; no content is removed | introduced |
| P2 (GapClosure) | Survivors close into the dense run `{q_1, …, q_{N−c}}`; prefix fixed, suffix shifts left by `c` carrying I-addresses unchanged, gap closes exactly, order and density preserved | introduced |
| P3 (AddressPermanence) | No I-address is removed or rebound; DELETE allocates and frees nothing — the content layer is invariant | introduced |
| P4 (LinkSurvival) | Every endset's coverage is unchanged and the link store untouched, `Σ'.L = Σ.L` (DEL-LIMM + LP3★, closing single-step LP3 over the composite); a link orphaned from `d` (LP17) still persists, stays discoverable from other documents arranging it (LP16), and is re-discoverable on re-arrangement (LP18) | introduced |
| P5 (DocumentIsolation) | Every other document's arrangement and resolved content — including transcluders of the deleted I-addresses — are invariant under DELETE on `d` | introduced |
| DEL-REMOVE | The arrangement loses exactly `c` V→I correspondences (`|{v ∈ dom(M'(d)) : subspace(v) = S}| = N − c`) and the top `c` labels `{q_{N−c+1}, …, q_N}` leave `dom(M'(d))`; the deleted I-addresses persist in `C` | introduced |
| DEL-SHIFT | Suffix positions `v ∈ R` move to `σ(v) = q_{k−c}`, carrying their I-address (ASN-0082 D-SHIFT) | introduced |
| DEL-LEFT | Prefix positions `v < p` are unchanged (ASN-0082 D-L) | introduced |
| DEL-DOM | `V_S(d')` is the dense run `{q_1, …, q_{N−c}}` with the gap closed (ASN-0082 D-DOM, D-SEP) | introduced |
| DEL-CIMM | `Σ'.C = Σ.C` — the content store is a strict frame (ASN-0082 D-I) | introduced |
| DEL-LIMM | `Σ'.L = Σ.L` — the link store is a strict frame, domain and value (stronger than L12) | introduced |
| DEL-FSUB | Positions in subspaces `S' ≠ S` (notably links) are unchanged (ASN-0082 D-CS) | introduced |
| DEL-FDOC | Arrangements of all documents `d' ≠ d` are unchanged (ASN-0082 D-CD) | introduced |
| DEL-FENT | `Σ'.E = Σ.E` — the entity set is a strict frame (the K.μ⁻+K.μ⁺ composite entity frames, ASN-0047); P1/P8 preserved | introduced |
| DEL-FPROV | `Σ'.R = Σ.R` — the provenance relation is a strict frame (the K.μ⁻+K.μ⁺ composite provenance frames, ASN-0047); P4★/P7a preserved | introduced |

## Open Questions

What must DELETE guarantee about the well-formedness of a deletion whose span begins before the document's first arranged position, so that no surviving V-position is carried below the document's origin?

Under what conditions may a deletion and a concurrent operation on the same document's content scope both be applied without a serializing authority while preserving canonical order?

What invariant relates a content-based discovery index to the arrangement after a deletion, given that the deleted I-addresses persist while the deleting document no longer arranges them?

What must the system guarantee about the reconstructibility of a prior arrangement from the permanent content store after a deletion, and what state beyond the content store must persist for backtrack to be exact?

What relationship must hold between a deletion that orphans a link from one document and the obligations of the documents that continue to arrange the same content?
