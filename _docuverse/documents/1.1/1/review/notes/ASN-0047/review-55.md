# Review of ASN-0047

## REVISE

### Issue 1: K.δ k=1 ghost-base versioning lacks a concrete worked example
**ASN-0047, K.δ Section, Sub-case "Sibling-at-deeper-tumbler-depth (k = 1) — restricted to documents"** and the subsequent multi-paragraph treatment "Scope and base-liveness".
**Problem**: The ghost-base versioning case is load-bearing — it admits an inc operand `t` outside E_doc, with intricate downstream consequences for P8, T10a's at-most-once, and version-chain liveness. The ASN devotes substantial prose to it but never demonstrates it operationally. The worked examples exercise K.α/K.μ⁺/K.ρ, K.δ (document creation only), K.μ⁻, K.μ~, K.λ, K.μ⁺_L — but never K.δ with `t ∉ E_doc`. A reader must mentally construct the scenario to verify the analysis (allocate v=1 from ghost base; check P8 holds because parent(v=1) is the account, not the ghost; chain v=2 via inc(v=1, 0); verify T10a.6 blocks a second inc(ghost, 1)).
**Required**: Add a worked example exercising ghost-base versioning at K.δ level. At minimum: (i) K.δ creating `e = [N, 0, U, 0, D, 1]` from ghost `t = [N, 0, U, 0, D]`; (ii) verification that P8 holds (`parent(e)` resolves to the account, which IS in E); (iii) subsequent K.δ via k=0 from `e` to allocate `[N, 0, U, 0, D, 2]`; (iv) demonstration that a second `inc(ghost, 1)` attempt is blocked (by `e ∉ E` precondition combined with T10a's at-most-once on `(ghost, 1)`).

### Issue 2: K.μ⁻ admissibility is implicit in postconditions rather than stated as explicit precondition
**ASN-0047, K.μ⁻ Section**: "The admissibility of any particular contraction (which subset of dom(M(d)) may be removed) is *not* stated as a precondition. It is recovered from the post-state requirement that M'(d) satisfy D-CTG★ and D-MIN★..."
**Problem**: This structure forces every reader to derive the admissibility envelope from the case analysis below the precondition. The case analysis already proves the form is exactly per-subspace suffix removal or full clearance. Stating this as an explicit precondition would make K.μ⁻'s contract self-contained, match the pattern used by every other transition in the ASN (K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L all state explicit preconditions), and remove the awkward "the postconditions implicitly constrain the precondition" phrasing.
**Required**: Promote the admissible-pattern characterization into an explicit precondition: "for each subspace S, the removed positions in V_S(d) form either a suffix `{[S, 1, ..., 1, k] : n'_S < k ≤ n_S}` for some `1 ≤ n'_S < n_S` (partial suffix removal) or all of V_S(d) (full clearance with n'_S = 0)". The case analysis below then becomes a *verification* that this precondition matches the D-CTG★/D-MIN★ postconditions, rather than the sole source of admissibility.

### Issue 3: Decomposition section forward-references "link-subspace fixity" in Case 2 before deriving it
**ASN-0047, Decomposition of K.μ~ Section, Case 2**: "The link-subspace identity property (derived from S3★ + K.μ⁺ amendment + CL-UNIQ, *Generalized referential integrity* above) gives `(A v ∈ dom(M(d)) : subspace(v) = s_L : π(v) = v)`."
**Problem**: Case 2 invokes "link-subspace fixity" to conclude `π = id` when `dom_C(M(d)) = ∅`. The derivation of link-subspace fixity appears *later* in the same section under "Link-subspace fixity under K.μ~". The cross-reference "(derived from S3★ + K.μ⁺ amendment + CL-UNIQ)" is correct but the proof itself is forward, making Case 2 lean on a result that is shown only after the case analysis it grounds. The ordering creates the appearance of circularity even though the underlying logic is sound (link-subspace fixity is established independently of the decomposition cases via CL-UNIQ's separate induction).
**Required**: Reorder the section so "Link-subspace fixity under K.μ~" precedes "Decomposition of K.μ~ into K.μ⁻ + K.μ⁺", or inline the brief argument needed for Case 2 directly into Case 2's discussion.

### Issue 4: "Every invariant exercised" claim for the worked example overstates coverage
**ASN-0047, end of Worked example: link allocation and arrangement**: "Steps 1–5 of this example exercise — explicitly or via the frame-preserved annotations — every invariant in the conjunction of ExtendedReachableStateInvariants (per-state) and ExtendedTransitionInvariants (per-transition)..."
**Problem**: S4 (OriginBasedIdentity), S7a, S7d, S9 (TwoStreamSeparation) are never named in the per-step verifications, neither explicitly nor as "frame-preserved". S8 (SpanDecomposition) in the extended state is derived from prerequisites but is not itself verified at any worked endpoint. The claim that the example exercises *every* invariant is technically inaccurate for at least these four.
**Required**: Either (a) extend the worked example's per-step verification list to name S4, S7a, S7d, S8, S9 explicitly (the omitted invariants are all framed by the chosen step sequence, so the additions are short); or (b) soften the claim to "exercises most invariants" with explicit enumeration of those left implicit.

### Issue 5: Structural sufficiency claim is bounded but the bounds are not summarized
**ASN-0047, end of Elementary transitions and end of Scoped coupling constraints**: The ASN makes a "structural sufficiency" claim twice — first for the five primitive transitions (four-component state), then for the seven (extended state). Each instance includes a caveat that completeness in the stronger sense (every admissible state difference realisable) is not claimed, plus an explicit "Known gap" identifying tombstone-style link withdrawal as outside the elementary set.
**Problem**: Two structural-sufficiency claims with two caveats and one named gap, scattered across two locations in the ASN, leave the reader without a single statement of what the elementary set covers and what it does not. The K.μ⁻ worked counterfactual in Step 5 of the link example is the only place tombstoning is concretely shown to fail — but a reader scanning the elementary-transition catalogue might miss this entirely.
**Required**: Consolidate the bounded-sufficiency statement and named gaps into a single subsection. State concretely what *is* covered (creation, allocation, content/link arrangement extension and contraction, reordering, provenance recording, fork) and what *is not* (tombstone-style withdrawal; account-level k=1; account/document arrangement under non-T10a allocators). Cross-reference the open questions section.

## OUT_OF_SCOPE

### Topic 1: Tombstone-style link withdrawal mechanism
**Why out of scope**: The ASN explicitly identifies this as a structural gap and defers it to an open question. The transition model intentionally restricts K.μ⁻ to suffix-only contractions; tombstone semantics require a separate operator outside the present elementary set. Resolving it requires extending the state model (status flag, tombstone marker, or retraction-link convention), which is downstream of the present ASN.

### Topic 2: Version-management contract beyond entity membership
**Why out of scope**: The ASN admits K.δ k=1 ghost-base versioning at the bare entity level (a structural property of the address) but defers the richer semantics — arrangement-transition invariants between versions, base/version allocator coupling, provenance flow across versions, lineage acyclicity — to a subsequent version-management ASN. The k=1 case here only fixes the address-allocation structure.

### Topic 3: Account-level depth-1 tumbler extension
**Why out of scope**: Explicitly raised in the open questions section. The current ASN restricts K.δ's k=1 sub-case to `IsDocument(t)`, deferring the account-level analog (e.g., for account renaming) to potential future extension. Admitting `IsAccount(t)` would be a precondition relaxation that requires its own semantic justification.

### Topic 4: Concurrent allocation under shared documents
**Why out of scope**: Raised in the open questions section. The ASN's transition model is sequential; concurrency semantics (serialization, conflict resolution under parallel K.λ or K.α calls targeting the same sub-allocator frontier) is outside the present scope.

### Topic 5: Operations and protocol-level realisations
**Why out of scope**: The ASN explicitly scopes out named operations (INSERT, DELETE, COPY, REARRANGE, MAKELINK, CREATENEWVERSION, DELETEVSPAN), atomicity, authority/BERT model, and protocol commands (FEBE, BEBE). The elementary transitions defined here are the *primitives* over which such operations would compose; the operations themselves belong to subsequent ASNs.

VERDICT: REVISE
