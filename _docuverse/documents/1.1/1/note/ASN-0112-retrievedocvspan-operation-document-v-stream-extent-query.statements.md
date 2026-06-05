# ASN-0112 Claim Statements

*Source: ASN-0112-retrievedocvspan-operation-document-v-stream-extent-query.md (revised 2026-06-04) — Extracted: 2026-06-05*

## Definition — OccupiedVPositions

`O(d) = dom(M(d))`

The set of *occupied V-positions* of `d`: the positions that currently carry content in the arrangement.

## Definition — BoundingSpanConstruction

> `origin_d = min O(d)`,  `reach_d = shift(max O(d), 1)`,  `extent_d = reach_d ⊖ origin_d`

`σ_d = (origin_d, extent_d)`

The reach advances one ordinal step past the maximum occupied position, realizing the half-open convention under which the last occupied position is included and the next is excluded.

## Definition — SpanDenotation

`⟦σ_d⟧ = {t ∈ T : origin_d ≤ t < origin_d ⊕ extent_d}`

where `reach(σ) = s ⊕ ℓ` (T12, ASN-0053). A span is *well-formed* when `Pos(ℓ)` and `actionPoint(ℓ) ≤ #s`; it is *level-uniform* when `#s = #ℓ`.

## Definition — SubspacePartition

`V_S(d) = {v ∈ O(d) : subspace(v) = S}`

for `S ∈ {s_C, s_L}`, with `s_C = 1`, `s_L = 2` (SubspaceConventionAxiom).

---

## V0 — ResultType (DEF, function)

`RETRIEVEDOCVSPAN : dom(M) → Span + {⟨⟩}` (tagged union): one well-formed span `σ_d = (origin_d, extent_d)` for a non-empty document, or the distinguished empty span-set `⟨⟩` (denoting `∅`, not a T12 span) when `O(d) = ∅` — never a content sequence, never a count; uniform singleton-span-set typing rejected to keep the non-empty result literally a span per Nelson 4/68

## V1 — OriginIsOccupied (LEMMA, lemma)

When `O(d) ≠ ∅`, `origin_d = min O(d)` under T1 and `origin_d ∈ O(d)` (the origin is an occupied position)

## V2 — Coverage (LEMMA, lemma)

`O(d) ⊆ ⟦σ_d⟧` (coverage), proved unconditionally via D0/D1 without assuming level-uniformity; the actual reach `r⋆ = origin_d ⊕ extent_d ≥ reach_d = shift(max O(d), 1) > max O(d)`, with equality `r⋆ = reach_d` iff `#origin_d ≤ #reach_d`; the span `(origin_d, extent_d)` is always a well-formed T12 span

## V3 — TightestLevelUniformCovering (LEMMA, lemma)

`origin_d` is the greatest lower bound of `O(d)`; `reach_d` is the least strict upper bound of `max O(d)` *among same-depth tumblers* (the deeper zero-extension `max O(d).0` is a smaller upper bound but breaks level-uniformity) — so `σ_d` is the tightest *level-uniform* covering span

## V4 — VstreamBounded (INV, predicate)

`extent_d` is computed from `O(d) = dom(M(d))` alone; content in `dom(C)` but absent from the arrangement (deleted, or native elsewhere) contributes nothing (Vstream-bounded, not Istream)

## V5 — ExactCoverSingleSubspace (LEMMA, lemma)

When all occupied positions share one subspace, `⟦σ_d⟧` contains no occupied-depth position outside `O(d)` (exact cover of a contiguous run)

## V6 — CrossSubspaceBoundingBox (LEMMA, lemma)

When occupied positions span more than one subspace, `O(d) ⊊ ⟦σ_d⟧` — the span bridges the inter-subspace void (bounding box, not exact cover); the endpoints are level-compatible and the span level-uniform whenever the subspaces share a depth (`m_C = m_L`, the case the implementation always realizes per consultation Q2), and coverage holds even when `m_C ≠ m_L`

## V7 — SingleSpanContiguity (LEMMA, lemma)

The result is always one convex region; fragmentation is unrepresentable in a single span, so multi-subspace documents are reported by enclosure (single-span contiguity)

## V8 — OriginPermanence (INV, predicate)

While the content subspace is non-empty, `origin_d = [s_C,1,…,1]`, invariant under all editing that leaves content present (origin permanence)

## V9 — ExtentTracksComposition (LEMMA, lemma)

`σ_d` is a function of `O(d)` alone; pure rearrangement preserves `O(d)` and returns the identical span (extent tracks composition, not arrangement)

## V10 — InsertionMonotonicity (LEMMA, lemma)

When the content subspace is maximal (link subspace empty), inserting `n` content positions advances reach and extent by `n` ordinal steps (`extent_after = shift(extent_before, n)`) and leaves the origin fixed — the count-coincidence (extent's final component `= |O(d)|`) holds only in the dense, depth-uniform single-subspace regime; when links occupy the maximum, content insertion leaves reach and extent invariant (insertion monotonicity, content-maximal case)

## V11 — TotalAnswerability (LEMMA, lemma)

The operation is total over allocated documents; `O(d) = ∅` yields the distinguished empty span-set `⟨⟩` (not a T12 span), with `origin_d` undefined and no extent — the implementation's zeros are a sentinel, not a legal address (TA6)

## V12 — InformationGain (OBS, lemma)

The span discloses the live origin (addressing anchor) and current extent (present bounds) — neither derivable from `d`'s identity (information gain)

## V13 — Independence (LEMMA, lemma)

`σ_d` depends only on `O(d)`; two documents sharing content report independent spans; transcluded positions count toward the borrowing document's extent (independence)

## V14 — Permanence (LEMMA, lemma)

Every *occupied* position in `O(d)` maps through `M(d)` to a permanent, immutable image, by subspace (S3★): content positions to `dom(C)` (S0, P0), link positions to `dom(L)` (L12); covered-but-unoccupied positions in the cross-subspace case (V6) carry no `M(d)` image; sharing preserves what the span denotes (permanence)

## V15 — SnapshotStability (INV, predicate)

A returned span keeps its meaning under later edits to `d` or to home documents supplying its content; a fresh report is a new query, not a mutation (snapshot stability)

## V16 — Determinism (LEMMA, lemma)

`σ_d` is a pure function of `O(d)`; equal arrangements return identical spans, independent of how the arrangement was built (determinism)

## V17 — WellFormedPositiveExtent (LEMMA, lemma)

For non-empty `d`, `extent_d` is a positive tumbler with `actionPoint(extent_d) ≤ #origin_d` (well-formed T12 span); `reach_d > origin_d` always, so the extent is never negative

## V18 — DeletionSymmetryAndOriginMigration (LEMMA, lemma)

Deletion of `n` content positions retreats reach and extent by `n` ordinal steps when the content subspace is maximal (inverse of V10) and leaves both invariant when links occupy the maximum; clearing the content subspace while links survive migrates `origin_d` from `[s_C,1,…,1]` to the link minimum `[s_L,1,…,1]` — the sole editing transition that moves the origin, and exactly the boundary V8 excludes (deletion symmetry and origin migration)
