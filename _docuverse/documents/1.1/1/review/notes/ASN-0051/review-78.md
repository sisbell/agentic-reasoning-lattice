# Review of ASN-0051

## REVISE

### Issue 1: Incorrect citation for the per-block mapping rule

**ASN-0051, SV11 (Partial Survival, "Derivation of the formula" paragraph)**: "within each block β_k = (v_k, a_k, n_k) the per-block mapping rule (M0/M3, ASN-0058) sets M(d)(v) = a_k + (v − v_k) ∈ I(β_k)"

**Problem**: The cited claims do not establish what the text says they do. M0 (WidthCoupling) only states |V(β)| = |I(β)| = n — a cardinality fact, not a mapping rule. M3 (RepresentationInvariance) only states that I-address determination is invariant across equivalent decompositions — well-definedness, not the rule's form. Neither M0 nor M3 directly says M(d)(v_j + k) = a_j + k. A reader following the citation to verify the proof step would find unrelated content.

**Required**: Cite B3 (Consistency, ASN-0058), which states the mapping rule directly: `(A j : 1 ≤ j ≤ m : (A k : 0 ≤ k < nⱼ : M(d)(vⱼ + k) = aⱼ + k))`. Alternatively, cite the MappingBlock definition `⟦β⟧ = {(v + k, a + k) : 0 ≤ k < n}` from ASN-0058, which is where the rule originates definitionally. The single re-citation suffices; the surrounding derivation (B1 coverage, set algebra for distribution) is otherwise correct.

## OUT_OF_SCOPE

None. The Open Questions section appropriately identifies future-ASN topics (same-content multi-V-position resolution, dormant link revival, fragment ordering convention, multi-link overlapping coverage interaction, fragment count bounds, discovery latency, fork preservation, home-vital relationship), and the scope note correctly excludes link type semantics and BEBE replication.

VERDICT: REVISE
