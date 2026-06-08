# Review of ASN-0112

## REVISE

### Issue 1: V18 overstates origin-moving transitions

**ASN-0112, V18 (origin migration bounds V8)**: "clearing the content subspace (`V_{s_C}(d) = ∅`) while one or more links survive ... `origin_d` migrates from the content anchor `[s_C,1,…,1]` to the link minimum `[s_L,1,…,1]` — **the sole editing transition that moves the origin**."

**Problem**: This is false. There is a second origin-moving transition, symmetric to the one V18 names: **adding content to a link-only document**. The ASN itself establishes (V5, single-subspace discussion) that a link-only document is a reachable, non-empty state with `origin_d = min O(d) = [s_L,1,…,1]`. Insert the first content position into such a document and `[s_C,1,…,1]` becomes occupied; since `s_C < s_L`, `origin_d` now drops to `[s_C,1,…,1]`. The origin moved — `[s_L,1,…,1] → [s_C,1,…,1]` — under an editing transition that V18 does not account for, directly contradicting "the sole editing transition." V8 is correctly hedged ("while content present"), so the defect is confined to V18's universal "sole" claim and its "the one transition that moves the origin" framing.

**Required**: Either drop the "sole" universality and characterize *both* origin-moving transitions (content-clearing moves origin up to the link minimum; first-content insertion into a link-only document moves it down to the content anchor), or restrict the claim's quantifier to transitions that begin with content present.

### Issue 2: V10 duplicates V16

**ASN-0112, V10 (edits act on the span only through `O(d)`)**: "Because `σ_d` is a pure function of `O(d)` (V16), *any* edit alters the reported span exactly insofar as it alters `O(d)`."

**Problem**: V10's invariant content is exactly V16 (`σ_d` is a pure function of `O(d)`) — "a pure function changes its output iff its input changes" is the definition of V16, not an independent claim. What remains in the paragraph ("the exact reach-arithmetic ... belongs to INSERT and DELETE, not this query") is a scope-deferral, not an invariant. This is the anti-bloat pattern: a structural claim slot occupied by a restatement plus a downstream deferral.

**Required**: Remove V10, or replace it with whatever distinct content it is meant to carry. If the only purpose is to disclaim reach-arithmetic, that belongs in the Scope section as one sentence, not as a numbered claim.

### Issue 3: Removable forward-reference deferral

**ASN-0112, "What the caller must be handed"**: "The empty case is taken up in full below (V11)."

**Problem**: Pointer prose that advances no reasoning. The empty case is fully specified at V11 and already flagged in the V0 row of the claims table; the deferral note is the redundant third mention.

**Required**: Delete the sentence.

### Issue 4: Motivational essay inside a proof / repeated rhetorical frame

**ASN-0112, V3 paragraph**: "This is the formal core of Nelson's claim that origin and extent 'describe the document as a whole' *implicitly* — 'there is no choice as to what lies between...'"; and the recurring section openers "Nelson asks whether X ... and answers yes/no" (V8, V11, and the Vstream section).

**Problem**: The V3 quotation sits mid-derivation between the `inc(w,0)` identification and the level-uniformity distinction, forcing the reader to skip essay content to follow the tightness argument. The "Nelson asks whether ... answers ..." device, repeated across three sections, is essay framing that reads as motivation rather than claim.

**Required**: Move the Nelson quotation to a single motivating sentence outside the proof body, and prune the repeated rhetorical framing to once.

## OUT_OF_SCOPE

### Topic 1: Reach-arithmetic of INSERT/DELETE

The exact step-count by which an insertion or deletion moves `max O(d)` (and hence the reach) is correctly left to the INSERT/DELETE ASNs; the note's deferral here is appropriate (see Issue 2 only for the claim-slot duplication, not for the deferral itself).

VERDICT: REVISE
