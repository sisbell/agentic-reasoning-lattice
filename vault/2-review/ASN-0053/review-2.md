# Review of ASN-0053

## REVISE

### Issue 1: S1 and S3 preconditions omit level-uniformity

**ASN-0053, S1**: "For level-compatible spans α and β (level_compat(start(α), start(β)))"
**ASN-0053, S3**: same formulation

**Problem**: Both proofs invoke S6 to conclude that all boundary tumblers — starts, reaches, their min/max — share the same length. S6 delivers this only when each span is individually level-uniform (#start = #width), which guarantees #reach = #start. The stated precondition requires only that the two starts have equal length, not that each span be level-uniform. Without level-uniformity, a span's reach can have a different length from its start, and the displacement / round-trip arguments break.

S8 gets this right: "component spans are level-uniform and mutually level-compatible." S4 also gets it right by requiring "a level-uniform span σ." S1 and S3 do not.

**Required**: Change the precondition of S1 and S3 to: "For level-uniform spans α and β with level_compat(start(α), start(β))." S11's "(subject to D0)" parenthetical should similarly note level-uniformity as a precondition for representability.

### Issue 2: Round-trip identity used four times, never stated

**ASN-0053, S1/S3/S4/S8**: each constructs a span γ = (s, r ⊖ s) and asserts ⟦γ⟧ = {t : s ≤ t < r}

**Problem**: This requires s ⊕ (r ⊖ s) = r for same-length tumblers s < r. The "reach function" section proves the ingredient — (s ⊕ ℓ) ⊖ s = ℓ for level-uniform spans — but the general round-trip is never named or stated. The derivation is not trivial from ASN-0034: TA4 and the Reverse Inverse impose far stronger conditions (action point at last position, zero prefix, matching lengths). A reader checking S4's claim "the round-trip is faithful: s ⊕ (p ⊖ s) = p" finds no citable property.

The full chain is:
1. Given s < b with #s = #b, construct w by the TumblerAdd formula (wᵢ = 0 for i < k, wₖ = bₖ − sₖ, wᵢ = bᵢ for i > k where k = divergence(s, b)). Then s ⊕ w = b component-by-component.
2. The reach-function verification gives (s ⊕ w) ⊖ s = w.
3. Therefore b ⊖ s = w and s ⊕ (b ⊖ s) = b.

**Required**: State and prove a named lemma (e.g., D1 — DisplacementRoundTrip): for same-length tumblers a ≤ b with divergence k ≤ #a, a ⊕ (b ⊖ a) = b. The reach-function section already supplies the core argument; promote it.

### Issue 3: S5 action-point precondition is unnecessarily strong and proof has a gap

**ASN-0053, S5**: "with the additional assumption that d and ℓ have the same action point k"

**Problem (a) — proof gap**: The component-by-component proof applies TumblerAdd as if d' has action point k. When ℓₖ = dₖ (the split exhausts the width's value at position k exactly), d' = ℓ ⊖ d has its first nonzero at some k' > k. TumblerAdd then copies from d (not d') for positions k < i < k'. The proof's third line — "(d ⊕ d')ᵢ = d'ᵢ = ℓᵢ for i > k" — applies the wrong branch of TumblerAdd in this range. The result d ⊕ d' = ℓ still holds because dᵢ = ℓᵢ for those positions (a fact that follows from the shared-action-point assumption between d and ℓ), but the proof does not show this.

Concrete instance: σ = ([1, 3, 0, 1], [0, 2, 0, 5]), split at p = [1, 5, 0, 3]. Then d = [0, 2, 0, 2] and ℓ = [0, 2, 0, 5] share action point k = 2 with ℓ₂ = d₂ = 2. So d' = [0, 0, 0, 2] has action point 4, not 2.

**Problem (b) — precondition can be dropped**: Width composition holds for all level-compatible interior splits, not only those with matching action points. By the round-trip (Issue 2), s ⊕ d = p and p ⊕ d' = reach(σ). Then:

  (s ⊕ d) ⊕ d' = reach(σ) = s ⊕ ℓ
  s ⊕ (d ⊕ d') = s ⊕ ℓ            (associativity, ASN-0034)
  d ⊕ d' = ℓ                        (left-cancellation)

Left-cancellation of TumblerAdd is a short proof: if s ⊕ x = s ⊕ y with both well-defined, differing action points k₁ < k₂ yield sₖ₁ + xₖ₁ = sₖ₁ (contradicting xₖ₁ > 0), so action points agree, and components match at and beyond that point.

**Required**: Either (a) handle both sub-cases (d' at k and d' at k' > k) in the existing proof, or preferably (b) drop the action-point precondition, prove S5 via associativity + left-cancellation + round-trip, and state left-cancellation as a lemma. Option (b) strengthens S5 while simplifying the argument.

### Issue 4: Properties table uses span-set symbol for span properties

**ASN-0053, Properties table**: labels "Σ.reach" and "Σ.denotation"

**Problem**: These use Σ (capital sigma, the span-set symbol used throughout) but describe properties of individual spans (σ). The body text consistently uses σ for spans. The third entry "Σ.setdenotation" correctly uses Σ for a span-set property.

**Required**: Change to σ.reach and σ.denotation.

## OUT_OF_SCOPE

### Topic 1: Span-set intersection and difference

S1 covers two-span intersection; S11 covers containment difference. The extensions — intersecting or differencing two span-sets — are natural compositions of single-span operations plus normalization, but the resulting bounds and construction deserve explicit treatment.

**Why out of scope**: New algebraic operations building on what this ASN establishes, not corrections to it.

### Topic 2: Left-cancellation as a tumbler arithmetic property

TumblerAdd is left-cancellative (s ⊕ x = s ⊕ y ⟹ x = y when both sides are well-defined). This is a property of the arithmetic from ASN-0034, not of spans. If used to clean up S5, it should be established in the tumbler-arithmetic foundation and cited here.

**Why out of scope**: Foundation arithmetic property, belongs as a supplement to ASN-0034.

VERDICT: REVISE
