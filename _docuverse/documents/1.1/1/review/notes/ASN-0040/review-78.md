# Review of ASN-0040

This is a mature, carefully-revised ASN. The core proofs (S(p,d) canonical form, S0, B5/B5a, B6 sufficiency+necessity, B7 disjointness, B1 contiguity, B2, B8, B9) are rigorous: inductions are complete, base/step cases are shown, edge cases (hwm=0 first child, d=1 vs d=2, genesis seed, equal- vs unequal-length parents) are all exercised, and the trace plus the three B7 illustrations supply concrete witnesses that map cleanly onto the proof's case splits. The co-reachability restriction on B8 is honest scoping (divergent version branches legitimately reuse an hwm), not a gap. I checked it against anti-bloat patterns specifically, given the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Condition-(i) justification duplicated into the Formal Contract postcondition slot
**ASN-0040, B6 prose vs. B6 Formal Contract postcondition (b)**:
- Prose: "Condition (i) is imposed by definition, not forced by stream validity: a pure-trailing-zero parent at d = 1 yields a T4-valid stream, yet we exclude it to break the aliasing..."
- Formal Contract (b): "...violating (ii) or (iii) forces a stream T4 violation. **Condition (i) itself is imposed by definition, not forced by stream validity — it disambiguates the d = 1 / d = 2 stream aliasing.**"

**Problem**: The second sentence of postcondition (b) restates the prose paragraph's point. A Formal Contract postcondition slot should state the postcondition (here: the necessity result for (ii)/(iii)); re-justifying *why precondition (i) is included* is essay content in a structural slot, and it duplicates the full account already given in prose. This is exactly the kind of meta-prose that compounds across cycles.

**Required**: Drop the second sentence from Formal Contract postcondition (b), leaving the necessity statement alone. The aliasing rationale is correct and worth keeping — but once, in the prose paragraph that already carries the concrete `([1,0],1)` / `([1],2)` aliasing example.

## OUT_OF_SCOPE

None beyond the topics the ASN already routes to its Open Questions and the Scope list (ownership/parent-prerequisite, `allocated(s) ⊆ s.B` activation discipline, bulk allocation, cross-replica ordering, subspace partitioning). These are correctly deferred, not errors here.

VERDICT: REVISE
