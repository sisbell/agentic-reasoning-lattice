# Review of ASN-0071

## REVISE

### Issue 1: Same deferrals stated twice — "What we do not specify" duplicates Open Questions
**ASN-0071, "What we do not specify" (ii)/(iii) vs "Open Questions" Q3/Q4/Q5**: (ii) "replica-divergent views in a distributed deployment are out of scope" / (iii) "layering Nelson's visibility policy ... is out of scope" — versus Open Questions "What completeness must FINDDOCSCONTAINING guarantee when ... distributed across replicas ...?" / "What abstract operation must filter FINDDOCSCONTAINING's result by requester visibility?" / "What completeness must visibility-filtering preserve ...?"
**Problem**: Replica freshness and access-control filtering are each deferred in two different sections — once as "out of scope" non-promises, once as future-ASN questions. This is the multiple-paragraphs-defer-to-the-same-downstream pattern; a reader meets the same deferral twice. The two framings ("implementation may add" vs "future ASN must answer") carry no distinct content.
**Required**: Keep the deferral in one place. Either drop (ii)/(iii) from "What we do not specify" and let the Open Questions carry the forward pointer, or drop the corresponding Open Questions and keep only the scope statement.

### Issue 2: The σ′ paragraph analyzes a case the precondition already excludes
**ASN-0071, "Interior action point, rejected against an arrangement"**: "The coarse span `σ' = ([s_C, 1, 2], [0, 1, 0])` has action point 2, *interior* to `#u = 3`; ... The `actionPoint(ℓ) = #u` precondition rejects `σ'` outright (`2 ≠ 3`)."
**Problem**: `σ'` fails the vspec precondition, so `find` never processes it. Computing its hypothetical `⟦σ'⟧ ∩ dom(M(d_E))` and contrasting it with `σ''` does not establish any property of the operation — it argues *why the precondition is there*. "The contrast with `σ_E` is the discrimination the precondition is for" is precondition-rationale prose. The permitted depth-wise case (`σ_E`) is a genuine behavior worth exhibiting; the excluded breadth-wise case is justification of the precondition's existence, which the precondition's statement already settles.
**Required**: Drop the `σ'` analysis. The `actionPoint(ℓ) = #u` precondition stands on its own statement; `σ_E` already demonstrates the operation on a valid deep source.

## OUT_OF_SCOPE

### Topic 1: Relationship between current-containment result and the permanent provenance relation R
**Why out of scope**: Correctly identified by the ASN itself (Currency section + Open Questions). The current-vs-historical containment guarantee is genuinely new territory, not a defect in this query specification.

META:

VERDICT: REVISE
