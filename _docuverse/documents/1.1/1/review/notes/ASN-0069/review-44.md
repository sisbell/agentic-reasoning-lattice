# Review of ASN-0069

I've worked through V0–V12, the elementary decomposition verification, and the worked example with particular attention to the induction structures, frame-composition arguments, and edge case handling.

## REVISE

[No items]

## OUT_OF_SCOPE

[No items — the Open Questions list adequately handles deferred topics: concurrent forks, fork discoverability, snapshot vs. living forks, transcludent sources, fork-of-empty intermediates, V-stream depth differences, and fork-plus-deletion interactions.]

---

The ASN meets the rigor standards:

- **Inductions are explicit.** V1's IsDocument and parent-equality inductions on `A_v(d_src)`'s emission count have explicit base and inductive steps, with the inductive step's discharge of `d_prev ∈ E_doc` via P1 stated. V2's prefix-relation induction includes the nested length-induction. V11's chain induction handles `k = 1` base via V4 + V5 and `k ≥ 2` step via IH + premise + V4, with the Stage 1 / Stage 2 decomposition making the membership transfer through the premise explicit.

- **Sub-case discharges are complete.** The K.δ verification covers both sub-case A (k=1, first fork) and sub-case B (k=0, subsequent fork). Sub-case A's freshness uses T10a at-most-once at `(d_src, 1)` plus T10a.6. Sub-case B's freshness uses three independent steps (T10a.7 within-allocator + Sequential+P1 frontier-advancement + T10a.6 cross-allocator). Both outer-preconditions, uniform precondition, per-sub-case preconditions, and the IsDocument derivation are discharged.

- **Frame compositions are traced.** V3 (C invariance), V5 (source isolation), and the R' set equality each compose the elementary frames of K.δ, K.μ⁺, K.ρ across the composite, with sub-state notation `Σ^{(j)}` typographically distinct from V10/V11's `Σ^k`.

- **Edge cases covered.** Empty-source via V7's K.δ-alone composite, with the empty K.δ-alone ValidComposite★ verification supplied separately. First fork vs. subsequent fork via V1 sub-cases. Sibling forks via V10 (with V5a Corollary 2 instantiation explicit). Fork chains via V11. The worked example walks through 3-position content, link-bearing source, subsequent edits, fork-of-fork, sibling fork (showing the k=0 mechanics with the `d_new² = inc(d_new, 0)` length-and-component check), empty source (V7 with both `V_{s_L}(d_src) = ∅` and `V_{s_L}(d_src) ≠ ∅` variants).

- **Design commitments are honest.** V4 and V4b are explicitly labelled as design commitments not derivable from J4 alone, with structural justifications for the literal-inheritance form and an explicit acknowledgement that alternative ASNs could weaken V4 with strengthened correspondence machinery.

- **Foundation use is precise.** Each appeal cites a specific foundation lemma (TA5(b)/(c)/(d), KDeltaZerosK01, KDeltaParentK01, T10a.4, T10a.6, T10a.7, P0–P2, P4★, P8, J1★/J1'★, S3★, S8a, S8-depth, D-CTG★/D-MIN★/D-SEQ★, CL-OWN, etc.). The Dependency Audit correctly identifies ASN-0040 as unused and flags it for removal.

- **Transitivity of `≼` is proved locally in V11a** rather than cited — appropriate since ASN-0034's Prefix entry does not state transitivity as a postcondition.

VERDICT: CONVERGED
