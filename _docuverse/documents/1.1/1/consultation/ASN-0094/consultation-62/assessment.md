# Channel Assignment — ASN-0094 review-62

**Date:** 2026-05-24 09:01

## Issue 1: Appendix's ℤ example is mathematically incorrect
Reason: Pure mathematical error in the counterexample structure. The fix involves replacing ℤ with a structure that actually satisfies NAT-wellorder while distinguishing the standard reading — derivable from the listed NAT axioms in the appendix itself.

## Issue 2: Sh5(b) audit table — `K_is_fresh` rejection sub-categorization is incomplete
Reason: Format/procedural consistency issue between the accepted-row format (per-symbol classifications inlined) and the rejected-row callout. The fix is either inlining the missing positive classifications for `from_K` and `K_target_of` before isolating `mtime`'s failure, or documenting the format divergence — both authorial decisions.

## Issue 3: Sh4 Case D's `|leaving| ≤ 1` derivation conflates two distinct antichain arguments
Reason: Proof rigor — the missing antecedents (Sh-conf clause (d) placing `b ∈ dom(Σ.L)`; Prefix reflexivity giving `b ∈ {a : b ≼ a}`; R0a applied between b and any other a) are all already cited elsewhere in the ASN. The fix inserts the explicit chain from machinery the ASN already commits to.

## Issue 4: Lemma — LinkAddressNotPrefixOfEmit Case II.B Step II.2 — Step 3.2's bridge to Step II.2 is asserted but not exhibited
Reason: Proof rigor — extending the single-position argument to three positional ranges requires uniform application of T4a/T4b/T4c at each range, all of which are cited in the ASN already. The fix either exhibits the per-range index identification or commits to uniformity.

## Issue 5: Sh4 Case A — "transitions outside the enumeration but satisfying the case-equation" leaves a soundness gap
Reason: Resolution depends on whether ASN-0086's `↦` vocabulary is exhaustively enumerated by the four classes the framework names. This is a question about ASN-0086's design — what transition classes the substrate intends `↦` to comprise.
Nelson question: Does ASN-0086's `↦` transition relation comprise exactly `(K.σ ∪ K.α ∪ K.λ) ∪ arrangement-modifying`, or are there other transition classes (e.g., layer-arrangement steps not captured by ASN-0086's `→ \ →` split) the substrate intends to admit?

## Issue 6: Coverage walkthrough — Empty-`S_d` dispatch table is presented as a stand-alone artifact but its construction depends on framework state not surfaced at the table's introduction
Reason: Documentation clarity — the conflation of initial-state-empty and post-retraction-empty regimes is internal to the walkthrough's framing. The fix is either splitting the table by regime or scoping the table to initial-state-empty (the regime actually exhibited), both authorial decisions derivable from the walkthrough's existing state.

## Issue 7: `T_cat` decidability — coverage-equality procedure for unrestricted finite span sets is asserted but the worked example shows only canonical-form sets
Reason: The decidability claim's scope is broader than the catalog's actual use. The fix involves either restricting the catalog's representative-list discipline to canonical-form (matching exercised use) or exhibiting a non-canonical worked example — both internal scoping decisions. The mathematical procedure itself uses only T1/T2/T12/TumblerAdd from ASN-0034, which the ASN already cites.
