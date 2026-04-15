# Cone Review — ASN-0034/D0 (cycle 1)

*2026-04-13 19:59*

### Displacement narrative claims unconditional equivalence between "reading off" and TumblerSub, but they diverge when #a > #w

**Foundation**: TumblerAdd result-length identity `#(a ⊕ w) = #w`; TumblerSub result-length identity `#(a ⊖ w) = max(#a, #w)`; T3 (CanonicalRepresentation) — tumblers of different length are distinct.

**ASN**: Displacement identities section (narrative between TumblerSub and D0):
> "Reading off the width: wᵢ = 0 for i < k, wₖ = bₖ − aₖ, wᵢ = bᵢ for i > k where k = divergence(a, b). This is exactly the formula for b ⊖ a from TumblerSub. We write w = b ⊖ a and call it the *displacement from a to b*."

**Issue**: The "reading off" formula produces a tumbler of length `#b = #w` (since `b = a ⊕ w` and TumblerAdd gives `#(a ⊕ w) = #w`). TumblerSub produces `b ⊖ a` with length `max(#a, #b) = max(#a, #w)`. When `#a > #w`, these lengths differ, and the results are distinct tumblers by T3.

Counterexample: `a = [1, 2, 3, 4, 5]`, `w = [0, 0, 7]`. Action point 3 ≤ 5, so `b = a ⊕ w = [1, 2, 10]` with `#b = 3`. The "reading off" correctly recovers `w = [0, 0, 7]`. But TumblerSub computes `[1, 2, 10] ⊖ [1, 2, 3, 4, 5]` by zero-padding to length 5: `zpd = 3`, yielding `[0, 0, 7, 0, 0]`. By T3, `[0, 0, 7] ≠ [0, 0, 7, 0, 0]`.

The claim "This is exactly the formula for b ⊖ a from TumblerSub" is false when `#a > #w` — the formulas agree on components but TumblerSub's `max`-length rule appends trailing zeros that the original displacement does not have. The identification `w = b ⊖ a` then inherits this error, and the term "displacement from a to b" is introduced on a foundation that holds only when `#a ≤ #w`. D0's formal postconditions are correct (they work from TumblerSub's actual result and explicitly flag the `#a > #b` failure case for the reverse direction), but the narrative's unconditional forward-direction claim could mislead any downstream ASN that cites it.

**What needs resolving**: The narrative must qualify the identification: either restrict `w = b ⊖ a` to the case `#a ≤ #w` (under which `max(#a, #w) = #w` and the lengths agree), or acknowledge that `b ⊖ a` extends `w` with trailing zeros when `#a > #w`. D0's round-trip boundary analysis already handles the reverse direction (`a ⊕ (b ⊖ a) ≠ b` when `#a > #b`); the forward direction needs the symmetric treatment.
