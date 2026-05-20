# Channel Assignment — ASN-0094 review-3

**Date:** 2026-05-19 20:08

## Issue 1: Restatement of foundation definitions
Reason: Determining which definitions are used/unused is a textual audit of the ASN itself; deciding what to delete vs. cite-by-name is derivable from the ASN's own body. No external channels needed.

## Issue 2: Foreign ASN references in restated SubstrateConformingLayer body
Reason: The fix is removal/citation-by-name, contingent on Issue 1's resolution. The ASN's own scaffolding section already enumerates the specific properties it consumes, so citing the contract by name suffices internally.

## Issue 3: Sh0-Sh3 proof Case A conflates two sub-cases
Reason: Proof structure is internal to the ASN; the missing sub-case (K.λ emitting non-K tuples) is handled by `L_K^{Σ'} = L_K^Σ` which is mechanically derivable from definitions already in the ASN.

## Issue 4: Sh4 proof case structure incomplete
Reason: Same kind of fix as Issue 3 — adding the missing K.λ-for-K'∉{K,R} branch. The reasoning uses only properties (`L_K` unchanged, `nullified(Σ')=nullified(Σ)`) already stated in the ASN.

## Issue 5: Opaque notation `slot_addrs(F)(τ)`
Reason: Pure notational fix using accessors (`from_K^Σ`, `to_K^Σ`) already defined later in the ASN. No external information needed.

## Issue 6: Notational collision Σ_K for shape vs Σ for state
Reason: Renaming the shape tuple is purely notational. The ASN already uses `shape(K)` throughout, so the fix is mechanical.

## Issue 7: T_cat closure under ~ ambiguous
Reason: The ASN already states the registry "operates on the quotient `T_cat / ~`"; the fix is to pick one formal reading consistent with that statement. Internal formalization.

## Issue 8: Tpl referenced in properties table but not defined
Reason: The ASN itself exhibits template families per shape; deciding whether to drop the table row or formalize Tpl as a function is internal bookkeeping.

## Issue 9: AllocatedAddressAntichain Case 3 "vice versa" not made explicit
Reason: Adding one symmetric sentence completes the proof; the symmetry argument is mechanical from the case already worked.

## Issue 10: emission_order monotonicity claim lacks derivation
Reason: The derivation composes already-cited foundation theorems (T9, T10a.7, T1) with the per-document link sub-allocator chain assumption already in the scaffolding section. Internal composition.

## Issue 11: Worked example covers only Comment shape
Reason: Constructing additional worked examples is a spec-authoring task using the framework's own definitions; the substrate behavior needed (chain ordering, partial accessors, bipartite substitution) is fully specified in the ASN.

## Issue 12: Worked example omits cardinality-violation rejection
Reason: Adding a rejection case exercising Sh-conf clause (c) uses only definitions present in the ASN.

## Issue 13: Sh5 expressive-ceiling claim unsupported
Reason: The ASN already explicitly marks Sh5 as META; rephrasing Consequence (b) to match that status is internally consistent. No design-intent or implementation question needed.

## Issue 14: `-^Σ` (absent-slot expansion) not formally specified
Reason: Specifying `-^Σ = ∅` (or equivalent) is a one-line formal completion of the ASN's own conformance definition.

## Issue 15: Set-vs-bag semantics distinction informal
Reason: Rephrasing to drop the bag-semantics framing aligns with the ASN's own treatment of A_K as a set of distinct-address tuples. Internal terminology cleanup.
