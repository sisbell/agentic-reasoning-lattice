# Cone Review — ASN-0034/D0 (cycle 2)

*2026-04-13 20:13*

### TumblerSub narrative claims to invert TumblerAdd, but the formula uses a different pivot and TumblerAdd is explicitly many-to-one

**Foundation**: TumblerAdd constructive definition (action-point-based, many-to-one property explicitly stated); TumblerSub constructive definition (zpd-based)

**ASN**: TumblerSub introductory description:
> "Given an end position `a` and a displacement `w`, recover the start position."

**Issue**: This description presents TumblerSub as the inverse of TumblerAdd: given `end` and displacement `w`, recover `start` such that `start ⊕ w = end`. Two independent obstacles make this false.

First, TumblerAdd is many-to-one — the ASN states this explicitly with examples showing `[1,1] ⊕ [0,2] = [1,1,5] ⊕ [0,2] = [1,1,999] ⊕ [0,2] = [1,3]`. The start's sub-structure below the action point is destroyed by tail replacement. No operation on `(end, w)` alone can recover it.

Second, even setting aside information loss, TumblerSub's formula acts at the wrong position. TumblerAdd acts at `actionPoint(w)` — the first nonzero component of the displacement. TumblerSub acts at `zpd(a, w)` — the first zero-padded divergence between the two operands. These differ whenever the end position and the displacement first disagree before the displacement's action point, which is the common case (the end position typically has nonzero leading components while the displacement has leading zeros).

Counterexample: `start = [1, 2]`, `w = [3]` (action point 1). `end = start ⊕ w = [4]`. Attempting recovery: `end ⊖ w = [4] ⊖ [3]`, zpd = 1, result = `[1]`. Actual start was `[1, 2]`.

Counterexample 2: `start = [3, 2, 1]`, `w = [0, 5]` (action point 2). `end = [3, 7]`. Attempting recovery: `[3, 7] ⊖ [0, 5]`, zpd = 1 (since `3 ≠ 0`), result = `[3, 7]`. Actual start was `[3, 2, 1]`. The subtraction acts at position 1 instead of position 2 and returns the end position unchanged.

The formula is correct for its actual usage in the displacement identities section — computing displacements between two positions (`b ⊖ a`) — but the narrative describes a different operation (inverting TumblerAdd) that the formula does not and cannot perform.

**What needs resolving**: The introductory description of TumblerSub must describe what the operation actually computes, not an inverse relationship with TumblerAdd that does not hold. The operation computes a component-wise difference at the first point of (zero-padded) divergence — this is the operation used downstream (e.g., in D0 as `b ⊖ a`), and the description should match that use.
