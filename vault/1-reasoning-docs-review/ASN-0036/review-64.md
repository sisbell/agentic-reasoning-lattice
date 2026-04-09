# Review of ASN-0036

## REVISE

### Issue 1: S8 proof — m = 1 cross-subspace gap omits depth ≥ 2 V-positions

**ASN-0036, S8 proof, "Uniqueness across subspaces"**: "So both within-subspace and cross-subspace uniqueness are immediate at m = 1 — singleton intervals for distinct subspaces S₁ ≠ S₂ have distinct sole members [S₁] and [S₂]."

**Problem**: The m = 1 branch proves that no other depth-1 tumbler from a different subspace falls in `[[S₁], [S₁+1])`. But S8-depth constrains depth *within* a subspace, not across subspaces — subspace S₁ could have depth 1 while subspace S₂ has depth 2. The "distinct sole members" argument excludes only depth-1 V-positions from other subspaces; it does not address whether `[S₂, x]` (depth 2, subspace S₂) could fall in `[[S₁], [S₁+1])`.

The gap is real: the interval `[[S₁], [S₁+1])` contains every proper extension of `[S₁]` — by T1(ii), `[S₁] < [S₁, x, ...]`, and by T1(i), `[S₁, x, ...] < [S₁+1]` since the first component `S₁ < S₁+1`. So the interval includes infinitely many tumblers at depth ≥ 2, all with first component S₁. The proof must establish that *only* tumblers with first component S₁ inhabit the interval.

The m ≥ 2 branch does not rescue this. It uses TA5(b) to show `(v+1)₁ = v₁ = S₁`, then applies T5 to conclude every element of `[v, v+1)` extends `[S₁]`. At depth 1, `v+1 = [S₁+1]` does *not* extend `[S₁]` (since `S₁ ≠ S₁+1`), so the T5 precondition `[S₁] ≼ (v+1)` fails — which is precisely why the proof splits into two branches. Neither branch covers the case (v at depth 1, w at depth ≥ 2 from another subspace).

**Required**: Add to the m = 1 branch: Every tumbler t in `[[S₁], [S₁+1])` has `t₁ = S₁`. From `[S₁] ≤ t`: if `t₁ < S₁`, then `t < [S₁]` by T1(i), contradicting `[S₁] ≤ t`; so `t₁ ≥ S₁`. From `t < [S₁+1]`: if `t₁ > S₁`, then `t₁ ≥ S₁+1`, and either `t₁ > S₁+1` giving `t > [S₁+1]` by T1(i), or `t₁ = S₁+1` and `#t = 1` giving `t = [S₁+1]`, or `t₁ = S₁+1` and `#t > 1` giving `t > [S₁+1]` by T1(ii) — all contradicting `t < [S₁+1]`; so `t₁ ≤ S₁`. Combined: `t₁ = S₁`. Therefore no V-position from subspace `S₂ ≠ S₁`, at any depth, falls in the interval.

## OUT_OF_SCOPE

### Topic 1: Canonical maximal span decomposition
**Why out of scope**: S8 proves existence of a finite decomposition via the singleton construction but does not address whether a unique coarsest decomposition (fewest runs) exists. This is already noted in the open questions and belongs in a future ASN on span algebra or arrangement normal forms.

VERDICT: REVISE
