# ASN-0119 Claim Statements

*Source: ASN-0119-rearrange-operation.md (revised 2026-06-08) — Extracted: 2026-06-09*

## Definition — CutSequence

A *cut sequence* is a strictly ascending list of V-positions `c₀ < c₁ < ... < c_{n-1}` in the text subspace `s_C` at depth 2, with `n ∈ {3, 4}` and every cut landing on a boundary of the current arrangement (ASN-0084, CutSequence — its conditions CS3/CS4 fix exactly this subspace and depth). Three cuts specify a *pivot*; four cuts specify a *swap*.

For three cuts the affected interval `[c₀, c₂)` splits into two regions:

    α = { v : c₀ ≤ v < c₁ },    β = { v : c₁ ≤ v < c₂ }

with widths `w_α = ord(c₁) − ord(c₀)` and `w_β = ord(c₂) − ord(c₁)`.

For four cuts the interval `[c₀, c₃)` splits into three:

    α = [c₀, c₁),    μ = [c₁, c₂),    β = [c₂, c₃)

where `μ` is the *intervening region* belonging to neither moved block. `w_μ = ord(c₂) − ord(c₁)`. Both region widths of the moved blocks are strictly positive, and in the four-cut case `w_μ ≥ 1` as well.

## Definition — FootprintProjection

For a link `a` with slot `i`, let `coverage(a, i)` be the set of I-addresses its endset references (ASN-0098), and define the link's footprint in `d` as the V-positions that resolve to those addresses:

    project(a, i, d, Σ) = { v ∈ dom(M(d)) : M(d)(v) ∈ coverage(a, i) }

## Definition — ArrangementPermutation

    π : dom(M(d)) → dom(M(d)),   defined by   M'(d)(π(v)) = M(d)(v)

Closed form **R-PPERM** (pivot) and **R-SPERM** (swap); totality and bijectivity together with the domain identity `dom(M'(d)) = dom(M(d))` are **R-PIV** and **R-SWP** (ASN-0084).

---

## REARRANGE_K — RearrangeK (imported, operation)

Operation imported from ASN-0084: 3-/4-cut transposition in the text subspace at depth 2, specified by PivotPostcondition (R-EXT, R-P1, R-P2) or SwapPostcondition (R-EXT, R-S1, R-S2, R-S3) with frame R-FRAME-P/R-FRAME-S.

**Pivot** (n = 3):

    v < c₀ ∨ v ≥ c₂  ⟹  M'(d)(v) = M(d)(v),                  (R-EXT)
    M'(d)(c₀ + j)       = M(d)(c₁ + j),   0 ≤ j < w_β,        (R-P1)
    M'(d)(c₀ + w_β + j) = M(d)(c₀ + j),   0 ≤ j < w_α.        (R-P2)

**Swap** (n = 4):

    v < c₀ ∨ v ≥ c₃  ⟹  M'(d)(v) = M(d)(v),                  (R-EXT)
    M'(d)(c₀ + j)             = M(d)(c₂ + j),  0 ≤ j < w_β,   (R-S1)
    M'(d)(c₀ + w_β + j)       = M(d)(c₁ + j),  0 ≤ j < w_μ,   (R-S2)
    M'(d)(c₀ + w_β + w_μ + j) = M(d)(c₀ + j),  0 ≤ j < w_α.   (R-S3)

## P0 — ContentPermanence (POSTCONDITION, frame)

`Σ'.C = Σ.C` — the content store is a verbatim frame; no I-address is created, destroyed, or rebound.

*Imported (ASN-0084 R-FRAME-P/S)*

## P1 — IdentityCorrespondence (LEMMA, range-invariant)

`M'(d)(π(v)) = M(d)(v)`, hence

    ran(M'(d)) = { M'(d)(π(v)) : v ∈ dom(M(d)) }
               = { M(d)(v)     : v ∈ dom(M(d)) }
               = ran(M(d))

I-addresses are carried across the reassignment.

*Imported (ASN-0084 R-RI)*

## P2 — Permutation (LEMMA, domain-preservation)

The induced `π` (R-PPERM/R-SPERM) is a bijection of `dom(M(d))` onto itself:

    dom(M'(d)) = dom(M(d))

*Imported (ASN-0084 R-PIV/R-SWP)*

## S2 — FunctionalityPreserved (INV, single-valued)

`M'(d)` is single-valued — the disjoint tiling of destinations (R-PIV/R-SWP) gives each V-position one I-address (ASN-0036 S2).

*Status: preserved*

## S3★ — ReferentialIntegrityPreserved (INV, per-subspace)

Per-subspace referential integrity:

    v ∈ dom(M'(d)) ∧ subspace(v) = s_C  ⟹  M'(d)(v) ∈ dom(C),
    v ∈ dom(M'(d)) ∧ subspace(v) = s_L  ⟹  M'(d)(v) ∈ dom(L).

For a text position `v`, `M'(d)(v) = M(d)(π⁻¹(v))` with `π⁻¹(v)` again a text position, so pre-state S3★ gives `M(d)(π⁻¹(v)) ∈ dom(C)`; link positions are frame-fixed, so their images stay in `dom(L)`. What is invariant is that `π` maps each subspace onto itself, not the image filed at any individual key.

*Status: preserved (ASN-0047 S3★)*

## P3 — VExtentConservation (LEMMA, cardinality)

    | dom(M'(d)) | = | dom(M(d)) |,    min and max V-position fixed.

*Status: introduced*

## P5 — Discoverability (LEMMA, navigation)

Moved content is discoverable under its new V-position `π(v)` and resolves to its original I-address `M(d)(v)`.

*Status: introduced*

## P6 — LinkStoreFrame (POSTCONDITION, frame)

    Σ'.L = Σ.L

Links are untouched; a link anchored in a moved region survives and travels with its content because endsets reference unchanged I-addresses.

*Status: introduced*

## P7a — FootprintTransport (LEMMA, footprint)

    project(a, i, d, Σ') = π( project(a, i, d, Σ) )

A link's V-footprint is relocated through `π`; a contiguous footprint stays contiguous iff its `π`-image is again an interval (e.g. within-region confinement, or coverage of two or more relocated regions that `π` re-abuts), so fragmentation of a contiguous run occurs *only when* it straddles a cut — straddling alone does not force it, and conversely a straddle that mixes the fixed exterior with a relocated region can fragment even when every block it covers is complete.

*Status: introduced*

## P7c — FootprintRunStructure (LEMMA, sufficient-condition)

    project(a, i, d, Σ) ⊆ one region (exterior, α, μ, or β)
      ⟹  π preserves the footprint's run structure
          (in particular, a single run stays a single run).

Within each region `π` is a uniform ordinal shift, so confinement to one region is *sufficient* (not necessary) for contiguity-preservation; this is not a weakest precondition, since relocating the region blocks creates new seams (a straddle across two relocated regions that re-abut may stay contiguous; a straddle mixing the fixed exterior with a relocated region may fragment even with complete-block coverage; a within-region gap stays fragmented).

*Status: introduced*

## P7b — DiscoverabilityPreserved (LEMMA, biconditional)

    project(a, i, d, Σ') ≠ ∅   ⟺   project(a, i, d, Σ) ≠ ∅

Fragmentation never costs discoverability.

*Status: introduced*

## P8a — FinalStateInvariance (LEMMA, atomicity)

    M'(d) under T   =   M(d) under (T₁ ; T₂)

The atomic transposition and any two-move composite achieving the same net `π` reach the same final arrangement.

*Status: introduced*

## P8b — IntermediateDivergence (LEMMA, observable-intermediate)

A two-move composite passes through an observable intermediate arrangement (exhibited: `A C D B E` for the worked pivot) realized by neither endpoint of the atomic transposition:

    M_mid(d) ≠ M(d)  ∧  M_mid(d) ≠ M'(d).

*Status: introduced*

## P9 — DocumentIsolation (POSTCONDITION, frame)

    (∀ d' ≠ d :: M'(d') = M(d'))   ∧   Σ'.C = Σ.C   ∧   Σ'.L = Σ.L

Every other document, including transcluders of the rearranged I-addresses, is invariant.

*Status: introduced*
