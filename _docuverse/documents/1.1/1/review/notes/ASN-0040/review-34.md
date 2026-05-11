# Review of ASN-0040

## REVISE

None.

## OUT_OF_SCOPE

None.

This revision is clean. Key observations:

- **State-space framework.** The Kripke-style 𝒮/Op/→ machinery is well-defined, and the relationship to ASN-0034's allocator vocabulary is handled through explicit re-lettering and the labelled bridge requirements.

- **Joint induction structure.** The mutual recursion among B_type, B_fin, B1, B10, and Bop's correctness is identified explicitly, the inductive hypothesis is stated, and the per-invariant proofs cite the joint hypothesis at the precondition state. No circularity at a fixed state — each preservation step uses prior-state hypotheses only.

- **Case exhaustion.** B1's "other namespaces" partition into sub-cases (A)/(B)/(C) is exhaustive and the (C) trailing-zero/stream-coincidence argument is explicit. B6's necessity proof handles every failure mode for each condition with named propagation mechanisms (TA5(b) preservation, TA5(d) separator placement, B5 zero-count). B7 covers all three configurations of (#a vs #b, nesting).

- **Boundary cases handled.** Singleton p = [0], pure trailing zero with d ∈ {1, 2} producing structurally distinct failure modes, hwm = 0 vs hwm ≥ 1 in next and B1, empty children vs non-empty children, M ≤ m vs M > m in B9. The trace exercises d = 1 (Step 4) and unbounded extent (Steps 5–7) concretely.

- **Forward requirements clearly marked.** Bridge1, Bridge2, B3 are labelled "forward requirement," with the conditional nature of allocator/registry coincidence ("Σ.B ⊆ allocated(Σ) requires parent-prerequisite enforcement, deferred") tracked through the text.

- **Cross-ASN references.** All references are to foundation ASNs (ASN-0034). No non-foundation ASN-NNNN references.

- **B6(iii) redundancy at d = 1.** Acknowledged explicitly as a presentation choice — the uniform form `zeros(p) + (d − 1) ≤ 3` collapses TA5a's two d-cases under T4-validity of p.

- **B0★ vs B0.** Single-step vs multi-step monotonicity are separately labelled, with use-site discrimination (B8 Case 1 cites B0★; wp analyses cite B0).

The ASN remains at specification level throughout — Gregory's implementation is cited as motivation/confirmation, not as specification.

VERDICT: CONVERGED
