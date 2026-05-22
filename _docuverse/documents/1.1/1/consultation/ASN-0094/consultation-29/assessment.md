# Channel Assignment — ASN-0094 review-29

**Date:** 2026-05-21 22:13

## Issue 1: Lemma — RetractionTargetNotOnChain Case II is dense and under-structured
Reason: Pure expository restructuring — factoring out a sub-lemma or numbering sub-steps. The mathematical content is already established in the ASN; no design intent or implementation evidence is needed.

## Issue 2: AllocatedAddressAntichain Case 3 sub-case presentation is inconsistent with its worked example
Reason: Alignment of formal proof and worked example to walk the same sub-case. Purely editorial; both versions of the argument are already in the ASN.

## Issue 3: Sh-conf's return-type signature change has incomplete callsite analysis
Reason: Enumerating ASN-0086's `Emit_K` consumers is an internal reading of the project's own substrate spec. The framework author can construct the compatibility table directly from ASN-0086's content.

## Issue 4: Emit_K routing commitment is load-bearing but its violation mode is not consolidated
Reason: Consolidating existing scattered statements about routing violation into one paragraph. The failure-mode content is already derivable from the preservation proofs and contract clauses present in the ASN.

## Issue 5: Single-home commitment specification is buried inside the Coverage walkthrough
Reason: Pure document reorganization — promoting an existing definition to its own section parallel to the other two layer-discipline contracts. No external input needed.

## Issue 6: Gate ordering with multiple disciplines is not documented in one place
Reason: Consolidation of per-discipline ordering specifications already stated within each contract section, plus the mutual-exclusion argument that follows from the existing `idem` shape-component constraint.

## Issue 7: Per-class constancy is asserted as a registry property without specifying the registration interface
Reason: Specifying the registration interface is a framework-internal design choice; the shape registry is a substrate abstraction above what either Nelson designed or Gregory implemented. The framework author can fix the interface by analogy with `T_cat`'s already-specified representative-list registration.

## Issue 8: Worked examples have partial template coverage
Reason: Adding one-line template evaluations to existing worked examples. The template bodies and example states are already specified in the ASN; the work is mechanical verification.
