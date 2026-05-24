# Revision Categorization — ASN-0051 review-3

**Date:** 2026-03-20 20:41

## Issue 1: SV6 proof cites wrong foundation and skips a non-trivial step
Category: INTERNAL
Reason: The review itself supplies the correct multi-step argument (element-level field structure forces origin equality) and identifies the T10 citation as replaceable by a direct contrapositive. All needed reasoning is present in the ASN's tumbler algebra definitions and the review's own analysis.

## Issue 2: SV10 formal statement has an unbound variable
Category: INTERNAL
Reason: Pure notational fix — V needs to be quantified or replaced with a concrete set like ran(M(d)). The prose already describes the intent; the formal statement just needs to match it.

## Issue 3: SV11 incorrectly equates projection with span-set denotation
Category: INTERNAL
Reason: The review provides the correct analysis (projection is a finite set of allocated addresses, span denotations include unallocated child-depth tumblers) and two concrete fix options. The distinction follows from definitions already in the ASN.

## Issue 4: SV4 label does not match scope
Category: INTERNAL
Reason: Simple renaming from "ContractionIsolation" to "ArrangementIsolation" — the property's actual quantification over K.μ⁺/K.μ⁻/K.μ~ is already stated in the ASN text.

## Issue 5: State-subscript ambiguity in SV2 and SV4
Category: INTERNAL
Reason: Notation collision where d' means two different things in adjacent properties. The fix is mechanical — adopt state subscripts (π_Σ, π_{Σ'}) and reserve d' for distinct documents.
