# ASN-0069: CREATENEWVERSION Operation

*2026-05-25*

We are looking for the precise effect of forking a document into a new version. A user has a document; they want a starting point for something different. They do not want to lose what is already there, do not want to duplicate the bytes, and do not want every subsequent reader to have to ask which of two textually identical fragments is "the real one." The operation we are deriving must give them a *new document* that begins where the source stands, while leaving the source untouched and the storage unchanged.

The temptation is to read the operation as a copy, and Nelson is emphatic that this is the wrong frame:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

The word *inclusion* is load-bearing. The new document does not contain a fresh stock of bytes; it contains *references to existing bytes*. The bytes have permanent addresses, and the new document arranges those addresses into its own V-stream. What is shared is structural — same I-addresses, same origin attribution, same link survivability. What is independent is the arrangement: edits on either side change one mapping and leave the other intact.

This ASN derives the operation as a state transition. The substrate is the system state `Σ = (C, L, E, M, R)` of ASN-0047, with `C : T ⇀ Val` the content store, `L : T ⇀ Link` the link store, `E ⊆ T` the entity set, `M(d) : T ⇀ T` the arrangement of each document, and `R ⊆ T × E_doc` the provenance relation. The operation creates a new document entity and populates its arrangement; the content store grows by nothing.

## What Must Be Constructed

The fork operation produces a new document `d_new` from a source document `d_src ∈ E_doc`. Three things are needed and only three:

(a) *An identity for `d_new`.* A fresh tumbler in `E_doc`, distinct from every existing entity but bearing a structural relationship to `d_src`.

(b) *An arrangement for `d_new`.* A new partial function `M'(d_new) : T ⇀ T` whose image lies in `dom(C)` — referencing existing content, not allocating new content.

(c) *A provenance record.* For every I-address appearing in `M'(d_new)`, a witness `(a, d_new) ∈ R'` recording that `d_new` now contains `a`.

The first is supplied by entity creation; the second by arrangement extension; the third by provenance recording. The vocabulary of ASN-0047 names these K.δ (case (ii) with `k = 1` for the first fork of `d_src`, `k = 0` for subsequent forks — both consistent with `A_v(d_src)`'s chain-advancement convention), K.μ⁺ (arrangement extension), and K.ρ (provenance recording — invoked once per inherited I-address). The fork composite is exactly the sequencing of these elementary steps.

The composite is J4 of ASN-0047, named *ForkComposite*. We adopt it as the structural skeleton and derive from first principles what it guarantees, what it forbids, and what it leaves to the source-fork relationship.

J4 distinguishes two operands. The *identity source* is `d_src` — the document being forked, fixed by V0's precondition. The *content source operand* `d_op` is the document whose content-subspace arrangement is transcribed into `d_new`; J4's operand-tracking rule fixes it by sub-case:

- *First fork of `d_src`* (when `A_v(d_src)` has emitted no prior version): `d_new = inc(d_src, 1)` and `d_op = d_src`.
- *Subsequent fork of `d_src`* (when `A_v(d_src)` already has a frontier): `d_new = inc(d_prev, 0)` and `d_op = d_prev = max(dom(A_v(d_src)))` — the most recent prior emission of `d_src`'s version sub-allocator.

The two operands coincide on a first fork (`d_op = d_src`) and diverge on a subsequent fork, where `d_op` is the prior version, not the original source. J4's precondition for the non-empty branch is `d_src ∈ E_doc ∧ d_op ∈ E_doc ∧ V_{s_C}(d_op) ≠ ∅`. Most of this ASN's narrative and the worked example treat the first fork, where `d_op = d_src`; the content-inheritance claims below are stated against `d_op` so that they remain correct for subsequent forks, and reduce to the `d_src` reading when `d_op = d_src`.

## Identity by Sub-Allocation

We begin with `d_new`. The system already has an apparatus for allocating tumblers under the version sub-allocator of `d_src`: T10a's allocator discipline and ASN-0047's K.δ. For a document's versions, the producing allocator is `A_v(d_src)` (ASN-0047's Allocator hierarchy), which emits its first output via K.δ case (ii) at `k = 1` — `inc(d_src, 1)`, by TA5(d) appending a single non-zero component — and emits each subsequent output via K.δ case (ii) at `k = 0` — `inc(d_prev, 0)`, by TA5(c) preserving length while advancing the trailing component. We establish `Document(d_new)` in both cases by induction on `A_v(d_src)`'s emission count. K.δ-ID.zeros-0/1 (ASN-0047) preserves zeros at both `k = 0` and `k = 1`, but preservation alone does not establish `zeros(d_new) = 2`; the induction supplies the input value `zeros(input) = 2` that K.δ-ID.zeros-0/1 then carries through.

*Base case (first fork).* `zeros(d_src) = 2` because `d_src ∈ E_doc` (V0's precondition). K.δ-ID.zeros-0/1 at `k = 1` gives `zeros(d_new) = zeros(d_src) = 2`, hence `Document(d_new)`.

*Inductive step (subsequent fork).* The induction hypothesis is that `A_v(d_src)`'s most recent prior emission `d_prev` satisfies `Document(d_prev)`, so `zeros(d_prev) = 2`. `d_prev ∈ E_doc` is preserved across all intermediate states by P1 (entity permanence, ASN-0047) applied to its prior K.δ event, so `d_prev ∈ E_doc` at the state of the current fork. K.δ-ID.zeros-0/1 at `k = 0` then gives `zeros(d_new) = zeros(d_prev) = 2`, hence `Document(d_new)`. ∎

We establish `parent(d_new) = parent(d_src)` by the same form of induction on `A_v(d_src)`'s emission count. K.δ-ID.parent-0/1 (ASN-0047) supplies the per-step relation `parent(inc(t, k)) = parent(t)` for `k ∈ {0, 1}`; the induction chains this per-step preservation across `A_v(d_src)`'s emission count to recover `parent(d_src)` from any emission. The first-emission step uses `k = 1` and reaches `parent(d_src)` directly; each subsequent sibling-stream step uses `k = 0` and reaches `parent(d_prev)`, which the inductive hypothesis identifies with `parent(d_src)`.

*Base case (first fork).* `d_new = inc(d_src, 1)`. K.δ-ID.parent-0/1 at `k = 1` gives `parent(d_new) = parent(d_src)` directly.

*Inductive step (subsequent fork).* The induction hypothesis is that `A_v(d_src)`'s most recent prior emission `d_prev` satisfies `parent(d_prev) = parent(d_src)`. The current emission is `d_new = inc(d_prev, 0)`. K.δ-ID.parent-0/1 at `k = 0` gives `parent(d_new) = parent(d_prev)`. Composing with the induction hypothesis: `parent(d_new) = parent(d_prev) = parent(d_src)`. ∎

We make explicit:

> **V1** (*new-version identity*): A fork of `d_src` produces a new entity `d_new` allocated as `A_v(d_src)`'s next emission per the Allocator hierarchy (ASN-0047):
>
> - *First fork of `d_src`* (when `A_v(d_src)` has emitted no prior version): `d_new = inc(d_src, 1)`, produced by K.δ case (ii) with `k = 1`, `t = d_src`.
> - *Subsequent fork of `d_src`* (when `A_v(d_src)` has prior emissions with most recent `d_prev`): `d_new = inc(d_prev, 0)`, produced by K.δ case (ii) with `k = 0`, `t = d_prev`.
>
> In either case `d_new ∈ E'_doc`, `d_new ∉ E_doc` (pre-fork), `Document(d_new)` (by the Document induction above on `A_v(d_src)`'s emission count, which combines K.δ-ID.zeros-0/1's zero-preservation at `k = 0` and `k = 1` with P1-supplied membership `d_prev ∈ E_doc` at every inductive step), and `parent(d_new) = parent(d_src)` (by the parent-equality induction above on `A_v(d_src)`'s emission count, which combines K.δ-ID.parent-0/1's per-step preservation at `k ∈ {0, 1}` with the inductive hypothesis `parent(d_prev) = parent(d_src)` at every subsequent-emission step). The new entity inherits the source's account-level prefix while extending into a fresh sub-tumbler.

V1 instantiates J4's allocation-and-operand-tracking rule directly — the `k = 1` branch on a first fork, the `k = 0` branch on a subsequent fork; the one deviation, literal inheritance, is V4.

Two consequences follow without further machinery.

*Structural ancestry.* J4 (ASN-0047) supplies `d_src ≼ d_new` directly as a derived consequence in both sub-cases (`d_src ≼ inc(d_src, 1)` on a first fork, `d_src ≼ inc(d_prev, 0)` on a subsequent fork). We name this consequence so that downstream users of the operation can rely on it as a structural property of the operation itself, not as a metadata field that could fall out of sync.

> **V2** (*prefix-encoded ancestry*): `d_src ≼ d_new` under the tumbler prefix order. The ancestry relationship is recoverable from `d_new`'s tumbler alone by truncating the trailing extension component; no separate lineage table is consulted.

*Address uniqueness.* The producing allocator of `inc(d_src, 1)` is the *version sub-allocator* `A_v(d_src)` defined in ASN-0047's Allocator hierarchy — not the document sub-allocator of any account. By the hierarchy definition, `A_v(d_src)` is associated with `d_src` itself and produces its first emission `inc(d_src, 1)`, with subsequent emissions `inc(prev_version, 0)`. By T10a.6 (DomainDisjointness, ASN-0034), `A_v(d_src)`'s domain is disjoint from every other allocator's domain. The K.δ precondition `e ∉ E` (uniformly required for all sub-cases) forces `d_new` to be a fresh tumbler. No future fork — of `d_src` or any other document — can re-use this address. Combined with T8 (AllocationPermanence, ASN-0034), once `d_new` enters `E`, it remains in `E` for all subsequent reachable states. The identity is permanent.

The identity argument is structurally independent of content inheritance, correspondence, and isolation. K.δ creates an empty-arrangement document; the fork's arrangement starts empty (the `Document(e)` effect clause of K.δ sets `M'(d_new) = ∅`).

An alternative implementation could fork by performing only K.δ and producing an empty new document. That would satisfy V1, V2, and the basic identity guarantees. What that implementation would *lack* is the inherited content that makes the fork meaningfully a *version of* something.

## Sharing, Not Duplication

The K.μ⁺ phase populates `M'(d_new)`. The question is what V-to-I mappings it installs. There are two candidate disciplines:

- *Duplication.* For every `v ∈ V_{s_C}(d_op)`, allocate a fresh I-address `a' ∈ dom(C')` with `C'(a') = C(M(d_op)(v))`, and set `M'(d_new)(v') = a'` for a corresponding fresh V-position `v'`.

- *Transclusion.* For every `v ∈ V_{s_C}(d_op)`, set `M'(d_new)(v') = M(d_op)(v)` directly — the same I-address that `d_op`'s arrangement holds.

The duplication discipline contradicts Nelson's central design commitment. It produces two distinct I-addresses for the same byte, severing the connection to origin: `origin(a') = d_new` rather than `origin(a)`, and the system has no way to recognize the fragment as derived from `d_src`. Royalty splits collapse; link survivability fails; intercomparison cannot distinguish "derived from" from "happened to look the same." Most concretely, duplication forces a K.α step for every byte, which the foundation's J0 (AllocationPlacementCoupling, ASN-0047) requires to be paired with placement, but which produces an extensional state that no longer agrees with the source on identity.

Transclusion preserves identity. The new arrangement references the source's I-addresses; the content store grows by nothing. Every property that depends on I-address identity — origin attribution (S7, ASN-0036), link discoverability via shared addresses, royalty distribution, version intercomparison — is automatic.

J4's defining clause makes the discipline explicit:

> "(ii) K.μ⁺ populating `M'(d_new)` via the unique order-preserving bijection `φ : V_{s_C}(d_op) → V_{s_C}(d_new)`: `(A v ∈ V_{s_C}(d_op) :: M'(d_new)(φ(v)) = M(d_op)(v))`. Derived consequence: `ran(M'(d_new)) = ran(M(d_op)|_{V_{s_C}(d_op)})` — no new content addresses are introduced, every target lies in the pre-existing content store." [ASN-0047 J4]

We promote the content-sharing consequence to a named property:

> **V3** (*content-store invariance*): A fork produces no new content. `C' = C` and `dom(C') = dom(C)`.

The derivation is mechanical. By the elementary decomposition of the fork composite into K.δ + K.μ⁺ + K.ρ (and, in the empty case, just K.δ), no step allocates content. K.δ's frame condition includes `C' = C`; K.μ⁺'s frame condition includes `C' = C`; K.ρ's frame condition includes `C' = C`. By the conjunction of these elementary frames, the composite preserves `C`.

The consequence is that I-address allocation is unaffected by forking. The content sub-allocator of `d_src` (`A_C(d_src)` of ASN-0047) does not advance; its next emission after a fork is the same tumbler as before the fork. The content sub-allocator of `d_new` is freshly activated by K.δ (SubAllocatorBundle, ASN-0047) and stands at its first emission, ready for future K.α invocations into `d_new`.

> **V3a** (*allocation invariance*): For every document `d'`, the set of I-addresses allocated under `d'` is unchanged by forking: `{a ∈ dom(C') : origin(a) = d'} = {a ∈ dom(C) : origin(a) = d'}`. *Derivation.* `dom(C') = dom(C)` by V3; the origin function depends only on the I-address (S7, ASN-0036). ∎

We observe an implementation distinction worth recording. Gregory's `docreatenewversion` allocates fresh POOM nodes for the new version's V→I mapping tree, deep-copying the tree structure (consultation answer 10). The POOM is a representation of the partial function `M`, not the function itself. Two distinct trees representing the same partial function are *the same M* by S2 (ArrangementFunctionality, ASN-0036) — functional equality is by graph. The deep-copy versus shared-tree question is internal to the implementation of `M`; the abstract claim — V3 — is the same either way. An alternative implementation could share tree structure with copy-on-write and still satisfy V3 unchanged.

## The Arrangement Layer

We now characterize `M'(d_new)`. The fork populates it from `d_op`'s content-subspace arrangement — `d_op` being the content source operand fixed by J4: `d_src` on the first fork, the prior version `d_prev` on a subsequent fork.

Let `V_{s_C}(d) = {v ∈ dom(M(d)) : subspace(v) = s_C}` denote the content-subspace V-positions of `d` (ASN-0047). By D-SEQ★ (ASN-0047), when `V_{s_C}(d_op) ≠ ∅`, `V_{s_C}(d_op) = {[s_C, 1, ..., 1, k] : 1 ≤ k ≤ n_{s_C}}` for some `n_{s_C} ≥ 1`, with all positions sharing a common depth `m_{s_C}` (S8-depth, ASN-0036).

The fork installs the content source's content-subspace V-positions and their I-addresses into `M'(d_new)`. The discipline we commit to here — *literal inheritance*: the same V-positions and the same I-addresses appear in `M'(d_new)` as in `M(d_op)|_{V_{s_C}(d_op)}` — is a design commitment of this ASN, strengthening J4's clause (ii). (J4's clause (ii) installs content via an order-preserving bijection `φ : V_{s_C}(d_op) → V_{s_C}(d_new)`, constraining the *range* of `M'(d_new)` to `ran(M(d_op)|_{V_{s_C}(d_op)})` but leaving the *V-position identity* of the pairing to any such `φ`. Literal inheritance fixes `φ` to be the identity on V-positions — one admissible discipline among several.) We name the commitment as V4 and then derive what follows from it.

> **V4** (*arrangement inheritance — design commitment*): After any fork of `d_src`, the new document's content-subspace arrangement inherits literally from the content source operand `d_op` (`= d_src` on the first fork, `= d_prev` on a subsequent fork):
>
> `(A v ∈ V_{s_C}(d_op) :: v ∈ dom(M'(d_new)) ∧ M'(d_new)(v) = M(d_op)(v))`
>
> V4 holds unconditionally: the formal universal is vacuously true when `V_{s_C}(d_op) = ∅` (V7's empty-source case, where the quantifier ranges over the empty set) and substantively true when `V_{s_C}(d_op) ≠ ∅` (where K.μ⁺ populates `M'(d_new)` from `V_{s_C}(d_op)` per J4's clause (ii)). No precondition on `V_{s_C}(d_op)` is needed.

V4 makes two distinct claims. First, the *V-positions are inherited literally* — the same tumblers `[s_C, 1, ..., 1, k]` appear in both arrangements, not rebased relative to `d_new` (J4's `φ` is the identity). Second, the *I-addresses at each position are inherited literally* — every `M'(d_new)(v)` equals `M(d_op)(v)`, the same I-address the content source holds.

The literal-inheritance form has two structural justifications.

*Why V-positions are not rebased.* V-positions live in the V-coordinate space of a document. They are tumblers in `T`, structured by S8a (zero-count zero, all components positive) and S8-depth (common depth within a subspace). They do not encode the owning document; the owning document is implicit in `M(d)(v)`'s second argument. Rebasing `[s_C, 1, ..., 1, k]` to anything else would (a) require selecting a target depth/subspace identifier scheme for `d_new` that is no longer comparable to `d_op`, and (b) destroy the structural correspondence that V8 below requires.

*Why I-addresses are not rebased.* I-addresses are permanent — by S7 (StructuralAttribution, ASN-0036), every `a ∈ dom(C)` has a unique `origin(a) ∈ E_doc` extractable from its tumbler. Rebasing would require either changing the I-addresses (impossible by P0/S0) or allocating fresh ones with new origins (which is the duplication discipline ruled out above).

For every `v ∈ V_{s_C}(d_op)`, `M(d_op)(v)` is defined (since `v ∈ V_{s_C}(d_op) ⊆ dom(M(d_op))`), and by V4 `M'(d_new)(v)` is defined and equal to it: the same V-position tumbler carries the same I-address in both arrangements.

V4 gives the one-way containment `V_{s_C}(d_op) ⊆ dom(M'(d_new))`. The converse — *no other* V-position enters `dom(M'(d_new))` — follows from the fork composite's elementary decomposition: K.δ initialises `M'(d_new) = ∅` (its effect clause when `Document(e)`); the subsequent K.μ⁺ invocation populates `M'(d_new)` with exactly the positions of `V_{s_C}(d_op)`; K.ρ does not modify arrangements. By the K.μ⁺ amendment (ContentSubspaceRestriction, ASN-0047) — which requires `subspace(v) = s_C` for every new V-position added by K.μ⁺ — together with K.δ's initialisation `dom(M'(d_new)) = ∅` and K.ρ's arrangement-preservation, every position in `dom(M'(d_new))` lies in the content subspace, so:

> **V4b** (*domain equality*): In the post-fork state, `dom(M'(d_new)) = V_{s_C}(d_op)` and `V_{s_C}(d_new) = V_{s_C}(d_op)`. The fork's V-position domain is *exactly* the content source's content-subspace V-position set — not merely a superset.

V4 and V4b together are the structural basis of correspondence.

## Frame: Source Isolation

The fork must not modify `d_src`. This is Nelson's most emphatically stated commitment:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals." [LM 2/45]

The argument is by frame composition. K.δ's frame condition (ASN-0047) states that for all documents other than the one being created, `M'(d') = M(d')`. Since the document being created is `d_new`, every `d' ≠ d_new` retains its arrangement; in particular, `d_src ≠ d_new` (by V1, `d_new ∉ E_doc` pre-fork while `d_src ∈ E_doc` pre-fork), so `M'(d_src) = M(d_src)` across the K.δ step. K.μ⁺'s frame condition states that for all documents other than the one being extended, `M'(d') = M(d')`. The document being extended in J4's clause (ii) is `d_new`, so K.μ⁺ leaves `M(d_src)` unchanged. K.ρ's frame condition is `(A d :: M'(d) = M(d))` — provenance recording does not touch arrangements at all.

The composition: across the entire fork composite, `M(d_src)` is unchanged.

> **V5** (*source isolation*): For every fork composite `Σ →* Σ'`: `M'(d_src) = M(d_src)`.

V5 is foundational to the source-fork relationship. It establishes that the source owner's arrangement is unaffected by anyone else's forking activity. They cannot prevent forking (per Nelson's permissionless publishing contract, when applicable), but they incur no observable side effect.

The frame is bidirectional in a sense V5 does not capture but which we record separately. After the fork, subsequent modifications to `M(d_src)` by `d_src`'s owner do not propagate to `M'(d_new)`, and modifications to `M(d_new)` by `d_new`'s owner do not propagate to `M(d_src)`. Each arrangement is owned by its document's owner, and the K.μ⁺ / K.μ⁻ / K.μ~ / K.μ⁺_L transitions of ASN-0047 modify exactly one document's arrangement per invocation. The same per-target frame discipline applies symmetrically to *any* pair of distinct documents, not only the source-fork pair. We formulate the claim as a per-document, per-sequence property of the arrangement-modifying transition vocabulary.

> **V5a** (*per-document arrangement independence*): Let `K_M = {K.μ⁺, K.μ⁻, K.μ⁺_L}` denote the three arrangement-modifying *elementary* transition kinds of ASN-0047. `K_M` lists only the three elementary kinds; the named composite K.μ~ is handled by decomposition in clause (a). Each member of `K_M` names a unique *target document* `d_target` in its preconditions; we call an elementary transition `Σ → Σ'` *M-targeted at `d_target`* iff it is an instance of some `K ∈ K_M` whose preconditions name `d_target`. Two clauses, one per-step and one per-sequence:
>
> *(a) Per-elementary-transition frame.* For any single elementary transition `Σ → Σ'` and any document `d* ∈ E_doc`: if the transition is M-targeted at some `d_target ≠ d*`, or is any elementary transition that preserves the arrangement of every pre-existing document of `E_doc` (K.α, K.λ, K.ρ unconditionally; K.δ for every `d' ≠ d_new`, which includes every pre-existing `d* ∈ E_doc` since the K.δ outer precondition `e ∉ E` places `d_new ∉ E` pre-step while `d* ∈ E_doc ⊆ E` pre-step), then `M'(d*) = M(d*)`.
>
> *(b) Per-sequence frame.* For any sequence of valid composite transitions `Σ →* Σ'` and any document `d* ∈ E_doc`: if no elementary step of the sequence is M-targeted at `d*`, then `M'(d*) = M(d*)`.
>
> *Derivation.*
>
> *Clause (a).* Each of K.μ⁺, K.μ⁻, K.μ⁺_L (ASN-0047) carries the frame condition `(A d' : d' ≠ d_target : M'(d') = M(d'))` for its named target `d_target`; instantiating at `d' = d*` (admissible because the hypothesis fixes `d_target ≠ d*`) gives `M'(d*) = M(d*)`. The remaining non-arrangement-modifying elementary transitions each carry an `M`-preservation clause covering `d*`: K.α frames `(A d :: M'(d) = M(d))`; K.λ frames `(A d' :: M'(d') = M(d'))`; K.δ frames `(A d' : d' ≠ d_new : M'(d') = M(d'))` for its freshly created `d_new`, and `d_new ≠ d*` because the K.δ outer precondition `e ∉ E` places `d_new ∉ E` pre-step while `d* ∈ E_doc ⊆ E` pre-step; K.ρ frames `(A d :: M'(d) = M(d))`. In every case, `M'(d*) = M(d*)`. *The composite K.μ~* is handled by decomposition rather than as a single elementary step: it expands (ASN-0047) into a K.μ⁻ + K.μ⁺ pair, both M-targeted at the same `d_target`. If `d_target ≠ d*`, each constituent step preserves `M(d*)` by the `K_M` frame above, so the composite does too. Thus every member of ASN-0047's arrangement-modifying vocabulary — the three elementary kinds and the one composite — is covered. ∎(a)
>
> *Clause (b).* Induction on sequence length. *Base* (length 0): `Σ' = Σ` and the conclusion holds trivially. *Step* (`Σ →* Σ_mid → Σ'`): by the induction hypothesis applied to `Σ →* Σ_mid` (no step M-targeted at `d*` by the sequence-level hypothesis), `M_mid(d*) = M(d*)`. The final step `Σ_mid → Σ'` is by assumption either M-targeted at some `d_target ≠ d*` or non-arrangement-modifying; clause (a) applied at this step gives `M'(d*) = M_mid(d*)`. Composing the two equalities: `M'(d*) = M(d*)`. ∎(b)
>
> *Corollary 1 — source–fork isolation.* For `d* = d_src` and any subsequent sequence `Σ' →* Σ''` after the fork in which no step is M-targeted at `d_src`: `M''(d_src) = M'(d_src)`. Symmetric for `d* = d_new`.
>
> *Corollary 2 — pairwise independence.* For any two distinct documents `d¹, d² ∈ E_doc` and any subsequent sequence `Σ' →* Σ''` in which no step is M-targeted at `d¹`: `M''(d¹) = M'(d¹)`. This is V5a(b) instantiated at `d* = d¹`.

## Subspace Selectivity

J4's clause (ii) restricts the inherited arrangement to the *content subspace*: `ran(M'(d_new)) = ran(M(d_op)|_{V_{s_C}(d_op)})`, where `d_op` is the content source operand. The link subspace is excluded. We derive why this must be so abstractly.

The link subspace of any document is governed by CL-OWN (ASN-0047):

> `(A d, v : v ∈ dom(M(d)) ∧ subspace(v) = s_L : origin(M(d)(v)) = d)`

For every V-position in `d`'s arrangement that lies in the link subspace, the I-address at that position has `origin = d`. Links in a document's arrangement are *home-document links* — they are owned by the document whose arrangement holds them.

The content-subspace restriction is therefore principled, not arbitrary: CL-OWN requires every link-subspace V-position's image to have `origin = d_new`, so transcluding `d_op`'s links — whose origin is `d_op ≠ d_new` — would violate it, which is why only the content subspace may be inherited.

> **V6** (*subspace selectivity*): A fork transfers only the source's content-subspace arrangement. The new document's link subspace is empty in the post-fork state:
>
> `V_{s_L}(d_new) = ∅` (in `Σ'`, the post-fork state)
>
> *Derivation.* K.δ's effect on the newly created document is `M'(d_new) = ∅`. K.μ⁺ in J4's clause (ii) extends `M'(d_new)` only with positions drawn from `V_{s_C}(d_op)`, all of which have `subspace(v) = s_C` by the definition of `V_{s_C}(d_op) := {v ∈ dom(M(d_op)) : subspace(v) = s_C}` (ASN-0047). No link-subspace V-position is added. K.ρ does not modify arrangements. ∎

V6 has an immediate consequence: links in `d_op` are not present in `d_new`'s arrangement. But this does not mean they are inaccessible from `d_new`. A link's endsets reference I-addresses (`Endset` per ASN-0047), and the I-addresses in `d_new`'s arrangement are *the same I-addresses* as in the content source `d_op`'s arrangement at every inherited V-position (V4). The post-fork state inherits both the link store and the content source's projections, and the fork's content-subspace V-positions project under any endset whose coverage hits the shared range.

To make this precise, we introduce three local definitions that the lemma below uses. An *endset* `e` (per ASN-0047's `Endset`) is a finite set of spans; each span `(s, ℓ) ∈ e` is a (start tumbler, length tumbler) pair denoting the address range `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}` from T12 (ASN-0034). Define:

- *Coverage:* `coverage(e) := ⋃_{(s, ℓ) ∈ e} span(s, ℓ) ⊆ T` — the set of I-addresses spanned by `e`.
- *Projection:* `project(a, i, d, Σ) := {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(Σ.L(a).eᵢ)}` — the V-positions of `d` at state `Σ` whose images at slot `i` of link `a`'s endset structure (per L3, ASN-0047) fall inside the slot's coverage.
- *Discoverability:* `discoverable_from(a, d, Σ) := (E i : 1 ≤ i ≤ |Σ.L(a)| : project(a, i, d, Σ) ≠ ∅)` — link `a` is discoverable from `d` at `Σ` iff some slot of `a` projects to at least one V-position of `d`.

We record the consequence as a structural lemma:

> **V6a** (*link discoverability inheritance*): For every link `a ∈ dom(Σ.L)`, after the fork composite `Σ →* Σ'`:
>
> (i) `Σ'.L(a) = Σ.L(a)` — the link's endsets persist across the composite. *Derivation.* The fork composite decomposes into K.δ + K.μ⁺ + K.ρ × n (or K.δ alone in the empty-source case per V7), and each elementary transition frames `L' = L` by its frame clause (ASN-0047): K.δ's frame is `C' = C; L' = L; R' = R`; K.μ⁺'s frame is `C' = C; L' = L; E' = E; …; R' = R`; K.ρ's frame is `C' = C; E' = E; (A d :: M'(d) = M(d))` together with the elementary effect `R' = R ∪ {(a, d)}`, which leaves `L` unchanged because K.ρ's signature acts on `R` only. Composing across the constituent steps: `Σ'.L = Σ.L`, hence `Σ'.L(a) = Σ.L(a)` for every `a ∈ dom(Σ.L)`, and in particular `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)` for every slot `i`.
>
> (ii) `project(a, i, d_src, Σ') = project(a, i, d_src, Σ)` for every slot `i` — the source's projection is unchanged. *Derivation.* Unfolding the definition: `project(a, i, d_src, Σ') = {v ∈ dom(Σ'.M(d_src)) : Σ'.M(d_src)(v) ∈ coverage(Σ'.L(a).eᵢ)}`. By V5, `Σ'.M(d_src) = Σ.M(d_src)` (so `dom` and pointwise values coincide); by (i), `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)`. Substituting both equalities into the set-builder: `project(a, i, d_src, Σ') = {v ∈ dom(Σ.M(d_src)) : Σ.M(d_src)(v) ∈ coverage(Σ.L(a).eᵢ)} = project(a, i, d_src, Σ)`.
>
> (iii) `project(a, i, d_op, Σ) ∩ V_{s_C}(d_op) = project(a, i, d_new, Σ')` for every slot `i` — the fork's projection equals the content source `d_op`'s content-subspace-restricted projection (on a first fork `d_op = d_src`). *Derivation.* We show both inclusions. *(⊆)* For every `v ∈ project(a, i, d_op, Σ) ∩ V_{s_C}(d_op)`: by V4, `v ∈ dom(M'(d_new))` and `M'(d_new)(v) = M(d_op)(v)` (V4's universal supplies both conjuncts directly given `v ∈ V_{s_C}(d_op)` in the premise; V4b — the domain-equality commitment — is not consulted in this direction). By the definition of `project(a, i, d_op, Σ)`, `M(d_op)(v) ∈ coverage(Σ.L(a).eᵢ)`. By (i), `coverage(Σ.L(a).eᵢ) = coverage(Σ'.L(a).eᵢ)`. Composing: `M'(d_new)(v) ∈ coverage(Σ'.L(a).eᵢ)`, so `v ∈ project(a, i, d_new, Σ')`. *(⊇)* For every `v ∈ project(a, i, d_new, Σ')`: by the definition of `project`, `v ∈ dom(M'(d_new))` and `M'(d_new)(v) ∈ coverage(Σ'.L(a).eᵢ)`. By V4b's exact equality `dom(M'(d_new)) = V_{s_C}(d_op)`, `v ∈ V_{s_C}(d_op)` (which is `⊆ dom(M(d_op))` by `V_{s_C}(d_op) := {v ∈ dom(M(d_op)) : subspace(v) = s_C}`, so `v ∈ dom(M(d_op))`). By V4, `M'(d_new)(v) = M(d_op)(v)`; by (i), `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)`. Composing: `M(d_op)(v) ∈ coverage(Σ.L(a).eᵢ)`, so `v ∈ project(a, i, d_op, Σ)`, and combined with `v ∈ V_{s_C}(d_op)`, `v ∈ project(a, i, d_op, Σ) ∩ V_{s_C}(d_op)`.
>
> The link store is unchanged, the named source `d_src`'s discoverability is preserved (ii), and the fork inherits the content source `d_op`'s content-subspace projection witnesses (iii).

The implementation observation is that Gregory's `docreatenewversion` excludes the link subspace through a structural V-space layout — text starts at `1.x` and links at `2.x`, with the kluged `retrievedocumentpartofvspanpm` extracting only the text-subspace V-span. We note this is one of several ways to achieve V6: an alternative implementation could check `subspace(v) = s_C` explicitly per position, or could compute the V-span of the content subspace by a different mechanism entirely. The abstract claim — V6 — is what every conforming implementation must satisfy.

## The Empty-Source Case

J4 imposes the precondition `V_{s_C}(d_op) ≠ ∅` on the content source operand. We now consider what happens when this fails — when `d_op`'s content subspace is empty (either because nothing has ever been inserted, or because everything has been deleted via K.μ⁻ down to zero content positions). On a first fork `d_op = d_src`; on a subsequent fork `d_op = d_prev`, so the relevant emptiness is that of the prior version, which may be empty even when `d_src` is not.

The K.μ⁺ transition cannot fire with an empty extension set: its precondition `dom(M'(d)) ⊃ dom(M(d))` requires strict extension. With nothing to add, K.μ⁺ has no admissible invocation. The composite therefore cannot include a K.μ⁺ step; it must consist of K.δ alone (with K.ρ vacuously contributing nothing, since `ran(M'(d_new)) = ∅`).

Nelson's specification of CREATENEWVERSION reads: "This creates a new document with the contents of document `<doc id>`. It returns the id of the new document." [LM 4/66] The natural reading is that the new document is created *with whatever contents the source has*, including the degenerate case of zero contents. Empty documents are first-class entities in the design — CREATENEWDOCUMENT explicitly produces one [LM 4/65]. There is no gate in the specification text that conditions the operation on the source having content.

We therefore commit to producing an empty fork as the normative behavior:

> **V7** (*empty-source behavior*): A fork of `d_src` with `V_{s_C}(d_op) = ∅` reduces to K.δ alone, producing a new entity `d_new ∈ E'_doc` with `M'(d_new) = ∅` and `R' = R`. The operation succeeds; the fork is itself an empty document, eligible for subsequent insertion or further forking.

V0 dispatches on whether `V_{s_C}(d_op)` is empty: when non-empty, the K.δ + K.μ⁺ + K.ρ composite of J4 (ASN-0047); when empty, V7's K.δ-alone composite, which vacates J4's clauses (ii) and (iii) since K.μ⁺ does not fire and `ran(M'(d_new))` is empty.

Under V7's normative behavior, V1, V2, V3, V5, V10, V11, V12 hold unconditionally; V6 holds substantively — K.δ's effect on the freshly created document initialises `M'(d_new) = ∅` directly, which forces `V_{s_L}(d_new) = ∅` as an immediate consequence, so V6's equation is established by total arrangement emptiness rather than by the selective subspace exclusion of the non-empty case; V9 holds vacuously (`ran(M'(d_new)) = ∅` adds nothing to `R`); V4 and V8 are vacuous when `V_{s_C}(d_op) = ∅` (their universal quantifiers range over the empty set — V4 and V8 quantify over `V_{s_C}(d_op)`, so vacuity is governed by emptiness of `d_op`'s content subspace, consistent with V0's dispatch). A fork of an empty fork produces a third empty entity, each with prefix-encoded ancestry via V2 but no shared I-addresses (because there were none to share). The fork chain remains structurally coherent.

## Structural Correspondence

We arrive at the deepest claim — the one that distinguishes a *version* from an arbitrary new document. Two documents are *versions of each other* when their arrangements share I-addresses derived from a common forking event. The structural test of this relationship is automatic: it inheres in the I-addresses themselves.

> **V8** (*positional correspondence — corollary of V4 + source frame*): For every `v ∈ V_{s_C}(d_op)`: `v ∈ dom(M'(d_new))` and `M'(d_op)(v) = M'(d_new)(v)`. This is V4 re-expressed in post-state coordinates: the per-document frame gives `M'(d_op) = M(d_op)` (the K.μ⁺ phase targets only `d_new`, and `d_op ≠ d_new`; on the first fork `d_op = d_src`, exactly V5), and V4 gives `v ∈ dom(M'(d_new))` with `M'(d_new)(v) = M(d_op)(v)`, so `M'(d_op)(v) = M(d_op)(v) = M'(d_new)(v)`.

V8 says: immediately after forking, every content-subspace V-position of the content source `d_op` corresponds to the same V-position in `d_new`, with the same I-address. On the first fork `d_op = d_src`, so this is full correspondence between the named source and the fork; on a subsequent fork it is correspondence between the prior version `d_op` and the fork. When `d_new` is the *second* version (so `d_prev` is the first fork of `d_src`, with its own content operand `d_op = d_src`), the transitive `d_src ↔ d_new` correspondence follows by composing two V8 instances: V8 at the current fork (`d_prev ↔ d_new`) with V8 at `d_prev`'s first fork (`d_src ↔ d_prev`), under the premise that `d_src` and `d_prev` are unedited across the intervening gap. For versions past the second, `d_prev` is itself a subsequent emission whose content operand is the version *before* `d_prev`, not `d_src`; V8 at `d_prev`'s fork then yields `(version-before-d_prev) ↔ d_prev`, and the two-step composition does not reach `d_src`. The general transitive correspondence in that case would require an induction along the entire emission sequence of `A_v(d_src)` with every consecutive pair unedited, which we do not derive here. The correspondence is *exact, structural, and computable from the I-address equality alone*. No history is consulted; no derivation lineage is traversed.

This is what underlies Nelson's intercomparison promise:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

The "word for word" comparison is the I-address equality test: at each shared V-position, the question "is this the same content?" reduces to "is `M(d₁)(v) = M(d₂)(v)`?" Any intercomparison operation reads this equality directly from the arrangements; nothing more is required of the storage layer, because nothing more was needed.

We record an immediate corollary.

> **V8c** (*correspondence is symmetric and untyped*): The corresponding-position set `{v ∈ T : v ∈ dom(M'(d_src)) ∩ dom(M'(d_new)) ∧ M'(d_src)(v) = M'(d_new)(v)}` is defined by `∩` and `=`, both symmetric, so it is invariant under swap of `d_src` and `d_new`. V8 records a relationship between two documents in `E_doc`; it does not distinguish "source" from "fork."

The intercomparison guarantee is *perpetual*. By T8 (AllocationPermanence, ASN-0034), `d_src` and `d_new` remain in `E_doc` forever; by P0/S0, their I-addresses persist in `dom(C)` forever; by the per-document arrangement frame discipline, neither side's arrangement modifies the other's. V8 holds in the post-fork state, and its consequences propagate to every subsequent state in which neither side has overwritten the relevant V-positions.

## Provenance Recording

The third elementary step of J4 is K.ρ, recording provenance for every I-address now in `d_new`'s arrangement.

K.ρ adds `(a, d_new)` to `R` for each `a ∈ ran(M'(d_new))`. By J1★ (ExtensionRecordsProvenance, ASN-0047) — the extended-state coupling that supersedes J1 under ValidComposite★ — provenance is *required* for every I-address newly content-subspace-referenced in `d_new`'s arrangement. By J1'★ (ProvenanceRequiresExtension), it is the only permitted extension. The fork must record provenance for every inherited I-address.

> **V9** (*fork provenance*): After a fork of `d_src`:
>
> `(A a : a ∈ ran(M'(d_new)) : (a, d_new) ∈ R')`
>
> *Derivation.* The fork composite's K.ρ × n phase records one pair `(aⱼ, d_new)` per `aⱼ ∈ ran(M'(d_new))`, with cumulative effect `R' = R ∪ {(a, d_new) : a ∈ ran(M'(d_new))}`. Hence every `a ∈ ran(M'(d_new))` satisfies `(a, d_new) ∈ R'`. This is precisely what *discharges* J1★ (ExtensionRecordsProvenance) for the composite: the coupling obligation is satisfied by V9's records, not a premise from which they are derived. ∎

V9 has the consequence that, after the fork, querying R for "documents containing I-address `a`" returns at least `{d_src, d_new}` for every `a ∈ ran(M'(d_new))` (and possibly more, if `a` was also transcluded elsewhere). The fork makes `d_new` discoverable as a container of each inherited I-address.

We observe what V9 does *not* record. By the consultation answers, the pair `(a, d_new) ∈ R'` records that `d_new` contains `a`. It does *not* record that `d_new` obtained `a` from `d_src` (as opposed to from some other transclusion path). Two things remain reconstructable from the I-addresses themselves: the content origin, because `origin(a)` identifies the original allocator, and the document fork tree, because V2's prefix-ancestry identifies the immediate parent of `d_new`. But the acquisition path — the chain of custody by which a document obtained a given I-address, e.g. "A transcluded to B, B forked to C" — is *not* stored in R and *not* reconstructable: the relation cannot distinguish a fork from a coincidental transclusion of the same I-address along an unrelated path. What is recoverable is the fork-tree lineage and the content origin, not the per-address acquisition route.

> **V9a** (*provenance does not record derivation path*): For every `(a, d_new) ∈ R'` recorded by a fork, the relation does not distinguish whether `d_new` acquired `a` via fork from `d_src`, via transclusion from a third document also containing `a`, or via direct allocation. The relation reports *who has it*; the I-address tells you *who made it*; the parent prefix tells you *who you came from*. These three pieces of information are recoverable independently from the I-address and the fork's prefix structure.

> **V9b** (*fresh forks inherit only externally-allocated I-addresses*): For every `(a, d_new) ∈ R'` recorded by a fork, `origin(a) ≠ d_new`. *Derivation.* By V3, `C' = C`, so the I-addresses inherited by `d_new` are exactly those already present in `dom(C)` at the pre-fork state. Pre-fork, `d_new ∉ E_doc`, so by SubAllocatorBundle (ASN-0047) the content sub-allocator `A_C(d_new)` had not been activated and had emitted nothing into `dom(C)`. By S7 (StructuralAttribution, ASN-0036), every `a ∈ dom(C)` has a unique `origin(a) ∈ E_doc` fixed by the I-address itself, and no inherited I-address can have `origin(a) = d_new` because `A_C(d_new)` produced no element of `dom(C)` prior to the fork. The direct-allocation branch of V9a's enumeration of acquisition paths is therefore vacuous for fresh forks; only the fork-from-`d_src` and transclusion-from-third-document branches contribute.

## Independence Among Forks

A single source may be forked many times. Each fork produces a distinct child tumbler. The K.δ allocation discipline forbids two children of `d_src` from receiving the same tumbler:

By T10a's allocator discipline and the Allocator hierarchy definition (ASN-0047), the version sub-allocator `A_v(d_src)` of `d_src` activates upon `d_src`'s creation and produces version outputs by repeated sibling generation. The first fork's `d_new = inc(d_src, 1)`; a second fork — under the chain-advancement convention `inc(prev_version, 0)` of ASN-0047's allocator hierarchy — produces a distinct sibling. T10a.7 (EnumerationInjectivity) makes the indexing map of the sub-allocator's outputs injective: distinct enumeration indices produce distinct addresses. No two forks of the same source share a tumbler.

*Notation for multiple forks.* The remainder of this ASN distinguishes two structurally different fork configurations, each with its own indexing convention:
>
> - *Sibling forks (V10).* Multiple forks of the *same* source `d_src`. We write `d_new¹, d_new²` (superscript *after* `_new`) for the first and second sibling fork of `d_src` — both produced by `A_v(d_src)`, both having `d_src` as parent in the version sub-allocator.
> - *Chain forks (V11).* A sequence of forks where each step's source is the prior step's fork. We write `d¹_new, d²_new, ..., d^k_new` (superscript *before* `_new`) for the chain, with `d⁰_new := d_src`; each `dⁱ_new` is produced by `A_v(d^{i-1}_new)` from its parent `d^{i-1}_new` in the chain.
>
> Superscript position is the disambiguator: `d_new²` is the second sibling fork of `d_src`; `d²_new` is the second link in a fork chain from `d_src`. The two are structurally distinct tumblers — `d_new²` has length `#d_src + 1` (TA5(c) at sibling step) while `d²_new` has length `#d_src + 2` (TA5(d) at chain step). The conventions are used uniformly in V10, V11, and the worked example.

Two forks of the same source occur *sequentially*, not in parallel: the SequentialTransitionAxiom (ASN-0047) orders all state transitions totally, and `A_v(d_src)`'s emission count is part of the state, so any later fork necessarily reads a post-state in which all prior forks of `d_src` have already advanced the sub-allocator. The pre-state of each subsequent fork lies at or after the post-state of every earlier fork of `d_src`, with prior emissions having entered `E_doc` and `A_v(d_src)`'s frontier having advanced past them. V1's subsequent-fork sub-case then governs each fork's allocation.

> **V10** (*sibling independence*): Let `Σ →* Σ¹` be a fork of `d_src` producing `d_new¹`, and let `Σ_g →* Σ²` be any later fork of the same `d_src` producing `d_new²`, where `Σ_g` is any state reachable from `Σ¹` by a finite sequence of valid composite transitions (the intervening transitions may be of any kind on any documents, including further forks of `d_src` itself). The two forks are independent in three senses:
>
> (a) *Distinct identities.* `d_new¹ ≠ d_new²`. By V1, both `d_new¹` and `d_new²` are emissions of `A_v(d_src)` — both lie within a single allocator's domain, so no cross-allocator collision is possible to consider. By SequentialTransitionAxiom (ASN-0047) and P1 (entity permanence, ASN-0047), `d_new¹` is already in `E` at `Σ_g`, so the K.δ event placing `d_new²` is a strictly later K.δ event on `A_v(d_src)`'s frontier — `d_new¹` and `d_new²` lie at distinct enumeration indices in `A_v(d_src)`'s sibling stream. T10a.7 (EnumerationInjectivity, ASN-0034) applied to `A_v(d_src)`'s enumeration gives distinct addresses at distinct indices. So `d_new¹ ≠ d_new²`.
>
> (b) *Independent content shares.* Each sibling fork inherits content from its own content source operand `d_op` (J4) *at the moment of that fork*. `d_new¹`'s operand `d_op¹` is fixed by V1's fork-dispatch at `Σ`: `d_op¹ = d_src` when `d_new¹` is the first fork of `d_src`, and `d_op¹ = max(dom(A_v(d_src)))` (a prior version) otherwise; either way it reads `M(d_op¹)` at `Σ`. `d_new²`'s operand `d_op²` is fixed by V1's dispatch at `Σ_g`: since `d_new¹ ∈ E` at `Σ_g` by (a)'s argument, `A_v(d_src)` already has a frontier, so `d_new²` is necessarily a subsequent fork and `d_op² = max(dom(A_v(d_src)))` — the most recent prior version emitted by `A_v(d_src)` at `Σ_g` (e.g. `d_new¹` when no intervening sibling fork occurred) — and it reads `M(d_op²)` at `Σ_g`. The two reads may or may not agree, depending on the operands `d_op¹, d_op²` and on whether any intervening transition modified them between `Σ` and `Σ_g`. Their inherited V→I mappings live in separate arrangements `M¹(d_new¹)` and `M²(d_new²)`. Sibling forks are distinct documents (V10(a)), and V5a Corollary 2 — pairwise independence, in which `d¹` names the *preserved* document and `d²` the other party — yields the two preservation directions via two independent instantiations of the same corollary. *Direction 1* (modifications M-targeted at `d_new¹` preserve `M(d_new²)`): instantiate Corollary 2 at `(d¹, d²) = (d_new², d_new¹)`. The corollary's hypothesis "no step M-targeted at `d¹`" reads "no step M-targeted at `d_new²`"; since `d_new¹ ≠ d_new²` by V10(a), a step M-targeted at `d_new¹` is not M-targeted at `d_new²`, satisfying the hypothesis. The corollary's conclusion `M''(d¹) = M'(d¹)` then reads `M''(d_new²) = M'(d_new²)` — `M(d_new²)` is preserved across such a step. *Direction 2* (modifications M-targeted at `d_new²` preserve `M(d_new¹)`): instantiate Corollary 2 at `(d¹, d²) = (d_new¹, d_new²)`, by the same argument with operands swapped.
>
> (c) *Independent provenance records.* `R²` contains both `(a, d_new¹)` and `(a, d_new²)` for shared I-addresses, but these are distinct pairs (since `d_new¹ ≠ d_new²` by (a)).

V10's part (a) follows from V1 and T10a.7 as derived above. Part (b) follows from V5a Corollary 2 applied symmetrically. Part (c) follows from V9 applied at each fork independently.

We further observe that each fork independently derives from `d_src`'s state *at the moment of forking*. If two forks are separated in time by an editing operation on `d_src`, the two forks inherit different arrangements.

> **V10a** (*time-sensitivity of derivation*): A fork in state `Σ` inherits `V_{s_C}(d_op)` and the mappings `M(d_op)|_{V_{s_C}(d_op)}` of its content source operand as they stand in `Σ`, not as they stood at any prior or subsequent state. Two forks of the same source at different times may produce different new versions, reflecting whatever state changes to the operands (and, for subsequent forks, whatever change of operand from `d_src` to `d_prev`) occurred between them.

By SequentialTransitionAxiom (ASN-0047), state transitions are sequentially atomic — there is no intermediate state visible to a fork mid-edit. The "moment of forking" is well-defined as the pre-state `Σ` of the fork composite.

## Composability: Fork of a Fork

The structural account treats `d_src` as any element of `E_doc`. A fork creates `d_new ∈ E_doc`, which is itself eligible to be the source of a subsequent fork. We trace what happens.

Suppose `Σ →* Σ¹` forks `d_src` to `d¹_new`, then `Σ¹ →* Σ²` forks `d¹_new` to `d²_new`, where each step is the *first* fork of its immediate source — so each step's J4 content source operand `d_op` coincides with that immediate source (step 1's `d_op = d_src`, step 2's `d_op = d¹_new`). By V1 at each fork: `d¹_new = inc(d_src, 1)` and `d²_new = inc(d¹_new, 1)`. By V2 at each fork: `d_src ≼ d¹_new ≼ d²_new`. Ancestry composes.

By V4 at each fork (with `d_op` the immediate source): `M¹(d¹_new) = M(d_src)|_{V_{s_C}(d_src)}` (in the sense that for each content-subspace V-position of the source, the same V-position with the same I-address appears in the fork). Then `M²(d²_new) = M¹(d¹_new)|_{V_{s_C}(d¹_new)}`. Composing: the I-addresses in `M²(d²_new)` are the same I-addresses as in `M(d_src)` over the V-positions present in all three arrangements.

> **V11** (*transitive identity along unedited fork chains*): Let `Σ` denote the pre-state of the first fork — the chain's initial state. For every chain length `k ≥ 1` and every chain of forks `d_src → d¹_new → d²_new → ... → d^k_new` starting from `Σ` (with `d⁰_new := d_src`), where each step `dⁱ⁻¹_new → dⁱ_new` is a fork composite that is the *first* fork of its immediate source `d^{i-1}_new` — so that step `i`'s J4 content source operand `d_op` equals `d^{i-1}_new`, and V4 at step `i` reads `M(d^{i-1}_new)` — and *each step's source has its content-subspace arrangement unchanged between the prior step's post-state and the current step's pre-state* — that is, for every `1 ≤ i ≤ k`, `V_{s_C}(d^{i-1}_new)` is the same set in the post-state of step `i − 1` and the pre-state of step `i`, and for every `v` in this set, `M(d^{i-1}_new)(v)` is the same value in both states (with the convention that at `i = 1`, "step 0's post-state" denotes `Σ` itself — equivalently the pre-state of step 1 — so the premise at `i = 1` is satisfied trivially by reflexivity of set and pointwise equality) — the I-addresses inherited by `d^k_new` are the same I-addresses that `d_src` held at `Σ`: for every `v ∈ V_{s_C}(d_src)` evaluated at `Σ`, `v ∈ dom(M^k(d^k_new))` at the post-state of step `k`, and the value `M^k(d^k_new)(v)` at the post-state of step `k` equals the value `M(d_src)(v)` at `Σ`.
>
> *Anchoring at `Σ`.* The premise scopes per-step source preservation to each step's *immediate* source `d^{i-1}_new` across the gap between step `i-1`'s post-state and step `i`'s pre-state. For `i ≥ 2` the source is `d^{i-1}_new`, not `d_src`, so the premise leaves `d_src` unconstrained across gaps after step 1. To keep the conclusion well-defined under that scope, V11 anchors `V_{s_C}(d_src)` and `M(d_src)(v)` at `Σ` — the immutable historical state at the chain's start — rather than at any later state. Arrangement edits M-targeted elsewhere — third documents, non-immediate chain members — are discharged operationally by V5a Corollary 2.
>
> *Derivation by induction on chain length `k`.*
>
> *Base case (`k = 1`).* V4 applied to the first fork `d_src → d¹_new` gives `M¹(d¹_new)(v) = M(d_src)(v)` for every `v ∈ V_{s_C}(d_src)`, both sides evaluated at the post-state of step 1 (V4's post-fork claim). V5 applied to step 1 gives `M¹(d_src) = M(d_src)`, so the source's arrangement is identical at post-step-1 and at the pre-state of step 1 — which is `Σ`. Consequently `V_{s_C}(d_src)` is the same set at `Σ` and at post-step-1, and for every `v` in this set, `M(d_src)(v)` at post-step-1 equals `M(d_src)(v)` at `Σ`. The base case conclusion: for every `v ∈ V_{s_C}(d_src)` evaluated at `Σ`, `v ∈ dom(M¹(d¹_new))` at post-step-1, and `M¹(d¹_new)(v)` at post-step-1 equals `M(d_src)(v)` at `Σ`.
>
> Note that `v ∈ V_{s_C}(d_src)` already implies `subspace(v) = s_C`, and `v ∈ dom(M¹(d¹_new))` by the V4 conclusion, so `v ∈ V_{s_C}(d¹_new)` at the post-state of step 1 — i.e., `V_{s_C}(d_src) ⊆ V_{s_C}(d¹_new)`.
>
> *Inductive step (`k ≥ 2`).* Assume the induction hypothesis at step `k − 1`: for every `v ∈ V_{s_C}(d_src)` evaluated at `Σ`, `v ∈ dom(M^{k-1}(d^{k-1}_new))` at the post-state of step `k − 1`, and `M^{k-1}(d^{k-1}_new)(v)` at the post-state of step `k − 1` equals `M(d_src)(v)` at `Σ`.
>
> The k-th fork composite `Σ^{k-1} →* Σ^k` takes `d^{k-1}_new` as source. Applying V4 at step `k` to each `v ∈ V_{s_C}(d_src)` at `Σ` requires `v ∈ V_{s_C}(d^{k-1}_new)` at step `k`'s pre-state. We establish the required inclusion in two stages, then close.
>
> *Stage 1 — IH delivers inclusion at the post-state of step `k − 1`.* Take any `v ∈ V_{s_C}(d_src)` at `Σ`. The IH gives `v ∈ dom(M^{k-1}(d^{k-1}_new))` at the post-state of step `k − 1`. By the definition of `V_{s_C}` (ASN-0047, ASN-0036 S8a inheritance), `subspace(v) = s_C` for every `v ∈ V_{s_C}(d_src)` at `Σ`. The two conjuncts of `V_{s_C}(d^{k-1}_new) = {v ∈ dom(M^{k-1}(d^{k-1}_new)) : subspace(v) = s_C}` are met, so `v ∈ V_{s_C}(d^{k-1}_new)` at the post-state of step `k − 1`. Pointwise the IH also supplies `M^{k-1}(d^{k-1}_new)(v)` at post-step-(k−1) equals `M(d_src)(v)` at `Σ`.
>
> *Stage 2 — formal premise carries the inclusion across the gap to the pre-state of step `k`.* The formal premise at `i = k` states that `V_{s_C}(d^{k-1}_new)` is the same set in the post-state of step `k − 1` and the pre-state of step `k`, and that for every element `v` of this set, `M(d^{k-1}_new)(v)` is the same value in both states. Applying the premise pointwise to the `v ∈ V_{s_C}(d^{k-1}_new)` supplied by Stage 1: `v ∈ V_{s_C}(d^{k-1}_new)` at the pre-state of step `k`, and the value `M^{k-1}(d^{k-1}_new)(v)` at post-step-(k−1) — which by the IH equals `M(d_src)(v)` at `Σ` — reads through unchanged into the pre-state of step `k`.
>
> *Closing.* V4 at the k-th fork now applies for every `v ∈ V_{s_C}(d_src)` at `Σ`: V4 takes `v ∈ V_{s_C}(d^{k-1}_new)` (pre-step-k) as input and concludes `v ∈ dom(M^k(d^k_new))` at post-step-k with `M^k(d^k_new)(v)` at post-step-k equal to `M^{k-1}(d^{k-1}_new)(v)` at pre-step-k (V4's standard prime-convention reading: post-state value of the fork equals pre-state value of the source). Composing:
>
> `M^k(d^k_new)(v) at post-step-k = M^{k-1}(d^{k-1}_new)(v) at pre-step-k     [V4 at step k]`
> `                              = M^{k-1}(d^{k-1}_new)(v) at post-step-(k-1) [premise at i=k, Stage 2]`
> `                              = M(d_src)(v) at Σ                          [induction hypothesis]`
>
> The induction closes. ∎

> **V11a** (*ancestry composition*): The prefix relation chains: `d_src ≼ d¹_new ≼ d²_new ≼ ... ≼ d^k_new`. Each step `dⁱ⁻¹_new → dⁱ_new` is the *first* fork of its immediate source (V11's premise), so by V1 it is `inc(dⁱ⁻¹_new, 1)` — K.δ case (ii) at `k = 1` — extending the tumbler by exactly one component at position `#dⁱ⁻¹_new + 1` whose value is `1` (TA5(d) at `k = 1`). The full chain is recoverable from `d^k_new`'s tumbler alone by reading prefixes of strictly increasing length: the prefix of `d^k_new` of length `#d_src + i` is exactly `dⁱ_new` for every `0 ≤ i ≤ k` (with `d⁰_new := d_src`). *Derivation of prefix chain.* We first verify that `≼` is transitive by unfolding the Prefix definition (ASN-0034). Suppose `a ≼ b` and `b ≼ c`. By Prefix, `a ≼ b` gives `#a ≤ #b` and `(A i : 1 ≤ i ≤ #a : bᵢ = aᵢ)`; `b ≼ c` gives `#b ≤ #c` and `(A i : 1 ≤ i ≤ #b : cᵢ = bᵢ)`. By NAT-order's transitivity of `<` composed with the `m ≤ n ⟺ m < n ∨ m = n` definition (case analysis on the disjuncts of `#a ≤ #b` and `#b ≤ #c`: `<`-`<` chains by NAT-order transitivity; `<`-`=` and `=`-`<` substitute equality into the strict step; `=`-`=` composes equalities), `#a ≤ #c`. For each `i` with `1 ≤ i ≤ #a`: since `#a ≤ #b`, also `1 ≤ i ≤ #b`, so `cᵢ = bᵢ` by the second hypothesis; and `bᵢ = aᵢ` by the first hypothesis; composing the two component equalities gives `cᵢ = aᵢ`. Both conjuncts of `a ≼ c` are established. With transitivity in hand, V2 applied at each chain step `i` (for `1 ≤ i ≤ k`) — whose source is `dⁱ⁻¹_new` and fork is `dⁱ_new`, with `d⁰_new := d_src` — supplies the direct conjunction `d⁰_new ≼ d¹_new ∧ d¹_new ≼ d²_new ∧ ... ∧ d^{k-1}_new ≼ d^k_new`. Composing these `k` per-step inclusions via `k − 1` applications of single-triple transitivity yields `dⁱ_new ≼ dⱼ_new` for every `0 ≤ i ≤ j ≤ k`, and in particular `d_src ≼ d^k_new`. *Derivation of recovery.* Two facts establish the recovery procedure. (i) *Length identity.* `#dⁱ_new = #d_src + i` for every `0 ≤ i ≤ k`. Induction on `i`. *Base* (`i = 0`): `d⁰_new := d_src`, so `#d⁰_new = #d_src + 0`. *Step* (`i → i + 1`): each chain step is the *first* fork of its immediate source (V11's premise), so by V1 `dⁱ⁺¹_new = inc(dⁱ_new, 1)`; TA5(d) at `k = 1` gives `#dⁱ⁺¹_new = #dⁱ_new + 1`. Composing with the outer induction hypothesis: `#dⁱ⁺¹_new = #d_src + (i + 1)`. (ii) *Prefix identity.* For each `0 ≤ i ≤ k`, the relation `dⁱ_new ≼ d^k_new` is already established by the prefix chain derivation above as the `j = k` instance of `dⁱ_new ≼ dⱼ_new`. The Prefix definition then gives `(A j : 1 ≤ j ≤ #dⁱ_new : (d^k_new)_j = (dⁱ_new)_j)`. By (i), `#dⁱ_new = #d_src + i`, so the prefix of `d^k_new` of length `#d_src + i` agrees componentwise with `dⁱ_new` at every position; T3 (CanonicalRepresentation, ASN-0034) — equal length plus componentwise agreement is identity — gives that this prefix equals `dⁱ_new`. Reading off prefixes of length `#d_src, #d_src + 1, ..., #d_src + k` recovers `d_src, d¹_new, ..., d^k_new` in order; the per-step extension component at position `#dⁱ⁻¹_new + 1` of each successive prefix is the value `1` characterised in the lemma statement. ∎

The depth of the fork chain is invisible to the mechanism. Each fork performs the same structural operation independently of how deep the chain is. There is no accumulation of state, no recursion, no per-chain bookkeeping. We can fork arbitrarily deep, and every document in the resulting tree shares the original source's I-addresses for inherited V-positions.

This compounds with V8: any two documents anywhere in the fork tree can be intercompared via I-address equality, and the comparison surfaces the V-positions where their inherited mappings still agree. Siblings, ancestors, descendants, cousins — the relationship is irrelevant to the comparison machinery, because the I-addresses carry the relationship structurally.

We note what V11 does *not* claim. It does not claim the I-addresses are *visible from the same V-positions* at every state — subsequent editing may have rearranged or removed them on any branch. It claims only that the I-addresses are the same I-addresses; where they appear in each arrangement depends on each document's editing history.

## Permanence Across Source and Fork

We collect the permanence guarantees that hold across both documents after the fork.

By T8 (AllocationPermanence, ASN-0034) and P1 (EntityPermanence, ASN-0047): both `d_src` and `d_new` remain in `E_doc` for all subsequent reachable states. Neither can be removed.

By P0 (ContentPermanence, ASN-0047) and S0/S1 (ASN-0036): every I-address in `dom(C)` at fork-time remains in `dom(C')` for all subsequent states, with unchanged value. In particular, every I-address in `ran(M'(d_new))` persists in `dom(C)` forever, regardless of how either document's arrangement evolves.

By P2 (ProvenancePermanence, ASN-0047): the provenance records `(a, d_new)` added by V9 persist in `R` forever, regardless of subsequent arrangement modifications. Even if `d_new`'s owner later deletes `a` from `d_new`'s arrangement (via K.μ⁻), the historical fact `(a, d_new) ∈ R` records that `d_new` once contained `a`.

We name the combined consequence.

> **V12** (*joint permanence*): After a fork, both `d_src` and `d_new` and all their inherited I-addresses are permanent. For every reachable state subsequent to the fork:
>
> (a) `d_src ∈ E'_doc ∧ d_new ∈ E'_doc` (P1)
>
> (b) `(A a ∈ ran(M'(d_new)) :: a ∈ dom(C'')` for every subsequent state `Σ''` (P0)
>
> (c) `(A a ∈ ran(M'(d_new)) :: (a, d_new) ∈ R'')` for every subsequent state `Σ''` (P2 applied to the post-fork records of V9)
>
> (d) `(A a ∈ ran(M'(d_new)) :: (a, d_op) ∈ R'')` — provenance records for the *content source operand* `d_op` (`= d_src` on the first fork, `= d_prev` on a subsequent fork) are also permanent. *Derivation.* V4 + V4b give range equality `ran(M'(d_new)) = ran(M(d_op)|_{V_{s_C}(d_op)})`, so every inherited `a` is content-subspace-referenced in `M(d_op)` at the pre-fork boundary `Σ` with `d_op ∈ E_doc`; hence `(a, d_op) ∈ Contains_C(Σ) ⊆ R` by P4★ at `Σ`, and P2 carries the pair into every subsequent `Σ''`. (On the first fork `d_op = d_src`, recovering the original "provenance for the named source is permanent" reading.)

V12 underwrites Nelson's "lengthy due process" claim: published content stays published precisely because the permanence is structural, not policy. There is no operation in the transition vocabulary of ASN-0047 that removes content from `C`, removes entities from `E`, or removes pairs from `R`. The permanence is absolute at the abstract level; any withdrawal mechanism a deployment chooses to layer on top is a policy decision above the transition system, not an operation within it.

The consequence for source-fork pairs specifically: neither owner can remove the shared content from the storage substrate. The source owner can delete content from their own *arrangement* (K.μ⁻ on `d_src`), and similarly the fork owner can delete from their own arrangement. Neither action affects the other's arrangement (V5a Corollary 1, applied at the pair `(d_src, d_new)`) and neither affects `dom(C)` (V3 holds for K.μ⁻ as well; its frame condition is `C' = C`). The I-addresses persist; the arrangements evolve independently.

## The Fork Composite

We assemble the formal definition.

> **V0** (*fork operation*): A *fork* of `d_src` is a composite state transition `Σ →* Σ'`.
>
> *Composite structure.* The composite is the *uninterrupted* sequence of elementary transitions K.δ + K.μ⁺ + K.ρ × n (where `n = |ran(M'(d_new))|`), or K.δ alone in the empty-source case per V7's extension of J4. No other elementary transitions fire between the constituent steps — in particular, no intervening K.μ⁻, K.μ~, or K.μ⁺ on `d_op` disturbs the content source between steps.
>
> *Precondition.* `d_src ∈ E_doc`. No content-existence precondition is imposed; the empty-source case is normative per V7.
>
> *Effects.* Write `d_op` for the J4 content source operand: `d_op = d_src` on the first fork, `d_op = d_prev` on a subsequent fork. When `V_{s_C}(d_op) ≠ ∅` (the composite is K.δ + K.μ⁺ + K.ρ × n, where `n = |ran(M'(d_new))|`):
>
> ```
> C' = C                                              (V3)
> L' = L                                              (no K.λ or K.μ⁺_L steps)
> E' = E ∪ {d_new}                                    (V1)
>   where d_new is A_v(d_src)'s next emission:
>     d_new = inc(d_src, 1)   on first fork of d_src      (d_op = d_src)
>     d_new = inc(d_prev, 0)  on subsequent fork          (d_op = d_prev)
>       (d_prev = A_v(d_src)'s most recent prior emission)
> M'(d_new)(v) = M(d_op)(v)   for v ∈ V_{s_C}(d_op)   (V4)
> M'(d_new)(v) undefined       for v ∉ V_{s_C}(d_op) (V4b; V6 as corollary for link-subspace V-positions)
> (A d' : d' ≠ d_new : M'(d') = M(d'))                (V5 for d' = d_src; K.δ + K.μ⁺ + K.ρ frame conditions for d' ≠ d_src ∧ d' ≠ d_new — in particular M'(d_op) = M(d_op))
> R' = R ∪ {(a, d_new) : a ∈ ran(M'(d_new))}          (V9; set equality, verified below)
> ```
>
> The set `V_{s_C}(d_op)` (and `M(d_op)(v)` for `v` in it) is evaluated at the pre-state `Σ`; the per-document frame guarantee `M'(d_op) = M(d_op)` pins the same value in `Σ'`.
>
> The K.ρ phase is `n` elementary K.ρ invocations (one per `a ∈ ran(M'(d_new))`), each recording a single `(a, d_new)` pair per K.ρ's definition (ASN-0047). The set-builder `{(a, d_new) : a ∈ ran(M'(d_new))}` denotes the cumulative effect of all `n` invocations on `R`.
>
> When `V_{s_C}(d_op) = ∅` (the composite is K.δ alone, per V7's extension of J4): `C' = C`, `L' = L`, `E' = E ∪ {d_new}` (where `d_new` is `A_v(d_src)`'s next emission, formula as above), `M'(d_new) = ∅`, `M'(d') = M(d')` for `d' ≠ d_new`, `R' = R`. The operation succeeds.

The elementary decomposition into K.δ + K.μ⁺ + K.ρ × n (where `n = |ran(M'(d_new))|`), or K.δ alone in the empty case, verifies the ValidComposite★ conditions of ASN-0047. We check briefly.

*Notation for the verification.* Within this verification we denote intra-composite sub-states by `Σ^{(j)}` (parenthesised superscript), with state-stamped components inheriting the same superscript: `Σ^{(0)} = Σ` (pre-state), `Σ^{(1)}` after K.δ, `Σ^{(2)}` after K.μ⁺, and `Σ^{(2+j)}` after the j-th elementary K.ρ step (so the K.ρ × n phase terminates at `Σ^{(2+n)}`).

*K.δ at the pre-fork state Σ.* The K.δ sub-case is determined by `A_v(d_src)`'s state.

*K.δ sub-case A — first fork.* `A_v(d_src)` has emitted no prior version. K.δ case (ii) with `k = 1`, `t = d_src`. The K.δ outer preconditions are `e ∉ E ∧ T4-valid(e) ∧ ¬Element(e)`; the uniform Case (ii) precondition is `parent(e) ∈ E`; the per-sub-case precondition at `k = 1` is `t ∈ E_doc`. We discharge each in turn.

Per-sub-case: `d_src ∈ E_doc` is V0's precondition.

Outer-precondition `e ∉ E` (freshness of `d_new = inc(d_src, 1)`) is discharged by ChildSpawnFreshness (ASN-0047) at `t = d_src`, `k' = 1`, which gives `inc(d_src, 1) ∉ Σ.E ⟺ the (d_src, 1) child-spawn has not yet been performed`. The lemma's operand admissibility holds: `k' = 1` requires `Document(d_src)`, which follows from `d_src ∈ E_doc`. Sub-case A's governing predicate — `A_v(d_src)` has emitted no prior version — *is* the statement that the `(d_src, 1)` child-spawn (the K.δ event that activates `A_v(d_src)` and places its base address `inc(d_src, 1)` into `E`) has not yet fired. The biconditional then yields `d_new ∉ E` directly.

Outer-precondition `T4-valid(d_new)` (T4-validity) is discharged by T10a.4 (T4PreservationUnderDiscipline, ASN-0034) applied to `A_v(d_src)`. T10a-conformance of `A_v(d_src)` is established by ASN-0047's Allocator hierarchy definition, which declares T10a-conformance per sub-allocator frontier; T10a.4 then guarantees every output — including `d_new` as `A_v(d_src)`'s first emission — satisfies T4. Outer-precondition `¬Element(d_new)` follows from `Document(d_new)` (established below): `Document(d_new)` will mean `zeros(d_new) = 2`, while `Element(d_new)` would require `zeros(d_new) = 3`; the two are exclusive.

Uniform-precondition `parent(d_new) ∈ E` is discharged in two steps. K.δ-ID.parent-0/1 (ASN-0047), applied to `e = inc(d_src, 1)` at `k = 1`, gives `parent(d_new) = parent(d_src)`. P8 (EntityHierarchy, ASN-0047), applied to `d_src ∈ E` with `¬Node(d_src)` (since `Document(d_src)` from `d_src ∈ E_doc` forces `zeros(d_src) = 2 ≠ 0`), yields `parent(d_src) ∈ E`. Composing: `parent(d_new) = parent(d_src) ∈ E`.

By K.δ-ID.zeros-0/1, `zeros(d_new) = zeros(d_src) = 2`, so `Document(d_new)`.

*K.δ sub-case B — subsequent fork.* `A_v(d_src)` has prior emissions with most recent `d_prev ∈ E_doc`. K.δ case (ii) with `k = 0`, `t = d_prev`. The K.δ outer preconditions are `e ∉ E ∧ T4-valid(e) ∧ ¬Element(e)`; the uniform Case (ii) precondition is `parent(e) ∈ E`; the per-sub-case precondition at `k = 0` is `t ∈ E ∧ ¬Node(t) ∧ inc(t, 0) ∉ E`. We discharge each in turn.

Per-sub-case `d_prev ∈ E` holds by P1 (entity permanence, ASN-0047) applied to `d_prev`'s earlier K.δ event. Per-sub-case `¬Node(d_prev)` holds because `d_prev` is a `A_v(d_src)` output with `Document(d_prev)` (zeros preserved at the first emission by K.δ-ID.zeros-0/1 at `k = 1`, and preserved at each subsequent emission by K.δ-ID.zeros-0/1 at `k = 0`); `Document` excludes `Node` (`zeros = 2 ≠ 0`).

Per-sub-case freshness `inc(d_prev, 0) ∉ E` is discharged by FrontierEquivalence (ASN-0047) at `t = d_prev`, which gives `inc(d_prev, 0) ∉ Σ.E ⟺ d_prev is the frontier of A_v(d_src)'s (d_prev, 0)-branch`. The lemma's operand admissibility holds: `d_prev ∈ E` and `¬Node(d_prev)` were just established, and ActivatedEmission (ASN-0047) supplies the activated entity-level sub-allocator whose domain contains `d_prev` — namely `A_v(d_src)`, unique by T10a.6. Sub-case B's governing predicate — `d_prev` is `A_v(d_src)`'s most recent emission, i.e., `d_prev = max(dom(A_v(d_src)))` — *is* the statement that `d_prev` is that frontier. The biconditional then yields `inc(d_prev, 0) ∉ E` directly.

Outer-precondition `e ∉ E` is the same condition as the per-sub-case freshness just discharged. Outer-precondition `T4-valid(d_new)` is discharged by T10a.4 (T4PreservationUnderDiscipline, ASN-0034) applied to `A_v(d_src)` — T10a-conforming per ASN-0047's Allocator hierarchy definition — which guarantees every output (every sibling emission and the base address) is T4-valid. Outer-precondition `¬Element(d_new)` follows from `Document(d_new)` (established below): `zeros(d_new) = 2 ≠ 3`.

Uniform-precondition `parent(d_new) ∈ E` is discharged in two steps. K.δ-ID.parent-0/1 (ASN-0047), applied to `e = inc(d_prev, 0)` at `k = 0`, gives `parent(d_new) = parent(d_prev)`. P8 (EntityHierarchy, ASN-0047), applied to `d_prev ∈ E` with `¬Node(d_prev)` (just established), yields `parent(d_prev) ∈ E`. Composing: `parent(d_new) = parent(d_prev) ∈ E`.

By K.δ-ID.zeros-0/1, `zeros(d_new) = zeros(d_prev) = 2`, so `Document(d_new)`.

(NodeBaptism does not apply in either sub-case — it governs only K.δ events with `Node(e)`, while `d_new` satisfies `Document(d_new)`.)

Effect (both sub-cases): `E^{(1)} = E ∪ {d_new}`, `M^{(1)}(d_new) = ∅`, `M^{(1)}(d') = M(d')` for `d' ≠ d_new`. Frame: `C^{(1)} = C`, `L^{(1)} = L`, `R^{(1)} = R`.

*K.μ⁺ at Σ^{(1)} (skipped in the empty case).* Target `d = d_new`. The extension set is `V_{s_C}(d_op)`, where `d_op` is the content source operand (`d_src` on the first fork, `d_prev` on a subsequent fork). Precondition: `d_new ∈ E^{(1)}_doc` (just established); for every `v ∈ V_{s_C}(d_op)`, the target `M(d_op)(v) ∈ dom(C^{(1)}) = dom(C)` (S3★ at `d_op` restricted to `subspace(v) = s_C`, ASN-0047, with `M^{(1)}(d_op) = M(d_op)` by K.δ's frame condition `(A d' : d' ≠ d_new : M^{(1)}(d') = M(d'))` (ASN-0047) applied to `d_op ≠ d_new` — the inequality holds because V1 places `d_new ∉ E_doc` pre-fork while `d_op ∈ E_doc` pre-fork, as J4's precondition requires `d_op ∈ E_doc`); new V-positions satisfy S8a (all components positive, by S8a applied at `d_op`) and S8-depth (common depth `m_{s_C}`); `dom(M^{(2)}(d_new))` finite (subset of `dom(M(d_op))` which is finite by S8-fin); `M^{(2)}(d_new)` satisfies D-CTG★ (the inherited positions form `V_{s_C}(d_op) = {[s_C, 1, ..., 1, k] : 1 ≤ k ≤ n_{s_C}}` per D-SEQ★, contiguous by construction) and D-MIN★ (minimum is `[s_C, 1, ..., 1]`); newly added V-positions are pairwise distinct (they are pairwise distinct in `V_{s_C}(d_op)`). The K.μ⁺ amendment of ASN-0047 requires `subspace(v) = s_C` for all new V-positions, which holds throughout. Strict extension: `V_{s_C}(d_op) ≠ ∅` by the non-empty-source case hypothesis governing this branch of V0.

Effect: `M^{(2)}(d_new)(v) = M(d_op)(v)` for `v ∈ V_{s_C}(d_op)`. Frame: `C^{(2)} = C`, `L^{(2)} = L`, `E^{(2)} = E^{(1)}`, `M^{(2)}(d') = M^{(1)}(d')` for `d' ≠ d_new`, `R^{(2)} = R^{(1)} = R`.

*K.ρ × n at Σ^{(2)}, n = |ran(M^{(2)}(d_new))|.* The K.ρ phase consists of `n` elementary K.ρ invocations, each recording one `(aⱼ, d_new)` pair. Enumerate `ran(M^{(2)}(d_new)) = {a₁, ..., a_n}` (finite by S8-fin applied to `dom(M^{(2)}(d_new))`; image of a finite set under a function is finite). The composite proceeds through `n` sequential elementary K.ρ steps: at step `j` (for `1 ≤ j ≤ n`), K.ρ at intermediate state `Σ^{(1+j)}` records `(aⱼ, d_new)` producing `Σ^{(1+j+1)} = Σ^{(2+j)}`. At step `j`, the K.ρ precondition (ASN-0047) is `aⱼ ∈ dom(C^{(1+j)})` and `d_new ∈ E^{(1+j)}_doc`. The content store is preserved by K.ρ's frame condition at each prior step (`C^{(1+j)} = C^{(1+j-1)} = ... = C^{(2)} = C` by induction on `j`), so `aⱼ ∈ dom(C^{(1+j)}) ⟺ aⱼ ∈ dom(C)`; the latter holds because `aⱼ ∈ ran(M^{(2)}(d_new))` and S3★ (content-subspace restriction, ASN-0047) at `M^{(2)}(d_new)` (from K.μ⁺'s postcondition) gives `ran(M^{(2)}(d_new)) ⊆ dom(C^{(2)}) = dom(C)`. Similarly, `d_new ∈ E^{(1+j)}_doc` holds because K.ρ's frame preserves E, so `E^{(1+j)} = E^{(2)} = E^{(1)}`, and `d_new ∈ E^{(1)}_doc` from the K.δ effect. Each elementary K.ρ step satisfies its precondition.

Cumulative effect across the `n` K.ρ steps: `R^{(2+n)} = R^{(2)} ∪ {(aⱼ, d_new) : 1 ≤ j ≤ n} = R ∪ {(a, d_new) : a ∈ ran(M^{(2)}(d_new))}`. Frame: `C^{(2+n)} = C`, `L^{(2+n)} = L`, `E^{(2+n)} = E^{(2)}`, `M^{(2+n)} = M^{(2)}`.

*Coupling at (Σ, Σ^{(2+n)}).* J0 holds vacuously: `dom(C^{(2+n)}) \ dom(C) = ∅`. J1★ holds because every `a` with `(E v ∈ dom(M^{(2+n)}(d_new)) : subspace(v) = s_C ∧ M^{(2+n)}(d_new)(v) = a)` had `(a, d_new)` recorded by some K.ρ step (the K.ρ enumeration ranges over all of `ran(M^{(2)}(d_new))`, which is exactly the content-subspace range by V6). J1'★ holds because every `(a, d) ∈ R^{(2+n)} \ R` was added by some K.ρ step with `d = d_new` and `a ∈ ran(M^{(2)}(d_new))`, satisfying the range-based content-subspace scoping.

The composite is a valid composite under ValidComposite★. ∎

*K.δ-alone composite verification (empty-source case, V7's extension).* When `V_{s_C}(d_op) = ∅`, V7 reduces V0 to a single elementary K.δ step — no K.μ⁺ phase, no K.ρ phase — and the composite is `Σ → Σ^{(1)}`. We verify ValidComposite★ for this shape directly. The K.δ precondition is the same as in the non-empty case (sub-case A for first fork, sub-case B for subsequent fork), and the discharge above is independent of `V_{s_C}(d_op)`'s emptiness — `d_src ∈ E_doc` and the ChildSpawnFreshness/FrontierEquivalence/P1/P8/K.δ-ID.parent-0/1/K.δ-ID.zeros-0/1/T10a.4 arguments all carry through unchanged. So K.δ's elementary precondition holds at `Σ`. *Coupling at (Σ, Σ^{(1)}).* J0 holds vacuously: K.δ's frame gives `C^{(1)} = C`, so `dom(C^{(1)}) \ dom(C) = ∅` and J0's antecedent is unsatisfiable. J1★ holds vacuously: K.δ's effect sets `M^{(1)}(d_new) = ∅`, so for `d = d_new` no `v ∈ dom(M^{(1)}(d_new))` exists, and the existential antecedent of J1★ is unsatisfiable for `d_new`; for every `d ≠ d_new`, K.δ's frame gives `M^{(1)}(d) = M(d)`, so no `a` is in `ran(M^{(1)}(d)) \ ran(M(d))`, and the antecedent is again unsatisfiable. J1'★ holds vacuously: K.δ's frame gives `R^{(1)} = R`, so `R^{(1)} \ R = ∅` and J1'★'s antecedent is empty. All three coupling constraints are satisfied vacuously at `(Σ, Σ^{(1)})`. The K.δ-alone composite is therefore a valid composite under ValidComposite★. ∎

## Worked Example

Let `d_src ∈ E_doc` with content-subspace depth `m_{s_C} = 2` and arrangement `M(d_src)`:

```
V-position    I-address
[s_C, 1]      a₁
[s_C, 2]      a₂
[s_C, 3]      a₃
```

where `a₁, a₂, a₃ ∈ dom(C)` with `origin(a₁) = origin(a₂) = origin(a₃) = d_src`. Suppose `d_src` also has a link-subspace V-position `[s_L, 1] ↦ ℓ` with `origin(ℓ) = d_src` (by CL-OWN).

A fork of `d_src` produces `d_new = inc(d_src, 1)`.

*Identity (V1).* `d_new` is a fresh tumbler with `zeros(d_new) = 2` (so `Document`), with `d_src ≼ d_new` (V2).

*Content (V3).* `C' = C`. No new I-address is allocated. `dom(C')` is exactly `dom(C)`.

*Arrangement (V4, V6).* `M'(d_new)` is:

```
V-position    I-address
[s_C, 1]      a₁
[s_C, 2]      a₂
[s_C, 3]      a₃
```

The link subspace of `d_new` is empty: `V_{s_L}(d_new) = ∅`. The link `ℓ` remains in `d_src`'s arrangement at `[s_L, 1]`, with `origin(ℓ) = d_src` still satisfied.

*Source isolation (V5).* `M'(d_src) = M(d_src)`. `d_src`'s arrangement is unchanged, including its link-subspace position.

*Provenance (V9).* `R' = R ∪ {(a₁, d_new), (a₂, d_new), (a₃, d_new)}`.

*Correspondence (V8).* At each `v ∈ {[s_C, 1], [s_C, 2], [s_C, 3]}`, `M'(d_src)(v) = M'(d_new)(v)` — the inherited I-address at each shared content-subspace V-position is equal in source and fork. Reading this equality pointwise across the three positions yields the intercomparison alignment `(v_src, v_new, length) = ([s_C, 1], [s_C, 1], 3)` — source V-position equal to fork V-position over a run of three pointwise-corresponding positions — directly from I-address equality (V8), with no comparison operation required of the storage layer. This alignment is a cross-document V-position correspondence: its first two slots are V-positions, distinguishing it from an S8/S8★ correspondence run, whose middle slot is an I-address.

*Link discoverability (V6a).* By V6a(i), `Σ'.L(ℓ) = Σ.L(ℓ)` across the fork composite, so `ℓ`'s endset structure persists. Querying "which links reference `a₁`?" returns `ℓ` (assuming `a₁ ∈ coverage(Σ.L(ℓ).eᵢ)` for some slot `i`, hypothetically), and this answer is the same whether we ask from `d_src`'s vantage or `d_new`'s vantage. From `d_src`'s vantage: by V6a(ii), `project(ℓ, i, d_src, Σ') = project(ℓ, i, d_src, Σ)`, so any pre-fork witness in `d_src` (e.g., the V-position `[s_C, 1]` whose image `a₁` lies in coverage) remains a post-fork witness, and `discoverable_from(ℓ, d_src, Σ')` holds. From `d_new`'s vantage: by V6a(iii), every `v ∈ project(ℓ, i, d_src, Σ) ∩ V_{s_C}(d_src)` also lies in `project(ℓ, i, d_new, Σ')` — in particular, `[s_C, 1] ∈ project(ℓ, i, d_new, Σ')` if the hypothetical pre-fork witness applied, so `discoverable_from(ℓ, d_new, Σ')` holds.

*Subsequent edits.* Suppose `d_src`'s owner later deletes `[s_C, 3]` from `d_src`'s arrangement via a K.μ⁻ contraction with `n'_{s_C} = 2` — retaining the suffix-prefix `{[s_C, 1], [s_C, 2]}`, as required by K.μ⁻'s per-subspace retention semantics (ASN-0047) and D-CTG★. A middle-only deletion such as removing `[s_C, 2]` while keeping `[s_C, 3]` is not expressible as a K.μ⁻ at all. By V5a Corollary 1 applied at `d* = d_new` to a single-step sequence consisting of this K.μ⁻ (M-targeted at `d_src ≠ d_new`), `M(d_new)` is unaffected — `a₃` remains in `d_new`'s arrangement. By V12(c), `(a₃, d_new) ∈ R` persists; by V12(b), `a₃ ∈ dom(C)` persists. Symmetrically, if `d_new`'s owner deletes from `d_new`'s arrangement, V5a Corollary 1 applied at `d* = d_src` gives that `d_src` is unaffected.

*Further forking — fork of a fork (V11 chain case).* A fork of `d_new` (chained from the original fork of `d_src`, so `d_new` plays the role of `d¹_new` in V11's chain notation) produces `d²_new = inc(d_new, 1)` with `d_src ≼ d_new ≼ d²_new` (V11a). Here `d²_new` is *chain* notation — the second link in a fork chain, of length `#d_src + 2`. The I-addresses inherited by `d²_new` are still `a₁, a₂, a₃` — the same I-addresses originally allocated by `d_src` (V11).

*Subsequent fork of `d_src` — V1's `k = 0` sub-case (V10 sibling case).* Returning to the state after the first fork of `d_src` (with `d_new` having been allocated as `inc(d_src, 1)`, so `d_new` plays the role of `d_new¹` in V10's sibling notation), suppose the operator now forks `d_src` again. V1's subsequent-fork sub-case applies: `A_v(d_src)`'s most recent emission is `d_new`, so the new fork is `d_new² = inc(d_new, 0)`. The sibling-notation `d_new²` distinguishes this second sibling fork of `d_src` — of length `#d_src + 1`, parent `d_src` in the version sub-allocator — from any chain notation; in particular, `d_new² ≠ d²_new` of the prior paragraph (which has length `#d_src + 2` and parent `d_new` in its sub-allocator). By K.δ-ID.parent-0/1, `parent(d_new²) = parent(d_new) = parent(d_src)`. By V2 applied at this second fork — whose inductive argument we walked through in §"Identity by Sub-Allocation" — `d_src ≼ d_new²`. We can verify directly: by TA5(c) `#d_new² = #d_new = #d_src + 1`; by TA5(b) at `k = 0`, `d_new²` agrees with `d_new` at every position except `sig(d_new) = #d_new`; combined with the base-case agreement `d_new_i = d_src_i` for `1 ≤ i ≤ #d_src`, the positions `1 ≤ i ≤ #d_src` satisfy `(d_new²)_i = (d_new)_i = (d_src)_i`, and `#d_src ≤ #d_new²` since `#d_new² = #d_src + 1`. The Prefix definition then gives `d_src ≼ d_new²`.

V10(a) holds concretely: both `d_new = inc(d_src, 1)` and `d_new² = inc(d_new, 0)` have length `#d_src + 1` (the first by TA5(d) at `k = 1`, the second by TA5(c) at `k = 0` inheriting `d_new`'s length), so they share a length — both extend `d_src` by exactly one component — and differ in that single trailing component (TA5(c) at the subsequent fork modifies position `sig(d_new) = #d_new` only — incrementing `d_new`'s final `1` to `2` — so `(d_new²)_{#d_new} = 2 ≠ 1 = (d_new)_{#d_new}`). The two siblings are distinct addresses sharing the same parent prefix `d_src`. V10(b) and V10(c) apply with `Σ¹` (the post-first-fork state) as the pre-state of the second fork. Because `d_new²` is a *subsequent* fork of `d_src`, its J4 content source operand is not `d_src` but the most recent prior version, `d_op² = d_new` (= `inc(d_src, 1)`); so `M²(d_new²)` inherits from `M(d_new)`, not `M(d_src)`. It is populated with `{[s_C, 1] ↦ a₁, [s_C, 2] ↦ a₂, [s_C, 3] ↦ a₃}` precisely when `d_new` (the prior version) has not been edited since its own creation — for then `M(d_new) = M(d_src)|_{V_{s_C}(d_src)}` still holds the three inherited I-addresses. (Had the operator instead edited `d_new` before this fork, `M²(d_new²)` would track `d_new`'s edited arrangement, not `d_src`'s.) The records `R² ⊇ R¹ ∪ {(a₁, d_new²), (a₂, d_new²), (a₃, d_new²)}` are disjoint from the analogous `(aᵢ, d_new)` records added by the first fork; by V12(d) the corresponding source-side records here are `(aᵢ, d_op²) = (aᵢ, d_new)`.

*Empty source (V7).* Consider a separate document `d_src°` with `V_{s_C}(d_src°) = ∅` — a freshly produced CREATENEWDOCUMENT result with no content yet inserted. A fork of `d_src°` triggers V7's extension of J4: the composite reduces to K.δ alone, with no K.μ⁺ and no K.ρ phases. The fork produces `d_new° = inc(d_src°, 1)` (V1's first-fork sub-case; V1 imposes no precondition on source content), with `Document(d_new°)` and `d_src° ≼ d_new°` (V2). The K.δ effect on `Document(e)` initialises `M'(d_new°) = ∅` directly. Since the K.ρ phase does not fire, no `(a, d_new°)` pair is added to `R`: `R' = R`. V9's universal quantifier `(A a : a ∈ ran(M'(d_new°)) : (a, d_new°) ∈ R')` ranges over the empty set `ran(M'(d_new°)) = ∅` and is satisfied vacuously; V12(c) and V12(d) likewise quantify over the empty range and hold vacuously. V12(a) — joint permanence of the two entities — holds substantively: `d_src° ∈ E'_doc` (K.δ's E-frame `E^{(1)} = E ∪ {d_new°}` preserves `E ⊆ E^{(1)}`; P1; the K.δ-alone composite has `Σ' = Σ^{(1)}`, so this is also the post-composite state) and `d_new° ∈ E'_doc` (V1) persist into every subsequent state by T8 and P1. The empty fork is itself a first-class document; a later K.μ⁺ on `d_new°` (with content drawn from K.α invocations under `A_C(d_new°)`) populates `V_{s_C}(d_new°)` without any reference to `d_src°`'s arrangement, and the two documents proceed independently. The branching is on content-subspace emptiness alone — V7's predicate `V_{s_C}(d_op) = ∅` is independent of `V_{s_L}` — so a source carrying a non-empty *link* subspace forks identically: its links are preserved on the source by V5 (`L' = L`, since no K.λ or K.μ⁺_L step fires) and contribute nothing to the fork, whose link subspace stays empty by V6.

## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| V0 | FORK composite: K.δ + K.μ⁺ + K.ρ × n (n = `|ran(M'(d_new))|`), or K.δ alone in the empty-source case (V7's extension of J4); produces new document inheriting source's content-subspace arrangement | introduced |
| V1 | `d_new ∈ E'_doc`, `d_new ∉ E_doc`, `parent(d_new) = parent(d_src)`, with `d_new` = `A_v(d_src)`'s next emission: `inc(d_src, 1)` on first fork, `inc(d_prev, 0)` on subsequent fork | introduced |
| V2 | `d_src ≼ d_new` — prefix-encoded ancestry recoverable from `d_new`'s tumbler | introduced |
| V3 | `C' = C` — fork allocates no new content | introduced |
| V3a | `{a ∈ dom(C') : origin(a) = d'} = {a ∈ dom(C) : origin(a) = d'}` for every `d'` — allocation invariance | introduced |
| V4 | `(A v ∈ V_{s_C}(d_op) :: v ∈ dom(M'(d_new)) ∧ M'(d_new)(v) = M(d_op)(v))` — literal arrangement inheritance from the content source operand `d_op` (`= d_src` on first fork, `= d_prev` on subsequent fork) | introduced |
| V4b | `dom(M'(d_new)) = V_{s_C}(d_op)` and `V_{s_C}(d_new) = V_{s_C}(d_op)` — domain equality (exact, not just one-sided containment) | introduced |
| V5 | `M'(d_src) = M(d_src)` — source arrangement isolated from fork | introduced |
| V5a | Per-document arrangement independence: a sequence with no step M-targeted at `d*` preserves `M(d*)` (with per-step and per-sequence clauses and source-isolation / pairwise-independence corollaries) | introduced |
| V6 | `V_{s_L}(d_new) = ∅` in the post-fork state — link subspace not inherited (forced by CL-OWN) | introduced |
| V6a | Link discoverability inheritance: the link store, the source's projection, and the fork's content-subspace-restricted projection are all preserved across the fork composite | introduced |
| V7 | Empty-source behavior: fork of `d_src` with `V_{s_C}(d_op) = ∅` reduces to K.δ alone, succeeding with `M'(d_new) = ∅` and `R' = R` | introduced |
| V8 | `(A v ∈ V_{s_C}(d_op) :: M'(d_op)(v) = M'(d_new)(v))` — structural correspondence at fork-time between the content source `d_op` and the fork (`d_op = d_src` on first fork) | introduced |
| V8c | Correspondence is symmetric and document-type-untyped | introduced |
| V9 | `(A a : a ∈ ran(M'(d_new)) : (a, d_new) ∈ R')` — provenance recorded for every inherited I-address | introduced |
| V9a | Provenance records containment, not derivation path — content origin and fork-tree lineage are reconstructable from I-addresses and prefix structure, but the per-address acquisition path is neither stored nor reconstructable | introduced |
| V9b | Fresh forks inherit only externally-allocated I-addresses: for every `(a, d_new) ∈ R'` recorded by a fork, `origin(a) ≠ d_new` | introduced |
| V10 | Sibling forks of the same source are independent in identity, arrangement, and provenance | introduced |
| V10a | Each fork derives from `M(d_op)` of its content source operand *at the moment of forking* — time-sensitivity | introduced |
| V11 | Transitive identity along unedited fork chains: for every fork chain `d_src → d¹_new → ... → d^k_new` starting from initial state `Σ`, where each step is the first fork of its immediate source (so step `i`'s content operand `d_op = d^{i-1}_new`) and each step's source has its content-subspace arrangement (set and pointwise values) unchanged between the prior step's post-state and the current step's pre-state, `v ∈ dom(M^k(d^k_new))` at post-step-k and `M^k(d^k_new)(v)` at post-step-k equals `M(d_src)(v)` at `Σ`, for every `v ∈ V_{s_C}(d_src)` evaluated at `Σ` | introduced |
| V11a | Prefix relation chains: `d_src ≼ d¹_new ≼ ... ≼ d^k_new` — ancestry composition recoverable from tumbler structure | introduced |
| V12 | Joint permanence of source, fork, inherited I-addresses, and provenance records across all subsequent states | introduced |

## Dependency Audit

The inquiry declares `depends: [34, 36, 40, 47]`. ASN-0034 (Tumbler Algebra), ASN-0036 (Strand Model), and ASN-0047 (Transition Model) are each consumed.

ASN-0040 (Tumbler Baptism) has no use site. The baptism vocabulary (`Σ.B`, `next`, `hwm`, `baptize`, B0–B10) does not appear anywhere in this ASN; entity allocation and frontier advancement are sourced from ASN-0047 and ASN-0034 instead. ASN-0040 is flagged for removal from this inquiry's `depends:` set.

## Open Questions

What must the system guarantee when a fork is invoked while the source's arrangement is being concurrently modified — beyond what the sequential atomic transition axiom supplies?

Under what conditions must a fork operation be discoverable from the source's vantage — i.e., must the source's owner be able to enumerate all descendants of their document, and within what time bound?

What invariants must distinguish a *snapshot* fork (whose inherited arrangement is frozen at fork-time) from a *living* fork (whose inherited V-positions reflect the source's current arrangement), if the abstract specification is to admit both as valid implementations?

What must remain true about the fork operation when the source document is itself a transcludent — i.e., when `M(d_src)` references I-addresses with `origin ≠ d_src`?

Under what conditions can the size of a fork's arrangement be bounded relative to the source's, without exhaustive enumeration of `V_{s_C}(d_src)`?

What invariants must hold over the set of all forks ever produced from a single source, if the version space is to be presented as a coherent collection rather than as independent siblings?

What must the system guarantee about correspondence under the special case where the fork operation is applied with the source equal to its own previous fork — i.e., forks of forks within a single editorial session?

Under what conditions does the V-stream depth of the fork's arrangement match the source's, and what must hold when they differ — for instance, if the fork operation is allowed to renumber inherited V-positions for compactness?

What invariants must hold when a fork is followed immediately by deletion of content from the source — must the fork's inherited arrangement remain referentially valid, and through what mechanism?

What additional structure must the system provide to relate independently-typed but textually identical content across documents — counterpart correspondence that I-address identity alone, which assigns such content distinct addresses, cannot express?

What must distinguish two distinct I-addresses holding equal byte values, if the specification is to treat them as non-identical content rather than collapse them by value?
