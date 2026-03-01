# ASN-0004 Formal Properties

*Source: ASN-0004-content-insertion.md (revised 2026-02-24) — Contract: 2026-03-01 — Extracted: 2026-03-01*

## Definition — ShiftMapping

Let `m : Pos ⇀ Addr` be a partial mapping, `p` a position, and `w > 0` a width. The shift of m at p by w is:

  `shift(m, p, w) = {(q, m.q) : q ∈ dom.m ∧ sub(q) = sub(p) ∧ q < p}`
  `              ∪ {(q + w, m.q) : q ∈ dom.m ∧ sub(q) = sub(p) ∧ q ≥ p}`
  `              ∪ {(q, m.q) : q ∈ dom.m ∧ sub(q) ≠ sub(p)}`

Variables: `m` — V→I mapping for a document; `p` — insertion position; `w` — insertion width (#c); `sub(q)` — subspace identifier of position q.

---

## S-DISJ — SubspaceDisjoint (INV, predicate(State))

`(A d : (A a₁, a₂ : a₁ ∈ img_text(d) ∧ a₂ ∈ img_link(d) : a₁ ≠ a₂))`

Variables: `img_text(d)` — set of I-addresses allocated in d's text subspace; `img_link(d)` — set of I-addresses allocated in d's link subspace.

---

## S0 — VIGrounding (INV, predicate(State))

`(A d, q : q ∈ dom.poom(d) : poom(d).q ∈ dom.ispace)`

---

## S1 — IspaceImmutable (INV, predicate(State, State))

`(A a : a ∈ dom.ispace : ispace'.a = ispace.a)`

---

## S2 — LinkGrounding (INV, predicate(State))

`(A L ∈ links, a ∈ addrs(endsets(L)) : a ∈ dom.ispace)`

---

## S3 — SpanIndexConsistent (INV, predicate(State))

`(A (a, d) ∈ spanindex : a ∈ dom.ispace)`

---

## S4 — PoomInjective (INV, predicate(State))

`(A d, q₁, q₂ : q₁ ∈ dom.poom(d) ∧ q₂ ∈ dom.poom(d) ∧ q₁ ≠ q₂ : poom(d).q₁ ≠ poom(d).q₂)`

---

## S5 — PositionsDense (INV, predicate(State))

For every document d, the occupied text positions form a contiguous range `[1, |poom(d)|]` (or the empty set when `|poom(d)| = 0`).

Variables: `|poom(d)|` — number of active positions in d's text subspace.

---

## P0 — AddressIrrevocable (LEMMA, lemma)

`(A a : a ∈ dom.ispace : a ∈ dom.ispace')`

Derived from S1 (I-space immutability) together with the append-only property of I-space.

---

## P1 — ContentImmutable (LEMMA, lemma)

`(A a : a ∈ dom.ispace : ispace'.a = ispace.a)`

Restates S1 directly.

---

## P2 — SpanIndexMonotone (INV, predicate(State, State))

`(A (a, d) : (a, d) ∈ spanindex : (a, d) ∈ spanindex')`

Axiomatic status: the span index is append-only by design.

---

## PRE1 — DocExists (PRE, requires)

`d ∈ dom.owner`

---

## PRE2 — IsOwner (PRE, requires)

`user = owner(d)`

---

## PRE3 — PositionValid (PRE, requires)

`1 ≤ p ≤ |poom(d)| + 1`

Variables: `p` — insertion position; `|poom(d)|` — current text length of document d (0 for empty document).

---

## PRE4 — ContentNonEmpty (PRE, requires)

`#c > 0`

Variables: `#c` — length (byte count) of content sequence c.

---

## INS1 — FreshAddresses (POST, ensures)

`(E S : S ⊆ Addr ∧ #S = #c ∧ S ∩ dom.ispace = ∅ : S ⊆ dom.ispace')`

The freshly allocated addresses form a contiguous range: if a₀ is the starting address, the allocation produces `{a₀, a₀+1, ..., a₀+#c-1}`, where the successor operation respects the tumbler allocation order within the document's text subspace.

---

## INS1a — TextSubspaceAllocation (POST, ensures)

`(A i : 0 ≤ i < #c : sub_i(a₀ + i) = TEXT)`

Variables: `a₀` — starting address of the fresh allocation; `sub_i(a)` — I-space subspace classifier of address a; `TEXT` — the text subspace identifier.

---

## INS2 — ContentEstablished (POST, ensures)

`(A i : 0 ≤ i < #c : ispace'.(a₀ + i) = c.i)`

Variables: `a₀` — starting address of the fresh allocation; `c.i` — i-th byte of the content being inserted.

---

## INS3 — ContentPlacement (POST, ensures)

`(A i : 0 ≤ i < #c : poom'(d).(p + i) = a₀ + i)`

---

## INS4 — PositionShift (POST, ensures)

(a) `(A q : q < p ∧ q ∈ dom.poom(d) ∧ sub(q) = sub(p) : poom'(d).q = poom(d).q)`

(b) `(A q : q ≥ p ∧ q ∈ dom.poom(d) ∧ sub(q) = sub(p) : poom'(d).(q + #c) = poom(d).q)`

---

## INS-D1 — DomainSize (LEMMA, lemma)

`|poom'(d)| = |poom(d)| + #c`

Derived from INS3 and INS4 together.

---

## INS5 — SpanIndexExtended (POST, ensures)

`(A i : 0 ≤ i < #c : (a₀ + i, d) ∈ spanindex')`

---

## INS-F1 — IspaceUpperBound (FRAME, ensures)

`dom.ispace' ⊆ dom.ispace ∪ {a₀, ..., a₀ + #c - 1}`

Combined with P0 (`dom.ispace ⊆ dom.ispace'`) and INS1 (`{a₀, ..., a₀+#c-1} ⊆ dom.ispace'`), yields: `dom.ispace' = dom.ispace ∪ {a₀, ..., a₀ + #c - 1}`.

---

## INS-F2 — OtherDocsUnchanged (FRAME, ensures)

`(A d' : d' ≠ d : poom'(d') = poom(d'))`

---

## INS-D2 — VICorrespondencePreserved (LEMMA, lemma)

(a) `(A q : q ∈ dom.poom(d) ∧ sub(q) = sub(p) ∧ q < p : ispace'.(poom'(d).q) = ispace.(poom(d).q))`

(b) `(A q : q ∈ dom.poom(d) ∧ sub(q) = sub(p) ∧ q ≥ p : ispace'.(poom'(d).(q + #c)) = ispace.(poom(d).q))`

Derived from INS4 and P1.

---

## INS-F4 — LinksPreserved (FRAME, ensures)

`(A L ∈ links : L ∈ links' ∧ endsets'(L) = endsets(L))`

---

## INS-F4a — NoNewLinks (FRAME, ensures)

`links' ⊆ links`

Together with INS-F4 (`links ⊆ links'`), yields: `links' = links`.

---

## INS-F5 — SubspaceIsolation (FRAME, ensures)

`(A q : q ∈ dom.poom(d) ∧ sub(q) ≠ sub(p) : poom'(d).q = poom(d).q)`

---

## INS-F6 — SpanIndexUpperBound (FRAME, ensures)

`spanindex' ⊆ spanindex ∪ {(a₀ + i, d) : 0 ≤ i < #c}`

Combined with P2 and INS5, yields: `spanindex' = spanindex ∪ {(a₀ + i, d) : 0 ≤ i < #c}`.

---

## INS-CORR — InsertCorrectness (LEMMA, lemma)

Let Σ' = INSERT(d, p, c) applied to state Σ satisfying PRE1–PRE4. Then:

(i) `dom.ispace' = dom.ispace ∪ {a₀, ..., a₀ + #c - 1}` where `{a₀, ..., a₀ + #c - 1} ∩ dom.ispace = ∅`

(ii) `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)`

(iii) `(A i : 0 ≤ i < #c : ispace'.(a₀ + i) = c.i)`

(iv) `poom'(d) = shift(poom(d), p, #c) ∪ {(p+i, a₀+i) : 0 ≤ i < #c}`

(v) `(A d' : d' ≠ d : poom'(d') = poom(d'))`

(vi) `spanindex' = spanindex ∪ {(a₀+i, d) : 0 ≤ i < #c}`

(vii) `links' = links`

Sources: (i) from P0, INS1, INS-F1; (ii) from P1; (iii) from INS2; (iv) from INS3, INS4, INS-F5; (v) from INS-F2; (vi) from P2, INS5, INS-F6; (vii) from INS-F4, INS-F4a.

---

## INS-ATOM — InsertAtomic (LEMMA, lemma)

Either INSERT(d, p, c) transitions Σ to a state Σ' satisfying all of INS-CORR(i)–(vii), or the state is unchanged: Σ' = Σ.
