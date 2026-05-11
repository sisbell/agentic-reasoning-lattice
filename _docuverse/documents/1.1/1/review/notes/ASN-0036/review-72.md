# Review of ASN-0036

## REVISE

### Issue 1: T4 cited as "FieldSeparatorConstraint" — foundation canonical name is "HierarchicalParsing"
**ASN-0036, S7 proof, S7 contract, S7b preconditions, S8a preconditions, S8a proof, S8a contract, D-CTG-depth proof**: Citations of the form "T4 (FieldSeparatorConstraint, ASN-0034)" recur throughout.
**Problem**: Foundation ASN-0034 names T4 "HierarchicalParsing" — that is the canonical Name. The field-segment constraint is one conjunct of T4's content, not its identifier. A reader cross-referencing the foundation will not locate a "FieldSeparatorConstraint" claim, and the substitution invites the impression that the ASN is citing a different T4 from the verified one.
**Required**: Replace "T4 (FieldSeparatorConstraint, ASN-0034)" with "T4 (HierarchicalParsing, ASN-0034)" at every citation site.

### Issue 2: S8 proof uses inc(v, 0) for "v + 1" but the ASN defines v + 1 = shift(v, 1)
**ASN-0036, S8 proof, Coverage step**: "Each v ∈ dom(M(d)) lies in its own singleton's interval: v ≤ v < v + 1, where the right inequality holds because v + 1 = inc(v, 0) > v by TA5(a)."
**ASN-0036, S8 proof, Uniqueness within a subspace**: "By TA5(c), v + 1 = inc(v, 0) satisfies #(v + 1) = m and differs from v only at position m, with (v + 1)_m = v_m + 1."
**Problem**: The V-position notation is defined earlier in the ASN as `v + 0 = v` and `v + k = shift(v, k)` for k ≥ 1, with `shift(v, n) = v ⊕ δ(n, m)` from OrdinalShift. The S8 proof then switches to `inc(v, 0)` from TA5 (HierarchicalIncrement) without bridging the operators. The equivalence `shift(v, 1) = inc(v, 0)` holds for v satisfying S8a (because S8a's positivity forces sig(v) = m, at which inc(v, 0) advances by 1 — matching TumblerAdd's effect at the action point of δ(1, m) by T3), but this equivalence is neither stated nor proved.
**Required**: Either (a) prove the lemma "shift(v, 1) = inc(v, 0) for v satisfying S8a" as a preliminary and then use either notation freely; or (b) replace `inc(v, 0)` with `shift(v, 1)` throughout S8's proof and cite TumblerAdd's postconditions directly — TumblerAdd supplies `a ⊕ w > a`, `#(a ⊕ w) = #w`, and the three-region component formula, so the proof can run entirely via shift without invoking inc.

### Issue 3: S8 proof Case j = m uses t_m ≥ v_m where T1(i) delivers t_m > v_m
**ASN-0036, S8 proof, Uniqueness within a subspace, Case j = m**: "From v ≤ t with first divergence at m: t_m ≥ v_m by T1(i). From t < v + 1 with first divergence at m: t_m < (v + 1)_m = v_m + 1 by T1(i). Since components are natural numbers, v_m ≤ t_m < v_m + 1 forces t_m = v_m. But then t agrees with v at all m components with #t = #v = m, so t = v by T3 — contradicting t ≠ v."
**Problem**: With t ≠ v and v ≤ t established, v < t holds. T1(i) for v < t at first divergence position j = m yields the strict inequality v_m < t_m — i.e., t_m ≥ v_m + 1. The proof writes the weaker t_m ≥ v_m and then routes through t_m = v_m and a T3 application to derive the contradiction. The direct contradiction from the strict bound is one line shorter and does not require T3: t_m ≥ v_m + 1 and t_m < v_m + 1 is empty in ℕ.
**Required**: Tighten "t_m ≥ v_m" to "t_m > v_m" (equivalently t_m ≥ v_m + 1) reflecting what T1(i) actually delivers from v < t, and close the case directly without invoking T3.

### Issue 4: "Treats j generically for any 1 ≤ j ≤ m" overstates the j range
**ASN-0036, S8 proof, Uniqueness within a subspace**: "shared subspace w₁ = v₁ = S gives t₁ = v₁, forcing j ≥ 2; at m = 2 this further forces j = m = 2, leaving only the j = m case below. The two-case argument that follows treats j generically for any 1 ≤ j ≤ m."
**Problem**: In the immediately preceding sentence the proof correctly notes j ≥ 2 within the analysis context (shared subspace forces position-1 agreement). The next sentence then claims generality "for any 1 ≤ j ≤ m". While the case-j-< m argument happens to work for j = 1 too, the analyzed range is 2 ≤ j ≤ m, not 1 ≤ j ≤ m. The mismatched range invites a reader to question whether the j = 1 case is being handled or implicitly excluded.
**Required**: Restate as "treats j generically for any 2 ≤ j ≤ m" to match the j-range established by the preceding shared-subspace reduction.

VERDICT: REVISE
