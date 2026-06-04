# Review of ASN-0091

## REVISE

### Issue 1: "RE-subpres as a downstream consequence" is defensive meta-prose, duplicated in the RA-adm table cell
**ASN-0091, "REARRANGE_K Realises the Abstract Class"**: The paragraph beginning "*RE-subpres as a downstream consequence.* RE-subpres is not a layer that establishes RA-adm — it is a consequence of it..."
**Problem**: This paragraph advances no reasoning. It exists to clarify *what RE-subpres is not* (not one of the two RA-adm layers) and to reassure against a circularity that the document never actually risks — the abstract RE-subpres derivation is explicitly conditional on RA-adm as a class-definitional clause, so no circularity exists to head off. The recent revise commit ("correct RA-adm layer count and RE-subpres causal order") confirms this slot has been churning across cycles. The same statement is then duplicated verbatim in the RA-adm row of the clause-correspondence table ("RE-subpres is a downstream consequence of RA-adm, not a layer that establishes it"), and a third time the content recurs where K.μ~ clause (iv) is discharged ("clause (iv)... is exactly `subspace(π(v)) = subspace(v)`"). Three locations establish/relitigate the same fact.
**Required**: Delete the "RE-subpres as a downstream consequence" paragraph. RE-subpres is derived once in "REARRANGE as Vstream-Only Operation" and its REARRANGE_K constructive availability is already recorded by clause (iv) of the admissibility table; the causal-ordering reassurance is not load-bearing. Drop the redundant "not a layer" clause from the table cell, leaving only the two-layer discharge.

### Issue 2: Net-effect case split is deferred to from three sites
**ASN-0091, K.μ~ admissibility table clause (ii); "Run Decomposition Is Not Invariant" (RE-eq); opening section**: clause (ii)'s cell re-explains the S5 witness ("the net-effect case split established in 'REARRANGE as Vstream-Only Operation'... K.μ~ is the realiser exactly in the non-trivial case").
**Problem**: The full S5 witness (π ≠ id while M'(d) = M(d)) is constructed once in the opening section; clause (ii) and the RE-eq discussion each re-narrate the case split rather than citing it once. This is the "multiple paragraphs defer to the same location" pattern.
**Required**: Reduce clause (ii)'s cell to a bare citation of the opening-section witness without re-stating the come-apart phenomenon.

## OUT_OF_SCOPE

No out-of-scope claims are present — the ASN defines no INSERT/DELETE/COPY/version/replication mechanics, and the Open Questions are correctly deferred (cross-document span reconstitution, link-subspace rearrangement semantics, observational equivalence, run-cardinality bounds, cut-sequence completeness).

VERDICT: REVISE
