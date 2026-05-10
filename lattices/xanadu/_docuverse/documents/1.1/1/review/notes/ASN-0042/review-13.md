# Review of ASN-0042

## REVISE

### Issue 1: O14 omits T4 base case for initial principals' prefixes

**ASN-0042, State Axioms (O14)**: O14 provides explicit base cases for O1a (`zeros(pfx(π)) ≤ 1`) and O1b (injectivity) but does not require `T4(pfx(π))` for initial principals.

**Problem**: The delegation T4 preservation proof states: "Existing principals' prefixes are unchanged by O12. T4 is maintained across the transition." This inductive step assumes existing principals already satisfy T4, which requires the base case. The Properties Introduced table declares `T4(pfx(π))` as a universal constraint on `pfx`, and the O6 forward direction explicitly relies on T4 of the prefix ("which are positive by T4 applied to `pfx(π)`"). Without the base case, a pathological initial state could admit a prefix like `[1, 2, 0]` (satisfying `zeros ≤ 1` but violating T4 — trailing zero, empty user field), breaking the O6 proof and the `acct` function's well-definedness.

The ASN is *inconsistent* in its treatment: O1a and O1b each receive explicit base-case clauses in O14, yet T4 — which receives an analogous inductive-step proof in the Delegation section — receives none.

**Required**: Add a fourth clause to O14: `(A π ∈ Π₀ : T4(pfx(π)))`. This closes the T4 induction and makes O14 parallel in structure for all three preserved properties (O1a, O1b, T4).

### Issue 2: O6 forward proof does not handle the sub-case where both `zeros(pfx(π)) = 0` and `zeros(a) = 0`

**ASN-0042, Structural Provenance (O6 forward direction, zeros = 0 case)**: "By T4's field structure (FieldParsing), the nonzero components preceding `a`'s first zero separator constitute `a`'s node field."

**Problem**: When `zeros(a) = 0`, there is no zero separator in `a`. The stated reasoning — "nonzero components preceding `a`'s first zero separator" — does not apply; there is no separator to precede. By FieldParsing, `zeros(a) = 0` means the entire tumbler is the node field. The conclusion `pfx(π) ≼ acct(a)` still holds trivially (`acct(a) = a` when `zeros(a) = 0`, so `pfx(π) ≼ a = acct(a)`), but the intermediate step's language is inapplicable to this sub-case. Since the zeros = 0 / zeros ≥ 1 distinction in `a` produces different field structures, the sub-case should be shown.

**Required**: Split the `zeros(pfx(π)) = 0` case into two sub-cases: (1) when `zeros(a) = 0`, note `acct(a) = a` and the result is immediate; (2) when `zeros(a) ≥ 1`, proceed with the existing zero-separator argument.

### Issue 3: Worked example O3 verification assumes `a₁ ∈ Σ₀.alloc` without establishment

**ASN-0042, Worked Example (State Σ₁)**: "**O3 (refinement)**: In the transition Σ₀ → Σ₁, `ω(a₁)` changed from `π_N` to `π_A`."

**Problem**: O3 is scoped to `a ∈ Σ.alloc` — addresses allocated in the pre-state. The example introduces `a₁ = [1, 0, 2, 0, 3, 0, 1]` in "State Σ₁" without stating whether `a₁` was allocated in Σ₀. If `a₁` was first allocated in Σ₁ (after the delegation), `ω_{Σ₀}(a₁)` is undefined and O3 does not apply — there is no prior effective owner to change from. The verification's ✓ is therefore grounded on an unstated assumption.

**Required**: Either (a) state explicitly that `a₁ ∈ Σ₀.alloc` (e.g., "Suppose `a₁` was allocated by `π_N` before delegation"), or (b) note that O3 applies only if `a₁` was in `Σ₀.alloc` and show the verification conditionally.

## OUT_OF_SCOPE

### Topic 1: Operational consequences of ownership beyond subdivision

The ASN defines what ownership *is* (prefix containment, exclusivity, delegation) and one right it confers (O5, subdivision authority). What modification, withdrawal, or publication rights `ω(a) = π` confers — "only the owner has a right to withdraw a document or change it" (LM 2/29) — is not formalized.

**Why out of scope**: The ASN's scope section explicitly excludes "Modification rights and access control." The ownership model provides the authorization *subject* (who owns what); the content model provides the authorization *object* (what can be done). These are separate concerns.

### Topic 2: Version DAG relationship between original and fork under O10

When O10 produces a fork `a'` of foreign content at `a`, the ownership model establishes that `a'` is independently owned. The *content* relationship between `a` and `a'` — whether `a'` transcludesthe content, how version parentage is recorded, whether links follow — is unspecified.

**Why out of scope**: The scope section excludes "document creation and lifecycle," "I-space and V-space," and "links and endsets." O10 deliberately states only the ownership postconditions, deferring the content semantics to the content model ASN.

VERDICT: REVISE
