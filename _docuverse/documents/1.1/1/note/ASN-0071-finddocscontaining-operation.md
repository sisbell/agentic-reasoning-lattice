# ASN-0071: FINDDOCSCONTAINING Operation
*2026-05-25*

A reader of a document can ask: *what is in this document?* The answer comes from walking the document's arrangement and resolving each V-position to the content at its I-address — the read-direction.

The same reader can ask the inverse: *what documents contain this content?* This is the search-direction. A scholar tracing a quotation, a system computing royalty for transcluded reuse, a writer enumerating who has cited a passage — each needs to enumerate documents whose arrangements reference some specified material.

We specify what such an operation must do. Following Nelson we call it **FINDDOCSCONTAINING**. The question this ASN answers is: what is its result set? What determines membership, what guarantees govern completeness, and what does the operation deliberately not promise about currency in a permanent address space?

We work within the strand model as extended by ASN-0047. State `Σ` carries the content store `Σ.C : T ⇀ Val`, the link store `Σ.L`, document entities `Σ.E_doc ⊆ Σ.E`, and arrangements `Σ.M(d) : T ⇀ T` for each `d ∈ Σ.E_doc` — partial functions from V-positions to I-addresses satisfying functionality (S2), generalized referential integrity (S3★), and content permanence (P0, which subsumes S0 and S1). Sharing is unrestricted: distinct `(d, v)` pairs may map to the same I-address (ASN-0058 M13, SharedContent), and such co-occurrences are permanently independent arrangement entries (ASN-0058 M14, IndependentOccurrences). The extended state admits two V-subspaces — content (`s_C`) and link (`s_L`) — and S3★ routes each V-position to its appropriate store: `M(d)(v) ∈ dom(C)` when `subspace(v) = s_C`, and `M(d)(v) ∈ dom(L)` when `subspace(v) = s_L`. We assume content has been allocated and arranged through the standard transitions of ASN-0047; we specify only the query, not the operations that produce its inputs.

## The query

Content can be named in two registers. By I-address — "the content at addresses `A`" — purely structural. By V-position with source — "the content of document `d` at positions `σ`" — referenced from where the user encountered it.

We accept the latter. A **vspec** is a pair `(d_s, σ)` where `d_s ∈ Σ.E_doc` names a source document and `σ = (u, ℓ)` is a level-uniform V-span confined to the content subspace — `subspace(u) = s_C`, `Pos(ℓ)`, `actionPoint(ℓ) ≤ #u`, `#ℓ = #u` (in the sense of ASN-0053), and `actionPoint(ℓ) ≥ 2` (equivalently `ℓ₁ = 0`: the displacement does not perturb the subspace identifier at position 1). A **vspec-set** is a finite set `Q = {q₁, q₂, ..., q_k}` of vspecs, possibly drawn from multiple source documents.

The restriction `subspace(u) = s_C` is load-bearing. FINDDOCSCONTAINING tracks transclusion of byte content — Nelson's "regardless of where the native copies are located" — and only the content subspace participates in transclusion. Link addresses have unique home documents recoverable directly from the tumbler via `origin` (ASN-0047 L1a, LinkScopedAllocation: `origin(a) ∈ E_doc` for every link address), so a query naming a link-subspace span would degenerate to "the link's home document," derivable without the operation. We exclude such queries by construction.

The companion restriction `actionPoint(ℓ) ≥ 2` enforces *subspace confinement* of the entire span. Without it, the vspec preconditions admit displacements that perturb position 1 — for example, `u = [1, 5]` with `ℓ = [2, 0]` satisfies `Pos(ℓ)`, `actionPoint(ℓ) = 1 ≤ #u`, and `#ℓ = #u`, so the span `⟦σ⟧` extends to `[3, 0)` and contains `[2, 1]` whose subspace identifier is `2 = s_L`. Such a span would straddle the content and link subspaces in `d_s`'s V-space, conflating two transclusion regimes that the operation deliberately separates. Requiring `actionPoint(ℓ) ≥ 2` places `ℓ`'s first nonzero component at position 2 or beyond, so by TumblerAdd's prefix-copy region position 1 of every `t ∈ ⟦σ⟧` equals `u₁ = s_C` — the entire span lives in the content subspace. We rely on this property in the codomain argument below.

A vspec is structurally a relaxation of ASN-0058's `ContentReference`. ContentReference additionally requires well-formedness — every depth-`m` position in `⟦σ⟧` belongs to `dom(M(d_s))` — together with `V_{u₁}(d_s) ≠ ∅` and `#u = m` (the common depth of `d_s`'s text-subspace V-positions per S8-depth). The vspec drops all three: it admits spans whose positions may not all be currently arranged, whose source subspace may be empty in `d_s`, and whose depth may differ from `d_s`'s common depth. The relaxation makes the query total over well-typed inputs; resolution silently filters anything that does not match a current arrangement entry (justified below). What the vspec retains from ContentReference is subspace confinement — well-formedness implies `actionPoint(ℓ) = m ≥ 2` via C0, and we lift this consequence into an explicit precondition since the well-formedness that C0 derived it from is no longer available.

Why vspecs and not direct I-addresses? Because users name content from where they encounter it. The reader sees document `d` at position `v`; what they want to find is content equivalent to "what `d` puts at `v`". The I-address is structural, typically unknown to the user, and reachable only by consulting `M(d_s)`. The operation accepts the user's name; resolution to I-addresses is its first task.

## Resolution

For a single vspec `(d_s, σ)`, the resolved I-addresses are those that `d_s`'s current arrangement assigns to positions within the span:

  `iaddrs_one(d_s, σ)(Σ) := { Σ.M(d_s)(v) : v ∈ ⟦σ⟧ ∩ dom(Σ.M(d_s)) }`

For a vspec-set `Q`:

  `iaddrs(Q)(Σ) := ⋃_{(d_s, σ) ∈ Q} iaddrs_one(d_s, σ)(Σ)`

Every element of `iaddrs(Q)(Σ)` lies in `dom(Σ.C)` — the subset claim `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` holds for every `Q` and every `Σ`. The argument is that every position consulted by `iaddrs_one` is in the content subspace, so S3★ routes the image into `dom(Σ.C)` rather than `dom(Σ.L)`. We show subspace confinement first, then apply S3★.

*Subspace confinement.* Fix `t ∈ ⟦σ⟧`. By the half-open interval definition, `u ≤ t < u ⊕ ℓ`. We argue `t₁ = u₁`. Position 1 lies strictly below the action point: by the vspec precondition `actionPoint(ℓ) ≥ 2`, we have `1 < actionPoint(ℓ)`. By TumblerAdd, the result of `u ⊕ ℓ` at any position `i < actionPoint(ℓ)` is copied from `u`: `(u ⊕ ℓ)₁ = u₁`. Now `u` and `u ⊕ ℓ` agree at position 1, so any `t` lying in the lexicographic interval between them must also agree at position 1 — were `t₁ < u₁`, then `t < u` by T1 case (i) at position 1, contradicting `u ≤ t`; were `t₁ > u₁ = (u ⊕ ℓ)₁`, then `t > u ⊕ ℓ` by T1 case (i) at position 1, contradicting `t < u ⊕ ℓ`. So `t₁ = u₁ = s_C` by NAT-order trichotomy on ℕ applied to the components `t₁, u₁ ∈ ℕ` (T0), hence `subspace(t) = s_C`.

*Routing.* Therefore every `v ∈ ⟦σ⟧ ∩ dom(Σ.M(d_s))` is a content-subspace V-position, and S3★ (ASN-0047) routes it: `Σ.M(d_s)(v) ∈ dom(Σ.C)`. The subset claim `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` is read with `Σ` explicit on both sides — the right-hand side is the input state's content store, not a fixed set. Without the `actionPoint(ℓ) ≥ 2` precondition, position 1 could fall *at* or *beyond* the action point, where TumblerAdd's prefix-copy reasoning does not apply — and the counter-example `u = [1, 5]`, `ℓ = [2, 0]` exhibited above would silently include a link-subspace V-position in the resolution if `d_s` arranges one.

When a vspec `(d_s, σ)` is also a well-formed ContentReference, `iaddrs_one(d_s, σ)(Σ)` equals the set-flattening of ASN-0058's `resolve(d_s, σ)` — concretely, `{ a + k : (a, n) ∈ resolve(d_s, σ) ∧ 0 ≤ k < n }`. We derive the equality in one step. By C1a, `resolve(d_s, σ)` is read off the unique maximally merged block decomposition `⟨β₁, ..., β_K⟩` of the restriction `f = M(d_s)|⟦σ⟧`, with `β_j = (v_j, a_j, n_j)` and `resolve(d_s, σ) = ⟨(a₁, n₁), ..., (a_K, n_K)⟩`. The decomposition covers `dom(f)` exactly (B1, Coverage): `dom(f) = ⟦σ⟧ ∩ dom(M(d_s))` — precisely the index set of `iaddrs_one`. For each block, B3 (Consistency) gives `a_j + k = M(d_s)(v_j + k)` for `0 ≤ k < n_j`, and the `v_j + k` range over `V(β_j)`; by coverage the union of all `V(β_j)` is `dom(f)`. So
> `{ a_j + k : 1 ≤ j ≤ K ∧ 0 ≤ k < n_j } = { M(d_s)(v) : v ∈ dom(f) } = iaddrs_one(d_s, σ)(Σ)`.

The left side is the set-flattening of `resolve`. Set-flattening absorbs duplicate I-addresses: two distinct blocks may carry shared content (ASN-0058 M14), and the same `a` then appears in both — the set union dedupes it, matching `iaddrs_one`'s set codomain. The relaxation matters only when `⟦σ⟧` contains positions outside `dom(M(d_s))`: ContentReference treats such a span as ill-formed, while vspec silently drops the missing positions.

A vspec may name positions not currently in `dom(Σ.M(d_s))`. The definition handles this silently: the intersection `⟦σ⟧ ∩ dom(Σ.M(d_s))` drops unresolvable positions, and their absence contributes nothing to `iaddrs`. The query reads charitably — as "find documents containing the content at whatever positions of `σ` are currently bound" — rather than insisting on total resolvability.

This is a substantive choice. An alternative specification could reject the entire query as ill-formed if any position is unresolvable. The charitable reading is justified: a position not in the arrangement names no content, so excluding it from the resolution is the natural extension of "find documents containing the content at these positions". The price is reduced diagnostic information — the user cannot distinguish "no documents contain this" from "this query resolved to no I-addresses".

We note a structural property: `iaddrs_one(d_s, σ)(Σ)` depends only on `Σ.M(d_s)`. Each vspec is *source-anchored* — its meaning is fully determined by the pair `(d_s, σ)` given the state. No global context or caller's view is consulted. The resolution of `Q` is the union of independent per-source resolutions; sources can be consulted independently in any order, by any node holding the relevant arrangement.

## The operation

Given resolved I-addresses, FINDDOCSCONTAINING returns the documents whose arrangements currently reference any of them:

  `find(Q)(Σ) := { d ∈ Σ.E_doc : ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅ }`

The definition is brief. Everything FINDDOCSCONTAINING claims is contained in the predicate `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅`. The remainder of this ASN unpacks what that predicate guarantees.

*Only content sharing can satisfy the predicate.* The range `ran(Σ.M(d))` carries both content-subspace and link-subspace images: by S3★, a content-subspace V-position routes into `dom(Σ.C)` and a link-subspace V-position into `dom(Σ.L)` (and by CL-OWN, ASN-0047, the latter are exactly `d`'s own links). The link-subspace portion can never contribute a match. We discharged the source side already — `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` by subspace confinement — and the target side is its dual: the link-subspace images lie in `dom(Σ.L)`, which is disjoint from `dom(Σ.C)` (ASN-0047 L14, StoreDisjointness: `dom(C) ∩ dom(L) = ∅`). Therefore `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ⊆ dom(Σ.L) ∩ dom(Σ.C) ∪ dom(Σ.C) = dom(Σ.C)` — more precisely, any `a` in the intersection lies in `iaddrs(Q)(Σ) ⊆ dom(Σ.C)`, so it cannot be a link image of `d`, and the witness `a ∈ ran(Σ.M(d))` must come from a content-subspace V-position. A document is returned because it shares *byte content*, never because it shares a *link* address. This is what justifies calling the operation content-transclusion discovery.

The empty query is the boundary case. When `Q = ∅`, the union `iaddrs(∅)(Σ) = ⋃_{(d_s, σ) ∈ ∅} ...` is the empty set, so for every `d ∈ Σ.E_doc` the intersection `ran(Σ.M(d)) ∩ ∅ = ∅` is empty. Therefore `find(∅)(Σ) = ∅`. The operation is total on the empty input — no special case is needed in the definition.

## A worked scenario

We exhibit a minimal state in which two documents share a single content I-address through transclusion, and trace what FINDDOCSCONTAINING returns.

Start from `Σ₀` and apply the following transitions of ASN-0047 (each precondition is discharged by the prior state; we narrate the result):

1. K.δ creates document `d_A ∈ E_doc` (a fresh document address; activates `A_C(d_A)` and `A_L(d_A)`).
2. K.α emits one content I-address `a₁` under `d_A`: `a₁ = [d_A.0.s_C.1]`, `Σ.C(a₁) = val_A` for some value `val_A ∈ Val`, `origin(a₁) = d_A`.
3. K.μ⁺ binds `M(d_A)(v_A) = a₁`, where `v_A = [s_C, 1]` is the minimum content-subspace V-position of `d_A` (D-MIN★, depth `m_C = 2`).
4. K.ρ records provenance: `(a₁, d_A) ∈ R`.
5. K.δ creates document `d_B ∈ E_doc`.
6. K.μ⁺ binds `M(d_B)(v_B) = a₁`, where `v_B = [s_C, 1]` is the minimum content-subspace V-position of `d_B`. This is transclusion: the I-address `a₁` allocated under `d_A` is now also referenced from `d_B`'s arrangement, *without* a new K.α emission. The bind is licensed by S3★ since `a₁ ∈ dom(C)`.
7. K.ρ records provenance: `(a₁, d_B) ∈ R`. The composite (steps 5–7) discharges J1★ (ASN-0047): the content-subspace range of `M(d_B)` gains a new entry `a₁`, which forces `(a₁, d_B) ∈ R'`. The converse coupling J1'★ holds symmetrically — the new provenance entry corresponds to a range-new I-address.
8. K.δ creates a third document `d_C ∈ E_doc` (a fresh document address; activates `A_C(d_C)`).
9. K.α emits one content I-address `a₂` under `d_C`: `a₂ = [d_C.0.s_C.1]`, `Σ.C(a₂) = val_C` for some value `val_C ∈ Val`, `origin(a₂) = d_C`. Since `a₂` is allocated under `d_C`'s own sub-allocator while `a₁` is allocated under `d_A`'s, the two are distinct I-addresses: `a₂ ≠ a₁` (their tumbler prefixes differ at the document field).
10. K.μ⁺ binds `M(d_C)(v_C) = a₂`, where `v_C = [s_C, 1]` is the minimum content-subspace V-position of `d_C`. K.ρ records `(a₂, d_C) ∈ R`. Document `d_C` references only its own native content `a₂`; it does not transclude `a₁`.

The resulting state `Σ` has:

  `Σ.E_doc ⊇ {d_A, d_B, d_C}`,   `Σ.C ⊇ {a₁ ↦ val_A, a₂ ↦ val_C}`,   `Σ.M(d_A) = {v_A ↦ a₁}`,   `Σ.M(d_B) = {v_B ↦ a₁}`,   `Σ.M(d_C) = {v_C ↦ a₂}`,   `origin(a₁) = d_A`,   `origin(a₂) = d_C`

Construct the query `Q = {(d_A, σ_A)}` with `σ_A = (v_A, δ(1, 2))` — a single-position level-uniform span starting at `v_A` with width 1 in the content subspace.

**Resolution.** The vspec preconditions hold: `subspace(v_A) = s_C`, `Pos(δ(1, 2))`, `actionPoint(δ(1, 2)) = 2 ≥ 2`, `actionPoint(δ(1, 2)) = 2 ≤ #v_A = 2`, `#δ(1, 2) = 2 = #v_A`. Computing the reach: `v_A ⊕ δ(1, 2) = [s_C, 2]` by TumblerAdd (position 1 lies below the action point and is copied from `v_A`; position 2 is the action point itself and sums to `1 + 1 = 2`). So the span denotes the half-open interval

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
  All other `d ∈ E_doc`: `a₁ ∉ ran(M(d))` (those documents reference no I-addresses), so `d ∉ find(Q)(Σ)`.

Therefore `find(Q)(Σ) = {d_A, d_B}` — `d_C` excluded.

**What this verifies.**

- *F-SHARE.* Both `d_A` and `d_B` are discovered by the same query, demonstrating cross-document discovery through shared I-address. The query named `(d_A, σ_A)` — `d_B` was not mentioned — yet `d_B` appears in the result because its arrangement references the resolved I-address.
- *F-DIST.* Each document appears exactly once in `find(Q)(Σ) = {d_A, d_B}`, despite both satisfying the predicate. The result is a set; `d_A` is not duplicated even though it is both the source-document of `Q` and a member of the result.
- *F-PART.* A single shared I-address (`a₁`) is sufficient for inclusion. The result does not require a document to reference any particular portion of the queried span.
- *F-SOUND (exclusion).* `d_C` references content (`a₂`) but shares no I-address with `iaddrs(Q)(Σ) = {a₁}`, so the membership predicate evaluates to *false* and `d_C ∉ find(Q)(Σ)`. The biconditional is exercised in its harder, negative direction against a concrete non-containing document — membership is not merely an absence of mention but a tested empty intersection.
- *F-FILT.* The span `⟦σ_A⟧` is an infinite subset of `T`, but the intersection with `dom(M(d_A)) = {v_A}` reduces it to a single position. The operation does not reject `σ_A` for naming positions outside `d_A`'s arrangement — unresolvable positions contribute nothing and the query reads charitably over what is currently bound.
- *F-CUR.* The result depends only on `Σ.M(d_A)` and `Σ.M(d_B)`. Were a later K.μ⁻ to contract `M(d_B)` to remove `v_B`, the query would return `{d_A}` only — `d_B` would no longer be currently containing, even though `(a₁, d_B) ∈ R` would persist (P2).
- *Home/transcluding recovery.* `origin(a₁) = d_A`, the home document of the content I-address `a₁` (grounded in `E_doc` by ASN-0047 P6, ExistentialCoherence), so the requester can distinguish: `d_A` is the home document of `a₁`, and `d_B` transcludes it. The operation itself does not tag the result; the tagging is a function the requester computes from each `a ∈ iaddrs(Q)` and each `d ∈ find(Q)`.

## Completeness and soundness

The membership criterion is a biconditional — the definition of `find(Q)(Σ)`:

  `d ∈ find(Q)(Σ)  ⟺  d ∈ Σ.E_doc ∧ ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅`

The biconditional decomposes into two directions:

  (⟸) **F-COMP** (completeness): every `d` satisfying the predicate is in `find(Q)(Σ)`.
  (⟹) **F-SOUND** (soundness): every `d ∈ find(Q)(Σ)` satisfies the predicate.

F-COMP and F-SOUND are not independent properties of the abstract operation — they are the two halves of its definition. Together they constitute the definition; separately, they name the obligations on any candidate implementation. An implementation that omits any qualifying document realizes a strict subset of `find` (the `⟸` direction of the definition is violated). An implementation that includes a document not satisfying the predicate realizes a strict superset (the `⟹` direction is violated). Conformance to FINDDOCSCONTAINING means: the returned set coincides with the set characterized by the predicate.

A specific failure mode is worth flagging. An implementation that maintains an auxiliary index — "documents containing I-address `a`" — in an append-only fashion, never removing entries when arrangements are contracted, returns a *superset*. Every truly containing document is included (F-COMP preserved) but some included documents may no longer contain (F-SOUND violated). Such an implementation realizes `find` as a superset oracle:

  `actual_find(Q)(Σ) ⊆ implementation(Q)(Σ)`

The deviation is observable from the abstract specification — a returned `d` for which `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) = ∅` is an F-SOUND failure. We do not adjudicate whether such relaxation is acceptable in practice; we only note that the abstract specification demands exact correspondence, and any deviation must be flagged as a relaxation against the specification rather than treated as conforming.

## Partial overlap suffices

The predicate uses `≠ ∅`. A single shared I-address — one `a ∈ ran(Σ.M(d)) ∩ iaddrs(Q)(Σ)` — is sufficient for `d`'s inclusion:

  `d ∈ find(Q)(Σ)  ⟺  d ∈ Σ.E_doc ∧ (E a : a ∈ ran(Σ.M(d)) : a ∈ iaddrs(Q)(Σ))`

The result does not require `d` to reference all of `iaddrs(Q)`; it does not require `d`'s reference to be of any particular extent. A document that transcludes a single sentence from a chapter-length query passage qualifies, alongside documents that transclude the whole.

This is the operative reading of Nelson's "any portion": completeness is over the existence of non-empty intersection, not over inclusion of the whole. The asymmetry matters — a query about a large passage may discover documents that each reference only a tiny fragment of it. The result set has no inherent measure of "how much" each returned document contains; to recover an extent measure, the requester must compute `|ran(Σ.M(d)) ∩ iaddrs(Q)(Σ)|` for each returned `d` separately.

## Set semantics

`find(Q)(Σ)` is a set. Each document appears at most once regardless of how many I-addresses it shares with `iaddrs(Q)`:

  for every `d_* ∈ Σ.E_doc`:   `|{ x ∈ find(Q)(Σ) : x = d_* }| ≤ 1`

A document that transcludes ten distinct passages from a queried chapter is reported once, not ten times. The result enumerates documents, not occurrences. To recover occurrence counts, the requester must separately compute the cardinality of `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ)` for each returned `d`.

Set semantics must be stated explicitly because the natural implementation — iterating over each queried I-address and collecting source documents — produces duplicates by default. The specification requires deduplication; an implementation that returns a multiset of `(d, a)` pairs satisfies neither the type signature nor the intent.

## Discovery through sharing

The most architecturally significant consequence concerns transclusion. If I-address `a` is referenced by multiple documents — `a ∈ ran(Σ.M(d))` for several `d` — then a query that resolves to `a` discovers all of them:

  `a ∈ iaddrs(Q)(Σ) ∧ a ∈ ran(Σ.M(d)) ∧ d ∈ Σ.E_doc  ⟹  d ∈ find(Q)(Σ)`

In particular: `a`'s home document (`origin(a)`, grounded in `E_doc` by ASN-0047 P6 — if it itself still references `a`) and every transcluding document are discovered by the same query and reported as equally-qualifying members of the result.

The find operation does not distinguish home from transcluding document. Both reference `a`; both satisfy the predicate. The mechanism is structural — the I-address `a` is the same `a` everywhere it appears, because content has permanent identity (P0). Sharing of content corresponds to identity of I-address; identity of I-address is what `find` tests for.

This makes `find` the structural dual of the read-direction. Reading goes from arrangement to content: given `d`, `M(d)` tells which I-addresses `d` references. Finding goes from content to arrangement: given resolved I-addresses, `find` tells which documents reference them. The two operations are duals over the same `M : E_doc → (T ⇀ T)` structure.

The result does not, on its own, distinguish *how* each reported document references the content — native authorship versus transclusion. This distinction is recoverable from the address structure already returned. For each `a ∈ iaddrs(Q)`, `origin(a)` (a function of `a`'s tumbler alone, grounded in `E_doc` by ASN-0047 P6) names `a`'s home document. Comparing `origin(a)` against each `d ∈ find(Q)` recovers the relationship: `d = origin(a)` means `d` authored `a`; `d ≠ origin(a)` means `d` transcludes `a`. The `find` operation does not need to tag its results because tagging is a function the requester can compute from the data.

## Currency: state dependence

`find(Q)(Σ)` is a function of `Σ`. It depends only on the current state — specifically on `Σ.E_doc` and `Σ.M`. (It reads neither `dom(Σ.C)` nor any content value: `iaddrs(Q)(Σ)` is computed purely as images of `Σ.M(d_s)`, and the membership predicate intersects those images against `ran(Σ.M(d))`. S3★ supplies the standing context that `ran(Σ.M(d)) ⊆ dom(Σ.C) ∪ dom(Σ.L)`, but `find` does not consult the content store to evaluate it.)

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

The completeness guarantee of `find` is over *currency*. The completeness guarantee of `R` is over *history*. An operation must commit to one semantic. FINDDOCSCONTAINING, as Nelson specifies it and as we have specified it here, commits to currency.

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
| F-iaddrs | `iaddrs : VSpecSet × Σ → P(T)` with `iaddrs(Q)(Σ) = ⋃_{(d_s, σ) ∈ Q} { Σ.M(d_s)(v) : v ∈ ⟦σ⟧ ∩ dom(Σ.M(d_s)) }`; subset claim `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` for every `Q` and `Σ` (both sides state-dependent at `Σ`) | definition; subset claim derived from vspec preconditions `subspace(u) = s_C` and `actionPoint(ℓ) ≥ 2` (subspace confinement of `⟦σ⟧` via TumblerAdd prefix-copy + T1) + S3★ | introduced |
| F-find | `find : VSpecSet × Σ → P(E_doc)` with `find(Q)(Σ) = { d ∈ Σ.E_doc : ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅ }` | definition | introduced |
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
