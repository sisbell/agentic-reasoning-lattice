# Review of ASN-0074

## REVISE

### Issue 1: C2 enumeration argument compresses a multi-step derivation into a single assertion

**ASN-0074, Resolution / C2 — ResolutionWidthPreservation**: "any depth-m tumbler diverging from u before component m falls outside the range by T1(i) (ASN-0034)"

**Problem**: This sentence is doing the work of a multi-step argument. The claim is that every depth-m tumbler t in [u, reach(σ)) satisfies tⱼ = uⱼ for all j < m — a component-by-component confinement result strictly stronger than C0a (which only establishes t₁ = u₁). The underlying argument for each j has two cases:

1. If tⱼ < uⱼ, then t < u by T1(i) at divergence point j, contradicting t ≥ u.
2. If tⱼ > uⱼ, then since reach(σ)ⱼ = uⱼ (action point m > j, established earlier in C2), we have tⱼ > reach(σ)ⱼ, so t > reach(σ) by T1(i), contradicting t < reach(σ).

Case 2 depends on the fact reach(σ)ⱼ = uⱼ for all j < m — which C2 does establish two sentences earlier, but never connects to the enumeration claim. C0a performs exactly this two-case analysis at j = 1; C2 needs it at every j from 1 to m − 1 but shows neither the cases nor the inductive extension.

The "Conversely" sentence that follows compounds this: it cites C0a (which only gives t₁ = u₁) as the basis for concluding that "the enumeration is exhaustive," but exhaustiveness requires all m − 1 leading components to be fixed, not just the first.

**Required**: Either (a) strengthen C0a to a full prefix-confinement lemma — "every t ∈ ⟦σ⟧ satisfies tⱼ = uⱼ for all 1 ≤ j < m" — using the same proof technique at each component (the argument is structurally identical to C0a's, replacing j = 1 with general j and using reach(σ)ⱼ = uⱼ from TumblerAdd), then cite it in C2; or (b) show the two-case argument inline in C2 at general j and note it applies uniformly for 1 ≤ j < m. The "Conversely" sentence should then cite this result, not bare C0a.

## OUT_OF_SCOPE

### Topic 1: Subspace applicability beyond text subspace
The content reference definition permits any subspace identifier u₁, but the block decomposition machinery (ASN-0058) is stated for text-subspace positions (v₁ ≥ 1). C1a's generalization argument is sound for any subspace, but ASN-0058 does not formally cover the u₁ = 0 (link subspace) case.
**Why out of scope**: Extending ASN-0058's block decomposition definitions to non-text subspaces is new territory, not a defect in this ASN.

### Topic 2: Composite resolution optimization
The open question about reordering source references in a content reference sequence, and the related question of whether adjacent I-address runs from different source references may be merged when they happen to be I-adjacent.
**Why out of scope**: The ASN correctly defines composite resolution as concatenation. Optimization strategies are a future design decision.

### Topic 3: Higher-depth worked example
The worked example uses m = 2, the simplest non-trivial case where the prefix-confinement argument reduces to a single application of C0a. An example at m ≥ 3 would exercise the multi-component confinement that C2 relies on.
**Why out of scope**: Additional examples strengthen confidence but are not required by the current claims.

VERDICT: REVISE
