# Review of ASN-0047

## REVISE

### Issue 1: K.μ~ decomposition undefined when content subspace is empty

**ASN-0047, Elementary transitions**: "When dom(M(d)) is non-empty, it decomposes into K.μ⁻ (removing content-subspace mappings) followed by K.μ⁺ (re-adding content-subspace mappings at new positions)."

**Problem**: The decomposition is undefined when `dom(M(d)) ≠ ∅` but `dom_C(M(d)) = ∅` — a document with link-subspace positions only. K.μ⁻ requires `dom(M'(d)) ⊂ dom(M(d))` (strict); there are no content-subspace positions to remove. Removing link-subspace positions is fatal: K.μ⁺ (amended, `subspace(v) = s_C`) cannot restore them. The state is reachable: K.δ + K.λ + K.μ⁺_L produces a document with `V_{s_L}(d) ≠ ∅` and `V_{s_C}(d) = ∅`.

The same gap propagates to four locations:

1. **"The decomposition into K.μ⁻ + K.μ⁺ is a vacuous round-trip"** — there are no content-subspace positions to round-trip. The identity on M(d) is not a K.μ⁻ + K.μ⁺ sequence; it is zero elementary steps.

2. **ValidComposite★**: "K.μ~ appearing in the sequence is shorthand for its K.μ⁻ + K.μ⁺ decomposition — it expands into two consecutive elementary steps" — false when `dom_C(M(d)) = ∅`. A composite containing K.μ~ on such a document is not well-formed under the stated definition.

3. **ExtendedReachableStateInvariants proof, Class (a), K.μ~**: "K.μ~ decomposes into K.μ⁻ + K.μ⁺" — the proof mechanism fails. The conclusion (all invariants preserved) is correct — `M'(d) = M(d)` trivially preserves everything — but the proof as written does not cover this case.

4. **"For any bijection π, a valid decomposition always exists"** — false for `dom_C = ∅`, `dom_L ≠ ∅`, where π is forced to be identity by link-subspace fixity and the n' = 0 strategy produces zero elementary steps rather than the claimed K.μ⁻ + K.μ⁺ pair.

**Required**: Add an explicit case: when `dom_C(M(d)) = ∅`, link-subspace fixity forces π to fix all positions, producing `M'(d) = M(d)` — K.μ~ expands into zero elementary steps. Update ValidComposite★'s expansion clause to "zero or two consecutive elementary steps." Add the trivial `M'(d) = M(d)` case to the ExtendedReachableStateInvariants proof for K.μ~.

## OUT_OF_SCOPE

### Topic 1: Link arrangement uniqueness
**Why out of scope**: K.μ⁺_L has no precondition preventing the same link ℓ from being arranged at multiple V-positions via repeated application. Whether duplicate link arrangements should be prohibited is a link-subspace semantic question — the ASN's own open questions ask "What invariants must the link subspace satisfy beyond those inherited from D-CTG, D-MIN, and S8-depth?" This belongs in a future link-subspace ASN, not a revision of this one.

VERDICT: REVISE
