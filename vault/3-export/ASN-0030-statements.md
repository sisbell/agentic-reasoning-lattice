# ASN-0030 Formal Statements

*Source: ASN-0030-address-permanence.md (revised 2026-03-11) — Index: 2026-03-12 — Extracted: 2026-03-12*

## Definition — Reachable

```
reachable(a, d) ≡ (E p : (d, p) ∈ refs(a))
```
Equivalent to: `(E p : 1 ≤ p ≤ n_d : Σ.V(d)(p) = a)`

Where `refs(a) = {(d, p) : d ∈ Σ.D ∧ 1 ≤ p ≤ n_d ∧ Σ.V(d)(p) = a}` (ASN-0026).

---

## Definition — GloballyReachable

```
reachable(a) ≡ refs(a) ≠ ∅
```
Equivalently: `(E d : d ∈ Σ.D : reachable(a, d))`

---

## Definition — Endset

```
endset(L) = ∪{[s, s ⊕ l) : (s, l) ∈ from(L) ∪ to(L) ∪ type(L)}
```
Where each span `(s, l)` with `l > 0` denotes the contiguous set `{t : s ≤ t < s ⊕ l}` (T12, SpanWellDefined, ASN-0001). `a ∈ endset(L)` means `a` is an individual I-address in this union.

---

## Definition — Ghost

```
ghost(a) ≡ a ∉ dom(Σ.I) ∧ T4(a)
```

---

## A0 — IdentityPermanence (LEMMA, lemma)

For any state transition Σ → Σ':

```
[a ∈ dom(Σ.I) ⟹ a ∈ dom(Σ'.I) ∧ Σ'.I(a) = Σ.I(a)]
```

Conjunction of P0 (ISpaceImmutable) and P1 (ISpaceMonotone) from ASN-0026.

---

## A1 — ReachabilityNonMonotone (LEMMA, lemma)

```
¬[reachable(a, d) in Σ ⟹ reachable(a, d) in Σ']
```

Witness: DELETE on document `d` can remove the V-space mappings that made `a` reachable through `d`.

---

## A2 — AccessibilityPartition (LEMMA, lemma)

For any address `a` satisfying T4 and state Σ, exactly one of:

```
(i)   a ∈ dom(Σ.I) ∧ reachable(a)       — active
(ii)  a ∈ dom(Σ.I) ∧ ¬reachable(a)      — unreferenced
(iii) a ∉ dom(Σ.I)                        — unallocated
```

Exhaustiveness: P2 (ReferentiallyComplete, ASN-0026) gives `Σ.V(d)(p) ∈ dom(Σ.I)` for every valid position, so `reachable(a) ⟹ a ∈ dom(Σ.I)`. Contrapositively: `a ∉ dom(Σ.I) ⟹ ¬reachable(a)` — the fourth combination is impossible.

---

## A3 — AccessibilityTransitions (LEMMA, lemma)

```
(a)  (iii) → (i):   permitted
(b)  (i) → (ii):    permitted
(c)  (ii) → (i):    permitted by invariants; not achievable by any currently defined operation for truly unreferenced addresses
(d)  (i) → (iii):   forbidden — violates P1
(e)  (ii) → (iii):  forbidden — violates P1
(f)  (iii) → (ii):  achievable — composite via (a) then (b)
```

---

## A4 pre — DeletePre (PRE, requires)

```
d ∈ Σ.D ∧ 1 ≤ p ∧ p + k − 1 ≤ n_d ∧ k ≥ 1
```

Operation: DELETE(d, p, k) — remove k positions starting at p from document d.

---

## A4(a) — ISpaceUnchanged/DELETE (FRAME, ensures)

```
Σ'.I = Σ.I
```

Instance of +_ext (ISpaceExtension, ASN-0026) with `fresh = ∅`.

---

## A4(b) — DeleteContentPersists (LEMMA, lemma)

```
(A j : p ≤ j < p + k :
    let a = Σ.V(d)(j) :
    a ∈ dom(Σ'.I) ∧ Σ'.I(a) = Σ.I(a))
```

---

## A4(c) — DeleteVLength (POST, ensures)

```
|Σ'.V(d)| = n_d − k
```

---

## A4(d) — LeftUnchanged/DELETE (FRAME, ensures)

```
(A j : 1 ≤ j < p : Σ'.V(d)(j) = Σ.V(d)(j))
```

---

## A4(e) — DeleteRightShift (POST, ensures)

```
(A j : p + k ≤ j ≤ n_d : Σ'.V(d)(j − k) = Σ.V(d)(j))
```

---

## A4(f) — OtherDocsUnchanged/DELETE (FRAME, ensures)

```
(A d' : d' ∈ Σ.D ∧ d' ≠ d : Σ'.V(d') = Σ.V(d'))
```

Instance of P7 (CrossDocVIndependent, ASN-0026).

---

## A4(g) — DocSetUnchanged/DELETE (FRAME, ensures)

```
Σ'.D = Σ.D
```

---

## A4a pre — RearrangePre (PRE, requires)

```
d ∈ Σ.D
```

Operation: REARRANGE(d, cuts).

---

## A4a(a) — ISpaceUnchanged/REARRANGE (FRAME, ensures)

```
Σ'.I = Σ.I
```

---

## A4a(b) — RearrangeVLength (FRAME, ensures)

```
|Σ'.V(d)| = |Σ.V(d)|
```

---

## A4a(c) — RearrangePermutation (POST, ensures)

```
(E π : π is a bijection [1..n_d] → [1..n_d] :
    (A p : 1 ≤ p ≤ n_d : Σ'.V(d)(p) = Σ.V(d)(π(p))))
```

---

## A4a(d) — OtherDocsUnchanged/REARRANGE (FRAME, ensures)

```
(A d' : d' ∈ Σ.D ∧ d' ≠ d : Σ'.V(d') = Σ.V(d'))
```

Instance of P7 (CrossDocVIndependent, ASN-0026).

---

## A4a(e) — DocSetUnchanged/REARRANGE (FRAME, ensures)

```
Σ'.D = Σ.D
```

---

## A5 pre — CopyPre (PRE, requires)

```
d_s ∈ Σ.D ∧ d_t ∈ Σ.D ∧ k ≥ 1
∧ 1 ≤ p_s ∧ p_s + k − 1 ≤ n_{d_s}
∧ 1 ≤ p_t ≤ n_{d_t} + 1
```

Operation: COPY(d_s, p_s, k, d_t, p_t) — copy k positions from d_s into d_t.

---

## A5(a) — CopyAddressSharing (POST, ensures)

```
(A j : 0 ≤ j < k : Σ'.V(d_t)(p_t + j) = Σ.V(d_s)(p_s + j))
```

---

## A5(b) — ISpaceUnchanged/COPY (FRAME, ensures)

```
Σ'.I = Σ.I
```

Instance of +_ext (ASN-0026) with `fresh = ∅`.

---

## A5(c) — CopyTargetLength (POST, ensures)

```
|Σ'.V(d_t)| = n_{d_t} + k
```

---

## A5(d) — LeftUnchanged/COPY (FRAME, ensures)

```
(A j : 1 ≤ j < p_t : Σ'.V(d_t)(j) = Σ.V(d_t)(j))
```

---

## A5(e) — CopyRightShift (POST, ensures)

```
(A j : p_t ≤ j ≤ n_{d_t} : Σ'.V(d_t)(j + k) = Σ.V(d_t)(j))
```

---

## A5(f) — CopySourceUnchanged (FRAME, ensures)

```
d_s ≠ d_t ⟹ Σ'.V(d_s) = Σ.V(d_s)
```

---

## A5(g) — OtherDocsUnchanged/COPY (FRAME, ensures)

```
(A d' : d' ∈ Σ.D ∧ d' ≠ d_t : Σ'.V(d') = Σ.V(d'))
```

Instance of P7 (CrossDocVIndependent, ASN-0026).

---

## A5(h) — DocSetUnchanged/COPY (FRAME, ensures)

```
Σ'.D = Σ.D
```

---

## A6 — VersionCorrespondence (LEMMA, lemma)

At the moment of version creation, for source document d_s and new version d_v:

```
(A p : 1 ≤ p ≤ |Σ.V(d_s)| : correspond(d_s, p, d_v, p))
```

Where `correspond` is defined in ASN-0026. Derived from D12 (VersionCreation, ASN-0029): `(A p : 1 ≤ p ≤ |Σ.V(d_s)| : Σ'.V(d_v)(p) = Σ.V(d_s)(p))` and `Σ'.I = Σ.I`.

---

## A7 — LinkTargetStability (LEMMA, lemma)

For any link L whose endset addresses are in dom(Σ.I), and any operation:

```
(A a ∈ endset(L) : Σ'.I(a) = Σ.I(a))
```

Precondition: `(A a ∈ endset(L) : a ∈ dom(Σ.I))`. Holds by P2 (ReferentiallyComplete, ASN-0026) at link creation and P1 (ISpaceMonotone) thereafter. Derived from A0.

---

## A7a — EndsetPermanence (LEMMA, lemma)

```
(A a ∈ endset(L) : a ∈ dom(Σ.I) ⟹ a ∈ dom(Σ'.I))
```

Restriction of P1 (ISpaceMonotone, ASN-0026) to endset members.

---

## resolvable — Resolvable (INV, predicate)

```
resolvable(L, d) ≡ (E a ∈ endset(L) : reachable(a, d))
```

---

## A7b — EndsetResolvability (LEMMA, lemma)

```
¬[resolvable(L, d) in Σ ⟹ resolvable(L, d) in Σ']
```

Witness: DELETE on d can remove V-space mappings that made L's endpoints reachable through d.

---

## A8 — GhostLinkValidity (INV, predicate(Link, State))

A link L is structurally valid when its endset contains ghost addresses:

```
(E a ∈ endset(L) : ghost(a))
```

where `ghost(a) ≡ a ∉ dom(Σ.I) ∧ T4(a)`. Such addresses are well-formed tumblers; content retrieval at `a` yields no bytes until transition (iii)→(i).

---

## A9 — CoordinateIndependence (remark)

```
(A a ∈ dom(Σ.I), Σ → Σ' : Σ'.I(a) = Σ.I(a))
```

regardless of whether bytes at `a` have been migrated, cached, replicated, or reorganized in physical storage. Design remark; not a proof obligation.

---

## A10 — AuthenticityCaveat (remark)

A0 is an invariant of the abstract specification. It asserts what correct implementations preserve. It does not provide a mechanism for a client to verify that a particular retrieval satisfies A0. Design remark; not a proof obligation.
