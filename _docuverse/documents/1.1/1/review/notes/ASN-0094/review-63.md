# Review of ASN-0094

## REVISE

### Issue 1: Inaccurate claim about step 0 status of the Retraction row

**ASN-0094, Sh5 Template Catalog, "Status of the audit table" paragraph**: "the eleven currently-accepted rows below and the rejected `K_is_fresh` callout exhibit the checklist's outcome at the catalog's current state (all eleven rows clear step 0 by carrying shape tuples distinct from R's on at least one component; the `K_is_fresh` rejection fires at step 2 rather than step 0)"

**Problem**: The audit table's row 9 is Retraction with shape `(*, 1, A, A_rel, ⊤)` — which is exactly R's shape, not distinct from it. Step 0's acceptance criterion (i) (shape distinct on at least one component) does not apply to the Retraction row; it clears step 0 only by criterion (ii) (K_rep ~ R, alias of R). The blanket claim that "all eleven rows" clear step 0 by criterion (i) is incorrect for row 9.

**Required**: Revise the parenthetical to distinguish the two acceptance criteria, e.g., "ten of the eleven rows clear step 0 by criterion (i) (shape distinct from R's on at least one component); the Retraction row (row 9) clears step 0 by criterion (ii) (K_rep ~ R, the R-class registration itself). The `K_is_fresh` rejection fires at step 2 rather than step 0." Alternatively, the audit table row for Retraction could note its special status under step 0.

## OUT_OF_SCOPE

No items. The Open Questions section already documents design choices, refinement candidates, and scope boundaries explicitly with appropriate tagging.

VERDICT: REVISE
