# Review of ASN-0111

## REVISE

### Issue 1: Worked-example coverage of the type endset is computed as a singleton, contradicting the coverage semantics the ASN itself established

**ASN-0111, "A worked read" (RL5 check)**: "`Θ`'s address holds nothing, yet the read returns it intact; the type is interpreted as `coverage(Θ) = {[1.0.1.0.9.0.1.1]}` (L8), no dereference attempted."

**Problem**: The type endset is `Θ = {([1.0.1.0.9.0.1.1], δ(1, 8))}` with `#s = 8`, so its span is exactly the canonical unit-depth span `(x, δ(1, #x))`. By PrefixSpanCoverage (ASN-0043), `coverage({(x, δ(1, #x))}) = {t : x ≼ t}` — the entire subtree beneath `x`, an **infinite** tumbler set (it contains `x`, `x.0`, `x.1`, `x.0.5`, …). It is not the singleton `{[1.0.1.0.9.0.1.1]}`.

This is the very confusion the ASN warns against earlier in the same example, where it correctly insists for the from-set that `coverage(F)` is "a union of two half-open intervals, not a finite list of points … an infinite tumbler set, not the two addresses …1.1 and …1.2 alone." The second from-span `([1.0.1.0.2.0.1.1], δ(1, 8))` has the identical δ(1,8) shape and is correctly described as "the interval `[ [1.0.1.0.2.0.1.1], [1.0.1.0.2.0.1.2] )`" — yet the structurally identical type span is collapsed to a single address. The treatment is internally inconsistent.

This is load-bearing, not cosmetic: RL5, RL-REP, and L8's `same_type` all turn on coverage as an address-*set*. A worked example that mis-states coverage as a point set undermines the distinction the note is built to make.

**Required**: Replace `coverage(Θ) = {[1.0.1.0.9.0.1.1]}` with `coverage(Θ) = {t : [1.0.1.0.9.0.1.1] ≼ t}` (the subtree, per PrefixSpanCoverage), and adjust the surrounding prose so the ghost-type coverage is described as an interval/subtree consistent with the from-set treatment. The "ghost / no dereference / complete read" point survives unchanged; only the set value must be corrected.

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
