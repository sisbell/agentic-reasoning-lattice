# Review of ASN-0047

After thorough analysis, this ASN is rigorous and well-constructed. The verification matrix is exhaustive, edge cases are handled, the K.μ~ link-subspace fixity proof's dependency chain (S3★(Σ') → subspace preservation → Steps 1-3 functional identity → Step 4 pointwise identity) is non-circular, the K.μ⁻ admissibility shape derivation establishes a genuine equivalence rather than circular dependence on D-SEQ★, and the K.δ case (ii) sub-case discharge structure handles all sub-cases (k ∈ {0, 1, 2}; sub-cases A1/A2/B/C of k = 2). The Cross-document disjointness chain lemma is sound; FrontierEquivalence's three-premise derivation correctly identifies the load-bearing chain (T10a.7 + P1 + precondition for k = 0). The four worked examples cover representative scenarios including interior content replacement (the non-trivial case where K.μ⁻ must remove an entire suffix to preserve D-CTG★ at intermediate states).

## REVISE

### Issue 1: A_doc(·) and A_account(·) notation introduced ad-hoc
**ASN-0047, "Allocator hierarchy under documents" / "Sub-allocator names" section**: The catalogue lists only `A_C(d)`, `A_L(d)`, `A_v(d)` as "three T10a sub-allocators... associated with d". However, `A_doc(parent(d))` is invoked in the same section's case (a') discussion of `A_v(d)`'s parent allocator, and `A_account(·)` appears extensively in the K.δ case (ii) k = 2 sub-case A discharge — neither is defined in the catalogue. The text later acknowledges this ("the Sub-allocator names section listed only the three sub-allocators rooted at a document...but A_doc(·) and A_account(·) are first-class members of the same naming family").
**Problem**: The notation is referenced before formal definition. The acknowledgment is parenthetical rather than a definition.
**Required**: Add A_doc(A) and A_account(N) to the Sub-allocator names catalogue with their structural roles (emits documents under A; emits accounts under N) and their first-emission addresses ([A.0.1] and [N.0.1] respectively).

### Issue 2: K.δ structural identities embedded in prose rather than as cited postconditions
**ASN-0047, K.δ definition in *Elementary transitions***: The structural identities (`zeros(e) = zeros(t)` for k ∈ {0, 1}; `zeros(e) = zeros(t) + 1` for k = 2; `parent(e) = parent(t)` for k ∈ {0, 1}; `parent(e) = t` for k = 2) are catalogued as embedded prose under "Structural identities (consequences of TA5 + T4b's parent projection)" and explicitly noted as "not repeated as per-sub-case preconditions".
**Problem**: These identities are load-bearing throughout — cited in worked examples, A_v(d) parent-allocator dispatch, sub-case A1/A2 recursion, P8 preservation. Discharging the citations requires unpacking the prose catalogue each time.
**Required**: Promote each structural identity to a named lemma or numbered postcondition of K.δ for direct citation, or include them in the Properties Introduced table with explicit names.

### Issue 3: K.μ⁻ definition's strict-contraction effect clause references implicit subset relation
**ASN-0047, K.μ⁻ definition**: The effect clause states "dom(M'(d)) ⊂ dom(M(d)) ∧ (A v ∈ dom(M'(d)) : M'(d)(v) = M(d)(v))". The `⊂` symbol is used to mean proper subset, but the ASN does not define its convention (some texts use `⊂` for subset, ⊊ for proper subset).
**Problem**: Reader must infer the strict subset reading from context (the per-subspace consequence paragraph confirms strict contraction).
**Required**: Either state the convention explicitly ("⊂ denotes proper subset") or use ⊊ unambiguously.

### Issue 4: "By similarly" in K.μ~ subspace preservation derivation
**ASN-0047, K.μ~ definition section, *Decomposition of K.μ~* paragraph**: The subspace preservation derivation shows the content-subspace contradiction case in full, then asserts: "The link-subspace case is symmetric, with the roles of dom(C) and dom(L) interchanged."
**Problem**: The symmetry is mechanical, but the text is making a "by similarly" argument. A strict reviewer would want both cases written.
**Required**: Either write the link-subspace case in full (3-4 lines: "Suppose π maps a link-subspace v to s_C. By S3★(Σ) at v, M(d)(v) ∈ dom(L)..."), or explicitly note that the L14 ∩ symmetry forces the second case mechanically.

### Issue 5: Forward references in derivation chains lack explicit cycle-breaking justification
**ASN-0047, *Decomposition of K.μ~* section, "Dependency chain at a glance"**: The chain reads "S3★(Σ') established via K.μ⁻ + K.μ⁺ decomposition (independent route) → subspace preservation derived → link-subspace fixity Steps 1-3 → Step 4 → admissibility clause (ii) → existence condition". The "(independent route)" parenthetical and "(established without invoking CL-UNIQ)" for Steps 1-3 are the cycle-breaking annotations.
**Problem**: The cycle-breaking is asserted but the reader must verify that S3★(Σ') is genuinely independent of subspace preservation (and that Steps 1-3 are genuinely independent of CL-UNIQ). The matrix entry for S3★ under K.μ~ says "preserved via K.μ⁻ restriction + K.μ⁺ amendment alone (link-subspace fixity is downstream, not prerequisite)" — but this is in the matrix, not in the dependency chain itself.
**Required**: In the dependency chain paragraph, explicitly state which lemmas/properties each step consumes, making the non-circularity verifiable without cross-referencing the matrix.

### Issue 6: Step 4 of K.μ~ link-subspace fixity proof requires CL-UNIQ but doesn't explicitly state CL-UNIQ's role at the inductive step
**ASN-0047, *Decomposition of K.μ~* section, Step (4)**: The proof says "CL-UNIQ at Σ — the inductive hypothesis, link-subspace injectivity of M(d)|_{dom_L} — forces π(v) = v."
**Problem**: The induction is over reachable composite transitions, with CL-UNIQ as a per-state invariant of ExtendedReachableStateInvariants. The phrase "inductive hypothesis" is used without explicit reference to the ExtendedReachableStateInvariants induction. A reader checking this proof in isolation might not immediately see what "inductive hypothesis" refers to.
**Required**: Either cite the ExtendedReachableStateInvariants induction explicitly ("CL-UNIQ at Σ holds by the ExtendedReachableStateInvariants induction's per-state hypothesis at Σ"), or restate that CL-UNIQ is preserved at every reachable state and Σ is reachable.

## OUT_OF_SCOPE

### Topic 1: Concurrency and atomicity beyond SequentialTransitionAxiom
**Why out of scope**: The Scope section explicitly excludes "Operation atomicity and concurrency". The ASN relies on SequentialTransitionAxiom (inherited from ASN-0093) for the sequential atomic transition model. Per-operation atomicity (e.g., COPY appearing atomic at the operations layer despite decomposing into multiple elementary transitions) is left to future operations ASNs.

### Topic 2: Link-subspace contiguity exemption for tombstoning
**Why out of scope**: Nelson's tombstoning design (LM 4/9) for "deleted links awaiting historical backtrack" is addressed in the Open Questions section as requiring a separate mechanism outside K.μ⁻'s presentational-removal contract. This ASN intentionally enforces D-CTG★/D-MIN★/D-SEQ★ uniformly across both subspaces; interior link withdrawal is deferred.

### Topic 3: Account-level depth-1 tumbler extension
**Why out of scope**: Acknowledged in Open Questions — admitting K.δ k = 1 with `IsAccount(t)` would produce account-shaped siblings. The present ASN excludes this at the precondition, citing the consultation evidence that versioning is reserved to documents (Nelson, LM 4/29; Gregory `docreatenewversion`).

### Topic 4: Link inheritance under forking
**Why out of scope**: J4's fork definition explicitly notes "Link-subspace mappings from the source document are not copied" and that "A mechanism for link inheritance under forking, if desired, would require K.μ⁺_L steps in the fork composite and is outside this ASN's scope." This is consistent with the home-document ownership of links (L1a) and refractive following behavior.

VERDICT: REVISE
