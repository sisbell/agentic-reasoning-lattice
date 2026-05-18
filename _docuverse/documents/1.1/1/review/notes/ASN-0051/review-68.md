# Review of ASN-0051

I worked through the projection/discovery/vitality definitions, every SV claim, the SV6 cross-origin proof, the SV11 partial-survival construction (including the lift schemata and disjoint-pair structural lemma), the worked example, and the wp analysis. The ASN is unusually rigorous — most claims have explicit derivations and concrete witnesses. I found one technical issue worth fixing.

## REVISE

### Issue 1: Case (IV) bound in the four-case structural lemma is too strict

**ASN-0051, SV11 disjoint-pair sub-case (b), Four-case structural lemma**: "*(IV) #y ≠ #e and no prefix relationship holds (different length, non-prefix).* Then y diverges from q_{k₁} at some position p ≤ min(#y, #e) − 1 (a position strictly before either's last)."

**Problem**: The stated bound `p ≤ min(#y, #e) − 1` excludes the realisable case where `#y < #e` and divergence happens at `p = #y` (the last position of the shorter tumbler). Concrete counterexample: let β_{k₁} contain `[3, 1]` and `[3, 2]` (so #e = 2, q_{k₁} = [3]). Take y = [4]. Then `#y = 1 ≠ 2 = #e`; y is not a prefix of any β_{k₁}-element (since y₁ = 4 ≠ 3); no β_{k₁}-element is a prefix of y (since #e > #y). So this is case (IV). Divergence from q_{k₁} is at p = 1 = #y, but the stated bound gives p ≤ min(1, 2) − 1 = 0, which fails. The parenthetical gloss "strictly before either's last" is wrong when y is the shorter tumbler and divergence falls at y's last position.

**Required**: Replace `p ≤ min(#y, #e) − 1` with `p ≤ min(#y, #e − 1)`. This is the correct bound that arises from "divergence between y (length #y) and q_{k₁} (length #e − 1) requires comparison in the overlap range 1..min(#y, #e − 1)". The conclusion (T-linear separation by T1(i)) is unaffected: the proof needs `p ≤ #e − 1` (so q_{k₁} is defined at p, giving uniformity across β_{k₁}) and `p ≤ min(#y, #e)` (so T1(i) applies), both implied by `p ≤ min(#y, #e − 1)`. Drop or rephrase the "strictly before either's last" gloss accordingly.

## OUT_OF_SCOPE

None. The ASN explicitly scopes link-subspace reflexive cases, broader-level (k ≤ p₃) spans, and the link-type and replication topics from the Scope notice to future ASNs, and the deferrals are appropriately handled at each invocation site.

VERDICT: REVISE
