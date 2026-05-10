# Review of ASN-0057

## REVISE

### Issue 1: D1 stated at #a = #b when the natural boundary is D0 + #a ≤ #b

**ASN-0057, D1 and parenthetical**: "For tumblers a, b ∈ T with a < b and #a = #b: a ⊕ (b ⊖ a) = b" ... "(The case #a < #b with type (i) divergence ... also admits a faithful round-trip, since the D1 proof depends only on k ≤ #a, not on #a = #b.)"

**Problem**: Two issues compound here.

(a) The parenthetical's reasoning is incomplete. "The D1 proof depends only on k ≤ #a" would, if true, mean D1 works for #a > #b with type (i) divergence — but it does not. When #a > #b, `w = b ⊖ a` has length max(#a, #b) = #a, and the result `a ⊕ w` has length #w = #a > #b, so it cannot equal b (by T3). The parenthetical omits the second necessary condition: the result length #w = max(#a, #b) must equal #b, which requires #a ≤ #b. Within the parenthetical's own scope (#a < #b), this is automatically satisfied, but the "since" clause overgeneralizes the reason.

(b) The formal statement D1 restricts to #a = #b when the ASN's own analysis shows the round-trip holds for all (a, b) satisfying D0 with #a ≤ #b. The component-by-component argument in the D1 proof uses #a = #b only to establish #w = #a; when #a < #b, #w = #b and every step still goes through (components before k copy from a = b, at k the advance cancels the subtraction, after k they copy from w = b's components, and the result has length #b). A future ASN building on D1 might unnecessarily restrict span computations to equal-length endpoints.

**Required**: Either generalize D1 to: "For a, b ∈ T with a < b, divergence(a, b) ≤ #a, and #a ≤ #b: a ⊕ (b ⊖ a) = b" — or keep D1 at #a = #b and add a corollary D1' for the #a < #b case. In either case, fix the parenthetical's reasoning to name both conditions (k ≤ #a for the component argument, #a ≤ #b for the length match).

### Issue 2: No concrete example

**ASN-0057, entire note**: No worked example with specific tumblers.

**Problem**: The D1 proof is component-by-component with variables, which is correct but abstract. A concrete scenario would verify both D0 and D1 against a specific case and anchor the reader's understanding — for instance, verifying that the displacement from `[1, 2, 3]` to `[1, 5, 1]` is `[0, 3, 1]` and that `[1, 2, 3] ⊕ [0, 3, 1] = [1, 5, 1]`.

**Required**: Add at least one worked example with specific tumblers, checking D0's precondition and tracing D1's round-trip step by step.

### Issue 3: Foundation name mismatch — "TumblerSubtract" for "TumblerSub"

**ASN-0057, displacement recovery section**: "This is exactly the formula for b ⊖ a from ASN-0034's TumblerSubtract" and "TumblerSubtract produces a displacement of length max(#a, #b) = #a"

**Problem**: ASN-0034 names the definition "TumblerSub." The ASN uses "TumblerSubtract," which is not the foundation name. This is inconsistent with the foundation's identifier for the same definition.

**Required**: Replace "TumblerSubtract" with "TumblerSub" throughout.

## OUT_OF_SCOPE

### Topic 1: Converse round-trip — (a ⊕ w) ⊖ a = w
**Why out of scope**: D1 recovers the endpoint b from the start a and the displacement. The converse — recovering the displacement from the endpoint and start — is a distinct identity with its own preconditions (related to but different from TA4's partial inverse). Natural companion to D1 but new territory.

### Topic 2: Uniqueness of displacement
**Why out of scope**: TA-LC (left cancellation, from the foundation) immediately gives: if a ⊕ w₁ = b = a ⊕ w₂ then w₁ = w₂. Combined with D1 (existence), the displacement from a to b is unique. The ASN's displacement recovery section derives this informally — formalizing it as a corollary would be tidy but is a one-line consequence of existing foundation material, not a gap in this ASN.

VERDICT: REVISE
