# Review of ASN-0121

I checked the foundation usage, the satisfaction rule, the decidability argument, the permanence/monotonicity scaffolding, the worked traces, and—most closely—FL-WP, since it was the subject of the last several revision cycles. One genuine exhaustiveness gap remains in FL-WP.

## REVISE

### Issue 1: FL-WP's fresh-link cases are not exhaustive — higher-arity retraction-typed links fall in a gap

**ASN-0121, FL-WP cases (a) and (c)**: case (a) defines a fresh link as *ordinary* "exactly when its committed type endset does not fall in the retraction coverage class — `coverage(Θ) ∉ [coverage(R)]`"; case (c) handles the complement, `coverage(Θ_b) ∈ [coverage(R)]`, asserting "by ASN-0086's slot-3 test `b ∈ L_R^{Σ'}`" and `L_R^{Σ'} = L_R^Σ ∪ {(b, ∅, G')}`.

**Problem**: The cut "`coverage(e₃) ∈ [R]`" is conflated with "the committed link enters `L_R`," but these differ. ASN-0086 defines `L_R^Σ = {(a,F,G) : a ∈ dom(Σ.L) ∧ |Σ.L(a)| = 3 ∧ …}` — entry into `L_R` requires **arity exactly 3** in addition to the slot-3 coverage test. Consider a fresh K.λ committing a link with arity `N > 3` and `coverage(e₃) ∈ [coverage(R)]`. FL-WILD explicitly keeps such higher-arity links in scope. This link:
- is **not** *ordinary* by case (a)'s definition (`coverage(Θ) ∈ [R]`), so case (a) excludes it;
- does **not** enter `L_R` (arity > 3), so case (c)'s premise `b ∈ L_R^{Σ'}` and `L_R^{Σ'} = L_R^Σ ∪ {(b,∅,G')}` are false — `L_R` is in fact unchanged, there is no self-retraction term, and the link retracts nothing.

Its actual entry-wp is precisely case (a)'s five-way conjunction (no `L_R` growth, no `b ∉ coverage(G')` term), yet case (a) is the one case definitionally forbidden to it. So a realisable result-changing K.λ step is characterized by none of the three cases. Case (a)'s own justification — "`coverage(Θ) ∉ [R]` … places `ℓ ∉ L_R^{Σ'}`" — shows the condition is *sufficient* for `ℓ ∉ L_R` but silently treats it as *necessary*, which it is not.

**Required**: Recut the partition by `L_R`-membership rather than coverage-class alone. Define case (a)'s "ordinary" as `ℓ ∉ L_R^{Σ'}` — equivalently `¬(|Σ'.L(ℓ)| = 3 ∧ coverage(e₃) ∈ [coverage(R)])` — so that (a) and (c) are genuinely complementary and exhaustive over the fresh-link space, and the higher-arity retraction-typed link is routed to (a) (where its wp actually lives).

### Issue 2: FL-WP case (c) is silently restricted to unattributed (empty-from) retractions

**ASN-0121, FL-WP case (c)**: "(following ASN-0086's RetractionDirectionality convention, empty from-slot, targets in the to-slot `G'`)", fixing the value as `(∅, G', Θ_b)` and the matching conjunct as `lift(∅, q.F)`.

**Problem**: ASN-0086's RetractionDirectionality convention explicitly admits attribution-bearing retractions — the from-set "is reserved for attribution-bearing endset content **or** is left empty for unattributed retractions." A fresh *attributed* retraction link carries `e₁ = F_b ≠ ∅`, and its entry-wp differs only by replacing `lift(∅, q.F)` with `lift(F_b, q.F)`. As stated, FL-WP(c) — presented in the claims table as *the* wp for "entry of a fresh retraction link" — proves only the empty-from sub-case.

**Required**: Either generalize case (c) to an arbitrary from-endset `F_b` (replace `lift(∅, q.F)` by `lift(F_b, q.F)`; the self-retraction derivation is unaffected since `L_R`-membership and `nullified` depend only on slot 3 and the to-coverage), or state explicitly that the from-slot is taken empty WLOG and why the attributed case reduces to it.

## OUT_OF_SCOPE

(none — both issues are internal to FL-WP, a claim this ASN introduces.)

VERDICT: REVISE
