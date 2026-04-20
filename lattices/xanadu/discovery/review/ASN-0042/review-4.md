# Review of ASN-0042

## REVISE

### Issue 1: O8 formalization admits the pre-delegation state, where the claim is false
**ASN-0042, Delegation (O8)**: `(A π, π', a, Σ, Σ' : delegated_Σ(π, π') ∧ a ∈ dom(π') ∩ Σ'.alloc ∧ Σ →* Σ' : ω_{Σ'}(a) ≠ π)`
**Problem**: The reflexive-transitive closure `→*` includes `Σ' = Σ` (zero transitions). At `Σ` — the pre-delegation state — `π'` does not yet exist in `Π_Σ` (by delegation condition (iii)). If `π` is the most-specific covering principal for addresses in `dom(π')` at `Σ` (which it must be, by delegation condition (ii)), then `ω_Σ(a) = π` for any `a ∈ dom(π') ∩ Σ.alloc`. The claim `ω_Σ(a) ≠ π` is false. Concrete counterexample: `π` has `pfx = [1, 0, 2]`, `π'` has `pfx = [1, 0, 2, 3]`, `a = [1, 0, 2, 3, 0, 1, 0, 1] ∈ Σ.alloc`. Before delegation, `ω_Σ(a) = π` — the sole covering principal with the longest prefix. The prose correctly says "never *regains*," which presupposes the loss has already occurred. The formalization says "never owns," which covers states where the loss hasn't happened yet.
**Required**: Replace `Σ →* Σ'` with `Σ →⁺ Σ'` (transitive closure — at least one transition from `Σ`), ensuring `Σ'` is a post-delegation state. Equivalently, let `Σ₁` be the immediate post-delegation state and write `Σ₁ →* Σ'`.

### Issue 2: O6 derived guarantee `pfx(ω(a)) ≼ acct(a)` stated without derivation
**ASN-0042, Structural Provenance**: "The effective owner's prefix is always embedded within the account field: `pfx(ω(a)) ≼ acct(a)`."
**Problem**: This is a derived guarantee used in the worked example (verifying O6 for `a₄`) and in the discussion of when equality vs. strict containment holds, but no derivation is given. The claim requires connecting three facts: (1) by definition of `ω`, `pfx(ω(a)) ≼ a`; (2) by O1a, `zeros(pfx(ω(a))) ≤ 1`, so `pfx(ω(a))` extends at most through the user field; (3) `acct(a)` includes the full node and user fields of `a`, so `pfx(ω(a))` — being no longer than the account portion — is a prefix of `acct(a)`. Each step is straightforward, but the chain must be shown, not asserted. The claim is load-bearing: the worked example uses it to verify the sub-account namespace case, and the prose builds on the equality/containment distinction.
**Required**: Add the three-step derivation. Two sentences suffice: "By definition of `ω`, `pfx(ω(a)) ≼ a`. Since `zeros(pfx(ω(a))) ≤ 1` (O1a), all components of `pfx(ω(a))` fall within the node-and-user portion of `a`, which is `acct(a)`; hence `pfx(ω(a)) ≼ acct(a)`."

### Issue 3: O4 inductive argument omits the preservation step
**ASN-0042, The Exclusivity Invariant (O4 derivation)**: "by O14, the initial state has a principal covering all initially allocated addresses. If `a` is newly allocated in a transition `Σ → Σ'`, then by O5 the allocator is a principal `π` with `pfx(π) ≼ a`. By O12, `π` persists in `Σ'`. By induction on the transition history, O4 holds in every reachable state."
**Problem**: The inductive step handles new allocations (by O5) and the base case (by O14) but does not explicitly state that *previously* covered addresses remain covered. The derivation says "By O12, `π` persists" for the specific allocating principal, but the general statement — that ALL previously covering principals persist with unchanged prefixes, so ALL previously covered addresses retain their coverage — is not given. The preservation step requires both O12 (no principal is removed) and O13 (no prefix changes), and their conjunction is what closes the induction.
**Required**: Add one sentence to the inductive step: "For addresses already in `Σ.alloc`, their covering principals persist in `Σ'` (O12) with unchanged prefixes (O13), so coverage is preserved."

## OUT_OF_SCOPE

### Topic 1: Modification authority — the rights ownership confers beyond allocation and delegation
**Why out of scope**: The ASN establishes *who owns what* but deliberately does not formalize *what an owner may do to content*. O10 implies that non-ownership prevents modification (the system offers a fork instead), but the formal content of modification rights — which operations an effective owner is authorized to perform on content at owned addresses — belongs in a future ASN on access control. The current ASN's scope exclusion ("Modification rights and access control") is correct.

### Topic 2: Delegation atomicity under concurrent transitions
**Why out of scope**: O5 and the delegation definition assume a linearized transition history (the "most-specific covering principal" is evaluated at a definite state `Σ`). Under concurrent delegation by independent principals, the ordering of state transitions determines which delegation succeeds first, which affects the most-specific covering principal for subsequent delegations. This is an execution-model concern, not an ownership-model concern.

VERDICT: REVISE
