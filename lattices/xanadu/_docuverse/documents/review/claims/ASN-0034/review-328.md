# Cone Review — ASN-0034/ReverseInverse (cycle 8)

*2026-04-18 20:49*

### Step 1's divergence sub-case `aₖ > wₖ` consumes ZPD's case-split and minimality clauses without citing ZPD for that site

**Foundation**: ZPD (ZeroPaddedDivergence) — case-split clause ("`zpd(a, w)` is defined iff the padded sequences disagree somewhere") and minimality clause ("when defined, `zpd(a, w)` is the least such disagreement position").

**ASN**: ReverseInverse, Step 1, divergence sub-case: "If `aₖ > wₖ`, then `k` is the first divergence, and TumblerSub produces `yᵢ = 0` for `i < k`, `yₖ = aₖ - wₖ > 0` … and no components beyond `k` (since `L = k` by the sub-case (α) dispatch above)."

**Issue**: For TumblerSub's three-region production rule (`rᵢ = 0` for `i < k`, `rₖ = aₖ − wₖ`, tail copy beyond) to apply at the named `k`, TumblerSub's Definition requires `k = zpd(a, w)`. Establishing that identity consumes ZPD at two coupled steps: (a) ZPD's case-split clause affirmatively — the padded sequences disagree at position `k` (since `aₖ > wₖ` entails `aₖ ≠ wₖ`), so `zpd(a, w)` is defined; and (b) ZPD's minimality clause — no position `i < k` is a padded-disagreement (both `aᵢ = wᵢ = 0` by the zero-prefix precondition and action-point definition), so the named `k` is the least disagreement position, fixing `k = zpd(a, w)`. ReverseInverse's ZPD Depends entry enumerates only "*Step 1's equality sub-case `aₖ = wₖ`* consumes ZPD's case-split clause … contrapositively" — the *divergence* sub-case's affirmative case-split + minimality use is not enumerated. TA4's sibling Depends entry for ZPD explicitly lists both a Case 1 minimality use (the divergence-branch identification `k = zpd(r, w)`) and a Case 2 case-split use (the no-divergence-branch identification), so the per-site convention ReverseInverse otherwise follows requires the divergence-branch citation here too; without it, the Y3b assertion `yₖ = aₖ - wₖ` (which TumblerSub's divergence-branch output can only supply at a zpd-identified position) is unsourced for the `k = zpd(a, w)` premise TumblerSub's Definition consumes.

**What needs resolving**: Either expand Step 1's divergence sub-case with an explicit ZPD citation (case-split affirmatively to conclude `zpd(a, w)` defined, minimality to identify `k = zpd(a, w)`) and add a corresponding per-site entry to the ZPD Depends block paralleling TA4's Case 1 minimality site, or articulate why the divergence sub-case's `k = zpd(a, w)` identification is exempt from the per-step discipline the equality sub-case and TA4's sibling entry both enforce.

## Result

Cone not converged after 8 cycles.

*Elapsed: 4426s*
