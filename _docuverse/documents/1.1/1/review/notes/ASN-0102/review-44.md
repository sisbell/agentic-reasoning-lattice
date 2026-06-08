# Review of ASN-0102

The operation is defined with all five state components pinned, the wp(COPY, S3★) reduction is sound, the tiling in X16 is exact, and the full ExtendedReachableStateInvariants package plus P3 are discharged conjunct-by-conjunct. The five worked examples each exercise a genuinely distinct boundary configuration (cross-origin non-merge, self-transclusion pre-state pinning, empty-subspace first insert, append/no-trailing-boundary, coalescing/firing-merges) and are exactly what the standards demand — they are not bloat and should stay.

The findings below are the `review-mode.anti-bloat` patterns this note carries: meta-commentary and redundant prose accreted around an otherwise-correct argument.

## REVISE

### Issue 1: Duplicated Nelson [LM 4/11] usage across "cardinal question" and X4
**ASN-0102, "The cardinal question" and X4**: the section quotes [LM 4/11] ("Bytes native elsewhere have an ordinal position…Non-native byte-spans are called inclusions or virtual copies") and X4 quotes the adjacent sentence of the same passage ("Native bytes…all other bytes are obtained by front-end or back-end requests to their home locations") to make the same shared-reference point.
**Problem**: The thesis "placement is by reference, not duplication" is carried formally by X1 (`Σ'.C = Σ.C`) and X3 (SharedReference). The "cardinal question" section restates it in motivational essay-prose ("We are asked what happens…", "Nelson is explicit that…") that the formal claims already establish, and leans on the same primary-source passage X4 uses.
**Required**: Keep the [LM 4/11] grounding at its load-bearing site (X4, where identity-of-instance is derived) and collapse the "cardinal question" framing to at most the single motivating sentence, removing the duplicated quote.

### Issue 2: Meta-commentary comparing worked examples to each other
**ASN-0102, self-transclusion and coalescing examples**: "This is the configuration in which X10(b)'s snapshot resolution and X15's atomicity are *load-bearing* rather than decorative"; "The discriminating predicates of X8 and X12 are now exhibited firing, not merely failing"; "This is the configuration the merge machinery exists for".
**Problem**: These sentences editorialize about each example's pedagogical role relative to the others (and implicitly relative to prior review findings) rather than advancing the reasoning. They are not statements of what COPY does — the concrete tables and the per-claim checks already carry the content.
**Required**: Delete the comparative meta-commentary. The example tables plus the bulleted X-claim checks stand on their own; the reader does not need to be told an example is "load-bearing" or "now firing."

### Issue 3: Defensive parenthetical previewing X8's own bullets
**ASN-0102, X8 opening**: "(each per-reference maximally merged, but not merged across reference boundaries — `resolve_Σ(R)` is the concatenation `resolve(r_1) ⌢ … ⌢ resolve(r_q)`…so consecutive list elements straddling a reference boundary may be I-adjacent without having been merged)".
**Problem**: This parenthetical pre-states the conclusion of X8's own "Across an inter-reference boundary" bullet a few lines later. The same fact is then derived properly in the two-case body. The preview adds words without advancing the argument.
**Required**: Drop the parenthetical; let the two-case body (within-reference / across-boundary) carry the result, since that is where the conclusion is actually earned.

## OUT_OF_SCOPE

### Topic 1: The four Open Questions (later re-displacement, transitive containment recording, time-varying views, allocator unreachability)
**Why out of scope**: These are correctly posed as open and point at future operation/version/replication ASNs, not at gaps in COPY's contract. No action needed — they are not errors in this ASN.

VERDICT: REVISE
