# Review of ASN-0034

## REVISE

### Issue 1: TA3 proof, Case 0, sub-case `a = w` — false positivity claim
**ASN-0034, Verification of TA3, Case 0**: "Since `b > a = w`, we have `b ≥ w` and `b > w`, so `b ⊖ w` is a positive tumbler."
**Problem**: The claim `b > w ⟹ b ⊖ w` is positive is false when `b` extends `w` by only zero-valued components. Counter-example: `b = [1, 0, 3, 0, 0]`, `w = [1, 0, 3]`. Zero-padding `w` yields `[1, 0, 3, 0, 0] = b`, so `b ⊖ w = [0, 0, 0, 0, 0]` — a zero tumbler, not positive. The conclusion `a ⊖ w ≤ b ⊖ w` still holds (shorter zero tumbler < longer zero tumbler by T1 case (ii)), but the stated reasoning does not establish it for this edge case.
**Required**: Split the sub-case. When `b ⊖ w` is positive, the existing TA6 argument applies. When `b ⊖ w` is also a zero tumbler, observe `#(a ⊖ w) = max(#a, #w) = #w < #b = max(#b, #w) = #(b ⊖ w)` (since `#b > #a = #w` in Case 0), making `a ⊖ w` a proper prefix of `b ⊖ w`, hence `a ⊖ w < b ⊖ w` by T1 case (ii).

### Issue 2: TA1/TA1-strict proof preamble — inaccurate claim for prefix divergence
**ASN-0034, Verification of TA1 and TA1-strict**: "Let `j = divergence(a, b)` — the first position where `a` and `b` differ (`aⱼ < bⱼ` since `a < b`)."
**Problem**: When `a` is a proper prefix of `b`, the Divergence definition case (ii) gives `j = min(#a, #b) + 1`, which exceeds both tumblers' shared positions. There is no position `j` at which `aⱼ < bⱼ` — the ordering comes from the prefix rule (T1 case ii), not component comparison. The subsequent case analysis is correct: prefix pairs satisfy `k ≤ min(#a, #b) < j`, so only Case 1 applies, and Case 1 never references `aⱼ` or `bⱼ`. But the preamble asserts a property that does not hold for all pairs with `a < b`.
**Required**: Qualify the preamble to distinguish component divergence from prefix divergence — e.g., "In case (i) of the Divergence definition, `aⱼ < bⱼ`; in case (ii), `j` exceeds both tumblers' shared positions and the ordering follows from the prefix rule." Alternatively, drop the parenthetical entirely and let the case analysis speak for itself.

## OUT_OF_SCOPE

### Topic 1: Span composition operations
**Why out of scope**: The ASN defines individual spans and establishes their well-formedness (T12). Operations on collections of spans — union, intersection, difference, and the algebraic properties of span-sets — are new territory for a future ASN.

### Topic 2: Uniqueness of the tumbler arithmetic model
**Why out of scope**: The ASN proves the constructive definitions of `⊕` and `⊖` satisfy axioms TA0–TA4. Whether these are the unique operations satisfying those axioms (categoricity) is a valid mathematical question but independent of the specification's correctness.

VERDICT: REVISE
