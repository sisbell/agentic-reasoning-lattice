# Review of ASN-0127

I worked through every claim, recomputed every witness, and checked the case analyses for completeness. This is an unusually disciplined note: the two-phase factoring is honest about being a *definition* (F-V), the two stability keystones are deliberately kept separate (F-CIL for the store-fixed lane, LP13 for the existence lane), and the hard cases — non-injective image swings, full clearance, the discovery/existence asymmetry — are confronted directly rather than waved through. I found no REVISE-worthy defect.

## REVISE

None.

What I verified, with the points most likely to hide a bug:

- **F-IMG-SWING witnesses.** Both the injective lateral swing (`{a} → {b}`) and the non-injective gain (`{a} ⊊ {a,b}`) recompute correctly under the bijection equation `Σ'.M(d)(π(u)) = Σ.M(d)(u)`, including `π⁻¹(W)` and the preserved `ran`. The claim that strict containment of the *image* requires a non-injective arrangement, while incomparable swings are realizable under *both* injectivity regimes, holds: the `v₁↦a, v₂↦b, v₃↦c, v₄↦a` witness produces `{a,b} ↔ {a,c}` (incomparable) under non-injectivity, exactly as asserted.
- **The image-cardinality vs discovery-cardinality distinction** (D-NONMONO reorder clause + worked illustration's cardinality-changing variant). The variant keeps the arrangement injective (image cardinality pinned at 1) yet moves the discovery set `{L_1} → {L_2, L_2'}` (cardinality 1→2) purely through link structure. This is the subtle point most likely to be gotten wrong, and it is correct.
- **D-CWP bridge.** `I_R = image(W,d_q,Σ') ⊆ image(W,d_q,Σ)` is discharged by F-IMG-CONTR, so `image(W,d_q,Σ) = I_R ∪ Δ` is sound; the `A = A ∪ B ⟺ B ⊆ A` reduction yields a genuine pre-state-only weakest precondition, and the `R = ∅` boundary correctly collapses to `findlinks_disc(W,d_q,Σ) = ∅`. The grain contrast with LP12a's single-link `wp ≡ false` is accurate.
- **Existence lane.** E-INV's reliance on LP13 (not merely LP3★) is correctly justified — LP3★ fixes per-slot coverage but not the arity bound over which the `matches` existential ranges; LP13 supplies both. E-CONS's exclusion direction genuinely uses E-INV, and D-ZERO's "historical absence" argument chains E-MONO + E-INV soundly.
- **Case completeness.** All seven atomic transitions plus K.μ~ are accounted for in D-NONMONO (the four on-`d_q` arrangement cases, plus K.α/K.δ/K.λ/K.ρ folded into "transitions not on `d_q`"). The worked illustration verifies F-INERT, the contraction/extension/reorder clauses, F-LAMBDA, and the existence-vs-discovery-zero contrast against a concrete scenario, with the link/arrangement admissibility checks (K.μ~-FIX, length/subspace preservation, D-CTG★/D-MIN★ on the fixed V-domain) stated where needed.
- **Foundation hygiene.** `image`, `matches`, `findlinks` are new primitives, not reinventions — `image` is the V→I forward image, genuinely distinct from ASN-0098's I→V `project`. Every cross-ASN reference (0034, 0036, 0043, 0047, 0058, 0093, 0098) targets a foundation. `subtree`, `coverage`, `δ` are used per their foundation definitions.

## OUT_OF_SCOPE

### Topic 1: Path-level (multi-step) discovery characterization
The existence lane gets a multi-step treatment (E-MONO, E-CONS over `Σ →* Σ'`), but the discovery lane is analyzed only per-step (D-NONMONO case analysis, D-CWP single-step wp). A net-effect characterization of `findlinks_disc` across a *sequence* of edits has no analog here.
**Why out of scope**: The single-step discovery analysis plus the existence-lane closure is sufficient to pin down the algebra and its stability classification; multi-step discovery composition is a natural successor, not a gap in this foundation. It sits beyond even the note's own Q3 (which asks only for a *single-step* uniform wp).

### Topic 2: The note's own open questions are correctly placed
Content-keyed queries (Q1), filter-set distributivity (Q2), uniform single-step wp (Q3), and the inverse composition with ASN-0098's projection (Q4) are each genuinely new territory rather than holes in the present scope.
**Why out of scope**: These are correctly identified by the ASN as future work; flagging them would be redundant.

VERDICT: CONVERGED
