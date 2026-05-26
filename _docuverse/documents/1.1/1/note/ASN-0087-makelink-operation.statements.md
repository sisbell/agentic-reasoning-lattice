# ASN-0087 Claim Statements

*Source: ASN-0087-makelink-operation.md (revised 2026-05-26) — Extracted: 2026-05-26*

## Definition — StandardAuthoringPred

```
StandardAuthoring(e, Σ)  ≡  coverage(e) ⊆ dom(Σ.C) ∪ dom(Σ.L)

A link's input endset sequence (e₁, ..., eₙ) is standardly authored at Σ iff
StandardAuthoring(eᵢ, Σ) holds for every i ∈ {1, ..., N}.
```

## Definition — Project

```
project(ℓ, i, d, Σ')  =  {v ∈ dom(Σ'.M(d)) : Σ'.M(d)(v) ∈ coverage(Σ'.L(ℓ).eᵢ)}
```

## Definition — DiscoverableFrom

```
discoverable_from(ℓ, d, Σ')  ≡  (E i :: project(ℓ, i, d, Σ') ≠ ∅)

By LP12 (ASN-0098):
  discoverable_from(ℓ, d, Σ')  ⟺  (E i : coverage(Σ'.L(ℓ).eᵢ) ∩ ran(Σ'.M(d)) ≠ ∅)

Defined only when ℓ ∈ dom(Σ.L) ∧ d ∈ dom(Σ.M).
```

---

## M-Comp — MakelinkComposite (DEF, definition)

MAKELINK is the composite `K.λ ; K.μ⁺_L` — K.λ followed by K.μ⁺_L — applied to the same home document `d`. The semicolon denotes sequential composition, distinct from the tumbler addition `⊕` of ASN-0034.

## M-Pre — MakelinkPrecondition (PRE, requires)

Caller-visible precondition: `d ∈ dom(M)`, `N ≥ 3`, `(A i : eᵢ ∈ Endset)`, `e₃ ≠ ∅`. System-supplied parameters: `ℓ` from `A_L(d)`'s next emission, `v_ℓ` from K.μ⁺_L's positioning rule at depth `m_L = 2`.

## M-Alloc — MakelinkAlloc (LEMMA, lemma)

MAKELINK allocates a fresh `ℓ ∈ T \ (dom(Σ.L) ∪ dom(Σ.C))` and a fresh `v_ℓ ∈ T \ dom(Σ.M(d))` with `subspace(v_ℓ) = s_L` and `#v_ℓ = 2`.

## M-Effect — MakelinkEffect (DEF, definition)

`Σ'.L = Σ.L ∪ {ℓ ↦ (e₁, ..., eₙ)}`; `Σ'.M(d) = Σ.M(d) ∪ {v_ℓ ↦ ℓ}` where `v_ℓ = [s_L, 1]` if `V_{s_L}(d) = ∅` at `Σ`, else `v_ℓ = shift(max(V_{s_L}(d)), 1) = [s_L, n_L + 1]` (with `n_L = |V_{s_L}(d)|`).

## M-Frame — MakelinkFrame (LEMMA, lemma)

`Σ'.C = Σ.C`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R`; existing entries in `L` and in `M(d')` for `d' ≠ d` are unchanged.

## M-NoContentEffect — MakelinkNoContentEffect (LEMMA, lemma)

For every `a ∈ dom(Σ.C)`: `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)`. The referenced content is byte-identical before and after MAKELINK.

## M-DiscSymmetry — MakelinkDiscSymmetry (LEMMA, lemma)

Discoverability of `ℓ` is symmetric across all documents whose arrangements reach into any endset coverage; the home document has no privileged role in LP12's definition. Any asymmetry of outcome reflects asymmetry of arrangement-reach, not a privileged status.

## StandardAuthoring — StandardAuthoring (DEF, predicate)

`StandardAuthoring(e, Σ) ≡ coverage(e) ⊆ dom(Σ.C) ∪ dom(Σ.L)` — a structural predicate on endset values at a state. A link's endset sequence is standardly authored at `Σ` iff every constituent endset satisfies the predicate. This is the named discipline cited by M-Reflexive, M-WP, and the cascade-vacuity discussion.

## M-Reflexive — MakelinkReflexive (LEMMA, lemma)

If `ℓ ∈ coverage(eᵢ)` for some `i` (the reflexive endset case), then `v_ℓ ∈ project(ℓ, i, d, Σ')` and `discoverable_from(ℓ, d, Σ')` is forced true regardless of `Σ.M(d)`'s pre-existing arrangement. When `(A i : StandardAuthoring(eᵢ, Σ))` holds for the input endsets, the reflexive case is structurally excluded by K.λ's freshness: `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)` combined with `coverage(eᵢ) ⊆ dom(Σ.C) ∪ dom(Σ.L)` gives `ℓ ∉ coverage(eᵢ)` for every `i`.

## M-PriorLinkDisc — MakelinkPriorLinkDisc (LEMMA, lemma)

For every prior link `ℓ' ∈ dom(Σ.L)` and every document `d_target ∈ dom(Σ.M)`:

- if `d_target = d` (the home document of the new link `ℓ`), then:
  ```
  discoverable_from(ℓ', d, Σ') ⟺ discoverable_from(ℓ', d, Σ) ∨ (E i :: ℓ ∈ coverage(Σ.L(ℓ').eᵢ))
  ```
  — a prior link is newly discoverable from `d` precisely when some endset of `ℓ'` covers `ℓ`;

- if `d_target ≠ d`, then `discoverable_from(ℓ', d_target, Σ') = discoverable_from(ℓ', d_target, Σ)` by K.μ⁺_L's frame on `M` (and K.λ's frame on `M`), so prior-link discoverability is unchanged.

The discoverability relation is derived from `(L, M)` and is not preserved by the frame on `L` alone; the side-effect window is confined to the home document. Cross-document discovery cascades across sequences of MAKELINK invocations preserve every per-state invariant by LP9 (monotone projection) + LP13 (link persistence) + L12 (link immutability); the cascade redistributes discoverability but corrupts no state component.

## M-WP — MakelinkWP (LEMMA, lemma)

Post-MAKELINK discoverability has explicit weakest preconditions on `Σ`, each conjoined with the membership clause that keeps `discoverable_from` defined at the post-state:

- for `d_target ≠ d`:
  ```
  wp ≡ d_target ∈ dom(Σ.M) ∧ (E i :: coverage(eᵢ) ∩ ran(Σ.M(d_target)) ≠ ∅)
  ```
- for `d_target = d`:
  ```
  wp ≡ d ∈ dom(Σ.M) ∧ [(E i :: coverage(eᵢ) ∩ ran(Σ.M(d)) ≠ ∅) ∨ (E i :: ℓ ∈ coverage(eᵢ))]
  ```
  (the `d ∈ dom(Σ.M)` conjunct is automatic from MAKELINK's input precondition).

By M1 combined with the K.λ and K.μ⁺_L frames on `dom(M)` (which together give equality `dom(Σ'.M) = dom(Σ.M)` at MAKELINK), the membership clause is equivalent to `d_target ∈ dom(Σ'.M)`. When `(A i : StandardAuthoring(eᵢ, Σ))`, the home and non-home wp shapes coincide (the reflexive disjunct collapses).

## M-Perm — MakelinkPermanence (LEMMA, lemma)

After MAKELINK: `(A reachable Σ' →* Σ'' :: ℓ ∈ dom(Σ''.L) ∧ Σ''.L(ℓ) = Σ'.L(ℓ))`, by LP13.

## M-NoIndexState — MakelinkNoIndexState (LEMMA, lemma)

The abstract specification requires no separate index state component. Discoverability is computed from `L` and `M` via the projection function of ASN-0098.

## M-CompAtomicity — MakelinkCompositeAtomicity (LEMMA, lemma)

The composite is not atomic at the substrate level. The intermediate state `Σ_mid` between K.λ and K.μ⁺_L has the link allocated but not placed. `discoverable_from(ℓ, d_target, ·)` agrees at `Σ_mid` and `Σ'` for every `d_target ≠ d`; for `d_target = d` the two values agree unless some endset reflexively covers `ℓ`. Composite-level atomicity, if required, belongs to the protocol layer above the substrate.

## M-Inv-State — MakelinkInvState (INV, predicate)

*Per-state invariants at `Σ'`.* The post-state satisfies: link-store invariants (L0, L1, L1a, L1b, L1c, L3, L14, L-fin); arrangement invariants (S2, S3★, S3★-aux, S8a, S8-depth, S8-fin, S8★, CL-OWN, CL-UNIQ, D-MIN★, D-CTG★, D-SEQ★); and vacuous-by-frame invariants (M0, S4, S7a, S7b, S7c, S7d, C-fin, P6, P7, P8, NodeLineage).

## M-Inv-Bdry — MakelinkInvBoundary (INV, predicate)

*Composite-boundary properties at `Σ'`.* P4★, P4a, P7a hold at `Σ'` — all preserved because `R' = R`, `dom(Σ'.C) = dom(Σ.C)`, and the new V-arrangement entry is link-subspace (so it does not enter `Contains_C(Σ')`). The three coupling constraints are discharged separately: J0 by `dom(Σ'.C) ∖ dom(Σ.C) = ∅` (frame on `C`); J1★ by `subspace(v_ℓ) = s_L ≠ s_C` (structural, the new V-position fails J1★'s content-subspace filter); J1'★ by `R' ∖ R = ∅` (frame on `R`).

## M-Inv-Trans — MakelinkInvTransition (INV, predicate)

*Transition invariants for `Σ → Σ'`.* M1, L12, P0, P1, P2 hold, and P3 (= P0 ∧ P1 ∧ P2 ∧ L12) holds as their conjunction; S9 follows from P0. Each conjunct is discharged trivially by the frames `Σ'.C = Σ.C`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R`, and L12 by K.λ adding only the fresh `ℓ`.
