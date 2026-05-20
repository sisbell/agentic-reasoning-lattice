# Channel Assignment — ASN-0094 review-5

**Date:** 2026-05-19 21:03

## Issue 1: Catalog internally inconsistent with Sh5's organizing claim
Reason: The fix is internal — restructure catalog rows to separate base templates (shape-forced) from opt-in extensions (discipline-forced), mirroring how FunctionalDependencyDiscipline already factors `K_target_of` out of DirectedPair's base. The pattern for the fix is already present in the ASN.

## Issue 2: FunctionalDependencyDiscipline preservation proof omitted
Reason: The fix is internal — FDD's shape constraint `(1, 1, A_doc, A_doc, ⊤)` directly precludes K ~ R (Retraction has `(*, 1, A, A_rel, ⊤)`), so Case D cannot fire. The corrected Cases A/B/C structure and the "broadened scope, strictened gate" phrasing are derivable from the ASN's own shape definitions.

## Issue 3: AllocatedAddressAntichain — E(x) ≼ E(a) step elided
Reason: The fix is internal — the sub-arguments (x's three zero positions are the only zeros of a, and componentwise prefix agreement implies E-field prefix) are derivable from ASN-0034's definitions of `zeros`, `E`, and the prefix relation, already cited in the proof.

## Issue 4: "depth-2 span" terminology misuses δ's parameters
Reason: The fix is internal — ASN-0034's OrdinalDisplacement defines `δ(n, m) = [0, ..., 0, n]` of length m, making n the increment and m the depth. The terminology correction to "width-2 displacement" follows directly from that definition.

## Issue 5: "three structural gates" inconsistent with Sh-conf's four clauses
Reason: The fix is internal and presentational — either fold the (a)/(b) consolidation explicitly into Sh-conf's definition or count consistently as four. Both options are pure editorial choices over the ASN's own structure.

## Issue 6: SingleHomeCoverageDiscipline emission_order well-definedness depends on shared-chain reasoning that isn't tight
Reason: The fix is internal — chain-index injectivity (T10a.7) and T1-monotonicity (T9, TA5a) transfer to any subset of the chain enumeration; the clarifying sentence is derivable from properties already cited in the walkthrough.

## Issue 7: Sh4 contract's atomicity scope justification missing for cross-class retraction
Reason: The fix is internal — Sh4's predicate is pairwise distinctness on `A_K`, and removal from `A_K` is monotone in the negative direction over a universally-quantified pairwise condition, which preserves it. The argument is derivable from Sh4's own statement.
