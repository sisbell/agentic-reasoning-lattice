# ASN-0087 Claim Statements

*Source: ASN-0087-makelink-operation.md (revised 2026-05-26) — Extracted: 2026-06-04*

## Definition — StandardAuthoring

```
StandardAuthoring(e, Σ)  ≡  coverage(e) ∩ F  ⊆  dom(Σ.C) ∪ dom(Σ.L)
```

Where `F` is ASN-0098's set of substrate-emittable addresses (the only set K.α and K.λ allocate from, with `dom(Σ.C) ∪ dom(Σ.L) ⊆ F` by LP-Sub). A link's input endset sequence `(e₁, ..., eₙ)` is standardly authored at `Σ` iff `StandardAuthoring(eᵢ, Σ)` holds for every `i ∈ {1, ..., N}`.

---

## Definition — EnabledMAKELINK

```
enabled(MAKELINK)  ≡  d ∈ dom(Σ.M)  ∧  N ≥ 3  ∧  (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset)  ∧  e₃ ≠ ∅
```

---

## Definition — MFreshExcl

*Fresh-address exclusion (M-FreshExcl).* For any `x ∈ F` with `x ∉ dom(Σ.C) ∪ dom(Σ.L)` and any endset `e` satisfying `StandardAuthoring(e, Σ)`:

```
x ∉ coverage(e)
```

---

## Definition — MDocFixity

```
dom(Σ'.M) = dom(Σ.M)
```

Follows from K.λ's frame holding `M` entirely fixed and K.μ⁺_L's effect extending `dom(M(d))` for an already-registered `d` without adding any new document, combined with the M1 inclusion `dom(Σ.M) ⊆ dom(Σ'.M)`.

---

## M-Comp — MComp (PROP, axiom)

MAKELINK is the composite `K.λ ; K.μ⁺_L` — K.λ followed by K.μ⁺_L — applied to the same home document `d`.

---

## M-DepthConv — MDepthConv (INV, predicate)

MAKELINK fixes every first link's V-position depth at the canonical minimal `m = 2`; thereafter S8-depth pins `m_L(d) = 2`. Stated and scoped in *Inputs*.

Full statement from *Inputs*: When `V_{s_L}(d) = ∅`, the substrate operation K.μ⁺_L (ASN-0047) admits *any* `m ≥ 2` for the first link's V-position via `ValidFirstLinkPosition(d, v_ℓ, m)`. MAKELINK commits to the *minimal admissible* depth `m = 2` for every first link *it* places. Once it has done so, S8-depth (ASN-0047) pins `m_L(d) = 2` for all later link V-positions of that document.

---

## M-Pre — MPre (PRE, requires)

Caller-visible precondition: `d ∈ dom(M)`, `N ≥ 3`, `(A i : eᵢ ∈ Endset)`, `e₃ ≠ ∅`. The caller supplies neither the link address nor its V-position.

Formal expansion from *Preconditions*:

```
d ∈ dom(M)
ℓ is produced by A_L(d) (first emission if d has no prior links; otherwise inc(ℓ_prev, 0))
N ≥ 3 ∧ (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset) ∧ e₃ ≠ ∅
```

The freshness and structural shape of `ℓ` are derived — ASN-0093 facts that hold automatically for any `A_L(d)` emission:

```
ℓ ∉ dom(C) ∪ dom(L)                                   [FirstEmissionFreshness, SubsequentEmissionFreshness]
zeros(ℓ) = 3 ∧ E(ℓ)₁ = s_L ∧ #E(ℓ) ≥ 2 ∧ origin(ℓ) = d   [FirstEmission, ChainDiscipline]
```

---

## M-Alloc — MAlloc (PROP, lemma)

MAKELINK derives and allocates a fresh `ℓ ∈ T \ (dom(Σ.L) ∪ dom(Σ.C))` from `A_L(d)`'s next emission, and a fresh `v_ℓ ∈ T \ dom(Σ.M(d))` from K.μ⁺_L's positioning rule (serial component `n_L + 1` computed from `Σ`), with `subspace(v_ℓ) = s_L` and `#v_ℓ` per M-DepthConv.

---

## M-Effect — MEffect (PROP, axiom)

`Σ'.L = Σ.L ∪ {ℓ ↦ (e₁, ..., eₙ)}`; `Σ'.M(d) = Σ.M(d) ∪ {v_ℓ ↦ ℓ}` (the empty/non-empty positioning case split stated once in *Effect*).

Full positioning split:

```
v_ℓ  =  [s_L, 1]                          if V_{s_L}(d) = ∅ at Σ  (depth per M-DepthConv)
v_ℓ  =  shift(max(V_{s_L}(d)), 1)          otherwise  (depth m_L(d), the existing link-subspace depth)
```

By D-SEQ★ (ASN-0047), `V_{s_L}(d) = {[s_L, 1, ..., 1, k] : 1 ≤ k ≤ n_L}` of common depth `m_L(d)` when non-empty (with `n_L = |V_{s_L}(d)|`), so the non-empty case yields `v_ℓ = shift(max(V_{s_L}(d)), 1) = [s_L, 1, ..., 1, n_L + 1]` at that same depth `m_L(d)`.

---

## M-Frame — MFrame (INV, predicate)

`Σ'.C = Σ.C`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R`; existing entries in `L` and in `M(d')` for `d' ≠ d` are unchanged. Content is byte-identical before and after MAKELINK (referencing is read-only).

Formal frame conditions:

```
Σ'.C  =  Σ.C
Σ'.E  =  Σ.E                                          [K.λ, K.μ⁺_L hold E fixed]
Σ'.R  =  Σ.R                                          [K.λ, K.μ⁺_L hold R fixed]
(A ℓ' ∈ dom(Σ.L) :: Σ'.L(ℓ') = Σ.L(ℓ'))               [L12]
(A d' ∈ dom(Σ.M), d' ≠ d :: Σ'.M(d') = Σ.M(d'))
```

---

## M-DiscSymmetry — MDiscSymmetry (PROP, lemma)

For the standard content-reach route, discoverability of `ℓ` is symmetric across all documents whose arrangements reach into an endset coverage — LP12 grants the home document no privileged status. The reflexive route is the home document's alone, since MAKELINK places `ℓ` into its arrangement and no other.

Under `(A i : StandardAuthoring(eᵢ, Σ))`:

```
wp(MAKELINK, discoverable_from(ℓ, d, ·))
  ≡  enabled(MAKELINK)  ∧  (E i :: coverage(eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)
```

— the same shape as Case 1 (with `d_target := d`); there is no automatic "self-discovery" of `ℓ` from `d`.

---

## StandardAuthoring — StandardAuthoring (DEF, predicate)

`StandardAuthoring(e, Σ) ≡ coverage(e) ∩ F ⊆ dom(Σ.C) ∪ dom(Σ.L)`, where `F` is ASN-0098's set of substrate-emittable addresses. A link's endset sequence is standardly authored at `Σ` iff every constituent endset satisfies the predicate.

---

## M-Reflexive — MReflexive (LEMMA, lemma)

If `ℓ ∈ coverage(eᵢ)` for some `i` (the reflexive endset case), then `v_ℓ ∈ project(ℓ, i, d, Σ')` and `discoverable_from(ℓ, d, Σ')` is forced true regardless of `Σ.M(d)`'s pre-existing arrangement. Under `(A i : StandardAuthoring(eᵢ, Σ))` the reflexive case is structurally excluded.

Formal witness: since `Σ'.L(ℓ).eᵢ = eᵢ` (K.λ's effect, K.μ⁺_L's frame on `L`) and `Σ'.M(d)(v_ℓ) = ℓ`, we have `v_ℓ ∈ project(ℓ, i, d, Σ')`, so `discoverable_from(ℓ, d, Σ')` holds.

Exclusion under standard authoring: K.λ's freshness gives `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)`, so M-FreshExcl instantiated at `x = ℓ` yields `ℓ ∉ coverage(eᵢ)` for every `i`.

---

## M-PriorLinkDisc — MPriorLinkDisc (LEMMA, lemma)

For every prior link `ℓ' ∈ dom(Σ.L)`: from the home document `d`, `discoverable_from(ℓ', d, Σ') ⟺ discoverable_from(ℓ', d, Σ) ∨ (E i :: ℓ ∈ coverage(Σ.L(ℓ').eᵢ))` — newly discoverable precisely when some endset of `ℓ'` covers `ℓ`; from any `d_target ≠ d`, `discoverable_from(ℓ', d_target, Σ') = discoverable_from(ℓ', d_target, Σ)`. The side-effect window is confined to the home document.

Formal derivation:

```
discoverable_from(ℓ', d, Σ')
  ⟺  (E i :: coverage(Σ'.L(ℓ').eᵢ) ∩ ran(Σ'.M(d)) ≠ ∅)
  ⟺  (E i :: coverage(Σ.L(ℓ').eᵢ) ∩ (ran(Σ.M(d)) ∪ {ℓ}) ≠ ∅)
  ⟺  discoverable_from(ℓ', d, Σ)  ∨  (E i :: ℓ ∈ coverage(Σ.L(ℓ').eᵢ))
```

Newly discoverable characterization:

```
¬discoverable_from(ℓ', d, Σ)  ∧  discoverable_from(ℓ', d, Σ')
  ⟺  ¬(E i :: coverage(Σ.L(ℓ').eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)
     ∧ (E i :: ℓ ∈ coverage(Σ.L(ℓ').eᵢ))
```

---

## M-WP — MWP (LEMMA, lemma)

Post-MAKELINK discoverability has explicit weakest preconditions (total correctness): for `d_target ≠ d`, `wp ≡ enabled(MAKELINK) ∧ d_target ∈ dom(Σ.M) ∧ (E i :: coverage(eᵢ) ∩ ran(Σ.M(d_target)) ≠ ∅)`; for `d_target = d`, `wp ≡ enabled(MAKELINK) ∧ [(E i :: coverage(eᵢ) ∩ ran(Σ.M(d)) ≠ ∅) ∨ (E i :: ℓ ∈ coverage(eᵢ))]`. Under `(A i : StandardAuthoring(eᵢ, Σ))` the reflexive disjunct collapses and the two shapes coincide.

*Case 1 (d_target ≠ d):*

```
wp(MAKELINK, discoverable_from(ℓ, d_target, ·))
  ≡  enabled(MAKELINK)  ∧  d_target ∈ dom(Σ.M)  ∧  (E i :: coverage(eᵢ) ∩ ran(Σ.M(d_target)) ≠ ∅)
```

*Case 2 (d_target = d):*

```
wp(MAKELINK, discoverable_from(ℓ, d, ·))
  ≡  enabled(MAKELINK)  ∧  [(E i :: coverage(eᵢ) ∩ ran(Σ.M(d)) ≠ ∅) ∨ (E i :: ℓ ∈ coverage(eᵢ))]
```

*Reduction under standard authoring* (`(A i : StandardAuthoring(eᵢ, Σ))`):

```
wp(MAKELINK, discoverable_from(ℓ, d, ·))
  ≡  enabled(MAKELINK)  ∧  (E i :: coverage(eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)
```

---

## M-Perm — MPerm (INV, predicate)

After MAKELINK: `(A Σ' →* Σ'' :: ℓ ∈ dom(Σ''.L) ∧ Σ''.L(ℓ) = Σ'.L(ℓ))`, by LP13.

Coverage corollary: `coverage(Σ''.L(ℓ).eᵢ) = coverage(Σ'.L(ℓ).eᵢ)` for every slot `i` and every reachable `Σ''`.

---

## M-NoIndexState — MNoIndexState (PROP, axiom)

The abstract specification requires no separate index state component. Discoverability is computed from `L` and `M` via the projection function of ASN-0098.

Formal basis: LP12 computes discoverability from `Σ'.L(ℓ)` and `Σ'.M(d)` alone — no separate state component participates.

```
discoverable_from(ℓ, d, Σ')  ⟺  (E i : coverage(Σ'.L(ℓ).eᵢ) ∩ ran(Σ'.M(d)) ≠ ∅)
```

---

## M-CompAtomicity — MCompAtomicity (PROP, lemma)

The composite is not atomic at the substrate level. The intermediate state `Σ_mid` between K.λ and K.μ⁺_L has the link allocated but not placed. `discoverable_from(ℓ, d_target, ·)` agrees at `Σ_mid` and `Σ'` for every `d_target ≠ d`; for `d_target = d` the two values agree unless some endset reflexively covers `ℓ`. Composite-level atomicity, if required, belongs to the protocol layer above the substrate.

Intermediate-state characterization:

- `ℓ ∈ dom(Σ_mid.L)` with value `Σ_mid.L(ℓ) = (e₁, ..., eₙ)`
- `ℓ ∉ ran(Σ_mid.M(d))`
- `discoverable_from(ℓ, d_target, Σ_mid)` is well-defined for every `d_target ∈ dom(Σ_mid.M) = dom(Σ.M)` since `ℓ ∈ dom(Σ_mid.L)`

Because K.λ's frame fixes `M` (`Σ_mid.M = Σ.M`), the discoverability change across MAKELINK occurs entirely at the K.μ⁺_L step.

---

## M-Inv-State — MInvState (INV, predicate)

*Per-state invariants at `Σ'`.* The post-state satisfies the link-store invariants (L0, L1, L1a, L1b, L1c, L3, L14, L-fin), the arrangement invariants (S2, S3★, S3★-aux, S8a, S8-depth, S8-fin, S8★, CL-OWN, CL-UNIQ, D-MIN★, D-CTG★, D-SEQ★), and the frame-inherited invariants over unchanged domains (S4, S7a, S7b, S7d, C1b, C1c, C-fin, P6, P7, P8, M0, NodeLineage, ActivatedEmission). Discharged in *Invariant Preservation*.

Key sub-claims:

(a) `ℓ ∉ ran(Σ.M(d))`: by S3★ every `Σ.M(d)(v) ∈ dom(Σ.C) ∪ dom(Σ.L)`, but `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)` by derived freshness, hence `ℓ ∉ ran(Σ.M(d))`.

(b) D-SEQ★ post-state:
```
V_{s_L}^{Σ'}(d) = {[s_L, 1, ..., 1, k] : 1 ≤ k ≤ 1}       if n_L = 0
V_{s_L}^{Σ'}(d) = {[s_L, 1, ..., 1, k] : 1 ≤ k ≤ n_L + 1}  if n_L ≥ 1
```

(c) D-MIN★ post-state:
```
min(V_{s_L}^{Σ'}(d)) = [s_L, 1, ..., 1]
```

(d) D-CTG★: for any slice tuple `z = [s_L, z_2, ..., z_m]` with `v_lo ≤ z ≤ v_hi`, all interior components `z_j = 1` for `2 ≤ j ≤ m − 1`, hence `z = [s_L, 1, ..., 1, z_m]` with `1 ≤ z_m ≤ K`, i.e. `z ∈ V_{s_L}^{Σ'}(d)`.

(e) CL-UNIQ: `ℓ ∉ ran(Σ_mid.M(d))` derived via S3★ + S3★-aux + K.λ freshness chain.

---

## M-Inv-Bdry — MInvBdry (INV, predicate)

*Composite-boundary properties at `Σ'`.* P4★, P4a, P7a hold at `Σ'`, and the coupling constraints J0, J1★, J1'★ are satisfied across the composite. Discharged in *Invariant Preservation*.

Sub-claims:

(a) J0, J1★, J1'★ vacuously satisfied: `dom(Σ'.C) ∖ dom(Σ.C) = ∅` and `R' ∖ R = ∅`; the sole new V-position has `subspace(v_ℓ) = s_L ≠ s_C`.

(b) P4★ (ProvenanceBounds): `Contains_C(Σ') ⊆ R'`. The new entry `v_ℓ ↦ ℓ` has `subspace(v_ℓ) = s_L`, so `Contains_C(Σ') = Contains_C(Σ) ⊆ R = R'`.

(c) P4a (TraceWitnessing): `R' = R`, obligation identical to P4a at `Σ`, holds by reachability hypothesis.

(d) P7a (ProvenanceCoverage): `dom(Σ'.C) = dom(Σ.C)` and `R' = R`, obligation identical to P7a at `Σ`, holds by reachability.

---

## M-Inv-Trans — MInvTrans (INV, predicate)

*Transition invariants for `Σ → Σ'`.* M1, L12, P0, P1, P2 hold, and P3 (= P0 ∧ P1 ∧ P2 ∧ L12) holds as their conjunction. Discharged in *Invariant Preservation*.

Sub-claims:

(a) M1: `dom(Σ.M) ⊆ dom(Σ'.M)`, holds with equality by M-DocFixity.

(b) L12: `(A ℓ' ∈ dom(Σ.L) :: ℓ' ∈ dom(Σ'.L) ∧ Σ'.L(ℓ') = Σ.L(ℓ'))`. K.λ adds only the fresh `ℓ`; no prior entry is modified.

(c) P0 (ContentPermanence): `Σ'.C = Σ.C` by frame.

(d) P1 (EntityPermanence): `Σ'.E = Σ.E` by frame.

(e) P2 (ProvenancePermanence): `Σ'.R = Σ.R` by frame.

(f) P3 = P0 ∧ P1 ∧ P2 ∧ L12.
