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

## Identity by Sub-Allocation

We begin with `d_new`. The system already has an apparatus for allocating tumblers under the version sub-allocator of `d_src`: T10a's allocator discipline and ASN-0047's K.δ. For a document's versions, the producing allocator is `A_v(d_src)` (ASN-0047's Allocator hierarchy), which emits its first output via K.δ case (ii) at `k = 1` — `inc(d_src, 1)`, by TA5(d) appending a single non-zero component — and emits each subsequent output via K.δ case (ii) at `k = 0` — `inc(d_prev, 0)`, by TA5(c) preserving length while advancing the trailing component. We establish `IsDocument(d_new)` in both cases by induction on `A_v(d_src)`'s emission count — parallel to V2's structural-ancestry induction below. KDeltaZerosK01 (ASN-0047) preserves zeros at both `k = 0` and `k = 1`, but preservation alone does not establish `zeros(d_new) = 2`; the induction supplies the input value `zeros(input) = 2` that KDeltaZerosK01 then carries through.

*Base case (first fork).* `zeros(d_src) = 2` because `d_src ∈ E_doc` (V0's precondition). KDeltaZerosK01 at `k = 1` gives `zeros(d_new) = zeros(d_src) = 2`, hence `IsDocument(d_new)`.

*Inductive step (subsequent fork).* The induction hypothesis is that `A_v(d_src)`'s most recent prior emission `d_prev` satisfies `IsDocument(d_prev)`, so `zeros(d_prev) = 2`. `d_prev ∈ E_doc` is preserved across all intermediate states by P1 (entity permanence, ASN-0047) applied to its prior K.δ event, so `d_prev ∈ E_doc` at the state of the current fork. KDeltaZerosK01 at `k = 0` then gives `zeros(d_new) = zeros(d_prev) = 2`, hence `IsDocument(d_new)`. ∎

We establish `parent(d_new) = parent(d_src)` by the same form of induction on `A_v(d_src)`'s emission count. KDeltaParentK01 (ASN-0047) supplies the per-step relation `parent(inc(t, k)) = parent(t)` for `k ∈ {0, 1}`; the induction chains this per-step preservation across `A_v(d_src)`'s emission count to recover `parent(d_src)` from any emission. The first-emission step uses `k = 1` and reaches `parent(d_src)` directly; each subsequent sibling-stream step uses `k = 0` and reaches `parent(d_prev)`, which the inductive hypothesis identifies with `parent(d_src)`.

*Base case (first fork).* `d_new = inc(d_src, 1)`. KDeltaParentK01 at `k = 1` gives `parent(d_new) = parent(d_src)` directly.

*Inductive step (subsequent fork).* The induction hypothesis is that `A_v(d_src)`'s most recent prior emission `d_prev` satisfies `parent(d_prev) = parent(d_src)`. The current emission is `d_new = inc(d_prev, 0)`. KDeltaParentK01 at `k = 0` gives `parent(d_new) = parent(d_prev)`. Composing with the induction hypothesis: `parent(d_new) = parent(d_prev) = parent(d_src)`. ∎

We make explicit:

> **V1** (*new-version identity*): A fork of `d_src` produces a new entity `d_new` allocated as `A_v(d_src)`'s next emission per the Allocator hierarchy (ASN-0047):
>
> - *First fork of `d_src`* (when `A_v(d_src)` has emitted no prior version): `d_new = inc(d_src, 1)`, produced by K.δ case (ii) with `k = 1`, `t = d_src`.
> - *Subsequent fork of `d_src`* (when `A_v(d_src)` has prior emissions with most recent `d_prev`): `d_new = inc(d_prev, 0)`, produced by K.δ case (ii) with `k = 0`, `t = d_prev`.
>
> In either case `d_new ∈ E'_doc`, `d_new ∉ E_doc` (pre-fork), `IsDocument(d_new)` (by the IsDocument induction above on `A_v(d_src)`'s emission count, which combines KDeltaZerosK01's zero-preservation at `k = 0` and `k = 1` with P1-supplied membership `d_prev ∈ E_doc` at every inductive step), and `parent(d_new) = parent(d_src)` (by the parent-equality induction above on `A_v(d_src)`'s emission count, which combines KDeltaParentK01's per-step preservation at `k ∈ {0, 1}` with the inductive hypothesis `parent(d_prev) = parent(d_src)` at every subsequent-emission step). The new entity inherits the source's account-level prefix while extending into a fresh sub-tumbler.

V1's two cases stand in different relations to J4 of ASN-0047. The *first-fork sub-case* — `d_new = inc(d_src, 1)` produced by K.δ case (ii) with `k = 1`, `t = d_src` — is exactly J4's clause (i) as written: K.δ case (ii) with k = 1 and t = d_src, producing `d_new = inc(d_src, 1)` with `d_new ∉ E_doc`. The *subsequent-fork sub-case* — `d_new = inc(d_prev, 0)` produced by K.δ case (ii) with `k = 0`, `t = d_prev` — is an extension of J4: J4's clause (i) names only the first-fork shape and does not contemplate sibling-stream advancement on `A_v(d_src)`'s frontier. We frame V1's subsequent-fork case as an *extension* of J4, parallel to V7's empty-source extension: this ASN's fork operation V0 admits both first-fork and subsequent-fork shapes, dispatching on whether `A_v(d_src)` has prior emissions. The basis for admitting the subsequent-fork shape is ASN-0047's Allocator hierarchy convention for `A_v(d_src)` — first emission `inc(d_src, 1)`, subsequent emissions `inc(prev_version, 0)` — which J4's clause (i) tacitly invokes for the first emission but does not exhaust. The deviation is explicit and intentional; J4's clauses (ii) and (iii) (the K.μ⁺ and K.ρ phases) continue to apply unchanged to the subsequent-fork sub-case.

Two consequences follow without further machinery.

*Structural ancestry.* We derive `d_src ≼ d_new` by induction on `A_v(d_src)`'s emission count.

*Base case (first fork).* `d_new = inc(d_src, 1)`. By TA5(b) at `k = 1 > 0`, every component of `d_src` is preserved: `(A i : 1 ≤ i ≤ #d_src : (d_new)_i = (d_src)_i)`. By TA5(d), `#d_new = #d_src + 1`, so `#d_src ≤ #d_new`. By the Prefix definition (ASN-0034), `d_src ≼ d_new`.

*Inductive step (subsequent fork).* Suppose `d_src ≼ d_prev`, where `d_prev` is `A_v(d_src)`'s most recent prior emission. Then `d_new = inc(d_prev, 0)`. By TA5(b) at `k = 0`, agreement holds at every position of `d_prev` except `sig(d_prev)`: `(A i : 1 ≤ i ≤ #d_prev ∧ i ≠ sig(d_prev) : (d_new)_i = (d_prev)_i)`. By T10a.4 (T4PreservationUnderDiscipline, ASN-0034), every `A_v(d_src)` output is T4-valid, so `d_prev` is T4-valid; by TA5-SigValid (ASN-0034), `sig(d_prev) = #d_prev`. The modified position is therefore the last position of `d_prev`. By TA5(c), `#d_new = #d_prev`. We observe that every `A_v(d_src)` output has length exactly `#d_src + 1`, by a *nested induction* on `A_v(d_src)`'s emission count — distinct from V2's outer induction (whose inductive goal is the prefix relation `d_src ≼ ·`, while the inner goal here is the length equation `#· = #d_src + 1`), though indexed over the same enumeration of `A_v(d_src)`'s outputs. *Inner base case (first emission of `A_v(d_src)`).* `inc(d_src, 1)` has length `#d_src + 1` by TA5(d) at `k = 1`. *Inner inductive step (subsequent emission).* The inner induction hypothesis is that the prior emission has length `#d_src + 1`; the next emission via `inc(·, 0)` preserves length by TA5(c), so it also has length `#d_src + 1`. The nested induction closes. In particular `#d_prev = #d_src + 1 > #d_src`. The modified position `sig(d_prev) = #d_prev` therefore exceeds `#d_src`. For positions `1 ≤ i ≤ #d_src`: agreement gives `(d_new)_i = (d_prev)_i` (since `i ≤ #d_src < #d_prev = sig(d_prev)`), and the induction hypothesis gives `(d_prev)_i = (d_src)_i`. Composing: `(d_new)_i = (d_src)_i` for `1 ≤ i ≤ #d_src`. With `#d_src ≤ #d_new` (since `#d_new = #d_prev > #d_src`), the Prefix definition gives `d_src ≼ d_new`. ∎

The source's tumbler is a prefix of the fork's tumbler. We name this so that downstream users of the operation can rely on it as a structural property of the operation itself, not as a metadata field that could fall out of sync.

> **V2** (*prefix-encoded ancestry*): `d_src ≼ d_new` under the tumbler prefix order. The ancestry relationship is recoverable from `d_new`'s tumbler alone by truncating the trailing extension component; no separate lineage table is consulted.

*Address uniqueness.* The producing allocator of `inc(d_src, 1)` is the *version sub-allocator* `A_v(d_src)` defined in ASN-0047's Allocator hierarchy — not the document sub-allocator of any account. By the hierarchy definition, `A_v(d_src)` is associated with `d_src` itself and produces its first emission `inc(d_src, 1)`, with subsequent emissions `inc(prev_version, 0)`. By T10a.6 (DomainDisjointness, ASN-0034), `A_v(d_src)`'s domain is disjoint from every other allocator's domain. The K.δ precondition `e ∉ E` (uniformly required for all sub-cases) forces `d_new` to be a fresh tumbler. No future fork — of `d_src` or any other document — can re-use this address. Combined with T8 (AllocationPermanence, ASN-0034), once `d_new` enters `E`, it remains in `E` for all subsequent reachable states. The identity is permanent.

We pause to record what V1 and V2 do *not* yet claim. They do not establish that `d_new` carries any content; that is the work of K.μ⁺. They do not establish any relationship between the source's V-stream and the fork's V-stream; that is the work of the content-sharing argument below. They do not establish that the source is unaffected by the creation; that is a frame condition we will discharge separately. The identity argument is structurally independent of all of these. K.δ creates an empty-arrangement document; the fork's arrangement starts empty (the `IsDocument(e)` effect clause of K.δ sets `M'(d_new) = ∅`).

This last point matters: an alternative implementation could fork by performing only K.δ and producing an empty new document. That would satisfy V1, V2, and the basic identity guarantees. What that implementation would *lack* is the inherited content that makes the fork meaningfully a *version of* something. The arrangement-extension phase is what supplies the inheritance, and we turn to it next.

## Sharing, Not Duplication

The K.μ⁺ phase populates `M'(d_new)`. The question is what V-to-I mappings it installs. There are two candidate disciplines:

- *Duplication.* For every `v ∈ V_{s_C}(d_src)`, allocate a fresh I-address `a' ∈ dom(C')` with `C'(a') = C(M(d_src)(v))`, and set `M'(d_new)(v') = a'` for a corresponding fresh V-position `v'`.

- *Transclusion.* For every `v ∈ V_{s_C}(d_src)`, set `M'(d_new)(v') = M(d_src)(v)` directly — the same I-address that `d_src`'s arrangement holds.

The duplication discipline contradicts Nelson's central design commitment. It produces two distinct I-addresses for the same byte, severing the connection to origin: `origin(a') = d_new` rather than `origin(a)`, and the system has no way to recognize the fragment as derived from `d_src`. Royalty splits collapse; link survivability fails; intercomparison cannot distinguish "derived from" from "happened to look the same." Most concretely, duplication forces a K.α step for every byte, which the foundation's J0 (AllocationRequiresPlacement) requires to be paired with placement, but which produces an extensional state that no longer agrees with the source on identity.

Transclusion preserves identity. The new arrangement references the source's I-addresses; the content store grows by nothing. Every property that depends on I-address identity — origin attribution (S7, ASN-0036), link discoverability via shared addresses, royalty distribution, version intercomparison — is automatic.

J4's defining clause makes the discipline explicit:

> "K.μ⁺ populating `M'(d_new)` from `d_src`'s content subspace under transclusion: `ran(M'(d_new)) ⊆ ran(M(d_src)|_{V_{s_C}(d_src)})` — no new content addresses are introduced, every target lies in the pre-existing content store." [ASN-0047 J4]

We promote the content-sharing consequence to a named property:

> **V3** (*content-store invariance*): A fork produces no new content. `C' = C` and `dom(C') = dom(C)`.

The derivation is mechanical. By the elementary decomposition of the fork composite into K.δ + K.μ⁺ + K.ρ (and, in the empty case, just K.δ), no step allocates content. K.δ's frame condition includes `C' = C`; K.μ⁺'s frame condition includes `C' = C`; K.ρ's frame condition includes `C' = C`. By the conjunction of these elementary frames, the composite preserves `C`.

The consequence is that I-address allocation is unaffected by forking. The content sub-allocator of `d_src` (`A_C(d_src)` of ASN-0047) does not advance; its next emission after a fork is the same tumbler as before the fork. The content sub-allocator of `d_new` is freshly activated by K.δ (SubAllocatorAxiom, ASN-0047) and stands at its first emission, ready for future K.α invocations into `d_new`.

> **V3a** (*allocation invariance*): For every document `d'`, the set of I-addresses allocated under `d'` is unchanged by forking: `{a ∈ dom(C') : origin(a) = d'} = {a ∈ dom(C) : origin(a) = d'}`. *Derivation.* `dom(C') = dom(C)` by V3; the origin function depends only on the I-address (S7, ASN-0036). ∎

We observe an implementation distinction worth recording. Gregory's `docreatenewversion` allocates fresh POOM nodes for the new version's V→I mapping tree, deep-copying the tree structure (consultation answer 10). The POOM is a representation of the partial function `M`, not the function itself. Two distinct trees representing the same partial function are *the same M* by S2 (ArrangementFunctionality, ASN-0036) — functional equality is by graph. The deep-copy versus shared-tree question is internal to the implementation of `M`; the abstract claim — V3 — is the same either way. An alternative implementation could share tree structure with copy-on-write and still satisfy V3 unchanged.

## The Arrangement Layer

We now characterize `M'(d_new)`. The fork populates it from `d_src`'s content-subspace arrangement.

Let `V_{s_C}(d) = {v ∈ dom(M(d)) : subspace(v) = s_C}` denote the content-subspace V-positions of `d` (ASN-0047). By D-SEQ★ (ASN-0047), when `V_{s_C}(d_src) ≠ ∅`, `V_{s_C}(d_src) = {[s_C, 1, ..., 1, k] : 1 ≤ k ≤ n_{s_C}}` for some `n_{s_C} ≥ 1`, with all positions sharing a common depth `m_{s_C}` (S8-depth, ASN-0036).

The fork installs the source's content-subspace V-positions and their I-addresses into `M'(d_new)`. The discipline we commit to here — *literal inheritance*: the same V-positions and the same I-addresses appear in `M'(d_new)` as in `M(d_src)|_{V_{s_C}(d_src)}` — is a design commitment of this ASN, not a derivation from J4's clause (ii) alone. (J4's clause (ii) constrains the *range* of `M'(d_new)`; the *domain* and *pairing* are left open, and the literal-inheritance form is one admissible discipline among several. The structural justification for this choice — and the alternatives ruled out — appears immediately after V4's statement below.) We name the commitment as V4 and then derive what follows from it.

> **V4** (*arrangement inheritance — design commitment*): After any fork of `d_src`, the new document's content-subspace arrangement satisfies:
>
> `(A v ∈ V_{s_C}(d_src) :: v ∈ dom(M'(d_new)) ∧ M'(d_new)(v) = M(d_src)(v))`
>
> V4 holds unconditionally: the formal universal is vacuously true when `V_{s_C}(d_src) = ∅` (V7's empty-source case, where the quantifier ranges over the empty set) and substantively true when `V_{s_C}(d_src) ≠ ∅` (where K.μ⁺ populates `M'(d_new)` from `V_{s_C}(d_src)` per J4's clause (ii)). No precondition on `V_{s_C}(d_src)` is needed; the claim is consistent with the Properties Introduced table entry, which likewise carries no precondition.

V4 makes two distinct claims. First, the *V-positions are inherited literally* — the same tumblers `[s_C, 1, ..., 1, k]` appear in both arrangements, not rebased relative to `d_new`. Second, the *I-addresses at each position are inherited literally* — every `M'(d_new)(v)` equals `M(d_src)(v)`, the same I-address the source holds.

V4 *strengthens* J4's clause (ii). J4 constrains only the *range*: `ran(M'(d_new)) ⊆ ran(M(d_src)|_{V_{s_C}(d_src)})` — every target I-address must come from the source's pre-existing content-subspace mappings, but the *domain* (which V-positions are populated) and the *pairing* (which V-position maps to which I-address) are left unspecified by J4 alone. An implementation satisfying J4 alone could populate `M'(d_new)` at rebased V-positions, with rearranged correspondences, or with only a subset of the source's V-positions, so long as every I-address is drawn from the source's content-subspace range.

V4 commits to *full literal inheritance*: the same V-positions as `d_src`, the same pairing, the entire content-subspace domain. This is a design commitment of this ASN — not derivable from J4 alone. The motivation is twofold. First, V8's structural correspondence (below) requires the same V-positions in both arrangements; without literal V-position inheritance, V8 would collapse into a more elaborate correspondence machinery requiring explicit mapping between source and fork V-spaces. Literal inheritance is the cheapest discipline that supports V8 directly. Second, it matches the natural reading of Nelson's "with the contents of" [LM 4/66] at the moment of forking, and it matches the discipline of every reference implementation we have evidence for.

We note that an alternative ASN could weaken V4 to admit rebased V-positions or rearranged correspondences, provided it strengthened V8 with explicit correspondence tables. Such an ASN would still satisfy J4 of ASN-0047 and the foundation invariants. The choice made here is to keep the correspondence relation structurally implicit in V-position equality.

The literal-inheritance form has two structural justifications.

*Why V-positions are not rebased.* V-positions live in the V-coordinate space of a document. They are tumblers in `T`, structured by S8a (zero-count zero, all components positive) and S8-depth (common depth within a subspace). They do not encode the owning document; the owning document is implicit in `M(d)(v)`'s second argument. Rebasing `[s_C, 1, ..., 1, k]` to anything else would (a) require selecting a target depth/subspace identifier scheme for `d_new` that is no longer comparable to `d_src`, and (b) destroy the structural correspondence that V8 below requires.

*Why I-addresses are not rebased.* I-addresses are permanent — by S7 (StructuralAttribution, ASN-0036), every `a ∈ dom(C)` has a unique `origin(a) ∈ E_doc` extractable from its tumbler. Rebasing would require either changing the I-addresses (impossible by P0/S0) or allocating fresh ones with new origins (which is the duplication discipline ruled out above).

We register the consequence:

> **V4a** (*positional identity*): For every V-position `v ∈ V_{s_C}(d_src)`, both `M(d_src)(v)` and `M'(d_new)(v)` are defined, and both equal the same I-address `a ∈ dom(C)`. The V-position `v` is *the same tumbler* in both arrangements.

V4 gives the one-way containment `V_{s_C}(d_src) ⊆ dom(M'(d_new))`. We now commit to the converse — *no other* V-position enters `dom(M'(d_new))` — as an independent design commitment of this ASN, parallel to V4's. The commitment is not derivable from J4 alone (J4's clause (ii) constrains only the *range* `ran(M'(d_new)) ⊆ ran(M(d_src)|_{V_{s_C}(d_src)})`, leaving the domain and pairing unspecified) and is not derivable from V4 alone (V4's universal quantifier supplies only the one-way containment). It is structurally supported by the fork composite's elementary decomposition: K.δ initialises `M'(d_new) = ∅` (its effect clause when `IsDocument(e)`); the subsequent K.μ⁺ invocation populates `M'(d_new)` with exactly the positions of `V_{s_C}(d_src)` (the design commitment, reified in V0's Effects table below); K.ρ does not modify arrangements. By V6 every position in `dom(M'(d_new))` lies in the content subspace, so:

> **V4b** (*domain equality*): In the post-fork state, `dom(M'(d_new)) = V_{s_C}(d_src)` and `V_{s_C}(d_new) = V_{s_C}(d_src)`. The fork's V-position domain is *exactly* the source's content-subspace V-position set — not merely a superset. V4b is a design commitment of this ASN; V0's Effects table below carries the commitment forward as the primary positional characterisation of `M'(d_new)`, with V4b as the named restatement.

V4a and V4b together are the structural basis of correspondence. We expand their consequences in §"Structural Correspondence" below.

## Frame: Source Isolation

The fork must not modify `d_src`. This is Nelson's most emphatically stated commitment:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals." [LM 2/45]

The argument is by frame composition. K.δ's frame condition (ASN-0047) states that for all documents other than the one being created, `M'(d') = M(d')`. Since the document being created is `d_new`, every `d' ≠ d_new` retains its arrangement; in particular, `d_src ≠ d_new` (by V1, `d_new ∉ E_doc` pre-fork while `d_src ∈ E_doc` pre-fork), so `M'(d_src) = M(d_src)` across the K.δ step. K.μ⁺'s frame condition states that for all documents other than the one being extended, `M'(d') = M(d')`. The document being extended in J4's clause (ii) is `d_new`, so K.μ⁺ leaves `M(d_src)` unchanged. K.ρ's frame condition is `(A d :: M'(d) = M(d))` — provenance recording does not touch arrangements at all.

The composition: across the entire fork composite, `M(d_src)` is unchanged.

> **V5** (*source isolation*): For every fork composite `Σ →* Σ'`: `M'(d_src) = M(d_src)`.

V5 is foundational to the source-fork relationship. It establishes that the source owner's arrangement is unaffected by anyone else's forking activity. They cannot prevent forking (per Nelson's permissionless publishing contract, when applicable), but they incur no observable side effect.

The frame is bidirectional in a sense V5 does not capture but which we record separately. After the fork, subsequent modifications to `M(d_src)` by `d_src`'s owner do not propagate to `M'(d_new)`, and modifications to `M(d_new)` by `d_new`'s owner do not propagate to `M(d_src)`. Each arrangement is owned by its document's owner, and the K.μ⁺ / K.μ⁻ / K.μ~ / K.μ⁺_L transitions of ASN-0047 modify exactly one document's arrangement per invocation. The same per-target frame discipline applies symmetrically to *any* pair of distinct documents, not only the source-fork pair. We formulate the claim at that level of generality so its use sites — source isolation against fork-side edits (here), sibling fork independence (V10(b)), and transitive identity along fork chains (V11) — all consume the same lemma.

> **V5a** (*per-document arrangement independence*): Let `K_M = {K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L}` denote the four arrangement-modifying elementary transition kinds of ASN-0047. Each of these names a unique *target document* `d_target` in its preconditions; we call a transition `Σ → Σ'` *M-targeted at `d_target`* iff it is an instance of some `K ∈ K_M` whose preconditions name `d_target`. Two clauses, one per-step and one per-sequence:
>
> *(a) Per-elementary-transition frame.* For any single elementary transition `Σ → Σ'` and any document `d* ∈ E_doc`: if the transition is M-targeted at some `d_target ≠ d*`, or is any elementary transition that preserves the arrangement of every pre-existing document of `E_doc` (K.α, K.λ, K.ρ unconditionally; K.δ for every `d' ≠ d_new`, which includes every pre-existing `d* ∈ E_doc` since the K.δ outer precondition `e ∉ E` places `d_new ∉ E` pre-step while `d* ∈ E_doc ⊆ E` pre-step), then `M'(d*) = M(d*)`.
>
> *(b) Per-sequence frame.* For any sequence of valid composite transitions `Σ →* Σ'` and any document `d* ∈ E_doc`: if no elementary step of the sequence is M-targeted at `d*`, then `M'(d*) = M(d*)`.
>
> *Derivation.*
>
> *Clause (a).* Each of K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L (ASN-0047) carries the frame condition `(A d' : d' ≠ d_target : M'(d') = M(d'))` for its named target `d_target`; instantiating at `d' = d*` (admissible because the hypothesis fixes `d_target ≠ d*`) gives `M'(d*) = M(d*)`. The four non-arrangement-modifying elementary transitions each carry an `M`-preservation clause covering `d*`: K.α frames `(A d :: M'(d) = M(d))`; K.λ frames `(A d' :: M'(d') = M(d'))`; K.δ frames `(A d' : d' ≠ d_new : M'(d') = M(d'))` for its freshly created `d_new`, and `d_new ≠ d*` because the K.δ outer precondition `e ∉ E` places `d_new ∉ E` pre-step while `d* ∈ E_doc ⊆ E` pre-step; K.ρ frames `(A d :: M'(d) = M(d))`. In every case, `M'(d*) = M(d*)`. ∎(a)
>
> *Clause (b).* Induction on sequence length. *Base* (length 0): `Σ' = Σ` and the conclusion holds trivially. *Step* (`Σ →* Σ_mid → Σ'`): by the induction hypothesis applied to `Σ →* Σ_mid` (no step M-targeted at `d*` by the sequence-level hypothesis), `M_mid(d*) = M(d*)`. The final step `Σ_mid → Σ'` is by assumption either M-targeted at some `d_target ≠ d*` or non-arrangement-modifying; clause (a) applied at this step gives `M'(d*) = M_mid(d*)`. Composing the two equalities: `M'(d*) = M(d*)`. ∎(b)
>
> *Corollary 1 — source–fork isolation.* For `d* = d_src` and any subsequent sequence `Σ' →* Σ''` after the fork in which no step is M-targeted at `d_src`: `M''(d_src) = M'(d_src)`. Symmetric for `d* = d_new`. The original "if the modification targets X" reading specializes to this corollary by restricting attention to sequences whose M-targets all coincide with one of the two documents.
>
> *Corollary 2 — pairwise independence.* For any two distinct documents `d¹, d² ∈ E_doc` and any subsequent sequence `Σ' →* Σ''` in which no step is M-targeted at `d¹`: `M''(d¹) = M'(d¹)`. This is V5a(b) instantiated at `d* = d¹`, and it is the form consumed by V10(b) for sibling forks (`d¹ = d_new¹`, `d² = d_new²`). The corollary also underwrites V11's first premise-scope remark (on non-immediate-source modifications), which observes that arrangement modifications targeting documents outside the chain leave each chain source's content-subspace mapping intact — V11 takes its premise as a hypothesis on each step, and Corollary 2 supplies the operational discharge by which a sequence consisting entirely of non-immediate-source M-modifications satisfies that hypothesis at the next chain step. The second remark (on `d_src` modifications after step 1) is discharged not by V5a but by conclusion anchoring at `Σ`, distinct from this corollary's operational role.

V5a is not a property of the fork operation itself — it is a property of the transition system's per-document frame discipline. We record it here because it is what makes the source-fork relationship semantically symmetric (Corollary 1: neither owner can disturb the other's arrangement through their own editing) and what underwrites the independence of sibling forks (Corollary 2: V10(b)).

## Subspace Selectivity

J4's clause (ii) restricts the inherited arrangement to the *content subspace*: `ran(M'(d_new)) ⊆ ran(M(d_src)|_{V_{s_C}(d_src)})`. The link subspace is excluded. We derive why this must be so abstractly.

The link subspace of any document is governed by CL-OWN (ASN-0047):

> `(A d, v : v ∈ dom(M(d)) ∧ subspace(v) = s_L : origin(M(d)(v)) = d)`

For every V-position in `d`'s arrangement that lies in the link subspace, the I-address at that position has `origin = d`. Links in a document's arrangement are *home-document links* — they are owned by the document whose arrangement holds them.

Suppose, for contradiction, that a fork transferred `d_src`'s link-subspace V-positions to `d_new` under transclusion. Then for some `v ∈ V_{s_L}(d_src)` with `ℓ := M(d_src)(v) ∈ dom(L)` and `origin(ℓ) = d_src` (by CL-OWN at `d_src`), the post-fork state would have `v ∈ V_{s_L}(d_new)` with `M'(d_new)(v) = ℓ` and `origin(ℓ) = d_src ≠ d_new`. This violates CL-OWN at `d_new`: the link-subspace V-position's image must have `origin = d_new`, but its origin is `d_src`. The contradiction forces link-subspace exclusion.

> **V6** (*subspace selectivity*): A fork transfers only the source's content-subspace arrangement. The new document's link subspace is empty in the post-fork state:
>
> `V_{s_L}(d_new) = ∅` (in `Σ'`, the post-fork state)
>
> *Derivation.* K.δ's effect on the newly created document is `M'(d_new) = ∅`. K.μ⁺ in J4's clause (ii) extends `M'(d_new)` only with positions drawn from `V_{s_C}(d_src)`, all of which have `subspace(v) = s_C` by the definition of `V_{s_C}(d_src) := {v ∈ dom(M(d_src)) : subspace(v) = s_C}` (ASN-0047). No link-subspace V-position is added. K.ρ does not modify arrangements. ∎

V6 has an immediate consequence: links in `d_src` are not present in `d_new`'s arrangement. But this does not mean they are inaccessible from `d_new`. A link's endsets reference I-addresses (`Endset` per ASN-0047), and the I-addresses in `d_new`'s arrangement are *the same I-addresses* as in `d_src`'s arrangement at every inherited V-position (V4a). The post-fork state inherits both the link store and the source's projections, and the fork's content-subspace V-positions project under any endset whose coverage hits the shared range.

To make this precise, we introduce three local definitions that the lemma below uses. An *endset* `e` (per ASN-0047's `Endset`) is a finite set of spans; each span `(s, ℓ) ∈ e` is a (start tumbler, length tumbler) pair denoting the address range `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}` from T12 (ASN-0034). Define:

- *Coverage:* `coverage(e) := ⋃_{(s, ℓ) ∈ e} span(s, ℓ) ⊆ T` — the set of I-addresses spanned by `e`.
- *Projection:* `project(a, i, d, Σ) := {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(Σ.L(a).eᵢ)}` — the V-positions of `d` at state `Σ` whose images at slot `i` of link `a`'s endset structure (per L3, ASN-0047) fall inside the slot's coverage.
- *Discoverability:* `discoverable_from(a, d, Σ) := (E i : 1 ≤ i ≤ |Σ.L(a)| : project(a, i, d, Σ) ≠ ∅)` — link `a` is discoverable from `d` at `Σ` iff some slot of `a` projects to at least one V-position of `d`.

These three definitions are local constructs over the foundation vocabulary; no further foundation ASN is consumed.

We record the consequence as a structural lemma:

> **V6a** (*link discoverability inheritance*): For every link `a ∈ dom(Σ.L)`, after the fork composite `Σ →* Σ'`:
>
> (i) `Σ'.L(a) = Σ.L(a)` — the link's endsets persist across the composite. *Derivation.* The fork composite decomposes into K.δ + K.μ⁺ + K.ρ × n (or K.δ alone in the empty-source case per V7), and each elementary transition frames `L' = L` by its frame clause (ASN-0047): K.δ's frame is `C' = C; L' = L; R' = R`; K.μ⁺'s frame is `C' = C; L' = L; E' = E; …; R' = R`; K.ρ's frame is `C' = C; E' = E; (A d :: M'(d) = M(d))` together with the elementary effect `R' = R ∪ {(a, d)}`, which leaves `L` unchanged because K.ρ's signature acts on `R` only. Composing across the constituent steps: `Σ'.L = Σ.L`, hence `Σ'.L(a) = Σ.L(a)` for every `a ∈ dom(Σ.L)`, and in particular `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)` for every slot `i`.
>
> (ii) `project(a, i, d_src, Σ') = project(a, i, d_src, Σ)` for every slot `i` — the source's projection is unchanged. *Derivation.* Unfolding the definition: `project(a, i, d_src, Σ') = {v ∈ dom(Σ'.M(d_src)) : Σ'.M(d_src)(v) ∈ coverage(Σ'.L(a).eᵢ)}`. By V5, `Σ'.M(d_src) = Σ.M(d_src)` (so `dom` and pointwise values coincide); by (i), `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)`. Substituting both equalities into the set-builder: `project(a, i, d_src, Σ') = {v ∈ dom(Σ.M(d_src)) : Σ.M(d_src)(v) ∈ coverage(Σ.L(a).eᵢ)} = project(a, i, d_src, Σ)`.
>
> (iii) `project(a, i, d_src, Σ) ∩ V_{s_C}(d_src) = project(a, i, d_new, Σ')` for every slot `i` — the fork's projection equals the source's content-subspace-restricted projection. *Derivation.* We show both inclusions. *(⊆)* For every `v ∈ project(a, i, d_src, Σ) ∩ V_{s_C}(d_src)`: by V4, `v ∈ dom(M'(d_new))` and `M'(d_new)(v) = M(d_src)(v)` (V4's universal supplies both conjuncts directly given `v ∈ V_{s_C}(d_src)` in the premise; V4b — the domain-equality commitment — is not consulted in this direction). By the definition of `project(a, i, d_src, Σ)`, `M(d_src)(v) ∈ coverage(Σ.L(a).eᵢ)`. By (i), `coverage(Σ.L(a).eᵢ) = coverage(Σ'.L(a).eᵢ)`. Composing: `M'(d_new)(v) ∈ coverage(Σ'.L(a).eᵢ)`, so `v ∈ project(a, i, d_new, Σ')`. *(⊇)* For every `v ∈ project(a, i, d_new, Σ')`: by the definition of `project`, `v ∈ dom(M'(d_new))` and `M'(d_new)(v) ∈ coverage(Σ'.L(a).eᵢ)`. By V4b's exact equality `dom(M'(d_new)) = V_{s_C}(d_src)`, `v ∈ V_{s_C}(d_src)` (which is `⊆ dom(M(d_src))` by `V_{s_C}(d_src) := {v ∈ dom(M(d_src)) : subspace(v) = s_C}`, so `v ∈ dom(M(d_src))`). By V4, `M'(d_new)(v) = M(d_src)(v)`; by (i), `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)`. Composing: `M(d_src)(v) ∈ coverage(Σ.L(a).eᵢ)`, so `v ∈ project(a, i, d_src, Σ)`, and combined with `v ∈ V_{s_C}(d_src)`, `v ∈ project(a, i, d_src, Σ) ∩ V_{s_C}(d_src)`.
>
> The link store is unchanged, the source's discoverability is preserved, and the fork inherits the source's content-subspace projection witnesses.

The implementation observation is that Gregory's `docreatenewversion` excludes the link subspace through a structural V-space layout — text starts at `1.x` and links at `2.x`, with the kluged `retrievedocumentpartofvspanpm` extracting only the text-subspace V-span. We note this is one of several ways to achieve V6: an alternative implementation could check `subspace(v) = s_C` explicitly per position, or could compute the V-span of the content subspace by a different mechanism entirely. The abstract claim — V6 — is what every conforming implementation must satisfy.

## The Empty-Source Case

J4 imposes the precondition `V_{s_C}(d_src) ≠ ∅`. We now consider what happens when this fails — when `d_src`'s content subspace is empty (either because nothing has ever been inserted, or because everything has been deleted via K.μ⁻ down to zero content positions).

The K.μ⁺ transition cannot fire with an empty extension set: its precondition `dom(M'(d)) ⊃ dom(M(d))` requires strict extension. With nothing to add, K.μ⁺ has no admissible invocation. The composite therefore cannot include a K.μ⁺ step; it must consist of K.δ alone (with K.ρ vacuously contributing nothing, since `ran(M'(d_new)) = ∅`).

Nelson's specification of CREATENEWVERSION reads: "This creates a new document with the contents of document `<doc id>`. It returns the id of the new document." [LM 4/66] The natural reading is that the new document is created *with whatever contents the source has*, including the degenerate case of zero contents. Empty documents are first-class entities in the design — CREATENEWDOCUMENT explicitly produces one [LM 4/65]. There is no gate in the specification text that conditions the operation on the source having content.

We therefore commit to producing an empty fork as the normative behavior:

> **V7** (*empty-source behavior*): A fork of `d_src` with `V_{s_C}(d_src) = ∅` reduces to K.δ alone, producing a new entity `d_new ∈ E'_doc` with `M'(d_new) = ∅` and `R' = R`. The operation succeeds; the fork is itself an empty document, eligible for subsequent insertion or further forking.

V7's K.δ-alone composite is not a J4 composite. J4 of ASN-0047 defines the fork composite as K.δ + K.μ⁺ + K.ρ with precondition `V_{s_C}(d_src) ≠ ∅`; V7 admits an additional composite shape — K.δ alone, without K.μ⁺ or K.ρ — when J4's precondition fails. We frame V7 as an *extension* of J4: this ASN's fork operation V0 supports both composite shapes, dispatching on whether `V_{s_C}(d_src)` is empty. The structural skeleton from "What Must Be Constructed" is therefore *J4 plus V7's extension*, with J4 covering the non-empty case and V7 covering the empty case. The deviation from J4 is explicit and intentional; J4's clauses (ii) and (iii) — which constrain K.μ⁺ and require K.ρ records — are vacated in V7's composite, where K.μ⁺ does not fire and `ran(M'(d_new))` is empty.

The alternative — rejecting the operation when the source is empty — is *inadmissible* under V7. Rejection would force the user to populate the source before forking, which contradicts Nelson's design intent that an empty source is degenerate but valid (CREATENEWDOCUMENT produces empty documents on demand, and they remain valid `E_doc` members). Rejection would also make the downstream property V11 (transitive identity through fork chains) implementation-dependent: a chain involving an empty intermediate would succeed under one implementation and fail under another.

Under V7's normative behavior, V1, V2, V3, V5, V10, V11, V12 hold unconditionally; V6 holds substantively — K.δ's effect on the freshly created document initialises `M'(d_new) = ∅` directly, which forces `V_{s_L}(d_new) = ∅` as an immediate consequence, so V6's equation is established by total arrangement emptiness rather than by the selective subspace exclusion of the non-empty case; V9 holds vacuously (`ran(M'(d_new)) = ∅` adds nothing to `R`); V4 and V8 are vacuous when `V_{s_C}(d_src) = ∅` (their universal quantifiers range over an empty set). A fork of an empty fork produces a third empty entity, each with prefix-encoded ancestry via V2 but no shared I-addresses (because there were none to share). The fork chain remains structurally coherent.

## Structural Correspondence

We arrive at the deepest claim — the one that distinguishes a *version* from an arbitrary new document. Two documents are *versions of each other* when their arrangements share I-addresses derived from a common forking event. The structural test of this relationship is automatic: it inheres in the I-addresses themselves.

> **V8** (*positional correspondence*): Let `V_{s_C}(d_src)` denote the content-subspace V-positions of `d_src` — equal in the pre-fork state `Σ` and the post-fork state `Σ'` because V5 establishes `M'(d_src) = M(d_src)`. For every `v ∈ V_{s_C}(d_src)`: `v ∈ dom(M'(d_new))` and `M'(d_src)(v) = M'(d_new)(v)`.
>
> *Derivation.* By V5, `M'(d_src) = M(d_src)`, so `V_{s_C}(d_src)` and the mapping values `M'(d_src)(v) = M(d_src)(v)` are the same in `Σ` and `Σ'`. By V4, for every `v ∈ V_{s_C}(d_src)`, `v ∈ dom(M'(d_new))` and `M'(d_new)(v) = M(d_src)(v)`. Composing: `M'(d_src)(v) = M(d_src)(v) = M'(d_new)(v)`. ∎

V8 says: immediately after forking, every content-subspace V-position of `d_src` corresponds to the same V-position in `d_new`, with the same I-address. The correspondence is *exact, structural, and computable from the I-address equality alone*. No history is consulted; no derivation lineage is traversed.

This is what underlies Nelson's intercomparison promise:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

The "word for word" comparison is the I-address equality test: at each shared V-position, the question "is this the same content?" reduces to "is `M(d₁)(v) = M(d₂)(v)`?" Any intercomparison operation reads this equality directly from the arrangements; nothing more is required of the storage layer, because nothing more was needed.

We record two immediate corollaries.

> **V8b** (*correspondence is state-relative — bounded fork-time witness set*): Let `Σ' →* Σ_g` be any sequence of valid composite transitions from the post-fork state `Σ'`. The set of V-positions at which `d_src` and `d_new` correspond at `Σ_g` is
>
> `Corr_g := {v ∈ T : v ∈ dom(M_g(d_src)) ∩ dom(M_g(d_new)) ∧ M_g(d_src)(v) = M_g(d_new)(v)}`
>
> Let `F := V_{s_C}(d_src)|_{Σ'}` denote the fork-time content-subspace witness set (fixed by the post-fork state), and define the *time-indexed fork-time witness set*
>
> `Π_g := F ∩ Corr_g`
>
> — the V-positions that existed in `d_src`'s content subspace at fork-time *and* still witness correspondence at `Σ_g`. Two facts hold about `Π_g`:
>
> (i) *Set bound.* `Π_g ⊆ F` at every reachable `Σ_g`. The witness set never grows beyond the fork-time set, since `F` is fixed by the post-fork state and `Π_g` is its intersection with `Corr_g`.
>
> (ii) *Initial coverage.* At the post-fork state itself, `Π_{Σ'} = F`. V8 supplies `F ⊆ Corr_{Σ'}`, so `Π_{Σ'} = F ∩ Corr_{Σ'} = F`.
>
> *Non-monotonicity.* `Π_g` need not decay monotonically: subsequent K.μ⁻ on either side may move `v` out of `dom(M_g(d_src)) ∩ dom(M_g(d_new))` and subsequent K.μ⁺ may re-install a binding (subject to D-CTG★/D-MIN★ contiguity and the operator's choice of target I-address); K.μ~ may remap an image. The remaining elementary transitions in ASN-0047's vocabulary leave `Π_g` unchanged. K.α and K.λ each frame `(A d :: M'(d) = M(d))` (no arrangement is touched); K.ρ likewise frames `(A d :: M'(d) = M(d))`; in all three cases `Corr_g` is invariant by these frame conditions on `M`, so `Π_g = F ∩ Corr_g` is invariant as well. K.μ⁺_L on any target document `d` modifies `M(d)` only at a single V-position `v_ℓ` with `subspace(v_ℓ) = s_L` (its effect `M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}` adds exactly the one binding, and its frame `(A d' : d' ≠ d : M'(d') = M(d'))` preserves every other document's arrangement entirely). We trace the effect on `Corr_g` restricted to `F` in two steps. (i) For every `v ∈ F`, `subspace(v) = s_C` (since `F ⊆ V_{s_C}(d_src)` by `F`'s definition as a restriction of `V_{s_C}(d_src)`, and `s_C ≠ s_L` by SubspaceConventionAxiom, ASN-0047), so `v ≠ v_ℓ`. (ii) Hence `M'(d_src)(v) = M(d_src)(v)` and `M'(d_new)(v) = M(d_new)(v)` for every `v ∈ F` — whether the target `d` is `d_src` (the `v ≠ v_ℓ` step of (i) preserves `M(d_src)(v)` because K.μ⁺_L's union effect alters only `v_ℓ`), `d_new` (symmetric), or a third document (K.μ⁺_L's frame condition preserves both `M(d_src)` and `M(d_new)` entirely). (iii) So `Corr_g` restricted to `F` is unchanged across the K.μ⁺_L step. (iv) Hence `Π_g = F ∩ Corr_g` is unchanged. K.δ initialises only the freshly-created entity's arrangement (which by precondition `e ∉ E` is distinct from both `d_src` and `d_new`, themselves in `E` at every state from `Σ'` onward by P1) and frames `M'(d') = M(d')` for every pre-existing `d'`, including `d_src` and `d_new`, so `Corr_g` and hence `Π_g` are unchanged. K.μ⁻, K.μ⁺, and K.μ~ acting on any target document `d` with `d ≠ d_src ∧ d ≠ d_new` are likewise neutral: each of these three transition kinds carries the per-target frame condition `(A d' : d' ≠ d : M'(d') = M(d'))` (ASN-0047), and since `d_src ≠ d` and `d_new ≠ d`, both `M(d_src)` and `M(d_new)` are preserved entirely across the step, so `Corr_g` is invariant and `Π_g = F ∩ Corr_g` is invariant. So `Π_g` shifts only via K.μ⁻, K.μ⁺, or K.μ~ acting on `d_src` or `d_new`; the operational mechanics of removal, re-installation, and remapping are properties of those three transition kinds as defined in ASN-0047, not of the fork operation.
>
> *Derivation.* (i) is immediate from set-theoretic intersection: `Π_g = F ∩ Corr_g ⊆ F`. (ii) follows from V8 applied at `Σ'`: V4 ∧ V5 give `M'(d_src)(v) = M'(d_new)(v)` for every `v ∈ F = V_{s_C}(d_src)|_{Σ'}`, so `F ⊆ Corr_{Σ'}`, and the intersection collapses to `F`. ∎

> **V8c** (*correspondence is symmetric and untyped*): The relationship V8 records is between two documents; it does not distinguish "source" from "fork." After the fork is complete, both `d_src` and `d_new` are documents in `E_doc`, and the set of corresponding V-positions `{v ∈ T : v ∈ dom(M'(d_src)) ∩ dom(M'(d_new)) ∧ M'(d_src)(v) = M'(d_new)(v)}` is invariant under swap of the two documents. *Derivation.* The set is defined by two conjuncts: (i) `v ∈ dom(M'(d_src)) ∩ dom(M'(d_new))` and (ii) `M'(d_src)(v) = M'(d_new)(v)`. Conjunct (i) is invariant under swap because set intersection is commutative: `dom(M'(d_src)) ∩ dom(M'(d_new)) = dom(M'(d_new)) ∩ dom(M'(d_src))`. For conjunct (ii), V8 supplies `M'(d_src)(v) = M'(d_new)(v)` for the V-positions in the set; symmetry of equality (a property of `=`, applied to the V8-supplied equality) gives the equivalent `M'(d_new)(v) = M'(d_src)(v)`, which is conjunct (ii) under the swapped ordering. Both conjuncts therefore evaluate the same under either ordering of the two documents, and the set is unchanged. ∎

The intercomparison guarantee is *perpetual*. By T8 (AllocationPermanence, ASN-0034), `d_src` and `d_new` remain in `E_doc` forever; by P0/S0, their I-addresses persist in `dom(C)` forever; by the per-document arrangement frame discipline, neither side's arrangement modifies the other's. V8 holds in the post-fork state, and its consequences propagate to every subsequent state in which neither side has overwritten the relevant V-positions.

## Provenance Recording

The third elementary step of J4 is K.ρ, recording provenance for every I-address now in `d_new`'s arrangement.

K.ρ adds `(a, d_new)` to `R` for each `a ∈ ran(M'(d_new))`. By J1★ (ExtensionRecordsProvenanceContentSubspace, ASN-0047) — the extended-state coupling that supersedes J1 under ValidComposite★ — provenance is *required* for every I-address newly content-subspace-referenced in `d_new`'s arrangement. By J1'★ (ProvenanceRequiresExtensionContentSubspace), it is the only permitted extension. The fork must record provenance for every inherited I-address.

> **V9** (*fork provenance*): After a fork of `d_src`:
>
> `(A a : a ∈ ran(M'(d_new)) : (a, d_new) ∈ R')`
>
> *Derivation.* By J1★ applied to the composite `Σ →* Σ'`, every `a` such that `(E v ∈ dom(M'(d_new)) : subspace(v) = s_C ∧ M'(d_new)(v) = a)` and not previously content-subspace-referenced in `M(d_new)` must satisfy `(a, d_new) ∈ R'`. Pre-fork, `d_new ∉ E_doc`, so `M(d_new) = ∅` vacuously and no pre-fork content-subspace references exist. By V6, `V_{s_L}(d_new) = ∅` in the post-fork state, so `ran(M'(d_new))` is exactly the content-subspace range. The condition therefore reduces to every `a ∈ ran(M'(d_new))` having `(a, d_new) ∈ R'`. ∎

V9 has the consequence that, after the fork, querying R for "documents containing I-address `a`" returns at least `{d_src, d_new}` for every `a ∈ ran(M'(d_new))` (and possibly more, if `a` was also transcluded elsewhere). The fork makes `d_new` discoverable as a container of each inherited I-address.

We observe what V9 does *not* record. By the consultation answers, the pair `(a, d_new) ∈ R'` records that `d_new` contains `a`. It does *not* record that `d_new` obtained `a` from `d_src` (as opposed to from some other transclusion path). The chain of custody — A transcluded to B, B forked to C — is not stored in R; it is reconstructable from the I-addresses themselves, because `origin(a)` identifies the original allocator and V2's prefix-ancestry identifies the immediate parent in the fork tree.

> **V9a** (*provenance does not record derivation path*): For every `(a, d_new) ∈ R'` recorded by a fork, the relation does not distinguish whether `d_new` acquired `a` via fork from `d_src`, via transclusion from a third document also containing `a`, or via direct allocation (if `origin(a) = d_new`, which cannot occur in a fresh fork: by V3, `C' = C`, so the inherited I-addresses are exactly those already in `dom(C)` before the fork, none of which can have `origin(a) = d_new` because `d_new ∉ E_doc` pre-fork means `A_C(d_new)` had not been activated by SubAllocatorAxiom and so had emitted nothing into `dom(C)` prior to the fork). The relation reports *who has it*; the I-address tells you *who made it*; the parent prefix tells you *who you came from*. These three pieces of information are recoverable independently from the I-address and the fork's prefix structure.

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
> (b) *Independent content shares.* Both `d_new¹` and `d_new²` inherit content from `M(d_src)` *at the moment of each respective fork* — `d_new¹` reads `M(d_src)` at `Σ`, and `d_new²` reads `M(d_src)` at `Σ_g`. The two reads may or may not agree, depending on whether any intervening transition modified `M(d_src)` between `Σ` and `Σ_g`. Their inherited V→I mappings live in separate arrangements `M¹(d_new¹)` and `M²(d_new²)`. Sibling forks are distinct documents (V10(a)), and V5a Corollary 2 — pairwise independence, in which `d¹` names the *preserved* document and `d²` the other party — yields the two preservation directions via two independent instantiations of the same corollary. *Direction 1* (modifications M-targeted at `d_new¹` preserve `M(d_new²)`): instantiate Corollary 2 at `(d¹, d²) = (d_new², d_new¹)`. The corollary's hypothesis "no step M-targeted at `d¹`" reads "no step M-targeted at `d_new²`"; since `d_new¹ ≠ d_new²` by V10(a), a step M-targeted at `d_new¹` is not M-targeted at `d_new²`, satisfying the hypothesis. The corollary's conclusion `M''(d¹) = M'(d¹)` then reads `M''(d_new²) = M'(d_new²)` — `M(d_new²)` is preserved across such a step. *Direction 2* (modifications M-targeted at `d_new²` preserve `M(d_new¹)`): symmetrically, instantiate Corollary 2 at `(d¹, d²) = (d_new¹, d_new²)`, by the same argument with operands swapped. The two instantiations are independent applications of the corollary; the "and symmetrically" in this clause refers to the second instantiation, not to a free swap of the labels within a single instantiation. (V5a Corollary 1 — source–fork isolation — does not apply to this pair, since neither sibling fork plays the source role with respect to the other; both are forks of `d_src`.)
>
> (c) *Independent provenance records.* `R²` contains both `(a, d_new¹)` and `(a, d_new²)` for shared I-addresses, but these are distinct pairs (since `d_new¹ ≠ d_new²` by (a)).

V10's part (a) follows from V1 and T10a.7 as derived above. Part (b) follows from V5a Corollary 2 applied symmetrically. Part (c) follows from V9 applied at each fork independently.

We further observe that each fork independently derives from `d_src`'s state *at the moment of forking*. If two forks are separated in time by an editing operation on `d_src`, the two forks inherit different arrangements.

> **V10a** (*time-sensitivity of derivation*): A fork in state `Σ` inherits `V_{s_C}(d_src)` and the mappings `M(d_src)|_{V_{s_C}(d_src)}` as they stand in `Σ`, not as they stood at any prior or subsequent state. Two forks of the same source at different times may produce different new versions, reflecting whatever state changes to `M(d_src)` occurred between them.

By SequentialTransitionAxiom (ASN-0047), state transitions are sequentially atomic — there is no intermediate state visible to a fork mid-edit. The "moment of forking" is well-defined as the pre-state `Σ` of the fork composite.

## Composability: Fork of a Fork

The structural account treats `d_src` as any element of `E_doc`. A fork creates `d_new ∈ E_doc`, which is itself eligible to be the source of a subsequent fork. We trace what happens.

Suppose `Σ →* Σ¹` forks `d_src` to `d¹_new`, then `Σ¹ →* Σ²` forks `d¹_new` to `d²_new`. By V1 at each fork: `d¹_new = inc(d_src, 1)` and `d²_new = inc(d¹_new, 1)`. By V2 at each fork: `d_src ≼ d¹_new ≼ d²_new`. Ancestry composes.

By V4 at each fork: `M¹(d¹_new) = M(d_src)|_{V_{s_C}(d_src)}` (in the sense that for each content-subspace V-position of the source, the same V-position with the same I-address appears in the fork). Then `M²(d²_new) = M¹(d¹_new)|_{V_{s_C}(d¹_new)}`. Composing: the I-addresses in `M²(d²_new)` are the same I-addresses as in `M(d_src)` over the V-positions present in all three arrangements.

> **V11** (*transitive identity along unedited fork chains*): Let `Σ` denote the pre-state of the first fork — the chain's initial state. For every chain length `k ≥ 1` and every chain of forks `d_src → d¹_new → d²_new → ... → d^k_new` starting from `Σ` (with `d⁰_new := d_src`), where each step `dⁱ⁻¹_new → dⁱ_new` is a fork composite and *each step's source has its content-subspace arrangement unchanged between the prior step's post-state and the current step's pre-state* — that is, for every `1 ≤ i ≤ k`, `V_{s_C}(d^{i-1}_new)` is the same set in the post-state of step `i − 1` and the pre-state of step `i`, and for every `v` in this set, `M(d^{i-1}_new)(v)` is the same value in both states (with the convention that at `i = 1`, "step 0's post-state" denotes `Σ` itself — equivalently the pre-state of step 1 — so the premise at `i = 1` is satisfied trivially by reflexivity of set and pointwise equality) — the I-addresses inherited by `d^k_new` are the same I-addresses that `d_src` held at `Σ`: for every `v ∈ V_{s_C}(d_src)` evaluated at `Σ`, `v ∈ dom(M^k(d^k_new))` at the post-state of step `k`, and the value `M^k(d^k_new)(v)` at the post-state of step `k` equals the value `M(d_src)(v)` at `Σ`.
>
> *Anchoring at `Σ`.* The premise scopes per-step source preservation to each step's *immediate* source `d^{i-1}_new` across the gap between step `i-1`'s post-state and step `i`'s pre-state. For `i ≥ 2` the source is `d^{i-1}_new`, not `d_src`, so the premise leaves `d_src` unconstrained across gaps after step 1. To keep the conclusion well-defined under that scope, V11 anchors `V_{s_C}(d_src)` and `M(d_src)(v)` at `Σ` — the immutable historical state at the chain's start — rather than at any later state in which `d_src`'s arrangement may have been modified independently. Modifications M-targeted at `d_src` between fork steps are admissible (they change `d_src`'s current arrangement without altering its `Σ`-state values, which is what V11's conclusion references).
>
> *Derivation by induction on chain length `k`.*
>
> *Base case (`k = 1`).* V4 applied to the first fork `d_src → d¹_new` gives `M¹(d¹_new)(v) = M(d_src)(v)` for every `v ∈ V_{s_C}(d_src)`, both sides evaluated at the post-state of step 1 (V4's post-fork claim). V5 applied to step 1 gives `M¹(d_src) = M(d_src)`, so the source's arrangement is identical at post-step-1 and at the pre-state of step 1 — which is `Σ`. Consequently `V_{s_C}(d_src)` is the same set at `Σ` and at post-step-1, and for every `v` in this set, `M(d_src)(v)` at post-step-1 equals `M(d_src)(v)` at `Σ`. The base case conclusion: for every `v ∈ V_{s_C}(d_src)` evaluated at `Σ`, `v ∈ dom(M¹(d¹_new))` at post-step-1, and `M¹(d¹_new)(v)` at post-step-1 equals `M(d_src)(v)` at `Σ`.
>
> Note that `v ∈ V_{s_C}(d_src)` already implies `subspace(v) = s_C`, and `v ∈ dom(M¹(d¹_new))` by the V4 conclusion, so `v ∈ V_{s_C}(d¹_new)` at the post-state of step 1 — i.e., `V_{s_C}(d_src) ⊆ V_{s_C}(d¹_new)`. (V4b strengthens this to set equality `V_{s_C}(d¹_new) = V_{s_C}(d_src)`, though only the inclusion is consumed by the inductive step.)
>
> *Inductive step (`k ≥ 2`).* Assume the induction hypothesis at step `k − 1`: for every `v ∈ V_{s_C}(d_src)` evaluated at `Σ`, `v ∈ dom(M^{k-1}(d^{k-1}_new))` at the post-state of step `k − 1`, and `M^{k-1}(d^{k-1}_new)(v)` at the post-state of step `k − 1` equals `M(d_src)(v)` at `Σ`.
>
> The k-th fork composite `Σ^{k-1} →* Σ^k` takes `d^{k-1}_new` as source. Applying V4 at step `k` to each `v ∈ V_{s_C}(d_src)` at `Σ` requires `v ∈ V_{s_C}(d^{k-1}_new)` at step `k`'s pre-state. We establish the required inclusion in two stages, then close.
>
> *Stage 1 — IH delivers inclusion at the post-state of step `k − 1`.* Take any `v ∈ V_{s_C}(d_src)` at `Σ`. The IH gives `v ∈ dom(M^{k-1}(d^{k-1}_new))` at the post-state of step `k − 1`. By the definition of `V_{s_C}` (ASN-0047, ASN-0036 S8a inheritance), `subspace(v) = s_C` for every `v ∈ V_{s_C}(d_src)` at `Σ`. The two conjuncts of `V_{s_C}(d^{k-1}_new) = {v ∈ dom(M^{k-1}(d^{k-1}_new)) : subspace(v) = s_C}` are met, so `v ∈ V_{s_C}(d^{k-1}_new)` at the post-state of step `k − 1`. Pointwise the IH also supplies `M^{k-1}(d^{k-1}_new)(v)` at post-step-(k−1) equals `M(d_src)(v)` at `Σ`.
>
> *Stage 2 — formal premise carries the inclusion across the gap to the pre-state of step `k`.* The formal premise at `i = k` states that `V_{s_C}(d^{k-1}_new)` is the same set in the post-state of step `k − 1` and the pre-state of step `k`, and that for every element `v` of this set, `M(d^{k-1}_new)(v)` is the same value in both states. Applying the premise pointwise to the `v ∈ V_{s_C}(d^{k-1}_new)` supplied by Stage 1: `v ∈ V_{s_C}(d^{k-1}_new)` at the pre-state of step `k`, and the value `M^{k-1}(d^{k-1}_new)(v)` at post-step-(k−1) — which by the IH equals `M(d_src)(v)` at `Σ` — reads through unchanged into the pre-state of step `k`. (The premise's universal "`V_{s_C}(d^{i-1}_new)` is the same set" entails the membership-transfer step `v ∈ V_{s_C}(d^{k-1}_new) at post-(k−1) ⟹ v ∈ V_{s_C}(d^{k-1}_new) at pre-k` directly; no set-equality chain back to `V_{s_C}(d_src)` through earlier chain members is needed, so the derivation rests on the formal premise as written without strengthening it.)
>
> *Closing.* V4 at the k-th fork now applies for every `v ∈ V_{s_C}(d_src)` at `Σ`: V4 takes `v ∈ V_{s_C}(d^{k-1}_new)` (pre-step-k) as input and concludes `v ∈ dom(M^k(d^k_new))` at post-step-k with `M^k(d^k_new)(v)` at post-step-k equal to `M^{k-1}(d^{k-1}_new)(v)` at pre-step-k (V4's standard prime-convention reading: post-state value of the fork equals pre-state value of the source). Composing:
>
> `M^k(d^k_new)(v) at post-step-k = M^{k-1}(d^{k-1}_new)(v) at pre-step-k     [V4 at step k]`
> `                              = M^{k-1}(d^{k-1}_new)(v) at post-step-(k-1) [premise at i=k, Stage 2]`
> `                              = M(d_src)(v) at Σ                          [induction hypothesis]`
>
> The induction closes. ∎

*Remark on V11's premise scope — non-immediate-source modifications.* The premise is scoped to *each step's immediate source* — for every `1 ≤ i ≤ k`, only `d^{i-1}_new` is constrained, and only across the gap between step `i − 1`'s post-state and step `i`'s pre-state. Earlier chain members (`dⱼ_new` for `j < i − 1`) are not constrained across later gaps, and the derivation does not need them to be: V4 at step `k` reads only `d^{k-1}_new`'s arrangement at step `k`'s pre-state, and Stage 1's appeal to the IH supplies the membership `v ∈ V_{s_C}(d^{k-1}_new)` at the post-state of step `k − 1` purely from the IH's domain conjunct together with `subspace(v) = s_C` — no set equality across earlier chain members is invoked. Arrangement modifications M-targeted at documents *other than* the current step's immediate source — third documents outside the chain, or non-immediate chain members `dⱼ_new` with `j < i − 1` — are therefore structurally outside the premise's scope at step `i`. V5a Corollary 2 (pairwise independence) supplies the operational discharge: instantiating at `(d¹, d²) = (d^{i-1}_new, d_target)` for any such M-targeted `d_target ≠ d^{i-1}_new`, the corollary guarantees `M(d^{i-1}_new)` is preserved across each non-immediate-source step, so an operational sequence consisting entirely of such steps automatically satisfies the per-step premise at the next chain step. Modifications confined to a chain source's *link* subspace (e.g., K.μ⁺_L on `d^{i-1}_new`, which extends only `V_{s_L}(d^{i-1}_new)` and leaves `V_{s_C}(d^{i-1}_new)` and its image untouched) are likewise admissible at the immediate-source scope itself: the V4-readable values `M^{i-1}(d^{i-1}_new)|_{V_{s_C}(d^{i-1}_new)}` are unchanged.

*Remark on V11's premise scope — modifications M-targeted at `d_src` after step 1.* Modifications M-targeted at `d_src` itself between step 1 and step `k` appear outside the premise's per-step-immediate-source scope, but the structural justification for their admissibility is distinct from the non-immediate-source case above. For `i ≥ 2`, the immediate source is `d^{i-1}_new`, not `d_src`, so the per-step premise is silent on `d_src`'s state across those gaps. The discharge here is *conclusion anchoring* rather than V5a: V11's conclusion anchors `V_{s_C}(d_src)` and `M(d_src)(v)` at `Σ` (the chain's initial pre-state — the historical state fixed at the chain's beginning, immutable by definition), so any later edits to `d_src` change `d_src`'s current arrangement without altering the historical `Σ`-state values the conclusion references. The premise reflects exactly the values the derivation consults at each step, and the conclusion's anchoring at `Σ` insulates the result from any subsequent `d_src` edits. At `i = 1` the gap between step 0's post-state (which the reflexivity convention identifies with `Σ`) and step 1's pre-state (also `Σ`) is empty, so the premise is satisfied trivially and no admissibility argument is needed at the chain's start.

> **V11a** (*ancestry composition*): The prefix relation chains: `d_src ≼ d¹_new ≼ d²_new ≼ ... ≼ d^k_new`. Each step `dⁱ⁻¹_new → dⁱ_new` extends the tumbler by exactly one component at position `#dⁱ⁻¹_new + 1` whose value is `1 + j`, where `j ≥ 0` is the *subsequent-emission count* of `A_v(dⁱ⁻¹_new)` immediately prior to step `i`'s firing — `j = 0` covers V1's first-fork sub-case (`inc(dⁱ⁻¹_new, 1)`, placing value `1` at position `#dⁱ⁻¹_new + 1` by TA5(d)) and `j ≥ 1` covers V1's subsequent-fork sub-case (`inc(d_prev, 0)` for `d_prev` the most recent prior emission of `A_v(dⁱ⁻¹_new)`, with each successive `inc(·, 0)` strictly incrementing the component at position `#dⁱ⁻¹_new + 1` by TA5(c) — since `sig(d_prev) = #d_prev = #dⁱ⁻¹_new + 1` for every emission of `A_v(dⁱ⁻¹_new)` by the V2 length argument — so the `j`-th subsequent emission has value `1 + j` at this position). The unified form `1 + j` covers both V1 sub-cases without case split: at `j = 0` the value is `1` (first fork), and at `j ≥ 1` the value is `1 + j ≥ 2` (subsequent fork). The two regimes exhaust `A_v(dⁱ⁻¹_new)`'s emission stream because `A_v(dⁱ⁻¹_new)` produces its first emission via `inc(dⁱ⁻¹_new, 1)` and every later emission via `inc(d_prev, 0)` on the prior emission — there is no third emission mode in ASN-0047's Allocator hierarchy convention for version sub-allocators. The full chain is recoverable from `d^k_new`'s tumbler alone by reading prefixes of strictly increasing length: the prefix of `d^k_new` of length `#d_src + i` is exactly `dⁱ_new` for every `0 ≤ i ≤ k` (with `d⁰_new := d_src`). *Derivation of prefix chain.* We first verify that `≼` is transitive by unfolding the Prefix definition (ASN-0034). Suppose `a ≼ b` and `b ≼ c`. By Prefix, `a ≼ b` gives `#a ≤ #b` and `(A i : 1 ≤ i ≤ #a : bᵢ = aᵢ)`; `b ≼ c` gives `#b ≤ #c` and `(A i : 1 ≤ i ≤ #b : cᵢ = bᵢ)`. By NAT-order's transitivity of `<` composed with the `m ≤ n ⟺ m < n ∨ m = n` definition (case analysis on the disjuncts of `#a ≤ #b` and `#b ≤ #c`: `<`-`<` chains by NAT-order transitivity; `<`-`=` and `=`-`<` substitute equality into the strict step; `=`-`=` composes equalities), `#a ≤ #c`. For each `i` with `1 ≤ i ≤ #a`: since `#a ≤ #b`, also `1 ≤ i ≤ #b`, so `cᵢ = bᵢ` by the second hypothesis; and `bᵢ = aᵢ` by the first hypothesis; composing the two component equalities gives `cᵢ = aᵢ`. Both conjuncts of `a ≼ c` are established. With single-triple transitivity in hand, the chain `d_src ≼ d¹_new ≼ ... ≼ d^k_new` follows by induction on `k`, with `d⁰_new := d_src`. *Base case (`k = 1`).* V2 applied at the first fork step gives `d⁰_new ≼ d¹_new` directly — equivalently, `d_src ≼ d¹_new`. *Inductive step (`k → k + 1`).* Assume the induction hypothesis at length `k`: `d_src ≼ d^k_new`. V2 applied at the `(k+1)`-th fork step — whose source is `d^k_new` and whose fork is `d^{k+1}_new` — supplies `d^k_new ≼ d^{k+1}_new`. Single-triple transitivity applied to the pair `(d_src ≼ d^k_new, d^k_new ≼ d^{k+1}_new)` yields `d_src ≼ d^{k+1}_new`, extending the chain by one. The induction closes for every `k ≥ 1`, and the full chain `d_src ≼ d¹_new ≼ ... ≼ d^k_new` is recovered by reading each intermediate `dⁱ_new ≼ d^{i+1}_new` from V2 at step `i+1` and chaining them via the induction. *Derivation of recovery.* Two facts establish the recovery procedure. (i) *Length identity.* `#dⁱ_new = #d_src + i` for every `0 ≤ i ≤ k`. Induction on `i`. *Base* (`i = 0`): `d⁰_new := d_src`, so `#d⁰_new = #d_src + 0`. *Step* (`i → i + 1`): the V2 derivation's nested-induction-on-emission-count argument, applied to `A_v(dⁱ_new)` in place of `A_v(d_src)`, establishes that every emission of `A_v(dⁱ_new)` has length `#dⁱ_new + 1` — first emission via TA5(d) at `k = 1`, each subsequent emission via TA5(c) preserving the prior emission's length composed with the inner induction hypothesis. By V1, `dⁱ⁺¹_new` is an emission of `A_v(dⁱ_new)` in either sub-case, so `#dⁱ⁺¹_new = #dⁱ_new + 1`. Composing with the outer induction hypothesis: `#dⁱ⁺¹_new = #d_src + (i + 1)`. (ii) *Prefix identity.* For each `0 ≤ i ≤ k`, we establish `dⁱ_new ≼ d^k_new` by an inner induction on `k − i` (the remaining chain length from `i` to `k`); the inner induction is necessary because the outer prefix-chain derivation produced only `d_src ≼ d^k_new`, with `d_src = d⁰_new` fixing the start point, and the recovery argument requires the analogous result starting at every intermediate index. *Inner base* (`k − i = 0`, i.e., `i = k`): `d^k_new ≼ d^k_new` by reflexivity of `≼` — immediate from the Prefix definition, since `#d^k_new ≤ #d^k_new` and componentwise self-agreement hold trivially. *Inner step* (`k − i > 0`): the inner induction hypothesis applied at `i + 1` gives `dⁱ⁺¹_new ≼ d^k_new`; V2 applied at step `i + 1` of the chain (whose source is `dⁱ_new` and fork is `dⁱ⁺¹_new`) gives `dⁱ_new ≼ dⁱ⁺¹_new`; transitivity of `≼` (established at the opening of V11a's derivation) composes the two into `dⁱ_new ≼ d^k_new`. The inner induction closes for every `0 ≤ i ≤ k`. The Prefix definition then gives `(A j : 1 ≤ j ≤ #dⁱ_new : (d^k_new)_j = (dⁱ_new)_j)`. By (i), `#dⁱ_new = #d_src + i`, so the prefix of `d^k_new` of length `#d_src + i` agrees componentwise with `dⁱ_new` at every position; T3 (CanonicalRepresentation, ASN-0034) — equal length plus componentwise agreement is identity — gives that this prefix equals `dⁱ_new`. Reading off prefixes of length `#d_src, #d_src + 1, ..., #d_src + k` recovers `d_src, d¹_new, ..., d^k_new` in order; the per-step extension component at position `#dⁱ⁻¹_new + 1` of each successive prefix is the per-step value `1 + j` characterised in the lemma statement, with `j` the subsequent-emission count of `A_v(dⁱ⁻¹_new)` at step `i`. ∎

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
> (d) `(A a ∈ ran(M'(d_new)) :: (a, d_src) ∈ R'')` — provenance records for the source are also permanent. *Derivation.* By V4b (*domain equality*), `dom(M'(d_new)) = V_{s_C}(d_src)`, and by V4 (*arrangement inheritance*), `M'(d_new)(v) = M(d_src)(v)` for every `v ∈ V_{s_C}(d_src)`. Composing the two gives `ran(M'(d_new)) = ran(M(d_src)|_{V_{s_C}(d_src)})` (range equality, of which the inclusion is an immediate corollary) — every inherited I-address is content-subspace-referenced in `d_src`'s arrangement at the pre-fork state. V4 alone supplies equality on the restriction (`ran(M'(d_new)|_{V_{s_C}(d_src)}) = ran(M(d_src)|_{V_{s_C}(d_src)})` follows directly from V4's pointwise equality on `V_{s_C}(d_src)`) but leaves `dom(M'(d_new)) \ V_{s_C}(d_src)` unconstrained; equivalently, V4 alone gives only the unrestricted containment `ran(M(d_src)|_{V_{s_C}(d_src)}) ⊆ ran(M'(d_new))`. V4b is needed to close the reverse direction `ran(M'(d_new)) ⊆ ran(M(d_src)|_{V_{s_C}(d_src)})` by ruling out V-positions outside `V_{s_C}(d_src)` in `dom(M'(d_new))` that would otherwise contribute I-addresses outside `ran(M(d_src)|_{V_{s_C}(d_src)})`. P4★ (ProvenanceBoundsContentSubspace, ASN-0047) applied at the pre-fork state gives `(a, d_src) ∈ R` for every such `a`. P2 (ProvenancePermanence, ASN-0047) carries the pair forward into every subsequent reachable state `Σ''`.

V12 underwrites Nelson's "lengthy due process" claim: published content stays published precisely because the permanence is structural, not policy. There is no operation in the transition vocabulary of ASN-0047 that removes content from `C`, removes entities from `E`, or removes pairs from `R`. The permanence is absolute at the abstract level; any withdrawal mechanism a deployment chooses to layer on top is a policy decision above the transition system, not an operation within it.

The consequence for source-fork pairs specifically: neither owner can remove the shared content from the storage substrate. The source owner can delete content from their own *arrangement* (K.μ⁻ on `d_src`), and similarly the fork owner can delete from their own arrangement. Neither action affects the other's arrangement (V5a Corollary 1, applied at the pair `(d_src, d_new)`) and neither affects `dom(C)` (V3 holds for K.μ⁻ as well; its frame condition is `C' = C`). The I-addresses persist; the arrangements evolve independently.

## The Fork Composite

We assemble the formal definition.

> **V0** (*fork operation*): A *fork* of `d_src` is a composite state transition `Σ →* Σ'`.
>
> *Composite structure.* The composite is the *uninterrupted* sequence of elementary transitions K.δ + K.μ⁺ + K.ρ × n (where `n = |ran(M'(d_new))|`), or K.δ alone in the empty-source case per V7's extension of J4. No other elementary transitions fire between the constituent steps; the intra-composite sub-states `Σ^{(1)}, Σ^{(2)}, …` named in the verification below (parenthesised superscript per the verification's Notation paragraph) are visible only at the boundaries between consecutive elementary transitions of the composite itself, and are intentionally typographically distinct from the post-composite states `Σ¹, Σ², …, Σ^k` (unbracketed superscript) used in V10 and V11 to index a sequence of fork composites. This uninterrupted-sequence requirement is what permits V4 (arrangement inheritance) and V5 (source isolation) to compose cleanly across the composite: K.μ⁺ reads the unmodified `M(d_src)` placed in scope by V5's frame, and V5's "unchanged across the composite" claim on `M(d_src)` is discharged by composing K.δ, K.μ⁺, and K.ρ frame conditions across exactly the steps the composite names, with no intervening K.μ⁻, K.μ~, or K.μ⁺ on `d_src` that could disturb the source between steps. The inter-composite analogue is V11's premise that each step's source has its content-subspace arrangement unchanged between the prior step's post-state and the current step's pre-state; the present clause is its intra-composite counterpart.
>
> *Precondition.* `d_src ∈ E_doc`. No content-existence precondition is imposed; the empty-source case is normative per V7.
>
> *Effects.* When `V_{s_C}(d_src) ≠ ∅` (the composite is K.δ + K.μ⁺ + K.ρ × n, where `n = |ran(M'(d_new))|`):
>
> ```
> C' = C                                              (V3)
> L' = L                                              (no K.λ or K.μ⁺_L steps)
> E' = E ∪ {d_new}                                    (V1)
>   where d_new is A_v(d_src)'s next emission:
>     d_new = inc(d_src, 1)   on first fork of d_src
>     d_new = inc(d_prev, 0)  on subsequent fork
>       (d_prev = A_v(d_src)'s most recent prior emission)
> M'(d_new)(v) = M(d_src)(v)  for v ∈ V_{s_C}(d_src)  (V4)
> M'(d_new)(v) undefined       for v ∉ V_{s_C}(d_src) (V4b; V6 as corollary for link-subspace V-positions)
> (A d' : d' ≠ d_new : M'(d') = M(d'))                (V5 for d' = d_src; K.δ + K.μ⁺ + K.ρ frame conditions for d' ≠ d_src ∧ d' ≠ d_new)
> R' = R ∪ {(a, d_new) : a ∈ ran(M'(d_new))}          (V9; set equality verified by sequential composition: R^{(1)} = R by K.δ frame; then R^{(2)} = R^{(1)} by K.μ⁺ frame; then R^{(2+n)} = R^{(2)} ∪ {(a, d_new) : a ∈ ran(M^{(2)}(d_new))} by the K.ρ × n cumulative effect)
> ```
>
> *State of `V_{s_C}(d_src)` in the Effects above.* The set `V_{s_C}(d_src)` (and `M(d_src)(v)` for `v` in it) is evaluated at the pre-state `Σ`. V5's source-isolation guarantee `M'(d_src) = M(d_src)` makes the choice immaterial: `V_{s_C}(d_src)` denotes the same set and `M(d_src)(v)` denotes the same value in `Σ` and `Σ'`. Either reading produces the same Effects.
>
> The "undefined elsewhere" line is the *exact* characterization `dom(M'(d_new)) = V_{s_C}(d_src)` supplied by V4b — V6's `V_{s_L}(d_new) = ∅` is a corollary covering the link-subspace V-positions specifically, but V4b is the primary justification because it rules out any V-position outside `V_{s_C}(d_src)` regardless of subspace.
>
> The R' line is a set equality, not the inclusion `R' ⊇ R ∪ {(a, d_new) : a ∈ ran(M'(d_new))}` that V9 alone supplies. The equality is verified by the elementary decomposition: K.δ's frame condition gives `R^{(1)} = R` (no pairs added by entity creation); K.μ⁺'s frame condition gives `R^{(2)} = R^{(1)}` (no pairs added by arrangement extension); the K.ρ × n phase adds exactly the `n` distinct pairs `{(a_j, d_new) : 1 ≤ j ≤ n}` enumerating `ran(M'(d_new))`. Composing the three elementary frame and effect clauses across the composite produces the set equality.
>
> The K.ρ phase is `n` elementary K.ρ invocations (one per `a ∈ ran(M'(d_new))`), each recording a single `(a, d_new)` pair per K.ρ's definition (ASN-0047). The set-builder `{(a, d_new) : a ∈ ran(M'(d_new))}` denotes the cumulative effect of all `n` invocations on `R`; the elementary multiplicity is verified per step in "The Fork Composite" verification below.
>
> When `V_{s_C}(d_src) = ∅` (the composite is K.δ alone, per V7's extension of J4): `C' = C`, `L' = L`, `E' = E ∪ {d_new}` (where `d_new` is `A_v(d_src)`'s next emission, formula as above), `M'(d_new) = ∅`, `M'(d') = M(d')` for `d' ≠ d_new`, `R' = R`. The operation succeeds.

The elementary decomposition into K.δ + K.μ⁺ + K.ρ × n (where `n = |ran(M'(d_new))|`), or K.δ alone in the empty case, verifies the ValidComposite★ conditions of ASN-0047. We check briefly.

*Notation for the verification.* Within this verification we denote intra-composite sub-states by `Σ^{(j)}` (parenthesised superscript): `Σ^{(0)} = Σ` (pre-state), `Σ^{(1)}` after K.δ, `Σ^{(2)}` after K.μ⁺, and `Σ^{(2+j)}` after the j-th elementary K.ρ step (so the K.ρ × n phase terminates at `Σ^{(2+n)}`). State-stamped components inherit the same superscript: `C^{(j)}`, `L^{(j)}`, `E^{(j)}`, `M^{(j)}`, `R^{(j)}`. This notation is intentionally distinct from V10's and V11's `Σ¹, Σ², …, Σ^k` (unbracketed superscript), which name post-composite end-states across a sequence of fork composites — `Σ^k` there is the post-state of the k-th fork composite, not the state after the k-th elementary step of any single composite. The two conventions are disjoint and never collide.

*K.δ at the pre-fork state Σ.* The K.δ sub-case is determined by `A_v(d_src)`'s state.

*K.δ sub-case A — first fork.* `A_v(d_src)` has emitted no prior version. K.δ case (ii) with `k = 1`, `t = d_src`. The K.δ outer preconditions are `e ∉ E ∧ ValidAddress(e) ∧ ¬IsElement(e)`; the uniform Case (ii) precondition is `parent(e) ∈ E`; the per-sub-case precondition at `k = 1` is `t ∈ E_doc`. We discharge each in turn.

Per-sub-case: `d_src ∈ E_doc` is V0's precondition.

Outer-precondition `e ∉ E` (freshness of `d_new = inc(d_src, 1)`) is discharged by three independent steps that jointly rule out every K.δ event in the system's history that could have placed `inc(d_src, 1)` into `E`. *(i) Within the parent allocator's spawning event at `(t = d_src, k = 1)`.* T10a's at-most-once-per-(t, k') child-spawning constraint (ASN-0034) — "Each `(t, k')` pair — domain element and spawning parameter — yields at most one child-spawning event" — governs the K.δ event that simultaneously activates `A_v(d_src)` as a sub-allocator and places `inc(d_src, 1)` into `E` as `A_v(d_src)`'s base address (its first emission). Sub-case A's predicate that `A_v(d_src)` has emitted no prior version means no K.δ event with `(t = d_src, k = 1)` has fired yet; the at-most-once constraint then forces that no past K.δ event has placed `inc(d_src, 1)` into `E` via this exact spawning path. *(ii) Within the parent allocator's other spawning events at `(t = d_src, k' ≠ 1)`.* A K.δ event at `(t = d_src, k' = 2)` is inadmissible to begin with: K.δ case (ii) at `k = 2` carries the precondition `zeros(t) ≤ 1` (ASN-0047), and `d_src ∈ E_doc` forces `zeros(d_src) = 2`, violating the precondition. Even were such an event admissible, TA5(d) at `k = 2` would produce `inc(d_src, 2) = [d_src..., 0, 1]` of length `#d_src + 2` — distinct from `inc(d_src, 1) = [d_src..., 1]` of length `#d_src + 1` by T3 (CanonicalRepresentation, ASN-0034), since the two tumblers have unequal length. A K.δ event at `(t = d_src, k' = 0)` would produce a sibling of `d_src` in the parent account's document sub-allocator stream, not `inc(d_src, 1)`. *(iii) Within `A_v(d_src)`'s subsequent sibling stream and across every other allocator.* Subsequent emissions of `A_v(d_src)` — `inc(d_prev, 0)` for `d_prev` already in `dom(A_v(d_src))` — are governed by T10a.7's enumeration injectivity; they produce addresses different from `inc(d_src, 1)` because each sibling step modifies only the trailing component (TA5(c)), distinguishing the second and later versions from the first. T10a.6 (DomainDisjointness, ASN-0034) — `A_v(d_src)`'s domain is disjoint from every other allocator's domain — rules out any other allocator across the entire system from having produced `inc(d_src, 1)`. Combining (i)–(iii): no allocator, present or past, has placed `inc(d_src, 1)` into `E`, so `d_new ∉ E`.

Outer-precondition `ValidAddress(d_new)` (T4-validity) is discharged by T10a.4 (T4PreservationUnderDiscipline, ASN-0034) applied to `A_v(d_src)`. T10a-conformance of `A_v(d_src)` is established by ASN-0047's Allocator hierarchy definition, which declares T10a-conformance per sub-allocator frontier; T10a.4 then guarantees every output — including `d_new` as `A_v(d_src)`'s first emission — satisfies T4. Outer-precondition `¬IsElement(d_new)` follows from `IsDocument(d_new)` (established below): `IsDocument(d_new)` will mean `zeros(d_new) = 2`, while `IsElement(d_new)` would require `zeros(d_new) = 3`; the two are exclusive.

Uniform-precondition `parent(d_new) ∈ E` is discharged in two steps. KDeltaParentK01 (ASN-0047), applied to `e = inc(d_src, 1)` at `k = 1`, gives `parent(d_new) = parent(d_src)`. P8 (EntityHierarchy, ASN-0047), applied to `d_src ∈ E` with `¬IsNode(d_src)` (since `IsDocument(d_src)` from `d_src ∈ E_doc` forces `zeros(d_src) = 2 ≠ 0`), yields `parent(d_src) ∈ E`. Composing: `parent(d_new) = parent(d_src) ∈ E`.

By KDeltaZerosK01, `zeros(d_new) = zeros(d_src) = 2`, so `IsDocument(d_new)`.

*K.δ sub-case B — subsequent fork.* `A_v(d_src)` has prior emissions with most recent `d_prev ∈ E_doc`. K.δ case (ii) with `k = 0`, `t = d_prev`. The K.δ outer preconditions are `e ∉ E ∧ ValidAddress(e) ∧ ¬IsElement(e)`; the uniform Case (ii) precondition is `parent(e) ∈ E`; the per-sub-case precondition at `k = 0` is `t ∈ E ∧ ¬IsNode(t) ∧ inc(t, 0) ∉ E`. We discharge each in turn.

Per-sub-case `d_prev ∈ E` holds by P1 (entity permanence, ASN-0047) applied to `d_prev`'s earlier K.δ event. Per-sub-case `¬IsNode(d_prev)` holds because `d_prev` is a `A_v(d_src)` output with `IsDocument(d_prev)` (zeros preserved at the first emission by KDeltaZerosK01 at `k = 1`, and preserved at each subsequent emission by KDeltaZerosK01 at `k = 0`); `IsDocument` excludes `IsNode` (`zeros = 2 ≠ 0`).

Per-sub-case freshness `inc(d_prev, 0) ∉ E` is discharged in three independent steps. *(i) Within-allocator distinctness.* T10a.7 (EnumerationInjectivity, ASN-0034) applied to `A_v(d_src)`'s sibling-stream enumeration `(t₀, t₁, t₂, ...)` gives injectivity of the indexing map: distinct enumeration indices produce distinct outputs. The to-be-emitted tumbler `inc(d_prev, 0)` is the next index in this enumeration, hence distinct from every prior index's output as a tumbler value. *(ii) Prior emissions are in E while the new emission has not yet fired.* SequentialTransitionAxiom (ASN-0047) totally orders state transitions, so `A_v(d_src)`'s emission count is part of the state and increases monotonically per K.δ firing on `A_v(d_src)`'s frontier. P1 (entity permanence, ASN-0047) preserves every prior emission in `E`. The conjunction supplies the operative fact: every prior emission's tumbler is currently in `E`, and the to-be-emitted next-index tumbler has not yet fired and so is *not* the output of any prior K.δ event. Combined with step (i)'s within-allocator distinctness from prior outputs as tumblers, the new emission's tumbler is not in `A_v(d_src)`'s domain restricted to `E`. *(iii) Cross-allocator non-collision.* T10a.6 (DomainDisjointness, ASN-0034) gives `A_v(d_src)`'s domain disjoint from every other allocator's domain, so the new emission is not in any other allocator's domain either; no other allocator has placed `inc(d_prev, 0)` into `E`. Combining (i)–(iii): `inc(d_prev, 0) ∉ E`.

Outer-precondition `e ∉ E` is the same condition as the per-sub-case freshness just discharged. Outer-precondition `ValidAddress(d_new)` is discharged by T10a.4 (T4PreservationUnderDiscipline, ASN-0034) applied to `A_v(d_src)` — T10a-conforming per ASN-0047's Allocator hierarchy definition — which guarantees every output (every sibling emission and the base address) is T4-valid. Outer-precondition `¬IsElement(d_new)` follows from `IsDocument(d_new)` (established below): `zeros(d_new) = 2 ≠ 3`.

Uniform-precondition `parent(d_new) ∈ E` is discharged in two steps. KDeltaParentK01 (ASN-0047), applied to `e = inc(d_prev, 0)` at `k = 0`, gives `parent(d_new) = parent(d_prev)`. P8 (EntityHierarchy, ASN-0047), applied to `d_prev ∈ E` with `¬IsNode(d_prev)` (just established), yields `parent(d_prev) ∈ E`. Composing: `parent(d_new) = parent(d_prev) ∈ E`.

By KDeltaZerosK01, `zeros(d_new) = zeros(d_prev) = 2`, so `IsDocument(d_new)`.

(NodeUniqueAllocation does not apply in either sub-case — it governs only K.δ events with `IsNode(e)`, while `d_new` satisfies `IsDocument(d_new)`.)

Effect (both sub-cases): `E^{(1)} = E ∪ {d_new}`, `M^{(1)}(d_new) = ∅`, `M^{(1)}(d') = M(d')` for `d' ≠ d_new`. Frame: `C^{(1)} = C`, `L^{(1)} = L`, `R^{(1)} = R`.

*K.μ⁺ at Σ^{(1)} (skipped in the empty case).* Target `d = d_new`. The extension set is `V_{s_C}(d_src)`. Precondition: `d_new ∈ E^{(1)}_doc` (just established); for every `v ∈ V_{s_C}(d_src)`, the target `M(d_src)(v) ∈ dom(C^{(1)}) = dom(C)` (S3★ at `d_src` restricted to `subspace(v) = s_C`, ASN-0047, with `M^{(1)}(d_src) = M(d_src)` by K.δ's frame condition `(A d' : d' ≠ d_new : M^{(1)}(d') = M(d'))` (ASN-0047) applied to `d_src ≠ d_new` — the inequality holds because V1 places `d_new ∉ E_doc` pre-fork while V0's precondition has `d_src ∈ E_doc` pre-fork); new V-positions satisfy S8a (all components positive, by S8a applied at `d_src`) and S8-depth (common depth `m_{s_C}`); `dom(M^{(2)}(d_new))` finite (subset of `dom(M(d_src))` which is finite by S8-fin); `M^{(2)}(d_new)` satisfies D-CTG★ (the inherited positions form `V_{s_C}(d_src) = {[s_C, 1, ..., 1, k] : 1 ≤ k ≤ n_{s_C}}` per D-SEQ★, contiguous by construction) and D-MIN★ (minimum is `[s_C, 1, ..., 1]`); newly added V-positions are pairwise distinct (they are pairwise distinct in `V_{s_C}(d_src)`). The K.μ⁺ amendment of ASN-0047 requires `subspace(v) = s_C` for all new V-positions, which holds throughout. Strict extension: `V_{s_C}(d_src) ≠ ∅` by the non-empty-source case hypothesis governing this branch of V0.

Effect: `M^{(2)}(d_new)(v) = M(d_src)(v)` for `v ∈ V_{s_C}(d_src)`. Frame: `C^{(2)} = C`, `L^{(2)} = L`, `E^{(2)} = E^{(1)}`, `M^{(2)}(d') = M^{(1)}(d')` for `d' ≠ d_new`, `R^{(2)} = R^{(1)} = R`.

*K.ρ × n at Σ^{(2)}, n = |ran(M^{(2)}(d_new))|.* The K.ρ phase consists of `n` elementary K.ρ invocations, each recording one `(aⱼ, d_new)` pair. Enumerate `ran(M^{(2)}(d_new)) = {a₁, ..., a_n}` (finite by S8-fin applied to `dom(M^{(2)}(d_new))`; image of a finite set under a function is finite). The composite proceeds through `n` sequential elementary K.ρ steps: at step `j` (for `1 ≤ j ≤ n`), K.ρ at intermediate state `Σ^{(1+j)}` records `(aⱼ, d_new)` producing `Σ^{(1+j+1)} = Σ^{(2+j)}`. At step `j`, the K.ρ precondition (ASN-0047) is `aⱼ ∈ dom(C^{(1+j)})` and `d_new ∈ E^{(1+j)}_doc`. The content store is preserved by K.ρ's frame condition at each prior step (`C^{(1+j)} = C^{(1+j-1)} = ... = C^{(2)} = C` by induction on `j`), so `aⱼ ∈ dom(C^{(1+j)}) ⟺ aⱼ ∈ dom(C)`; the latter holds because `aⱼ ∈ ran(M^{(2)}(d_new))` and S3 at `M^{(2)}(d_new)` (from K.μ⁺'s postcondition) gives `ran(M^{(2)}(d_new)) ⊆ dom(C^{(2)}) = dom(C)`. Similarly, `d_new ∈ E^{(1+j)}_doc` holds because K.ρ's frame preserves E, so `E^{(1+j)} = E^{(2)} = E^{(1)}`, and `d_new ∈ E^{(1)}_doc` from the K.δ effect. Each elementary K.ρ step satisfies its precondition.

Cumulative effect across the `n` K.ρ steps: `R^{(2+n)} = R^{(2)} ∪ {(aⱼ, d_new) : 1 ≤ j ≤ n} = R ∪ {(a, d_new) : a ∈ ran(M^{(2)}(d_new))}`. Frame: `C^{(2+n)} = C`, `L^{(2+n)} = L`, `E^{(2+n)} = E^{(2)}`, `M^{(2+n)} = M^{(2)}`.

*Coupling at (Σ, Σ^{(2+n)}).* J0 holds vacuously: `dom(C^{(2+n)}) \ dom(C) = ∅`. J1★ holds because every `a` with `(E v ∈ dom(M^{(2+n)}(d_new)) : subspace(v) = s_C ∧ M^{(2+n)}(d_new)(v) = a)` had `(a, d_new)` recorded by some K.ρ step (the K.ρ enumeration ranges over all of `ran(M^{(2)}(d_new))`, which is exactly the content-subspace range by V6). J1'★ holds because every `(a, d) ∈ R^{(2+n)} \ R` was added by some K.ρ step with `d = d_new` and `a ∈ ran(M^{(2)}(d_new))`, satisfying the range-based content-subspace scoping.

The composite is a valid composite under ValidComposite★. ∎

*K.δ-alone composite verification (empty-source case, V7's extension).* When `V_{s_C}(d_src) = ∅`, V7 reduces V0 to a single elementary K.δ step — no K.μ⁺ phase, no K.ρ phase — and the composite is `Σ → Σ^{(1)}`. We verify ValidComposite★ for this shape directly. The K.δ precondition is the same as in the non-empty case (sub-case A for first fork, sub-case B for subsequent fork), and the discharge above is independent of `V_{s_C}(d_src)`'s emptiness — `d_src ∈ E_doc` and the T10a/P1/P8/KDeltaParentK01/KDeltaZerosK01/T10a.4/T10a.6/T10a.7 arguments all carry through unchanged. So K.δ's elementary precondition holds at `Σ`. *Coupling at (Σ, Σ^{(1)}).* J0 holds vacuously: K.δ's frame gives `C^{(1)} = C`, so `dom(C^{(1)}) \ dom(C) = ∅` and J0's antecedent is unsatisfiable. J1★ holds vacuously: K.δ's effect sets `M^{(1)}(d_new) = ∅`, so for `d = d_new` no `v ∈ dom(M^{(1)}(d_new))` exists, and the existential antecedent of J1★ is unsatisfiable for `d_new`; for every `d ≠ d_new`, K.δ's frame gives `M^{(1)}(d) = M(d)`, so no `a` is in `ran(M^{(1)}(d)) \ ran(M(d))`, and the antecedent is again unsatisfiable. J1'★ holds vacuously: K.δ's frame gives `R^{(1)} = R`, so `R^{(1)} \ R = ∅` and J1'★'s antecedent is empty. All three coupling constraints are satisfied vacuously at `(Σ, Σ^{(1)})`. The K.δ-alone composite is therefore a valid composite under ValidComposite★. ∎

## Why I-Address Identity Suffices for the Relationship

We have built the source-fork relationship entirely from I-address equality. We pause to record what this gives us and what it does not.

What I-address identity captures: structural correspondence (V8), shared content discoverability (V9), link discoverability via shared addresses (V6a, derived locally from K.δ/K.μ⁺/K.ρ frame conditions on `L`, V5's source-arrangement isolation, and V4/V4b's arrangement inheritance), automatic attribution (origin invariance through V4a and S7 of ASN-0036), transitive identity through fork chains (V11). All of these arise from the single design commitment that I-addresses are permanent and unique.

What I-address identity does not capture: counterpart correspondence (independently typed but textually identical content has different I-addresses), derivation lineage at the I-address level (an I-address does not record which forking event placed it where), semantic equivalence (two distinct I-addresses with equal byte values are not the same content). These would require additional structure — explicitly asserted counterpart links, an explicit derivation graph, or value-based comparison machinery — none of which is part of the abstract specification of the fork operation itself.

The minimalism is by design. The fork operation creates a new document that *structurally inherits* from the source via shared I-addresses. The structural inheritance is what makes intercomparison, attribution, and link survival automatic. Anything beyond the structural inheritance is a separate concern, handled by separate operations.

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

*Identity (V1).* `d_new` is a fresh tumbler with `zeros(d_new) = 2` (so `IsDocument`), with `d_src ≼ d_new` (V2).

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

*Correspondence (V8).* At each `v ∈ {[s_C, 1], [s_C, 2], [s_C, 3]}`, `M'(d_src)(v) = M'(d_new)(v)`. The CompareVersions operation on `(d_src, d_new)` over the full content subspace would return a single maximal run `([s_C, 1], [s_C, 1], 3)` — three pointwise-corresponding positions.

*Link discoverability (V6a).* By V6a(i), `Σ'.L(ℓ) = Σ.L(ℓ)` across the fork composite, so `ℓ`'s endset structure persists. Querying "which links reference `a₁`?" returns `ℓ` (assuming `a₁ ∈ coverage(Σ.L(ℓ).eᵢ)` for some slot `i`, hypothetically), and this answer is the same whether we ask from `d_src`'s vantage or `d_new`'s vantage. From `d_src`'s vantage: by V6a(ii), `project(ℓ, i, d_src, Σ') = project(ℓ, i, d_src, Σ)`, so any pre-fork witness in `d_src` (e.g., the V-position `[s_C, 1]` whose image `a₁` lies in coverage) remains a post-fork witness, and `discoverable_from(ℓ, d_src, Σ')` holds. From `d_new`'s vantage: by V6a(iii), every `v ∈ project(ℓ, i, d_src, Σ) ∩ V_{s_C}(d_src)` also lies in `project(ℓ, i, d_new, Σ')` — in particular, `[s_C, 1] ∈ project(ℓ, i, d_new, Σ')` if the hypothetical pre-fork witness applied, so `discoverable_from(ℓ, d_new, Σ')` holds.

*Subsequent edits.* Suppose `d_src`'s owner later deletes `[s_C, 3]` from `d_src`'s arrangement via a K.μ⁻ contraction with `n'_{s_C} = 2` — retaining the suffix-prefix `{[s_C, 1], [s_C, 2]}`, as required by K.μ⁻'s per-subspace retention semantics (ASN-0047) and D-CTG★. A middle-only deletion such as removing `[s_C, 2]` while keeping `[s_C, 3]` is not expressible as a K.μ⁻ at all. By V5a Corollary 1 applied at `d* = d_new` to a single-step sequence consisting of this K.μ⁻ (M-targeted at `d_src ≠ d_new`), `M(d_new)` is unaffected — `a₃` remains in `d_new`'s arrangement. By V12(c), `(a₃, d_new) ∈ R` persists; by V12(b), `a₃ ∈ dom(C)` persists. Symmetrically, if `d_new`'s owner deletes from `d_new`'s arrangement, V5a Corollary 1 applied at `d* = d_src` gives that `d_src` is unaffected.

*Further forking — fork of a fork (V11 chain case).* A fork of `d_new` (chained from the original fork of `d_src`, so `d_new` plays the role of `d¹_new` in V11's chain notation) produces `d²_new = inc(d_new, 1)` with `d_src ≼ d_new ≼ d²_new` (V11a). Here `d²_new` is *chain* notation — the second link in a fork chain, of length `#d_src + 2`. The I-addresses inherited by `d²_new` are still `a₁, a₂, a₃` — the same I-addresses originally allocated by `d_src` (V11).

*Subsequent fork of `d_src` — V1's `k = 0` sub-case (V10 sibling case).* Returning to the state after the first fork of `d_src` (with `d_new` having been allocated as `inc(d_src, 1)`, so `d_new` plays the role of `d_new¹` in V10's sibling notation), suppose the operator now forks `d_src` again. V1's subsequent-fork sub-case applies: `A_v(d_src)`'s most recent emission is `d_new`, so the new fork is `d_new² = inc(d_new, 0)`. The sibling-notation `d_new²` distinguishes this second sibling fork of `d_src` — of length `#d_src + 1`, parent `d_src` in the version sub-allocator — from any chain notation; in particular, `d_new² ≠ d²_new` of the prior paragraph (which has length `#d_src + 2` and parent `d_new` in its sub-allocator). By KDeltaParentK01, `parent(d_new²) = parent(d_new) = parent(d_src)`. By V2 applied at this second fork — whose inductive argument we walked through in §"Identity by Sub-Allocation" — `d_src ≼ d_new²`. We can verify directly: by TA5(c) `#d_new² = #d_new = #d_src + 1`; by TA5(b) at `k = 0`, `d_new²` agrees with `d_new` at every position except `sig(d_new) = #d_new`; combined with the base-case agreement `d_new_i = d_src_i` for `1 ≤ i ≤ #d_src`, the positions `1 ≤ i ≤ #d_src` satisfy `(d_new²)_i = (d_new)_i = (d_src)_i`, and `#d_src ≤ #d_new²` since `#d_new² = #d_src + 1`. The Prefix definition then gives `d_src ≼ d_new²`.

V10(a) holds concretely: both `d_new = inc(d_src, 1)` and `d_new² = inc(d_new, 0)` have length `#d_src + 1` (the first by TA5(d) at `k = 1`, the second by TA5(c) at `k = 0` inheriting `d_new`'s length), so they share a length — both extend `d_src` by exactly one component — and differ in that single trailing component (TA5(c) at the subsequent fork modifies position `sig(d_new) = #d_new` only — incrementing `d_new`'s final `1` to `2` — so `(d_new²)_{#d_new} = 2 ≠ 1 = (d_new)_{#d_new}`). The two siblings are distinct addresses sharing the same parent prefix `d_src`. V10(b) and V10(c) apply with `Σ¹` (the post-first-fork state) as the pre-state of the second fork; `M²(d_new²)` is again populated with `{[s_C, 1] ↦ a₁, [s_C, 2] ↦ a₂, [s_C, 3] ↦ a₃}` (assuming `M(d_src)` has not been edited between the two forks), and `R² ⊇ R¹ ∪ {(a₁, d_new²), (a₂, d_new²), (a₃, d_new²)}` is disjoint from the analogous `(aᵢ, d_new)` records added by the first fork.

*Empty source (V7).* Consider a separate document `d_src°` with `M(d_src°) = ∅` — a freshly produced CREATENEWDOCUMENT result with no content yet inserted, so `V_{s_C}(d_src°) = ∅` and `V_{s_L}(d_src°) = ∅`. A fork of `d_src°` triggers V7's extension of J4: the composite reduces to K.δ alone, with no K.μ⁺ and no K.ρ phases. The fork produces `d_new° = inc(d_src°, 1)` (V1's first-fork sub-case; V1 imposes no precondition on source content), with `IsDocument(d_new°)` and `d_src° ≼ d_new°` (V2). The K.δ effect on `IsDocument(e)` initialises `M'(d_new°) = ∅` directly — vignette point (i). Since the K.ρ phase does not fire, no `(a, d_new°)` pair is added to `R`: `R' = R` — vignette point (ii). V9's universal quantifier `(A a : a ∈ ran(M'(d_new°)) : (a, d_new°) ∈ R')` ranges over the empty set `ran(M'(d_new°)) = ∅` and is satisfied vacuously; V12(c) and V12(d) likewise quantify over the empty range and hold vacuously — vignette point (iii). V12(a) — joint permanence of the two entities — holds substantively: `d_src° ∈ E'_doc` (K.δ's E-frame `E^{(1)} = E ∪ {d_new°}` preserves `E ⊆ E^{(1)}`; P1; the K.δ-alone composite has `Σ' = Σ^{(1)}`, so this is also the post-composite state) and `d_new° ∈ E'_doc` (V1) persist into every subsequent state by T8 and P1. The empty fork is itself a first-class document; a later K.μ⁺ on `d_new°` (with content drawn from K.α invocations under `A_C(d_new°)`) populates `V_{s_C}(d_new°)` without any reference to `d_src°`'s arrangement, and the two documents proceed independently.

*Link-only source (V7 with `V_{s_L}(d_src) ≠ ∅`).* Consider now a third document `d_src°°` with `V_{s_C}(d_src°°) = ∅` but `V_{s_L}(d_src°°) = {[s_L, 1]}` and `M(d_src°°)([s_L, 1]) = ℓ°` for some `ℓ° ∈ dom(L)` with `origin(ℓ°) = d_src°°` (by CL-OWN). The fork branching is on content-subspace emptiness alone — V7's predicate `V_{s_C}(d_src) = ∅` is independent of `V_{s_L}(d_src)` — so the same K.δ-alone composite fires, producing `d_new°° = inc(d_src°°, 1)` with `M'(d_new°°) = ∅`. In particular `V_{s_L}(d_new°°) = ∅`, confirming V6 in this regime: the fork's link subspace is empty, as before, but now via total arrangement emptiness rather than the selective subspace exclusion of the non-empty case — vignette point (iv) first half. The source's link arrangement is preserved by V5: `M'(d_src°°)([s_L, 1]) = ℓ°` still holds, `ℓ° ∈ dom(L)` is preserved (no K.λ or K.μ⁺_L step fires across the K.δ-alone composite, so `L' = L`), and `origin(ℓ°) = d_src°°` is unchanged (origin is a property of the I-address tumbler, fixed at allocation) — vignette point (iv) second half. Link discoverability via shared I-addresses (V6a) applies trivially: there are no shared I-addresses to discover, since `ran(M'(d_new°°)) = ∅` and `dom(M'(d_new°°)) = ∅`. The source's link `ℓ°` remains discoverable from `d_src°°`'s vantage by the same machinery as in the populated case; the fork simply contributes nothing to the discovery.

## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| V0 | FORK composite: K.δ + K.μ⁺ + K.ρ × n (n = `|ran(M'(d_new))|`), or K.δ alone in the empty-source case (V7's extension of J4); produces new document inheriting source's content-subspace arrangement | introduced |
| V1 | `d_new ∈ E'_doc`, `d_new ∉ E_doc`, `parent(d_new) = parent(d_src)`, with `d_new` = `A_v(d_src)`'s next emission: `inc(d_src, 1)` on first fork, `inc(d_prev, 0)` on subsequent fork | introduced |
| V2 | `d_src ≼ d_new` — prefix-encoded ancestry recoverable from `d_new`'s tumbler | introduced |
| V3 | `C' = C` — fork allocates no new content | introduced |
| V3a | `{a ∈ dom(C') : origin(a) = d'} = {a ∈ dom(C) : origin(a) = d'}` for every `d'` — allocation invariance | introduced |
| V4 | `(A v ∈ V_{s_C}(d_src) :: v ∈ dom(M'(d_new)) ∧ M'(d_new)(v) = M(d_src)(v))` — arrangement inheritance | introduced |
| V4a | For every `v ∈ V_{s_C}(d_src)`, `M'(d_src)(v) = M'(d_new)(v)` — positional identity | introduced |
| V4b | `dom(M'(d_new)) = V_{s_C}(d_src)` and `V_{s_C}(d_new) = V_{s_C}(d_src)` — domain equality (exact, not just one-sided containment) | introduced |
| V5 | `M'(d_src) = M(d_src)` — source arrangement isolated from fork | introduced |
| V5a | Per-document arrangement independence: (a) per-elementary-transition — a step M-targeted at `d_target ≠ d*` or any non-arrangement-modifying step preserves `M(d*)`; (b) per-sequence — a sequence with no step M-targeted at `d*` preserves `M(d*)`. Corollary 1: source–fork isolation. Corollary 2: pairwise independence for sibling forks (consumed by V10(b)) | introduced |
| V6 | `V_{s_L}(d_new) = ∅` in the post-fork state — link subspace not inherited (forced by CL-OWN) | introduced |
| V6a | Across the fork composite: `Σ'.L(a) = Σ.L(a)` (link store unchanged by frame composition), `project(a, i, d_src, Σ') = project(a, i, d_src, Σ)` (source projection invariant via V5), and `project(a, i, d_src, Σ) ∩ V_{s_C}(d_src) = project(a, i, d_new, Σ')` (fork's projection equals the source's content-subspace-restricted projection via V4/V4b). `coverage`, `project`, and `discoverable_from` defined locally over foundation vocabulary | introduced |
| V7 | Empty-source behavior: fork of `d_src` with `V_{s_C}(d_src) = ∅` reduces to K.δ alone, succeeding with `M'(d_new) = ∅` and `R' = R` | introduced |
| V8 | `(A v ∈ V_{s_C}(d_src) :: M'(d_src)(v) = M'(d_new)(v))` — structural correspondence at fork-time | introduced |
| V8b | Correspondence is state-relative — bounded fork-time witness set: let `F := V_{s_C}(d_src)\|_{Σ'}` and `Π_g := F ∩ Corr_g`; then `Π_g ⊆ F` at every reachable state and `Π_{Σ'} = F`; membership of `v ∈ Π_g` is evaluated from the current arrangements alone and may shift across the transition sequence (no monotonic-decay claim); K.α, K.λ, K.ρ, K.δ, K.μ⁺_L, and third-document K.μ⁻/K.μ⁺/K.μ~ each leave `Π_g` invariant | introduced |
| V8c | Correspondence is symmetric and document-type-untyped | introduced |
| V9 | `(A a : a ∈ ran(M'(d_new)) : (a, d_new) ∈ R')` — provenance recorded for every inherited I-address | introduced |
| V9a | Provenance records containment, not derivation path — chain of custody is reconstructable from I-addresses and prefix structure, not stored | introduced |
| V10 | Sibling forks of the same source are independent in identity, arrangement, and provenance | introduced |
| V10a | Each fork derives from `M(d_src)` *at the moment of forking* — time-sensitivity | introduced |
| V11 | Transitive identity along unedited fork chains: for every fork chain `d_src → d¹_new → ... → d^k_new` starting from initial state `Σ`, where each step's source has its content-subspace arrangement (set and pointwise values) unchanged between the prior step's post-state and the current step's pre-state, `v ∈ dom(M^k(d^k_new))` at post-step-k and `M^k(d^k_new)(v)` at post-step-k equals `M(d_src)(v)` at `Σ`, for every `v ∈ V_{s_C}(d_src)` evaluated at `Σ` | introduced |
| V11a | Prefix relation chains: `d_src ≼ d¹_new ≼ ... ≼ d^k_new` — ancestry composition recoverable from tumbler structure | introduced |
| V12 | Joint permanence of source, fork, inherited I-addresses, and provenance records across all subsequent states | introduced |

## Dependency Audit

This ASN's body consumes claims from three foundation ASNs. ASN-0034 (Tumbler Algebra) supplies T0, T1, T3, T8, T12, TA5, TA5(b), TA5(c), TA5(d), TA5-SigValid, T10a, T10a.4, T10a.6, T10a.7, Prefix, and ASN-0034's NAT-order transitivity. ASN-0036 (Strand Model) supplies S2, S7, S8a, S8-fin, S8-depth, and the V-position / I-address vocabulary. ASN-0047 (Transition Model) supplies K.δ (cases (ii) at `k = 0` and `k = 1`), K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ, K.α, K.λ, J0, J1★, J1'★, J4, L3, P0, P1, P2, P4★, S3★, D-CTG★, D-MIN★, D-SEQ★, CL-OWN, `Endset`, KDeltaZerosK01, KDeltaParentK01, SubAllocatorAxiom, SequentialTransitionAxiom, SubspaceConventionAxiom, ValidComposite★, the Allocator hierarchy, P8 (EntityHierarchy), and the `Σ = (C, L, E, M, R)` substrate. V6a's `coverage`, `project`, and `discoverable_from` are local constructs defined over T12 (span) and the L-component of the substrate; no further foundation ASN is consumed.

ASN-0040 (Tumbler Baptism), declared in the inquiry's `depends:` set, has no use site in this ASN's body. The baptism vocabulary (`Σ.B`, `next`, `hwm`, `baptize`, B0–B10) does not appear: the fork operation works entirely in ASN-0047's K.δ + Allocator hierarchy + SubAllocatorAxiom + SequentialTransitionAxiom vocabulary for entity allocation and frontier advancement, with ASN-0034's T10a (allocator discipline), T10a.6 (DomainDisjointness), T10a.7 (EnumerationInjectivity), and T10a.4 (T4PreservationUnderDiscipline) supplying the underlying tumbler-arithmetic guarantees. ASN-0040 is flagged for removal from this inquiry's `depends:` set.

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
