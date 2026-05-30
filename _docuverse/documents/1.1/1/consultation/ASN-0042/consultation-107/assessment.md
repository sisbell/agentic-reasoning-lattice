# Channel Assignment — ASN-0042 review-107

**Date:** 2026-05-30 03:47

## Issue 1: Undefined notation `dom(a')`
Reason: The fix substitutes a notation already defined in the ASN — `odom(π)` (defined on principals) or the prefix-subtree `{t : a' ≼ t}`. Choosing the intended set is a self-contained editorial resolution requiring no design intent or implementation evidence.

## Issue 2: Downstream-consumer inventory in the closure introduction
Reason: The fix is a pure deletion of use-site enumeration that does not bear on the definition's meaning. No external channel informs whether to delete redundant prose.

## Issue 3: Naming-justification meta-prose around `R_Σ`
Reason: The required action keeps the load-bearing `R_Σ` definition and bridge lemma (both already proven internally) and strips only defensive framing sentences. Purely editorial, derivable from the ASN's own content.

## Issue 4: Duplication of the entry-state/per-state distinction in O7(c)
Reason: De-duplicating two passages that say the same thing is an internal editorial fix; the substantive content is already established in the O7(c) proof body. No channel needed.

## Issue 5: Long witness-chain example placed inside a proof body
Reason: Relocating the existing `π_0 … π_{k+1}` witness chain to the Worked Example section is reorganization of content already present and verified in the ASN. No design intent or implementation evidence is required.

## Issue 6: Defensive framing of the `Σ.B` notation
Reason: Keeping the one-line identification of `Σ.B` as ASN-0040's `s.B` and dropping the "not a relabel" defense is editorial; the identification fact is already stated and internal to the ASN.
