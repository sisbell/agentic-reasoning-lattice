# ASN-0116 Claim Statements

*Source: ASN-0116-insert-operation.md (revised 2026-06-08) — Extracted: 2026-06-09*

## Definition — SubspacePositions

`V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}` — the V-positions of `d` in subspace `S`.

## Definition — CanonicalPosition

`q_k = [S, 1, …, 1, k]` of depth `m`, where `m` is pinned by the insertion precondition. The `k`-th position of the dense run `{q_1, …, q_N}` in the text subspace.

Arithmetic fact: `shift(q_k, n) = q_{k+n}` — advancing the last component by `n` carries the `k`-th slot to the `(k+n)`-th, leaving the shared prefix `[S, 1, …, 1]` untouched (by OrdinalShift, since `actionPoint(δ(n, m)) = m = #q_k`).

## Definition — AllocatedRun

`A_new = {shift(a, k) : 0 ≤ k < n}` — the `n` freshly allocated I-addresses, where `a` is the K.α-fresh origin-`d` content I-start, contiguous on `d`'s content chain `A_C(d)`, with `A_new ∩ dom(C) = ∅`.

Each successive address advances by `inc(·, 0) = shift(·, 1)`. The start `a = inc(a_prev, 0)` where `a_prev = max{a' ∈ dom(C) : origin(a') = d}` (subsequent-emission branch), or `a = [d.0.s_C.1]` (first-emission branch when `{a' ∈ dom(C) : origin(a') = d} = ∅`).

## Definition — DiscoverableLinks

`D(d, Σ) = {a ∈ dom(Σ.L) : discoverable_from(a, d, Σ)}` — the links discoverable from `d` at state `Σ`. By LP12 (DiscoverabilityCharacterisation, ASN-0098): `discoverable_from(a, d, Σ) ⟺ (E i : coverage(Σ.L(a).eᵢ) ∩ ran(M(d)) ≠ ∅)`.

## Definition — ResolvedWitnessSet

`project(e, d, Σ) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}` — the set of V-positions of `d` whose arrangement image falls in the coverage of endset `e`.

---

## INSERT — Insert (OP, composite)

**INSERT(`d`, `p`, `w₀ … w_{n-1}`).**

*Precondition.* `d ∈ dom(M) = E_doc`; `Σ` is reachable from `Σ₀` by a valid transition trace; `n ≥ 1`; `(A k : 0 ≤ k < n : w_k ∈ Val)`; `S = subspace(p) = s_C`; `m := #p ≥ 2`, and when `V_S(d) ≠ ∅` this `m` equals the common depth that S8-depth fixes on `V_S(d)`; `p` is S8a-well-formed; and `p` is a valid insertion position in the foundation sense (ASN-0036). The position predicates are:
- if `V_S(d) = ∅`: `ValidFirstInsertionPosition(d, p, m)` — `p` is the canonical first position `[S, 1, …, 1]` of depth `m`, and this first insertion *fixes* the subspace depth at `m` for every later insertion;
- if `V_S(d) ≠ ∅`: `ValidInsertionPosition(d, p)` — `p = q_J` for some `1 ≤ J ≤ N+1`, with `J = N+1` the *append* case `p = shift(max(V_S(d)), 1)`.

Allocation supplies `a` as the K.α-fresh origin-`d` content I-start, with `A_new ∩ dom(C) = ∅`.

*Effect.* INSERT is the composite of `n` content allocations (K.α, ASN-0093), an arrangement contraction–extension pair `K.μ⁻` then `K.μ⁺` (degenerating to a single `K.μ⁺` when no suffix moves) whose net effect realises the post-insertion shift of ASN-0082's I3 family, and `n` provenance recordings (K.ρ, ASN-0047) that couple each allocated address to `d`.

*Suffix-present case `1 ≤ J ≤ N`*: `K.α₁, …, K.αₙ` → `K.μ⁻` → `K.μ⁺` → `K.ρ₁, …, K.ρₙ`.

*Append case `J = N+1` and empty case `V_S(d) = ∅`*: `K.α₁, …, K.αₙ` → `K.μ⁺` → `K.ρ₁, …, K.ρₙ`.

---

## I-ALLOC — IAlloc (EFFECT, clause)

`dom(C') = dom(C) ∪ A_new`, with `C'(shift(a, k)) = w_k` for `0 ≤ k < n` — the K.α effect (ASN-0093), iterated `n` times along `A_C(d)`.

## I-IMM — IImm (EFFECT, clause)

`(A b : b ∈ dom(C) : C'(b) = C(b))` — K.α append-only (C0, ASN-0093).

## I-SHIFT — IShift (EFFECT, clause)

`(A v : v ∈ V_S(d) ∧ v ≥ p : shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v))` — ASN-0082 **I3 (PostInsertionShift)** fixes these values on the shifted-suffix region `{J+n, …, N+n}` of `M'₀(d)`; the gapped/filled bridge carries them to `M'(d)` unchanged.

## I-LEFT — ILeft (EFFECT, clause)

`(A v : v ∈ V_S(d) ∧ v < p : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))` — ASN-0082 **I3-L (PostInsertionLeftFrame)** fixes these values on the left region `{1, …, J-1}` of `M'₀(d)`; the gapped/filled bridge carries them to `M'(d)` unchanged.

## I-NEW — INew (EFFECT, clause)

`(A k : 0 ≤ k < n : shift(p, k) ∈ dom(M'(d)) ∧ M'(d)(shift(p, k)) = shift(a, k))` — the `{block fill}` of the gapped/filled bridge: the block positions `shift(p, k) = q_{J+k}` (`0 ≤ k < n`), left free by the gapped arrangement, mapped in lockstep to the K.α run `A_new`.

## I-DOM — IDom (EFFECT, clause)

`{v ∈ dom(M'(d)) : subspace(v) = S} = {q_1, …, q_{J-1}} ∪ {q_J, …, q_{J+n-1}} ∪ {q_{J+n}, …, q_{N+n}}` — the gapped/filled bridge at the domain level: I3-CS (PostInsertionSubspaceClosure) supplies the gapped domain (left prefix `{q_1, …, q_{J-1}}` and shifted suffix `{q_{J+n}, …, q_{N+n}}`), and INSERT's own I-NEW `{block fill}` supplies the middle block `{q_J, …, q_{J+n-1}}`.

## I-PROV — IProv (EFFECT, clause)

`R' = R ∪ {(shift(a, k), d) : 0 ≤ k < n}` — the `n` provenance records coupling each freshly allocated I-address to its inserting document, by **K.ρ (ProvenanceRecording, ASN-0047)** iterated `n` times. The record is `(shift(a, k), d)` with `shift(a, k)` element-level content (S7b/C1) and `d` document-level, matching `Σ.R ⊆ T_elem × E_doc`. These are the only additions to `R`; INSERT removes nothing from it (P2 of ASN-0047, R monotone).

## F-SUB — FSub (FRAME, clause)

`(A S' : S' ≠ S : {v ∈ dom(M'(d)) : subspace(v) = S'} = {v ∈ dom(M(d)) : subspace(v) = S'}` and `M'(d)` agrees with `M(d)` there`)` — the set equality is two inclusions. Every prior cross-subspace position persists with its value (`{v ∈ dom(M(d)) : subspace(v) = S'} ⊆ {v ∈ dom(M'(d)) : subspace(v) = S'}`, with agreement there) by ASN-0082 **I3-X (PostInsertionCrossSubspaceFrame)**; and INSERT adds no cross-subspace position (the reverse inclusion `{v ∈ dom(M'(d)) : subspace(v) = S'} ⊆ {v ∈ dom(M(d)) : subspace(v) = S'}`) by ASN-0082 **I3-CX (PostInsertionCrossSubspaceClosure)**.

## F-DOC — FDoc (FRAME, clause)

`(A d' : d' ≠ d : M'(d') = M(d'))` — ASN-0082 **I3-D (PostInsertionCrossDocumentFrame)**.

## F-LINK — FLink (FRAME, clause)

`Σ'.L = Σ.L` — the link store is untouched. INSERT's only K-atomics are K.α (content), K.μ⁻/K.μ⁺ (arrangement), and K.ρ (provenance); none touches `Σ.L`.

## F-ENT — FEnt (FRAME, clause)

`Σ'.E = Σ.E` — the entity set is untouched. INSERT registers no entity (it requires `d ∈ dom(M) = E_doc` already).

---

## IP0 (OriginIdentity) — OriginIdentity (LEMMA, lemma)

*For each `k` with `0 ≤ k < n`, `shift(a, k) ∉ dom(C)`, and `shift(a, k)` is distinct from every I-address in `dom(C)` regardless of whether the freshly written value `C'(shift(a, k)) = w_k` equals `C(b)` for any existing `b ∈ dom(C)`.*

## IP1 (InsertedRun) — InsertedRun (LEMMA, lemma)

*The inserted material forms a single correspondence run: for `0 ≤ k < n`, `M'(d)(shift(p, k)) = shift(a, k)`, so V-positions and I-addresses advance in lockstep over a contiguous block. The block `{shift(p, k) : 0 ≤ k < n}` is order-isomorphic to its image `{shift(a, k) : 0 ≤ k < n}` under T1.*

## IP2 (ContentAppendOnly) — ContentAppendOnly (LEMMA, lemma)

*`dom(C) ⊆ dom(C')` and `(A b : b ∈ dom(C) : C'(b) = C(b))`.*

## IP3 (PositionImpermanence) — PositionImpermanence (LEMMA, lemma)

*A V-position binds no permanent content. When the insertion point is occupied (`J ≤ N`), the block slots `{q_k : J ≤ k ≤ min(J+n−1, N)}` lie in `dom(M(d)) ∩ dom(M'(d))` yet `M'(d)(q_k) = shift(a, k−J) ≠ M(d)(q_k)` — the same slot now resolves to freshly minted content, since `shift(a, k−J) ∈ A_new` is fresh (IP0) while `M(d)(q_k) ∈ dom(C)` by **S3★ (GeneralizedReferentialIntegrity, ASN-0047)**, since `subspace(q_k) = s_C` places the image of a content-subspace V-position in the content store. The permanence guarantee attaches to the I-address (IP0, IP2), never to the slot.*

## IP4 (LinkSurvival) — LinkSurvival (LEMMA, lemma)

*For every prior link `a ∈ dom(Σ.L)` and every slot `i`, with `e = Σ.L(a).eᵢ` its endset, LP3★ (with L12 across the composite) fixes `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)` — no link's designated content changes. The post-insert resolved-witness set of `e` in `d` is `project(e, d, Σ') = {v ∈ dom(M'(d)) : M'(d)(v) ∈ coverage(e)}`, which decomposes into four disjoint parts:*

- *Left witnesses: `{v ∈ V_S(d) : v < p ∧ M(d)(v) ∈ coverage(e)}`, preserved verbatim by I-LEFT.*
- *Shifted-suffix witnesses: `{shift(v, n) : v ∈ V_S(d) ∧ v ≥ p ∧ M(d)(v) ∈ coverage(e)}`, carried to the new slot by I-SHIFT.*
- *Cross-subspace witnesses: `{v ∈ dom(M(d)) : subspace(v) ≠ S ∧ M(d)(v) ∈ coverage(e)}`, preserved verbatim by F-SUB.*
- *New-block witnesses, present iff `coverage(e) ∩ A_new ≠ ∅`: `{shift(p, k) : 0 ≤ k < n ∧ shift(a, k) ∈ coverage(e)}` (a resurrection in the sense of LP18 only when the link was orphaned at `Σ`).*

*The prior witness set `project(e, d, Σ)` partitions into left, suffix, and cross-subspace witnesses, and INSERT maps these injectively into the post-insert set: left and cross-subspace verbatim, suffix by the bijection `v ↦ shift(v, n)` (I-SHIFT). In every case the map is a bijection from the prior set onto (left ∪ shifted-suffix ∪ cross-subspace). Hence the witness **count** is non-decreasing,*

> `|project(e, d, Σ')| = |project(e, d, Σ)| + |{shift(p, k) : 0 ≤ k < n ∧ shift(a, k) ∈ coverage(e)}|`,

*and the resolved **content** grows monotonically,*

> `coverage(e) ∩ ran(M(d)) ⊆ coverage(e) ∩ ran(M'(d))`,

*with equality in both iff the new-block part is empty, i.e. iff `coverage(e) ∩ A_new = ∅`.*

## IP5 (DocumentIsolation) — DocumentIsolation (LEMMA, lemma)

*For every `d' ≠ d`: `M'(d') = M(d')`, and for every `v' ∈ dom(M(d'))` the resolved entity is invariant per subspace — `subspace(v') = s_C ⟹ M'(d')(v') ∈ dom(C')` with `C'(M'(d')(v')) = C(M(d')(v'))` (content value fixed by IP2), and `subspace(v') = s_L ⟹ M'(d')(v') ∈ dom(L')` with `L'(M'(d')(v')) = L(M(d')(v'))` (link value fixed by F-LINK). The arrangement and resolved content of every other document are invariant under INSERT on `d`.*

## IP6 (DiscoverabilityWP) — DiscoverabilityWP (LEMMA, lemma)

*The weakest precondition under which INSERT preserves the set of links discoverable from `d` is*

> `wp(INSERT, D(d, Σ') = D(d, Σ)) ≡ INSERT-pre ∧ {a ∈ dom(Σ.L) : (E i : coverage(Σ.L(a).eᵢ) ∩ A_new ≠ ∅)} ⊆ D(d, Σ)`.

*where `D(d, Σ) = {a ∈ dom(Σ.L) : discoverable_from(a, d, Σ)}` and `D(d, Σ') = D(d, Σ) ∪ Added` with `Added = {a ∈ dom(Σ.L) : (E i : coverage(Σ.L(a).eᵢ) ∩ A_new ≠ ∅)}`. The two coincide iff `Added ⊆ D(d, Σ)` — not iff `Added = ∅`. A sufficient condition discharging the wp: if every prior endset is tight at its creation state, then LP19a (TightFreshness) gives `A_new ∩ coverage(e) = ∅` for every K.α-fresh address, so `Added = ∅ ⊆ D(d, Σ)` and the wp reduces to `INSERT-pre`.*

## PROV (InsertionProvenance) — InsertionProvenance (LEMMA, lemma)

*INSERT records `R' = R ∪ {(shift(a, k), d) : 0 ≤ k < n}` (I-PROV) within the same composite that allocates and places the content, not deferred: every freshly minted content address `shift(a, k)` enters `R` coupled to its inserting document `d` in the same composite that mints it.*
