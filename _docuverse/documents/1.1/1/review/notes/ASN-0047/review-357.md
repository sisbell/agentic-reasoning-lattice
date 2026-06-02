# Review of ASN-0047

## REVISE

### Issue 1: Depth-rebasing fork bijection is load-bearing but never exercised at differing depths
**ASN-0047, J4 step (ii) / worked examples**: "This *depth-rebasing bijection* is the characterization of the fork... d_new's content subspace is freshly rebased to its own depth `m_new`."

**Problem**: J4 names the order- and multiplicity-preserving φ between `V_{s_C}(d_op)` at depth `m_old` and `V_{s_C}(d_new)` at depth `m_new` as *the* characterization of forking, and emphasizes that the two sets "differ only in depth." Yet every fork worked example (first-version, subsequent-version, duplicate-source) takes `m_new = m_old = 2`, so `φ([1,k]) = [1,k]` identically — the depth *rebasing* (mapping the k-th position at depth `m_old` to the k-th at a *different* depth `m_new`) is never concretely verified. Since `m_new` is a free caller choice (≥2) at d_new's first content insertion, a depth change is reachable, and it is precisely the case where φ is non-identity on V-position values. Standard 6 mandates a concrete example for key postconditions; the characterizing claim is checked only in its degenerate case.

**Required**: Add a worked fork in which `m_new ≠ m_old`, verifying that φ remains an order-/multiplicity-preserving bijection and that D-SEQ★/D-CTG★/D-MIN★ hold at the rebased depth, or state explicitly why `m_new = m_old` is forced (it does not appear to be).

### Issue 2: "Elementary" K.μ⁻ precondition is stated in terms of properties defined two sections later
**ASN-0047, Elementary transitions, K.μ⁻**: "Under D-SEQ★ at Σ, each non-empty `V_S(d)` has canonical shape `{[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}`..."

**Problem**: K.μ⁻'s elementary definition's precondition depends on D-SEQ★ (and the per-subspace D-CTG★/D-MIN★/S3★), all of which are introduced only in the later "Amendments to existing transitions" section. The definition is therefore not self-contained at its point of introduction, and the elementary/extended-state layering the ASN otherwise maintains (elementary defs, then subspace amendments) is conflated here: the "elementary" contraction is specified using a derived extended-state invariant. The forward reference is non-circular but obscures which layer owns the constructive precondition.

**Required**: Either state K.μ⁻'s elementary precondition in foundation terms (ASN-0036 D-CTG/D-MIN per-document) and introduce the per-subspace canonical-shape constraint in the Amendments section alongside D-SEQ★, or relocate the constructive precondition to after D-SEQ★ is defined.

### Issue 3: K.δ sub-case dispatch is specified twice
**ASN-0047, K.δ definition box (case (ii) k=0/1/2) and the separate "K.δ case (ii) discharge and parent-allocator activation" section**

**Problem**: The k=0/1/2 dispatch — operand admissibility, spawn parameter, and freshness discharge — is laid out in the K.δ definition's case (ii) sub-bullets, then re-narrated in the dedicated "K.δ case (ii) discharge" section ("k = 0 (sibling under existing allocator)... k = 1 (version...)... k = 2 (descent...)"). The second pass adds the spawnPt-premise table (genuinely new), but the surrounding per-k prose restates the box. A reader must reconcile two descriptions of the same three-way split. This is the relocated/duplicated-content pattern the anti-bloat classifier targets.

**Required**: Keep the spawnPt-premise table and activation mapping in the discharge section; reduce the per-k prose there to a pointer back to the K.δ box rather than re-describing each sub-case's operand/freshness conditions.

## OUT_OF_SCOPE

### Topic 1: Complete CREATENEWVERSION copy semantics (J4)
J4 specifies the fork composite's full postconditions (φ order/multiplicity preservation, depth rebasing, edit-inheritance source tracking) as an explicit model of Nelson's CREATENEWVERSION and Gregory's `docreatenewversion`. The Scope section lists CREATENEWVERSION as a named operation whose specification is out of scope.
**Why out of scope**: Establishing that the elementary taxonomy (K.δ + K.μ⁺ + K.ρ) *suffices* to compose forking belongs here; pinning down the named operation's complete copy contract is named-operation territory for a later ASN. The composite-existence claim can stay; the full operation spec should not anchor this ASN's invariant work.

VERDICT: REVISE
