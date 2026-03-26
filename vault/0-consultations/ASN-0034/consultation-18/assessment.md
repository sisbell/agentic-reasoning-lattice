# Revision Categorization — ASN-0034 review-18

**Date:** 2026-03-25 23:23

## Issue 1: TA7a verification contains a false intermediate claim and S is undefined
Category: INTERNAL
Reason: The false divergence claim, the counterexample, and the undefined set S are all diagnosable and fixable from the ASN's own definitions (TumblerSub, T4's positive-component constraint, the constructive subtraction formula). No external design intent or implementation evidence is needed.

## Issue 2: Dependency graph has circular and reversed dependencies
Category: INTERNAL
Reason: Each cycle and reversal is resolved by reading the proofs already present in the ASN — TA-strict's proof cites TumblerAdd and T1 (not T12), D0 is a precondition stated before D1, and TA4's proof uses TumblerAdd (not the reverse).

## Issue 3: Dependency graph has spurious dependencies
Category: INTERNAL
Reason: Every spurious entry is identifiable by comparing each property's `follows_from` list against the premises actually cited in its proof or definition, all of which are contained within the ASN text.

## Issue 4: Dependency graph has missing dependencies and name mismatches
Category: INTERNAL
Reason: The missing dependencies (Divergence for TA1-strict, TumblerAdd for TA-strict, TA5/T3 for PartitionMonotonicity), the non-existent TA5(a) reference, and the truncated names are all correctable from the ASN's own property definitions and proof texts.
