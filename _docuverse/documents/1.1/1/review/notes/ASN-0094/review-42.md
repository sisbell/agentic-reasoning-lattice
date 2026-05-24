# Review of ASN-0094

## REVISE

(none)

## OUT_OF_SCOPE

(none)

The ASN is comprehensive and well-structured. I worked through the major claims systematically:

**Proofs checked in detail:**
- AllocatedAddressAntichain — Cases 1, 2, 3a, 3b. Sub-case 3b's "by symmetry" is justified by the explicit case-symmetry paragraph that documents how Steps 3.1, 3.2 are domain-agnostic while only Step 3.3 swaps subspace identifiers. Worked example provided.
- LinkAddressNotPrefixOfEmit — Case I (same-home via uniform chain length + T10a.7 + T3) and Case II (cross-home with Sub-cases II.A equal-length and II.B strict via Steps II.0–II.3). Concrete and counterfactual examples both provided.
- Sh0–Sh3 — induction on ↦* with explicit Case A (unchanged) and Case B (extension) coverage. Stratification (Sh0/Sh1 independent → Sh2/Sh3 consume them) is acyclic.
- Sh4 — Cases A/B/C/D covered. Case D's `|leaving| ≤ 1` derivation from R0a + R1 + PrefixSpanCoverage is sound. Subset-closure derivation explicit.
- EffectiveWpSimplification — Step 1 (NoCraftedSpanReachesD via Sh1/Sh3 at K:=R + Lemma) and Step 2 (case split K≁R vs K~R) discharge wp_086 conjuncts.
- Per-K discipline preservation (FDD, single-home) — independent inductions, Case D excluded by shape-tuple structure for FDD.

**Worked examples** exercise every canonical shape with admission cases, rejection cases (4 in Comment, including the unregistered-type case), and template evaluation. Empty-baseline behavior at `latest_K_for_addr` is exhibited. Sh4 suppression, FDD subsumption, and single-home rejection are all walked at concrete addresses.

**Foundation use** is consistent — `addr`, `home`, `coverage`, `nullified`, `A_K^Σ`, `L_K^Σ` used per their ASN-0034/0043/0086 definitions; no reinvention.

**Scope commitments** are honest: single-process substrate (acknowledged), manual catalog extension (Sh5 META status), no closure theorem for composites (hedged in Consequences).

VERDICT: CONVERGED
