# Channel Assignment — ASN-0047 review-134

**Date:** 2026-05-19 21:53

## Issue 1: Typo or unclear phrasing in version-chain discussion
Reason: Pure typographical/clarity fix; the intended relation (`{v_i : i ≥ 1} ⊆ dom(A_v(d))`) is derivable from the surrounding text on allocator-tree provenance and is internal to the ASN.

## Issue 2: T10a.7 citation in (t, 0) uniqueness derivation
Reason: This is an attribution-accuracy fix within the derivation chain. The correct citation (TA5(c) for functional determinism of `inc(t, 0)` + P1 + precondition) is derivable from foundation references already in the ASN; no design or implementation input is needed.

## Issue 3: Sub-allocator names provenance labeling
Reason: Attribution clarification — A_v(d) is introduced in this ASN, not ASN-0093. The correct provenance labels are derivable from the ASN's own Sub-allocator names section and the inherited ASN-0093 properties table.

## Issue 4: S8★ link-subspace decomposition relies on undefined operation
Reason: The fix is to either state a `shift(v, 0) := v` convention or rework the trivial decomposition's S8 condition (b) verification. Both options are derivable from ASN-0036's S8 statement and ASN-0034's OrdShift definition already referenced in the ASN; internal.

## Issue 5: J4 fork omits link-subspace clearance discharge
Reason: The route through K.δ's totality-convention effect on M(d_new) → empty V_{s_L}(d_new) is already in the ASN's own content (totality convention is stated in *The state model*); the fix is to make the citation explicit in the J4 verification. Internal.

## Issue 6: Worked example "Step 5" verification gap
Reason: The fix is to state the chosen (n'_{s_C}, n'_{s_L}) pair and confirm the constructive precondition; the K.μ⁻ definition and admissible-shape derivation already in the ASN supply the verification template. Internal.

## Issue 7: K.μ⁺ pairwise-distinctness clause is overcomplicated
Reason: Clarity/style reformulation. The simpler direct distinctness statement is derivable from S2's functionality requirement already established in the ASN; no external input needed.

## Issue 8: K.μ~ matrix entry "via fixity" is imprecise
Reason: Rephrasing fix — the full-clearance form retains V_{s_L}(d) pointwise by construction (K.μ⁻ removes only V_{s_C}(d)), distinct from the fixity theorem's role. The construction-based account is derivable from the K.μ⁻ amendment's per-subspace structure and the full-clearance form's definition in *Decomposition of K.μ~*. Internal.
