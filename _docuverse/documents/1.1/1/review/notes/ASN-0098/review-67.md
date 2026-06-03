# Review of ASN-0098

## REVISE

### Issue 1: LP-Fin Corollary cites sub-case labels that do not exist in the proof

**ASN-0098, "Boundary and Width Behaviour" (LP-Fin Corollary)**: "cross-document chains are excluded by the proof's `#d ≤ #d_0` bound (sub-cases (i) and (ii) of the bound argument) together with sub-case A's separator argument at lengths `z_2 < #d < #d_0`"

**Problem**: The bound argument in LP-Fin (`*Bound #d ≤ #d_0.* Suppose #d > #d_0. … Hence #d ≤ #d_0.`) is a single contradiction with no numbered sub-cases. There is no "sub-case (i)" or "sub-case (ii)" of the bound argument to refer to. The cross-reference is dangling — a stale label from an earlier draft of the proof. The underlying claim is fine (cross-document candidates have `#d ≤ #d_0`, then `#d < #d_0` is killed by sub-case A and `#d = #d_0` forces `d = d_0` by T3, so no cross-document candidate survives), but the citation names structure that isn't there.

**Required**: Replace the parenthetical with an accurate pointer — e.g., "by the `#d ≤ #d_0` bound, which forces any cross-document candidate's document prefix to a proper prefix of `d_0` (`#d < #d_0`), excluded by sub-case A; `#d = #d_0` collapses to `d = d_0` by T3."

### Issue 2: Worked-trace admissibility check is skippable verification that does not advance the displacement reasoning

**ASN-0098, "A Worked Trace" (*Admissibility check.*)**: the full paragraph verifying S8a, S8-depth, D-MIN★, D-CTG★, D-SEQ★, S3★, and `π ≠ id` conjunct-by-conjunct for the 3-element permutation `π(v₁)=v₃, π(v₂)=v₂, π(v₃)=v₁`.

**Problem**: The example's purpose is to exhibit projection *displacement* under K.μ~, and the displacement results (`project(a, 2, d₁, Σ_3) = {v₃} = π(project(a, 2, d₁, Σ_1))`, etc.) are already stated before this paragraph. The conjunct-by-conjunct admissibility verification re-establishes operation legality but does not advance the projection reasoning — a precise reader skips it to follow the claim. The entire check reduces to one observation: K.μ~-FIX fixes the V-position *set*, every shape invariant (S8a, S8-depth, D-CTG★, D-MIN★, D-SEQ★) is a property of the V-positions alone and so is preserved, S3★ holds because all three I-addresses are content-subspace, and `π ≠ id`. This is exhaustiveness content padding an example slot.

**Required**: Compress to one or two sentences — π permutes the K.μ~-FIX-fixed V-position set, so the shape invariants (depending only on the V-positions, not the mapping) carry over, S3★ holds by content-subspace targeting, and `π(v₁) = v₃ ≠ v₁`.

## OUT_OF_SCOPE

### Topic 1: Reverse-discovery primitive, V-order preservation, link-to-link induced discovery, cross-document operation comparability, fork link-subspace non-transclusion, link-canonical contraction discoverability

**Why out of scope**: These are exactly the note's own "Open Questions" — each names a new state predicate or operation invariant not yet defined here. They belong in successor ASNs, not as revisions to the projection-displacement claims this note establishes.

VERDICT: REVISE
