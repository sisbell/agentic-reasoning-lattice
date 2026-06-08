# Channel Assignment — ASN-0099 review-92

**Date:** 2026-06-07 22:02

## Issue 1: F21 describes K.μ⁻ as retaining an arbitrary subset
Reason: The fix is editorial and self-contained — the ASN already gates the formula on `enabled(K.μ⁻[d, ℛ])`, and the review supplies the precise correction (ℛ must be a per-subspace canonical initial segment, matching the cited ASN-0047 K.μ⁻ and ASN-0098 LP12a). No design intent or implementation evidence is required to restate the quantifier constraint.

## Issue 2: F15's introductory paragraph previews its own proof
Reason: Pure anti-bloat editorial fix — drop the redundant preview sentence and let the per-clause proof carry the argument. Wholly derivable from the ASN's own structure; no channel needed.
