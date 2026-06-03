# Channel Assignment — ASN-0102 review-16

**Date:** 2026-06-03 16:29

## Issue 1: COPY invokes ValidComposite★'s coupling machinery without admitting COPY into its closed atomic vocabulary
Reason: The fix is internal — the ASN already cites ValidComposite★'s enumeration (ASN-0047) and the required move is a formal bookkeeping amendment (add COPY to the atomic vocabulary with an "(amended)" tag, declare its pre/post-states composite boundaries to ground the P4★ appeal). No design intent or implementation evidence is needed; the reasoning for the discharge is already present and only the explicit vocabulary-extension step is missing.

## Issue 2: No worked example exercises the genuinely distinct boundary cases
Reason: The fix is purely mechanical — instantiate the existing definition, X16 tiling/density, and the X14 J1★/J1'★ split at specific boundary values (`n_S = 0, p = 1` and `p = n_S + 1`). Everything needed is already derived in the ASN's own theorems; no external channel is required.
