# ASN-0026 Formal Statements

*Source: ASN-0026-i-space-and-v-space.md (revised 2026-03-07) — Index: 2026-03-09 — Extracted: 2026-03-09*

## Definition — ISpaceMap

`Sigma.I : Addr rightharpoonup Byte` — partial function from I-space addresses (tumblers per ASN-0001) to content bytes. The domain `dom(Sigma.I)` is the set of all allocated I-addresses.

## Definition — VSpaceMap

For each document `d`, `Sigma.V(d) : [1..n_d] -> Addr` is a total function from positions (positive naturals) to I-space addresses, where `n_d = |Sigma.V(d)|` is the document's current length. The domain is the dense interval `{1, ..., n_d}` with no gaps.

## Definition — DocumentSet

`Sigma.D` — the set of all documents that currently exist. `Sigma.V(d)` is defined if and only if `d in Sigma.D`.

## Definition — Retrieve

`RETRIEVE : (DocId, Pos) -> Byte` — operational delivery function. `RETRIEVE(d, p)` denotes the byte the system delivers when position `p` of document `d` is requested.

## Definition — RefSet

`refs(a) = {(d, p) : d in Sigma.D /\ 1 <= p <= n_d /\ Sigma.V(d)(p) = a}`

## Definition — Correspond

`correspond(d_1, p_1, d_2, p_2) == Sigma.V(d_1)(p_1) = Sigma.V(d_2)(p_2)`

---

## P0 — ISpaceImmutable (INV, predicate(State, State))

    [a in dom(Sigma.I)  ==>  Sigma'.I(a) = Sigma.I(a)]

for any state transition `Sigma -> Sigma'`.

## P1 — ISpaceMonotone (INV, predicate(State, State))

    [a in dom(Sigma.I)  ==>  a in dom(Sigma'.I)]

for any transition `Sigma -> Sigma'`.

## NO-REUSE — NoAddressReuse (LEMMA, lemma)

Address reuse is impossible. Derived from P0 + P1:

Suppose `a in dom(Sigma.I)` with `Sigma.I(a) = c`. By P1, `a in dom(Sigma'.I)` for every successor state. By P0, `Sigma'.I(a) = c`. The address is never freed, and its content never changes. There is no state in which `a` is available for reallocation.

## P2 — ReferentiallyComplete (INV, predicate(State))

    [d in Sigma.D /\ 1 <= p <= n_d  ==>  Sigma.V(d)(p) in dom(Sigma.I)]

## P3 — MappingExact (INV, predicate(State))

    [d in Sigma.D /\ 1 <= p <= n_d  ==>  RETRIEVE(d, p) = Sigma.I(Sigma.V(d)(p))]

## P4 — CreationBasedIdentity (LEMMA, lemma)

Distinct allocation acts produce distinct I-addresses.

Derivation: restatement of GlobalUniqueness from ASN-0001 — "No two distinct allocations, anywhere in the system, at any time, produce the same address."

## P5 — NonInjective (LEMMA, lemma)

Self-transclusion (existence witness):

    (E d_1, p_1, p_2 : p_1 =/= p_2 : Sigma.V(d_1)(p_1) = Sigma.V(d_1)(p_2))

is permitted, and cross-document transclusion:

    (E d_1, d_2, p_1, p_2 : d_1 =/= d_2 : Sigma.V(d_1)(p_1) = Sigma.V(d_2)(p_2))

is permitted.

## +_ext — ISpaceExtension (LEMMA, lemma)

For any operation `op`:

    Sigma'.I = Sigma.I +_ext fresh

where `+_ext` denotes extension: `Sigma'.I` agrees with `Sigma.I` on all of `dom(Sigma.I)` and may additionally be defined on new addresses `fresh` where `fresh intersection dom(Sigma.I) = emptyset`.

The freshness condition follows from GlobalUniqueness (ASN-0001): every address in `dom(Sigma.I)` was produced by a prior allocation; every address in `fresh` is produced by a new allocation. By GlobalUniqueness, `fresh intersection dom(Sigma.I) = emptyset`.

Operation classification:
- DELETE, REARRANGE, COPY: `fresh = emptyset`
- INSERT: `fresh` is the set of newly allocated I-addresses for the inserted content
- CREATENEWVERSION: `fresh = emptyset`

## P7 — CrossDocVIndependent (INV, predicate(State, State))

    (A d' : d' in Sigma.D /\ d' =/= target(op) : Sigma'.V(d') = Sigma.V(d'))

The quantifier ranges over `Sigma.D` — documents that exist in the pre-state.

Write targets: INSERT writes `d`; DELETE writes `d`; REARRANGE writes `d`; COPY writes the target document; CREATENEWVERSION writes no existing document.

## P8 — NoRefCounting (LEMMA, lemma)

Derived from P1: `dom(Sigma.I)` never shrinks, regardless of `|refs(a)|`. Content persists even when `refs(a) = emptyset`.

## P9 (pre) — ValidInsertPos (PRE, requires)

`1 <= p <= n_d + 1` and `k >= 1`.

## P9 (length) — InsertLength (POST, ensures)

`|Sigma'.V(d)| = n_d + k`

## P9 (left) — LeftUnchanged (FRAME, ensures)

    (A j : 1 <= j < p : Sigma'.V(d)(j) = Sigma.V(d)(j))

## P9 (new) — FreshPositions (POST, ensures)

Let `fresh` be the set of `k` newly allocated I-addresses, with `fresh intersection dom(Sigma.I) = emptyset`. Then:

    (A j : p <= j < p + k : Sigma'.V(d)(j) in fresh)

## P9 (inj) — FreshInjective (POST, ensures)

    (A j_1, j_2 : p <= j_1 < j_2 < p + k : Sigma'.V(d)(j_1) =/= Sigma'.V(d)(j_2))

## P9 (right) — RightShifted (FRAME, ensures)

    (A j : p <= j <= n_d : Sigma'.V(d)(j + k) = Sigma.V(d)(j))

## P11 — ViewerIndependent (INV, predicate(State))

RETRIEVE protocol signature:

    RETRIEVE : (DocId, Pos) -> Byte

No viewer, session, or context parameter exists in the protocol signature. The back-end operation is a pure function of document and position.

## REF-STABILITY — RefStability (LEMMA, lemma)

Let `Sigma` be a state where documents `d_s` and `d_t` share I-addresses (i.e., `(E a : a in range(Sigma.V(d_s)) intersection range(Sigma.V(d_t)))`). After any operation whose write target is `d_s` (and `d_t =/= d_s`), producing `Sigma'`:

    (A p : 1 <= p <= n_{d_t} : Sigma'.V(d_t)(p) in dom(Sigma'.I))

Proof: Since `d_t in Sigma.D` and `d_t` is not the write target, P7 gives `Sigma'.V(d_t) = Sigma.V(d_t)`. By P1, `dom(Sigma.I) subset dom(Sigma'.I)`. By P2 on `Sigma` and P1, P2 holds on `Sigma'` for `d_t`.
