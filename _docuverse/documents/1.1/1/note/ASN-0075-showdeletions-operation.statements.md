# ASN-0075 Claim Statements

*Source: ASN-0075-showdeletions-operation.md (revised 2026-05-25) — Extracted: 2026-06-03*

## CURRENT — Current (DEF, predicate)

```
CURRENT(a, d)  ≡  a ∈ ran(M(d))
```

Where `a ∈ dom(C)`, `subspace_I(a) = s_C`, `d ∈ E_doc`.

---

## DELETED — Deleted (DEF, predicate)

```
DELETED(a, d)  ≡  (a, d) ∈ R  ∧  a ∉ ran(M(d))
```

Where `a ∈ dom(C)`, `subspace_I(a) = s_C`, `d ∈ E_doc`.

---

## NEVER_INCLUDED — NeverIncluded (DEF, predicate)

```
NEVER_INCLUDED(a, d)  ≡  (a, d) ∉ R
```

Where `a ∈ dom(C)`, `subspace_I(a) = s_C`, `d ∈ E_doc`.

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

## Definition — ShowDeletions

```
SHOWDELETIONS(d_A, d_B)
   =  (DeletedFromAWithB(d_A, d_B), DeletedFromBWithA(d_A, d_B))
```

Precondition: `d_A ∈ E_doc ∧ d_B ∈ E_doc ∧ Σ is a composite-boundary state`

Postcondition (wp form), letting `q` abbreviate:
```
Result = (DeletedFromAWithB(Σ, d_A, d_B), DeletedFromBWithA(Σ, d_A, d_B))
```
then `wp(SHOWDELETIONS(d_A, d_B), q) = (d_A ∈ E_doc ∧ d_B ∈ E_doc ∧ Σ is a composite-boundary state)`

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

The impossible row is excluded by: from `a ∈ ran(M(d))` and `a ∈ dom(Σ.C)`, L14 gives `a ∉ dom(L)`; by S3★-aux, `subspace(v) ∈ {s_C, s_L}`; the contrapositive of S3★'s link clause forces `subspace(v) = s_C`; so `(a, d) ∈ Contains_C(Σ)` and `Contains_C(Σ) ⊆ R` by P4★, contradicting `(a, d) ∉ R`.

---

## D-DISCR — DiscriminationRequiresProvenance (LEMMA, lemma)

**Lemma D-DISCR (Discrimination Requires Provenance).** No function computable from `(Σ.C, Σ.L, Σ.E, Σ.M)` alone can distinguish `DELETED(a, d)` from `NEVER_INCLUDED(a, d)` for arbitrary `(a, d)`.

Equivalently: any system supporting SHOWDELETIONS must maintain state components `C*` beyond `(C, L, E, M)` such that consulting `(C, L, E, M, C*)` at every reachable `Σ` determines whether each `(a, d)` is `DELETED` or `NEVER_INCLUDED`.

Witnesses: two reachable states `Σ_1` and `Σ_2` with `(Σ_1.C, Σ_1.L, Σ_1.E, Σ_1.M) = (Σ_2.C, Σ_2.L, Σ_2.E, Σ_2.M)` on every component, but `DELETED(a, d)` holds at `Σ_1` and `NEVER_INCLUDED(a, d)` holds at `Σ_2`. The states differ only in `R`: `R_1 ⊇ {(a, d), (a, d')}` and `R_2 ⊇ {(a, d')}`, with `(a, d) ∈ R_1 \ R_2`.

---

## DeletedFromAWithB — DeletedFromAWithB (DEF, function)

```
{a ∈ dom(C) : subspace_I(a) = s_C ∧ DELETED(a, d_A) ∧ CURRENT(a, d_B)}
```

(See Definition above.)

---

## DeletedFromBWithA — DeletedFromBWithA (DEF, function)

Symmetric counterpart of DeletedFromAWithB:

```
{a ∈ dom(C) : subspace_I(a) = s_C ∧ DELETED(a, d_B) ∧ CURRENT(a, d_A)}
```

---

## SHOWDELETIONS — ShowDeletions (DEF, function)

```
SHOWDELETIONS(d_A, d_B)
   =  (DeletedFromAWithB(d_A, d_B), DeletedFromBWithA(d_A, d_B))
```

(See Definition above.)

---

## D-BOUND — DBound (AX, axiom)

**Observational-discipline axiom (D-BOUND).** SHOWDELETIONS is an observational operation invoked between composites: the pre-state `Σ` is a *composite-boundary state* — reachable from `Σ_0` by a finite sequence of valid composite transitions under ValidComposite★ (ASN-0047).

The axiom is part of the operation's contract: D-EXH's composite-boundary hypothesis is discharged at every invocation by D-BOUND, not by run-time verification or by appeal to informal "operational scope."

---

## D-SUBSP — DSubsp (CLAIM, claim)

**Claim D-SUBSP.** SHOWDELETIONS operates only over the content subspace (`s_C`).

Formal basis: For any link address `ℓ` with `origin(ℓ) = d_A` and any `d_B ≠ d_A`, `ℓ ∉ ran(M(d_B))`. Proof: L0 gives `subspace_I(ℓ) = s_L`, so `ℓ ∈ dom(L)`. Suppose `ℓ ∈ ran(M(d_B))` for contradiction. By S3★-aux, `subspace(v) ∈ {s_C, s_L}` for the witnessing `v`:
- `subspace(v) = s_C` ⟹ `M(d_B)(v) ∈ dom(C)`, but `ℓ ∈ dom(L)` and L14 gives `ℓ ∉ dom(C)` — contradiction.
- `subspace(v) = s_L` ⟹ CL-OWN forces `origin(M(d_B)(v)) = d_B`, but `origin(ℓ) = d_A ≠ d_B` — contradiction.

Therefore `CURRENT(ℓ, d_B)` can never be satisfied across documents for link material.

---

## D-IDENT — DIdent (CLAIM, claim)

**Claim D-IDENT.** For every `a` in either output set, the returned reference is precisely the I-address `a` — not a copy with new identity.

The output sets are defined as subsets of `dom(C)`. Each element is an existing I-address. We return addresses, not values.

Three guarantees that depend on persistent I-address identity survive recovery:
- *Link survival*: every link referencing `a` via any endset span `σ` with `a ∈ ⟦σ⟧ = {t : start(σ) ≤ t < reach(σ)}` continues to reference the same `a`; by P3, `L' = L` across all transitions.
- *Transclusion integrity*: by S2 and S3★'s content clause, `subspace(v) = s_C ⟹ M(d)(v) ∈ dom(C)`; by P0, `dom(C)` and values are preserved.
- *Origin attribution*: by S7, `origin(a)` is invariant across all states in which `a ∈ dom(C)`.

---

## D-ORIG — DOrig (CLAIM, claim)

**Claim D-ORIG.** For every `a` in either output set, `origin(a)` is determined and identifies a unique document — the originating allocator of `a`.

By S7 (ASN-0036), `origin(a)` is defined for every `a ∈ dom(C)` and is invariant across all states in which `a ∈ dom(C)`. The output sets are subsets of `dom(C)`, so `origin` is well-defined on every output element.

---

## D-ORD — DOrd (CLAIM, claim)

**Claim D-ORD.** Each output half is a finite subset of `dom(C) ⊆ T`, and therefore inherits the total order T1 (ASN-0034) imposes on tumblers. No separate ordering structure is needed: the addresses are self-ordering, and any presentation may list them in T1 order.

The output sets are subsets of `dom(C)`, finite by C-fin (ASN-0047), and T1 is a strict total order on `T` (ASN-0034).

---

## D-SYM — DSym (CLAIM, claim)

**Claim D-SYM.** Argument swap maps each output half into the other:

```
SHOWDELETIONS(d_A, d_B)  =  (X, Y)
SHOWDELETIONS(d_B, d_A)  =  (Y, X)
```

where `X = DeletedFromAWithB(d_A, d_B)` and `Y = DeletedFromBWithA(d_A, d_B)`.

By name-substitution: `DeletedFromAWithB(d_B, d_A)` reads as `{a : DELETED(a, d_B) ∧ CURRENT(a, d_A)} = DeletedFromBWithA(d_A, d_B)`. Likewise the other half.

---

## D-ACT — DAct (CLAIM, claim)

**Claim D-ACT.** The output is in a form usable as input to any operation that consumes I-addresses to produce arrangement extensions.

Each output element is an I-address in `dom(C)`, carrying determinate origin (D-ORIG) and preserved identity (D-IDENT). Any operation whose input type accepts I-addresses (or spans thereof) can consume the output directly.

---

## D-OBS — DObs (CLAIM, claim)

**Claim D-OBS.** SHOWDELETIONS does not modify any state component.

Formally, for state `Σ = (C, L, E, M, R)` and the state `Σ'` obtaining after the operation:

```
Σ'.C  =  Σ.C
Σ'.L  =  Σ.L
Σ'.E  =  Σ.E
Σ'.R  =  Σ.R
(A d ∈ E_doc ::  Σ'.M(d) = Σ.M(d))
```

---

## D-STORE — DStore (CLAIM, claim)

**Claim D-STORE.** The output is not required to be stored as a document; it is a query result.

Because the operation is observational (D-OBS), its result is merely delivered to the caller and is not stored as a document or otherwise integrated into the persistent store; the system creates no persistent artefact of its own accord.

---

## D-RECONS — DRecons (CLAIM, claim)

**Claim D-RECONS.** The output depends only on the current state `Σ`. It does not depend on the particular sequence of transitions by which `Σ` was reached.

Each predicate `CURRENT`, `DELETED`, `NEVER_INCLUDED` is defined in terms of components of `Σ` only (`M`, `R`, `dom(C)`, `subspace_I`). The output sets are characterised entirely by these projections. Two distinct transition histories yielding the same `Σ` therefore yield identical SHOWDELETIONS outputs.
