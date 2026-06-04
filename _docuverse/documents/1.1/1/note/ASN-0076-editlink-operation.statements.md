# ASN-0076 Claim Statements

*Source: ASN-0076-editlink-operation.md (revised 2026-05-25) — Extracted: 2026-06-04*

## Definition — EditLinkPrecondition

```
Precondition (composite, evaluated at the pre-state Σ):

Σ is a reachable state of ASN-0047's extended reachable state
ℓ_old ∈ dom(Σ.L)
d_new ∈ E_doc
N ≥ 3
(A i : 1 ≤ i ≤ N : e'_i ∈ Endset)
e'_3 ≠ ∅
τ_sup ∈ T
```

## Definition — EditLinkComposite

```
EDITLINK(ℓ_old, (e'_1, ..., e'_N), d_new, τ_sup) ≡
    Step 1: emit ℓ_new ← K.λ(d_new, (e'_1, ..., e'_N));
    Step 2: emit ℓ_sup ← K.λ(d_new, (E_from, E_to, E_type))

where:
    E_from = { (ℓ_old, δ(1, #ℓ_old)) }
    E_to   = { (ℓ_new, δ(1, #ℓ_new)) }
    E_type = { (τ_sup, δ(1, #τ_sup))  }
```

---

## E0 — EditLinkComposite (LEMMA, lemma)

EDITLINK is realized as a sequence of exactly two K.λ steps: the first allocates the successor link `ℓ_new` with the new endset sequence; the second allocates the supersession link `ℓ_sup` whose from- and to-endsets reference `ℓ_old` and `ℓ_new` respectively, and whose type-endset references the designated supersession-type address `τ_sup`.

Sub-claims discharged:

(a) K.λ preconditions at the successor step (`ℓ_new ← K.λ(d_new, (e'_1, ..., e'_N))`):

- Sub-case (a) — first emission: when `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d_new} = ∅`, the determinate first emission of `A_L(d_new)` fixes `ℓ_new = [d_new.0.s_L.1]` with `origin(ℓ_new) = d_new` and `#E(ℓ_new) = 2`.
- Sub-case (b) — subsequent emission: when `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d_new} ≠ ∅`, `ℓ_new = inc(max{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d_new}, 0)`.
- In both sub-cases: `ℓ_new ∉ dom(Σ.C) ∪ dom(Σ.L)`.
- `zeros(ℓ_new) = 3 ∧ E(ℓ_new)_1 = s_L ∧ #E(ℓ_new) ≥ 2 ∧ origin(ℓ_new) = d_new`.

After the successor step: `dom(Σ_1.L) = dom(Σ.L) ∪ {ℓ_new}` with `Σ_1.L(ℓ_new) = (e'_1, ..., e'_N)`.

(b) K.λ preconditions at the supersession step (`ℓ_sup ← K.λ(d_new, (E_from, E_to, E_type))`), firing from `Σ_1`:

- `ℓ_sup = inc(ℓ_new, 0)`.
- `ℓ_sup ∉ dom(Σ_1.C) ∪ dom(Σ_1.L)`.
- `zeros(ℓ_sup) = 3 ∧ E(ℓ_sup)_1 = s_L ∧ #E(ℓ_sup) ≥ 2 ∧ origin(ℓ_sup) = d_new`.
- L3 for `(E_from, E_to, E_type)`: arity 3, each endset in `Endset`, `E_type ≠ ∅`.

(c) ValidComposite★ discharge:

- J0 (AllocationPlacementCoupling): vacuously satisfied (`dom(Σ'.C) = dom(Σ.C)`).
- J1★ (ExtensionRecordsProvenance): vacuously satisfied (`ran(M'(d)) \ ran(M(d))` empty for all `d`).
- J1'★ (ProvenanceRequiresExtension): vacuously satisfied.

---

## E1 — OriginalPreservation (LEMMA, lemma)

For any state transition `Σ →* Σ'` realizing EDITLINK applied to `ℓ_old`:

```
ℓ_old ∈ dom(Σ'.L)  ∧  Σ'.L(ℓ_old) = Σ.L(ℓ_old)
```

---

## E2 — SuccessorDistinctness (LEMMA, lemma)

The successor link's I-address differs from the original's, and the supersession link's I-address differs from both:

```
ℓ_new ≠ ℓ_old  ∧  ℓ_sup ≠ ℓ_old  ∧  ℓ_sup ≠ ℓ_new
```

---

## E3 — SuccessorEndsetFreedom (LEMMA, lemma)

The successor's endset sequence `(e'_1, ..., e'_N)` may differ arbitrarily from `Σ.L(ℓ_old)`, subject only to the structural constraints of L3: `N ≥ 3`, each `e'_i ∈ Endset`, and `e'_3 ≠ ∅`.

Sub-claims:

- the new from-endset may name different spans, more spans, fewer spans, or no spans at all;
- the new type-endset may designate a different type;
- the arity itself may differ from `|Σ.L(ℓ_old)|`, subject to the floor of 3.

---

## E4 — SupersessionLink (LEMMA, lemma)

Following EDITLINK, the state `Σ'` contains a link `ℓ_sup ∈ dom(Σ'.L)` with:

```
(ℓ_old, δ(1, #ℓ_old)) ∈ Σ'.L(ℓ_sup).e₁
(ℓ_new, δ(1, #ℓ_new)) ∈ Σ'.L(ℓ_sup).e₂
(τ_sup,  δ(1, #τ_sup))  ∈ Σ'.L(ℓ_sup).e₃
```

---

## E5 — DivergentSuccessors (LEMMA, lemma)

For any reachable state `Σ` of ASN-0047's extended reachable state — that is, any state derivable from the system's initial state by a finite sequence of valid composite transitions — any `ℓ_old ∈ dom(Σ.L)`, and any natural number `k`, there exists a sequence of transitions `Σ →* Σ_k` — a chain of `k` consecutive EDITLINK composites — such that `Σ_k` contains `k` distinct supersession links each naming `ℓ_old` in its from-endset, with `k` distinct successor links in their respective to-endsets.

Post-state structure verified at `Σ_k`:

(a) For each `j ∈ {1, ..., k-1}`: `ℓ_sup,j ∈ dom(Σ_k.L) ∧ Σ_k.L(ℓ_sup,j) = Σ_{k-1}.L(ℓ_sup,j)`.

(b) For each `j ∈ {1, ..., k-1}`: `ℓ_new,j ∈ dom(Σ_k.L) ∧ Σ_k.L(ℓ_new,j) = Σ_{k-1}.L(ℓ_new,j)`.

(c) `(ℓ_old, δ(1, #ℓ_old)) ∈ Σ_k.L(ℓ_sup,k).e_1` and `(ℓ_new,k, δ(1, #ℓ_new,k)) ∈ Σ_k.L(ℓ_sup,k).e_2`.

(d) All 2k allocated link addresses `{ℓ_new,1, ℓ_sup,1, ..., ℓ_new,k, ℓ_sup,k}` are pairwise distinct.

---

## E6 — SupersessionOwnershipFreedom (LEMMA, lemma)

The supersession link's home document `d_new` is not constrained by the link model to equal `home(ℓ_old)`. Formally: EDITLINK places no constraint coupling `d_new` to `home(ℓ_old)`; for any state `Σ` satisfying all invariants and otherwise-valid inputs, every pair `(ℓ_old, d_new)` with `ℓ_old ∈ dom(Σ.L)` and `d_new ∈ Σ.E_doc` is admitted.

---

## E7 — LineageWitness (LEMMA, lemma)

The supersession link's endsets structurally contain `ℓ_old` and `ℓ_new` as covering witnesses — a property of `Σ'.L` alone:

```
ℓ_old ∈ coverage(Σ'.L(ℓ_sup).e₁)  ∧  ℓ_new ∈ coverage(Σ'.L(ℓ_sup).e₂)
```

---

## E8 — OriginalResolutionUnaffected (LEMMA, lemma)

Any operation that resolves an endset reference to `ℓ_old` and reads `Σ.L(ℓ_old)` obtains the same value before and after EDITLINK.

```
Σ'.L(ℓ_old) = Σ.L(ℓ_old)
```

---

## E9 — LineagePermanence (LEMMA, lemma)

Once created, the supersession link persists across all subsequent state transitions:

```
ℓ_sup ∈ dom(Σ.L)  ⟹  (A Σ → Σ' :: ℓ_sup ∈ dom(Σ'.L) ∧ Σ'.L(ℓ_sup) = Σ.L(ℓ_sup))
```

---

## E10 — NoImplicitNotification (LEMMA, lemma)

EDITLINK modifies neither any arrangement nor the provenance record of any document:

```
(A d ∈ E_doc :: Σ'.M(d) = Σ.M(d))  ∧  Σ'.R = Σ.R
```

---

## E11 — DiscoverabilityPrecondition (LEMMA, lemma)

For any document `d ∈ dom(Σ.M)`, the weakest precondition under which the supersession link is discoverable from `d` after EDITLINK is a condition on the *pre-state* arrangement of `d`.

Full form (prior to collapse):

```
wp(EDITLINK, discoverable_from(ℓ_sup, d, ·))
  ≡  pre(EDITLINK)
     ∧ ( {t : ℓ_old ≼ t} ∩ ran(Σ.M(d)) ≠ ∅
       ∨ {t : ℓ_new ≼ t} ∩ ran(Σ.M(d)) ≠ ∅
       ∨ {t : τ_sup ≼ t} ∩ ran(Σ.M(d)) ≠ ∅ )
```

where `pre(EDITLINK)` is the composite precondition of E0.

Collapsed form (after discharging the vacuous `ℓ_new` disjunct via `{t : ℓ_new ≼ t} ∩ ran(Σ.M(d)) = ∅`):

```
wp(EDITLINK, discoverable_from(ℓ_sup, d, ·))
  ≡  pre(EDITLINK)
     ∧ ( {t : ℓ_old ≼ t} ∩ ran(Σ.M(d)) ≠ ∅
       ∨ {t : τ_sup ≼ t} ∩ ran(Σ.M(d)) ≠ ∅ )
```

Sub-claim (vacuity of `ℓ_new` branch):

```
{t : ℓ_new ≼ t} ∩ ran(Σ.M(d)) = ∅
```

established via: `ran(Σ.M(d)) ⊆ dom(Σ.C) ∪ dom(Σ.L)` (S3★, ASN-0047); `ℓ_new ∉ dom(Σ.C) ∪ dom(Σ.L)` (E0); and `{t : ℓ_new ≼ t} ∩ (dom(Σ.C) ∪ dom(Σ.L)) ⊆ {ℓ_new}` (by `#E` uniformity argument on `F`).
