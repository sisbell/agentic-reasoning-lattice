# ASN-0027 Formal Statements

*Source: ASN-0027-address-permanence.md (revised 2026-03-10) — Index: 2026-03-10 — Extracted: 2026-03-10*

## Definition — Refs

`refs(a) = {(d, p) : d ∈ Σ.D ∧ 1 ≤ p ≤ n_d ∧ Σ.V(d)(p) = a}`

## Definition — Reachable

`reachable(a, Σ)  ≡  refs(a) ≠ ∅`

where `refs(a)` is as defined above.

## Definition — RearrangeBijectionPivot

For m = 3, cuts `c_1 < c_2 < c_3`, bijection σ on `{1, ..., n_d}`:

```
σ(j) = j + (c_3 − c_2)      for c_1 ≤ j < c_2
σ(j) = j − (c_2 − c_1)      for c_2 ≤ j < c_3
σ(j) = j                     otherwise
```

## Definition — RearrangeBijectionSwap

For m = 4, cuts `c_1 < c_2 < c_3 < c_4`, bijection σ on `{1, ..., n_d}`:

```
σ(j) = j + (c_4 − c_2)                       for c_1 ≤ j < c_2
σ(j) = j + (c_4 − c_3) − (c_2 − c_1)        for c_2 ≤ j < c_3
σ(j) = j − (c_3 − c_1)                       for c_3 ≤ j < c_4
σ(j) = j                                      otherwise
```

---

## Σ.reachable — Reachable (INV, predicate(Addr, State))

`reachable(a, Σ)  ≡  refs(a) ≠ ∅`

where `refs(a) = {(d, p) : d ∈ Σ.D ∧ 1 ≤ p ≤ n_d ∧ Σ.V(d)(p) = a}`

---

## A0 — ReachabilityNonPermanent (LEMMA, lemma)

There exist transitions `Σ → Σ'` such that `reachable(a, Σ) ∧ ¬reachable(a, Σ')`.

---

## A1 — ISpaceFrame (INV, predicate(State, State))

For each primitive operation, the I-space transition is:

| Operation | I-space transition |
|-----------|-------------------|
| INSERT | `Σ'.I = Σ.I ∪ {(a_j, c_j) : 1 ≤ j ≤ k}`, each `a_j ∉ dom(Σ.I)` |
| DELETE | `Σ'.I = Σ.I` |
| REARRANGE | `Σ'.I = Σ.I` |
| COPY | `Σ'.I = Σ.I` |
| CREATENEWVERSION | `Σ'.I = Σ.I` |

---

## A2.pre — DeletePre (PRE, requires)

`d ∈ Σ.D ∧ 1 ≤ p ∧ p + k − 1 ≤ n_d ∧ k ≥ 1`

## A2.length — DeleteLength (POST, ensures)

`|Σ'.V(d)| = n_d − k`

## A2.left — DeleteLeftFrame (FRAME, ensures)

`(A j : 1 ≤ j < p : Σ'.V(d)(j) = Σ.V(d)(j))`

## A2.compact — DeleteCompaction (POST, ensures)

`(A j : p + k ≤ j ≤ n_d : Σ'.V(d)(j − k) = Σ.V(d)(j))`

## A2.frame-I — DeleteISpacePreserved (FRAME, ensures)

`Σ'.I = Σ.I`

## A2.frame-doc — DeleteCrossDocFrame (FRAME, ensures)

`(A d' : d' ∈ Σ.D ∧ d' ≠ d : Σ'.V(d') = Σ.V(d'))`

---

## A3.pre — RearrangePre (PRE, requires)

`d ∈ Σ.D ∧ m ∈ {3, 4} ∧ 1 ≤ c_1 < c_2 < ... < c_m ≤ n_d + 1`

## A3.length — RearrangeLength (POST, ensures)

`|Σ'.V(d)| = n_d`

## A3.perm — RearrangePermutation (POST, ensures)

`(A j : 1 ≤ j ≤ n_d : Σ'.V(d)(σ(j)) = Σ.V(d)(j))`

where σ is the bijection on `{1, ..., n_d}` defined by RearrangeBijectionPivot (m = 3) or RearrangeBijectionSwap (m = 4).

## A3.range — RearrangeRangePreservation (LEMMA, lemma)

`range(Σ'.V(d)) = range(Σ.V(d))`

Derived from A3.perm: a bijection preserves the multiset of values, hence the range.

## A3.frame-I — RearrangeISpacePreserved (FRAME, ensures)

`Σ'.I = Σ.I`

## A3.frame-doc — RearrangeCrossDocFrame (FRAME, ensures)

P7 (cross-document frame — see foundation ASNs)

---

## A4.pre — CopyPre (PRE, requires)

`d_s ∈ Σ.D ∧ d_t ∈ Σ.D ∧ k ≥ 1 ∧ 1 ≤ p_s ∧ p_s + k − 1 ≤ n_{d_s} ∧ 1 ≤ p_t ≤ n_{d_t} + 1`

## A4.identity — CopyIdentitySharing (POST, ensures)

`(A j : 0 ≤ j < k : Σ'.V(d_t)(p_t + j) = Σ.V(d_s)(p_s + j))`

## A4.length — CopyLength (POST, ensures)

`|Σ'.V(d_t)| = n_{d_t} + k`

## A4.left — CopyLeftFrame (FRAME, ensures)

`(A j : 1 ≤ j < p_t : Σ'.V(d_t)(j) = Σ.V(d_t)(j))`

## A4.right — CopyRightShift (POST, ensures)

`(A j : p_t ≤ j ≤ n_{d_t} : Σ'.V(d_t)(j + k) = Σ.V(d_t)(j))`

## A4.frame-I — CopyISpacePreserved (FRAME, ensures)

`Σ'.I = Σ.I`

## A4.frame-doc — CopyCrossDocFrame (FRAME, ensures)

`(A d' : d' ∈ Σ.D ∧ d' ≠ d_t : Σ'.V(d') = Σ.V(d'))`

---

## A5.new — VersionNewDoc (POST, ensures)

`d' ∈ Σ'.D ∧ d' ∉ Σ.D`

## A5.identity — VersionIdentitySharing (POST, ensures)

`|Σ'.V(d')| = n_d ∧ (A j : 1 ≤ j ≤ n_d : Σ'.V(d')(j) = Σ.V(d)(j))`

where `d'` is the new document from A5.new and `d` is the source document.

## A5.frame-doc — VersionCrossDocFrame (FRAME, ensures)

`(A d'' : d'' ∈ Σ.D : Σ'.V(d'') = Σ.V(d''))`

(All existing documents are unchanged; the bound variable is `d''` to avoid collision with `d'` the new version.)

## A5.frame-I — VersionISpacePreserved (FRAME, ensures)

`Σ'.I = Σ.I`

---

## A6 — NonInvertibility (LEMMA, lemma)

**Setup:** Let `Σ_0.V(d)(p + j) = a_j` for `0 ≤ j < k`. Let `Σ_1 = DELETE(Σ_0, d, p, k)`. Let `Σ_2 = INSERT(Σ_1, d, p, k, c)` for any content `c`.

**Conclusion:**

`(A j : 0 ≤ j < k : Σ_2.V(d)(p + j) ≠ a_j)`

---

## A7 — IdentityRestoringCopy (LEMMA, lemma)

**Setup:** Let `Σ_0.V(d)(p + j) = a_j` for `0 ≤ j < k`. Let `Σ_1 = DELETE(Σ_0, d, p, k)`. Suppose there exists a document `d'` such that `Σ_1.V(d')(q + j) = a_j` for `0 ≤ j < k`. Let `Σ_2 = COPY(d', (q, k), d, p)` in state `Σ_1`.

**Conclusion:**

`(A j : 0 ≤ j < k : Σ_2.V(d)(p + j) = a_j)`

---

## A7.corollary — FullRestoration (LEMMA, lemma)

**Setup:** Under the conditions of A7.

**Conclusion:** `Σ_2.V(d) = Σ_0.V(d)`

**Sub-parts:**

- *Left frame:* `(A j : 1 ≤ j < p : Σ_2.V(d)(j) = Σ_0.V(d)(j))`
- *Restored positions:* `(A j : p ≤ j < p + k : Σ_2.V(d)(j) = Σ_0.V(d)(j))`
- *Right frame:* `(A m : p + k ≤ m ≤ n_d : Σ_2.V(d)(m) = Σ_0.V(d)(m))`
- *Length:* `|Σ_2.V(d)| = |Σ_1.V(d)| + k = (n_d − k) + k = n_d`

---

## A8 — ReferencePermanence (LEMMA, lemma)

**Setup:** Let `a ∈ dom(Σ.I)`. For any finite sequence of operations producing state `Σ_n`:

(i) `a ∈ dom(Σ_n.I)`

(ii) `Σ_n.I(a) = Σ.I(a)`

---

## A9 — ReachabilityDecay (LEMMA, lemma)

If `reachable(a, Σ)`, then there exists a finite sequence of operations producing `Σ'` with `¬reachable(a, Σ')`.

---

## A10 — PublicationObligation (INV, predicate(Addr, State))

For content that has been published: `reachable(a, Σ)` is maintained across all states.

Contractual, not architectural. The architecture permits DELETE on any V-space position without checking publication status.
