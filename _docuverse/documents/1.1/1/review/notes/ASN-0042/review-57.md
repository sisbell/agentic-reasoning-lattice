# Review of ASN-0042

## REVISE

(No REVISE items found.)

After thorough review of the proofs of O0 through O10 plus the auxiliary state axioms O12–O18 and derived properties (SelfOwnershipAtPrefix, OwnershipDomainPermanence, FiniteRegistry, NestingByDelegation, PrefixBaptismCoupling, DelegatorAllocatesPrefix, AccountPrefix):

- **Case analyses are exhaustive.** O2 (Steps 1–4 for non-emptiness, total ordering, finiteness, uniqueness), O6 (cases on `zeros(pfx(π)) ∈ {0,1}` with sub-cases on `zeros(a)`), O9 (cases on `zeros(pfx(π))`), and AccountField/AccountPrefix (cases on `zeros(a) ∈ {0,1,2,3}`) all dispatch every reachable configuration.

- **Boundary cases are addressed.** O10's `hwm_0 = 0` field-opening branch is exhibited concretely via the `π_B` delegation in the worked example; the `hwm_0 > 0` sibling-advance branch via the running `π_A` trajectory. Single-bootstrap-principal vs. multi-bootstrap configurations are handled (worked example uses two-node `Π₀`; O7(c) chain construction works in both).

- **The PrefixBaptismCoupling argument in O10 is tight.** Form A excluded by component-value comparison; Form B at length > `#pfx(π)+2` excluded by length; Form B at length `#pfx(π)+2` excluded by PrefixBaptismCoupling + ASN-0040 B1. The non-`π` covering analysis closes via the covering-chain lemma.

- **O8's trajectory-passes-through-`Σ_d^post` argument is rigorous.** Uniqueness of introduction event (O15 + O12 + condition (iii)) combined with reachability-grounded `Π₀ ⊆ Π_Σ` excludes the bootstrap case.

- **The worked example verifies every property concretely** — O0/O1/O1a/O1b/O2/O3/O4/O6/O7/O8/O9/O10, plus SelfOwnershipAtPrefix, the field-opening boundary case, namespace-vs-delegation mutual exclusion, and cross-node O9.

- **Cross-ASN references are limited to foundation ASNs** (ASN-0034 and ASN-0040, both supplied as foundation in this review). No ASN-0042-internal references reach beyond foundations.

- **Depth is met.** Each derived property has a proof with named dependencies. Derived corollaries (O3 monotonic refinement, OwnershipDomainPermanence★ multi-step, first-delegator form) are explicit. The worked example's Fork section verifies O10 against two distinct trajectories (sibling-advance via `π_A`, field-opening via `π_B`).

## OUT_OF_SCOPE

(No OUT_OF_SCOPE items found. The ASN's Scope section explicitly enumerates excluded topics — modification rights, publication, custodial relationships, document lifecycle, content storage, operations, links, baptism mechanism, enfilade internals, replication, concrete authentication — and the body respects these boundaries.)

VERDICT: CONVERGED
