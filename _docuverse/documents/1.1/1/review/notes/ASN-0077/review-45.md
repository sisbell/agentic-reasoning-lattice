# Review of ASN-0077

## REVISE

### Issue 1: Misnamed foundation claim LP11
**ASN-0077, O14 and worked example (Σ₁ → Σ₁')**: "the projection-level counterpart of this rebinding is recorded as LP11 (**ReorderingRebinding**, ASN-0098)"
**Problem**: Foundation ASN-0098's LP11 is named **ReorderingBijection**, not "ReorderingRebinding". The citation convention used throughout (`LabelID (FoundationClaimName, ASN-XXXX)`) presents the parenthetical as the foundation claim's name, so this is a factual misreference appearing twice (O14 and the worked-example K.μ~ paragraph).
**Required**: Rename both occurrences to `LP11 (ReorderingBijection, ASN-0098)`.

### Issue 2: Dangling reference to non-existent S7c
**ASN-0077, singleton I-span edge case**: "S7c supplies only `#E(a) ≥ 2`, not equality, and the present ASN's pointwise origin development (O0) is built precisely to avoid such closure."
**Problem**: ASN-0036 has no claim S7c (its S-series is S0–S5, S7, S7a, S7b, S7d, S8…). The fact `#E(a) ≥ 2` for content addresses is supplied by ASN-0047 (`C1b`, as the `b_C/b_L` note records: "content addresses have `#E ≥ 2` (C1b)"), not by ASN-0036. The reference cannot be discharged as written.
**Required**: Cite the correct foundation claim (C1b, ASN-0047) for `#E(a) ≥ 2`, or correct the label if a different claim was intended.

### Issue 3: J4 range guarantee misstated
**ASN-0077, "Direct resolution through transclusion" (O4 motivation)**: "J4 (ForkComposite, ASN-0047) propagates I-address ranges through forks by the range-inclusion guarantee `ran(M'(d_new)) ⊆ ran(M(d_src)|_{V_{s_C}(d_src)})`"
**Problem**: Foundation J4's derived consequence is the *equality* `ran(M'(d_new)) = ran(M(d_op)|_{V_{s_C}(d_op)})`, where `d_op` is the content-source operand. In J4's `k = 0` sub-case `d_op = prev_version = max(dom(A_v(d_src)))`, which is **not** `d_src`. The cited set `ran(M(d_src)|…)` is therefore the wrong source in that sub-case. The misstatement is in motivational prose and does not enter O4's formal derivation, but it misattributes a foundation guarantee.
**Required**: State the guarantee over `d_op` (matching J4's equality), or restrict the claim to the `k = 1` sub-case where `d_op = d_src`.

## OUT_OF_SCOPE

### Topic 1: Cross-subspace I-span origin reporting
The I-span lift silently drops link addresses (`⟦σ⟧ ∩ dom(C)` excludes `dom(L)`), acknowledged as Open Question 1. Defining a combined-subspace I-span origin operation is new territory, correctly deferred — not an error here.

### Topic 2: Historical-containment operation (from Σ.R)
The ASN explicitly excludes provenance-based historical containment and leaves the coupling invariants as an open question. This belongs to a future ASN.

VERDICT: REVISE
