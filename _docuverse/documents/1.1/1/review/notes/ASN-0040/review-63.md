# Review of ASN-0040

## REVISE

### Issue 1: The namespace-disjointness exception is stated four times

**ASN-0040, S2 Remark / B6 necessity / B6 Postconditions (b)**: The same point — that a pure trailing-zero parent at d=1 yields a T4-valid stream and condition (i) is retained there only for namespace injectivity — appears in four places:
- S2 Remark: "This is a design motivation for retaining condition (i) where T4 does not force it, not a T4-necessity step."
- B6 necessity opening: "with one exception noted below: a pure trailing-zero parent at d = 1 yields a T4-valid stream, and condition (i) is retained there for the namespace-disjointness reason recorded in the S2 remark above."
- B6 sub-case (b): "at d = 1 such a parent yields a T4-valid stream and is retained for the namespace-disjointness reason recorded in the S2 remark."
- B6 Postconditions (b): "with one exception: a pure trailing-zero parent at d = 1 ... (a design motivation, not a T4-necessity step; recorded in the S2 remark)."

**Problem**: Three downstream paragraphs defer to one location (the S2 remark) and restate its content in slightly different words — the exact compounding pattern the anti-bloat classifier flags. The precise reader must reconcile four near-identical statements to confirm they say the same thing.

**Required**: State the exception once (the S2 remark is the natural home). In B6 necessity, the single phrase "the d=1 trailing-zero case is the S2 exception" suffices; delete the re-explanations in sub-case (b) and Postconditions (b).

### Issue 2: "Sufficient statistic" derivation duplicated between hwm and B2

**ASN-0040, hwm Justification and B2 commentary**: hwm's Justification argues "knowing only #children(B, p, d) determines max(children(B, p, d))" and concludes "the count alone is a sufficient statistic for the allocation state of the namespace." B2's commentary then repeats: "No counter distinct from the data, no free list, no reservation table. The cardinality of the existing children is a sufficient statistic for the next allocation."

**Problem**: Two paragraphs in adjacent sections make the same claim. The hwm Justification re-derives from B1 what B2 then proves formally; the prose conclusions are interchangeable.

**Required**: Let hwm carry the definition and the one-line "count determines the prefix" observation; let B2 carry the formal proof. Remove the duplicated "sufficient statistic" prose from one of them.

### Issue 3: B0b previews its own consumers and proof method

**ASN-0040, B0b**: "The registry-invariant proofs below — B1, B_fin, B10 — share an induction skeleton." and "Consequently, to show that a registry invariant holds in every reachable state it suffices to (i) verify it at the seed B₀ and (ii) show it survives the single element next(s.B, p, d) ..."

**Problem**: The first sentence is a downstream-consumer inventory (the flagged pattern). The second pre-states the induction recipe that B1, B_fin, and B10 each then carry out in full — so the recipe is written four times. B0b's *content* (the dichotomy `s'.B = s.B` or `s'.B = s.B ∪ {one element}`) is load-bearing and should stay; the consumer list and method-preview are not.

**Required**: Keep the dichotomy statement. Delete the "proofs below ... share an induction skeleton" inventory and the "it suffices to (i)...(ii)..." preview — the three proofs already cite "By B0b" at the exact step they need it.

### Issue 4: B9 trace defers to B9's own proof

**ASN-0040, B9 trace (Step 7 commentary)**: "(The general no-ceiling argument that licenses arbitrarily many such steps lives in B9's proof; the trace only instantiates it.)"

**Problem**: A parenthetical pointing from the worked trace to the co-located proof of the same property. The reader has just read B9's proof a few lines above; the pointer advances nothing.

**Required**: Delete the parenthetical. The trace stands on its own as a concrete instantiation.

## OUT_OF_SCOPE

### Topic 1: Cross-branch uniqueness of baptismal acts
B8 explicitly scopes itself to co-reachable acts and declares cross-branch uniqueness "unaddressed." This is correctly deferred — it belongs with a treatment of branching/merge in the reachability relation, not this ASN. Not an error; the scoping is stated honestly.

META: not applicable — the ASN defines a state component (s.B), an operation on it (baptize), and growth invariants (B0/B1/B7/B8/B9/B10) at the abstract level any implementation must satisfy; it has not drifted into implementation mechanics.

VERDICT: REVISE
