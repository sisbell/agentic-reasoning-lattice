# Revision Categorization — ASN-0042 review-22

**Date:** 2026-03-28 21:15

The ASN shows "(none)" under REVISE Items. Let me check the pending review file.

<tool_use>
{"type":"tool","name":"Read","input":{"file_path":"vault/2-review/ASN-0042/review-22.md"}}
</tool_use>

<tool_result>
<result>
---
asn: ASN-0042
review: 22
date: 2026-03-28
reviewer: o3
---

# Review 22: ASN-0042 (Tumbler Ownership)

## Summary

ASN-0042 is a mature, carefully argued specification with strong evidence integration. This review focuses on residual gaps in proof rigor and notational precision that would need resolution before formalization.

## Findings

### Finding 1 — O14 non-nesting clause needs inductive preservation proof
**Severity: REVISE**

O14 establishes a pairwise non-nesting invariant for bootstrap principals: no bootstrap principal's prefix extends another's. The text then claims delegation preserves O1a, O1b, and T4, with detailed proofs for each — but never proves that delegation preserves the *non-nesting invariant itself* across transitions.

The Account-level permanence Corollary's inductive step assumes that at the point of any delegation, the existing principal set satisfies pairwise constraints that prevent unauthorized nesting. But the only invariant shown to be preserved inductively is O1a/O1b/T4 — the non-nesting property (that no two principals have nested prefixes *unless one was delegated by or through the other*) is used but never stated as an invariant or shown to be maintained.

Specifically: condition (vi) of the `delegated` relation prevents a new principal from being introduced *above* an existing one, and condition (i) ensures it is introduced *below* its delegator. But the proof never shows that the combination of (i), (ii), and (vi) across multiple delegation steps maintains the property that every nesting relationship in Π traces back through the delegation chain. This is the load-bearing claim in the Corollary's inductive step ("whose authority derives from π by the inductive hypothesis"), and it needs an explicit invariant statement and preservation proof.

**Recommendation:** State an explicit invariant — e.g., "for all π₁, π₂ ∈ Π with pfx(π₁) ≺ pfx(π₂), either π₂ was delegated by π₁ or there exists a chain π₁ → ... → π₂ through the delegation relation" — and prove it is preserved by each delegation step. This closes the gap between O14's base case and the Corollary's inductive assumption.


### Finding 2 — O9 domain restriction incomplete for node-level principals
**Severity: REVISE**

O9 states `owns(π, a) ⟹ N(pfx(π)) ≼ N(a)` and proves it for both `zeros(pfx(π)) = 0` and `zeros(pfx(π)) = 1`. For the `zeros = 0` case, the text correctly derives `N(pfx(π)) ≼ N(a)` but notes this permits `N(a)` to be strictly longer than `N(pfx(π))`.

The issue: the text claims O9 restricts ownership to not "cross node boundaries," but for node-level principals, the prefix relation gives `pfx(π) ≼ a` which (when `zeros(pfx(π)) = 0`) means *every* component of the prefix matches `a`'s leading components. If `pfx(π) = [1, 2]` with `zeros = 0`, then `[1, 2] ≼ [1, 2, 3, 0, 1, 0, 1]` — the address could have a 3-component node field `[1, 2, 3]`. The principal "owns" addresses with node fields it didn't explicitly enumerate.

This isn't a bug — it's a correct consequence of prefix semantics — but the text's claim that "ownership cannot cross node boundaries" is imprecise. What O9 actually guarantees is that ownership cannot cross to a *different* node subtree, not that it is confined to a single node-field value. The distinction matters for multi-component node fields. The text should either:
(a) Clarify that "node boundary" means "node subtree" (addresses whose node field has `pfx(π)` as a prefix), not "addresses with the same node field," or
(b) Restrict O9's domain to `Σ.alloc` (it currently quantifies over `Π × Σ.alloc` but the narrative reads as if it applies universally).

**Recommendation:** Revise the prose surrounding O9 to distinguish between "crossing to a different node subtree" (which O9 prevents) and "spanning multiple node-field values within the same subtree" (which O9 permits for node-level principals). This is a precision issue, not a correctness issue — the formal statement is correct as written.


### Finding 3 — `delegated` relation condition (vi) asymmetry with condition (ii)
**Severity: NOTE**

Condition (ii) of the `delegated` relation checks that the delegator is the most-specific covering principal *for the delegate's prefix*. Condition (vi) checks that no existing principal has a prefix *extending* the delegate's prefix. Together these enforce top-down ordering.

The interaction between (ii) and (vi) is subtle and well-explained in the text. This finding simply notes that (vi) is doing more work than the text acknowledges: it not only prevents out-of-order delegation but also ensures the delegate's O7(a) postcondition is categorical (as noted) *and* prevents a form of "sandwiching" where a new principal is inserted between two existing ones in the prefix chain. The text could note that (vi) prevents both upward and lateral interference, not just the out-of-order case described.


### Finding 4 — O10 existence proof assumes unbounded allocation
**Severity: NOTE**

The O10 existence proof (showing π can always find an address it effectively owns for forking) uses T0a (UnboundedComponents) to find a fresh user-field component value exceeding all existing sub-delegate prefixes. This proof is correct but assumes the allocation mechanism can produce an address with an arbitrary component value.

The text correctly notes that the allocation *mechanism* is out of scope (belonging to the baptism specification). But the existence argument implicitly assumes the baptism mechanism can produce any address satisfying T4 within the principal's domain. If the baptism mechanism has constraints beyond T4 (e.g., sequential allocation, bounded component values), the existence guarantee might not hold in practice. This is not a bug in ASN-0042 — it's a dependency on the baptism specification that could be made explicit.

## Statistics

- Findings: 4
- REVISE: 2
- NOTE: 2

</result>
</tool_result>

## Issue 1: O14 non-nesting clause needs inductive preservation proof
Category: INTERNAL
Reason: The delegation relation's conditions (i), (ii), (vi) and the existing preservation proofs for O1a/O1b/T4 are all present in the ASN. The missing invariant statement and preservation proof can be constructed entirely from these existing definitions — no external evidence needed.

## Issue 2: O9 domain restriction incomplete for node-level principals
Category: INTERNAL
Reason: The formal statement of O9 is correct; the issue is imprecise prose around "node boundary" vs "node subtree." The fix is a clarification derivable from the existing prefix semantics and the O9 proof's own case analysis for `zeros(pfx(π)) = 0`.
