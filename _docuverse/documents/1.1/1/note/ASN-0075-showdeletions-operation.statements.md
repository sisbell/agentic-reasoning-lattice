# ASN-0075 Claim Statements

*Source: ASN-0075-showdeletions-operation.md (revised 2026-05-25) — Extracted: 2026-06-03*

## CURRENT — Current (DEF, predicate)

```
CURRENT(a, d) ≡ a ∈ ran(M(d))
```

Variables: `a` is a content I-address (`a ∈ dom(C)`, `subspace_I(a) = s_C`); `d ∈ E_doc`.

---

## DELETED — Deleted (DEF, predicate)

```
DELETED(a, d) ≡ (a, d) ∈ R ∧ a ∉ ran(M(d))
```

Variables: `a` is a content I-address; `d ∈ E_doc`; `R ⊆ T_elem × E_doc` is the provenance relation.

---

## NEVER_INCLUDED — NeverIncluded (DEF, predicate)

```
NEVER_INCLUDED(a, d) ≡ (a, d) ∉ R
```

Variables: `a` is a content I-address; `d ∈ E_doc`; `R` is the provenance relation.

---

## D-EXH — ThreeStateExhaustion (LEMMA, lemma)

**Lemma D-EXH (Three-State Exhaustion).** Let `Σ` be a state reachable from `Σ_0` by a finite sequence of valid composite transitions (equivalently, `Σ` is a composite boundary). For every `(a, d)` with `a ∈ dom(Σ.C)`, `subspace_I(a) = s_C`, and `d ∈ Σ.E_doc`, exactly one of `CURRENT(a, d)`, `DELETED(a, d)`, `NEVER_INCLUDED(a, d)` holds.

The three predicates correspond to three of the four cases of the cross-product `(a ∈ ran(M(d))) × ((a, d) ∈ R)`:

| `a ∈ ran(M(d))` | `(a, d) ∈ R` | Predicate |
|---|---|---|
| Yes | Yes | CURRENT |
| Yes | No | impossible |
| No  | Yes | DELETED |
| No  | No  | NEVER_INCLUDED |

The "impossible" row is excluded: from `a ∈ ran(M(d))` and the hypothesis `a ∈ dom(Σ.C)`, L14 gives `a ∉ dom(L)`; by S3★-aux, `subspace(v) ∈ {s_C, s_L}` for the witness `v`; the contrapositive of S3★'s link clause forces `subspace(v) = s_C`; the pair `(a, d)` belongs to `Contains_C(Σ)` by definition; and `Contains_C(Σ) ⊆ R` by P4★.

---

## D-DISCR — DiscriminationRequiresProvenance (LEMMA, lemma)

**Lemma D-DISCR (Discrimination Requires Provenance).** No function computable from `(Σ.C, Σ.L, Σ.E, Σ.M)` alone can distinguish `DELETED(a, d)` from `NEVER_INCLUDED(a, d)` for arbitrary `(a, d)`.

Stronger consequence stated in the ASN: Any system supporting SHOWDELETIONS must maintain state components `C*` beyond `(C, L, E, M)` such that consulting `(C, L, E, M, C*)` at every reachable `Σ` determines whether each `(a, d)` is DELETED or NEVER_INCLUDED. `R` as defined in ASN-0047 is one such `C*`; the necessity claim is that *some* `C*` adequate to discharge this disambiguation must be present, regardless of its specific representation.

Witnesses: Two reachable states `Σ_1`, `Σ_2` with `(Σ_1.C, Σ_1.L, Σ_1.E, Σ_1.M) = (Σ_2.C, Σ_2.L, Σ_2.E, Σ_2.M)` but `DELETED(a, d)` at `Σ_1` and `NEVER_INCLUDED(a, d)` at `Σ_2`. The component agreement is total:

| Component | `Σ_1` | `Σ_2` |
|---|---|---|
| `dom(C)` | `{a}` | `{a}` |
| `C` value at `a` | the K.α-supplied value `v_a` | same |
| `L` | `∅` | `∅` |
| `E` | `{n_0, …, d, d'}` | `{n_0, …, d, d'}` |
| `E_doc` | `{d, d'}` | `{d, d'}` |
| `M(d)` | `∅` | `∅` |
| `M(d')` | `{v' ↦ a}` | `{v' ↦ a}` |

The histories differ only in `R`: `R_1 ⊇ {(a, d), (a, d')}` and `R_2 ⊇ {(a, d')}`, with `(a, d) ∈ R_1 \ R_2`.

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

## SHOWDELETIONS — ShowDeletions (DEF, operation)

**Definition (SHOWDELETIONS).** The operation is the ordered pair:

```
SHOWDELETIONS(d_A, d_B)
   =  (DeletedFromAWithB(d_A, d_B), DeletedFromBWithA(d_A, d_B))
```

Precondition: `d_A ∈ E_doc ∧ d_B ∈ E_doc ∧ Σ is a composite-boundary state`.

Let `q` abbreviate:
```
Result = (DeletedFromAWithB(Σ, d_A, d_B), DeletedFromBWithA(Σ, d_A, d_B))
```

Then `wp(SHOWDELETIONS(d_A, d_B), q) = (d_A ∈ E_doc ∧ d_B ∈ E_doc ∧ Σ is a composite-boundary state)`.

Disjointness (unconditional): membership in `DeletedFromAWithB` requires `CURRENT(a, d_B)` (i.e., `a ∈ ran(M(d_B))`); membership in `DeletedFromBWithA` requires `DELETED(a, d_B)` (i.e., `a ∉ ran(M(d_B))`). These are directly contradictory; no `a` can belong to both halves.

wp for non-emptiness of one half (`Q1 ≡ DeletedFromAWithB(d_A, d_B) ≠ ∅`):
```
wp(SHOWDELETIONS(d_A, d_B), Q1)
   =  d_A ∈ E_doc  ∧  d_B ∈ E_doc
    ∧  Σ is a composite-boundary state
    ∧  (E a ∈ dom(C) :  subspace_I(a) = s_C
                       ∧ (a, d_A) ∈ R
                       ∧ a ∉ ran(M(d_A))
                       ∧ a ∈ ran(M(d_B)))
```

wp for vacuity of both halves (`Q0 ≡ DeletedFromAWithB(d_A, d_B) = ∅ ∧ DeletedFromBWithA(d_A, d_B) = ∅`):
```
wp(SHOWDELETIONS(d_A, d_B), Q0)
   =  d_A ∈ E_doc  ∧  d_B ∈ E_doc
    ∧  Σ is a composite-boundary state
    ∧  (A a ∈ dom(C) :  subspace_I(a) = s_C :
            ¬(DELETED(a, d_A)  ∧  CURRENT(a, d_B))
          ∧ ¬(DELETED(a, d_B)  ∧  CURRENT(a, d_A)))
```

Supplementary lemma (R-disjointness implies Q0): Documents with `{a : (a, d_A) ∈ R} ∩ {a : (a, d_B) ∈ R} = ∅` satisfy `Q0` at any composite-boundary state `Σ`.

---

## D-BOUND — ObservationalBound (AXM, axiom)

**Observational-discipline axiom (D-BOUND).** SHOWDELETIONS is an observational operation invoked between composites: the pre-state `Σ` is a *composite-boundary state* — reachable from `Σ_0` by a finite sequence of valid composite transitions under ValidComposite★ (ASN-0047). This axiom is part of the operation's contract: D-EXH's composite-boundary hypothesis is discharged at every invocation by D-BOUND, not by run-time verification.

---

## D-SUBSP — ContentSubspaceRestriction (CLAIM, claim)

**Claim D-SUBSP.** SHOWDELETIONS operates only over the content subspace (`s_C`).

Formal witness-impossibility for link addresses: Let `ℓ` be a link address with `origin(ℓ) = d_A`, and let `d_B ≠ d_A` be any candidate witness document. Then `ℓ ∉ ran(M(d_B))`. Proof by contradiction: suppose some `v ∈ dom(M(d_B))` has `M(d_B)(v) = ℓ`, and by S3★-aux `subspace(v) ∈ {s_C, s_L}`:

- *Content V-position (`subspace(v) = s_C`)*: S3★ content clause would force `ℓ ∈ dom(C)`; but `ℓ ∈ dom(L)` and L14 (`dom(C) ∩ dom(L) = ∅`) gives `ℓ ∉ dom(C)` — contradiction.
- *Link V-position (`subspace(v) = s_L`)*: CL-OWN forces `origin(M(d_B)(v)) = d_B`; but `origin(ℓ) = d_A ≠ d_B` — contradiction.

Hence `CURRENT(ℓ, d_B)` can never be satisfied across documents for link material.

---

## D-IDENT — IdentityPreservation (CLAIM, claim)

**Claim D-IDENT.** For every `a` in either output set, the returned reference is precisely the I-address `a` — not a copy with new identity.

Consequences:
- *Link survival.* By P3 (ArrangementMutabilityOnly), `L' = L` for every K.μ⁺/K.μ⁻/K.μ~; a link whose endset contains a span anchored at `a` continues to reference the same `a`.
- *Transclusion integrity.* By S2 and the content clause of S3★, `subspace(v) = s_C ⟹ M(d)(v) ∈ dom(C)`. By P0 (ContentPermanence), `dom(C)` and all values are preserved across all transitions; no aliasing or shadow copy is introduced.
- *Origin attribution.* By S7 (StructuralAttribution), `origin(a)` is derivable from `a`'s tumbler alone and is invariant across all states in which `a ∈ dom(C)`.

---

## D-ORIG — OriginTraceability (CLAIM, claim)

**Claim D-ORIG.** For every `a` in either output set, `origin(a)` is determined and identifies a unique document — the originating allocator of `a`.

Formal basis: By S7 (ASN-0036), `origin(a)` is defined for every `a ∈ dom(C)` and is invariant across all states in which `a ∈ dom(C)`. The output sets are subsets of `dom(C)`, so `origin` is well-defined on every output element.

---

## D-ORD — OrderPreservation (CLAIM, claim)

**Claim D-ORD.** If the output is presented as an ordered sequence, the order is consistent with the witness document's V-position ordering of the referenced addresses.

For `DeletedFromAWithB(d_A, d_B)`, define:
```
vpos_B(a) = min{v ∈ dom(M(d_B)) : M(d_B)(v) = a}  under T1
```
The set `{v ∈ dom(M(d_B)) : M(d_B)(v) = a}` is finite (subset of `dom(M(d_B))`, finite by S8-fin) and non-empty when `a ∈ ran(M(d_B))`; the minimum under T1 is a canonical representative. Distinct I-addresses in `DeletedFromAWithB` yield distinct minima (by S2, a single V-position cannot map to two distinct I-addresses; so if `a ≠ a'` then `vpos_B(a) ≠ vpos_B(a')`). Hence `vpos_B` is injective on `DeletedFromAWithB`, and:
```
a < a'  ⟺  vpos_B(a) < vpos_B(a')
```
is a strict total order on `DeletedFromAWithB`. The output is ordered such that for any `a, a'` with `vpos_B(a) < vpos_B(a')` under T1 (ASN-0034), `a` precedes `a'` in the presentation. Symmetrically for `DeletedFromBWithA` using:
```
vpos_A(a) = min{v ∈ dom(M(d_A)) : M(d_A)(v) = a}
```

---

## D-SYM — Symmetry (CLAIM, claim)

**Claim D-SYM.** Argument swap maps each output half into the other:

```
SHOWDELETIONS(d_A, d_B)  =  (X, Y)
SHOWDELETIONS(d_B, d_A)  =  (Y, X)
```

where `X = DeletedFromAWithB(d_A, d_B)` and `Y = DeletedFromBWithA(d_A, d_B)`.

By name-substitution: `DeletedFromAWithB(d_B, d_A)` reads as "addresses with `DELETED(a, d_B) ∧ CURRENT(a, d_A)`," which is exactly `DeletedFromBWithA(d_A, d_B)`. Likewise the other half.

---

## D-ACT — Actionability (CLAIM, claim)

**Claim D-ACT.** The output is in a form usable as input to any operation that consumes I-addresses to produce arrangement extensions.

Each output element is an I-address in `dom(C)`. The output is *not* wrapped in V-position structure; the output is *not* wrapped in content values.

The natural compact form is a set of I-spans as deletion witness runs (see DeletionWitnessRun). From the witness-run collection, the deletion set is recoverable as the union, over each run `(i_start, ℓ, origin)`, of:
```
{i_start, shift(i_start, 1), …, shift(i_start, ℓ − 1)}
```
a set of cardinality `ℓ` determined by the run's components alone via OrdinalShift.

The `ℓ` listed addresses are pairwise distinct: `i_start < shift(i_start, j)` for `j ≥ 1` by TA-strict (StrictIncrease, ASN-0034), and `shift(i_start, j_1) < shift(i_start, j_2)` for `1 ≤ j_1 < j_2 < ℓ` by TS5 (ShiftAmountMonotonicity, ASN-0034).

Note: the witness-run decomposition is applied to each half of the SHOWDELETIONS output independently, never to their union.

---

## D-OBS — ObservationalFrame (CLAIM, claim)

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

Consequence for wp: `wp(SHOWDELETIONS, P) = (precondition) ∧ P(Σ)` whenever `P` depends only on `Σ`.

---

## D-STORE — OutputNotRequired (CLAIM, claim)

**Claim D-STORE.** The output is not required to be stored as a document or otherwise integrated into the persistent content store.

SHOWDELETIONS is observational (D-OBS); its result is delivered to the caller. The system does not, of its own accord, create a new document or other persistent artefact to hold the result.

---

## D-RECONS — StateFunctionalIndependence (CLAIM, claim)

**Claim D-RECONS.** The output depends only on the current state `Σ`. It does not depend on the particular sequence of transitions by which `Σ` was reached.

Each predicate `CURRENT`, `DELETED`, `NEVER_INCLUDED` is defined in terms of components of `Σ` only (`M`, `R`, `dom(C)`, `subspace_I`). The output sets are characterised entirely by these projections. Two distinct transition histories yielding the same `Σ` therefore yield identical SHOWDELETIONS outputs.

---

## Definition — DeletionWitnessRun

A *deletion witness run* is a triple `(i_start, ℓ, origin)` with `ℓ ≥ 1` such that, using OrdinalShift of ASN-0034:

- *Coverage.* Every address in `{i_start, shift(i_start, 1), …, shift(i_start, ℓ − 1)}` (which is `{i_start}` when `ℓ = 1`) belongs to the deletion set.
- *Origin uniformity.* Every such address satisfies `origin(·) = origin`.
- *Right-maximality.* `shift(i_start, ℓ)` is not in the deletion set.
- *Left-maximality.* Either `i_start` is the first emission `[origin.0.s_C.1]` of `A_C(origin)` (which has no predecessor in the allocator's enumeration), or — writing `i_start = [origin.0.s_C.k]` with `k ≥ 2` — the unique predecessor `i_pred = [origin.0.s_C.k − 1]` (equivalently, the address satisfying `shift(i_pred, 1) = i_start`) is not in the deletion set.

The decomposition into maximal witness runs is uniquely determined by the deletion set: the deletion set is finite (subset of `dom(C)`, finite by C-fin, ASN-0047) and totally ordered under T1 (ASN-0034). I-adjacency: two addresses `a, a'` are *I-adjacent* iff (`a' = shift(a, 1)` or `a = shift(a', 1)`) and `origin(a) = origin(a')`. Its reflexive-transitive closure partitions the deletion set into equivalence classes; each class is a maximal T1-contiguous run sharing one origin. Each equivalence class `C` corresponds to a unique witness run `(i_start_C, ℓ_C, origin_C)` where `i_start_C = min(C)` under T1, `ℓ_C = |C|`, and `origin_C` is the shared origin.
