# ASN-0090: DELETE Operation

*2026-05-24*

We are asking what changes when content is removed from a position in a document. The naive answer — "take the content out" — collapses two operations Nelson took pains to separate. We must say what is *not* destroyed (because Xanadu's content store is append-only and permanence is unconditional), what is *vacated* (the V-position itself, with no marker, no scar), what *shifts* (because the Vstream tolerates no gaps), what is *preserved* (every byte's identity, attribution, and accessibility through history and through other documents), and what it means for this to be a single observable event.

Nelson's specification at [LM 4/66] is again one sentence: "This removes the given span from the given document." The verb "removes" hides what does *not* happen. It does not destroy bytes — those persist in the Istream. It does not affect other documents that include the same bytes by transclusion. It does not break links pointing into the removed region. It does not change the document's identity. The sentence is small because Xanadu's architecture pre-discharges the obligations a destructive deletion would impose. Our task is to recover those discharged obligations and state them as named, verifiable claims.

## Foundation setting

We work in the foundation state introduced by ASN-0036 and ASN-0093: a content store `Σ.C : T ⇀ Val`, a link store `Σ.L : T ⇀ Endset*`, a document set `dom(Σ.M) ⊆ T`, and per-document arrangements `Σ.M(d) : T ⇀ T`. Foundation invariants we will preserve include S0 (content immutability), S2 (arrangement functionality), S3 (referential integrity), S7 (structural attribution), S8a (V-position well-formedness), S8-depth (per-subspace depth uniformity), S8-fin (arrangement finiteness), D-CTG, D-MIN, D-SEQ (text-subspace contiguity), L0 (subspace partition), L12 (link immutability), and L14 (store disjointness).

We work with the content subspace `s_C = 1` (SubspaceConventionAxiom of ASN-0093). For each document `d`, let `V_1(d) = {v ∈ dom(Σ.M(d)) : subspace(v) = s_C}`. By S8-depth, when `V_1(d)` is non-empty its positions share a common depth `m_C ≥ 2`; by D-SEQ, `V_1(d) = {[1, 1, ..., 1, k] : 1 ≤ k ≤ N}` for some `N ≥ 1`. The shift function `shift(v, n) = v ⊕ δ(n, #v)` is the OrdinalShift of ASN-0034; for a depth-`m` V-position `v`, `shift(v, n)` agrees with `v` on positions `1, ..., m-1` and adds `n` to position `m`. We will need an inverse: when `v_m ≥ n + 1`, `unshift(v, n) := vpos(subspace(v), ord(v) ⊖ δ(n, m-1))` is well-defined and `shift(unshift(v, n), n) = v`.

## The operation signature

We are looking for the minimum input DELETE needs. It needs a target document (to scope the deletion), a position (where the deleted span begins), and a width (how many V-positions to remove). The shape of the width is determined by the foundation, as we will see, but it must be supplied.

**DEL-OP** (operation signature). A DELETE operation is parameterized by a tuple `(d, p, w)` where:

- `d ∈ dom(Σ.M)` — an allocated document;
- `p ∈ V_1(d)` — a V-position in the content subspace, present in `d`'s arrangement;
- `w ∈ T` with `Pos(w)` and `actionPoint(w) ≤ #p` — a width displacement (T12, ASN-0034).

We call `c := w_m` (with `m = #p`) the *deletion width* — the count of V-positions to remove — and `r := p ⊕ w` the *deletion reach*, the first position strictly past the span. Nelson [LM 4/11, Q9] admits deletion of arbitrary contiguous V-ranges down to the individual byte: "All editing operations — INSERT, DELETEVSPAN, REARRANGE, COPY — work at byte-level granularity on the Vstream." There is no minimum unit and no "contribution boundary" that constrains where the span may end.

## Valid deletion spans

We need to constrain `(p, w)` so that the post-state remains coherent. As with INSERT (ASN-0089), the constraint emerges from D-CTG (text-subspace contiguity) and D-SEQ (sequential structure). A deletion that leaves a gap, or that begins outside `V_1(d)`, or that extends past `N`, would violate the foundation.

**DEL-VALID** (valid deletion span). For pre-state `V_1(d) = {[1, 1, ..., 1, k] : 1 ≤ k ≤ N}` at common depth `m_C` (D-SEQ), the span `(p, w)` satisfies:

(a) *Start in the run.* `p = [1, 1, ..., 1, p_m]` for some `p_m ∈ {1, 2, ..., N}` of depth `m_C`.

(b) *Pure ordinal width.* `w = δ(c, m_C)` for some `c ≥ 1`.

(c) *Containment.* `p_m + c − 1 ≤ N`.

Condition (b) is forced. By T12 and the foundation, `actionPoint(w) ≤ #p = m_C`. The reach `r = p ⊕ w` must by D-SEQ have the form `[1, ..., 1, r_m]` if it is to coincide with the boundary of the span being removed. By TumblerAdd, `r` agrees with `p` on positions before `actionPoint(w)`, has `r_{actionPoint(w)} = p_{actionPoint(w)} + w_{actionPoint(w)}`, and copies `w` on positions after. For `r` to be `[1, ..., 1, p_m + w_m]`, the action point must be exactly `m_C` and only position `m_C` of `w` may be nonzero — precisely `δ(c, m_C)` (OrdinalDisplacement, ASN-0034).

Condition (c) is the analog of INSERT's `j ≤ N+1` bound. With `p_m + c − 1 ≤ N`, every V-position in `[p, r)` lies in `V_1(d)`: the span is fully contained in the pre-state arrangement. The boundary case `p_m + c − 1 = N` is the suffix-truncation case (the deletion includes the last V-position); the boundary case `p_m = 1` and `c = N` is the full-content-vacation case. Both are admissible; both must satisfy DEL-VALID for the operation to be well-formed.

A specification could permit `p_m + c − 1 > N` and absorb the excess as a no-op, but doing so adds no semantic content — DELETE on a partial overlap is equivalent to DELETE on `(p, δ(min(c, N − p_m + 1), m_C))`. We adopt full containment as the precondition; partial-overlap callers truncate at the call site.

## What must NOT change: the Istream

We start the discharge of obligations with the one Nelson elevates to architectural status: deletion never destroys content. The first sentence of his answer to question 1 reads:

> Deletion in Xanadu removes content from a document's current arrangement but never destroys the content itself. This is not a policy choice — it is architectural. The system is built so that destruction of content is impossible by design.

The formal content is exact. The pre-state's content store and the post-state's content store coincide *as functions*:

**DEL-ISTREAM** (Istream invariance). `Σ'.C = Σ.C`, equivalently:

`dom(Σ'.C) = dom(Σ.C) ∧ (A a ∈ dom(Σ.C) :: Σ'.C(a) = Σ.C(a))`.

This is strictly stronger than the foundation's S0 (content immutability), which guarantees only that existing entries are preserved across all transitions. DELETE adds nothing to `dom(C)`, removes nothing from `dom(C)`, and changes no value. The append-only Istream of [LM 2/14] is not merely append-only across DELETE — it is *exactly* invariant. The two-stream architecture of [LM 4/9] ("DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions)") names a system state in which Istream content has lost only its current V-addressability, not its existence.

DEL-ISTREAM has consequences we will return to repeatedly: every I-address that was in `dom(C)` before remains in `dom(C)` after, with the same value, with the same origin (S7), referenceable by any link, retrievable by historical backtrack to a pre-deletion version, and visible in any other document that transcludes it.

## What must be vacated

The V-positions in `[p, r)` are removed from `dom(M(d))`. Defining

`X := {v ∈ V_1(d) : p ≤ v < r} = {[1, ..., 1, p_m + j] : 0 ≤ j < c}`,

we have `|X| = c`, the set is non-empty (by `c ≥ 1` and TA-strict, ASN-0034), and every `v ∈ X` is in `dom(M(d))` by DEL-VALID(c) and D-SEQ.

**DEL-VAC** (vacation). `(A v ∈ X :: v ∉ dom(Σ'.M(d)))`.

The vacated positions disappear entirely from the post-state arrangement; no marker, tombstone, or sentinel takes their place. Nelson is unambiguous on question 2:

> The Vstream always forms a dense, contiguous sequence. When content is removed, all subsequent positions shift down to maintain this invariant. There are no placeholders or holes.

And on question 4, the consequence for the reader:

> The current version shows no trace; history reveals everything. The document appears as though the content was never there — *in the current version*.

Vacation is total. The identity of a V-position `v ∈ X` as a position in `d`'s current arrangement is extinguished. The I-address `Σ.M(d)(v)` is not extinguished — DEL-ISTREAM keeps it in `dom(C)` with its value, its origin, its accessibility through historical backtrack, and its arrangement in any other document that transcludes it. But the *V-position* `v` is gone, and the V-address space of `d` has reorganized around its absence.

We pause to draw the distinction Nelson makes between V-deletion and I-deletion. The Vstream operation we are specifying removes a V-position. There is no I-deletion operation in Xanadu — Nelson's design rules it out structurally. From his question 1 answer: "Deletion that destroys content would violate nearly every guarantee the system makes: permanence of addresses, historical backtrack, link survivability, transclusion integrity, and the rights of others who have linked to or transcluded that content." DELETE without further qualification means V-deletion; I-deletion is not part of the transition vocabulary.

## What must shift

The V-positions in `V_1(d)` lying past the reach must move down to close the gap. Let

`R := {v ∈ V_1(d) : v ≥ r} = {[1, ..., 1, k] : p_m + c ≤ k ≤ N}`.

For each `v ∈ R`, define the *shifted image* `unshift(v, c)`. With `v = [1, ..., 1, v_m]` and `v_m ≥ p_m + c ≥ 1 + c > c`, we have `v_m − c ≥ p_m ≥ 1`, so `unshift(v, c) = [1, ..., 1, v_m − c]` satisfies S8a's positivity constraint and is well-defined.

**DEL-SHIFT** (left shift). `(A v ∈ R :: unshift(v, c) ∈ dom(Σ'.M(d)) ∧ Σ'.M(d)(unshift(v, c)) = Σ.M(d)(v))`.

The mapping from V-position to I-address is preserved under the shift. Every I-address reached from `R` in the pre-state remains reached from `unshift(R, c)` in the post-state — via a different V-position, but with the same I-address. Nelson [Q2]:

> If you have 100 bytes and delete bytes 20–30, you now have 89 bytes addressed 1 through 89. The former byte 31 is now at V-address 20.

The positions shift; the content stays. This is the architectural inverse of INS-SHIFT (ASN-0089): INSERT increases V-addresses past the insertion point by the inserted width; DELETE decreases them by the deletion width. In both cases the I-address targets are preserved exactly. The asymmetry between V-addresses ("constantly changing") and I-addresses ("permanent") of [LM 4/11] is the source of both shifts being benign — only the *mutable* coordinate changes, and the *immutable* coordinate carries everything that depends on identity.

The shift map `unshift(·, c) : R → unshift(R, c)` is an order-preserving bijection. Order preservation follows from TA3-strict (ASN-0034): for `v_1, v_2 ∈ R` with `v_1 < v_2`, the last components satisfy `(v_1)_m < (v_2)_m`, hence `(v_1)_m − c < (v_2)_m − c`, hence `unshift(v_1, c) < unshift(v_2, c)`. Injectivity follows by left-cancellation of the underlying tumbler subtraction. Surjectivity onto `unshift(R, c)` is by construction.

## What must be preserved on the left

The V-positions in `V_1(d)` strictly below `p` are left exactly as they were.

`L := {v ∈ V_1(d) : v < p} = {[1, ..., 1, k] : 1 ≤ k < p_m}`.

**DEL-PRESERVE-LEFT** (left preservation). `(A v ∈ L :: v ∈ dom(Σ'.M(d)) ∧ Σ'.M(d)(v) = Σ.M(d)(v))`.

Pre-existing positions strictly below `p` keep their V-position and their I-address target. Their content has not moved in either coordinate. The set `L` is the part of `d`'s arrangement that DELETE leaves entirely undisturbed in the content subspace; together with DEL-FRAME(d) below, it pins down everything within `d` that DELETE does not touch.

When `p_m = 1`, `L` is empty — the deletion begins at the document's first V-position and nothing precedes it. DEL-PRESERVE-LEFT holds vacuously in that case.

## Gap closure: the post-state V-subspace

The three regions `L`, `X`, `R` partition `V_1(d)` in the pre-state. In the post-state, `X` is gone, `R` has been replaced by `unshift(R, c)`, and `L` is intact. We claim that `L` and `unshift(R, c)` together exhaust the post-state's positions in subspace 1.

**DEL-DOMAIN-CLOSURE** (post-state subspace-1 domain).

`V_1(d') = L ∪ unshift(R, c) = {[1, 1, ..., 1, k] : 1 ≤ k ≤ N − c}`.

Direct computation: `L = {[1, ..., 1, k] : 1 ≤ k < p_m}` (last component in `[1, p_m − 1]`), and `unshift(R, c) = {[1, ..., 1, k] : p_m ≤ k ≤ N − c}` (last component in `[p_m, N − c]`). The integer ranges `[1, p_m − 1]` and `[p_m, N − c]` are adjacent and non-overlapping; their union is `[1, N − c]`. By T3 (CanonicalRepresentation, ASN-0034), tumblers with different last components at common depth are distinct, so the two sets are disjoint. The union is `{[1, ..., 1, k] : 1 ≤ k ≤ N − c}` — again a contiguous initial segment of the form prescribed by D-SEQ, now with `N − c` in place of `N`.

This is the formal content of Nelson's "no placeholders, no scars" guarantee. A reader of `Σ'.M(d)` cannot detect from the post-state alone that a DELETE occurred. The V-positions present are `{[1, ..., 1, k] : 1 ≤ k ≤ N − c}`, indistinguishable in shape from a document that always had `N − c` content positions. From [Q4]:

> The document appears as though the content was never there — but only to a reader who looks at nothing but the present.

The historical fact of the deletion is recoverable only from external version history. The DELETE operation itself does not preserve a record of `(p, w)` in the current state; that obligation falls on whatever version mechanism layers above DELETE (out of scope here). What DELETE provides is parameters `(p, w)` that *can be logged* by a surrounding versioning system to make backtrack possible. Nelson's question 6 answer makes this division explicit: "The boundaries are not stored as separate 'deletion records' — they are implicit in the difference between the pre-deletion and post-deletion Vstream mappings, both of which the system retains" — the retention is the version system's job, not DELETE's.

The full-content-vacation boundary case (`p_m = 1`, `c = N`) gives `V_1(d') = ∅`. The post-state has an empty content subspace in `d`. We will return to this case under invariant preservation.

## What must NOT change: the frame

The state components DELETE leaves alone are:

**DEL-FRAME** (frame conditions). For the transition `Σ → Σ'` realizing `DELETE(d, p, w)`:

(a) *Content store.* `Σ'.C = Σ.C` (DEL-ISTREAM, restated for completeness).

(b) *Link store.* `Σ'.L = Σ.L` (link store domain and values unchanged).

(c) *Document set.* `dom(Σ'.M) = dom(Σ.M)` (no documents added or removed).

(d) *Cross-subspace within `d`.* `(A S' ≠ s_C, v : v ∈ dom(Σ.M(d)) ∧ subspace(v) = S' : v ∈ dom(Σ'.M(d)) ∧ Σ'.M(d)(v) = Σ.M(d)(v))`.

(e) *Cross-document.* `(A d' ∈ dom(Σ.M) : d' ≠ d : Σ'.M(d') = Σ.M(d'))`.

(f) *Origin permanence.* `(A a ∈ dom(Σ.C) :: origin'(a) = origin(a))`.

Clause (a) is DEL-ISTREAM; we restate it here for the completeness of the frame. Clause (b) extends invariance to the link store: DELETE on text-subspace V-positions does not touch any link's address or value. By L12 (link immutability), this clause is implied by the structure of any conforming transition — we name it explicitly because the consultation evidence repeatedly turns on it. From [Q5]:

> Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end. [LM 4/43]

The link store survives DELETE not because DELETE "cleans up" anything in `L`, but because DELETE does not touch `L` at all. The endset spans that some link's values contain may, in the post-state, resolve to different V-positions (because the V-positions have shifted), but the link itself — its address, its value, its endset structure — is byte-identical.

Clause (c) names the identity-preservation Nelson asserts in answer to question 7: "The document retains its identity after a removal." DELETE modifies `Σ.M(d)` for a single `d`; it allocates no new documents (which would extend `dom(M)`) and removes no documents (which would contradict ASN-0093's M1, ArrangementMonotonicity). The address `d` is the same tumbler before and after. From [LM 2/14]:

> A document is really an evolving ONGOING BRAID. Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted.

Editing is re-twisting the braid, not cutting and starting a new one.

Clauses (d) and (e) are the subspace and document frame conditions. Clause (d) reflects that subspace `s_C` and subspace `s_L` are independent partitions of `dom(M(d))`: a DELETE in the content subspace does not shift link-subspace V-positions, does not vacate any link-subspace position, does not change which link addresses are arranged at which link-subspace positions. Clause (e) is the cross-document independence of [Q3]:

> Each document's Vstream is independent. Editing one document's arrangement — inserting, deleting, rearranging — changes only that document's V-to-I mapping. No other document's mapping is affected.

The two-stream architecture forces this. Other documents' arrangements are functions over their own V-positions, and DELETE on `d` modifies only `d`'s function. The case that most reveals the depth of (e) is transclusion: if `d` and `d'` both reference some `a ∈ dom(C)` at V-positions `v ∈ dom(M(d))` and `v' ∈ dom(M(d'))`, and DELETE on `d` vacates `v`, then `d'`'s reference at `v'` is unchanged — `a` remains in `dom(C')` (by (a)) and `v' ∈ dom(M'(d'))` with `Σ'.M(d')(v') = a` (by (e)). The transclusion survives.

Clause (f) is the origin-permanence claim. The origin function `origin(a) = N(a).0.U(a).0.D(a)` (S7, ASN-0036) projects the document-level prefix from a content address's structural form. Since `dom(C)` is unchanged and every address's structural form is intrinsic (T8, ASN-0034 — addresses are immutable tumblers), the origin of every content address is invariant under DELETE. From [Q5]:

> Attribution is the address. It cannot be stripped without destroying the addressing system itself.

In particular, for any `a` that was referenced from the vacated region `X` and is *no longer* referenced from `d`, `origin(a)` is still `d`. The address remembers who created it even after the creator's current arrangement has removed it.

## Identity preservation: the architectural commitment

The frame conditions above are individually verifiable surface obligations. They derive from a deeper commitment that Nelson states as the architectural inversion of conventional editing systems [LM 2/14]:

> Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version.

Xanadu rejects this. DELETE in Xanadu is a Vstream-only operation: the Istream is permanent, identities are permanent, links are permanent, attributions are permanent. We capture the synthesis as a single identity claim that subsumes the frame conditions and serves as the load-bearing architectural commitment.

**DEL-IDENTITY** (permanent identity preservation). For every pre-state I-address `a ∈ dom(Σ.C)`:

(a) *Address persistence.* `a ∈ dom(Σ'.C)`.

(b) *Value preservation.* `Σ'.C(a) = Σ.C(a)`.

(c) *Origin permanence.* `origin'(a) = origin(a)` (a is forever attributed to the document that created it, even if no V-position in any current arrangement still references it).

(d) *Cross-document reference preservation.* For every `d' ≠ d` and every `v' ∈ dom(Σ.M(d'))` with `Σ.M(d')(v') = a`: `v' ∈ dom(Σ'.M(d'))` and `Σ'.M(d')(v') = a` (any other document's reference to `a` is unchanged).

(e) *Link reference preservation.* For every `ℓ ∈ dom(Σ.L)` and every endset `eᵢ` of `Σ.L(ℓ)` whose coverage includes `a`: `ℓ ∈ dom(Σ'.L)`, `Σ'.L(ℓ) = Σ.L(ℓ)`, and the endset eᵢ still covers `a` (any link's reference to `a` is unchanged).

(f) *Historical reachability.* For any V-position `v ∈ dom(Σ.M(d))` with `Σ.M(d)(v) = a` that is vacated by DELETE (i.e., `v ∈ X`): a version system layered above DELETE can reconstruct `(v, a) ∈ Σ.M(d)` from the pre-state, given the operation parameters `(p, w)`.

Clauses (a) and (b) are DEL-ISTREAM unpacked over a specific address. Clause (c) follows from S7's structural-attribution discipline applied to the unchanged content store. Clause (d) is DEL-FRAME(e) applied to a specific cross-document reference. Clause (e) is DEL-FRAME(b) applied to a specific link.

Clause (f) is more subtle. It says that DELETE does not by itself preserve the pre-state — the *current* state after DELETE is `Σ'`, which does not contain the vacated `(v, a)` pair. Reconstruction of `(v, a)` requires (i) the operation parameters `(p, w)` and (ii) the surviving post-state `Σ'.M(d)`. Given these, a version system reconstructs the pre-state mapping by:

- Restoring `L = {v ∈ V_1(d') : v ≤ [1, ..., 1, p_m − 1]}` from `Σ'.M(d)` unchanged.
- Identifying the vacated positions `X = {[1, ..., 1, p_m + j] : 0 ≤ j < c}` from `(p, w)`.
- Recovering each vacated I-address `a_j = Σ.M(d)([1, ..., 1, p_m + j])` from version-system storage (an external commitment).
- Restoring `R = {shift(v, c) : v ∈ unshift(R, c) ⊆ V_1(d')}` from the post-state's surviving above-`p` positions.

The historical-reachability clause is what makes Nelson's [LM 2/15] guarantee hold: "When you ask for a given part of a given version at a given time, it comes to your screen." DELETE preserves the *recoverability* of `(v, a)` even though it does not preserve `(v, a)` itself in the current state. The mechanism is the version system; the obligation on DELETE is to make recovery possible — by leaving `dom(C)` intact (so the I-addresses remain), by accepting parameters that fully characterize the operation (so the version system has what it needs), and by being deterministic (so the post-state can be checked against the pre-state plus parameters).

DEL-IDENTITY is the architectural commitment that distinguishes Xanadu DELETE from destructive deletion in any conventional system. A destructive DELETE could honor DEL-VAC, DEL-SHIFT, DEL-PRESERVE-LEFT, and DEL-DOMAIN-CLOSURE perfectly while violating every clause of DEL-IDENTITY — by removing `a` from `dom(C)`, by losing the origin attribution, by breaking links pointing into `a`, by leaving transcluded references dangling. Xanadu DELETE rules these out structurally. The Istream and the link store are *not* sites where DELETE may act; they are sites where DELETE must abstain.

## Atomicity

The "canonical order" requirement Nelson articulates at [LM 1/34] applies to DELETE as it does to INSERT.

**DEL-ATOM** (atomic transition). DELETE is observable as a single state transition `Σ → Σ'`. The post-state satisfies DEL-VAC, DEL-SHIFT, DEL-PRESERVE-LEFT, DEL-DOMAIN-CLOSURE, DEL-FRAME, and DEL-IDENTITY, together with every foundation invariant carried forward. No state `Σ_mid` is observable between `Σ` and `Σ'` in which any of these conditions partially holds.

An implementation may decompose DELETE into multiple internal steps — slicing partial blocks at the span boundaries, freeing vacated mapping nodes, shifting surviving block start positions, possibly compacting the resulting structure — but no external observer (any operation that reads state) may witness an intermediate state. Equivalently, DELETE either fully commits or has no effect; the post-state is one in which all conditions hold simultaneously.

The implementation evidence (Gregory's question 11 answer) makes the decomposition vivid: the operation constructs two "knife" cut points at `p` and `r`, slices any mapping blocks that the knives fall interior to, frees the entirely-within-range blocks, and shifts the displacement of the entirely-past-range blocks. From the abstract perspective, this is a single transition; from the implementation perspective, it is a sequence of internal steps with a single commit point. DEL-ATOM constrains the external observability, not the internal trajectory.

## Invariant preservation

We verify that the foundation invariants survive DELETE. For each invariant, we identify what discharges its preservation.

| Invariant | Source | Discharged by |
|-----------|--------|---------------|
| P0 (content permanence) | ASN-0093 | DEL-FRAME(a) |
| P1 (entity permanence) | ASN-0047 | DEL-FRAME(c) |
| S0 (content immutability) | ASN-0036 | DEL-FRAME(a) (strictly stronger: exact equality) |
| S2 (arrangement functionality) | ASN-0036 | Disjoint-domain argument, below |
| S3 (referential integrity) | ASN-0036 | Surviving mappings target I-addresses that remain in `dom(C')` by DEL-FRAME(a) |
| S7 (structural attribution) | ASN-0036 | DEL-FRAME(f); origin function is intrinsic to the address |
| S8a (V-position well-formedness) | ASN-0036 | Preserved positions unchanged; shifted positions have last-component `v_m − c ≥ p_m ≥ 1`, other components 1 |
| S8-depth (per-subspace depth uniformity) | ASN-0036 | All post-state subspace-1 positions have depth `m_C`; other subspaces unchanged |
| S8-fin (arrangement finiteness) | ASN-0036 | `|dom(Σ'.M(d))| = |dom(Σ.M(d))| − c`, still finite |
| D-CTG (text-subspace contiguity) | ASN-0036 | DEL-DOMAIN-CLOSURE: `V_1(d') = {[1, ..., 1, k] : 1 ≤ k ≤ N − c}`, contiguous |
| D-MIN (minimum position) | ASN-0036 | If `p_m > 1` then `[1, ..., 1, 1] ∈ L ⊆ V_1(d')`; if `p_m = 1` then either `c < N` (`unshift([1, ..., 1, c+1], c) = [1, ..., 1, 1] ∈ V_1(d')`) or `c = N` (`V_1(d') = ∅`, D-MIN vacuous) |
| D-SEQ (sequential structure) | ASN-0036 | Derived from D-CTG ∧ D-MIN ∧ S8-fin ∧ S8-depth |
| L0 (subspace partition) | ASN-0093 | DEL-FRAME(a, b): no addresses added to `C` or `L` |
| L12 (link immutability) | ASN-0043 | DEL-FRAME(b): `Σ'.L = Σ.L` |
| L14 (store disjointness) | ASN-0093 | DEL-FRAME(a, b): both stores' domains unchanged, pre-existing disjointness preserved |
| C-fin (content store finiteness) | ASN-0093 | DEL-FRAME(a): `dom(Σ'.C) = dom(Σ.C)`, still finite |
| L-fin (link store finiteness) | ASN-0093 | DEL-FRAME(b): `dom(Σ'.L) = dom(Σ.L)`, still finite |

The S2 discharge requires the same care as for INSERT. We decompose `Σ'.M(d)` (restricted to subspace 1) as the union of two partial functions:

- `M_L := {(v, Σ.M(d)(v)) : v ∈ L}` — the preserved-left mapping;
- `M_S := {(unshift(v, c), Σ.M(d)(v)) : v ∈ R}` — the shifted mapping.

The domains:

- `dom(M_L) = {[1, ..., 1, k] : 1 ≤ k < p_m}` — last component in `[1, p_m − 1]`;
- `dom(M_S) = {[1, ..., 1, k] : p_m ≤ k ≤ N − c}` — last component in `[p_m, N − c]`.

The integer ranges `[1, p_m − 1]` and `[p_m, N − c]` are pairwise disjoint (they share no integer, since one ends at `p_m − 1` and the other begins at `p_m`). By T3, tumblers with different last components at common depth are distinct, so the two domains are disjoint. The union of two functions with disjoint domains is a function: S2 holds.

The S8a discharge for shifted positions: `unshift(v, c)` with `v = [1, ..., 1, v_m]` and `v_m ≥ p_m + c` gives `unshift(v, c) = [1, ..., 1, v_m − c]` with last component `v_m − c ≥ p_m ≥ 1`, all other components 1, depth `m_C ≥ 2`, no zeros. S8a is satisfied.

The boundary case `c = N` (full content vacation) deserves attention. The post-state has `V_1(d') = ∅`. D-MIN holds vacuously (its predicate `V_1(d) ≠ ∅` is false). D-SEQ holds vacuously (the existential `(E n ≥ 1 : V_1(d) = {[1, ..., 1, k] : 1 ≤ k ≤ n})` is replaced by `V_1(d) = ∅`, the boundary of the schema). D-CTG holds vacuously. Subsequent INSERTs into `d` follow ASN-0089's empty case: the depth `m_C` is chosen, the first new position is `[1, ..., 1]` of that depth. From the foundation's perspective, the post-state of a full-vacation DELETE is observationally identical to a never-populated content subspace — the foundation does not distinguish "empty by birth" from "empty by deletion" within the current arrangement, only through historical backtrack.

## What DELETE is not

We close with the distinctions Nelson's design forces, parallel to the closing distinctions of INSERT.

DELETE is not content destruction. Content destruction would remove I-addresses from `dom(C)`, contradicting DEL-ISTREAM. From [Q1]: "There is no operation in Xanadu that can sever attribution." DELETE removes the V-position; the content is not destroyed.

DELETE is not the inverse of INSERT in the strict algebraic sense. INSERT allocates fresh I-addresses (INS-ALLOC); DELETE vacates V-positions but leaves the I-addresses in `dom(C)`. The composition `DELETE(d, p, w); INSERT(d, p, values)` does not recover the pre-state's I-addresses — INSERT allocates new ones. From [LM 2/14]'s braid metaphor, the braid is being re-twisted; the bytes that were in one position are not the bytes that come back when new content is inserted at that position. To recover identical I-addresses requires version-system mechanisms (CREATENEWVERSION, transclusion), not the editing operations themselves.

DELETE is not transclusion-aware. The operation is local to `d`'s arrangement. It does not check whether vacated V-positions reference I-addresses that are also referenced from other documents; it does not, for instance, refuse to vacate positions that participate in transclusions. The cross-document independence of DEL-FRAME(e) makes such checks unnecessary: other documents' transclusions are unaffected by DELETE on `d` regardless of whether `d`'s vacated positions overlap with theirs.

DELETE is not a permission-protected operation in any sense the foundation specifies. Nelson [Q8] explicitly disclaims region-level permissions: "There are no permissions granted on regions of documents. A document is either private (owner and designees) or published (everyone). That is the entire access model." DELETE proceeds whenever DEL-VALID holds; access control is layered above and is not part of this ASN.

DELETE on a span containing zero V-positions is not admitted as a no-op. DEL-VALID requires `c ≥ 1`, ruling out empty deletions. A specification could admit `c = 0` as a no-op, but the abstract semantics gain nothing — a caller who needs "delete zero positions" simply does not call DELETE. We adopt `c ≥ 1` as a hard precondition to preserve the operational meaning of "removing content."

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| DEL-OP | DELETE operation signature: tuple `(d, p, w)` with `d ∈ dom(M)`, `p ∈ V_1(d)`, `Pos(w)`, `actionPoint(w) ≤ #p` | introduced |
| DEL-VALID | Valid deletion span: `p = [1, ..., 1, p_m]` with `1 ≤ p_m ≤ N`, `w = δ(c, m_C)` with `c ≥ 1`, and containment `p_m + c − 1 ≤ N` | introduced |
| DEL-ISTREAM | `Σ'.C = Σ.C` exactly (domain and values both invariant) | introduced |
| DEL-VAC | `(A v ∈ X :: v ∉ dom(Σ'.M(d)))` where `X = [p, r) ∩ V_1(d)` | introduced |
| DEL-SHIFT | `(A v ∈ R :: unshift(v, c) ∈ dom(Σ'.M(d)) ∧ Σ'.M(d)(unshift(v, c)) = Σ.M(d)(v))` | introduced |
| DEL-PRESERVE-LEFT | `(A v ∈ L :: v ∈ dom(Σ'.M(d)) ∧ Σ'.M(d)(v) = Σ.M(d)(v))` | introduced |
| DEL-DOMAIN-CLOSURE | `V_1(d') = L ∪ unshift(R, c) = {[1, ..., 1, k] : 1 ≤ k ≤ N − c}` | introduced |
| DEL-FRAME | Six clauses: content store, link store, document set, other subspaces of `d`, other documents, origin permanence | introduced |
| DEL-IDENTITY | Permanent identity preservation: every pre-existing I-address persists with its value, its origin, its cross-document references, and its link references; vacated V→I pairs remain reconstructable by version-system mechanisms given operation parameters | introduced |
| DEL-ATOM | DELETE is a single observable state transition; no intermediate state in which the operation has partially committed is observable | introduced |

## Open Questions

What must DELETE guarantee about the V-position-to-I-address mapping for vacated V-positions, given that the I-addresses remain in `dom(C)` but no current arrangement entry recovers the original V-position?

What additional invariants must DELETE preserve when applied to a document that is concurrently the source of a transclusion held by another document, and how do these invariants relate to DEL-FRAME(e)?

Under what structural conditions on two deletion spans does sequential composition of DELETE operations equal a single DELETE on a combined span, and under what conditions does it not?

What does DELETE guarantee about the resolvability of a link whose endset coverage includes I-addresses associated with V-positions that DELETE vacates from the link's home document?

What must DELETE guarantee for I-addresses that, after the operation, are referenced from no V-position in any arrangement — must they remain enumerable through some structural means, or are they permitted to become unreachable in the current state?

What invariants must DELETE preserve when applied to a subspace whose foundation invariants permit non-sequential V-position structure, distinct from the content subspace's D-SEQ form?

What constraints must DELETE respect to ensure that two non-overlapping DELETEs on disjoint spans of the same document commute observably?
