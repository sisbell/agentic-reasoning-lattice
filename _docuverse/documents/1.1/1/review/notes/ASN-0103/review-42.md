# Review of ASN-0103

The core mathematics is sound. The length-filter argument (`D_A = E ∩ S(A,2)`, excluding versions by length `≥ #A+3`) is rigorous in both inclusions, the freshness chain `d ∈ S(A,2) \ D_A = S(A,2) \ E ⟹ d ∉ E` is tight, the K.δ decomposition discharges its case-(ii) preconditions correctly, and the worked example concretely verifies the claims. The findings below are accretion, consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Meta-prose describing the abandoned approach in the distinctness argument
**ASN-0103, Effect One (Freshness and distinctness)**: "so `d` differs from each of them with no bespoke exhaustiveness or namespace-disjointness argument. A sharper same-chain statement is available when wanted: `A_doc(A) = S(A, 2)` is a SiblingStream whose enumeration is strictly increasing under T1, hence injective (S0, StreamOrdering; ASN-0040)..."
**Problem**: Two accretions in one passage. First, "with no bespoke exhaustiveness or namespace-disjointness argument" describes what the proof does *not* do — a relic of the prior revision that replaced the bespoke argument with GlobalUniqueness (per the recent commit). It advances no reasoning. Second, the "sharper same-chain statement... when wanted" introduces an unused alternative that is strictly *weaker* than the GlobalUniqueness conclusion already established (same-chain injectivity is a subset of "no two distinct allocation events collide"). It is offered optionally ("when wanted") and consumed nowhere.
**Required**: Delete the "with no bespoke exhaustiveness..." clause and the "A sharper same-chain statement..." sentence. GlobalUniqueness alone discharges distinctness.

### Issue 2: The redundant same-chain hedge is triplicated
**ASN-0103, CND.monotone (Claims table)**: "distinctness from every other document address ... by GlobalUniqueness (ASN-0034 ...), with the sharper same-chain injectivity also available via S0 (StreamOrdering, ASN-0040)"
**Problem**: The same unused "sharper same-chain injectivity also available" hedge from Issue 1 recurs verbatim-in-substance here, and the distinctness-via-GlobalUniqueness claim appears a third time in *Invariants Maintained* ("Address permanence and distinctness"). The table row should summarize the proof, not re-carry the optional alternative the proof does not use.
**Required**: Drop "with the sharper same-chain injectivity also available via S0" from the CND.monotone row. Keep the GlobalUniqueness basis only.

## OUT_OF_SCOPE

### Topic 1: Effective ownership `ω_{Σ'}(d) = π`
**Why out of scope**: The ASN establishes structural ownership `owns(π, d) ≡ pfx(π) ≼ d` (CND.own) and explicitly defers the effective-owner reading to the entity-set/baptismal-registry coupling raised in the final Open Question. This is correctly scoped as future territory, not a defect.

VERDICT: REVISE
