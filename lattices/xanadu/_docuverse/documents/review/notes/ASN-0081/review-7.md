# Review of ASN-0081

## REVISE

### Issue 1: D-SEP(b) proof conflates two cases under a single D-CTG application
**ASN-0081, D-SEP proof of (b)**: "The last element of X (with ordinal ord(p) + c − 1) is in V_S(d), and v ∈ V_S(d) with v ≥ r > last element of X. By D-CTG, every same-subspace, same-depth position between them — including r — is in V_S(d)."
**Problem**: When v = r, the position r is not strictly between the last element of X and v — it *is* v. D-CTG quantifies over positions strictly between two members of V_S(d) and says nothing about the endpoints themselves. The "including r" phrasing is incorrect for this case. The conclusion r ∈ V_S(d) is correct (trivially, since v = r ∈ V_S(d)), but the D-CTG citation doesn't establish it. When v > r, D-CTG does apply and r is properly between u and v. The proof must distinguish the two cases.
**Required**: Replace the single-argument paragraph with: "Either v = r, so r ∈ V_S(d) directly, or v > r, in which case the last element of X and v bracket r in V_S(d), and D-CTG gives r ∈ V_S(d). In both cases r ∈ R and r = min(R)."

### Issue 2: Foundation Citations section incomplete
**ASN-0081, Foundation Citations**: "The following ASN-0036 properties are cited throughout."
**Problem**: The section lists only S8-depth, S8a, and D-CTG. The proofs also cite D-SEQ (Contraction Setup, D-CTG-post), D-MIN (D-MIN-post), S2 (S2-post), S3 (S3-post), S8-fin (S8-fin-post), and S0 (D-I). A reader using the Foundation Citations section to understand the ASN's dependency footprint will miss six of the nine ASN-0036 properties actually used.
**Required**: Either list all cited ASN-0036 properties or retitle the section to indicate it covers only the most frequently cited ones (e.g., "Frequently Cited ASN-0036 Properties") and note that others are cited inline.

### Issue 3: D-CS registry entry drops quantifier domain
**ASN-0081, Statement registry, D-CS row**: "(A v : subspace(v) ≠ S : M'(d)(v) = M(d)(v))"
**Problem**: The body text correctly restricts the second conjunct to `v ∈ dom(M(d))`: "(A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ S : M'(d)(v) = M(d)(v))". The registry version quantifies over all v with subspace ≠ S, including v ∉ dom(M(d)) for which M(d)(v) is undefined.
**Required**: Registry entry should match the body: "(A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ S : M'(d)(v) = M(d)(v))".

### Issue 4: OrdinalDisplacementProjection lacks w_ord > 0 postcondition
**ASN-0081, OrdinalDisplacementProjection**: defines w_ord = [w₂, ..., wₘ] with no postcondition on positivity.
**Problem**: D-SEP(a) cites TA4 (PartialInverse), which requires w > 0. The proof applies TA4 with w = w_ord but does not verify w_ord > 0. The depth-2 specialization mentions "positive integer c" in passing, but this is not a formal postcondition of the definition. The result is independently proven by direct computation, so D-SEP(a) is correct — but the TA4 citation is incomplete without verifying all its preconditions.
**Required**: Add postcondition to OrdinalDisplacementProjection: "When w > 0 and w₁ = 0, w_ord > 0" (at depth 2: w = [0, c] with c > 0 implies w_ord = [c] > 0). Then verify this in the D-SEP(a) TA4 citation.

## OUT_OF_SCOPE

### Topic 1: Generalization beyond depth-2 V-positions
**Why out of scope**: The ASN explicitly scopes to #p = 2 via a scoping axiom and lists generalization as an open question. The depth-2 case is the minimal non-trivial case (depth 1 causes subspace escape, as noted in ValidInsertionPosition). Deeper ordinals introduce multi-component subtraction where TA4's zero-prefix condition is no longer vacuous and TA3-strict's equal-length precondition must be established per case. This is genuinely new territory requiring its own analysis.

VERDICT: REVISE
