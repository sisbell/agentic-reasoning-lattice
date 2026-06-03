# Review of ASN-0070

I checked the core proofs (F-canonical's case split on action point, the consecutivity Characterisation induction, Step 2a existence, the inter-component left/right closures, F-contig, the wp analysis) and the six worked configurations. The mathematics is sound: the action-point exhaustiveness is correct, the infinite/finite denotation split at `k < m` vs `k = m` is rigorous, the maximal-run reconstruction establishes per-subspace uniqueness without relying on S9 over `⟦·⟧_V` (consistent with the prior declined finding), and each configuration exercises a distinct property. No mathematical gap found.

The note carries the anti-bloat classifier, and the residual findings are accretion, not error.

## REVISE

### Issue 1: Redundant "lookup totality" restatement under F-subspace

**ASN-0070, F-subspace / Consequence**: "**Derived guarantee (lookup totality).** For every `v ∈ R(d, e)|_{s_C}`, `M(d)(v) ∈ dom(C)`, by S3★ ... For every `v ∈ R(d, e)|_{s_L}`, `M(d)(v) ∈ dom(L)` ..."

**Problem**: The Consequence immediately above already establishes `R(d, e)|_{s_C} = M(d)⁻¹(coverage(e) ∩ dom(C))` (and the `s_L` analogue), from which `M(d)(v) ∈ dom(C)` is an immediate projection — the "Derived guarantee" restates established content in different words. The named property "lookup totality" has no downstream consumer in the note; no later lemma cites it. This is the "two paragraphs say the same thing" pattern.

**Required**: Remove the paragraph, or fold its content into the Consequence if a named handle is genuinely needed by a downstream claim (none currently uses it).

### Issue 2: Defensive precondition-narration around M-int

**ASN-0070, Computation via Decomposition**: "M-int (TumblerIntervalCharacterization, ASN-0058) requires *both* of its operands in dom(M(d)); we therefore apply it not to arbitrary interval points but to each `y = v + k ∈ V(β)` — which the B3 step has placed in dom(M(d)) — paired with the block start `v ∈ dom(M(d))` ..."

**Problem**: The load-bearing conclusion is "each block lives in exactly one V-subspace." The surrounding narration about M-int's operand requirements and how-we-are-careful-to-apply-it is defensive meta-prose the reader must traverse to reach that conclusion. The care is real but can be stated directly without narrating the precondition-management.

**Required**: Reduce to the load-bearing statement, e.g.: "By B3, every `v + k ∈ V(β)` lies in dom(M(d)); M-int (ASN-0058) then gives `subspace(v + k) = subspace(v)`, so each block lives in one V-subspace and the decomposition partitions cleanly by subspace."

## OUT_OF_SCOPE

### Topic 1: Multi-home reach relationships, concurrency semantics, transclusion-lineage relationships
**Why out of scope**: These are the note's own Open Questions and belong to future ASNs; FOLLOWLINK correctly defines the pure-query inverse-image semantics without committing to them.

VERDICT: REVISE
