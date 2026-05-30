# Review of ASN-0084

## REVISE

### Issue 1: R-SP claims S7 is discharged by a list that omits it
**ASN-0084, R-SP proof**: "Every clause of Q except S8 — ... S5, S7 with its sub-clauses S7a, S7b, S7d, ... — is therefore discharged generically by the *Invariant preservation* paragraph above (C-transport for the Σ.C-only invariants and S7, ...)."
**Problem**: The "Invariant preservation / C-transport" paragraph it points to enumerates "S0 ..., S1 ..., S4 ..., S7a ..., S7b ..., and S7d ..." — **S7 itself (StructuralAttribution) is not in that list.** S7 is a theorem whose postconditions (`origin(a)`, including S7(c) distinctness and S7(d) cross-state invariance) need an actual discharge step, not a back-reference to a paragraph that never mentions it. The discharge is trivial (origin is a function of the address `a` and `dom(C)`, both unchanged), but as written R-SP cites coverage that does not exist.
**Required**: Add S7 explicitly to the C-transport enumeration in *Invariant preservation*, with the one-line derivation that `origin(a)` depends only on `a` and `dom(C) = dom(C')`, so S7(a)–(d) transport. Then R-SP's citation is honest.

### Issue 2: R-SP conjoins a redundant precondition and spends its proof on a non-Q construction
**ASN-0084, R-SP**: `wp(REARRANGE_K, Q) ⇐ R-PRE(K) ∧ ASN-0036-invariants(Σ, d) ∧ (B is a correspondence-run partition ...)`; and in the proof, "Existence and uniqueness of the maximal decomposition of M'(d) hold by foundation S8, whose preconditions are preserved ... To document the run-level effect, we additionally verify that B' = R-BLK(B) ... is *a* valid correspondence-run partition ... though B' is in general non-maximal."
**Problem**: Q's only non-generic clause is S8, and the proof itself concedes S8 follows from foundation S8 once S8-fin/S2/S3/S8a/S8-depth are preserved — none of which reference the pre-state partition `B`. The existence of `B` is *already implied* by the ASN-0036 invariant suite (foundation S8 guarantees a partition). So the third conjunct adds nothing to the sufficient condition, and the entire `B' = R-BLK(B)` verification (S8-uniq/S8-cons for B') discharges nothing in Q — it is explicitly "documentary," and B' is non-maximal whereas Q asks about the maximal decomposition. A sufficiency lemma should not carry a superfluous precondition plus a half-page proof of a property outside its postcondition.
**Required**: Drop the `B`-partition conjunct from the sufficient precondition (or justify why Q is not provable without it). Move the B' run-level characterization out of the wp-proof — it is a statement about R-BLK, belonging in R-BLK, not in the S8 discharge.

### Issue 3: "maximal refinement" inverts the partition order
**ASN-0084, Canonical decomposition**: "The Merge operation above relates a valid partition to its maximal refinement (each merge strictly reduces the run count, and V_S(d) is finite by S8-fin, so iterated merging terminates)."
**Problem**: Merging reduces run count — it *coarsens* the partition toward the maximal-run (coarsest) decomposition. "Refinement" denotes the finer direction. The maximal-run decomposition is the coarsest, not a refinement, of B'. The parenthetical even states the run count decreases, contradicting "refinement."
**Required**: Replace "maximal refinement" with "maximal-run (coarsest) decomposition" or equivalent.

### Issue 4: R-BLK "Interaction between successive cuts" is a defensive exhaustiveness essay
**ASN-0084, R-BLK Phase 1**: the paragraph beginning "Phase 1 processes cuts in index order against the *current* (already-refined) partition rather than against the original B, so we must verify that the interior/boundary/outside dispatch remains coherent ..." with "*Case A*", "*Case B*", and the closing "The case split (A vs. B) exhausts every Phase 1 outcome ...".
**Problem**: This is meta-prose justifying that the algorithm "remains coherent," carried by a Case A/B exhaustiveness argument whose payload — cuts are strictly increasing (CS2), so a later cut lands in the right piece of an earlier split — is one sentence. The surrounding scaffolding ("we must verify ... remains coherent," "the case split exhausts every outcome ... under partition disjointness ... Case A subsumes both ...") is the accretion the precise reader must skip past. This is exactly the defensive-justification pattern flagged for this note.
**Required**: Reduce to the load-bearing fact: by CS2, `ord(c_j) > ord(cᵢ)` for `j > i`, so `c_j` never lies in the left piece produced by splitting at `cᵢ`; therefore processing in index order against the refined partition agrees with processing against B. Delete the Case A/B framing and the "coherence"/"exhausts every outcome" prose.

### Issue 5: Multiple sections defer to the same downstream location (R-SP)
**ASN-0084**: Canonical decomposition — "for the post-state M'(d) specifically, that transport is discharged once in R-SP above"; R-BLK closing — "The S8-unique maximal partition of M'(d) exists by the foundation-S8 transport discharged in R-SP"; and R-SP itself carries the transport.
**Problem**: Three locations point at the R-SP foundation-S8 transport, a flagged accretion pattern ("multiple paragraphs in different sections defer to the same downstream location"). Combined with Issue 2 (the transport is a one-line consequence of foundation S8), the repeated cross-references inflate the apparent dependency structure.
**Required**: State the foundation-S8 transport once, at its natural home (the invariant audit), and let R-BLK/Canonical decomposition use it without re-announcing where it lives.

## OUT_OF_SCOPE

### Topic 1: Operational recovery of the maximal partition from B'
The note correctly defers the merge-driven reduction of B' to its canonical (maximal) form and records it as Open Question 6. The Merge lemma and the worked-example merge-checks are enough to motivate it; the confluence/process belongs in the future arrangement-operations ASN, not here.

### Topic 2: k-cut rearrangements for k > 4 and composition of rearrangements
Open Questions 1–2. Genuinely new territory (the permutation class and its closure under composition), not a defect in the 3/4-cut treatment.

VERDICT: REVISE
