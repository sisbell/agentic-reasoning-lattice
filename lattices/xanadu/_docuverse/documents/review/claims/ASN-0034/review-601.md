# Cone Review — ASN-0034/T10a (cycle 5)

*2026-04-26 05:01*

### T4(ii) discharge in cases `k = 1` and `k = 2` is one-line and elides interior positions
**Class**: REVISE
**Foundation**: T4 (HierarchicalParsing) — T4(ii) on `t'` is `(A i : 1 ≤ i < #t' : ¬(t'ᵢ = 0 ∧ t'ᵢ₊₁ = 0))`, universally quantified
**ASN**: TA5a, Case `k = 1`: "Left-flank `t'_{#t} = t_{#t} ≠ 0` by T4(iv), so no adjacent zeros; boundary `t'_{#t'} = 1 ≠ 0`." And Case `k = 2`: "Left-flank `t'_{#t} = t_{#t} ≠ 0` by T4(iv); right-flank is `1`; boundary `t'_{#t'} = 1 ≠ 0`."
**Issue**: T4(ii) on `t'` ranges over indices `1 ≤ i < #t'` — for `k = 1`, that is `1 ≤ i ≤ #t`; for `k = 2`, that is `1 ≤ i ≤ #t + 1`. The interior range `1 ≤ i < #t`, where adjacency on `t'` follows from TA5(b)'s original-position agreement at `i` and `i + 1` together with T4(ii) on `t`, is not labeled in either case. In `k = 2` the additional boundary index `i = #t + 1` (with pair `(t'_{#t+1}, t'_{#t+2}) = (0, 1)`, falsified at the right conjunct via `1 ≠ 0`) is not explicitly given a T4(ii) discharge — the cryptic phrase "right-flank is `1`" hints at it but is conflated with the T4(iv) clause that follows. By contrast, the previous review cycle explicitly required Case `k = 0`'s T4(ii) to be expanded into the three-way case split on `sig(t) ∉ {i, i+1}`, `i = sig(t)`, `i + 1 = sig(t)`, and the current proof body now does so. The same explicitness standard is not applied to the surface T4(ii) discharges in cases `k = 1` and `k = 2`, leaving the same kind of gap (the interior range and, in `k = 2`, the new appended-zero-adjacency index) that motivated the earlier finding.
**What needs resolving**: Expand the T4(ii) discharge in case `k = 1` to label both branches — interior `1 ≤ i < #t` (TA5(b) agreement at `i` and `i + 1` plus T4(ii) on `t`) and the new boundary index `i = #t` (pair `(t_{#t}, 1)` falsified via T4(iv) on the left or `1 ≠ 0` on the right). Symmetrically expand case `k = 2` to label the interior range, the boundary `i = #t` (pair `(t_{#t}, 0)` falsified by T4(iv)), and the new index `i = #t + 1` (pair `(0, 1)` falsified by `1 ≠ 0`); separate the T4(ii) discharge cleanly from the T4(iv) discharge so the four-conjunct walk is explicit.

### Failure clause cites T4(i) alone for the discrete-value enumeration `zeros(t) ∈ {0, 1, 2, 3}`
**Class**: OBSERVE
**Foundation**: T4 (HierarchicalParsing) — T4(i) is the bound `zeros(t) ≤ 3`; the discrete enumeration `zeros(t) ∈ {0, 1, 2, 3}` is T4's Exhaustion Consequence
**ASN**: TA5a, *Failure* slot: "The Guarantee's iff yields two failure regions on the precondition domain (`t` satisfies T4, so `zeros(t) ∈ {0, 1, 2, 3}` by T4(i); `k ∈ ℕ`)..."
**Issue**: T4(i) supplies the upper bound `zeros(t) ≤ 3` and ranges over `zeros(t) ∈ ℕ` (via NAT-card's codomain). The collapse to the four-element set `{0, 1, 2, 3}` is not T4(i) alone but T4's Exhaustion Consequence `(A t ∈ T : zeros(t) ≤ 3 : zeros(t) ∈ {0, 1, 2, 3})`, which T4 derives explicitly using NAT-zero, NAT-discrete, NAT-order's trichotomy, and NAT-closure's left-identity in addition to the bound. Citing "T4(i)" for the discrete-value enumeration short-circuits the named Consequence T4 exports for exactly this purpose. The reasoning is sound — the Consequence is in scope — but the citation tag is one half of a two-step chain.
**What needs resolving**: (OBSERVE — no revision required.) Replacing the citation "by T4(i)" with "by T4's Exhaustion Consequence (or T4(i) chained with NAT-discrete)" would name the actual axiom slot used.

VERDICT: REVISE
