# Review of ASN-0082

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Contraction generalization to ordinal depth > 1
The scoping axiom (#p = 2) restricts the contraction proofs to single-component ordinals, where TA4's zero-prefix condition is vacuously satisfied. At ordinal depth 2 (m = 3), the round-trip (ord(p) ⊕ w\_ord) ⊖ w\_ord ≠ ord(p) because TumblerSub finds the divergence at position 1 (where ord(p)₁ > 0 = (w\_ord)₁) and copies the tail from the minuend rather than reversing the addition — confirmed by concrete counterexample: [1, j+c] ⊖ [0, c] = [1, j+c] ≠ [1, j]. The ASN correctly identifies this in its open questions. A deeper treatment would need ordinal-level subtraction defined independently of TumblerSub.
**Why out of scope**: Requires new algebraic machinery (ordinal-level inverse operations) beyond what the current foundation provides.

### Topic 2: Correspondence-run preservation under shift
I3 establishes point-level mapping preservation; I3-S establishes span-level width preservation. The bridge property — that a pre-state correspondence run (v, a, n\_run) becomes a post-state run (shift(v, n), a, n\_run) — combines I3 with the S8 correspondence-run definition from ASN-0036 and belongs in the INSERT operation ASN.
**Why out of scope**: This is a composition result, not a gap in the displacement algebra.

### Topic 3: Promotion of "ordinal-level" to span algebra
The concept of an ordinal-level span (actionPoint(ℓ) = m) is a natural subclass of level-uniform spans that may warrant promotion to ASN-0053 if downstream ASNs need it. Currently correctly scoped as a local definition.
**Why out of scope**: No downstream consumer yet; promotion is a future editorial decision.

VERDICT: CONVERGED
