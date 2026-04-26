# Cone Review — ASN-0034/TA3 (cycle 4)

*2026-04-26 07:10*

### Sub-case B1 still uses native components at potentially-padding indices
**Class**: REVISE
**Foundation**: (n/a — internal)
**ASN**: TA3 Sub-case B1 ("a is zero-padded-equal to w"):
> "Then `a ⊖ w` is the zero tumbler of length `L_{a,w}`. At position `j`, `wⱼ = aⱼ`, so `bⱼ > wⱼ`. The pair `(b, w)` diverges at or before `j`, making `b ⊖ w` positive."

Case B's witness `j` satisfies `j ≤ #a ∧ j ≤ #b` from T1 case (i) — but **not** `j ≤ #w`. In B1's hypothesis "a is zero-padded-equal to w", the ZPD-level fact is `âᵢ = ŵᵢ` on `1..L_{a,w}`, not a native equality. When `j > #w` (which is possible — e.g. `#a > #w` with `a` consisting of `w` followed by zeros, and `j` in `(#w, #a]`), `wⱼ` is undefined natively and the cited equation `wⱼ = aⱼ` is ill-typed. The downstream inequality `bⱼ > wⱼ` similarly mixes native `bⱼ` (well-defined since `j ≤ #b`) with a non-existent native `wⱼ`.

**Issue**: This is the same native/padded conflation the prior cycle flagged for sub-case A2, repeated here in B1. The conclusion (b ⊖ w is positive, hence b not zero-padded-equal to w) is sound — when `j > #w`, the argument is `âⱼ = aⱼ` (since `j ≤ #a`), `ŵⱼ = 0` (since `j > #w` and `j ≤ L_{a,w}`), and zpd-equality forces `aⱼ = 0`, whence `bⱼ > aⱼ = 0`, witnessing `b̂ⱼ ≠ ŵⱼ` for the (b,w) padding pair (with `j ≤ L_{b,w}` since `j ≤ #b`). The prose collapses this two-case handling into a native-only sentence that is undefined in one of those cases.

**What needs resolving**: Recast B1's argument on padded projections — `âⱼ = ŵⱼ` from a's zero-padded-equality, then case on whether `j ≤ #w` to lift to native or to read `ŵⱼ = 0`. Then derive the disagreement `b̂ⱼ ≠ ŵⱼ` (from `bⱼ > 0` or `bⱼ ≠ wⱼ` as the case dictates) to conclude `(b,w)` is not zero-padded-equal, hence `b ⊖ w` is positive by TumblerSub's exported `Pos` postcondition.

VERDICT: REVISE
