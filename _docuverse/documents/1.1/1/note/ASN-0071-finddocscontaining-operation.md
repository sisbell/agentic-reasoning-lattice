# ASN-0071: FINDDOCSCONTAINING Operation
*2026-05-25*

A reader of a document can ask: *what is in this document?* The answer comes from walking the document's arrangement and resolving each V-position to the content at its I-address — the read-direction.

The same reader can ask the inverse: *what documents contain this content?* This is the search-direction. A scholar tracing a quotation, a system computing royalty for transcluded reuse, a writer enumerating who has cited a passage — each needs to enumerate documents whose arrangements reference some specified material.

We specify what such an operation must do. Following Nelson we call it **FINDDOCSCONTAINING**. The question this ASN answers is: what is its result set? What determines membership, what guarantees govern completeness, and what does the operation deliberately not promise about currency in a permanent address space?

Nelson frames the search-direction as a retrieval promise: the system should *"retrieve any portion of the material specified ... regardless of where the native copies are located"* (LM 4/63), so a query about a passage finds documents referencing even a fragment of it, native copy or transclusion alike. The address convention reinforces the reach — *"A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author ... or the entire docuverse"* (LM 4/38) — so a coarse coordinate names everything beneath it.

We work within the strand model as extended by ASN-0047. State `Σ` carries the content store `Σ.C : T ⇀ Val`, the link store `Σ.L`, document entities `Σ.E_doc ⊆ Σ.E`, and arrangements `Σ.M(d) : T ⇀ T` for each `d ∈ Σ.E_doc` — partial functions from V-positions to I-addresses satisfying functionality (S2), generalized referential integrity (S3★), and content permanence (P0, which subsumes S0 and S1). Sharing is unrestricted: distinct `(d, v)` pairs may map to the same I-address (ASN-0058 M13, SharedContent), and such co-occurrences are permanently independent arrangement entries (ASN-0058 M14, IndependentOccurrences). The extended state admits two V-subspaces — content (`s_C`) and link (`s_L`) — and S3★ routes each V-position to its appropriate store: `M(d)(v) ∈ dom(C)` when `subspace(v) = s_C`, and `M(d)(v) ∈ dom(L)` when `subspace(v) = s_L`. We assume content has been allocated and arranged through the standard transitions of ASN-0047; we specify only the query, not the operations that produce its inputs.

## The query

Content can be named in two registers. By I-address — "the content at addresses `A`" — purely structural. By V-position with source — "the content of document `d` at positions `σ`" — referenced from where the user encountered it.

We accept the latter. A **vspec** is a pair `(d_s, σ)` where `d_s` is a document address naming a source document and `σ = (u, ℓ)` is a level-uniform V-span confined to the content subspace — `subspace(u) = s_C`, `Pos(ℓ)`, `actionPoint(ℓ) = #u`, `#ℓ = #u` (level-uniformity, ASN-0053 S6), and `actionPoint(ℓ) ≥ 2` (equivalently `ℓ₁ = 0`: the displacement does not perturb the subspace identifier at position 1; together with `actionPoint(ℓ) = #u` this also forces `#u ≥ 2`). Its denotation `⟦σ⟧` and reach `u ⊕ ℓ` used throughout are ASN-0053's (σ.denotation: `⟦σ⟧ = {t : start(σ) ≤ t < reach(σ)}`; σ.reach: `reach(σ) = start(σ) ⊕ width(σ)`); we apply those definitions rather than restate them below. A **vspec-set** is a finite set `Q = {q₁, q₂, ..., q_k}` of vspecs, possibly drawn from multiple source documents.

A vspec relaxes ASN-0058's `ContentReference (d_s, σ)` by dropping the demands that presume control over the queried source: subspace-non-emptiness `V_{u₁}(d_s) ≠ ∅` (clause i), the depth-match `#u = m_C` (the `= m_C` half of clause iii), and the full-coverage well-formedness requirement. Search must tolerate all three, since a query is posed against a source whose arrangement the requester does not control.

We name the claim we need *prefix confinement* (PC): every `t ∈ ⟦σ⟧` agrees with `u` on all components `1 ≤ j < #u`. This is the relaxed analogue of ASN-0058's C0a; we derive it below from the vspec preconditions `subspace(u) = s_C` and `actionPoint(ℓ) = #u ≥ 2`.

*Componentwise fact.* For any position `p` with `1 ≤ p < #u` *at which `t_p` exists*, `t` cannot first disagree with `u` at `p`. Since `p < #u = actionPoint(ℓ)`, TumblerAdd's prefix-copy gives `u_p = (u ⊕ ℓ)_p`; were `t_p ≠ u_p`, NAT-order trichotomy (T0) splits the disagreement at `p` into `t_p < u_p` or `t_p > u_p`, and T1 case (i) at `p` would then force either `t < u` (if `t_p < u_p`) or `t > u ⊕ ℓ` (if `t_p > u_p`), each contradicting `u ≤ t < u ⊕ ℓ`. T0 thus excludes `p` as a *first* point of disagreement, but settling every position needs one further step. Were the disagreement set `{p : 1 ≤ p < #u ∧ t_p exists ∧ t_p ≠ u_p}` non-empty, well-ordering of the positions would furnish it a least element — a first disagreement — which the contradiction just excluded; the set is therefore empty, and `t_p = u_p` wherever `t_p` exists with `p < #u`.

*Totality.* Every `t ∈ ⟦σ⟧` has depth `#t ≥ #u`, so each `t_j` (`1 ≤ j < #u`) exists. Were `#t < #u`, then either `t` agrees with `u` on its whole length — making `t` a proper prefix of `u`, hence `t < u` by T1 case (ii), contradicting `u ≤ t` — or `t` first disagrees with `u` at some position `p ≤ #t < #u`, where `t_p` exists, contradicting the componentwise fact; either way `#t < #u` is impossible.

*Prefix agreement.* The componentwise fact applies at every `1 ≤ j < #u`, so `t_j = u_j` throughout — PC. Its position-1 instance `t₁ = u₁` is subspace confinement, `subspace(t) = s_C` for every `t ∈ ⟦σ⟧`. By PC, `⟦σ⟧` varies only at component `#u` and deeper, so resolution reads exactly the prefix the user named.

## Resolution

For a single vspec `(d_s, σ)`, the resolved I-addresses are those that `d_s`'s current arrangement assigns to positions within the span. Resolution consults `Σ.M(d_s)` for each source `d_s`, so it is meaningful only at a state `Σ` where each named arrangement is defined — i.e. where each source is an allocated document. We name this semantic precondition

  `wp-defined:  (A (d_s, σ) ∈ Q :: d_s ∈ Σ.E_doc)`

and evaluate throughout this section at a state `Σ` satisfying it:

  `iaddrs_one(d_s, σ)(Σ) := { Σ.M(d_s)(v) : v ∈ ⟦σ⟧ ∩ dom(Σ.M(d_s)) }`

For a vspec-set `Q`:

  `iaddrs(Q)(Σ) := ⋃_{(d_s, σ) ∈ Q} iaddrs_one(d_s, σ)(Σ)`

`iaddrs_one` is the set-valued, deduplicating, coverage-tolerant counterpart of ASN-0058's `resolve(d_s, σ)`. Where `resolve` presumes the well-formed `ContentReference` of that foundation and yields an *ordered* sequence of run/width pairs `⟨(a₁, n₁), ..., (a_k, n_k)⟩` covering the whole span, `iaddrs_one` discards V-order and run structure, deduplicates, and quietly omits any span position absent from `dom(M(d_s))` (F-FILT).

Every element of `iaddrs(Q)(Σ)` lies in `dom(Σ.C)` — the subset claim `iaddrs(Q)(Σ) ⊆ dom(Σ.C)`. With each `d_s ∈ Σ.E_doc` (by `wp-defined`), every position consulted by `iaddrs_one` is in the content subspace, so S3★ routes the image into `dom(Σ.C)` rather than `dom(Σ.L)`. We show subspace confinement first, then apply S3★.

*Subspace confinement.* Every `t ∈ ⟦σ⟧` has `subspace(t) = s_C` — the subspace-confinement corollary already established in *The query* as PC's position-1 instance. We reuse that result rather than re-derive it.

*Routing.* Therefore every `v ∈ ⟦σ⟧ ∩ dom(Σ.M(d_s))` is a content-subspace V-position, and S3★ (ASN-0047) routes it: `Σ.M(d_s)(v) ∈ dom(Σ.C)`.

*Which positions resolve — cross-depth capture in general.* PC fixes the prefix `⟦σ⟧` shares with `u`; we now characterise exactly which arrangement positions the intersection `⟦σ⟧ ∩ dom(M(d_s))` retains, including those deeper than `#u`. Fix a vspec `(d_s, σ)` with `σ = (u, ℓ)`, action point `#u`, and reach `r = u ⊕ ℓ`; since `actionPoint(ℓ) = #u`, TumblerAdd copies `r_j = u_j` for `j < #u` and sums `r_{#u} = u_{#u} + ℓ_{#u}` at the action point. The vspec preconditions place no relation between `#u` and the source's content-subspace depth `m_C` (S8-depth), so a position `v ∈ dom(M(d_s))` may be shallower than, equal to, or deeper than the anchor. We split on this, since the component `v_{#u}` named below exists only when `#v ≥ #u`.

*Positions of depth `#v ≥ #u`.* Here `v_{#u}` is defined, and we claim:

  `v ∈ ⟦σ⟧  ⟺  (A j : 1 ≤ j < #u : v_j = u_j) ∧ u_{#u} ≤ v_{#u} < r_{#u}`

PC already gives the prefix-agreement conjunct for any `v ∈ ⟦σ⟧`. Given that agreement, the two order comparisons reduce to position `#u`. The boundary component values `v_{#u} = u_{#u}` and `v_{#u} = r_{#u}` behave differently according to whether `v` is at the anchor's depth or strictly deeper, so we split the sub-case `#v ≥ #u` into `#v = #u` and `#v > #u`. The equal-depth sub-case is the principal one: by S8-depth every content-subspace `v ∈ dom(M(d_s))` has `#v = m_C`, so whenever the anchor matches the source depth (`#u = m_C`) *every* captured position satisfies `#v = #u`.

*Sub-case `#v = #u`.* Here `v`, `u`, and `r` all share depth `#u` and agree below it, so each pair differs at most at component `#u`. T1 case (i) at `#u` gives `u ≤ v ⟺ u_{#u} ≤ v_{#u}` and `v < r ⟺ v_{#u} < r_{#u}` directly. At the boundary values: `v_{#u} = u_{#u}` forces `v = u`, so `u ≤ v` holds by *equality*; `v_{#u} = r_{#u}` forces `v = r`, which is excluded because `r = reach(σ)` is an *exclusive* upper bound (`r ∉ ⟦σ⟧`) — not by any order relation between `r` and `v`.

*Sub-case `#v > #u`.* Here `v` is strictly deeper than both `u` and `r`. For `u ≤ v`, T1 case (i) at `#u` gives `u ≤ v ⟺ u_{#u} ≤ v_{#u}` (when `v_{#u} = u_{#u}`, `u` is a proper prefix of the deeper `v`, so `u < v` by T1 case (ii) — still `u ≤ v`); for `v < r`, since `r` has depth `#u` and agrees with `v` below `#u`, T1 case (i) at `#u` gives `v < r ⟺ v_{#u} < r_{#u}` (equality `v_{#u} = r_{#u}` makes `r` a proper prefix of the deeper `v`, so `r < v` by T1 case (ii), excluded).

*Positions of depth `#v < #u`.* Such a `v` has no component at index `#u`, so the right-hand conjunct `u_{#u} ≤ v_{#u} < r_{#u}` references an undefined component and cannot hold — `v` is excluded from the right-hand set. On the left, PC's totality clause (*The query*) established that every `t ∈ ⟦σ⟧` has `#t ≥ #u`; hence `v ∉ ⟦σ⟧`, excluding it from the left as well. Both sides drop every position shallower than the anchor, so the characterisation contributes nothing — and costs nothing — for these positions. Intersecting with `dom(M(d_s))`, the two cases combine into:

  `⟦σ⟧ ∩ dom(M(d_s)) = { v ∈ dom(M(d_s)) : #v ≥ #u ∧ (A j : 1 ≤ j < #u : v_j = u_j) ∧ u_{#u} ≤ v_{#u} < r_{#u} }`

where the depth guard `#v ≥ #u` is what makes the remaining conjuncts well-typed.

We name this **PC-RANGE**. The captured set is `⟦σ⟧ ∩ dom(M(d_s))`, parameterised by the action-point width `ℓ_{#u} = r_{#u} − u_{#u}`: it *lies within* the union of `ℓ_{#u}` sibling subtrees, those whose component `#u` ranges over `[u_{#u}, u_{#u} + ℓ_{#u})`. Actual membership is determined by the intersection `∩ dom(M(d_s))`, and within each such subtree by D-SEQ★, which pins the intermediate components `2 ≤ j < #v` of every arrangement position to `1`: most of those geometric subtrees hold no arrangement positions, and if some `u_j ≠ 1` for `2 ≤ j < #u` the intersection is empty even when `#u ≤ m_C`. The width-1 case `ℓ_{#u} = 1` pins `v_{#u} = u_{#u}`, confining the capture to the single subtree under the prefix `u`. PC-RANGE's range condition at component `#u` couples to the arrangement's content-subspace depth `m_C` (S8-depth, which fixes `#v = m_C` for every *content-subspace* `v ∈ dom(M(d_s))`): the comparison `u_{#u} ≤ v_{#u} < r_{#u}` is well-typed exactly when `#u ≤ m_C`.

The depth `m_C` (S8-depth) is well-defined only when `V_{s_C}(d_s) ≠ ∅`, so we split. If `V_{s_C}(d_s) = ∅` the source carries no content-subspace position; since every `v ∈ ⟦σ⟧ ∩ dom(M(d_s))` is content-subspace (PC's position-1 instance gives `subspace(v) = s_C`), the intersection is empty and `iaddrs_one(d_s, σ)(Σ) = ∅` trivially. If `V_{s_C}(d_s) ≠ ∅` then `m_C` is defined, and when additionally `#u > m_C` the anchor is finer than every content-subspace arrangement position: by S8-depth every content-subspace `v ∈ dom(M(d_s))` has `#v = m_C < #u`, so the depth-`#v < #u` case of the characterisation excludes each such `v` from `⟦σ⟧`; the intersection is empty and `iaddrs_one(d_s, σ)(Σ) = ∅`. We record the latter as **F-DEEP**: `V_{s_C}(d_s) ≠ ∅ ∧ #u > m_C ⟹ iaddrs_one(d_s, σ)(Σ) = ∅` — a vspec whose anchor is deeper than the source's content-subspace arrangement depth resolves to nothing.

The resolution of `Q` is the union of independent per-source resolutions, each `iaddrs_one(d_s, σ)(Σ)` depending only on `Σ.M(d_s)`.

## The operation

Given resolved I-addresses, FINDDOCSCONTAINING returns the documents whose arrangements currently reference any of them:

  `find(Q)(Σ) := { d ∈ Σ.E_doc : ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅ }`

This biconditional is its own completeness and soundness statement: its (⟸) direction — every `d ∈ Σ.E_doc` satisfying the predicate is returned — is recorded as **F-COMP**, and its (⟹) direction — every returned `d` satisfies the predicate — as **F-SOUND**. The `P(E_doc)` codomain likewise makes `find(Q)(Σ)` a set, so each document appears at most once (**F-DIST**) — a document transcluding ten queried passages is reported once, not ten times. The result enumerates documents, not occurrences.

*Well-definedness precondition.* `find` inherits `wp-defined` (named in *Resolution*) as its domain: `find(Q)(Σ)` is defined exactly when `wp-defined` holds at the evaluation state `Σ`, since `find` invokes `iaddrs(Q)(Σ)`, whose definedness `wp-defined` already establishes. When it holds, every `Σ.M(d_s)` named in `iaddrs(Q)(Σ)` is a defined arrangement and the resolution of the previous section applies unchanged.

*Only content sharing can satisfy the predicate.* The range `ran(Σ.M(d))` carries both content-subspace and link-subspace images: by S3★, a content-subspace V-position routes into `dom(Σ.C)` and a link-subspace V-position into `dom(Σ.L)`. By S3★ ∧ S3★-aux (SubspaceExhaustiveness, ASN-0047), `ran(Σ.M(d)) ⊆ dom(Σ.C) ∪ dom(Σ.L)`. The link-subspace portion can never contribute a match. We discharged the source side already — `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` by subspace confinement — and the target side is its dual: the link-subspace images lie in `dom(Σ.L)`, which is disjoint from `dom(Σ.C)` (ASN-0047 L14, StoreDisjointness: `dom(C) ∩ dom(L) = ∅`). From `ran(Σ.M(d)) ⊆ dom(Σ.C) ∪ dom(Σ.L)` (S3★ ∧ S3★-aux) and `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` (the subspace-confinement subset claim above), `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ⊆ (dom(Σ.C) ∪ dom(Σ.L)) ∩ dom(Σ.C) = dom(Σ.C)`. We record this as **F-CONTENT**: every shared address witnessing a match lies in `dom(Σ.C)` — `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ⊆ dom(Σ.C)`. A document is returned because it shares *byte content*, never because it shares a *link* address.

*Source self-inclusion.* Whenever a source resolves any I-address at all, the source document is itself among the results — querying a document's own passage must return at least that document, the formal bridge between the read-direction (what `d_s` contains) and the search-direction (who contains it). Suppose `iaddrs_one(d_s, σ)(Σ) ≠ ∅`. Then some `a = Σ.M(d_s)(v)` with `v ∈ ⟦σ⟧ ∩ dom(Σ.M(d_s))`, so `a ∈ ran(Σ.M(d_s))` and `a ∈ iaddrs_one(d_s, σ)(Σ) ⊆ iaddrs(Q)(Σ)`; hence `ran(Σ.M(d_s)) ∩ iaddrs(Q)(Σ) ≠ ∅`. With `d_s ∈ Σ.E_doc` by `wp-defined`, the membership predicate holds, so `d_s ∈ find(Q)(Σ)`. We record this as **F-SELF**: `iaddrs_one(d_s, σ)(Σ) ≠ ∅ ⟹ d_s ∈ find(Q)(Σ)` for every `(d_s, σ) ∈ Q`.

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

*Reachability.* Every step in this scenario — the thirteen here and the two added later for `Σ⁺` — is a standard allocate–place–record (and create-document) composite of ASN-0047: entity creation followed by content allocation, placement, and provenance recording. A reachable state extended by such composites remains reachable and continues to satisfy ASN-0047's invariants, so both `Σ` and its later extension `Σ⁺` are reachable.

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

**A multi-address query.** Take `Q_D = {(d_D, σ_D)}` with `σ_D = (w₁, δ(3, 2))` — a width-3 content-subspace span from `w₁ = [s_C, 1]`. Its reach is `w₁ ⊕ δ(3, 2) = [s_C, 4]` (position 1 below the action point is copied; position 2 sums to `1 + 3 = 4`), so

  `⟦σ_D⟧ ∩ dom(M(d_D)) = {[s_C,1], [s_C,2], [s_C,3]} = {w₁, w₂, w₃}`

*Resolution.* The restriction `f = M(d_D)|⟦σ_D⟧` maps `w₁ ↦ a₁`, `w₂ ↦ a₂`, `w₃ ↦ a₁`, so the image collects all three I-addresses and dedupes the repeated `a₁`:

  `iaddrs_one(d_D, σ_D)(Σ) = { M(d_D)(v) : v ∈ {w₁, w₂, w₃} } = {a₁, a₂, a₁} = {a₁, a₂}`

Hence `iaddrs(Q_D)(Σ) = {a₁, a₂}`.

*Find with proper-subset references.* Evaluate the predicate at each document:

  `d = d_A`: `ran(M(d_A)) ∩ {a₁, a₂} = {a₁} ∩ {a₁, a₂} = {a₁} ≠ ∅`, so `d_A ∈ find(Q_D)(Σ)`. `d_A` references only `a₁` — a *proper subset* of the two-address query.
  `d = d_B`: `{a₁} ∩ {a₁, a₂} = {a₁} ≠ ∅`, so `d_B ∈ find(Q_D)(Σ)`. Proper subset again.
  `d = d_C`: `{a₂} ∩ {a₁, a₂} = {a₂} ≠ ∅`, so `d_C ∈ find(Q_D)(Σ)`. `d_C` references only `a₂` — the *other* address of the query, disjoint from `d_A`'s and `d_B`'s share.
  `d = d_D`: `{a₁, a₂} ∩ {a₁, a₂} = {a₁, a₂} ≠ ∅`, so `d_D ∈ find(Q_D)(Σ)`. The whole resolved set.

Therefore `find(Q_D)(Σ) = {d_A, d_B, d_C, d_D}`. Here `d_A` (sharing only `a₁`) and `d_C` (sharing only `a₂`) each qualify on one address out of two, sharing *disjoint* fragments of the query, yet both belong.

**A multi-source query — cross-source deduplication.** Every query so far has been a singleton vspec-set, so `iaddrs`'s defining feature — the union *over several vspecs*, including dedup of an address resolved by more than one source — has not yet been traced. Take `Q_G = {(d_A, σ_A), (d_B, σ_B)}` with `σ_A = (v_A, δ(1, 2))` as before and `σ_B = (v_B, δ(1, 2))`, `v_B = [s_C, 1]`. The two vspecs name *distinct* source documents `d_A ≠ d_B`, yet both resolve the transcluded `a₁`:

  `iaddrs_one(d_A, σ_A)(Σ) = {a₁}`,   `iaddrs_one(d_B, σ_B)(Σ) = {M(d_B)(v_B)} = {a₁}`

The defining union collapses the two contributions to a single address — set union is idempotent on the shared `a₁` regardless of which source produced it:

  `iaddrs(Q_G)(Σ) = {a₁} ∪ {a₁} = {a₁}`

This is cross-source deduplication: two independent per-source resolutions both naming `a₁` yield `a₁` once, not twice.

*Find.* Evaluate `ran(M(d)) ∩ {a₁} ≠ ∅`: it holds at `d_A` (`{a₁}`), `d_B` (`{a₁}`), and `d_D` (`{a₁, a₂}`), and fails at `d_C` (`{a₂}`). Therefore

  `find(Q_G)(Σ) = {d_A, d_B, d_D}`

Each document is reported exactly once (F-DIST). `d_D` references `a₁` at two non-adjacent positions (`w₁`, `w₃`) and is named by neither vspec of `Q_G`, yet appears a single time; `d_A` and `d_B` are each simultaneously a query *source* and a *result*, again listed once. Both layers of deduplication act here: the cross-source union folds the doubly-resolved `a₁`, and the `P(E_doc)` codomain folds the multiply-referencing document.

**A cross-depth query.** We extend the construction with one depth-3 document, reaching a state `Σ⁺` that adds `d_E` to `Σ`:

14. K.δ creates `d_E = inc(d_D, 0) ∈ E_doc` by case (ii) sibling (`k = 0`), operand `d_D ∈ E` with `¬Node(d_D)`. `parent(d_E) = parent(d_D) = acct ∈ E` (K.δ-ID.parent-0) discharges P8; `zeros(d_E) = 2`, so `Document(d_E)` (activates `A_C(d_E)`).
15. K.μ⁺ binds three content-subspace positions of `d_E` at common depth `m_C = 3` — S8a fixes the depth from scratch at first insertion at any value `≥ 2`, here 3 — all by transclusion (no new K.α): `M(d_E)([s_C, 1, 1]) = a₁`, `M(d_E)([s_C, 1, 2]) = a₂`, `M(d_E)([s_C, 1, 3]) = a₁`. By D-SEQ★ at depth 3 the positions are `{[s_C, 1, k] : 1 ≤ k ≤ 3}`, contiguous (D-CTG★) with minimum `[s_C, 1, 1]` (D-MIN★). K.ρ records `(a₁, d_E)` and `(a₂, d_E)`.

By the *Reachability* remark above, `Σ⁺` is reachable. The extended state adds `Σ⁺.M(d_E) = {[s_C,1,1] ↦ a₁, [s_C,1,2] ↦ a₂, [s_C,1,3] ↦ a₁}`, leaving every other arrangement as in `Σ`.

Now submit the *shallow* vspec `Q_E = {(d_E, σ_E)}` with `σ_E = ([s_C, 1], δ(1, 2))`, so `u = [s_C, 1]` has `#u = 2 < m_C = 3` — the cross-depth case.

**Resolution.** The vspec preconditions hold: `subspace(u) = s_C`, `Pos(δ(1, 2))`, `actionPoint(δ(1, 2)) = 2 = #u ≥ 2`, `#δ(1, 2) = 2 = #u`. The reach is `u ⊕ δ(1, 2) = [s_C, 2]` (position 1 below the action point is copied from `u`; position 2 is the action point, summing `1 + 1 = 2`). So `⟦σ_E⟧ = {t : [s_C, 1] ≤ t < [s_C, 2]}`. Each `[s_C, 1, k]` is a proper extension of the prefix `[s_C, 1]`, hence exceeds it by T1 case (ii), and lies below `[s_C, 2]` by T1 case (i) at position 2 (`1 < 2`). Therefore

  `⟦σ_E⟧ ∩ dom(M(d_E)) = {[s_C,1,1], [s_C,1,2], [s_C,1,3]}`

— the *entire* depth-3 subtree hanging under the depth-2 anchor `[s_C, 1]`, captured by a span the user anchored at a single coarse coordinate. These positions *are* current arrangement entries, so F-FILT offers no defense; collecting them is the intended semantics. Resolving:

  `iaddrs(Q_E)(Σ⁺) = { M(d_E)(v) : v ∈ {[s_C,1,1], [s_C,1,2], [s_C,1,3]} } = {a₁, a₂}`

**Find.** Evaluate `ran(M(d)) ∩ {a₁, a₂} ≠ ∅` at each document: `d_A` (`{a₁}`), `d_B` (`{a₁}`), `d_C` (`{a₂}`), `d_D` (`{a₁, a₂}`), and `d_E` (`{a₁, a₂}`) all qualify. So

  `find(Q_E)(Σ⁺) = {d_A, d_B, d_C, d_D, d_E}`

The coarse shallow anchor — naming a single depth-2 coordinate over a depth-3 source — discovered the full transclusion community of the subtree's content. This is the width-1 (`ℓ_{#u} = 1`) instance of PC-RANGE at `u = [s_C, 1]`, with `#u = 2 < m_C = 3`.

**The dual: a deep anchor against a shallow source (F-DEEP).** The cross-depth example above lands the *full* subtree; its dual lands nothing. Submit the *deep* vspec `Q_F = {(d_A, σ_F)}` with `σ_F = ([s_C, 1, 1], δ(1, 3))`, so `u = [s_C, 1, 1]` has `#u = 3 > m_C = 2` — `d_A`'s content-subspace arrangement sits at depth `m_C = 2` (`dom(M(d_A)) = {v_A} = {[s_C, 1]}`). The vspec preconditions hold: `subspace(u) = s_C`, `Pos(δ(1, 3))`, `actionPoint(δ(1, 3)) = 3 = #u ≥ 2`, `#δ(1, 3) = 3 = #u`. The reach is `u ⊕ δ(1, 3) = [s_C, 1, 2]` (positions 1, 2 below the action point are copied from `u`; position 3 sums `1 + 1 = 2`), so `⟦σ_F⟧ = {t : [s_C, 1, 1] ≤ t < [s_C, 1, 2]}`. PC's totality clause requires every `t ∈ ⟦σ_F⟧` to have `#t ≥ #u = 3`; the sole arrangement position `v_A = [s_C, 1]` has depth `2 < 3`, so `v_A ∉ ⟦σ_F⟧`. Therefore

  `⟦σ_F⟧ ∩ dom(M(d_A)) = ∅`,   hence   `iaddrs_one(d_A, σ_F)(Σ) = ∅`

and `iaddrs(Q_F)(Σ) = ∅`, so `find(Q_F)(Σ) = ∅` directly: the intersection `ran(M(d)) ∩ ∅ = ∅` at every `d`, so the membership predicate fails everywhere. A vspec that looks well-formed resolves to nothing: an anchor finer than the source's arrangement names a coordinate below where any content was placed.

## Partial overlap suffices

The predicate uses `≠ ∅`, so a single shared I-address suffices for `d`'s inclusion (F-PART): the result does not require `d` to reference all of `iaddrs(Q)`, nor its reference to be of any particular extent. A document that transcludes a single sentence from a chapter-length query passage qualifies, alongside documents that transclude the whole.

The result set therefore carries no inherent measure of "how much" each returned document contains. To recover an extent measure, the requester must compute `|ran(Σ.M(d)) ∩ iaddrs(Q)(Σ)|` for each returned `d` separately.

## Home versus transcluding documents

Because `origin(a)` is a function of `a`'s tumbler alone, grounded in `E_doc` by ASN-0047 P6, a caller can separate `a`'s home reference (`d = origin(a)`) from transcluding references (`d ≠ origin(a)`) without `find` tagging its results (F-ORIGIN).

## Currency: state dependence

`find(Q)(Σ)` reads only `Σ.E_doc` and `Σ.M`: `iaddrs(Q)(Σ)` is computed purely as images of `Σ.M(d_s)`, and the membership predicate intersects those images against `ran(Σ.M(d))` — neither `dom(Σ.C)`, nor a content value, nor any past state enters.

  `(Σ.E_doc = Σ'.E_doc) ∧ (A d ∈ Σ.E_doc : Σ.M(d) = Σ'.M(d))  ⟹  find(Q)(Σ) = find(Q)(Σ')`

This is what Nelson's "containing" (present participle) commits to. The predicate is evaluated at the moment of query, not over the lifetime of the docuverse. A document whose arrangement once referenced `a` but has since been contracted (via K.μ⁻ from ASN-0047) is not in `find(Q)` even if it once was. The operation reports current containment, full stop. `find` does not consult ASN-0047's provenance relation `R`, which records `(a, d)` permanently (P2); completeness (F-COMP) is therefore over the *currently-containing* set.

## Finiteness

  `|find(Q)(Σ)| < ∞`

The argument is three-step:

(a) The initial state has `|Σ₀.E_doc| = 0`. ASN-0047 gives `E₀ = {n₀}` with `Node(n₀)`, so `n₀ ∉ E_doc` and `(E₀)_doc = ∅`.

(b) Each elementary transition adds at most one entity to `E_doc`. Among ASN-0047's *elementary* transitions, only K.δ modifies `E` (its effect is `E' = E ∪ {e}` for a single `e`); the other elementary transitions (K.α, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ) leave `E` unchanged by their frame clauses. K.δ adds `e` to `E_doc` only when `Document(e)`, otherwise to `E_node` or `E_account`. Either way, `|E_doc|` grows by at most one per transition.

(c) A reachable state is reached by finitely many *elementary* transitions. ASN-0047's ExtendedReachableStateInvariants characterises every reachable state as "reachable from `Σ₀` by a finite sequence of valid composite transitions". Each composite is itself, by ValidCompositeAmended, a finite sequence of atomic transitions; a finite concatenation of finite sequences is finite, so the total count `n_elem` of elementary transitions producing any reachable `Σ` is a finite natural number.

Combining: step (b) bounds the per-elementary-transition growth of `|E_doc|` by one, and step (c) bounds the number of elementary transitions by `n_elem`, so `|Σ.E_doc| ≤ n_elem < ∞` at any reachable `Σ`. (The bound is stated against the elementary count, not the composite count — a single composite may fire several K.δ steps, e.g. node → account → document creation, so `|E_doc|` can exceed the number of composites.) Since `find(Q)(Σ) ⊆ Σ.E_doc`, finiteness follows.

This is worth stating because `iaddrs(Q)` may name content that is widely transcluded — a single popular passage could appear in many documents. The result is bounded only by `E_doc` itself.

## What we do not specify

The returned set has a presentation property we leave unspecified. It is not entailed by the abstract operation, and an implementation may add it without conflicting with the specification.

*Order.* `find(Q)(Σ)` is a set. Some implementations may return its elements in a deterministic order (such as ascending tumbler order on document ISA, naturally arising from a sorted index); others may not. Order is a presentation choice, not a conformance criterion — it is left entirely unspecified.

## Claims Introduced

| Label | Statement | Basis | Status |
|-------|-----------|-------|--------|
| F-iaddrs | `iaddrs : VSpecSet × Σ ⇀ P(T)` with `iaddrs(Q)(Σ) = ⋃_{(d_s, σ) ∈ Q} { Σ.M(d_s)(v) : v ∈ ⟦σ⟧ ∩ dom(Σ.M(d_s)) }`, defined under `wp-defined: (A (d_s, σ) ∈ Q :: d_s ∈ Σ.E_doc)`; subset claim `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` whenever `wp-defined` holds | definition; subset claim proven in *Resolution* (subspace confinement of `⟦σ⟧` + S3★), gated on `wp-defined` | introduced |
| F-find | `find : VSpecSet × Σ ⇀ P(E_doc)` with `find(Q)(Σ) = { d ∈ Σ.E_doc : ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅ }`, defined under the precondition `(A (d_s, σ) ∈ Q :: d_s ∈ Σ.E_doc)` | definition; precondition couples each vspec source to the evaluation state (M1, P1 of ASN-0047) | introduced |
| PC | Prefix confinement: for a vspec `(d_s, σ)` with `σ = (u, ℓ)` and `actionPoint(ℓ) = #u`, every `t ∈ ⟦σ⟧` satisfies `t_j = u_j` for `1 ≤ j < #u` | derived locally from TumblerAdd prefix-copy + T1 case (i) + NAT-order trichotomy (T0) for the per-position case split + well-ordering of positions for the universal closure | introduced |
| PC-RANGE | Cross-depth capture: for a vspec `(d_s, σ)` with `σ = (u, ℓ)`, `actionPoint(ℓ) = #u`, reach `r = u ⊕ ℓ`, `⟦σ⟧ ∩ dom(M(d_s)) = { v ∈ dom(M(d_s)) : #v ≥ #u ∧ (A j : 1 ≤ j < #u : v_j = u_j) ∧ u_{#u} ≤ v_{#u} < r_{#u} }` — the union of the `ℓ_{#u}` sibling subtrees under prefix-component range `[u_{#u}, u_{#u} + ℓ_{#u})`; the single-subtree case is the width-1 specialisation `ℓ_{#u} = 1` | PC + T1 case (i)/(ii) at position `#u` for `#v ≥ #u`; PC totality for the depth guard, excluding `#v < #u` from both sides | introduced |
| F-DEEP | Deep-anchor empty resolution: for a vspec `(d_s, σ)` with `σ = (u, ℓ)`, `V_{s_C}(d_s) ≠ ∅ ∧ #u > m_C` (the source's content-subspace depth, S8-depth) `⟹ iaddrs_one(d_s, σ)(Σ) = ∅`; the companion empty-source case `V_{s_C}(d_s) = ∅ ⟹ iaddrs_one(d_s, σ)(Σ) = ∅` holds trivially | PC-RANGE depth guard + S8-depth (`#v = m_C < #u` for every content-subspace `v ∈ dom(M(d_s))`) excludes every position via the `#v < #u` case; empty case from content-subspace confinement of `⟦σ⟧` | introduced |
| F-COMP | Completeness: every `d ∈ Σ.E_doc` with `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅` is in `find(Q)(Σ)` | direct from F-find (⟸ direction of the defining iff) | introduced |
| F-SOUND | Soundness: every `d ∈ find(Q)(Σ)` is in `Σ.E_doc` with `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅` | direct from F-find (⟹ direction of the defining iff) | introduced |
| F-PART | Partial overlap suffices: `d ∈ find(Q)(Σ) ⟺ d ∈ Σ.E_doc ∧ (E a : a ∈ ran(Σ.M(d)) : a ∈ iaddrs(Q)(Σ))` | direct from F-find (unfolding `≠ ∅` of a binary intersection) | introduced |
| F-DIST | `find(Q)(Σ)` is a set; each `d ∈ E_doc` appears at most once | direct from F-find (codomain is `P(E_doc)`) | introduced |
| F-ORIGIN | Home/transcluding recovery: for `a ∈ iaddrs(Q)(Σ)`, a caller separates `a`'s home reference (`d = origin(a)`) from transcluding references (`d ≠ origin(a)`) using `origin(a)`, without `find` tagging its results | derived from P6 (`origin(a)` grounded in `E_doc`) | introduced |
| F-CONTENT | Matches occur only via shared content addresses: `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ⊆ dom(Σ.C)` | derived from S3★ ∧ S3★-aux (ASN-0047) ∧ L14 ∧ the `iaddrs ⊆ dom(C)` subset claim | introduced |
| F-SELF | Source self-inclusion: `iaddrs_one(d_s, σ)(Σ) ≠ ∅ ⟹ d_s ∈ find(Q)(Σ)` for every `(d_s, σ) ∈ Q` | derived from F-find + F-iaddrs + `wp-defined` (a resolved address lies in both `ran(Σ.M(d_s))` and `iaddrs(Q)(Σ)`) | introduced |
| F-CUR | State dependence: `(Σ.E_doc = Σ'.E_doc) ∧ (A d ∈ Σ.E_doc : Σ.M(d) = Σ'.M(d)) ⟹ find(Q)(Σ) = find(Q)(Σ')` | derived from F-find + F-iaddrs (the operation reads only `E_doc` and `M`, both of which are identical at Σ and Σ' by hypothesis) | introduced |
| F-FILT | Silent resolution filtering: positions in `⟦σ⟧ \ dom(Σ.M(d_s))` contribute no I-addresses to `iaddrs(Q)(Σ)` | direct from F-iaddrs (the intersection `⟦σ⟧ ∩ dom(Σ.M(d_s))` excludes such positions) | introduced |
| F-EMPTY | `find(∅)(Σ) = ∅` | direct from F-find (union over empty index set is empty; intersection with ∅ is empty) | introduced |
| F-FIN | `|find(Q)(Σ)| < ∞` at every reachable state | derived from F-find + ASN-0047 (`Σ₀.E_doc = ∅`; K.δ adds ≤ 1; reachable states have finite transition count) | introduced |

## Open Questions

What relationship between FINDDOCSCONTAINING's current-state result and the historical containment relation `R` must the system guarantee?

Under what conditions must the system reject unresolvable vspec positions rather than silently filter them?

What invariant must connect FINDDOCSCONTAINING's result immediately before and after a transition that contracts an arrangement?
