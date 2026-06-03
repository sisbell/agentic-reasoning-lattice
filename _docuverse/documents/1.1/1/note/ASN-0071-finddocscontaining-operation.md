# ASN-0071: FINDDOCSCONTAINING Operation
*2026-05-25*

A reader of a document can ask: *what is in this document?* The answer comes from walking the document's arrangement and resolving each V-position to the content at its I-address — the read-direction.

The same reader can ask the inverse: *what documents contain this content?* This is the search-direction. A scholar tracing a quotation, a system computing royalty for transcluded reuse, a writer enumerating who has cited a passage — each needs to enumerate documents whose arrangements reference some specified material.

We specify what such an operation must do. Following Nelson we call it **FINDDOCSCONTAINING**. The question this ASN answers is: what is its result set? What determines membership, what guarantees govern completeness, and what does the operation deliberately not promise about currency in a permanent address space?

We work within the strand model as extended by ASN-0047. State `Σ` carries the content store `Σ.C : T ⇀ Val`, the link store `Σ.L`, document entities `Σ.E_doc ⊆ Σ.E`, and arrangements `Σ.M(d) : T ⇀ T` for each `d ∈ Σ.E_doc` — partial functions from V-positions to I-addresses satisfying functionality (S2), generalized referential integrity (S3★), and content permanence (P0, which subsumes S0 and S1). Sharing is unrestricted: distinct `(d, v)` pairs may map to the same I-address (ASN-0058 M13, SharedContent), and such co-occurrences are permanently independent arrangement entries (ASN-0058 M14, IndependentOccurrences). The extended state admits two V-subspaces — content (`s_C`) and link (`s_L`) — and S3★ routes each V-position to its appropriate store: `M(d)(v) ∈ dom(C)` when `subspace(v) = s_C`, and `M(d)(v) ∈ dom(L)` when `subspace(v) = s_L`. We assume content has been allocated and arranged through the standard transitions of ASN-0047; we specify only the query, not the operations that produce its inputs.

## The query

Content can be named in two registers. By I-address — "the content at addresses `A`" — purely structural. By V-position with source — "the content of document `d` at positions `σ`" — referenced from where the user encountered it.

We accept the latter. A **vspec** is a pair `(d_s, σ)` where `d_s ∈ Σ.E_doc` names a source document and `σ = (u, ℓ)` is a level-uniform V-span confined to the content subspace — `subspace(u) = s_C`, `Pos(ℓ)`, `actionPoint(ℓ) = #u`, `#ℓ = #u` (level-uniformity, ASN-0053 S6), and `actionPoint(ℓ) ≥ 2` (equivalently `ℓ₁ = 0`: the displacement does not perturb the subspace identifier at position 1; together with `actionPoint(ℓ) = #u` this also forces `#u ≥ 2`). Its denotation `⟦σ⟧` and reach `u ⊕ ℓ` used throughout are ASN-0053's (σ.denotation: `⟦σ⟧ = {t : start(σ) ≤ t < reach(σ)}`; σ.reach: `reach(σ) = start(σ) ⊕ width(σ)`); we apply those definitions rather than restate them below. A **vspec-set** is a finite set `Q = {q₁, q₂, ..., q_k}` of vspecs, possibly drawn from multiple source documents.

The restriction `subspace(u) = s_C` is load-bearing. FINDDOCSCONTAINING tracks transclusion of byte content — Nelson's "regardless of where the native copies are located" — and only the content subspace participates in transclusion. Link addresses have unique home documents recoverable directly from the tumbler via `origin` (ASN-0047 L1a, LinkScopedAllocation: `origin(a) ∈ E_doc` for every link address), so a query naming a link-subspace span would degenerate to "the link's home document," derivable without the operation. We exclude such queries by construction.

The companion restriction `actionPoint(ℓ) ≥ 2` enforces *subspace confinement* of the entire span. Under the standing precondition `actionPoint(ℓ) = #u` it is equivalent to the floor `#u ≥ 2`, placing the action point at position 2 or beyond, so by TumblerAdd's prefix-copy region position 1 of every `t ∈ ⟦σ⟧` equals `u₁ = s_C` — the entire span lives in the content subspace, with `subspace(t) = s_C` for every `t ∈ ⟦σ⟧`.

A vspec is structurally a relaxation of ASN-0058's `ContentReference`. ContentReference additionally requires well-formedness — every depth-`m` position in `⟦σ⟧` belongs to `dom(M(d_s))` — together with `V_{u₁}(d_s) ≠ ∅` and `#u = m` (the common depth of `d_s`'s text-subspace V-positions per S8-depth). The vspec drops all three: it admits spans whose positions may not all be currently arranged, whose source subspace may be empty in `d_s`, and whose depth may differ from `d_s`'s common depth. The relaxation makes the query total over well-typed inputs; resolution silently filters anything that does not match a current arrangement entry. What the vspec retains from ContentReference is subspace confinement, recovered from its explicit preconditions `actionPoint(ℓ) = #u` and `#u ≥ 2` — the action point sits at the span's *own* deepest component, with `#u` standing in for the common depth `m` the vspec no longer references. This is strictly tighter than T12's well-formedness bound `actionPoint(ℓ) ≤ #u`, and the tightening is load-bearing: pinning `actionPoint(ℓ) = #u` forecloses an action point *interior* to the span, which would otherwise let the displacement collect content positions the user never named — the over-collection C0's `actionPoint = m` exists to prevent. The claim we need — call it *prefix confinement* — is that every `t ∈ ⟦σ⟧` agrees with `u` on all components `1 ≤ j < #u`. This is the relaxed analogue of ASN-0058's C0a, proven here directly from the vspec preconditions. The argument is the position-1 reasoning of the Resolution section, run at every prefix position rather than just position 1: for any `j` with `1 ≤ j < #u = actionPoint(ℓ)`, position `j` lies strictly below the action point, so TumblerAdd's prefix-copy gives `(u ⊕ ℓ)_j = u_j` — `u` and `u ⊕ ℓ` share the whole prefix `1 ≤ j < #u`. We first establish the componentwise fact that drives both halves of the argument: for any position `p` with `1 ≤ p < #u` *at which `t_p` exists*, `t` cannot first disagree with `u` at `p`. Since `p < #u = actionPoint(ℓ)`, TumblerAdd's prefix-copy gives `u_p = (u ⊕ ℓ)_p`; were `t_p ≠ u_p`, T1 case (i) at `p` would force either `t < u` (if `t_p < u_p`) or `t > u ⊕ ℓ` (if `t_p > u_p`), each contradicting `u ≤ t < u ⊕ ℓ`. By NAT-order trichotomy (T0), `t_p = u_p` wherever `t_p` exists with `p < #u`. This fact discharges *totality* — that every `t ∈ ⟦σ⟧` has depth `#t ≥ #u`, so each `t_j` exists, the T1 *case (ii)* exclusion. Were `#t < #u`, then either `t` agrees with `u` on its whole length — making `t` a proper prefix of `u`, hence `t < u` by T1 case (ii), contradicting `u ≤ t` — or `t` first disagrees with `u` at some position `p ≤ #t < #u`, where `t_p` exists, contradicting the componentwise fact just established; either way `#t < #u` is impossible, so `#t ≥ #u` and `t_j` is defined for all `1 ≤ j < #u`. With totality in hand the componentwise fact applies at every `1 ≤ j < #u`, so `t_j = u_j` throughout. We name this *prefix confinement* (PC); it holds with no appeal to well-formedness. Its position-1 instance `t₁ = u₁` is subspace confinement. By PC, `⟦σ⟧` varies only at component `#u` and deeper, so resolution reads exactly the prefix the user named.

The third relaxation — dropping ContentReference's `#u = m` requirement — admits a *cross-depth* collection: when the anchor depth `#u` is shallower than the source's common depth `m`, the span `⟦σ⟧` captures every arrangement position in the deeper subtree hanging under the named coordinate. These positions *are* current arrangement entries, so F-FILT offers no defense — but collecting them is the intended semantics. FINDDOCSCONTAINING is specified to return *"any portion of the material specified ... regardless of where the native copies are located"* (LM 4/63): the user who names the coarse coordinate names its whole subtree — the *"prefix names subtree"* semantics.

## Resolution

For a single vspec `(d_s, σ)`, the resolved I-addresses are those that `d_s`'s current arrangement assigns to positions within the span:

  `iaddrs_one(d_s, σ)(Σ) := { Σ.M(d_s)(v) : v ∈ ⟦σ⟧ ∩ dom(Σ.M(d_s)) }`

For a vspec-set `Q`:

  `iaddrs(Q)(Σ) := ⋃_{(d_s, σ) ∈ Q} iaddrs_one(d_s, σ)(Σ)`

Every element of `iaddrs(Q)(Σ)` lies in `dom(Σ.C)` — the subset claim `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` holds whenever `iaddrs(Q)(Σ)` is itself well-defined. `iaddrs_one(d_s, σ)(Σ)` consults `Σ.M(d_s)`, and `dom(Σ.M) = Σ.E_doc` (M1, ASN-0047), so the expression `⟦σ⟧ ∩ dom(Σ.M(d_s))` is ill-formed when `d_s ∉ Σ.E_doc`. The subset claim is therefore gated on the same well-definedness precondition we state for `find` below — `wp-defined: (A (d_s, σ) ∈ Q :: d_s ∈ Σ.E_doc)` — which ensures every `Σ.M(d_s)` consulted is a defined arrangement. Under that gate the argument is that every position consulted by `iaddrs_one` is in the content subspace, so S3★ routes the image into `dom(Σ.C)` rather than `dom(Σ.L)`. We show subspace confinement first, then apply S3★.

*Subspace confinement.* Fix `t ∈ ⟦σ⟧`. The position-1 instance of prefix confinement (PC, proven in *The query*) applies — `1 < actionPoint(ℓ) = #u` since `#u ≥ 2` — giving `t₁ = u₁ = s_C`, hence `subspace(t) = s_C`.

*Routing.* Therefore every `v ∈ ⟦σ⟧ ∩ dom(Σ.M(d_s))` is a content-subspace V-position, and S3★ (ASN-0047) routes it: `Σ.M(d_s)(v) ∈ dom(Σ.C)`. The subset claim `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` is read with `Σ` explicit on both sides — the right-hand side is the input state's content store, not a fixed set. The `actionPoint(ℓ) ≥ 2` precondition licenses this position-1 step.

When a vspec `(d_s, σ)` is also a well-formed ContentReference, `iaddrs_one(d_s, σ)(Σ)` equals the set-flattening of ASN-0058's `resolve(d_s, σ)` — concretely, `{ a + k : (a, n) ∈ resolve(d_s, σ) ∧ 0 ≤ k < n }`. We derive the equality in one step. By C1a, `resolve(d_s, σ)` is read off the unique maximally merged block decomposition `⟨β₁, ..., β_K⟩` of the restriction `f = M(d_s)|⟦σ⟧`, with `β_j = (v_j, a_j, n_j)` and `resolve(d_s, σ) = ⟨(a₁, n₁), ..., (a_K, n_K)⟩`. The decomposition covers `dom(f)` exactly (B1, Coverage): `dom(f) = ⟦σ⟧ ∩ dom(M(d_s))` — precisely the index set of `iaddrs_one`. For each block, B3 (Consistency) gives `a_j + k = M(d_s)(v_j + k)` for `0 ≤ k < n_j`, and the `v_j + k` range over `V(β_j)`; by coverage the union of all `V(β_j)` is `dom(f)`. So
> `{ a_j + k : 1 ≤ j ≤ K ∧ 0 ≤ k < n_j } = { M(d_s)(v) : v ∈ dom(f) } = iaddrs_one(d_s, σ)(Σ)`.

The left side is the set-flattening of `resolve`. Set-flattening absorbs duplicate I-addresses: two distinct blocks may carry shared content (ASN-0058 M14), and the same `a` then appears in both — the set union dedupes it, matching `iaddrs_one`'s set codomain. The relaxation matters only when `⟦σ⟧` contains positions outside `dom(M(d_s))`: ContentReference treats such a span as ill-formed, while vspec silently drops the missing positions.

A vspec may name positions not currently in `dom(Σ.M(d_s))`. The definition handles this silently: the intersection `⟦σ⟧ ∩ dom(Σ.M(d_s))` drops unresolvable positions, and their absence contributes nothing to `iaddrs`. The query reads charitably — as "find documents containing the content at whatever positions of `σ` are currently bound" — rather than insisting on total resolvability.

This is a substantive choice. An alternative specification could reject the entire query as ill-formed if any position is unresolvable. The charitable reading is justified: a position not in the arrangement names no content, so excluding it from the resolution is the natural extension of "find documents containing the content at these positions". The price is reduced diagnostic information — the user cannot distinguish "no documents contain this" from "this query resolved to no I-addresses".

We note a structural property: `iaddrs_one(d_s, σ)(Σ)` depends only on `Σ.M(d_s)`. Each vspec is *source-anchored* — its meaning is fully determined by the pair `(d_s, σ)` given the state. No global context or caller's view is consulted. The resolution of `Q` is the union of independent per-source resolutions; sources can be consulted independently in any order, by any node holding the relevant arrangement.

## The operation

Given resolved I-addresses, FINDDOCSCONTAINING returns the documents whose arrangements currently reference any of them:

  `find(Q)(Σ) := { d ∈ Σ.E_doc : ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅ }`

*Well-definedness precondition.* The type signature presents `Q` and `Σ` as independent arguments, but `iaddrs(Q)(Σ)` consults `Σ.M(d_s)` for each source `(d_s, σ) ∈ Q`, and `dom(Σ.M) = Σ.E_doc` (M1, ASN-0047). The expression `⟦σ⟧ ∩ dom(Σ.M(d_s))` is therefore meaningful only when `d_s ∈ Σ.E_doc`. We make this explicit as the domain of the partial function `find`:

  `wp-defined:  (A (d_s, σ) ∈ Q :: d_s ∈ Σ.E_doc)`

`find(Q)(Σ)` is defined precisely when this precondition holds. The vspec clause `d_s ∈ Σ.E_doc` is a constraint on well-formedness *at the source state at which the vspec was formed*; the precondition above binds that constraint to the *evaluation state* `Σ`. The two coincide whenever `Q` is formed at a state no later than `Σ`, since entity permanence (P1, ASN-0047: `Σ.E ⊆ Σ'.E`) preserves `d_s ∈ E_doc` forward. When it holds, every `Σ.M(d_s)` named in `iaddrs(Q)(Σ)` is a defined arrangement and the resolution of the previous section applies unchanged.

The definition is brief. Everything FINDDOCSCONTAINING claims is contained in the predicate `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅`. The remainder of this ASN unpacks what that predicate guarantees.

*Only content sharing can satisfy the predicate.* The range `ran(Σ.M(d))` carries both content-subspace and link-subspace images: by S3★, a content-subspace V-position routes into `dom(Σ.C)` and a link-subspace V-position into `dom(Σ.L)` (and by CL-OWN, ASN-0047, the latter are exactly `d`'s own links). S3★ is conditional — it routes positions whose subspace is `s_C` or `s_L` but is silent on any V-position of a third subspace; to conclude that *every* image of `M(d)` lands in `dom(Σ.C) ∪ dom(Σ.L)` we also invoke S3★-aux (SubspaceExhaustiveness, ASN-0047), which forecloses a third subspace: `(A d, v : v ∈ dom(M(d)) : subspace(v) = s_C ∨ subspace(v) = s_L)`. The link-subspace portion can never contribute a match. We discharged the source side already — `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` by subspace confinement (proven directly from PC, with no appeal to S3★-aux) — and the target side is its dual: the link-subspace images lie in `dom(Σ.L)`, which is disjoint from `dom(Σ.C)` (ASN-0047 L14, StoreDisjointness: `dom(C) ∩ dom(L) = ∅`). Therefore `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ⊆ (dom(Σ.C) ∪ dom(Σ.L)) ∩ dom(Σ.C) = dom(Σ.C)`, where the left factor `ran(Σ.M(d)) ⊆ dom(Σ.C) ∪ dom(Σ.L)` is S3★ ∧ S3★-aux and the right factor `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` is the subspace-confinement subset claim above; the product set evaluates to `dom(Σ.C)` since `dom(Σ.C) ⊆ dom(Σ.C) ∪ dom(Σ.L)`. A document is returned because it shares *byte content*, never because it shares a *link* address. This is what justifies calling the operation content-transclusion discovery.

The empty query is the boundary case. When `Q = ∅`, the union `iaddrs(∅)(Σ) = ⋃_{(d_s, σ) ∈ ∅} ...` is the empty set, so for every `d ∈ Σ.E_doc` the intersection `ran(Σ.M(d)) ∩ ∅ = ∅` is empty. Therefore `find(∅)(Σ) = ∅`. The operation is total on the empty input — no special case is needed in the definition.

## A worked scenario

We exhibit a state in which several documents share content through transclusion — including one document that references two distinct I-addresses, with one of them repeated at two non-adjacent positions — and trace what FINDDOCSCONTAINING returns for both a single-address query and a multi-address query.

Start from `Σ₀`, whose only entity is the bootstrap node `n₀ = [1]` (`E₀ = {n₀}`, `Node(n₀)`, so `(E₀)_doc = (E₀)_account = ∅`). No document can be created directly at `Σ₀`: a document `d` has `zeros(d) = 2`, and EntityHierarchy (P8, ASN-0047) demands `parent(d) ∈ E` — its account prefix — which does not yet exist. So we first mint the node-descendant → account → document scaffold, discharging `parent ∈ E` at each entity creation, then apply the content transitions. Each precondition is discharged by the prior state; we narrate the result:

1. K.δ creates account `acct = inc(n₀, 2) ∈ E_account` by case (ii) descent (`k = 2`), operand `n₀ ∈ E₀` with `zeros(n₀) = 0 ≤ 1`. `parent(acct) = n₀ ∈ E` discharges P8; `zeros(acct) = 1` (K.δ-ID.zeros-2).
2. K.δ creates document `d_A = inc(acct, 2) ∈ E_doc` by case (ii) descent (`k = 2`), operand `acct ∈ E` with `zeros(acct) = 1 ≤ 1`. `parent(d_A) = acct ∈ E` discharges P8; `zeros(d_A) = 2`, so `Document(d_A)` (activates `A_C(d_A)` and `A_L(d_A)`).
3. K.α emits one content I-address `a₁` under `d_A`: `a₁ = [d_A.0.s_C.1]`, `Σ.C(a₁) = val_A` for some value `val_A ∈ Val`, `origin(a₁) = d_A`.
4. K.μ⁺ binds `M(d_A)(v_A) = a₁`, where `v_A = [s_C, 1]` is the minimum content-subspace V-position of `d_A` (D-MIN★, depth `m_C = 2`).
5. K.ρ records provenance: `(a₁, d_A) ∈ R`.
6. K.δ creates document `d_B = inc(d_A, 0) ∈ E_doc` by case (ii) sibling (`k = 0`), operand `d_A ∈ E` with `¬Node(d_A)`. `parent(d_B) = parent(d_A) = acct ∈ E` (K.δ-ID.parent-0) discharges P8; `zeros(d_B) = zeros(d_A) = 2` (K.δ-ID.zeros-0), so `Document(d_B)`.
7. K.μ⁺ binds `M(d_B)(v_B) = a₁`, where `v_B = [s_C, 1]` is the minimum content-subspace V-position of `d_B`. This is transclusion: the I-address `a₁` allocated under `d_A` is now also referenced from `d_B`'s arrangement, *without* a new K.α emission. The bind is licensed by S3★ since `a₁ ∈ dom(C)`.
8. K.ρ records provenance: `(a₁, d_B) ∈ R`. The composite (steps 6–8) discharges J1★ (ASN-0047): the content-subspace range of `M(d_B)` gains a new entry `a₁`, which forces `(a₁, d_B) ∈ R'`. The converse coupling J1'★ holds symmetrically — the new provenance entry corresponds to a range-new I-address.
9. K.δ creates a third document `d_C = inc(d_B, 0) ∈ E_doc` by case (ii) sibling (`k = 0`), operand `d_B ∈ E` with `¬Node(d_B)`. `parent(d_C) = parent(d_B) = acct ∈ E` (K.δ-ID.parent-0) discharges P8; `zeros(d_C) = 2`, so `Document(d_C)` (activates `A_C(d_C)`).
10. K.α emits one content I-address `a₂` under `d_C`: `a₂ = [d_C.0.s_C.1]`, `Σ.C(a₂) = val_C` for some value `val_C ∈ Val`, `origin(a₂) = d_C`. Since `a₂` is allocated under `d_C`'s own sub-allocator while `a₁` is allocated under `d_A`'s, the two are distinct I-addresses: `a₂ ≠ a₁` (their tumbler prefixes differ at the document field).
11. K.μ⁺ binds `M(d_C)(v_C) = a₂`, where `v_C = [s_C, 1]` is the minimum content-subspace V-position of `d_C`. K.ρ records `(a₂, d_C) ∈ R`. Document `d_C` references only its own native content `a₂`; it does not transclude `a₁`.
12. K.δ creates a fourth document `d_D = inc(d_C, 0) ∈ E_doc` by case (ii) sibling (`k = 0`), operand `d_C ∈ E` with `¬Node(d_C)`. `parent(d_D) = parent(d_C) = acct ∈ E` (K.δ-ID.parent-0) discharges P8; `zeros(d_D) = 2`, so `Document(d_D)`.
13. K.μ⁺ binds three contiguous content-subspace positions of `d_D`, all by transclusion (no new K.α): `M(d_D)(w₁) = a₁`, `M(d_D)(w₂) = a₂`, `M(d_D)(w₃) = a₁`, where `w_k = [s_C, k]` are the content-subspace V-positions of `d_D` (D-SEQ★, depth `m_C = 2`, positions `1 ≤ k ≤ 3`, so D-CTG★ and D-MIN★ hold). K.ρ records `(a₁, d_D)` and `(a₂, d_D)`. Positions `w₁` and `w₃` both reference `a₁`: distinct V-positions of a single document may share an I-address (M13, SharedContent), and the two occurrences are permanently independent arrangement entries (M14, IndependentOccurrences).

*Composite structure.* ValidCompositeAmended (ASN-0047) evaluates the coupling constraints J0, J1★, and J1'★ *only between the initial and final state of each composite*, so reachability is not established step-by-step but at composite boundaries. The thirteen steps group into four valid composites — the allocate–place–record triples are the natural grouping — and we confirm the coupling at each boundary:

- **Composite 1 (steps 1–5):** the `n₀ → acct → d_A` scaffold, then `a₁`'s allocation (K.α), placement (K.μ⁺), and provenance (K.ρ). At the boundary `a₁` is the sole freshly-allocated I-address and it appears in `M(d_A)(v_A)`, discharging J0; `a₁` is range-new to `M(d_A)`'s content subspace, so J1★ forces `(a₁, d_A) ∈ R'` (recorded at step 5), and J1'★ holds since that lone new provenance entry corresponds to the range-new `a₁`.
- **Composite 2 (steps 6–8):** `d_B`'s creation (K.δ) and its transclusion of `a₁` (K.μ⁺, K.ρ). This is the canonical *transcluding discharge*, which every later transcluding composite repeats verbatim: no I-address is freshly allocated — the transcluded addresses are already in `dom(C)` — so J0 is vacuous; each transcluded address that is range-new to the document's content subspace forces a provenance entry under J1★, and J1'★ holds symmetrically since each new provenance entry corresponds to one such range-new address. Here `a₁ ∈ dom(C)` already, `a₁` is range-new to `M(d_B)`'s content subspace, so J1★ forces `(a₁, d_B) ∈ R'`.
- **Composite 3 (steps 9–11):** `d_C`'s creation (K.δ) and its native `a₂` (K.α, K.μ⁺, K.ρ). `a₂` is freshly allocated and appears in `M(d_C)(v_C)`, discharging J0; J1★ and J1'★ couple `(a₂, d_C)` to the range-new `a₂`.
- **Composite 4 (steps 12–13):** `d_D`'s creation (K.δ) and its three transcluding binds (K.μ⁺, K.ρ). The range-new addresses are `a₁` and `a₂`, so the transcluding discharge of Composite 2 applies, forcing `(a₁, d_D), (a₂, d_D) ∈ R'`. The repeated bind of `a₁` at `w₃` adds no further range-new content, so it triggers no additional provenance obligation.

Each composite also satisfies clause (1) of ValidCompositeAmended — every atomic step's elementary precondition holds at the intermediate state, as narrated above. The state `Σ` is therefore reached by a finite sequence of valid composites, hence reachable, so ASN-0047's invariants hold at `Σ`.

The resulting state `Σ` has:

  `Σ.E_doc ⊇ {d_A, d_B, d_C, d_D}`,   `Σ.C ⊇ {a₁ ↦ val_A, a₂ ↦ val_C}`,   `Σ.M(d_A) = {v_A ↦ a₁}`,   `Σ.M(d_B) = {v_B ↦ a₁}`,   `Σ.M(d_C) = {v_C ↦ a₂}`,   `Σ.M(d_D) = {[s_C,1] ↦ a₁, [s_C,2] ↦ a₂, [s_C,3] ↦ a₁}`,   `origin(a₁) = d_A`,   `origin(a₂) = d_C`

Construct the query `Q = {(d_A, σ_A)}` with `σ_A = (v_A, δ(1, 2))` — a single-position level-uniform span starting at `v_A` with width 1 in the content subspace.

**Resolution.** The vspec preconditions hold: `subspace(v_A) = s_C`, `Pos(δ(1, 2))`, `actionPoint(δ(1, 2)) = 2 ≥ 2`, `actionPoint(δ(1, 2)) = 2 = #v_A = 2`, `#δ(1, 2) = 2 = #v_A`. Computing the reach: `v_A ⊕ δ(1, 2) = [s_C, 2]` by TumblerAdd (position 1 lies below the action point and is copied from `v_A`; position 2 is the action point itself and sums to `1 + 1 = 2`). So the span denotes the half-open interval

  `⟦σ_A⟧ = {t ∈ T : [s_C, 1] ≤ t < [s_C, 2]}`

This set is infinite as a subset of `T`: by T1 case (ii), every extension `[s_C, 1, x₁, ..., x_m]` of any depth ≥ 3 exceeds `[s_C, 1]` (proper prefix); by T1 case (i) at position 2, every such tumbler lies below `[s_C, 2]` since `1 < 2`. The depth-2 tumblers in `⟦σ_A⟧` are exactly `{[s_C, 1]} = {v_A}`, but `⟦⋅⟧` is not depth-restricted. The intersection with `dom(M(d_A)) = {v_A}` filters the entire infinite reach down to a single position:

  `⟦σ_A⟧ ∩ dom(M(d_A)) = {v_A}`

Positions in `⟦σ_A⟧ \ dom(M(d_A))` are silently dropped (F-FILT). Hence:

  `iaddrs_one(d_A, σ_A)(Σ) = { M(d_A)(v) : v ∈ {v_A} } = { M(d_A)(v_A) } = { a₁ }`

  `iaddrs(Q)(Σ) = { a₁ }`

**Find.** Evaluate the membership predicate at each `d ∈ E_doc`:

  `d = d_A`: `ran(M(d_A)) ∩ {a₁} = {a₁} ∩ {a₁} = {a₁} ≠ ∅`, so `d_A ∈ find(Q)(Σ)`.
  `d = d_B`: `ran(M(d_B)) ∩ {a₁} = {a₁} ∩ {a₁} = {a₁} ≠ ∅`, so `d_B ∈ find(Q)(Σ)`.
  `d = d_C`: `ran(M(d_C)) ∩ {a₁} = {a₂} ∩ {a₁} = ∅` (since `a₂ ≠ a₁`), so `d_C ∉ find(Q)(Σ)`. This is the exclusion direction against a concrete non-containing document: `d_C` is a present member of `E_doc` with a non-empty arrangement, yet its range shares no I-address with `iaddrs(Q)(Σ)`, so the membership predicate evaluates to *false*.
  `d = d_D`: `ran(M(d_D)) ∩ {a₁} = {a₁, a₂} ∩ {a₁} = {a₁} ≠ ∅`, so `d_D ∈ find(Q)(Σ)`. `d_D` transcludes `a₁` (at two positions) alongside `a₂`; one shared address suffices.
  All other `d ∈ E_doc`: `a₁ ∉ ran(M(d))` (those documents reference no I-addresses), so `d ∉ find(Q)(Σ)`.

Therefore `find(Q)(Σ) = {d_A, d_B, d_D}` — `d_C` excluded.

**A multi-address query.** The singleton query `Q` resolves to one I-address, so it cannot exercise partial overlap: with `|iaddrs(Q)(Σ)| = 1`, any non-empty intersection *is* the whole resolved set, and "references a proper portion" and "references the whole" are indistinguishable. We construct a second query whose resolution carries two I-addresses and whose source decomposes into more than one block. Take `Q_D = {(d_D, σ_D)}` with `σ_D = (w₁, δ(3, 2))` — a width-3 content-subspace span from `w₁ = [s_C, 1]`. Its reach is `w₁ ⊕ δ(3, 2) = [s_C, 4]` (position 1 below the action point is copied; position 2 sums to `1 + 3 = 4`), so

  `⟦σ_D⟧ ∩ dom(M(d_D)) = {[s_C,1], [s_C,2], [s_C,3]} = {w₁, w₂, w₃}`

*Multi-block resolution.* The restriction `f = M(d_D)|⟦σ_D⟧` maps `w₁ ↦ a₁`, `w₂ ↦ a₂`, `w₃ ↦ a₁`. No two consecutive positions are I-adjacent: `a₂ ≠ shift(a₁, 1)` and `a₁ ≠ shift(a₂, 1)`, because `origin(a₁) = d_A ≠ d_C = origin(a₂)` forbids cross-origin I-adjacency (M16, CrossOriginMergeImpossibility). So the unique maximally merged decomposition (C1a) splits into three width-1 blocks `β₁ = (w₁, a₁, 1)`, `β₂ = (w₂, a₂, 1)`, `β₃ = (w₃, a₁, 1)`, and

  `resolve(d_D, σ_D) = ⟨(a₁, 1), (a₂, 1), (a₁, 1)⟩`   (K = 3 blocks, not the degenerate K = 1)

The set-flattening absorbs the duplicate `a₁` carried by *both* `β₁` and `β₃` — the dedup step that the singleton query left untested:

  `{ a + k : (a, n) ∈ resolve(d_D, σ_D) ∧ 0 ≤ k < n } = {a₁, a₂, a₁} = {a₁, a₂}`

which equals `iaddrs_one(d_D, σ_D)(Σ) = { M(d_D)(v) : v ∈ {w₁, w₂, w₃} } = {a₁, a₂}` computed directly. The resolve-equivalence of the Resolution section is thus checked against a concrete multi-block arrangement with a shared I-address across blocks, not merely asserted. Hence `iaddrs(Q_D)(Σ) = {a₁, a₂}`.

*Find with proper-subset references.* Evaluate the predicate at each document:

  `d = d_A`: `ran(M(d_A)) ∩ {a₁, a₂} = {a₁} ∩ {a₁, a₂} = {a₁} ≠ ∅`, so `d_A ∈ find(Q_D)(Σ)`. `d_A` references only `a₁` — a *proper subset* of the two-address query.
  `d = d_B`: `{a₁} ∩ {a₁, a₂} = {a₁} ≠ ∅`, so `d_B ∈ find(Q_D)(Σ)`. Proper subset again.
  `d = d_C`: `{a₂} ∩ {a₁, a₂} = {a₂} ≠ ∅`, so `d_C ∈ find(Q_D)(Σ)`. `d_C` references only `a₂` — the *other* address of the query, disjoint from `d_A`'s and `d_B`'s share.
  `d = d_D`: `{a₁, a₂} ∩ {a₁, a₂} = {a₁, a₂} ≠ ∅`, so `d_D ∈ find(Q_D)(Σ)`. The whole resolved set.

Therefore `find(Q_D)(Σ) = {d_A, d_B, d_C, d_D}`. Here `d_A` (sharing only `a₁`) and `d_C` (sharing only `a₂`) each qualify on one address out of two, sharing *disjoint* fragments of the query — the empty/non-empty intersection distinction is genuinely tested, since neither references what the other does, yet both belong.

**What this verifies.**

- *F-SHARE.* `d_A`, `d_B`, and `d_D` are all discovered by the same query `Q`, demonstrating cross-document discovery through a shared I-address. The query named only `(d_A, σ_A)` — `d_B` and `d_D` were not mentioned — yet both appear because their arrangements reference the resolved I-address `a₁`.
- *F-DIST.* Each document appears exactly once in `find(Q)(Σ) = {d_A, d_B, d_D}`, despite all three satisfying the predicate. The result is a set; `d_A` is not duplicated even though it is both the source-document of `Q` and a member of the result, and `d_D` is not duplicated even though it references `a₁` at two distinct positions `w₁` and `w₃`.
- *F-PART.* Demonstrated against the two-address query `Q_D` with `iaddrs(Q_D)(Σ) = {a₁, a₂}`. Both `d_A` (referencing only `a₁`) and `d_C` (referencing only `a₂`) are included — each shares a *proper subset* of the resolved set, and their shares are disjoint. A single shared I-address suffices; the operation does not require a document to reference all of `iaddrs(Q_D)`, nor any particular portion of the queried span. The singleton query `Q` cannot exhibit this, since with one resolved address every non-empty intersection is the whole set.
- *Resolve-equivalence (multi-block).* For `Q_D`, the source `d_D` decomposes into three maximal-run blocks `⟨β₁, β₂, β₃⟩`, with `β₁` and `β₃` carrying the same I-address `a₁`. The set-flattening of `resolve(d_D, σ_D) = ⟨(a₁,1),(a₂,1),(a₁,1)⟩` dedupes the repeated `a₁` to `{a₁, a₂}`, matching `iaddrs_one(d_D, σ_D)(Σ)`. The multi-block, shared-I-address case of the Resolution section is thereby verified concretely rather than only asserted.
- *F-SOUND (exclusion).* `d_C` references content (`a₂`) but shares no I-address with `iaddrs(Q)(Σ) = {a₁}`, so the membership predicate evaluates to *false* and `d_C ∉ find(Q)(Σ)`. The biconditional is exercised in its harder, negative direction against a concrete non-containing document — membership is not merely an absence of mention but a tested empty intersection.
- *F-FILT.* The span `⟦σ_A⟧` is an infinite subset of `T`, but the intersection with `dom(M(d_A)) = {v_A}` reduces it to a single position. The operation does not reject `σ_A` for naming positions outside `d_A`'s arrangement — unresolvable positions contribute nothing and the query reads charitably over what is currently bound.
- *F-CUR.* The result depends only on the current arrangements `Σ.M(d)`. Were a later K.μ⁻ to contract `M(d_B)` to remove `v_B`, the query `Q` would return `{d_A, d_D}` — `d_B` would no longer be currently containing, even though `(a₁, d_B) ∈ R` would persist (P2).
- *Home/transcluding recovery.* `origin(a₁) = d_A` (grounded in `E_doc` by ASN-0047 P6, ExistentialCoherence), so applying the `origin(a)`-comparison recipe of *Discovery through sharing* to this state recovers that `d_A` is `a₁`'s home document while `d_B` and `d_D` transclude it.

**A cross-depth query.** Every document above has common content depth `m_C = 2`, so neither the cross-depth subtree capture (`#u < m`) nor the interior-action-point rejection (`#u ≥ 3`) argued in *The query* can be exercised against an actual arrangement — both require a deeper source. We extend the construction with one depth-3 document, reaching a state `Σ⁺` that adds `d_E` to `Σ`:

14. K.δ creates `d_E = inc(d_D, 0) ∈ E_doc` by case (ii) sibling (`k = 0`), operand `d_D ∈ E` with `¬Node(d_D)`. `parent(d_E) = parent(d_D) = acct ∈ E` (K.δ-ID.parent-0) discharges P8; `zeros(d_E) = 2`, so `Document(d_E)` (activates `A_C(d_E)`).
15. K.μ⁺ binds three content-subspace positions of `d_E` at common depth `m_C = 3` — S8a fixes the depth from scratch at first insertion at any value `≥ 2`, here 3 — all by transclusion (no new K.α): `M(d_E)([s_C, 1, 1]) = a₁`, `M(d_E)([s_C, 1, 2]) = a₂`, `M(d_E)([s_C, 1, 3]) = a₁`. By D-SEQ★ at depth 3 the positions are `{[s_C, 1, k] : 1 ≤ k ≤ 3}`, contiguous (D-CTG★) with minimum `[s_C, 1, 1]` (D-MIN★). K.ρ records `(a₁, d_E)` and `(a₂, d_E)`.

These two steps form a fifth valid composite: the range-new addresses are `a₁` and `a₂`, so the transcluding discharge of Composite 2 applies, forcing `(a₁, d_E), (a₂, d_E) ∈ R'`. The extended state adds `Σ⁺.M(d_E) = {[s_C,1,1] ↦ a₁, [s_C,1,2] ↦ a₂, [s_C,1,3] ↦ a₁}`, leaving every other arrangement as in `Σ`.

Now submit the *shallow* vspec `Q_E = {(d_E, σ_E)}` with `σ_E = ([s_C, 1], δ(1, 2))`, so `u = [s_C, 1]` has `#u = 2 < m_C = 3` — the cross-depth case.

**Resolution.** The vspec preconditions hold: `subspace(u) = s_C`, `Pos(δ(1, 2))`, `actionPoint(δ(1, 2)) = 2 = #u ≥ 2`, `#δ(1, 2) = 2 = #u`. The reach is `u ⊕ δ(1, 2) = [s_C, 2]` (position 1 below the action point is copied from `u`; position 2 is the action point, summing `1 + 1 = 2`). So `⟦σ_E⟧ = {t : [s_C, 1] ≤ t < [s_C, 2]}`. Each `[s_C, 1, k]` is a proper extension of the prefix `[s_C, 1]`, hence exceeds it by T1 case (ii), and lies below `[s_C, 2]` by T1 case (i) at position 2 (`1 < 2`). Therefore

  `⟦σ_E⟧ ∩ dom(M(d_E)) = {[s_C,1,1], [s_C,1,2], [s_C,1,3]}`

— the *entire* depth-3 subtree hanging under the depth-2 anchor `[s_C, 1]`, captured by a span the user anchored at a single coarse coordinate. This is the *"prefix names subtree"* semantics made concrete. Resolving:

  `iaddrs(Q_E)(Σ⁺) = { M(d_E)(v) : v ∈ {[s_C,1,1], [s_C,1,2], [s_C,1,3]} } = {a₁, a₂}`

**Find.** Evaluate `ran(M(d)) ∩ {a₁, a₂} ≠ ∅` at each document: `d_A` (`{a₁}`), `d_B` (`{a₁}`), `d_C` (`{a₂}`), `d_D` (`{a₁, a₂}`), and `d_E` (`{a₁, a₂}`) all qualify. So

  `find(Q_E)(Σ⁺) = {d_A, d_B, d_C, d_D, d_E}`

The coarse shallow anchor — naming a single depth-2 coordinate over a depth-3 source — discovered the full transclusion community of the subtree's content, confirming the subtree-capture intent against a concrete result set rather than stopping at the abstract `⟦σ⟧ ∩ dom = n positions`.

**Interior action point, rejected against an arrangement.** With `d_E` at depth 3, the over-collection foreclosed in *The query* — abstract there for want of a deep source — is now exhibitable against a live arrangement. The coarse span `σ' = ([s_C, 1, 2], [0, 1, 0])` has action point 2, *interior* to `#u = 3`; its reach is `[s_C, 1, 2] ⊕ [0, 1, 0] = [s_C, 2, 2]`, so `⟦σ'⟧ ∩ dom(M(d_E)) = {[s_C,1,2], [s_C,1,3]}` — positions 2 *and* 3, though the user named position 2 alone. This is the breadth-wise sibling sweep: the displacement acts on the prefix component the anchor fixes, dragging in a sibling the anchor's prefix does not name. The `actionPoint(ℓ) = #u` precondition rejects `σ'` outright (`2 ≠ 3`). The well-formed alternative `σ'' = ([s_C, 1, 2], δ(1, 3))` has action point `3 = #u`, reach `[s_C, 1, 3]`, and `⟦σ''⟧ ∩ dom(M(d_E)) = {[s_C, 1, 2]}` — exactly the named position. The contrast with `σ_E` is the discrimination the precondition is for: `σ_E` descends *depth-wise* into the subtree of the coordinate it names (permitted), while `σ'` sweeps *breadth-wise* across a sibling of a fixed prefix component (forbidden).

## Completeness and soundness

The membership criterion is a biconditional — the definition of `find(Q)(Σ)`:

  `d ∈ find(Q)(Σ)  ⟺  d ∈ Σ.E_doc ∧ ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅`

The biconditional decomposes into two directions:

  (⟸) **F-COMP** (completeness): every `d` satisfying the predicate is in `find(Q)(Σ)`.
  (⟹) **F-SOUND** (soundness): every `d ∈ find(Q)(Σ)` satisfies the predicate.

F-COMP and F-SOUND are not independent properties of the abstract operation — they are the two halves of its definition. Together they constitute the definition; separately, they name the obligations on any candidate implementation. An implementation that omits any qualifying document realizes a strict subset of `find` (the `⟸` direction of the definition is violated). An implementation that includes a document not satisfying the predicate realizes a strict superset (the `⟹` direction is violated). Conformance to FINDDOCSCONTAINING means: the returned set coincides with the set characterized by the predicate.

Any returned `d` for which `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) = ∅` is an F-SOUND failure: the abstract specification demands exact correspondence between the returned set and the set characterized by the predicate.

## Partial overlap suffices

The predicate uses `≠ ∅`. A single shared I-address — one `a ∈ ran(Σ.M(d)) ∩ iaddrs(Q)(Σ)` — is sufficient for `d`'s inclusion:

  `d ∈ find(Q)(Σ)  ⟺  d ∈ Σ.E_doc ∧ (E a : a ∈ ran(Σ.M(d)) : a ∈ iaddrs(Q)(Σ))`

The result does not require `d` to reference all of `iaddrs(Q)`; it does not require `d`'s reference to be of any particular extent. A document that transcludes a single sentence from a chapter-length query passage qualifies, alongside documents that transclude the whole.

This is the operative reading of Nelson's "any portion": completeness is over the existence of non-empty intersection, not over inclusion of the whole. The asymmetry matters — a query about a large passage may discover documents that each reference only a tiny fragment of it. The result set has no inherent measure of "how much" each returned document contains; to recover an extent measure, the requester must compute `|ran(Σ.M(d)) ∩ iaddrs(Q)(Σ)|` for each returned `d` separately.

## Set semantics

`find(Q)(Σ)` is a set. Each document appears at most once regardless of how many I-addresses it shares with `iaddrs(Q)`:

  for every `d_* ∈ Σ.E_doc`:   `|{ x ∈ find(Q)(Σ) : x = d_* }| ≤ 1`

A document that transcludes ten distinct passages from a queried chapter is reported once, not ten times. The result enumerates documents, not occurrences.

Set semantics must be stated explicitly because the natural implementation — iterating over each queried I-address and collecting source documents — produces duplicates by default. The specification requires deduplication; an implementation that returns a multiset of `(d, a)` pairs satisfies neither the type signature nor the intent.

## Discovery through sharing

The most architecturally significant consequence concerns transclusion. If I-address `a` is referenced by multiple documents — `a ∈ ran(Σ.M(d))` for several `d` — then a query that resolves to `a` discovers all of them:

  `a ∈ iaddrs(Q)(Σ) ∧ a ∈ ran(Σ.M(d)) ∧ d ∈ Σ.E_doc  ⟹  d ∈ find(Q)(Σ)`

In particular: `a`'s home document (`origin(a)`, grounded in `E_doc` by ASN-0047 P6 — if it itself still references `a`) and every transcluding document are discovered by the same query and reported as equally-qualifying members of the result.

The find operation does not distinguish home from transcluding document. Both reference `a`; both satisfy the predicate. The mechanism is structural — the I-address `a` is the same `a` everywhere it appears, because content has permanent identity (P0). Sharing of content corresponds to identity of I-address; identity of I-address is what `find` tests for.

This makes `find` the structural dual of the read-direction. Reading goes from arrangement to content: given `d`, `M(d)` tells which I-addresses `d` references. Finding goes from content to arrangement: given resolved I-addresses, `find` tells which documents reference them. The two operations are duals over the same `M : E_doc → (T ⇀ T)` structure.

This non-distinction is recoverable from the address structure already returned. For each `a ∈ iaddrs(Q)`, `origin(a)` (a function of `a`'s tumbler alone, grounded in `E_doc` by ASN-0047 P6) names `a`'s home document. Comparing `origin(a)` against each `d ∈ find(Q)` recovers the relationship: `d = origin(a)` means `d` authored `a`; `d ≠ origin(a)` means `d` transcludes `a`. The `find` operation does not need to tag its results because tagging is a function the requester can compute from the data.

## Currency: state dependence

`find(Q)(Σ)` is a function of `Σ`. It depends only on the current state — specifically on `Σ.E_doc` and `Σ.M`. (It reads neither `dom(Σ.C)` nor any content value: `iaddrs(Q)(Σ)` is computed purely as images of `Σ.M(d_s)`, and the membership predicate intersects those images against `ran(Σ.M(d))`. S3★ ∧ S3★-aux (SubspaceExhaustiveness, ASN-0047) supply the standing context that `ran(Σ.M(d)) ⊆ dom(Σ.C) ∪ dom(Σ.L)` — S3★ routes the two known subspaces and S3★-aux forecloses a third — but `find` does not consult the content store to evaluate it.)

  `(Σ.E_doc = Σ'.E_doc) ∧ (A d ∈ Σ.E_doc : Σ.M(d) = Σ'.M(d))  ⟹  find(Q)(Σ) = find(Q)(Σ')`

History does not enter the definition. The operation does not consult past states, past arrangements, or past transitions. It is a pure function of the present.

This is what Nelson's "containing" (present participle) commits to. The predicate is evaluated at the moment of query, not over the lifetime of the docuverse. A document whose arrangement once referenced `a` but has since been contracted (via K.μ⁻ from ASN-0047) is not in `find(Q)` even if it once was. The operation reports current containment, full stop.

F-COMP must be read in this light. Completeness is over the *currently-containing* set, not over the historically-containing set. An implementation that misses a currently-containing document violates F-COMP; one that omits a historically-containing-but-no-longer-current document does not. The two semantics are distinct, and the operation commits to the present-tense reading.

## Permanence and currency reconciled

The strand model retains entities permanently (P1: `Σ.E ⊆ Σ'.E`) and content permanently (P0: `dom(Σ.C) ⊆ dom(Σ'.C)`), but arrangements may shrink. So at first inspection, a document whose arrangement contracted away a reference to `a` appears to "lose" that historical containment from `find`'s perspective irrecoverably — a structural tension between permanence (of content and entities) and currency (of containment).

The reconciliation runs through versioning. When a document is to be modified, the design convention is to derive a new version-document — a fresh entity in `E_doc` whose arrangement is initialized from the original via transclusion — and modify the new version, leaving the original arrangement intact. Because P1 preserves the original document in `E_doc` and no transition is applied to `M(d_original)`, the original remains a present document whose present arrangement still references `a`. `find(Q)(Σ)` still discovers the original under its own tumbler address, distinct from the modified version.

But this reconciliation is convention, not a structural guarantee of the strand model. Nothing prevents direct modification of any document via arrangement contraction — and such direct modification erases the historical reference irrecoverably from `find`'s perspective. The operation knows only current arrangements; it has no memory of past ones.

Two consequences follow:

(i) Historical state queries succeed insofar as historical states persist as their own document-entities. If version `V₁` of document family `D` contained passage `a`, and version `V₂` deleted `a`, then a query resolving to `a` reports `V₁` (which still contains `a`) and excludes `V₂` (which does not). Both are documents in `E_doc`, addressed by distinct tumblers. The model treats them as equally first-class — there is no privileged "current" version, only a set of co-existing version-documents each with its own arrangement.

(ii) Recovering "what documents EVER contained this" — the full historical containment relation — requires a separate mechanism. ASN-0047's provenance relation `R` tracks exactly this: `(a, d) ∈ R` records that `d`'s arrangement once contained `a` in the content subspace, and P2 makes `R` permanent. `find(Q)` does not consult `R`. The two operations have different semantics: `find` returns currently-containing documents; an `R`-based query returns ever-containing documents. They coincide exactly when no arrangement contraction has occurred for any document containing the queried I-addresses; they may differ otherwise.

## Finiteness

  `|find(Q)(Σ)| < ∞`

The argument is three-step:

(a) The initial state has `|Σ₀.E_doc| = 0`. ASN-0047 gives `E₀ = {n₀}` with `Node(n₀)`, so `n₀ ∉ E_doc` and `(E₀)_doc = ∅`.

(b) Each elementary transition adds at most one entity to `E_doc`. Among ASN-0047's *elementary* transitions, only K.δ modifies `E` (its effect is `E' = E ∪ {e}` for a single `e`); the other elementary transitions (K.α, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ) leave `E` unchanged by their frame clauses. The named composite K.μ~ is not atomic; it decomposes into K.μ⁻ + K.μ⁺ (ValidCompositeAmended), both of which appear in the elementary list and fix `E`, so the induction over elementary steps need not enumerate it separately. K.δ adds `e` to `E_doc` only when `Document(e)`, otherwise to `E_node` or `E_account`. Either way, `|E_doc|` grows by at most one per transition.

(c) A reachable state is reached by finitely many *elementary* transitions. ASN-0047's ExtendedReachableStateInvariants characterises every reachable state as "reachable from `Σ₀` by a finite sequence of valid composite transitions" — finite ancestry is by definition of reachability, not a consequence of any single axiom. Each composite is itself, by ValidCompositeAmended, a finite sequence of atomic transitions; a finite concatenation of finite sequences is finite, so the total count `n_elem` of elementary transitions producing any reachable `Σ` is a finite natural number. SequentialTransitionAxiom (ASN-0047) supplies the orthogonal property that each transition is atomic, uninterruptible, and totally ordered, which makes individual elementary transitions countable within such a sequence.

Combining: step (b) bounds the per-elementary-transition growth of `|E_doc|` by one, and step (c) bounds the number of elementary transitions by `n_elem`, so `|Σ.E_doc| ≤ n_elem < ∞` at any reachable `Σ`. (The bound is stated against the elementary count, not the composite count — a single composite may fire several K.δ steps, e.g. node → account → document creation, so `|E_doc|` can exceed the number of composites.) Since `find(Q)(Σ) ⊆ Σ.E_doc`, finiteness follows.

This is worth stating because `iaddrs(Q)` may name content that is widely transcluded — a single popular passage could appear in many documents. The result is bounded only by `E_doc` itself. The operation does not promise a small result, only a finite one. Implementations that must materialize the entire result before returning it should be designed expecting that the result can grow with the docuverse.

## What we do not specify

The returned set has presentation and policy properties we have left unspecified. These are not entailed by the abstract operation, and an implementation may add them without conflicting with the specification, provided the unfiltered semantics remain available.

(i) *Order.* `find(Q)(Σ)` is a set. Some implementations may return its elements in a deterministic order (such as ascending tumbler order on document ISA, naturally arising from a sorted index); others may not. Order is a presentation choice. Two implementations both meeting the specification may return the same elements in different orders, and neither violates the specification by virtue of order alone.

(ii) *Replica freshness.* We have specified `find` as a function of "the" state `Σ`. In a distributed deployment, different nodes may hold different views, and "the current state" is replica-dependent. We have not addressed replication consistency. The specification holds within a single-state perspective; extending it to distributed deployments requires additional commitments about consistency model that lie outside the scope of `find`'s definition.

(iii) *Access-control filtering.* The `find` we specified returns ALL containing documents — public, private, and inaccessible-to-requester alike. Nelson's broader design intent (LM 2/59) is that private documents not visible to the requester should not appear in the result. Whether and how to enforce this is a separable concern: implement `find` as specified, then post-filter against the requester's visibility set. The unfiltered `find` is the abstract basis; filtering is a policy layer overlaid on it.

These omissions are deliberate. They distinguish what FINDDOCSCONTAINING fundamentally is from what specific deployments may add around it. Each is properly the subject of a separate specification.

## Claims Introduced

The Basis column records how each claim relates to the definitions F-iaddrs and F-find. *Definition* indicates a top-level definition; *direct from F-X* indicates that the claim is a definitional consequence — one direction of the defining iff, a type signature unfolded, or a substitution into the definition. *Derived* indicates that further reasoning is required (auxiliary lemmas, induction over reachable states, or composition with foundation invariants).

| Label | Statement | Basis | Status |
|-------|-----------|-------|--------|
| F-iaddrs | `iaddrs : VSpecSet × Σ ⇀ P(T)` with `iaddrs(Q)(Σ) = ⋃_{(d_s, σ) ∈ Q} { Σ.M(d_s)(v) : v ∈ ⟦σ⟧ ∩ dom(Σ.M(d_s)) }`, defined under `wp-defined: (A (d_s, σ) ∈ Q :: d_s ∈ Σ.E_doc)`; subset claim `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` whenever `wp-defined` holds (both sides state-dependent at `Σ`) | definition; subset claim derived from vspec preconditions `subspace(u) = s_C` and `actionPoint(ℓ) ≥ 2` (subspace confinement of `⟦σ⟧` via TumblerAdd prefix-copy + T1) + S3★, gated on `wp-defined` (M1, ASN-0047) | introduced |
| F-find | `find : VSpecSet × Σ ⇀ P(E_doc)` with `find(Q)(Σ) = { d ∈ Σ.E_doc : ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅ }`, defined under the precondition `(A (d_s, σ) ∈ Q :: d_s ∈ Σ.E_doc)` | definition; precondition couples each vspec source to the evaluation state (M1, P1 of ASN-0047) | introduced |
| PC | Prefix confinement: for a vspec `(d_s, σ)` with `σ = (u, ℓ)` and `actionPoint(ℓ) = #u`, every `t ∈ ⟦σ⟧` satisfies `t_j = u_j` for `1 ≤ j < #u` | derived locally from TumblerAdd prefix-copy + T1 case (i) + NAT-order trichotomy (T0); holds without ContentReference well-formedness, so it does not rest on ASN-0058's C0a | introduced |
| F-COMP | Completeness: every `d ∈ Σ.E_doc` with `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅` is in `find(Q)(Σ)` | direct from F-find (⟸ direction of the defining iff) | introduced |
| F-SOUND | Soundness: every `d ∈ find(Q)(Σ)` is in `Σ.E_doc` with `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅` | direct from F-find (⟹ direction of the defining iff) | introduced |
| F-PART | Partial overlap suffices: `d ∈ find(Q)(Σ) ⟺ d ∈ Σ.E_doc ∧ (E a : a ∈ ran(Σ.M(d)) : a ∈ iaddrs(Q)(Σ))` | direct from F-find (unfolding `≠ ∅` of a binary intersection) | introduced |
| F-DIST | `find(Q)(Σ)` is a set; each `d ∈ E_doc` appears at most once | direct from F-find (codomain is `P(E_doc)`) | introduced |
| F-SHARE | Cross-document discovery: `a ∈ iaddrs(Q)(Σ) ∧ a ∈ ran(Σ.M(d)) ∧ d ∈ Σ.E_doc ⟹ d ∈ find(Q)(Σ)` | direct from F-find (sufficient condition for non-empty intersection) | introduced |
| F-CUR | State dependence: `(Σ.E_doc = Σ'.E_doc) ∧ (A d ∈ Σ.E_doc : Σ.M(d) = Σ'.M(d)) ⟹ find(Q)(Σ) = find(Q)(Σ')` | derived from F-find + F-iaddrs (the operation reads only `E_doc` and `M`, both of which are identical at Σ and Σ' by hypothesis) | introduced |
| F-FILT | Silent resolution filtering: positions in `⟦σ⟧ \ dom(Σ.M(d_s))` contribute no I-addresses to `iaddrs(Q)(Σ)` | direct from F-iaddrs (the intersection `⟦σ⟧ ∩ dom(Σ.M(d_s))` excludes such positions) | introduced |
| F-LOC | Source locality: `Σ.M(d_s) = Σ'.M(d_s) ⟹ iaddrs_one(d_s, σ)(Σ) = iaddrs_one(d_s, σ)(Σ')` | direct from F-iaddrs (iaddrs_one references state Σ only via `Σ.M(d_s)`) | introduced |
| F-EMPTY | `find(∅)(Σ) = ∅` | direct from F-find (union over empty index set is empty; intersection with ∅ is empty) | introduced |
| F-FIN | `|find(Q)(Σ)| < ∞` at every reachable state | derived from F-find + ASN-0047 (`Σ₀.E_doc = ∅`; K.δ adds ≤ 1; reachable states have finite transition count) | introduced |

## Open Questions

What relationship between FINDDOCSCONTAINING's current-state result and the historical containment relation `R` must the system guarantee?

Under what conditions must the system reject unresolvable vspec positions rather than silently filter them?

What completeness must FINDDOCSCONTAINING guarantee when the docuverse state is distributed across replicas with possibly divergent views?

What abstract operation must filter FINDDOCSCONTAINING's result by requester visibility?

What completeness must visibility-filtering preserve over the visible subset of documents accessible to the requester?

What invariant must connect FINDDOCSCONTAINING's result immediately before and after a transition that contracts an arrangement?
