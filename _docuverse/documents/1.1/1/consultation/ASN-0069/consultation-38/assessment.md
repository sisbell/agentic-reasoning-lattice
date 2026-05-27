# Channel Assignment — ASN-0069 review-38

**Date:** 2026-05-27 15:23

## Issue 1: V11's premise is insufficient for its IH and conclusion when d_src is edited between fork steps
Reason: Internal formal consistency problem between V11's premise scope, the IH's "current-state" evaluation, and the worked example's "frozen" wording. The fix is a choice between strengthening the premise to constrain `d_src` chain-wide or reformulating the IH/conclusion to anchor on the chain's initial pre-state — both options are derivable from the ASN's own machinery (V5a is already in hand for the strengthened premise; the frozen-value reformulation just renames what V4-at-step-1 captured). No design-intent or implementation-evidence question is involved.
