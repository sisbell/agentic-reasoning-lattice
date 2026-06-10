# Channel Assignment — ASN-0119 review-14

**Date:** 2026-06-09 17:07

## Issue 1: LP11 is invoked by mischaracterizing its hypothesis; REARRANGE is never established as a K.μ~ transition
Reason: Internal. The fix is a lemma-chaining re-derivation against definitions already in the dependency lattice — either discharge ASN-0047's K.μ~ admissibility (i)–(v) using facts the note already proves (the "`V_{s_C}(d)` unchanged as a set" observation and the "π maps each subspace onto itself" fact from the S3★ proof), with non-triviality (ii) handled as a logical case-split on symmetric content; or derive transport inline from P2 + ASN-0098 LP2/LP3. Neither path needs design intent or implementation evidence.

## Issue 2: Forward-reference accretion and essay content in structural slots
Reason: Internal. Purely editorial anti-bloat — remove two deferral pointers and the provenance meta-line, and compress the P7a/P7c table cells to one-line statements while leaving the geometry in the body. No external knowledge required.

## Issue 3 (minor): the "first position" boundary is handled only implicitly
Reason: Internal. R-EXT's `v < c₀` branch degenerates to an empty quantifier when `c₀ = min(V_{s_C}(d))`, and the review itself confirms the existing equations cover it; adding the confirming line against P2/P3 (or folding it into well-definedness) is derivable from the note's own content.
