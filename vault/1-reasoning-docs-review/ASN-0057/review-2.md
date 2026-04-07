# Review of ASN-0057

## REVISE

### Issue 1: Uniqueness of displacement not stated as a corollary

**ASN-0057, Displacement recovery**: "We write w = b ⊖ a and call it the *displacement from a to b*."

**Problem**: The definite article "the" implies that b ⊖ a is the only w satisfying a ⊕ w = b under D1's conditions. The "reading off" argument already proves this informally — it shows that any w with a ⊕ w = b must have wᵢ = 0 for i < k, wₖ = bₖ − aₖ, wᵢ = bᵢ for i > k, which is exactly b ⊖ a. Alternatively, the result follows in one step from D1 + TA-LC: if a ⊕ w = b = a ⊕ (b ⊖ a), then w = b ⊖ a. Either way, the proof is present in spirit but uniqueness is never stated as a result.

**Required**: Add a corollary (e.g., D2): under D1's preconditions, if a ⊕ w = b then w = b ⊖ a. One line of derivation from D1 and TA-LC. This completes the characterization — D1 says b ⊖ a works, the corollary says nothing else does.

## OUT_OF_SCOPE

### Topic 1: Converse round-trip identity

The converse (a ⊕ w) ⊖ a = w does not hold in general. When #a > #w, the subtraction zero-pads w to length #a, producing a result of length #a ≠ #w. Characterizing when the converse holds is a natural companion to D1 but a distinct identity.

**Why out of scope**: New territory — D1 is the forward direction and the ASN treats it completely.

### Topic 2: Displacement beyond TumblerSub

When #a > #b, b ⊖ a has length #a > #b, so a ⊕ (b ⊖ a) ≠ b by T3. However, a displacement of length #b — with the same components as b ⊖ a at positions 1..#b — satisfies a ⊕ w' = b under D0 alone, without the #a ≤ #b restriction. (The proof is identical to D1's: components before k agree, at k the addition recovers bₖ, and the tail copies from w'.) This means displacement recovery succeeds in a wider regime than D1 covers, though the recovering displacement is not the TumblerSub output.

**Why out of scope**: The ASN's stated scope is the identity a ⊕ (b ⊖ a) = b, which it characterizes completely. A generalized displacement operator is new work.

VERDICT: REVISE
