# Channel Assignment — ASN-0075 review-4

**Date:** 2026-05-25 14:15

## Issue 1: K.δ notation ambiguity in histories and worked example
Reason: The fix is derivable from ASN-0047's K.δ definition (case (ii) k=2 preconditions) and the ASN's own notational convention for composites. Either the convention can be extended to declare "K.δ(d)" as shorthand for the necessary precursor-bundled composite, or the histories can be expanded to show account creation explicitly — both choices follow from the cited foundation.

## Issue 2: D-EXH proof relies on P4★ without explicit reachability assumption
Reason: P4★ is defined in ASN-0047 as a Class (b) composite-boundary property, and the ASN's worked example already operates at composite boundaries. The fix — adding "reachable" / "at composite boundary" to D-EXH's precondition or noting SHOWDELETIONS is meaningful only at reachable states — is fully derivable from ASN-0047's classification of P4★.

## Issue 3: Q0 vacuity explanation is logically incomplete
Reason: The review supplies the corrected chain (CURRENT → P4★ → contradiction with disjointness) and the elements are already in scope within ASN-0075 (P4★ is in Foundation Recap). The fix is prose tightening that requires no external evidence.

## Issue 4: D-DISCR conclusion understates the witness's strength
Reason: The witnesses Σ_1 and Σ_2 explicitly agree on dom(C), C(a), E_doc, M(d), M(d') (per the table in the lemma itself), and L = ∅ for both is established by the history (no K.λ steps invoked). The strengthening to (C, L, E, M)-insufficiency is internal arithmetic on the witnesses already exhibited.
