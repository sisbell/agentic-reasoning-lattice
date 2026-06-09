# ASN-0116 Claim Statements

*Source: ASN-0116-insert-operation.md (revised 2026-06-08) — Extracted: 2026-06-08*

## Definition — OrdinalShift

`shift(v, n) = v ⊕ δ(n, #v)` — advances a tumbler's final component by `n` while fixing its prefix. Consequence used throughout: `shift(q_k, n) = q_{k+n}`, where `q_k = [S, 1, …, 1, k]` of depth `m` and `actionPoint(δ(n, m)) = m = #q_k`.

## Definition — VPositionsInSubspace

`V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}` — the V-positions of document `d` in subspace `S`. For the text subspace obeying D-SEQ: `V_S(d) = {q_1, …, q_N}` where `q_k = [S, 1, …, 1, k]` of depth `m ≥ 2`, with `N = 0` the empty case.

## Definition — AllocatedRun

`A_new = {shift(a, k) : 0 ≤ k < n}` — the `n` freshly allocated I-addresses, contiguous on document `d`'s content chain, with `a` the K.α-fresh origin-`d` content I-start and each successive address advancing by `inc(·, 0) = shift(·, 1)`.

## Definition — ResolvedWitnessSet

`project(e, d, Σ) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}` — the set of V-positions of `d` that map into the coverage of endset `e` at state `Σ`.

## Definition — DiscoverableLinks

`D(d, Σ) = {a ∈ dom(Σ.L) : discoverable_from(a, d, Σ)}` — the links discoverable from document `d` at state `Σ`, where by LP12: `discoverable_from(a, d, Σ) ⟺ (E i : coverage(Σ.L(a).eᵢ) ∩ ran(M(d)) ≠ ∅)`.

## Definition — ValidInsertionPosition

`ValidInsertionPosition(d, p)` — `p = q_J` for some `1 ≤ J ≤ N+1`, with `J = N+1` the *append* case `p = shift(max(V_S(d)), 1)` (one past the end). Requires `V_S(d) ≠ ∅`.

## Definition — ValidFirstInsertionPosition

`ValidFirstInsertionPosition(d, p, m)` — `p` is the canonical first position `[S, 1, …, 1]` of depth `m ≥ 2`; requires `V_S(d) = ∅`. This first insertion *fixes* the subspace depth at `m` for every later insertion.

---

## INSERT — Insert (OP, composite)

*Precondition.* `d ∈ dom(M) = E_doc`; `n ≥ 1`; `(A k : 0 ≤ k < n : w_k ∈ Val)`; `S = subspace(p) = s_C`; `m := #p ≥ 2`, and when `V_S(d) ≠ ∅` this `m` equals the common depth that S8-depth fixes on `V_S(d)`; `p` is S8a-well-formed; and `p` is a valid insertion position in the foundation sense (ASN-0036). The constraint `S = s_C` is load-bearing: K.α yields only content-subspace addresses (`subspace_I(a) = s_C`); were `p` in the link subspace, I-NEW would map link-subspace positions to content addresses, violating S3★ (ASN-0047).

Position predicates:
- if `V_S(d) = ∅`: `ValidFirstInsertionPosition(d, p, m)`
- if `V_S(d) ≠ ∅`: `ValidInsertionPosition(d, p)`

Allocation: `A_new ∩ dom(C) = ∅`; `a` is K.α-fresh, origin-`d`, `subspace_I(a) = s_C`.

*Effect.* INSERT is the composite of `n` content allocations (K.α, ASN-0093), an arrangement contraction–extension pair `K.μ⁻` then `K.μ⁺` (degenerating to a single `K.μ⁺` when no suffix moves) whose net effect realises the post-insertion shift of ASN-0082's I3 family, and `n` provenance recordings (K.ρ, ASN-0047).

*Step sequence — suffix-present case `1 ≤ J ≤ N`:*
> `K.α₁, …, K.αₙ` → `K.μ⁻` → `K.μ⁺` → `K.ρ₁, …, K.ρₙ`

*Step sequence — append case `J = N+1` and empty case `V_S(d) = ∅`:*
> `K.α₁, …, K.αₙ` → `K.μ⁺` → `K.ρ₁, …, K.ρₙ`

K.μ⁻ is *inapplicable* (not optional) in the append/empty cases: with `J−1 = N = n_{s_C}` the content subspace would not contract strictly.

---

## I-ALLOC — IAlloc (POST, ensures)

`dom(C') = dom(C) ∪ A_new`, with `C'(shift(a, k)) = w_k` for `0 ≤ k < n` — the K.α effect (ASN-0093), iterated `n` times along `A_C(d)`.

## I-IMM — IImm (POST, ensures)

`(A b : b ∈ dom(C) : C'(b) = C(b))` — K.α append-only (C0, ASN-0093).

## I-SHIFT — IShift (POST, ensures)

`(A v : v ∈ V_S(d) ∧ v ≥ p : shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v))` — by ASN-0082 **I3 (PostInsertionShift)** together with block-disjointness. The block `{shift(p, k) : 0 ≤ k < n}` (index interval `{J, …, J+n-1}`) is disjoint from the shifted-suffix positions (index interval `{J+n, …, N+n}`), so the union adds no entry at any shifted-suffix slot and I3's values transfer unchanged.

## I-LEFT — ILeft (POST, ensures)

`(A v : v ∈ V_S(d) ∧ v < p : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))` — by ASN-0082 **I3-L (PostInsertionLeftFrame)** together with the same block-disjointness: the block sits at index interval `{J, …, J+n-1}`, disjoint from the left positions `{1, …, J-1}`.

## I-NEW — INew (POST, ensures)

`(A k : 0 ≤ k < n : shift(p, k) ∈ dom(M'(d)) ∧ M'(d)(shift(p, k)) = shift(a, k))` — the INSERT-specific fill of the block that ASN-0082's gapped arrangement leaves vacated, mapped in lockstep to the K.α run `A_new`.

Attribution per block position `shift(p, k) = q_{J+k}`:
- For `shift(p, k) ∈ dom(M(d))` (index `J+k ≤ N`, hence `≥ p` and not in the shifted image): absence withheld by I3-V (PostInsertionVacating).
- For `shift(p, k) ∉ dom(M(d))` (index `> N`): absence follows from the domain-closure characterisation I3-CS.

No block position is a shifted-suffix image: block index `i ≤ J+n−1` implies `i−n ≤ J−1 < J`, forcing the would-be pre-image `q_{i−n}` outside `{u ∈ V_S(d) : u ≥ p}`.

## I-DOM — IDom (POST, ensures)

`{v ∈ dom(M'(d)) : subspace(v) = S} = {q_1, …, q_{J-1}} ∪ {q_J, …, q_{J+n-1}} ∪ {q_{J+n}, …, q_{N+n}}`

The three index intervals `{1, …, J-1}` (prefix), `{J, …, J+n-1}` (new), `{J+n, …, N+n}` (shifted suffix) are consecutive integer intervals — no gap — and pairwise disjoint — no double assignment — with union `{1, …, N+n}`. Therefore `V_S(d') = {q_1, …, q_{N+n}}` with `N' = N + n`. Domain closure cites I3-CS/I3-CX, ASN-0082.

## I-PROV — IProv (POST, ensures)

`R' = R ∪ {(shift(a, k), d) : 0 ≤ k < n}` — the `n` provenance records coupling each freshly allocated I-address to its inserting document, by **K.ρ (ProvenanceRecording, ASN-0047)** iterated `n` times. Each K.ρ step's precondition `shift(a, k) ∈ dom(C') ∧ d ∈ E_doc` is met: `shift(a, k)` is in the store the moment its K.α step commits it, and `d ∈ dom(M) = E_doc` by precondition. The record `(shift(a, k), d)` has `shift(a, k)` element-level content (S7b/C1) and `d` document-level, matching `Σ.R ⊆ T_elem × E_doc`.

## F-SUB — FSub (POST, ensures)

`(A S' : S' ≠ S : {v ∈ dom(M'(d)) : subspace(v) = S'} = {v ∈ dom(M(d)) : subspace(v) = S'}` and `M'(d)` agrees with `M(d)` there`)` — ASN-0082 **I3-X (PostInsertionCrossSubspaceFrame)**.

## F-DOC — FDoc (POST, ensures)

`(A d' : d' ≠ d : M'(d') = M(d'))` — ASN-0082 **I3-D (PostInsertionCrossDocumentFrame)**.

---

## P0 (OriginIdentity) — OriginIdentity (POST, ensures)

*(Restatement of K.α freshness + S4.)*

For each `k` with `0 ≤ k < n`, `shift(a, k) ∉ dom(C)`, and `shift(a, k)` is distinct from every I-address in `dom(C)` regardless of whether `C(shift(a, k))` equals the content stored at any existing address.

## P1 (InsertedRun) — InsertedRun (LEMMA, lemma)

The inserted material forms a single correspondence run: for `0 ≤ k < n`, `M'(d)(shift(p, k)) = shift(a, k)`, so V-positions and I-addresses advance in lockstep over a contiguous block. The block `{shift(p, k) : 0 ≤ k < n}` is order-isomorphic to its image `{shift(a, k) : 0 ≤ k < n}` under T1.

## P2 (ContentAppendOnly) — ContentAppendOnly (INV, predicate)

`dom(C) ⊆ dom(C')` and `(A b : b ∈ dom(C) : C'(b) = C(b))`. INSERT is purely additive on the content layer.

## P3 (AddressPermanence) — AddressPermanence (INV, predicate)

No I-address in `dom(C)` is removed or rebound by INSERT: `(A b : b ∈ dom(C) : b ∈ dom(C') ∧ C'(b) = C(b))`, and every new binding is at a fresh address (P0).

## P4 (LinkSurvival) — LinkSurvival (LEMMA, lemma)

For every endset `e` existing in `Σ`, `coverage_{Σ'}(e) = coverage_{Σ}(e)` (by L12 + LP3★ across the composite) — no link's designated content changes. The post-insert resolved-witness set of `e` in `d` is
`project(e, d, Σ') = {v ∈ dom(M'(d)) : M'(d)(v) ∈ coverage(e)}`, which decomposes into four disjoint parts:

- *Left witnesses:* `{v ∈ V_S(d) : v < p ∧ M(d)(v) ∈ coverage(e)}`, preserved verbatim by I-LEFT.
- *Shifted-suffix witnesses:* `{shift(v, n) : v ∈ V_S(d) ∧ v ≥ p ∧ M(d)(v) ∈ coverage(e)}`, carried to the new slot by I-SHIFT.
- *Cross-subspace witnesses:* `{v ∈ dom(M(d)) : subspace(v) ≠ S ∧ M(d)(v) ∈ coverage(e)}`, preserved verbatim by F-SUB.
- *New-block witnesses, present iff `coverage(e) ∩ A_new ≠ ∅`:* `{shift(p, k) : 0 ≤ k < n ∧ shift(a, k) ∈ coverage(e)}` (a resurrection in the sense of LP18 only when the link was orphaned at `Σ`).

The prior witness set `project(e, d, Σ)` partitions into left, suffix, and cross-subspace witnesses, and INSERT maps these injectively into the post-insert set: left and cross-subspace verbatim, suffix by the bijection `v ↦ shift(v, n)` (I-SHIFT). The map is a bijection from the prior set onto (left ∪ shifted-suffix ∪ cross-subspace). Hence the witness **count** is non-decreasing,

> `|project(e, d, Σ')| = |project(e, d, Σ)| + |{shift(p, k) : 0 ≤ k < n ∧ shift(a, k) ∈ coverage(e)}|`,

and the resolved **content** grows monotonically,

> `coverage(e) ∩ ran(M(d)) ⊆ coverage(e) ∩ ran(M'(d))`,

with equality in both iff the new-block part is empty, i.e. iff `coverage(e) ∩ A_new = ∅`.

## P5 (DocumentIsolation) — DocumentIsolation (LEMMA, lemma)

For every `d' ≠ d`: `M'(d') = M(d')`, and for every `v' ∈ dom(M(d'))`, `M'(d')(v') ∈ dom(C')` with `C'(M'(d')(v')) = C(M(d')(v'))`. The arrangement and resolved content of every other document are invariant under INSERT on `d`.

## P6 (DiscoverabilityWP) — DiscoverabilityWP (LEMMA, lemma)

The weakest precondition under which INSERT preserves the set of links discoverable from `d` is

> `wp(INSERT, D(d, Σ') = D(d, Σ)) ≡ INSERT-pre ∧ {a ∈ dom(Σ.L) : (E i : coverage(Σ.L(a).eᵢ) ∩ A_new ≠ ∅)} ⊆ D(d, Σ)`.

Derivation: `ran(M'(d)) = ran(M(d)) ∪ A_new` (from I-LEFT, I-SHIFT, I-NEW). Substituting into LP12:

```
  discoverable_from(a, d, Σ')
    ⟺ (E i : coverage(eᵢ) ∩ (ran(M(d)) ∪ A_new) ≠ ∅)
    ⟺ discoverable_from(a, d, Σ)  ∨  (E i : coverage(eᵢ) ∩ A_new ≠ ∅).
```

Therefore `D(d, Σ') = D(d, Σ) ∪ Added`, where `Added = {a ∈ dom(Σ.L) : (E i : coverage(Σ.L(a).eᵢ) ∩ A_new ≠ ∅)}`. The two coincide iff `Added ⊆ D(d, Σ)`.

Corollaries:
- (i) Sufficient discharge: if every prior endset is tight at its creation state (foundation `tight`, ASN-0098), then LP19a (TightFreshness) gives `A_new ∩ coverage(e) = ∅` for every K.α-fresh address, so `Added = ∅ ⊆ D(d, Σ)` and the wp reduces to `INSERT-pre`.
- (ii) The strictly stronger sufficient condition `(A a ∈ dom(Σ.L), i : coverage(Σ.L(a).eᵢ) ∩ A_new = ∅)` discharges by emptying `Added` but over-rejects: it refuses ghost-plus-live-span pre-states on which discoverability is in fact preserved.

## PROV (InsertionProvenance) — InsertionProvenance (LEMMA, lemma)

INSERT records `R' = R ∪ {(shift(a, k), d) : 0 ≤ k < n}` (I-PROV), which discharges the coupling constraints J0, J1★, J1'★ of ASN-0047 between the composite's initial and final states, and — together with the pre-state's coverage — establishes P7a and P7 at the post-state. Provenance is thus established atomically-with-allocation as part of the operation, not deferred: every freshly minted content address `shift(a, k)` enters `R` coupled to its inserting document `d` in the same composite that allocates and places it.

Sub-claims:

- **J0 (AllocationPlacementCoupling):** Every freshly allocated I-address must appear in some arrangement of the post-state. The fresh addresses are `A_new`, and I-NEW places each `shift(a, k)` at the V-position `shift(p, k) ∈ dom(M'(d))` with `d ∈ E_doc`. So J0 holds.

- **J1★ (ExtensionRecordsProvenance):** Every I-address new to the content-subspace range of `M'(d)` must carry a record `(a, d) ∈ R'`. The range-new addresses are exactly `A_new` (from I-LEFT + I-SHIFT + I-NEW: `ran(M'(d)) = ran(M(d)) ∪ A_new`), and I-PROV records `(shift(a, k), d)` for each `0 ≤ k < n`. So J1★ holds.

- **J1'★ (ProvenanceRequiresExtension):** Every new provenance entry `(a, d) ∈ R' ∖ R` must correspond to an I-address range-new in `M'(d)`. The new entries are exactly `{(shift(a, k), d) : 0 ≤ k < n}` (I-PROV adds only these), and each `shift(a, k) ∈ A_new` is range-new. So J1'★ holds.

- **P7a (ProvenanceCoverage) at post-state:** Every `a ∈ dom(C')` carries some record `(a, d') ∈ R'`. Split `dom(C') = dom(C) ∪ A_new` (I-ALLOC). For prior addresses `b ∈ dom(C)`: P7a held at pre-state, giving some `(b, d') ∈ R`; and `R ⊆ R'` (I-PROV purely additive). For new addresses `shift(a, k) ∈ A_new`: I-PROV supplies `(shift(a, k), d) ∈ R'` directly.

- **P7 (ProvenanceGrounding) at post-state:** Every `(a, d') ∈ R'` has `a ∈ dom(C')` — prior entries by P2-monotonicity, new entries because each `shift(a, k) ∈ A_new ⊆ dom(C')`.
