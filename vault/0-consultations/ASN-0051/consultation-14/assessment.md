# Revision Categorization — ASN-0051 review-14

**Date:** 2026-03-23 01:19

## Issue 1: SV11 ran_text guard includes link-subspace V-positions
Category: INTERNAL
Reason: The ASN already identifies the link-subspace distinction and the `subspace()` predicate exists in ASN-0047. The fix — replacing `v₁ ≥ 1` with `subspace(v) = s_C` — is derivable from existing definitions.

## Issue 2: SV13(g) does not specify text-subspace restriction
Category: INTERNAL
Reason: SV11 already states the text-subspace restriction explicitly. SV13(g) is an editorial alignment to match wording already present in the same ASN.

## Issue 3: SV6 proof omits short-tumbler elimination
Category: INTERNAL
Reason: The review finding itself supplies the missing argument (prefix contradiction via T1(ii)). The fix is adding one sentence using tumbler ordering properties already cited in the proof.

## Issue 4: Endset Fragment definition depends on choice of block decomposition
Category: INTERNAL
Reason: ASN-0058 already defines the canonical maximally merged block decomposition (M11, M12). The fix is specifying that decomposition in the definition, which is derivable from existing cross-referenced material.
