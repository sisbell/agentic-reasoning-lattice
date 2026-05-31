# Review of ASN-0093

I worked through the invariant discharges, the freshness lemmas, the chain-membership induction, and the cross-document disjointness argument. The mathematics is sound: the simultaneous induction is well-founded (no circular dependency between the freshness lemmas, `ChainMembershipForOrigin`, and `StoreT4Validity`), the boundary zero-counts sit correctly at the T4 limits, the anchors are correctly excluded from the stores by `#E = 1`, and the symmetry collapses in L1b/L1c are genuine (content↔link substitution is clean). The one issue I found is an anti-bloat duplication that the note's own collapse-by-reference convention already solves elsewhere.

## REVISE

### Issue 1: L1's K.λ discharge verbatim-duplicates C1's K.α discharge instead of collapsing by reference
**ASN-0093, Inductive-step matrix, L1 (K.λ) cell** vs **C1 (K.α) cell**: The L1 K.λ entry writes out, word-for-word under `a↔ℓ`, the same argument C1's K.α entry already gives:

- C1/K.α: "...`zeros(a) = zeros(a_prev) = 3` by B5a ... B5a's precondition `a_prev_{sig(a_prev)} > 0` is discharged from the T4-validity of `a_prev` (IH via ChainElementT4Validity), which by TA5-SigValid gives `sig(a_prev) = #a_prev` with non-zero terminal component (T4's `t_{#t} ≠ 0`)"
- L1/K.λ: identical text with `ℓ`, `ℓ_prev`, `A_L(d)` substituted.

**Problem**: This is the "two paragraphs say the same thing in different words" pattern (here, the *same* words). It is also internally inconsistent: the very next rows already collapse the parallel — L1b's K.λ cell reads "identical to the C1b K.α discharge above under the content↔link substitution," and L1c's subsequent-emit case reads "Identical to the C1c subsequent-emit case above under the content↔link substitution." L1 is the lone holdout that re-derives instead of referencing. The same redundancy appears in the **SD** row, whose K.α and K.λ cells carry identical text ("Standing consequence of the L0/C1/L1/StoreT4Validity rows at Σ': those premises hold at Σ' by their own rows this step, and the SD invariant statement carries the one T7 derivation").

**Required**: Replace L1's K.λ subsequent-emit text with the shorthand L1b/L1c already use ("identical to the C1 K.α discharge above under the content↔link substitution"). Collapse the duplicated SD cell text into a single statement covering both allocation transitions.

## OUT_OF_SCOPE

### Topic 1: Allocation-event uniqueness as a stated theorem
The substrate proves per-transition freshness (each emission ≠ every prior store entry) and inductively this yields global address uniqueness, but no standalone uniqueness theorem (the analog of ASN-0034 GlobalUniqueness / ASN-0043 L11a) is stated.
**Why out of scope**: The freshness lemmas fully cover what this substrate needs to discharge C0/L12; promoting it to a named cross-store uniqueness theorem is additive packaging, not a correctness gap in this note.

VERDICT: REVISE
