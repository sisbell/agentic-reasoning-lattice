# Review of ASN-0043

I traced the load-bearing proofs (PrefixSpanCoverage in both inclusion directions with all boundary cases, the L9 ghost-type construction across Cases A/B, FSP's per-invariant coverage, FSE, and the worked-example arithmetic), and checked the anti-bloat patterns flagged for this note. The note is sound and complete; I have no REVISE items.

## REVISE

None.

## OUT_OF_SCOPE

None to flag — the note confines itself to state (`Σ.L`), invariants (L0–L14, L-fin), and structural lemmas; the operations and discovery topics listed under Scope appear only as future-work entries in Open Questions, not as claims.

### Verification notes (why this converges)

- **PrefixSpanCoverage** establishes `coverage({(x, δ(1,#x))}) = {t : x ≼ t}` by mutual inclusion with every T1 case handled: (⊇) splits on `#t = m` (T3 equality) vs `#t > m` (T1(ii)); (⊆) splits on `x = t`, T1(ii) proper-prefix, and T1(i) divergence with the `k < m` and `k = m` (including `t_m = shift_m`) sub-cases each driven to contradiction. No skipped case.
- **L9** discharges all of FSP's h1–h3 constructively. Case A builds the chain `inc(d',2)`→sweep→`inc(·,1)` with TA5a side-conditions checked at each step and freshness from the empty-prior-allocations hypothesis; Case B routes through FSE. The empty-from/empty-to padded payload `(∅, ∅, {(g,·)}, ∅,…,∅)` satisfies L3 (only slot 3 constrained), and the higher-arity quantifier `(A N ≥ 3)` is genuinely covered.
- **FSP** verifies every member of the declared state-local list (L0, L1, L1a, L1b, L1c, L3, L5, L6, L14, L14a, L-fin, S0–S3, S7a/b/d, S8-fin, S8a, S8-depth, D-CTG/MIN/SEQ); ASN-0036 theorems over `M` (e.g. S8) follow since `Σ'.M = Σ.M`. The L1c bullet derives both strong conjuncts (`k₁=2`, `#tᵢ > #s`) from the seed-equals-home constraint, matching the prior reviser ruling.
- **Worked example** arithmetic checks out, including the non-trivial Step-6 coverage equality: `[g,g') ∪ [g',h) = [g,h) = coverage({(g, δ(2,8))})` with `g' = shift(g,1)`, exhibiting L8's coverage-vs-decomposition distinction with `Θ_split ≠ Θ_single`.

The three previously declined findings (PrefixSpanCoverage promotion, L1b grounding, FSP/L1c strength) remain correctly addressed in the current text; I did not re-surface variants.

META: not applicable — the note specifies abstract state, invariants, and address-structure guarantees, not implementation mechanics.

VERDICT: CONVERGED
