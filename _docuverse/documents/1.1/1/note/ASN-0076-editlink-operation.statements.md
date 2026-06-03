# ASN-0076 Claim Statements

*Source: ASN-0076-editlink-operation.md (revised 2026-05-25) — Extracted: 2026-06-03*

## Definition — EditLinkPrecondition

**Precondition (composite, evaluated at the pre-state `Σ`):**

```
ℓ_old ∈ dom(Σ.L)
d_new ∈ E_doc
N ≥ 3
(A i : 1 ≤ i ≤ N : e'_i ∈ Endset)
e'_3 ≠ ∅
τ_sup ∈ T ∧ #τ_sup ≥ 1
```

## Definition — EditLinkComposite

```
EDITLINK(ℓ_old, (e'_1, ..., e'_N), d_new, τ_sup) ≡
    Step 1: emit ℓ_new ← K.λ(d_new, (e'_1, ..., e'_N));
    Step 2: emit ℓ_sup ← K.λ(d_new, (E_from, E_to, E_type))
```

Where:

```
E_from = { (ℓ_old, δ(1, #ℓ_old)) }
E_to   = { (ℓ_new, δ(1, #ℓ_new)) }
E_type = { (τ_sup, δ(1, #τ_sup))  }
```

## Definition — Covers

```
covers(Σ, a) ≡ {ℓ ∈ dom(Σ.L) : (E i, (s, w) : 1 ≤ i ≤ |Σ.L(ℓ)| ∧ (s, w) ∈ Σ.L(ℓ).e_i : a ∈ coverage({(s, w)}))}
```

---

## E0 — EditLinkComposite (LEMMA)

EDITLINK is realized as a sequence of exactly two K.λ steps: the first allocates the successor link `ℓ_new` with the new endset sequence; the second allocates the supersession link `ℓ_sup` whose from- and to-endsets reference `ℓ_old` and `ℓ_new` respectively, and whose type-endset references the designated supersession-type address `τ_sup`.

The composite must be admissible under K.λ's preconditions evaluated at each intermediate state. K.λ requires (i) the target document to be in `E_doc`; (ii) the new link's I-address to lie outside `dom(C) ∪ dom(L)`; (iii) the I-address to satisfy the link allocation discipline `zeros(·) = 3 ∧ E(·)_1 = s_L ∧ #E(·) ≥ 2 ∧ origin(·) = d_new`; and (iv) the endset sequence to satisfy L3 — arity at least 3, each endset in `Endset`, and the third endset non-empty.

Sub-claims:

(a) *Sub-case — first emission.* When `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d_new} = ∅`, the determinate first emission of `A_L(d_new)` fixes `ℓ_new = [d_new.0.s_L.1]`, with `origin(ℓ_new) = d_new` and `#E(ℓ_new) = 2`.

(b) *Sub-case — subsequent emission.* When `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d_new} ≠ ∅`, the T10a-conforming `inc(·, 0)` sibling-advance discipline fixes `ℓ_new = inc(max{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d_new}, 0)`.

(c) In both sub-cases: `ℓ_new ∉ dom(Σ.C) ∪ dom(Σ.L)`, `zeros(ℓ_new) = 3`, `E(ℓ_new)_1 = s_L`, `origin(ℓ_new) = d_new`, `#E(ℓ_new) ≥ 2`.

(d) The supersession step fires from intermediate state `Σ_1` with `ℓ_sup = inc(ℓ_new, 0)`, and analogously: `ℓ_sup ∉ dom(Σ_1.C) ∪ dom(Σ_1.L)`, `zeros(ℓ_sup) = 3`, `E(ℓ_sup)_1 = s_L`, `origin(ℓ_sup) = d_new`, `#E(ℓ_sup) ≥ 2`.

(e) L3 holds for `(E_from, E_to, E_type)`: arity 3, each endset in `Endset`, `E_type ≠ ∅`.

(f) EDITLINK satisfies ValidComposite★.

---

## E1 — OriginalPreservation (LEMMA)

For any state transition `Σ →* Σ'` realizing EDITLINK applied to `ℓ_old`:

```
ℓ_old ∈ dom(Σ'.L)  ∧  Σ'.L(ℓ_old) = Σ.L(ℓ_old)
```

---

## E2 — SuccessorDistinctness (LEMMA)

The successor link's I-address differs from the original's, and the supersession link's I-address differs from both:

```
ℓ_new ≠ ℓ_old  ∧  ℓ_sup ≠ ℓ_old  ∧  ℓ_sup ≠ ℓ_new
```

Sub-claims:

(a) *Step 1* — K.λ's precondition `ℓ_new ∉ dom(Σ.L)`, evaluated at `Σ`, combined with `ℓ_old ∈ dom(Σ.L)` from EDITLINK's precondition, gives `ℓ_new ≠ ℓ_old`.

(b) *Step 2* — By L12 applied to Step 1, `ℓ_old ∈ dom(Σ_1.L)`; by the effect clause of K.λ on Step 1, `ℓ_new ∈ dom(Σ_1.L)`. K.λ's precondition `ℓ_sup ∉ dom(Σ_1.L)`, evaluated at `Σ_1`, gives `ℓ_sup ≠ ℓ_old` and `ℓ_sup ≠ ℓ_new`.

---

## E3 — SuccessorEndsetFreedom (LEMMA)

The successor's endset sequence `(e'_1, ..., e'_N)` may differ arbitrarily from `Σ.L(ℓ_old)`, subject only to the structural constraints of L3: `N ≥ 3`, each `e'_i ∈ Endset`, and `e'_3 ≠ ∅`.

K.λ accepts any endset sequence satisfying `N ≥ 3 ∧ (A i : 1 ≤ i ≤ N : e_i ∈ Endset) ∧ e_3 ≠ ∅`. There is no precondition coupling the new sequence to any prior link's sequence.

---

## E4 — SupersessionLink (LEMMA)

Following EDITLINK, the state `Σ'` contains a link `ℓ_sup ∈ dom(Σ'.L)` with:

```
(ℓ_old, δ(1, #ℓ_old)) ∈ Σ'.L(ℓ_sup).e₁
(ℓ_new, δ(1, #ℓ_new)) ∈ Σ'.L(ℓ_sup).e₂
(τ_sup,  δ(1, #τ_sup))  ∈ Σ'.L(ℓ_sup).e₃
```

---

## E5 — DivergentSuccessors (LEMMA)

For any reachable state `Σ` of ASN-0047's extended reachable state — that is, any state derivable from the system's initial state by a finite sequence of valid composite transitions — any `ℓ_old ∈ dom(Σ.L)`, and any natural number `k`, there exists a sequence of transitions `Σ →* Σ_k` — a chain of `k` consecutive EDITLINK composites — such that `Σ_k` contains `k` distinct supersession links each naming `ℓ_old` in its from-endset, with `k` distinct successor links in their respective to-endsets.

Sub-claims established by induction on `k`:

(a) *Prior supersession links persist with unchanged values.* For each `j ∈ {1, ..., k-1}`, by LP13 applied to `Σ_{k-1} →* Σ_k`: `ℓ_sup,j ∈ dom(Σ_k.L) ∧ Σ_k.L(ℓ_sup,j) = Σ_{k-1}.L(ℓ_sup,j)`.

(b) *Prior successor links persist.* For each `j ∈ {1, ..., k-1}`, by LP13: `ℓ_new,j ∈ dom(Σ_k.L) ∧ Σ_k.L(ℓ_new,j) = Σ_{k-1}.L(ℓ_new,j)`.

(c) *New supersession link references `ℓ_old`.* By E4 applied to the k-th composite: `(ℓ_old, δ(1, #ℓ_old)) ∈ Σ_k.L(ℓ_sup,k).e_1` and `(ℓ_new,k, δ(1, #ℓ_new,k)) ∈ Σ_k.L(ℓ_sup,k).e_2`.

(d) *Pairwise distinctness of all 2k allocated link addresses.* All 2k K.λ allocation events are pairwise distinct events (SequentialTransitionAxiom); by L11a (LinkUniqueness), distinct T10a-conforming allocation events produce distinct link addresses; hence all 2k allocated addresses are pairwise distinct.

---

## E6 — SupersessionOwnershipFreedom (LEMMA)

For any state `Σ` satisfying all invariants, any `ℓ_old ∈ dom(Σ.L)`, and any `d_new ∈ Σ.E_doc` (not required to equal `home(ℓ_old)`), the composite EDITLINK is admissible at `Σ`.

Formally: the conjunction `ℓ_old ∈ dom(Σ.L) ∧ d_new ∈ Σ.E_doc` is the entirety of the constraint EDITLINK places on the pair `(ℓ_old, d_new)`.

---

## E7 — LineageWitness (LEMMA)

The supersession link's endsets structurally contain `ℓ_old` and `ℓ_new` as covering witnesses. Using the `covers` predicate defined above, in the post-state `Σ'`:

```
ℓ_sup ∈ covers(Σ', ℓ_old)  ∧  ℓ_sup ∈ covers(Σ', ℓ_new)
```

Note: this is a property of `Σ.L` alone (inverse lookup over the link store), distinct from and weaker than ASN-0098's arrangement-conditional `discoverable_from`. Absent arrangement of the referents, `ℓ_sup` is orphaned per LP17.

---

## E8 — OriginalResolutionUnaffected (LEMMA)

Any operation that resolves an endset reference to `ℓ_old` and reads `Σ.L(ℓ_old)` obtains the same value before and after EDITLINK:

```
Σ'.L(ℓ_old) = Σ.L(ℓ_old)
```

---

## E9 — LineagePermanence (LEMMA)

Once created, the supersession link persists across all subsequent state transitions:

```
ℓ_sup ∈ dom(Σ.L)  ⟹  (A Σ → Σ' :: ℓ_sup ∈ dom(Σ'.L) ∧ Σ'.L(ℓ_sup) = Σ.L(ℓ_sup))
```

The multi-step extension: for any reachable sequence `Σ →* Σ'`, `ℓ_sup ∈ dom(Σ'.L) ∧ Σ'.L(ℓ_sup) = Σ.L(ℓ_sup)`.

---

## E10 — NoImplicitNotification (LEMMA)

EDITLINK modifies neither any arrangement nor the provenance record of any document:

```
(A d ∈ E_doc :: Σ'.M(d) = Σ.M(d))  ∧  Σ'.R = Σ.R
```
