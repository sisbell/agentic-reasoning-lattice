# Review of ASN-0100

I reviewed the INSERT specification for correctness of every proof, completeness of edge cases, every conjunct of each invariant in ExtendedReachableStateInvariants (ASN-0047), and — given the `review-mode.anti-bloat` classifier — for accreted meta-prose around forward references.

## Correctness checks performed

- **Region disjointness (S2).** All three pairwise disjointnesses (Left∩Insertion, Insertion∩Shifted-right, Left∩Shifted-right) are shown via last-component arithmetic, with the shared-prefix justification (D-SEQ★/D-CTG-depth) correctly established before the last-component comparison is invoked. INS.M-exhaustive rules out a fourth region. Sound.
- **Closed-interval reduction (D-CTG★).** The off-prefix exclusion for `m ≥ 3` (the live case) is proved by T1 case (i) at the first interior divergence; the arbitrary-pair-to-extremes reduction is valid; the `m = 2` degenerate case is correctly dispatched.
- **Projection-shift correspondence (INS.proj).** The step-by-step tracking through K.α (LP6), K.μ⁻ (LP10), K.μ⁺ (LP9), K.ρ (LP14) is arithmetically correct; the K.μ⁻-omitted branch collapses to the same expression via (INS.μ⁻-fires); `ran(M'(d)) = ran(M(d)) ∪ {a_k}` holds.
- **Boundary cases.** Prepend (`j=0`, forced full clearance), append (`j=N`, K.μ⁻ omitted), empty-document first insertion (first-emission branch), re-insertion into cleared subspace with residual content (subsequent-emission branch, V-index/chain-index decoupling), and deep subspace (`m_C=3`) are each worked concretely and check out.
- **All invariant conjuncts.** Every per-state invariant in ExtendedReachableStateInvariants is discharged at each intermediate (frame-preservation grouped by component; per-address discharge for fresh `a_k`); composite-boundary P4★/P4a/P7a and couplings J0/J1★/J1'★ at the boundary; P3 as the P0∧P1∧P2∧L12 synthesis. The Shifted-right/J1★ range-based non-trigger and the P4a witness-at-Σ' arguments are correct.
- **Foundation usage.** All cross-references are to foundation ASNs (0034, 0036, 0047, 0058, 0082, 0093, 0098); no non-foundation references; no reinvented notation. Standard 7 satisfied.
- **wp analysis.** Both the discoverability wp (non-trivial, tight-endset collapse via INS.proj) and the provenance-membership wp (chain-index decidability) are genuine, not trivial.

## Anti-bloat pass

I checked for the flagged accretion patterns: imagined-excluded cases, relocated prior-finding content, why-an-axiom prose, compounding forward-deferrals, document-ordering justifications, consumer-enumeration in definitions, and twinned paragraphs. The branch-selection nuance appears in Effect One prose, a parenthetical, and a dedicated worked example, but the example is concrete demonstration (explicitly not meta-prose) and the prose states the principle it demonstrates — defensible at review-50. The repeated back-references to the "S7 bullet" are single-discharge-and-cite factoring that aids cold reading, not compounding deferral. No paragraph requires the precise reader to work around non-advancing prose.

No correctness defects, missing edge cases, hand-waves, or REVISE-worthy bloat found.

VERDICT: CONVERGED
