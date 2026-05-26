# Review of ASN-0077

## REVISE

### Issue 1: O11 formally covers K.μ⁺ only; K.μ⁺_L treatment is parenthetical

**ASN-0077, O11 derivation final paragraph**: "The same argument carries through verbatim for the link-subspace extension K.μ⁺_L (ASN-0047), which likewise extends `dom(M(d))` while preserving existing mappings; the parallel claim is omitted as a separate derivation."

**Problem**: O11's formal statement is restricted to K.μ⁺ ("For any reachable K.μ⁺ transition Σ → Σ' extending M(d)..."). The K.μ⁺_L generalization is asserted in prose but not formalized as a labeled, citable claim. The claims table mentions K.μ⁺_L only inside O11's row description. The proof structure does transfer (both transitions extend dom and preserve mappings, both subspace cases discharge via S3★ + O5), but downstream proofs needing monotonic growth under K.μ⁺_L cannot cite a labeled O11' — they must invoke the parenthetical extension. Per the standard "if cases differ, show each case," K.μ⁺ and K.μ⁺_L are formally distinct transitions with different preconditions and effects, and the formal scope of O11 should reflect both.

**Required**: Either (a) restate O11 generically — e.g., "For any reachable arrangement-extending transition that extends dom(M(d)) and preserves existing mappings (instantiated by K.μ⁺ and K.μ⁺_L)..." — with both as labeled instances, or (b) introduce a labeled parallel claim O11' for K.μ⁺_L. Option (b) would let the derivation confirm that preservation holds trivially because v_ℓ ∉ dom(M(d)) by construction (in the V_{s_L}(d) = ∅ case, v_ℓ has subspace s_L distinct from any s_C positions; in the V_{s_L}(d) ≠ ∅ case, v_ℓ = shift(max(V_{s_L}(d)), 1) is fresh by construction).

### Issue 2: Worked example does not contain a K.μ~ scenario the prose claims it discusses

**ASN-0077, O11 derivation closing sentence**: "...under K.μ⁻ (contraction) the inclusion can fail by loss of admissibility, and under K.μ~ (reordering) by mapping reassignment — both are discussed in the worked example."

**Problem**: The worked example contains transitions Σ₀ → Σ₁ (K.α + K.μ⁺) and Σ₁ → Σ₂ (K.μ⁻). No K.μ~ transition appears. The prose claim that "both" K.μ⁻ and K.μ~ are discussed is correct only for K.μ⁻; K.μ~ is named in the abstract commentary but no concrete scenario exhibits how reordering changes `origins_V`. This is the only place in the worked example where the mapping-reassignment failure mode of O7/O11 would be made concrete, and its absence weakens the example's coverage of the framework's non-extension transitions.

**Required**: Either (a) add a K.μ~ scenario — for instance, a transition where d₃ reorders its arrangement so that V-positions [1,1,3] and [1,1,7] swap their I-targets (each pointing to addresses from different origins), then verify origins_V(Σ, d₃, σ_{1..3}) shifts from {d₁} to a different set despite |dom(M(d₃))| being unchanged — or (b) revise the prose to "K.μ⁻ is discussed in the worked example; the K.μ~ failure mode is noted abstractly."

## OUT_OF_SCOPE

The ASN's Open Questions section already enumerates appropriate future work: cross-subspace I-span behavior, intermediate-chain visibility, native vs. transcluded distinction, unreachable-source-document protocols, historical containment vs. current arrangement, and intra-document sharing semantics under S5. No additional out-of-scope items identified.

VERDICT: REVISE
