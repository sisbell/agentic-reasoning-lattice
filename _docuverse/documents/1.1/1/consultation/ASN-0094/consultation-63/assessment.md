# Channel Assignment — ASN-0094 review-63

**Date:** 2026-05-24 10:11

## Issue 1: Inaccurate claim about step 0 status of the Retraction row
Reason: The fix is derivable from the ASN's own content. The Retraction row's shape `(*, 1, A, A_rel, ⊤)` and R's shape are both defined within ASN-0094, as are step 0's two acceptance criteria (i) and (ii). The correction is a simple self-consistency fix: distinguish that ten rows clear by criterion (i) while the Retraction row (being R itself) clears by criterion (ii).
