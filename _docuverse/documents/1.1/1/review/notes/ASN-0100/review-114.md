# Review of ASN-0100

This is a thorough and, on the mathematics, a rigorous specification. The three-region decomposition, the I3 identification, the per-state/composite-boundary atomicity split, the closed-interval D-CTG★ reduction (including the live off-prefix case at `m ≥ 3`), and the projection-tracking derivation all hold up under scrutiny. The boundary cases — append (`j=N`), prepend (`j=0`, forced `n'_{s_C}=0`), empty document, deep subspace — are each worked and checked. I found no correctness gap.

The remaining issues are the accreted meta-prose and duplication this note is flagged for under `review-mode.anti-bloat`.

## REVISE

### Issue 1: Duplicated closing paragraphs + document-ordering justification in §Atomicity

**ASN-0100, §Atomicity and Canonical Order**: The two paragraphs closing the forced-ordering discussion restate the same conclusion:

> "These forced orderings determine INSERT's boundary obligations; every other interleaving of the elementary steps reaches the same Σ'. … so the canonical placement of the K.ρ firings at the end of steps 1–4 is **expository, not mandatory**."

immediately followed by:

> "The abstract specification commits to none of the admissible interleavings; each intermediate is itself a reachable state satisfying the per-state invariants, and the boundary couplings J0, J1★, J1'★ discharge at the composite boundary (Σ, Σ')."

**Problem**: Two consecutive paragraphs assert the same thing in different words (spec is interleaving-independent; couplings discharge at the boundary). The clause "the canonical placement of the K.ρ firings … is expository, not mandatory" is prose justifying the document's own ordering choice — a flagged accretion pattern, not a property of the operation.
**Required**: Collapse to one statement of decomposition-independence. Drop the self-referential justification of the exposition's step ordering.

### Issue 2: `d' ≠ d` projection invariance derived twice in separate sections

**ASN-0100, §Cross-document independence**: "Cross-document independence extends to link projection: for any link `ℓ ∈ dom(L)` and any document `d' ≠ d` … so `project(ℓ, i, d', Σ') = project(ℓ, i, d', Σ)` directly."

**ASN-0100, §Coverage and link discoverability (INS.proj)**: "*For `d' ≠ d`:* `π` is the identity and `N_{ℓ,i} = ∅` … composing across the finite step sequence … yields `project(ℓ, i, d', Σ') = project(ℓ, i, d', Σ)`."

**Problem**: The same conclusion for unmodified documents is established independently in two places — a quick argument in the invariant section and the full LP4-composition in INS.proj. The same conclusion proved twice is duplication.
**Required**: State it once (in INS.proj, where the per-step LP4 derivation lives) and have §Cross-document independence cite INS.proj rather than re-derive.

## OUT_OF_SCOPE

None — the Open Questions correctly defer link-subspace insertion, COPY/DELETE/REARRANGE, version derivation, and replication.

VERDICT: REVISE
