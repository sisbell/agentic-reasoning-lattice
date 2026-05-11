# Review of ASN-0040

## REVISE

### Issue 1: TA5 citation error in three places

**ASN-0040, B_type proof Case 2**: "The final component of cₘ is positive — c₁ = inc(p, d) has value 1 at position #p + d (TA5(d)), and each sibling increment advances that position by 1 (TA5(c)) — so TA5(c)'s positivity precondition is met. TA5(c) gives `inc(cₘ, 0) ∈ T`."

**ASN-0040, NextAddress proof Case 2**: "By TA5(c), inc(t, 0) is well-defined for any t ∈ T: it preserves the length of t and advances the value at position sig(t) by 1, producing an element of T."

**ASN-0040, Bop well-definedness**: "The sibling increment inc(cₘ, 0) is well-defined by TA5(c), since cₘ has a positive last component..."

**Problem**: TA5 in ASN-0034 has preconditions `t ∈ T, k ≥ 0`. There is no "positivity precondition" in TA5(c). TA5(c) is the postcondition about length preservation and component modification when k = 0 — it does not supply the membership claim `inc(t, 0) ∈ T`. Membership comes from TA5's first (unlabeled) postcondition `t' ∈ T`. The fabricated "positivity precondition" mischaracterizes TA5's contract; the conclusions are correct but the cited reasoning is wrong.

**Required**: Cite TA5's first (unlabeled) postcondition `t' ∈ T` for membership in all three locations. If the positivity argument is intended to justify `sig(cₘ) = #cₘ` (for TA5-SigValid via B10), state that explicitly and route through TA5-SigValid; otherwise remove the extraneous positivity prose.

### Issue 2: Concrete trace omits d = 1 baptism

**ASN-0040, "A baptism traced" section**: Steps 1, 2, 3, 4, 5, 6 all use d = 2.

**Problem**: The trace exercises only level-crossing baptisms (d = 2). Same-level baptism (d = 1) has structurally distinct behavior — TA5(d) appends no intermediate zeros, B5 preserves zeros count rather than incrementing it, and the resulting child sits at the parent's hierarchical level rather than below. The B7 Case 2 verification uses d = 1 streams hypothetically and the Case 3 verification mentions `inc([1], 1) = [1, 1]` parenthetically, but no registered baptism step in the main trace witnesses d = 1.

**Required**: Add a trace step exercising d = 1 (e.g., baptize a sub-document under document [1, 0, 1, 0, 1] producing [1, 0, 1, 0, 1, 1] via `inc([1, 0, 1, 0, 1], 1)`), and verify B5 (zeros preserved), B6 (B6(iii) at d = 1 reduces to zeros(p) ≤ 3), and B1 (contiguous prefix extension) against the result.

## OUT_OF_SCOPE

None — the ASN clearly demarcates its scope and defers ownership, content storage, and the parent-prerequisite question to forward requirements without entangling them in the registry-level invariants.

VERDICT: REVISE
