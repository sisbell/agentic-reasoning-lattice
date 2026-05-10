# Cone Review — ASN-0034/ReverseInverse (cycle 5)

*2026-04-18 20:12*

### Step 1's dichotomy `aₖ = wₖ ∨ aₖ > wₖ` is unsourced — the trichotomy invocation and the T1-refutation that exclude `aₖ < wₖ` are not enumerated

**Foundation**: NAT-order (NatStrictTotalOrder) — trichotomy at the component pair `(aₖ, wₖ)`; T1 (LexicographicOrder) — case (i) needed to convert the excluded component inequality into the tumbler inequality that contradicts `a ≥ w`.

**ASN**: ReverseInverse, Step 1: "Two cases arise at position `k`. If `aₖ = wₖ`, … If `aₖ > wₖ` (the only alternative, since `a ≥ w` excludes `aₖ < wₖ`), then `k` is the first divergence …"

**Issue**: The case split is binary but the underlying NAT-order trichotomy on `(aₖ, wₖ)` is three-way. Reducing it to two requires (a) NAT-order's trichotomy at the component pair `(aₖ, wₖ)` to enumerate the three outcomes, and (b) T1 case (i) at divergence position `k` (using the just-established pre-`k` agreement `aᵢ = wᵢ = 0` and the lengths `k ≤ #a ∧ k ≤ #w`) to convert the hypothetical `aₖ < wₖ` into `a < w`, contradicting `a ≥ w`. ReverseInverse's NAT-order Depends entry enumerates four roles — length-pair dispatch at `(#a, #w)`, defining-clause unfolding at `(wₖ, aₖ)` for NAT-sub, and Step 3's defining-clause/irreflexivity sites — but no trichotomy at the component pair `(aₖ, wₖ)`. T1 is enumerated for Step 3's trichotomy/divergence/irreflexivity, not for this Step 1 refutation. Under the same per-instance convention T1's Depends declares ("branches of a case that instantiate an axiom at distinct symbols count as separate sites") and that this ASN's other properties enforce, both sites are missing.

**What needs resolving**: Either expand Step 1's "`aₖ > wₖ` (the only alternative, since `a ≥ w` excludes `aₖ < wₖ`)" with the explicit trichotomy + T1-case-(i) refutation chain and add the corresponding sites to NAT-order's and T1's Depends entries, or articulate why this binary case split can be read off the precondition `a ≥ w` without consuming either axiom's clause at `(aₖ, wₖ)`.

### Step 1's `aₖ = wₖ` branch consumes ZPD's case-split clause without citing ZPD

**Foundation**: ZPD (ZPD) — case-split clause "`zpd(a, w)` is defined iff the padded sequences disagree somewhere", whose contrapositive is the premise TumblerSub's no-divergence branch consumes.

**ASN**: ReverseInverse, Step 1, equality sub-case: "If `aₖ = wₖ`, then `a` and `w` agree at every position — there are no positions beyond `k` since both have length `k` — and TumblerSub produces the zero tumbler of length `k`."

**Issue**: TumblerSub's Definition produces the zero tumbler in the branch gated on `zpd(a, w)` undefined. The inference from "agree at every position" to "TumblerSub's no-divergence branch applies" is precisely the contrapositive of ZPD's case-split clause: universal agreement of the padded sequences implies `zpd` undefined. ReverseInverse's Depends enumerates TumblerSub but not ZPD. Under the per-step convention this ASN enforces (articulated at TA4's T0 entry and applied in TA3-strict, TumblerSub itself, and TA2 — all of which list ZPD as a separate Depends entry alongside TumblerSub), transitive availability through TumblerSub does not satisfy the citation: TumblerSub's exported postconditions cover only `∈ T`, the result length `L`, and (when zpd is defined) `Pos` and `actionPoint`; they do not export the case-split mechanism that gates the zero-tumbler branch. TA4's own Depends entry for ZPD makes the same point explicitly: "TumblerSub's three-region production rule for `s = r ⊖ w` is keyed on `k = zpd(r, w)` and its no-divergence branch is gated on `zpd(r, w)` being undefined — neither keying surfaced by TumblerSub's exported postconditions."

**What needs resolving**: Either add ZPD to ReverseInverse's Depends with a per-site entry for Step 1's case-split use (paralleling TA4's site (ii) and TA2's analogous case-split entry), or articulate why this consumption of ZPD's case-split clause is exempt from the per-step convention every sibling property follows.
