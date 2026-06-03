# Review of ASN-0091

I read the full ASN and checked the abstract Vstream-only class, its realization by REARRANGE_K, every RE-* derivation, the invariant discharges, and all four worked examples.

## Verification performed

**Bijection characterization (the forward/reverse biconditional).** The four sub-inferences (a)–(d) for the forward direction and the pointwise reconstruction for the reverse are both correct; the within-block freedom is correctly localized to non-singleton pre-image sets, and the fourth worked example concretely exhibits two distinct witnesses π₁, π₂ with `π(project) = project'` invariant across both.

**Circularity avoidance.** The two places where a cycle could arise are both correctly broken: (i) RA-dom is sourced directly from ASN-0084's PivotPostcondition/SwapPostcondition domain clause, *not* K.μ~-FIX, and clause-(iii) length preservation is discharged from CS4 + ordinal-shift length identity alone; (ii) the REARRANGE_K S3★ discharge uses the constructive fact (b), not RE-subpres/RA-adm. The Remark deriving RA-dom from bijection+admissibility is consistent (RE-subpres needs only RA-π's codomain signature, not RA-dom).

**RA-adm completeness.** I cross-checked every per-state invariant in ASN-0047's ExtendedReachableStateInvariants (S2, S3★, S3★-aux, S4, S7a/b/d, C1b/c, S8a, S8-fin, S8-depth, S8★, C-fin, D-CTG★/D-MIN★/D-SEQ★, P6/7/8, NodeLineage, ActivatedEmission, L0–L14, CL-OWN/UNIQ) plus M0/M1 and the three composite-boundary properties (P4★, P4a, P7a) — each is discharged, and the S5/T0 exclusions from RA-adm are correctly handled as state-independent theorems.

**Collapse-case characterization.** I verified the swap criterion independently: w_α=1,w_μ=1,w_β=2 forces value-uniformity, and w_α=w_β=2 yields α/β positional equality with free μ. The dichotomy `M'(d)≠M(d)` vs `M'(d)=M(d)` (the only load-bearing distinction) is precise; the gcd/swap-cycle analysis is supplementary and not relied on by any RE-* proof.

**Edge cases.** Empty arrangement (admitted abstractly, excluded for REARRANGE_K via R-PRE(iv)+CS2), identity case, exterior cuts (RE-ext exercised in trace 3), shared I-addresses (trace 4), and the multi-step (+,−) composition (trace 2, with RE-ext bridging verified) are all covered with correct cardinality counts and R-PRE(iv) discharge (including the unpopulated exclusive upper bound c_{n−1}).

**ChainDisjointAdjacency** correctly invokes T3 and handles the proper-prefix length case. Cross-ASN references are all to foundation ASNs (0034, 0036, 0047, 0084, 0093, 0098) and thus permitted. Open questions are correctly scoped to future territory (link-subspace semantics, transclusion-split guarantees, run-cardinality bounds).

I found no hand-waved multi-case proof, no skipped invariant conjunct, no missing boundary case, and no load-bearing gap. The depth requirements (derived consequences, concrete examples, witness-uniformity analysis) are met.

VERDICT: CONVERGED
