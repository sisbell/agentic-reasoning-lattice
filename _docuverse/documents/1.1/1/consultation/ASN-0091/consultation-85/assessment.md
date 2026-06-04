# Channel Assignment — ASN-0091 review-85

**Date:** 2026-06-04 04:46

## Issue 1: Target document named inconsistently (`d` vs `d_tgt`)
Reason: Pure notational consistency fix — rename the target variable uniformly across the note. Both the conflicting usages and the correct convention are visible in the ASN itself; no design intent or implementation evidence bears on the choice of variable name.

## Issue 2: Scope-gloss paragraph in the REARRANGE_K realisation
Reason: Editorial trim of self-referential meta-prose, folding the reachable-Σ qualifier into the theorem statement. The reachability obligation and its discharge are already present in the ASN, so the fix is internal.
