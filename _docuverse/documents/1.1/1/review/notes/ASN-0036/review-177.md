# Review of ASN-0036

The mathematical core is sound. I checked every proof — S1 (trivial from S0), S4 (clean reduction to GlobalUniqueness), the S5 constructions, the S8 partition lemma, D-CTG-depth, and D-SEQ — and found no logical gaps. Boundary cases (empty arrangement, single-subspace, m=2 vs m≥3) are handled, and the worked example concretely verifies S0/S3/S5/S7/S8/D-SEQ across three states. The findings below are anti-bloat / forward-reference prose, which this note's classifier directs me to surface.

## REVISE

### Issue 1: Forward-reference circularity justification in S5
**ASN-0036, Sharing (S5 proof, "Genuine strand state")**: "The structural requirements S7*, S8-*, and D-* are stated in the later sections Structural attribution, Singleton span partition, and Arrangement contiguity; since none of their statements depends on S5, the forward references in the constructions below carry no circularity and may be discharged once those sections are reached."
**Problem**: This is exactly the flagged pattern — prose justifying document ordering with a non-circularity argument, plus a multi-target deferral ("see sections X, Y, Z below"). It advances no reasoning about sharing multiplicity; the reader must skip past it to reach the constructions.
**Required**: Delete the circularity sentence. The constructions verify each invariant in place; if a forward label needs naming, name it without the meta-argument about ordering.

### Issue 2: S5 double-counts the domain-restriction axiom and S8a
**ASN-0036, Sharing (S5)**: the "Genuine strand state" list names "the domain-restriction axiom on Σ.M(d) (`zeros(v) = 0 ∧ #v ≥ 2`, equivalently S8a)", and the Postconditions/Depends then list "...the domain-restriction axiom, S8a" as two separate entries.
**Problem**: The note states the two are equivalent (S8a is "a one-line reformulation of the domain-restriction axiom, not an independent claim") and then enumerates both as distinct requirements. Two slots saying the same thing.
**Required**: List one (the domain-restriction axiom or S8a), not both, in the requirement set and Depends.

### Issue 3: Defensive n=0 exclusion in ValidInsertionPosition
**ASN-0036, Valid insertion position (ValidInsertionPosition, Derivation)**: "...at `j = 0` the position is `min(V_1(d)) = [1, ..., 1]` directly by D-MIN — the same form with last component `1` — so no extension of OrdinalShift (which requires `n ≥ 1`) to `n = 0` is invoked."
**Problem**: Borderline. The j=0 case genuinely differs (OrdinalShift requires n≥1), so noting it is defensible, but the trailing clause "so no extension ... is invoked" pre-empts an objection rather than stating what the j=0 position is. Mild meta-prose.
**Required**: State the j=0 case as `v = min(V_1(d))` and stop; drop the "no extension ... invoked" justification.

## OUT_OF_SCOPE

### Topic 1: Operation-layer preservation of D-CTG/D-MIN/S2
The final Open Question (and S3's "Preservation across transitions" clause) gestures at how INSERT/DELETE/COPY maintain the contiguity invariants. This is correctly deferred — operation frame/postconditions are out of scope per the Scope section, and the state-model invariants stand independently of them.

META: not applicable — the ASN specifies abstract state, transition invariants, and arrangement structure that any implementation must satisfy; it has not drifted into implementation mechanics.

VERDICT: REVISE
