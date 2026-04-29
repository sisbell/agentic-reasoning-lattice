# Review of ASN-0082

## REVISE

### Issue 1: Structural preservation omits S8-fin and S2

**ASN-0082, Structural preservation**: "We derive that S8-depth and S8a hold for the post-state M'(d), and that referential integrity (S3) is preserved, enabling composition with subsequent operations."

**Problem**: The paragraph commits to enabling composition but omits two invariants a downstream INSERT ASN will need:

- **S8-fin (FiniteArrangement)**: `dom(M'(d))` is finite. Follows from I3-CS and I3-CX (every post-state position originates from `dom(M(d))`, directly or via the injective shift (TS2)), plus S8-fin on the pre-state. Unstated and absent from the registry.

- **S2 (ArrangementFunctionality)**: `M'(d)` is a function. The consistency check establishes this — pairwise disjointness of assignment regions ensures no position receives two values — but the result is never named as S2 preservation or entered in the registry. The sentence "ensuring M'(d) and C' are well-defined" implicitly carries the S2 guarantee, but a consumer looking for S2 by name will not find it.

A downstream ASN composing the shift with gap-filling needs all structural invariants stated as citable postconditions, not left implicit in a consistency argument.

**Required**: Add named postconditions I3-fin (S8-fin preservation) and I3-S2 (S2 preservation) with brief derivations. Add both to the statement registry. The derivations are short — I3-S2 can cite the consistency check; I3-fin can cite I3-CS/I3-CX, TS2 injectivity, and pre-state S8-fin.

### Issue 2: Worked example does not trace I3-V

**ASN-0082, Worked Example**: The table shows positions present in the post-state but does not verify which positions are vacated by I3-V or why.

**Problem**: I3-V is a key postcondition — it prevents content duplication and completes the shift semantics. The worked example table shows only positions that ARE in `dom(M'(d))`. The vacated positions ([1,3] and [1,4]) are first mentioned in the "Arrangement invariants not preserved" paragraph, attributed to a D-CTG gap rather than traced through I3-V's logic. To verify I3-V against the example, a reader must independently reconstruct the shifted-image set `{[1,5], [1,6], [1,7]}` and check each original position's membership.

The overlap case is particularly worth showing: [1,5] is both an original position at or beyond p AND a shifted image (shift([1,3], 2) = [1,5]), so I3-V does not vacate it — I3 reassigns it with value M(d)([1,3]) = b + 2 instead of the original M(d)([1,5]) = b + 4. This case demonstrates that I3 and I3-V interact correctly through the exclusion condition, and should be made explicit.

**Required**: Add an I3-V trace to the worked example. Compute the shifted-image set, then for each original position at or beyond p, show whether it is vacated or retained. The [1,5] overlap case should be shown explicitly.


## OUT_OF_SCOPE

### Topic 1: Span behavior across the insertion point
**Why out of scope**: A span σ with `start(σ) < p` and `reach(σ) > p` has part of its denotation preserved in place (I3-L) and part shifted forward (I3). The post-state denotation is no longer contiguous — the gap tears it. Analyzing how such straddling spans decompose under the shift belongs in the INSERT ASN or a dedicated span-splitting analysis. The shift ASN correctly limits I3-S to spans within the shifted region (`s ≥ p`), where the algebraic result is clean.

VERDICT: REVISE
