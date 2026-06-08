# Review of ASN-0099

I checked each claim against its derivation, traced the preservation lemmas across the full ASN-0047 extended vocabulary, and verified the worked example and the weakest-precondition analysis.

## Coverage of the operation surface

The two-phase factoring (image V→I, findlinks I→Link) is clean, and the effect of *every* operation in `V` on `findlinks(I, ·)` is characterized: A1a covers all of `V ∖ {K.λ}` (atomics publish `L' = L`, K.μ~ by composition), and F9-λ characterizes the unique store-changing step `K.λ` as a disjoint-union increment. This is genuinely exhaustive over the vocabulary, not a "by similar reasoning" gesture.

Boundary cases are all present and correct: `I = ∅`, `dom(Σ.L) = ∅`, `R` disjoint from the arrangement, empty constraint set `C = ∅` (vacuous universal → `dom(Σ.L)`), empty constraint target `J = ∅` (→ `∅`), empty scope, and the `ℛ = ∅` total-clearance boundary of F21 (wp = false). The `N = 0` empty-union case in the filtered-unfolding identity is handled.

The technical core holds under scrutiny:
- F21's image-collapse to `R ∩ ℛ` and the reduction to `(E i : project ∩ R ∩ ℛ ≠ ∅)` is correct, with both specializations (full-document = LP12a lift; `ℛ = ∅`) discharged.
- F23's demonic-wp composition (Step 1 law, Step 2 LP9 monotonicity giving `Q ⟹ wp(K.μ⁺,Q)` on enabled states, Step 3 postcondition-monotonicity) is carefully stated and sound.
- F22 correctly restricts reordering-invariance to `R = T`, where LP11 range-invariance makes the I-argument fixed; partial-`R` invariance would be false and is rightly not claimed.
- The I-side vs V-side distinction (F11/F19 vs F21/F22/F23) is the right architectural separation — `findlinks` depends only on `Σ.L`, so M-only edits leave it invariant while V-side answers can shrink under K.μ⁻.

The worked example exercises F1, F6 (transclusion), filtered conjunction, cross-subspace link-image routing through S3★, F9 multi-step inertness, and F11+F9-λ+F19 across `K.λ`, with concrete tumblers and verified overlaps. The F4 individuation witnesses (including the now-justified non-empty slots in Strengthening 1) correctly pin F1's per-endset overlap form against the four alternative designs.

## OUT_OF_SCOPE

### Topic 1: Inverse direction (result endsets → V-positions)
**Why out of scope**: FOLLOWLINK/RETRIEVEENDSETS is correctly deferred and listed under "What We Have Not Specified."

### Topic 2: Auditability witness and latency bound
**Why out of scope**: The two Open Questions (recoverable index-agreement witness; abstract latency handle) are genuinely new territory for a future ASN, not defects here.

No META: the ASN specifies abstract state, a query operation, and its invariants (determinism, persistence, monotonicity, wp under edits) — pinned by the F2∧F3 obligation so any conforming implementation must satisfy them. It has not drifted into implementation mechanics.

VERDICT: CONVERGED
