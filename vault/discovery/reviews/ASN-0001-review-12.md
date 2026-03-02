# Review of ASN-0001

## REVISE

### Issue 1: TA3 is falsified by a counterexample involving prefix-related operands with zero-padding

**ASN-0001, TA3 and its proof**: "If `a < b`, `a ≥ w`, and `b ≥ w`, then `a ⊖ w < b ⊖ w`."

**Problem**: The strict form of TA3 is false for the constructive definition of `⊖`. Counterexample:

```
a = [1, 2],  b = [1, 2, 0],  w = [0, 1, 0]

a < b:  [1, 2] is a proper prefix of [1, 2, 0] → T1 case (ii) → a < b.  ✓
a ≥ w:  pad a to [1, 2, 0]; compare with [0, 1, 0]; diverge at 1: 1 > 0.  ✓
b ≥ w:  [1, 2, 0] vs [0, 1, 0]; diverge at 1: 1 > 0.  ✓

a ⊖ w:  pad a → [1, 2, 0].  Scan vs [0, 1, 0]: diverge at pos 1.
         Result: [1-0, 2, 0] = [1, 2, 0].

b ⊖ w:  pad w → [0, 1, 0].  Scan vs [0, 1, 0]: diverge at pos 1.
         Result: [1-0, 2, 0] = [1, 2, 0].

a ⊖ w = b ⊖ w = [1, 2, 0].   Not strictly less.  ✗
```

The mechanism: when `a` is a proper prefix of `b`, `b` extends `a` with zeros, and `#w ≥ #b`, the zero-padding of `a` to `max(#a, #w)` produces the same padded representation as `b` padded to `max(#b, #w)`. Both subtractions receive identical operands and produce identical results.

The proof's Case 0 claims "a ⊖ w is strictly shorter than b ⊖ w and is a prefix of it" for the sub-case `max(#a, #w) < max(#b, #w)`. This sub-case excludes the counterexample (where `max(#a, #w) = max(#b, #w) = 3`). But the second sub-case ("If `max(#a, #w) = max(#b, #w)`, then `#a < #b ≤ #w`") asserts that "zero-padding makes `a` and `b` differ at position `#a + 1`." This is false when `b_{#a+1} = 0` — the padding of `a` at that position is also 0, so they agree.

The editing use case is not affected: ordinal shifts operate on single-component tumblers, which cannot stand in a prefix relationship (same-length operands with different values diverge at position 1). But TA3 as stated claims to hold for all of T.

**Required**: Either (a) weaken TA3 to `a ⊖ w ≤ b ⊖ w` (weak order preservation, parallel to TA1), with a strict variant conditioned on `#a = #b` or on the operands not being prefix-related after zero-padding; or (b) add a precondition excluding the degenerate case; or (c) restrict the claim to same-length operands and state the general form as weak. The proof of the Reverse Inverse corollary, which invokes TA3 for the contradiction argument, must be re-verified against whichever fix is adopted — it applies TA3 to operands `a` and `y ⊕ w` which satisfy `#a = #y = k = #w` (the TA4 precondition), so same-length operands, and the strict form holds in that case.

### Issue 2: TA3 proof Case 0 contains an incorrect intermediate claim

**ASN-0001, TA3 verification, Case 0**: "Since `aᵢ = bᵢ` for all `i ≤ #a`, the results agree on positions `1, ..., max(#a, #w)`."

**Problem**: This claim is false when the divergence point `d ≤ #a` and there exist positions `d < i ≤ max(#a, #w)` where `i > #a`. At such positions, `a ⊖ w` copies from padded `a` (giving 0) while `b ⊖ w` copies from `b` (which may have nonzero components). Concrete example: `a = [3, 2]`, `b = [3, 2, 5]`, `w = [1, 1, 7]`. Divergence at position 1 for both. At position 3: `(a ⊖ w)₃ = 0` (padded) but `(b ⊖ w)₃ = 5` (from `b`). The results agree on positions `1, ..., #a` (here, 1 and 2), not on `1, ..., max(#a, #w)` (here, 1, 2, and 3). The conclusion `a ⊖ w < b ⊖ w` still holds in this sub-case (the first disagreement past `#a` has `0 < b_i`), but the stated reasoning is wrong.

**Required**: Rewrite Case 0 to correctly identify that the results agree on positions `1, ..., #a`, not `1, ..., max(#a, #w)`. Then argue the conclusion from the behavior at positions beyond `#a`, handling all sub-cases (including the counterexample from Issue 1 where the conclusion degrades to equality).

### Issue 3: TA3 proof omits the case `a = w`

**ASN-0001, TA3 verification**: "Let `dₐ = divergence(a, w)` and `d_b = divergence(b, w)` (under zero-padding). Three cases arise from the relationship between `dₐ` and `d_b`."

**Problem**: When `a = w` (after zero-padding), `dₐ` does not exist — there is no divergence. The three-case analysis (`dₐ = d_b`, `dₐ < d_b`, `dₐ > d_b`) presupposes that `dₐ` is defined. The case `a = w` is consistent with the preconditions: `a < b`, `a ≥ w` (as equality), `b ≥ w` (since `b > a = w`).

In this case `a ⊖ w` is the zero tumbler (by the subtraction definition), and `b ⊖ w` has a positive component at `d_b` (since `b > w`). The conclusion `a ⊖ w < b ⊖ w` holds, but the proof never shows it.

**Required**: Add a preliminary case handling `a = w` before the three-case analysis, or restructure so that `dₐ` undefined is handled. The argument is one sentence: `a ⊖ w` is the zero tumbler, `b ⊖ w` is positive (since `b > w` gives a positive component at the divergence), and zero tumblers are less than positive tumblers under T1.

## DEFER

### Topic 1: Span intersection and splitting semantics
**Why defer**: The ASN defines spans (T12) but does not formalize span intersection, splitting, or the conditions under which a span `(s, ℓ)` can be decomposed into sub-spans. These are needed for DELETE (which may partially overlap a span) and for link endset computation, but they belong to the operations ASN, not to the tumbler algebra.

### Topic 2: Crash recovery and allocation counter durability
**Why defer**: The ASN's open questions include "Must allocation counter durability across crashes be a global-history property or only a per-session property?" This is a systems-level question about the recovery protocol, not a property of the abstract algebra. It belongs in an ASN on system liveness or fault tolerance.

### Topic 3: V-space position representation — full tuple vs ordinal extraction
**Why defer**: The worked example demonstrates that `⊖` applied to full V-positions `[N, x]` with displacement `[0, n]` finds the wrong divergence point. The resolution — arithmetic on ordinals only, with the subspace identifier as context — is stated but not formalized as a representation invariant. A future ASN on INSERT/DELETE operations should formalize how V-positions are decomposed before arithmetic is applied.

VERDICT: REVISE
