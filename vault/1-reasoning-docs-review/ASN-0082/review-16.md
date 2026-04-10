# Review of ASN-0082

## REVISE

### Issue 1: Gap exclusion argument cites TS4 but needs TS1
**ASN-0082, Gap and vacated regions**: "for every v ≥ p, shift(v, n) > v ≥ p by TS4 (ASN-0034), so no shifted image lands in the gap"
**Problem**: TS4 gives shift(v, n) > v ≥ p, hence shift(v, n) > p. But the gap is [p, shift(p, n)), so excluding the gap requires shift(v, n) ≥ shift(p, n), not merely shift(v, n) > p. The argument as stated shows shifted images are past the *start* of the gap but not past its *end*. Two cases are needed: (1) v = p: shift(p, n) equals the exclusive upper bound, so it is not in [p, shift(p, n)); (2) v > p with #v = #p = m: TS1 (ShiftOrderPreservation) gives shift(v, n) > shift(p, n), placing the image strictly past the gap's upper bound.
**Required**: Replace the one-sentence TS4 argument with the two-case argument citing both TS4 (or direct computation for the v = p boundary) and TS1 (for v > p).

## OUT_OF_SCOPE

### Topic 1: Post-deletion shift
The analogous property for deletion — shifting positions backward when content is removed — is a natural companion to I3 but structurally different (contraction vs. expansion, backward vs. forward).
**Why out of scope**: This ASN addresses insertion displacement only; deletion belongs in a future DELETE or span-algebra extension ASN.

### Topic 2: Shift composition
When two insertions occur in sequence, their shifts compose. Whether composed shifts commute or associate determines whether insertion order matters for the final arrangement.
**Why out of scope**: Composition is an operation-sequencing concern for the INSERT ASN or a separate composition ASN, not for the single-shift property defined here.

VERDICT: REVISE
