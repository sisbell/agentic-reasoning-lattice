# Review of ASN-0075

The proofs (D-WIT, D-EXH, D-DISCR, D-DISJ) are rigorous: the four-row exhaustion table is total, the two-history discrimination construction agrees on `(C,L,E,M)` and differs only on `R`, and the worked example checks out against every claim. The remaining issues are anti-bloat / precision, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Editorial framing prose in D-RECONS justification
**ASN-0075, "State-Functional Independence" (D-RECONS justification)**: "This is what makes the operation an honest function of state. The user need not know how the system arrived at its current configuration; consulting the current configuration suffices."
**Problem**: These two sentences are editorializing that does not advance the argument. The substantive content of the paragraph is the next clause — P4a guarantees that a `DELETED` report corresponds to a real past containment, while the route is irrelevant. The "honest function of state" / "the user need not know" framing is essay prose in a justification slot.
**Required**: Delete the two framing sentences; keep the P4a-grounded clause, which carries the actual reasoning.

### Issue 2: Foundation Recap states R's historical characterization as definition, duplicating P4a/P4★
**ASN-0075, "Foundation Recap"**: the provenance bullet reads "`Σ.R ⊆ T_elem × E_doc` (ASN-0047) … `(a, d) ∈ R` iff document `d` has, at some point in the system's history, contained I-address `a` in its content-subspace arrangement."
**Problem**: R's foundation definition is the structural one (`R ⊆ T_elem × E_doc`). The appended "iff … contained … at some point in history" is not R's definition — it is exactly the conjunction of the separately-listed P4a (the `R ⟹` past-containment direction) and P4★ (the containment `⟹ R` converse), both recapped one and two bullets later. Presenting the iff inline as part of R's meaning both duplicates those bullets and overstates a structural subset as a biconditional theorem.
**Required**: State the R bullet as the structural definition only (subset of `T_elem × E_doc`), and let P4a/P4★ supply the historical directions, or drop the redundant P4a bullet if the iff gloss is retained.

## OUT_OF_SCOPE

### Topic 1: Per-occurrence (V-position-level) deletion detection
**Why out of scope**: The note correctly scopes this out — its predicates are at I-address-set granularity, and per-occurrence removal among transcluded copies is a Vstream concern. This is future-ASN territory, not a defect here.

### Topic 2: Multi-document (>2) deletion families, span-based output presentation, restoration operation
**Why out of scope**: Raised appropriately in Open Questions; these are new operations/structure, not gaps in the binary SHOWDELETIONS specification.

VERDICT: REVISE
