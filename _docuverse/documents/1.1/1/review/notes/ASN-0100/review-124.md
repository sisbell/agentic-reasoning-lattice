# Review of ASN-0100

I checked the substrate decomposition, each invariant-preservation argument, the boundary cases (empty document, append `j=N`, prepend `j=0`, deep-subspace `m_C=3`, re-insertion into a cleared subspace), the wp analyses, and the atomicity/uniqueness treatment against the foundation contracts.

## Findings

**Allocation & freshness (INS.alloc).** The per-firing freshness against the *immediately preceding* state (SubsequentEmissionFreshness / FirstEmissionFreshness), and the content-store-keyed branch selection, are correctly distinguished from the arrangement state. The re-insertion example correctly exhibits chain-index/V-position decoupling.

**K.μ⁻ firing condition (INS.μ⁻-fires).** The "fires iff Right ≠ ∅" rule, the strict-contraction discharge (`n'_{s_C}=p_m−1 < n_{s_C}` when `Right≠∅`), and the forced K.μ⁻-before-K.μ⁺ ordering (image-preservation precondition would be violated at `p`) are all sound. Omission in append/empty cases correctly yields `Right=∅`.

**Sequential invariants (INS.inv.seq).** The closed-interval reduction handles the live `m≥3` off-prefix exclusion rigorously (T1 case (i) at the first off-prefix divergence), and the arbitrary-pair → extreme-pair reduction via T1 least/greatest elements is correct. Region last-components `{1..p_m−1} ∪ {p_m..p_m+n−1} ∪ {p_m+n..N+n}` tile `{1..N+n}` with no gap/overlap.

**Functionality / exhaustiveness (INS.M-exhaustive).** Pairwise region disjointness is correctly grounded on the shared-prefix reduction (so last-component comparison is sound), and exhaustiveness is established from the composite construction (K.α/K.ρ frame M, K.μ⁻ only removes, K.μ⁺ adds exactly the two specified sets).

**S8★(c) uniqueness.** Correctly routed through C1a's general single-subspace restriction form (not only the `⟦σ⟧` corollary), with the three preconditions discharged via INS.C1a-app.

**Atomicity.** Per-state vs. composite-boundary class separation is respected: P7a/P4★/P4a need not hold at the unarranged-content K.α intermediate; the post-K.μ⁻ contraction intermediate gets an independent invariant discharge rather than relying on I3. J0/J1★/J1'★ are correctly evaluated only at the boundary, with J1★'s range-based semantics correctly excluding Shifted-right addresses.

**Depth & consequences.** Multiple concrete examples, two non-trivial wp derivations (tight-endset discoverability collapse; provenance-membership chain predicate), and derived consequences (INS.identity.crossdoc, projection-shift correspondence) are all present and explicit.

The four cross-references to the consolidated S7-bullet discharge reflect the deliberate consolidation in recent revisions (discharge-once, reference-many), not accretion; I decline to flag them. The brief cross-document/coverage preview sentences in §Verifying the Invariants are minor and within acceptable cross-section consistency, not paragraph-level meta-prose.

No cross-ASN references outside the foundation set. No drift into implementation mechanics. I found no skipped case, hand-waved conjunct, or underived "derived" claim.

VERDICT: CONVERGED
