# ASN-0115 Claim Statements

*Source: ASN-0115-retrievev-operation-content-delivery-by-spec-set.md (revised 2026-06-04) — Extracted: 2026-06-10*

## Definition — DepthCompat

`depthcompat(ρ, Σ) ≡ V_S(d) = ∅ ∨ #s = m_S(d)`

where `ρ = (d, σ)`, `S = s₁` (subspace of span start `s`), `m_S(d)` defined only while `V_S(d) ≠ ∅`.

## Definition — Act

```
act(ρ, Σ) = dom(Σ.M(d)) ∩ ⟦σ⟧   when depthcompat(ρ, Σ)
act(ρ, Σ) = ∅                     otherwise
```

`act(ρ, Σ)` is finite (subset of `dom(Σ.M(d))`, which is finite by S8-fin) and totally ordered (subset of `T` with T1 order), admitting unique ascending enumeration `v₁ < v₂ < … < v_k` where `k = |act(ρ, Σ)|`.

## Definition — Item

```
item(v, ρ, Σ) =
  ⟨content, Σ.C(a)⟩   if subspace(v) = s_C   (then a ∈ dom(Σ.C) by S3★)
  ⟨ref, a⟩            if subspace(v) = s_L   (then a ∈ dom(Σ.L) by S3★)
```

where `a = Σ.M(d)(v)`. Total on `act(ρ, Σ)` by S3★-aux (SubspaceExhaustiveness).

## Definition — Deliver1

`deliver₁(ρ, Σ) = ⟨item(v₁, ρ, Σ), …, item(v_k, ρ, Σ)⟩`

where `v₁ < v₂ < … < v_k` is the unique ascending enumeration of `act(ρ, Σ)`.

## Confinement — PrefixConfinement (LEMMA, lemma)

For an ordinal-level, level-uniform span `σ = (s, ℓ)` with `#s = #ℓ = m ≥ 2`, every `t ∈ ⟦σ⟧` agrees with `s` on its first `m − 1` components — `tⱼ = sⱼ` for `1 ≤ j < m`. In particular `t₁ = s₁`, so `⟦σ⟧` lies wholly in subspace `s₁` and cannot cross the subspace boundary.

*Proof.* Ordinal-level width acts only at position `m` (`actionPoint(ℓ) = m`), so the length-`(m − 1)` prefix `p = [s₁, …, s_{m−1}]` satisfies `p ≼ s`, and the reach `reach(σ) = s ⊕ ℓ` copies that prefix unchanged below the action point (TumblerAdd, ASN-0034), giving `p ≼ reach(σ)`. For any `t ∈ ⟦σ⟧`, `s ≤ t < reach(σ)`, hence `s ≤ t ≤ reach(σ)`; T5 (ContiguousSubtrees, ASN-0034) then yields `p ≼ t`, i.e. `tⱼ = sⱼ` for `1 ≤ j < m`. ∎

---

## R0 — Deliver (DEF, definition)

`deliver(R, Σ) = deliver₁(ρ₁, Σ) ⌢ deliver₁(ρ₂, Σ) ⌢ … ⌢ deliver₁(ρₚ, Σ)`

where `R = ⟨ρ₁, …, ρₚ⟩`, `p ≥ 0`. When `p = 0`: `deliver(⟨⟩, Σ) = ⟨⟩`.

`act(ρ,Σ) = dom(Σ.M(d)) ∩ ⟦σ⟧` when `ρ` is depth-compatible at `Σ` (`V_S(d) = ∅ ∨ #s = m_S(d)`) and `∅` otherwise; `item` carries `Σ.C(a)` for content positions, the reference `a` for link positions.

## R1 — MaterialDelivery (INV, predicate)

For every active content position, the delivered item carries the bound content value `Σ.C(Σ.M(d)(v))`, not a description of where that value is stored.

## R2 — Faithfulness (INV, predicate)

Every delivered content item equals the value bound, in the content store, to the address the arrangement assigns its position: `item(v, ρ, Σ).val = Σ.C(Σ.M(d)(v))`. No other value may be substituted.

Frame limit: this governs the denotation of delivery, not any transmission channel.

## R3 — SpecSetExactness (INV, predicate)

The delivery contains an item for *exactly* the active positions `act(ρⱼ, Σ)` of each spec, and no others: every delivered item arises from some `v ∈ act(ρⱼ, Σ)` (nothing extra), and every `v ∈ act(ρⱼ, Σ)` contributes an item (nothing active omitted). For a spec depth-compatible at `Σ` this reads as span-for-span exactness, `act(ρⱼ, Σ) = ⟦σⱼ⟧ ∩ dom(Σ.M(dⱼ))` — every position the span names and the arrangement binds, and no other; for a spec depth-incompatible at `Σ`, `act(ρⱼ, Σ) = ∅`, so that spec contributes nothing.

## R4 — ArrangementRelativity (INV, predicate)

Each V-spec `(dⱼ, σⱼ)` is resolved through the arrangement `Σ.M(dⱼ)` of the document it names — and through no other. The delivered material reflects exactly what the named arrangement binds those spans to.

## R5 — OrderFidelity (INV, predicate)

Across V-specs, delivery follows spec-set sequence order: the items of `ρᵢ` wholly precede the items of `ρⱼ` whenever `i < j`, irrespective of the relative V-magnitudes of the two specs. Within a single V-spec, items are delivered in ascending T1 order of their V-positions. Each item's extent is fixed by its position; the boundary between consecutive items is implicit in the spec-set structure and the span endpoints, with nothing interpolated between them.

## R6 — SilentGapFiltering (INV, predicate)

A named position the consulted arrangement does not make active — one outside `act(ρⱼ, Σ)` — contributes nothing to the delivery and causes no failure; delivery succeeds and returns the items for exactly the active positions `act(ρⱼ, Σ)`, the rest represented by their absence. When `ρⱼ` is depth-compatible at `Σ`, `act(ρⱼ, Σ) = dom(Σ.M(dⱼ)) ∩ ⟦σⱼ⟧`, so the filtered positions are precisely the geometrically unbound ones, `v ∈ ⟦σⱼ⟧ \ dom(Σ.M(dⱼ))`; when `ρⱼ` is depth-incompatible at `Σ`, `act(ρⱼ, Σ) = ∅` and the whole span is filtered, still without failure. Moreover, for a depth-compatible `ρⱼ`, restricted to the depth-`m_S`, subspace-`S` slice of `⟦σⱼ⟧` — the only named positions the arrangement can bind — the unbound portion never falls as an interior hole within the subspace's contiguous active range; and whenever that slice meets the active range, the unbound portion is exactly a *terminal overrun* past the bound frontier. The no-interior-hole guarantee is a claim about the bindable slice, not about every named tumbler in the interval.

## R7 — Repeatability (LEMMA, lemma)

Let `Σ`, `Σ'` be two states of one evolving docuverse with one a reachability descendant of the other along the sequential transition order — without loss of generality `Σ →* Σ'` (ASN-0047, SequentialTransitionAxiom) — for which the consulted arrangement restrictions agree, `Σ.M(dⱼ)|⟦σⱼ⟧ = Σ'.M(dⱼ)|⟦σⱼ⟧` for every `j`. Then `deliver(R, Σ) = deliver(R, Σ')`.

## R8 — TransclusionCoResolution (INV, predicate)

If two active positions `v, v'` (within one spec or across specs) resolve to the same address, `Σ.M(d)(v) = Σ.M(d')(v') = a`, then they share one subspace, and the co-delivery guarantee is content-only. In the **content sub-case** (`a ∈ dom(Σ.C)`) the two positions are co-resolved through the one shared address `a`:

- (i) both items carry the identical value `Σ.C(a)` (R2);
- (ii) both resolve *through* `a` — identity-preserving co-resolution — so `origin(a)` of both is one and the same (S4, S7);
- (iii) the operation performs no deduplication, so the shared content appears once per V-position.

The sharing is a fact of *resolution*, not of the delivered output: each item carries the value `Σ.C(a)`, never the address `a` (R1), so the co-delivery is byte-indistinguishable from the delivery of two coincidentally-equal contents at distinct addresses (S4) and discloses nothing about the shared origin. The **link sub-case** is *vacuous*: two distinct active link positions can never share a link address. Genuine transclusion is therefore confined to content.

## R9 — CoherentMultiOriginAssembly (INV, predicate)

A spec-set drawing on multiple origins is delivered as one ordered sequence (R5), assembled by resolving each spec against its own document's arrangement independently (R4). How much origin survives *into the delivered stream* is *kind-asymmetric*, tracking the payload asymmetry of R1 and R10: a **link** item carries the address `a` itself (R10), so its home `home(a)` is recoverable from the delivered output; a **content** item carries only the value `Σ.C(a)` (R1), so its origin `origin(a)` is *not* recoverable from the output — it is determinate only through the resolution mapping `v ↦ a`, an internal artifact of computing `deliver`.

## R10 — SubspaceCrossingObservability (INV, predicate)

When an active position lies in the link subspace (`subspace(v) = s_L`), it resolves (by S3★) to a link address `a ∈ dom(Σ.L)`, and the delivered item is a *reference* to that link entity — an item distinguishable in kind from a content-value item. A spec-set spanning both subspaces therefore yields a heterogeneous delivery in which the subspace boundary is observable as a change of item kind. A span confined to the text subspace never exposes link-subspace material.

## R11 — PermanentSourcing (INV, predicate)

Delivery sources every content item from the immutable content store by I-address. Consequently a content address that has ever entered `dom(Σ.C)` remains deliverable for all time: if any arrangement — the document's own, a later version's, or a transcluding document's — binds some V-position to `a`, then a spec over that document resolves to `a` and delivers `Σ.C(a)`, even if the originally-creating document's *current* arrangement no longer references `a`.

The weakest precondition for delivery to include the value at `a` is a *single* live condition:

- (i) the consulted arrangement binds some *active* content position to `a` — a `v ∈ act(ρ, Σ)` with `subspace(v) = s_C` and `Σ.M(d)(v) = a`.

Stating (i) through `act` folds in: the spec is depth-compatible at `Σ` (else `act = ∅`), that `v` is named (`act ⊆ ⟦σ⟧`), and that `v` is bound (`act ⊆ dom(Σ.M(d))`). There is no independent store-membership conjunct: `Σ.M(d)(v) = a ⟹ a ∈ dom(Σ.C)` (S3★), and `Σ.C(a)` is then fixed for all time by S0.
