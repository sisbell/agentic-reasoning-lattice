# ASN-0069 Claim Statements

*Source: ASN-0069-createnewversion-operation.md (revised 2026-05-25) — Extracted: 2026-05-27*

## Definition — ContentSubspaceVPositions

`V_{s_C}(d) = {v ∈ dom(M(d)) : subspace(v) = s_C}`

(content-subspace V-positions of document `d`; by D-SEQ★, when `V_{s_C}(d) ≠ ∅`, equals `{[s_C, 1, ..., 1, k] : 1 ≤ k ≤ n_{s_C}}` for some `n_{s_C} ≥ 1`, all positions sharing common depth `m_{s_C}`)

## Definition — Coverage

`coverage(e) := ⋃_{(s, ℓ) ∈ e} span(s, ℓ) ⊆ T`

where each span `(s, ℓ) ∈ e` denotes the address range `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}` from T12 (ASN-0034); `e` is a finite set of (start tumbler, length tumbler) pairs.

## Definition — Project

`project(a, i, d, Σ) := {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(Σ.L(a).eᵢ)}`

V-positions of `d` at state `Σ` whose images at slot `i` of link `a`'s endset structure (per L3, ASN-0047) fall inside the slot's coverage.

## Definition — DiscoverableFrom

`discoverable_from(a, d, Σ) := (E i : 1 ≤ i ≤ |Σ.L(a)| : project(a, i, d, Σ) ≠ ∅)`

link `a` is discoverable from `d` at `Σ` iff some slot of `a` projects to at least one V-position of `d`.

---

## V0 — ForkComposite (DEF, definition)

*Precondition.* `d_src ∈ E_doc`. No content-existence precondition is imposed; the empty-source case is normative per V7.

*Composite structure.* The composite is the *uninterrupted* sequence of elementary transitions K.δ + K.μ⁺ + K.ρ × n (where `n = |ran(M'(d_new))|`), or K.δ alone in the empty-source case per V7's extension of J4.

*Effects.* When `V_{s_C}(d_src) ≠ ∅` (the composite is K.δ + K.μ⁺ + K.ρ × n, where `n = |ran(M'(d_new))|`):

```
C' = C                                              (V3)
L' = L                                              (no K.λ or K.μ⁺_L steps)
E' = E ∪ {d_new}                                    (V1)
  where d_new is A_v(d_src)'s next emission:
    d_new = inc(d_src, 1)   on first fork of d_src
    d_new = inc(d_prev, 0)  on subsequent fork
      (d_prev = A_v(d_src)'s most recent prior emission)
M'(d_new)(v) = M(d_src)(v)  for v ∈ V_{s_C}(d_src)  (V4)
M'(d_new)(v) undefined       for v ∉ V_{s_C}(d_src) (V4b; V6 as corollary for link-subspace V-positions)
(A d' : d' ≠ d_new : M'(d') = M(d'))                (V5 for d' = d_src; K.δ + K.μ⁺ + K.ρ frame conditions for d' ≠ d_src ∧ d' ≠ d_new)
R' = R ∪ {(a, d_new) : a ∈ ran(M'(d_new))}          (V9)
```

When `V_{s_C}(d_src) = ∅` (the composite is K.δ alone, per V7's extension of J4): `C' = C`, `L' = L`, `E' = E ∪ {d_new}` (where `d_new` is `A_v(d_src)`'s next emission, formula as above), `M'(d_new) = ∅`, `M'(d') = M(d')` for `d' ≠ d_new`, `R' = R`.

---

## V1 — NewVersionIdentity (LEMMA, lemma)

A fork of `d_src` produces a new entity `d_new` allocated as `A_v(d_src)`'s next emission per the Allocator hierarchy (ASN-0047):

- *First fork of `d_src`* (when `A_v(d_src)` has emitted no prior version): `d_new = inc(d_src, 1)`, produced by K.δ case (ii) with `k = 1`, `t = d_src`.
- *Subsequent fork of `d_src`* (when `A_v(d_src)` has prior emissions with most recent `d_prev`): `d_new = inc(d_prev, 0)`, produced by K.δ case (ii) with `k = 0`, `t = d_prev`.

In either case `d_new ∈ E'_doc`, `d_new ∉ E_doc` (pre-fork), `IsDocument(d_new)` (by the IsDocument induction above on `A_v(d_src)`'s emission count, which combines KDeltaZerosK01's zero-preservation at `k = 0` and `k = 1` with P1-supplied membership `d_prev ∈ E_doc` at every inductive step), and `parent(d_new) = parent(d_src)` (by the parent-equality induction above on `A_v(d_src)`'s emission count, which combines KDeltaParentK01's per-step preservation at `k ∈ {0, 1}` with the inductive hypothesis `parent(d_prev) = parent(d_src)` at every subsequent-emission step). The new entity inherits the source's account-level prefix while extending into a fresh sub-tumbler.

---

## V2 — PrefixEncodedAncestry (LEMMA, lemma)

`d_src ≼ d_new` under the tumbler prefix order. The ancestry relationship is recoverable from `d_new`'s tumbler alone by truncating the trailing extension component; no separate lineage table is consulted.

---

## V3 — ContentStoreInvariance (INV, invariant)

A fork produces no new content. `C' = C` and `dom(C') = dom(C)`.

---

## V3a — AllocationInvariance (LEMMA, lemma)

For every document `d'`, the set of I-addresses allocated under `d'` is unchanged by forking:

`{a ∈ dom(C') : origin(a) = d'} = {a ∈ dom(C) : origin(a) = d'}`

*Derivation.* `dom(C') = dom(C)` by V3; the origin function depends only on the I-address (S7, ASN-0036). ∎

---

## V4 — ArrangementInheritance (LEMMA, lemma)

After any fork of `d_src`, the new document's content-subspace arrangement satisfies:

`(A v ∈ V_{s_C}(d_src) :: v ∈ dom(M'(d_new)) ∧ M'(d_new)(v) = M(d_src)(v))`

V4 holds unconditionally: the formal universal is vacuously true when `V_{s_C}(d_src) = ∅` (V7's empty-source case, where the quantifier ranges over the empty set) and substantively true when `V_{s_C}(d_src) ≠ ∅` (where K.μ⁺ populates `M'(d_new)` from `V_{s_C}(d_src)` per J4's clause (ii)). No precondition on `V_{s_C}(d_src)` is needed.

---

## V4a — PositionalIdentity (LEMMA, lemma)

For every V-position `v ∈ V_{s_C}(d_src)`, both `M(d_src)(v)` and `M'(d_new)(v)` are defined, and both equal the same I-address `a ∈ dom(C)`. The V-position `v` is *the same tumbler* in both arrangements.

---

## V4b — DomainEquality (LEMMA, lemma)

In the post-fork state, `dom(M'(d_new)) = V_{s_C}(d_src)` and `V_{s_C}(d_new) = V_{s_C}(d_src)`. The fork's V-position domain is *exactly* the source's content-subspace V-position set — not merely a superset.

---

## V5 — SourceIsolation (INV, invariant)

For every fork composite `Σ →* Σ'`: `M'(d_src) = M(d_src)`.

---

## V5a — PerDocumentArrangementIndependence (LEMMA, lemma)

Let `K_M = {K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L}` denote the four arrangement-modifying elementary transition kinds of ASN-0047. Each names a unique *target document* `d_target` in its preconditions; a transition `Σ → Σ'` is *M-targeted at `d_target`* iff it is an instance of some `K ∈ K_M` whose preconditions name `d_target`. Two clauses:

*(a) Per-elementary-transition frame.* For any single elementary transition `Σ → Σ'` and any document `d* ∈ E_doc`: if the transition is M-targeted at some `d_target ≠ d*`, or is any elementary transition that preserves the arrangement of every pre-existing document of `E_doc` (K.α, K.λ, K.ρ unconditionally; K.δ for every `d' ≠ d_new`, which includes every pre-existing `d* ∈ E_doc` since the K.δ outer precondition `e ∉ E` places `d_new ∉ E` pre-step while `d* ∈ E_doc ⊆ E` pre-step), then `M'(d*) = M(d*)`.

*(b) Per-sequence frame.* For any sequence of valid composite transitions `Σ →* Σ'` and any document `d* ∈ E_doc`: if no elementary step of the sequence is M-targeted at `d*`, then `M'(d*) = M(d*)`.

*Corollary 1 — source–fork isolation.* For `d* = d_src` and any subsequent sequence `Σ' →* Σ''` after the fork in which no step is M-targeted at `d_src`: `M''(d_src) = M'(d_src)`. Symmetric for `d* = d_new`.

*Corollary 2 — pairwise independence.* For any two distinct documents `d¹, d² ∈ E_doc` and any subsequent sequence `Σ' →* Σ''` in which no step is M-targeted at `d¹`: `M''(d¹) = M'(d¹)`.

---

## V6 — SubspaceSelectivity (LEMMA, lemma)

A fork transfers only the source's content-subspace arrangement. The new document's link subspace is empty in the post-fork state:

`V_{s_L}(d_new) = ∅` (in `Σ'`, the post-fork state)

*Derivation.* K.δ's effect on the newly created document is `M'(d_new) = ∅`. K.μ⁺ in J4's clause (ii) extends `M'(d_new)` only with positions drawn from `V_{s_C}(d_src)`, all of which have `subspace(v) = s_C` by the definition of `V_{s_C}(d_src) := {v ∈ dom(M(d_src)) : subspace(v) = s_C}` (ASN-0047). No link-subspace V-position is added. K.ρ does not modify arrangements. ∎

---

## V6a — LinkDiscoverabilityInheritance (LEMMA, lemma)

For every link `a ∈ dom(Σ.L)`, after the fork composite `Σ →* Σ'`:

(i) `Σ'.L(a) = Σ.L(a)` — the link's endsets persist across the composite.

(ii) `project(a, i, d_src, Σ') = project(a, i, d_src, Σ)` for every slot `i` — the source's projection is unchanged.

(iii) `project(a, i, d_src, Σ) ∩ V_{s_C}(d_src) = project(a, i, d_new, Σ')` for every slot `i` — the fork's projection equals the source's content-subspace-restricted projection.

---

## V7 — EmptySourceBehavior (LEMMA, lemma)

A fork of `d_src` with `V_{s_C}(d_src) = ∅` reduces to K.δ alone, producing a new entity `d_new ∈ E'_doc` with `M'(d_new) = ∅` and `R' = R`. The operation succeeds; the fork is itself an empty document, eligible for subsequent insertion or further forking.

---

## V8 — PositionalCorrespondence (LEMMA, lemma)

Let `V_{s_C}(d_src)` denote the content-subspace V-positions of `d_src` — equal in the pre-fork state `Σ` and the post-fork state `Σ'` because V5 establishes `M'(d_src) = M(d_src)`. For every `v ∈ V_{s_C}(d_src)`: `v ∈ dom(M'(d_new))` and `M'(d_src)(v) = M'(d_new)(v)`.

*Derivation.* By V5, `M'(d_src) = M(d_src)`, so `V_{s_C}(d_src)` and the mapping values `M'(d_src)(v) = M(d_src)(v)` are the same in `Σ` and `Σ'`. By V4, for every `v ∈ V_{s_C}(d_src)`, `v ∈ dom(M'(d_new))` and `M'(d_new)(v) = M(d_src)(v)`. Composing: `M'(d_src)(v) = M(d_src)(v) = M'(d_new)(v)`. ∎

---

## V8b — CorrespondenceForkTimeWitnessSet (LEMMA, lemma)

Let `Σ' →* Σ_g` be any sequence of valid composite transitions from the post-fork state `Σ'`. The set of V-positions at which `d_src` and `d_new` correspond at `Σ_g` is

`Corr_g := {v ∈ T : v ∈ dom(M_g(d_src)) ∩ dom(M_g(d_new)) ∧ M_g(d_src)(v) = M_g(d_new)(v)}`

Let `F := V_{s_C}(d_src)|_{Σ'}` denote the fork-time content-subspace witness set (fixed by the post-fork state), and define the *time-indexed fork-time witness set*

`Π_g := F ∩ Corr_g`

Two facts hold about `Π_g`:

(i) *Set bound.* `Π_g ⊆ F` at every reachable `Σ_g`. The witness set never grows beyond the fork-time set, since `F` is fixed by the post-fork state and `Π_g` is its intersection with `Corr_g`.

(ii) *Initial coverage.* At the post-fork state itself, `Π_{Σ'} = F`. V8 supplies `F ⊆ Corr_{Σ'}`, so `Π_{Σ'} = F ∩ Corr_{Σ'} = F`.

*Non-monotonicity.* `Π_g` need not decay monotonically: subsequent K.μ⁻ on either side may move `v` out of `dom(M_g(d_src)) ∩ dom(M_g(d_new))` and subsequent K.μ⁺ may re-install a binding; K.μ~ may remap an image. K.α, K.λ, K.ρ, K.δ, K.μ⁺_L, and third-document K.μ⁻/K.μ⁺/K.μ~ each leave `Π_g` invariant.

---

## V8c — CorrespondenceSymmetry (LEMMA, lemma)

The relationship V8 records is between two documents; it does not distinguish "source" from "fork." After the fork is complete, both `d_src` and `d_new` are documents in `E_doc`, and the set of corresponding V-positions `{v ∈ T : v ∈ dom(M'(d_src)) ∩ dom(M'(d_new)) ∧ M'(d_src)(v) = M'(d_new)(v)}` is invariant under swap of the two documents.

*Derivation.* The set is defined by two conjuncts: (i) `v ∈ dom(M'(d_src)) ∩ dom(M'(d_new))` and (ii) `M'(d_src)(v) = M'(d_new)(v)`. Conjunct (i) is invariant under swap because set intersection is commutative: `dom(M'(d_src)) ∩ dom(M'(d_new)) = dom(M'(d_new)) ∩ dom(M'(d_src))`. For conjunct (ii), V8 supplies `M'(d_src)(v) = M'(d_new)(v)`; symmetry of equality gives the equivalent `M'(d_new)(v) = M'(d_src)(v)`. ∎

---

## V9 — ForkProvenance (LEMMA, lemma)

After a fork of `d_src`:

`(A a : a ∈ ran(M'(d_new)) : (a, d_new) ∈ R')`

*Derivation.* By J1★ applied to the composite `Σ →* Σ'`, every `a` such that `(E v ∈ dom(M'(d_new)) : subspace(v) = s_C ∧ M'(d_new)(v) = a)` and not previously content-subspace-referenced in `M(d_new)` must satisfy `(a, d_new) ∈ R'`. Pre-fork, `d_new ∉ E_doc`, so `M(d_new) = ∅` vacuously and no pre-fork content-subspace references exist. By V6, `V_{s_L}(d_new) = ∅` in the post-fork state, so `ran(M'(d_new))` is exactly the content-subspace range. The condition therefore reduces to every `a ∈ ran(M'(d_new))` having `(a, d_new) ∈ R'`. ∎

---

## V9a — ProvenanceDerivationPath (NOTE, note)

For every `(a, d_new) ∈ R'` recorded by a fork, the relation does not distinguish whether `d_new` acquired `a` via fork from `d_src`, via transclusion from a third document also containing `a`, or via direct allocation. The relation reports *who has it*; the I-address tells you *who made it*; the parent prefix tells you *who you came from*. These three pieces of information are recoverable independently from the I-address and the fork's prefix structure.

---

## V9b — FreshForksExternalIAddresses (LEMMA, lemma)

For every `(a, d_new) ∈ R'` recorded by a fork, `origin(a) ≠ d_new`.

*Derivation.* By V3, `C' = C`, so the I-addresses inherited by `d_new` are exactly those already present in `dom(C)` at the pre-fork state. Pre-fork, `d_new ∉ E_doc`, so by SubAllocatorAxiom (ASN-0047) the content sub-allocator `A_C(d_new)` had not been activated and had emitted nothing into `dom(C)`. By S7 (StructuralAttribution, ASN-0036), every `a ∈ dom(C)` has a unique `origin(a) ∈ E_doc` fixed by the I-address itself, and no inherited I-address can have `origin(a) = d_new` because `A_C(d_new)` produced no element of `dom(C)` prior to the fork. ∎

---

## V10 — SiblingIndependence (LEMMA, lemma)

Let `Σ →* Σ¹` be a fork of `d_src` producing `d_new¹`, and let `Σ_g →* Σ²` be any later fork of the same `d_src` producing `d_new²`, where `Σ_g` is any state reachable from `Σ¹` by a finite sequence of valid composite transitions. The two forks are independent in three senses:

(a) *Distinct identities.* `d_new¹ ≠ d_new²`. By V1, both `d_new¹` and `d_new²` are emissions of `A_v(d_src)`. T10a.7 (EnumerationInjectivity, ASN-0034) applied to `A_v(d_src)`'s enumeration gives distinct addresses at distinct indices. So `d_new¹ ≠ d_new²`.

(b) *Independent content shares.* Both `d_new¹` and `d_new²` inherit content from `M(d_src)` *at the moment of each respective fork* — `d_new¹` reads `M(d_src)` at `Σ`, and `d_new²` reads `M(d_src)` at `Σ_g`. Their inherited V→I mappings live in separate arrangements `M¹(d_new¹)` and `M²(d_new²)`. V5a Corollary 2 — pairwise independence — yields the two preservation directions via two independent instantiations: instantiate at `(d¹, d²) = (d_new², d_new¹)` for Direction 1, and at `(d¹, d²) = (d_new¹, d_new²)` for Direction 2.

(c) *Independent provenance records.* `R²` contains both `(a, d_new¹)` and `(a, d_new²)` for shared I-addresses, but these are distinct pairs (since `d_new¹ ≠ d_new²` by (a)).

---

## V10a — TimeSensitivity (NOTE, note)

A fork in state `Σ` inherits `V_{s_C}(d_src)` and the mappings `M(d_src)|_{V_{s_C}(d_src)}` as they stand in `Σ`, not as they stood at any prior or subsequent state. Two forks of the same source at different times may produce different new versions, reflecting whatever state changes to `M(d_src)` occurred between them.

---

## V11 — TransitiveIdentity (LEMMA, lemma)

For every chain length `k ≥ 1` and every chain of forks `d_src → d¹_new → d²_new → ... → d^k_new` starting from `Σ` (with `d⁰_new := d_src`), where each step `dⁱ⁻¹_new → dⁱ_new` is a fork composite and *each step's source has its content-subspace arrangement unchanged between the prior step's post-state and the current step's pre-state* — that is, for every `1 ≤ i ≤ k`, `V_{s_C}(d^{i-1}_new)` is the same set in the post-state of step `i − 1` and the pre-state of step `i`, and for every `v` in this set, `M(d^{i-1}_new)(v)` is the same value in both states (with the convention that at `i = 1`, "step 0's post-state" denotes `Σ` itself, so the premise at `i = 1` is satisfied trivially by reflexivity) — the I-addresses inherited by `d^k_new` are the same I-addresses that `d_src` held at `Σ`: for every `v ∈ V_{s_C}(d_src)` evaluated at `Σ`, `v ∈ dom(M^k(d^k_new))` at the post-state of step `k`, and the value `M^k(d^k_new)(v)` at the post-state of step `k` equals the value `M(d_src)(v)` at `Σ`.

*Anchoring at `Σ`.* V11 anchors `V_{s_C}(d_src)` and `M(d_src)(v)` at `Σ` — the immutable historical state at the chain's start — rather than at any later state in which `d_src`'s arrangement may have been modified independently.

---

## V11a — AncestryComposition (LEMMA, lemma)

The prefix relation chains: `d_src ≼ d¹_new ≼ d²_new ≼ ... ≼ d^k_new`. Each step `dⁱ⁻¹_new → dⁱ_new` extends the tumbler by exactly one component at position `#dⁱ⁻¹_new + 1` whose value is `1 + j`, where `j ≥ 0` is the *subsequent-emission count* of `A_v(dⁱ⁻¹_new)` immediately prior to step `i`'s firing — `j = 0` covers V1's first-fork sub-case (`inc(dⁱ⁻¹_new, 1)`, placing value `1` at position `#dⁱ⁻¹_new + 1` by TA5(d)) and `j ≥ 1` covers V1's subsequent-fork sub-case (each successive `inc(·, 0)` strictly incrementing the component at position `#dⁱ⁻¹_new + 1` by TA5(c), so the `j`-th subsequent emission has value `1 + j` at this position). The full chain is recoverable from `d^k_new`'s tumbler alone by reading prefixes of strictly increasing length: the prefix of `d^k_new` of length `#d_src + i` is exactly `dⁱ_new` for every `0 ≤ i ≤ k` (with `d⁰_new := d_src`).

*Length identity:* `#dⁱ_new = #d_src + i` for every `0 ≤ i ≤ k`.

*Prefix identity:* For each `0 ≤ i ≤ k`, the relation `dⁱ_new ≼ d^k_new` holds, and T3 (CanonicalRepresentation, ASN-0034) gives that the prefix of `d^k_new` of length `#d_src + i` equals `dⁱ_new`.

---

## V12 — JointPermanence (INV, invariant)

After a fork, both `d_src` and `d_new` and all their inherited I-addresses are permanent. For every reachable state subsequent to the fork:

(a) `d_src ∈ E'_doc ∧ d_new ∈ E'_doc` (P1)

(b) `(A a ∈ ran(M'(d_new)) :: a ∈ dom(C''))` for every subsequent state `Σ''` (P0)

(c) `(A a ∈ ran(M'(d_new)) :: (a, d_new) ∈ R'')` for every subsequent state `Σ''` (P2 applied to the post-fork records of V9)

(d) `(A a ∈ ran(M'(d_new)) :: (a, d_src) ∈ R'')` — provenance records for the source are also permanent.

*Derivation of (d).* By V4b (*domain equality*), `dom(M'(d_new)) = V_{s_C}(d_src)`, and by V4 (*arrangement inheritance*), `M'(d_new)(v) = M(d_src)(v)` for every `v ∈ V_{s_C}(d_src)`. Composing the two gives `ran(M'(d_new)) = ran(M(d_src)|_{V_{s_C}(d_src)})` — every inherited I-address is content-subspace-referenced in `d_src`'s arrangement at the pre-fork state. P4★ (ProvenanceBoundsContentSubspace, ASN-0047) applied at the pre-fork state gives `(a, d_src) ∈ R` for every such `a`. P2 (ProvenancePermanence, ASN-0047) carries the pair forward into every subsequent reachable state `Σ''`. ∎
