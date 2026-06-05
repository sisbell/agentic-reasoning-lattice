# Review of ASN-0112

This ASN is unusually careful — the case analysis for well-formedness (V2 via D0/D1 without assuming level-uniformity), the explicit endpoint-depth-divergent worked example, and the empty-vs-zero-width distinction (V11) are all rigorous and correctly discharged. I checked the displacement arithmetic in all three worked examples and the D0/D1/TumblerSub appeals against the foundation contracts; they hold. Two issues remain.

## REVISE

### Issue 1: V10's "increases by exactly n" asserts a count-correspondence the ASN simultaneously declares open and forbids

**ASN-0112, V10 / Open Questions / intro**: "inserting `n` content positions increases the extent by exactly `n`" — yet Open Question 2 asks "What invariant must relate the reported extent to the count of occupied positions, given that a span designates boundaries and explicitly not a cardinality?" and the intro quotes Nelson: the extent "does not designate a number of anything" (4/24).

**Problem**: These are in tension. In the dense single-subspace case the ASN's own machinery forces `extent_d = [0,…,0,n_s]`, whose last component equals `|O(d)| = n_s` exactly (from D-SEQ★'s dense run + D-MIN★ + uniform depth — the same facts V5 uses). So the extent-to-count correspondence is *partially established by V5/V10*, not open, in precisely the dense uniform-depth single-subspace regime. As written, V10 reads the extent change as a numeric count (the very thing V12 and the Nelson quote disavow), while Open Question 2 treats that relationship as unresolved. A reader cannot tell whether the ASN has answered its own open question or contradicted its own principle.

**Required**: Reconcile the three. State V10 in displacement terms (the body already does this correctly: "growing the reach by `n` ordinal steps," i.e. `extent_after = shift(extent_before, n)`), and add one sentence noting that the count-coincidence holds *because* the run is dense and depth-uniform (so the final component happens to equal `|O(d)|`), while the "not a cardinality" caveat governs the cross-subspace / cross-population case where positions between endpoints are not enumerable. Then narrow or remove Open Question 2 to the genuinely-unresolved part (e.g. the multi-subspace case), since the single-subspace case is settled.

### Issue 2: No weakest-precondition treatment of a non-trivial result property

**ASN-0112, "Preconditions and well-definedness"**: the section establishes totality under `d ∈ dom(M)` but performs no wp analysis.

**Problem**: For this pure query the load-bearing wp questions are exactly the state conditions under which the result attains a distinguished property — `wp(RETRIEVEDOCVSPAN(d), "result is an exact cover") = `O(d)` lies in a single subspace` (the V5/V6 dichotomy), and `wp(…, "reach(σ_d) = reach_d") = #origin_d ≤ #reach_d`. The ASN derives these facts inside V2/V5/V6 but never frames them as the precondition characterization a caller needs to know *before* querying whether the answer will be exact or a bounding box. The standards require a non-trivial wp, and one is readily available here.

**Required**: Add a short wp paragraph deriving the precondition for at least one non-trivial result property — the exact-cover condition (single-subspace occupancy) is the natural choice and connects V5, V6, and V7 into one statement.

## OUT_OF_SCOPE

### Topic 1: Per-subspace exact extents for multi-subspace documents
**Why out of scope**: V7 and the first open question correctly defer span-set decomposition to a per-subspace operation (RETRIEVEDOCVSPANSET / ASN-0113). This is new territory, not a defect here.

### Topic 2: Authorization / session read-entitlement gating
**Why out of scope**: The ASN rightly notes the BERT/session gate (consultation Q17) is a deployment-level access concern the abstract state `Σ = (C, L, E, M, R)` cannot express, and excludes it from value semantics. Correct call.

VERDICT: REVISE
