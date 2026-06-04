# Channel Assignment — ASN-0091 review-94

**Date:** 2026-06-04 06:03

## Issue 1: Comparative-to-foundation editorializing in the realisation section
Reason: Pure prose-register trim — state the pointwise-fixity facts (π(v) = v, arrangement preservation) and their R-PPERM/R-SPERM/R-FRAME sources directly, dropping the "stronger/weaker than clause N" comparison. The facts and their citations already exist in the ASN; no design intent or implementation evidence is at stake.

## Issue 2: Exhaustive use-site inventory of binary transition invariants
Reason: Internal consolidation — the discharge principle ("every binary transition invariant constrains a component fixed with equality by RA-frame, hence holds trivially") is already fully present in the ASN; replacing the per-invariant enumeration with the single principle plus one citation is derivable from the existing text alone.

## Issue 3: "Why the precondition is needed" rationale prose
Reason: Internal trim — RA-bndy and ExtendedReachableStateInvariants are both already defined in the ASN; collapsing the "interior states" rationale to a bare scoping statement plus citation needs no external input.
