# Review of ASN-0108

I worked through every claim (W0–W11), re-derived the weakest-precondition analysis in W2, the partition induction in W4, and the termination argument in W9a, and checked each concrete walk against its asserted formulas.

## Verification performed

**W2 (wp analysis).** Recomputed both branches. With `After(c,Σ')` beginning at rank `j'+1` where `j' = |{a : κ(a) ≤_K κ(c)}|`: the offset window `[j+1, min(j+N,m')]` coincides with R's target `[j'+1, m']`-prefix iff `j'=j` (nonempty case) or both empty (`j≥m' ∧ j'≥m'`). The stated `wp(resume_offset, R) ≡ j'=j ∨ (j≥m' ∧ j'≥m')` is exact; I confirmed the two asymmetric corners (`j<m'≤j'` and `j'<m'≤j`) both correctly yield `wp = false`. The three-condition strict nesting (membership-identity ⟹ frozen-prefix ⟹ weakest) checks out, with k<j the charitable reading of the middle witness.

**W4 (partition).** The cumulative cut-point induction `W_i = ranks [S_i+1, min(S_{i+1},m)]` is sound for variable `N_i`, and the disjoint/consecutive/exhaustive conclusion holds. The count formula is correctly restricted to the constant schedule.

**W9a count formula.** Verified `⌈m/N⌉ + [N∣m]` against all four boundary walks (m=4→3, m=5→3, m=0→1, N=3/m=2→1), including the N∣0 case firing the `+1` term.

**W9a sufficiency.** The "finite tail inflow + cut-point preservation at each cursor" condition: I traced the no-re-ascension argument (delivered `a` has `κ(a) ≤ κ(c_i) < κ(c_{i+1})`, preserved forward), confirmed the bounded-instantaneous-but-unbounded-inflow counterexample and the zero-inflow-but-cut-point-violation counterexample both defeat termination as claimed, and confirmed clause-2 (tail-order) is genuinely not required.

**Foundation references.** All citations (T1, T8, T9, ASN-0043 L12/L12a/L-fin, ASN-0093 K.λ, ASN-0098 LP13/LP17) are to listed foundation ASNs. No improper cross-ASN reference; no reinvented notation.

**Depth standards.** Non-trivial wp present (W2, and W9/W8 recoverability). Concrete walks present for W2, W5 (both clauses), W6, W8, W9/W9a, including empty-set and N>m boundaries. Derived claims (W6a frame argument, W8 cursor survival, W9a sufficiency) carry explicit derivations.

The deferred topics (satisfaction predicate, multi-document monotone key, progress-sizing companion, orphan-vs-exhaustion disambiguation) are correctly routed to Open Questions rather than smuggled in as claims. The implementation evidence (udanax-green insertion-sort, address vs content-position key) is used to motivate which abstract key satisfies which abstract guarantee — the claims themselves remain implementation-independent, so the ASN has not drifted.

I found no hand-wave, no missing boundary case, no unaddressed invariant conjunct, and no under-derived claim.

VERDICT: CONVERGED
