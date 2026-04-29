# Cone Review — ASN-0034/TA4 (cycle 6)

*2026-04-18 13:39*

### "TumblerSub's precondition" in TA4 Case 1 names a componentwise inequality that is not in TumblerSub's precondition list

**Foundation**: TumblerSub (TumblerSub) — `Formal Contract: Preconditions: a ∈ T, w ∈ T, a ≥ w (T1). Consequence: when zpd(a, w) is defined, aₖ > wₖ at k = zpd(a, w)`. TumblerSub's preconditions are stated at the tumbler level (`a ≥ w`); the component-level inequality at the zpd point is a *derived consequence* internal to TumblerSub's proof (and in the strict form `aₖ > wₖ`, not `aₖ ≥ wₖ`).

**ASN**: TA4 (PartialInverse), proof Step 2 Case 1: "Hence `rₖ ≠ wₖ`; combined with the pre-divergence agreement `rᵢ = wᵢ` at positions `i < k` established at Step 2's opening, ZPD's minimality clause — applied to the pair `(r, w)` on the common length `L = k` — identifies `k` as the least position at which the padded projections disagree… **Since `rₖ > wₖ`, TumblerSub's precondition `rₖ ≥ wₖ` at the divergence point is satisfied.** TumblerSub produces: `sᵢ = 0` for `i < k`…"

**Issue**: TumblerSub's contract states three preconditions — `a ∈ T`, `w ∈ T`, `a ≥ w (T1)` — none of them a componentwise inequality. The caller's obligation when invoking TumblerSub at `(r, w)` is to discharge exactly those three. `rₖ ≥ wₖ` at the divergence point is neither (i) in TumblerSub's precondition list nor (ii) TumblerSub's stated precondition-consequence (which is the *strict* `aₖ > wₖ`, conditional on `zpd(a, w)` being defined). The ASN elsewhere enforces that every term has one meaning — "precondition" in particular — yet here TA4 relabels an internal NAT-sub conditional-closure premise as TumblerSub's precondition. The only precondition TA4 owes TumblerSub at this call site (the ordering `r ≥ w`) was already discharged at Step 2's opening via TumblerAdd's dominance postcondition; the sentence in question is either dischargeing something that isn't a TumblerSub precondition or double-discharging `r ≥ w` under a different name. A formalization that reads "TumblerSub's precondition" literally will search for a componentwise clause in TumblerSub's contract and not find it.

**What needs resolving**: TA4 must either (a) reframe the sentence to name what `rₖ > wₖ` actually discharges — namely, the premise internal to TumblerSub's own NAT-sub conditional-closure step (and TumblerSub's precondition-consequence) at the identified `k = zpd(r, w)`, making clear that TA4's tumbler-level precondition `r ≥ w` has already been discharged separately — or (b) delete the sentence entirely, since TA4's actual need for `rₖ > wₖ` in Case 1 is to identify `zpd(r, w) = k` via ZPD minimality (already accomplished in the preceding sentence), not to discharge any precondition of TumblerSub.

## Result

Cone converged after 7 cycles.

*Elapsed: 3418s*
