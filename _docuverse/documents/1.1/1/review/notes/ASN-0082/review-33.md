# Review of ASN-0082

## REVISE

### Issue 1: Commutativity of ℕ addition invoked without derivation
**ASN-0082, I3-S derivation of (a)**: "δₙ ⊕ ℓ = [0, …, 0, n + ℓₘ] since both operands have all zeros before position m; similarly ℓ ⊕ δₙ = [0, …, 0, ℓₘ + n]. These are equal by commutativity of natural-number addition."
**Problem**: The foundation's NAT-* axioms (NAT-closure, NAT-addcompat, NAT-cancel, NAT-addbound, NAT-addassoc, NAT-zero, NAT-discrete, NAT-order, NAT-sub, NAT-wellorder) do not include commutativity of addition. The ASN's own PositiveOffsetExceeds derivation explicitly notes this absence ("the foundation offers no commutativity-of-+ axiom on ℕ — its NAT-* axioms are stated as independent left/right pairs") and goes to substantial length to derive a + b > b without commutativity. Invoking commutativity here appeals to a property not in scope, while citing it as obvious. This is exactly the "hand-wave disguised as proof" the review should catch.
**Required**: Either derive commutativity as a named lemma from NAT-wellorder + induction (substantial inline proof), record it as a needed foundation extension to ASN-0034, or restructure the postcondition to one whose proof does not require swapping operands of ⊕.

### Issue 2: Same commutativity dependency in D-S(a)
**ASN-0082, D-S(a)**: "σ(reach(σₛ)) = … = [1, s₂ + c' − c]" versus "reach(σ'ₛ) = … = [1, s₂ + c' − c]", obtained by rewriting [1, (s₂ − c) + c'] as [1, s₂ + c' − c].
**Problem**: σ(reach(σₛ)) computed via TumblerSub gives [1, (s₂ + c') − c]; reach(σ'ₛ) computed via TumblerAdd gives [1, (s₂ − c) + c']. Equality requires (s₂ + c') − c = (s₂ − c) + c' on ℕ, which (chasing through the foundation: NAT-addassoc, NAT-sub right-inverse, NAT-cancel) hits an unavoidable commutativity step c' + c = c + c'. The proof asserts both forms are equal to "s₂ + c' − c" without showing the bridging identity.
**Required**: Same remediation as Issue 1.

### Issue 3: I3-S(b) and D-S(b) route through commutativity unnecessarily
**ASN-0082, I3-S(b) derivation**: "differ at position m by (sₘ + ℓₘ + n) − (sₘ + n) = ℓₘ"
**ASN-0082, D-S(b) derivation**: "differ at position 2 by (s₂ + c' − c) − (s₂ − c) = c'"
**Problem**: Both (b) clauses can be proved directly from the action-point components of reach(σ') and start(σ') using NAT-sub left-telescoping `(n + m) − n = m`: width at position m equals `((sₘ + n) + ℓₘ) − (sₘ + n) = ℓₘ` (instantiating n_arg = sₘ + n, m_arg = ℓₘ). The current proofs route through the commutativity-laden form from (a) when a direct route exists.
**Required**: Restructure both (b) proofs to compute width at the action-point position directly via NAT-sub left-telescoping, without invoking (a) or the rewritten form.

### Issue 4: TS4 citation name does not match foundation
**ASN-0082, I3-S2 wp analysis (and elsewhere)**: "Discharged by TS4 (ShiftStrictlyAdvances, ASN-0034)"
**Problem**: The foundation registers this lemma as TS4 — ShiftStrictIncrease. The ASN's text uses "ShiftStrictlyAdvances", a name not in the foundation.
**Required**: Replace all occurrences of "ShiftStrictlyAdvances" with "ShiftStrictIncrease".

### Issue 5: D-MIN-post step is implicit
**ASN-0082, D-MIN-post proof, Case L ≠ ∅**: "Since p > min(V_1(d)), we have min(V_1(d)) ∈ L."
**Problem**: The premise "p > min(V_1(d))" is neither a precondition nor derived in the preceding text. It follows from L ≠ ∅, but the inference is not shown.
**Required**: Insert: "L ≠ ∅ supplies some v ∈ V_1(d) with v < p, so min(V_1(d)) ≤ v < p; hence min(V_1(d)) ∈ L."

### Issue 6: Worked examples for I3 cover only S = 1
**ASN-0082, worked examples for post-insertion shift**: All concrete scenarios use S = subspace(p) = 1 (text), including the "cross-subspace preservation" example which inserts into text and verifies the link side is unchanged.
**Problem**: I3 is stated generally for any S ≥ 1. The contract claims handle subspace-2 (link) insertion via the same machinery, but no worked example exercises the case where the shifted region is itself the link subspace and S8a-shaped well-formedness has to survive at a sparse, tombstone-bearing pre-state V_2(d). Given that I3-VV's wp derivation depends on S8a but not on D-CTG, the lemma should be exercised against a pre-state that lacks D-CTG.
**Required**: Add one worked example exercising I3 with S = 2 (or explicit prose noting that the generality of I3 over S has been verified by the lemmas and an example would add no further coverage).

## OUT_OF_SCOPE

### Topic 1: Link endset behavior under shifted text content
**Why out of scope**: The ASN's prose notes that links attach to I-addresses, so shifting V-positions leaves link endsets invariant. Formal treatment of link endset shape, MAKELINK/BREAKLINK, and their interaction with the shift sub-operations belongs to a future link-subspace ASN.

### Topic 2: Composing INSERT (shift sub-operation + content allocation)
**Why out of scope**: The ASN is explicit that I3 specifies only the shift sub-operation, deferring the full INSERT (which extends dom(C) and fills the gap positions) to a future ASN. The S0-to-I3-C weakening note correctly anchors the composition.

### Topic 3: Generalizing the contraction to depth > 2
**Why out of scope**: The "Necessity from TA4" argument and the Open Questions section together capture this as future work. Resolving it requires either a strengthened TA4 in the foundation or a separate derivation of the partial-inverse identity from primitives, both of which are out of scope here.

### Topic 4: Formal tombstoning semantics in the link subspace
**Why out of scope**: The worked example uses "tombstone gap" colloquially for missing V-positions in V_2(d). A formal distinction between never-allocated, currently-mapped, and explicitly-tombstoned positions belongs to a future link-mutation ASN.

VERDICT: REVISE
