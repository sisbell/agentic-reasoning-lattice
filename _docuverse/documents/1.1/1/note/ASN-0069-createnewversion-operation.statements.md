# ASN-0069 Claim Statements

*Source: ASN-0069-createnewversion-operation.md (revised 2026-05-25) — Extracted: 2026-05-25*

## Definition — ContentSubspacePositions

`V_{s_C}(d) = {v ∈ dom(M(d)) : subspace(v) = s_C}` — the content-subspace V-positions of document `d`. When `V_{s_C}(d) ≠ ∅`, by D-SEQ★: `V_{s_C}(d) = {[s_C, 1, ..., 1, k] : 1 ≤ k ≤ n_{s_C}}` for some `n_{s_C} ≥ 1`, all positions sharing common depth `m_{s_C}`.

## Definition — LinkSubspacePositions

`V_{s_L}(d) = {v ∈ dom(M(d)) : subspace(v) = s_L}` — the link-subspace V-positions of document `d`.

## Definition — CorrespondenceSet

`Corr_g := {v ∈ T : v ∈ dom(M_g(d_src)) ∩ dom(M_g(d_new)) ∧ M_g(d_src)(v) = M_g(d_new)(v)}`

The set of V-positions at which `d_src` and `d_new` correspond at state `Σ_g`.

## Definition — ForkTimeWitnessSet

`F := V_{s_C}(d_src)|_{Σ'}` — the fork-time content-subspace witness set, fixed by the post-fork state `Σ'`.

`Π_g := F ∩ Corr_g` — the time-indexed fork-time witness set: V-positions that existed in `d_src`'s content subspace at fork-time *and* still witness correspondence at `Σ_g`.

---

## V0 — ForkOperation (DEF, definition)

A *fork* of `d_src` is a composite state transition `Σ →* Σ'`.

*Precondition.* `d_src ∈ E_doc`. No content-existence precondition is imposed; the empty-source case is normative per V7.

*Composite structure.* The composite is the *uninterrupted* sequence of elementary transitions K.δ + K.μ⁺ + K.ρ × n (where `n = |ran(M'(d_new))|`), or K.δ alone in the empty-source case per V7's extension of J4.

*Effects when `V_{s_C}(d_src) ≠ ∅`* (the composite is K.δ + K.μ⁺ + K.ρ × n, where `n = |ran(M'(d_new))|`):

```
C' = C                                              (V3)
L' = L                                              (no K.λ or K.μ⁺_L steps)
E' = E ∪ {d_new}                                    (V1)
  where d_new is A_v(d_src)'s next emission:
    d_new = inc(d_src, 1)   on first fork of d_src
    d_new = inc(d_prev, 0)  on subsequent fork
      (d_prev = A_v(d_src)'s most recent prior emission)
M'(d_new)(v) = M(d_src)(v)  for v ∈ V_{s_C}(d_src)  (V4)
M'(d_new)(v) undefined       for v ∉ V_{s_C}(d_src)  (V4b; V6 as corollary for link-subspace V-positions)
(A d' : d' ≠ d_new : M'(d') = M(d'))                (V5 for d' = d_src; K.δ + K.μ⁺ + K.ρ frame conditions for d' ≠ d_src ∧ d' ≠ d_new)
R' = R ∪ {(a, d_new) : a ∈ ran(M'(d_new))}          (V9)
```

*Effects when `V_{s_C}(d_src) = ∅`* (the composite is K.δ alone, per V7's extension of J4): `C' = C`, `L' = L`, `E' = E ∪ {d_new}` (where `d_new` is `A_v(d_src)`'s next emission, formula as above), `M'(d_new) = ∅`, `M'(d') = M(d')` for `d' ≠ d_new`, `R' = R`.

---

## V1 — NewVersionIdentity (LEMMA, lemma)

A fork of `d_src` produces a new entity `d_new` allocated as `A_v(d_src)`'s next emission per the Allocator hierarchy (ASN-0047):

- *First fork of `d_src`* (when `A_v(d_src)` has emitted no prior version): `d_new = inc(d_src, 1)`, produced by K.δ case (ii) with `k = 1`, `t = d_src`.
- *Subsequent fork of `d_src`* (when `A_v(d_src)` has prior emissions with most recent `d_prev`): `d_new = inc(d_prev, 0)`, produced by K.δ case (ii) with `k = 0`, `t = d_prev`.

In either case `d_new ∈ E'_doc`, `d_new ∉ E_doc` (pre-fork), `IsDocument(d_new)`, and `parent(d_new) = parent(d_src)`.

---

## V2 — PrefixEncodedAncestry (LEMMA, lemma)

`d_src ≼ d_new` under the tumbler prefix order. The ancestry relationship is recoverable from `d_new`'s tumbler alone by truncating the trailing extension component; no separate lineage table is consulted.

---

## V3 — ContentStoreInvariance (INV, predicate)

A fork produces no new content. `C' = C` and `dom(C') = dom(C)`.

---

## V3a — AllocationInvariance (LEMMA, lemma)

For every document `d'`, the set of I-addresses allocated under `d'` is unchanged by forking:

`{a ∈ dom(C') : origin(a) = d'} = {a ∈ dom(C) : origin(a) = d'}`

---

## V4 — ArrangementInheritance (LEMMA, lemma)

After any fork of `d_src`, the new document's content-subspace arrangement satisfies:

`(A v ∈ V_{s_C}(d_src) :: v ∈ dom(M'(d_new)) ∧ M'(d_new)(v) = M(d_src)(v))`

V4 holds unconditionally: the formal universal is vacuously true when `V_{s_C}(d_src) = ∅` and substantively true when `V_{s_C}(d_src) ≠ ∅`.

---

## V4a — PositionalIdentity (LEMMA, lemma)

For every V-position `v ∈ V_{s_C}(d_src)`, both `M(d_src)(v)` and `M'(d_new)(v)` are defined, and both equal the same I-address `a ∈ dom(C)`. The V-position `v` is *the same tumbler* in both arrangements.

---

## V4b — DomainEquality (LEMMA, lemma)

In the post-fork state, `dom(M'(d_new)) = V_{s_C}(d_src)` and `V_{s_C}(d_new) = V_{s_C}(d_src)`. The fork's V-position domain is *exactly* the source's content-subspace V-position set — not merely a superset.

---

## V5 — SourceIsolation (LEMMA, lemma)

For every fork composite `Σ →* Σ'`: `M'(d_src) = M(d_src)`.

---

## V5a — BidirectionalIndependence (LEMMA, lemma)

For any subsequent state transition `Σ' →* Σ''` after the fork:

`(M''(d_src) ≠ M'(d_src) ⟹ M''(d_new) = M'(d_new))` *if the modification targets `d_src`*

`(M''(d_new) ≠ M'(d_new) ⟹ M''(d_src) = M'(d_src))` *if the modification targets `d_new`*

---

## V6 — SubspaceSelectivity (LEMMA, lemma)

A fork transfers only the source's content-subspace arrangement. The new document's link subspace is empty in the post-fork state:

`V_{s_L}(d_new) = ∅` (in `Σ'`, the post-fork state)

---

## V6a — LinkDiscoverabilityInheritance (LEMMA, lemma)

For any I-address `a ∈ ran(M'(d_new))`, the set of links `ℓ ∈ dom(L)` whose endsets reference `a` is the same set of links discoverable from `a` via `d_src`'s arrangement. The link store `L` is unchanged by the fork (its frame condition under K.δ + K.μ⁺ + K.ρ is `L' = L`), so the link-discovery relation grounded in I-address identity is preserved.

---

## V7 — EmptySourceBehavior (LEMMA, lemma)

A fork of `d_src` with `V_{s_C}(d_src) = ∅` reduces to K.δ alone, producing a new entity `d_new ∈ E'_doc` with `M'(d_new) = ∅` and `R' = R`. The operation succeeds; the fork is itself an empty document, eligible for subsequent insertion or further forking.

---

## V8 — PositionalCorrespondence (LEMMA, lemma)

Let `V_{s_C}(d_src)` denote the content-subspace V-positions of `d_src` — equal in the pre-fork state `Σ` and the post-fork state `Σ'` because V5 establishes `M'(d_src) = M(d_src)`. For every `v ∈ V_{s_C}(d_src)`: `v ∈ dom(M'(d_new))` and `M'(d_src)(v) = M'(d_new)(v)`.

---

## V8a — CorrespondencePersistenceUnderGrowth (LEMMA, lemma)

Subsequent K.α allocations (extending `C`) leave every arrangement unchanged — K.α's frame condition `(A d :: M'(d) = M(d))` (ASN-0047) preserves `M(d_src)` and `M(d_new)` across each K.α step. Since V8's correspondence is an equality of arrangement values `M(d_src)(v) = M(d_new)(v)`, and neither side of the equality is modified by K.α, V8's correspondence between `d_src` and `d_new` over the V-positions present at fork time is preserved across every K.α step as long as those V-positions remain in both arrangements.

---

## V8b — CorrespondenceStateRelative (LEMMA, lemma)

Let `Σ' →* Σ_g` be any sequence of valid composite transitions from the post-fork state `Σ'`. The set of V-positions at which `d_src` and `d_new` correspond at `Σ_g` is:

`Corr_g := {v ∈ T : v ∈ dom(M_g(d_src)) ∩ dom(M_g(d_new)) ∧ M_g(d_src)(v) = M_g(d_new)(v)}`

Let `F := V_{s_C}(d_src)|_{Σ'}` denote the fork-time content-subspace witness set (fixed by the post-fork state), and define the *time-indexed fork-time witness set*:

`Π_g := F ∩ Corr_g`

Two facts hold about `Π_g`:

(i) *Set bound.* `Π_g ⊆ F` at every reachable `Σ_g`. The witness set never grows beyond the fork-time set, since `F` is fixed by the post-fork state and `Π_g` is its intersection with `Corr_g`.

(ii) *Initial coverage.* At the post-fork state itself, `Π_{Σ'} = F`. V8 supplies `F ⊆ Corr_{Σ'}`, so `Π_{Σ'} = F ∩ Corr_{Σ'} = F`.

---

## V8c — CorrespondenceSymmetric (LEMMA, lemma)

The relationship V8 records is between two documents; it does not distinguish "source" from "fork." After the fork is complete, both `d_src` and `d_new` are documents in `E_doc`, and the set of corresponding V-positions:

`{v ∈ T : v ∈ dom(M'(d_src)) ∩ dom(M'(d_new)) ∧ M'(d_src)(v) = M'(d_new)(v)}`

is invariant under swap of the two documents.

---

## V9 — ForkProvenance (LEMMA, lemma)

After a fork of `d_src`:

`(A a : a ∈ ran(M'(d_new)) : (a, d_new) ∈ R')`

---

## V9a — ProvenanceNoDerivationPath (LEMMA, lemma)

For every `(a, d_new) ∈ R'` recorded by a fork, the relation does not distinguish whether `d_new` acquired `a` via fork from `d_src`, via transclusion from a third document also containing `a`, or via direct allocation (if `origin(a) = d_new`, which cannot occur in a fresh fork since `d_new ∉ E_doc` pre-fork). The relation reports *who has it*; the I-address tells you *who made it*; the parent prefix tells you *who you came from*. These three pieces of information are recoverable independently from the I-address and the fork's prefix structure.

---

## V10 — SiblingIndependence (LEMMA, lemma)

Let `Σ →* Σ¹` be a fork of `d_src` producing `d_new¹`, and let `Σ_g →* Σ²` be any later fork of the same `d_src` producing `d_new²`, where `Σ_g` is any state reachable from `Σ¹` by a finite sequence of valid composite transitions. The two forks are independent in three senses:

(a) *Distinct identities.* `d_new¹ ≠ d_new²`.

(b) *Independent content shares.* Both `d_new¹` and `d_new²` inherit content from `M(d_src)` *at the moment of each respective fork* — `d_new¹` reads `M(d_src)` at `Σ`, and `d_new²` reads `M(d_src)` at `Σ_g`. Their inherited V→I mappings live in separate arrangements `M¹(d_new¹)` and `M²(d_new²)`. By V5a, modifications to one do not propagate to the other.

(c) *Independent provenance records.* `R²` contains both `(a, d_new¹)` and `(a, d_new²)` for shared I-addresses, but these are distinct pairs (since `d_new¹ ≠ d_new²` by (a)).

---

## V10a — TimeSensitivityOfDerivation (LEMMA, lemma)

A fork in state `Σ` inherits `V_{s_C}(d_src)` and the mappings `M(d_src)|_{V_{s_C}(d_src)}` as they stand in `Σ`, not as they stood at any prior or subsequent state. Two forks of the same source at different times may produce different new versions, reflecting whatever state changes to `M(d_src)` occurred between them.

---

## V11 — TransitiveIdentity (LEMMA, lemma)

For every chain of forks `d_src → d¹_new → d²_new → ... → d^k_new` where each step `dⁱ⁻¹_new → dⁱ_new` is a fork composite (with `d⁰_new := d_src`) and *each step's source has its content-subspace arrangement unchanged between the prior step's post-state and the current step's pre-state* — that is, for every `1 ≤ i ≤ k`, `V_{s_C}(d^{i-1}_new)` is the same set in the post-state of step `i − 1` and the pre-state of step `i`, and for every `v` in this set, `M(d^{i-1}_new)(v)` is the same value in both states — the I-addresses inherited by `d^k_new` are the same I-addresses as in `d_src`'s arrangement:

for every `v ∈ V_{s_C}(d_src)`, `v ∈ dom(M^k(d^k_new))` and `M^k(d^k_new)(v) = M(d_src)(v)`.

---

## V11a — AncestryComposition (LEMMA, lemma)

The prefix relation chains: `d_src ≼ d¹_new ≼ d²_new ≼ ... ≼ d^k_new`. Every fork in the chain is recoverable from the prefix structure of `d^k_new`'s tumbler alone, by reading off the successive extensions added by each `inc(·, 1)`.

---

## V12 — JointPermanence (LEMMA, lemma)

After a fork, both `d_src` and `d_new` and all their inherited I-addresses are permanent. For every reachable state subsequent to the fork:

(a) `d_src ∈ E'_doc ∧ d_new ∈ E'_doc` (T8, P1)

(b) `(A a ∈ ran(M'(d_new)) :: a ∈ dom(C''))` for every subsequent state `Σ''` (P0)

(c) `(A a ∈ ran(M'(d_new)) :: (a, d_new) ∈ R'')` for every subsequent state `Σ''` (P2 applied to the post-fork records of V9)

(d) `(A a ∈ ran(M'(d_new)) :: (a, d_src) ∈ R'')` — provenance records for the source are also permanent.
