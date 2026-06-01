# Review of ASN-0047

This ASN is formally mature; the per-state/composite-boundary partition, the wp-derivations of J1★/J1'★, and the worked examples all hold up under checking. The note carries the `review-mode.anti-bloat` classifier, and the substantive findings below are accretion patterns — redundant discharges and deferral chains that a precise reader must work around. No correctness defect or non-foundation cross-reference was found.

## REVISE

### Issue 1: Redundant freshness premise in the fork worked example
**ASN-0047, "Worked example: fork with subsequent insertion" → "Insert new content into d₂", K.α step**: "The freshness of a₃ — i.e., `a₃ ∉ dom(C₂)` — is discharged by two complementary premises." … "The two premises together close the obligation."
**Problem**: Premise (ii) cites SubAllocatorBundle.FirstEmission, which supplies `a₃ ∉ dom(Σ.C) ∪ dom(Σ.L)` outright. That already discharges `a₃ ∉ dom(C₂)` in full. Premise (i) (cross-document distinctness from a₁, a₂) only re-derives distinctness from a subset of dom(C₂) that (ii) already covers, so the "two premises together" framing imagines a residual obligation that (ii) closes alone. This is reviser drift — an over-supplied discharge presented as jointly load-bearing.
**Required**: Discharge freshness from premise (ii) alone; drop premise (i) or demote it to a one-line corroboration, not a co-required premise.

### Issue 2: K.δ case (ii) dispatch stated three times
**ASN-0047, "Elementary transitions" (K.δ case (ii)), "ParentAllocatorDispatch (sub-lemma)", and "K.δ case (ii) discharge and parent-allocator activation"**: The per-k (k = 0/1/2) operand admissibility, structural identities, and parent-allocator activation appear across all three locations in overlapping detail — e.g. the k = 2 spawnPt-premise sourcing is given both in the discharge section's table and in the K.δ definition's structural identities; the k = 1 `A_v` activation is stated in both the definition and the discharge section.
**Problem**: Matches the flagged pattern "two paragraphs in the same document say the same thing in different words," forcing the reader to reconcile three near-identical treatments of one dispatch.
**Required**: Designate one authoritative per-k discharge (the discharge section is the natural home); have the K.δ definition and ParentAllocatorDispatch reference it rather than restate the per-k analysis.

### Issue 3: K.μ⁻ contraction-shape deferral chain
**ASN-0047, K.μ⁻ definition (constructive precondition), "K.μ⁻ amendment (PerSubspaceScope)", and "K.μ⁻ admissible contraction shape"**: The amendment says "the derivation in *K.μ⁻ admissible contraction shape* below shows this is equivalent to the post-state characterization," while the definition's constructive precondition and the equivalence section each restate the constructive-vs-post-state correspondence.
**Problem**: Three sections defer to one another and re-state the same equivalence — the flagged "multiple paragraphs in different sections defer to the same downstream location" pattern.
**Required**: State the constructive ⟺ post-state equivalence once (in the dedicated section); remove the forward-pointer scaffolding from the definition and amendment, leaving a single bare reference.

### Issue 4: CL-UNIQ-under-K.μ~ derived twice
**ASN-0047, "Decomposition of K.μ~" sub-step (4)**: "The same functional identity (3) also gives post-state CL-UNIQ preservation directly, without passing through the pointwise identity…"
**Problem**: The CL-UNIQ preservation argument is then given again in the Class (a) CL-UNIQ verification prose ("Steps (1)–(4) of the link-subspace fixity proof, where the functional identity `M'(d)|_{dom_L} = M(d)|_{dom_L}` carries CL-UNIQ from Σ to Σ'"). The same inference (equal functions share injectivity) is made in both places.
**Required**: Keep the CL-UNIQ-from-(3) inference in one site and reference it from the other.

## OUT_OF_SCOPE

None. The future-directed material (link-subspace capacity bounds, concurrent allocation, link inheritance under forking, tombstoning reconciliation) is already correctly confined to the Open Questions list rather than asserted in the body.

VERDICT: REVISE
