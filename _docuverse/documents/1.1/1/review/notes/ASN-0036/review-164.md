# Review of ASN-0036

I checked every proof (S1, S4, S5 dual construction, S7, S8 with its within/across-subspace lemma, D-CTG-depth, D-SEQ) and the worked example. The mathematics is sound: the S8 incompatibility lemma correctly splits at j<m and j=m, the across-subspace argument correctly composes T5 with T10, the D-CTG-depth construction correctly forces infinitely many intermediates against S8-fin, and the boundary cases (empty document, single position, deletion) are all exercised. No correctness defects found. All foundation citations are to ASN-0034 (permitted), and the subspace-identifier-vs-separator distinction is handled correctly in S8a. The findings below are the bloat/redundancy patterns the `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: S8a is a tautological restatement of the domain-restriction axiom
**ASN-0036, S8a**: "`(A v ∈ dom(Σ.M(d)) :: (A i : 1 ≤ i ≤ #v : vᵢ > 0))`" — derived "via T0, NAT-discrete."
**Problem**: `zeros(t)` is defined (T4) as `#{i : tᵢ = 0}`. The domain-restriction axiom already supplies `zeros(v) = 0`, which over the ℕ-carrier is *definitionally equivalent* to "every component `> 0`." S8a therefore derives nothing new — it re-expresses an existing axiom conjunct in per-component form. The accompanying proof ("`zeros(v) = 0` forces each to be `≠ 0`, hence `≥ 1` by NAT-discrete instantiated at `m = 0`") is a multi-citation apparatus around a one-step unfolding. This is the "two statements say the same thing in different words" pattern, dressed as a theorem.
**Required**: Either fold the per-component positivity directly into the domain-restriction axiom's note (stating `zeros(v) = 0 ⟺ all components positive` once), or reduce S8a to a one-line alias without the NAT-discrete proof block. Downstream citations of S8a can then point at the axiom.

### Issue 2: S5 restates its own formal claim in prose
**ASN-0036, Sharing (S5)**: "The property is an architectural anti-constraint: the invariants place no finite cap on how many references may accumulate."
**Problem**: This sentence restates the property statement immediately above it ("they place no constraint on `|{(d, v) : …}|`"). The preceding clause — that multiplicity is finite in any single state but unbounded across states — is genuine clarification and should stay; the "architectural anti-constraint" sentence adds nothing the formal line did not already say.
**Required**: Delete the restatement; keep the per-state-finite/no-uniform-bound clarification.

### Issue 3: S7d carries document-lifecycle detail S7 does not consume
**ASN-0036, S7d**: "allocated via T10a … under the owning user's prefix."
**Problem**: S7 consumes exactly one fact from S7d — distinct documents have distinct document-level (`zeros = 2`) tumblers, via GlobalUniqueness. GlobalUniqueness needs only "distinct allocation events under T10a," not "under the owning user's prefix." The user-prefix clause is document-creation/ownership detail (an out-of-scope topic per the Scope section) that is not load-bearing for any claim in this ASN.
**Required**: Trim S7d to the minimal premise S7 needs (document-level tumbler, T10a allocation event, distinctness), dropping the owning-user-prefix elaboration.

## OUT_OF_SCOPE

### Topic 1: Operation-level preservation of D-CTG / D-MIN / S2
The ASN correctly defers (in Open Questions) the obligation that INSERT/DELETE/COPY/REARRANGE and the insertion-displacement mechanism preserve the contiguity invariants. This is operation-specific frame/postcondition territory, explicitly excluded by Scope — not a gap in this ASN.

### Topic 2: Subspace alignment between `subspace(v)` and the I-address element field
Whether `subspace(v) = v₁` must match the first element-field component of `M(d)(v)` is named as an operations-layer preservation obligation in the Open Questions. Correctly scoped out at the state-model level.

VERDICT: REVISE
