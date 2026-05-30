# Channel Assignment — ASN-0042 review-110

**Date:** 2026-05-30 03:57

## Issue 1: Use-site / "why-needed" prose appended to the O17b axiom
Reason: Pure editorial deletion — removing a use-site explanatory paragraph from an axiom. No design intent or implementation evidence is at stake; the axiom's disjunction and its consumers (O18, DelegatorAllocatesPrefix) already stand within the ASN.

## Issue 2: Duplicated framing prose for O10
Reason: A choice between two redundant thematic paragraphs already present in the ASN; keeping the concrete worked-example sentence is a self-contained editorial decision requiring no external channel.

## Issue 3: `R_Σ` / `covers_Σ*` / NestingByDelegation apparatus is heavy machinery with a single worked-example consumer
Reason: Whether to route OwnershipDomainPermanence's "sub-delegate" reading through `covers_Σ*` or demote the apparatus is a formalization/structural decision fully determined by the ASN's own definitions and proofs; no design-intent or implementation question arises.

## Issue 4: Proof-local notation reused across proofs without restatement
Reason: Promoting or inlining the `C(a)` definition is a notation-scoping fix internal to the ASN's existing proofs, with no bearing on design intent or implementation evidence.
