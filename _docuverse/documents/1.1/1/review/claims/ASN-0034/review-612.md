# Cone Review — ASN-0034/TA3 (cycle 6)

*2026-04-26 07:45*

### Preamble bound `dₐ ≤ #a` (and symmetric `d_b ≤ #b`) cites T1 cases without identifying T1's witness with the zpd index
**Class**: REVISE
**Foundation**: (n/a — internal)
**ASN**: TA3, Case B preamble (after `d_b` is shown defined):

> "T1's case analysis of `a > w` (which holds since `a ≥ w` and `dₐ` is defined) gives `dₐ ≤ #a` hypothesis-free: T1 case (i) for `(a, w)` supplies `dₐ ≤ #a ∧ dₐ ≤ #w`; T1 case (ii) places `w` as a proper prefix of `a` with `dₐ` the first `i > #w` where `aᵢ ≠ 0`, hence `#w < dₐ ≤ #a`."

Same pattern is invoked for `d_b ≤ #b` in the symmetric paragraph: "T1 case (i) for `(b, w)` supplies `d_b ≤ #b ∧ d_b ≤ #w`". Sub-case A2 also opens with the analogous claim ("`a > w` by T1 case (i), it supplies `dₐ ≤ #a ∧ dₐ ≤ #w`").

**Issue**: T1 case (i) supplies a witness *of its own* — call it `k` — with `k ≤ #w ∧ k ≤ #a ∧ wₖ < aₖ` and prefix agreement on `1..k−1`. It does *not* supply a bound on `dₐ = zpd(a, w)`. To translate "T1 case (i)'s `k ≤ #a`" into "`dₐ ≤ #a`" the proof must identify `dₐ` with `k` (or at least show `dₐ ≤ k`). That identification step is missing — the text leaps straight from "T1 case (i)" to "supplies `dₐ ≤ #a`". TumblerSub's *body* walks this identification carefully (via Divergence's uniqueness clause and ZPD's Relationship-to-Divergence postcondition), but TA3's preamble cites only T1 and skips it. The same gap appears in T1 case (ii) for the b-side argument and in A2's opening claim. (A clean alternative bypasses T1 entirely: TumblerSub's exported `â_{dₐ} > ŵ_{dₐ}` together with NAT-zero's `0 ≤ ŵ_{dₐ}` and ZPD's padding clause `âᵢ = 0 for #a < i ≤ L` rules out `dₐ > #a` directly. Either route is fine, but the T1 route as written has an unjustified leap.)

This is the same class of issue cycle 4's finding 3 reported (the bound was unsupported); the revision moved the derivation out of the contradiction block but introduced a new gap in its place.

**What needs resolving**: Either walk the T1-witness-to-`dₐ` identification step (using ZPD's minimality and padded/native coincidence on the shared native domain to lift T1's witness `k` to a bound on `dₐ`, or invoke ZPD's Relationship-to-Divergence postcondition explicitly), or replace the T1-routed argument with a direct derivation from TumblerSub's exported divergence-point postcondition and ZPD's padding clause. Apply consistently in the A2 opening, the Case B preamble's `dₐ ≤ #a` paragraph, and the symmetric `d_b ≤ #b` paragraph.

VERDICT: REVISE
