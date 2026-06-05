# Review of ASN-0108

## REVISE

### Issue 1: The offset-cursor weakest precondition is stated strictly stronger than the genuine weakest

**ASN-0108, "The Cursor: Identity, Not Offset" (W2 wp analysis)**: "`wp(resume_offset, R) ≡ ranks 1..j of Match(q, Σ') = the j links already delivered` — *no membership change at or below the cut* between the two calls."

**Problem**: A weakest precondition is, by definition, the weakest. The stated condition is *sufficient* but not *necessary*, so labeling it `wp` is a precision error in the analysis the ASN itself frames as central depth.

The postcondition `R` is single-step: "delivered window = the ≺-least `min(N, |After(c,Σ')|)` of `After(c,Σ')`." The offset resume delivers ranks `[j+1, j+N]` of `Match(q,Σ')`. For these to coincide with `R`, all that is required is that rank `j+1` *begins* `After(c,Σ')` — i.e.

> `|{a ∈ Match(q,Σ') : κ(a) ≤ κ(c)}| = j`

(exactly `j` matching links lie at or below the cursor's key). This count-at-cut condition is *weaker* than "ranks 1..j = the delivered links."

Counterexample: between calls, orphan one delivered link `a_k` (`k ≤ j`, key `< κ(c)`) and create one fresh matching link `a'` with `κ(a') < κ(c)`. The count at/below the cut stays `j`, so rank `j+1` of `Σ'` is still the least of `After(c,Σ')` and the offset window is *correct* — yet `ranks 1..j ≠ the delivered set` (`a_k` gone, `a'` present). So the stated condition fails while `R` holds; it is therefore strictly stronger than `wp`.

**Required**: State the genuine weakest precondition (`|{a ∈ Match(q,Σ') : κ(a) ≤ κ(c)}| = j`, net-count invariance at the cut), not the membership-identity condition. Note that this correction *strengthens* the paper's point — even net-count invariance is not discharged over a mutable set (any unmatched insertion/deletion below the cut breaks it), so the asymmetry with the identity cursor's free obligation (`κ(c)` recoverable) is preserved. The "no membership change" gloss should be replaced by "no net count change at or below the cut."

## OUT_OF_SCOPE

The multi-document allocation-monotonicity gap, late-link delivery, cross-state completeness, orphan-vs-exhaustion disambiguation, delivery/count-order correspondence, and partition preservation under mutation are correctly carried as Open Questions rather than claims. No spurious coverage of the excluded operations (count-only, full-set, MAKELINK, FOLLOWLINK, BEBE) appears.

VERDICT: REVISE
