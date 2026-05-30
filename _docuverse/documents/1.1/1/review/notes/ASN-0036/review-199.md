# Review of ASN-0036

## REVISE

### Issue 1: Internal inconsistency in S5's two constructions
**ASN-0036, S5 proof**: Cross-document construction concludes "With the shared facts, `Σ_N` satisfies the state-level invariants S2, S3"; within-document construction concludes "With the shared facts, `Σ'_N` satisfies S0–S3."
**Problem**: The proof's own "Shared facts" paragraph carefully establishes that S0 and S1 are transition-level invariants that "impose no constraint on the standalone witness." The within-document conclusion then asserts the standalone state `Σ'_N` "satisfies S0–S3" — directly contradicting that framing and diverging from the parallel cross-document conclusion, which correctly names only S2, S3. Two parallel constructions should discharge the same obligations with the same wording.
**Required**: Change the within-document conclusion to "satisfies the state-level invariants S2, S3," matching the cross-document construction and the proof's transition-level argument.

### Issue 2: "Vacuously" misused for the length-1 run
**ASN-0036, S8 proof, "Partition" / "Coverage"**: "at minimum `(v, M(d)(v), 1)` is a run (conjunct (a) holds vacuously at `k=0`)."
**Problem**: For `n = 1`, the index `k` ranges over `{0}`, so conjunct (a) *is* evaluated at `k = 0`: it asserts `shift(v,0) ∈ dom(M(d))` and `M(d)(shift(v,0)) = shift(a,0)`, both of which hold by the convention `shift(t,0) := t` together with `a = M(d)(v)`. This is a trivially-true instance, not a vacuous one. "Vacuous" specifically means the quantifier ranges over the empty set, which is false here.
**Required**: Replace "holds vacuously at `k=0`" with "holds trivially at `k=0` by the convention `shift(t,0):=t`."

### Issue 3: OrdShiftHom cited for `i = 0`, outside its precondition
**ASN-0036, S8 proof, "Chains are runs"**: "By OrdShiftHom, each `shift(v, i)` is a well-formed V-position of the same subspace and depth."
**Problem**: OrdShiftHom's preconditions require `n ≥ 1`; at `i = 0`, `shift(v,0) = v` by convention, so OrdShiftHom does not apply to that index. The conclusion is still true (`v ∈ dom(M(d))` satisfies S8a directly), but the cited justification does not cover `i = 0`.
**Required**: Split the citation: `i = 0` is well-formed because `v ∈ dom(M(d))` satisfies S8a; `i ≥ 1` is covered by OrdShiftHom.

### Issue 4: S5's transition-level point stated twice (reviser drift)
**ASN-0036, S5 proof, "Shared facts" and "Conclusion"**: "Shared facts" says "S0 ... and S1 ... are transition-level invariants — quantified over transitions `Σ → Σ'`, not over a single state — so they impose no constraint on the standalone witness `Σ_N`"; "Conclusion" repeats "S0 and S1, being transition-level, impose no constraint on a standalone state."
**Problem**: The same observation is asserted in two paragraphs of one proof. Carrying the point once (where the witness obligations are enumerated) suffices; the restatement in the conclusion is the duplicated-claim pattern the anti-bloat classifier targets.
**Required**: State the transition-level scoping once in "Shared facts" and let the conclusion reference S2, S3 discharge without re-deriving why S0/S1 are exempt.

## OUT_OF_SCOPE

### Topic 1: Contiguity of non-text subspaces
D-CTG, D-MIN, D-SEQ are deliberately restricted to subspace `S = 1` per Nelson. Whether link/other subspaces carry analogous contiguity guarantees is a separate question (links are out of scope), not a defect here.

META: (none — the ASN defines abstract state, invariants, and a partition theorem stated implementation-independently; it has not drifted into mechanics.)

VERDICT: REVISE
