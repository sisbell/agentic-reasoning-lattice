# Review of ASN-0075

## REVISE

None.

## OUT_OF_SCOPE

None — the ASN respects its declared scope (excluding INSERT/DELETE/COPY/REARRANGE mechanics, link semantics, version DAG structure, replication). Restoration mechanics are noted as future work without intrusion; concurrency, multi-document generalisation, and source-document-specific semantics are properly relegated to open questions.

VERDICT: CONVERGED

The ASN is rigorous on every load-bearing claim:

- **D-EXH** discharges the composite-boundary hypothesis explicitly, traces the impossible row through L14 → S3★-aux → S3★-contrapositive → Contains_C → P4★, and verifies mutual exclusion and exhaustiveness per row.
- **D-DISCR** exhibits two reachable states agreeing on every component of (C, L, E, M) but differing in R, with the histories carefully validated against ValidComposite★ and J0/J1★ couplings. The K.α-bundling justification is correct and explicit.
- **D-BOUND** is presented as a contract axiom that structurally discharges P4★ at every invocation, not as informal handwaving.
- **D-ACT**'s witness-run decomposition is genuinely complete: the I_C-contiguity argument via discrete intermediate-value, the T1-min/index-min coincidence via T9, and the four bijection conditions are each verified rather than asserted.
- **D-ORD**'s use of `min` rather than uniqueness correctly accommodates S5 sharing and proves injectivity from S2.
- The **worked example** concretely verifies D-EXH, D-IDENT, D-ORIG, and D-SYM with full K.δ/K.α/K.μ⁺/K.μ~/K.μ⁻/K.ρ traces.
- Edge cases (d_A = d_B, both empty, asymmetric population, R-disjoint via the supplementary lemma) are addressed.
