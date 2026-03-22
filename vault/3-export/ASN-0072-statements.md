# ASN-0072 Formal Statements

*Source: ASN-0072-state-transitions-0.md (revised 2026-03-22) — Extracted: 2026-03-22*

## Definition — Endset

`Endset = 𝒫_fin(Span)`, where `Span` is the set of well-formed span pairs `(s, ℓ)` satisfying T12 (ASN-0034). The empty set ∅ is a valid endset.

## Definition — LinkValue

A *link value* is a triple `(F, G, Θ)` where `F, G, Θ ∈ Endset` — the *from-endset*, *to-endset*, and *type-endset* respectively.

## Definition — SubspaceIdentifiers

`s_C` is the content subspace identifier; `s_L` is the link subspace identifier.

- `fields(a).E₁ = s_C` for content addresses `a`
- `fields(ℓ).E₁ = s_L` for link addresses `ℓ`
- `subspace(v) = v₁` for V-positions

---

## L0 — SubspacePartition (INV, predicate)

```
(A a ∈ dom(Σ.L) :: fields(a).E₁ = s_L)
(A a ∈ dom(Σ.C) :: fields(a).E₁ = s_C)
```

## L1 — LinkElementLevel (INV, predicate)

```
(A a ∈ dom(Σ.L) :: zeros(a) = 3)
```

## L1a — LinkScopedAllocation (INV, predicate)

```
(A a ∈ dom(Σ.L) :: origin(a) ∈ E_doc)
```

## L3 — TripleEndsetStructure (INV, predicate)

```
(A a ∈ dom(Σ.L) :: Σ.L(a) = (F, G, Θ) where F, G, Θ ∈ Endset)
```

## L12 — LinkImmutability (INV, predicate)

```
(A Σ → Σ' : (A a : a ∈ dom(Σ.L) : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)))
```

## L14 — StoreDisjointness (INV, predicate)

```
dom(Σ.C) ∩ dom(Σ.L) = ∅
```

---

## SC-NEQ — SubspaceDistinctness (AX, axiom)

```
s_C ≠ s_L
```

## K.α amendment — ContentSubspaceRestriction (TRANS, amended)

*Additional precondition on allocated address:*

```
fields(a).E₁ = s_C
```

*Additional postcondition:* M'(d) satisfies D-CTG and D-MIN for each subspace.

## K.μ⁺ amendment — ContentSubspaceRestriction (TRANS, amended)

*Additional precondition on new V-positions:*

```
subspace(v) = s_C
```

*Additional postcondition:* M'(d) satisfies D-CTG and D-MIN for each subspace.

## K.μ⁻ amendment — PerSubspaceContiguity (TRANS, amended)

*Additional postcondition:* M'(d) satisfies D-CTG and D-MIN for each subspace. Contraction is constrained to removal from the maximum end of V_S(d) or removal of all positions in V_S(d). By D-SEQ at the input state, for each non-empty subspace S, V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}; the result must be {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'} for some 0 ≤ n' ≤ n.

## K.λ — LinkAllocation (TRANS, definition)

*Precondition:*
- `d ∈ E_doc`
- `ℓ ∉ dom(L) ∪ dom(C)`
- `zeros(ℓ) = 3 ∧ fields(ℓ).E₁ = s_L`
- `origin(ℓ) = d`
- `(A ℓ' : ℓ' ∈ dom(L) ∧ origin(ℓ') = d : ℓ' < ℓ)`
- `(F, G, Θ) ∈ Link`

*Effect:*
```
L' = L ∪ {ℓ ↦ (F, G, Θ)}
```

*Frame:*
```
C' = C; E' = E; (A d' :: M'(d') = M(d')); R' = R
```

## K.μ⁺_L — LinkSubspaceExtension (TRANS, definition)

*Precondition:*
- `d ∈ E_doc`
- `ℓ ∈ dom(L)`
- `origin(ℓ) = d`
- `subspace(v_ℓ) = s_L`
- `m_L ≥ 2`, where: if `V_{s_L}(d) ≠ ∅`, `m_L` is the common depth of existing link-subspace V-positions; if `V_{s_L}(d) = ∅`, `m_L` is a parameter of the transition subject only to `m_L ≥ 2`
- If `V_{s_L}(d) = ∅`: `v_ℓ` is the minimum position `[s_L, 1, ..., 1]` of depth `m_L` (D-MIN)
- If `V_{s_L}(d) ≠ ∅`: `v_ℓ = shift(max(V_{s_L}(d)), 1)` (D-CTG)
- `#v_ℓ = m_L`

*Effect:*
```
M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}
```

*Frame:*
```
C' = C; L' = L; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R
```

## S3★ — GeneralizedReferentialIntegrity (INV, predicate)

```
(A d, v : v ∈ dom(Σ.M(d)) :
  (subspace(v) = s_C ⟹ Σ.M(d)(v) ∈ dom(Σ.C)) ∧
  (subspace(v) = s_L ⟹ Σ.M(d)(v) ∈ dom(Σ.L)))
```

## S3★-aux — SubspaceExhaustiveness (INV, predicate)

```
(A d, v : v ∈ dom(M(d)) : subspace(v) = s_C ∨ subspace(v) = s_L)
```

## Definition — ContentContainment

```
Contains_C(Σ) = {(a, d) : d ∈ E_doc ∧ (E v : v ∈ dom(M(d)) ∧ subspace(v) = s_C : M(d)(v) = a)}
```

## P4★ — ProvenanceBoundsContent (INV, predicate)

```
Contains_C(Σ) ⊆ R
```

## J1★ — ExtensionRecordsProvenance (AX, predicate)

```
(A Σ → Σ', d, v, a :
  v ∈ dom(M'(d)) \ dom(M(d)) ∧ subspace(v) = s_C ∧ M'(d)(v) = a :
  (a, d) ∈ R')
```

## J1'★ — ProvenanceRequiresExtension (AX, predicate)

```
(A Σ → Σ', a, d :
  (a, d) ∈ R' \ R :
  (E v : v ∈ dom(M'(d)) \ dom(M(d)) ∧ subspace(v) = s_C : M'(d)(v) = a))
```

## ValidComposite★ — ValidCompositeExtended (DEF, predicate)

A composite transition `Σ → Σ'` in the extended state `Σ = (C, L, E, M, R)` is *valid* iff it is a finite sequence of elementary transitions `Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ'` — drawn from K.α (amended), K.δ, K.λ, K.μ⁺ (amended), K.μ⁺_L, K.μ⁻ (amended), K.μ~, and K.ρ — satisfying:

1. *Elementary preconditions:* each step `Σᵢ → Σᵢ₊₁` satisfies the precondition of its elementary transition kind, evaluated at `Σᵢ`.
2. *Coupling constraints:* J0, J1★, and J1'★ hold for the composite — evaluated between `Σ` and `Σ'`.

## P3★ — ArrangementMutabilityOnly (INV, predicate)

```
(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ dom(L) ⊆ dom(L') ∧ E ⊆ E' ∧ R ⊆ R')
```

## P5★ — DestructionConfinement (INV, predicate)

```
(a) dom(C') ⊇ dom(C) ∧ (A a : a ∈ dom(C) : C'(a) = C(a))
(b) dom(L') ⊇ dom(L) ∧ (A ℓ : ℓ ∈ dom(L) : L'(ℓ) = L(ℓ))
(c) E' ⊇ E
(d) R' ⊇ R
```

## CL-OWN — LinkSubspaceOwnership (INV, predicate)

```
(A d, v : v ∈ dom(M(d)) ∧ subspace(v) = s_L : origin(M(d)(v)) = d)
```

## ExtendedReachableStateInvariants — ExtendedReachableStateInvariants (THEOREM, theorem)

Every state reachable from `Σ₀ = (C₀, L₀, E₀, M₀, R₀)` by a finite sequence of valid composite transitions — composed from K.α, K.δ, K.λ, K.μ⁺ (amended), K.μ⁺_L, K.μ⁻, K.μ~, and K.ρ — satisfies:

```
S0 ∧ S1 ∧ S2 ∧ S3★ ∧ S3★-aux ∧ S8a ∧ S8-fin ∧ S8-depth ∧ S8 ∧
D-CTG ∧ D-MIN ∧
P0 ∧ P1 ∧ P2 ∧ P3★ ∧ P4★ ∧ P5★ ∧ P6 ∧ P7 ∧ P7a ∧ P8 ∧
L0 ∧ L1 ∧ L1a ∧ L3 ∧ L12 ∧ L14 ∧ CL-OWN
```

*Proof structure.* By induction on the number of valid composite transitions from Σ₀.

**Base.** `Σ₀` satisfies all invariants: `L₀ = ∅` satisfies link invariants vacuously; S3★ and P4★ reduce to S3 and P4; S3★-aux holds vacuously since `M₀(d) = ∅` for all d; D-CTG and D-MIN hold vacuously since `V_S(d) = ∅` for every subspace S.

**Class (a) — Elementary invariants** (all except P4★ and P7a): preserved by each elementary transition individually.

**Class (b) — Composite invariants** (P4★ and P7a): may be violated at intermediate states; hold at every valid composite boundary by J1★ (for P4★) and J0 + J1★ (for P7a). ∎
