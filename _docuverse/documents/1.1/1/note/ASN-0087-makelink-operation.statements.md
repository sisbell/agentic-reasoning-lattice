# ASN-0087 Claim Statements

*Source: ASN-0087-makelink-operation.md (revised 2026-05-26) — Extracted: 2026-06-03*

## Definition — Project

```
project(ℓ, i, d, Σ')  =  {v ∈ dom(Σ'.M(d)) : Σ'.M(d)(v) ∈ coverage(Σ'.L(ℓ).eᵢ)}
```

## Definition — DiscoverableFrom

```
discoverable_from(ℓ, d, Σ')  ≡  (E i :: project(ℓ, i, d, Σ') ≠ ∅)
```

Biconditional form (LP12):
```
discoverable_from(ℓ, d, Σ')  ⟺  (E i : coverage(Σ'.L(ℓ).eᵢ) ∩ ran(Σ'.M(d)) ≠ ∅)
```

Defined only when `ℓ ∈ dom(Σ'.L) ∧ d ∈ dom(Σ'.M)`.

## Definition — StandardAuthoring

```
StandardAuthoring(e, Σ)  ≡  coverage(e) ⊆ dom(Σ.C) ∪ dom(Σ.L)
```

A link's input endset sequence `(e₁, ..., eₙ)` is standardly authored at `Σ` iff `StandardAuthoring(eᵢ, Σ)` holds for every `i ∈ {1, ..., N}`.

## Definition — EnabledMAKELINK

```
enabled(MAKELINK)  ≡  d ∈ dom(Σ.M)  ∧  N ≥ 3  ∧  (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset)  ∧  e₃ ≠ ∅
```

---

## M-Comp — MComp (DEF, definition)

MAKELINK is the composite `K.λ ; K.μ⁺_L` — K.λ followed by K.μ⁺_L — applied to the same home document `d`. The semicolon denotes sequential composition, distinct from the tumbler addition `⊕` of ASN-0034.

## M-DepthConv — MDepthConv (AXIOM, convention)

Normative convention: MAKELINK fixes the V-position depth of every first link *it* places at the canonical minimal `m = 2`. When `V_{s_L}(d) = ∅`, the substrate K.μ⁺_L admits any `m ≥ 2` and `Σ` does not determine `m`; MAKELINK supplies `m = 2`. Once MAKELINK has placed that first link, S8-depth pins `m_L(d) = 2` for all subsequent link V-positions of `d`. Scoped universal: for any document `d` whose every link V-position was placed by MAKELINK, `m_L(d) = 2`. This is *not* a system-wide invariant — K.μ⁺_L is a standalone primitive admitting any `m ≥ 2` and may be invoked outside MAKELINK (in another ASN or by direct substrate call), so the foundations do not establish that every link-subspace V-position in every execution sits at depth 2. Grounded in Nelson's canonical link-subspace structure (`version.0.2.serial`, depth 2) and Gregory's `findnextlinkvsa` (first link hardcoded at `2.1`), while Nelson explicitly anticipates deeper link subdivision "by further digits (after '2' and the position)".

## M-Pre — MPre (PRE, requires)

Caller-visible precondition: `d ∈ dom(M)`, `N ≥ 3`, `(A i : eᵢ ∈ Endset)`, `e₃ ≠ ∅`. System-supplied parameters: `ℓ` from `A_L(d)`'s next emission; `v_ℓ` from K.μ⁺_L's positioning rule at depth `m_L(d)` — the serial component computed from `Σ` (`n_L + 1`), the depth being the existing `m_L(d)` when `V_{s_L}(d) ≠ ∅`, or fixed at 2 by M-DepthConv for the first link (since `Σ` leaves it free).

## M-Alloc — MAlloc (LEMMA, lemma)

MAKELINK allocates a fresh `ℓ ∈ T \ (dom(Σ.L) ∪ dom(Σ.C))` and a fresh `v_ℓ ∈ T \ dom(Σ.M(d))` with `subspace(v_ℓ) = s_L` and `#v_ℓ = m_L(d)` (depth 2 by M-DepthConv for the first link; the existing `m_L(d)` thereafter).

## M-Effect — MEffect (SPEC, definition)

```
Σ'.L = Σ.L ∪ {ℓ ↦ (e₁, ..., eₙ)}
Σ'.M(d) = Σ.M(d) ∪ {v_ℓ ↦ ℓ}
```

where:
```
v_ℓ  =  [s_L, 1]                            (depth 2, fixed by M-DepthConv) if V_{s_L}(d) = ∅ at Σ
v_ℓ  =  shift(max(V_{s_L}(d)), 1)            of depth m_L(d) otherwise
```

with `n_L = |V_{s_L}(d)|`.

## M-Frame — MFrame (INV, predicate)

```
Σ'.C = Σ.C
Σ'.E = Σ.E
Σ'.R = Σ.R
```

Existing entries in `L` and in `M(d')` for `d' ≠ d` are unchanged:
```
(A ℓ' ∈ dom(Σ.L) :: Σ'.L(ℓ') = Σ.L(ℓ'))
(A d' ∈ dom(Σ.M), d' ≠ d :: Σ'.M(d') = Σ.M(d'))
```

## M-NoContentEffect — MNoContentEffect (LEMMA, lemma)

For every `a ∈ dom(Σ.C)`: `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)`. The referenced content is byte-identical before and after MAKELINK.

## M-DiscSymmetry — MDiscSymmetry (LEMMA, lemma)

Discoverability of `ℓ` is symmetric across all documents whose arrangements reach into any endset coverage; the home document has no privileged role in LP12's definition. Any asymmetry of outcome reflects asymmetry of arrangement-reach, not a privileged status.

## StandardAuthoring — StandardAuthoring (DEF, definition)

```
StandardAuthoring(e, Σ) ≡ coverage(e) ⊆ dom(Σ.C) ∪ dom(Σ.L)
```

A structural predicate on endset values at a state. A link's endset sequence is standardly authored at `Σ` iff every constituent endset satisfies the predicate. This is the named discipline cited by M-Reflexive, M-WP, and the cascade-vacuity discussion.

## M-Reflexive — MReflexive (LEMMA, lemma)

If `ℓ ∈ coverage(eᵢ)` for some `i` (the reflexive endset case), then `v_ℓ ∈ project(ℓ, i, d, Σ')` and `discoverable_from(ℓ, d, Σ')` is forced true regardless of `Σ.M(d)`'s pre-existing arrangement. When `(A i : StandardAuthoring(eᵢ, Σ))` holds for the input endsets, the reflexive case is structurally excluded by K.λ's freshness: `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)` combined with `coverage(eᵢ) ⊆ dom(Σ.C) ∪ dom(Σ.L)` gives `ℓ ∉ coverage(eᵢ)` for every `i`.

## M-PriorLinkDisc — MPriorLinkDisc (LEMMA, lemma)

For every prior link `ℓ' ∈ dom(Σ.L)` and every document `d_target ∈ dom(Σ.M)`:

If `d_target = d` (the home document of the new link `ℓ`):
```
discoverable_from(ℓ', d, Σ') ⟺ discoverable_from(ℓ', d, Σ) ∨ (E i :: ℓ ∈ coverage(Σ.L(ℓ').eᵢ))
```

If `d_target ≠ d`:
```
discoverable_from(ℓ', d_target, Σ') = discoverable_from(ℓ', d_target, Σ)
```

A prior link is newly discoverable from `d` precisely when some endset of `ℓ'` covers `ℓ`; prior-link discoverability from any other document is unchanged. The discoverability relation is derived from `(L, M)` and is not preserved by the frame on `L` alone; the side-effect window is confined to the home document. Cross-document discovery cascades across sequences of MAKELINK invocations preserve every per-state invariant by LP9 (monotone projection) + LP13 (link persistence) + L12 (link immutability); the cascade redistributes discoverability but corrupts no state component.

## M-WP — MWP (LEMMA, lemma)

Post-MAKELINK discoverability has explicit weakest preconditions on `Σ`, each conjoining MAKELINK's enabledness:
```
enabled(MAKELINK) ≡ d ∈ dom(Σ.M) ∧ N ≥ 3 ∧ (A i : eᵢ ∈ Endset) ∧ e₃ ≠ ∅
```

For `d_target ≠ d`:
```
wp(MAKELINK, discoverable_from(ℓ, d_target, ·))
  ≡  enabled(MAKELINK)  ∧  d_target ∈ dom(Σ.M)  ∧  (E i :: coverage(eᵢ) ∩ ran(Σ.M(d_target)) ≠ ∅)
```

For `d_target = d`:
```
wp(MAKELINK, discoverable_from(ℓ, d, ·))
  ≡  enabled(MAKELINK)  ∧  [(E i :: coverage(eᵢ) ∩ ran(Σ.M(d)) ≠ ∅) ∨ (E i :: ℓ ∈ coverage(eᵢ))]
```

This is the weakest precondition for *total* correctness. By M1 combined with the K.λ and K.μ⁺_L frames on `dom(M)` (which together give equality `dom(Σ'.M) = dom(Σ.M)` at MAKELINK), the membership clause is equivalent to `d_target ∈ dom(Σ'.M)`. When `(A i : StandardAuthoring(eᵢ, Σ))`, the home and non-home wp shapes coincide (the reflexive disjunct collapses).

## M-Perm — MPerm (LEMMA, lemma)

After MAKELINK:
```
(A reachable Σ' →* Σ'' :: ℓ ∈ dom(Σ''.L) ∧ Σ''.L(ℓ) = Σ'.L(ℓ))
```

by LP13.

## M-NoIndexState — MNoIndexState (INV, predicate)

The abstract specification requires no separate index state component. Discoverability is computed from `L` and `M` via the projection function of ASN-0098.

## M-CompAtomicity — MCompAtomicity (LEMMA, lemma)

The composite is not atomic at the substrate level. The intermediate state `Σ_mid` between K.λ and K.μ⁺_L has the link allocated but not placed. For `d_target ≠ d`:
```
discoverable_from(ℓ, d_target, Σ_mid) = discoverable_from(ℓ, d_target, Σ')
```

For `d_target = d`, the two values agree unless some endset reflexively covers `ℓ`. Composite-level atomicity, if required, belongs to the protocol layer above the substrate.

## M-Inv-State — MInvState (INV, predicate)

*Per-state invariants at `Σ'`.* The post-state satisfies:

Link-store invariants (L0, L1, L1a, L1b, L1c, L3, L14, L-fin); arrangement invariants (S2, S3★, S3★-aux, S8a, S8-depth, S8-fin, S8★, CL-OWN, CL-UNIQ, D-MIN★, D-CTG★, D-SEQ★); and frame-inherited invariants over unchanged domains, grouped by which frame supplies preservation:

(i) *content-frame* (`Σ'.C = Σ.C`, no new `dom(C)` entries) — S4, S7a, S7b, C1b, C1c, C-fin, P6, P7;

(ii) *entity-frame* (`Σ'.E = Σ.E`, no new `E` entries) — P8, NodeLineage, ActivatedEmission;

(iii) *document-set frame* (`dom(Σ'.M) = dom(Σ.M)`, no new document registered) — M0 and S7d, both quantified over document tumblers / `dom(M)` rather than over `dom(C)` or `E`.

These are preserved by inheritance, not vacuously: the domains are generally nonempty, but no new instances arise and existing ones are unchanged.

## M-Inv-Bdry — MInvBdry (INV, predicate)

*Composite-boundary properties at `Σ'`.* P4★, P4a, P7a hold at `Σ'` — all preserved because `R' = R`, `dom(Σ'.C) = dom(Σ.C)`, and the new V-arrangement entry is link-subspace (so it does not enter `Contains_C(Σ')`). The three coupling constraints are discharged separately:

- J0 by `dom(Σ'.C) ∖ dom(Σ.C) = ∅` (frame on `C`)
- J1★ by `subspace(v_ℓ) = s_L ≠ s_C` (structural, the new V-position fails J1★'s content-subspace filter)
- J1'★ by `R' ∖ R = ∅` (frame on `R`)

## M-Inv-Trans — MInvTrans (INV, predicate)

*Transition invariants for `Σ → Σ'`.* M1, L12, P0, P1, P2 hold, and P3 (= P0 ∧ P1 ∧ P2 ∧ L12) holds as their conjunction. Each conjunct is discharged trivially by the frames:
```
Σ'.C = Σ.C          [P0: ContentPermanence]
Σ'.E = Σ.E          [P1: EntityPermanence]
Σ'.R = Σ.R          [P2: ProvenancePermanence]
(A ℓ' ∈ dom(Σ.L) :: ℓ' ∈ dom(Σ'.L) ∧ Σ'.L(ℓ') = Σ.L(ℓ'))    [L12: LinkImmutability]
dom(Σ.M) ⊆ dom(Σ'.M)    [M1: ArrangementMonotonicity — holds with equality at MAKELINK]
```
