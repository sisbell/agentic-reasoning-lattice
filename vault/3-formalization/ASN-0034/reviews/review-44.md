# Cone Review — ASN-0034/ReverseInverse (cycle 1)

*2026-04-14 09:14*

### TumblerAdd omits `a ⊕ w ≥ w`, leaving TA4's invocation of TumblerSub with an undischarged precondition

**Foundation**: TumblerAdd postconditions; TumblerSub precondition `a ≥ w (T1)`
**ASN**: TA4 (PartialInverse), Step 2: *"By TumblerSub, subtraction scans r and w for the first divergence"*
**Issue**: TumblerAdd exports three postconditions: `a ⊕ w ∈ T`, `#(a ⊕ w) = #w`, and `a ⊕ w > a`. TA4 Step 2 invokes TumblerSub on `(r, w)` where `r = a ⊕ w`, but TumblerSub's stated precondition is `a ≥ w (T1)` — i.e., the minuend must dominate the subtrahend in T1 ordering. The proof never establishes `r ≥ w`. It proceeds directly to case analysis on the divergence point and verifies component-level non-negativity within each case, but the formal T1-ordering obligation is never discharged at the call site.

The root cause is upstream: `a ⊕ w ≥ w` is a general consequence of TumblerAdd's construction — for `i < k`, `r_i = a_i ≥ 0 = w_i`; at `k`, `r_k = a_k + w_k ≥ w_k`; for `i > k`, `r_i = w_i` — yielding `r ≥ w` by T1 in all cases. TumblerAdd's text even identifies the three exported results as "load-bearing for subsequent properties," but this fourth result, equally load-bearing (TA4 depends on it), is neither stated nor proved.

By contrast, ReverseInverse's Step 3 explicitly constructs the proof that `y ⊕ w > w` before invoking TA3-strict, correctly discharging the same kind of obligation. The asymmetry between the two proofs makes the gap in TA4 visible.

**What needs resolving**: TumblerAdd must export `a ⊕ w ≥ w` as a postcondition (with proof from the construction), and TA4 Step 2 must cite it to discharge TumblerSub's precondition before proceeding to the divergence case analysis.
