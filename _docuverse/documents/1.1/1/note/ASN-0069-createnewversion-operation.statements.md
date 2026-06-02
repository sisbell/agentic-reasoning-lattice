# ASN-0069 Claim Statements

*Source: ASN-0069-createnewversion-operation.md (revised 2026-05-25) — Extracted: 2026-06-02*

## Definition — ContentSubspaceVPositions

`V_{s_C}(d) = {v ∈ dom(M(d)) : subspace(v) = s_C}`

The content-subspace V-positions of document `d`: the subset of `dom(M(d))` whose subspace component equals `s_C`.

## Definition — Coverage

`coverage(e) := ⋃_{(s, ℓ) ∈ e} span(s, ℓ) ⊆ T`

The set of I-addresses spanned by endset `e`, where each span `(s, ℓ) ∈ e` denotes the address range `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}` from T12 (ASN-0034).

## Definition — Projection

`project(a, i, d, Σ) := {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(Σ.L(a).eᵢ)}`

The V-positions of `d` at state `Σ` whose images at slot `i` of link `a`'s endset structure (per L3, ASN-0047) fall inside the slot's coverage.

## Definition — Discoverability

`discoverable_from(a, d, Σ) := (E i : 1 ≤ i ≤ |Σ.L(a)| : project(a, i, d, Σ) ≠ ∅)`

Link `a` is discoverable from `d` at `Σ` iff some slot of `a` projects to at least one V-position of `d`.

## Definition — CorrespondenceSet

`Corr_g := {v ∈ T : v ∈ dom(M_g(d_op)) ∩ dom(M_g(d_new)) ∧ M_g(d_op)(v) = M_g(d_new)(v)}`

The set of V-positions at which `d_op` and `d_new` correspond at state `Σ_g`.

---

## V0 — ForkOperation (DEF, composite)

A *fork* of `d_src` is a composite state transition `Σ →* Σ'`.

*Composite structure.* The composite is the *uninterrupted* sequence of elementary transitions K.δ + K.μ⁺ + K.ρ × n (where `n = |ran(M'(d_new))|`), or K.δ alone in the empty-source case per V7's extension of J4.

*Precondition.* `d_src ∈ E_doc`. No content-existence precondition is imposed; the empty-source case is normative per V7.

*Effects.* Write `d_op` for the J4 content source operand: `d_op = d_src` on the first fork, `d_op = d_prev` on a subsequent fork. When `V_{s_C}(d_op) ≠ ∅` (the composite is K.δ + K.μ⁺ + K.ρ × n, where `n = |ran(M'(d_new))|`):

```
C' = C                                              (V3)
L' = L                                              (no K.λ or K.μ⁺_L steps)
E' = E ∪ {d_new}                                    (V1)
  where d_new is A_v(d_src)'s next emission:
    d_new = inc(d_src, 1)   on first fork of d_src      (d_op = d_src)
    d_new = inc(d_prev, 0)  on subsequent fork          (d_op = d_prev)
      (d_prev = A_v(d_src)'s most recent prior emission)
M'(d_new)(v) = M(d_op)(v)   for v ∈ V_{s_C}(d_op)   (V4)
M'(d_new)(v) undefined       for v ∉ V_{s_C}(d_op) (V4b; V6 as corollary for link-subspace V-positions)
(A d' : d' ≠ d_new : M'(d') = M(d'))                (V5 for d' = d_src; K.δ + K.μ⁺ + K.ρ frame conditions for d' ≠ d_src ∧ d' ≠ d_new — in particular M'(d_op) = M(d_op))
R' = R ∪ {(a, d_new) : a ∈ ran(M'(d_new))}          (V9)
```

When `V_{s_C}(d_op) = ∅` (the composite is K.δ alone, per V7's extension of J4): `C' = C`, `L' = L`, `E' = E ∪ {d_new}` (where `d_new` is `A_v(d_src)`'s next emission, formula as above), `M'(d_new) = ∅`, `M'(d') = M(d')` for `d' ≠ d_new`, `R' = R`. The operation succeeds.

---

## V1 — NewVersionIdentity (LEMMA, lemma)

A fork of `d_src` produces a new entity `d_new` allocated as `A_v(d_src)`'s next emission per the Allocator hierarchy (ASN-0047):

- *First fork of `d_src`* (when `A_v(d_src)` has emitted no prior version): `d_new = inc(d_src, 1)`, produced by K.δ case (ii) with `k = 1`, `t = d_src`.
- *Subsequent fork of `d_src`* (when `A_v(d_src)` has prior emissions with most recent `d_prev`): `d_new = inc(d_prev, 0)`, produced by K.δ case (ii) with `k = 0`, `t = d_prev`.

In either case `d_new ∈ E'_doc`, `d_new ∉ E_doc` (pre-fork), `Document(d_new)`, and `parent(d_new) = parent(d_src)`. The new entity inherits the source's account-level prefix while extending into a fresh sub-tumbler.

---

## V2 — PrefixEncodedAncestry (LEMMA, lemma)

`d_src ≼ d_new` under the tumbler prefix order. The ancestry relationship is recoverable from `d_new`'s tumbler alone by truncating the trailing extension component; no separate lineage table is consulted.

---

## V3 — ContentStoreInvariance (LEMMA, lemma)

A fork produces no new content. `C' = C` and `dom(C') = dom(C)`.

---

## V3a — AllocationInvariance (LEMMA, lemma)

For every document `d'`, the set of I-addresses allocated under `d'` is unchanged by forking:

`{a ∈ dom(C') : origin(a) = d'} = {a ∈ dom(C) : origin(a) = d'}`

---

## V4 — ArrangementInheritance (LEMMA, lemma)

After any fork of `d_src`, the new document's content-subspace arrangement inherits literally from the content source operand `d_op` (`= d_src` on the first fork, `= d_prev` on a subsequent fork):

`(A v ∈ V_{s_C}(d_op) :: v ∈ dom(M'(d_new)) ∧ M'(d_new)(v) = M(d_op)(v))`

V4 holds unconditionally: the formal universal is vacuously true when `V_{s_C}(d_op) = ∅` (V7's empty-source case, where the quantifier ranges over the empty set) and substantively true when `V_{s_C}(d_op) ≠ ∅` (where K.μ⁺ populates `M'(d_new)` from `V_{s_C}(d_op)` per J4's clause (ii)).

---

## V4a — PositionalIdentity (LEMMA, lemma)

For every V-position `v ∈ V_{s_C}(d_op)`, both `M(d_op)(v)` and `M'(d_new)(v)` are defined, and both equal the same I-address `a ∈ dom(C)`. The V-position `v` is *the same tumbler* in both arrangements. (On the first fork `d_op = d_src`, so this is positional identity between the named source and the fork.)

---

## V4b — DomainEquality (LEMMA, lemma)

In the post-fork state, `dom(M'(d_new)) = V_{s_C}(d_op)` and `V_{s_C}(d_new) = V_{s_C}(d_op)`. The fork's V-position domain is *exactly* the content source's content-subspace V-position set — not merely a superset.

---

## V5 — SourceIsolation (LEMMA, lemma)

For every fork composite `Σ →* Σ'`: `M'(d_src) = M(d_src)`.

---

## V5a — PerDocumentArrangementIndependence (LEMMA, lemma)

Let `K_M = {K.μ⁺, K.μ⁻, K.μ⁺_L}` denote the three arrangement-modifying *elementary* transition kinds of ASN-0047. Each member of `K_M` names a unique *target document* `d_target` in its preconditions; we call an elementary transition `Σ → Σ'` *M-targeted at `d_target`* iff it is an instance of some `K ∈ K_M` whose preconditions name `d_target`. Two clauses:

*(a) Per-elementary-transition frame.* For any single elementary transition `Σ → Σ'` and any document `d* ∈ E_doc`: if the transition is M-targeted at some `d_target ≠ d*`, or is any elementary transition that preserves the arrangement of every pre-existing document of `E_doc` (K.α, K.λ, K.ρ unconditionally; K.δ for every `d' ≠ d_new`, which includes every pre-existing `d* ∈ E_doc` since the K.δ outer precondition `e ∉ E` places `d_new ∉ E` pre-step while `d* ∈ E_doc ⊆ E` pre-step), then `M'(d*) = M(d*)`.

*(b) Per-sequence frame.* For any sequence of valid composite transitions `Σ →* Σ'` and any document `d* ∈ E_doc`: if no elementary step of the sequence is M-targeted at `d*`, then `M'(d*) = M(d*)`.

*Corollary 1 — source–fork isolation.* For `d* = d_src` and any subsequent sequence `Σ' →* Σ''` after the fork in which no step is M-targeted at `d_src`: `M''(d_src) = M'(d_src)`. Symmetric for `d* = d_new`.

*Corollary 2 — pairwise independence.* For any two distinct documents `d¹, d² ∈ E_doc` and any subsequent sequence `Σ' →* Σ''` in which no step is M-targeted at `d¹`: `M''(d¹) = M'(d¹)`.

---

## V6 — SubspaceSelectivity (LEMMA, lemma)

A fork transfers only the source's content-subspace arrangement. The new document's link subspace is empty in the post-fork state:

`V_{s_L}(d_new) = ∅` (in `Σ'`, the post-fork state)

---

## V6a — LinkDiscoverabilityInheritance (LEMMA, lemma)

For every link `a ∈ dom(Σ.L)`, after the fork composite `Σ →* Σ'`:

(i) `Σ'.L(a) = Σ.L(a)` — the link's endsets persist across the composite.

(ii) `project(a, i, d_src, Σ') = project(a, i, d_src, Σ)` for every slot `i` — the source's projection is unchanged.

(iii) `project(a, i, d_op, Σ) ∩ V_{s_C}(d_op) = project(a, i, d_new, Σ')` for every slot `i` — the fork's projection equals the content source `d_op`'s content-subspace-restricted projection (on a first fork `d_op = d_src`).

The link store is unchanged, the named source `d_src`'s discoverability is preserved (ii), and the fork inherits the content source `d_op`'s content-subspace projection witnesses (iii).

---

## V7 — EmptySourceBehavior (LEMMA, lemma)

A fork of `d_src` with `V_{s_C}(d_op) = ∅` reduces to K.δ alone, producing a new entity `d_new ∈ E'_doc` with `M'(d_new) = ∅` and `R' = R`. The operation succeeds; the fork is itself an empty document, eligible for subsequent insertion or further forking.

---

## V8 — PositionalCorrespondence (LEMMA, lemma)

Let `V_{s_C}(d_op)` denote the content-subspace V-positions of the content source operand `d_op` — equal in the pre-fork state `Σ` and the post-fork state `Σ'` because the fork does not modify `M(d_op)`. For every `v ∈ V_{s_C}(d_op)`: `v ∈ dom(M'(d_new))` and `M'(d_op)(v) = M'(d_new)(v)`.

---

## V8b — CorrespondenceStateBounded (LEMMA, lemma)

Let `Σ' →* Σ_g` be any sequence of valid composite transitions from the post-fork state `Σ'`. Let `F := V_{s_C}(d_op)|_{Σ'}` denote the fork-time content-subspace witness set (fixed by the post-fork state), and define the *time-indexed fork-time witness set*

`Π_g := F ∩ Corr_g`

where `Corr_g := {v ∈ T : v ∈ dom(M_g(d_op)) ∩ dom(M_g(d_new)) ∧ M_g(d_op)(v) = M_g(d_new)(v)}`.

Two facts hold about `Π_g`:

(i) *Set bound.* `Π_g ⊆ F` at every reachable `Σ_g`.

(ii) *Initial coverage.* At the post-fork state itself, `Π_{Σ'} = F`.

K.α, K.λ, K.ρ, K.δ, K.μ⁺_L, and third-document K.μ⁻/K.μ⁺ (and the K.μ~ composite they form) each leave `Π_g` invariant. `Π_g` shifts only via K.μ⁻ or K.μ⁺ steps — whether standalone or arising as the two constituents of a K.μ~ composite — acting on `d_op` or `d_new`.

---

## V8c — CorrespondenceSymmetric (LEMMA, lemma)

The relationship V8 records is between two documents; it does not distinguish "source" from "fork." After the fork is complete, both `d_src` and `d_new` are documents in `E_doc`, and the set of corresponding V-positions `{v ∈ T : v ∈ dom(M'(d_src)) ∩ dom(M'(d_new)) ∧ M'(d_src)(v) = M'(d_new)(v)}` is invariant under swap of the two documents.

---

## V9 — ForkProvenance (LEMMA, lemma)

After a fork of `d_src`:

`(A a : a ∈ ran(M'(d_new)) : (a, d_new) ∈ R')`

---

## V9a — ProvenanceNoDerivationPath (LEMMA, lemma)

For every `(a, d_new) ∈ R'` recorded by a fork, the relation does not distinguish whether `d_new` acquired `a` via fork from `d_src`, via transclusion from a third document also containing `a`, or via direct allocation. The relation reports *who has it*; the I-address tells you *who made it*; the parent prefix tells you *who you came from*. These three pieces of information are recoverable independently from the I-address and the fork's prefix structure.

---

## V9b — FreshForksExternalIAddresses (LEMMA, lemma)

For every `(a, d_new) ∈ R'` recorded by a fork, `origin(a) ≠ d_new`.

---

## V10 — SiblingIndependence (LEMMA, lemma)

Let `Σ →* Σ¹` be a fork of `d_src` producing `d_new¹`, and let `Σ_g →* Σ²` be any later fork of the same `d_src` producing `d_new²`, where `Σ_g` is any state reachable from `Σ¹` by a finite sequence of valid composite transitions. The two forks are independent in three senses:

(a) *Distinct identities.* `d_new¹ ≠ d_new²`.

(b) *Independent content shares.* Each sibling fork inherits content from its own content source operand `d_op` (J4) *at the moment of that fork*. `d_new¹` is the first fork of `d_src`, so its `d_op¹ = d_src`, and it reads `M(d_src)` at `Σ`. `d_new²` is a subsequent fork of `d_src`, so its `d_op² = max(dom(A_v(d_src)))` at `Σ_g` — and it reads `M(d_op²)` at `Σ_g`. Their inherited V→I mappings live in separate arrangements `M¹(d_new¹)` and `M²(d_new²)`. By V5a Corollary 2: modifications M-targeted at `d_new¹` preserve `M(d_new²)`, and modifications M-targeted at `d_new²` preserve `M(d_new¹)`.

(c) *Independent provenance records.* `R²` contains both `(a, d_new¹)` and `(a, d_new²)` for shared I-addresses, but these are distinct pairs (since `d_new¹ ≠ d_new²` by (a)).

---

## V10a — TimeSensitivityOfDerivation (LEMMA, lemma)

A fork in state `Σ` inherits `V_{s_C}(d_op)` and the mappings `M(d_op)|_{V_{s_C}(d_op)}` of its content source operand as they stand in `Σ`, not as they stood at any prior or subsequent state. Two forks of the same source at different times may produce different new versions, reflecting whatever state changes to the operands (and, for subsequent forks, whatever change of operand from `d_src` to `d_prev`) occurred between them.

---

## V11 — TransitiveIdentity (LEMMA, lemma)

For every chain length `k ≥ 1` and every chain of forks `d_src → d¹_new → d²_new → ... → d^k_new` starting from `Σ` (with `d⁰_new := d_src`), where each step `dⁱ⁻¹_new → dⁱ_new` is a fork composite that is the *first* fork of its immediate source `d^{i-1}_new` — so that step `i`'s J4 content source operand `d_op` equals `d^{i-1}_new`, and V4 at step `i` reads `M(d^{i-1}_new)` — and *each step's source has its content-subspace arrangement unchanged between the prior step's post-state and the current step's pre-state* — that is, for every `1 ≤ i ≤ k`, `V_{s_C}(d^{i-1}_new)` is the same set in the post-state of step `i − 1` and the pre-state of step `i`, and for every `v` in this set, `M(d^{i-1}_new)(v)` is the same value in both states (with the convention that at `i = 1`, "step 0's post-state" denotes `Σ` itself, so the premise at `i = 1` is satisfied trivially by reflexivity) — the I-addresses inherited by `d^k_new` are the same I-addresses that `d_src` held at `Σ`:

For every `v ∈ V_{s_C}(d_src)` evaluated at `Σ`: `v ∈ dom(M^k(d^k_new))` at the post-state of step `k`, and `M^k(d^k_new)(v)` at the post-state of step `k` equals `M(d_src)(v)` at `Σ`.

---

## V11a — AncestryComposition (LEMMA, lemma)

The prefix relation chains: `d_src ≼ d¹_new ≼ d²_new ≼ ... ≼ d^k_new`. Each step `dⁱ⁻¹_new → dⁱ_new` extends the tumbler by exactly one component at position `#dⁱ⁻¹_new + 1` whose value is `1 + j`, where `j ≥ 0` is the *subsequent-emission count* of `A_v(dⁱ⁻¹_new)` immediately prior to step `i`'s firing — `j = 0` covers V1's first-fork sub-case (`inc(dⁱ⁻¹_new, 1)`, placing value `1` at position `#dⁱ⁻¹_new + 1` by TA5(d)) and `j ≥ 1` covers V1's subsequent-fork sub-case (`inc(d_prev, 0)` for `d_prev` the most recent prior emission of `A_v(dⁱ⁻¹_new)`, with each successive `inc(·, 0)` strictly incrementing the component at position `#dⁱ⁻¹_new + 1` by TA5(c), so the `j`-th subsequent emission has value `1 + j` at this position).

The full chain is recoverable from `d^k_new`'s tumbler alone by reading prefixes of strictly increasing length: the prefix of `d^k_new` of length `#d_src + i` is exactly `dⁱ_new` for every `0 ≤ i ≤ k` (with `d⁰_new := d_src`).

---

## V12 — JointPermanence (LEMMA, lemma)

After a fork, both `d_src` and `d_new` and all their inherited I-addresses are permanent. For every reachable state subsequent to the fork:

(a) `d_src ∈ E'_doc ∧ d_new ∈ E'_doc` (P1)

(b) `(A a ∈ ran(M'(d_new)) :: a ∈ dom(C''))` for every subsequent state `Σ''` (P0)

(c) `(A a ∈ ran(M'(d_new)) :: (a, d_new) ∈ R'')` for every subsequent state `Σ''` (P2 applied to the post-fork records of V9)

(d) `(A a ∈ ran(M'(d_new)) :: (a, d_op) ∈ R'')` — provenance records for the *content source operand* `d_op` (`= d_src` on the first fork, `= d_prev` on a subsequent fork) are also permanent. By V4b, `dom(M'(d_new)) = V_{s_C}(d_op)`, and by V4, `M'(d_new)(v) = M(d_op)(v)` for every `v ∈ V_{s_C}(d_op)`, composing to `ran(M'(d_new)) = ran(M(d_op)|_{V_{s_C}(d_op)})`. P4★ applied at `Σ` gives `(a, d_op) ∈ R`; P2 carries the pair forward into every subsequent reachable state `Σ''`.
