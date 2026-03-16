# Review of ASN-0042

## REVISE

### Issue 1: O14 does not provide the base case for O1a and O1b invariants

**ASN-0042, State Axioms / Delegation**: The invariant proof for O1a is: "By condition (iv), any π' admitted by the delegated relation satisfies zeros(pfx(π')) ≤ 1. [...] the existing principals are unchanged by O12. O1a is maintained." Similarly, O1b preservation is proved against existing principals at each transition.

**Problem**: Both invariants require induction on the transition history. The inductive step is shown (delegation preserves O1a via condition (iv); O1b via the length contradiction). The base case — that all principals in Π₀ satisfy `zeros(pfx(π)) ≤ 1` and have pairwise distinct prefixes — is assumed but never stated in O14's formalization. O14 says only `Π₀ ≠ ∅` and coverage of initially allocated addresses. The prose says initial principals are "node-level" (zeros = 0), which satisfies both constraints, but the formal statement of O14 is silent. The inductive argument for O1a and O1b is incomplete without this base case.

**Required**: Add explicit constraints to O14:

  `(A π ∈ Π₀ : zeros(pfx(π)) ≤ 1)` and `(A π₁, π₂ ∈ Π₀ : pfx(π₁) = pfx(π₂) ⟹ π₁ = π₂)`

Or equivalently, state in the O1a/O1b preservation proofs that the base case holds by requiring O14 to include these constraints.

---

### Issue 2: O6 biconditional forward direction compresses the field-alignment argument

**ASN-0042, Structural Provenance**: "Since pfx(π) ≼ a, the components of pfx(π) match a's leading components, and these leading components — being confined to node and user fields by the zero count — form a prefix of the components in acct(a). Hence pfx(π) ≼ a implies pfx(π) ≼ acct(a)."

**Problem**: The claim "form a prefix of the components in acct(a)" requires showing that the prefix relation forces field-boundary alignment between pfx(π) and a. Specifically: when `zeros(pfx(π)) = 1`, the zero at position α+1 in pfx(π) forces `a_{α+1} = 0` via the prefix relation, and T4 applied to `a` ensures this zero is a's node-user field separator (since all prior matched components are positive). This aligns pfx(π)'s field structure with a's, ensuring the matched components fall within acct(a). When `zeros(pfx(π)) = 0`, all matched components are positive and therefore within a's node field, which is a prefix of acct(a).

The ASN provides exactly this case split later (in the "effective owner's prefix is embedded" derivation, step (3)), but only for the specific instance π = ω(a). The general biconditional — which is the tool used to prove O6 — is established before the case split appears, with the field-alignment step compressed into a single clause.

**Required**: Inline the two-case field-alignment argument into the biconditional's forward direction, or at minimum forward-reference the later case split explicitly. The biconditional is load-bearing (used to prove O6 and referenced in O10); its forward direction should not require the reader to locate a later proof of a specific instance to verify the general claim.

---

### Issue 3: O10 does not establish existence of a suitable fork address

**ASN-0042, The Fork as Ownership Boundary**: "the system provides an alternative: π may create a new address a' within dom(π)" with postcondition "ω(a') = π."

**Problem**: The postcondition `ω(a') = π` requires that `a'` lies in `dom(π)` but not in any sub-delegate's domain — i.e., `a' ∈ dom(π) ∖ ⋃{dom(π_i) : π_i sub-delegate of π}`. The ASN asserts "an unbounded supply of fresh addresses" but does not prove that suitable addresses exist in every reachable state. The argument is straightforward but missing:

(i) At any reachable state, Π is finite (O15: at most one new principal per transition, finitely many transitions).
(ii) Sub-delegates' prefixes satisfy `zeros ≤ 1` (O1a), so no sub-delegate has a document-level or element-level prefix.
(iii) For an account-level principal (zeros = 1), document-level addresses within its domain (obtainable via allocation with the zero separator crossing into the document field) are never in any sub-delegate's domain, because sub-delegates' prefixes have zeros ≤ 1 and cannot reach document-level.
(iv) For a node-level principal (zeros = 0), component values are unbounded (T0a), so a fresh user-field value not matching any existing sub-delegate's user field is always available.

In either case, `π` can always find an address where it remains the effective owner.

**Required**: State and prove the existence of `a'` satisfying `ω(a') = π` for any principal `π` in any reachable state. The argument from finite Π, O1a, and T0a/T0b is compact and should appear alongside O10's formulation.

---

## OUT_OF_SCOPE

### Topic 1: Content rights as distinct from address ownership

The ASN cleanly separates provenance (O6 — the address records its creator) from authority (ω — the effective owner controls subdivision and delegation). The consequence — that under a hypothetical transfer regime, provenance and authority would diverge — is noted but not formalized. The formal relationship between "who created" and "who may act" is a distinct concern that belongs in a future ASN on access rights or content sharing, building on the ownership model established here.

**Why out of scope**: The ownership model defines authority over address space, not rights over content. Content rights (read, transclude, annotate, withdraw) require the operation model, which is explicitly excluded from this ASN's scope.

VERDICT: REVISE
