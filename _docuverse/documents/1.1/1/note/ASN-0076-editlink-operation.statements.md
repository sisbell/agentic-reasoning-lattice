# ASN-0076 Claim Statements

*Source: ASN-0076-editlink-operation.md (revised 2026-05-25) — Extracted: 2026-05-25*

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

The supersession endsets are:

```
E_from = { (ℓ_old, δ(1, #ℓ_old)) }
E_to   = { (ℓ_new, δ(1, #ℓ_new)) }
E_type = { (τ_sup, δ(1, #τ_sup))  }
```

The arrow `←` indicates output binding: the K.λ rule (ASN-0047) produces the address as a function of the pre-state allocator configuration via its first-/subsequent-emission predicates, and the produced address is bound to the named variable. The caller does not supply `ℓ_new` or `ℓ_sup` as inputs; they are determined by the allocator discipline applied to `d_new`. Step 2's endset construction `E_to` reads the `ℓ_new` value produced by Step 1.

## Definition — Covers

For each `a ∈ T` the *covering set*:

```
covers(Σ, a) ≡ {ℓ ∈ dom(Σ.L) : (E i, (s, w) : 1 ≤ i ≤ |Σ.L(ℓ)| ∧ (s, w) ∈ Σ.L(ℓ).e_i : a ∈ coverage({(s, w)}))}
```

— the set of links whose endsets reference `a` through at least one span.

---

## E0 — EditLinkComposite (LEMMA)

**E0 (EditLinkComposite).** EDITLINK is realized as a sequence of exactly two K.λ steps: the first allocates the successor link `ℓ_new` with the new endset sequence; the second allocates the supersession link `ℓ_sup` whose from- and to-endsets reference `ℓ_old` and `ℓ_new` respectively, and whose type-endset references the designated supersession-type address `τ_sup`.

The composite must be admissible under K.λ's preconditions evaluated at each intermediate state. K.λ requires (i) the target document to be in `E_doc`; (ii) the new link's I-address to lie outside `dom(C) ∪ dom(L)`; (iii) the I-address to satisfy the link allocation discipline `zeros(·) = 3 ∧ E(·)_1 = s_L ∧ #E(·) ≥ 2 ∧ origin(·) = d_new`; and (iv) the endset sequence to satisfy L3 — arity at least 3, each endset in `Endset` (equivalently: each constituent span satisfies T12), and the third endset non-empty.

Sub-case (a) — first emission. When `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d_new} = ∅`, K.λ's first-emission rule fixes `ℓ_new = [d_new.0.s_L.1]`.

Sub-case (b) — subsequent emission. When `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d_new} ≠ ∅`, K.λ's subsequent-emission rule fixes `ℓ_new = inc(max{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d_new}, 0)`.

---

## E1 — OriginalPreservation (LEMMA)

**E1 (OriginalPreservation).** For any state transition `Σ →* Σ'` realizing EDITLINK applied to `ℓ_old`:

```
ℓ_old ∈ dom(Σ'.L)  ∧  Σ'.L(ℓ_old) = Σ.L(ℓ_old)
```

---

## E2 — SuccessorDistinctness (LEMMA)

**E2 (SuccessorDistinctness).** The successor link's I-address differs from the original's, and the supersession link's I-address differs from both:

```
ℓ_new ≠ ℓ_old  ∧  ℓ_sup ≠ ℓ_old  ∧  ℓ_sup ≠ ℓ_new
```

Per-step discharge:

- *Step 1* — K.λ's precondition `ℓ_new ∉ dom(Σ.L)`, evaluated at `Σ`, combined with `ℓ_old ∈ dom(Σ.L)` from EDITLINK's precondition, gives `ℓ_new ≠ ℓ_old`.
- *Step 2* — By L12 applied to Step 1, `ℓ_old ∈ dom(Σ.L) ⟹ ℓ_old ∈ dom(Σ_1.L)`; by the effect clause of K.λ on Step 1, `ℓ_new ∈ dom(Σ_1.L)`. K.λ's precondition `ℓ_sup ∉ dom(Σ_1.L)`, evaluated at `Σ_1`, then gives `ℓ_sup ≠ ℓ_old` and `ℓ_sup ≠ ℓ_new`.

---

## E3 — SuccessorEndsetFreedom (LEMMA)

**E3 (SuccessorEndsetFreedom).** The successor's endset sequence `(e'_1, ..., e'_N)` may differ arbitrarily from `Σ.L(ℓ_old)`, subject only to the structural constraints of L3: `N ≥ 3`, each `e'_i ∈ Endset`, and `e'_3 ≠ ∅`.

K.λ accepts any endset sequence satisfying L3 (the precondition `N ≥ 3 ∧ (A i : 1 ≤ i ≤ N : e_i ∈ Endset) ∧ e_3 ≠ ∅`). There is no precondition coupling the new sequence to any prior link's sequence. In particular:

- the new from-endset may name different spans, more spans, fewer spans, or no spans at all;
- the new type-endset may designate a different type;
- the arity itself may differ from `|Σ.L(ℓ_old)|`, subject to the floor of 3.

---

## E4 — SupersessionLink (LEMMA)

**E4 (SupersessionLink).** Following EDITLINK, the state `Σ'` contains a link `ℓ_sup ∈ dom(Σ'.L)` with:

```
(ℓ_old, δ(1, #ℓ_old)) ∈ Σ'.L(ℓ_sup).e₁
(ℓ_new, δ(1, #ℓ_new)) ∈ Σ'.L(ℓ_sup).e₂
(τ_sup,  δ(1, #τ_sup))  ∈ Σ'.L(ℓ_sup).e₃
```

---

## E5 — DivergentSuccessors (LEMMA)

**E5 (DivergentSuccessors).** For any reachable state `Σ` of ASN-0047's extended reachable state — that is, any state derivable from `Σ_0` by a finite sequence of valid composite transitions — any `ℓ_old ∈ dom(Σ.L)`, and any natural number `k`, there exists a sequence of transitions `Σ →* Σ_k` — a chain of `k` consecutive EDITLINK composites — such that `Σ_k` contains `k` distinct supersession links each naming `ℓ_old` in its from-endset, with `k` distinct successor links in their respective to-endsets.

Sub-claims verified at `Σ_k`:

(a) For each `j ∈ {1, ..., k-1}`, `ℓ_sup,j ∈ dom(Σ_k.L)` and `Σ_k.L(ℓ_sup,j) = Σ_{k-1}.L(ℓ_sup,j)`.

(b) For each `j ∈ {1, ..., k-1}`, `ℓ_new,j ∈ dom(Σ_k.L)` with `Σ_k.L(ℓ_new,j) = Σ_{k-1}.L(ℓ_new,j)`.

(c) `Σ_k` contains `ℓ_sup,k ∈ dom(Σ_k.L)` with `(ℓ_old, δ(1, #ℓ_old)) ∈ Σ_k.L(ℓ_sup,k).e_1` and `(ℓ_new,k, δ(1, #ℓ_new,k)) ∈ Σ_k.L(ℓ_sup,k).e_2`.

(d) All `2k` allocated link addresses `{ℓ_new,1, ℓ_sup,1, ..., ℓ_new,k, ℓ_sup,k}` are pairwise distinct.

---

## E6 — SupersessionOwnershipFreedom (LEMMA)

**E6 (SupersessionOwnershipFreedom).** The supersession link's home document `d_new` is not constrained by the link model to equal `home(ℓ_old)`. Formally: for any state `Σ` satisfying all invariants, any `ℓ_old ∈ dom(Σ.L)`, and any `d_new ∈ Σ.E_doc` (not required to equal `home(ℓ_old)`), the composite EDITLINK is admissible at `Σ`.

The conjunction `ℓ_old ∈ dom(Σ.L) ∧ d_new ∈ Σ.E_doc` is the entirety of the constraint EDITLINK places on the pair `(ℓ_old, d_new)`; the model admits every such pair.

---

## E7 — LineageDiscoverability (LEMMA)

**E7 (LineageDiscoverability).** The supersession link's endsets structurally contain `ℓ_old` and `ℓ_new` as discoverable referents. Using the definition of `covers(Σ, a)` above, in the post-state `Σ'`:

```
ℓ_sup ∈ covers(Σ', ℓ_old)  ∧  ℓ_sup ∈ covers(Σ', ℓ_new)
```

---

## E8 — OriginalResolutionUnaffected (LEMMA)

**E8 (OriginalResolutionUnaffected).** Any operation that resolves an endset reference to `ℓ_old` and reads `Σ.L(ℓ_old)` obtains the same value before and after EDITLINK.

```
Σ'.L(ℓ_old) = Σ.L(ℓ_old)
```

No state component intermediating this lookup is altered by EDITLINK (the frame of K.λ preserves `C`, `M`, `E`, `R`; and EDITLINK only extends `L`, never modifies).

---

## E9 — LineagePermanence (LEMMA)

**E9 (LineagePermanence).** Once created, the supersession link persists across all subsequent state transitions:

```
ℓ_sup ∈ dom(Σ.L)  ⟹  (A Σ → Σ' :: ℓ_sup ∈ dom(Σ'.L) ∧ Σ'.L(ℓ_sup) = Σ.L(ℓ_sup))
```

---

## E10 — NoImplicitNotification (LEMMA)

**E10 (NoImplicitNotification).** EDITLINK modifies neither any arrangement nor the provenance record of any document:

```
(A d ∈ E_doc :: Σ'.M(d) = Σ.M(d))  ∧  Σ'.R = Σ.R
```
