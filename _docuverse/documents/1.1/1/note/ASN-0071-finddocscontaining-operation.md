# ASN-0071: FINDDOCSCONTAINING Operation
*2026-05-25*

A reader of a document can ask: *what is in this document?* The answer comes from walking the document's arrangement and resolving each V-position to the content at its I-address — the read-direction.

The same reader can ask the inverse: *what documents contain this content?* This is the search-direction. A scholar tracing a quotation, a system computing royalty for transcluded reuse, a writer enumerating who has cited a passage — each needs to enumerate documents whose arrangements reference some specified material.

We specify what such an operation must do. Following Nelson we call it **FINDDOCSCONTAINING**. The question this ASN answers is: what is its result set? What determines membership, what guarantees govern completeness, and what does the operation deliberately not promise about currency in a permanent address space?

We work within the strand model as extended by ASN-0047. State `Σ` carries the content store `Σ.C : T ⇀ Val`, the link store `Σ.L`, document entities `Σ.E_doc ⊆ Σ.E`, and arrangements `Σ.M(d) : T ⇀ T` for each `d ∈ Σ.E_doc` — partial functions from V-positions to I-addresses satisfying functionality (S2), generalized referential integrity (S3★), and content permanence (P0, which subsumes S0 and S1). Sharing is unrestricted: distinct `(d, v)` pairs may map to the same I-address (ASN-0058 M13, SharedContent), and such co-occurrences are permanently independent arrangement entries (ASN-0058 M14, IndependentOccurrences). The extended state admits two V-subspaces — content (`s_C`) and link (`s_L`) — and S3★ routes each V-position to its appropriate store: `M(d)(v) ∈ dom(C)` when `subspace(v) = s_C`, and `M(d)(v) ∈ dom(L)` when `subspace(v) = s_L`. We assume content has been allocated and arranged through the standard transitions of ASN-0047; we specify only the query, not the operations that produce its inputs.

## The query

Content can be named in two registers. By I-address — "the content at addresses `A`" — purely structural. By V-position with source — "the content of document `d` at positions `σ`" — referenced from where the user encountered it.

We accept the latter. A **vspec** is a pair `(d_s, σ)` where `d_s ∈ Σ.E_doc` names a source document and `σ = (u, ℓ)` is a level-uniform V-span confined to the content subspace — `subspace(u) = s_C`, `Pos(ℓ)`, `actionPoint(ℓ) = #u`, `#ℓ = #u` (level-uniformity, ASN-0053 S6), and `actionPoint(ℓ) ≥ 2` (equivalently `ℓ₁ = 0`: the displacement does not perturb the subspace identifier at position 1; together with `actionPoint(ℓ) = #u` this also forces `#u ≥ 2`). Its denotation `⟦σ⟧` and reach `u ⊕ ℓ` used throughout are ASN-0053's (σ.denotation: `⟦σ⟧ = {t : start(σ) ≤ t < reach(σ)}`; σ.reach: `reach(σ) = start(σ) ⊕ width(σ)`); we apply those definitions rather than restate them below. A **vspec-set** is a finite set `Q = {q₁, q₂, ..., q_k}` of vspecs, possibly drawn from multiple source documents.

We name the claim we need *prefix confinement* (PC): every `t ∈ ⟦σ⟧` agrees with `u` on all components `1 ≤ j < #u`. This is the relaxed analogue of ASN-0058's C0a (which assumes well-formedness), proven here directly from the vspec preconditions `subspace(u) = s_C` and `actionPoint(ℓ) = #u ≥ 2`, with no appeal to well-formedness.

*Componentwise fact.* For any position `p` with `1 ≤ p < #u` *at which `t_p` exists*, `t` cannot first disagree with `u` at `p`. Since `p < #u = actionPoint(ℓ)`, TumblerAdd's prefix-copy gives `u_p = (u ⊕ ℓ)_p`; were `t_p ≠ u_p`, NAT-order trichotomy (T0) splits the disagreement at `p` into `t_p < u_p` or `t_p > u_p`, and T1 case (i) at `p` would then force either `t < u` (if `t_p < u_p`) or `t > u ⊕ ℓ` (if `t_p > u_p`), each contradicting `u ≤ t < u ⊕ ℓ`. T0 thus excludes `p` as a *first* point of disagreement, but settling every position needs one further step. Were the disagreement set `{p : 1 ≤ p < #u ∧ t_p exists ∧ t_p ≠ u_p}` non-empty, well-ordering of the positions would furnish it a least element — a first disagreement — which the contradiction just excluded; the set is therefore empty, and `t_p = u_p` wherever `t_p` exists with `p < #u`.

*Totality.* Every `t ∈ ⟦σ⟧` has depth `#t ≥ #u`, so each `t_j` (`1 ≤ j < #u`) exists. Were `#t < #u`, then either `t` agrees with `u` on its whole length — making `t` a proper prefix of `u`, hence `t < u` by T1 case (ii), contradicting `u ≤ t` — or `t` first disagrees with `u` at some position `p ≤ #t < #u`, where `t_p` exists, contradicting the componentwise fact; either way `#t < #u` is impossible.

*Prefix agreement.* The componentwise fact applies at every `1 ≤ j < #u`, so `t_j = u_j` throughout — PC. Its position-1 instance `t₁ = u₁` is subspace confinement, `subspace(t) = s_C` for every `t ∈ ⟦σ⟧`. By PC, `⟦σ⟧` varies only at component `#u` and deeper, so resolution reads exactly the prefix the user named.

## Resolution

For a single vspec `(d_s, σ)`, the resolved I-addresses are those that `d_s`'s current arrangement assigns to positions within the span. For `Σ.M(d_s)` to be a defined arrangement — `dom(Σ.M) = Σ.E_doc` (M1, ASN-0047) — we require `d_s ∈ Σ.E_doc`; under that condition:

  `iaddrs_one(d_s, σ)(Σ) := { Σ.M(d_s)(v) : v ∈ ⟦σ⟧ ∩ dom(Σ.M(d_s)) }`

For a vspec-set `Q`:

  `iaddrs(Q)(Σ) := ⋃_{(d_s, σ) ∈ Q} iaddrs_one(d_s, σ)(Σ)`

Every element of `iaddrs(Q)(Σ)` lies in `dom(Σ.C)` — the subset claim `iaddrs(Q)(Σ) ⊆ dom(Σ.C)`. With each `d_s ∈ Σ.E_doc` (the gating condition under which `iaddrs_one` is defined above), every position consulted by `iaddrs_one` is in the content subspace, so S3★ routes the image into `dom(Σ.C)` rather than `dom(Σ.L)`. We show subspace confinement first, then apply S3★.

*Subspace confinement.* For every `t ∈ ⟦σ⟧`, PC's position-1 instance (proven in *The query*) gives `t₁ = u₁ = s_C`, hence `subspace(t) = s_C`.

*Routing.* Therefore every `v ∈ ⟦σ⟧ ∩ dom(Σ.M(d_s))` is a content-subspace V-position, and S3★ (ASN-0047) routes it: `Σ.M(d_s)(v) ∈ dom(Σ.C)`. The subset claim `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` is read with `Σ` explicit on both sides — the right-hand side is the input state's content store, not a fixed set.

When a vspec `(d_s, σ)` is also a well-formed ContentReference, `iaddrs_one(d_s, σ)(Σ)` equals the set-flattening of ASN-0058's `resolve(d_s, σ)` — concretely, `{ a + k : (a, n) ∈ resolve(d_s, σ) ∧ 0 ≤ k < n }`. We derive the equality in one step. By C1a, `resolve(d_s, σ)` is read off the unique maximally merged block decomposition `⟨β₁, ..., β_K⟩` of the restriction `f = M(d_s)|⟦σ⟧`, with `β_j = (v_j, a_j, n_j)` and `resolve(d_s, σ) = ⟨(a₁, n₁), ..., (a_K, n_K)⟩`. The decomposition covers `dom(f)` exactly (B1, Coverage): `dom(f) = ⟦σ⟧ ∩ dom(M(d_s))` — precisely the index set of `iaddrs_one`. For each block, B3 (Consistency) gives `a_j + k = M(d_s)(v_j + k)` for `0 ≤ k < n_j`, and the `v_j + k` range over `V(β_j)`; by coverage the union of all `V(β_j)` is `dom(f)`. So
> `{ a_j + k : 1 ≤ j ≤ K ∧ 0 ≤ k < n_j } = { M(d_s)(v) : v ∈ dom(f) } = iaddrs_one(d_s, σ)(Σ)`.

The left side is the set-flattening of `resolve`. Set-flattening absorbs duplicate I-addresses: two distinct blocks may carry shared content (ASN-0058 M14), and the same `a` then appears in both — the set union dedupes it, matching `iaddrs_one`'s set codomain. The equality is conditional on well-formedness, which the vspec preconditions relax along two independent axes. *First*, `⟦σ⟧` may contain positions outside `dom(M(d_s))`: ContentReference's well-formedness clause requires every span position to lie in the source's arrangement and so treats such a span as ill-formed, while vspec silently drops the missing positions — the intersection `⟦σ⟧ ∩ dom(Σ.M(d_s))` contributes nothing for them (F-FILT). The query thus reads charitably — as "find documents containing the content at whatever positions of `σ` are currently bound" — rather than insisting on total resolvability. *Second*, the equivalence requires `#u = m_C` — the source's common content depth — which ContentReference condition (iii) (`#ℓ = #u = m`) imposes but the vspec preconditions do not. Where both axes are clear — `#u = m_C` and every span position present — vspec resolution and well-formed-ContentReference resolution coincide exactly.

The resolution of `Q` is the union of independent per-source resolutions, each `iaddrs_one(d_s, σ)(Σ)` depending only on `Σ.M(d_s)` (F-LOC).

## The operation

Given resolved I-addresses, FINDDOCSCONTAINING returns the documents whose arrangements currently reference any of them:

  `find(Q)(Σ) := { d ∈ Σ.E_doc : ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅ }`

*Well-definedness precondition.* The type signature presents `Q` and `Σ` as independent arguments, but `iaddrs(Q)(Σ)` consults `Σ.M(d_s)` for each source `(d_s, σ) ∈ Q`, and `dom(Σ.M) = Σ.E_doc` (M1, ASN-0047). The expression `⟦σ⟧ ∩ dom(Σ.M(d_s))` is therefore meaningful only when `d_s ∈ Σ.E_doc`. We make this explicit as the domain of the partial function `find`:

  `wp-defined:  (A (d_s, σ) ∈ Q :: d_s ∈ Σ.E_doc)`

`find(Q)(Σ)` is defined exactly when `wp-defined` holds at the evaluation state `Σ`. When it holds, every `Σ.M(d_s)` named in `iaddrs(Q)(Σ)` is a defined arrangement and the resolution of the previous section applies unchanged.

*Only content sharing can satisfy the predicate.* The range `ran(Σ.M(d))` carries both content-subspace and link-subspace images: by S3★, a content-subspace V-position routes into `dom(Σ.C)` and a link-subspace V-position into `dom(Σ.L)`. S3★ is conditional — it routes positions whose subspace is `s_C` or `s_L` but is silent on any V-position of a third subspace; to conclude that *every* image of `M(d)` lands in `dom(Σ.C) ∪ dom(Σ.L)` we also invoke S3★-aux (SubspaceExhaustiveness, ASN-0047), which forecloses a third subspace: `(A d, v : v ∈ dom(M(d)) : subspace(v) = s_C ∨ subspace(v) = s_L)`. The link-subspace portion can never contribute a match. We discharged the source side already — `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` by subspace confinement — and the target side is its dual: the link-subspace images lie in `dom(Σ.L)`, which is disjoint from `dom(Σ.C)` (ASN-0047 L14, StoreDisjointness: `dom(C) ∩ dom(L) = ∅`). Therefore `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ⊆ (dom(Σ.C) ∪ dom(Σ.L)) ∩ dom(Σ.C) = dom(Σ.C)`, where the left factor `ran(Σ.M(d)) ⊆ dom(Σ.C) ∪ dom(Σ.L)` is S3★ ∧ S3★-aux and the right factor `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` is the subspace-confinement subset claim above; the product set evaluates to `dom(Σ.C)` since `dom(Σ.C) ⊆ dom(Σ.C) ∪ dom(Σ.L)`. We record this as **F-CONTENT**: every shared address witnessing a match lies in `dom(Σ.C)` — `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ⊆ dom(Σ.C)`. A document is returned because it shares *byte content*, never because it shares a *link* address. This is what justifies calling the operation content-transclusion discovery.

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

*Reachability.* The thirteen steps are the standard allocate–place–record (and create-document) composites of ASN-0047 — entity creation followed by content allocation, placement, and provenance recording — so `Σ` is reachable and ASN-0047's invariants hold at `Σ`.

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

**A cross-depth query.** Every document above has common content depth `m_C = 2`, so neither the cross-depth subtree capture (`#u < m`) nor the interior-action-point rejection (`#u ≥ 3`) can be exercised against an actual arrangement — both require a deeper source. We extend the construction with one depth-3 document, reaching a state `Σ⁺` that adds `d_E` to `Σ`:

14. K.δ creates `d_E = inc(d_D, 0) ∈ E_doc` by case (ii) sibling (`k = 0`), operand `d_D ∈ E` with `¬Node(d_D)`. `parent(d_E) = parent(d_D) = acct ∈ E` (K.δ-ID.parent-0) discharges P8; `zeros(d_E) = 2`, so `Document(d_E)` (activates `A_C(d_E)`).
15. K.μ⁺ binds three content-subspace positions of `d_E` at common depth `m_C = 3` — S8a fixes the depth from scratch at first insertion at any value `≥ 2`, here 3 — all by transclusion (no new K.α): `M(d_E)([s_C, 1, 1]) = a₁`, `M(d_E)([s_C, 1, 2]) = a₂`, `M(d_E)([s_C, 1, 3]) = a₁`. By D-SEQ★ at depth 3 the positions are `{[s_C, 1, k] : 1 ≤ k ≤ 3}`, contiguous (D-CTG★) with minimum `[s_C, 1, 1]` (D-MIN★). K.ρ records `(a₁, d_E)` and `(a₂, d_E)`.

These two steps form another standard transcluding composite of ASN-0047, so `Σ⁺` is reachable. The extended state adds `Σ⁺.M(d_E) = {[s_C,1,1] ↦ a₁, [s_C,1,2] ↦ a₂, [s_C,1,3] ↦ a₁}`, leaving every other arrangement as in `Σ`.

Now submit the *shallow* vspec `Q_E = {(d_E, σ_E)}` with `σ_E = ([s_C, 1], δ(1, 2))`, so `u = [s_C, 1]` has `#u = 2 < m_C = 3` — the cross-depth case.

**Resolution.** The vspec preconditions hold: `subspace(u) = s_C`, `Pos(δ(1, 2))`, `actionPoint(δ(1, 2)) = 2 = #u ≥ 2`, `#δ(1, 2) = 2 = #u`. The reach is `u ⊕ δ(1, 2) = [s_C, 2]` (position 1 below the action point is copied from `u`; position 2 is the action point, summing `1 + 1 = 2`). So `⟦σ_E⟧ = {t : [s_C, 1] ≤ t < [s_C, 2]}`. Each `[s_C, 1, k]` is a proper extension of the prefix `[s_C, 1]`, hence exceeds it by T1 case (ii), and lies below `[s_C, 2]` by T1 case (i) at position 2 (`1 < 2`). Therefore

  `⟦σ_E⟧ ∩ dom(M(d_E)) = {[s_C,1,1], [s_C,1,2], [s_C,1,3]}`

— the *entire* depth-3 subtree hanging under the depth-2 anchor `[s_C, 1]`, captured by a span the user anchored at a single coarse coordinate. These positions *are* current arrangement entries, so F-FILT offers no defense; collecting them is the intended semantics. FINDDOCSCONTAINING is specified to return *"any portion of the material specified ... regardless of where the native copies are located"* (LM 4/63): the user who names the coarse coordinate names its whole subtree — the *"prefix names subtree"* semantics, here made concrete. Resolving:

  `iaddrs(Q_E)(Σ⁺) = { M(d_E)(v) : v ∈ {[s_C,1,1], [s_C,1,2], [s_C,1,3]} } = {a₁, a₂}`

**Find.** Evaluate `ran(M(d)) ∩ {a₁, a₂} ≠ ∅` at each document: `d_A` (`{a₁}`), `d_B` (`{a₁}`), `d_C` (`{a₂}`), `d_D` (`{a₁, a₂}`), and `d_E` (`{a₁, a₂}`) all qualify. So

  `find(Q_E)(Σ⁺) = {d_A, d_B, d_C, d_D, d_E}`

The coarse shallow anchor — naming a single depth-2 coordinate over a depth-3 source — discovered the full transclusion community of the subtree's content, confirming the subtree-capture intent against a concrete result set rather than stopping at the abstract `⟦σ⟧ ∩ dom = n positions`.

**Interior action point, rejected against an arrangement.** With `d_E` at depth 3, the over-collection that the `actionPoint(ℓ) = #u` precondition forecloses — collecting content positions the user never named — can be exhibited against a live arrangement. The coarse span `σ' = ([s_C, 1, 2], [0, 1, 0])` has action point 2, *interior* to `#u = 3`; its reach is `[s_C, 1, 2] ⊕ [0, 1, 0] = [s_C, 2, 2]`, so `⟦σ'⟧ ∩ dom(M(d_E)) = {[s_C,1,2], [s_C,1,3]}` — positions 2 *and* 3, though the user named position 2 alone. This is the breadth-wise sibling sweep: the displacement acts on the prefix component the anchor fixes, dragging in a sibling the anchor's prefix does not name. The `actionPoint(ℓ) = #u` precondition rejects `σ'` outright (`2 ≠ 3`). The well-formed alternative `σ'' = ([s_C, 1, 2], δ(1, 3))` has action point `3 = #u`, reach `[s_C, 1, 3]`, and `⟦σ''⟧ ∩ dom(M(d_E)) = {[s_C, 1, 2]}` — exactly the named position. The contrast with `σ_E` is the discrimination the precondition is for: `σ_E` descends *depth-wise* into the subtree of the coordinate it names (permitted), while `σ'` sweeps *breadth-wise* across a sibling of a fixed prefix component (forbidden).

## Completeness and soundness

The membership criterion is a biconditional — the definition of `find(Q)(Σ)`:

  `d ∈ find(Q)(Σ)  ⟺  d ∈ Σ.E_doc ∧ ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅`

The biconditional decomposes into two directions:

  (⟸) **F-COMP** (completeness): every `d` satisfying the predicate is in `find(Q)(Σ)`.
  (⟹) **F-SOUND** (soundness): every `d ∈ find(Q)(Σ)` satisfies the predicate.

## Partial overlap suffices

The predicate uses `≠ ∅`. A single shared I-address — one `a ∈ ran(Σ.M(d)) ∩ iaddrs(Q)(Σ)` — is sufficient for `d`'s inclusion:

  `d ∈ find(Q)(Σ)  ⟺  d ∈ Σ.E_doc ∧ (E a : a ∈ ran(Σ.M(d)) : a ∈ iaddrs(Q)(Σ))`

The result does not require `d` to reference all of `iaddrs(Q)`; it does not require `d`'s reference to be of any particular extent. A document that transcludes a single sentence from a chapter-length query passage qualifies, alongside documents that transclude the whole.

This is the operative reading of Nelson's "any portion": completeness is over the existence of non-empty intersection, not over inclusion of the whole. The asymmetry matters — a query about a large passage may discover documents that each reference only a tiny fragment of it. The result set has no inherent measure of "how much" each returned document contains; to recover an extent measure, the requester must compute `|ran(Σ.M(d)) ∩ iaddrs(Q)(Σ)|` for each returned `d` separately.

## Set semantics

`find(Q)(Σ)` is a set. Each document appears at most once regardless of how many I-addresses it shares with `iaddrs(Q)`:

  for every `d_* ∈ Σ.E_doc`:   `|{ x ∈ find(Q)(Σ) : x = d_* }| ≤ 1`

A document that transcludes ten distinct passages from a queried chapter is reported once, not ten times. The result enumerates documents, not occurrences.

## Discovery through sharing

A query discovers every document that shares its resolved content. If I-address `a` is referenced by multiple documents — `a ∈ ran(Σ.M(d))` for several `d` — then a query that resolves to `a` discovers all of them:

  `a ∈ iaddrs(Q)(Σ) ∧ a ∈ ran(Σ.M(d)) ∧ d ∈ Σ.E_doc  ⟹  d ∈ find(Q)(Σ)`

In particular: `a`'s home document `origin(a)` (a function of `a`'s tumbler alone, grounded in `E_doc` by ASN-0047 P6) — if it itself still references `a` — and every transcluding document are discovered by the same query and reported as equally-qualifying members of the result.

The find operation does not distinguish home from transcluding document: both reference `a`, both satisfy the predicate. The mechanism is structural — the I-address `a` is the same `a` everywhere it appears, because content has permanent identity (P0); sharing of content corresponds to identity of I-address, and identity of I-address is what `find` tests for. The distinction is nonetheless recoverable from the address structure already returned, so `find` need not tag its results: for each `a ∈ iaddrs(Q)`, `origin(a)` names `a`'s home document, and comparing it against each `d ∈ find(Q)` recovers the relationship — `d = origin(a)` means `d` authored `a`, `d ≠ origin(a)` means `d` transcludes `a`.

## Currency: state dependence

`find(Q)(Σ)` reads only `Σ.E_doc` and `Σ.M`: `iaddrs(Q)(Σ)` is computed purely as images of `Σ.M(d_s)`, and the membership predicate intersects those images against `ran(Σ.M(d))` — neither `dom(Σ.C)`, nor a content value, nor any past state enters.

  `(Σ.E_doc = Σ'.E_doc) ∧ (A d ∈ Σ.E_doc : Σ.M(d) = Σ'.M(d))  ⟹  find(Q)(Σ) = find(Q)(Σ')`

This is what Nelson's "containing" (present participle) commits to. The predicate is evaluated at the moment of query, not over the lifetime of the docuverse. A document whose arrangement once referenced `a` but has since been contracted (via K.μ⁻ from ASN-0047) is not in `find(Q)` even if it once was. The operation reports current containment, full stop. `find` does not consult ASN-0047's provenance relation `R`, which records `(a, d)` permanently (P2): the current-containment result versus the ever-containing relation `R` is deferred (Open Questions). F-COMP must be read in this light — completeness is over the *currently-containing* set: an implementation that misses a currently-containing document violates F-COMP; one that omits a historically-containing-but-no-longer-current document does not.

## Finiteness

  `|find(Q)(Σ)| < ∞`

The argument is three-step:

(a) The initial state has `|Σ₀.E_doc| = 0`. ASN-0047 gives `E₀ = {n₀}` with `Node(n₀)`, so `n₀ ∉ E_doc` and `(E₀)_doc = ∅`.

(b) Each elementary transition adds at most one entity to `E_doc`. Among ASN-0047's *elementary* transitions, only K.δ modifies `E` (its effect is `E' = E ∪ {e}` for a single `e`); the other elementary transitions (K.α, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ) leave `E` unchanged by their frame clauses. K.δ adds `e` to `E_doc` only when `Document(e)`, otherwise to `E_node` or `E_account`. Either way, `|E_doc|` grows by at most one per transition.

(c) A reachable state is reached by finitely many *elementary* transitions. ASN-0047's ExtendedReachableStateInvariants characterises every reachable state as "reachable from `Σ₀` by a finite sequence of valid composite transitions" — finite ancestry is by definition of reachability, not a consequence of any single axiom. Each composite is itself, by ValidCompositeAmended, a finite sequence of atomic transitions; a finite concatenation of finite sequences is finite, so the total count `n_elem` of elementary transitions producing any reachable `Σ` is a finite natural number.

Combining: step (b) bounds the per-elementary-transition growth of `|E_doc|` by one, and step (c) bounds the number of elementary transitions by `n_elem`, so `|Σ.E_doc| ≤ n_elem < ∞` at any reachable `Σ`. (The bound is stated against the elementary count, not the composite count — a single composite may fire several K.δ steps, e.g. node → account → document creation, so `|E_doc|` can exceed the number of composites.) Since `find(Q)(Σ) ⊆ Σ.E_doc`, finiteness follows.

This is worth stating because `iaddrs(Q)` may name content that is widely transcluded — a single popular passage could appear in many documents. The result is bounded only by `E_doc` itself.

## What we do not specify

The returned set has presentation and policy properties we have left unspecified. These are not entailed by the abstract operation, and an implementation may add them without conflicting with the specification, provided the unfiltered semantics remain available.

(i) *Order.* `find(Q)(Σ)` is a set. Some implementations may return its elements in a deterministic order (such as ascending tumbler order on document ISA, naturally arising from a sorted index); others may not. Order is a presentation choice. Two implementations both meeting the specification may return the same elements in different orders, and neither violates the specification by virtue of order alone.

(ii) *Replica freshness.* We specify `find` against a single state `Σ`; replica-divergent views in a distributed deployment are out of scope.

(iii) *Access-control filtering.* The `find` we specified returns ALL containing documents, unfiltered by requester visibility; layering Nelson's visibility policy (LM 2/59) over the unfiltered basis is out of scope.

## Claims Introduced

| Label | Statement | Basis | Status |
|-------|-----------|-------|--------|
| F-iaddrs | `iaddrs : VSpecSet × Σ ⇀ P(T)` with `iaddrs(Q)(Σ) = ⋃_{(d_s, σ) ∈ Q} { Σ.M(d_s)(v) : v ∈ ⟦σ⟧ ∩ dom(Σ.M(d_s)) }`, defined under `wp-defined: (A (d_s, σ) ∈ Q :: d_s ∈ Σ.E_doc)`; subset claim `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` whenever `wp-defined` holds | definition; subset claim proven in *Resolution* (subspace confinement of `⟦σ⟧` + S3★), gated on `wp-defined` | introduced |
| F-find | `find : VSpecSet × Σ ⇀ P(E_doc)` with `find(Q)(Σ) = { d ∈ Σ.E_doc : ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅ }`, defined under the precondition `(A (d_s, σ) ∈ Q :: d_s ∈ Σ.E_doc)` | definition; precondition couples each vspec source to the evaluation state (M1, P1 of ASN-0047) | introduced |
| PC | Prefix confinement: for a vspec `(d_s, σ)` with `σ = (u, ℓ)` and `actionPoint(ℓ) = #u`, every `t ∈ ⟦σ⟧` satisfies `t_j = u_j` for `1 ≤ j < #u` | derived locally from TumblerAdd prefix-copy + T1 case (i) + NAT-order trichotomy (T0) for the per-position case split + well-ordering of positions for the universal closure | introduced |
| F-COMP | Completeness: every `d ∈ Σ.E_doc` with `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅` is in `find(Q)(Σ)` | direct from F-find (⟸ direction of the defining iff) | introduced |
| F-SOUND | Soundness: every `d ∈ find(Q)(Σ)` is in `Σ.E_doc` with `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅` | direct from F-find (⟹ direction of the defining iff) | introduced |
| F-PART | Partial overlap suffices: `d ∈ find(Q)(Σ) ⟺ d ∈ Σ.E_doc ∧ (E a : a ∈ ran(Σ.M(d)) : a ∈ iaddrs(Q)(Σ))` | direct from F-find (unfolding `≠ ∅` of a binary intersection) | introduced |
| F-DIST | `find(Q)(Σ)` is a set; each `d ∈ E_doc` appears at most once | direct from F-find (codomain is `P(E_doc)`) | introduced |
| F-SHARE | Cross-document discovery: `a ∈ iaddrs(Q)(Σ) ∧ a ∈ ran(Σ.M(d)) ∧ d ∈ Σ.E_doc ⟹ d ∈ find(Q)(Σ)` | direct from F-find (sufficient condition for non-empty intersection) | introduced |
| F-CONTENT | Matches occur only via shared content addresses: `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ⊆ dom(Σ.C)` | derived from S3★ ∧ S3★-aux (ASN-0047) ∧ L14 ∧ the `iaddrs ⊆ dom(C)` subset claim | introduced |
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
