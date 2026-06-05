# ASN-0087 Claim Statements

*Source: ASN-0087-makelink-operation.md (revised 2026-05-26) — Extracted: 2026-06-05*

## Definition — StandardAuthoring

`StandardAuthoring(e, Σ) ≡ coverage(e) ∩ F ⊆ dom(Σ.C) ∪ dom(Σ.L)`, where `F` is ASN-0098's set of substrate-emittable addresses.

A link's input endset sequence `(e₁, ..., eₙ)` is standardly authored at `Σ` iff `StandardAuthoring(eᵢ, Σ)` holds for every `i ∈ {1, ..., N}`.

## Definition — MFreshExcl

For any `x ∈ F` with `x ∉ dom(Σ.C) ∪ dom(Σ.L)` and any endset `e` satisfying `StandardAuthoring(e, Σ)`:

  x ∉ coverage(e)

---

## M-Comp — MakeLinkComp (DEF, OP)

MAKELINK is the composite `K.λ ; K.μ⁺_L` — K.λ followed by K.μ⁺_L — applied to the same home document `d`.

## M-DepthConv — MakeLinkDepthConv (INV, predicate)

MAKELINK fixes every first link's V-position depth at the canonical minimal `m = 2`; thereafter S8-depth pins `m_L(d) = 2`. Stated and scoped in *Inputs*.

Formally: when `V_{s_L}(d) = ∅`, K.μ⁺_L admits any `m ≥ 2` via `ValidFirstLinkPosition(d, v_ℓ, m)`; MAKELINK commits to `m = 2` for every first link it places. Once it has done so, S8-depth pins `m_L(d) = 2` for all later link V-positions of that document.

## M-Pre — MakeLinkPre (PRE, requires)

Caller-visible precondition: `d ∈ dom(M)`, `N ≥ 3`, `(A i : eᵢ ∈ Endset)`, `e₃ ≠ ∅`. The caller supplies neither the link address nor its V-position.

Formally:

  enabled(MAKELINK)  ≡  d ∈ dom(Σ.M)  ∧  N ≥ 3  ∧  (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset)  ∧  e₃ ≠ ∅

## M-Alloc — MakeLinkAlloc (LEMMA, lemma)

MAKELINK derives and allocates a fresh `ℓ ∈ T \ (dom(Σ.L) ∪ dom(Σ.C))` from `A_L(d)`'s next emission, and a fresh `v_ℓ ∈ T \ dom(Σ.M(d))` from K.μ⁺_L's positioning rule (serial component `n_L + 1` computed from `Σ`), with `subspace(v_ℓ) = s_L` and `#v_ℓ` per M-DepthConv.

Sub-claims:
- (a) `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)`  [FirstEmissionFreshness, SubsequentEmissionFreshness]
- (b) `zeros(ℓ) = 3 ∧ E(ℓ)₁ = s_L ∧ #E(ℓ) ≥ 2 ∧ origin(ℓ) = d`  [FirstEmission, ChainDiscipline]
- (c) `v_ℓ ∉ dom(Σ.M(d))`

## M-Effect — MakeLinkEffect (POST, ensures)

`Σ'.L = Σ.L ∪ {ℓ ↦ (e₁, ..., eₙ)}`; `Σ'.M(d) = Σ.M(d) ∪ {v_ℓ ↦ ℓ}` (the empty/non-empty positioning case split stated once in *Effect*).

The V-position `v_ℓ` is determined by:

  v_ℓ  =  [s_L, 1]                             if V_{s_L}(d) = ∅ at Σ  (depth per M-DepthConv)
  v_ℓ  =  shift(max(V_{s_L}(d)), 1)             otherwise  (depth m_L(d), the existing link-subspace depth)

By D-SEQ★, when non-empty: `v_ℓ = [s_L, 1, ..., 1, n_L + 1]` at depth `m_L(d)`.

## M-Frame — MakeLinkFrame (POST, ensures)

`Σ'.C = Σ.C`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R`; existing entries in `L` and in `M(d')` for `d' ≠ d` are unchanged. Content is byte-identical before and after MAKELINK (referencing is read-only).

Formally:

  Σ'.C  =  Σ.C
  Σ'.E  =  Σ.E
  Σ'.R  =  Σ.R
  (A ℓ' ∈ dom(Σ.L) :: Σ'.L(ℓ') = Σ.L(ℓ'))
  (A d' ∈ dom(Σ.M), d' ≠ d :: Σ'.M(d') = Σ.M(d'))

Also (M-DocFixity): `dom(Σ'.M) = dom(Σ.M)`.

## M-DiscSymmetry — MakeLinkDiscSymmetry (LEMMA, lemma)

For the standard content-reach route, discoverability of `ℓ` is symmetric across all documents whose arrangements reach into an endset coverage — LP12 grants the home document no privileged status. The reflexive route is the home document's alone, since MAKELINK places `ℓ` into its arrangement and no other.

Formally: under `(A i : StandardAuthoring(eᵢ, Σ))`, the wp for `d_target = d` reduces to the same shape as `d_target ≠ d`:

  wp(MAKELINK, discoverable_from(ℓ, d, ·))
    ≡  enabled(MAKELINK)  ∧  (E i :: coverage(eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)

## StandardAuthoring — StandardAuthoring (DEF, predicate)

`StandardAuthoring(e, Σ) ≡ coverage(e) ∩ F ⊆ dom(Σ.C) ∪ dom(Σ.L)`, where `F` is ASN-0098's set of substrate-emittable addresses. A link's endset sequence is standardly authored at `Σ` iff every constituent endset satisfies the predicate.

## M-Reflexive — MakeLinkReflexive (LEMMA, lemma)

If `ℓ ∈ coverage(eᵢ)` for some `i` (the reflexive endset case), then `v_ℓ ∈ project(ℓ, i, d, Σ')` and `discoverable_from(ℓ, d, Σ')` is forced true regardless of `Σ.M(d)`'s pre-existing arrangement. Under `(A i : StandardAuthoring(eᵢ, Σ))` the reflexive case is structurally excluded.

Formally: if `ℓ ∈ coverage(eᵢ)` for some `i`, then since `Σ'.L(ℓ).eᵢ = eᵢ` and `Σ'.M(d)(v_ℓ) = ℓ`, we have `v_ℓ ∈ project(ℓ, i, d, Σ')`, so `discoverable_from(ℓ, d, Σ')` holds.

Under standard authoring: `ℓ ∈ F` and `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)`, so M-FreshExcl at `x = ℓ` gives `ℓ ∉ coverage(eᵢ)` for every `i` — the reflexive disjunct `(E i :: ℓ ∈ coverage(eᵢ))` is unreachable.

## M-PriorLinkDisc — MakeLinkPriorLinkDisc (LEMMA, lemma)

For every prior link `ℓ' ∈ dom(Σ.L)`: from the home document `d`, `discoverable_from(ℓ', d, Σ') ⟺ discoverable_from(ℓ', d, Σ) ∨ (E i :: ℓ ∈ coverage(Σ.L(ℓ').eᵢ))` — newly discoverable precisely when some endset of `ℓ'` covers `ℓ`; from any `d_target ≠ d`, `discoverable_from(ℓ', d_target, Σ') = discoverable_from(ℓ', d_target, Σ)`. The side-effect window is confined to the home document.

Formally:

  discoverable_from(ℓ', d, Σ')
    ⟺  discoverable_from(ℓ', d, Σ)  ∨  (E i :: ℓ ∈ coverage(Σ.L(ℓ').eᵢ))

  ¬discoverable_from(ℓ', d, Σ)  ∧  discoverable_from(ℓ', d, Σ')
    ⟺  ¬(E i :: coverage(Σ.L(ℓ').eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)
       ∧ (E i :: ℓ ∈ coverage(Σ.L(ℓ').eᵢ))

  (A d_target ≠ d :: discoverable_from(ℓ', d_target, Σ') = discoverable_from(ℓ', d_target, Σ))

## M-WP — MakeLinkWP (LEMMA, lemma)

Post-MAKELINK discoverability has explicit weakest preconditions (total correctness): for `d_target ≠ d`, `wp ≡ enabled(MAKELINK) ∧ d_target ∈ dom(Σ.M) ∧ (E i :: coverage(eᵢ) ∩ ran(Σ.M(d_target)) ≠ ∅)`; for `d_target = d`, `wp ≡ enabled(MAKELINK) ∧ [(E i :: coverage(eᵢ) ∩ ran(Σ.M(d)) ≠ ∅) ∨ (E i :: ℓ ∈ coverage(eᵢ))]`. Under `(A i : StandardAuthoring(eᵢ, Σ))` the reflexive disjunct collapses and the two shapes coincide.

Formally:

*Case 1 (`d_target ≠ d`):*

  wp(MAKELINK, discoverable_from(ℓ, d_target, ·))
    ≡  enabled(MAKELINK)  ∧  d_target ∈ dom(Σ.M)  ∧  (E i :: coverage(eᵢ) ∩ ran(Σ.M(d_target)) ≠ ∅)

*Case 2 (`d_target = d`):*

  wp(MAKELINK, discoverable_from(ℓ, d, ·))
    ≡  enabled(MAKELINK)  ∧  [(E i :: coverage(eᵢ) ∩ ran(Σ.M(d)) ≠ ∅) ∨ (E i :: ℓ ∈ coverage(eᵢ))]

*Reduction under standard authoring:*

  wp(MAKELINK, discoverable_from(ℓ, d, ·))
    ≡  enabled(MAKELINK)  ∧  (E i :: coverage(eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)

## M-Perm — MakeLinkPerm (LEMMA, lemma)

After MAKELINK: `(A Σ' →* Σ'' :: ℓ ∈ dom(Σ''.L) ∧ Σ''.L(ℓ) = Σ'.L(ℓ))`, by LP13.

Sub-claims:
- (a) `(A Σ' →* Σ'' :: ℓ ∈ dom(Σ''.L))`
- (b) `(A Σ' →* Σ'' :: Σ''.L(ℓ) = Σ'.L(ℓ))`
- (c) `(A Σ' →* Σ'' :: Σ''.L(ℓ).eᵢ = Σ'.L(ℓ).eᵢ)` for every slot `i`
- (d) `(A Σ' →* Σ'' :: coverage(Σ''.L(ℓ).eᵢ) = coverage(Σ'.L(ℓ).eᵢ))` for every slot `i`

## M-NoIndexState — MakeLinkNoIndexState (INV, predicate)

The abstract specification requires no separate index state component. Discoverability is computed from `L` and `M` via the projection function of ASN-0098.

Formally: LP12 computes discoverability from `Σ'.L(ℓ)` and `Σ'.M(d)` alone:

  discoverable_from(ℓ, d, Σ')  ⟺  (E i : coverage(Σ'.L(ℓ).eᵢ) ∩ ran(Σ'.M(d)) ≠ ∅)

No separate state component participates; discoverability is a derived function of `L` and `M`.

## M-CompAtomicity — MakeLinkCompAtomicity (LEMMA, lemma)

The composite is not atomic at the substrate level. The intermediate state `Σ_mid` between K.λ and K.μ⁺_L has the link allocated but not placed. `discoverable_from(ℓ, d_target, ·)` agrees at `Σ_mid` and `Σ'` for every `d_target ≠ d`; for `d_target = d` the two values agree unless some endset reflexively covers `ℓ`. Composite-level atomicity, if required, belongs to the protocol layer above the substrate.

Formally at `Σ_mid`:
- `ℓ ∈ dom(Σ_mid.L)` with `Σ_mid.L(ℓ) = (e₁, ..., eₙ)`
- `ℓ ∉ ran(Σ_mid.M(d))`
- `Σ_mid.M = Σ.M`  [K.λ frame]
- `(A d_target ≠ d :: discoverable_from(ℓ, d_target, Σ_mid) = discoverable_from(ℓ, d_target, Σ'))`
- For `d_target = d`: `discoverable_from(ℓ, d, Σ_mid) ≠ discoverable_from(ℓ, d, Σ')` only when `(E i :: ℓ ∈ coverage(eᵢ))`

## M-Inv-State — MakeLinkInvState (INV, predicate)

*Per-state invariants at `Σ'`.* The post-state satisfies the link-store invariants (L0, L1, L1a, L1b, L1c, L3, L14, L-fin), the arrangement invariants (S2, S3★, S3★-aux, S8a, S8-depth, S8-fin, S8★, CL-OWN, CL-UNIQ, D-MIN★, D-CTG★, D-SEQ★), and the frame-inherited invariants over unchanged domains (S4, S7a, S7b, S7d, C1b, C1c, C-fin, P6, P7, P8, M0, NodeLineage, ActivatedEmission). Discharged in *Invariant Preservation*.

Sub-claims for the new entries `ℓ ∈ dom(L')` and `v_ℓ ∈ dom(M'(d))`:

  L0:    E(ℓ)₁ = s_L
  L1:    zeros(ℓ) = 3
  L1a:   origin(ℓ) = d ∈ dom(Σ'.M)
  L1b:   #E(ℓ) ≥ 2
  L3:    N ≥ 3 ∧ e₃ ≠ ∅
  L14:   ℓ ∉ dom(Σ'.C)
  S2:    v_ℓ ∉ dom(Σ.M(d))  [cross-subspace: (v_ℓ)₁ = s_L ≠ s_C; within-subspace: v_ℓ = [s_L,...,n_L+1] ∉ V_{s_L}(d)]
  S3★:   Σ'.M(d)(v_ℓ) = ℓ ∈ dom(L') ∧ subspace(v_ℓ) = s_L
  S8a:   zeros(v_ℓ) = 0 ∧ #v_ℓ = m_L^{Σ'}(d) ≥ 2 ∧ all components > 0
  D-MIN★: min(V_{s_L}^{Σ'}(d)) = [s_L, 1, ..., 1]
  D-SEQ★: V_{s_L}^{Σ'}(d) = {[s_L, 1, ..., 1, k] : 1 ≤ k ≤ K}  where K = 1 (empty case) or n_L + 1 (non-empty case)
  D-CTG★: (A z : v_lo ≤ z ≤ v_hi ∧ depth(z) = m_L^{Σ'}(d) ∧ (z)₁ = s_L :: z ∈ V_{s_L}^{Σ'}(d))
  CL-OWN: origin(Σ'.M(d)(v_ℓ)) = origin(ℓ) = d
  CL-UNIQ: ℓ ∉ ran(Σ_mid.M(d))  [hence partial injection preserved]

## M-Inv-Bdry — MakeLinkInvBdry (INV, predicate)

*Composite-boundary properties at `Σ'`.* P4★, P4a, P7a hold at `Σ'`, and the coupling constraints J0, J1★, J1'★ are satisfied across the composite. Discharged in *Invariant Preservation*.

Formally:
- J0 (AllocationPlacementCoupling): `dom(Σ'.C) ∖ dom(Σ.C) = ∅` → vacuously satisfied
- J1'★ (ProvenanceRequiresExtension): `R' ∖ R = ∅` → vacuously satisfied
- J1★ (ExtensionRecordsProvenance): `subspace(v_ℓ) = s_L ≠ s_C` → no content-subspace witness arises
- P4★: `Contains_C(Σ') ⊆ R'`; since `subspace(v_ℓ) = s_L`, `Contains_C(Σ') = Contains_C(Σ) ⊆ R = R'`
- P4a: `(A (a, d') ∈ R' :: (E Σ_k, v :: M_k(d')(v) = a ∧ subspace(v) = s_C))`; holds by reachability since `R' = R`
- P7a: `(A a ∈ dom(Σ'.C) :: (E d' :: (a, d') ∈ R'))`; holds by reachability since `dom(Σ'.C) = dom(Σ.C)` and `R' = R`

## M-Inv-Trans — MakeLinkInvTrans (INV, predicate)

*Transition invariants for `Σ → Σ'`.* M1, L12, P0, P1, P2 hold, and P3 (= P0 ∧ P1 ∧ P2 ∧ L12) holds as their conjunction. Discharged in *Invariant Preservation*.

Formally:
- M1: `dom(Σ.M) ⊆ dom(Σ'.M)`  [holds with equality by M-DocFixity]
- L12: `(A ℓ' ∈ dom(Σ.L) :: ℓ' ∈ dom(Σ'.L) ∧ Σ'.L(ℓ') = Σ.L(ℓ'))`
- P0: `Σ'.C = Σ.C`
- P1: `Σ'.E = Σ.E`
- P2: `Σ'.R = Σ.R`
- P3: `P0 ∧ P1 ∧ P2 ∧ L12`
