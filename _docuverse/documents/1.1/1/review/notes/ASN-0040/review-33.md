# Review of ASN-0040

## REVISE

(none — see below)

## OUT_OF_SCOPE

(none — the Scope section and Open Questions correctly partition deferred concerns)

VERDICT: CONVERGED

---

After working through this ASN with care, I find no REVISE items. A few observations on why this clears the bar:

**Proof completeness.** Every claim has a proof or is explicitly labelled as a design requirement / forward requirement. The joint-induction frame (Bop ↔ {B1, B10, B_fin, B_type}) is named, the dependency order is made explicit (B_fin standalone; B_type needs B_fin; B10 needs B_fin and B_type; B1 needs B10 and B7), and forward references inside step arguments are explicitly tied back to the joint hypothesis rather than to as-yet-unproven theorems.

**Case enumeration.** B1's "other namespaces" case splits exhaustively into B6-valid (A), B6-invalid with entire-stream T4-violation (B), and B6-invalid with stream identity collapse (C); each propagation mechanism inside (B) — leading zero, interior adjacency, B6(iii) failure, d ≥ 3, trailing-zero-with-d=2 — is named with its TA5 mechanism. B6 necessity sub-case (b) at d = 1 explicitly constructs p' and verifies S(p, 1) = S(p', 2) by first-element component comparison plus deterministic recurrence, rather than asserting coincidence.

**Boundary cases.** Empty children (next Case 1), singleton seed, the singleton p = [0] coincidence of leading/trailing positions, m = 0 vs m ≥ 1, d = 1 vs d = 2, B7 Cases 1/2/3, and M = 0 in B9 are all explicitly handled. The worked trace (Steps 1–7) verifies B7 Cases 1, 2, and 3 against concrete addresses and witnesses B9 by construction.

**Derived consequences.** Bop's monotonicity is derived as B0 and then promoted to multi-step B0★; B1's contiguity is reduced to scalar hwm via B2; B7 partition + B1 contiguity composes into B8. The wp analysis identifies non-trivial dependencies for B1, freshness, and B10 rather than reducing to "hwm = N+1 needs hwm = N".

**Cross-ASN discipline.** Only foundation ASN-0034 is cited (T0(a), T1, T3, T4, T5, T8, T9, T10, T10a, TA5, TA5a, AllocatedSet, GlobalUniqueness). Bridge1 and Bridge2 are properly labelled as forward requirements on the activation-discipline ASN, with Bridge1's uniqueness clause proved from B7 directly.

The ASN defines state (Σ.B), operation (Bop), and invariants (B0–B10, B_fin, B_type) at the right level of abstraction — implementation-neutral, alternative-realization-admitting. No drift toward implementation mechanics.
