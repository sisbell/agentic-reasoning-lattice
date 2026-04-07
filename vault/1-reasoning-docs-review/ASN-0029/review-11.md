# Review of ASN-0029

## REVISE

### Issue 1: D0/D14a verification missing base case for first document under an account

**ASN-0029, D0 discussion**: "The `parent(d) undefined` constraint makes explicit that D0 uses the account's root allocator (T10a sibling stream via `inc(·, 0)`)."

**ASN-0029, D14a verification**: "D0 allocates via `inc(·, 0)` on the account's root allocator stream, where the current maximum is a root document with single-component positive document field; `inc(·, 0)` increments that component, producing a positive single-component document field (`#D = 1`, `D₁ > 0`)."

**Problem**: The claim that D0 always uses `inc(·, 0)` is false for the first document created under an account. By T10a, the document-level allocator does not yet exist — the account-level allocator must spawn it via `inc(a, 2)` (child creation with `k' = 2`), producing the first document `N.0.U.0.1`. Only subsequent documents use `inc(·, 0)` on the sibling stream. The D14a verification assumes "the current maximum is a root document" — but for the first invocation, no root document exists yet.

The formal postconditions of D0 are correct regardless: `inc(a, 2)` by TA5(d) with `k = 2` produces `[N, 0, U, 0, 1]` with `#D = 1`, `D₁ = 1 > 0`, satisfying D14a. The monotonicity postcondition is vacuously satisfied when no existing documents are under the account. But the verification argument has a gap (missing base case), and the mechanism narrative is false for the first invocation.

**Required**: Add the base case to D14a's verification of D0: "When no root documents exist under the account, the document-level allocator is spawned by `inc(a, 2)` (T10a child creation), producing the first document with `D₁ = 1 > 0` and `#D = 1`." Adjust D0's mechanism narrative accordingly — either distinguish first invocation from subsequent, or describe the allocator model abstractly without committing to `inc(·, 0)` for all cases.

## OUT_OF_SCOPE

### Topic 1: Account creation and lifecycle
**Why out of scope**: D0 requires `a ∈ AccountAddr` as a precondition, and the allocator model assumes account-level allocators exist. How accounts enter the system — what operation creates them, what invariants govern the account set — is a separate specification concern, not an error in the document lifecycle ASN.

### Topic 2: Full D-series verification for DELETE, COPY, REARRANGE
**Why out of scope**: D2's verification honestly notes that DELETE, COPY, and REARRANGE lack formal postconditions in ASN-0026 (only INSERT is fully specified). Complete verification of D2, D7b, D10-ext, etc. for those operations depends on the ASN that formalizes them. This is a dependency between ASNs, not a gap in ASN-0029.

VERDICT: CONVERGED
