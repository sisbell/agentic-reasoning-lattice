# Review of ASN-0034

## REVISE

### Issue 1: T9 cites wrong property for strict increase of `inc`

**ASN-0034, T9 (Forward allocation)**: "Since `inc` produces a strictly greater tumbler at each step (TA-strict), it follows that within each allocator's sequential stream, new addresses are strictly monotonically increasing"

**Problem**: TA-strict states `(A a ∈ T, w > 0 : a ⊕ w > a)` — a property of tumbler *addition* (`⊕`). The property that `inc(t, k)` produces a strictly greater tumbler is TA5(a): `t' > t`. These are properties of distinct operations (`⊕` vs `inc`); `inc` is defined independently and is not a special case of `⊕`. A reader verifying the derivation of T9 from TA-strict would find a statement about addition, not increment, and would be unable to complete the verification without recognizing the intended reference.

**Required**: Change "(TA-strict)" to "TA5(a)" in the T9 derivation.

### Issue 2: Worked example mislabels position 1 as "subspace identifier"

**ASN-0034, Worked example (TA4 round-trip failure)**: "The subtraction is a no-op — it finds the divergence at the subspace identifier, not at the action point."

**Problem**: The computation shows the divergence at position 1, where the minuend has value 1 and the subtrahend has value 0. Position 1 of `a₂ = [1,0,3,0,2,0,1,2]` is the **node/server field** (value 1), not the subspace identifier. The subspace identifier is defined earlier in the ASN as the first component of the element field — position 7 in this address (also value 1, coincidentally). The computation is correct; the label identifying *what* is at position 1 is wrong. The final sentence of the paragraph ("the subtraction algorithm's divergence-discovery mechanism is misled by nonzero prefix components") gives the correct explanation.

**Required**: Replace "at the subspace identifier" with "at the node field" or "at position 1 (the first nonzero prefix component)."

## OUT_OF_SCOPE

None beyond what the ASN already identifies in its Open Questions and Scope sections.

VERDICT: REVISE
