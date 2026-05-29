# Review of ASN-0053

## REVISE

### Issue 1: Level-compatibility is defined twice, with a forward pointer

**ASN-0053, "reach function" section**: "Two tumblers are *level-compatible* when they have the same length, and a span σ = (s, ℓ) is *level-uniform* when its start and width share a length, #s = #ℓ. ... (S6 below states level-compatibility formally as the predicate level_compat.)"

**Problem**: The same two concepts are introduced informally here and then formally restated in S6. The parenthetical is a bare forward pointer that advances no reasoning at its point of occurrence — exactly the forward-reference accretion the `review-mode.anti-bloat` classifier targets. A reader must hold an informal definition, then reconcile it with the numbered one.

**Required**: Define level_compat / level-uniform once. Either move S6 ahead of WR (WR is the first consumer), or state the predicate at first use and drop the duplicate. Remove the "(S6 below…)" pointer.

### Issue 2: S6's definition slot carries use-site justification

**ASN-0053, S6**: "A level-uniform span automatically satisfies D0 for the (start(σ), reach(σ)) pair: by TA-strict… The level_compat precondition is what excludes the troublesome case: a deeper-level point such as [1, 3, 0, 1]…"

**Problem**: "Automatically satisfies D0" is a fact consumed by S1/S3/WF, not a clause of the definition. Placing the D0-discharge argument in the definition is use-site inventory in a structural slot — the same discharge is then repeated verbatim inside WR, WF, S1, S3. The definition should say what level_compat *is*; the D0 discharge belongs once, where it is used (it already recurs there).

**Required**: Reduce S6 to the predicate and the "all boundaries share length L" consequence. Drop the D0-satisfaction sentence (it is re-derived at each consuming claim).

### Issue 3: S9 closes with a scope-deferral to an Open Question

**ASN-0053, end of S9**: "This uniqueness is fixed-instant: S8–S9 concern a fixed span-set's canonical decomposition, not its stability as new addresses are allocated into the ambient population — Open Question 1 poses that concern."

**Problem**: This sentence explains what the claim does *not* cover and defers to a downstream location. It is meta-prose around the proof boundary, not part of the argument. The Open Questions section already poses the concern.

**Required**: Delete. The Open Question already records the deferral.

### Issue 4: WR section's right-cancellation excursion is unused content

**ASN-0053, after WR**: "Of the three quantities — start, width, reach — two of the three pairings determine the third… But width and reach do not determine start: ⊕ is not right-cancellative (TA-RC, ASN-0034)… s₁ = [1, 3, 5] and s₂ = [1, 3, 7] with width [0, 2, 4]…"

**Problem**: This restates a foundation property (TA-RC / TA-MTO) and supplies an example for a fact — non-recoverability of start from (width, reach) — that no later claim in this ASN uses. Spans are identified by (start, width); the asymmetry is never consumed. It is essay content padding a structural slot.

**Required**: Either trim to the one load-bearing sentence ("start ⊕ width determines reach; start ⊕ reach determines width by D2") or cut the s₁/s₂ excursion entirely.

## OUT_OF_SCOPE

### Topic 1: Intersection/merge/difference for spans at differing hierarchical levels
**Why out of scope**: The algebra is restricted to level-uniform, level-compatible spans throughout, and cross-level behavior is correctly posed as Open Question 2. New territory, not an error here.

### Topic 2: Split at a finer-level interior point
**Why out of scope**: S4 requires level_compat(s, p). Splits at deeper points are posed as Open Question 3. Correctly deferred.

### Topic 3: Span-set difference bound
**Why out of scope**: S11d bounds single-span difference; span-set vs span-set difference is Open Question 7. Future ASN.

VERDICT: REVISE
