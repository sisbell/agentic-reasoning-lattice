# Channel Assignment — ASN-0042 review-47

**Date:** 2026-05-14 07:33

## Issue 1: Inconsistent state subscripting on ω
Reason: Pure notational consistency cleanup. The ASN already establishes ω as state-relativized (O2's definition ranges over Π_Σ); threading Σ uniformly through all appearances requires no design intent or implementation evidence.

## Issue 2: Allocator-delegator equivalence is implicit but load-bearing
Reason: The derivation follows mechanically from O5 (allocator is most-specific covering principal), O16 (allocation closure), condition (ii) of `delegated` (delegator is most-specific covering), and O2 Step 4 (uniqueness of longest match). All ingredients are present; only the named property and its short proof need adding.

## Issue 3: O3's formal statement is weaker than the prose
Reason: The proof body already establishes the delegation witness via O15 + reachability + bootstrap exclusion. Strengthening the postcondition to expose `delegated_Σ(π_d, π')` is a pure contract update — no new evidence required.

## Issue 4: O10's field-opening boundary case is exhibited only via a scenario substitution
Reason: A freshly baptized prefix has `hwm = 0` by ASN-0040's definition of `hwm` and B1 (children empty until first baptism). Constructing a second account-level principal `π_D` delegated within the running scenario uses only existing delegation mechanics; no design or implementation evidence needed.

## Issue 5: O0's framing overstates structural decidability
Reason: The distinction between `owns(π, a)` (predicate on a candidate principal) and `ω(a)` (function returning the owner) is already present in the ASN — O1 defines the predicate, O2 defines the function, O6 sharpens to `acct(a)`. The fix is prose alignment to what the formal contracts already say.
