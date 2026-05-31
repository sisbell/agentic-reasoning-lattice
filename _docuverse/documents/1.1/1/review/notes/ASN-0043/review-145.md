# Review of ASN-0043

This note is mathematically sound throughout — I checked the L1c chain construction, the FSP/FSE conformance lemmas, the L9 ghost-type witness (both cases), PrefixSpanCoverage, and the worked example's six-step extension, and the derivations hold. The L1c chain shape, the `k₁=2`-forces-`home` argument, and the coverage-equality computation in Step 6 all verify. My findings are confined to the accreted meta-prose the `review-mode.anti-bloat` classifier flags.

## REVISE

### Issue 1: `subspace_I` well-definedness is argued twice in adjacent paragraphs
**ASN-0043, Notational convention (Subspace Residence) and L0a**:
- Notational convention: "*`zeros(a) = 3` together with `#E(a) ≥ 1` ensures the projected element field is non-empty so its first component `E(a)₁` exists.*"
- L0a: "*`subspace_I` is well-defined here because every such address is T4-valid with `zeros = 3`, so `#E ≥ 1` by T4's field-segment constraint and `E(·)₁` exists.*"

**Problem**: The same well-definedness chain (T4-valid + `zeros = 3` ⟹ `#E ≥ 1` ⟹ `E₁` exists) is established in the Notational convention paragraph that introduces `subspace_I` uniformly, then re-established in L0a for the content slice. The Notational convention already defines `subspace_I` "*uniformly across every tumbler on which T4b's E projection is well-defined*," which subsumes the content slice. L0a's clause adds nothing the general definition did not already license.

**Required**: Drop the well-definedness clause from L0a and let it cite the Notational convention's uniform definition; L0a need only establish the *slice* and the `s_C`-residence predicate.

### Issue 2: L11a opens with a defensive framer that the following derivation makes redundant
**ASN-0043, L11a — LinkUniqueness**: "*Its precondition is not merely per-event T10a-conformance but that the events are distinct allocation events within a single system conforming to T10a.*"

**Problem**: This sentence explains *why* the next paragraph is needed rather than advancing the argument. The paragraph that follows ("*By S7d each home ... is a node of the system's single allocator tree 𝒯 ... Hence both link-producing events are distinct allocation events within the single T10a system 𝒯, which is exactly GlobalUniqueness's precondition*") is the load-bearing discharge and stands on its own. The framer is a "why the obligation exists" preamble of exactly the kind that compounds across cycles.

**Required**: Delete the framer sentence; begin directly with the S7d/𝒯-membership derivation, which already names the precondition it discharges.

### Issue 3: L5 closes with a speculative aside about a function that was never written
**ASN-0043, L5 — EndsetSetSemantics**: "*A planned `consolidatespanset` function — which might have imposed normalization — was never implemented.*"

**Problem**: The preceding sentences (sequential V-addresses on storage, retrieval ordered by I-address, no positional accessor, uniform iteration in `sporglset2linksetinrange`/`intersectlinksets`) are legitimate implementation evidence for "no span-positional accessor." The closing sentence speculates about what a non-existent function *might* have done — it neither witnesses the claim nor states what any operation does. It is essay content appended to a structural slot.

**Required**: Remove the sentence; the positive evidence already establishes L5.

## OUT_OF_SCOPE

### Topic 1: Global content-subspace constant extending disjointness beyond the `s_C` slice
**Why out of scope**: The note deliberately scopes L14/L14a disjointness to `dom(Σ.C)|_{s_C}` (L0a) and lists the global-constant question in Open Questions. Extending disjointness to all of `dom(Σ.C)` is new territory, not an error here.

### Topic 2: Link/content consistency under transclusion and compound-link well-formedness
**Why out of scope**: Transclusion-time invariants between `Σ.L` and `Σ.C`, and constraints on compound link-to-link structures, are flagged in Open Questions and depend on operation semantics, which this ASN excludes.

VERDICT: REVISE
