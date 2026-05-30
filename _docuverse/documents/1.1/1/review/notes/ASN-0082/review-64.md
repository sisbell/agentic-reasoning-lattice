# Review of ASN-0082

## REVISE

### Issue 1: Foundation lemmas mis-attributed to ASN-0036 in S7-post

**ASN-0082, S7-post (AllocationInvariantsPreservation)**: "S7 follows as a corollary since its remaining dependencies — the foundation lemmas T4, T4a, T4b, T0, T10a, T10a.4 (ASN-0036) — are state-independent."

**Problem**: T4, T4a, T4b, T0, T10a, T10a.4 are ASN-0034 claims, not ASN-0036. ASN-0036's own statement of S7 correctly cites them as "(ASN-0034)". The parenthetical "(ASN-0036)" attached to this list is a factual mis-citation — a reader verifying the foundation provenance of these lemmas is misdirected to the wrong source ASN. (I3-S7 lists the same set without a wrong attachment, so the error is localized to S7-post, but the two passages should agree.)

**Required**: Correct the attribution to ASN-0034 for T4, T4a, T4b, T0, T10a, T10a.4 (S7a, S7b, S7d remain ASN-0036).

### Issue 2: NAT-CA posited as a local axiom rather than cited from the foundation

**ASN-0082, Span Width Preservation**: "NAT-CA — *CarrierAdditionCommutativityAssociativity* (introduced locally). For all m, n, k ∈ ℕ: `m + n = n + m` (commutativity) and `(m + n) + k = m + (n + k)` (associativity)."

**Problem**: Commutativity and associativity of ℕ addition are substrate arithmetic facts, not properties of system state, operations, or invariants. The foundation (ASN-0034) deliberately separates ℕ facts into individually citable axioms — T0 states this convention explicitly ("The standard arithmetic facts about ℕ that proofs need are separated into their own axioms so each proof cites only what it actually uses"), and the NAT-* family (NAT-addcompat, NAT-closure, NAT-discrete, NAT-order, NAT-wellorder) realizes it. NAT-CA is exactly such a fact and belongs in that family. Positing it as a local axiom in an operational projection ASN inverts the layering: NAT-CA is load-bearing in I3-S(a) (n + ℓₘ = ℓₘ + n) and D-S(a) (the regrouping step), so it is genuinely consumed, but it should be a foundation citation, not a fresh axiom asserted here.

**Required**: Cite a foundation NAT axiom for ℕ commutativity/associativity rather than introducing NAT-CA locally. (If the foundation NAT-* family genuinely lacks these, extending the foundation is the fix — see OUT_OF_SCOPE — but ASN-0082 must not be the site that posits a universal ℕ axiom.)

## OUT_OF_SCOPE

### Topic 1: Foundation NAT-* family lacks commutativity/associativity of ℕ addition

**Why out of scope**: The extracted NAT-* axioms of ASN-0034 omit `m + n = n + m` and `(m + n) + k = m + (n + k)`. Supplying them is a correction to the foundation, not to this ASN. ASN-0082 should cite them once they exist.

### Topic 2: Contraction at ordinal depth greater than one

**Why out of scope**: The contraction operation is scoped to `#p = 2`, and the Open Questions correctly identify the TA4-zero-prefix / S8a-positivity collision at intermediate components as the obstruction. Generalizing the gap-closure and dense-partition results to deeper ordinals is new territory for a future ASN, not a defect here. The insertion half (I3) already handles general `m ≥ 2`; the asymmetry is openly acknowledged.

### Topic 3: Non-ordinal-level spans in I3-S / D-S

**Why out of scope**: Both span lemmas require `actionPoint(ℓ) = m` (width acting purely at the deepest component). Spans whose width acts at a higher component are not covered, but the precondition is stated explicitly, so this is a deliberate scoping rather than a gap — generalizing it belongs to a future span-algebra extension.

VERDICT: REVISE
