# Review of ASN-0029

## REVISE

### Issue 1: D17 type error in FINDDOCSCONTAINING
**ASN-0029, Document Discovery**: "FINDDOCSCONTAINING(S) = {d ∈ Σ.D : (E p : 1 ≤ p ≤ n_d : Σ.V(d)(p) ∈ S)}"
**Problem**: S is introduced as "a set of I-address spans" — each element is a (start, length) pair. But `Σ.V(d)(p)` is a tumbler (an I-address). The membership test `tumbler ∈ set-of-spans` is a type error. A tumbler is not a span.
**Required**: Either define S as the union of address ranges `{t : (E (s,l) ∈ S : s ≤ t < s ⊕ l)}` and test membership against that set, or write the body as `(E (s,l) ∈ S : s ≤ Σ.V(d)(p) < s ⊕ l)`.

### Issue 2: Σ.pub has no specified initial value, no frame conditions, and no transition operation
**ASN-0029, Publication / Summary of State**: Σ.pub is introduced as new state but:
- D0 (CREATENEWDOCUMENT) does not specify `Σ'.pub(d)` for the new document. Presumably `private`, but unstated.
- D12 (CREATENEWVERSION) does not specify `Σ'.pub(d_v)` for the new version.
- Neither D0 nor D12 includes `(A d' ∈ Σ.D : Σ'.pub(d') = Σ.pub(d'))` in the frame.
- No PUBLISH operation is defined. The ASN describes what publication *means* (D10, D11) but never defines the operation that transitions `private → published` or `private → privashed`. D10 is an invariant over a state component that no specified operation writes to, making it vacuously true.

**Required**: (a) Specify initial publication status in D0 and D12. (b) Add Σ.pub preservation to the frame of every operation. (c) Define at minimum one transition operation (PUBLISH) with pre/post/frame, even if withdrawal and privash transitions are deferred to open questions.

### Issue 3: D10 "standard operations" is undefined
**ASN-0029, Publication**: "for all standard operations"
**Problem**: The invariant `[Σ.pub(d) = published ⟹ Σ'.pub(d) = published]` is qualified by "for all standard operations," but no operation is classified as standard vs. non-standard. This makes D10 unfalsifiable — any counterexample can be dismissed as a non-standard operation.
**Required**: Either state D10 unconditionally (published is permanent, full stop) and handle withdrawal as a separate mechanism with explicit preconditions, or define precisely which operations are standard.

### Issue 4: D5(a), D5a, and D15 state the same property at three inconsistent strengths
**ASN-0029, Structural Ownership / Access Control**: 
- D5(a): "only the owner may alter Σ.V(d)" — informal
- D5a: `[op modifies Σ.V(d) ∧ system_correct ⟹ account(d) = account(actor(op))]` — conditional
- D15: `[op modifies Σ.V(d) ⟹ account(d) = account(actor(op))]` — unconditional

**Problem**: D15 is strictly stronger than D5a. If D15 holds, D5a is redundant. But the prose acknowledges the system is cooperative ("the backend's account-validation function unconditionally accepts any account address"), which means D15 is not mechanically enforced and D5a is the honest formulation. The ASN presents both without resolving the discrepancy. Additionally, `actor(op)` and `system_correct` are undefined predicates.
**Required**: Choose one formulation. If the property is a design requirement on correct participants (not a mechanically enforced invariant), say so explicitly and define the terms.

### Issue 5: D13 uses `session` in a formal property after declaring sessions to be implementation
**ASN-0029, Versioning**: "account(d_s) = account(session) ⟹ ..." and "account(d_s) ≠ account(session) ⟹ ..."
**Problem**: The Access Control section states "The session mechanism is implementation. The principles it serves are abstract." Yet D13 places `session` in a formal property. `account(session)` is never defined — sessions are not part of the abstract state. The two cases in D13 cannot be evaluated without knowing what `session` means.
**Required**: Reformulate D13 in terms of the abstract state. E.g., parameterize CREATENEWVERSION by the requesting account: `CREATENEWVERSION(d_s, a_req)` where `a_req` is the requester's account address. Then the two cases are `account(d_s) = a_req` vs. `account(d_s) ≠ a_req`.

### Issue 6: D14 claims ≺ forms a forest, but ≺ as defined is the ancestor relation
**ASN-0029, Versioning**: "The structural subordination relation d_s ≺ d_v (defined as d_s ≼ d_v ∧ d_s ≠ d_v ∧ zeros(d_s) = zeros(d_v) = 2) forms a forest: no document has two structural parents"
**Problem**: ≺ as defined includes ALL proper document-level prefixes, not just the immediate parent. For d = A.0.B.0.C₁.C₂.C₃, both A.0.B.0.C₁ and A.0.B.0.C₁.C₂ satisfy ≺ with respect to d. So d has two predecessors under ≺, which violates the forest property. What forms a forest is the *covering relation* (immediate parent = longest proper document-level prefix), not ≺ itself.
**Required**: Either redefine ≺ as the immediate parent relation (each document's parent is its longest proper prefix at document level), or state that the Hasse diagram of the partial order ≺ is a forest.

### Issue 7: D12 missing explicit precondition
**ASN-0029, Versioning**: "CREATENEWVERSION(d_s) produces d_v such that: (a) d_v ∉ Σ.D ∧ d_v ∈ Σ'.D"
**Problem**: No precondition is stated. At minimum, `d_s ∈ Σ.D` is required — CREATENEWVERSION references `Σ.V(d_s)` in conditions (b) and (c), which is only defined when `d_s ∈ Σ.D`.
**Required**: State `pre: d_s ∈ Σ.D`.

### Issue 8: No concrete example verifying postconditions
**ASN-0029**: The ASN defines two operations (D0, D12) with formal postconditions but never traces through a specific scenario with concrete tumbler addresses and states.
**Problem**: D12 has five conditions plus a frame. D13 has two cases for version placement. Neither is verified against a concrete state — e.g., "Let Σ have document d = 1.0.1.0.1 with Σ.V(d) = {1↦a₁, 2↦a₂}. CREATENEWVERSION(d) by the owner produces d_v = 1.0.1.0.1.1. Check (a)–(e)..."
**Required**: Add at least one worked example for D12, covering both the own-document and cross-account cases of D13.

## OUT_OF_SCOPE

### Topic 1: COPY operation specification
**Why out of scope**: D8 and D9 correctly derive frame properties from P7. The full specification of COPY (which positions in the target receive which I-addresses, interaction with existing content) is new territory for a future ASN.

### Topic 2: Accessibility predicate and withdrawal mechanics
**Why out of scope**: The ASN correctly separates existence (D2: d ∈ Σ.D is permanent) from accessibility (an unformalized concept). Defining an accessibility predicate, withdrawal operations, and their interaction with D10 is new territory.

### Topic 3: Actor identity and authentication model
**Why out of scope**: The ASN acknowledges the cooperative trust model. Formalizing actor identity, authentication, and the relationship between claimed and actual identity is a separate concern.

VERDICT: REVISE
