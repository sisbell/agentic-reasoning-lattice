# Review of ASN-0067

## REVISE

### Issue 1: Worked example I-addresses violate L0 under ordinal shift

**ASN-0067, Worked Example**: "B = {([1,1], 1.0.1.0.1.0.1, 3), ([1,4], 1.0.1.0.1.0.7, 2)}"

**Problem**: The I-address `1.0.1.0.1.0.1` is a 7-component tumbler with element field `[1]` (depth δ = 1). A mapping block of width 3 produces I-addresses `1.0.1.0.1.0.1`, `1.0.1.0.1.0.2`, `1.0.1.0.1.0.3` via ordinal shift. Ordinal shift on a 7-component tumbler changes the 7th component — which IS the subspace identifier E₁. So these three I-addresses have E₁ = 1, 2, 3 respectively, violating L0 (SubspacePartition, ASN-0047): `(A a ∈ dom(Σ.C) :: fields(a).E₁ = s_C)`.

The same problem affects the source I-address `1.0.2.0.1.0.4` (E₁ = 4) and the second block's `1.0.1.0.1.0.7` (E₁ = 7). In any reachable state, L0 + S3 + the ordinal shift definition force I-address element fields to have depth ≥ 2: if `a ∈ dom(C)` with element field `[s_C]` (depth 1), then `a + 1` changes E₁ to `s_C + 1 ≠ s_C`, so `a + 1 ∉ dom(C)` by L0 — making any block of width > 1 impossible. The example's blocks of width 3 and 2 require element field depth ≥ 2.

**Required**: Either (a) use 8-component I-addresses with explicit 2-component element fields — e.g., `1.0.1.0.1.0.1.1` (element field `[1, 1]`, E₁ = 1 = s_C, ordinal 1), so ordinal shift produces `1.0.1.0.1.0.1.2` (E₁ still 1) — or (b) state explicitly that the example uses ordinal-only notation per TA7a (ASN-0034), where the written final component is the ordinal with subspace s_C held as structural context and not written. Option (a) is clearer; option (b) is terser but needs an explicit convention statement.

## OUT_OF_SCOPE

### Topic 1: Concurrent COPY semantics
**Why out of scope**: The ASN correctly identifies (in C13's observation) that the ValidComposite framework provides sequential correctness only. Formalizing visibility of intermediate states under concurrent access requires a concurrency model not yet present in the foundation. The ASN's sequential treatment is complete and correct.

### Topic 2: Authorization invariants for cross-owner COPY
**Why out of scope**: The ASN correctly lists this as an open question. COPY's formal mechanics (resolution, displacement, placement) are independent of who is authorized to perform them. Authorization is a policy layer, not a structural concern of the operation definition.

### Topic 3: Version-pinned vs live transclusion
**Why out of scope**: The COPY definition operates on a single state Σ. Whether the source reference tracks a specific version or the "current" state of the source document is a version-management concern that depends on version semantics not yet formalized.

VERDICT: REVISE
