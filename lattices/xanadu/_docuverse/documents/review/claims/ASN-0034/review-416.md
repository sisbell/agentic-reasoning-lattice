# Regional Review — ASN-0034/TA6 (cycle 2)

*2026-04-23 02:12*

### Redundant `1 ≤ tₖ` detour in TA-PosDom preamble
**Class**: REVISE
**Foundation**: TA-PosDom (PositiveDominatesZero)
**ASN**: TA-PosDom proof: "For (iii) `1 ≤ tₖ`: ... leaves `0 < tₖ`; NAT-discrete's forward direction ... gives `0 + 1 ≤ tₖ`; NAT-closure's additive identity ... rewrites `0 + 1 ≤ tₖ` to `1 ≤ tₖ`." Then in case `#z ≥ k`: "(iii) supplies `1 ≤ tₖ`. NAT-addcompat's `n < n + 1` at `n = 0` gives `0 < 0 + 1`; NAT-closure's `0 + n = n` at `n = 1` rewrites this to `0 < 1`. NAT-order unfolds `1 ≤ tₖ` to `1 < tₖ ∨ 1 = tₖ`; composing with `0 < 1` ... yields `0 < tₖ`."
**Issue**: Step (iii) derives `0 < tₖ` directly from NAT-zero and `tₖ ≠ 0`, then promotes it to `1 ≤ tₖ` via NAT-discrete and NAT-closure, and the only downstream use immediately re-unfolds `1 ≤ tₖ` back to `0 < tₖ` via `0 < 1` transitivity. The detour adds no content to the argument while inflating the Depends list: NAT-addcompat is used only in the roundabout `0 < 0 + 1 ⟶ 0 < 1`, and NAT-closure's additive identity is used only to rewrite `0 + 1` into `1`. The case's actual need is `0 < tₖ` with `zₖ = 0`, which (iii)'s first sentence already supplies.
**What needs resolving**: Either drop the `1 ≤ tₖ` step and use `0 < tₖ` at the case site directly (revising the Depends list accordingly: NAT-addcompat becomes unused; NAT-closure's appearance at this step disappears), or exhibit a proof step that genuinely consumes `1 ≤ tₖ` in its successor-bound form.

### NAT-wellorder listed in TA6 Depends as inherited-only
**Class**: REVISE
**Foundation**: TA6 (ZeroTumblers)
**ASN**: TA6 Depends: "NAT-wellorder (NatWellOrdering) — well-ordering of ℕ inherited via TA-PosDom's case analysis."
**Issue**: The rationale itself says NAT-wellorder is used inside TA-PosDom, not at any TA6 proof step. TA6's proof contains no direct least-element invocation. If TA6 follows the convention of listing only direct dependencies, NAT-wellorder is spurious — TA6 doesn't also list NAT-addcompat, NAT-closure, NAT-discrete (all used inside TA-PosDom), so the treatment of transitive dependencies is inconsistent. An "inherited via X" annotation in a Depends slot is either everywhere or nowhere.
**What needs resolving**: Either remove NAT-wellorder from TA6 Depends (matching the treatment of TA-PosDom's other upstream axioms), or adopt the inherited-deps convention uniformly and list all of TA-PosDom's NAT dependencies in TA6.

### TA-Pos note mislocates T1's position
**Class**: OBSERVE
**Foundation**: TA-Pos (PositiveTumbler)
**ASN**: TA-Pos Note on notation: "The lexicographic ordering and its prefix rule alluded to here are supplied by claims outside this region and enter no obligation of TA-Pos."
**Issue**: The lexicographic ordering is T1, which is presented in this same ASN — not "outside this region". The intent (that T1 is not a Depends of TA-Pos) is fine, but the geography is misstated. Minor and only in a parenthetical.

### TA6 Conjunct 2 proves an unneeded biconditional
**Class**: OBSERVE
**Foundation**: TA6 (ZeroTumblers)
**ASN**: TA6 Conjunct 2: "By T0, each `tⱼ ∈ ℕ`; NAT-zero gives `0 ≤ tⱼ`, and combined with NAT-order this yields `tⱼ > 0 ⟺ tⱼ ≠ 0`."
**Issue**: Only the forward direction `tⱼ > 0 ⟹ tⱼ ≠ 0` is used to extract `Pos(t)` from the hypothesis. That direction follows from NAT-order's disjointness axiom `m < n ⟹ m ≠ n` at `(0, tⱼ)` alone — no appeal to NAT-zero's lower bound is required. Deriving the biconditional is strictly more than the proof needs.

VERDICT: REVISE
