# Review of ASN-0086

## OUT_OF_SCOPE

### Topic 1: Multi-arity typed relations
**Why out of scope**: L_K and A_K are restricted to arity-3 standard-triple links. Higher-arity links (L3-admissible at |L(a)| > 3) exist in dom(Σ.L) but fall outside L_K. Extension to A_K^{(n)} is explicitly deferred in Open Questions.

### Topic 2: Concurrency between Emit and Observe
**Why out of scope**: The substrate model is sequential. Atomicity guarantees and observer consistency for concurrent emissions are higher-layer concerns. Acknowledged in Open Questions.

### Topic 3: Substrate-level elevation of sibling-frontier discipline
**Why out of scope**: R0a, R0a-Cor1, R0a-Cor2, Emit_K function-ness, and Nullify single-tuple scope are discipline-conditional. Whether SubstrateEmissionPrimitive should be tightened (making R0a unconditional) is an upstream design question. Acknowledged in Open Questions.

### Topic 4: Unconditional element-field-depth bound
**Why out of scope**: R0a-Cor2 establishes #E(a) = 2 only under the discipline. Tightening ASN-0043's L1b from #E ≥ 2 to #E = 2 is an upstream question, not an ASN-0086 issue.

### Topic 5: Native scoped form of L14
**Why out of scope**: The globally s_C-resident-content Setup hypothesis strengthens ASN-0043's L14 to substrate-wide disjointness. Slice-wise reformulations of R0, R4, R5 under L14's native scoped form are explicitly noted as future work.

### Topic 6: Inter-layer type catalog coordination
**Why out of scope**: Dynamic extension of T_cat by multiple layers and collision handling on type addresses is a higher-layer concern.

VERDICT: CONVERGED
