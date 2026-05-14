# Channel Assignment — ASN-0042 review-28

**Date:** 2026-05-14 00:07

## Issue 1: O10 proof uses incorrect baptism granularity
Reason: Fix is internal — the corrected trajectory must use ASN-0040's defined `inc(·, d)` operations with d ∈ {0, 1, 2}. The reviewer has identified the exact replacement chain; no design intent or implementation evidence needed.

## Issue 2: O10 glosses over sub-delegate coordination
Reason: Fix is internal — the proof must decide whether `Σ →⁺ Σ'` admits transitions by sub-delegates (a model interpretation choice within the spec) or weaken the postcondition. This is a formal proof-structure question resolvable from ASN-0040's baptism mechanism and the ownership model's transition semantics.

## Issue 3: Citation error — Prefix relation conflated with T5
Reason: Fix is internal — pure citation correction. The componentwise expansion is supplied by Prefix (PrefixRelation) in ASN-0034; T5 is about lexicographic contiguity. Both properties are already defined in the source ASN.

## Issue 4: AccountLevelPermanence★ "chain begins with π" claim not formally proven
Reason: Fix is internal — the required ingredients (O14 non-nesting, FiniteRegistry, condition (ii) of delegation) are all present in this ASN. The fix is to either assemble the backward-induction argument or remove the strengthening.

## Issue 5: Reachability assumption used but not stated
Reason: Fix is internal — formal precondition tightening across O3, O8, and AccountLevelPermanence (or a global statement that quantified claims range over reachable states). No external evidence needed.
