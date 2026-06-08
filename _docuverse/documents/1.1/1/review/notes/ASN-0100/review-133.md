# Review of ASN-0100

The proof obligations are met with unusual thoroughness: every conjunct of `ExtendedReachableStateInvariants` is discharged, the composite-boundary couplings are tracked through each intermediate, all boundary cases (empty `V_{s_C}`, prepend forcing full clearance, append omitting K.μ⁻, deep `m_C ≥ 3` off-prefix exclusion, re-insertion with chain/V-index decoupling) carry their own worked example, and the recent S3★ fix correctly severs the I3 inheritance at the content-frame boundary. The findings below are anti-bloat (this note carries `review-mode.anti-bloat`), not correctness.

## REVISE

### Issue 1: Cross-document projection invariance stated twice
**ASN-0100, §Cross-document independence and §Coverage and link discoverability (INS.proj)**: §Cross-document independence asserts "for any link ℓ ∈ dom(L) and any document d' ≠ d, project(ℓ, i, d', Σ') = project(ℓ, i, d', Σ) — the projection ... depends only on M(d') and on ℓ's coverage, both unchanged here." §Coverage then states and *derives* the identical claim (INS.proj, `d' ≠ d` case: "π is the identity and N_{ℓ,i} = ∅ ... LP4 ... composing across the finite step sequence ... yields project(ℓ, i, d', Σ') = project(ℓ, i, d', Σ)").
**Problem**: Two paragraphs make the same claim; the first is an un-derived hand-wave ("depends only on ..., both unchanged") subsumed by the second's LP4 derivation. This is the "two paragraphs say the same thing in different words" accretion pattern.
**Required**: Drop the projection sentence from §Cross-document independence (keep only the arrangement/content-frame independence there) and let INS.proj be the single site, or have §Cross-document independence forward exactly once without restating the equation.

### Issue 2: Forward-deferral parenthetical in a structural slot
**ASN-0100, §Effect One**: "Branch selection keys on dom(C) ... even when V_{s_C}(d) = ∅. (The worked example 'Re-insertion into a cleared content subspace' exercises this.)"
**Problem**: The parenthetical is a use-site pointer to a downstream worked example. The decoupling point is already made by the sentence itself, and the worked example stands on its own; the cross-reference is removable accretion, not reasoning that advances the claim.
**Required**: Delete the parenthetical. The preceding sentence already states the subtlety.

## OUT_OF_SCOPE

(none — the §Bounding the Scope list and Open Questions appropriately defer link-subspace insertion, COPY, DELETE, version derivation, and replication without specifying them.)

VERDICT: REVISE
