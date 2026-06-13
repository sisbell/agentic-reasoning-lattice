# Review of ASN-0132

I checked the mathematics first, against the foundations. The operation is sound: `countlinks_FTT` is well-defined (the counted set is a finite, computable subset of `dom(Σ.L)` by L-fin and FL-DEC), CN-LOC correctly inherits from FL-LOC, and the ten derived claims each hold. I verified the harder ones by hand:

- **CN-UNIT (d)** — version-refraction reduces to appearance multiplicity correctly: J4's `K.μ⁺` ranges over `V_{s_C}` and its "no other elementary steps" clause excludes `K.λ`, so `Σ.L` is genuinely untouched by forking.
- **CN-MONO** — the ordinary-link increment wp is derived in full and matches FL-WP(a); the retraction-link case correctly carries FL-WP(b)'s self-retraction conjunct and notes the from-wildcard requirement (empty from-endset annihilates a constrained from-slot).
- **The worked store** — I recomputed every contribution. `coverage(F) = [1.0.1.0.1.0.1.5, .13)` holds ordinals 5..12; `a₁` (.6/.7/.9 ∈ F) → 1, `a₂` (.8 ∈ F but nullified) → 0, `a₃` (.11 ∈ F, orphan) → 1, `a₄` (references `d₂`, diverges at component 5, disjoint) → 0, `a_R` (empty from) → 0; `nullified(Σ) = {a₂}`; count = 2. The wildcard count (4) and the two home-bound cases (`H₁ = d₁` → 2; `H₂ = d₂` → 0, a genuine non-degenerate CN-ZERO) all check out. `home(aᵢ) = d₁` for all five via the NUDE projection. Correct throughout.

No correctness gap, no skipped boundary, no proof-by-checkmark. The findings below are prose-economy issues the anti-bloat mode targets, not defects in the reasoning.

## REVISE

### Issue 1: The "re-phrasing → different count" corollary is previewed, then made load-bearing
**ASN-0132, "The satisfying set is already named" (remark) and "Stability under content editing" (CN-STAB)**: The remark ends —

> "A fixed resolved q is what the operation measures, whereas re-phrasing the same intent can re-resolve to a different q. Any discrepancy a reader perceives between two such requests lives in the resolution, never in the count."

and CN-STAB's resolution paragraph then states the same corollary where it actually does work:

> "A reader who re-phrases the same intent after an edit ... submits a different request, because the resolution against the edited arrangement yields different addresses. The count of that different request may differ."

**Problem**: The scope statement ("q is a resolved request, upstream of the operation") is genuinely needed before any claim and should stay. But its last two sentences preview the re-phrasing/different-count corollary, which CN-STAB then carries in context — it is precisely what explains why CN-STAB's stability is asserted "for a fixed q." The corollary appears twice; the up-front instance is accretion.
**Required**: End the remark at "Everything we say about `countlinks_FTT(q, Σ)` is said of a resolved request," letting CN-STAB make the re-phrasing point once, where it is load-bearing.

### Issue 2: The cost non-claim is wrapped in meta-commentary about the act of not-claiming
**ASN-0132, "Cost, and the meaning of asking for a number"**:
> "About cost, the honest answer is a deliberate non-claim, and saying so is part of the specification. One might hope that offering a count as its own service commits the design to computing cardinality more cheaply than delivery — that 'how many' should be answerable without producing 'which ones.' The specification fixes what is computed ... not how much it costs..."

**Problem**: The substantive content — cost-asymmetry is a quality of service, not a correctness obligation, and is therefore not a claim — is sound and worth stating. But it is wrapped in defensive meta-prose: "the honest answer is a deliberate non-claim, and saying so is part of the specification" is commentary on the act of not-claiming, and "One might hope that..." erects a strawman to knock down. The precise reader works past both to reach the one sentence that matters.
**Required**: State the non-claim directly — "Cost is not specified: cost-asymmetry is a quality of service an implementation may provide, not a correctness obligation, and is not among the claims below" — and drop the framing.

## OUT_OF_SCOPE

None. The ASN defers delivery (CN-OBT), V-spec/position-based counting, concurrency, caching, federation, and cost-as-primitive to the Open Questions rather than claiming them, and makes no claim that belongs in a sibling ASN. CN-OBT touches delivery only to disclaim it, which is in scope.

VERDICT: REVISE
