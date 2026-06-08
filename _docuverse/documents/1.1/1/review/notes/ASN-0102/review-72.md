# Review of ASN-0102

I read the full COPY specification. The technical core — the wp-reduction to S3★ (X3), the three-class tiling that establishes density (X16), the merge/origin reasoning (X8/X11/X12), and the coupling discharge (X14) — is sound, and the five worked examples genuinely exercise distinct boundaries (cross-origin fragmentation, overlapping self-transclusion, empty-subspace first insertion, append, coalescing). No missing edge case or broken proof step found. The residual issues are the meta-prose this note's `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: Duplicated "natural framing" prose across two sections
**ASN-0102, X14 and the self-transclusion example**: X14 states "For a standalone, self-coupling COPY the natural framing is `B = Σ`, where this coincides with the split by prior membership at COPY's own pre-state." The self-transclusion example then repeats: "Reading this example's pre-state `Σ` as the composite boundary `B` (the natural framing for a standalone, self-coupling COPY)..."
**Problem**: The same `B = Σ` framing is explained twice in nearly identical words — the pattern "two paragraphs in the same document say the same thing." The example only needs to instantiate, not re-explain.
**Required**: State the `B = Σ` framing once (in X14). In the example, write "taking `B = Σ`" without re-deriving the rationale.

### Issue 2: PC3 explains *why* the subspace choice is made rather than *what* it is
**ASN-0102, PC3**: "COPY targets the content (byte) subspace: `S = s_C` — a definitional choice, consistent with placing content, since `dom(Σ'.C) ∩ dom(Σ'.L) = ∅` (store disjointness, ASN-0093 SD) means a content image cannot route to an `s_L` slot. The S3★ obligation over the inserted mappings is discharged once in the `wp` computation below."
**Problem**: This is the flagged pattern — prose around a definitional choice that argues why the choice is needed rather than stating it, plus a forward-pointer ("discharged once ... below"). The store-disjointness justification adds nothing the wp computation does not already establish.
**Required**: Reduce to the choice itself: "COPY targets the content subspace: `S = s_C`." The S3★ discharge belongs to the wp computation and need not be announced from the precondition.

### Issue 3: Implementation-essay sentence in X14's structural conclusion
**ASN-0102, X14**: "This is the abstract counterpart of the spanfilade entry that makes FINDDOCSCONTAINING return the target immediately after a copy, recorded against the *destination* document, not the original creator (Gregory Q18/Q19; Nelson Q6/Q8)."
**Problem**: This sits at the close of the coupling-discharge proof and narrates implementation mechanics (FINDDOCSCONTAINING, spanfilade entries) rather than advancing the abstract guarantee, which the preceding sentence (content-containment permanence) already states. It is corroboration prose occupying a proof-conclusion slot.
**Required**: Drop the sentence or fold the one load-bearing point ("recorded against the destination, not the creator") into the permanence statement without the implementation narration.

## OUT_OF_SCOPE

The four Open Questions (discoverability after later displacement, containment when a referencing document is itself a source, time-varying views, identity when the allocator is unreachable) correctly defer to future ASNs and are not errors here.

VERDICT: REVISE
