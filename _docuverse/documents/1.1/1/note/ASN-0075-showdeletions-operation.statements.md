# ASN-0075 Claim Statements

*Source: ASN-0075-showdeletions-operation.md (revised 2026-05-25) — Extracted: 2026-05-25*

## CURRENT — Current (DEF, predicate)

```
CURRENT(a, d)  ≡  a ∈ ran(M(d))
```

Variables: `a ∈ dom(C)` with `subspace_I(a) = s_C`, `d ∈ E_doc`.

---

## DELETED — Deleted (DEF, predicate)

```
DELETED(a, d)  ≡  (a, d) ∈ R  ∧  a ∉ ran(M(d))
```

Variables: `a ∈ dom(C)` with `subspace_I(a) = s_C`, `d ∈ E_doc`, `R ⊆ T_elem × E_doc`.

---

## NEVER_INCLUDED — NeverIncluded (DEF, predicate)

```
NEVER_INCLUDED(a, d)  ≡  (a, d) ∉ R
```

Variables: `a ∈ dom(C)` with `subspace_I(a) = s_C`, `d ∈ E_doc`, `R ⊆ T_elem × E_doc`.

---

## D-EXH — ThreeStateExhaustion (LEMMA, lemma)

**Lemma D-EXH (Three-State Exhaustion).** Let `Σ` be a state reachable from `Σ_0` by a finite sequence of valid composite transitions (equivalently, `Σ` is a composite boundary). For every `(a, d)` with `a ∈ dom(Σ.C)`, `subspace_I(a) = s_C`, and `d ∈ Σ.E_doc`, exactly one of `CURRENT(a, d)`, `DELETED(a, d)`, `NEVER_INCLUDED(a, d)` holds.

The cross-product case table:

| `a ∈ ran(M(d))` | `(a, d) ∈ R` | Predicate |
|---|---|---|
| Yes | Yes | CURRENT |
| Yes | No | impossible |
| No  | Yes | DELETED |
| No  | No  | NEVER_INCLUDED |

The "impossible" row is excluded by: from `a ∈ ran(M(d))`, some `v ∈ dom(M(d))` with `M(d)(v) = a`; `a ∈ dom(Σ.C)` and L14 give `a ∉ dom(L)`; S3★-aux gives `subspace(v) ∈ {s_C, s_L}`; contrapositive of S3★'s link clause with `M(d)(v) = a ∉ dom(L)` forces `subspace(v) = s_C`; then `(a, d) ∈ Contains_C(Σ)` by definition, and `Contains_C(Σ) ⊆ R` by P4★ (activated by composite-boundary hypothesis), so `(a, d) ∈ R`.

---

## D-DISCR — DiscriminationRequiresProvenance (LEMMA, lemma)

**Lemma D-DISCR (Discrimination Requires Provenance).** No function computable from `(Σ.C, Σ.L, Σ.E, Σ.M)` alone can distinguish `DELETED(a, d)` from `NEVER_INCLUDED(a, d)` for arbitrary `(a, d)`.

Witness states `Σ_1`, `Σ_2` with identical `(C, L, E, M)` but differing `R`:

| Component | `Σ_1` | `Σ_2` |
|---|---|---|
| `dom(C)` | `{a}` | `{a}` |
| `C` value at `a` | `v_a` | `v_a` |
| `L` | `∅` | `∅` |
| `E` | `{n_0, …, d, d'}` | `{n_0, …, d, d'}` |
| `E_doc` | `{d, d'}` | `{d, d'}` |
| `M(d)` | `∅` | `∅` |
| `M(d')` | `{v' ↦ a}` | `{v' ↦ a}` |

`R_1 ⊇ {(a, d), (a, d')}`, `R_2 ⊇ {(a, d')}`, `(a, d) ∈ R_1 \ R_2`. At `Σ_1`: `DELETED(a, d)`. At `Σ_2`: `NEVER_INCLUDED(a, d)`.

Corollary: any system supporting SHOWDELETIONS must maintain state components `C*` beyond `(C, L, E, M)` such that consulting `(C, L, E, M, C*)` at every reachable `Σ` determines whether each `(a, d)` is `DELETED` or `NEVER_INCLUDED`.

---

## Definition — DeletedFromAWithB

```
DeletedFromAWithB(d_A, d_B)
   =  {a ∈ dom(C) :
         subspace_I(a) = s_C
       ∧ DELETED(a, d_A)
       ∧ CURRENT(a, d_B)}
```

---

## Definition — DeletedFromBWithA

```
DeletedFromBWithA(d_A, d_B)
   =  {a ∈ dom(C) :
         subspace_I(a) = s_C
       ∧ DELETED(a, d_B)
       ∧ CURRENT(a, d_A)}
```

---

## SHOWDELETIONS — ShowDeletions (DEF, function)

**Definition (SHOWDELETIONS).** The operation is the ordered pair:

```
SHOWDELETIONS(d_A, d_B)
   =  (DeletedFromAWithB(d_A, d_B), DeletedFromBWithA(d_A, d_B))
```

Precondition: `d_A ∈ E_doc ∧ d_B ∈ E_doc ∧ Σ is a composite-boundary state`.

Postcondition (wp form): let `q` abbreviate

```
Result = (DeletedFromAWithB(Σ, d_A, d_B), DeletedFromBWithA(Σ, d_A, d_B))
```

Then `wp(SHOWDELETIONS(d_A, d_B), q) = (d_A ∈ E_doc ∧ d_B ∈ E_doc ∧ Σ is a composite-boundary state)`.

The two halves are necessarily disjoint: no `a` can simultaneously satisfy `DELETED(a, d_A)` and `CURRENT(a, d_A)` (by D-EXH), so an address `a` in `DeletedFromAWithB` cannot be in `DeletedFromBWithA` (the former requires `CURRENT(a, d_B)`, the latter requires `DELETED(a, d_B)`).

Derived wp for non-emptiness of one half (`Q1`: `DeletedFromAWithB(d_A, d_B) ≠ ∅`):

```
wp(SHOWDELETIONS(d_A, d_B), Q1)
   =  d_A ∈ E_doc  ∧  d_B ∈ E_doc
    ∧  Σ is a composite-boundary state
    ∧  (E a ∈ dom(C) :  subspace_I(a) = s_C
                       ∧ (a, d_A) ∈ R
                       ∧ a ∉ ran(M(d_A))
                       ∧ a ∈ ran(M(d_B)))
```

Derived wp for vacuity of both halves (`Q0`: `DeletedFromAWithB(d_A, d_B) = ∅ ∧ DeletedFromBWithA(d_A, d_B) = ∅`):

```
wp(SHOWDELETIONS(d_A, d_B), Q0)
   =  d_A ∈ E_doc  ∧  d_B ∈ E_doc
    ∧  Σ is a composite-boundary state
    ∧  (A a ∈ dom(C) :  subspace_I(a) = s_C :
            ¬(DELETED(a, d_A)  ∧  CURRENT(a, d_B))
          ∧ ¬(DELETED(a, d_B)  ∧  CURRENT(a, d_A)))
```

---

## D-BOUND — BoundaryInvocation (AX, axiom)

**Observational-discipline axiom (D-BOUND).** SHOWDELETIONS is an observational operation invoked between composites: the pre-state `Σ` is a *composite-boundary state* — reachable from `Σ_0` by a finite sequence of valid composite transitions under ValidComposite★ (ASN-0047). The axiom is part of the operation's contract: D-EXH's composite-boundary hypothesis is discharged at every invocation by D-BOUND.

Supplementary lemma (R-disjointness implies Q0 at composite-boundary states): documents with disjoint `R`-projections on the content subspace —

```
{a : (a, d_A) ∈ R} ∩ {a : (a, d_B) ∈ R} = ∅
```

— satisfy `Q0` at any composite-boundary state `Σ`.

---

## D-SUBSP — ContentSubspaceRestriction (CLM, claim)

**Claim D-SUBSP.** SHOWDELETIONS operates only over the content subspace (`s_C`).

The condition `subspace_I(a) = s_C` is required throughout. By CL-OWN (ASN-0047): if `subspace(v) = s_L` and `M(d)(v) = a`, then `origin(a) = d`. Cross-document deletion comparison of link-subspace material is not well-formed.

---

## D-IDENT — IdentityPreservation (CLM, claim)

**Claim D-IDENT.** For every `a` in either output set, the returned reference is precisely the I-address `a` — not a copy with new identity.

The output sets are defined as subsets of `dom(C)`. Each element is an existing I-address. The operation returns addresses, not values. Three structural guarantees that depend on persistent I-address identity survive recovery:

- *Link survival.* By L3 (NEndsetStructure, ASN-0047) and P3 (ArrangementMutabilityOnly, ASN-0047): `L' = L` for every K.μ⁺/K.μ⁻/K.μ~; any link whose endset contains a span anchored at `a` continues to reference the same `a`.
- *Transclusion integrity.* By S2 (ASN-0036) and content clause of S3★ (ASN-0047): `subspace(v) = s_C ⟹ M(d)(v) ∈ dom(C)`; P0 (ContentPermanence, ASN-0047) preserves both `dom(C)` and the value at every existing entry across all transitions.
- *Origin attribution.* By S7 (ASN-0036): `origin(a)` is derivable from `a`'s tumbler alone and is invariant across all states in which `a ∈ dom(C)`.

---

## D-ORIG — OriginTraceability (CLM, claim)

**Claim D-ORIG.** For every `a` in either output set, `origin(a)` is determined and identifies a unique document — the originating allocator of `a`.

By S7 (ASN-0036): `origin(a)` is defined for every `a ∈ dom(C)` and is invariant across all states in which `a ∈ dom(C)`. The output sets are subsets of `dom(C)`, so `origin` is well-defined on every output element.

---

## D-ORD — OrderPreservation (CLM, claim)

**Claim D-ORD.** If the output is presented as an ordered sequence, the order is consistent with the witness document's V-position ordering of the referenced addresses.

For `DeletedFromAWithB(d_A, d_B)`, define:

```
vpos_B(a) = min{v ∈ dom(M(d_B)) : M(d_B)(v) = a}  under T1
```

The minimum exists: `{v ∈ dom(M(d_B)) : M(d_B)(v) = a}` is finite (subset of `dom(M(d_B))`, finite by S8-fin) and non-empty when `a ∈ ran(M(d_B))`. `vpos_B` is injective on `DeletedFromAWithB`: by S2, `v` cannot map to two distinct I-addresses, so `a ≠ a' ⟹ vpos_B(a) ≠ vpos_B(a')`. The induced relation `a < a' ⟺ vpos_B(a) < vpos_B(a')` is a strict total order on `DeletedFromAWithB`.

The output is ordered such that for any `a, a'` with `vpos_B(a) < vpos_B(a')` under T1 (ASN-0034), `a` precedes `a'` in the presentation.

Symmetrically for `DeletedFromBWithA` using:

```
vpos_A(a) = min{v ∈ dom(M(d_A)) : M(d_A)(v) = a}  under T1
```

---

## D-SYM — Symmetry (CLM, claim)

**Claim D-SYM.** Argument swap maps each output half into the other:

```
SHOWDELETIONS(d_A, d_B)  =  (X, Y)
SHOWDELETIONS(d_B, d_A)  =  (Y, X)
```

where `X = DeletedFromAWithB(d_A, d_B)` and `Y = DeletedFromBWithA(d_A, d_B)`.

By name-substitution: `DeletedFromAWithB(d_B, d_A)` = `{a : DELETED(a, d_B) ∧ CURRENT(a, d_A)}` = `DeletedFromBWithA(d_A, d_B)`, and `DeletedFromBWithA(d_B, d_A)` = `DeletedFromAWithB(d_A, d_B)`.

---

## D-ACT — Actionability (CLM, claim)

**Claim D-ACT.** The output is in a form usable as input to any operation that consumes I-addresses to produce arrangement extensions.

Each output element is an I-address in `dom(C)`. The natural compact form is a set of I-spans grouped into deletion witness runs. The deletion set (either `DeletedFromAWithB` or `DeletedFromBWithA` individually — never their union) decomposes uniquely into a finite collection of deletion witness runs (defined in DeletionWitnessRun below). The deletion set is recoverable from the run collection as:

```
⋃_{(i_start, ℓ, origin)} {i_start, shift(i_start, 1), …, shift(i_start, ℓ − 1)}
```

---

## D-OBS — ObservationalFrame (CLM, claim)

**Claim D-OBS.** SHOWDELETIONS does not modify any state component.

Formally, for state `Σ = (C, L, E, M, R)` and the state `Σ'` obtaining after the operation:

```
Σ'.C  =  Σ.C
Σ'.L  =  Σ.L
Σ'.E  =  Σ.E
Σ'.R  =  Σ.R
(A d ∈ E_doc ::  Σ'.M(d) = Σ.M(d))
```

The operation reads `M(d_A)`, `M(d_B)`, and `R`; it computes the output sets; it returns them. No transition relation is invoked.

For any predicate `P` depending only on `Σ`: `wp(SHOWDELETIONS, P) = (precondition) ∧ P(Σ)`.

---

## D-STORE — OutputNotStored (CLM, claim)

**Claim D-STORE.** The output is not required to be stored as a document or otherwise integrated into the persistent content store.

SHOWDELETIONS is observational (D-OBS); its result is delivered to the caller. The system does not create a new document or other persistent artefact to hold the result.

---

## D-RECONS — StateFunctionalIndependence (CLM, claim)

**Claim D-RECONS.** The output depends only on the current state `Σ`. It does not depend on the particular sequence of transitions by which `Σ` was reached.

Each predicate `CURRENT`, `DELETED`, `NEVER_INCLUDED` is defined in terms of components of `Σ` only (`M`, `R`, `dom(C)`, `subspace_I`). Two distinct transition histories yielding the same `Σ` yield identical SHOWDELETIONS outputs.

---

## Definition — DeletionWitnessRun

A *deletion witness run* is a triple `(i_start, ℓ, origin)` with `ℓ ≥ 1` such that, using OrdinalShift (ASN-0034):

- *Coverage.* Every address in `{i_start, shift(i_start, 1), …, shift(i_start, ℓ − 1)}` (which is `{i_start}` when `ℓ = 1`) belongs to the deletion set;
- *Origin uniformity.* Every such address satisfies `origin(·) = origin`;
- *Right-maximality.* `shift(i_start, ℓ)` is not in the deletion set;
- *Left-maximality.* Either `i_start` is the first emission `[origin.0.s_C.1]` of `A_C(origin)` (which has no predecessor in the allocator's enumeration), or — writing `i_start = [origin.0.s_C.k]` with `k ≥ 2` — the unique predecessor `i_pred = [origin.0.s_C.k − 1]` (equivalently, the address satisfying `shift(i_pred, 1) = i_start`) is not in the deletion set.

The *deletion set* refers to either `DeletedFromAWithB(d_A, d_B)` or `DeletedFromBWithA(d_A, d_B)` individually; the decomposition is applied to each half independently, never to their union.

The decomposition into maximal witness runs is uniquely determined. The deletion set is finite (subset of `dom(C)`, finite by C-fin, ASN-0047) and totally ordered under T1 (ASN-0034). I-adjacency on the deletion set: `a, a'` are *I-adjacent* iff (`a' = shift(a, 1)` or `a = shift(a', 1)`) and `origin(a) = origin(a')`. The reflexive-transitive closure of I-adjacency is an equivalence relation partitioning the deletion set into maximal contiguous same-origin runs. Each equivalence class `C` corresponds to a unique witness run `(min(C), |C|, origin_C)` where `min(C)` is the T1-minimum of `C` and `origin_C` is the shared origin.
