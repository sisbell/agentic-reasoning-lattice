# Review of ASN-0053

## REVISE

### Issue 1: S6 restates its own load-bearing fact in two consecutive paragraphs

**ASN-0053, S6 (LevelConstraint)**: Paragraph A — "A level-uniform span automatically satisfies D0 for the (start(σ), reach(σ)) pair: by TA-strict, start(σ) < reach(σ); and since #start(σ) = #reach(σ), neither is a proper prefix of the other, so divergence is of type (i) with k ≤ #start(σ)." Paragraph B — "The load-bearing fact is the one just stated: when #s = #ℓ, every endpoint pair drawn from the span has equal length, so divergence is of type (i) with k ≤ #start, and D0 is satisfied."

**Problem**: Paragraph B announces that it is restating paragraph A ("the one just stated") and then does so. Same claim, same chain, different words — the precise reader must verify they are identical before moving on. This is the anti-bloat duplicate-paragraph pattern.

**Required**: Delete paragraph B; the D0-satisfaction fact is fully stated in paragraph A. Fold the only new content (the deeper-interior-point counterexample at [1,3,0,1]) onto the surviving paragraph.

### Issue 2: S6's opening enumerates downstream consumers instead of defining

**ASN-0053, S6 (LevelConstraint)**: "The properties that follow — intersection, merge, split, normalization — require span operands to be level-compatible. We formalize this now, since every subsequent operation depends on it."

**Problem**: This is a use-site inventory ("intersection, merge, split, normalization") plus a why-it-is-needed rationale, not content that advances the definition of level-compatibility. The definition stands on its own; the consumer list rots as the algebra changes and adds nothing the reader needs to understand `level_compat(t₁, t₂) ≡ #t₁ = #t₂`.

**Required**: Open S6 with the definition. Drop the consumer enumeration and the "we formalize this now" rationale.

### Issue 3: The D0/D1 setup forward-references S6 and defends excluded cases

**ASN-0053, "The reach function"**: "For #a > #b, the foundation already settles the failure… When #a < #b and a is a proper prefix of b… no valid displacement exists. Since every span operation below uses level-uniform spans with #start = #reach, the equal-length case is all we need. We formalize the sufficient condition as level compatibility in S6."

**Problem**: This paragraph works through the #a > #b and #a < #b cases only to conclude they never arise, then forward-points to S6. It is defensive justification for inputs the carrier (level-uniform spans) already excludes, plus a deferral to a downstream definition — the same level-compat point is then made again in S6. The reach function only needs the equal-length width-recovery fact; the dichotomy walkthrough is accretion.

**Required**: State the width-recovery result for equal-length endpoints directly. Drop the #a≠#b case analysis and the "we formalize this in S6" pointer; let S6 introduce level-compatibility once.

### Issue 4: S1 asserts the intersection denotation without the element-chase it gives elsewhere

**ASN-0053, S1 (IntersectionClosure)**: "Otherwise r' > s', and: ⟦α⟧ ∩ ⟦β⟧ = {t : s' ≤ t < r'}. This is a half-open interval."

**Problem**: The core claim — that the intersection of the two half-open intervals equals [s', r') — is asserted in one line, while the structurally identical union claim (S3) and the difference claims (S11, S11c) are each established by explicit element-chasing. For uniform rigor the intersection equality should be shown (t ∈ ⟦α⟧ ∩ ⟦β⟧ ⟺ max(starts) ≤ t < min(reaches)), not asserted.

**Required**: Add the two-direction membership argument, matching the standard set in S3/S11.

## OUT_OF_SCOPE

The Open Questions already route operation-level effects (INSERT/DELETE/REARRANGE), subspace-boundary guarantees, and span-set difference bounds to future ASNs; no additional out-of-scope topics need flagging.

VERDICT: REVISE
