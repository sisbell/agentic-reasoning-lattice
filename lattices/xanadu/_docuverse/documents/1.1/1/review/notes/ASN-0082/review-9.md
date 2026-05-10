# Review of ASN-0082

## REVISE

### Issue 1: VB axiom language admits an alternative reading that breaks VD

**ASN-0082, Local Axioms, VB**: "after which all subsequent V-positions are produced by flat sibling allocation (`inc(·, 0)` only)"

**Problem**: VD's derivation depends on every element of dom(M(d)) within a subspace being a sibling-stream output. VB's phrase "all subsequent V-positions" naturally implies the bootstrap produces only structural prefixes, not V-positions — but the word "subsequent" admits a reading where earlier bootstrap-produced entries are also V-positions at a shallower depth. Under that reading, the bootstrap prefix (e.g., the single-component subspace identifier [S]) has depth 1 while sibling outputs have depth 2+, and VD does not follow from VB + T10a.1.

Additionally, "two-level nesting" is informal. It isn't clear whether this constrains every subspace to exactly depth 2 or is merely illustrative. The ASN doesn't depend on the exact depth (only on uniformity via VD), but the axiom should be precise about what it constrains.

**Required**: Tighten VB to explicitly state that bootstrap-established prefixes are not elements of dom(M(d)). For example: "All V-positions in dom(M(d)) within a subspace are produced exclusively by a single allocator's sibling stream (`inc(·, 0)` only); bootstrap-established prefixes are structural and do not appear in dom(M(d))." Clarify whether "two-level nesting" prescribes a fixed depth or describes typical bootstrap topology.


## OUT_OF_SCOPE

### Topic 1: Extension of I3-S beyond ordinal-level spans
**Why out of scope**: I3-S restricts to ordinal-level spans (actionPoint(ℓ) = m) because the commutativity of δₙ ⊕ ℓ with ℓ ⊕ δₙ requires both displacements to act at the same position. Spans with actionPoint(ℓ) < m act on a different structural axis — extending the result requires new machinery.

### Topic 2: Shift composition under successive insertions
**Why out of scope**: Two insertions at different positions produce two shifts whose interaction (ordering dependence, combined frame conditions) is an operation-sequencing concern that builds on I3 but extends beyond this single-operation ASN.

### Topic 3: External V-position reference tracking
**Why out of scope**: The ASN's own open question. When external state records a V-position, the system needs a propagation mechanism. This depends on the full INSERT specification (deferred) and the reference-tracking architecture.

VERDICT: REVISE
