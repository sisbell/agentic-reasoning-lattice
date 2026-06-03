# ASN-0069 Claim Statements

*Source: ASN-0069-createnewversion-operation.md (revised 2026-05-25) — Extracted: 2026-06-03*

## V0 — ForkOperation (DEF, composite)

A *fork* of `d_src` is a composite state transition `Σ →* Σ'`.

*Composite structure.* The composite is the contiguous K.δ + K.μ⁺ + K.ρ × n sequence of J4 (where `n = |ran(M'(d_new))|`), or K.δ alone in the empty-source case per V7's extension of J4.

*Precondition.* `d_src ∈ E_doc`. No content-existence precondition is imposed; the empty-source case is normative per V7.

*Effects.* When `V_{s_C}(d_op) ≠ ∅` (the composite is K.δ + K.μ⁺ + K.ρ × n, where `n = |ran(M'(d_new))|`):

```
C' = C                                              (V3)
L' = L                                              (no K.λ or K.μ⁺_L steps)
E' = E ∪ {d_new}                                    (V1)
  where d_new is A_v(d_src)'s next emission:
    d_new = inc(d_src, 1)   on first fork of d_src
    d_new = inc(d_prev, 0)  on subsequent fork
      (d_prev = A_v(d_src)'s most recent prior emission)
M'(d_new)(v) = M(d_op)(v)   for v ∈ V_{s_C}(d_op)   (V4)
M'(d_new)(v) undefined       for v ∉ V_{s_C}(d_op) (V4b; V6 as corollary for link-subspace V-positions)
(A d' : d' ≠ d_new : M'(d') = M(d'))                (V5 for d' = d_src; K.δ + K.μ⁺ + K.ρ frame conditions for d' ≠ d_src ∧ d' ≠ d_new — in particular M'(d_op) = M(d_op))
R' = R ∪ {(a, d_new) : a ∈ ran(M'(d_new))}          (V9; set equality, verified below)
```

The set `V_{s_C}(d_op)` (and `M(d_op)(v)` for `v` in it) is evaluated at the pre-state `Σ`; the per-document frame guarantee `M'(d_op) = M(d_op)` pins the same value in `Σ'`.

The K.ρ phase is `n` elementary K.ρ invocations (one per `a ∈ ran(M'(d_new))`), each recording a single `(a, d_new)` pair per K.ρ's definition (ASN-0047). The set-builder `{(a, d_new) : a ∈ ran(M'(d_new))}` denotes the cumulative effect of all `n` invocations on `R`.

When `V_{s_C}(d_op) = ∅` (the composite is K.δ alone, per V7's extension of J4): `C' = C`, `L' = L`, `E' = E ∪ {d_new}` (where `d_new` is `A_v(d_src)`'s next emission, formula as above), `M'(d_new) = ∅`, `M'(d') = M(d')` for `d' ≠ d_new`, `R' = R`. The operation succeeds.

---

## V1 — NewVersionIdentity (LEMMA, property)

A fork of `d_src` produces a new entity `d_new` allocated as `A_v(d_src) = S(d_src, 1)`'s next emission `next(s.B, d_src, 1)` (NextAddress, ASN-0040; equivalently the Allocator-hierarchy frontier of ASN-0047):

- *First fork of `d_src`* (when `A_v(d_src)` has emitted no prior version): `d_new = inc(d_src, 1)`, produced by K.δ case (ii) with `k = 1`, `t = d_src`.
- *Subsequent fork of `d_src`* (when `A_v(d_src)` has prior emissions with most recent `d_prev`): `d_new = inc(d_prev, 0)`, produced by K.δ case (ii) with `k = 0`, `t = d_prev`.

In either case `d_new ∈ E'_doc`, `d_new ∉ E_doc` (pre-fork), `Document(d_new)`, and `parent(d_new) = parent(d_src)`.

---

## V2 — PrefixEncodedAncestry (LEMMA, property)

`d_src ≼ d_new` under the tumbler prefix order. The ancestry relationship is recoverable from `d_new`'s tumbler alone by truncating the trailing extension component; no separate lineage table is consulted.

---

## V3 — ContentStoreInvariance (INV, predicate)

A fork produces no new content. `C' = C` and `dom(C') = dom(C)`.

---

## V3a — AllocationInvariance (LEMMA, property)

For every document `d'`, the set of I-addresses allocated under `d'` is unchanged by forking: `{a ∈ dom(C') : origin(a) = d'} = {a ∈ dom(C) : origin(a) = d'}`.

---

## V4 — ArrangementInheritance (LEMMA, property)

After any fork of `d_src`, the new document's content-subspace arrangement inherits literally from the content source operand `d_op`:

`(A v ∈ V_{s_C}(d_op) :: v ∈ dom(M'(d_new)) ∧ M'(d_new)(v) = M(d_op)(v))`

The universal is vacuous on V0's empty-source branch (`V_{s_C}(d_op) = ∅`); on the non-empty branch K.μ⁺ populates `M'(d_new)` from `V_{s_C}(d_op)` per J4's clause (ii).

---

## V4b — DomainEquality (LEMMA, property)

In the post-fork state, `dom(M'(d_new)) = V_{s_C}(d_op)` and `V_{s_C}(d_new) = V_{s_C}(d_op)`. The fork's V-position domain is *exactly* the content source's content-subspace V-position set — not merely a superset.

---

## V5 — SourceIsolation (LEMMA, property)

For every fork composite `Σ →* Σ'`: `M'(d_src) = M(d_src)`. V5 is V5a at `d* = d_src`: `d_src ∈ Σ.E_doc` by V0's precondition, and the fork composite has no step M-targeted at `d_src` (its only K.μ⁺ step targets `d_new ≠ d_src`).

---

## V5a — PerDocumentArrangementIndependence (LEMMA, property)

Each arrangement-modifying transition of ASN-0047 (K.μ⁺, K.μ⁻, K.μ⁺_L, and the K.μ~ composite) names a single *target document* in its preconditions; we call a step *M-targeted at `d*`* iff its target is `d*`. For any sequence of valid composite transitions `Σ →* Σ'` and any document `d* ∈ Σ.E_doc` (in the initial state): if no step of the sequence is M-targeted at `d*`, then `M'(d*) = M(d*)`.

---

## V6 — SubspaceSelectivity (LEMMA, property)

A fork transfers only the source's content-subspace arrangement. The new document's link subspace is empty in the post-fork state:

`V_{s_L}(d_new) = ∅` (in `Σ'`, the post-fork state)

---

## V6a — LinkStorePersistence (LEMMA, property)

For every link `a ∈ dom(Σ.L)`, after the fork composite `Σ →* Σ'`, `Σ'.L(a) = Σ.L(a)` — the link store is unchanged.

The consequence for the fork is immediate. By V4 the inherited V-positions of `d_new` carry exactly the I-addresses they carried in the content source `d_op`; combined with `Σ'.L = Σ.L`, any link whose endsets reference an inherited I-address still references content that `d_new`'s arrangement now holds, exactly as it does for `d_op`.

---

## V7 — EmptySourceBehavior (LEMMA, property)

A fork of `d_src` with `V_{s_C}(d_op) = ∅` reduces to K.δ alone, producing a new entity `d_new ∈ E'_doc` with `M'(d_new) = ∅` and `R' = R`. The operation succeeds; the fork is itself an empty document, eligible for subsequent insertion or further forking.

---

## V8 — PositionalCorrespondence (LEMMA, corollary)

For every `v ∈ V_{s_C}(d_op)`: `v ∈ dom(M'(d_new))` and `M'(d_op)(v) = M'(d_new)(v)`. The per-document frame gives `M'(d_op) = M(d_op)` (the K.μ⁺ phase targets only `d_new`, and `d_op ≠ d_new`), and V4 gives `v ∈ dom(M'(d_new))` with `M'(d_new)(v) = M(d_op)(v)`, so `M'(d_op)(v) = M(d_op)(v) = M'(d_new)(v)`.

---

## V8c — CorrespondenceSymmetry (LEMMA, corollary)

The corresponding-position set `{v ∈ T : v ∈ dom(M'(d_op)) ∩ dom(M'(d_new)) ∧ M'(d_op)(v) = M'(d_new)(v)}` is defined by `∩` and `=`, both symmetric, so it is invariant under swap of `d_op` and `d_new`. V8 records a relationship between two documents in `E_doc`; it does not distinguish "source" from "fork."

---

## V8d — PerpetualCorrespondence (LEMMA, property)

Let `Σ →* Σ'` be a fork and let `Σ''` be any state reachable from the post-fork state `Σ'` such that no step on the path `Σ' →* Σ''` is M-targeted at `d_op` and none is M-targeted at `d_new`. Then for every `v ∈ V_{s_C}(d_op)` (evaluated at `Σ`):

`M''(d_op)(v) = M''(d_new)(v)` — the corresponding V-positions still carry equal I-addresses.

---

## V9 — ForkProvenance (LEMMA, property)

After a fork of `d_src`:

`(A a : a ∈ ran(M'(d_new)) : (a, d_new) ∈ R')`

---

## V9a — ProvenanceContainmentOnly (LEMMA, property)

A fork's K.ρ phase adds pairs `(a, d_new)` recording that `d_new` came to contain `a`, but no edge connecting that acquisition to `d_src`, to a prior version, or to any third document that also contained `a`. The provenance relation is therefore silent on *whether* `d_new` obtained `a` by fork or by transclusion.

---

## V9b — ExternallyAllocatedInheritance (LEMMA, property)

For every `(a, d_new) ∈ R'` recorded by a fork, `origin(a) ≠ d_new`.

---

## V10 — SiblingIndependence (LEMMA, property)

Let `Σ →* Σ¹` be a fork of `d_src` producing `d_new¹`, and let `Σ_g →* Σ²` be any later fork of the same `d_src` producing `d_new²`, where `Σ_g` is any state reachable from `Σ¹` by a finite sequence of valid composite transitions (the intervening transitions may be of any kind on any documents, including further forks of `d_src` itself). The two forks are independent in three senses:

(a) *Distinct identities.* `d_new¹ ≠ d_new²`.

(b) *Independent content shares.* Each sibling fork inherits content from its own content source operand `d_op` (J4) *at the moment of that fork*. `d_new¹`'s operand `d_op¹` is fixed by V1's fork-dispatch at `Σ`: `d_op¹ = d_src` when `d_new¹` is the first fork of `d_src`, and `d_op¹ = max(dom(A_v(d_src)))` (a prior version) otherwise; either way it reads `M(d_op¹)` at `Σ`. `d_new²`'s operand `d_op²` is fixed by V1's dispatch at `Σ_g`: since `d_new¹ ∈ E` at `Σ_g` by (a)'s argument, `A_v(d_src)` already has a frontier, so `d_new²` is necessarily a subsequent fork and `d_op² = max(dom(A_v(d_src)))` — the most recent prior version emitted by `A_v(d_src)` at `Σ_g`. Their inherited V→I mappings live in separate arrangements `M¹(d_new¹)` and `M²(d_new²)`. Restricted to any sequence beginning at `Σ²`, modifications M-targeted at `d_new¹` preserve `M(d_new²)`, and vice versa.

(c) *Independent provenance records.* `R²` contains both `(a, d_new¹)` and `(a, d_new²)` for shared I-addresses, but these are distinct pairs (since `d_new¹ ≠ d_new²` by (a)).

---

## V10a — TimeSensitivityOfDerivation (LEMMA, property)

A fork in state `Σ` inherits `V_{s_C}(d_op)` and the mappings `M(d_op)|_{V_{s_C}(d_op)}` of its content source operand as they stand in `Σ`, not as they stood at any prior or subsequent state. Two forks of the same source at different times may produce different new versions, reflecting whatever state changes to the operands (and, for subsequent forks, whatever change of operand from `d_src` to `d_prev`) occurred between them.

---

## V11 — TransitiveForkChainIdentity (LEMMA, property)

Let `Σ` denote the pre-state of the first fork — the chain's initial state. For every chain length `k ≥ 1` and every chain of forks `d_src → d¹_new → d²_new → ... → d^k_new` starting from `Σ` (with `d⁰_new := d_src`) satisfying two premises —

- *(first-fork chain)* each step `dⁱ⁻¹_new → dⁱ_new` is a fork composite that is the *first* fork of its immediate source `d^{i-1}_new`;
- *(per-step unedited source)* for every `1 ≤ i ≤ k`, `V_{s_C}(d^{i-1}_new)` is the same set in the post-state of step `i − 1` and the pre-state of step `i`, and for every `v` in this set, `M(d^{i-1}_new)(v)` is the same value in both states —

the I-addresses inherited by `d^k_new` are the same I-addresses that `d_src` held at `Σ`: for every `v ∈ V_{s_C}(d_src)` evaluated at `Σ`, `v ∈ dom(M^k(d^k_new))` at the post-state of step `k`, and the value `M^k(d^k_new)(v)` at the post-state of step `k` equals the value `M(d_src)(v)` at `Σ`.

---

## V11a — AncestryComposition (LEMMA, property)

The prefix relation chains: `d_src ≼ d¹_new ≼ d²_new ≼ ... ≼ d^k_new`. Each step `dⁱ⁻¹_new → dⁱ_new` is the *first* fork of its immediate source (V11's premise), so by V1 it is `inc(dⁱ⁻¹_new, 1)` — K.δ case (ii) at `k = 1` — extending the tumbler by exactly one component at position `#dⁱ⁻¹_new + 1` whose value is `1` (TA5(d) at `k = 1`). The full chain is recoverable from `d^k_new`'s tumbler alone by reading prefixes of strictly increasing length: the prefix of `d^k_new` of length `#d_src + i` is exactly `dⁱ_new` for every `0 ≤ i ≤ k` (with `d⁰_new := d_src`).

---

## V12 — JointPermanence (LEMMA, property)

After a fork, both `d_src` and `d_new` and all their inherited I-addresses are permanent. For every reachable state subsequent to the fork:

(a) `d_src ∈ E'_doc ∧ d_new ∈ E'_doc` (T8, P1): both documents remain in `E_doc` for all subsequent reachable states; neither can be removed.

(b) `(A a : a ∈ ran(M'(d_new)) : a ∈ dom(C''))` for every subsequent state `Σ''` (P0): every inherited I-address persists in `dom(C)` with unchanged value, regardless of how either document's arrangement evolves.

(c) `(A a ∈ ran(M'(d_new)) :: (a, d_new) ∈ R'')` for every subsequent state `Σ''` (P2, V9): the provenance records added by V9 persist in `R` forever. Even if `d_new`'s owner later deletes `a` from its arrangement (via K.μ⁻), the historical fact `(a, d_new) ∈ R` records that `d_new` once contained `a`.

(d) `(A a ∈ ran(M'(d_new)) :: (a, d_op) ∈ R'')` — provenance records for the *content source operand* `d_op` are also permanent.
