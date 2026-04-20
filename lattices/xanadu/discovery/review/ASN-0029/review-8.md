# Review of ASN-0029

## REVISE

### Issue 1: D12(g₂) cross-account monotonicity stated without proof
**ASN-0029, D12 postcondition (g₂)**: "(A d' : d' ∈ Σ.D ∧ account(d') = a_req : d' < d_v)"
**Problem**: This postcondition claims the new version exceeds ALL documents under a_req's account, including children of earlier root documents. D1 establishes only per-allocator monotonicity and explicitly warns that different allocators are NOT jointly monotonic. The argument that root allocator outputs exceed all descendants of earlier roots — divergence at the first document component via T1(i) — is given in D0's discussion but neither reproduced nor referenced in D12. The worked example's Case 2 says "Postconditions (a)–(f) hold identically" and skips g₂ entirely.
**Required**: D12 should reference D0's argument explicitly: D12 Case 2 uses the root allocator for a_req (D1); the new root d_v has a first document component exceeding all existing first document components under a_req; any document d' under a_req with first document component K' < K satisfies d' < d_v by T1(i) at the first document component, regardless of d's depth in the version tree. Alternatively, factor the argument into a lemma that both D0 and D12(g₂) cite.

### Issue 2: No worked example for D0
**ASN-0029, D0 (EmptyCreation)**: D0 is the foundational document-creation operation. The ASN has an excellent worked example for D12 but none for D0.
**Problem**: D0's monotonicity clause — `(A d' : d' ∈ Σ.D ∧ account(d') = a : d' < d)` — is the non-trivial postcondition. The claim that a new root exceeds all existing documents under the account, including children of earlier roots, deserves concrete verification. A scenario with at least one existing root and one child document would exercise the argument beyond the vacuous case.
**Required**: A worked example for D0 demonstrating the monotonicity postcondition with existing child documents under the account. For instance: account `1.0.1` has root `1.0.1.0.3` and child `1.0.1.0.3.1`; D0 produces `1.0.1.0.5`; verify `1.0.1.0.3 < 1.0.1.0.5` and `1.0.1.0.3.1 < 1.0.1.0.5` by citing the T1 divergence at the first document component.

### Issue 3: Preservation section omits this ASN's own invariant D7b
**ASN-0029, Preservation of ASN-0026 Invariants**: "The four operations introduced in this ASN — D0, D10a, D12, D17 — must preserve P0, P1, P2, P3, and P7."
**Problem**: The section verifies ASN-0026 invariants but does not verify D7b (HomeDocumentMembership), which is this ASN's own invariant. D7b is derivable from P2 + D7a + D2 (all of which are verified), but the derivation is not stated. A reader checking "does D12 preserve D7b?" must reconstruct the argument: Σ'.V(d_v)(p) = Σ.V(d_s)(p) by (c); home of that address is in Σ.D by D7b on the pre-state; by D2 that home document persists in Σ'.D.
**Required**: Add D7b to the preservation section with the one-line derivation: for D0, vacuous (empty document); for D12, Σ'.V(d_v)(p) = Σ.V(d_s)(p) and home of that address is in Σ.D ⊆ Σ'.D; for D10a and D17, V-space unchanged and Σ.D ⊆ Σ'.D.

### Issue 4: D10 verification enumeration omits D17
**ASN-0029, D10-ext paragraph**: "With D10-ext, D10 holds universally: D0 sets... D10a transitions... D12 sets... ASN-0026 operations preserve Σ.pub by D10-ext."
**Problem**: The explicit enumeration of operations preserving D10 lists D0, D10a, D12, and ASN-0026 operations but omits D17. The later preservation section notes "D17 is a pure query with Σ' = Σ, so all invariants are preserved vacuously," but the D10-specific argument should be self-contained.
**Required**: Add D17 to the D10-ext paragraph's enumeration: "D17 is a pure query (Σ' = Σ), so D10 is trivially preserved."

## OUT_OF_SCOPE

### Topic 1: Full D2 verification for DELETE, COPY, and REARRANGE targets
**Why out of scope**: The ASN transparently flags the proof obligation — these operations' postconditions are not yet formalized in ASN-0026 (+_ext classification only). Verification of D2 for these targets depends on their future formalization establishing that Σ'.V(d) remains a defined total function.

### Topic 2: Associate access model for private documents
**Why out of scope**: D5(c) references "designated associates" with visibility access to private documents. The mechanism for designation is a separate access-control concern, not an error in this ASN's formalization of ownership and publication.

### Topic 3: Withdrawal and privashed transition mechanics
**Why out of scope**: The ASN correctly identifies that `privashed` is currently permanent (no operation transitions out of it) and that Nelson's intent requires a future WITHDRAW or UNPRIVASH operation. This is new operational territory.

### Topic 4: Concurrent access properties
**Why out of scope**: The ASN models state transitions atomically. The abstract properties governing concurrent access — ensuring D15 holds under simultaneous sessions — belong to a concurrency-focused ASN, as the open questions acknowledge.

VERDICT: REVISE
