# Review of ASN-0029

## REVISE

### Issue 1: D13 Case 2 — structural parent undetermined
**ASN-0029, D13 (VersionPlacement)**: "account(d_s) ≠ a_req ⟹ account(d_v) = a_req"
**Problem**: Case 1 explicitly states `parent(d_v) = d_s`. Case 2 states only `account(d_v) = a_req`, leaving `parent(d_v)` unstated. The worked example and D14's operational argument establish that Case 2 produces a root document (undefined parent), but D13 itself should state this symmetrically — a reader consulting D13 alone cannot determine the structural relationship for cross-account versions.
**Required**: Add `∧ parent(d_v) undefined` to Case 2, or append: "Cross-account versions are root documents under `a_req`; `parent(d_v)` is undefined."

### Issue 2: Missing Σ.D well-formedness invariant
**ASN-0029, D14 (VersionForest)**: "The restriction to Σ.D is essential: without it, degenerate tumblers such as N.0.U.0 (which has zeros = 2 but an empty document field) would qualify as ancestors..."
**Problem**: The forest structure depends on Σ.D containing no degenerate document-level tumblers (empty document field, such as `N.0.U.0`). The ASN argues correctness by restricting `parent` to Σ.D and noting no operation creates degenerate documents — but never states this as an invariant. The argument is sound for D0 and D12, but any future document-creating operation could silently break the forest by introducing a degenerate tumbler if the invariant isn't explicit.
**Required**: State an invariant: `(A d ∈ Σ.D : the document field of d, as extracted by fields(d), has at least one component, and all document-field components are strictly positive)`. Verify against D0 and D12. This makes the forest's structural dependency explicit and protectable.

### Issue 3: D16 implication unsatisfiable for inaccessible documents
**ASN-0029, D16 (NonOwnerForking)**: "account(d) ≠ actor(op) ∧ op requests modification of d ⟹ system applies CREATENEWVERSION(d, actor(op))"
**Problem**: When `d` is private and `account(d) ≠ actor(op)`, D16's antecedent is satisfied but D12's precondition (`Σ.pub(d_s) ∈ {published, privashed} ∨ account(d_s) = a_req`) fails. The implication is false in this case — the system cannot apply CREATENEWVERSION as D16 promises.
**Required**: Add D12's accessibility condition to D16's antecedent: "account(d) ≠ actor(op) ∧ op requests modification of d ∧ (Σ.pub(d) ∈ {published, privashed}) ⟹ ..."

## OUT_OF_SCOPE

### Topic 1: Associate access model for private documents
**Why out of scope**: D5(c) references "designated associates" and D12's precondition is conservative (owner-only for private docs). The designation mechanism is a separate access-control formalization, correctly deferred.

### Topic 2: DELETE, COPY, REARRANGE target-document postconditions
**Why out of scope**: D2's verification for these operations' write targets depends on their yet-to-be-formalized postconditions (ASN-0026 gap). The ASN correctly identifies this as a proof obligation on those future specifications.

### Topic 3: Concurrent access under D15
**Why out of scope**: The properties concurrent sessions must satisfy to uphold D15 require their own formalization — locks, tokens, serialization — which is independent of document lifecycle.

### Topic 4: Withdrawal and privashed-to-private transition
**Why out of scope**: Nelson's design intent for privashed withdrawal requires a WITHDRAW operation with its own preconditions and invariant analysis. The current model correctly treats both published and privashed as stable under all defined operations.

VERDICT: CONVERGED
