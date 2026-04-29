# Regional Review — ASN-0034/TA5a (cycle 1)

*2026-04-23 01:47*

### Missing NAT-card dependency in TA5a's zero-count arithmetic
**Class**: REVISE
**Foundation**: TA5a (IncrementPreservesT4), Depends slot
**ASN**: TA5a proof cases k = 0, 1, 2: "Therefore `zeros(t') = zeros(t)` and no new adjacencies arise" (k = 0), "Zero count unchanged: `zeros(t') = zeros(t)`" (k = 1), "So `zeros(t') = zeros(t) + 1`" (k = 2).
**Issue**: `zeros(·)` is defined in T4 via the cardinality operator `|·|` grounded in NAT-card. The three equalities above are claims about how cardinality of the zero-index subset behaves when the underlying sequence is modified (position overwritten, position appended as non-zero, position appended as zero). Each requires NAT-card's enumeration characterisation to lift "same set" or "set extended by one element" to "same cardinality" or "cardinality + 1". NAT-card is not in TA5a's Depends list, and the proof states the cardinality identities without citing the axiom that licenses them.
**What needs resolving**: Declare NAT-card in TA5a's Depends slot and justify each cardinality claim at its use site — explicitly relating the zero-index subset of `t'` to that of `t` under each increment branch before invoking the equality or successor-relation on the counts.

### k - 1 ≥ 2 not walked from k ≥ 3
**Class**: REVISE
**Foundation**: TA5a (IncrementPreservesT4), case `k ≥ 3`
**ASN**: "By NAT-sub, `k - 1 ∈ ℕ` and `k - 1 ≥ 2`, so `t'_{#t+1} = t'_{#t+2} = 0`."
**Issue**: `k - 1 ∈ ℕ` follows from NAT-sub's conditional closure at `k ≥ 1` (implied by `k ≥ 3`). But `k - 1 ≥ 2` does not follow from a single NAT-sub clause: NAT-sub supplies strict monotonicity (`m < n ⟹ m − p < n − p`) and right telescoping (`(m + n) − n = m`), but no weak monotonicity `m ≤ n ⟹ m − p ≤ n − p`. The antecedent `k ≥ 3` decomposes via NAT-order into `k = 3` (where right telescoping at `(2, 1)` gives `3 − 1 = 2`, hence `k − 1 = 2`) and `k > 3` (where strict monotonicity at `(3, k, 1)` gives `3 − 1 < k − 1`, and right telescoping rewrites the left side to `2`). The proof compresses this two-branch derivation into a single appeal to NAT-sub.
**What needs resolving**: Walk the two sub-cases explicitly, or cite the specific NAT-sub clauses (right telescoping plus strict monotonicity, combined with NAT-order's trichotomy on `k ≥ 3`) that together yield `k − 1 ≥ 2`.

### TA5a does not walk all four T4 conditions per case
**Class**: OBSERVE
**Foundation**: TA5a (IncrementPreservesT4)
**ASN**: Cases `k = 0`, `k = 1`, `k = 2` each check boundary `t'_{#t'} ≠ 0` and no-adjacency, but none explicitly verifies T4(iii) `t'_1 ≠ 0`.
**Issue**: The preservation of `t'_1 ≠ 0` is trivial (TA5(b) gives `t'_1 = t_1`, and T4(iii) supplies `t_1 ≠ 0`), but the four-condition enumeration opening the proof promised all four would be checked. Skipping one is the pattern the "walk every case" discipline cautions against, even when the skipped case is immediate.

### TA5 case k = 0 appeals to sig(t) ≤ #t without citing TA5-SIG's range guarantee at the use site
**Class**: OBSERVE
**Foundation**: TA5 (HierarchicalIncrement), Verification of (a), case `k = 0`
**ASN**: "Since `j = sig(t) ≤ m = #t = #t'`, both tumblers have a component at `j`."
**Issue**: The inequality `sig(t) ≤ #t` is a range guarantee of TA5-SIG (cited by name only in TA5-SigValid's proof). TA5 declares TA5-SIG as a dependency but does not surface which clause of TA5-SIG is invoked at this step. A reader tracking the dependency chain must reconstruct that the range guarantee — not the definitional formula for `sig(t)` — is what licenses this inequality.

VERDICT: REVISE
