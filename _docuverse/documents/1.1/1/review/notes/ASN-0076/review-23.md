# Review of ASN-0076

## REVISE

(None — proofs are detailed and rigorous, foundation citations are correct, edge cases are handled, and explicit deferrals are appropriately marked.)

## OUT_OF_SCOPE

### Topic 1: Supersession-type address registry
**Why out of scope**: Open Question 2 defers `τ_sup` semantic designation to a future ASN on type-endset conventions. The current ASN supplies structural witnesses (E4, E7) without model-level identification of "supersession-type" addresses; the Appendix's Step 2 gap (filter-by-supersession-type) flags exactly this hole.

### Topic 2: Supersession-chain termination and cycles
**Why out of scope**: Open Questions 1 and 4. The Appendix's Step 4 (recursion) explicitly admits there is no termination story and that cycles are admissible under the current model. Acyclicity invariants and well-founded reader procedures belong to a future ASN.

### Topic 3: Multi-link supersession (arity > 3)
**Why out of scope**: Open Question 5 — whether supersession may relate more than two links jointly (split, merge). The current ASN fixes arity 3 by convention; generalization is a future ASN's responsibility.

### Topic 4: Authorization layer
**Why out of scope**: E6's "informal motivation" paragraph explicitly defers authorization (who may fire K.λ on which document) to a future ASN. The abstract K.λ has no executor field, so this concern lies entirely outside the present ASN's vocabulary.

### Topic 5: Counter-claims, retractions, discovery, content coordination
**Why out of scope**: Open Questions 3, 6, 7. Formalization of counter-claims/retractions, edited-link interaction with discovery operations, and edit-to-content coordination are all flagged as deferred. The Appendix is honest about being illustrative-only on the discovery side.

### Topic 6: Notification mechanisms
**Why out of scope**: E10 establishes structurally that no notification reaches the original owner (frame of K.λ precludes touching `home(ℓ_old)`'s arrangement). Whether a separate notification primitive is desired is a future-ASN question; the current ASN correctly establishes its absence.

VERDICT: CONVERGED
