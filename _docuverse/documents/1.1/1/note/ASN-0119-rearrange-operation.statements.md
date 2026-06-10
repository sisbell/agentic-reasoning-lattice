# ASN-0119 Claim Statements

*Source: ASN-0119-rearrange-operation.md (revised 2026-06-08) — Extracted: 2026-06-10*

## Definition — CutSequence

A *cut sequence* is a strictly ascending list of V-positions
`c₀ < c₁ < ... < c_{n-1}` in the text subspace `s_C` at depth 2, with
`n ∈ {3, 4}` and every cut landing on a boundary of the current arrangement
(ASN-0084, CutSequence — its conditions CS3/CS4 fix exactly this subspace and
depth).

Precondition R-PRE: every depth-2 text position from `c₀` up to the last cut is
active; moved-region widths are each ≥ 1.

## Definition — RegionPartition

For three cuts the affected interval `[c₀, c₂)` splits into two regions:

      α = { v : c₀ ≤ v < c₁ },    β = { v : c₁ ≤ v < c₂ },

with widths `w_α = ord(c₁) − ord(c₀)` and `w_β = ord(c₂) − ord(c₁)`.

For four cuts the interval `[c₀, c₃)` splits into three:

      α = [c₀, c₁),    μ = [c₁, c₂),    β = [c₂, c₃),

with `w_α = ord(c₁) − ord(c₀)`, `w_μ = ord(c₂) − ord(c₁)`, `w_β = ord(c₃) − ord(c₂)`.

Both moved-block widths are strictly positive; in the four-cut case `w_μ ≥ 1`.

## Definition — Coverage

(Imported from ASN-0098, Definition — Coverage.)

`coverage(a, i)` is the set of I-addresses the endset of slot `i` of link `a` references — a purely combinatorial function of the endset that consults no state component.

## Definition — Project

(Imported from ASN-0098, Definition — Project.)

      project(a, i, d, Σ) = { v ∈ dom(M(d)) : M(d)(v) ∈ coverage(a, i) }

The set of V-positions in document `d` under state `Σ` that resolve to addresses covered by link `a`'s slot `i` endset.

---

## REARRANGE_K — RearrangeK (OP, imported)

Operation imported from ASN-0084: 3-/4-cut transposition in the text subspace at depth 2, specified by PivotPostcondition (R-EXT, R-P1, R-P2) or SwapPostcondition (R-EXT, R-S1, R-S2, R-S3) with frame R-FRAME-P/R-FRAME-S.

Pivot postconditions (`n = 3`):

      v < c₀ ∨ v ≥ c₂  ⟹  M'(d)(v) = M(d)(v),                  (R-EXT)
      M'(d)(c₀ + j)       = M(d)(c₁ + j),   0 ≤ j < w_β,        (R-P1)
      M'(d)(c₀ + w_β + j) = M(d)(c₀ + j),   0 ≤ j < w_α.        (R-P2)

Swap postconditions (`n = 4`):

      v < c₀ ∨ v ≥ c₃  ⟹  M'(d)(v) = M(d)(v),                  (R-EXT)
      M'(d)(c₀ + j)             = M(d)(c₂ + j),  0 ≤ j < w_β,   (R-S1)
      M'(d)(c₀ + w_β + j)       = M(d)(c₁ + j),  0 ≤ j < w_μ,   (R-S2)
      M'(d)(c₀ + w_β + w_μ + j) = M(d)(c₀ + j),  0 ≤ j < w_α.   (R-S3)

The induced map `π : dom(M(d)) → dom(M(d))` is defined by `M'(d)(π(v)) = M(d)(v)`.

---

## RA0 — ContentStoreFrame (INV, predicate)

`Σ'.C = Σ.C` — the content store is a verbatim frame; no I-address is created, destroyed, or rebound.

---

## RA1 — IdentityCorrespondence (LEMMA, lemma)

`M'(d)(π(v)) = M(d)(v)` (ASN-0084 ArrangementRearrangement / R-PPERM / R-SPERM, = RA2's source), hence `ran(M'(d)) = ran(M(d))` (ASN-0084 R-RI) — I-addresses carried across the reassignment.

Derivation of range equality:

      ran(M'(d)) = { M'(d)(π(v)) : v ∈ dom(M(d)) }
                 = { M(d)(v)     : v ∈ dom(M(d)) }
                 = ran(M(d)).

---

## RA2 — Permutation (LEMMA, lemma)

The induced `π` (R-PPERM/R-SPERM) is a bijection of `dom(M(d))` onto itself; `dom(M'(d)) = dom(M(d))`.

---

## S2 — FunctionalityPreserved (INV, predicate)

`M'(d)` is single-valued — the disjoint tiling of destinations (R-PIV/R-SWP) gives each V-position one I-address (ASN-0036 S2).

---

## S3★ — ReferentialIntegrityPreserved (INV, predicate)

Per-subspace:

      v ∈ dom(M'(d)) ∧ subspace(v) = s_C  ⟹  M'(d)(v) ∈ dom(C),
      v ∈ dom(M'(d)) ∧ subspace(v) = s_L  ⟹  M'(d)(v) ∈ dom(L).

(ASN-0047 S3★.)

Derivation: For a text position `v` with `subspace(v) = s_C`: `M'(d)(v) = M(d)(π⁻¹(v))`, and `π⁻¹(v)` is again a text position (`π` permutes the text subspace onto itself); pre-state S3★ at `π⁻¹(v)` gives `M(d)(π⁻¹(v)) ∈ dom(C)`. For a link position `v` with `subspace(v) = s_L`: fixed pointwise by the non-text-subspace frame (R-NS / R-FRAME-P/S(a)), so `M'(d)(v) = M(d)(v) ∈ dom(L)` by pre-state S3★.

---

## S8★ — SpanDecompositionPreserved (INV, predicate)

`M'(d)` admits the unique maximal correspondence-run decomposition S8 guarantees — content subspace by ASN-0084 R-BLK + R-CANON, link subspace by the frozen frame (ASN-0047 S8★).

---

## RA3 — VExtentConservation (LEMMA, lemma)

`|dom(M'(d))| = |dom(M(d))|`, and the active run's endpoints are fixed — the document's total extent is conserved.

Precondition: R-PRE holds for the cut sequence K.

---

## RA5 — Discoverability (LEMMA, lemma)

Moved content is discoverable under its new V-position `π(v)` and resolves to its original I-address `M(d)(v)`.

      moved content is discoverable under its new V-position,
      and resolves to its original I-address.

---

## RA6 — LinkStoreFrame (INV, predicate)

`Σ'.L = Σ.L` — links are untouched; a link anchored in a moved region survives and travels with its content because endsets reference unchanged I-addresses.

---

## RA7a — FootprintTransport (LEMMA, lemma)

`project(a, i, d, Σ') = π(project(a, i, d, Σ))` — a link's V-footprint is relocated through `π`, neither lost nor enlarged.

Derivation: For any `v ∈ dom(M(d))`,

      v ∈ project(a, i, d, Σ)
        ⟺ M(d)(v) ∈ coverage(a, i)            (definition of project)
        ⟺ M'(d)(π(v)) ∈ coverage(a, i)        (RA1: M'(d)(π(v)) = M(d)(v))
        ⟺ π(v) ∈ project(a, i, d, Σ'),        (definition of project; π(v) ∈ dom(M'(d)) by RA2)

and since `π` is a bijection of `dom(M(d))` (RA2):

      project(a, i, d, Σ') = π( project(a, i, d, Σ) ).

---

## RA7b — DiscoverabilityPreserved (LEMMA, lemma)

`project(a, i, d, Σ') ≠ ∅   ⟺   project(a, i, d, Σ) ≠ ∅` — fragmentation never costs discoverability; corollary of RA7a (`π` a bijection), with discoverability reduced to `coverage ∩ ran ≠ ∅` by ASN-0098 LP12.

---

## RA7c — FootprintRunStructure (LEMMA, lemma)

      project(a, i, d, Σ) ⊆ one region
        (the `s_C` exterior, α, μ, β, or the frozen link subspace `s_L`)
        ⟹  π preserves the footprint's run structure
            (in particular, a single run stays a single run).

Within-region confinement is sufficient (not necessary) for contiguity-preservation.

---

## RA8a — FinalStateInvariance (LEMMA, lemma)

The atomic transposition and any two-move composite achieving the same net `π` reach the same final arrangement.

      M'(d) under T   =   M(d) under (T₁ ; T₂)

---

## RA8b — IntermediateDivergence (LEMMA, lemma)

A two-move composite passes through an observable intermediate arrangement (exhibited: `A C D B E` for the worked pivot) realized by neither endpoint of the atomic transposition.

      M_mid(d) ≠ M(d)  ∧  M_mid(d) ≠ M'(d).

Witness: `M_mid([s_C,4]) = a₂`, while `M([s_C,4]) = a₄` and `M'([s_C,4]) = a₅`.

---

## RA9 — DocumentIsolation (LEMMA, lemma)

`(∀ d' ≠ d :: M'(d') = M(d'))` together with RA0, RA6 — every other document, including transcluders of the rearranged I-addresses, is invariant.

Full conjunction:

      (∀ d' ≠ d :: M'(d') = M(d'))   ∧   Σ'.C = Σ.C   ∧   Σ'.L = Σ.L.
