# ASN-0115 Claim Statements

*Source: ASN-0115-retrievev-operation-content-delivery-by-spec-set.md (revised 2026-06-04) — Extracted: 2026-06-05*

## Definition — ActivePositions

`act(ρ, Σ) = dom(Σ.M(d)) ∩ ⟦σ⟧`

where `ρ = (d, σ)` is a V-spec, `Σ` is a reachable state, and `⟦σ⟧ = {t ∈ T : s ≤ t < s ⊕ ℓ}` for span `σ = (s, ℓ)`.

The set `act(ρ, Σ)` is finite (subset of `dom(Σ.M(d))`, which is finite by S8-fin) and totally ordered (subset of `T` by T1), giving unique ascending enumeration `v₁ < v₂ < … < v_k` where `k = |act(ρ, Σ)|`.

## Definition — DeliveryItem

```
item(v, ρ, Σ) =
  ⟨content, Σ.C(a)⟩   if subspace(v) = s_C   (then a ∈ dom(Σ.C) by S3★)
  ⟨ref, a⟩            if subspace(v) = s_L   (then a ∈ dom(Σ.L) by S3★)
```

where `a = Σ.M(d)(v)` (well-defined and single-valued by S2). Defined on all `v ∈ act(ρ, Σ)` because S3★-aux (SubspaceExhaustiveness) ensures every active V-position has `subspace(v) = s_C` or `subspace(v) = s_L`.

## Definition — PerSpecDelivery

`deliver₁(ρ, Σ) = ⟨item(v₁, ρ, Σ), …, item(v_k, ρ, Σ)⟩`

the ascending-V sequence of items over the enumeration `v₁ < v₂ < … < v_k` of `act(ρ, Σ)`.

## R0 — Deliver (DEF, definition)

`deliver(R, Σ) = deliver₁(ρ₁, Σ) ⌢ deliver₁(ρ₂, Σ) ⌢ … ⌢ deliver₁(ρₚ, Σ)`

where `R = ⟨ρ₁, …, ρₚ⟩` is a finite ordered sequence of V-specs, `p ≥ 0`.

Boundary: `deliver(⟨⟩, Σ) = ⟨⟩`.

Frame: no component of `Σ` is modified — neither `Σ.C`, nor `Σ.L`, nor any `Σ.M(d)`.

## R1 — MaterialDelivery (INV, predicate)

For every active content position, the delivered item carries the bound content value `Σ.C(Σ.M(d)(v))`, not a description of where that value is stored.

## R2 — Faithfulness (INV, predicate)

Every delivered content item equals the value bound, in the content store, to the address the arrangement assigns its position: `item(v, ρ, Σ).val = Σ.C(Σ.M(d)(v))`. No other value may be substituted.

Frame limit: this governs the denotation of delivery, not any transmission channel.

## R3 — SpecSetExactness (INV, predicate)

The delivery contains an item for *exactly* the active positions of each span, and no others: every item arises from some `v ∈ ⟦σⱼ⟧ ∩ dom(Σ.M(dⱼ))` (nothing extra — every delivered item is named by a span), and every such `v` contributes an item (nothing present-and-named is omitted).

## R4 — ArrangementRelativity (INV, predicate)

Each V-spec `(dⱼ, σⱼ)` is resolved through the arrangement `Σ.M(dⱼ)` of the document it names — and through no other. The delivered material reflects exactly what the named arrangement binds those spans to.

## R5 — OrderFidelity (INV, predicate)

Across V-specs, delivery follows spec-set sequence order: the items of `ρᵢ` wholly precede the items of `ρⱼ` whenever `i < j`, irrespective of the relative V-magnitudes of the two specs. Within a single V-spec, items are delivered in ascending T1 order of their V-positions. Each item's extent is fixed by its position; the boundary between consecutive items is implicit in the spec-set structure and the span endpoints, with nothing interpolated between them.

## R6 — SilentGapFiltering (INV, predicate)

A named position with no binding in the consulted arrangement — `v ∈ ⟦σⱼ⟧ \ dom(Σ.M(dⱼ))` — contributes nothing to the delivery and causes no failure. Delivery succeeds and returns the items for the bound positions; the unbound positions are represented by their absence. Moreover, restricted to the depth-`m_S`, subspace-`S` slice of `⟦σⱼ⟧` — the only named positions the arrangement can bind — the unbound portion is always a *terminal overrun* of the subspace's contiguous active range — the named positions past the bound frontier — never an interior hole within that range. Named positions of `⟦σⱼ⟧` deeper than `m_S` are unbound too, but for a simpler reason: by S8-depth every active subspace-`S` position has depth exactly `m_S`, so any named position of depth `> m_S` is absent from `dom(Σ.M(dⱼ))` outright and is harmlessly filtered out of `act`; the no-interior-hole guarantee is a claim about the bindable slice, not about every named tumbler in the interval.

## R7 — Repeatability (INV, predicate)

Let `Σ`, `Σ'` be two states of one evolving docuverse with one a reachability descendant of the other along the sequential transition order — without loss of generality `Σ →* Σ'` (ASN-0047, SequentialTransitionAxiom) — for which the consulted arrangement restrictions agree, `Σ.M(dⱼ)|⟦σⱼ⟧ = Σ'.M(dⱼ)|⟦σⱼ⟧` for every `j`. Then `deliver(R, Σ) = deliver(R, Σ')`.

## R8 — TransclusionRevelation (INV, predicate)

If two active positions `v, v'` (within one spec or across specs) satisfy `Σ.M(d)(v) = Σ.M(d')(v') = a`, then the two positions share a single subspace: by S3★ the shared address `a` lies in `dom(Σ.C)` or in `dom(Σ.L)` but, by store disjointness (SD), not both. Two cases arise by that shared subspace:

**(Content sub-case)** `subspace(v) = s_C`, `a ∈ dom(Σ.C)`:
- (i) the two delivered items carry the identical value `Σ.C(a)`, by R2
- (ii) both items are resolved through the one shared address `a` — identity-preserving co-resolution — never fabricating two independent origins, so `origin(a)` of both is one and the same (S4, S7)
- (iii) the operation performs no deduplication: each position yields its own item, so the shared content appears once per V-position

**(Link sub-case)** `subspace(v) = s_L`, `a ∈ dom(Σ.L)`: vacuous. CL-OWN (ASN-0047) forces `origin(Σ.M(d)(v)) = d` for every link-subspace position, so two documents both binding `a` in their link subspaces are forced equal, `d = d'`. Within that one document, CL-UNIQ (ASN-0047) makes `Σ.M(d)` injective on the link subspace, so two positions both mapping to `a` are forced equal, `v = v'`. Genuine link transclusion therefore does not occur.

## R9 — CoherentMultiOriginAssembly (INV, predicate)

A spec-set drawing on multiple origins is delivered as one ordered sequence (R5), assembled by resolving each spec against its own document's arrangement independently (R4). The *resolution* is provenance-traceable: each active position `v` resolves to `a = Σ.M(d)(v)`, and that address determines a home document — for a content position (`subspace(v) = s_C`, `a ∈ dom(Σ.C)`) the document-level prefix `origin(a)` (S7); for a link position (`subspace(v) = s_L`, `a ∈ dom(Σ.L)`) the link's home `home(a)` (ASN-0043, L1a), which coincides with `origin` on link addresses (ASN-0086, HomeOriginCoincidence) — so no fragment's provenance is collapsed by co-assembly. Whether that origin travels *inside* the delivered material or is recoverable only through the resolution mapping is a separate question; R9 asserts traceability of the resolution, not inline provenance of the delivered stream.

## R10 — SubspaceCrossingObservability (INV, predicate)

When an active position lies in the link subspace (`subspace(v) = s_L`), it resolves (by S3★) to a link address `a ∈ dom(Σ.L)`, and the delivered item is a *reference* to that link entity — an item distinguishable in kind from a content-value item. A spec-set spanning both subspaces therefore yields a heterogeneous delivery in which the subspace boundary is observable as a change of item kind. A span confined to the text subspace never exposes link-subspace material.

## R11 — PermanentSourcing (INV, predicate)

Delivery sources every content item from the immutable content store by I-address. Consequently a content address that has ever entered `dom(Σ.C)` remains deliverable for all time: if any arrangement — the document's own, a later version's, or a transcluding document's — binds some V-position to `a`, then a spec over that document resolves to `a` and delivers `Σ.C(a)`, even if the originally-creating document's *current* arrangement no longer references `a`.

Weakest precondition for delivery to include the value at `a`: a single live condition — (i) the consulted arrangement binds some named content position to `a` (`subspace(v) = s_C`, `Σ.M(d)(v) = a`). Store membership `a ∈ dom(Σ.C)` is an automatic, permanent consequence: S3★ supplies membership, S0 supplies immutability.
