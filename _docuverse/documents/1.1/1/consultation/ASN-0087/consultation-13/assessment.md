# Channel Assignment — ASN-0087 review-13

**Date:** 2026-05-26 15:28

## Issue 1: "bounded" terminology in cascade discussion is non-standard
Reason: Pure terminology/clarity fix. The substitution and gloss expansion are derivable from the ASN's own argument structure; no design intent or implementation evidence is needed.

## Issue 2: M-Inv-Trans claim lists P3 alongside its constituents
Reason: Logical structure cleanup. P3's definition as `P0 ∧ P1 ∧ P2 ∧ L12` is already stated; the fix is choosing which side of the equation to keep. Derivable from the ASN alone.

## Issue 3: M1's role in the wp membership clause needs sharper attribution
Reason: Attribution sharpening. M1 supplies inclusion; the frames on `dom(M)` from K.λ and K.μ⁺_L are explicitly stated in the ASN. Combining them for equality requires no external input.

## Issue 4: Worked example does not exercise the reflexive-endset or prior-link cascade cases
Reason: The mechanics of M-Reflexive and M-PriorLinkDisc are fully established in the ASN; constructing a concrete numeric instance requires only applying existing definitions (`coverage`, `project`, `discoverable_from`, LP12) to the same `Σ` already set up. No design intent or implementation evidence needed.

## Issue 5: L1c chain construction is correct but distorts the section's readability
Reason: Presentation restructuring only. Splitting the existence proof from the uniqueness strengthening is editorial; the technical content is unchanged.

## Issue 6: Cascade-vacuity dependence on Store Monotonicity★ is implicit
Reason: The missing premise — Store Monotonicity★ from ASN-0098 — is already an established invariant in the framework. Citing it explicitly is internal cross-referencing, not a substantive question for Nelson or Gregory.
