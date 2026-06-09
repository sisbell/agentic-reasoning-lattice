# Review of ASN-0118

This is a strong, carefully-scoped ASN. The composite decomposition (K.μ⁻ + K.μ⁺ + K.ρ), the tiling argument, the worked two-source example, and the link-discoverability wp are all genuine and largely sound. The transclusion frame CP1 is correctly identified as the load-bearing stipulation, and the displacing/append/empty case split is handled. Two issues remain.

## REVISE

### Issue 1: Provenance dichotomy misses "range-new but already recorded"
**ASN-0118, CP8 derivation**: "For each `cᵢ` that is *range-new* ... J1★ ... is an obligation on the composite: a valid COPY must include a K.ρ step recording `(cᵢ, d)`" — paired with the alternative branch "For each `cᵢ` *already* referenced by `d` ... no K.ρ step is needed ... by P4★ ... `(cᵢ, d) ∈ Σ.R` already holds".

**Problem**: The case split is binary (range-new vs. currently-in-range), but a third configuration is reachable: `cᵢ` not in the *current* content-subspace range of `M(d)` (hence range-new, so the P4★ branch does not apply) yet `(cᵢ, d) ∈ Σ.R` already, because `d` referenced `cᵢ` earlier and then contracted those V-positions away (K.μ⁻ removes from range; P2 keeps the provenance pair forever). This is exactly a re-COPY of previously-deleted transcluded content. In that case J1★ requires only the membership `(cᵢ, d) ∈ Σ'.R`, which already holds via P2 — a K.ρ step is *not* required. The claim "must include a K.ρ step" overstates necessity. (Including the redundant K.ρ is harmless and J1'★-admissible, so soundness is not broken — but the necessity claim in the derivation is wrong for this branch.)

**Required**: Either restate J1★'s effect as a membership requirement satisfiable *either* by a K.ρ step *or* by pre-existing `Σ.R` membership (P2), or add the third branch explicitly: range-new ∧ already-in-`R` ⟹ provenance supplied by permanence, K.ρ optional.

### Issue 2: Ordinal-level required as input but no consumer in the derivation
**ASN-0118, "What a spec-set names"**: "we require, as input discipline, that the span be *ordinal-level* ... we do *not* inherit ordinal-level from C0 but require it directly — a condition on `ℓ`."

**Problem**: The requirement is asserted but never shown to be load-bearing for any COPY claim. The ASN's own reasoning routes around the one place ordinal-level would be consumed: CP0(c) obtains the single-subspace premise of ASN-0058's C1a from *content-residence* (`act(ρ, Σ) ⊆ V_{s_C}(d_s)`) rather than from C0a/C0 (the well-formed/ordinal-level consumer), and CP0(a) grounds resolution integrity in S3★ rather than C1. The bound active set `dom(M(d_s)) ∩ ⟦σ⟧` is single-subspace by content-residence and single-depth by S8-depth regardless of `ℓ`'s action point, so the placement/resolution arithmetic does not appear to depend on it. As written, ordinal-level looks like a dangling precondition.

**Required**: Exhibit the specific claim or step that fails without ordinal-level (e.g., a derivation that genuinely needs `actionPoint(ℓ) = #ℓ` and is not already discharged by content-residence + S8-depth), or downgrade it from a required input discipline to an optional/normalizing convention.

## OUT_OF_SCOPE

### Topic 1: Width shortfall under partial binding (C2 loss)
**Why out of scope**: The ASN's first open question — what COPY must guarantee about a partially-bound span's nominal extent versus its smaller placed width `W` — is correctly deferred. The decision to admit partial binding and silently restrict via `act` is settled here; the relationship to ASN-0058's C2 is new territory, not an error in this ASN.

### Topic 2: Link-subspace transclusion, overlapping/repeated spec-set placement order, mixed-depth assembly, correspondence relation
**Why out of scope**: The remaining open questions name genuinely future obligations (placing a link by reference, ordering invariants for repeated resolution, level-uniformity across differing depths, the correspondence relation across appearances). None is a gap in COPY-as-content-transclusion.

VERDICT: REVISE
