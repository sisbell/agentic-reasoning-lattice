# ASN-0089: INSERT Operation

*2026-05-24*

We are asking what changes when new content joins a document at a chosen position. The naive answer — "put the content at the position" — hides everything important. We must say what is allocated (because Xanadu's permanence guarantee demands new content receive permanent identity), what shifts (because content beyond the insertion point cannot occupy the same V-positions), what stays the same (because identity-bearing references depend on stability), and what it means for all of this to happen as one event.

Nelson's specification at [LM 4/66] is one sentence: "This inserts `<text set>` in document `<doc id>` at `<doc vsa>`. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." The sentence is deceptively compact. The verb "inserts" hides allocation. The phrase "v-stream addresses ... are increased" hides which addresses do not change. The constraint "in the document" hides the cross-document frame. Our task is to recover these implicit commitments and state them as named, verifiable claims.

## Foundation setting

We work in the foundation state introduced by ASN-0036 and ASN-0093: a content store `Σ.C : T ⇀ Val`, a link store `Σ.L : T ⇀ Endset*`, a document set `dom(Σ.M) ⊆ T`, and per-document arrangements `Σ.M(d) : T ⇀ T`. Foundation invariants we will preserve include S0 (content immutability), S2 (arrangement functionality), S3 (referential integrity), S7 (structural attribution), S8a (V-position well-formedness), S8-depth (per-subspace depth uniformity), S8-fin (arrangement finiteness), D-CTG, D-MIN, D-SEQ (text-subspace contiguity), L0 (subspace partition), and L14 (store disjointness).

We work with the content subspace `s_C = 1` (SubspaceConventionAxiom of ASN-0093). For each document `d`, let `V_1(d) = {v ∈ dom(Σ.M(d)) : subspace(v) = s_C}`. By S8-depth, when `V_1(d)` is non-empty its positions share a common depth `m_C ≥ 2`; by D-SEQ, `V_1(d) = {[1, 1, ..., 1, k] : 1 ≤ k ≤ N}` for some `N ≥ 1`. The shift function `shift(v, n) = v ⊕ δ(n, #v)` is the OrdinalShift of ASN-0034; for a depth-`m` V-position `v`, `shift(v, n)` agrees with `v` on positions `1, ..., m-1` and adds `n` to position `m`. By convention `shift(v, 0) = v` (OrdinalShiftBase).

## The operation signature

We are looking for the minimum input INSERT needs. It needs a target document (to scope the new content), a position (where in the V-stream the content goes), and the content itself (which values to place).

**INS-OP** (operation signature). An INSERT operation is parameterized by a tuple `(d, p, ⟨v_1, ..., v_n⟩)` where:

- `d ∈ dom(Σ.M)` — an allocated document;
- `p ∈ T` with `subspace(p) = s_C` — a V-position in the content subspace;
- `n ≥ 1` and `v_1, ..., v_n ∈ Val` — the content values, in order.

We call `n` the *insertion width* and `p` the *insertion position*. Nelson explicitly admits insertions at any position in the document's V-extent [LM 4/66, Q6]: the beginning, the end (where APPEND is a convenience for the same effect), or any interior point. The empty case — first insertion into a fresh document — is also admitted.

## Valid positions

We need to constrain `p` so that the post-state remains coherent. The constraint emerges from two foundation invariants: the V-positions in subspace 1 must remain contiguous (D-CTG), starting at `[1, 1, ..., 1]` (D-MIN). Any choice of `p` that would create gaps is inadmissible.

**INS-VALID** (valid insertion position). Two cases by the state of `V_1(d)` in `Σ`:

*Empty case.* If `V_1(d) = ∅`, then `p = [1, 1, ..., 1]` (the canonical minimum, by D-MIN) for some depth `m_C ≥ 2` (by S8a). The depth `m_C` is chosen by the operation; once chosen, S8-depth fixes it for all subsequent text-subspace V-positions of `d`.

*Non-empty case.* If `V_1(d) ≠ ∅` with common depth `m_C` and D-SEQ enumeration `V_1(d) = {[1, 1, ..., 1, k] : 1 ≤ k ≤ N}`, then `p = [1, 1, ..., 1, j]` for some `j ∈ {1, 2, ..., N+1}` of depth `m_C`.

The bound `j ≤ N+1` is forced. Were `j > N+1`, the new positions `[1, ..., 1, j], [1, ..., 1, j+1], ..., [1, ..., 1, j+n-1]` would lie above the existing run with a gap of `[1, ..., 1, N+1], ..., [1, ..., 1, j-1]` between, violating D-CTG. The boundary `j = N+1` is exactly Nelson's APPEND case — every existing position lies strictly below `p`, no shifting is needed. The boundary `j = 1` is prepending — every existing position lies at or above `p`, and every one shifts by `n`. Intermediate `j` splits the run.

The depth constraint `#p = m_C` (in the non-empty case) is forced by S8-depth: if `#p` differed, the post-state would contain V-positions of two different depths in the same subspace.

## What must be allocated

We need to assign permanent identity to the new content. This is the first place where Nelson's design intent commits us: the Istream is append-only, and content within it is permanent and immutable. Nelson [LM 2/14]:

> Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically.

We observe two requirements together. The new content must receive *fresh* I-addresses — addresses not previously bound — because P0 (content permanence from ASN-0093) forbids overwriting existing bindings. And those addresses must be *scoped to d* — because origin attribution flows from the I-address (S7), and the new content's origin is `d`.

**INS-ALLOC** (content allocation). INSERT produces a sequence of `n` I-addresses `⟨a_1, ..., a_n⟩` satisfying, against the pre-state `Σ`:

(a) *Freshness.* `(A i : 1 ≤ i ≤ n : a_i ∉ dom(Σ.C) ∪ dom(Σ.L))`.

(b) *Home-document scope.* `(A i : 1 ≤ i ≤ n : origin(a_i) = d)`.

(c) *Structural form.* `(A i : 1 ≤ i ≤ n : zeros(a_i) = 3 ∧ E(a_i)_1 = s_C ∧ #E(a_i) ≥ 2)`.

(d) *Distinctness.* `(A i, j : 1 ≤ i < j ≤ n : a_i ≠ a_j)`.

In the post-state `Σ'`:

(e) *Domain extension.* `dom(Σ'.C) = dom(Σ.C) ∪ {a_1, ..., a_n}`.

(f) *Value placement.* `(A i : 1 ≤ i ≤ n : Σ'.C(a_i) = v_i)`.

The freshness condition (a) protects L14 (store disjointness): the new addresses do not collide with any link address. The scope condition (b) makes origin-based attribution well-defined: every byte of new content is traceable to `d`, supporting Nelson's [LM 2/45] royalty mechanism and [LM 2/40] "always know where you are". The structural conditions (c) are what the substrate's content sub-allocator `A_C(d)` (ASN-0093) is constructed to guarantee.

We note an implementation-specific observation that does not rise to an abstract claim: in the substrate of ASN-0093, consecutive applications of `K.α` produce consecutive addresses on `d`'s content chain, so `a_{i+1} = inc(a_i, 0)` for `1 ≤ i < n`. This contiguity in I-space enables Gregory's coalescing optimization where the next adjacent INSERT can extend an existing crum instead of creating a new one (Q11, Q13). An alternative implementation could allocate non-contiguous addresses, satisfying INS-ALLOC at higher constant cost. The abstract requirement is fresh + scoped + distinct, not contiguous.

## What must shift

Existing V-positions at or beyond `p` must move. Nelson's "v-stream addresses ... are increased by the length of the inserted text" admits two possible readings: shift the V-positions (the mapping changes which positions exist), or renumber the I-addresses they target (the storage changes its labels). The second reading is ruled out by Nelson's design. From Q5:

> The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this. [LM 4/11]

The "address ... constantly changing" refers to *V-addresses*. I-addresses, by [LM 4/30] and [LM 2/14], never change. The shift must therefore be a V-position operation only.

We split the post-state into three regions by what happens to each pre-existing position.

**INS-PRESERVE-LEFT** (left preservation). For every `v ∈ V_1(d)` with `v < p`:

`v ∈ dom(Σ'.M(d)) ∧ Σ'.M(d)(v) = Σ.M(d)(v)`

Pre-existing positions strictly below `p` remain at the same V-position with the same I-address target. Their content has not moved in either coordinate.

**INS-SHIFT** (right shift). For every `v ∈ V_1(d)` with `v ≥ p`:

`shift(v, n) ∈ dom(Σ'.M(d)) ∧ Σ'.M(d)(shift(v, n)) = Σ.M(d)(v)`

Pre-existing positions at or above `p` have new V-positions `shift(v, n)`, but their I-address target is unchanged. The content has moved *only* in V-coordinate; its identity is invariant.

The new positions vacated at the original `v` for `v ∈ V_1(d)` with `v ≥ p` are precisely the `n` positions `[1, ..., 1, j], [1, ..., 1, j+1], ..., [1, ..., 1, j+n-1]` — the gap into which the new content settles.

**INS-PLACE** (new content placement). For each `k ∈ {0, 1, ..., n-1}`:

`shift(p, k) ∈ dom(Σ'.M(d)) ∧ Σ'.M(d)(shift(p, k)) = a_{k+1}`

The `k`-th unit of new content occupies the position `shift(p, k)`, where `shift(p, 0) = p` by OrdinalShiftBase. The ordering is preserved: the values `v_1, ..., v_n` from INS-OP map to the positions `p, shift(p, 1), ..., shift(p, n-1)` in order, via the addresses `a_1, ..., a_n` of INS-ALLOC.

**INS-DOMAIN-CLOSURE** (post-state subspace-1 domain). The post-state's text-subspace V-positions are exactly the union of the three regions:

`V_1(d') = {v ∈ V_1(d) : v < p} ∪ {shift(v, n) : v ∈ V_1(d) ∧ v ≥ p} ∪ {shift(p, k) : 0 ≤ k < n}`

Computing with the D-SEQ enumeration `V_1(d) = {[1, ..., 1, k] : 1 ≤ k ≤ N}` and `p = [1, ..., 1, j]`:

- Left region: `{[1, ..., 1, k] : 1 ≤ k < j}` — `j-1` positions
- Shifted region: `{[1, ..., 1, k+n] : j ≤ k ≤ N} = {[1, ..., 1, k] : j+n ≤ k ≤ N+n}` — `N-j+1` positions
- New region: `{[1, ..., 1, k] : j ≤ k < j+n}` — `n` positions

The union: `{[1, ..., 1, k] : 1 ≤ k ≤ N+n}`. The post-state is contiguous (D-CTG holds) and starts at `[1, ..., 1, 1]` (D-MIN holds), with `|V_1(d')| = N + n`.

## What must not change

The frame is at least as important as the effect. Nelson's [LM 4/11] insistence that editing is a per-document operation is what makes the system safe for independent authors working on shared content. We collect all the non-changes.

**INS-FRAME** (frame conditions). The following hold of every state transition produced by INSERT(d, p, ⟨v_1, ..., v_n⟩):

(a) *Content immutability.* `(A a ∈ dom(Σ.C) : a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))`. Every existing content address persists with its value.

(b) *Link store unchanged.* `Σ'.L = Σ.L`. INSERT neither allocates, modifies, nor removes any link.

(c) *Other documents unchanged.* `(A d' ∈ dom(Σ.M) : d' ≠ d ⟹ Σ'.M(d') = Σ.M(d'))`.

(d) *Other subspaces of d unchanged.* `(A v ∈ dom(Σ.M(d)) : subspace(v) ≠ s_C ⟹ v ∈ dom(Σ'.M(d)) ∧ Σ'.M(d)(v) = Σ.M(d)(v))`.

(e) *Document set unchanged.* `dom(Σ'.M) = dom(Σ.M)`. INSERT does not create or remove documents.

(f) *Origin permanence.* `(A a ∈ dom(Σ.C) : origin_{Σ'}(a) = origin_{Σ}(a))`. By (a), `dom(C)` grows but does not change values; by the definition of origin from the address structure (S7), origin is determined by the address alone and is therefore unaffected by any state change.

Clause (c) is the structural protection of cross-document sharing. We re-derive Nelson's [Q3] guarantee: if content is shared between `d` and `d'` (i.e., `(E v_1 ∈ dom(Σ.M(d)), v_2 ∈ dom(Σ.M(d')) : Σ.M(d)(v_1) = Σ.M(d')(v_2))`), an INSERT into `d` does not alter `Σ.M(d')` (by INS-FRAME(c)) and does not alter the value at the shared I-address (by INS-FRAME(a)). The shared content is therefore visible at the same V-position in `d'` with the same value. Insertion into one document cannot leak into another.

Clause (d) is the within-document cross-subspace protection. INSERT into the content subspace does not perturb the link subspace's V-positions. From Q17, the foundation substrate need not even traverse link-subspace entries during the shift pass — they can be classified as outside the shift range — but at the abstract level, the requirement is simply that they remain unchanged.

## The identity-preservation guarantee

We have arrived at Nelson's central architectural commitment. INS-PRESERVE-LEFT, INS-SHIFT, and INS-FRAME together imply a deeper invariant that gives Xanadu its link-survivability property. We state it explicitly because it is the load-bearing claim for every operation that comes after INSERT.

**INS-IDENTITY** (permanent identity preservation). For every `v ∈ V_1(d)` in the pre-state, let `a = Σ.M(d)(v)`. Then:

(a) `a ∈ dom(Σ'.C)` — the I-address persists in the content store.

(b) `Σ'.C(a) = Σ.C(a)` — the value at that I-address is unchanged.

(c) `a ∈ ran(Σ'.M(d))` — `a` remains arranged in `d`, specifically at the V-position `v` if `v < p` (by INS-PRESERVE-LEFT) and at `shift(v, n)` if `v ≥ p` (by INS-SHIFT).

(d) For every other document `d''` with `a ∈ ran(Σ.M(d''))`: `a ∈ ran(Σ'.M(d''))` at the same V-position. By INS-FRAME(c), `Σ'.M(d'') = Σ.M(d'')`, so any pre-existing reference to `a` from `d''` is unchanged.

This is Nelson [LM 4/30] made formal:

> Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them.

Links attach to I-addresses. INSERT does not change I-addresses, does not change values at I-addresses, and does not remove any V-stream reference to any I-address. Therefore any link, anywhere in the system, that names an I-address in the pre-state continues to name the same content in the post-state. Link survivability under INSERT follows from INS-IDENTITY directly.

The contrapositive sharpens the claim. Suppose some implementation, in the course of "inserting", produced a post-state where a pre-existing I-address was bound to a different value, or removed from `dom(C)`, or no longer arranged in `d`. Then INS-IDENTITY would fail. By the chain of consequences:

- If (a) failed: a link to `a` would dangle.
- If (b) failed: a link to `a` would target different content (semantic corruption).
- If (c) failed: `a` would be orphaned in `d`'s arrangement — readable from the content store but absent from the document.

Any such implementation would violate the architectural guarantee. INS-IDENTITY is the structural commitment that rules these failures out.

## Atomicity

Nelson does not use the word "atomicity", but his [LM 1/34] "canonical order, which was an internal mandate of the system" carries the same force in different vocabulary. From Q4:

> The phrase "canonical order, which was an internal mandate" is the key. This is not a suggestion — it is a design requirement. After any change, the system must be in canonical order.

"Canonical order" means: every foundation invariant holds. The mandate is that the system never observably violates an invariant. We translate this into a constraint on INSERT.

**INS-ATOM** (atomic transition). INSERT is observable as a single state transition `Σ → Σ'`. The post-state satisfies INS-ALLOC, INS-PRESERVE-LEFT, INS-SHIFT, INS-PLACE, INS-DOMAIN-CLOSURE, and INS-FRAME, together with every foundation invariant carried forward (the next section verifies this). No state `Σ_mid` is observable between `Σ` and `Σ'` in which any of these conditions partially holds.

The constraint is on observation, not execution. An implementation may decompose INSERT into multiple internal steps — allocate addresses, shift existing positions, place new content — but no external observer (any operation that reads state) may witness an intermediate state. Equivalently, INSERT either fully commits or has no effect; the post-state is one in which all of INS-ALLOC through INS-FRAME hold simultaneously.

We do not specify behavior under infrastructure failure. Nelson [LM 5/18] disclaims hardware reliability. INS-ATOM constrains the abstract semantics: if the transition occurs, the post-state is fully canonical; if it does not occur, the pre-state is unchanged. The handling of partial failures (logging, rollback, retry) is implementation choice subject to this observable-atomicity requirement.

## Invariant preservation

We verify that the foundation invariants survive INSERT. For each invariant, we identify which part of the specification discharges its preservation.

| Invariant | Source | Discharged by |
|-----------|--------|---------------|
| P0 (content permanence) | ASN-0093 | INS-FRAME(a) on existing addresses; INS-ALLOC(e,f) on new ones |
| P1 (entity permanence, document set) | ASN-0047 | INS-FRAME(e) |
| S0 (content immutability) | ASN-0036 | INS-FRAME(a) |
| S2 (arrangement functionality) | ASN-0036 | Disjoint-domain argument, below |
| S3 (referential integrity) | ASN-0036 | Pre-existing mappings: INS-FRAME(a) preserves targets; new mappings: INS-ALLOC(e) places `a_i` in `dom(C')` |
| S7 (structural attribution) | ASN-0036 | INS-ALLOC(b,c) makes new addresses well-structured and `d`-scoped; INS-FRAME(a,f) preserves existing origins |
| S8a (V-position well-formedness) | ASN-0036 | Preserved positions: unchanged; shifted positions: shift preserves zero-count, depth, componentwise positivity; new positions: contiguous with existing, all components positive |
| S8-depth (per-subspace depth uniformity) | ASN-0036 | INS-VALID forces `#p = m_C`; all post-state subspace-1 positions have depth `m_C` |
| S8-fin (arrangement finiteness) | ASN-0036 | `|dom(Σ'.M(d))| = |dom(Σ.M(d))| + n`, still finite |
| D-CTG (text-subspace contiguity) | ASN-0036 | INS-DOMAIN-CLOSURE computation: post-state is `{[1, ..., 1, k] : 1 ≤ k ≤ N+n}`, contiguous |
| D-MIN (minimum position) | ASN-0036 | `[1, ..., 1, 1] ∈ V_1(d')`: either preserved (if `j > 1`) or established by INS-PLACE at `k = 0` (if `j = 1`) |
| D-SEQ (sequential structure) | ASN-0036 | Derived from D-CTG ∧ D-MIN ∧ S8-fin ∧ S8-depth |
| L0 (subspace partition, content) | ASN-0093 | INS-ALLOC(c): new addresses have `E(·)_1 = s_C` |
| L0 (subspace partition, link) | ASN-0093 | INS-FRAME(b): `L` unchanged |
| L14 (store disjointness) | ASN-0093 | INS-ALLOC(a): freshness against `dom(C) ∪ dom(L)`; pre-existing disjointness preserved by INS-FRAME(a,b) |
| C-fin (content store finiteness) | ASN-0093 | `|dom(Σ'.C)| = |dom(Σ.C)| + n`, still finite |
| L-fin (link store finiteness) | ASN-0093 | `dom(Σ'.L) = dom(Σ.L)` by INS-FRAME(b) |

The S2 discharge requires a moment of attention because the post-state mapping is built from three pieces and we must check that the pieces do not collide in their domains.

We decompose `Σ'.M(d)` (restricted to subspace 1) as the union of three partial functions:

- `M_L := {(v, Σ.M(d)(v)) : v ∈ V_1(d) ∧ v < p}` — the preserved-left mapping
- `M_S := {(shift(v, n), Σ.M(d)(v)) : v ∈ V_1(d) ∧ v ≥ p}` — the shifted-right mapping
- `M_N := {(shift(p, k-1), a_k) : 1 ≤ k ≤ n}` — the new-content mapping

With pre-state D-SEQ enumeration and `p = [1, ..., 1, j]`, the three domains are:

- `dom(M_L) = {[1, ..., 1, k] : 1 ≤ k < j}` — last component in `[1, j-1]`
- `dom(M_S) = {[1, ..., 1, k] : j+n ≤ k ≤ N+n}` — last component in `[j+n, N+n]`
- `dom(M_N) = {[1, ..., 1, k] : j ≤ k < j+n}` — last component in `[j, j+n-1]`

The three integer ranges `[1, j-1]`, `[j, j+n-1]`, `[j+n, N+n]` are pairwise disjoint by direct inspection on ℕ. By T3 (CanonicalRepresentation, ASN-0034), tumblers with different last components at common depth are distinct. So the three domains are pairwise disjoint. The union is a function: S2 holds.

The S3 discharge benefits from inspection. We must check that every `v ∈ dom(Σ'.M(d))` has `Σ'.M(d)(v) ∈ dom(Σ'.C)`. For `v ∈ dom(M_L)`: the target is `Σ.M(d)(v) ∈ dom(Σ.C) ⊆ dom(Σ'.C)` by pre-state S3 and INS-ALLOC(e). For `v ∈ dom(M_S)`: same target, same argument. For `v ∈ dom(M_N)`: the target is `a_k ∈ dom(Σ'.C)` by INS-ALLOC(e). Cross-subspace V-positions (handled by INS-FRAME(d)) map to targets already in `dom(C) ⊆ dom(C')`. S3 holds.

The S8a discharge for shifted positions deserves a moment. Given `v ∈ V_1(d)` with `v = [1, ..., 1, k]` of length `m_C`, `shift(v, n) = [1, ..., 1, k+n]`. Since `k ≥ 1` and `n ≥ 1`, the last component `k+n ≥ 2 ≥ 1` is positive; all other components are 1; zero-count is 0; length is `m_C ≥ 2`. S8a is satisfied.

## A note on what INSERT is not

It is worth distinguishing INSERT from operations that look superficially similar, because the distinction sharpens what INSERT requires.

INSERT is not transclusion. Transclusion (out of scope for this ASN) places references to *existing* I-addresses at new V-positions. INSERT, by INS-ALLOC, creates *fresh* I-addresses. Two INSERTs of identical content into two different documents produce structurally distinct content — different I-addresses, different origins, no shared identity. A transclusion of the same content into both documents preserves identity. The choice of operation determines who is attributed and what subsequent origin queries discover.

INSERT is not APPEND in any architecturally significant sense. APPEND is INSERT at `j = N+1` in the non-empty case, or the empty case with depth chosen by the operation. The structural effect is identical; APPEND is a convenience for callers who do not know `N`.

These distinctions are load-bearing for the foundation invariants: S7 (origin attribution) depends on INSERT producing fresh addresses; the D-SEQ structure of the text subspace depends on INSERT respecting INS-VALID's bound on `j`.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| INS-OP | INSERT operation signature: tuple `(d, p, ⟨v_1, ..., v_n⟩)` with `d ∈ dom(M)`, `subspace(p) = s_C`, `n ≥ 1`, `v_i ∈ Val` | introduced |
| INS-VALID | Valid insertion position: empty case `p = [1, ..., 1]` of operator-chosen depth `m_C ≥ 2`; non-empty case `p = [1, ..., 1, j]` with `j ∈ {1, ..., N+1}` and `#p = m_C` | introduced |
| INS-ALLOC | Content allocation: `n` fresh, distinct, `d`-scoped, element-level content addresses `⟨a_1, ..., a_n⟩` added to `dom(C)` with values `⟨v_1, ..., v_n⟩` | introduced |
| INS-PRESERVE-LEFT | `(A v ∈ V_1(d) : v < p : v ∈ dom(Σ'.M(d)) ∧ Σ'.M(d)(v) = Σ.M(d)(v))` | introduced |
| INS-SHIFT | `(A v ∈ V_1(d) : v ≥ p : shift(v, n) ∈ dom(Σ'.M(d)) ∧ Σ'.M(d)(shift(v, n)) = Σ.M(d)(v))` | introduced |
| INS-PLACE | `(A k : 0 ≤ k < n : shift(p, k) ∈ dom(Σ'.M(d)) ∧ Σ'.M(d)(shift(p, k)) = a_{k+1})` | introduced |
| INS-DOMAIN-CLOSURE | `V_1(d') = {v ∈ V_1(d) : v < p} ∪ {shift(v, n) : v ∈ V_1(d) ∧ v ≥ p} ∪ {shift(p, k) : 0 ≤ k < n}` | introduced |
| INS-FRAME | Six clauses: content immutability, link store unchanged, other documents unchanged, other subspaces of `d` unchanged, document set unchanged, origin permanence | introduced |
| INS-IDENTITY | Permanent identity preservation: every pre-existing I-address persists with its value, remains arranged in `d` at `v` (if `v < p`) or `shift(v, n)` (if `v ≥ p`), and any other document's reference to it is unchanged | introduced |
| INS-ATOM | INSERT is a single observable state transition; no intermediate state in which the operation has partially committed is observable | introduced |

## Open Questions

What invariants must INSERT preserve about the ordering between newly allocated I-addresses and those allocated by prior operations on the same document?

What does INSERT guarantee about the resolvability of a link allocated before INSERT whose endpoint references an I-address that INSERT shifts in V-coordinate but preserves in identity?

Under what conditions must INSERT fail to commit rather than produce a post-state that satisfies the operation's specification?

What additional invariants must INSERT preserve when applied to a document that is concurrently the source of a transclusion held by another document?

What guarantees must INSERT make about the relationship between the new content's V-extent and any pre-existing reference to the insertion position that was issued before INSERT committed?

What constraints on INSERT are necessary to ensure that two non-overlapping INSERTs into the same document commute observably?

What invariants must INSERT into a link subspace preserve, given that the link subspace's V-positions need not be contiguous?
