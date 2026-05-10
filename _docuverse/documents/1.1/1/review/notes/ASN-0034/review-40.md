# Proof Verification: TumblerSub

I need to verify the TumblerSub property section, including its definition, the TA1/TA1-strict verification, the TA3/TA3-strict verification, and the TA4 cancellation proof.

**Checking precondition completeness, case coverage, postcondition establishment, formal contracts, and dependencies.**

The TumblerSub definition is well-formed. The TA1/TA1-strict verification within the property section is sound — the three-case analysis on `k` vs `j = divergence(a, b)` is exhaustive and each case correctly establishes its conclusion. The TA3-strict proof correctly eliminates Case 0 via equal-length.

However, in the **TA3 verification** (property section version), there is a gap in the transition from Case 0a to Cases 1–3. The proof states:

> For the remaining cases, `a < b` by T1 case (i) and `a` is not zero-padded-equal to `w`, so `dₐ = divergence(a, w)` is well-defined. Let `d_b = divergence(b, w)` (under zero-padding).

The proof then case-splits on the ordering of `dₐ` vs `d_b`. But it never establishes that `d_b` is well-defined — i.e., that `b` is **not** zero-padded-equal to `w`. The three-way case split (`dₐ = d_b`, `dₐ < d_b`, `dₐ > d_b`) is only valid when both values exist.

The canonical TA3 proof in the dependencies (Sub-case B1→B2 transition) fills exactly this gap with an explicit argument: if `b` were zero-padded-equal to `w`, then at position `dₐ` we'd have `a_{dₐ} > w_{dₐ} = b_{dₐ}` (since `a ≥ w` forces `a_{dₐ} > w_{dₐ}` at the divergence), while `aᵢ = wᵢ = bᵢ` for all `i < dₐ`, giving `a > b` by T1 — contradicting `a < b`. The property section's proof omits this argument entirely.

```
RESULT: FOUND

**Problem**: The TA3 proof in the property section assumes `d_b = divergence(b, w)` is well-defined without justification. At the transition "For the remaining cases... Let `d_b = divergence(b, w)` (under zero-padding)", the proof does not rule out the possibility that `b` is zero-padded-equal to `w`, which would make `d_b` undefined and invalidate the subsequent three-way case split on `dₐ` vs `d_b`. The canonical TA3 proof in the dependencies (between Sub-cases B1 and B2) includes the necessary contradiction argument; the property section's version omits it.

**Required**: Between Case 0a and the "remaining cases" paragraph, add: "We show `d_b` is well-defined. If `b` were zero-padded-equal to `w`, then since `dₐ` exists, `a_{dₐ} > w_{dₐ}` (from `a ≥ w` at the first padded divergence) and `w_{dₐ} = b_{dₐ}` (from `b`'s zero-padded equality with `w`), giving `a_{dₐ} > b_{dₐ}`. At all positions `i < dₐ`, `aᵢ = wᵢ = bᵢ`. By T1 case (i), `a > b` — contradicting `a < b`. So `b` is not zero-padded-equal to `w` and `d_b` is well-defined."
```
