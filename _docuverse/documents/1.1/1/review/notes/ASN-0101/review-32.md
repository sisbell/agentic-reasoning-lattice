# Review of ASN-0101

I checked the operation specification (D0), gap-closure (D1), the seven preservation/derived claims (D2–D8), the projection characterisation (D9), the ValidComposite★/LP-family extension (D10), and the weakest-precondition analysis (D11), together with all three worked examples and the boundary-case enumeration.

## REVISE

I was unable to identify a sound REVISE item. The specific things I verified:

- **D0 reduction of the containment precondition** — the middle-component argument (`v_j = 1` for `2 ≤ j ≤ m_S − 1`) is handled at both the `m_S = 2` vacuous base and the `m_S ≥ 3` least-divergence induction, ruling out `v_{j₀} = 0` and `v_{j₀} ≥ 2` separately. Correct.
- **D1 gap closure** — order-preservation (TS1), injectivity (via trichotomy), surjectivity (construction), and well-definedness of `σ_d` (TS2 + length preservation, with `k − n ≥ p ≥ 1` keeping components positive) all check out; `Λ ∪ Q = {[S,1,…,1,k] : 1 ≤ k ≤ n_S − n}` is genuinely contiguous from 1 because `Λ` covers `1..p−1` and `Q` covers `p..n_S−n`.
- **D8** — the invariant catalogue is complete against ASN-0047's ExtendedReachableStateInvariants (incl. the composite-boundary P4★/P4a/P7a); the source-correspondence route for S3★/S3★-aux/CL-OWN/CL-UNIQ correctly handles the `Q ∩ X` re-mapping case; S8★ condition (c) is split correctly (M12 when `S = s_C`, D6 inheritance when `S = s_L`); the P4★ inclusion chain is traced step-by-step rather than asserted.
- **Boundary cases** — empty post-state, deletion-at-start (the one non-vacuous D-MIN★ `σ_d`-witness case), deletion-at-end (`Π = ∅`), singleton subspace, singleton interior, non-singleton interior — each is routed through the correct discharge mechanism without "by similarity."
- **D11** — the discoverability wp reduction (`project ⊄ X` from `project ∩ (dom(M(d)) \ X)`), the cardinality wp (inclusion-exclusion across the `Λ ⊎ X ⊎ Π` partition), the cross-document bullets, and the partial-deterministic negation equivalence are all correct, with the `enabled(·)` guard carried uniformly.
- **Worked examples** — the content (depth 3), link (depth 2, exercising CL-OWN/CL-UNIQ), and cross-document transclusion examples each compute consistently and exercise distinct invariant routes.

The one apparent vocabulary inconsistency (K.σ in the body list vs. D10) does not exist in the current text — the body's list at "The operation" already reads the nine-entry `{…, K.ρ, K.σ}`, matching D10's pre-DEL extension target. This matches the two previously declined findings and is not resurfaced.

## OUT_OF_SCOPE

None. The references to INSERT (as the ASN-0082 contraction generalisation), versioning (K.δ depth-1 / J4 ForkComposite), and the recoverability mechanism are framed as cross-references and open questions, not as in-scope claims about those operations' mechanics. The "Open Questions" correctly defer reversibility, causal ordering, and full historical reconstruction to future ASNs.

VERDICT: CONVERGED
