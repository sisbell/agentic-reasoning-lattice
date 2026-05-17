# Review of ASN-0047

## REVISE

### Issue 1: K.δ combined `zeros` formula is incorrect for k = 0
**ASN-0047, K.δ (Entity creation), case (ii) sub-case combination**: "Combined: `zeros(e) = zeros(t) + (k − 1)`."
**Problem**: The combined formula gives `zeros(t) − 1` for k = 0, but the explicit k = 0 sub-case immediately above states `zeros(e) = zeros(t)` (sibling at same depth). The formula is correct for k = 1 (`zeros(e) = zeros(t)`, since TA5(d) at k = 1 introduces no zero separator) and k = 2 (`zeros(e) = zeros(t) + 1`, one separator added) but wrong for k = 0. The ghost-base worked example's Step 2 confirms: `e₂ = inc(e₁, 0)` gives `zeros(e₂) = zeros(e₁) = 2`, not `zeros(e₁) − 1 = 1`. The formula contradicts both the per-sub-case statements and the worked example.
**Required**: Replace with a formula that handles k = 0 correctly. Options: (a) closed form `zeros(e) = zeros(t) + max(0, k − 1)`; (b) explicit case split: "`zeros(e) = zeros(t)` for k ∈ {0, 1}; `zeros(e) = zeros(t) + 1` for k = 2".

### Issue 2: K.μ⁻ admissibility precondition references a nonexistent "third subspace"
**ASN-0047, K.μ⁻ (Arrangement contraction), Admissible removal pattern**: "the per-subspace patterns are independent: a composite K.μ⁻ may mix suffix removal in one subspace with full clearance in another and no change in a third, provided at least one subspace contracts strictly..."
**Problem**: The extended state has exactly two subspaces (s_C, s_L) per SC-NEQ. The phrase "no change in a third" references a third subspace that does not exist in this model. The reader cannot reconcile "in a third" with the two-subspace structure consistent throughout the rest of the ASN.
**Required**: Rephrase to fit the two-subspace structure, e.g., "a composite K.μ⁻ may apply any of {suffix removal, full clearance, no change} to each of the two subspaces independently, provided at least one subspace contracts strictly".

### Issue 3: Worked examples don't exercise NodeUniqueAllocation or NodeLineage non-vacuously
**ASN-0047, three worked examples**: None of the three examples (fork with insertion; ghost-base versioning; link allocation) includes a K.δ node-allocation event. The ghost-base example explicitly states "NodeUniqueAllocation (vacuous): K.δ at k = 1 with non-node t produces a non-node entity" and "NodeLineage: ... `e₁` is not a node, so the universal quantifier extends vacuously".
**Problem**: Two load-bearing axioms (NodeUniqueAllocation, NodeLineage) and the K.δ case (i) `n₀ ≼ e` precondition are introduced as central to the entity-allocation discipline but are never exercised in a concrete scenario. The depth standard requires verification against at least one specific scenario; node allocation has none.
**Required**: Add a worked example exercising K.δ case (i) — e.g., baptising a new node `[1, 2]` under n₀ = [1] — with explicit verification of NodeUniqueAllocation (freshness), NodeLineage (`[1] ≼ [1, 2]`), and the case (i) precondition discharge.

### Issue 4: SubAllocatorAxiom's "outside T10a's per-owner inc tree" framing conflicts with the structural producibility it later concedes
**ASN-0047, Allocator hierarchy under documents**: The section first asserts that sub-allocator anchors `b_C(d)`, `b_L(d)` are "outside T10a's per-owner inc tree rooted at d" but the L1c reconciliation paragraph admits the anchors are structurally derivable from a T10a-conforming inc chain (`d → inc(d, 2) → inc(·, 0)`).
**Problem**: The two framings appear contradictory on first reading. The resolution (operational vs structural) is buried in long prose after the apparent contradiction. A careful reader must work through several paragraphs to reconcile.
**Required**: Lead with the structural derivation (`b_C(d) = inc(d, 2)`, `b_L(d) = inc(b_C(d), 0)` — both producible via T10a inc steps), then introduce SubAllocatorAxiom as the *operational* claim that the anchors exist as named entry points at document-creation time without requiring the chain to be operationally executed by a single allocator (which T10a's at-most-once would forbid). Demote "outside T10a's tree" to a parenthetical about operational spawning events.

## OUT_OF_SCOPE

### Topic 1: Tombstone-style interior link withdrawal mechanism
**Why out of scope**: The ASN's Open Questions section and the *Structural sufficiency and known gaps* section both flag this as a deferred topic. The K.μ⁻ amendment's D-CTG★/D-MIN★ postconditions restrict link-subspace contractions to suffix truncations by design, foreclosing Nelson's tombstone mechanism; the resolution belongs to a future withdrawal-mechanism ASN.

### Topic 2: Version-management semantics beyond bare entity allocation
**Why out of scope**: K.δ's k = 1 sub-case structurally admits version creation, but version-specific invariants (arrangement transitions between versions, lineage acyclicity, content-allocator linkage between base and version) are explicitly deferred to a future version-management ASN.

### Topic 3: Account-level K.δ with k = 1 (depth-1 tumbler extension at the account level)
**Why out of scope**: K.δ's k = 1 sub-case is restricted to `IsDocument(t)` because the design admits no account-version semantics. The exclusion is recorded as an open question; admitting it would require defining account-version semantics first.

### Topic 4: Non-T10a allocator admissibility for content or links
**Why out of scope**: The ASN assumes T10a-conforming allocation throughout, with node allocation as a stipulated exception via NodeUniqueAllocation. Broader allocator disciplines are deferred per *Structural sufficiency and known gaps*.

VERDICT: REVISE
