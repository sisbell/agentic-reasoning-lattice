# Review of ASN-0033

## REVISE

### Issue 1: N1 quantifies over N, but the property is false for N
**ASN-0033, "The node tree"**: "Every node n ∈ N with n ≠ r satisfies r ≼ n."
**Problem**: N is defined as `{n ∈ T : n > 0 ∧ zeros(n) = 0}`. The tumbler `[2]` satisfies both conditions — it is positive and contains no zeros — so `[2] ∈ N`. But `r = [1]` is not a prefix of `[2]`: PrefixOf requires `p_i = t_i` for all `i ≤ #p`, and `1 ≠ 2`. The universal claim over N is false. The text asserts "The first component of every node address is 1" as though it follows from the definition, but the definition places no constraint on the first component beyond positivity.
**Required**: Either restrict the definition of N (add `n₁ = 1`), or quantify N1 over `Σ.nodes` instead of N. The second option is cleaner: N is the syntactic class of tumbler shapes that *could* be node addresses; the constraint that all actual nodes descend from `[1]` is a system invariant on `Σ.nodes`, not a property of tubler syntax.

### Issue 2: N3 is not a specialization of T8
**ASN-0033, "Baptism"**: "This is T8 (AddressPermanence) specialized to node addresses."
**Problem**: T8 says: "If tumbler `a ∈ T` is assigned to *content* `c` at any point in the system's history, then `a` remains assigned to `c`." T8 governs the I-space content-assignment relation. `Σ.nodes` is a new state component introduced by this ASN — it tracks which node addresses have been baptized, not which addresses have been assigned content. The monotonicity of set membership in `Σ.nodes` is structurally analogous to T8 but is not entailed by it. Different state component, different relation.
**Required**: State N3 as an independent invariant with its own justification, not as a corollary of T8. The justification is straightforward (BAPTIZE only adds; no operation removes — see Issue 3), but it must stand on its own.

### Issue 3: BAPTIZE exclusivity is assumed but never stated
**ASN-0033, "Baptism" / properties N3, N4**: N3 (monotonicity: no operation removes a node) and N4 (gap-free children: siblings differ by exactly 1) both depend on BAPTIZE being the *exclusive* mechanism for modifying `Σ.nodes`. If any other operation could add to or remove from `Σ.nodes`, N3 could be violated by removal, and N4 could be violated by inserting a child out of sequence (e.g., adding `[p, 5]` without `[p, 4]`). The ASN defines BAPTIZE and verifies N2 preservation against it, but never formally states: "BAPTIZE is the sole operation that modifies `Σ.nodes`; all other operations preserve `Σ.nodes` as a frame condition."
**Required**: Add an explicit statement that `Σ.nodes` is modified only by BAPTIZE. This is the load-bearing assumption for N3, N4, and the N2 preservation argument. Without it, the invariants are conditional on an unstated premise. (Additionally, N3 and N4 preservation under BAPTIZE is argued informally but not verified with the same rigor as N2 — brief explicit verification for each would close the gap.)

### Issue 4: N9 introduces undefined terms and contradicts BAPTIZE's precondition
**ASN-0033, "The allocation boundary"**: "Only an agent authorized by the parent node p can invoke BAPTIZE(p)."
**Problem**: "Agent" and "authorized by" are undefined. BAPTIZE's formal precondition is `p ∈ Σ.nodes` — it makes no reference to agents, callers, or authorization. The property table lists N9 as a formal property, but the formal operation specification permits unrestricted invocation by any party with access to a baptized parent. The prose and the formalism disagree.
**Required**: Either (a) add an authorization predicate to BAPTIZE's precondition (`p ∈ Σ.nodes ∧ authorized(caller, p)`, with `authorized` left abstract), or (b) demote N9 to an open question / design constraint to be formalized when the authorization model is specified. As stated, N9 is a property that cannot be verified or falsified.

### Issue 5: Gregory evidence mislabels account addresses as node addresses
**ASN-0033, "Baptism"**: "Golden test evidence shows node addresses [1, 1, 0, 1, 1], [1, 1, 0, 1, 2], [1, 1, 0, 1, 3]"
**Problem**: By the ASN's own T4 classification, `zeros(t) = 0` is a node address and `zeros(t) = 1` is an account address. Each of `[1, 1, 0, 1, 1]`, `[1, 1, 0, 1, 2]`, `[1, 1, 0, 1, 3]` contains exactly one zero component, making them account addresses under node `[1, 1]`, not node addresses. The text calls them "node addresses."
**Required**: Correct the labeling. These are account addresses whose *node field* `[1, 1]` demonstrates the all-positive, zero-free property. If the intent is to show that node-level allocation produces no zero separator, the evidence should either be actual node addresses (e.g., `[1, 1]`, `[1, 2]`, `[1, 3]`) or the text should say "addresses with node field `[1, 1]`" rather than "node addresses."

## OUT_OF_SCOPE

No items. The ASN's scope section correctly delineates its boundaries, and the open questions appropriately flag future work.

VERDICT: REVISE
