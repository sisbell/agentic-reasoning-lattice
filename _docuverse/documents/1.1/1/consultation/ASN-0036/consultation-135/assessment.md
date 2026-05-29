# Channel Assignment — ASN-0036 review-135

**Date:** 2026-05-29 00:08

## Issue 1: S8's conjunct-(b) scoping disclaimer is stated twice
Reason: Purely editorial deduplication — delete the intro restatement, keep the postcondition version. Both texts are already present in the ASN; no design intent or implementation evidence is needed.

## Issue 2: Worked example asserts maximal runs the theorem deliberately does not establish
Reason: Internal consistency fix — reframe the example's nⱼ>1 runs as direct by-hand verification of conjunct (b), distinguished from S8's singleton existence claim. The distinction is already articulated in S8's own text; no channel needed.

## Issue 3: subspace_I notation carries a defensive non-obligation clause
Reason: Editorial trim — drop the "carries no proof obligation" justification, keep the definition. Fully derivable from the ASN's existing content.
