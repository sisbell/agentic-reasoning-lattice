# Channel Assignment — ASN-0047 review-64

**Date:** 2026-05-17 00:08

## Issue 1: Foundation S8 precondition cannot be discharged in extended state
Reason: Fix is internal — read ASN-0036's S8 statement and its proof structure to determine whether S3 is substantively required or whether the proof carries through under S3★ (with link-subspace correspondence runs targeting dom(L)). The decision among (a), (b), (c) is a self-contained re-derivation against ASN-0036's named S8 contract.

## Issue 2: K.μ⁻ case analysis routing in case (b) is obscure
Reason: Purely a presentational reorganization of an exhaustive case partition. The case content is already established within the ASN; the fix consolidates the three-way split into a cleaner labeled partition.

## Issue 3: J0 declared axiomatic but missing from axiom catalogue
Reason: Cataloguing fix — the ASN already explicitly states J0's axiomatic status; the fix adds it to the named load-bearing axiom enumeration using existing language.

## Issue 4: Worked-example invariant labels use four-component forms instead of starred forms
Reason: Notation update to use extended-state labels (P4★, Contains_C, J1★, J1'★, S3★) consistent with the section's extended-state scope.

## Issue 5: S4 verification for K.λ is one-line; cross-document disjointness chain not explicitly invoked
Reason: Internal expansion using machinery already established in this ASN — the Cross-document disjointness chain lemma and SubAllocatorAxiom are defined in the *Allocator hierarchy under documents* section and only need to be explicitly cited at the S4 verification site.

## Issue 6: K.δ ghost-base discharge wording understates the gate
Reason: Wording correction to make precise that TA5 supplies the *candidate address* while the *freshness check* is the K.δ precondition against E. Internal to the ASN's own statements about TA5's role.

## Issue 7: D-CTG★ closed-interval definition has implicit dependencies
Reason: Adding a one-line dependency note pointing to S8-depth and S8a, both of which are already named per-state invariants in the same Amendments section.

## Issue 8: ExtendedReachableStateInvariants does not verify P4★ behavior across composite boundary in the interior-replacement worked example
Reason: Adding intermediate-state verification lines using already-established invariants (P4★, Contains_C, K.μ⁻'s frame on R). The fact that K.μ⁻ can only shrink Contains_C is part of P4★'s proof structure in this ASN.

## Issue 9: K.μ~ contract bijection ambiguity under S5 transclusion not addressed
Reason: The contract is naturally an existential over (Σ, Σ') pairs, and the proof's conclusions are π-invariant. Fix is to make the existential quantification explicit and note that the proof works for any witness — derivable from the ASN's contract structure without external consultation.
