# Review of ASN-0045

I checked each derivation against the foundation contracts (T4, T4b, T4c, T0, and the NAT-* axioms), verified case coverage on both the valid and invalid subdomains, and confirmed the dependency chains.

## REVISE

None.

## Findings (verified, no action required)

**At-least-one is genuinely proved, not asserted.** The derivation refuses the circular shortcut of reading `zeros(t) ∈ {0,1,2,3}` off T4c's bijection domain. It instead bounds `n` by `0 ≤ n ≤ 3` (T4-valid's own `zeros(t) ≤ 3` conjunct plus T0's `n ∈ ℕ`) and then exhausts the segment with NAT-discrete (interior gaps vacuous), NAT-addcompat (`k < k+1` makes the numerals consecutive), and NAT-order (trichotomy at each boundary). Each of the three interior gaps is discharged by the same schema; this is the correct, non-hand-waved structure.

**At-most-one routes through the right premises.** Disjointness rests only on the single-valuedness of `zeros(t)` (T4) and the pairwise distinctness of 0,1,2,3 in ℕ (NAT-addcompat chain + NAT-order trichotomy/irreflexivity). The ASN correctly notes that T4c's *injectivity over levels* does no work here, since the four predicates compare zero-counts, not labels. The recent reroute of distinctness from T0 to the NAT axioms is consistent throughout.

**Boundary/edge coverage is complete.** Single-component `[7]` (Node), the three field-segment violations (leading/trailing/adjacent zero), and the bound violation `zeros = 4` are all exhibited. Partition covers the T4-valid subdomain; Off-Domain Vacuity covers `¬T4-valid` by conjunction elimination on the shared left conjunct. Together they tile all of T (exactly-one on-domain, exactly-zero off-domain).

**Level-correspondence applicability is discharged, not assumed.** T4c's preconditions (T4 positional constraints + T4b) are met at `t` via T4-valid(t) for the constraints and universal T3 + those constraints for T4b. The biconditional chaining is explicit.

**T4c-as-nomenclature-only is correctly argued.** Partition's exactly-one-of is a relation among zeros-count equalities; T4c contributes labels for reporting, not proof content. The separation is sound and the coining of `T4-valid` (T4 introduces no one-place predicate) does not reinvent foundation notation.

VERDICT: CONVERGED
