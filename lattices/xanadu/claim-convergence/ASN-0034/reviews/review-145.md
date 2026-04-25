# Cone Review — ASN-0034/T1 (cycle 8)

*2026-04-17 10:17*

### NAT-order site-count preamble disagrees with its own itemization (14 ≠ 13)

**Foundation**: NAT-order (NatStrictTotalOrder).

**ASN**: T1 (LexicographicOrder), Depends enumeration. The preamble asserts: *"the proof invokes the strict-total-order structure of `<` on ℕ at **thirteen distinct sites**, each a clause of NAT-order's Axiom."* The itemization that follows breaks down as:

- *"Irreflexivity is invoked **once**, at part (a) Case (i)"* — 1 site.
- *"Trichotomy is invoked **seven times**:"* — 7 sites (part (a) Case (ii); Case 2's opening step; Case 2's `k'=k` rebuttal via case (i); Case 2's `k'=k` rebuttal via case (ii); Case 2's `k'<k` rebuttal via case (ii); Case 3's opening step; sub-case (i, ii)).
- *"Transitivity is invoked **six times**:"* — 6 sites (Case `k₂<k₁` under hypothetical case-(ii) of `b<c`; Case `k₂<k₁` under case-(i) of `a<b`; sub-case (i, i); sub-case (ii, ii); Case 3's `m<n` branch rebuttal; Case 3's `n<m` branch rebuttal).

**Issue**: 1 + 7 + 6 = 14, not 13. The preamble total contradicts the itemized count by one site. Under T0's citation convention ("each proof cites only the ℕ facts it actually uses"), the enumeration functions as an auditable inventory; a preamble total that disagrees with the explicit clause-by-clause breakdown makes the inventory unverifiable without the reader first deciding which number to trust. The parallel totals for NAT-addcompat ("eight distinct sites" matching 8 itemized) and NAT-discrete ("three distinct sites" matching 3 itemized) pass this check, so the discrepancy is isolated to NAT-order and reads as an arithmetic slip rather than an intentional grouping.

**What needs resolving**: Either correct the preamble to "fourteen distinct sites" to match the 1+7+6 itemization, or identify which itemized site should be folded into another (for example, if two trichotomy invocations at the same pair `(m,n)` are intended to count as one under the declared per-instance convention) and restate both the preamble total and the clause-specific count so the arithmetic closes.

## Result

Cone not converged after 8 cycles.

*Elapsed: 4355s*
