# Review of ASN-0042

## REVISE

### Issue 1: O8 proof — notational error on π's membership

**ASN-0042, O8 proof (`The delegate persists with an unchanged prefix`)**: "By O12 (PrincipalPersistence), `Π_{Σ_d} ⊆ Π_{Σ'}`, and since `π' ∈ Π_{Σ_d}` (by condition (iii) of the delegation relation, `π'` entered `Π` at `Σ_d`), we have `π' ∈ Π_{Σ'}`."

**Problem**: The convention `delegated_Σ(π, π')` (per the Delegation Definition) means the transition is `Σ → Σ'` with `π' ∈ Π_{Σ'} ∖ Π_Σ`. Under that convention, `delegated_{Σ_d}(π, π')` implies `π' ∉ Π_{Σ_d}` — it enters at the target of the delegation transition, not at `Σ_d` itself. The claim `π' ∈ Π_{Σ_d}` contradicts condition (iii). The proof's `Π_{Σ_d} ⊆ Π_{Σ'}` step propagates the wrong side. Additionally, `π' ∈ Π_{Σ'}` is already a hypothesis of O8, so this whole derivation is unnecessary.

**Required**: Either delete the redundant derivation (since `π' ∈ Π_{Σ'}` is a hypothesis), or correct the notation to use `Π_{Σ_d^post}` (or `Π_{Σ_{d+1}}`) — the target of the delegation transition — and iterate O12 along the path `Σ_d^post →* Σ'`.

### Issue 2: O7(c) cites the wrong source for non-extension

**ASN-0042, O7(c) proof**: "no member of Π_{Σ'} has a prefix strictly extending `pfx(π')` (by O7(a)'s argument applied to `Σ'`, no member of `Π_Σ` strictly extends `pfx(π')`, and the only newcomer is `π'` itself)"

**Problem**: O7(a) establishes `ω_{Σ'}(a) = π'` for addresses in `dom(π') ∩ Σ'.B` — it concerns the longest-match outcome, not the structural fact "no member of `Π_Σ` strictly extends `pfx(π')`." That structural fact is exactly condition (vi) of the delegation relation (`¬(E π'' ∈ Π_Σ : pfx(π') ≺ pfx(π''))`). The citation invokes a derived consequence to justify what is a directly stated precondition of the delegation step.

**Required**: Replace the citation with condition (vi) of the delegation relation, which is what actually supplies the non-extension fact.

### Issue 3: NestingByDelegation IH application hand-waves chain preservation

**ASN-0042, NestingByDelegation inductive step**: "If both lie in `Π_{Σ_n}`, the IH applies (with `delegated_Σ*` extended to `Σ_{n+1}` by inclusion of the prior path)."

**Problem**: The parenthetical extension is asserted without justification. The disjunct "`pfx(π₁) ≺ pfx(π₂) ∧ delegated_{Σ_n}*(π₁, π₂)`" must be lifted to "`delegated_{Σ_{n+1}}*(π₁, π₂)`." The reasoning — that the witnessing delegation chain occurs at states along `Σ_0 → ... → Σ_n`, which is a prefix of `Σ_0 → ... → Σ_{n+1}`, so the same chain witnesses the closure at the later state — is correct but unstated. Similarly the non-nesting disjunct is preserved by O13 (immutable prefixes), which is also not cited.

**Required**: State the witness-preservation argument explicitly: the same delegation events along the shared path-prefix witness the closure at every later state, and prefix relations are preserved by O13.

### Issue 4: O18 bootstrap clause organization

**ASN-0042, O18**: "The base case is posited directly as a bootstrap clause companion to O14: `(A π ∈ Π₀ : pfx(π) ∈ Σ₀.B)` ... We posit the bootstrap reading as a separate baseline alongside O14."

**Problem**: The bootstrap clause is functionally part of O14's role (constraints on `Σ_0` and `Π_0`) but is stated inside O18 as a "companion" axiom. The "Properties Introduced" table lists O14 with six bootstrap clauses and O18 with "axiom" status, leaving the bootstrap clause `(A π ∈ Π₀ : pfx(π) ∈ Σ₀.B)` in an organizationally ambiguous place. Self-ownership at the prefix (worked example) and O10's non-coverage analysis both rely on this clause, so its provenance matters.

**Required**: Either move the bootstrap clause into O14's clause list, or make it an explicit named sub-axiom of O18 with its own labelled position in the Properties table — not a paragraph-level aside.

### Issue 5: O11 stated as a "property" but provides no formal contract

**ASN-0042, O11 (IdentityAxiomatic)**: "Any conforming implementation must provide *some* mechanism for binding sessions to principals, but the ownership properties O0–O10 are independent of which mechanism is chosen."

**Problem**: O11 is listed alongside O0–O10 in the Summary as if it carries the same kind of obligation, and it appears in the Properties Introduced table with status "axiom." But unlike the other axioms (O12, O13, O14, O15, O16, O18), it makes no verifiable claim — it is a scope disclaimer, not an axiom about state. The session-equation `session.account = pfx(π)` is presented as "an axiom of the session, not a theorem of the ownership model," which is meta-text describing the model's boundary rather than a property of the model.

**Required**: Either reframe O11 as a Scope note (similar to the Scope section at the end), or supply a formal contract that constrains some primitive of the model (e.g., a binding relation `session_principal : Session → Π`). As written, O11 is not a property at the same stratum as O0–O10.

### Issue 6: Recursive delegation depth argument cites T0(b) without zero-count refinement

**ASN-0042, O7(c) proof**: "by T0(b) (UnboundedLength), tumbler length is unbounded, so the ascending chain of prefixes `pfx(π) ≺ pfx(π') ≺ pfx(π'') ≺ ...` admits arbitrarily long delegation chains."

**Problem**: T0(b) provides a length-`n` witness `[1, 1, ..., 1]` with `zeros = 0`. Every delegate's prefix must satisfy `zeros ≤ 1` (condition (iv)). For account-level chains, the witness must extend the user field, not the node field — once the zero separator is placed, the user field can grow but no second zero may appear. The witnesses with `zeros = 1` of arbitrary length exist (e.g., `[1, 0, 1, 1, ..., 1]`) but require combining T0(a) (unbounded component values, used to choose successive U components) and T0(b) (unbounded length) and explicit zero-count tracking. The proof's bare citation of T0(b) does not deliver this.

**Required**: Either derive zero-count-constrained length unboundedness explicitly (T0(a) + T0(b) + zero-count construction) or weaken the claim to "the construction extends as far as the chosen sequence permits" without asserting unboundedness.

### Issue 7: O5 well-formedness for prefix not yet in Σ.B

**ASN-0042, O5 framing prose**: "This formulation avoids applying `ω` to the prefix itself (which may not yet be in `Σ.B`); instead it directly constrains the allocator to be the most-specific covering principal. Once `a` enters `Σ.B`, O2 gives `ω(a) = π` — the allocator becomes the effective owner of its own allocation."

**Problem**: This is an informal claim. The argument that "once `a` enters `Σ.B`, `ω(a) = π`" depends on the allocator being the unique most-specific covering principal *and* this status being preserved into `Σ'`. The first is given by O5's second conjunct; the second uses O12 + O13 (the prior covering principals from `Π_Σ` are exactly the covering principals in `Π_{Σ'} ∩ Π_Σ` with the same prefixes). The text asserts the conclusion without exhibiting the step. This argument is exercised in O4's inductive step but not centralized as a corollary.

**Required**: Either add a short corollary "Allocator becomes effective owner: `allocated_by_{Σ'}(π, a) ⟹ ω_{Σ'}(a) = π`" with derivation from O5 + O12 + O13 + O2, or remove the unsupported assertion from the O5 framing.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer mechanism
The ASN's "Open Questions" section explicitly flags this. The current model has no transfer; introducing one would require separate machinery (registry external to address structure, provenance/owner divergence semantics). This belongs in a future ASN that introduces a transfer operation.

### Topic 2: Cross-node identity federation
Mentioned in Open Questions. O9 (NodeLocalOwnership) deliberately treats per-node principals as independent; any federation would be additional structure on top of the model, not a revision of it.

### Topic 3: Liveness of allocation (every reachable principal can baptize again)
The fork existence proof (O10★) establishes that *if* `π` performs a baptism the postconditions hold and B6/O5 are satisfied. Whether `π` is *guaranteed* the opportunity to baptize in any given trajectory is a liveness question that belongs to a scheduling/operations ASN, not to the structural ownership specification.

VERDICT: REVISE
