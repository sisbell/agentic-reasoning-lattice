# ASN-0111 Claim Statements

*Source: ASN-0111-readlink-operation-read-a-link's-structure-by-its-address.md (revised 2026-06-04) — Extracted: 2026-06-08*

## Definition — Coverage

> `coverage(e) = (∪ (s, ℓ) : (s, ℓ) ∈ e : {t ∈ T : s ≤ t < s ⊕ ℓ})`

## Definition — LinkType

> `Link = {(e₁, e₂, ..., eₙ) : N ≥ 3, each eᵢ ∈ Endset}`,  `Endset = 𝒫_fin(Span)`

With standard-triple convention: slot 1 = *from*-endset, slot 2 = *to*-endset, slot 3 = *type*-endset.

## Definition — ReadLink

> `readlink(a, Σ)`
>   *defined when*  `a ∈ dom(Σ.L)`
>   `≡  Σ.L(a) = (e₁, e₂, ..., eₙ)`

Frame condition: `Σ' = Σ` (pure read, changes nothing).

## Definition — HomeAddress

> `home(a) = N(a).0.U(a).0.D(a)`

Determined by T4 field projection from the address `a` alone (L2, ASN-0043).

---

## RL0 — Definedness (LEMMA, PRE)

`readlink(a, Σ)` is defined iff `a ∈ dom(Σ.L)`. Reasoning backward from the postcondition "the result is the recorded relationship at `a`," the weakest precondition is precisely membership:

> `wp(readlink request at a, result = Σ.L(a)) ≡ a ∈ dom(Σ.L)`

For the composite "advance the system by any reachable sequence, then read":

> `wp(Σ →* Σ' ; readlink at a, result = Σ.L(a)) ≡ a ∈ dom(Σ.L)`

evaluated at the *initial* `Σ`. Link-shape of the address (`zeros(a) = 3 ∧ subspace_I(a) = s_L`) is necessary but not sufficient; definedness is a fact about `dom(Σ.L)`, not about address syntax.

---

## RL1 — Completeness (LEMMA, POST)

For each slot `i` and each span, the read omits nothing:

> `(A i, (s, ℓ) : 1 ≤ i ≤ |Σ.L(a)| ∧ (s, ℓ) ∈ Σ.L(a).eᵢ : (s, ℓ) ∈ readlink(a, Σ).eᵢ)`

and conversely the read introduces no span not recorded. Equivalently `readlink(a, Σ) = Σ.L(a)` componentwise.

---

## RL2 — RolePreservation (LEMMA, POST)

> `|readlink(a, Σ)| = |Σ.L(a)|`,  and for each `1 ≤ i ≤ |Σ.L(a)|` the positional accessor `readlink(a, Σ).eᵢ` is a model primitive (L6, ASN-0043), with link equality componentwise.

The quantifier ranges over *all* `|Σ.L(a)|` slots. Slot 1 = *from*, slot 2 = *to*, slot 3 = *type*; slots 4…N returned faithfully under their own indices with no privileged role assigned by this operation.

---

## RL3 — IntraEndsetSetSemantics (LEMMA, POST)

The spans inside `readlink(a, Σ).eᵢ` carry no positional meaning. The read exposes membership, not sequence: there is no operator selecting "the j-th span" of an endset (L5, ASN-0043). An endset is an arbitrary collection of spans, and each span's denotation is fixed by its own boundaries, independent of any position in a list. Two reads that present the same endset's spans in different incidental orders have returned the same endset.

---

## RL4 — HomeDisclosure (LEMMA, POST)

> `home(a) = N(a).0.U(a).0.D(a)` is determined by the read key `a` alone, by T4 field projection, and is independent of the returned endsets (L2, ASN-0043).

---

## RL5 — TypeByAddress (LEMMA, POST)

The relationship the type records is fixed by `coverage(e₃)` — the set of addresses the type-set names — and not by whatever is, or is not, stored at those addresses. Two links share a type exactly when their type endsets have equal coverage (L8, ASN-0043), a relation on address sets, decided without dereferencing a single one. Ghost types (L9, ASN-0043) read completely; the read of a ghost-typed link is no less complete than any other.

---

## RL6 — NestingFidelity (LEMMA, POST)

If `a' ∈ dom(Σ.L)` and `a' ∈ coverage(readlink(a, Σ).eᵢ)`, the read discloses `a'` as the tumbler address it is — it does not flatten the reference into the content, if any, that further reading of `a'` might yield. The read is address-faithful: a target address is returned as an address, whether it names content or another link. The read does not silently recurse, nor does it hide that a returned address is a link rather than content.

---

## RL7 — Determinacy (LEMMA, LEMMA)

`readlink` is a pure function of `(a, Σ.L)`: two reads of the same address in the same link store return identical values. Moreover, the read is stable across the whole future:

> `(A Σ, Σ' : Σ →* Σ' ∧ a ∈ dom(Σ.L) : readlink(a, Σ') = readlink(a, Σ))`

Discharge: LP13 (UnconditionalLinkPersistence, ASN-0098) carries both `a ∈ dom(Σ'.L)` (definedness) and `Σ'.L(a) = Σ.L(a)` (value preservation) across the closure `→*`, giving `readlink(a, Σ') = Σ'.L(a) = Σ.L(a) = readlink(a, Σ)`.

---

## RL8 — RecordedNotResolved (LEMMA, POST)

`readlink(a, Σ)` depends only on `Σ.L`; it is independent of every document arrangement. Consequently the read succeeds and returns the complete structure even for an *orphaned* link — one whose endpoint content is currently arranged in no document, so that resolving its endsets would yield nothing. The link's structure persists unconditionally (L12; LP13 of ASN-0098), and the read surfaces it unconditionally.

---

## RL-WF — WellFormedness (INV, predicate)

Each returned endset is a finite set of T12-well-formed spans (`Endset = 𝒫_fin(Span)`). Every span `(s, ℓ)` in the result satisfies:

> `Pos(ℓ) ∧ actionPoint(ℓ) ≤ #s`

so each denotes a non-empty contiguous region (ASN-0034). The read can never return a malformed or empty span.

---

## RL-ARITY — ArityTyped (INV, predicate)

The returned value has arity at least three, and its type slot is non-empty:

> `|readlink(a, Σ)| ≥ 3  ∧  readlink(a, Σ).e₃ ≠ ∅`   (from L3, ASN-0043)

The from- and to-endsets may individually be empty — `∅` is a valid endset — so the read may legitimately return an empty connective slot while never returning an empty type slot.

---

## RL-GEN — EndsetGenerality (INV, predicate)

The spans the read returns may point anywhere: across documents, within the link's own home document, or into the link subspace at other links (L4, ASN-0043). The read imposes no confinement on coverage beyond well-formedness; whatever the link recorded, the read returns.

---

## RL-REP — RepresentationIndependence (INV, predicate)

The relationship the read conveys is the *coverage* of each endset, not the particular span decomposition. Two recorded endsets with equal coverage record the same relationship and are interchangeable for every coverage-based use (the type relation of L8; projection independence, LP21 of ASN-0098). A reader interpreting the result should read it as a triple of address-sets-with-roles; the exact spans are one representation of those sets.
