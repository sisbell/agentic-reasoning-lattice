# Review of ASN-0077

## REVISE

### Issue 1: O0(b) L-closure for K.σ routes through LP8 imprecisely
**ASN-0077, O0 derivation (b)**: "LP8 (DocumentRegistrationInvariance, ASN-0098) supplies coverage of K.σ — which lies outside ASN-0047's transition vocabulary and so is not addressed by the per-transition inspection above… LP8 is invoked here only to discharge K.σ."
**Problem**: LP8 asserts projection invariance and characterises K.σ's M-effect (registering d_new with M'(d_new)=∅, preserving prior M-entries). It does *not* assert L'=L for K.σ — projection's definition (`{v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(e)}`) consults only M and coverage, so LP8's projection-invariance proof is silent on L. The asymmetric counterpart in (c) for C-closure handles K.σ correctly by direct citation of K.σ's effect ("K.σ's effect names only M…, so by the same frame-exhaustiveness assumption invoked in (b) to discharge K.σ on L, C'=C"), but (b)'s LP8 route does not actually establish what (c) presupposes (b) established.
**Required**: Unify (b) and (c). Route K.σ's L-closure through the same direct argument used in (c): cite K.σ's effect/frame as naming only M, then apply frame-exhaustiveness for L. Alternatively, document that LP8 is being read as exhaustive of K.σ's relevant effects and justify that reading.

### Issue 2: Cross-ASN parenthetical citations to ASN-0093
**ASN-0077, O0 derivation**: Multiple occurrences of "K.σ (ASN-0093)" — in (b), in (c)'s parenthetical, and in the surrounding prose.
**Problem**: ASN-0093 is not in the foundation set listed for this review. The standards state: "If the ASN references another ASN by number… flag it as a REVISE item. The exception is foundation ASNs." While K.σ is itself referenced from foundation LP8, the direct "(ASN-0093)" parentheticals violate self-containment.
**Required**: Either remove the "(ASN-0093)" parentheticals (relying on LP8's mediation), or escalate the request to add ASN-0093 / its K.σ definition to the foundation set.

### Issue 3: Missing multi-step versions O11★ / O11'★
**ASN-0077, O11 and O11'**: Both are stated and proved for a single K.μ⁺ / K.μ⁺_L transition. O5★ and O6★ exist as inductive multi-step companions, but no parallel ★ versions exist for O11 / O11'.
**Problem**: The worked example labels "Transition Σ₀ → Σ₁ (allocation of native content in d₃)" as a single step but it is really a composite (two K.α + one K.μ⁺). The subsequent O11 verification then references "the K.μ⁺ transition Σ₀ → Σ₁" — invoking O11 across what is actually a bundled composite. Strict verification requires either decomposing into atomic steps and chaining O11 with O5/O6, or invoking a multi-step O11★ that does not exist.
**Required**: Add O11★ / O11'★ (straightforward composition argument: chain O11 across each K.μ⁺ step in a sequence, combined with O5★ for the intervening allocation steps), or decompose the worked example into atomic transitions so each ★-claim verification cites the appropriate atomic step.

### Issue 4: Worked example uses informal multi-transition labels
**ASN-0077, Worked example**: "Transition Σ₀ → Σ₁ (allocation of native content in d₃). d₃ natively appends two new characters at V-positions [1,1,6] and [1,1,7], allocated at [d₃.0.1.1] and [d₃.0.1.2] via K.α (ASN-0047) and arranged via K.μ⁺."
**Problem**: The label "Σ₀ → Σ₁" covers a sequence of distinct atomic transitions (two K.α plus one K.μ⁺). The verification subsections then refer to "the K.μ⁺ transition Σ₀ → Σ₁" — applying single-step O11 to what is really a composite. The intent is clear but the labeling obscures which atomic step each ★-claim is being verified against.
**Required**: Re-label as Σ₀ → Σ₀' (K.α) → Σ₀'' (K.α) → Σ₁ (K.μ⁺) so verifications cite atomic steps cleanly. This pairs naturally with adding O11★ / O11'★ from Issue 3.

### Issue 5: wp characterisations not explicitly exercised in worked example
**ASN-0077, Weakest precondition for single-origin output**: Two wp formulas are derived (`wp(SHOWORIGIN_I, |result|=1)` and `wp(SHOWORIGIN_V, d_q ∈ result)`), but the worked example does not walk through either against a specific state.
**Problem**: At Σ₁, `origins_I(Σ₁, σ_cover) = {d₁, d₃}` would let the reader verify wp(|result|=1) evaluates to false (non-empty intersection but not all addresses share origin). Similarly the V-span wp could be exercised by showing `d₂ ∉ origins_V(Σ₁, d₃, σ_{1..7})` despite d₂ being an intermediate transcluding document. Both are exactly the "operational use as a discovery probe" the ASN claims, but they are asserted rather than demonstrated.
**Required**: Add a short paragraph to the worked example showing each wp evaluated at a concrete state — both a satisfying and a falsifying configuration for each wp.

## OUT_OF_SCOPE

### Topic 1: Cross-subspace I-span semantics (Open Question 1)
**Why out of scope**: The ASN explicitly defines the I-span lift to drop link addresses; admitting link origins from an I-span is a future operation, not an error here.

### Topic 2: Chain visibility for transcluded content (Open Question 2)
**Why out of scope**: Surfacing intermediate transcluders is a different operation from origin reporting.

### Topic 3: Native-vs-transcluded distinction (Open Question 3)
**Why out of scope**: Distinguishing natively-allocated from transcluded content within a queried document is a separate operation.

### Topic 4: Historical containment from R (Open Question 4)
**Why out of scope**: Historical containment is recorded in Σ.R and queried by a distinct operation; SHOWORIGIN reports current arrangement origins only.

### Topic 5: Origin extension O0 as foundation candidate
**Why out of scope**: O0 extends `origin` to dom(L). Once other operations need it, extracting it from ASN-0077 into a foundation ASN may be appropriate. The ASN's choice to place it here (since it's first needed here) is reasonable; extraction is a future organisational concern.

VERDICT: REVISE
