# Review of ASN-0102

The technical core is sound: the displacement/laydown effect, the wp(COPY, S3★) reduction to the copied region, the X16 tiling, the cross-origin and self-transclusion handling, and the coupling discharge all hold up under inspection. My findings are about ordering, an elided derivation step, and accreted framing prose — the latter expected given this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: "What shifts" claims depend on a tiling proved last in the same section
**ASN-0102, X7 (NonDestructivePlacement)**: "The copied `[v, v+W)` and displaced-image `[v+W, …)` ranges are disjoint by the X16 tiling, so no copied mapping collides with a displaced one."
**ASN-0102, X8**: "that boundary behaviour is treated in X12."
**Problem**: X7's no-overwrite conclusion rests entirely on the disjointness established by X16, and X15's atomicity argument also leans on X16, yet X16 is the *last* claim proved in the section — after X7, X8, X9. X8 additionally defers to X12. Multiple paragraphs in the section defer downstream to the same later claims (X16, X12), which is the forward-reference accretion pattern: the reader must jump ahead to verify the load-bearing tiling before the claims that consume it.
**Required**: Either reorder so the X16 tiling (range-disjointness) precedes its consumers X7/X8/X15, or have X7 establish copied/displaced range-disjointness locally (it needs only `[v, v+W) ∩ [v+W, n_S+W] = ∅`, a one-line fact) rather than citing the full density argument.

### Issue 2: PC3 elides the L0 step for `subspace_I = s_C`
**ASN-0102, PC3**: "by PC1 every source span is content-subspace-resident, so C1 yields resolved addresses in `dom(Σ.C)`, carrying `subspace_I(·) = s_C`."
**Problem**: The conclusion `subspace_I(a) = s_C` does not follow from the *source V-position* being in subspace `s_C`; it follows from the *I-address* lying in `dom(Σ.C)`, every member of which has `subspace_I = s_C` by L0 (ASN-0093/0047). The note jumps from "source span is content-resident" to "resolved address carries `subspace_I = s_C`" without naming the premise (L0) that actually licenses it. Per the depth standard, a derived property must name its premise.
**Required**: Cite L0: source `s_C` V-positions map via S3★ to `dom(Σ.C)`, and L0 fixes `subspace_I = s_C` on those addresses.

### Issue 3: Worked-example navigational framing is accreted meta-prose
**ASN-0102, worked examples**: "Both scenarios above are interior...", "Every scenario above lands on the non-merging side of X8 and X12... We now construct the discriminating case", "A second boundary configuration the interior examples do not exercise is the append..."
**Problem**: The five examples open with cross-referential sentences that orient the reader *among the accumulated examples* — confessing which gap each one fills relative to its predecessors — rather than advancing the argument. This is the accretion signature: examples added cycle-by-cycle to cover a case a prior reviewer flagged, each tagged with framing that explains its position in the set. The concrete examples themselves are valuable and should stay; the inter-example navigational prose is noise. The same over-justification appears in X14 ("it incurs two further provenance obligations that the foundation otherwise carries implicitly").
**Required**: Strip the navigational framing sentences (state each example's configuration directly without comparing it to the others), and remove the X14 meta-statement about obligations "the foundation otherwise carries implicitly" — discharge P7/P4★ without narrating why they are now owed.

## OUT_OF_SCOPE

### Topic 1: Re-displacement of copied content by a later operation
**Why out of scope**: The first Open Question (origin/discoverability under subsequent displacement) concerns interaction with INSERT/DELETE/REARRANGE mechanics, which are reserved for other ASNs.

### Topic 2: Provenance of a document that is itself re-sourced
**Why out of scope**: The second Open Question (containment when a reference-holding document becomes a source) is new territory about chained provenance, not a gap in COPY's own contract.

VERDICT: REVISE
