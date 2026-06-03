# Review of ASN-0069

## REVISE

### Issue 1: V11's "Remark on premise scope" duplicates the "Anchoring at Σ" paragraph

**ASN-0069, §"Composability: Fork of a Fork", V11**: The paragraph labeled "*Anchoring at `Σ`.*" (immediately after the V11 statement) and the paragraph labeled "*Remark on premise scope.*" (after the derivation) state the same content in different words. Anchoring: "the premise scopes per-step source preservation to each step's *immediate* source `d^{i-1}_new`... V11 anchors `V_{s_C}(d_src)` and `M(d_src)(v)` at `Σ`... Modifications M-targeted at `d_src` between fork steps are admissible." Remark: "The premise constrains only each step's *immediate* source `d^{i-1}_new`... edits to `d_src` after step 1 are immaterial because the conclusion anchors `V_{s_C}(d_src)` and `M(d_src)(v)` at the immutable initial state `Σ`."

**Problem**: Two paragraphs in the same claim say the same thing. The only non-overlapping content is the Remark's pointer to V5a Corollary 2 for discharging non-immediate edits.

**Required**: Merge into one paragraph. Keep the single V5a-Corollary-2 discharge point; drop the repeated anchoring rationale.

### Issue 2: Defensive notation-disambiguation meta-prose in the composite verification

**ASN-0069, §"The Fork Composite", "*Notation for the verification.*"**: "This notation is intentionally distinct from V10's and V11's `Σ¹, Σ², …, Σ^k` (unbracketed superscript)... The two conventions are disjoint and never collide."

**Problem**: This is meta-prose justifying that a notation choice won't collide rather than advancing the proof. The reader does not need a defense of why two superscript conventions coexist; introducing `Σ^{(j)}` for sub-states suffices.

**Required**: Reduce to a one-line definition of `Σ^{(j)}` for intra-composite sub-states; delete the collision-disjointness justification.

### Issue 3: V4 justifies internal consistency with the Properties table

**ASN-0069, §"The Arrangement Layer", V4**: "No precondition on `V_{s_C}(d_op)` is needed; the claim is consistent with the Properties Introduced table entry, which likewise carries no precondition."

**Problem**: The clause about consistency with the Properties Introduced table is meta-prose — it cross-checks the claim against the document's own summary table rather than advancing the claim. The vacuous/substantive split already establishes unconditionality.

**Required**: Drop the table-consistency clause. Keep the vacuous-when-empty / substantive-when-nonempty statement.

### Issue 4: V0 follow-up paragraph re-litigates which property is "primary justification"

**ASN-0069, §"The Fork Composite", V0**: After the effects block, "The 'undefined elsewhere' line is the *exact* characterization `dom(M'(d_new)) = V_{s_C}(d_op)` supplied by V4b — V6's `V_{s_L}(d_new) = ∅` is a corollary... but V4b is the primary justification because it rules out any V-position outside `V_{s_C}(d_op)` regardless of subspace."

**Problem**: The effects block already annotates the line with "(V4b; V6 as corollary for link-subspace V-positions)". The follow-up paragraph re-explains the V4b-vs-V6 relationship — a justification of which citation is primary, not new content.

**Required**: Delete the follow-up paragraph; the inline annotation already carries the citation.

OUT_OF_SCOPE: none beyond the Open Questions, which are correctly deferred (concurrency, snapshot-vs-living fork, transcludent sources, version-space coherence).

VERDICT: REVISE
