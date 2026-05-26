# Channel Assignment — ASN-0098 review-10

**Date:** 2026-05-25 23:16

## Issue 1: F is defined informally
Reason: Pure formalisation task — the ASN already describes F's contents textually and cites the chain structure from ASN-0093 with explicit forms `[d, 0, s_C, k]`/`[d, 0, s_L, k]`. Set-builder notation can be written directly from the existing prose.

## Issue 2: Inductive extensions hand-waved
Reason: The inductive structure rests on ASN-0034 (TumblerAdd, T1, divergence) and ASN-0047 (K.δ document-allocation rules), both already cited in the ASN. The fix is making the induction's variable, hypothesis, and discharge explicit using facts already in scope.

## Issue 3: LP20 stated as inclusion when equality is the natural content
Reason: The strengthening follows directly from the project definition and S3★ (both already in the ASN). Pure proof restatement; the equality is mechanical from existing definitions.

## Issue 4: LP18 proof does not establish `a ∈ dom(Σ'.L)`
Reason: The missing step is a citation to Store Monotonicity★ or LP13, both already introduced in this ASN. Pure proof-completion fix.

## Issue 5: Citation ambiguity for ChainEnumerationInjectivity
Reason: Disambiguating between two spec lemmas (one in ASN-0034, one in ASN-0093) is a matter of reading those documents to confirm which statement matches the inferential need (chain-index-to-address monotonicity under increment). Resolvable from the spec foundations.

## Issue 6: Order-preservation under K.μ⁺_L's first-arrangement constraint not addressed
Reason: LP9's proof depends only on the structural extension shape of `Σ.M(d)` (domain growth + agreement on prior domain), both documented in ASN-0047's K.μ⁺_L definition. Verifying that the additional constraints (`ℓ ∉ ran(M(d))`, fixed depth, link-subspace placement) don't affect this structural form is checkable from ASN-0047 directly.
