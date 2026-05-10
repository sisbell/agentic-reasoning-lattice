# Review of ASN-0084

## REVISE

### Issue 1: Worked-example I-addresses violate S7b (element-level requirement)

**ASN-0084, Worked Example (3-Cut Pivot)**: "M(d)([1,1]) = 3.0.1.0.1.1 (I-address A)"

**Problem**: The I-address `3.0.1.0.1.1` is the tumbler `[3, 0, 1, 0, 1, 1]`, which has `zeros(t) = 2` — a document-level address by T4c. S7b (ASN-0036) requires every I-address in `dom(Σ.C)` to satisfy `zeros(a) = 3` (element-level). Every I-address in both worked examples has this defect: `3.0.1.0.1.1`, `3.0.1.0.1.2`, `3.0.1.0.1.3`, `5.0.2.0.1.1`, `5.0.2.0.1.2`, `7.0.1.0.1.1`, `3.0.1.0.1.4` — all have exactly two zeros and are therefore document-level tumblers, not element-level.

As a consequence, the origin labels are also wrong. The example writes "origin 3.0.1" and "origin 5.0.2", which parse as `[3, 0, 1]` (zeros = 1, user-level) and `[5, 0, 2]` (zeros = 1, user-level). The `origin` function from ASN-0036 returns a document-level tumbler (zeros = 2).

The rearrangement proofs are structurally correct regardless of I-address depth — the permutation mechanics and block transformations do not depend on the hierarchical level of I-addresses — but worked examples exist to verify postconditions against explicit values that satisfy the invariants, and these values do not.

**Required**: Every I-address needs a third zero separator before the element field. For example, `3.0.1.0.1.1` should be `3.0.1.0.1.0.1.1` = `[3, 0, 1, 0, 1, 0, 1, 1]` (node=[3], user=[1], document=[1], element=[1,1], zeros=3). Origins should be the corresponding document-level tumblers: "origin 3.0.1.0.1" (not "3.0.1") and "origin 5.0.2.0.1" (not "5.0.2"). All I-addresses and origin references in both worked examples must be corrected.

## OUT_OF_SCOPE

### Topic 1: Generalization beyond depth-2 V-positions
**Why out of scope**: The ASN explicitly restricts to `#v = 2` and notes that generalization to deeper ordinals is "structurally identical by D-CTG-depth." This is plausible but unproved; establishing the general case (including adjusting CS4 to `#cᵢ = m` and verifying the commutativity proof generalizes) is new work beyond this ASN's scope.

VERDICT: REVISE
