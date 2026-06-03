# ASN-0075 Claim Statements

*Source: ASN-0075-showdeletions-operation.md (revised 2026-05-25) — Extracted: 2026-06-03*

## CURRENT — CurrentAddress (DEF, predicate)

```
CURRENT(a, d) ≡ a ∈ ran(M(d))
```

Variables: `a ∈ dom(C)` with `subspace_I(a) = s_C`; `d ∈ E_doc`.

---

## DELETED — DeletedAddress (DEF, predicate)

```
DELETED(a, d) ≡ (a, d) ∈ R ∧ a ∉ ran(M(d))
```

Variables: `a ∈ dom(C)` with `subspace_I(a) = s_C`; `d ∈ E_doc`; `R ⊆ T_elem × E_doc` is the provenance relation.

---

## NEVER_INCLUDED — NeverIncludedAddress (DEF, predicate)

```
NEVER_INCLUDED(a, d) ≡ (a, d) ∉ R
```

Variables: `a ∈ dom(C)` with `subspace_I(a) = s_C`; `d ∈ E_doc`.

---

## Definition — DeletedFromAWithB

```
DeletedFromAWithB(d_A, d_B)
   =  {a ∈ dom(C) :
         subspace_I(a) = s_C
       ∧ DELETED(a, d_A)
       ∧ CURRENT(a, d_B)}
```

Precondition: `d_A ∈ E_doc ∧ d_B ∈ E_doc`.

---

## Definition — DeletedFromBWithA

```
DeletedFromBWithA(d_A, d_B)
   =  {a ∈ dom(C) :
         subspace_I(a) = s_C
       ∧ DELETED(a, d_B)
       ∧ CURRENT(a, d_A)}
```

Precondition: `d_A ∈ E_doc ∧ d_B ∈ E_doc`. Symmetric counterpart of DeletedFromAWithB.

---

## Definition — ShowDeletions

```
SHOWDELETIONS(d_A, d_B)
   =  (DeletedFromAWithB(d_A, d_B), DeletedFromBWithA(d_A, d_B))
```

Precondition: `d_A ∈ E_doc ∧ d_B ∈ E_doc ∧ Σ is a composite-boundary state`.

wp form:
```
wp(SHOWDELETIONS(d_A, d_B), q) = (d_A ∈ E_doc ∧ d_B ∈ E_doc ∧ Σ is a composite-boundary state)
```

where `q` abbreviates `Result = (DeletedFromAWithB(Σ, d_A, d_B), DeletedFromBWithA(Σ, d_A, d_B))`.

The two halves are disjoint: membership in `DeletedFromAWithB` requires `CURRENT(a, d_B)` (i.e. `a ∈ ran(M(d_B))`); membership in `DeletedFromBWithA` requires `DELETED(a, d_B)` whose second conjunct is `a ∉ ran(M(d_B))`. These are directly contradictory, so no `a` belongs to both halves.

---

## D-EXH — ThreeStateExhaustion (LEMMA, lemma)

**Lemma D-EXH (Three-State Exhaustion).** Let `Σ` be a state reachable from `Σ_0` by a finite sequence of valid composite transitions (equivalently, `Σ` is a composite boundary). For every `(a, d)` with `a ∈ dom(Σ.C)`, `subspace_I(a) = s_C`, and `d ∈ Σ.E_doc`, exactly one of `CURRENT(a, d)`, `DELETED(a, d)`, `NEVER_INCLUDED(a, d)` holds.

The four cases of the cross-product `(a ∈ ran(M(d))) × ((a, d) ∈ R)`:

| `a ∈ ran(M(d))` | `(a, d) ∈ R` | Predicate |
|---|---|---|
| Yes | Yes | CURRENT |
| Yes | No | impossible |
| No  | Yes | DELETED |
| No  | No  | NEVER_INCLUDED |

The impossible row is excluded: from `a ∈ ran(M(d))`, L14 (`dom(C) ∩ dom(L) = ∅`) gives `a ∉ dom(L)`; S3★-aux gives `subspace(v) ∈ {s_C, s_L}`; contrapositive of S3★'s link clause with `M(d)(v) = a ∉ dom(L)` forces `subspace(v) = s_C`; the witness `v` places `(a, d) ∈ Contains_C(Σ)`; and `Contains_C(Σ) ⊆ R` by P4★ (activated by the composite-boundary hypothesis).

---

## D-DISCR — DiscriminationRequiresProvenance (LEMMA, lemma)

**Lemma D-DISCR (Discrimination Requires Provenance).** No function computable from `(Σ.C, Σ.L, Σ.E, Σ.M)` alone can distinguish `DELETED(a, d)` from `NEVER_INCLUDED(a, d)` for arbitrary `(a, d)`.

Witnesses `Σ_1` and `Σ_2`:

*History 1 (yields DELETED):*
```
Σ_0  →* K.δ(d)
     →* K.δ(d')
     →* K.α(a, d);   K.μ⁺(d,  v  ↦ a);  K.ρ(a, d)
     →* K.μ⁺(d', v' ↦ a);  K.ρ(a, d')
     →* K.μ⁻(d)              [retain n'_{s_C} = 0]
     =   Σ_1
```

Final state: `dom(C_1) = {a}`, `M_1(d) = ∅`, `M_1(d') = {v' ↦ a}`, `(a, d) ∈ R_1`. So `DELETED(a, d)` holds at `Σ_1`.

*History 2 (yields NEVER_INCLUDED):*
```
Σ_0  →* K.δ(d)
     →* K.δ(d')
     →* K.α(a, d);   K.μ⁺(d', v' ↦ a);  K.ρ(a, d')
     =   Σ_2
```

Final state: `dom(C_2) = {a}`, `M_2(d) = ∅`, `M_2(d') = {v' ↦ a}`, `(a, d) ∉ R_2`. So `NEVER_INCLUDED(a, d)` holds at `Σ_2`.

Agreement on `(C, L, E, M)`:

| Component | `Σ_1` | `Σ_2` |
|---|---|---|
| `dom(C)` | `{a}` | `{a}` |
| `C` value at `a` | `v_a` | `v_a` |
| `L` | `∅` | `∅` |
| `E` | `{n_0, …, d, d'}` | `{n_0, …, d, d'}` |
| `E_doc` | `{d, d'}` | `{d, d'}` |
| `M(d)` | `∅` | `∅` |
| `M(d')` | `{v' ↦ a}` | `{v' ↦ a}` |

`(Σ_1.C, Σ_1.L, Σ_1.E, Σ_1.M) = (Σ_2.C, Σ_2.L, Σ_2.E, Σ_2.M)`. Any function `f(C, L, E, M)` returns the same value at both states, yet classifications differ.

Consequence: any system supporting SHOWDELETIONS must maintain state components `C*` beyond `(C, L, E, M)` such that consulting `(C, L, E, M, C*)` at every reachable `Σ` determines whether each `(a, d)` is `DELETED` or `NEVER_INCLUDED`.

---

## D-BOUND — ShowDeletionsBoundaryAxiom (AXIOM, axiom)

**Observational-discipline axiom (D-BOUND).** SHOWDELETIONS is an observational operation invoked between composites: the pre-state `Σ` is a *composite-boundary state* — reachable from `Σ_0` by a finite sequence of valid composite transitions under ValidComposite★ (ASN-0047). This is part of the operation's contract; D-EXH's composite-boundary hypothesis is discharged at every invocation by D-BOUND, not by run-time verification.

---

## D-SUBSP — ContentSubspaceRestriction (CLAIM, lemma)

**Claim D-SUBSP.** SHOWDELETIONS operates only over the content subspace (`s_C`).

Formal witness-impossibility: Let `ℓ` be a link address with `origin(ℓ) = d_A`, and let `d_B ≠ d_A`. Then `ℓ ∉ ran(M(d_B))`.

*Proof structure.* Suppose `ℓ ∈ ran(M(d_B))`: some `v ∈ dom(M(d_B))` has `M(d_B)(v) = ℓ`, and by S3★-aux `subspace(v) ∈ {s_C, s_L}`. Both are excluded:

- *`subspace(v) = s_C`:* S3★ content clause forces `M(d_B)(v) = ℓ ∈ dom(C)`. But `ℓ ∈ dom(L)` and L14 gives `ℓ ∉ dom(C)` — contradiction.
- *`subspace(v) = s_L`:* CL-OWN forces `origin(M(d_B)(v)) = d_B`. But `origin(ℓ) = d_A ≠ d_B` — contradiction.

Therefore `CURRENT(ℓ, d_B)` can never be satisfied across documents for link material, so the witness condition SHOWDELETIONS requires cannot hold for link-subspace addresses.

---

## D-IDENT — IdentityPreservation (CLAIM, lemma)

**Claim D-IDENT.** For every `a` in either output set, the returned reference is precisely the I-address `a` — not a copy with new identity.

- Output sets are defined as subsets of `dom(C)`. Each element is an existing I-address.
- *Link survival:* By P3, `L` is preserved across all transitions, so every link referencing `a` by any endset span `σ` with `start(σ) ≤ a < reach(σ)` continues to reference the same `a`.
- *Transclusion integrity:* By S2, S3★ content clause, and P0, arrangements reference I-addresses by tumbler identity; no aliasing or shadow copy is introduced.
- *Origin attribution:* By S7, `origin(a)` is derivable from `a`'s tumbler alone and is invariant across all states in which `a ∈ dom(C)`.

---

## D-ORIG — OriginTraceability (CLAIM, lemma)

**Claim D-ORIG.** For every `a` in either output set, `origin(a)` is determined and identifies a unique document — the originating allocator of `a`.

- By S7, `origin(a)` is defined for every `a ∈ dom(C)` and is invariant across all states in which `a ∈ dom(C)`.
- The output sets are subsets of `dom(C)`, so `origin` is well-defined on every output element.

---

## D-ORD — OrderInheritance (CLAIM, lemma)

**Claim D-ORD.** Each output half is a finite subset of `dom(C) ⊆ T`, and therefore inherits the total order T1 (ASN-0034) imposes on tumblers. No separate ordering structure is needed: the addresses are self-ordering, and any presentation may list them in T1 order.

- The output sets are subsets of `dom(C)`, finite by C-fin (ASN-0047).
- T1 is a strict total order on `T`; its restriction to a finite subset is again a total order.

---

## D-SYM — ArgumentSwapSymmetry (CLAIM, lemma)

**Claim D-SYM.** Argument swap maps each output half into the other:

```
SHOWDELETIONS(d_A, d_B)  =  (X, Y)
SHOWDELETIONS(d_B, d_A)  =  (Y, X)
```

where `X = DeletedFromAWithB(d_A, d_B)` and `Y = DeletedFromBWithA(d_A, d_B)`.

By name-substitution: `DeletedFromAWithB(d_B, d_A)` = `{a : DELETED(a, d_B) ∧ CURRENT(a, d_A)}` = `DeletedFromBWithA(d_A, d_B)`. Likewise the other half.

---

## D-ACT — ActionabilityOfOutput (CLAIM, lemma)

**Claim D-ACT.** The output is in a form usable as input to any operation that consumes I-addresses to produce arrangement extensions.

- Each output element is an I-address in `dom(C)`, carrying determinate origin (D-ORIG) and preserved identity (D-IDENT).
- The output is not wrapped in V-position structure.
- The output is not wrapped in content values.
- Any packaging as spans is a representation choice, not part of the operation's contract.

---

## D-OBS — ObservationalFrame (CLAIM, lemma)

**Claim D-OBS.** SHOWDELETIONS does not modify any state component.

For state `Σ = (C, L, E, M, R)` and the state `Σ'` obtaining after the operation:

```
Σ'.C  =  Σ.C
Σ'.L  =  Σ.L
Σ'.E  =  Σ.E
Σ'.R  =  Σ.R
(∀ d ∈ E_doc ::  Σ'.M(d) = Σ.M(d))
```

---

## D-STORE — NoStorageRequirement (CLAIM, lemma)

**Claim D-STORE.** The output is not required to be stored as a document; it is a query result. The system creates no persistent artefact of its own accord.

Because the operation is observational (D-OBS), its result is merely delivered to the caller and is not stored as a document or otherwise integrated into the persistent store.

---

## D-RECONS — StateFunctionalIndependence (CLAIM, lemma)

**Claim D-RECONS.** The output depends only on the current state `Σ`. It does not depend on the particular sequence of transitions by which `Σ` was reached.

- Each predicate `CURRENT`, `DELETED`, `NEVER_INCLUDED` is defined in terms of components of `Σ` only: `M`, `R`, `dom(C)`, `subspace_I`.
- Two distinct transition histories yielding the same `Σ` yield identical SHOWDELETIONS outputs.
