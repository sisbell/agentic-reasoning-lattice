# Review of ASN-0042

## REVISE

### Issue 1: O8 (IrrevocableDelegation) is contradicted by sub-delegation

**ASN-0042, O8**: `(A π, π', a : delegated(π, π') ∧ a ∈ dom(π') : ω(a) = π' in all subsequent states)`

**Problem**: The formal statement claims `ω(a) = π'` permanently for *all* `a ∈ dom(π')`. But O7(c) permits `π'` to recursively delegate — if `π'` delegates to `π''` with `pfx(π') ≺ pfx(π'')`, then for `a ∈ dom(π'')`, O2 gives `ω(a) = π'' ≠ π'`. Property O3 explicitly permits this change. So O8 contradicts O3 and O7 for any `a` in a sub-delegate's domain.

Secondary issue: `dom(π')` includes non-allocated addresses where `ω` is undefined (ω is grounded by O4, which quantifies over `Σ.alloc`).

**Required**: The formalization should capture irrevocability as: the *delegating parent* `π` never regains effective ownership. A correct version:

`(A π, π', a, Σ, Σ' : delegated_Σ(π, π') ∧ a ∈ dom(π') ∩ Σ'.alloc ∧ Σ →* Σ' : ω_{Σ'}(a) ≠ π)`

This says the parent can never get the addresses back, without claiming the delegate keeps them forever.

### Issue 2: O6 (StructuralProvenance) has a counterexample

**ASN-0042, O6**: `(A a ∈ Σ.alloc : zeros(pfx(ω(a))) = 1 ⟹ acct(a) = pfx(ω(a)))`

**Problem**: Let `Π = {π₁}` with `pfx(π₁) = [1, 0, 2]` (zeros = 1). The address `a = [1, 0, 2, 3]` is valid by T4 (zeros = 1, node field `[1]`, user field `[2, 3]`, all components positive). By O5, `π₁` is the most-specific covering principal (`pfx(π₁) = [1, 0, 2] ≼ [1, 0, 2, 3]`) and may allocate `a`. After allocation: `ω(a) = π₁`, `zeros(pfx(π₁)) = 1`, but `acct(a) = [1, 0, 2, 3] ≠ [1, 0, 2] = pfx(π₁)`. O6 fails.

The root cause: when an account-level principal's domain contains addresses whose user field extends beyond the principal's own prefix (sub-account addresses not yet delegated), `acct(a)` is strictly longer than `pfx(ω(a))`. O10(b) inherits the same gap — the claim `acct(a') = pfx(π)` for forked addresses depends on the same assumption.

**Required**: Either (a) restrict O6 to document-level and deeper addresses by adding precondition `zeros(a) ≥ 2`; or (b) add a constraint that every allocated address at account level whose `acct` doesn't match a principal's prefix must correspond to a delegated principal; or (c) prove that T10a's allocation discipline prevents such addresses from existing without delegation. Whichever fix is chosen, the worked example should include a case that exercises this boundary.

### Issue 3: `delegated(π, π')` is used but never defined

**ASN-0042, O7 and O8**: `delegated(π, π')` appears as a premise in both properties.

**Problem**: The relation is used as a formal primitive but has no definition. This makes O7 and O8 formally vacuous — the premise cannot be evaluated for any concrete pair. The relation encodes *who* performed a delegation, which is distinct from the structural fact `pfx(π) ≺ pfx(π')`. Without a definition, O8's claim about the specific delegating parent is ungrounded, and the distinction between direct delegation (`π→π'`) and transitive delegation (`π→π'→π''`) is lost.

**Required**: Define `delegated(π, π')` — at minimum: "`π'` was introduced into `Π` by an act of `π`, with `pfx(π) ≺ pfx(π')`." This grounds O8 and lets the Corollary formally distinguish parent from grandparent delegation.

### Issue 4: O7 formal statement omits authorization constraint

**ASN-0042, O7**: `(A π, π' : pfx(π) ≺ pfx(π') ∧ zeros(pfx(π')) ≤ 1 ∧ delegated(π, π') : ...)`

**Problem**: The formal statement permits delegation by any ancestor whose prefix is a prefix of the delegate's. It does not require `π` to be the most-specific covering principal for `pfx(π')`. Concrete case: `π₁` with `pfx = [1, 0, 2]` delegates to `π₂` with `pfx = [1, 0, 2, 3]`. Now `π₁` attempts to delegate `[1, 0, 2, 3, 5]` to `π₃`. O7 as stated permits this (`pfx(π₁) ≺ [1, 0, 2, 3, 5]`), but O5 forbids it (`π₂` is the most-specific covering principal). The prose correctly invokes O5, but the formal statement is independently satisfiable without it.

**Required**: Either incorporate the O5 constraint into O7's premises — `(A π'' ∈ Π : pfx(π'') ≼ pfx(π') ⟹ #pfx(π'') ≤ #pfx(π))` — or add an explicit clause noting that O7's domain is restricted by O5.

## OUT_OF_SCOPE

### Topic 1: Delegation as a state transition
The ASN defines the *consequences* of delegation (O7) but not the transition itself — preconditions, what changes, whether allocation and principal creation are atomic. Natural future work for a baptism/delegation operations ASN.
**Why out of scope**: The ASN correctly separates authorization from mechanism.

### Topic 2: Ownership across the version DAG
O10 establishes that non-owners fork rather than modify. The formal relationship between the forked address and the source — version parentage, content sharing, link inheritance — belongs to the content/versioning model.
**Why out of scope**: The ownership model identifies the fork point; the content model specifies what the fork contains.

VERDICT: REVISE
