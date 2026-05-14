# Review of ASN-0042

## REVISE

### Issue 1: O5 used in O4's proof before its formal introduction
**ASN-0042, "The Exclusivity Invariant" (proof of O4)**: "By O5 (SubdivisionAuthority), whenever `π` allocates `a`, the first conjunct of the postcondition gives `pfx(π) ≼ a`..."
**Problem**: O5 is cited as an established axiom in O4's proof, but O5's formal statement appears later in the "Subdivision Authority" section. This is a forward reference within the ASN. The State Axioms section mentions O5 only obliquely as a "Constraint" on `allocated_by_Σ`, without stating it formally. A reader following the document linearly encounters a proof depending on an axiom that has not yet been stated.
**Required**: Move O5 into the State Axioms section alongside O12–O18 and O16, where the primitive `allocated_by_Σ` is introduced and where its constraints belong. Section 9 ("Subdivision Authority") can retain the motivational prose but should not be the formal introduction site.

### Issue 2: `delegated` relation referenced by name before its formal definition
**ASN-0042, "Permanence and Refinement" (OwnershipDomainPermanence proof, Step 3)**: "By condition (i) of the `delegated` relation, `pfx(π_d) ≺ pfx(π')`. By condition (ii), `π_d` is the most-specific covering principal..."
**Problem**: The `delegated_Σ(π, π')` relation is referenced by name in section 6 (Permanence and Refinement), but is formally defined as a named relation only in section 10 (Delegation). O15 introduces the six conditions inline and explicitly notes "The Delegation section later names the conjunction of these conditions the `delegated_Σ(π, π')` relation." The proof uses the name before it has been introduced.
**Required**: Either promote the `delegated` definition into O15 directly (since the conditions are already enumerated there), or restructure section ordering so that Delegation (currently section 10) precedes the proofs that rely on the name. The current arrangement makes section 6 unintelligible without flipping forward.

### Issue 3: "Five axioms" count is inconsistent with section contents
**ASN-0042, "State Axioms" intro**: "The ownership model rests on five axioms about state evolution that the subsequent derivations assume. We state them explicitly."
**Problem**: The section actually introduces seven axioms (O12, O13, O14, O15, the primitive `allocated_by_Σ`, O16, O18) plus four derived properties (FiniteRegistry, NestingByDelegation, O17, PrefixBaptismCoupling). The "five" claim is wrong by at least two; even if `allocated_by_Σ` is read as a signature rather than a substantive axiom, the count remains six. A reader trying to enumerate the foundations of the model from this paragraph will be misled.
**Required**: Fix the count or restate the intro to describe the axiom inventory accurately.

### Issue 4: Bootstrap allocation regime versus transition allocation regime is not explicitly distinguished
**ASN-0042, "State Axioms" and "Worked Example"**: O5's contract reads `Σ → Σ' ∧ a ∈ Σ'.B ∖ Σ.B ∧ allocated_by_{Σ'}(π, a) ⟹ ...`; O16 has the same shape. Both quantify over `Σ → Σ'` transitions. But the worked example places element-level addresses like `[1, 0, 2, 0, 3, 0, 1]` into `Σ_0.B` at bootstrap and asserts these are "covered by π_N".
**Problem**: A reader trying to check the worked example against O5/O16 may ask: "Who allocated `[1, 0, 2, 0, 3, 0, 1]` at bootstrap, and does that satisfy O5?" The answer (bootstrap allocations are governed by ASN-0040's B₀ conf, not by O5/O16, because B₀ conf is the base case and O5/O16 are inductive-step axioms) is correct but not stated. The ASN should make the bifurcation explicit.
**Required**: Add one sentence to the State Axioms section noting that O5 and O16 constrain transition-induced allocations only; bootstrap allocations are governed by O14's coverage clause together with ASN-0040's B₀ conf, and need not be witnessed by an `allocated_by` event.

### Issue 5: O10's fork construction at node level produces a user-level address but the cited implementation evidence is account-level
**ASN-0042, "The Fork as Ownership Boundary"**: "Nelson: 'Thus users may create new published documents out of old ones indefinitely...' Gregory confirms the structural mechanism: `docreatenewversion`, when invoked on a document belonging to a different account, routes the allocation through `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` — placing the fork under the requesting principal's account, not under the source document."
**Problem**: The implementation evidence supports the case `zeros(pfx(π)) = 1 → zeros(a') = 2` (account-level principal forks to a document address in one step). The abstract O10 also covers `zeros(pfx(π)) = 0 → zeros(a') = 1` (node-level principal forks to a *user* address). The text addresses this asymmetry only obliquely ("the descent is π's organizational choice within its sovereignty, not a requirement of O10"). But a single baptism producing a user-level address does not satisfy the motivating goal — the principal cannot place content at a user-level address. The reader is left to assemble a multi-baptism trajectory for node-level principals without seeing it traced.
**Required**: Either (a) trace the multi-baptism trajectory for the node-level case explicitly (with B6 checks at each step) so that O10's existence claim is exhibited at content-bearing depth in both cases, or (b) restate O10's postcondition to acknowledge that for `zeros(pfx(π)) = 0` principals, the minimum-witness produces a structural-namespace address rather than a content-bearing one, and the principal must descend further by additional O5-authorized baptisms.

### Issue 6: O0's structural-decidability postcondition is asserted but not derived from the O1 definition
**ASN-0042, "Ownership as a Structural Predicate"**: O0 states that `owns(π, a)` is decidable from `pfx(π)` and `a` alone. O1 *defines* `owns(π, a) ≡ pfx(π) ≼ a`.
**Problem**: O0 is labeled a "design requirement" in the Properties Introduced table. But under O1's definition, O0 follows as a *theorem* from the structure of the prefix relation (length comparison + componentwise equality, each decidable from the two tumblers alone by T3). Treating O0 as a design requirement rather than as a derived consequence of O1 obscures the chain of reasoning: O0 is the property the design *aims at*, and O1 is the definition that *achieves it*. The Properties Introduced table should mark O0 as derived from O1 + Prefix + T3, or O0 should be presented as a stated goal followed by O1's verification that the goal is met.
**Required**: Update O0's status to "derived" (from O1, Prefix, T3) in the Properties Introduced table, and either show the brief derivation explicitly or note that O0 is the verification target of O1's definition.

## OUT_OF_SCOPE

None — the ASN respects its declared scope. Modification rights, content storage, link structures, baptism mechanism internals, replication, and authentication are correctly deferred. The Principal Identity section explicitly records the trust-boundary scope note without making verifiable claims about it.

VERDICT: REVISE
