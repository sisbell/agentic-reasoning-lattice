# Channel Assignment — ASN-0099 review-72

**Date:** 2026-06-04 14:13

## Issue 1: "What We Have Not Specified" contradicts the total comprehension definition
Reason: Derivable from the ASN alone — the comprehension `findlinks(I, Σ)` is explicitly total over `I ⊆ T`, F8 asserts functionality for arbitrary I, and the Empty Query section already handles `I = ∅`. The fix (delete or reword to name the *interpretation* as unspecified) follows from the ASN's own definitions.

## Issue 2: Chronological-reading paragraph is self-disclaiming interpretive prose
Reason: Pure editorial removal — the paragraph itself admits it "plays no role in F10's ordering claim." No external semantics or design intent are at stake.

## Issue 3: "non-allocating" terminology forces a defensive clarification
Reason: Internal terminology cleanup — the ASN already supplies the synonym "link-store-inert" and states the A1a/A1 equivalence twice. Renaming, deleting the defensive sentence, and de-duplicating the equivalence are derivable from the ASN's own content.

## Issue 4: F17/F18 say "atomic K.μ-family step" but include the non-atomic K.μ~
Reason: Internally derivable — the ASN's own A1 text calls K.μ~ "the non-atomic K.μ⁻ + K.μ⁺ composite," and F9 already establishes preservation across composites via transitive composition, so the "atomic" qualifier is inconsistent on the ASN's own terms. The fix (drop "atomic") needs no external evidence.
