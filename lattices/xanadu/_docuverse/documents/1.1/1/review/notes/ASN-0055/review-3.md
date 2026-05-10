# Review of ASN-0055

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Left cancellation for the order
**Why out of scope**: The open question (does a ⊕ x ≤ a ⊕ y imply x ≤ y?) is a genuine extension. The current ASN establishes equality cancellation; order cancellation would interact with TA1/TA1-strict and belongs in a follow-up.

### Topic 2: Projection/idempotence properties of the action-point equivalence
**Why out of scope**: The observation that TumblerAdd at action point k acts as a projection discarding information below level k is a new algebraic lens. Exploring composition and idempotence is future work, not a gap here.

---

**Assessment notes.**

**TA-LC proof**: Complete. The action-point-agreement argument is case-exhaustive (k₁ < k₂, k₂ < k₁, k₁ = k₂). The "symmetrically" for k₂ < k₁ is genuine — swap x↔y and k₁↔k₂ in an identical structure. Component matching covers all three regions (i < k, i = k, i > k) plus the length argument via the result-length formula. The worked example (a = [2, 5], result [2, 8]) correctly traces the recovery of x = y = [0, 3].

**TA-RC proof**: Valid counterexample. a = [1,3,5], b = [1,3,7], w = [0,2,4] with k = 2. TA0 satisfied for both (2 ≤ 3). The tail-replacement mechanism at position 3 > k correctly erases the difference. Sufficient for an existential claim.

**TA-MTO proof**: Both directions of the biconditional are established component-by-component. Forward: agreement on 1..k makes the three regions of the result identical, with lengths equal (both #w). Converse: at positions i < k, the "copy from start" region forces a_i = b_i; at i = k, natural-number cancellation gives a_k = b_k; positions beyond k carry no information about a or b. The precondition #a ≥ k ∧ #b ≥ k correctly matches TA0 well-definedness.

**Edge cases verified**: k = 1 (action point at first component — no "copy from start" region, biconditional reduces to a₁ = b₁); k = #a = #b (action point at last component — no "copy from displacement" region); #a ≠ #b (result lengths are both #w regardless, so the biconditional holds across different-length starts).

**Consistency with ASN-0034**: All notation (action point, tail replacement, T3, TA0, result-length formula) used directly from ASN-0034 without reinvention. The many-to-one property noted informally in ASN-0034's TumblerAdd definition is now formalized as TA-MTO.

VERDICT: CONVERGED
