# Review of ASN-0082

## REVISE

### Issue 1: Statement Registry omits four cited foundation properties

**ASN-0082, Statement Registry**
**Problem**: TS4 (ShiftStrictIncrease), TA-assoc (AdditionAssociative), TumblerAdd (PositionAdvance), and TumblerSub (PositionReverse) are formally cited by name in derivations but absent from the registry.

- TS4 is cited in the Consistency paragraph ("shift(v, n) > v ≥ p by TS4 (ASN-0034)") and in the Gap region paragraph — used to establish that shifted outputs never land at or below p.
- TA-assoc is cited in the I3-S derivation of (a) ("TA-assoc (ASN-0034) applies") — the central algebraic step that commutes shift with span-reach.
- TumblerAdd is cited throughout ("By TumblerAdd (ASN-0034), shift(v, n)ᵢ = vᵢ for i < m" and in I3-S) — used for every component-level reasoning step about `⊕`.
- TumblerSub is cited in I3-S derivation of (b) ("By TumblerSub, the result is [0, …, 0, ℓₘ] = ℓ").

These are primary dependencies — each is invoked by name as a proof step, on par with TS1 and TS2 which are listed. The dependency graph is incomplete without them.

**Required**: Add registry rows for TS4, TA-assoc, TumblerAdd, and TumblerSub with type `cited (ASN-0034)`.

---

### Issue 2: Informal claim that actionPoint(ℓ) = m is "not restrictive" is too strong for m > 2

**ASN-0082, Span Width Preservation**: "The last condition is not restrictive: for a within-subspace span, actionPoint(ℓ) < m would change a component above the element-field ordinal, pushing the reach into a different subspace or document — so within-subspace spans necessarily have actionPoint(ℓ) = m."

**Problem**: For element-field tumblers of depth m ≥ 3, actionPoint(ℓ) = k with 2 ≤ k < m changes components above the deepest ordinal but does NOT change the subspace identifier (position 1 is copied from s whenever k ≥ 2). A span with actionPoint(ℓ) = 2 and m = 3 stays within subspace S — its reach has reach₁ = s₁ = S. The claim that such a displacement would "push the reach into a different subspace" is incorrect; it changes sub-structure within the subspace without crossing the subspace boundary.

The formal precondition `actionPoint(ℓ) = m` on I3-S is correct and well-motivated (it restricts to spans operating along the same axis as the ordinal shift). The issue is only with the justifying text.

**Required**: Either weaken the claim to "actionPoint(ℓ) < m would change structure above the deepest ordinal — for the typical m = 2 case this changes the subspace; for m > 2 it changes intermediate structure" or define "within-subspace span" precisely to mean a span that acts purely at the ordinal level, making the precondition definitional rather than argued.

## OUT_OF_SCOPE

### Topic 1: Shift composition for sequential insertions
**Why out of scope**: When a second insertion follows the first, the new insertion point may be in the shifted region or the gap. TS3 (ShiftComposition, ASN-0034) provides the algebraic building block, but the composition of two I3 postconditions — showing the second shift interacts correctly with the first — is operation-sequencing territory, not a defect in this single-insertion postcondition.

### Topic 2: Contraction (DELETE shift)
**Why out of scope**: The analog of I3 for deletion — where positions beyond the deletion point shift backward by n — requires separate treatment. Backward shift introduces new concerns (positions collapsing toward zero, potential emptying of subspaces) that have no counterpart here.

### Topic 3: Normalized span-set shift
**Why out of scope**: If a normalized span-set Σ has all component spans shifted by δₙ, does the result remain normalized? This follows from TS1 (order preservation) applied to both start and reach sequences, but establishing it formally belongs in a span-set operations ASN, not here.

VERDICT: REVISE
