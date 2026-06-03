# Review of ASN-0075

I checked the major proofs (D-EXH, D-DISCR, D-ACT, the R-disjointness supplementary lemma, the worked example, D-SUBSP, D-ORD) line by line against the foundations.

## Verified

- **D-EXH (Three-State Exhaustion).** The cross-product is genuinely 2×2; the impossible row (`a ∈ ran(M(d)) ∧ (a,d) ∉ R`) is excluded by a complete chain — L14 gives `a ∉ dom(L)`, S3★-aux + the contrapositive of S3★'s link clause force `subspace(v) = s_C`, then P4★ forces `(a,d) ∈ R`. The boundary hypothesis is correctly identified as load-bearing for P4★, and ASN-0047 does list P4★ as a composite-boundary property (not a per-state invariant), so the caveat is accurate. Mutual exclusion and exhaustiveness are both discharged per row.

- **D-DISCR.** The two histories agree on every component of `(C, L, E, M)`: same K.δ sequence (P1 permanence), same determinate first emission `a = [d.0.s_C.1]`, same stipulated content value `v_a`, History 1's `M(d)` populated-then-emptied to match History 2's never-populated `M(d) = ∅`. J0/J1★/J1'★ are correctly discharged in each composite (bundling K.α with K.μ⁺/K.ρ). The `(a,d) ∈ R_1 \ R_2` difference cleanly drives the discrimination impossibility.

- **D-ACT.** The witness-run bijection is the deepest argument and it holds: shift(·,1) ≡ inc(·,0) on `A_C(d)` emissions (TA5-SigValid + TA5(c) + TumblerAdd), index-contiguity of each equivalence class via the discrete intermediate-value argument on the I-adjacency graph, T1-min = index-min via T9, and right/left-maximality both verified including the `k=1` first-emission edge. The `ℓ` reconstructed addresses are shown pairwise distinct via TA-strict + TS5. The per-half (not union) scope is correctly justified.

- **Worked example, D-SUBSP, D-ORD, supplementary lemma, edge cases.** The fork-and-diverge example produces `({b},{c})` and the classification table checks out against the foundations. D-SUBSP's witness-impossibility for link addresses is fully unpacked (content-V-position excluded by L14, link-V-position by CL-OWN). D-ORD's `vpos` minimum is well-defined (S8-fin) and injective (S2), correctly invoking S5 to justify using `min` rather than asserting uniqueness. The R-disjointness lemma's three-group partition falsifies both conjuncts in each group.

The wp analysis is present and non-trivial (Q1 non-emptiness, Q0 vacuity, with the observational pass-through justified by D-OBS). All in-scope boundary cases (empty arrangements, self-comparison, asymmetric population, no shared content) are handled. Cross-ASN references are confined to the listed foundations.

No REVISE items found.

VERDICT: CONVERGED
