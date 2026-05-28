# Channel Assignment — ASN-0077 review-35

**Date:** 2026-05-28 10:03

## Issue 1: O0(b) L-closure for K.σ routes through LP8 imprecisely
Reason: Internal fix. The proof must be restructured to use the same direct frame-exhaustiveness argument that (c) already uses for C-closure under K.σ. All needed material (K.σ's effect clause, frame-exhaustiveness assumption) is already cited within the ASN.

## Issue 2: Cross-ASN parenthetical citations to ASN-0093
Reason: Internal citation-hygiene fix. Either drop the "(ASN-0093)" parentheticals (relying on LP8's foundation-mediated coverage) or flag an escalation request — both choices are derivable from the standards already named in the issue.

## Issue 3: Missing multi-step versions O11★ / O11'★
Reason: Internal derivation. O5★ and O6★ supply the induction template; O11/O11' compose with O5★ across atomic step sequences. No design intent or implementation evidence needed.

## Issue 4: Worked example uses informal multi-transition labels
Reason: Internal presentation fix. Re-label the composite as a chain of atomic K.α/K.μ⁺ steps using the elementary transition vocabulary already established in the ASN.

## Issue 5: wp characterisations not explicitly exercised in worked example
Reason: Internal extension. Both wp formulas evaluate against states (Σ₀, Σ₁, Σ₂) already defined in the worked example using `origins_I` and `origins_V` values already computed.
